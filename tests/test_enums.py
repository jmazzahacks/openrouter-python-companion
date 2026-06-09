"""Tests for capability flags and sort-order enums."""

from openrouter_companion import ModelCapability, SortOrder


def test_capabilities_combine_with_or() -> None:
    combined = ModelCapability.IMAGE_INPUT | ModelCapability.STRUCTURED_OUTPUT
    assert combined & ModelCapability.IMAGE_INPUT
    assert combined & ModelCapability.STRUCTURED_OUTPUT
    assert not (combined & ModelCapability.REASONING)


def test_none_capability_matches_nothing() -> None:
    assert not (ModelCapability.NONE & ModelCapability.IMAGE_INPUT)


def test_all_contains_every_capability() -> None:
    for capability in (
        ModelCapability.IMAGE_INPUT,
        ModelCapability.STRUCTURED_OUTPUT,
        ModelCapability.REASONING,
    ):
        assert ModelCapability.ALL & capability


def test_multimodal_alias_equals_image_input() -> None:
    assert ModelCapability.MULTIMODAL == ModelCapability.IMAGE_INPUT


def test_sort_orders_are_distinct() -> None:
    orders = [
        SortOrder.PRICE_ASC,
        SortOrder.PRICE_DESC,
        SortOrder.NAME_ASC,
        SortOrder.NAME_DESC,
        SortOrder.CONTEXT_ASC,
        SortOrder.CONTEXT_DESC,
    ]
    assert len(set(orders)) == len(orders)
