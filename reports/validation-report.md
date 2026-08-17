# Validation report

- Date: 2026-08-17
- Commit: working tree prior to publication; CI will record the immutable commit
- Environment: local macOS host; Docker through temporary Colima runtime

## Passed

| Check | Result |
|---|---|
| OpenAPI semantic validation | Six OpenAPI 3.0.3 documents passed `openapi-spec-validator` |
| YAML parsing | Nineteen repository YAML files parsed with PyYAML; rendered Helm YAML parsed with Ruby Psych |
| Matrix/question gates | 120 unique criteria and 180 unique questions |
| Markdown relative links | All detected local links resolve |
| Shell/Python | ShellCheck passed; Python bytecode compilation passed |
| Compose | Configuration parsed; images built; services reached healthy state |
| Kong declarative config | `kong config parse` successful on Kong 3.9.1 |
| Functional gateway | Missing key 401; six authenticated operations 200; correlation and request/response transforms asserted |
| Traffic control | Local fixed-window limit returned 429 |
| Metrics | Prometheus endpoint exposed request counters for 200, 401, and 429 outcomes |
| Kubernetes packaging | `kong/ingress` chart 0.24.0 with Kong 3.9.1 values rendered 41 resources/documents including CRDs |
| Repository hygiene | `git diff --check` and Docker Compose configuration passed |

## Not executed

The kind/Kubernetes runtime path was not executed because `kind` and `kubectl` were unavailable on the host. Its shell is linted, repository YAML is parsed, and the pinned Helm chart is rendered, but Gateway/HTTPRoute Accepted/Programmed conditions require a live cluster. Run `make kind-up && make k8s-smoke && make kind-down` in a prepared environment.

Licensed, SaaS, AKS, hybrid CP/DP, identity/PKI, distributed rate limiting, multi-region, vendor support, and representative performance scenarios remain explicitly `not-run` in `poc/test-plan.md`.
