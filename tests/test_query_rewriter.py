"""Test the Query Rewriter Agent."""

import asyncio
import logging
from src.llm.agents.chatbot.query_rewriter_agent import QueryRewriterAgent
from src.global_configs import QUERY_REWRITER_AGENT_CONFIGS

# Enable debug logging to see history being passed
logging.basicConfig(level=logging.DEBUG)


async def test_query_rewriter():
    """Test the query rewriter with various queries."""
    
    # Initialize agent
    rewriter = QueryRewriterAgent(config=QUERY_REWRITER_AGENT_CONFIGS)
    
    print("\n" + "=" * 70)
    print("Testing Query Rewriter Agent")
    print("=" * 70)
    
    # Test cases
    test_cases = [
        {
            "name": "Simple query with abbreviation",
            "message": "What's Messi's value?",
            "history": None
        },
        {
            "name": "Query with pronoun (with context)",
            "message": "Tell me about his development",
            "history": [
                {"role": "user", "content": "What is Cristiano Ronaldo's market value?"},
                {"role": "assistant", "content": "Cristiano Ronaldo's estimated market value is..."}
            ]
        },
        {
            "name": "Query with 'the player' (with context)",
            "message": "Is the player a breakout candidate?",
            "history": [
                {"role": "user", "content": "Tell me about Erling Haaland"},
                {"role": "assistant", "content": "Erling Haaland is a striker for Manchester City..."}
            ]
        },
        {
            "name": "General question (no player)",
            "message": "How do aging curves work?",
            "history": None
        },
        {
            "name": "Typo and informal",
            "message": "whats mbappes breakout potential lol",
            "history": None
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. Test: {test_case['name']}")
        print("-" * 70)
        print(f"Original Message: {test_case['message']}")
        
        if test_case['history']:
            print(f"History: {len(test_case['history'])} messages")
        
        try:
            rewritten = await rewriter.rewrite(
                message=test_case['message'],
                history=test_case['history']
            )
            
            print(f"\nRewritten Query: {rewritten}")
            
        except Exception as e:
            print(f"\n Error: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 70)
    print("Query Rewriter Tests Complete")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(test_query_rewriter())

