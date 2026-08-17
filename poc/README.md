# Executable Kong PoC

## Two execution paths

- `make poc-up`: Docker Compose, Kong Gateway OSS in DB-less mode, and one synthetic banking backend. This is the fastest functional policy baseline.
- `make kind-up`: local kind cluster, Gateway API v1.5.1, Kong's `ingress` Helm chart, Kubernetes routes/plugins, and the same backend image.

The static `make validate` path parses OpenAPI/YAML, checks the minimum research counts, and lints shell scripts where available.

## Current execution state

The [test plan](test-plan.md) is the canonical scenario-status register. “Implemented” or “configured” is not an execution result.

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

## Deliberately not claimed as tested

Konnect, self-managed hybrid CP/DP, Enterprise OIDC and request/OAS validation, distributed/global rate limiting, production mTLS/PKI, portal/catalog, enterprise audit/analytics, AKS networking/workload identity, multi-zone/region DR, SIEM/APM integration, licensed support, and vendor commercial terms. Use the documents in this directory as test plans for a vendor-enabled environment.

## Synthetic credential

The literal `api-platform-poc-key` is a public test fixture, not a secret. Production credentials must come from approved identity/secrets systems and must never be committed.

## Evidence capture

Copy `templates/poc-result-template.md` per test. Record product/edition/version/topology, commit, commands, expected/actual outcome, sanitized logs/metrics, criterion IDs, and limitation. Do not commit raw payloads or credentials.
