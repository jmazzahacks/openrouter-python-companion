"""Tests for the prompt templating utilities."""

import pytest

from openrouter_companion import Prompt, StringTemplatePrompt, FileTemplatePrompt


class _SuffixPrompt(Prompt):
    """Minimal concrete Prompt that emits fixed content plus a suffix."""

    def _render_content(self, **kwargs: object) -> str:
        return "BODY"

    def get_prompt_suffix(self) -> str:
        return "SUFFIX"


class _NoSuffixPrompt(Prompt):
    def _render_content(self, **kwargs: object) -> str:
        return "BODY"


# --- base Prompt render template method --------------------------------------

def test_render_appends_suffix() -> None:
    assert _SuffixPrompt().render() == "BODY\n\nSUFFIX"


def test_render_without_suffix_returns_content() -> None:
    assert _NoSuffixPrompt().render() == "BODY"


# --- StringTemplatePrompt ----------------------------------------------------

def test_string_template_substitutes_variables() -> None:
    prompt = StringTemplatePrompt("Hello $name, welcome to $place")
    assert prompt.render(name="Ada", place="Earth") == "Hello Ada, welcome to Earth"


def test_string_template_missing_variable_raises_valueerror() -> None:
    prompt = StringTemplatePrompt("Hello $name")
    with pytest.raises(ValueError, match="Missing required template variable: name"):
        prompt.render()


def test_string_template_safe_render_keeps_missing_placeholder() -> None:
    prompt = StringTemplatePrompt("Hello $name from $place")
    assert prompt.safe_render(name="Ada") == "Hello Ada from $place"


def test_get_template_variables_returns_unique_names() -> None:
    prompt = StringTemplatePrompt("$a and $b and $a")
    assert sorted(prompt.get_template_variables()) == ["a", "b"]


# --- FileTemplatePrompt ------------------------------------------------------

def test_file_template_reads_file(tmp_path) -> None:
    template_file = tmp_path / "template.txt"
    template_file.write_text("file contents here", encoding="utf-8")
    prompt = FileTemplatePrompt(str(template_file))
    assert prompt.render() == "file contents here"


def test_file_template_missing_file_raises() -> None:
    prompt = FileTemplatePrompt("/nonexistent/path/to/template.txt")
    with pytest.raises(FileNotFoundError):
        prompt.render()
