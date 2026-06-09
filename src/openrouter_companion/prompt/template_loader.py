"""Template loader prompt for loading file-based templates."""

from typing import Any
from .base import Prompt


class FileTemplatePrompt(Prompt):
    """Prompt for loading templates from files."""

    def __init__(self, template_path: str) -> None:
        """Initialize the template loader.

        Args:
            template_path: Path to the template file to load
        """
        super().__init__()
        self.template_path = template_path
    
    def _render_content(self, **kwargs: Any) -> str:
        """Load and return the template content from file.

        Args:
            **kwargs: Template parameters (not used for file loading)

        Returns:
            The template content as a string

        Raises:
            FileNotFoundError: If the template file cannot be found
            IOError: If the template file cannot be read
        """
        try:
            with open(self.template_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"Template file not found: {self.template_path}")
        except IOError as e:
            raise IOError(f"Could not read template file {self.template_path}: {e}") from e