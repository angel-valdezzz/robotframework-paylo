# User guide

## Install

```bash
pip install "robotframework-paylo[robot]"
```

Python users can install `robotframework-paylo` without the Robot adapter dependencies.

## Python and Robot Framework

```python
from paylo import render_template

payload = render_template(
    {"name": "{{customer.name}}", "quantity": "{{quantity}}"},
    {"customer": {"name": "Ana"}, "quantity": 3},
)
assert payload == {"name": "Ana", "quantity": 3}
```

```robotframework
*** Settings ***
Library    Paylo

*** Test Cases ***
Create A Payload
    VAR    &{values}    name=Ana    quantity=${3}
    ${body}=    Render JSON    {"name":"{{name}}","quantity":"{{quantity}}"}    ${values}
    Should Be Equal As Integers    ${body}[quantity]    3
```

## Substitution rules

| Template | Result |
|---|---|
| `"{{quantity}}"` | Original JSON type, for example number `3` |
| `"order-{{id}}"` | String containing a scalar value |
| `"{{customer.email}}"` | Nested mapping lookup |
| `"{{rows.0.id}}"` | List index lookup |

An exact key such as `customer.email` takes precedence over a nested lookup.
Templates must be valid JSON: quote placeholders in JSON files. Keys are not substituted.
An object/list must occupy the entire value; interpolation inside longer text accepts scalars only.
Missing variables raise `MissingVariableError`; use `missing="keep"` explicitly for partial templates.
Inserted values are copied and never evaluated or expanded again. The original template and variables stay unchanged.
Use UTF-8 files with `render_file`, or `python -m paylo examples/template.json --vars examples/variables.json`.
CSV rows can be passed as dictionaries after loading them with Pytabify or Python's CSV reader.
There are no loops, script expressions, HTTP execution or hidden environment lookups.
