"""Test the Report Answer Agent."""

import asyncio
from src.llm.agents.chatbot.report_answer_agent import ReportAnswerAgent
from src.global_configs import REPORT_ANSWER_AGENT_CONFIGS


# Simple test report
SIMPLE_REPORT = {
    "player_info": {
        "id": "test_001",
        "name": "John Doe",
        "position": "Forward",
        "age": 24,
        "club": "Test FC"
    },
    "performance_analysis": {
        "summary": "John Doe has shown strong performance this season with 15 goals and 8 assists.",
        "current_form": "Excellent form in the last 5 matches"
    },
    "market_value": {
        "estimated_value": "€25 million",
        "value_trend": "Increasing"
    },
    "strengths": ["Goal scoring", "Speed", "Finishing"],
    "weaknesses": ["Defensive contribution", "Aerial duels"],
    "recommendations": {
        "for_team": "Suitable for teams needing a goal scorer",
        "for_player": "Focus on improving defensive skills"
    },
    "statistics_summary": {},
    "news": [
        {
            "title": "John Doe scores hat-trick",
            "summary": "Scored three goals in the last match"
        }
    ],
    "news_analysis": {
        "analysis": "Recent performances suggest strong potential for value increase"
    },
    "ml_predictions": {
        "performance_score": 0.85
    },
    "player_development": {
        "aging_assessment": "At peak performance age",
        "performance_vs_expectation": "Exceeding expectations",
        "position_curve_comparison": "Above average for position",
        "trajectory_analysis": "On upward trajectory"
    },
    "breakout_analysis": {
        "is_breakout_candidate": True,
        "breakout_probability": "High (75%)",
        "expected_value_increase": "30-40%",
        "growth_indicators": ["Increasing goal rate", "Better shot quality"],
        "breakout_analysis": "Strong candidate for breakout based on recent form"
    },
    "valuation_insights": {
        "market_value_prediction": "€30-35 million within 12 months",
        "undervalued_assessment": "Slightly undervalued at current market price",
        "transfer_fee_performance_prediction": "Expected to command €30+ million",
        "value_determining_factors": ["Age", "Goal scoring record", "Recent form"],
        "market_positioning": "Attractive to mid-to-top tier clubs"
    },
    "generated_at": "2025-01-15T10:00:00Z"
}

# Simple player data
SIMPLE_PLAYER_DATA = {
    "goals": 15,
    "assists": 8,
    "matches_played": 20,
    "goals_per_match": 0.75,
    "shots_on_target": 45,
    "shot_accuracy": 0.60,
    "ml_performance_score": 0.85
}


async def test_basic_questions():
    """Test basic questions about the player."""
    print("\n" + "=" * 70)
    print("Test 1: Basic Questions")
    print("=" * 70)
    
    agent = ReportAnswerAgent(config=REPORT_ANSWER_AGENT_CONFIGS)
    user_id = "test_user_basic"
    session_id = None
    
    test_cases = [
        "What is the player's name?",
        "How many goals did he score?",
        "What is his market value?",
        "Is he a breakout candidate?"
    ]
    
    for i, query in enumerate(test_cases, 1):
        print(f"\n{i}. Query: {query}")
        print("-" * 70)
        print("Response (streaming): ", end="", flush=True)
        
        try:
            full_response = ""
            async for chunk in agent.process_message(
                user_id=user_id,
                message=query,
                report=SIMPLE_REPORT,
                player_data=SIMPLE_PLAYER_DATA,
                session_id=session_id
            ):
                print(chunk, end="", flush=True)
                full_response += chunk
            
            print()  # New line after streaming
            
            if session_id is None:
                session_id = agent.session_manager.list_sessions(user_id)[0]
            
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()


async def test_session_management():
    """Test that session management maintains conversation context."""
    print("\n" + "=" * 70)
    print("Test 2: Session Management & Context")
    print("=" * 70)
    
    agent = ReportAnswerAgent(config=REPORT_ANSWER_AGENT_CONFIGS)
    user_id = "test_user_session"
    session_id = None
    
    conversation = [
        "What is the player's name?",
        "How old is he?",
        "What position does he play?"
    ]
    
    for i, query in enumerate(conversation, 1):
        print(f"\n{i}. Query: {query}")
        print("-" * 70)
        print("Response (streaming): ", end="", flush=True)
        
        try:
            async for chunk in agent.process_message(
                user_id=user_id,
                message=query,
                report=SIMPLE_REPORT,
                player_data=SIMPLE_PLAYER_DATA,
                session_id=session_id
            ):
                print(chunk, end="", flush=True)
            
            print()  # New line after streaming
            
            if session_id is None:
                session_id = agent.session_manager.list_sessions(user_id)[0]
            
            history = agent.session_manager.get_conversation_history(session_id)
            print(f"Conversation history: {len(history)} messages")
            
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()


async def test_data_sources():
    """Test that agent uses both report and player data."""
    print("\n" + "=" * 70)
    print("Test 3: Using Both Report and Player Data")
    print("=" * 70)
    
    agent = ReportAnswerAgent(config=REPORT_ANSWER_AGENT_CONFIGS)
    user_id = "test_user_data"
    session_id = None
    
    test_cases = [
        {
            "query": "What are his goal statistics?",
            "description": "Should use player_data for specific stats"
        },
        {
            "query": "What does the report say about his breakout potential?",
            "description": "Should use report for analysis"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. {test_case['description']}")
        print(f"Query: {test_case['query']}")
        print("-" * 70)
        print("Response (streaming): ", end="", flush=True)
        
        try:
            async for chunk in agent.process_message(
                user_id=user_id,
                message=test_case['query'],
                report=SIMPLE_REPORT,
                player_data=SIMPLE_PLAYER_DATA,
                session_id=session_id
            ):
                print(chunk, end="", flush=True)
            
            print()  # New line after streaming
            
            if session_id is None:
                session_id = agent.session_manager.list_sessions(user_id)[0]
            
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()


async def main():
    """Run all tests."""
    print("\n" + "=" * 70)
    print("Report Answer Agent - Simple Tests")
    print("=" * 70)
    
    await test_basic_questions()
    await test_session_management()
    await test_data_sources()
    
    print("\n" + "=" * 70)
    print("All Tests Complete")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())

