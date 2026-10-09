"""Generate the landing's illustrative scenarios with the real Paylo renderer."""

import json
from pathlib import Path

from paylo import render_template


def generate_landing_data(root: Path) -> None:
    template = {"name": "{{customer.name}}", "quantity": "{{quantity}}", "active": "{{active}}"}
    variables = [
        {"customer": {"name": "Ana"}, "quantity": 3, "active": True},
        {"customer": {"name": "Luis"}, "quantity": 12, "active": False},
        {"customer": {"name": "Mina"}, "quantity": 7, "active": True},
    ]
    scenarios = [
        {"variables": item, "payload": render_template(template, item)} for item in variables
    ]
    for scenario in scenarios:
        payload = scenario["payload"]
        assert isinstance(payload["name"], str)
        assert type(payload["quantity"]) is int
        assert type(payload["active"]) is bool
    destination = root / "docs/assets/landing-scenarios.json"
    destination.write_text(
        json.dumps({"template": template, "scenarios": scenarios}, indent=2) + "\n",
        encoding="utf-8",
    )
