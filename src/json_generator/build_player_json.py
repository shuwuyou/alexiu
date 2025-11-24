import json
from pathlib import Path

import pandas as pd


# ---------------------------------------------------------
# 1. File paths
# ---------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
MODEL_DATA_DIR = BASE_DIR / "model_data"

SHAP_PATH = MODEL_DATA_DIR / "player_shap_transfer_fee_321.pkl"
SCORES_PATH = MODEL_DATA_DIR / "player_game_scores_and_values_321.pkl"
MLR_PATH = MODEL_DATA_DIR / "mlr_local_explanations_per_transfer_321.pkl"
JSONL_PATH = MODEL_DATA_DIR / "players_intersection_321.jsonl"


# ---------------------------------------------------------
# 2. Load all data once
# ---------------------------------------------------------
def load_all_data():
    """Load all model data files into DataFrames."""
    shap_df = pd.read_pickle(SHAP_PATH)
    scores_df = pd.read_pickle(SCORES_PATH)
    mlr_df = pd.read_pickle(MLR_PATH)

    # JSONL → each line is one player dict
    players_df = pd.read_json(JSONL_PATH, lines=True)

    # Make sure player_id types are consistent (very important)
    for df in (shap_df, scores_df, mlr_df, players_df):
        if "player_id" in df.columns:
            df["player_id"] = df["player_id"].astype(int)

    return shap_df, scores_df, mlr_df, players_df


# ---------------------------------------------------------
# 3. SHAP summary for one player
# ---------------------------------------------------------
def build_shap_section(player_id: int, shap_df: pd.DataFrame):
    """
    For a given player_id, read SHAP values.

    Assumptions:
    - shap_df is already 1 row per player.
    - All columns with prefix `shap_` are SHAP values.
    - 0 means "not selected" (not in top/bottom set).
    - Non-zero shap_xxx are already the features you care about.
    """
    player_shap = shap_df[shap_df["player_id"] == player_id]
    if player_shap.empty:
        return None

    # Exactly one row per player (as per your cleaning)
    row = player_shap.iloc[0]

    # All SHAP columns
    shap_cols = [c for c in player_shap.columns if c.startswith("shap_")]

    # Keep only non-zero SHAP values
    non_zero = {}
    for col in shap_cols:
        val = row[col]
        if pd.notna(val) and float(val) != 0.0:
            non_zero[col] = float(val)

    # If somehow all zero, still return metadata but with empty lists
    # (shouldn't happen if you've already filtered to top/bottom)
    # Grab transfer-level info if present in this row
    transfer_date_raw = row.get("transfer_date", None)
    transfer_date = None
    if transfer_date_raw is not None:
        transfer_date = pd.to_datetime(transfer_date_raw, errors="coerce")
        transfer_date = (
            transfer_date.strftime("%Y-%m-%d") if pd.notna(transfer_date) else None
        )

    reference_transfer = {
        "from_club_name": row.get("from_club_name"),
        "to_club_name": row.get("to_club_name"),
        "transfer_season": row.get("transfer_season"),
        "transfer_year": int(row["transfer_year"]) if "transfer_year" in row and pd.notna(row["transfer_year"]) else None,
        "transfer_date": transfer_date,
        "actual_transfer_fee": float(row.get("transfer_fee"))
        if pd.notna(row.get("transfer_fee"))
        else None,
        "predicted_transfer_fee": float(row.get("pred_transfer_fee"))
        if pd.notna(row.get("pred_transfer_fee"))
        else None,
    }

    if not non_zero:
        return {
            "reference_transfer": reference_transfer,
            "positive_features": [],
            "negative_features": [],
        }

    # Split into positive and negative (no truncation)
    positive = [(feat, val) for feat, val in non_zero.items() if val > 0]
    negative = [(feat, val) for feat, val in non_zero.items() if val < 0]

    # Sort for readability
    positive = sorted(positive, key=lambda x: x[1], reverse=True)
    negative = sorted(negative, key=lambda x: x[1])  # most negative first

    return {
        "reference_transfer": reference_transfer,
        "positive_features": [
            {
                "feature": feature.replace("shap_", ""),
                "shap_value": value,
            }
            for feature, value in positive
        ],
        "negative_features": [
            {
                "feature": feature.replace("shap_", ""),
                "shap_value": value,
            }
            for feature, value in negative
        ],
    }


# ---------------------------------------------------------
# 4. MLR coefficients section for one player
# ---------------------------------------------------------
def build_mlr_section(player_id: int, mlr_df: pd.DataFrame):
    """
    For a given player_id, collect all rows from the MLR local explanations
    table and return a list of transfers with their coefficients.

    Requirement:
    - Include ALL columns with prefix `coef_` for each transfer.
    """
    player_mlr = mlr_df[mlr_df["player_id"] == player_id].copy()
    if player_mlr.empty:
        return None

    coef_cols = [c for c in player_mlr.columns if c.startswith("coef_")]

    transfers = []
    for _, row in player_mlr.iterrows():
        transfer_date_raw = row.get("transfer_date", None)
        transfer_date = None
        if transfer_date_raw is not None:
            transfer_date = pd.to_datetime(transfer_date_raw, errors="coerce")
            transfer_date = (
                transfer_date.strftime("%Y-%m-%d") if pd.notna(transfer_date) else None
            )

        transfer_info = {
            "from_club_name": row.get("from_club_name"),
            "to_club_name": row.get("to_club_name"),
            "transfer_season": row.get("transfer_season"),
            "transfer_date": transfer_date,
            "pred_log_transfer_fee": float(row.get("pred_log_transfer_fee"))
            if pd.notna(row.get("pred_log_transfer_fee"))
            else None,
            "pred_transfer_fee": float(row.get("pred_transfer_fee"))
            if pd.notna(row.get("pred_transfer_fee"))
            else None,
            "actual_transfer_fee": float(row.get("actual_transfer_fee"))
            if pd.notna(row.get("actual_transfer_fee"))
            else None,
            "residual_log": float(row.get("residual_log"))
            if pd.notna(row.get("residual_log"))
            else None,
        }

        # All coefficients for this transfer (no filtering)
        coefs = {}
        for col in coef_cols:
            name = col.replace("coef_", "")
            value = row.get(col)
            coefs[name] = float(value) if pd.notna(value) else None

        transfer_info["coefficients"] = coefs
        transfers.append(transfer_info)

    return {"transfers": transfers}


# ---------------------------------------------------------
# 5. Time series: universal score & market value
# ---------------------------------------------------------
def build_time_series_section(player_id: int, scores_df: pd.DataFrame):
    """
    Build the time series of universal_score_100 and market_value
    for a given player_id.
    """
    player_scores = scores_df[scores_df["player_id"] == player_id].copy()
    if player_scores.empty:
        return []

    if "time" in player_scores.columns:
        player_scores["time"] = pd.to_datetime(
            player_scores["time"], errors="coerce"
        )
        player_scores = player_scores.sort_values("time")

    records = []
    for _, row in player_scores.iterrows():
        date_val = row.get("time")
        date_str = (
            date_val.strftime("%Y-%m-%d")
            if isinstance(date_val, pd.Timestamp) and pd.notna(date_val)
            else None
        )
        records.append(
            {
                "date": date_str,
                "universal_score_100": float(row.get("universal_score_100"))
                if pd.notna(row.get("universal_score_100"))
                else None,
                "market_value": float(row.get("market_value"))
                if pd.notna(row.get("market_value"))
                else None,
            }
        )

    return records


# ---------------------------------------------------------
# 6. Combine everything into one "massive" JSON
# ---------------------------------------------------------
def build_player_massive_json(
    player_id: int,
    shap_df: pd.DataFrame,
    scores_df: pd.DataFrame,
    mlr_df: pd.DataFrame,
    players_df: pd.DataFrame,
):
    """
    Combine:
      - original players_intersection JSONL record
      - SHAP section (non-zero shap_* features only)
      - MLR coefficients section (all coef_* columns)
      - time series of score/value
    into one big dictionary.
    """
    # Start with the original JSONL entry if available
    player_row = players_df[players_df["player_id"] == player_id]
    if not player_row.empty:
        base = player_row.iloc[0].to_dict()
    else:
        # Fallback if player not in JSONL
        base = {"player_id": player_id}

    base["shap_summary"] = build_shap_section(player_id, shap_df)
    base["mlr_coefficients"] = build_mlr_section(player_id, mlr_df)
    base["performance_time_series"] = build_time_series_section(player_id, scores_df)

    return base


# ---------------------------------------------------------
# 7. CLI entry point
# ---------------------------------------------------------
if __name__ == "__main__":
    import argparse

    shap_df, scores_df, mlr_df, players_df = load_all_data()

    parser = argparse.ArgumentParser(
        description="Build a massive JSON profile for a given player_id."
    )
    parser.add_argument("player_id", type=int, help="Player ID")
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default=None,
        help="Output JSON file path (if omitted, print to stdout).",
    )
    args = parser.parse_args()

    result = build_player_massive_json(
        args.player_id, shap_df, scores_df, mlr_df, players_df
    )

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))
