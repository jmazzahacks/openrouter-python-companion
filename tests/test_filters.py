"""Tests for ModelFilter capability filtering, sorting and error handling."""

import pytest

from openrouter_companion import ModelFilter, ModelCapability, SortOrder

from .factories import make_model, make_pricing, FakeClient


def _ids(models) -> list:
    return [model.id for model in models]


def test_filter_by_image_input_keeps_only_image_models() -> None:
    client = FakeClient([
        make_model(model_id="img", input_modalities=["text", "image"]),
        make_model(model_id="txt", input_modalities=["text"]),
    ])
    result = ModelFilter(client=client).filter_models(ModelCapability.IMAGE_INPUT)
    assert _ids(result) == ["img"]


def test_filter_by_structured_output() -> None:
    client = FakeClient([
        make_model(model_id="struct", supported_parameters=["response_format"]),
        make_model(model_id="plain", supported_parameters=[]),
    ])
    result = ModelFilter(client=client).filter_models(ModelCapability.STRUCTURED_OUTPUT)
    assert _ids(result) == ["struct"]


def test_combined_capabilities_require_all() -> None:
    client = FakeClient([
        make_model(
            model_id="both",
            input_modalities=["text", "image"],
            supported_parameters=["response_format"],
        ),
        make_model(model_id="image_only", input_modalities=["text", "image"]),
        make_model(model_id="struct_only", supported_parameters=["response_format"]),
    ])
    caps = ModelCapability.IMAGE_INPUT | ModelCapability.STRUCTURED_OUTPUT
    result = ModelFilter(client=client).filter_models(caps)
    assert _ids(result) == ["both"]


def test_no_capabilities_returns_all() -> None:
    client = FakeClient([make_model(model_id="a"), make_model(model_id="b")])
    result = ModelFilter(client=client).filter_models()
    assert set(_ids(result)) == {"a", "b"}


def test_deprecated_models_excluded_by_default() -> None:
    client = FakeClient([
        make_model(model_id="ok", description="A fine model"),
        make_model(model_id="old", description="This model is deprecated, do not use"),
    ])
    result = ModelFilter(client=client).filter_models()
    assert _ids(result) == ["ok"]


def test_deprecated_models_included_when_requested() -> None:
    client = FakeClient([
        make_model(model_id="ok", description="A fine model"),
        make_model(model_id="old", description="This model is deprecated"),
    ])
    result = ModelFilter(client=client).filter_models(include_deprecated=True)
    assert set(_ids(result)) == {"ok", "old"}


def test_problematic_variants_excluded_when_disabled() -> None:
    client = FakeClient([
        make_model(model_id="vendor/x", canonical_slug="vendor/x"),
        make_model(model_id="vendor/x:free", canonical_slug="vendor/x"),
    ])
    result = ModelFilter(client=client).filter_models(include_problematic_variants=False)
    assert _ids(result) == ["vendor/x"]


def test_problematic_variants_included_by_default() -> None:
    client = FakeClient([
        make_model(model_id="vendor/x", canonical_slug="vendor/x"),
        make_model(model_id="vendor/x:free", canonical_slug="vendor/x"),
    ])
    result = ModelFilter(client=client).filter_models()
    assert set(_ids(result)) == {"vendor/x", "vendor/x:free"}


def test_sort_price_ascending() -> None:
    client = FakeClient([
        make_model(model_id="pricey", pricing=make_pricing(prompt="0.00001")),
        make_model(model_id="cheap", pricing=make_pricing(prompt="0.000001")),
    ])
    result = ModelFilter(client=client).filter_models(sort_order=SortOrder.PRICE_ASC)
    assert _ids(result) == ["cheap", "pricey"]


def test_sort_name_ascending() -> None:
    client = FakeClient([
        make_model(model_id="z", name="Zebra"),
        make_model(model_id="a", name="Apple"),
    ])
    result = ModelFilter(client=client).filter_models(sort_order=SortOrder.NAME_ASC)
    assert _ids(result) == ["a", "z"]


def test_fetch_failure_is_wrapped_in_runtimeerror() -> None:
    class BoomModels:
        def list(self, details: bool = False):
            raise ConnectionError("network down")

    class BoomClient:
        def __init__(self) -> None:
            self.models = BoomModels()

    with pytest.raises(RuntimeError, match="Failed to fetch models"):
        ModelFilter(client=BoomClient()).filter_models()
