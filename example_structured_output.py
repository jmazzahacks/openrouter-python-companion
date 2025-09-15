#!/usr/bin/env python
"""
Filter models that support structured output (response_format parameter).

This script queries the OpenRouter API to find models that support
structured output via the response_format parameter, filtering out
deprecated models, and sorts them by price.
"""

import sys
import os

# Add src directory to path to import the library
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from openrouter_companion import ModelFilter, ModelInfo, ModelCapability, SortOrder

if __name__ == "__main__":
    print("Finding models that support structured output (sorted by price)...\n")
    
    # Create filter instance
    filter_obj = ModelFilter()
    
    # Get models with structured output support
    models = filter_obj.filter_models(
        capabilities=ModelCapability.STRUCTURED_OUTPUT,
        include_deprecated=False,
        sort_order=SortOrder.PRICE_ASC
    )
    
    print(f"Found {len(models)} models that support structured output (cheapest first):\n")
    
    for model in models:
        print(f"- {model.id}")
        
        if model.name:
            print(f"  Name: {model.name}")
        
        # Show pricing per 1M tokens
        price_per_1m = model.get_pricing_per_1m_tokens()
        if price_per_1m == float('inf'):
            print(f"  Price: No pricing available")
        elif price_per_1m == 0:
            print(f"  Price: FREE")
        else:
            print(f"  Price: ${price_per_1m:.2f} per 1M prompt tokens")
        
        # Show structured output support details
        if model.supported_parameters:
            structured_params = [p for p in model.supported_parameters if p in ['response_format', 'structured_outputs']]
            print(f"  Structured output support: {structured_params}")
        print()
    
    print(f"\nTotal: {len(models)} models support structured output")
    
    # Show pricing summary
    free_models = [m for m in models if m.is_free()]
    paid_models = [m for m in models if m.has_pricing() and not m.is_free()]
    
    if free_models:
        print(f"- {len(free_models)} are FREE")
    if paid_models:
        cheapest = min(paid_models, key=ModelInfo.get_pricing_per_1m_tokens)
        cheapest_price = cheapest.get_pricing_per_1m_tokens()
        print(f"- Cheapest paid model: {cheapest.id} at ${cheapest_price:.2f}/1M tokens")
    
    # Also show count with deprecated models
    all_models = filter_obj.filter_models(
        capabilities=ModelCapability.STRUCTURED_OUTPUT,
        include_deprecated=True,
        sort_order=SortOrder.NONE
    )
    deprecated_count = len(all_models) - len(models)
    if deprecated_count > 0:
        print(f"- {deprecated_count} additional deprecated models were filtered out")