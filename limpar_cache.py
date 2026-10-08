from pathlib import Path
import shutil

for path in Path(".").rglob("__pycache__"):
    shutil.rmtree(path)

for path in Path(".").rglob("*.pyc"):
    path.unlink()

print("Cache removido.")