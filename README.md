<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/angel-valdezzz/robotframework-paylo/main/docs/assets/wordmark-dark.svg">
  <img src="https://raw.githubusercontent.com/angel-valdezzz/robotframework-paylo/main/docs/assets/wordmark-light.svg" alt="Paylo" width="360">
</picture>

# Paylo

Safe JSON templates with explicit variables, preserved value types and clear missing-variable errors.

[![CI](https://github.com/angel-valdezzz/robotframework-paylo/actions/workflows/ci.yml/badge.svg)](https://github.com/angel-valdezzz/robotframework-paylo/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/robotframework-paylo)](https://pypi.org/project/robotframework-paylo/)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

[User guide](https://angel-valdezzz.github.io/robotframework-paylo/) · [Guía en español](https://angel-valdezzz.github.io/robotframework-paylo/es/) · [Keyword reference ↗](https://angel-valdezzz.github.io/robotframework-paylo/keywords/index.html) · [PyPI](https://pypi.org/project/robotframework-paylo/) · [Live examples](https://angel-valdezzz.github.io/robotframework-paylo/examples/)

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


## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md), [CHANGELOG.md](CHANGELOG.md), and the [development guide](https://angel-valdezzz.github.io/robotframework-paylo/development/).
