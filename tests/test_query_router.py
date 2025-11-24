"""Test the Query Router Agent."""

import asyncio
from src.llm.agents.chatbot.query_router_agent import QueryRouterAgent
from src.global_configs import QUERY_ROUTER_AGENT_CONFIGS


async def test_query_router():
    """Test the query router with various queries."""
    
    # Initialize agent
    router = QueryRouterAgent(config=QUERY_ROUTER_AGENT_CONFIGS)
    
    print("\n" + "=" * 70)
    print("Testing Query Router Agent")
    print("=" * 70)
    
    # Test cases
    test_cases = [
        {
            "name": "Report query - specific player value",
            "query": "What is Lionel Messi's current market value?",
            "expected": "report"
        },
        {
            "name": "Report query - breakout candidate",
            "query": "Is Erling Haaland a breakout candidate?",
            "expected": "report"
        },
        {
            "name": "Report query - player development",
            "query": "Tell me about Cristiano Ronaldo's development and aging trajectory",
            "expected": "report"
        },
        {
            "name": "General query - concept explanation",
            "query": "How do aging curves work in soccer player performance analysis?",
            "expected": "general"
        },
        {
            "name": "General query - definition",
            "query": "What is a breakout candidate?",
            "expected": "general"
        },
        {
            "name": "General query - general knowledge",
            "query": "Explain market value in soccer",
            "expected": "general"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. Test: {test_case['name']}")
        print("-" * 70)
        print(f"Query: {test_case['query']}")
        print(f"Expected: {test_case['expected']}")
        
        try:
            classification = await router.route(test_case['query'])
            
            print(f"Result: {classification}")
            
            if classification == test_case['expected']:
                print("✓ Correct classification")
            else:
                print(f"✗ Incorrect classification (expected {test_case['expected']}, got {classification})")
            
        except Exception as e:
            print(f"\n Error: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 70)
    print("Query Router Tests Complete")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(test_query_router())

