---
template: home.html
title: Paylo
description: Safe JSON templates with explicit variables and preserved value types.
---

## De la plantilla a tus pruebas

```python hl_lines="4-8"
from paylo import render_template

payload = render_template(
    {"name": "{{customer.name}}", "quantity": "{{quantity}}", "active": "{{active}}"},
    {"customer": {"name": "Ana"}, "quantity": 3, "active": True},
)
assert payload == {"name": "Ana", "quantity": 3, "active": True}
```

El resultado conserva el texto, el número y el booleano. No se envía ninguna petición HTTP.

[Guía de usuario](guide.md) · [Ejemplos completos](examples.md)
