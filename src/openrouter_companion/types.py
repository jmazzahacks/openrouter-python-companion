"""
Type definitions for OpenRouter Companion.
"""

from typing import Any, List, Optional, Callable
from dataclasses import dataclass, field


class ModelInfo:
    """Wrapper for OpenRouter model information with utility methods."""
    
    def __init__(self, model: Any) -> None:
        """
        Initialize ModelInfo from an OpenRouter model object.
        
        Args:
            model: Raw model object from OpenRouter API
        """
        self._model = model
        
    def __getattr__(self, name: str) -> Any:
        """Delegate attribute access to the wrapped model."""
        return getattr(self._model, name)
    
    @property
    def id(self) -> str:
        """Get model ID."""
        return self._model.id
    
    @property
    def name(self) -> Optional[str]:
        """Get model name."""
        return getattr(self._model, 'name', None)
    
    @property
    def description(self) -> Optional[str]:
        """Get model description."""
        return getattr(self._model, 'description', None)
    
    @property
    def pricing(self) -> Optional[Any]:
        """Get model pricing object."""
        return getattr(self._model, 'pricing', None)
    
    @property
    def architecture(self) -> Optional[Any]:
        """Get model architecture object."""
        return getattr(self._model, 'architecture', None)
    
    @property
    def supported_parameters(self) -> Optional[List[str]]:
        """Get supported parameters list."""
        return getattr(self._model, 'supported_parameters', None)
    
    @property
    def context_length(self) -> Optional[int]:
        """Get context length."""
        return getattr(self._model, 'context_length', None)
    
    def get_pricing_per_1m_tokens(self) -> float:
        """
        Get prompt pricing per 1M tokens.
        
        Returns:
            float: Price per 1M tokens, or float('inf') if pricing unavailable
        """
        if self.pricing and hasattr(self.pricing, 'prompt'):
            try:
                prompt_price = float(self.pricing.prompt)
                return prompt_price * 1_000_000
            except (ValueError, TypeError):
                return float('inf')
        return float('inf')
    
    def get_image_pricing(self) -> Optional[float]:
        """
        Get image pricing if available.
        
        Returns:
            float: Price per image, or None if not available
        """
        if self.pricing and hasattr(self.pricing, 'image'):
            try:
                image_price = float(self.pricing.image)
                if image_price > 0:
                    return image_price
            except (ValueError, TypeError):
                pass
        return None
    
    def is_free(self) -> bool:
        """Check if the model is free to use."""
        return self.get_pricing_per_1m_tokens() == 0
    
    def has_pricing(self) -> bool:
        """Check if the model has pricing information."""
        return self.get_pricing_per_1m_tokens() < float('inf')
    
    def supports_images(self) -> bool:
        """Check if model supports image input."""
        if self.architecture and hasattr(self.architecture, 'input_modalities'):
            modalities = self.architecture.input_modalities
            return bool(modalities) and ('image' in modalities)
        return False
    
    def supports_structured_output(self) -> bool:
        """Check if model supports structured output."""
        if self.supported_parameters:
            return ('response_format' in self.supported_parameters or 
                    'structured_outputs' in self.supported_parameters)
        return False
    
    def get_sort_name(self) -> str:
        """Get name for sorting (uses ID if name not available)."""
        return self.name or self.id
    
    def get_context_length_sort(self) -> int:
        """Get context length for sorting (0 if not available)."""
        return self.context_length or 0


def _default_deprecation_keywords() -> List[str]:
    return [
        'deprecated',
        'removed',
        'discontinued',
        'being deprecated',
    ]


@dataclass
class FilterConfig:
    """Configuration for model filtering."""
    include_deprecated: bool = False
    deprecation_keywords: List[str] = field(default_factory=_default_deprecation_keywords)