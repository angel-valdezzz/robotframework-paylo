# Guía de usuario

## Instalación

```bash
pip install "robotframework-paylo[robot]"
```

Para Python puedes instalar `robotframework-paylo` sin las dependencias del adaptador de Robot.

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

## Reglas de sustitución

| Plantilla | Resultado |
|---|---|
| `"{{quantity}}"` | Tipo JSON original; por ejemplo el número `3` |
| `"order-{{id}}"` | Texto que contiene un valor escalar |
| `"{{customer.email}}"` | Valor de un diccionario anidado |
| `"{{rows.0.id}}"` | Acceso por índice a una lista |

Una clave literal como `customer.email` tiene prioridad sobre la búsqueda anidada.
Las plantillas deben ser JSON válido: entrecomilla los placeholders. Las claves no se sustituyen.
Una lista u objeto debe ocupar el valor completo; dentro de texto solo se admiten escalares.
Las variables ausentes lanzan `MissingVariableError`; `missing="keep"` permite conservarlas explícitamente.
Los valores se copian, nunca se evalúan ni se expanden otra vez. Los datos originales no cambian.
Usa archivos UTF-8 con `render_file`, o `python -m paylo examples/template.json --vars examples/variables.json`.
Puedes pasar filas CSV como diccionarios después de cargarlas con Pytabify o el lector CSV de Python.
No hay bucles, expresiones ejecutables, peticiones HTTP ni lectura implícita del entorno.
