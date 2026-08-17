#!/usr/bin/env python3
import pathlib
import sys


try:
    import yaml  # type: ignore
except ImportError:
    print("SKIP: PyYAML unavailable; CI installs it and performs full YAML parsing")
    raise SystemExit(0)

root = pathlib.Path(__file__).resolve().parents[1]
files = sorted(path for path in root.rglob("*.yaml") if ".git" not in path.parts)
errors = []
for path in files:
    try:
        list(yaml.safe_load_all(path.read_text(encoding="utf-8")))
    except Exception as exc:
        errors.append(f"{path.relative_to(root)}: {exc}")
if errors:
    print("ERROR:\n" + "\n".join(errors), file=sys.stderr)
    raise SystemExit(1)
print(f"OK: parsed {len(files)} YAML files")
