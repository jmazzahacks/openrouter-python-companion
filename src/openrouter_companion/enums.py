"""
Enums for OpenRouter Companion.
"""

from enum import Flag, Enum, auto


class ModelCapability(Flag):
    """Flags for model capabilities that can be combined."""
    NONE = 0
    IMAGE_INPUT = auto()
    STRUCTURED_OUTPUT = auto()
    
    # Convenience combinations
    MULTIMODAL = IMAGE_INPUT
    ALL = IMAGE_INPUT | STRUCTURED_OUTPUT


class SortOrder(Enum):
    """Sort order options (single-choice)."""
    NONE = 0
    PRICE_ASC = auto()  # Cheapest first
    PRICE_DESC = auto()  # Most expensive first
    NAME_ASC = auto()
    NAME_DESC = auto()
    CONTEXT_ASC = auto()  # Smallest context first
    CONTEXT_DESC = auto()  # Largest context first