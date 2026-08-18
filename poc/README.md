# Executable API management PoC

## Two execution paths

- `make poc-up`: Docker Compose, Kong Gateway OSS in DB-less mode, and one synthetic banking backend. This is the fastest functional policy baseline.
- `make kind-up`: local kind cluster, Gateway API v1.5.1, Kong's `ingress` Helm chart, Kubernetes routes/plugins, and the same backend image.

The static `make validate` path parses OpenAPI/YAML, checks the minimum research counts, and lints shell scripts where available.

## Decision-grade experiment protocols

- [Real-world scenario portfolio](real-world-scenarios.md) — cross-layer business, failure, recovery, and migration experiments grounded in synthetic reference case RE-1.
- [Developer portal and API-product proof](portal-tests.md) — discovery-through-revocation lifecycle, identity, ownership, approval, credential, runtime-truth, accessibility, outage, and exit testing.
- [Observability and operational-evidence proof](observability-tests.md) — signal completeness, business-outcome correlation, error semantics, redaction, cardinality, backpressure, configuration truth, regional loss, audit, and operator diagnosis.

These are executable evidence protocols, not claims of product performance. All numeric inputs are scenario assumptions until ratified; all candidate states begin `not run`.

Files carrying `<!-- protocol-contract: decision-grade -->` are publication-gated. They must retain a purpose and decision boundary, operational scenario/fault coverage, explicit abort conditions, an evidence/reconciliation contract, independent review, inline causal diagrams, control tables, and a gate. `make validate-studies` enforces the structural floor; a passing file is still a protocol until immutable run evidence is linked and reviewed.

## Current execution state

The [test plan](test-plan.md) is the canonical scenario-status register. “Implemented” or “configured” is not an execution result.

The register contains 16 aggregate items: five have automated local-baseline evidence and 11 are not run. The three decision-grade protocols define a separate, overlapping set of **28 atomic cases**—12 real-world, seven portal and nine observability cases. All candidate × atomic-case cells begin `not run`. Do not add 16 and 28 or use protocol count as progress; the former tracks aggregate capability status and the latter defines the hard-gated comparative experiment design.

| Capability | Docker baseline | Kubernetes path | Evidence/test |
|---|---:|---:|---|
| Six banking facade operations | Executed — pass | Implemented — not run | `make smoke` / `make k8s-smoke` |
| API key allow/deny | Executed — pass | Implemented — not run | smoke negative/positive cases |
| Correlation ID | Executed — pass | Implemented — not run | response-header assertion |
| Request/response header transform | Executed — pass | Implemented — not run | backend/body and response assertion |
| Fixed-window local rate limit | Executed — pass | Implemented — not run | `make rate-limit-test` |
| Prometheus plugin | Executed — pass | Configured — not run | metrics endpoint/config inspection |
| Gateway API HTTPRoute | Not applicable | Implemented — not run | live Accepted/Programmed conditions and smoke |
| OpenAPI validation | Automated — pass | Automated — pass | `make validate-openapi` |
| Portal/product lifecycle | Not run | Not run | `portal-tests.md` with candidate-specific evidence bundle |
| Observability/operational evidence | Baseline only | Not run | `observability-tests.md` with candidate-specific evidence bundle |

## Deliberately not claimed as tested

Konnect, self-managed hybrid CP/DP, Enterprise OIDC and request/OAS validation, distributed/global rate limiting, production mTLS/PKI, portal/catalog, enterprise audit/analytics, AKS networking/workload identity, multi-zone/region DR, SIEM/APM integration, licensed support, and vendor commercial terms. Use the documents in this directory as test plans for a vendor-enabled environment.

## Synthetic credential

The literal `api-platform-poc-key` is a public test fixture, not a secret. Production credentials must come from approved identity/secrets systems and must never be committed.

## Evidence capture

Copy `templates/poc-result-template.md` per test. Record product/edition/version/topology, commit, commands, expected/actual outcome, sanitized logs/metrics, criterion IDs, and limitation. Do not commit raw payloads or credentials.
