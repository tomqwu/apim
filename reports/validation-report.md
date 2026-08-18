# Validation report

- Date: 2026-08-17
- Revision evidence: use the GitHub Actions run attached to the reviewed commit; this file records the local baseline environment and scope rather than claiming an immutable run ID
- Environment: local macOS host; Docker through temporary Colima runtime

## Passed

| Check | Result |
|---|---|
| OpenAPI semantic validation | Six OpenAPI 3.0.3 documents passed `openapi-spec-validator` |
| YAML parsing | 38 repository YAML files parsed with PyYAML; rendered Helm YAML parsed with Ruby Psych |
| Study/protocol contract | 39 principal studies / 130,498 words and three decision-grade protocols / 10,397 words passed structural, depth, evidence, inline-figure and next-gate controls |
| Matrix/question/workflow gates | 120 unique criteria, 180 unique questions and 68 traceable content-remediation recommendations |
| Markdown relative links | 355 detected local links resolve |
| Registered evidence chain | 40 unique sources, 24 findings and 28 source IDs used directly in findings resolve |
| Citation promotion boundary | 64 article files contain 211 unique external citations: 35 registered and 176 contextual/non-scoring until promoted |
| Visual parity | 12 canonical Mermaid mirrors, one canonical alias and three data-backed Markdown charts align |
| Static research portal | 184 resources built; seven bounded archetypes, seven methodology steps, 28 atomic protocol cases and six audiences project into the manifest |
| Browser/presentation | 47 presentation states passed at 1920×1080, 1440×900 and 390×844; critical labels are at least 24px, 20px and 16px respectively; six XY charts retain labels; no horizontal overflow or control collision |
| Shell/Python | ShellCheck passed; Python bytecode compilation passed |
| Compose | Configuration parsed; images built; services reached healthy state |
| Kong declarative config | `kong config parse` successful on Kong 3.9.1 |
| Functional gateway | Missing key 401; six authenticated operations 200; correlation and request/response transforms asserted |
| Traffic control | Local fixed-window limit returned 429 |
| Metrics | Prometheus endpoint exposed request counters for 200, 401, and 429 outcomes |
| Kubernetes packaging | `kong/ingress` chart 0.24.0 with Kong 3.9.1 values rendered 41 resources/documents including CRDs |
| Repository hygiene | Branding/privacy scans and `git diff --check` passed; workflow actions are commit-pinned; GitHub secret scanning, push protection and Dependabot security updates are enabled |

## Not executed

The kind/Kubernetes runtime path was not executed because `kind` and `kubectl` were unavailable on the host. Its shell is linted, repository YAML is parsed, and the pinned Helm chart is rendered, but Gateway/HTTPRoute Accepted/Programmed conditions require a live cluster. Run `make kind-up && make k8s-smoke && make kind-down` in a prepared environment.

Licensed, SaaS, AKS, hybrid CP/DP, identity/PKI, distributed rate limiting, multi-region, vendor support, and representative performance scenarios remain explicitly `not-run` in `poc/test-plan.md`.
