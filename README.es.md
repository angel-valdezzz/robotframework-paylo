<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/angel-valdezzz/robotframework-paylo/main/docs/assets/wordmark-dark.svg">
  <img src="https://raw.githubusercontent.com/angel-valdezzz/robotframework-paylo/main/docs/assets/wordmark-light.svg" alt="Paylo" width="360">
</picture>

# Paylo

Plantillas JSON con variables explícitas, conservación de tipos y errores claros cuando falta una variable.

[![CI](https://github.com/angel-valdezzz/robotframework-paylo/actions/workflows/ci.yml/badge.svg)](https://github.com/angel-valdezzz/robotframework-paylo/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/robotframework-paylo)](https://pypi.org/project/robotframework-paylo/)

[English](README.md) · **Español**

[Guía de usuario ↗](https://angel-valdezzz.github.io/robotframework-paylo/es/) · [Referencia de keywords ↗](https://angel-valdezzz.github.io/robotframework-paylo/es/keywords/index.html) · [PyPI ↗](https://pypi.org/project/robotframework-paylo/) · [Ejemplos visuales ↗](https://angel-valdezzz.github.io/robotframework-paylo/es/examples/)


![Python](https://img.shields.io/pypi/pyversions/robotframework-paylo?logo=python)
![Robot Framework](https://img.shields.io/badge/Robot_Framework-compatible-00A6A6?logo=robotframework)
[![License](https://img.shields.io/github/license/angel-valdezzz/robotframework-paylo)](LICENSE)

## Instalación

```bash
pip install "robotframework-paylo[robot]"
```

En Python puedes instalar `robotframework-paylo` sin las dependencias del adaptador Robot.

## Python y Robot Framework

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


## Contribuir

Consulta [CONTRIBUTING.md](CONTRIBUTING.md), [CHANGELOG.md](CHANGELOG.md) y la [guía de desarrollo ↗](https://angel-valdezzz.github.io/robotframework-paylo/es/development/).
