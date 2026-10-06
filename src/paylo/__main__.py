"""Command-line JSON rendering."""

import argparse
import json
from pathlib import Path

from .core import render_file, write_json


def main():
    parser = argparse.ArgumentParser(description="Render a Paylo JSON template")
    parser.add_argument("template")
    parser.add_argument("--vars", required=True, dest="variables")
    parser.add_argument("--output")
    args = parser.parse_args()
    try:
        data = render_file(
            args.template, json.loads(Path(args.variables).read_text(encoding="utf-8"))
        )
        if args.output:
            write_json(data, args.output)
        else:
            print(json.dumps(data, ensure_ascii=False, indent=2, allow_nan=False))
    except (ValueError, TypeError, OSError) as error:
        parser.exit(2, f"Paylo: {error}\n")


if __name__ == "__main__":
    main()
