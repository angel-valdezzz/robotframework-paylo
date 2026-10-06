"""Paylo: safe JSON payload templates for Python and Robot Framework."""

from .core import (
    MissingVariableError,
    render_file,
    render_json,
    render_template,
    template_variables,
    write_json,
)

__version__ = "0.1.0"
__all__ = [
    "MissingVariableError",
    "render_file",
    "render_json",
    "render_template",
    "template_variables",
    "write_json",
]
