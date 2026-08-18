#!/usr/bin/env python3
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from repository_inventory import InventoryError, files_with_suffixes


directory = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "poc/apis")
root = pathlib.Path(__file__).resolve().parents[1]
directory = (root / directory).resolve() if not directory.is_absolute() else directory.resolve()
try:
    files = files_with_suffixes(root, {".yaml"}, directory)
except InventoryError as exc:
    print(f"ERROR: {exc}", file=sys.stderr)
    raise SystemExit(1)
errors = []
if len(files) != 6:
    errors.append(f"expected 6 OpenAPI files; found {len(files)}")

try:
    import yaml  # type: ignore
except ImportError:
    yaml = None

try:
    from openapi_spec_validator import validate as validate_spec  # type: ignore
except ImportError:
    validate_spec = None

if yaml is None or validate_spec is None:
    missing = []
    if yaml is None:
        missing.append("PyYAML")
    if validate_spec is None:
        missing.append("openapi-spec-validator")
    print(
        "ERROR: required validation dependencies are unavailable: "
        + ", ".join(missing)
        + "; install requirements-validation.txt in Python 3.12",
        file=sys.stderr,
    )
    raise SystemExit(1)

operation_ids = []
for path in files:
    relative = path.relative_to(root)
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        errors.append(f"{relative}: document is unreadable or not valid UTF-8")
        continue
    if yaml is not None:
        try:
            doc = yaml.safe_load(text)
            if doc.get("openapi") != "3.0.3":
                errors.append(f"{relative}: openapi must be 3.0.3")
            if not doc.get("paths") or not doc.get("components", {}).get("securitySchemes"):
                errors.append(f"{relative}: paths/securitySchemes required")
            if validate_spec is not None:
                validate_spec(doc)
            for item in doc.get("paths", {}).values():
                for method, operation in item.items():
                    if method.lower() in {"get", "post", "put", "patch", "delete"}:
                        operation_ids.append(operation.get("operationId"))
        except Exception as exc:
            mark = getattr(exc, "problem_mark", None)
            location = f" at line {mark.line + 1}, column {mark.column + 1}" if mark is not None else ""
            errors.append(f"{relative}: invalid YAML or OpenAPI document{location}")
    else:
        for token in ("openapi: \"3.0.3\"", "paths:", "components:", "securitySchemes:", "operationId:"):
            if token not in text:
                errors.append(f"{relative}: missing {token}")
        operation_ids.extend(re.findall(r"^\s*operationId:\s*[\"']?([^\"'\s]+)", text, flags=re.MULTILINE))

if len(operation_ids) != 6 or len(set(operation_ids)) != 6 or any(not item for item in operation_ids):
    errors.append("expected six unique non-empty operationId values")
if errors:
    print("ERROR: " + "; ".join(errors), file=sys.stderr)
    raise SystemExit(1)
print("OK: six OpenAPI documents validated using OpenAPI semantic validation")
