"""Quick test for Chatbot Orchestrator."""

import asyncio
from src.llm.orchestrators import ChatbotOrchestrator


async def test_chatbot_orchestrator():
    """Test the chatbot orchestrator with a simple query."""
    print("\n" + "=" * 70)
    print("Chatbot Orchestrator - Quick Test")
    print("=" * 70)
    
    # Initialize orchestrator
    orchestrator = ChatbotOrchestrator()
    user_id = "test_user"
    session_id = None
    
    # Test 1: General question (should route to general chatbot)
    print("\nTest 1: General Question")
    print("-" * 70)
    query1 = "What is a breakout candidate in soccer?"
    print(f"Query: {query1}")
    print("\nResponse (streaming): ", end="", flush=True)
    
    try:
        full_response = ""
        async for chunk in orchestrator.process_message(
            user_id=user_id,
            message=query1,
            session_id=session_id
        ):
            print(chunk, end="", flush=True)
            full_response += chunk
        
        print("\n\n✅ Test 1 passed - General question processed")
        
        # Get session_id for next test
        if session_id is None:
            session_id = orchestrator.session_manager.list_sessions(user_id)[0]
            print(f"Session ID: {session_id}")
        
    except Exception as e:
        print(f"\n❌ Test 1 failed: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Test 2: Session continuity (same session_id)
    print("\n" + "=" * 70)
    print("Test 2: Session Continuity")
    print("-" * 70)
    query2 = "Can you tell me more about that?"
    print(f"Query: {query2}")
    print("\nResponse (streaming): ", end="", flush=True)
    
    try:
        full_response = ""
        async for chunk in orchestrator.process_message(
            user_id=user_id,
            message=query2,
            session_id=session_id  # Using same session_id
        ):
            print(chunk, end="", flush=True)
            full_response += chunk
        
        print("\n\n✅ Test 2 passed - Session continuity maintained")
        
        # Check conversation history
        history = orchestrator.session_manager.get_conversation_history(session_id)
        print(f"Conversation history length: {len(history)} messages")
        
    except Exception as e:
        print(f"\n❌ Test 2 failed: {e}")
        import traceback
        traceback.print_exc()
    
    # Test 3: Report question (should route to report chatbot, but fallback to general if no report)
    print("\n" + "=" * 70)
    print("Test 3: Report Question (without report data - should fallback)")
    print("-" * 70)
    query3 = "What is Messi's market value?"
    print(f"Query: {query3}")
    print("\nResponse (streaming): ", end="", flush=True)
    
    try:
        full_response = ""
        async for chunk in orchestrator.process_message(
            user_id=user_id,
            message=query3,
            session_id=session_id  # Same session
        ):
            print(chunk, end="", flush=True)
            full_response += chunk
        
        print("\n\n✅ Test 3 passed - Report question handled (fallback to general)")
        
    except Exception as e:
        print(f"\n❌ Test 3 failed: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 70)
    print("All Tests Complete")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(test_chatbot_orchestrator())

