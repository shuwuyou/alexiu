
import json
import numpy as np
from datetime import datetime
from tqdm import tqdm

# ---------------------------------------------------------
# Helpers
# ---------------------------------------------------------

def parse_date(d):
    return datetime.strptime(d.split()[0], "%Y-%m-%d")


def linear_slope(dates, values):
    """Return slope of values over time (normalized by days)."""
    if len(values) < 2:
        return 0.0
    x = np.array([(d - dates[0]).days for d in dates])
    y = np.array(values)
    try:
        m = np.polyfit(x, y, 1)[0]
    except:
        m = 0.0
    return m


def normalize_score(x, low, high, out_low, out_high):
    """Scale x from [low, high] to [out_low, out_high]."""
    if high == low:
        return (out_low + out_high) / 2
    x = max(min(x, high), low)
    return out_low + (x - low) * (out_high - out_low) / (high - low)


# ---------------------------------------------------------
# Component A — Market Value Trajectory (0–40)
# ---------------------------------------------------------

def compute_market_value_score(player):
    history = player.get("valuation_history", [])
    if len(history) < 4:
        return 20.0  # neutral

    # Use last 2 years only
    history_sorted = sorted(history, key=lambda x: x["date"])
    last_entries = history_sorted[-8:]  # roughly 24–30 months in TM data

    dates = [parse_date(h["date"]) for h in last_entries]
    values = [h["market_value_in_eur"] for h in last_entries]

    slope = linear_slope(dates, values)

    # Value slope ranges vary wildly; clamp small range
    score = normalize_score(slope,
                            low=-15000,   # strongly negative
                            high=15000,   # strongly positive
                            out_low=0,
                            out_high=40)
    return score


# ---------------------------------------------------------
# Component B — Performance Momentum (0–40)
# ---------------------------------------------------------

def compute_performance_momentum(player):
    perf = player.get("performance_time_series", [])
    recent = player.get("recent_form_last_10_games", {}).get("summary", {})

    # ---- B1: universal score slope (0–25)
    if len(perf) > 5:
        perf_sorted = sorted(perf, key=lambda x: x["date"])
        dates = [parse_date(p["date"]) for p in perf_sorted]
        uscores = [p["universal_score_100"] for p in perf_sorted]
        slope = linear_slope(dates, uscores)
        score_trend = normalize_score(slope,
                                      low=-0.5,
                                      high=0.5,
                                      out_low=0,
                                      out_high=25)
    else:
        score_trend = 12.5

    # ---- B2: recent form (0–15)
    mins = recent.get("minutes_played", 0)
    goals = recent.get("goals", 0)
    assists = recent.get("assists", 0)

    # simple formula
    recent_index = (
        (mins / 900) * 0.5 +       # at least playing matters
        (goals * 0.3) +
        (assists * 0.2)
    )

    score_recent = normalize_score(recent_index,
                                   low=0,
                                   high=1.2,  # good performance
                                   out_low=0,
                                   out_high=15)

    return score_trend + score_recent


# ---------------------------------------------------------
# Component C — Age (0–20)
# ---------------------------------------------------------

def compute_age_score(player):
    age = player.get("basic_info", {}).get("age_at_reference_date", None)
    if age is None:
        return 10.0

    # peak at 20–23; decline after 28; heavy decline after 32
    if age <= 23:
        return 20
    elif age <= 28:
        return normalize_score(age, 23, 28, 20, 12)
    elif age <= 32:
        return normalize_score(age, 28, 32, 12, 6)
    else:
        return max(0, 6 - (age - 32) * 1.2)


# ---------------------------------------------------------
# Final composer
# ---------------------------------------------------------

def compute_growth_potential(player):
    A = compute_market_value_score(player)        # 0–40
    B = compute_performance_momentum(player)      # 0–40
    C = compute_age_score(player)                 # 0–20
    return round(A + B + C, 2)


# ---------------------------------------------------------
# Main: process JSONL
# ---------------------------------------------------------

def process_jsonl(input_path, output_path):
    with open(input_path, "r") as f_in, open(output_path, "w") as f_out:
        for line in tqdm(f_in, desc="Processing players"):
            p = json.loads(line)

            score = compute_growth_potential(p)

            # write back into basic_info
            if "basic_info" not in p:
                p["basic_info"] = {}
            p["basic_info"]["growth_potential_score"] = score

            f_out.write(json.dumps(p) + "\n")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, required=True,
                        help="Path to players.jsonl")
    parser.add_argument("--output", type=str, default="players_with_growth.jsonl",
                        help="Output JSONL path")
    args = parser.parse_args()

    process_jsonl(args.input, args.output)
    print("Done.")
