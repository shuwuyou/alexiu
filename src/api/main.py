"""FastAPI application main file."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routes.generator import router as generator_router
from src.api.routes.chatbot import router as chatbot_router
from src.api.routes.player_search import router as player_search_router

# Create FastAPI app
app = FastAPI(
    title="Player Report Generation API",
    description="API for generating comprehensive soccer player analysis reports",
    version="0.1.0"
)

# Add CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual frontend origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Session-ID", "X-User-ID"],  # Expose custom headers
)

# Include routers
app.include_router(generator_router)
app.include_router(chatbot_router)
app.include_router(player_search_router)

@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}

