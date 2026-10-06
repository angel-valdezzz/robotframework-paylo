# Ejemplos visuales

## Conservar tipos y resolver rutas anidadas

Un placeholder que ocupa todo el valor conserva su tipo: números y booleanos llegan al API como números y booleanos.

```python hl_lines="4-5 7"
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

## Crear un payload desde Robot Framework

Reutiliza el diccionario de cada iteración; Paylo prepara el payload y RequestsLibrary ejecuta la petición.

```robotframework hl_lines="7-9"
*** Settings ***
Library    Paylo

*** Test Cases ***
Create Payload From Data
    VAR    &{values}    name=Ana    active=${True}    quantity=${3}
    ${body}=    Render JSON    {"name":"{{name}}","active":"{{active}}","quantity":"{{quantity}}"}    ${values}
    Should Be Equal    ${body}[active]    ${True}
    Should Be Equal As Integers    ${body}[quantity]    3
```

## Detectar variables faltantes

Una variable ausente genera un error explícito antes de enviar una petición.

```python hl_lines="4-5"
from paylo import render_template, MissingVariableError

try:
    render_template({"email": "{{email}}"}, {})
except MissingVariableError as error:
    print(error)
```

## Captura del resultado

![Paylo](assets/demo/payload-result-es.png)

Esta captura se genera con el motor Python de Paylo a partir del ejemplo anterior de valores anidados y tipos. Muestra la plantilla, los datos de la iteración y el cuerpo resultante; es independiente de la demo interactiva.

## Demo interactiva

La demo usa el idioma de esta documentación y permite experimentar con valores. Es una simulación en JavaScript; los ejemplos anteriores ejecutan la librería Python.

<iframe src="../assets/demo/index.html" title="Paylo demo" style="width:100%;height:780px;border:0;border-radius:12px" loading="lazy"></iframe>
