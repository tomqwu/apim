# API Management Studies

A living collection of API management studies, research, architecture, platform comparisons, proofs of concept, migration material, workshops, templates, and presentation-ready evidence. Kong hybrid variants are low-confidence priority-validation hypotheses; Azure API Management and Apigee remain required hybrid benchmarks, and MuleSoft remains the current-state baseline rather than a one-for-one migration target.

> **Assessment status:** approve evidence closure, not a purchase recommendation. All organization-specific topology, volume, SLO, inventory, regulatory, data-residency, identity, and commercial inputs remain to be confirmed. No customer data, credentials, private topology, commercial quotes, NDA material, raw security evidence, or named-person mapping belongs in this public repository.

**Live portal:** [API Management Studies](https://tomqwu.github.io/apim/) · [Audience briefings](https://tomqwu.github.io/apim/#/audiences) · [Visual Atlas](https://tomqwu.github.io/apim/#/visuals) · [Principal review](reports/methodology-review.md) · [Evidence state](reports/evidence-state.md) · [Repository roadmap](docs/39-repository-roadmap.md)

## Decision statement

Select the API management and gateway architecture that best supports a Kubernetes-centered target state, coexistence with legacy platforms, staged integration-platform decomposition, regulated-enterprise controls, and workload-local data planes without moving orchestration or business logic into gateway policy.

## Architecture principles

1. Keep complex transformation, orchestration, workflow, messaging, file transfer, and domain logic outside the gateway.
2. Separate control-plane availability from request-path availability and test both.
3. Prefer open contracts (OpenAPI, OAuth/OIDC, OpenTelemetry, Kubernetes Gateway API) while recording every vendor-specific extension.
4. Keep the gateway close to workloads where latency, data residency, or failure-domain isolation requires it.
5. Treat configuration as reviewed, promoted, reversible code; never expose an administration endpoint publicly.
6. Make policy ownership federated but guardrails, identity, audit, and evidence centrally governed.
7. Do not claim an enterprise, licensed, SaaS, or cloud feature was tested unless execution evidence exists.

## Repository map

| Area | Purpose |
|---|---|
| [`docs/`](docs/README.md) | Assessment narrative, architecture, security, operations, roadmap, risks, and open questions |
| [`architecture/`](architecture/README.md) | Current, transition, target, security, network, API operations, observability, and DR views |
| [`decision-matrix/`](decision-matrix/README.md) | 120 gated and weighted criteria, scoring method, exact-variant evidence-ledger schema, and scorecard projections |
| [`workshops/`](workshops/README.md) | Nine workshop plans, a 180-question bank, and vendor-specific validation prompts |
| [`poc/`](poc/README.md) | Executable Docker baseline plus Kubernetes/Kong manifests, tests, and evidence capture |
| [`mule-migration/`](mule-migration/README.md) | Inventory, classification, routing patterns, wave planning, and decommission controls |
| [`research/`](research/README.md) | Official-source log, claim register, assumptions, and glossary |
| [`adr/`](adr/README.md) | Architecture decision records; hypotheses are not silently promoted to decisions |
| [`templates/`](templates/README.md) | Reusable collection and governance templates |
| [`reports/`](reports/methodology-review.md) | Methodology review, delivery inventory, and reproducible validation record |

## Quick start

Prerequisites for the fastest path are Docker and `curl`:

```bash
make poc-up
make smoke
make rate-limit-test
make poc-down
```

For the Kubernetes path, install Docker, `kind`, `kubectl`, and Helm, then run:

```bash
make kind-up
make k8s-smoke
make kind-down
```

Static checks do not require a cluster:

```bash
make validate
```

See [`poc/README.md`](poc/README.md) for test scope and limitations.

## Research portal

The static site turns the repository into a searchable research library, visual evidence atlas, live Mermaid gallery, and interactive presentation without changing the source documents. Six audience briefings tailor the sequence, depth, visuals, and meeting close for executives and VPs, directors, architects, developers, DevOps/SRE, and API platform teams while retaining one canonical evidence base. Its generated index supports Markdown, Mermaid diagrams, CSV datasets, OpenAPI/YAML, code examples, images, PDF, HTML, and PowerPoint files.

Build and preview it locally:

```bash
make site-serve
```

Then open `http://localhost:8008`. Use **Audiences** to enter through a role-specific decision path, **Present** for the complete curated story, arrow keys to move, `F` for fullscreen, and `Esc` to exit. Use `Cmd/Ctrl + K` anywhere in the portal for full-text search.

The output is generated in `_site/` and is not committed. Adding supported material under an existing repository collection is enough for it to appear in the next build; the first Markdown heading becomes its display title.

### GitHub Pages

The public portal is published at [tomqwu.github.io/apim](https://tomqwu.github.io/apim/). The Pages workflow validates every change to `main` and deploys when the repository variable `PAGES_ENABLED` is `true`.

## What the baseline PoC proves

- Six OpenAPI-defined banking facade operations route through Kong to a synthetic backend.
- Key authentication, correlation ID, header transformation, basic rate limiting, structured proxy behavior, and Prometheus exposure can be exercised locally.
- Gateway API objects model portable Kubernetes routing; Kong-specific plugins are isolated and visible.
- Configuration and test evidence can be promoted through Git without embedding secrets.

It does **not** prove Konnect, Kong Enterprise plugins, OIDC, production PKI/mTLS, Azure networking, multi-region failover, licensed portals, enterprise analytics, or commercial support. Those remain gated vendor/environment tests.

## Assessment workflow

1. Confirm scope and inputs in [`docs/02-current-state-assumptions.md`](docs/02-current-state-assumptions.md).
2. Run stakeholder workshops and capture evidence rather than opinions.
3. Populate the Mule inventory and derive responsibility destinations.
4. Execute the thin PoC, then the security, resilience, scale, and disconnected-control-plane tests.
5. Score pass/fail gates first, then weighted criteria, using `unknown` rather than optimistic values.
6. Review commercial and contractual facts under separate approval.
7. Publish a recommendation only after evidence coverage and sensitivity analysis meet the agreed threshold.

## Current hypothesis

Kong hybrid variants are low-confidence priority-validation hypotheses because their control/data-plane separation, workload-local data planes, Kubernetes integration, and declarative automation align with the target intent. All seven variants receive an equivalent E1/E2 screen before finalists are approved for symmetric E3 proof. The Kong hypothesis fails if the PoC, operating model, support model, security review, total cost, or required enterprise capabilities do not meet decision gates.

Azure APIM is an important Azure-native benchmark. Its self-hosted gateway supports hybrid placement, but current documented feature and support boundaries—including the inability to associate APIM workspaces with self-hosted gateways—must be tested against the target federation model. Apigee Hybrid is an important enterprise-lifecycle benchmark, but its customer-managed runtime components and Google-hosted management plane must be justified in a hybrid Kubernetes estate.

## Evidence rules

Every material product claim must carry an evidence state (`confirmed`, `interpretation`, `assumption`, `risk`, `recommendation`, or `open-question`) and an official source where applicable. Sources were accessed on **2026-08-17** unless a row states otherwise. Scores without execution or authoritative evidence remain `unknown`.
