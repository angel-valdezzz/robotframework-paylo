"""Build bilingual manual, examples and keyword documentation."""

from pathlib import Path

from bilingual_libdoc import generate
from bilingual_site import build

ROOT = Path(__file__).resolve().parents[2]
if __name__ == "__main__":
    generate(
        "Paylo",
        ROOT,
        "keywords/index.html",
        "https://angel-valdezzz.github.io/robotframework-paylo/",
    )
    build(ROOT)
