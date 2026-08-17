# Audience guide for API management studies

## Purpose

This guide turns one canonical evidence base into six role-specific conversations. It changes the sequence, altitude, visuals, and meeting close; it does not create alternate facts, scores, or recommendations.

Use the [audience briefings](https://tomqwu.github.io/apim/#/audiences) to open a curated path or tailored presentation. Return to the source documents whenever a claim needs qualification, challenge, or approval.

## Briefing model

| Audience | Decision owned | Briefing altitude | Start with | Close with |
|---|---|---|---|---|
| Executives and VPs | Whether the decision is supportable and which investment gate opens next | Decision, exposure, optionality, and conditions | Decision readiness, mandatory gates, evidence gaps, risks, economics, and roadmap | Approve the decision contract and evidence-closure phase—not a vendor selection |
| Directors | What must be funded, staffed, governed, and sequenced | Portfolio, capacity, dependency, ownership, and delivery | Operating model, assumptions, risks, implementation sequence, and exit evidence | Name owners, dates, capacity, dependencies, funding, and phase gates |
| Architects | Whether the logical and candidate physical architectures satisfy the constraints | Capability boundaries, topology, transition, security, and resilience | Vendor-neutral target state, gateway/integration boundary, current-state gaps, and deployment variants | Approve logical boundaries and constraints before scoring candidate topologies |
| Developers | Whether producers and consumers can use the platform safely and efficiently | Contracts, API operations, developer experience, policy, and runnable proof | Contract-to-production flow, consumer journey, policy boundary, and PoC evidence | Prove approval, promotion, rollback, discovery, access, and credential lifecycle |
| DevOps and SRE | Whether the runtime can be operated and recovered under representative conditions | Runtime, automation, observability, failure, performance, and support | Kubernetes execution, failure modes, telemetry, SLOs, RTO/RPO, and runbooks | Execute disconnection, failure, soak, telemetry, redaction, and recovery tests |
| API platform teams | Whether the platform product can be adopted and operated repeatedly at scale | Paved road, tenancy, governance, support, migration, and unit economics | Service catalogue, operating contract, deployment variant, API operations, and adoption | Define support tiers, onboarding SLO, tenancy, decision rights, and unit economics |

## 1. Executives and VPs: decide

Lead with the decision state, not the volume of work completed. Separate the current working hypothesis from an approval-ready recommendation.

Recommended evidence path:

1. [Executive summary](00-executive-summary.md)
2. [Principal content and research review](../reports/content-research-principal-review.md)
3. [Content-remediation backlog](../reports/content-remediation-backlog.csv)
4. [Methodology review](../reports/methodology-review.md)
5. [Evidence state](../reports/evidence-state.md)
6. [Decision findings](../decision-matrix/findings.md)
7. [Decision matrix](../decision-matrix/README.md)
8. [Risks](37-risks.md)
9. [Delivery roadmap](36-implementation-roadmap.md)
10. [Repository roadmap](39-repository-roadmap.md)

The briefing should answer: what is known, what remains unknown, what can disqualify the priority-validation hypotheses, what investment is requested now, and who owns the next gate.

## 2. Directors: mobilize

Translate the study into accountable work. Distinguish content inventory from decision progress and activity from accepted exit evidence.

Recommended evidence path:

1. [Current-state assumptions](02-current-state-assumptions.md)
2. [Operating model](33-operating-model.md)
3. [Implementation roadmap](36-implementation-roadmap.md)
4. [Risks](37-risks.md)
5. [Open questions](38-open-questions.md)
6. [Repository roadmap](39-repository-roadmap.md)
7. [Workshop programme](../workshops/README.md)
8. [Migration factory](../mule-migration/migration-factory.md)

The briefing should produce accountable public roles or owner IDs, a restricted named-person map, capacity, dependencies, environments, commercial inputs, due dates, and evidence required at the next funding gate.

## 3. Architects: design

Keep the logical architecture vendor-neutral and maintain separate physical views for exact deployment variants. Make assumptions and unresolved data flows visible rather than smoothing them into a reference diagram.

Recommended evidence path:

1. [Current-state architecture](../architecture/current-state.md)
2. [Vendor-neutral target-state architecture](../architecture/target-state.md)
3. [Hybrid-cloud requirements](06-hybrid-cloud-requirements.md)
4. [Gateway and integration-runtime boundary](07-api-gateway-vs-integration-runtime.md)
5. [Network architecture](../architecture/network-architecture.md)
6. [Security architecture](../architecture/security-architecture.md)
7. [High availability and disaster recovery](../architecture/ha-dr-architecture.md)
8. [Architecture decisions](../adr/README.md)

The briefing should confirm capability boundaries, constraints, transition assumptions, candidate topologies, and the evidence needed to approve an architecture decision.

## 4. Developers: build and consume

Walk through the complete producer and consumer journeys. Do not use a successful gateway request as a proxy for discoverability, governance, delivery safety, or supportability.

Recommended evidence path:

1. [Gateway and integration-runtime boundary](07-api-gateway-vs-integration-runtime.md)
2. [API operations governance](29-apiops-governance.md)
3. [Developer portal and API products](30-developer-portal-api-products.md)
4. [PoC guide](../poc/README.md)
5. [API contracts](../poc/apis/README.md)
6. [API operations tests](../poc/apiops-tests.md)
7. [Migration strategy](35-mule-migration-strategy.md)
8. [Migration patterns](../mule-migration/migration-patterns.md)

The briefing should expose time-to-first-call, ownership, contract checks, approval, promotion, rollback, policy boundaries, discovery, access, credential rotation, and support.

## 5. DevOps and SRE: operate and recover

Treat a local functional baseline as proof of configuration—not proof of production operability. Use representative topology, load, dependency failure, control-plane loss, and recovery conditions.

Recommended evidence path:

1. [Observability architecture](../architecture/observability-architecture.md)
2. [High availability and disaster recovery](../architecture/ha-dr-architecture.md)
3. [Network architecture](../architecture/network-architecture.md)
4. [Failure tests](../poc/failure-tests.md)
5. [Performance tests](../poc/performance-tests.md)
6. [PoC observability](../poc/observability/README.md)
7. [Kubernetes PoC](../poc/kubernetes/README.md)
8. [Validation report](../reports/validation-report.md)

The briefing should agree the SLO, RTO, RPO, scale and failure profile, telemetry and redaction requirements, operational ownership, support boundary, and durable evidence format.

## 6. API platform teams: enable and govern

Frame the platform as a product, not a collection of gateway components. Make adoption, upgrades, exceptions, support, migration, and unit economics part of the architecture decision.

Recommended evidence path:

1. [Operating model](33-operating-model.md)
2. [API operations governance](29-apiops-governance.md)
3. [API operations architecture](../architecture/apiops-architecture.md)
4. [Kong on AKS reference architecture](../architecture/kong-aks-architecture.md)
5. [Konnect and self-managed comparison](12-kong-konnect-vs-self-managed.md)
6. [Decision matrix](../decision-matrix/README.md)
7. [API operations tests](../poc/apiops-tests.md)
8. [Repository roadmap](39-repository-roadmap.md)

The briefing should define the service catalogue, paved road, tenancy model, standard and exception ownership, onboarding SLO, support tiers, upgrade responsibility, staffing, and unit economics.

## Cross-audience handoffs

- Executives approve decision rules and investment gates; directors make the resulting work accountable.
- Architects define boundaries and constraints; platform teams turn them into a consumable service.
- Platform teams define operational standards; DevOps and SRE prove and run them.
- Platform teams provide the paved road; developers judge whether producer and consumer journeys are usable.
- Directors coordinate capacity and dependencies across every group without replacing the accountable technical or business owner.

## Facilitation rules

1. State the decision and meeting close before presenting evidence.
2. Show no score, ranking, cost, risk rating, or readiness claim without its evidence state and source.
3. Use `unknown` when the required evidence does not exist; never convert document volume into decision confidence.
4. Move detailed product facts to the canonical source path instead of duplicating them in audience material.
5. Record owner, due date, acceptance authority, and exit evidence for every action that can change the decision.
6. End with the explicit approval, rejection, evidence sprint, or escalation required from the room.
