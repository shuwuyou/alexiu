"""Generator Agent for combining all analysis into final report."""

from typing import Dict, Any, Optional, List
from datetime import datetime
from src.llm.clients.openai_client import OpenAIClient
from src.global_configs import (
    GENERATOR_AGENT_SYSTEM_PROMPT,
    GENERATOR_AGENT_USER_PROMPT,
    REPORT_SCHEMA
)
from src.utils.message_builder import MessageBuilder
from src.utils.response_utils import extract_json_from_response


class GeneratorAgent:
    """Agent responsible for combining all analyses into a final comprehensive report."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the Generator Agent.
        
        Args:
            config: Optional config dict. If not provided, uses default from model_configs.
        """
        self.config = config or {}
        self.client = OpenAIClient(config=self.config)
        
        # Use prompts from global_configs
        self.system_prompt = GENERATOR_AGENT_SYSTEM_PROMPT
        self.user_prompt_template = GENERATOR_AGENT_USER_PROMPT
    
    async def generate_report(
        self,
        player_analysis: Dict[str, Any],
        news_articles: List[Dict[str, Any]],
        news_analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate final report by combining all analyses.
        
        Args:
            player_analysis: Analysis results from AnalysisAgent
            news_articles: News articles from NewsAgent
            news_analysis: News analysis from NewsAnalysisAgent
        
        Returns:
            Dictionary with final report following report_schema.json structure
        """
        # Prepare data as JSON strings
        import json
        player_analysis_json = json.dumps(player_analysis, indent=2)
        news_articles_json = json.dumps(news_articles, indent=2)
        news_analysis_json = json.dumps(news_analysis, indent=2)
        
        # Prepare user prompt
        if self.user_prompt_template:
            user_prompt = self.user_prompt_template.format(
                player_analysis=player_analysis_json,
                news_articles=news_articles_json,
                news_analysis=news_analysis_json
            )
        else:
            user_prompt = f"Combine the following into a final report:\nPlayer Analysis: {player_analysis_json}\nNews: {news_articles_json}\nNews Analysis: {news_analysis_json}"
        
        # Build messages
        messages = MessageBuilder()
        if self.system_prompt:
            messages.add_system_message(self.system_prompt)
        messages.add_user_message(user_prompt)
        
        # Prepare response format with structured output
        response_format = {
            "type": "json_schema",
            "json_schema": {
                "name": "player_report",
                "schema": REPORT_SCHEMA,
                "strict": True
            }
        }
        
        # Call Chat Completions API with structured output
        response = await self.client.chat_completion(
            messages=messages.build(),
            response_format=response_format
        )
        
        # Extract report from response
        report = extract_json_from_response(response)
        if isinstance(report, dict):
            # Ensure generated_at is set
            if "generated_at" not in report or not report["generated_at"]:
                report["generated_at"] = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
            return report
        
        # Debug: Log raw response if extraction fails
        if hasattr(response, 'choices') and len(response.choices) > 0:
            import logging
            logger = logging.getLogger(__name__)
            content = response.choices[0].message.content
            logger.warning(f"Failed to extract JSON from response. Raw content: {content[:500] if content else 'None'}")
        
        # Fallback: return empty report structure with timestamp (matching new schema)
        return {
            "player_info": player_analysis.get("player_info", {}),
            "report": {
                "executive_summary": player_analysis.get("executive_summary", ""),
                "player_development": player_analysis.get("player_development", ""),
                "breakout_analysis": player_analysis.get("breakout_analysis", ""),
                "valuation_insights": player_analysis.get("valuation_insights", ""),
                "transfer_fee_analysis": player_analysis.get("transfer_fee_analysis", ""),
                "key_statistics": player_analysis.get("key_statistics", {}),
                "strengths": player_analysis.get("strengths", []),
                "weaknesses": player_analysis.get("weaknesses", []),
                "recommendation": player_analysis.get("recommendation", ""),
                "news_context": news_analysis.get("analysis", "")
            },
            "news": news_articles,
            "generated_at": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        }

