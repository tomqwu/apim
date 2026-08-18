#!/usr/bin/env python3
import pathlib
import sys


try:
    import yaml  # type: ignore
except ImportError:
    print("SKIP: PyYAML unavailable; CI installs it and performs full YAML parsing")
    raise SystemExit(0)

root = pathlib.Path(__file__).resolve().parents[1]
ignored_directories = {".git", "_site"}
files = sorted(
    {
        path
        for pattern in ("*.yaml", "*.yml")
        for path in root.rglob(pattern)
        if not ignored_directories.intersection(path.relative_to(root).parts)
    }
)
errors = []
document_count = 0
for path in files:
    try:
        documents = list(yaml.safe_load_all(path.read_text(encoding="utf-8")))
        document_count += len(documents)
    except Exception as exc:
        errors.append(f"{path.relative_to(root)}: {exc}")
if errors:
    print("ERROR:\n" + "\n".join(errors), file=sys.stderr)
    raise SystemExit(1)
print(f"OK: parsed {len(files)} source YAML files / {document_count} documents")
