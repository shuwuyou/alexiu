"""Session manager for chatbot conversations."""

from typing import Dict, List, Optional
from datetime import datetime, timezone
import uuid
import logging

logger = logging.getLogger(__name__)


class SessionManager:
    """
    Manages temporary conversation sessions for the chatbot.
    Sessions are stored in-memory and lost when server restarts.
    """
    
    def __init__(self):
        """Initialize the session manager."""
        self.sessions: Dict[str, Dict] = {}  # {session_id: session_data}
    
    async def start_session(self, user_id: str) -> str:
        """
        Start a new temporary conversation session.
        
        Args:
            user_id: Unique identifier for the user
            
        Returns:
            Session ID
        """
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = {
            'user_id': user_id,
            'messages': [],
            'created_at': datetime.now(timezone.utc),
            'last_activity': datetime.now(timezone.utc)
        }
        logger.info(f"Started new session {session_id} for user {user_id}")
        return session_id
    
    async def end_session(self, session_id: str) -> bool:
        """
        End a temporary conversation session.
        
        Args:
            session_id: Session ID to end
            
        Returns:
            True if session was ended, False if not found
        """
        if session_id in self.sessions:
            del self.sessions[session_id]
            logger.info(f"Ended session {session_id}")
            return True
        return False
    
    def clear_session(self, session_id: str) -> bool:
        """
        Clear all messages from a session (start fresh conversation).
        
        Args:
            session_id: Session ID to clear
            
        Returns:
            True if session was cleared, False if not found
        """
        if session_id in self.sessions:
            self.sessions[session_id]['messages'] = []
            logger.info(f"Cleared messages from session {session_id}")
            return True
        return False
    
    def add_message_to_session(self, session_id: str, role: str, content: str) -> bool:
        """
        Add a message to a session.
        
        Args:
            session_id: Session ID
            role: Message role (user/assistant)
            content: Message content
            
        Returns:
            True if message was added, False if session not found
        """
        if session_id in self.sessions:
            self.sessions[session_id]['messages'].append({
                'role': role,
                'content': content,
                'timestamp': datetime.now(timezone.utc)
            })
            self.sessions[session_id]['last_activity'] = datetime.now(timezone.utc)
            return True
        return False

    def get_conversation_history(self, session_id: str) -> List[Dict[str, str]]:
        """
        Get conversation history for a session.
        
        Args:
            session_id: Session ID
            
        Returns:
            List of messages with role and content
        """
        if session_id in self.sessions:
            return [
                {'role': msg['role'], 'content': msg['content']} 
                for msg in self.sessions[session_id]['messages']
            ]
        return []
    
    def get_session_info(self, session_id: str) -> Optional[Dict]:
        """
        Get information about a session.
        
        Args:
            session_id: Session ID
            
        Returns:
            Session info dict or None if not found
        """
        return self.sessions.get(session_id)
    
    def list_sessions(self, user_id: str) -> List[str]:
        """
        List all sessions for a user.
        
        Args:
            user_id: User ID
            
        Returns:
            List of session IDs
        """
        return [
            sid for sid, session in self.sessions.items() 
            if session['user_id'] == user_id
        ]
    
    def session_exists(self, session_id: str) -> bool:
        """
        Check if a session exists.
        
        Args:
            session_id: Session ID
            
        Returns:
            True if session exists, False otherwise
        """
        return session_id in self.sessions
    
    def add_rag_context(self, session_id: str, rag_context: str) -> bool:
        """Add RAG context to a session."""
        if session_id not in self.sessions:
            return False
        self.sessions[session_id]["rag_context"] = rag_context
        return True
    
    def retrieve_rag_context(self, session_id: str) -> Optional[str]:
        """Get RAG context from a session."""
        if session_id not in self.sessions:
            return None
        return self.sessions[session_id].get("rag_context", "")

