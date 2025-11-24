"""Test the General Chatbot Agent."""

import asyncio
import time
from src.llm.agents.chatbot.general_chatbot_agent import GeneralChatbotAgent
from src.global_configs import GENERAL_CHATBOT_AGENT_CONFIGS


async def test_general_questions():
    """Test general soccer questions that should be answered."""
    print("\n" + "=" * 70)
    print("Test 1: General Soccer Questions")
    print("=" * 70)
    
    chatbot = GeneralChatbotAgent(config=GENERAL_CHATBOT_AGENT_CONFIGS)
    user_id = "test_user_general"
    session_id = None
    
    test_cases = [
        "What is a breakout candidate?"
    ]
    
    for i, query in enumerate(test_cases, 1):
        print(f"\n{i}. Query: {query}")
        print("-" * 70)
        print("Response (streaming): ", end="", flush=True)
        
        try:
            async for chunk in chatbot.process_message(
                user_id=user_id,
                message=query,
                session_id=session_id
            ):
                print(chunk, end="", flush=True)  # Print chunks as they arrive
            
            print()  # New line after streaming completes
            
            if session_id is None:
                session_id = chatbot.session_manager.list_sessions(user_id)[0]
            
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()


async def test_name_identity():
    """Test that chatbot correctly identifies itself as Alexiu."""
    print("\n" + "=" * 70)
    print("Test 1.5: Name & Identity")
    print("=" * 70)
    
    chatbot = GeneralChatbotAgent(config=GENERAL_CHATBOT_AGENT_CONFIGS)
    user_id = "test_user_name"
    session_id = None
    
    test_cases = [
        "What is your name?",
        "Who are you?",
        "Tell me about yourself"
    ]
    
    for i, query in enumerate(test_cases, 1):
        print(f"\n{i}. Query: {query}")
        print("-" * 70)
        print("Response (streaming): ", end="", flush=True)
        
        try:
            full_response = ""
            async for chunk in chatbot.process_message(
                user_id=user_id,
                message=query,
                session_id=session_id
            ):
                print(chunk, end="", flush=True)  # Print chunks as they arrive
                full_response += chunk
            
            print()  # New line after streaming completes
            
            if session_id is None:
                session_id = chatbot.session_manager.list_sessions(user_id)[0]
            
            # Check if response mentions "Alexiu"
            if "alexiu" in full_response.lower():
                print(f"\n✅ Correctly identifies as Alexiu")
            else:
                print(f"\n⚠️  May not be identifying correctly (check response)")
            
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()


async def test_streaming():
    """Test that streaming works correctly."""
    print("\n" + "=" * 70)
    print("Test 2: Streaming Response")
    print("=" * 70)
    
    chatbot = GeneralChatbotAgent(config=GENERAL_CHATBOT_AGENT_CONFIGS)
    user_id = "test_user_stream"
    
    query = "What makes a player a breakout candidate? Explain the key indicators and metrics."
    print(f"\nQuery: {query}")
    print("-" * 70)
    
    try:
        print("\nStreaming chunks (as they arrive):")
        print("-" * 70)
        
        start_time = time.time()
        full_response = ""
        chunk_count = 0
        
        async for chunk in chatbot.process_message(
            user_id=user_id,
            message=query
        ):
            chunk_count += 1
            full_response += chunk
            # Print first few chunks to show streaming
            if chunk_count <= 5:
                print(f"Chunk {chunk_count}: {chunk[:50]}..." if len(chunk) > 50 else f"Chunk {chunk_count}: {chunk}")
            elif chunk_count == 6:
                print("... (streaming continues)")
        
        end_time = time.time()
        
        print(f"\n✅ Streaming test completed")
        print(f"Total chunks received: {chunk_count}")
        print(f"Response time: {end_time - start_time:.2f} seconds")
        print(f"Response length: {len(full_response)} characters")
        print(f"\nFull response preview:")
        print(full_response[:400] + "..." if len(full_response) > 400 else full_response)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


async def test_report_redirect():
    """Test that specific player questions redirect to report generation."""
    print("\n" + "=" * 70)
    print("Test 3: Report Generation Redirect")
    print("=" * 70)
    
    chatbot = GeneralChatbotAgent(config=GENERAL_CHATBOT_AGENT_CONFIGS)
    user_id = "test_user_redirect"
    session_id = None
    
    test_cases = [
        {
            "name": "Player market value",
            "query": "What is Messi's current market value?"
        },
        {
            "name": "Player statistics",
            "query": "Tell me about Cristiano Ronaldo's performance this season"
        },
        {
            "name": "Player development",
            "query": "How is Kylian Mbappé developing as a player?"
        },
        {
            "name": "Player breakout potential",
            "query": "Is Erling Haaland a breakout candidate?"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. {test_case['name']}")
        print(f"Query: {test_case['query']}")
        print("-" * 70)
        print("Response (streaming): ", end="", flush=True)
        
        try:
            full_response = ""
            async for chunk in chatbot.process_message(
                user_id=user_id,
                message=test_case['query'],
                session_id=session_id
            ):
                print(chunk, end="", flush=True)  # Print chunks as they arrive
                full_response += chunk
            
            print()  # New line after streaming completes
            
            if session_id is None:
                session_id = chatbot.session_manager.list_sessions(user_id)[0]
            
            # Check if response mentions generating a report
            report_keywords = ["generate", "report", "player report", "statistics", "data"]
            mentions_report = any(keyword.lower() in full_response.lower() for keyword in report_keywords)
            
            if mentions_report:
                print(f"\n✅ Correctly redirects to report generation")
            else:
                print(f"\n⚠️  May not be redirecting properly")
            
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()


async def test_session_management():
    """Test that session management maintains conversation context."""
    print("\n" + "=" * 70)
    print("Test 4: Session Management & Context")
    print("=" * 70)
    
    chatbot = GeneralChatbotAgent(config=GENERAL_CHATBOT_AGENT_CONFIGS)
    user_id = "test_user_session"
    session_id = None
    
    conversation = [
        "What is a breakout candidate?",
        "What are the key indicators?",
        "How do you identify them?"
    ]
    
    for i, query in enumerate(conversation, 1):
        print(f"\n{i}. Query: {query}")
        print("-" * 70)
        print("Response (streaming): ", end="", flush=True)
        
        try:
            async for chunk in chatbot.process_message(
                user_id=user_id,
                message=query,
                session_id=session_id
            ):
                print(chunk, end="", flush=True)  # Print chunks as they arrive
            
            print()  # New line after streaming completes
            
            if session_id is None:
                session_id = chatbot.session_manager.list_sessions(user_id)[0]
            
            history = chatbot.session_manager.get_conversation_history(session_id)
            print(f"Conversation history: {len(history)} messages")
            
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()


async def main():
    """Run all tests."""
    print("\n" + "=" * 70)
    print("General Chatbot Agent - Comprehensive Tests")
    print("=" * 70)
    
    # await test_general_questions()
    await test_name_identity()
    # await test_streaming()
    # await test_report_redirect()
    # await test_session_management()
    
    print("\n" + "=" * 70)
    print("All Tests Complete")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())
