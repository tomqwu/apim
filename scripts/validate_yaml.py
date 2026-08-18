#!/usr/bin/env python3
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from repository_inventory import InventoryError, files_with_suffixes


try:
    import yaml  # type: ignore
except ImportError:
    print("ERROR: PyYAML is required; install requirements-validation.txt in Python 3.12", file=sys.stderr)
    raise SystemExit(1)

root = pathlib.Path(__file__).resolve().parents[1]
try:
    files = files_with_suffixes(root, {".yaml", ".yml"})
except InventoryError as exc:
    print(f"ERROR: {exc}", file=sys.stderr)
    raise SystemExit(1)
errors = []
document_count = 0
for path in files:
    try:
        documents = list(yaml.safe_load_all(path.read_text(encoding="utf-8")))
        document_count += len(documents)
    except Exception as exc:
        mark = getattr(exc, "problem_mark", None)
        location = f" at line {mark.line + 1}, column {mark.column + 1}" if mark is not None else ""
        errors.append(f"{path.relative_to(root)}: invalid YAML{location}")
if errors:
    print("ERROR:\n" + "\n".join(errors), file=sys.stderr)
    raise SystemExit(1)
print(f"OK: parsed {len(files)} source YAML files / {document_count} documents")
