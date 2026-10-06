"""Check the actual wheel contents and short Robot import in isolation."""

import subprocess
import sys
import tempfile
import venv
import zipfile
from pathlib import Path

root = Path(__file__).resolve().parents[1]
wheel = next((root / "dist").glob("*.whl"))
with zipfile.ZipFile(wheel) as archive:
    names = archive.namelist()
    assert "paylo/core.py" in names
    assert "Paylo/__init__.py" in names
with tempfile.TemporaryDirectory() as directory:
    venv.create(directory, with_pip=True)
    python = Path(directory) / ("Scripts/python.exe" if sys.platform == "win32" else "bin/python")
    subprocess.run([str(python), "-m", "pip", "install", str(wheel) + "[robot]"], check=True)
    subprocess.run(
        [str(python), "-m", "robot.libdoc", "Paylo", str(Path(directory) / "keywords.html")],
        cwd=directory,
        check=True,
    )
print("Installed wheel and short Robot import OK")
