"""Route handler for report generation."""

from fastapi import APIRouter, HTTPException
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
import logging

from src.llm.orchestrators.report_orchestrator import ReportOrchestrator

logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api/reports", tags=["reports"])

# Initialize orchestrator
orchestrator = ReportOrchestrator()


class GenerateReportRequest(BaseModel):
    """Request model for generating a player report."""
    player_data: Dict[str, Any] = Field(
        ...,
        description="Combined player stats and ML model output in JSON format"
    )
    player_name: Optional[str] = Field(
        None,
        description="Name of the player (optional, will be extracted from player_data if not provided)"
    )
    club: Optional[str] = Field(
        None,
        description="Club name (optional, will be extracted from player_data if not provided)"
    )


class GenerateReportResponse(BaseModel):
    """Response model for report generation."""
    success: bool
    report: Optional[Dict[str, Any]] = Field(
        None,
        description="Generated player report following report_schema.json structure"
    )
    message: Optional[str] = Field(
        None,
        description="Error message if generation failed"
    )


@router.post("/generate", response_model=GenerateReportResponse)
async def generate_report(request: GenerateReportRequest):
    """Generate a comprehensive player report.
    
    This endpoint orchestrates all agents to create a complete player analysis report
    covering player development, breakout potential, and valuations.
    
    **Request Body:**
    - `player_data`: Required. Dictionary containing player statistics and ML predictions
    - `player_name`: Optional. Will be extracted from player_data if not provided
    - `club`: Optional. Will be extracted from player_data if not provided
    
    **Response:**
    - `success`: Boolean indicating if generation was successful
    - `report`: The generated report (if successful)
    - `message`: Error message (if failed)
    """
    try:
        logger.info(f"Generating report for player: {request.player_name or 'unknown'}")
        
        # Generate report using orchestrator
        report = await orchestrator.generate_player_report(
            player_data=request.player_data,
            player_name=request.player_name,
            club=request.club
        )
        
        logger.info("Report generated successfully")
        
        return GenerateReportResponse(
            success=True,
            report=report
        )
    
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    
    except Exception as e:
        logger.error(f"Error generating report: {e}", exc_info=True)
        return GenerateReportResponse(
            success=False,
            message=f"Failed to generate report: {str(e)}"
        )

