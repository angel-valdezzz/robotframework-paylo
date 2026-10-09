---
template: home.html
title: Paylo
description: Safe JSON templates with explicit variables and preserved value types.
---

## From a template to your tests

```python hl_lines="4-8"
from paylo import render_template

payload = render_template(
    {"name": "{{customer.name}}", "quantity": "{{quantity}}", "active": "{{active}}"},
    {"customer": {"name": "Ana"}, "quantity": 3, "active": True},
)
assert payload == {"name": "Ana", "quantity": 3, "active": True}
```

The result retains the string, number and boolean. No HTTP request is sent.

[User guide](guide.md) · [Complete examples](examples.md)
