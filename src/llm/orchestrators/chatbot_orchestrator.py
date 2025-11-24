"""Orchestrator for coordinating chatbot agents."""

from typing import Dict, Any, Optional, AsyncGenerator
from src.llm.agents.chatbot import (
    QueryRewriterAgent,
    QueryRouterAgent,
    GeneralChatbotAgent,
    ReportAnswerAgent
)
from src.utils.session_manager import SessionManager
from src.global_configs import (
    QUERY_REWRITER_AGENT_CONFIGS,
    QUERY_ROUTER_AGENT_CONFIGS,
    GENERAL_CHATBOT_AGENT_CONFIGS,
    REPORT_ANSWER_AGENT_CONFIGS
)
import logging

logger = logging.getLogger(__name__)


class ChatbotOrchestrator:
    """Orchestrator that coordinates query rewriting, routing, and chatbot responses.
    
    Flow:
    1. Rewrite user query using QueryRewriterAgent
    2. Route query using QueryRouterAgent (report vs general)
    3. Pass to appropriate chatbot (GeneralChatbotAgent or ReportAnswerAgent)
    4. Both chatbots use the same session_id for conversation continuity
    """
    
    def __init__(
        self,
        query_rewriter_config: Optional[Dict[str, Any]] = None,
        query_router_config: Optional[Dict[str, Any]] = None,
        general_chatbot_config: Optional[Dict[str, Any]] = None,
        report_answer_config: Optional[Dict[str, Any]] = None,
        session_manager: Optional[SessionManager] = None
    ):
        """Initialize the Chatbot Orchestrator.
        
        Args:
            query_rewriter_config: Optional config for QueryRewriterAgent
            query_router_config: Optional config for QueryRouterAgent
            general_chatbot_config: Optional config for GeneralChatbotAgent
            report_answer_config: Optional config for ReportAnswerAgent
            session_manager: Optional shared SessionManager instance
        """
        # Create shared session manager if not provided
        self.session_manager = session_manager if session_manager is not None else SessionManager()
        
        # Initialize all agents with shared session manager
        self.query_rewriter = QueryRewriterAgent(
            config=query_rewriter_config or QUERY_REWRITER_AGENT_CONFIGS
        )
        self.query_router = QueryRouterAgent(
            config=query_router_config or QUERY_ROUTER_AGENT_CONFIGS
        )
        self.general_chatbot = GeneralChatbotAgent(
            config=general_chatbot_config or GENERAL_CHATBOT_AGENT_CONFIGS,
            session_manager=self.session_manager
        )
        self.report_answer_agent = ReportAnswerAgent(
            config=report_answer_config or REPORT_ANSWER_AGENT_CONFIGS,
            session_manager=self.session_manager
        )
        
        logger.info("ChatbotOrchestrator initialized with shared SessionManager")
    
    async def process_message(
        self,
        user_id: str,
        message: str,
        session_id: Optional[str] = None,
        report: Optional[Dict[str, Any]] = None,
        player_data: Optional[Dict[str, Any]] = None
    ) -> AsyncGenerator[str, None]:
        """Process a user message through the full chatbot pipeline.
        
        Args:
            user_id: Unique identifier for the user
            message: User's raw message/query
            session_id: Optional session ID (creates new if None, both agents use same ID)
            report: Optional player report data (required if routing to report agent)
            player_data: Optional original player statistics and ML model output data
        
        Yields:
            Response chunks as strings
        """
        # Step 1: Get or create session (shared between both chatbots)
        if session_id is None:
            session_id = await self.session_manager.start_session(user_id)
            logger.info(f"ChatbotOrchestrator: Created new session {session_id} for user {user_id}")
        else:
            logger.info(f"ChatbotOrchestrator: Using existing session {session_id} for user {user_id}")
            # Check if session exists, create if not
            if not self.session_manager.session_exists(session_id):
                logger.warning(f"ChatbotOrchestrator: Session {session_id} not found, creating new session")
                session_id = await self.session_manager.start_session(user_id)
        
        # Step 2: Get conversation history and rewrite the query
        conversation_history = self.session_manager.get_conversation_history(session_id)
        
        try:
            rewritten_query = await self.query_rewriter.rewrite(
                message=message,
                history=conversation_history
            )
            logger.info(f"ChatbotOrchestrator: Rewritten query: {rewritten_query}")
        except Exception as e:
            logger.error(f"ChatbotOrchestrator: Query rewriting failed: {e}", exc_info=True)
            # Fallback to original message if rewriting fails
            rewritten_query = message
        
        # Step 3: Route the rewritten query
        try:
            route = await self.query_router.route(rewritten_query)
            logger.info(f"ChatbotOrchestrator: Query routed to: {route}")
        except Exception as e:
            logger.error(f"ChatbotOrchestrator: Query routing failed: {e}", exc_info=True)
            # Default to general if routing fails
            route = "general"
        
        # Step 4: Pass to appropriate chatbot (both use same session_id)
        # Use rewritten query for better LLM understanding (resolves pronouns, makes self-contained)
        message_to_process = rewritten_query
        
        if route == "report":
            # Route to report answer agent
            if not report:
                logger.warning("ChatbotOrchestrator: Route is 'report' but no report provided, falling back to general")
                # Fallback to general chatbot if no report available
                async for chunk in self.general_chatbot.process_message(
                    user_id=user_id,
                    message=message_to_process,
                    session_id=session_id
                ):
                    yield chunk
            else:
                # Use report answer agent with same session_id
                async for chunk in self.report_answer_agent.process_message(
                    user_id=user_id,
                    message=message_to_process,
                    report=report,
                    player_data=player_data,
                    session_id=session_id
                ):
                    yield chunk
        else:
            # Route to general chatbot with same session_id
            async for chunk in self.general_chatbot.process_message(
                user_id=user_id,
                message=message_to_process,
                session_id=session_id
            ):
                yield chunk

