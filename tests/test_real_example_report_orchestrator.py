"""Test report orchestrator with real player data (Jonas Hofmann example)."""

import asyncio
import json
from src.llm.orchestrators.report_orchestrator import ReportOrchestrator

# Import the real player data from the other test file
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from test_real_example_generator import REAL_PLAYER_DATA


async def test_real_example_report_orchestrator():
    """Test report orchestrator with real Jonas Hofmann data."""
    # Initialize orchestrator
    orchestrator = ReportOrchestrator()
    
    try:
        # Generate full report
        report = await orchestrator.generate_player_report(
            player_data=REAL_PLAYER_DATA,
            player_name="Jonas Hofmann",
            club="Bayer 04 Leverkusen"
        )
        return report
        
    except Exception as e:
        return None


async def main():
    """Run the test and output JSON."""
    result = await test_real_example_report_orchestrator()
    if result:
        print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    asyncio.run(main())

