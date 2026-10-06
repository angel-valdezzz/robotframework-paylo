"""Safe, type-preserving JSON templates; no evaluation and no implicit I/O."""

from __future__ import annotations

import copy
import json
import re
from collections.abc import Mapping
from pathlib import Path
from typing import Any

TOKEN = re.compile(r"\{\{\s*([A-Za-z_][\w.-]*)\s*\}\}")


class MissingVariableError(ValueError):
    """A required template variable is absent."""


def _resolve(name: str, variables: Mapping[str, Any]) -> Any:
    if name in variables:
        return variables[name]
    current: Any = variables
    for part in name.split("."):
        if isinstance(current, Mapping) and part in current:
            current = current[part]
        elif isinstance(current, list) and part.isdigit() and int(part) < len(current):
            current = current[int(part)]
        else:
            raise MissingVariableError(f"Missing template variable: {name}")
    return current


def render_template(template: Any, variables: Mapping[str, Any], *, missing: str = "error") -> Any:
    """Render a JSON-compatible structure without mutating template or variables.

    An entire ``{{name}}`` string preserves the value's JSON type. Inside a longer
    string only scalar values are accepted. Missing variables raise by default;
    ``missing='keep'`` retains their original placeholder. Values are not evaluated
    or recursively expanded. Object keys are deliberately left unchanged.
    """
    if missing not in {"error", "keep"}:
        raise ValueError("missing must be 'error' or 'keep'")
    if not isinstance(variables, Mapping):
        raise TypeError("variables must be a mapping")

    def value(match: re.Match[str], exact: bool) -> Any:
        try:
            resolved = _resolve(match[1], variables)
        except MissingVariableError:
            if missing == "keep":
                return match[0]
            raise
        # Validate JSON types (including nested structures and finite numbers).
        json.dumps(resolved, allow_nan=False)
        if exact:
            return copy.deepcopy(resolved)
        if isinstance(resolved, (dict, list)):
            raise ValueError(
                f"Variable '{match[1]}' must occupy the whole string for objects/lists"
            )
        return resolved if isinstance(resolved, str) else json.dumps(resolved, allow_nan=False)

    def visit(node: Any) -> Any:
        if isinstance(node, str):
            exact = TOKEN.fullmatch(node)
            return value(exact, True) if exact else TOKEN.sub(lambda m: value(m, False), node)
        if isinstance(node, list):
            return [visit(item) for item in node]
        if isinstance(node, dict):
            return {key: visit(item) for key, item in node.items()}
        return copy.deepcopy(node)

    json.dumps(template, allow_nan=False)
    return visit(template)


def render_json(text: str, variables: Mapping[str, Any], *, missing: str = "error") -> Any:
    """Parse valid JSON, substitute its values and return the rendered structure."""
    return render_template(json.loads(text), variables, missing=missing)


def render_file(path: str | Path, variables: Mapping[str, Any], *, missing: str = "error") -> Any:
    """Read a UTF-8 JSON template and render it."""
    return render_json(Path(path).read_text(encoding="utf-8"), variables, missing=missing)


def template_variables(template: Any) -> list[str]:
    """Return sorted unique placeholder names from values (not object keys)."""
    names: set[str] = set()

    def visit(node: Any) -> None:
        if isinstance(node, str):
            names.update(TOKEN.findall(node))
        elif isinstance(node, list):
            for item in node:
                visit(item)
        elif isinstance(node, dict):
            for item in node.values():
                visit(item)

    visit(template)
    return sorted(names)


def write_json(data: Any, path: str | Path) -> str:
    """Write UTF-8 JSON to an explicit path; return its absolute filename."""
    serialized = json.dumps(data, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
    target = Path(path).resolve()
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(serialized, encoding="utf-8")
    return str(target)
