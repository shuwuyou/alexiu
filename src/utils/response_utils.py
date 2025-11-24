"""Utilities for extracting data from OpenAI API responses."""

import json
import re
from typing import Any, Optional


def extract_json_from_response(response: Any, key: Optional[str] = None) -> Optional[Any]:
    """Extract JSON from OpenAI ChatCompletion or Responses API response.
    
    Args:
        response: OpenAI ChatCompletion or Responses API response object
        key: Optional key to extract from the parsed JSON (e.g., "news", "data")
            If provided and the parsed JSON is a dict, returns value at that key.
            If None, returns the entire parsed JSON.
    
    Returns:
        Parsed JSON object, or value at key if key is provided, or None if extraction fails
    
    Examples:
        # Extract entire JSON
        data = extract_json_from_response(response)
        
        # Extract specific key
        news = extract_json_from_response(response, key="news")
    """
    try:
        # Handle Responses API format
        if hasattr(response, 'output_text'):
            content = response.output_text
        # Handle ChatCompletion format
        elif hasattr(response, 'choices') and len(response.choices) > 0:
            content = response.choices[0].message.content
        else:
            return None
            
        if not content:
            return None
        
        # Try to parse JSON directly
        try:
            parsed = json.loads(content)
        except json.JSONDecodeError:
            # Try to extract JSON from markdown code blocks
            json_match = re.search(r'```(?:json)?\s*(\{.*?\}|\[.*?\])\s*```', content, re.DOTALL)
            if json_match:
                parsed = json.loads(json_match.group(1))
            else:
                # Try to find JSON object/array in the text
                json_match = re.search(r'(\{.*\}|\[.*\])', content, re.DOTALL)
                if json_match:
                    parsed = json.loads(json_match.group(1))
                else:
                    return None
        
        # Extract key if specified
        if key and isinstance(parsed, dict):
            return parsed.get(key)
        
        return parsed
        
    except (json.JSONDecodeError, AttributeError, KeyError, IndexError):
        return None

