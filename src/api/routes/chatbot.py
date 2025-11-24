"""Route handler for chatbot interactions."""

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
import logging

from src.llm.orchestrators.chatbot_orchestrator import ChatbotOrchestrator

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/chatbot", tags=["chatbot"])
orchestrator = ChatbotOrchestrator()


class ChatMessageRequest(BaseModel):
    """Request model for chatbot messages."""
    user_id: str
    message: str
    session_id: Optional[str] = None
    report: Optional[Dict[str, Any]] = None
    player_data: Optional[Dict[str, Any]] = None


class ReportChatRequest(BaseModel):
    """Request model for report chatbot messages (requires report)."""
    user_id: str
    message: str
    report: Dict[str, Any]  # Required for report chatbot
    session_id: Optional[str] = None
    player_data: Optional[Dict[str, Any]] = None


@router.post("/chat")
async def chat(request: ChatMessageRequest):
    """Chat with the soccer player analysis chatbot.
    
    Processes: query rewrite -> routing -> response generation
    Returns streaming text response with session_id in headers.
    """
    try:
        # Get or create session
        if not request.session_id or not orchestrator.session_manager.session_exists(request.session_id):
            session_id = await orchestrator.session_manager.start_session(request.user_id)
        else:
            session_id = request.session_id
        
        # Stream response
        async def stream_response():
            try:
                async for chunk in orchestrator.process_message(
                    user_id=request.user_id,
                    message=request.message,
                    session_id=session_id,
                    report=request.report,
                    player_data=request.player_data
                ):
                    yield chunk
            except Exception as e:
                logger.error(f"Error streaming response: {e}", exc_info=True)
                yield f"Error: {str(e)}"
        
        return StreamingResponse(
            stream_response(),
            media_type="text/plain",
            headers={"X-Session-ID": session_id}
        )
    
    except Exception as e:
        logger.error(f"Error processing chat: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/report-chat")
async def report_chat(request: ReportChatRequest):
    """Chat with report chatbot (query rewrite -> report chatbot only).
    
    Skips routing - directly uses report chatbot with query rewriting.
    Requires report data.
    """
    try:
        # Get or create session
        if not request.session_id or not orchestrator.session_manager.session_exists(request.session_id):
            session_id = await orchestrator.session_manager.start_session(request.user_id)
        else:
            session_id = request.session_id
        
        # Stream response
        async def stream_response():
            try:
                # Get conversation history
                conversation_history = orchestrator.session_manager.get_conversation_history(session_id)
                
                # Rewrite query
                try:
                    rewritten_query = await orchestrator.query_rewriter.rewrite(
                        message=request.message,
                        history=conversation_history
                    )
                    logger.info(f"Report chat: Rewritten query: {rewritten_query}")
                except Exception as e:
                    logger.error(f"Query rewriting failed: {e}", exc_info=True)
                    rewritten_query = request.message
                
                # Directly use report answer agent (skip routing)
                # Pass original message - agent will use conversation history for context
                async for chunk in orchestrator.report_answer_agent.process_message(
                    user_id=request.user_id,
                    message=request.message,  # Use original message
                    report=request.report,
                    player_data=request.player_data,
                    session_id=session_id
                ):
                    yield chunk
            except Exception as e:
                logger.error(f"Error streaming response: {e}", exc_info=True)
                yield f"Error: {str(e)}"
        
        return StreamingResponse(
            stream_response(),
            media_type="text/plain",
            headers={"X-Session-ID": session_id}
        )
    
    except Exception as e:
        logger.error(f"Error processing report chat: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

