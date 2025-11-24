"""Async OpenAI client for chat completions."""

from typing import Optional, List, Dict, Any
from openai import AsyncOpenAI
from src.global_configs import OPENAI_API_KEY
from dotenv import load_dotenv

load_dotenv()



class OpenAIClient:
    """Async OpenAI client wrapper for chat completions."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the async OpenAI client.
        
        Args:
            config: Optional config dict with model parameters. If not provided,
                   uses defaults. Config keys: model, temperature, max_completion_tokens,
                   top_p, frequency_penalty, presence_penalty, stream.
        """
        self.api_key = OPENAI_API_KEY
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in global_configs")
        
        self.client = AsyncOpenAI(api_key=self.api_key)
        self.config = config or {}
    
    async def chat_completion(
        self,
        messages: Optional[List[Dict[str, str]]] = None,
        reasoning_effort: Optional[str] = None,
        response_format: Optional[Dict[str, Any]] = None,
        **kwargs: Any
    ):
        """Create a chat completion asynchronously.
        
        Args:
            messages: List of message dicts with 'role' and 'content' keys.
                     Example: [{"role": "user", "content": "Hello!"}]
                     If not provided, uses default "Hello" message.
            reasoning_effort: Reasoning effort level for reasoning models.
                            - gpt-5.1: "none" (default), "low", "medium", "high"
                            - Other models: "none", "minimal", "low", "medium", "high"
                            Reducing effort = faster responses, fewer reasoning tokens.
            response_format: Response format specification. Options:
                - {"type": "text"}: Default text response
                - {"type": "json_object"}: JSON object (requires instruction)
                - {"type": "json_schema", "json_schema": {...}}: Structured output
            **kwargs: Additional parameters:
                - model: Model to use (default from config or "gpt-5.1")
                - temperature: Sampling temperature (default from config or 1.0)
                - max_completion_tokens: Max tokens to generate (default from config)
                - stream: Whether to stream (default from config or False)
                - top_p, frequency_penalty, presence_penalty, etc.
            
        Returns:
            ChatCompletion response object.
        
        Usage:
            # Basic usage
            client = OpenAIClient()
            response = await client.chat_completion(messages=[...])
            
            # With structured output
            response = await client.chat_completion(
                messages=[...],
                response_format={
                    "type": "json_schema",
                    "json_schema": {
                        "name": "player_report",
                        "schema": {...},
                        "strict": True
                    }
                }
            )
        """
        # Use default messages if not provided
        if messages is None:
            messages = [{"role": "user", "content": "Hello"}]
        
        # Build params with priority: explicit args > kwargs > config > defaults
        params = {
            "messages": messages,
            "model": kwargs.pop("model", None) if "model" in kwargs else self.config.get("model", "gpt-5.1"),
            "temperature": kwargs.pop("temperature", None) if "temperature" in kwargs else self.config.get("temperature", 1.0),
            "stream": kwargs.pop("stream", None) if "stream" in kwargs else self.config.get("stream", False),
            "max_completion_tokens": kwargs.pop("max_completion_tokens", None) if "max_completion_tokens" in kwargs else self.config.get("max_completion_tokens"),
            "top_p": kwargs.pop("top_p", None) if "top_p" in kwargs else self.config.get("top_p"),
            "frequency_penalty": kwargs.pop("frequency_penalty", None) if "frequency_penalty" in kwargs else self.config.get("frequency_penalty"),
            "presence_penalty": kwargs.pop("presence_penalty", None) if "presence_penalty" in kwargs else self.config.get("presence_penalty"),
            "reasoning_effort": reasoning_effort if reasoning_effort is not None else self.config.get("reasoning_effort"),
            "response_format": response_format if response_format is not None else self.config.get("response_format"),
        }
        
        # Remove None values to avoid sending them to API
        params = {k: v for k, v in params.items() if v is not None}
        
        # Add remaining kwargs
        params.update(kwargs)
        
        return await self.client.chat.completions.create(**params)
