"""Report Answer Agent for answering questions using player report data."""

from typing import Dict, Any, Optional, AsyncGenerator
from src.llm.clients.openai_client import OpenAIClient
from src.utils.message_builder import MessageBuilder
from src.utils.session_manager import SessionManager
import logging
import json

logger = logging.getLogger(__name__)


class ReportAnswerAgent:
    """
    Chatbot agent that answers questions about specific players using their report data.
    Uses MessageBuilder for conversation structure and SessionManager for session handling.
    Requires a player report to answer questions about specific players.
    """
    
    def __init__(
        self, 
        config: Optional[Dict[str, Any]] = None,
        session_manager: Optional[SessionManager] = None
    ):
        """
        Initialize the Report Answer Agent.
        
        Args:
            config: Optional config dict. If not provided, uses default from model_configs.
            session_manager: Optional shared SessionManager instance. If None, creates a new one.
        """
        self.config = config or {}
        self.client = OpenAIClient(config=self.config)
        self.session_manager = session_manager if session_manager is not None else SessionManager()
        
        # Load prompts from global_configs
        try:
            from src.global_configs import REPORT_ANSWER_AGENT_SYSTEM_PROMPT
            self.system_prompt = REPORT_ANSWER_AGENT_SYSTEM_PROMPT
        except ImportError:
            logger.warning("Report answer agent prompts not found in global_configs, using defaults")
            self.system_prompt = None
        
        logger.info(f"ReportAnswerAgent initialized with model: {self.config.get('model', 'default')}")
    
    async def process_message(
        self, 
        user_id: str, 
        message: str, 
        report: Dict[str, Any],
        player_data: Optional[Dict[str, Any]] = None,
        session_id: Optional[str] = None
    ) -> AsyncGenerator[str, None]:
        """
        Process a user message and return a streaming response using player report data.
        Maintains conversation context through temporary sessions.
        
        Args:
            user_id: Unique identifier for the user
            message: User's message
            report: Player report data (following report_schema.json structure)
            player_data: Optional original player statistics and ML model output data
            session_id: Optional session ID, creates new if None
            
        Yields:
            Response chunks as strings
        """
        # Get or create temporary session
        if session_id is None:
            session_id = await self.session_manager.start_session(user_id)
            logger.info(f"ReportAnswerAgent: Created new session {session_id} for user {user_id}")
        else:
            logger.info(f"ReportAnswerAgent: Using existing session {session_id} for user {user_id}")
            # Check if session exists
            if not self.session_manager.session_exists(session_id):
                logger.warning(f"ReportAnswerAgent: Session {session_id} not found, creating new session")
                session_id = await self.session_manager.start_session(user_id)
        
        # Prepare data for system prompt
        report_json = json.dumps(report, indent=2)
        player_data_json = json.dumps(player_data, indent=2) if player_data else None
        
        # Store report in session for context
        context_data = report_json
        if player_data_json:
            context_data = f"Report Data:\n{report_json}\n\nOriginal Player Data:\n{player_data_json}"
        self.session_manager.add_rag_context(session_id, context_data)
        
        # Add user message to session
        self.session_manager.add_message_to_session(session_id, "user", message)
        
        # Build conversation using MessageBuilder
        conversation_history = self.session_manager.get_conversation_history(session_id)
        messages = MessageBuilder()
        
        # Add system prompt with report data and optional player data
        if self.system_prompt:
            # Format system prompt with report data and optional player data
            if player_data_json:
                system_message = self.system_prompt.format(
                    report_data=report_json,
                    player_data=player_data_json
                )
            else:
                # If no player_data, use empty string for player_data placeholder
                system_message = self.system_prompt.format(
                    report_data=report_json,
                    player_data=""
                )
            messages.add_system_message(system_message)
        
        # Add all conversation history to MessageBuilder
        for msg in conversation_history:
            if msg['role'] == 'user':
                messages.add_user_message(msg['content'])
            elif msg['role'] == 'assistant':
                messages.add_assistant_message(msg['content'])
        
        # Get streaming response with collection
        full_response = ""
        
        async def stream_with_collection():
            nonlocal full_response
            try:
                # Force streaming
                stream = await self.client.chat_completion(
                    messages=messages.build(),
                    stream=True
                )
                
                async for chunk in stream:
                    try:
                        if chunk.choices and len(chunk.choices) > 0:
                            delta = chunk.choices[0].delta
                            if delta and delta.content:
                                content = delta.content
                                full_response += content
                                yield content
                    except (IndexError, AttributeError):
                        continue
                
                # After streaming is complete, save full response to session
                if full_response:
                    full_response = full_response.strip()
                    self.session_manager.add_message_to_session(session_id, "assistant", full_response)
                else:
                    logger.warning(f"Empty response from report answer agent for message: {message}")
                    error_msg = "I apologize, but I couldn't generate a response. Could you please rephrase your question?"
                    self.session_manager.add_message_to_session(session_id, "assistant", error_msg)
                    yield error_msg
                    
            except Exception as e:
                logger.error(f"Error in chat completion: {e}", exc_info=True)
                error_response = "I apologize, but I encountered an error processing your request. Could you please try again?"
                self.session_manager.add_message_to_session(session_id, "assistant", error_response)
                yield error_response
        
        async for chunk in stream_with_collection():
            yield chunk

