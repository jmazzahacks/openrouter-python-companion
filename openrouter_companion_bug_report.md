# Bug Report: Flagship Models Incorrectly Flagged as "Problematic Variants"

## Summary
The `ModelFilter.filter_models()` method incorrectly excludes many high-quality, flagship models from major providers when `include_problematic_variants=False` (the default). These are not "problematic" models - they are the latest, most capable releases from top-tier providers.

## Environment
- **Library**: `openrouter-python-companion`
- **Python Version**: 3.13.5
- **Discovery Context**: Using `ModelFilter(api_key=api_key).filter_models()` with default parameters

## Expected Behavior
When calling `filter_models()` with default parameters, flagship and latest models from major providers (Anthropic, OpenAI, DeepSeek, etc.) should be included in the results. The `include_problematic_variants` flag should only exclude genuinely problematic models (e.g., broken implementations, outdated variants with known issues, deprecated experimental versions).

## Actual Behavior
Calling `filter_models()` with defaults returns **224 models** and excludes **120 models** marked as "problematic variants", including many flagship models that are the latest and most capable offerings from major AI providers.

### Statistics
- **Default (no flags)**: 224 models
- **With `include_problematic_variants=True`**: 344 models
- **Models incorrectly excluded**: 120

## Examples of Incorrectly Excluded Models

### Anthropic Claude Models (9 excluded)
These are Anthropic's **latest flagship models** - not problematic:
- `anthropic/claude-sonnet-4.5` ⭐ (Latest Sonnet - most capable general model)
- `anthropic/claude-opus-4.1` ⭐ (Latest Opus - most capable for complex tasks)
- `anthropic/claude-haiku-4.5` ⭐ (Latest Haiku - fastest model)
- `anthropic/claude-3.7-sonnet`
- `anthropic/claude-opus-4`
- `anthropic/claude-sonnet-4`
- `anthropic/claude-3.5-haiku`
- `anthropic/claude-3.5-haiku-20241022`
- `anthropic/claude-3.7-sonnet:thinking`

### OpenAI Models (13 excluded)
- **GPT-5 family** (12 models) - OpenAI's **latest flagship series**:
  - `openai/gpt-5` ⭐
  - `openai/gpt-5.1` ⭐
  - `openai/gpt-5-pro` ⭐
  - `openai/gpt-5-chat`
  - `openai/gpt-5.1-chat`
  - `openai/gpt-5-codex`
  - `openai/gpt-5.1-codex`
  - `openai/gpt-5.1-codex-mini`
  - `openai/gpt-5-image`
  - `openai/gpt-5-image-mini`
  - `openai/gpt-5-mini`
  - `openai/gpt-5-nano`
- `openai/o1` ⭐ (o1-mini equivalent, reasoning model)

**Note**: `openai/o1-pro` IS included (not flagged as problematic), but the base `openai/o1` is excluded - this is inconsistent.

### DeepSeek Models (10 excluded)
These are DeepSeek's **latest and most capable models**:
- `deepseek/deepseek-chat` ⭐ (Latest chat model)
- `deepseek/deepseek-chat-v3.1:free`
- `deepseek/deepseek-chat-v3-0324:free`
- `deepseek/deepseek-r1:free` ⭐ (R1 reasoning model)
- `deepseek/deepseek-r1-0528:free`
- `deepseek/deepseek-r1-0528-qwen3-8b:free`
- `deepseek/deepseek-r1-distill-llama-70b:free`
- `deepseek/deepseek-v3.1-terminus:exacto`
- `tngtech/deepseek-r1t-chimera:free`
- `tngtech/deepseek-r1t2-chimera:free`

### Other High-Quality Models Excluded
- `cohere/command-a` (Cohere's latest)
- Many `:free` tier variants of otherwise-included models

## Impact

This bug has **severe impact** on applications that rely on `ModelFilter` for model selection:

1. **Random Model Selection**: Applications using `filter_models()` for random selection (e.g., `random.choice(filter_obj.filter_models())`) will never select flagship models from Anthropic, OpenAI GPT-5, or DeepSeek.

2. **Model Discovery**: Developers exploring available models won't discover the latest, most capable options.

3. **Capability Filtering**: Even when filtering by capabilities, flagship models are excluded before capability checks run.

4. **User Confusion**: Users expect "problematic variants" to mean broken/deprecated models, not the latest flagship releases.

## Root Cause Analysis

The `_is_problematic_variant()` method (or similar internal logic) appears to be using overly aggressive criteria for flagging models as "problematic".

Possible causes:
- Flagging all `:free` tier models as problematic (incorrect - free tiers are valid)
- Flagging newer model versions that haven't been manually allowlisted
- Flagging models with certain naming patterns (e.g., version numbers like `4.5`, `5.1`)
- Flagging models from certain providers or with specific suffixes

## Proposed Solution

### Option 1: Fix the `_is_problematic_variant()` Logic (Preferred)
Revise the criteria for what constitutes a "problematic variant". Problematic should mean:
- Deprecated/EOL models with known breaking changes
- Experimental/alpha models explicitly marked as unstable by the provider
- Models with documented bugs or issues on OpenRouter
- Duplicate model IDs or incorrect routing configurations

Problematic should **NOT** mean:
- Latest flagship models from major providers (Claude 4.5, GPT-5, DeepSeek R1)
- Free tier variants (`:free` suffix)
- New model versions (4.x, 5.x series)
- Models with enhanced capabilities (`:thinking` suffix)

### Option 2: Provide Model-Specific Metadata
Add a `is_flagship` or `tier` field to `ModelInfo` so consumers can distinguish between:
- Flagship/production models (should always be included)
- Experimental/beta models (may want to exclude)
- Deprecated models (should exclude)

### Option 3: More Granular Filtering Flags
Split `include_problematic_variants` into:
- `include_deprecated` (already exists, works correctly)
- `include_beta_models` (experimental/unreleased)
- `include_free_tier` (`:free` variants)
- `include_problematic` (genuinely broken models)

## Reproduction Steps

```python
from openrouter_companion import ModelFilter
import os

api_key = os.getenv('OPENROUTER_API_KEY')
filter_obj = ModelFilter(api_key=api_key)

# Get models with default settings
default_models = filter_obj.filter_models()
print(f'Default: {len(default_models)} models')

# Get all models including "problematic"
all_models = filter_obj.filter_models(include_problematic_variants=True)
print(f'With problematic: {len(all_models)} models')

# Check for Claude Sonnet 4.5 (flagship model)
sonnet_45 = [m for m in default_models if 'claude-sonnet-4.5' in m.id]
print(f'Claude Sonnet 4.5 in default list: {len(sonnet_45) > 0}')  # False - BUG!

sonnet_45_all = [m for m in all_models if 'claude-sonnet-4.5' in m.id]
print(f'Claude Sonnet 4.5 exists in catalog: {len(sonnet_45_all) > 0}')  # True

# Check for GPT-5 (flagship model)
gpt5 = [m for m in default_models if m.id == 'openai/gpt-5']
print(f'GPT-5 in default list: {len(gpt5) > 0}')  # False - BUG!

gpt5_all = [m for m in all_models if m.id == 'openai/gpt-5']
print(f'GPT-5 exists in catalog: {len(gpt5_all) > 0}')  # True
```

**Expected Output**:
```
Default: 344 models (or close to it - only truly problematic models excluded)
Claude Sonnet 4.5 in default list: True
GPT-5 in default list: True
```

**Actual Output**:
```
Default: 224 models
With problematic: 344 models
Claude Sonnet 4.5 in default list: False  ❌ BUG
Claude Sonnet 4.5 exists in catalog: True
GPT-5 in default list: False  ❌ BUG
GPT-5 exists in catalog: True
```

## Workaround

Until fixed, consumers must explicitly pass `include_problematic_variants=True` to access flagship models:

```python
# Workaround to get flagship models
all_models = filter_obj.filter_models(include_problematic_variants=True)
```

This is counterintuitive since these are not "problematic" models.

## Additional Context

The term "problematic variants" suggests models with known issues, not flagship models. This naming and behavior creates a poor developer experience where the latest, most capable models from trusted providers are hidden by default.

## Priority

**High** - This bug affects model discovery and selection for all users of the library. Applications using random model selection or capability-based filtering are missing access to the best available models.

---

**Reporter**: User via crypto-arcana trading strategy generation system
**Date**: 2025-11-13
**Library Version**: Latest (as of report date)
