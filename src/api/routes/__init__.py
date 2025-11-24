"""API routes package."""

from src.api.routes.generator import router as generator_router
from src.api.routes.chatbot import router as chatbot_router

__all__ = ["generator_router", "chatbot_router"]

