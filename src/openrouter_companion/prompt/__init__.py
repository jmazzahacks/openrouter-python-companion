"""
OpenRouter Companion Prompt Package - Prompt management utilities.
"""

from .base import Prompt
from .template_loader import FileTemplatePrompt
from .string_template import StringTemplatePrompt

__all__ = [
    "Prompt",
    "FileTemplatePrompt",
    "StringTemplatePrompt",
]