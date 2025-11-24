"""Test analysis agent with real player data (Jonas Hofmann example)."""

import asyncio
import json
from src.llm.agents.report.analysis_agent import AnalysisAgent


# Real player data for Jonas Hofmann (7161)
REAL_PLAYER_DATA = {
  "player_id": 7161,
  "name": "Jonas Hofmann",
  "basic_info": {
    "player_id": 7161,
    "name": "Jonas Hofmann",
    "date_of_birth": "1992-07-14",
    "age_at_reference_date": 32,
    "country_of_birth": "Germany",
    "city_of_birth": "Heidelberg",
    "nationality": "Germany",
    "primary_position": "Midfield",
    "secondary_position": "Attacking Midfield",
    "preferred_foot": "right",
    "height_cm": 176,
    "current_club_id": 15,
    "current_club_name": "Bayer 04 Leverkusen Fußball",
    "current_club_league_id": "L1",
    "market_value_eur_latest": 3000000.0,
    "highest_market_value_eur": 16000000.0,
    "contract_expiration_date": "2027-06-30 00:00:00",
    "agent_name": "Dr. Marco Gutfleisch",
    "last_season_in_db": 2024,
    "image_url": "https://img.a.transfermarkt.technology/portrait/header/7161-1689710421.jpg?lm=1"
  },
  "career_totals": {
    "matches_played": 342,
    "appearances_count": 342,
    "minutes_played": 20754,
    "goals": 66,
    "assists": 80,
    "shots": None,
    "shots_on_target": None,
    "yellow_cards": 15,
    "red_cards": 0,
    "fouls": None,
    "offsides": None,
    "touches": None,
    "avg_rating": None,
    "goals_per_90": 0.2862098873,
    "assists_per_90": 0.3469210755
  },
  "season_totals": [],
  "last_season_stats": None,
  "previous_season_stats": None,
  "recent_form_last_10_games": {
    "summary": {
      "matches_played": 10,
      "minutes_played": 330,
      "goals": 0,
      "assists": 2,
      "avg_rating": None
    },
    "games": [
      {
        "date": "2024-10-23 00:00:00",
        "game_id": 4445145,
        "player_club_id": 15,
        "minutes_played": 90,
        "goals": 0,
        "assists": 1,
        "yellow_cards": 0,
        "red_cards": 0,
        "club_name": "Bayer 04 Leverkusen Fußball"
      },
      {
        "date": "2024-10-29 00:00:00",
        "game_id": 4446799,
        "player_club_id": 15,
        "minutes_played": 79,
        "goals": 0,
        "assists": 0,
        "yellow_cards": 0,
        "red_cards": 0,
        "club_name": "Bayer 04 Leverkusen Fußball"
      },
      {
        "date": "2024-11-01 00:00:00",
        "game_id": 4373437,
        "player_club_id": 15,
        "minutes_played": 36,
        "goals": 0,
        "assists": 0,
        "yellow_cards": 0,
        "red_cards": 0,
        "club_name": "Bayer 04 Leverkusen Fußball"
      },
      {
        "date": "2024-11-05 00:00:00",
        "game_id": 4445048,
        "player_club_id": 15,
        "minutes_played": 17,
        "goals": 0,
        "assists": 0,
        "yellow_cards": 0,
        "red_cards": 0,
        "club_name": "Bayer 04 Leverkusen Fußball"
      },
      {
        "date": "2024-11-09 00:00:00",
        "game_id": 4373462,
        "player_club_id": 15,
        "minutes_played": 64,
        "goals": 0,
        "assists": 0,
        "yellow_cards": 0,
        "red_cards": 0,
        "club_name": "Bayer 04 Leverkusen Fußball"
      },
      {
        "date": "2025-01-18 00:00:00",
        "game_id": 4373590,
        "player_club_id": 15,
        "minutes_played": 9,
        "goals": 0,
        "assists": 0,
        "yellow_cards": 0,
        "red_cards": 0,
        "club_name": "Bayer 04 Leverkusen Fußball"
      },
      {
        "date": "2025-01-21 00:00:00",
        "game_id": 4445073,
        "player_club_id": 15,
        "minutes_played": 22,
        "goals": 0,
        "assists": 0,
        "yellow_cards": 0,
        "red_cards": 0,
        "club_name": "Bayer 04 Leverkusen Fußball"
      },
      {
        "date": "2025-01-29 00:00:00",
        "game_id": 4445071,
        "player_club_id": 15,
        "minutes_played": 1,
        "goals": 0,
        "assists": 0,
        "yellow_cards": 0,
        "red_cards": 0,
        "club_name": "Bayer 04 Leverkusen Fußball"
      },
      {
        "date": "2025-03-01 00:00:00",
        "game_id": 4373709,
        "player_club_id": 15,
        "minutes_played": 7,
        "goals": 0,
        "assists": 0,
        "yellow_cards": 0,
        "red_cards": 0,
        "club_name": "Bayer 04 Leverkusen Fußball"
      },
      {
        "date": "2025-04-05 00:00:00",
        "game_id": 4373780,
        "player_club_id": 15,
        "minutes_played": 5,
        "goals": 0,
        "assists": 1,
        "yellow_cards": 0,
        "red_cards": 0,
        "club_name": "Bayer 04 Leverkusen Fußball"
      }
    ]
  },
  "valuation_history": [
    {
      "date": "2011-07-01 00:00:00",
      "market_value_in_eur": 50000,
      "current_club_id": 15,
      "player_club_domestic_competition_id": "L1"
    },
    {
      "date": "2012-01-20 00:00:00",
      "market_value_in_eur": 100000,
      "current_club_id": 15,
      "player_club_domestic_competition_id": "L1"
    },
    {
      "date": "2012-02-06 00:00:00",
      "market_value_in_eur": 125000,
      "current_club_id": 15,
      "player_club_domestic_competition_id": "L1"
    },
    {
      "date": "2012-07-05 00:00:00",
      "market_value_in_eur": 150000,
      "current_club_id": 15,
      "player_club_domestic_competition_id": "L1"
    },
    {
      "date": "2012-10-23 00:00:00",
      "market_value_in_eur": 200000,
      "current_club_id": 15,
      "player_club_domestic_competition_id": "L1"
    },
    {
      "date": "2013-06-30 00:00:00",
      "market_value_in_eur": 500000,
      "current_club_id": 15,
      "player_club_domestic_competition_id": "L1"
    },
    {
      "date": "2013-08-27 00:00:00",
      "market_value_in_eur": 1000000,
      "current_club_id": 15,
      "player_club_domestic_competition_id": "L1"
    },
    {
      "date": "2013-11-05 00:00:00",
      "market_value_in_eur": 3000000,
      "current_club_id": 15,
      "player_club_domestic_competition_id": "L1"
    },
    {
      "date": "2014-07-10 00:00:00",
      "market_value_in_eur": 4000000,
      "current_club_id": 15,
      "player_club_domestic_competition_id": "L1"
    },
    {
      "date": "2015-02-04 00:00:00",
      "market_value_in_eur": 4000000,
      "current_club_id": 15,
      "player_club_domestic_competition_id": "L1"
    },
    {
      "date": "2015-07-01 00:00:00",
      "market_value_in_eur": 4000000,
      "current_club_id": 15,
      "player_club_domestic_competition_id": "L1"
    },
    {
      "date": "2016-02-15 00:00:00",
      "market_value_in_eur": 6000000,
      "current_club_id": 15,
      "player_club_domestic_competition_id": "L1"
    },
    {
      "date": "2016-07-22 00:00:00",
      "market_value_in_eur": 5000000,
      "current_club_id": 15,
      "player_club_domestic_competition_id": "L1"
    },
    {
      "date": "2016-10-13 00:00:00",
      "market_value_in_eur": 4000000,
      "current_club_id": 15,
      "player_club_domestic_competition_id": "L1"
    },
    {
      "date": "2017-02-07 00:00:00",
      "market_value_in_eur": 3500000,
      "current_club_id": 15,
      "player_club_domestic_competition_id": "L1"
    },
    {
      "date": "2017-06-19 00:00:00",
      "market_value_in_eur": 3500000,
      "current_club_id": 15,
      "player_club_domestic_competition_id": "L1"
    },
    {
      "date": "2017-12-28 00:00:00",
      "market_value_in_eur": 3000000,
      "current_club_id": 15,
      "player_club_domestic_competition_id": "L1"
    },
    {
      "date": "2018-06-05 00:00:00",
      "market_value_in_eur": 3000000,
      "current_club_id": 15,
      "player_club_domestic_competition_id": "L1"
    },
    {
      "date": "2018-10-22 00:00:00",
      "market_value_in_eur": 8000000,
      "current_club_id": 15,
      "player_club_domestic_competition_id": "L1"
    },
    {
      "date": "2018-12-18 00:00:00",
      "market_value_in_eur": 12000000,
      "current_club_id": 15,
      "player_club_domestic_competition_id": "L1"
    },
    {
      "date": "2019-06-05 00:00:00",
      "market_value_in_eur": 9000000,
      "current_club_id": 15,
      "player_club_domestic_competition_id": "L1"
    },
    {
      "date": "2019-12-17 00:00:00",
      "market_value_in_eur": 9000000,
      "current_club_id": 15,
      "player_club_domestic_competition_id": "L1"
    },
    {
      "date": "2020-04-08 00:00:00",
      "market_value_in_eur": 7000000,
      "current_club_id": 15,
      "player_club_domestic_competition_id": "L1"
    },
    {
      "date": "2020-07-08 00:00:00",
      "market_value_in_eur": 9000000,
      "current_club_id": 15,
      "player_club_domestic_competition_id": "L1"
    },
    {
      "date": "2020-11-26 00:00:00",
      "market_value_in_eur": 14000000,
      "current_club_id": 15,
      "player_club_domestic_competition_id": "L1"
    },
    {
      "date": "2021-02-10 00:00:00",
      "market_value_in_eur": 16000000,
      "current_club_id": 15,
      "player_club_domestic_competition_id": "L1"
    },
    {
      "date": "2021-06-01 00:00:00",
      "market_value_in_eur": 16000000,
      "current_club_id": 15,
      "player_club_domestic_competition_id": "L1"
    },
    {
      "date": "2021-12-22 00:00:00",
      "market_value_in_eur": 16000000,
      "current_club_id": 15,
      "player_club_domestic_competition_id": "L1"
    },
    {
      "date": "2022-06-09 00:00:00",
      "market_value_in_eur": 13000000,
      "current_club_id": 15,
      "player_club_domestic_competition_id": "L1"
    },
    {
      "date": "2022-11-09 00:00:00",
      "market_value_in_eur": 13000000,
      "current_club_id": 15,
      "player_club_domestic_competition_id": "L1"
    },
    {
      "date": "2023-06-22 00:00:00",
      "market_value_in_eur": 13000000,
      "current_club_id": 15,
      "player_club_domestic_competition_id": "L1"
    },
    {
      "date": "2023-12-14 00:00:00",
      "market_value_in_eur": 13000000,
      "current_club_id": 15,
      "player_club_domestic_competition_id": "L1"
    },
    {
      "date": "2024-05-29 00:00:00",
      "market_value_in_eur": 10000000,
      "current_club_id": 15,
      "player_club_domestic_competition_id": "L1"
    },
    {
      "date": "2024-10-09 00:00:00",
      "market_value_in_eur": 7000000,
      "current_club_id": 15,
      "player_club_domestic_competition_id": "L1"
    },
    {
      "date": "2024-12-20 00:00:00",
      "market_value_in_eur": 5000000,
      "current_club_id": 15,
      "player_club_domestic_competition_id": "L1"
    },
    {
      "date": "2025-03-27 00:00:00",
      "market_value_in_eur": 3000000,
      "current_club_id": 15,
      "player_club_domestic_competition_id": "L1"
    }
  ],
  "transfer_history": [
    {
      "transfer_date": "2004-07-01 00:00:00",
      "transfer_season": "04/05",
      "from_club_id": 42324,
      "to_club_id": 17474,
      "from_club_name": "FC Rot Yth.",
      "to_club_name": "Hoffenheim Yth.",
      "transfer_fee": 0.0,
      "market_value_in_eur": None
    },
    {
      "transfer_date": "2007-07-01 00:00:00",
      "transfer_season": "07/08",
      "from_club_id": 17474,
      "to_club_id": 21082,
      "from_club_name": "Hoffenheim Yth.",
      "to_club_name": "Hoffenheim U17",
      "transfer_fee": None,
      "market_value_in_eur": None
    },
    {
      "transfer_date": "2009-07-01 00:00:00",
      "transfer_season": "09/10",
      "from_club_id": 21082,
      "to_club_id": 8925,
      "from_club_name": "Hoffenheim U17",
      "to_club_name": "Hoffenheim U19",
      "transfer_fee": None,
      "market_value_in_eur": None
    },
    {
      "transfer_date": "2011-07-01 00:00:00",
      "transfer_season": "11/12",
      "from_club_id": 8925,
      "to_club_id": 17,
      "from_club_name": "Hoffenheim U19",
      "to_club_name": "B. Dortmund II",
      "transfer_fee": 0.0,
      "market_value_in_eur": 50000.0
    },
    {
      "transfer_date": "2013-07-01 00:00:00",
      "transfer_season": "13/14",
      "from_club_id": 17,
      "to_club_id": 16,
      "from_club_name": "B. Dortmund II",
      "to_club_name": "Bor. Dortmund",
      "transfer_fee": None,
      "market_value_in_eur": 500000.0
    },
    {
      "transfer_date": "2014-09-01 00:00:00",
      "transfer_season": "14/15",
      "from_club_id": 16,
      "to_club_id": 39,
      "from_club_name": "Bor. Dortmund",
      "to_club_name": "1.FSV Mainz 05",
      "transfer_fee": 0.0,
      "market_value_in_eur": 4000000.0
    },
    {
      "transfer_date": "2015-06-30 00:00:00",
      "transfer_season": "14/15",
      "from_club_id": 39,
      "to_club_id": 16,
      "from_club_name": "1.FSV Mainz 05",
      "to_club_name": "Bor. Dortmund",
      "transfer_fee": 0.0,
      "market_value_in_eur": 4000000.0
    },
    {
      "transfer_date": "2016-01-01 00:00:00",
      "transfer_season": "15/16",
      "from_club_id": 16,
      "to_club_id": 18,
      "from_club_name": "Bor. Dortmund",
      "to_club_name": "Bor. M'gladbach",
      "transfer_fee": 8000000.0,
      "market_value_in_eur": 4000000.0
    },
    {
      "transfer_date": "2023-07-05 00:00:00",
      "transfer_season": "23/24",
      "from_club_id": 18,
      "to_club_id": 15,
      "from_club_name": "Bor. M'gladbach",
      "to_club_name": "B. Leverkusen",
      "transfer_fee": 10000000.0,
      "market_value_in_eur": 13000000.0
    }
  ],
  "shap_summary": {
    "reference_transfer": {
      "from_club_name": "Bor. Dortmund",
      "to_club_name": "Bor. M'gladbach",
      "transfer_season": "15/16",
      "transfer_year": 2016,
      "transfer_date": "2016-01-01",
      "actual_transfer_fee": 8000000.0,
      "predicted_transfer_fee": 4128316.75
    },
    "positive_features": [
      {
        "feature": "market_value_in_eur",
        "shap_value": 0.6024075150489807
      },
      {
        "feature": "log_market_value_in_eur",
        "shap_value": 0.1622476130723953
      },
      {
        "feature": "transfer_year",
        "shap_value": 0.0327583439648151
      },
      {
        "feature": "contract_years_left",
        "shap_value": 0.0265571493655443
      },
      {
        "feature": "to_average_age",
        "shap_value": 0.0247408673167228
      }
    ],
    "negative_features": [
      {
        "feature": "games_365",
        "shap_value": -0.025495296344161
      },
      {
        "feature": "age_at_transfer",
        "shap_value": -0.0190003160387277
      },
      {
        "feature": "minutes_per_game",
        "shap_value": -0.0048407348804175
      },
      {
        "feature": "sub_position_Centre-Back",
        "shap_value": -0.0040614455938339
      },
      {
        "feature": "from_squad_size",
        "shap_value": -0.0036972274538129
      }
    ]
  },
  "mlr_coefficients": {
    "transfers": [
      {
        "from_club_name": "Bor. M'gladbach",
        "to_club_name": "B. Leverkusen",
        "transfer_season": "23/24",
        "transfer_date": "2023-07-05",
        "pred_log_transfer_fee": 15.823264826612714,
        "pred_transfer_fee": 7446575.547394338,
        "actual_transfer_fee": 10000000.0,
        "residual_log": 0.2948308243456061,
        "coefficients": {
          "height_in_cm_c": -0.0943639941563905,
          "age_at_transfer_c": -0.5624874614277339,
          "contract_years_left": 0.2064574048900203,
          "from_foreigners_percentage": 0.267404456970704,
          "to_foreigners_percentage": 0.3996941500628093,
          "to_squad_size": -0.2545936117905643,
          "to_average_age": 0.688865328363224,
          "minutes_365": 0.0830136152000163,
          "goals_per90": 0.0592894605442224,
          "assists_per90": 0.0338884408172122,
          "cards_per90": 0.0066847748833452,
          "log_market_value_in_eur": 15.648127289595024,
          "transfer_year_c": 0.0717520704403174,
          "intercept": -0.7304670977794925
        }
      }
    ]
  },
  "performance_time_series": [
    {
      "date": "2012-12-16",
      "universal_score_100": 19.04761904761905,
      "market_value": 200000.0
    },
    {
      "date": "2013-04-06",
      "universal_score_100": 23.80952380952381,
      "market_value": 200000.0
    },
    {
      "date": "2013-04-27",
      "universal_score_100": 19.04761904761905,
      "market_value": 200000.0
    },
    {
      "date": "2013-08-03",
      "universal_score_100": 47.61904761904761,
      "market_value": 500000.0
    },
    {
      "date": "2013-08-10",
      "universal_score_100": 33.33333333333333,
      "market_value": 500000.0
    },
    {
      "date": "2013-08-18",
      "universal_score_100": 52.38095238095237,
      "market_value": 500000.0
    },
    {
      "date": "2013-08-23",
      "universal_score_100": 19.04761904761905,
      "market_value": 500000.0
    },
    {
      "date": "2013-09-14",
      "universal_score_100": 19.04761904761905,
      "market_value": 1000000.0
    },
    {
      "date": "2013-09-18",
      "universal_score_100": 19.04761904761905,
      "market_value": 1000000.0
    },
    {
      "date": "2013-09-21",
      "universal_score_100": 19.04761904761905,
      "market_value": 1000000.0
    },
    {
      "date": "2013-09-24",
      "universal_score_100": 27.450980392156865,
      "market_value": 1000000.0
    },
    {
      "date": "2013-09-28",
      "universal_score_100": 33.33333333333333,
      "market_value": 1000000.0
    },
    {
      "date": "2013-10-01",
      "universal_score_100": 19.04761904761905,
      "market_value": 1000000.0
    },
    {
      "date": "2013-10-05",
      "universal_score_100": 19.04761904761905,
      "market_value": 1000000.0
    },
    {
      "date": "2013-10-19",
      "universal_score_100": 19.04761904761905,
      "market_value": 1000000.0
    },
    {
      "date": "2013-10-22",
      "universal_score_100": 19.04761904761905,
      "market_value": 1000000.0
    },
    {
      "date": "2013-10-26",
      "universal_score_100": 19.04761904761905,
      "market_value": 1000000.0
    },
    {
      "date": "2013-11-06",
      "universal_score_100": 19.04761904761905,
      "market_value": 3000000.0
    },
    {
      "date": "2013-11-09",
      "universal_score_100": 19.04761904761905,
      "market_value": 3000000.0
    },
    {
      "date": "2013-11-23",
      "universal_score_100": 19.04761904761905,
      "market_value": 3000000.0
    },
    {
      "date": "2013-12-03",
      "universal_score_100": 30.15873015873016,
      "market_value": 3000000.0
    },
    {
      "date": "2013-12-07",
      "universal_score_100": 19.04761904761905,
      "market_value": 3000000.0
    },
    {
      "date": "2013-12-11",
      "universal_score_100": 19.04761904761905,
      "market_value": 3000000.0
    },
    {
      "date": "2013-12-14",
      "universal_score_100": 19.04761904761905,
      "market_value": 3000000.0
    },
    {
      "date": "2013-12-21",
      "universal_score_100": 19.04761904761905,
      "market_value": 3000000.0
    },
    {
      "date": "2014-02-08",
      "universal_score_100": 33.33333333333333,
      "market_value": 3000000.0
    },
    {
      "date": "2014-02-11",
      "universal_score_100": 19.04761904761905,
      "market_value": 3000000.0
    },
    {
      "date": "2014-02-15",
      "universal_score_100": 19.04761904761905,
      "market_value": 3000000.0
    },
    {
      "date": "2014-02-22",
      "universal_score_100": 19.04761904761905,
      "market_value": 3000000.0
    },
    {
      "date": "2014-02-25",
      "universal_score_100": 19.04761904761905,
      "market_value": 3000000.0
    },
    {
      "date": "2014-03-01",
      "universal_score_100": 33.33333333333333,
      "market_value": 3000000.0
    },
    {
      "date": "2014-03-09",
      "universal_score_100": 19.04761904761905,
      "market_value": 3000000.0
    },
    {
      "date": "2014-03-15",
      "universal_score_100": 19.04761904761905,
      "market_value": 3000000.0
    },
    {
      "date": "2014-03-19",
      "universal_score_100": 19.04761904761905,
      "market_value": 3000000.0
    },
    {
      "date": "2014-03-22",
      "universal_score_100": 19.04761904761905,
      "market_value": 3000000.0
    },
    {
      "date": "2014-03-29",
      "universal_score_100": 24.686716791979947,
      "market_value": 3000000.0
    },
    {
      "date": "2014-04-02",
      "universal_score_100": 19.04761904761905,
      "market_value": 3000000.0
    },
    {
      "date": "2014-04-12",
      "universal_score_100": 25.960061443932418,
      "market_value": 3000000.0
    },
    {
      "date": "2014-04-19",
      "universal_score_100": 19.04761904761905,
      "market_value": 3000000.0
    },
    {
      "date": "2014-04-26",
      "universal_score_100": 19.04761904761905,
      "market_value": 3000000.0
    },
    {
      "date": "2014-05-03",
      "universal_score_100": 19.04761904761905,
      "market_value": 3000000.0
    },
    {
      "date": "2014-05-17",
      "universal_score_100": 19.04761904761905,
      "market_value": 3000000.0
    },
    {
      "date": "2014-08-13",
      "universal_score_100": 19.04761904761905,
      "market_value": 4000000.0
    },
    {
      "date": "2014-08-23",
      "universal_score_100": 19.04761904761905,
      "market_value": 4000000.0
    },
    {
      "date": "2014-08-29",
      "universal_score_100": 19.04761904761905,
      "market_value": 4000000.0
    },
    {
      "date": "2014-09-13",
      "universal_score_100": 19.04761904761905,
      "market_value": 4000000.0
    },
    {
      "date": "2014-09-20",
      "universal_score_100": 19.04761904761905,
      "market_value": 4000000.0
    },
    {
      "date": "2014-09-23",
      "universal_score_100": 25.615763546798032,
      "market_value": 4000000.0
    },
    {
      "date": "2014-09-26",
      "universal_score_100": 19.04761904761905,
      "market_value": 4000000.0
    },
    {
      "date": "2014-10-05",
      "universal_score_100": 26.373626373626376,
      "market_value": 4000000.0
    },
    {
      "date": "2014-10-18",
      "universal_score_100": 28.57142857142857,
      "market_value": 4000000.0
    },
    {
      "date": "2015-02-13",
      "universal_score_100": 19.04761904761905,
      "market_value": 4000000.0
    },
    {
      "date": "2015-02-28",
      "universal_score_100": 19.04761904761905,
      "market_value": 4000000.0
    },
    {
      "date": "2015-03-07",
      "universal_score_100": 15.873015873015875,
      "market_value": 4000000.0
    },
    {
      "date": "2015-03-14",
      "universal_score_100": 19.04761904761905,
      "market_value": 4000000.0
    },
    {
      "date": "2015-07-30",
      "universal_score_100": 27.705627705627705,
      "market_value": 4000000.0
    },
    {
      "date": "2015-08-06",
      "universal_score_100": 33.33333333333333,
      "market_value": 4000000.0
    },
    {
      "date": "2015-08-09",
      "universal_score_100": 19.04761904761905,
      "market_value": 4000000.0
    },
    {
      "date": "2015-08-23",
      "universal_score_100": 33.33333333333333,
      "market_value": 4000000.0
    },
    {
      "date": "2015-08-27",
      "universal_score_100": 23.80952380952381,
      "market_value": 4000000.0
    },
    {
      "date": "2015-08-30",
      "universal_score_100": 19.04761904761905,
      "market_value": 4000000.0
    },
    {
      "date": "2015-09-12",
      "universal_score_100": 26.190476190476183,
      "market_value": 4000000.0
    },
    {
      "date": "2015-09-20",
      "universal_score_100": 28.11791383219954,
      "market_value": 4000000.0
    },
    {
      "date": "2015-09-23",
      "universal_score_100": 19.04761904761905,
      "market_value": 4000000.0
    },
    {
      "date": "2015-10-01",
      "universal_score_100": 19.04761904761905,
      "market_value": 4000000.0
    },
    {
      "date": "2015-10-22",
      "universal_score_100": 19.04761904761905,
      "market_value": 4000000.0
    },
    {
      "date": "2015-11-26",
      "universal_score_100": 19.04761904761905,
      "market_value": 4000000.0
    },
    {
      "date": "2015-12-05",
      "universal_score_100": 19.04761904761905,
      "market_value": 4000000.0
    },
    {
      "date": "2015-12-19",
      "universal_score_100": 19.04761904761905,
      "market_value": 4000000.0
    },
    {
      "date": "2016-01-23",
      "universal_score_100": 19.04761904761905,
      "market_value": 4000000.0
    },
    {
      "date": "2016-01-29",
      "universal_score_100": 19.04761904761905,
      "market_value": 4000000.0
    },
    {
      "date": "2016-02-14",
      "universal_score_100": 19.04761904761905,
      "market_value": 4000000.0
    },
    {
      "date": "2016-02-20",
      "universal_score_100": 19.04761904761905,
      "market_value": 6000000.0
    },
    {
      "date": "2016-03-05",
      "universal_score_100": 19.04761904761905,
      "market_value": 6000000.0
    },
    {
      "date": "2016-04-24",
      "universal_score_100": 19.04761904761905,
      "market_value": 6000000.0
    },
    {
      "date": "2016-04-30",
      "universal_score_100": 19.04761904761905,
      "market_value": 6000000.0
    },
    {
      "date": "2016-05-14",
      "universal_score_100": 19.04761904761905,
      "market_value": 6000000.0
    },
    {
      "date": "2016-08-20",
      "universal_score_100": 19.04761904761905,
      "market_value": 5000000.0
    },
    {
      "date": "2016-09-17",
      "universal_score_100": 19.04761904761905,
      "market_value": 5000000.0
    },
    {
      "date": "2016-10-15",
      "universal_score_100": 19.04761904761905,
      "market_value": 4000000.0
    },
    {
      "date": "2016-10-19",
      "universal_score_100": 19.04761904761905,
      "market_value": 4000000.0
    },
    {
      "date": "2016-10-22",
      "universal_score_100": 19.04761904761905,
      "market_value": 4000000.0
    },
    {
      "date": "2016-11-04",
      "universal_score_100": 19.04761904761905,
      "market_value": 4000000.0
    },
    {
      "date": "2016-11-23",
      "universal_score_100": 19.04761904761905,
      "market_value": 4000000.0
    },
    {
      "date": "2016-12-17",
      "universal_score_100": 19.04761904761905,
      "market_value": 4000000.0
    },
    {
      "date": "2017-01-21",
      "universal_score_100": 19.04761904761905,
      "market_value": 4000000.0
    },
    {
      "date": "2017-01-28",
      "universal_score_100": 19.04761904761905,
      "market_value": 4000000.0
    },
    {
      "date": "2017-02-19",
      "universal_score_100": 19.04761904761905,
      "market_value": 3500000.0
    },
    {
      "date": "2017-02-23",
      "universal_score_100": 30.789302022178735,
      "market_value": 3500000.0
    },
    {
      "date": "2017-02-26",
      "universal_score_100": 19.04761904761905,
      "market_value": 3500000.0
    },
    {
      "date": "2017-03-01",
      "universal_score_100": 24.686716791979947,
      "market_value": 3500000.0
    },
    {
      "date": "2017-03-04",
      "universal_score_100": 19.04761904761905,
      "market_value": 3500000.0
    },
    {
      "date": "2017-03-09",
      "universal_score_100": 25.850340136054424,
      "market_value": 3500000.0
    },
    {
      "date": "2017-03-12",
      "universal_score_100": 19.04761904761905,
      "market_value": 3500000.0
    },
    {
      "date": "2017-03-16",
      "universal_score_100": 19.04761904761905,
      "market_value": 3500000.0
    },
    {
      "date": "2017-03-19",
      "universal_score_100": 19.04761904761905,
      "market_value": 3500000.0
    },
    {
      "date": "2017-04-01",
      "universal_score_100": 19.04761904761905,
      "market_value": 3500000.0
    },
    {
      "date": "2017-04-05",
      "universal_score_100": 19.04761904761905,
      "market_value": 3500000.0
    },
    {
      "date": "2017-04-08",
      "universal_score_100": 19.04761904761905,
      "market_value": 3500000.0
    },
    {
      "date": "2017-04-15",
      "universal_score_100": 19.04761904761905,
      "market_value": 3500000.0
    },
    {
      "date": "2017-04-22",
      "universal_score_100": 19.04761904761905,
      "market_value": 3500000.0
    },
    {
      "date": "2017-04-25",
      "universal_score_100": 24.195624195624195,
      "market_value": 3500000.0
    },
    {
      "date": "2017-04-29",
      "universal_score_100": 19.04761904761905,
      "market_value": 3500000.0
    },
    {
      "date": "2017-05-06",
      "universal_score_100": 19.04761904761905,
      "market_value": 3500000.0
    },
    {
      "date": "2017-05-13",
      "universal_score_100": 19.04761904761905,
      "market_value": 3500000.0
    },
    {
      "date": "2017-05-20",
      "universal_score_100": 23.80952380952381,
      "market_value": 3500000.0
    },
    {
      "date": "2017-08-11",
      "universal_score_100": 38.095238095238095,
      "market_value": 3500000.0
    },
    {
      "date": "2017-08-20",
      "universal_score_100": 19.04761904761905,
      "market_value": 3500000.0
    },
    {
      "date": "2017-08-26",
      "universal_score_100": 19.04761904761905,
      "market_value": 3500000.0
    },
    {
      "date": "2017-09-09",
      "universal_score_100": 19.04761904761905,
      "market_value": 3500000.0
    },
    {
      "date": "2017-09-16",
      "universal_score_100": 28.57142857142857,
      "market_value": 3500000.0
    },
    {
      "date": "2017-09-23",
      "universal_score_100": 19.04761904761905,
      "market_value": 3500000.0
    },
    {
      "date": "2017-10-21",
      "universal_score_100": 19.04761904761905,
      "market_value": 3500000.0
    },
    {
      "date": "2017-10-24",
      "universal_score_100": 19.04761904761905,
      "market_value": 3500000.0
    },
    {
      "date": "2017-10-28",
      "universal_score_100": 19.04761904761905,
      "market_value": 3500000.0
    },
    {
      "date": "2018-01-14",
      "universal_score_100": 19.04761904761905,
      "market_value": 3000000.0
    },
    {
      "date": "2018-01-20",
      "universal_score_100": 19.04761904761905,
      "market_value": 3000000.0
    },
    {
      "date": "2018-01-26",
      "universal_score_100": 19.04761904761905,
      "market_value": 3000000.0
    },
    {
      "date": "2018-02-11",
      "universal_score_100": 19.04761904761905,
      "market_value": 3000000.0
    },
    {
      "date": "2018-02-18",
      "universal_score_100": 19.04761904761905,
      "market_value": 3000000.0
    },
    {
      "date": "2018-02-24",
      "universal_score_100": 19.04761904761905,
      "market_value": 3000000.0
    },
    {
      "date": "2018-03-02",
      "universal_score_100": 19.04761904761905,
      "market_value": 3000000.0
    },
    {
      "date": "2018-03-10",
      "universal_score_100": 19.04761904761905,
      "market_value": 3000000.0
    },
    {
      "date": "2018-03-17",
      "universal_score_100": 23.80952380952381,
      "market_value": 3000000.0
    },
    {
      "date": "2018-04-01",
      "universal_score_100": 19.04761904761905,
      "market_value": 3000000.0
    },
    {
      "date": "2018-04-07",
      "universal_score_100": 19.04761904761905,
      "market_value": 3000000.0
    },
    {
      "date": "2018-04-14",
      "universal_score_100": 25.64102564102564,
      "market_value": 3000000.0
    },
    {
      "date": "2018-04-20",
      "universal_score_100": 24.404761904761905,
      "market_value": 3000000.0
    },
    {
      "date": "2018-04-28",
      "universal_score_100": 19.04761904761905,
      "market_value": 3000000.0
    },
    {
      "date": "2018-05-05",
      "universal_score_100": 23.80952380952381,
      "market_value": 3000000.0
    },
    {
      "date": "2018-05-12",
      "universal_score_100": 19.04761904761905,
      "market_value": 3000000.0
    },
    {
      "date": "2018-08-19",
      "universal_score_100": 39.68253968253968,
      "market_value": 3000000.0
    },
    {
      "date": "2018-08-25",
      "universal_score_100": 25.396825396825395,
      "market_value": 3000000.0
    },
    {
      "date": "2018-09-01",
      "universal_score_100": 19.04761904761905,
      "market_value": 3000000.0
    },
    {
      "date": "2018-09-15",
      "universal_score_100": 23.80952380952381,
      "market_value": 3000000.0
    },
    {
      "date": "2018-09-22",
      "universal_score_100": 19.04761904761905,
      "market_value": 3000000.0
    },
    {
      "date": "2018-09-26",
      "universal_score_100": 19.04761904761905,
      "market_value": 3000000.0
    },
    {
      "date": "2018-10-06",
      "universal_score_100": 26.984126984126984,
      "market_value": 3000000.0
    },
    {
      "date": "2018-10-21",
      "universal_score_100": 38.095238095238095,
      "market_value": 3000000.0
    },
    {
      "date": "2018-10-26",
      "universal_score_100": 19.04761904761905,
      "market_value": 8000000.0
    },
    {
      "date": "2018-10-31",
      "universal_score_100": 19.04761904761905,
      "market_value": 8000000.0
    },
    {
      "date": "2018-11-04",
      "universal_score_100": 25.770308123249304,
      "market_value": 8000000.0
    },
    {
      "date": "2018-11-10",
      "universal_score_100": 19.04761904761905,
      "market_value": 8000000.0
    },
    {
      "date": "2018-11-25",
      "universal_score_100": 19.04761904761905,
      "market_value": 8000000.0
    },
    {
      "date": "2018-12-21",
      "universal_score_100": 19.04761904761905,
      "market_value": 12000000.0
    },
    {
      "date": "2019-01-19",
      "universal_score_100": 23.86302835741038,
      "market_value": 12000000.0
    },
    {
      "date": "2019-01-26",
      "universal_score_100": 19.04761904761905,
      "market_value": 12000000.0
    },
    {
      "date": "2019-02-02",
      "universal_score_100": 19.04761904761905,
      "market_value": 12000000.0
    },
    {
      "date": "2019-02-09",
      "universal_score_100": 19.04761904761905,
      "market_value": 12000000.0
    },
    {
      "date": "2019-02-23",
      "universal_score_100": 19.04761904761905,
      "market_value": 12000000.0
    },
    {
      "date": "2019-03-02",
      "universal_score_100": 17.063492063492063,
      "market_value": 12000000.0
    },
    {
      "date": "2019-03-09",
      "universal_score_100": 19.04761904761905,
      "market_value": 12000000.0
    },
    {
      "date": "2019-03-15",
      "universal_score_100": 19.04761904761905,
      "market_value": 12000000.0
    },
    {
      "date": "2019-03-30",
      "universal_score_100": 19.04761904761905,
      "market_value": 12000000.0
    },
    {
      "date": "2019-04-07",
      "universal_score_100": 19.04761904761905,
      "market_value": 12000000.0
    },
    {
      "date": "2019-04-13",
      "universal_score_100": 19.04761904761905,
      "market_value": 12000000.0
    },
    {
      "date": "2019-04-20",
      "universal_score_100": 19.04761904761905,
      "market_value": 12000000.0
    },
    {
      "date": "2019-04-27",
      "universal_score_100": 19.04761904761905,
      "market_value": 12000000.0
    },
    {
      "date": "2019-05-11",
      "universal_score_100": 28.57142857142857,
      "market_value": 12000000.0
    },
    {
      "date": "2019-05-18",
      "universal_score_100": 19.04761904761905,
      "market_value": 12000000.0
    },
    {
      "date": "2019-08-09",
      "universal_score_100": 19.04761904761905,
      "market_value": 9000000.0
    },
    {
      "date": "2019-10-24",
      "universal_score_100": 19.04761904761905,
      "market_value": 9000000.0
    },
    {
      "date": "2019-10-27",
      "universal_score_100": 19.04761904761905,
      "market_value": 9000000.0
    },
    {
      "date": "2019-10-30",
      "universal_score_100": 19.04761904761905,
      "market_value": 9000000.0
    },
    {
      "date": "2019-11-02",
      "universal_score_100": 17.283950617283953,
      "market_value": 9000000.0
    },
    {
      "date": "2019-11-07",
      "universal_score_100": 19.04761904761905,
      "market_value": 9000000.0
    },
    {
      "date": "2019-11-10",
      "universal_score_100": 19.04761904761905,
      "market_value": 9000000.0
    },
    {
      "date": "2019-11-28",
      "universal_score_100": 19.04761904761905,
      "market_value": 9000000.0
    },
    {
      "date": "2019-12-01",
      "universal_score_100": 19.04761904761905,
      "market_value": 9000000.0
    },
    {
      "date": "2019-12-07",
      "universal_score_100": 22.222222222222225,
      "market_value": 9000000.0
    },
    {
      "date": "2019-12-15",
      "universal_score_100": 19.04761904761905,
      "market_value": 9000000.0
    },
    {
      "date": "2019-12-18",
      "universal_score_100": 19.04761904761905,
      "market_value": 9000000.0
    },
    {
      "date": "2020-01-17",
      "universal_score_100": 19.04761904761905,
      "market_value": 9000000.0
    },
    {
      "date": "2020-01-25",
      "universal_score_100": 19.04761904761905,
      "market_value": 9000000.0
    },
    {
      "date": "2020-02-01",
      "universal_score_100": 25.396825396825395,
      "market_value": 9000000.0
    },
    {
      "date": "2020-02-15",
      "universal_score_100": 26.666666666666668,
      "market_value": 9000000.0
    },
    {
      "date": "2020-02-22",
      "universal_score_100": 19.04761904761905,
      "market_value": 9000000.0
    },
    {
      "date": "2020-02-29",
      "universal_score_100": 19.04761904761905,
      "market_value": 9000000.0
    },
    {
      "date": "2020-03-07",
      "universal_score_100": 19.04761904761905,
      "market_value": 9000000.0
    },
    {
      "date": "2020-03-11",
      "universal_score_100": 19.04761904761905,
      "market_value": 9000000.0
    },
    {
      "date": "2020-05-16",
      "universal_score_100": 23.80952380952381,
      "market_value": 7000000.0
    },
    {
      "date": "2020-05-23",
      "universal_score_100": 19.04761904761905,
      "market_value": 7000000.0
    },
    {
      "date": "2020-05-26",
      "universal_score_100": 19.04761904761905,
      "market_value": 7000000.0
    },
    {
      "date": "2020-05-31",
      "universal_score_100": 17.305458768873404,
      "market_value": 7000000.0
    },
    {
      "date": "2020-06-05",
      "universal_score_100": 19.04761904761905,
      "market_value": 7000000.0
    },
    {
      "date": "2020-06-13",
      "universal_score_100": 19.04761904761905,
      "market_value": 7000000.0
    },
    {
      "date": "2020-06-16",
      "universal_score_100": 31.746031746031743,
      "market_value": 7000000.0
    },
    {
      "date": "2020-06-20",
      "universal_score_100": 19.04761904761905,
      "market_value": 7000000.0
    },
    {
      "date": "2020-06-27",
      "universal_score_100": 30.15873015873016,
      "market_value": 7000000.0
    },
    {
      "date": "2020-09-12",
      "universal_score_100": 30.15873015873016,
      "market_value": 9000000.0
    },
    {
      "date": "2020-09-19",
      "universal_score_100": 19.04761904761905,
      "market_value": 9000000.0
    },
    {
      "date": "2020-09-26",
      "universal_score_100": 23.80952380952381,
      "market_value": 9000000.0
    },
    {
      "date": "2020-10-03",
      "universal_score_100": 28.78787878787879,
      "market_value": 9000000.0
    },
    {
      "date": "2020-10-17",
      "universal_score_100": 25.396825396825395,
      "market_value": 9000000.0
    },
    {
      "date": "2020-10-21",
      "universal_score_100": 25.396825396825395,
      "market_value": 9000000.0
    },
    {
      "date": "2020-10-24",
      "universal_score_100": 52.38095238095237,
      "market_value": 9000000.0
    },
    {
      "date": "2020-10-27",
      "universal_score_100": 19.04761904761905,
      "market_value": 9000000.0
    },
    {
      "date": "2020-10-31",
      "universal_score_100": 19.04761904761905,
      "market_value": 9000000.0
    },
    {
      "date": "2020-11-03",
      "universal_score_100": 24.761904761904763,
      "market_value": 9000000.0
    },
    {
      "date": "2020-11-08",
      "universal_score_100": 19.04761904761905,
      "market_value": 9000000.0
    },
    {
      "date": "2020-12-22",
      "universal_score_100": 19.04761904761905,
      "market_value": 14000000.0
    },
    {
      "date": "2021-01-02",
      "universal_score_100": 23.80952380952381,
      "market_value": 14000000.0
    },
    {
      "date": "2021-01-08",
      "universal_score_100": 36.70411985018726,
      "market_value": 14000000.0
    },
    {
      "date": "2021-01-16",
      "universal_score_100": 17.460317460317462,
      "market_value": 14000000.0
    },
    {
      "date": "2021-01-19",
      "universal_score_100": 19.04761904761905,
      "market_value": 14000000.0
    },
    {
      "date": "2021-01-22",
      "universal_score_100": 25.64102564102564,
      "market_value": 14000000.0
    },
    {
      "date": "2021-01-30",
      "universal_score_100": 24.761904761904763,
      "market_value": 14000000.0
    },
    {
      "date": "2021-02-03",
      "universal_score_100": 19.04761904761905,
      "market_value": 14000000.0
    },
    {
      "date": "2021-02-06",
      "universal_score_100": 19.04761904761905,
      "market_value": 14000000.0
    },
    {
      "date": "2021-02-14",
      "universal_score_100": 19.04761904761905,
      "market_value": 16000000.0
    },
    {
      "date": "2021-02-20",
      "universal_score_100": 23.80952380952381,
      "market_value": 16000000.0
    },
    {
      "date": "2021-02-24",
      "universal_score_100": 19.04761904761905,
      "market_value": 16000000.0
    },
    {
      "date": "2021-02-27",
      "universal_score_100": 28.415300546448087,
      "market_value": 16000000.0
    },
    {
      "date": "2021-03-02",
      "universal_score_100": 19.04761904761905,
      "market_value": 16000000.0
    },
    {
      "date": "2021-03-12",
      "universal_score_100": 19.04761904761905,
      "market_value": 16000000.0
    },
    {
      "date": "2021-03-16",
      "universal_score_100": 19.04761904761905,
      "market_value": 16000000.0
    },
    {
      "date": "2021-03-20",
      "universal_score_100": 24.21113023522662,
      "market_value": 16000000.0
    },
    {
      "date": "2021-04-17",
      "universal_score_100": 31.242740998838563,
      "market_value": 16000000.0
    },
    {
      "date": "2021-04-21",
      "universal_score_100": 19.04761904761905,
      "market_value": 16000000.0
    },
    {
      "date": "2021-05-08",
      "universal_score_100": 19.04761904761905,
      "market_value": 16000000.0
    },
    {
      "date": "2021-05-15",
      "universal_score_100": 19.04761904761905,
      "market_value": 16000000.0
    },
    {
      "date": "2021-05-22",
      "universal_score_100": 19.04761904761905,
      "market_value": 16000000.0
    },
    {
      "date": "2021-08-09",
      "universal_score_100": 19.04761904761905,
      "market_value": 16000000.0
    },
    {
      "date": "2021-08-13",
      "universal_score_100": 19.04761904761905,
      "market_value": 16000000.0
    },
    {
      "date": "2021-08-21",
      "universal_score_100": 19.04761904761905,
      "market_value": 16000000.0
    },
    {
      "date": "2021-08-29",
      "universal_score_100": 25.396825396825395,
      "market_value": 16000000.0
    },
    {
      "date": "2021-09-12",
      "universal_score_100": 19.04761904761905,
      "market_value": 16000000.0
    },
    {
      "date": "2021-09-25",
      "universal_score_100": 19.04761904761905,
      "market_value": 16000000.0
    },
    {
      "date": "2021-10-02",
      "universal_score_100": 25.396825396825395,
      "market_value": 16000000.0
    },
    {
      "date": "2021-10-16",
      "universal_score_100": 25.396825396825395,
      "market_value": 16000000.0
    },
    {
      "date": "2021-10-23",
      "universal_score_100": 19.04761904761905,
      "market_value": 16000000.0
    },
    {
      "date": "2021-10-27",
      "universal_score_100": 24.91846053489889,
      "market_value": 16000000.0
    },
    {
      "date": "2021-10-31",
      "universal_score_100": 25.396825396825395,
      "market_value": 16000000.0
    },
    {
      "date": "2021-11-05",
      "universal_score_100": 19.04761904761905,
      "market_value": 16000000.0
    },
    {
      "date": "2021-11-20",
      "universal_score_100": 32.33665559246954,
      "market_value": 16000000.0
    },
    {
      "date": "2021-11-27",
      "universal_score_100": 25.396825396825395,
      "market_value": 16000000.0
    },
    {
      "date": "2021-12-05",
      "universal_score_100": 19.04761904761905,
      "market_value": 16000000.0
    },
    {
      "date": "2021-12-11",
      "universal_score_100": 19.04761904761905,
      "market_value": 16000000.0
    },
    {
      "date": "2022-01-22",
      "universal_score_100": 24.47257383966245,
      "market_value": 16000000.0
    },
    {
      "date": "2022-02-05",
      "universal_score_100": 23.80952380952381,
      "market_value": 16000000.0
    },
    {
      "date": "2022-02-12",
      "universal_score_100": 25.396825396825395,
      "market_value": 16000000.0
    },
    {
      "date": "2022-02-20",
      "universal_score_100": 19.04761904761905,
      "market_value": 16000000.0
    },
    {
      "date": "2022-02-26",
      "universal_score_100": 19.04761904761905,
      "market_value": 16000000.0
    },
    {
      "date": "2022-03-05",
      "universal_score_100": 19.04761904761905,
      "market_value": 16000000.0
    },
    {
      "date": "2022-04-09",
      "universal_score_100": 19.04761904761905,
      "market_value": 16000000.0
    },
    {
      "date": "2022-04-16",
      "universal_score_100": 23.80952380952381,
      "market_value": 16000000.0
    },
    {
      "date": "2022-04-23",
      "universal_score_100": 23.80952380952381,
      "market_value": 16000000.0
    },
    {
      "date": "2022-05-02",
      "universal_score_100": 30.15873015873016,
      "market_value": 16000000.0
    },
    {
      "date": "2022-05-08",
      "universal_score_100": 19.04761904761905,
      "market_value": 16000000.0
    },
    {
      "date": "2022-05-14",
      "universal_score_100": 38.69047619047619,
      "market_value": 16000000.0
    },
    {
      "date": "2022-07-31",
      "universal_score_100": 45.363408521303256,
      "market_value": 13000000.0
    },
    {
      "date": "2022-08-06",
      "universal_score_100": 19.04761904761905,
      "market_value": 13000000.0
    },
    {
      "date": "2022-08-13",
      "universal_score_100": 25.541125541125545,
      "market_value": 13000000.0
    },
    {
      "date": "2022-08-19",
      "universal_score_100": 19.04761904761905,
      "market_value": 13000000.0
    },
    {
      "date": "2022-08-27",
      "universal_score_100": 19.04761904761905,
      "market_value": 13000000.0
    },
    {
      "date": "2022-09-04",
      "universal_score_100": 19.04761904761905,
      "market_value": 13000000.0
    },
    {
      "date": "2022-09-11",
      "universal_score_100": 19.04761904761905,
      "market_value": 13000000.0
    },
    {
      "date": "2022-09-17",
      "universal_score_100": 31.746031746031743,
      "market_value": 13000000.0
    },
    {
      "date": "2022-10-01",
      "universal_score_100": 19.04761904761905,
      "market_value": 13000000.0
    },
    {
      "date": "2022-10-09",
      "universal_score_100": 34.53815261044177,
      "market_value": 13000000.0
    },
    {
      "date": "2022-10-15",
      "universal_score_100": 19.04761904761905,
      "market_value": 13000000.0
    },
    {
      "date": "2022-10-18",
      "universal_score_100": 19.04761904761905,
      "market_value": 13000000.0
    },
    {
      "date": "2022-11-04",
      "universal_score_100": 25.396825396825395,
      "market_value": 13000000.0
    },
    {
      "date": "2022-11-08",
      "universal_score_100": 19.04761904761905,
      "market_value": 13000000.0
    },
    {
      "date": "2022-11-11",
      "universal_score_100": 34.92063492063492,
      "market_value": 13000000.0
    },
    {
      "date": "2023-01-22",
      "universal_score_100": 19.04761904761905,
      "market_value": 13000000.0
    },
    {
      "date": "2023-01-28",
      "universal_score_100": 36.507936507936506,
      "market_value": 13000000.0
    },
    {
      "date": "2023-02-04",
      "universal_score_100": 17.460317460317462,
      "market_value": 13000000.0
    },
    {
      "date": "2023-02-12",
      "universal_score_100": 19.04761904761905,
      "market_value": 13000000.0
    },
    {
      "date": "2023-02-18",
      "universal_score_100": 34.92063492063492,
      "market_value": 13000000.0
    },
    {
      "date": "2023-02-24",
      "universal_score_100": 19.04761904761905,
      "market_value": 13000000.0
    },
    {
      "date": "2023-03-04",
      "universal_score_100": 19.04761904761905,
      "market_value": 13000000.0
    },
    {
      "date": "2023-03-11",
      "universal_score_100": 19.04761904761905,
      "market_value": 13000000.0
    },
    {
      "date": "2023-03-17",
      "universal_score_100": 23.80952380952381,
      "market_value": 13000000.0
    },
    {
      "date": "2023-04-02",
      "universal_score_100": 19.04761904761905,
      "market_value": 13000000.0
    },
    {
      "date": "2023-04-09",
      "universal_score_100": 19.04761904761905,
      "market_value": 13000000.0
    },
    {
      "date": "2023-04-15",
      "universal_score_100": 25.396825396825395,
      "market_value": 13000000.0
    },
    {
      "date": "2023-04-23",
      "universal_score_100": 19.04761904761905,
      "market_value": 13000000.0
    },
    {
      "date": "2023-04-29",
      "universal_score_100": 19.04761904761905,
      "market_value": 13000000.0
    },
    {
      "date": "2023-05-06",
      "universal_score_100": 23.80952380952381,
      "market_value": 13000000.0
    },
    {
      "date": "2023-05-13",
      "universal_score_100": 19.04761904761905,
      "market_value": 13000000.0
    },
    {
      "date": "2023-05-21",
      "universal_score_100": 25.396825396825395,
      "market_value": 13000000.0
    },
    {
      "date": "2023-05-27",
      "universal_score_100": 30.15873015873016,
      "market_value": 13000000.0
    },
    {
      "date": "2023-08-12",
      "universal_score_100": 25.396825396825395,
      "market_value": 13000000.0
    },
    {
      "date": "2023-08-19",
      "universal_score_100": 23.86302835741038,
      "market_value": 13000000.0
    },
    {
      "date": "2023-08-26",
      "universal_score_100": 24.33862433862434,
      "market_value": 13000000.0
    },
    {
      "date": "2023-09-02",
      "universal_score_100": 25.396825396825395,
      "market_value": 13000000.0
    },
    {
      "date": "2023-09-15",
      "universal_score_100": 22.222222222222225,
      "market_value": 13000000.0
    },
    {
      "date": "2023-09-21",
      "universal_score_100": 38.095238095238095,
      "market_value": 13000000.0
    },
    {
      "date": "2023-09-24",
      "universal_score_100": 25.396825396825395,
      "market_value": 13000000.0
    },
    {
      "date": "2023-09-30",
      "universal_score_100": 25.615763546798032,
      "market_value": 13000000.0
    },
    {
      "date": "2023-10-05",
      "universal_score_100": 19.04761904761905,
      "market_value": 13000000.0
    },
    {
      "date": "2023-10-08",
      "universal_score_100": 30.41125541125541,
      "market_value": 13000000.0
    },
    {
      "date": "2023-10-21",
      "universal_score_100": 17.424242424242426,
      "market_value": 13000000.0
    },
    {
      "date": "2023-10-29",
      "universal_score_100": 25.770308123249304,
      "market_value": 13000000.0
    },
    {
      "date": "2023-11-04",
      "universal_score_100": 24.404761904761905,
      "market_value": 13000000.0
    },
    {
      "date": "2023-11-09",
      "universal_score_100": 14.285714285714288,
      "market_value": 13000000.0
    },
    {
      "date": "2023-11-12",
      "universal_score_100": 24.33862433862434,
      "market_value": 13000000.0
    },
    {
      "date": "2023-11-25",
      "universal_score_100": 23.86302835741038,
      "market_value": 13000000.0
    },
    {
      "date": "2023-11-30",
      "universal_score_100": 19.04761904761905,
      "market_value": 13000000.0
    },
    {
      "date": "2023-12-03",
      "universal_score_100": 19.04761904761905,
      "market_value": 13000000.0
    },
    {
      "date": "2023-12-06",
      "universal_score_100": 19.04761904761905,
      "market_value": 13000000.0
    },
    {
      "date": "2023-12-10",
      "universal_score_100": 19.04761904761905,
      "market_value": 13000000.0
    },
    {
      "date": "2023-12-14",
      "universal_score_100": 26.31154156577885,
      "market_value": 13000000.0
    },
    {
      "date": "2023-12-17",
      "universal_score_100": 19.04761904761905,
      "market_value": 13000000.0
    },
    {
      "date": "2023-12-20",
      "universal_score_100": 19.04761904761905,
      "market_value": 13000000.0
    },
    {
      "date": "2024-01-13",
      "universal_score_100": 17.460317460317462,
      "market_value": 13000000.0
    },
    {
      "date": "2024-01-20",
      "universal_score_100": 23.80952380952381,
      "market_value": 13000000.0
    },
    {
      "date": "2024-01-27",
      "universal_score_100": 19.04761904761905,
      "market_value": 13000000.0
    },
    {
      "date": "2024-02-03",
      "universal_score_100": 19.04761904761905,
      "market_value": 13000000.0
    },
    {
      "date": "2024-02-06",
      "universal_score_100": 19.04761904761905,
      "market_value": 13000000.0
    },
    {
      "date": "2024-02-10",
      "universal_score_100": 19.04761904761905,
      "market_value": 13000000.0
    },
    {
      "date": "2024-02-17",
      "universal_score_100": 19.04761904761905,
      "market_value": 13000000.0
    },
    {
      "date": "2024-02-23",
      "universal_score_100": 19.04761904761905,
      "market_value": 13000000.0
    },
    {
      "date": "2024-03-03",
      "universal_score_100": 19.04761904761905,
      "market_value": 13000000.0
    },
    {
      "date": "2024-03-10",
      "universal_score_100": 19.04761904761905,
      "market_value": 13000000.0
    },
    {
      "date": "2024-03-14",
      "universal_score_100": 19.04761904761905,
      "market_value": 13000000.0
    },
    {
      "date": "2024-03-30",
      "universal_score_100": 19.04761904761905,
      "market_value": 13000000.0
    },
    {
      "date": "2024-04-03",
      "universal_score_100": 19.04761904761905,
      "market_value": 13000000.0
    },
    {
      "date": "2024-04-11",
      "universal_score_100": 52.38095238095237,
      "market_value": 13000000.0
    },
    {
      "date": "2024-04-14",
      "universal_score_100": 23.80952380952381,
      "market_value": 13000000.0
    },
    {
      "date": "2024-04-21",
      "universal_score_100": 19.04761904761905,
      "market_value": 13000000.0
    },
    {
      "date": "2024-04-27",
      "universal_score_100": 19.04761904761905,
      "market_value": 13000000.0
    },
    {
      "date": "2024-05-02",
      "universal_score_100": 19.04761904761905,
      "market_value": 13000000.0
    },
    {
      "date": "2024-05-05",
      "universal_score_100": 19.04761904761905,
      "market_value": 13000000.0
    },
    {
      "date": "2024-05-09",
      "universal_score_100": 19.04761904761905,
      "market_value": 13000000.0
    },
    {
      "date": "2024-05-12",
      "universal_score_100": 33.33333333333333,
      "market_value": 13000000.0
    },
    {
      "date": "2024-05-18",
      "universal_score_100": 19.04761904761905,
      "market_value": 13000000.0
    },
    {
      "date": "2024-05-25",
      "universal_score_100": 19.04761904761905,
      "market_value": 13000000.0
    },
    {
      "date": "2024-08-23",
      "universal_score_100": 19.04761904761905,
      "market_value": 10000000.0
    },
    {
      "date": "2024-08-28",
      "universal_score_100": 25.396825396825395,
      "market_value": 10000000.0
    },
    {
      "date": "2024-10-05",
      "universal_score_100": 28.57142857142857,
      "market_value": 10000000.0
    },
    {
      "date": "2024-10-23",
      "universal_score_100": 23.80952380952381,
      "market_value": 7000000.0
    },
    {
      "date": "2024-10-29",
      "universal_score_100": 19.04761904761905,
      "market_value": 7000000.0
    },
    {
      "date": "2024-11-01",
      "universal_score_100": 19.04761904761905,
      "market_value": 7000000.0
    },
    {
      "date": "2024-11-05",
      "universal_score_100": 19.04761904761905,
      "market_value": 7000000.0
    },
    {
      "date": "2024-11-09",
      "universal_score_100": 19.04761904761905,
      "market_value": 7000000.0
    },
    {
      "date": "2025-01-18",
      "universal_score_100": 19.04761904761905,
      "market_value": 5000000.0
    },
    {
      "date": "2025-01-21",
      "universal_score_100": 19.04761904761905,
      "market_value": 5000000.0
    },
    {
      "date": "2025-01-29",
      "universal_score_100": 19.04761904761905,
      "market_value": 5000000.0
    },
    {
      "date": "2025-03-01",
      "universal_score_100": 19.04761904761905,
      "market_value": 5000000.0
    },
    {
      "date": "2025-04-05",
      "universal_score_100": 33.33333333333333,
      "market_value": 3000000.0
    }
  ]
}


async def test_real_example_generator():
    """Test analysis agent with real Jonas Hofmann data."""
    # Initialize analysis agent
    analysis_agent = AnalysisAgent()
    
    try:
        # Run analysis
        analysis = await analysis_agent.analyze(player_data=REAL_PLAYER_DATA)
        return analysis
        
    except Exception as e:
        return None


async def main():
    """Run the test and output JSON."""
    result = await test_real_example_generator()
    if result:
        print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    asyncio.run(main())

