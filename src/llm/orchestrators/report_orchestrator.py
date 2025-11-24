"""Orchestrator for coordinating all report generation agents."""

from typing import Dict, Any, Optional, List
from src.llm.agents.report import (
    AnalysisAgent,
    NewsAgent,
    NewsAnalysisAgent,
    GeneratorAgent
)
from src.global_configs import (
    ANALYSIS_AGENT_CONFIGS,
    NEWS_AGENT_CONFIGS,
    NEWS_ANALYSIS_AGENT_CONFIGS,
    GENERATOR_AGENT_CONFIGS
)


class ReportOrchestrator:
    """Orchestrator that coordinates all agents to generate a complete player report."""
    
    def __init__(
        self,
        analysis_config: Optional[Dict[str, Any]] = None,
        news_config: Optional[Dict[str, Any]] = None,
        news_analysis_config: Optional[Dict[str, Any]] = None,
        generator_config: Optional[Dict[str, Any]] = None
    ):
        """Initialize the Report Orchestrator.
        
        Args:
            analysis_config: Optional config for AnalysisAgent (defaults to ANALYSIS_AGENT_CONFIGS)
            news_config: Optional config for NewsAgent (defaults to NEWS_AGENT_CONFIGS)
            news_analysis_config: Optional config for NewsAnalysisAgent (defaults to NEWS_ANALYSIS_AGENT_CONFIGS)
            generator_config: Optional config for GeneratorAgent (defaults to GENERATOR_AGENT_CONFIGS)
        """
        self.analysis_agent = AnalysisAgent(config=analysis_config or ANALYSIS_AGENT_CONFIGS)
        self.news_agent = NewsAgent(config=news_config or NEWS_AGENT_CONFIGS)
        self.news_analysis_agent = NewsAnalysisAgent(config=news_analysis_config or NEWS_ANALYSIS_AGENT_CONFIGS)
        self.generator_agent = GeneratorAgent(config=generator_config or GENERATOR_AGENT_CONFIGS)
    
    async def generate_player_report(
        self,
        player_data: Dict[str, Any],
        player_name: Optional[str] = None,
        club: Optional[str] = None
    ) -> Dict[str, Any]:
        """Generate a complete player report by orchestrating all agents.
        
        Args:
            player_data: Combined player stats and ML model output in one JSON dict.
                       Should contain player statistics and ML predictions.
            player_name: Name of the player (extracted from player_data if not provided)
            club: Club name (extracted from player_data if not provided)
        
        Returns:
            Dictionary with final report following report_schema.json structure
        
        Raises:
            ValueError: If player_name cannot be determined from player_data
        """
        # Extract player_name and club from player_data if not provided
        if not player_name:
            player_info = player_data.get("player_info", {})
            player_name = player_info.get("name")
            if not player_name:
                raise ValueError("player_name must be provided or present in player_data['player_info']['name']")
        
        if not club:
            player_info = player_data.get("player_info", {})
            club = player_info.get("club")
        
        # Step 1 & 2: Run analysis and news fetching in parallel
        import asyncio
        
        # Run analysis and news fetching concurrently
        analysis_task = self.analysis_agent.analyze(player_data)
        news_task = self.news_agent.fetch_news(player_name, club)
        
        player_analysis, news_articles = await asyncio.gather(
            analysis_task,
            news_task,
            return_exceptions=True
        )
        
        # Handle errors from parallel tasks
        if isinstance(player_analysis, Exception):
            raise RuntimeError(f"Analysis agent failed: {player_analysis}") from player_analysis
        if isinstance(news_articles, Exception):
            # News fetching failure is not critical, continue with empty list
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f"News agent failed: {news_articles}. Continuing with empty news list.")
            news_articles = []
        
        # Step 3: Analyze news (if we have news articles)
        if news_articles:
            try:
                news_analysis = await self.news_analysis_agent.analyze(news_articles)
            except Exception as e:
                import logging
                logger = logging.getLogger(__name__)
                logger.warning(f"News analysis agent failed: {e}. Continuing with empty news analysis.")
                news_analysis = {
                    "analysis": ""
                }
        else:
            # Empty news analysis if no news articles
            news_analysis = {
                "analysis": ""
            }
        
        # Step 4: Generate final report
        try:
            final_report = await self.generator_agent.generate_report(
                player_analysis=player_analysis,
                news_articles=news_articles,
                news_analysis=news_analysis
            )
            return final_report
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Generator agent failed: {e}")
            raise RuntimeError(f"Failed to generate final report: {e}") from e

