# External citation coverage and source-promotion debt

This report is generated from the article corpus by `scripts/validate_source_coverage.py`. It distinguishes the authoritative decision-bearing source chain from additional point-of-use context. It is a coverage inventory, not a liveness result or evidence-quality score.

## Decision rule

- A citation marked `registered` resolves to `research/sources.csv`; it may support a decision-bearing finding only when `research/findings.md` maps the relevant source ID and the claim preserves its version, topology, evidence state and limitation.
- A citation marked `contextual` can explain a mechanism at the point of argument, but it cannot affect a criterion score, rank, gate disposition or recommendation until it is promoted into the register and finding chain.
- Counts measure unique normalized URLs in each document. They do not imply that document volume or citation volume increases confidence.
- Network liveness is deliberately outside deterministic CI; time-sensitive sources must be rechecked at the next decision gate.

## Current inventory

| Measure | Count |
|---|---:|
| Article files scanned | 71 |
| Article files containing external citations | 50 |
| Unique external citations | 272 |
| Unique registered citations used by articles | 36 |
| Unique contextual citations awaiting promotion if decision-bearing | 236 |
| Latest access date in authoritative register | 2026-08-17 |

## Coverage by article

| Article | Registered links | Contextual links | Boundary |
|---|---:|---:|---|
| `docs/00-executive-summary.md` | 5 | 0 | registered citations only |
| `docs/01-problem-statement.md` | 6 | 0 | registered citations only |
| `docs/02-current-state-assumptions.md` | 3 | 0 | registered citations only |
| `docs/03-assessment-methodology.md` | 3 | 0 | registered citations only |
| `docs/04-kong-first-hypothesis.md` | 10 | 0 | registered citations only |
| `docs/05-target-state-vision.md` | 1 | 2 | promotion debt visible |
| `docs/06-hybrid-cloud-requirements.md` | 4 | 1 | promotion debt visible |
| `docs/07-api-gateway-vs-integration-runtime.md` | 1 | 2 | promotion debt visible |
| `docs/08-mule-capability-decomposition.md` | 0 | 5 | promotion debt visible |
| `docs/09-product-shortlist.md` | 4 | 5 | promotion debt visible |
| `docs/10-kong-deep-dive.md` | 2 | 15 | promotion debt visible |
| `docs/11-kong-control-data-plane.md` | 2 | 2 | promotion debt visible |
| `docs/12-kong-konnect-vs-self-managed.md` | 1 | 4 | promotion debt visible |
| `docs/13-kong-on-aks.md` | 2 | 6 | promotion debt visible |
| `docs/14-kong-security.md` | 1 | 10 | promotion debt visible |
| `docs/15-kong-apiops.md` | 2 | 3 | promotion debt visible |
| `docs/16-kong-observability.md` | 2 | 2 | promotion debt visible |
| `docs/17-kong-performance.md` | 0 | 4 | promotion debt visible |
| `docs/18-kong-ha-dr.md` | 1 | 3 | promotion debt visible |
| `docs/19-azure-apim-assessment.md` | 5 | 3 | promotion debt visible |
| `docs/20-azure-apim-hybrid-fit.md` | 4 | 0 | registered citations only |
| `docs/21-apigee-assessment.md` | 3 | 8 | promotion debt visible |
| `docs/22-apigee-hybrid-fit.md` | 2 | 4 | promotion debt visible |
| `docs/23-mulesoft-current-state-baseline.md` | 2 | 10 | promotion debt visible |
| `docs/24-secondary-products.md` | 0 | 19 | promotion debt visible |
| `docs/25-security-comparison.md` | 2 | 18 | promotion debt visible |
| `docs/26-networking-comparison.md` | 2 | 14 | promotion debt visible |
| `docs/27-hybrid-multicloud-comparison.md` | 4 | 7 | promotion debt visible |
| `docs/28-kubernetes-comparison.md` | 3 | 14 | promotion debt visible |
| `docs/29-apiops-governance.md` | 3 | 7 | promotion debt visible |
| `docs/30-developer-portal-api-products.md` | 0 | 17 | promotion debt visible |
| `docs/31-observability-comparison.md` | 2 | 10 | promotion debt visible |
| `docs/32-performance-resilience.md` | 3 | 6 | promotion debt visible |
| `docs/33-operating-model.md` | 1 | 5 | promotion debt visible |
| `docs/34-pcf-aks-consolidation.md` | 3 | 8 | promotion debt visible |
| `docs/35-mule-migration-strategy.md` | 2 | 6 | promotion debt visible |
| `docs/40-audience-guide.md` | 0 | 1 | promotion debt visible |
| `docs/41-enterprise-reference-case.md` | 3 | 9 | promotion debt visible |
| `docs/42-public-failure-casebook.md` | 5 | 0 | registered citations only |
| `docs/43-api-management-industry-problems.md` | 7 | 26 | promotion debt visible |
| `docs/44-kong-multicloud-study-roadmap.md` | 9 | 18 | promotion debt visible |
| `docs/45-api-management-industry-practices.md` | 7 | 36 | promotion debt visible |
| `docs/47-kong-enterprise-platform-strategy.md` | 5 | 21 | promotion debt visible |
| `docs/48-kong-guided-evaluation.md` | 4 | 4 | promotion debt visible |
| `docs/49-kong-guided-evaluation-facilitator-guide.md` | 4 | 6 | promotion debt visible |
| `poc/real-world-scenarios.md` | 4 | 9 | promotion debt visible |
| `research/apigee.md` | 3 | 12 | promotion debt visible |
| `research/azure-apim.md` | 5 | 3 | promotion debt visible |
| `research/kong.md` | 13 | 42 | promotion debt visible |
| `research/mulesoft.md` | 2 | 18 | promotion debt visible |

## Contextual-source concentration

This table helps evidence owners batch promotion and freshness work. A high count is not a criticism when the links remain non-scoring context.

| Host | Article-link occurrences |
|---|---:|
| `developer.konghq.com` | 145 |
| `docs.mulesoft.com` | 73 |
| `learn.microsoft.com` | 44 |
| `docs.cloud.google.com` | 31 |
| `cloud.google.com` | 24 |
| `gateway-api.sigs.k8s.io` | 15 |
| `opentelemetry.io` | 11 |
| `www.rfc-editor.org` | 11 |
| `spec.openapis.org` | 7 |
| `documentation.gravitee.io` | 6 |
| `sre.google` | 6 |
| `docs.nginx.com` | 5 |
| `gateway.envoyproxy.io` | 5 |
| `kubernetes.io` | 5 |
| `istio.io` | 4 |
| `csrc.nist.gov` | 3 |
| `docs.cloudfoundry.org` | 3 |
| `github.com` | 3 |
| `aws.amazon.com` | 2 |
| `cert-manager.io` | 2 |
| `hl7.org` | 2 |
| `tomqwu.github.io` | 2 |
| `tyk.io` | 2 |
| `www.osfi-bsif.gc.ca` | 2 |
| `blog.modelcontextprotocol.io` | 1 |
| `docs.stripe.com` | 1 |
| `engineering.fb.com` | 1 |
| `modelcontextprotocol.io` | 1 |
| `openid.net` | 1 |
| `owasp.org` | 1 |
| `slsa.dev` | 1 |
| `www.asyncapi.com` | 1 |
| `www.atlassian.com` | 1 |
| `www.hl7.org` | 1 |
| `www.nist.gov` | 1 |
| `www.w3.org` | 1 |

The machine-readable usage ledger is [`reports/source-coverage.csv`](source-coverage.csv). Promote only claims that can change the decision, and add the source ID to a specific finding rather than bulk-registering links to create an appearance of rigor.
