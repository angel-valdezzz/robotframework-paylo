# Visual examples

## Preserve types and resolve nested values

A placeholder occupying the entire value preserves its type: numbers and booleans reach the API as numbers and booleans.

```python
from paylo import render_template

body = render_template(
    {"name": "{{customer.name}}", "active": "{{active}}", "count": "{{count}}"},
    {"customer": {"name": "Ana"}, "active": True, "count": 3},
)
assert body == {"name": "Ana", "active": True, "count": 3}
```

```json
{"name": "Ana", "active": true, "count": 3}
```

## Create a payload from Robot Framework

Reuse the dictionary from each iteration; Paylo prepares the payload and RequestsLibrary sends the request.

```robotframework
*** Settings ***
Library    Paylo

*** Test Cases ***
Create Payload From Data
    VAR    &{values}    name=Ana    active=${True}    quantity=${3}
    ${body}=    Render JSON    {"name":"{{name}}","active":"{{active}}","quantity":"{{quantity}}"}    ${values}
    Should Be Equal    ${body}[active]    ${True}
    Should Be Equal As Integers    ${body}[quantity]    3
```

## Detect missing variables

A missing variable raises an explicit error before sending a request.

```python
from paylo import render_template, MissingVariableError

try:
    render_template({"email": "{{email}}"}, {})
except MissingVariableError as error:
    print(error)
```

## Result screenshot

The screenshot shows the demo input and rendered JSON. The Python example above uses the real Paylo engine.

## Interactive demo

The demo follows the documentation language and lets you experiment with values. It is a JavaScript simulation; the examples above execute the Python library.

[Open demo ↗](assets/demo/index.html){ target="_blank" rel="noopener noreferrer" .md-button }

<iframe src="../assets/demo/index.html" title="Paylo demo" style="width:100%;height:780px;border:0;border-radius:12px" loading="lazy"></iframe>
