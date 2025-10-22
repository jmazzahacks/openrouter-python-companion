# OpenRouter Python Companion

A comprehensive Python library for working with OpenRouter models, providing utilities for filtering, analyzing, and prompt management. This companion library works with the [OpenRouter Python client](https://github.com/dingo-actual/openrouter-python-client) to offer:

- **Model Filtering & Analysis**: Find models by capabilities, pricing, and features
- **Prompt Management**: Template-based prompt system with variable substitution
- **Quality Filtering**: Automatically exclude problematic model variants

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

### Model Filtering

```python
from openrouter_client import OpenRouterClient
from openrouter_companion import ModelFilter, ModelCapability, SortOrder

# Initialize OpenRouter client with your API key
client = OpenRouterClient(api_key="your-openrouter-api-key-here")

# Initialize filter with the client
filter_obj = ModelFilter(client=client)

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

### Prompt Management

```python
from openrouter_companion import Prompt, StringTemplatePrompt, FileTemplatePrompt

# Simple string template with variable substitution
template = StringTemplatePrompt("Hello $name! Help me with $task.")
prompt_text = template.render(name="Alice", task="Python debugging")

# Load prompts from files
file_prompt = FileTemplatePrompt("path/to/template.txt")
content = file_prompt.render()

# Custom prompt class
class CustomPrompt(Prompt):
    def _render_content(self, **kwargs):
        return f"Custom logic for {kwargs.get('topic', 'general')} assistance"

custom = CustomPrompt()
result = custom.render(topic="API integration")
```

## Core Components

### Model Filtering

#### ModelFilter

The main filtering interface that queries OpenRouter's API and applies filters:

```python
from openrouter_companion import ModelFilter

# Basic usage
filter_obj = ModelFilter()

# With custom API key or client
filter_obj = ModelFilter(api_key="your-key")
filter_obj = ModelFilter(client=your_openrouter_client)
```

#### ModelCapability (Flags)

Capability flags that can be combined using the `|` operator:

- `ModelCapability.IMAGE_INPUT` - Models that support image/multimodal input
- `ModelCapability.STRUCTURED_OUTPUT` - Models that support structured output (response_format)
- `ModelCapability.REASONING` - Models that support reasoning/thinking mode
- `ModelCapability.MULTIMODAL` - Alias for IMAGE_INPUT
- `ModelCapability.ALL` - All capabilities combined

#### SortOrder (Enum)

Sort options for filtering results:

- `SortOrder.PRICE_ASC` - Cheapest first
- `SortOrder.PRICE_DESC` - Most expensive first
- `SortOrder.NAME_ASC/NAME_DESC` - Alphabetical sorting
- `SortOrder.CONTEXT_ASC/CONTEXT_DESC` - By context length
- `SortOrder.NONE` - No sorting

#### ModelInfo

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
model.supports_reasoning()         # True if supports reasoning/thinking mode
```

### Prompt Management

#### Prompt (Base Class)

Abstract base class for all prompts using the template method pattern:

```python
from openrouter_companion import Prompt

class CustomPrompt(Prompt):
    def _render_content(self, **kwargs):
        # Implement your prompt logic here
        return "Your prompt content"

    def get_required_params(self):
        return ["param1", "param2"]

    def validate_params(self, **kwargs):
        # Custom validation logic
        pass
```

#### StringTemplatePrompt

Template-based prompts with `$variable` substitution:

```python
from openrouter_companion import StringTemplatePrompt

# Create template with variables
template = StringTemplatePrompt("Help $name with $task using $style approach.")

# Render with variables
result = template.render(name="Alice", task="debugging", style="systematic")

# Safe render (leaves missing variables as $var)
partial = template.safe_render(name="Bob")

# Get template variables
variables = template.get_template_variables()  # ['name', 'task', 'style']
```

#### FileTemplatePrompt

Load prompts from external files:

```python
from openrouter_companion import FileTemplatePrompt

# Load from file
file_prompt = FileTemplatePrompt("templates/system_prompt.txt")
content = file_prompt.render()

# Dynamic template path
file_prompt.set_template_path("other_template.txt")
```

## Usage Examples

### Model Filtering Examples

#### Filter by Single Capability

```python
# Find image-capable models
image_models = filter_obj.filter_models(
    capabilities=ModelCapability.IMAGE_INPUT,
    include_deprecated=False,
    sort_order=SortOrder.PRICE_ASC
)
```

#### Filter by Multiple Capabilities

```python
# Find models with both image input AND structured output
advanced_models = filter_obj.filter_models(
    capabilities=ModelCapability.IMAGE_INPUT | ModelCapability.STRUCTURED_OUTPUT,
    sort_order=SortOrder.PRICE_ASC
)

# Find reasoning models (thinking/chain-of-thought capable)
reasoning_models = filter_obj.filter_models(
    capabilities=ModelCapability.REASONING,
    sort_order=SortOrder.PRICE_ASC
)

# Find models with reasoning AND structured output
smart_models = filter_obj.filter_models(
    capabilities=ModelCapability.REASONING | ModelCapability.STRUCTURED_OUTPUT,
    sort_order=SortOrder.PRICE_ASC
)
```

#### Custom Filtering

```python
# Include deprecated models and sort by context length
all_models = filter_obj.filter_models(
    capabilities=ModelCapability.ALL,
    include_deprecated=True,
    sort_order=SortOrder.CONTEXT_DESC
)
```

#### Pricing Analysis

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

### Prompt Management Examples

#### Custom Prompt Classes

```python
from openrouter_companion import Prompt

class ErrorCorrectionPrompt(Prompt):
    """Prompt for providing error feedback during iterative generation."""

    def _render_content(self, **kwargs):
        self.validate_params(**kwargs)
        last_error = kwargs.get('last_error')

        return f"""The previous strategy had issues. Please fix them.

ERRORS FOUND:
{last_error}

Please provide a corrected version."""

    def validate_params(self, **kwargs):
        last_error = kwargs.get('last_error')
        if not last_error or not isinstance(last_error, str):
            raise ValueError("last_error is required and must be a string")

    def get_required_params(self):
        return ['last_error']

# Usage
error_prompt = ErrorCorrectionPrompt()
result = error_prompt.render(last_error="Variable x is undefined on line 42")
```

#### Template File Integration

```python
# Create a template file: templates/code_review.txt
"""
You are a senior software engineer reviewing code.

Task: {task}
Language: {language}
Experience Level: {experience}

Please provide {style} feedback focusing on:
1. Code quality and best practices
2. Potential bugs or issues
3. Performance optimizations
4. Security considerations

Code to review:
{code}
"""

# Use with FileTemplatePrompt (no variable substitution)
file_prompt = FileTemplatePrompt("templates/code_review.txt")
template_content = file_prompt.render()

# Use with StringTemplatePrompt for variable substitution
with open("templates/code_review.txt") as f:
    content = f.read().replace("{", "$").replace("}", "")  # Convert to $var format

string_prompt = StringTemplatePrompt(content)
review_prompt = string_prompt.render(
    task="API security review",
    language="Python",
    experience="senior",
    style="detailed",
    code="def authenticate(token): return True"
)
```

## API Reference

### Model Filtering API

#### ModelFilter.filter_models()

```python
def filter_models(
    capabilities: ModelCapability = ModelCapability.NONE,
    include_deprecated: bool = False,
    include_problematic_variants: bool = False,
    sort_order: SortOrder = SortOrder.NONE
) -> List[ModelInfo]:
```

**Parameters:**
- `capabilities`: Capability flags to filter by (can be combined with `|`)
- `include_deprecated`: Whether to include deprecated models
- `include_problematic_variants`: Whether to include models with canonical slug mismatches
- `sort_order`: How to sort the results

**Returns:** List of ModelInfo objects matching the criteria

#### ModelInfo Methods

- `get_pricing_per_1m_tokens() -> float`: Price per million tokens (0 for free, inf for no pricing)
- `is_free() -> bool`: True if the model is free to use
- `has_pricing() -> bool`: True if pricing information is available
- `get_image_pricing() -> Optional[float]`: Price per image for multimodal models
- `supports_images() -> bool`: True if model supports image input
- `supports_structured_output() -> bool`: True if model supports structured output
- `supports_reasoning() -> bool`: True if model supports reasoning/thinking mode
- `has_canonical_slug_mismatch() -> bool`: True if ID != canonical_slug (indicates problematic variant)

### Prompt Management API

#### Prompt (Base Class)

```python
class Prompt(ABC):
    def render(**kwargs) -> str:          # Main rendering method
    def _render_content(**kwargs) -> str: # Abstract method to implement
    def get_prompt_suffix() -> str:       # Optional suffix content
    def validate_params(**kwargs) -> None: # Parameter validation
    def get_required_params() -> list[str]: # Required parameter names
    def get_optional_params() -> list[str]: # Optional parameter names
    def get_schema() -> dict | None:       # JSON schema for structured output
```

#### StringTemplatePrompt

```python
class StringTemplatePrompt(Prompt):
    def __init__(template_string: str)
    def safe_render(**kwargs) -> str:              # Safe rendering with partial substitution
    def get_template_variables() -> list[str]:     # Get template variables
```

#### FileTemplatePrompt

```python
class FileTemplatePrompt(Prompt):
    def __init__(template_path: str)
    def get_template_path() -> str:        # Get current template path
    def set_template_path(path: str) -> None: # Set new template path
```

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