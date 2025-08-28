# OpenRouter Python Companion

Utilities for filtering and analyzing OpenRouter models by capabilities, pricing, and other criteria. This companion library works with the [OpenRouter Python client](https://github.com/dingo-actual/openrouter-python-client) to provide easy-to-use filtering and analysis tools.

## Installation

```bash
pip install -e .
```

Or install just the dependencies:

```bash
pip install -r requirements.txt
```

### Requirements

- Python 3.9+
- OpenRouter API key (set as `OPENROUTER_API_KEY` environment variable)
- The OpenRouter Python client (automatically installed from GitHub)

## Quick Start

```python
from openrouter_client import OpenRouterClient
from openrouter_companion import ModelFilter, ModelCapability, SortOrder

# Initialize OpenRouter client with your API key
client = OpenRouterClient(api_key="your-openrouter-api-key-here")

# Initialize filter with the client
filter_obj = ModelFilter(client=client)

# Alternative: Pass API key directly to ModelFilter
# filter_obj = ModelFilter(api_key="your-openrouter-api-key-here")

# Alternative: Use environment variable (OPENROUTER_API_KEY must be set)
# filter_obj = ModelFilter()

# Find models that support structured output
models = filter_obj.filter_models(
    capabilities=ModelCapability.STRUCTURED_OUTPUT,
    sort_order=SortOrder.PRICE_ASC
)

# Find models with multiple capabilities
multimodal_models = filter_obj.filter_models(
    capabilities=ModelCapability.IMAGE_INPUT | ModelCapability.STRUCTURED_OUTPUT,
    sort_order=SortOrder.PRICE_ASC
)

# Access model information
for model in models[:5]:  # Top 5 cheapest
    print(f"{model.id}: ${model.get_pricing_per_1m_tokens():.2f}/1M tokens")
```

## Core Components

### ModelFilter

The main filtering interface that queries OpenRouter's API and applies filters:

```python
from openrouter_companion import ModelFilter

# Basic usage
filter_obj = ModelFilter()

# With custom API key or client
filter_obj = ModelFilter(api_key="your-key")
filter_obj = ModelFilter(client=your_openrouter_client)
```

### ModelCapability (Flags)

Capability flags that can be combined using the `|` operator:

- `ModelCapability.IMAGE_INPUT` - Models that support image/multimodal input
- `ModelCapability.STRUCTURED_OUTPUT` - Models that support structured output (response_format)
- `ModelCapability.MULTIMODAL` - Alias for IMAGE_INPUT
- `ModelCapability.ALL` - All capabilities combined

### SortOrder (Enum)

Sort options for filtering results:

- `SortOrder.PRICE_ASC` - Cheapest first
- `SortOrder.PRICE_DESC` - Most expensive first
- `SortOrder.NAME_ASC/NAME_DESC` - Alphabetical sorting
- `SortOrder.CONTEXT_ASC/CONTEXT_DESC` - By context length
- `SortOrder.NONE` - No sorting

### ModelInfo

Enhanced model wrapper with utility methods:

```python
# Pricing information
model.get_pricing_per_1m_tokens()  # Price per million tokens
model.is_free()                    # True if free model
model.has_pricing()                # True if pricing info available
model.get_image_pricing()          # Price per image (if applicable)

# Capability checks
model.supports_images()            # True if supports image input
model.supports_structured_output() # True if supports structured output
```

## Usage Examples

### Filter by Single Capability

```python
# Find image-capable models
image_models = filter_obj.filter_models(
    capabilities=ModelCapability.IMAGE_INPUT,
    include_deprecated=False,
    sort_order=SortOrder.PRICE_ASC
)
```

### Filter by Multiple Capabilities

```python
# Find models with both image input AND structured output
advanced_models = filter_obj.filter_models(
    capabilities=ModelCapability.IMAGE_INPUT | ModelCapability.STRUCTURED_OUTPUT,
    sort_order=SortOrder.PRICE_ASC
)
```

### Custom Filtering

```python
# Include deprecated models and sort by context length
all_models = filter_obj.filter_models(
    capabilities=ModelCapability.ALL,
    include_deprecated=True,
    sort_order=SortOrder.CONTEXT_DESC
)
```

### Pricing Analysis

```python
models = filter_obj.filter_models(
    capabilities=ModelCapability.STRUCTURED_OUTPUT,
    sort_order=SortOrder.PRICE_ASC
)

# Find free models
free_models = [m for m in models if m.is_free()]
print(f"Found {len(free_models)} free models")

# Find cheapest paid model
paid_models = [m for m in models if m.has_pricing() and not m.is_free()]
if paid_models:
    cheapest = min(paid_models, key=lambda m: m.get_pricing_per_1m_tokens())
    print(f"Cheapest paid: {cheapest.id} at ${cheapest.get_pricing_per_1m_tokens():.2f}/1M tokens")
```

## API Reference

### ModelFilter.filter_models()

```python
def filter_models(
    capabilities: ModelCapability = ModelCapability.NONE,
    include_deprecated: bool = False,
    sort_order: SortOrder = SortOrder.NONE
) -> List[ModelInfo]:
```

**Parameters:**
- `capabilities`: Capability flags to filter by (can be combined with `|`)
- `include_deprecated`: Whether to include deprecated models
- `sort_order`: How to sort the results

**Returns:** List of ModelInfo objects matching the criteria

### ModelInfo Methods

- `get_pricing_per_1m_tokens() -> float`: Price per million tokens (0 for free, inf for no pricing)
- `is_free() -> bool`: True if the model is free to use
- `has_pricing() -> bool`: True if pricing information is available
- `get_image_pricing() -> Optional[float]`: Price per image for multimodal models
- `supports_images() -> bool`: True if model supports image input
- `supports_structured_output() -> bool`: True if model supports structured output

## Configuration

The library automatically handles OpenRouter API authentication through:

1. Environment variable: `OPENROUTER_API_KEY`
2. Custom API key passed to ModelFilter constructor
3. Pre-configured OpenRouterClient instance

## Error Handling

The library includes robust error handling for:
- Missing API keys
- Network failures
- Invalid model data
- API rate limits

Errors are wrapped in clear `RuntimeError` exceptions with descriptive messages.

## Contributing

This project is developed by [@jmazzahacks](https://github.com/jmazzahacks). Contributions are welcome!

## License

MIT License - see the project repository for details.