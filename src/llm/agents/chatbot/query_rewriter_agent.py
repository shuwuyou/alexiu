"""Query Rewriter Agent for normalizing user queries."""

from typing import Dict, Any, Optional, List
from src.llm.clients.openai_client import OpenAIClient
from src.utils.message_builder import MessageBuilder
import logging

logger = logging.getLogger(__name__)


class QueryRewriterAgent:
    """Agent responsible for rewriting and normalizing user queries.
    
    Rewrites raw user queries into clear, self-contained questions
    optimized for retrieval and analysis. Resolves pronouns using
    conversation history.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the Query Rewriter Agent.
        
        Args:
            config: Optional config dict. If not provided, uses default from model_configs.
        """
        self.config = config or {}
        self.client = OpenAIClient(config=self.config)
        
        # Load prompts from global_configs
        try:
            from src.global_configs import (
                QUERY_REWRITER_AGENT_SYSTEM_PROMPT,
                QUERY_REWRITER_AGENT_USER_PROMPT
            )
            self.system_prompt = QUERY_REWRITER_AGENT_SYSTEM_PROMPT
            self.user_prompt_template = QUERY_REWRITER_AGENT_USER_PROMPT
        except ImportError:
            logger.warning("Query rewriter prompts not found in global_configs, using defaults")
            self.system_prompt = None
            self.user_prompt_template = None
    
    async def rewrite(
        self,
        message: str,
        history: Optional[List[Dict[str, str]]] = None
    ) -> str:
        """Rewrite the input message into a clear, normalized query.
        
        Args:
            message: The user's raw message/query
            history: Optional conversation history as list of {"role": "user/assistant", "content": "..."}
        
        Returns:
            A rewritten query string
        """
        # Prepare conversation history (last 6 messages for context)
        history_text = "No previous conversation."
        if history:
            recent_messages = history[-6:]
            history_lines = []
            for msg in recent_messages:
                role = msg.get("role", "user")
                content = msg.get("content", "").strip()
                if content:
                    history_lines.append(f"{role}: {content}")
            if history_lines:
                history_text = "\n".join(history_lines)
        
        # Prepare user prompt
        if self.user_prompt_template:
            user_prompt = self.user_prompt_template.format(
                history=history_text,
                question=message
            )
        else:
            # Default prompt if template not loaded
            user_prompt = f"""Rewrite this query to be clear and self-contained.

                Conversation History:
                {history_text if history_text else "No previous conversation."}

                User Question: {message}

                Rewritten Query:"""
                        
        # Build messages
        messages = MessageBuilder()
        if self.system_prompt:
            messages.add_system_message(self.system_prompt)
        messages.add_user_message(user_prompt)
        
        # Call Chat Completions API
        response = await self.client.chat_completion(
            messages=messages.build()
        )
        
        # Extract text response
        try:
            content = response.choices[0].message.content
            if not content:
                logger.warning(f"Empty response from query rewriter for query: {message}")
                return message  
            result = content.strip()
            if not result:  
                return message
            return result
        except (IndexError, AttributeError) as e:
            logger.error(f"Failed to extract response: {e}")
            return message 

