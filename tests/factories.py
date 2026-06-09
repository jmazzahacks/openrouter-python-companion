"""Lightweight fakes that mimic the openrouter_client model objects.

ModelInfo only reads attributes off the wrapped object, so SimpleNamespace
stand-ins are enough to exercise the logic without the real client or network.
"""

from types import SimpleNamespace
from typing import Any, List, Optional


def make_pricing(prompt: Any = "0.000001", image: Any = None) -> SimpleNamespace:
    """Build a fake pricing object. Attributes are strings, like the real API."""
    return SimpleNamespace(prompt=prompt, image=image)


def make_model(
    model_id: str = "vendor/model",
    name: Optional[str] = "Test Model",
    description: Optional[str] = "",
    pricing: Any = None,
    input_modalities: Optional[List[str]] = None,
    supported_parameters: Optional[List[str]] = None,
    context_length: Optional[int] = 8000,
    canonical_slug: Optional[str] = None,
) -> SimpleNamespace:
    """Build a fake ModelData-like object with sensible defaults.

    ModelInfo reaches these via __getattr__, so every attribute it touches
    (pricing, architecture, supported_parameters, ...) must be present.
    """
    if pricing is None:
        pricing = make_pricing()
    if input_modalities is None:
        input_modalities = ["text"]
    if supported_parameters is None:
        supported_parameters = []
    architecture = SimpleNamespace(input_modalities=input_modalities)
    return SimpleNamespace(
        id=model_id,
        name=name,
        description=description,
        pricing=pricing,
        architecture=architecture,
        supported_parameters=supported_parameters,
        context_length=context_length,
        canonical_slug=canonical_slug,
    )


class FakeModelsEndpoint:
    """Stand-in for client.models with a list(details=...) method."""

    def __init__(self, models: List[SimpleNamespace]) -> None:
        self._models = models

    def list(self, details: bool = False) -> SimpleNamespace:
        return SimpleNamespace(data=self._models)


class FakeClient:
    """Stand-in for OpenRouterClient exposing only .models.list()."""

    def __init__(self, models: List[SimpleNamespace]) -> None:
        self.models = FakeModelsEndpoint(models)
