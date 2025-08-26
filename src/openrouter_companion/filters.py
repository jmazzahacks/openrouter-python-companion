"""
Model filtering functionality for OpenRouter models.
"""

from typing import List, Optional
from openrouter_client import OpenRouterClient

from .types import ModelInfo, FilterConfig
from .enums import ModelCapability, SortOrder
from .utils import get_client


class ModelFilter:
    """Filter and sort OpenRouter models based on various criteria."""
    
    def __init__(
        self, 
        client: Optional[OpenRouterClient] = None,
        api_key: Optional[str] = None
    ):
        """
        Initialize ModelFilter.
        
        Args:
            client: Optional OpenRouter client instance
            api_key: Optional API key (used if client not provided)
        """
        self.client = client or get_client(api_key)
        
    def _is_deprecated(self, model: ModelInfo, config: FilterConfig) -> bool:
        """
        Check if a model is deprecated based on its description.
        
        Args:
            model: Model information object
            config: Filter configuration
            
        Returns:
            bool: True if model appears to be deprecated
        """
        if not model.description:
            return False
            
        desc_lower = model.description.lower()
        return any(keyword in desc_lower for keyword in config.deprecation_keywords)
    
    def _fetch_models(self, details: bool = True) -> List[ModelInfo]:
        """
        Fetch all models from OpenRouter API and wrap them in ModelInfo.
        
        Args:
            details: Whether to fetch detailed model information
            
        Returns:
            List of ModelInfo objects
        """
        response = self.client.models.list(details=details)
        return [ModelInfo(model) for model in response.data]
    
    def _apply_sort(self, models: List[ModelInfo], sort_order: SortOrder) -> List[ModelInfo]:
        """
        Apply sorting to a list of models.
        
        Args:
            models: List of models to sort
            sort_order: How to sort the models
            
        Returns:
            Sorted list of models (sorts in place and returns for chaining)
        """
        if sort_order == SortOrder.PRICE_ASC:
            models.sort(key=ModelInfo.get_pricing_per_1m_tokens)
        elif sort_order == SortOrder.PRICE_DESC:
            models.sort(key=ModelInfo.get_pricing_per_1m_tokens, reverse=True)
        elif sort_order == SortOrder.NAME_ASC:
            models.sort(key=ModelInfo.get_sort_name)
        elif sort_order == SortOrder.NAME_DESC:
            models.sort(key=ModelInfo.get_sort_name, reverse=True)
        elif sort_order == SortOrder.CONTEXT_ASC:
            models.sort(key=ModelInfo.get_context_length_sort)
        elif sort_order == SortOrder.CONTEXT_DESC:
            models.sort(key=ModelInfo.get_context_length_sort, reverse=True)
        
        return models
    
    def filter_models(
        self,
        capabilities: ModelCapability = ModelCapability.NONE,
        include_deprecated: bool = False,
        sort_order: SortOrder = SortOrder.PRICE_ASC
    ) -> List[ModelInfo]:
        """
        Filter models by capabilities with flexible sorting.
        
        Args:
            capabilities: Flags for required capabilities (can be combined with |)
            include_deprecated: Whether to include deprecated models
            sort_order: How to sort the results
            
        Returns:
            List of models matching all specified capabilities
            
        Examples:
            # Get models with image input
            filter_models(ModelCapability.IMAGE_INPUT)
            
            # Get models with both image input AND structured output
            filter_models(ModelCapability.IMAGE_INPUT | ModelCapability.STRUCTURED_OUTPUT)
            
            # Get all models, sorted by context length
            filter_models(sort_order=SortOrder.CONTEXT_DESC)
        """
        config = FilterConfig(include_deprecated=include_deprecated)
        models = self._fetch_models(details=True)
        
        filtered_models = []
        for model in models:
            # Check each required capability
            if capabilities & ModelCapability.IMAGE_INPUT:
                if not model.supports_images():
                    continue
            
            if capabilities & ModelCapability.STRUCTURED_OUTPUT:
                if not model.supports_structured_output():
                    continue
            
            # Skip deprecated models if configured
            if not include_deprecated and self._is_deprecated(model, config):
                continue
            
            filtered_models.append(model)
        
        return self._apply_sort(filtered_models, sort_order)
    

    

    
