"""
OpenRouter Companion - Utilities for working with OpenRouter models.
"""

from .filters import ModelFilter
from .types import ModelInfo, FilterConfig
from .enums import ModelCapability, SortOrder
from .utils import get_client

__version__ = "0.1.0"
__all__ = [
    "ModelFilter",
    "ModelInfo",
    "FilterConfig",
    "ModelCapability",
    "SortOrder",
    "get_client",
]