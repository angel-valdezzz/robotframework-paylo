import copy
import json
import subprocess
import sys

import pytest

from paylo import (
    MissingVariableError,
    render_file,
    render_json,
    render_template,
    template_variables,
    write_json,
)


def test_types_nested_paths_and_inputs_unchanged():
    template = {
        "name": "{{user.name}}",
        "age": "{{age}}",
        "active": "{{active}}",
        "items": "{{items}}",
        "nested": ["{{rows.0.id}}"],
        "message": "Hi {{user.name}}: {{age}}",
    }
    variables = {
        "user": {"name": 'Ana "QA"\n'},
        "age": 30,
        "active": True,
        "items": [1, {"a": None}],
        "rows": [{"id": 9}],
    }
    before = copy.deepcopy((template, variables))
    result = render_template(template, variables)
    assert result == {
        "name": 'Ana "QA"\n',
        "age": 30,
        "active": True,
        "items": [1, {"a": None}],
        "nested": [9],
        "message": 'Hi Ana "QA"\n: 30',
    }
    result["items"][1]["a"] = 100
    assert (template, variables) == before


@pytest.mark.parametrize("value", [True, False, None, 12, 2.5, "x"])
def test_exact_and_interpolated_scalar(value):
    assert render_template("{{x}}", {"x": value}) == value
    expected = value if isinstance(value, str) else json.dumps(value)
    assert render_template("value={{x}}", {"x": value}) == "value=" + expected


def test_missing_modes_and_no_recursive_or_code_evaluation():
    with pytest.raises(MissingVariableError, match="user.name"):
        render_template({"x": "{{user.name}}"}, {})
    assert render_template("{{missing}}", {}, missing="keep") == "{{missing}}"
    assert render_template("{{x}}", {"x": "{{y}}", "y": "expanded"}) == "{{y}}"
    assert render_template('{{__import__("os")}}', {}) == '{{__import__("os")}}'
    assert render_template({"{{x}}": "literal"}, {"x": "new"}) == {"{{x}}": "literal"}


@pytest.mark.parametrize("variables", [{"x": []}, {"x": {}}, {"x": float("nan")}])
def test_invalid_embedded_values(variables):
    with pytest.raises(ValueError):
        render_template("prefix {{x}}", variables)


def test_errors_and_literal_dotted_key():
    assert render_template("{{a.b}}", {"a.b": 3, "a": {"b": 4}}) == 3
    with pytest.raises(ValueError):
        render_template("x", {}, missing="unknown")
    with pytest.raises(TypeError):
        render_template("x", [])
    with pytest.raises(ValueError):
        render_json('{"age":{{age}}}', {"age": 3})
    assert template_variables(
        {"key": ["{{ x }}", "{{user.email}}", "{{x}}"], "{{ignored}}": 1}
    ) == ["user.email", "x"]


def test_files_and_cli(tmp_path):
    source = tmp_path / "template.json"
    source.write_text('{"name":"{{name}}"}', encoding="utf-8")
    variables = tmp_path / "vars.json"
    variables.write_text('{"name":"José"}', encoding="utf-8")
    result = render_file(source, {"name": "José"})
    output = write_json(result, tmp_path / "nested/output.json")
    assert json.loads(open(output, encoding="utf-8").read()) == result
    process = subprocess.run(
        [sys.executable, "-m", "paylo", str(source), "--vars", str(variables)],
        capture_output=True,
        text=True,
    )
    assert process.returncode == 0 and json.loads(process.stdout) == result
