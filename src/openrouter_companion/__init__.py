"""
OpenRouter Companion - Utilities for working with OpenRouter models.
"""

from .filters import ModelFilter
from .types import ModelInfo, FilterConfig
from .enums import ModelCapability, SortOrder
from .prompt import Prompt, FileTemplatePrompt, StringTemplatePrompt

__version__ = "0.1.13"
__all__ = [
    "ModelFilter",
    "ModelInfo",
    "FilterConfig",
    "ModelCapability",
    "SortOrder",
    "Prompt",
    "FileTemplatePrompt",
    "StringTemplatePrompt",
]