"""News Agent for fetching player news using OpenAI web search."""

from typing import List, Dict, Any, Optional
from src.llm.clients.openai_client import OpenAIClient
from src.global_configs import NEWS_AGENT_USER_PROMPT
from src.utils.response_utils import extract_json_from_response


class NewsAgent:
    """Agent responsible for fetching and processing player news."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the News Agent.
        
        Args:
            config: Optional config dict. If not provided, uses default from model_configs.
        """
        self.config = config or {}
        self.client = OpenAIClient(config=self.config)
        
        # Use prompts from global_configs
        self.user_prompt_template = NEWS_AGENT_USER_PROMPT
    
    async def fetch_news(
        self, 
        player_name: str, 
        club: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Fetch news about a player using OpenAI web search.
        
        Args:
            player_name: Name of the player
            club: Optional club name for better search context
        
        Returns:
            List of news articles with title, summary, date, source, relevance
        """
        # Prepare user prompt
        if self.user_prompt_template:
            user_prompt = self.user_prompt_template.format(
                player_name=player_name,
                club=club or "their club"
            )
        else:
            user_prompt = f"Search for recent news about {player_name}. Return a JSON array of news articles with title, summary, date, source, and relevance (high/medium/low)."
        
        # Use Responses API for web search with gpt-5.1
        # Responses API supports web search tool but not structured output
        tools = [{"type": "web_search"}]
        
        # Call Responses API with web search
        # Get reasoning effort from config (default: "low")
        reasoning_effort = self.config.get("reasoning_effort", "low")
        response = await self.client.responses_create(
            input=user_prompt,
            tools=tools,
            tool_choice="auto",
            reasoning={"effort": reasoning_effort} if reasoning_effort else None
        )
        
        # Extract news from response
        # Try to extract from "news" key first, then try direct list
        news_articles = extract_json_from_response(response, key="news")
        if isinstance(news_articles, list):
            return news_articles
        
        # Try extracting without key (might be a list directly)
        news_articles = extract_json_from_response(response)
        if isinstance(news_articles, list):
            return news_articles
        
        # Debug: Log raw response if extraction fails
        if hasattr(response, 'output_text'):
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f"Failed to extract JSON from response. Raw output: {response.output_text[:500]}")
        
        # Fallback: return empty list
        return []

