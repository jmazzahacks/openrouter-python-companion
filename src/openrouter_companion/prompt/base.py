"""Base prompt class for LLM interactions."""

from abc import ABC, abstractmethod
from typing import Any


class Prompt(ABC):
    """Base class for all LLM prompts.
    
    Provides a consistent interface for generating prompts with parameter
    validation and template management.
    """
    
    def __init__(self) -> None:
        """Initialize the prompt."""
        pass
    
    def render(self, **kwargs: Any) -> str:
        """Render the prompt with the given parameters.

        Template method that calls _render_content() and appends get_prompt_suffix().

        Args:
            **kwargs: Parameters to use in prompt generation

        Returns:
            The rendered prompt string with any suffix appended

        Raises:
            ValueError: If required parameters are missing or invalid
        """
        # Render main content (implemented by subclasses)
        main_content = self._render_content(**kwargs)

        # Get any additional suffix content
        suffix = self.get_prompt_suffix()

        if suffix:
            return f"{main_content}\n\n{suffix}"
        else:
            return main_content

    @abstractmethod
    def _render_content(self, **kwargs: Any) -> str:
        """Render the main content of the prompt.

        Abstract method that subclasses must implement to provide the core prompt content.

        Args:
            **kwargs: Parameters to use in prompt generation

        Returns:
            The main prompt content string

        Raises:
            ValueError: If required parameters are missing or invalid
        """
        pass

    def get_prompt_suffix(self) -> str:
        """Get additional content to append to the end of the prompt.

        Hook method that subclasses can override to add format instructions,
        response guidelines, or other content that should appear at the end.

        Returns:
            Additional content to append, or empty string if none
        """
        return ""
    
    def validate_params(self, **kwargs: Any) -> None:
        """Validate prompt parameters.
        
        Args:
            **kwargs: Parameters to validate
            
        Raises:
            ValueError: If parameters are invalid
        """
        # Default implementation does no validation
        pass
    
    def get_required_params(self) -> list[str]:
        """Get list of required parameter names.
        
        Returns:
            List of required parameter names
        """
        return []
    
    def get_optional_params(self) -> list[str]:
        """Get list of optional parameter names.
        
        Returns:
            List of optional parameter names
        """
        return []
    
    def get_schema(self) -> dict[str, Any] | None:
        """Get the JSON schema for structured output from this prompt.
        
        Returns:
            JSON schema dictionary or None if no structured output expected
        """
        return None