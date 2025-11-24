"""Player search and JSON generation routes."""

from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
import pandas as pd
import numpy as np
import json
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))

from src.json_generator.build_player_json import (
    load_all_data,
    build_player_massive_json
)

router = APIRouter(prefix="/api/players", tags=["players"])

# Load players.csv for search
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
PLAYERS_CSV = BASE_DIR / "data" / "players.csv"

# Cache the data globally (loaded once on startup)
_players_search_df = None
_shap_df = None
_scores_df = None
_mlr_df = None
_players_df = None
_available_player_ids = None


def get_players_search_df():
    """Load and cache the players.csv for searching."""
    global _players_search_df
    if _players_search_df is None:
        _players_search_df = pd.read_csv(PLAYERS_CSV)
        # Ensure player_id is int
        _players_search_df['player_id'] = _players_search_df['player_id'].astype(int)
    return _players_search_df


def get_model_data():
    """Load and cache the model data."""
    global _shap_df, _scores_df, _mlr_df, _players_df, _available_player_ids
    if _shap_df is None:
        _shap_df, _scores_df, _mlr_df, _players_df = load_all_data()
        _available_player_ids = set(_players_df['player_id'].tolist())
    return _shap_df, _scores_df, _mlr_df, _players_df


def get_available_player_ids():
    """Get set of player IDs that have model data."""
    global _available_player_ids
    if _available_player_ids is None:
        get_model_data()  # This will populate _available_player_ids
    return _available_player_ids


@router.get("/search")
async def search_players(
    query: str = Query(..., min_length=1, description="Search query (player name or ID)"),
    limit: int = Query(10, ge=1, le=50, description="Maximum number of results")
) -> List[dict]:
    """
    Search for players by name or ID with fuzzy matching.
    Returns a list of matching players with basic info.
    """
    players_df = get_players_search_df()
    
    # Try to parse as player_id first
    try:
        player_id = int(query)
        matches = players_df[players_df['player_id'] == player_id]
    except ValueError:
        # Search by name (case-insensitive, partial match)
        query_lower = query.lower()
        matches = players_df[
            players_df['name'].str.lower().str.contains(query_lower, na=False) |
            players_df['first_name'].str.lower().str.contains(query_lower, na=False) |
            players_df['last_name'].str.lower().str.contains(query_lower, na=False)
        ]
    
    # Filter to only players with model data available
    available_ids = get_available_player_ids()
    matches = matches[matches['player_id'].isin(available_ids)]
    
    # Limit results
    matches = matches.head(limit)
    
    # Convert to list of dicts
    results = []
    for _, row in matches.iterrows():
        result_dict = {
            "player_id": int(row['player_id']),
            "name": row['name'],
            "first_name": row.get('first_name', ''),
            "last_name": row.get('last_name', ''),
            "position": row.get('position', ''),
            "current_club_name": row.get('current_club_name', ''),
            "nationality": row.get('country_of_citizenship', ''),
            "date_of_birth": str(row.get('date_of_birth', '')),
            "market_value_in_eur": float(row['market_value_in_eur']) if pd.notna(row.get('market_value_in_eur')) else None,
        }
        # Clean any remaining NaN values
        results.append(clean_json_data(result_dict))
    
    return results


def clean_json_data(obj):
    """
    Recursively clean data by converting NaN, inf, and -inf to None.
    This makes the data JSON-compliant.
    """
    if isinstance(obj, dict):
        return {key: clean_json_data(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [clean_json_data(item) for item in obj]
    elif isinstance(obj, (float, np.floating)):
        # Check for NaN or infinity
        if np.isnan(obj) or np.isinf(obj):
            return None
        return float(obj)  # Convert numpy float to Python float
    elif isinstance(obj, (np.integer, np.int64, np.int32)):
        return int(obj)  # Convert numpy int to Python int
    elif pd.isna(obj):
        return None
    elif obj is None:
        return None
    else:
        return obj


@router.get("/generate/{player_id}")
async def generate_player_json(player_id: int):
    """
    Generate complete player JSON data including SHAP, MLR, and time series.
    This is the json_generator pipeline endpoint.
    """
    try:
        # Load model data
        shap_df, scores_df, mlr_df, players_df = get_model_data()
        
        # Check if player exists in model data
        if player_id not in players_df['player_id'].values:
            # Try to get player name from search database
            search_df = get_players_search_df()
            player_row = search_df[search_df['player_id'] == player_id]
            player_name = player_row.iloc[0]['name'] if not player_row.empty else f"ID {player_id}"
            
            raise HTTPException(
                status_code=404,
                detail=f"Player '{player_name}' exists in database but doesn't have ML model data available. Only {len(players_df)} players have complete analysis data."
            )
        
        # Build the massive JSON
        result = build_player_massive_json(
            player_id, shap_df, scores_df, mlr_df, players_df
        )
        
        # Clean NaN values to make it JSON-compliant
        cleaned_result = clean_json_data(result)
        
        return cleaned_result
        
    except FileNotFoundError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Model data files not found: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating player JSON: {str(e)}"
        )


@router.get("/info/{player_id}")
async def get_player_info(player_id: int):
    """Get basic player information from players.csv."""
    players_df = get_players_search_df()
    
    player_row = players_df[players_df['player_id'] == player_id]
    
    if player_row.empty:
        raise HTTPException(
            status_code=404,
            detail=f"Player with ID {player_id} not found"
        )
    
    row = player_row.iloc[0]
    player_info = {
        "player_id": int(row['player_id']),
        "name": row['name'],
        "first_name": row.get('first_name', ''),
        "last_name": row.get('last_name', ''),
        "position": row.get('position', ''),
        "sub_position": row.get('sub_position', ''),
        "current_club_name": row.get('current_club_name', ''),
        "nationality": row.get('country_of_citizenship', ''),
        "date_of_birth": str(row.get('date_of_birth', '')),
        "height_in_cm": float(row['height_in_cm']) if pd.notna(row.get('height_in_cm')) else None,
        "foot": row.get('foot', ''),
        "market_value_in_eur": float(row['market_value_in_eur']) if pd.notna(row.get('market_value_in_eur')) else None,
        "highest_market_value_in_eur": float(row['highest_market_value_in_eur']) if pd.notna(row.get('highest_market_value_in_eur')) else None,
        "image_url": row.get('image_url', ''),
    }
    # Clean any remaining NaN values
    return clean_json_data(player_info)
