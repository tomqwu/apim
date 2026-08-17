#!/usr/bin/env python3
import pathlib
import re
import sys


directory = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "poc/apis")
files = sorted(directory.glob("*.yaml"))
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

operation_ids = []
for path in files:
    text = path.read_text(encoding="utf-8")
    if yaml is not None:
        try:
            doc = yaml.safe_load(text)
            if doc.get("openapi") != "3.0.3":
                errors.append(f"{path}: openapi must be 3.0.3")
            if not doc.get("paths") or not doc.get("components", {}).get("securitySchemes"):
                errors.append(f"{path}: paths/securitySchemes required")
            if validate_spec is not None:
                validate_spec(doc)
            for item in doc.get("paths", {}).values():
                for method, operation in item.items():
                    if method.lower() in {"get", "post", "put", "patch", "delete"}:
                        operation_ids.append(operation.get("operationId"))
        except Exception as exc:
            errors.append(f"{path}: YAML parse failed: {exc}")
    else:
        for token in ("openapi: \"3.0.3\"", "paths:", "components:", "securitySchemes:", "operationId:"):
            if token not in text:
                errors.append(f"{path}: missing {token}")
        operation_ids.extend(re.findall(r"^\s*operationId:\s*[\"']?([^\"'\s]+)", text, flags=re.MULTILINE))

if len(operation_ids) != 6 or len(set(operation_ids)) != 6 or any(not item for item in operation_ids):
    errors.append("expected six unique non-empty operationId values")
if errors:
    print("ERROR: " + "; ".join(errors), file=sys.stderr)
    raise SystemExit(1)
if validate_spec is not None:
    mode = "OpenAPI semantic validation"
elif yaml is not None:
    mode = "full YAML parse (install openapi-spec-validator for semantic validation)"
else:
    mode = "structural fallback (install PyYAML for full parse)"
print(f"OK: six OpenAPI documents validated using {mode}")
