"""Tests for ModelInfo pricing, capability and sort helpers."""

import math

from openrouter_companion import ModelInfo

from .factories import make_model, make_pricing


# --- pricing -----------------------------------------------------------------

def test_pricing_per_1m_tokens_scales_prompt_price() -> None:
    model = ModelInfo(make_model(pricing=make_pricing(prompt="0.000001")))
    assert model.get_pricing_per_1m_tokens() == 1.0


def test_pricing_per_1m_tokens_free_model_is_zero() -> None:
    model = ModelInfo(make_model(pricing=make_pricing(prompt="0")))
    assert model.get_pricing_per_1m_tokens() == 0.0


def test_pricing_per_1m_tokens_unparseable_is_infinite() -> None:
    model = ModelInfo(make_model(pricing=make_pricing(prompt="not-a-number")))
    assert math.isinf(model.get_pricing_per_1m_tokens())


def test_pricing_per_1m_tokens_none_price_is_infinite() -> None:
    model = ModelInfo(make_model(pricing=make_pricing(prompt=None)))
    assert math.isinf(model.get_pricing_per_1m_tokens())


def test_pricing_per_1m_tokens_no_pricing_object_is_infinite() -> None:
    model = ModelInfo(make_model(pricing=False))
    assert math.isinf(model.get_pricing_per_1m_tokens())


def test_is_free_true_for_zero_price() -> None:
    assert ModelInfo(make_model(pricing=make_pricing(prompt="0"))).is_free() is True


def test_is_free_false_for_paid_model() -> None:
    assert ModelInfo(make_model(pricing=make_pricing(prompt="0.001"))).is_free() is False


def test_has_pricing_false_when_unavailable() -> None:
    assert ModelInfo(make_model(pricing=make_pricing(prompt=None))).has_pricing() is False


def test_has_pricing_true_for_free_model() -> None:
    assert ModelInfo(make_model(pricing=make_pricing(prompt="0"))).has_pricing() is True


# --- image pricing -----------------------------------------------------------

def test_image_pricing_returns_value() -> None:
    model = ModelInfo(make_model(pricing=make_pricing(image="0.01")))
    assert model.get_image_pricing() == 0.01


def test_image_pricing_zero_returns_none() -> None:
    model = ModelInfo(make_model(pricing=make_pricing(image="0")))
    assert model.get_image_pricing() is None


def test_image_pricing_missing_returns_none() -> None:
    model = ModelInfo(make_model(pricing=make_pricing(image=None)))
    assert model.get_image_pricing() is None


# --- capabilities ------------------------------------------------------------

def test_supports_images_true_when_image_modality_present() -> None:
    model = ModelInfo(make_model(input_modalities=["text", "image"]))
    assert model.supports_images() is True


def test_supports_images_false_for_text_only() -> None:
    assert ModelInfo(make_model(input_modalities=["text"])).supports_images() is False


def test_supports_images_false_for_empty_modalities() -> None:
    assert ModelInfo(make_model(input_modalities=[])).supports_images() is False


def test_supports_structured_output_via_response_format() -> None:
    model = ModelInfo(make_model(supported_parameters=["response_format"]))
    assert model.supports_structured_output() is True


def test_supports_structured_output_via_structured_outputs() -> None:
    model = ModelInfo(make_model(supported_parameters=["structured_outputs"]))
    assert model.supports_structured_output() is True


def test_supports_structured_output_false_when_absent() -> None:
    model = ModelInfo(make_model(supported_parameters=["temperature"]))
    assert model.supports_structured_output() is False


def test_supports_reasoning_true_when_present() -> None:
    assert ModelInfo(make_model(supported_parameters=["reasoning"])).supports_reasoning() is True


def test_supports_reasoning_false_when_absent() -> None:
    assert ModelInfo(make_model(supported_parameters=[])).supports_reasoning() is False


# --- sort helpers ------------------------------------------------------------

def test_get_sort_name_uses_name() -> None:
    assert ModelInfo(make_model(name="Alpha")).get_sort_name() == "Alpha"


def test_get_sort_name_falls_back_to_id() -> None:
    model = ModelInfo(make_model(model_id="vendor/x", name=None))
    assert model.get_sort_name() == "vendor/x"


def test_get_context_length_sort_returns_value() -> None:
    assert ModelInfo(make_model(context_length=4096)).get_context_length_sort() == 4096


def test_get_context_length_sort_defaults_to_zero() -> None:
    assert ModelInfo(make_model(context_length=None)).get_context_length_sort() == 0


# --- canonical slug ----------------------------------------------------------

def test_canonical_slug_mismatch_true_when_different() -> None:
    model = ModelInfo(make_model(model_id="vendor/x:free", canonical_slug="vendor/x"))
    assert model.has_canonical_slug_mismatch() is True


def test_canonical_slug_mismatch_false_when_equal() -> None:
    model = ModelInfo(make_model(model_id="vendor/x", canonical_slug="vendor/x"))
    assert model.has_canonical_slug_mismatch() is False


def test_canonical_slug_mismatch_false_when_absent() -> None:
    assert ModelInfo(make_model(canonical_slug=None)).has_canonical_slug_mismatch() is False


# --- attribute delegation ----------------------------------------------------

def test_getattr_delegates_to_wrapped_model() -> None:
    model = ModelInfo(make_model(model_id="vendor/x", context_length=123))
    assert model.id == "vendor/x"
    assert model.context_length == 123
