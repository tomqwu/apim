# API Management Studies

A living collection of API management studies, research, architecture, platform comparisons, proofs of concept, migration material, workshops, templates, and presentation-ready evidence. Kong hybrid options are named low-confidence sequencing hypotheses with no execution priority; Azure API Management, Apigee, and the MuleSoft baseline receive the same option-resolution, evidence, and advancement rules.

> **Assessment status:** approve evidence closure, not a purchase recommendation. All organization-specific topology, volume, SLO, inventory, regulatory, data-residency, identity, and commercial inputs remain to be confirmed. No customer data, credentials, private topology, commercial quotes, NDA material, raw security evidence, or named-person mapping belongs in this public repository.

> **Study maturity:** the repository now has an implemented principal-content baseline—39 contract-enforced studies, deep symmetric dossiers, a reference case, a public failure casebook, three decision-grade protocols, and point-of-use figure contracts. Independent content acceptance remains open, and no protocol depth substitutes for observed candidate evidence. The [principal content review](reports/content-research-principal-review.md), [remediation backlog](reports/content-remediation-backlog.csv), [source-coverage report](reports/source-coverage.md), and [repository roadmap](docs/39-repository-roadmap.md) govern closure.

**Live portal:** [API Management Studies](https://tomqwu.github.io/apim/) · [Enterprise reference case](docs/41-enterprise-reference-case.md) · [Public failure casebook](docs/42-public-failure-casebook.md) · [Audience briefings](https://tomqwu.github.io/apim/#/audiences) · [Visual Atlas](https://tomqwu.github.io/apim/#/visuals) · [Baseline principal review](reports/content-research-principal-review.md) · [Post-remediation review](reports/content-depth-wave-1.md) · [Content backlog](reports/content-remediation-backlog.csv) · [Decision-assurance review](reports/methodology-review.md) · [Evidence state](reports/evidence-state.md) · [Repository roadmap](docs/39-repository-roadmap.md)

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
| [`decision-matrix/`](decision-matrix/README.md) | 120 gated and weighted criteria, bounded option IDs, option-resolution requirements, evidence-ledger schema, and unscored projections |
| [`workshops/`](workshops/README.md) | Nine workshop plans, a 180-question bank, and vendor-specific validation prompts |
| [`poc/`](poc/README.md) | Executable Docker baseline plus Kubernetes/Kong manifests, tests, and evidence capture |
| [`mule-migration/`](mule-migration/README.md) | Inventory, classification, routing patterns, wave planning, and decommission controls |
| [`research/`](research/README.md) | Official-source log, claim register, assumptions, and glossary |
| [`adr/`](adr/README.md) | Architecture decision records; hypotheses are not silently promoted to decisions |
| [`templates/`](templates/README.md) | Reusable collection and governance templates |
| [`reports/`](reports/content-research-principal-review.md) | Principal content review and backlog, decision-assurance review, evidence state, table-experience review, delivery inventory, and reproducible validation record |

Substantive articles use the [principal study standard](docs/STUDY-STANDARD.md) and [study template](templates/principal-study-template.md). The standard requires a real decision chain, bounded option scope with Gate-1 resolution blockers, mechanism and failure analysis, point-of-use evidence, scenario depth, inline figure contracts, falsification, and limitations; longer prose alone does not satisfy it.

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

The static site turns the repository into a searchable research library, visual evidence atlas, live Mermaid gallery, and interactive presentation without changing the source documents. Six audience briefings tailor the sequence, depth, visuals, and meeting close for executives and VPs, directors, architects, developers, DevOps/SRE, and API platform teams while retaining one canonical evidence base. Its generated index supports Markdown, Mermaid diagrams, CSV datasets, OpenAPI/YAML, code examples, images, PDF, HTML, and PowerPoint files. Successful generation and publication are technical controls; they do not certify study depth, evidence sufficiency, comparative fairness, or recommendation readiness.

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

1. Independently accept or return the implemented content baseline against the [principal review](reports/content-research-principal-review.md), strict study/figure contract, [source boundary](reports/source-coverage.md), and machine-readable backlog; no author self-closes a PCR item.
2. Approve Gate 0: sponsor, decision owner, scope/non-goals, calibrated organization inputs, bounded option catalog, option-resolution fields, mandatory/category thresholds, common-evidence/bounds/maximum-regret rules, capacity and evidence calendar.
3. Resolve edition, version, topology, region, entitlement, plugin, support and commercial fields before an archetype becomes an exact scoreable option.
4. Complete an equivalent E1/E2 screen, promote decision-bearing contextual citations into the source/finding chain, and select E3 finalists without brand priority.
5. Execute the 28 atomic real-world, portal and observability cases with identical validity, abort, reconciliation, artifact and independent-review rules; any applicable fail or indeterminate result blocks preference scoring.
6. Populate quote-based TCO, staffing/on-call, support, migration and exit evidence, then compare only with mandatory gates, common evidence, category coverage, full-weight bounds, maximum regret and sensitivity visible together.
7. Admit production pilots only after Gate 3; scale only after representative gateway- and integration-dominant E4 evidence; retire legacy responsibilities only after dependency-zero and commercial closure.

## Cross-session remediation workflow

The [content-remediation backlog](reports/content-remediation-backlog.csv) is the canonical queue for principal-review work. A Codex session should:

1. Select one or more dependency-ready `PCR-*` items and read the corresponding recommendation in the [principal content review](reports/content-research-principal-review.md).
2. Change the selected row to `in-progress`, populate its accountable owner, target gate/date, and dependencies, keep the recommendation ID stable, and limit the change to its declared scope.
3. Implement against the row's `required_remediation` and `acceptance_evidence`; update canonical evidence, figures, indexes, or generated projections rather than creating a competing source of truth.
4. Run `make validate` and record committed proof in `closure_evidence` using semicolon-separated `path:<tracked-file>`, `commit:<40-character-SHA>`, `restricted:<stable-reference>`, or `external:<https-url>#sha256=<64-hex-digest>` references. Path fragments are not accepted; use a dedicated evidence artifact when section-level precision is required. The author must not self-close the item: set it to `done` only after an independent reviewer records `review_status=accepted` and confirms that the stated acceptance evidence is satisfied.
5. Use `blocked` only when `blocker` records the unresolved dependency, missing authority, or external condition. Use `superseded` only with a stable `replacement_id` and preserved disposition history. Append a new unique recommendation ID when new work is discovered; never repurpose or delete a closed or superseded ID.

Repository validation requires every backlog ID to appear in the principal review, so the narrative findings and executable queue cannot silently diverge.

## Current hypothesis

Kong hybrid options are named low-confidence sequencing hypotheses because their documented control/data-plane separation, workload-local data planes, Kubernetes integration, and declarative automation align with the target intent. That observation confers no priority. All seven bounded archetypes receive an equivalent E1/E2 screen and must close their Gate-1 bills of materials before any finalist is approved for symmetric E3 proof. Any hypothesis fails if mandatory gates, common evidence, PoC, operating/support model, security review, total cost, or required enterprise capabilities do not support it.

Azure APIM is an important Azure-native benchmark. Its self-hosted gateway supports hybrid placement, but current documented feature and support boundaries—including the inability to associate APIM workspaces with self-hosted gateways—must be tested against the target federation model. Apigee Hybrid is an important enterprise-lifecycle benchmark, but its customer-managed runtime components and Google-hosted management plane must be justified in a hybrid Kubernetes estate.

## Evidence rules

Every material product claim must carry an evidence state (`confirmed`, `interpretation`, `assumption`, `risk`, `recommendation`, or `open-question`) and an official source where applicable. Sources were accessed on **2026-08-17** unless a row states otherwise. Scores without execution or authoritative evidence remain `unknown`.
