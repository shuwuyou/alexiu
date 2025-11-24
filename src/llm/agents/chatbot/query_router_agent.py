"""Query Router Agent for classifying queries."""

from typing import Dict, Any, Optional
from src.llm.clients.openai_client import OpenAIClient
from src.utils.message_builder import MessageBuilder
from src.utils.response_utils import extract_json_from_response
import logging

logger = logging.getLogger(__name__)


class QueryRouterAgent:
    """Agent responsible for classifying queries as report-related or general.
    
    Classifies rewritten queries to determine if they need player report data
    or can be answered with general soccer knowledge.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the Query Router Agent.
        
        Args:
            config: Optional config dict. If not provided, uses default from model_configs.
        """
        self.config = config or {}
        self.client = OpenAIClient(config=self.config)
        
        # Load prompts and schema from global_configs
        try:
            from src.global_configs import (
                QUERY_ROUTER_AGENT_SYSTEM_PROMPT,
                QUERY_ROUTER_AGENT_USER_PROMPT,
                QUERY_ROUTER_SCHEMA
            )
            self.system_prompt = QUERY_ROUTER_AGENT_SYSTEM_PROMPT
            self.user_prompt_template = QUERY_ROUTER_AGENT_USER_PROMPT
            self.schema = QUERY_ROUTER_SCHEMA
        except ImportError:
            logger.warning("Query router prompts/schema not found in global_configs, using defaults")
            self.system_prompt = None
            self.user_prompt_template = None
            self.schema = None
    
    async def route(self, rewritten_query: str) -> str:
        """Classify a rewritten query.
        
        Args:
            rewritten_query: The rewritten/normalized query string
        
        Returns:
            Classification string: "report" or "general"
        """
        # Prepare user prompt
        if self.user_prompt_template:
            user_prompt = self.user_prompt_template.format(
                query=rewritten_query
            )
        else:
            # Default prompt if template not loaded
            user_prompt = f"""Classify the following query about soccer players.

                Query: {rewritten_query}

                Is this query about a specific player that would require player report data, or is it a general soccer question?

                Return "report" if it needs player report data, or "general" if it's a general question."""
        
        # Build messages
        messages = MessageBuilder()
        if self.system_prompt:
            messages.add_system_message(self.system_prompt)
        messages.add_user_message(user_prompt)
        
        # Prepare response format with structured output
        if self.schema:
            response_format = {
                "type": "json_schema",
                "json_schema": {
                    "name": "query_classification",
                    "schema": self.schema,
                    "strict": True
                }
            }
        else:
            response_format = None
        
        # Call Chat Completions API
        response = await self.client.chat_completion(
            messages=messages.build(),
            response_format=response_format
        )
        
        # Extract classification from response
        if self.schema:
            # Use structured output
            result = extract_json_from_response(response)
            if isinstance(result, dict) and "classification" in result:
                classification = result["classification"]
                if classification in ["report", "general"]:
                    return classification
        
        # Fallback: try to extract from text response
        try:
            content = response.choices[0].message.content
            if content:
                content_lower = content.strip().lower()
                if "report" in content_lower:
                    return "report"
                elif "general" in content_lower:
                    return "general"
        except (IndexError, AttributeError):
            pass
        
        # Default fallback
        logger.warning(f"Could not classify query: {rewritten_query}, defaulting to 'general'")
        return "general"

