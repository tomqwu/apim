# Validation report

- Date: 2026-08-18
- Revision evidence: use the GitHub Actions run attached to the reviewed commit; this file records the local baseline environment and scope rather than claiming an immutable run ID
- Environment: local macOS host; Docker through temporary Colima runtime

## Passed

| Check | Result |
|---|---|
| OpenAPI semantic validation | Six OpenAPI 3.0.3 documents passed `openapi-spec-validator` |
| YAML parsing | 22 source YAML files / 32 documents parsed with PyYAML; generated `_site` copies are excluded; rendered Helm YAML parsed with Ruby Psych |
| Study/protocol contract | 43 principal studies / 176,981 words and three decision-grade protocols / 10,397 words passed structural, depth, evidence, inline-figure and next-gate controls |
| Matrix/question/workflow gates | 120 unique criteria, 180 unique questions and 68 traceable content-remediation recommendations |
| Markdown relative links | 521 detected local links resolve |
| Registered evidence chain | 40 unique sources, 24 findings and 28 source IDs used directly in findings resolve |
| Citation promotion boundary | 69 article files contain 271 unique external citations: 36 registered and 235 contextual/non-scoring until promoted |
| Visual parity | 12 canonical Mermaid mirrors, one canonical alias and three data-backed Markdown charts align |
| Static research portal | 191 resources built; seven bounded archetypes, seven methodology steps, 28 atomic protocol cases, 10 industry practices, eight industry-practice scenarios, five evidence-maturity stages, seven Kong fit conditions, 10 Kong problem responses, eight Kong platform cases, six adoption phases, 11 outcome contracts and six audiences project from canonical sources into the manifest |
| Browser/presentation | 81 configured presentation states; eight Kong-platform strategy states plus tailored audience routes passed at 1920×1080, 1440×900, 1024×768, 760×820 and 390×844. The canonical article renders six Mermaid figures and five data-backed placements; slide projections preserve seven fit conditions, 10 P1–P10 responses, eight cases, six roadmap phases and 11 outcome contracts. Critical labels remain at least 18px at room width and 16px elsewhere; every owner, cadence, proof, hold and exit field is reachable, with no painted-content clipping, hidden field, horizontal overflow, control collision or console error |
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
