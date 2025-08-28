"""
Utility functions for OpenRouter Companion.
"""

import os
from typing import Optional
from openrouter_client import OpenRouterClient


def get_client(api_key: Optional[str] = None) -> OpenRouterClient:
    """
    Create an OpenRouter client instance.
    
    Args:
        api_key: Optional API key. If not provided, uses OPENROUTER_API_KEY env var.
        
    Returns:
        OpenRouterClient: Configured client instance
        
    Raises:
        ValueError: If no API key is provided and OPENROUTER_API_KEY is not set
    """
    if api_key is None:
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise ValueError(
                "No API key provided. Either pass api_key parameter or "
                "set OPENROUTER_API_KEY environment variable."
            )
    
    return OpenRouterClient(api_key=api_key)