# Validation report

- Date: 2026-08-19
- Revision evidence: use the GitHub Actions run attached to the reviewed commit; this file records the local baseline environment and scope rather than claiming an immutable run ID
- Environment: local macOS host; Docker through temporary Colima runtime

## Passed

| Check | Result |
|---|---|
| OpenAPI semantic validation | Six OpenAPI 3.0.3 documents passed `openapi-spec-validator` |
| YAML parsing | 22 source YAML files / 32 documents parsed with PyYAML; generated `_site` copies are excluded; rendered Helm YAML parsed with Ruby Psych |
| Study/protocol contract | 43 principal studies / 177,105 words and three decision-grade protocols / 10,397 words passed structural, depth, evidence, inline-figure and next-gate controls |
| Matrix/question/workflow gates | 120 unique criteria, 180 unique questions and 68 traceable content-remediation recommendations |
| Markdown relative links | 526 detected local links resolve |
| Registered evidence chain | 40 unique sources, 24 findings and 28 source IDs used directly in findings resolve |
| Citation promotion boundary | 69 article files contain 271 unique external citations: 36 registered and 235 contextual/non-scoring until promoted |
| Visual parity | 12 canonical Mermaid mirrors, one canonical alias and three data-backed Markdown charts align |
| Static research portal | 191 resources built; seven bounded archetypes, seven methodology steps, 28 atomic protocol cases, 10 industry practices, eight industry-practice scenarios, five evidence-maturity stages, seven Kong fit conditions, 10 Kong problem responses, eight Kong platform cases, six adoption phases, 11 outcome contracts, six canonical Kong platform figures, six audiences and two named Kong decks project from canonical sources into the manifest |
| Browser/presentation | 130 configured presentation states: 37 generic, 63 tailored audience and 30 named states across the retained Kong technical deep dive and the new 15-slide Kong platform journey. The journey’s source-derived sequence is decision, bounded operating options, conditional self-managed target, architecture/trust/degraded-mode controls, operating model and adoption roadmap, three Mule migration boundaries, current proof boundary, outcome contracts and assurance/exit gates. Its phase allocation is 3 Options / 3 Architecture / 2 Adoption / 3 Migration / 4 Production. All 15 journey routes passed at 1920×1080, 1440×900, 1024×768, 760×820 and 390×844: no page-level horizontal overflow, painted-content clipping, hidden decision field, control collision, route error or default nested scrolling was observed; desktop/tablet main and proof surfaces remained one-frame, while narrow screens used one vertical stage scroller. Semantic copy measures at least 24px at the room viewport, 18px at laptop/tablet widths and 16px on narrow surfaces; provenance, phase and diagram UI metadata measure at least 16px; controls retain at least 44px targets. Six dense diagrams open on an authored Takeaway, with explicit Overview, Readable and expanded-canvas inspection modes. Every slide prints as one 16:9 current-route page with its Takeaway and visible source locator; the site does not claim a combined one-action 15-page PDF export. Exact `/0` through `/14` navigation, phase state, keyboard controls, source links and strict `/15` rejection passed. The canonical article continues to carry the full Mermaid and tabular evidence, and the existing technical-deep-dive route remains available as the implementation-detail companion |
| PoC evidence presentation | The canonical 16-item aggregate register projects as one 5-automated / 11-not-run evidence ratio rather than a redundant donut and repeated status ledger. The Lab shows every scenario ID exactly once in two cohorts and links directly to `poc/test-plan.md`; compact and presentation contexts retain the decision ratio while omitting the detail ledger. `#/lab` passed 1920, 1508, 1440, 1401, 1400, 1024, 760 and 390px-wide browser checks: panels are balanced 6+6 above 1400px and stack without page or internal overflow at and below 1400px. Overview, Visual Atlas, canonical document and generic proof regressions passed desktop/mobile checks. All five tailored proof routes passed final 1024×768 and 390×844 checks with both proportional segments and the rail boundary visibly distinct, 16px supporting-source metadata, keyboard-owned overflow where present, reachable source navigation and no browser errors |
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
