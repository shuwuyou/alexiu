"""Analysis Agent for analyzing player statistics and ML model outputs."""

from typing import Dict, Any, Optional
from src.llm.clients.openai_client import OpenAIClient
from src.global_configs import (
    ANALYSIS_AGENT_SYSTEM_PROMPT,
    ANALYSIS_AGENT_USER_PROMPT,
    ANALYSIS_SCHEMA
)
from src.utils.message_builder import MessageBuilder
from src.utils.response_utils import extract_json_from_response


class AnalysisAgent:
    """Agent responsible for analyzing player statistics and ML model outputs."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the Analysis Agent.
        
        Args:
            config: Optional config dict. If not provided, uses default from model_configs.
        """
        self.config = config or {}
        self.client = OpenAIClient(config=self.config)
        
        # Use prompts from global_configs
        self.system_prompt = ANALYSIS_AGENT_SYSTEM_PROMPT
        self.user_prompt_template = ANALYSIS_AGENT_USER_PROMPT
    
    async def analyze(
        self,
        player_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Analyze player statistics and ML model outputs.
        
        Args:
            player_data: Combined player stats and ML model output in one JSON dict.
                       Should contain player statistics and ML predictions.
        
        Returns:
            Dictionary with analysis results including:
            - player_info: Basic player information (id, name, position, age, club)
            - player_development: Aging assessment and performance vs expectation
            - breakout_analysis: Breakout candidate identification and growth indicators
            - valuation_insights: Market value predictions and transfer fee analysis
            - performance_analysis: Overall performance summary
            - market_value: Estimated value and trends
            - strengths, weaknesses, recommendations
            - statistics_summary, ml_predictions
        """
        # Prepare user prompt with player data
        if self.user_prompt_template:
            import json
            user_prompt = self.user_prompt_template.format(
                player_data=json.dumps(player_data, indent=2)
            )
        else:
            import json
            user_prompt = f"Analyze the following player data:\n{json.dumps(player_data, indent=2)}"
        
        # Build messages
        messages = MessageBuilder()
        if self.system_prompt:
            messages.add_system_message(self.system_prompt)
        messages.add_user_message(user_prompt)
        
        # Prepare response format with structured output
        response_format = {
            "type": "json_schema",
            "json_schema": {
                "name": "player_analysis",
                "schema": ANALYSIS_SCHEMA,
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
        return {}

