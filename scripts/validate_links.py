#!/usr/bin/env python3
import pathlib
import re
import sys
from urllib.parse import unquote

from repository_inventory import InventoryError, files_with_suffixes


root = pathlib.Path(__file__).resolve().parents[1]
pattern = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
errors = []
checked = 0
try:
    documents = files_with_suffixes(root, {".md"})
except InventoryError as exc:
    print(f"ERROR: {exc}", file=sys.stderr)
    raise SystemExit(1)

for document in documents:
    text = document.read_text(encoding="utf-8")
    for raw_target in pattern.findall(text):
        target = raw_target.strip().strip("<>").split()[0]
        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        target = unquote(target.split("#", 1)[0])
        if not target:
            continue
        resolved = (document.parent / target).resolve()
        checked += 1
        try:
            resolved.relative_to(root)
        except ValueError:
            errors.append(f"{document.relative_to(root)}: link escapes repository: {raw_target}")
            continue
        if not resolved.exists():
            errors.append(f"{document.relative_to(root)}: missing link target: {raw_target}")

if errors:
    print("ERROR:\n" + "\n".join(errors), file=sys.stderr)
    raise SystemExit(1)
print(f"OK: {checked} relative Markdown links resolve")
