"""String template prompt with variable substitution."""

from string import Template
from typing import Any
from .base import Prompt


class StringTemplatePrompt(Prompt):
    """Prompt that uses Python string Template for variable substitution."""

    def __init__(self, template_string: str) -> None:
        """Initialize with a template string.

        Args:
            template_string: Template string with $variable placeholders
        """
        super().__init__()
        self.template_string = template_string
        self.template = Template(template_string)

    def _render_content(self, **kwargs: Any) -> str:
        """Render the template with variable substitution.

        Args:
            **kwargs: Variables to substitute in the template

        Returns:
            The rendered template string

        Raises:
            KeyError: If required template variables are missing
        """
        try:
            return self.template.substitute(**kwargs)
        except KeyError as e:
            missing_var = str(e).strip("'")
            raise ValueError(f"Missing required template variable: {missing_var}") from e

    def safe_render(self, **kwargs: Any) -> str:
        """Safely render the template, leaving missing variables as placeholders.

        Args:
            **kwargs: Variables to substitute in the template

        Returns:
            The rendered template string with missing variables left as $variable
        """
        main_content = self.template.safe_substitute(**kwargs)
        suffix = self.get_prompt_suffix()

        if suffix:
            return f"{main_content}\n\n{suffix}"
        else:
            return main_content

    def get_template_variables(self) -> list[str]:
        """Get list of variables used in the template.

        Returns:
            List of variable names found in the template
        """
        import re
        # Find all $variable patterns
        pattern = r'\$([a-zA-Z_][a-zA-Z0-9_]*)'
        matches = re.findall(pattern, self.template_string)
        return list(set(matches))  # Remove duplicates