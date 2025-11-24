"""News Analysis Agent for analyzing news articles in context of problem statements."""

from typing import Dict, Any, Optional, List
from src.llm.clients.openai_client import OpenAIClient
from src.global_configs import (
    NEWS_ANALYSIS_AGENT_SYSTEM_PROMPT,
    NEWS_ANALYSIS_AGENT_USER_PROMPT,
    NEWS_ANALYSIS_SCHEMA
)
from src.utils.message_builder import MessageBuilder
from src.utils.response_utils import extract_json_from_response


class NewsAnalysisAgent:
    """Agent responsible for analyzing news articles in context of player development, breakout potential, and valuations."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the News Analysis Agent.
        
        Args:
            config: Optional config dict. If not provided, uses default from model_configs.
        """
        self.config = config or {}
        self.client = OpenAIClient(config=self.config)
        
        # Use prompts from global_configs
        self.system_prompt = NEWS_ANALYSIS_AGENT_SYSTEM_PROMPT
        self.user_prompt_template = NEWS_ANALYSIS_AGENT_USER_PROMPT
    
    async def analyze(
        self,
        news_articles: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Analyze news articles in context of the three problem statements.
        
        Args:
            news_articles: List of news articles with title, summary, date, source, relevance
            player_name: Name of the player
        
        Returns:
            Dictionary with analysis results including:
            - analysis: Concise merged analysis of how news relates to player development, breakout potential, and valuations
        """
        # Prepare news articles as JSON string
        import json
        news_json = json.dumps(news_articles, indent=2)
        
        # Prepare user prompt with news articles
        if self.user_prompt_template:
            user_prompt = self.user_prompt_template.format(
                news_articles=news_json
            )
        else:
            user_prompt = f"Analyze the following news articles about {player_name}:\n{news_json}"
        
        # Build messages
        messages = MessageBuilder()
        if self.system_prompt:
            messages.add_system_message(self.system_prompt)
        messages.add_user_message(user_prompt)
        
        # Prepare response format with structured output
        response_format = {
            "type": "json_schema",
            "json_schema": {
                "name": "news_analysis",
                "schema": NEWS_ANALYSIS_SCHEMA,
                "strict": True
            }
        }
        
        # Call Chat Completions API with structured output
        response = await self.client.chat_completion(
            messages=messages.build(),
            response_format=response_format
        )
        
        # Extract analysis from response
        analysis = extract_json_from_response(response)
        if isinstance(analysis, dict):
            return analysis
        
        # Debug: Log raw response if extraction fails
        if hasattr(response, 'choices') and len(response.choices) > 0:
            import logging
            logger = logging.getLogger(__name__)
            content = response.choices[0].message.content
            logger.warning(f"Failed to extract JSON from response. Raw content: {content[:500] if content else 'None'}")
        
        # Fallback: return empty dict
        return {
            "analysis": ""
        }

