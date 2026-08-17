# Consulting-style methodology and decision-readiness review

- Review date: 2026-08-17
- Scope: repository structure, assessment method, evidence chain, documents, PoC material, audience briefings, and presentation
- Evidence basis: committed repository content only; no stakeholder interviews, vendor briefings, commercial quotes, or client validation were available
- Review stance: decision-assurance challenge; no platform selection is approved by this report

## Executive verdict

The repository is a strong assessment scaffold and an early evidence baseline. It is not yet a completed comparative platform assessment.

| Dimension | Maturity | Finding |
|---|---|---|
| Assessment framework | Strong scaffold | Strong gates, evidence levels, variant separation, unknown handling, and falsification discipline |
| Evidence completion | Initial | All 120 criteria remain unknown and no candidate variant has a populated scorecard |
| Comparative integrity | Developing | The comparison model is sound, but research and executable proof are currently asymmetric |
| Governance readiness | Developing | Assumptions, risks, questions, weights, thresholds, and ADRs are visible but not yet operationally closed |
| Audience communication | Strong scaffold | Six role-specific briefings sequence the same canonical evidence for executives, directors, architects, developers, DevOps/SRE, and platform teams |
| Executive decision readiness | Not ready | The current direction is appropriately provisional; a final recommendation would be premature |

The maturity labels are deliberately qualitative: **Initial** means decision evidence is largely uncollected; **Developing** means material controls exist but are not operationally complete; **Strong scaffold** means the method is well structured but not yet executed; and **Not ready** means the stated decision gates are unmet. These labels are not vendor or product scores.

Current maturity is **structured assessment / evidence collection**. The appropriate steering decision is to approve the evidence-closure phase, not to select a product.

## Review method

Every material conclusion should preserve this traceable chain:

> Business outcome → requirement → mandatory gate → evidence → test → score → implication → decision

The review applies three lenses:

1. **Repository assurance:** completeness, provenance, freshness, reproducibility, navigation, and public-safe content.
2. **Decision assurance:** scope, alternatives, approved gates, evidence quality, comparative fairness, economics, sensitivity, and decision rights.
3. **Role-specific communication:** decision requested, appropriate level of detail, trade-offs, uncertainty, risks, roadmap, and accountable next actions for each audience.

A conclusion remains provisional whenever one of those links is missing.

## What is strong

- Exact deployment variants are evaluated separately in the [decision matrix](../decision-matrix/README.md).
- Mandatory gates cannot be averaged away, and unknown evidence is never treated as pass in the [scoring guide](../decision-matrix/scoring-guide.md).
- Evidence confidence progresses from assertion to official documentation, vendor confirmation, repeatable lab, and representative pilot in the [assessment methodology](../docs/03-assessment-methodology.md).
- The [Kong-first hypothesis](../docs/04-kong-first-hypothesis.md) includes explicit falsification conditions.
- The [executive summary](../docs/00-executive-summary.md) distinguishes a provisional direction from a product selection.
- The [audience guide](../docs/40-audience-guide.md) gives six roles different decisions, reading sequences, visuals, and meeting closes without duplicating the underlying evidence.
- The PoC documentation explicitly separates demonstrated baseline mechanics from licensed, hybrid, identity, performance, and production claims in [poc/README.md](../poc/README.md).

## Material gaps

### 1. Decision evidence is incomplete

All 120 criteria are currently `unknown`, including 30 mandatory gates. The seven exact deployment variants do not have populated criterion-level scorecards. A candidate ranking must not be published until the agreed evidence-coverage threshold is met.

### 2. The logical architecture is solution-anchored

The [target-state vision](../docs/05-target-state-vision.md) names Kong data planes before the organizational assumptions, gates, and scorecards are resolved. Maintain a vendor-neutral logical target architecture, then create candidate-specific deployment views for Kong, Azure API Management, and Apigee.

### 3. Organizational facts remain assumptions

All ten entries in the [assumption register](../docs/02-current-state-assumptions.md) remain open. Each needs a named accountable owner, validation evidence, due date, and explicit decision impact.

### 4. Comparative proof is asymmetric

The repository contains 27 official sources, of which 12 are Kong sources. Fifteen source IDs are cited in the claim register and twelve are not yet used there. The baseline PoC proves useful gateway mechanics, but eight of fourteen decision-critical scenarios remain not run in the [test plan](../poc/test-plan.md). Equivalent scenarios must be executed across the finalist variants.

### 5. Governance controls are not yet operational

- Category weights remain workshop defaults rather than approved decision weights.
- The steering committee has not approved an evidence-coverage threshold.
- Five ADRs remain proposed.
- Risks lack likelihood, impact, residual exposure, due date, and status.
- Open questions and assumptions identify functional owners but not accountable individuals or decision deadlines.

### 6. Economics and deliverability remain open

Organization-specific TCO, staffing, support boundaries, commercial terms, migration effort, exit cost, and benefits realization are not yet complete. These are decision criteria, not post-selection implementation details.

## Required remediation

1. Approve a decision contract: sponsor, decision owner, scope, non-goals, mandatory gates, weights, coverage threshold, and dissent process.
2. Confirm organizational inputs and convert assumptions into evidence-backed facts or explicit constraints.
3. Separate the vendor-neutral target operating model from candidate deployment architectures.
4. Build a criterion-level evidence ledger linking every score to source, version, topology, test, reviewer, limitation, and date.
5. Run symmetric PoCs using equivalent workloads, policy chains, failure modes, and evidence capture.
6. Complete TCO, staffing, support, contract, migration, and exit analysis using organization-specific inputs.
7. Populate scorecards, peer-review the evidence, run sensitivity analysis, and record dissent and conditions.
8. Issue a recommendation only after mandatory gates pass and the approved coverage threshold is reached.

## Definition of decision-ready

A recommendation is decision-ready only when:

- every mandatory gate is pass, fail, or supported by an approved time-bounded exception;
- the approved weighted-evidence threshold is reached for every finalist;
- exact deployment variants have independently reviewed scorecards;
- representative security, failure, performance, operations, and migration tests have execution artifacts;
- TCO and support assumptions use actual quotes and a documented resource model;
- sensitivity testing identifies any unstable ranking;
- architecture, security, operations, commercial, and program owners sign off or record dissent;
- the final ADR records the recommendation, conditions, exceptions, exit path, and review date.

The phased plan for closing these gaps is maintained in the [repository roadmap](../docs/39-repository-roadmap.md).
