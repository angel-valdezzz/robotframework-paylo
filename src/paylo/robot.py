"""Robot Framework adapter; all rendering lives in the independent Python core."""

from robot.api.deco import keyword

from . import __version__
from .core import render_file, render_json, render_template, template_variables, write_json


class Paylo:
    """Create JSON payloads from templates and explicit variables.

    Import with ``Library    Paylo``. Use ``{{name}}`` for placeholders and
    ``{{customer.email}}`` for nested values. Missing values raise a clear error.
    Templates are never mutated; substitution never evaluates Python or scripts.

    Example:
    | ${values}= | Create Dictionary | name=Ana |
    | ${body}= | Render JSON | {"name":"{{name}}"} | ${values} |
    """

    ROBOT_LIBRARY_SCOPE = "GLOBAL"
    ROBOT_AUTO_KEYWORDS = False
    ROBOT_LIBRARY_VERSION = __version__

    @keyword
    def render_template(self, template, variables, missing="error"):
        """Render a dictionary/list template, preserving JSON value types."""
        return render_template(template, variables, missing=missing)

    @keyword
    def render_json(self, text, variables, missing="error"):
        """Render a valid JSON string and return its dictionary/list/value."""
        return render_json(text, variables, missing=missing)

    @keyword
    def render_json_file(self, path, variables, missing="error"):
        """Read a UTF-8 JSON file and render it using explicit variables."""
        return render_file(path, variables, missing=missing)

    @keyword
    def get_template_variables(self, template):
        """List unique placeholders from template values in alphabetical order."""
        return template_variables(template)

    @keyword
    def write_json_file(self, data, path):
        """Save rendered JSON at the given path; return the absolute filename."""
        return write_json(data, path)
