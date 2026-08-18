# Principal consultant methodology and decision-assurance review

- Review date: 2026-08-18
- Scope: repository structure, assessment method, evidence chain, documents, architecture, PoC material, audience briefings, charts, and presentation
- Evidence basis: committed repository content only; no stakeholder interviews, vendor briefings, commercial quotes, or organization validation were available
- Review stance: principal decision-assurance challenge of the repository evidence; no platform selection is approved by this report and organizational acceptance remains external

## Executive verdict

The repository is a strong assessment scaffold and early evidence baseline. It is not yet a completed comparative platform assessment.

| Dimension | Maturity | Finding |
|---|---|---|
| Assessment framework | Strong scaffold | Strong gates, evidence levels, variant separation, unknown handling, falsification discipline, and a defined public/restricted evidence boundary |
| Evidence completion | Initial | All 120 criteria remain unknown; no bounded archetype has a resolved Gate-1 bill of materials or populated criterion-level scorecard |
| Comparative integrity | Developing | Deep symmetric dossiers and protocols now exist, but bounded archetypes are not yet resolved options and no equivalent E3 result exists |
| Governance readiness | Developing | Assumptions, risks, questions, weights, thresholds, and ADRs are visible but not operationally closed |
| Roadmap readiness | Strong scaffold | Repository and organization-delivery roadmaps now have explicit gates and decision rights; named assignments, capacity, dependencies, and dates remain to be mobilized |
| Audience communication | Strong scaffold | Six role-specific briefings sequence the same canonical evidence for executives, directors, architects, developers, DevOps/SRE, and platform teams |
| Executive decision readiness | Not ready | The current direction is appropriately provisional; a final recommendation would be premature |

The maturity labels are deliberately qualitative: **Initial** means decision evidence is largely uncollected; **Developing** means material controls exist but are not operationally complete; **Strong scaffold** means the method is well structured but not yet executed; and **Not ready** means the stated decision gates are unmet. These labels are not vendor or product scores.

Current maturity is **structured assessment / evidence collection**. The appropriate steering decision is to approve evidence closure, not to select a product.

## Principal recommendation

| Decision | Principal recommendation | Status | Exit evidence |
|---|---|---|---|
| Evidence-closure programme | Approve the prerequisite-driven, stage-gated programme and the capacity to execute it; do not promise Gate 2 in 90 days | Approve Gate 0 only | Decision contract, accountable roles, calibrated inputs, approved environments/vendor access, capacity-loaded action register and evidence calendar |
| Conditional product/platform selection | Defer any vendor selection, purchase, or migration commitment | Not ready | Gate 2: mandatory gates disposed, approved evidence/category threshold met, resolved-option ledger reviewed, symmetric E3 proof, TCO/support, bounds, maximum regret and sensitivity complete |
| Sequencing hypotheses | Keep Kong and every alternative as falsifiable hypotheses; confer no execution priority before the common E1/E2 screen and option-resolution gate | Conditional | Exact bill of materials, equivalent category coverage and mandatory dispositions support finalist status |
| Comparative benchmarks | Retain Azure APIM managed/self-hosted and Apigee X/Hybrid through the approved down-select | Required | Equivalent claims, candidate views, vendor confirmations, and symmetric finalist tests |
| Current-state baseline | Retain MuleSoft as the comparison and migration baseline, not the default target | Required | Workload inventory, capability decomposition, run-cost, migration effort, and dependency evidence |

### Steering ask

1. Approve the evidence-closure programme through Gate 2; do **not** approve a product selection.
2. Assign accountable public roles or anonymized owner IDs and maintain the named-person/capacity map in restricted programme records.
3. Authorize the organization inputs, vendor access, environments, commercial work, and independent reviewers required for comparable evidence.
4. Return at Gate 1 after the E1/E2 screen to approve the evidence-led finalist set and symmetric E3 PoC scope.

Explicitly excluded from this approval are vendor award, production platform build, full migration funding, contract commitment, and any claim that a local functional baseline proves enterprise operability.

```mermaid
flowchart TB
  G0{"Gate 0<br/>approve decision contract"} --> S["E1/E2 screen<br/>seven bounded archetypes"] --> O["Resolve edition · version<br/>topology · entitlement · support"] --> G1{"Gate 1<br/>approve finalists"}
  G1 --> P["Symmetric E3 PoC + TCO<br/>approved finalists"] --> G2{"Gate 2<br/>conditional selection-ready?"}
  G2 -->|"yes"| R["Conditional selection ADR<br/>conditions, dissent, exit path"] --> F["Platform foundation"] --> G3{"Gate 3<br/>production-pilot ready?"}
  G3 -->|"yes"| E4["Representative E4 production pilots"] --> G4{"Gate 4<br/>scale-ready?"}
  G4 -->|"yes"| M["Pattern-based migration factory"]
  G2 -->|"no"| X["Targeted evidence sprint,<br/>remove candidate, or stop"]
  X --> G2
  G3 -->|"no"| F
  G4 -->|"no"| E4
```

The quantitative evidence snapshot and Markdown-renderable charts are maintained in [evidence-state.md](evidence-state.md); the same canonical datasets drive the site Visual Atlas.

## Review method

Every material conclusion should preserve this traceable chain:

> Business outcome → requirement → mandatory gate → evidence → observable test → score → implication → decision

The review applies three lenses:

1. **Repository assurance:** completeness, provenance, freshness, reproducibility, navigation, visual parity, and public-safe content.
2. **Decision assurance:** scope, alternatives, approved gates, evidence quality, comparative fairness, economics, sensitivity, risk, and decision rights.
3. **Role-specific communication:** decision requested, appropriate level of detail, trade-offs, uncertainty, risks, roadmap, and accountable next actions for each audience.

A conclusion remains provisional whenever one of those links is missing.

## What is strong

- Bounded deployment archetypes are kept separate, and the [assessment methodology](../docs/03-assessment-methodology.md) prohibits scoring until each Gate-1 option definition is exact.
- Mandatory gates cannot be averaged away, and unknown evidence is never treated as pass in the [scoring guide](../decision-matrix/scoring-guide.md).
- Evidence confidence progresses from assertion to official documentation, vendor confirmation, repeatable lab, and representative pilot in the [assessment methodology](../docs/03-assessment-methodology.md).
- The [Kong-first hypothesis](../docs/04-kong-first-hypothesis.md) now states that current evidence does not justify execution priority, includes counter-hypotheses, and has falsification conditions.
- The [executive summary](../docs/00-executive-summary.md) distinguishes evidence closure, named sequencing hypotheses, finalist proof, and product selection.
- The [architecture catalog](../architecture/README.md) designates one vendor-neutral logical target and makes candidate-specific views visibly provisional.
- The [audience guide](../docs/40-audience-guide.md) gives six roles different decisions, reading sequences, visuals, and meeting closes without duplicating the underlying evidence.
- The PoC documentation separates 16 aggregate status-register items from 28 atomic decision-grade real-world, portal and observability cases, and does not count protocol depth as execution in [poc/README.md](../poc/README.md).
- Forty-one principal studies now enforce answer-first framing, mechanism/failure depth, counter-evidence, proof plans and inline interpreted figures; this is content maturity, not candidate evidence. The canonical P1–P10 industry-problem taxonomy structures reusable proof, while the Kong multicloud roadmap remains a candidate-specific sequencing hypothesis under the same gates.
- The [citation-coverage report](source-coverage.md) keeps contextual official links visibly outside the score-capable source/finding chain until promoted.

## Priority findings

| Priority | Finding | Required disposition |
|---|---|---|
| P0 | The 120 current `acceptance_test` cells are discovery prompts rather than measurable acceptance conditions | Refine the 30 mandatory gates first with measure, threshold, scenario, evidence level, decision owner, and exception rule before scoring |
| P0 | Seven bounded archetypes do not yet have resolved Gate-1 bills of materials or a canonical criterion-by-option evidence ledger | Resolve the option fields, populate the [ledger template](../decision-matrix/evidence-ledger-template.csv), and generate scorecards/charts from it |
| P0 | No candidate has equivalent observed E3 evidence, despite deep symmetric E1 research and protocols | Complete the common E1/E2 screen, approve finalists without brand priority, and execute the 28 atomic E3 cases symmetrically |
| P0 | Organization-specific inputs, TCO, support, staffing, migration, and exit evidence are absent | Keep selection deferred and complete the restricted evidence workstream before Gate 2 |
| P1 | The roadmaps define roles and gates but not actual capacity, dependencies, dates, or accepted exit artifacts | Mobilize the [action register](../templates/assessment-action-register-template.csv) under an accountable decision owner |
| P1 | Twenty RE-1 risks have scenario ratings and 36 questions carry owner/due-gate/impact fields, but organization likelihood/impact acceptance, assumptions, ADRs and questions remain unclosed | Calibrate and approve risk scales and private named ownership; publish no organization heatmap until observed inputs exist |
| P1 | The corpus contains 200 unique contextual external citations outside the authoritative source register | Promote only decision-bearing claims into `sources.csv` plus a mapped finding; keep the generated coverage ledger current and contextual links non-scoring |

## Material gaps

### 1. Decision evidence and acceptance conditions are incomplete

All 120 criteria are currently `unknown`, including 30 mandatory gates. No bounded archetype has closed its option-resolution record or has a populated criterion-level scorecard. The existing acceptance text restates each criterion and is not yet a measurable pass/fail condition. A candidate ranking must not be published until the gates are operational and the agreed evidence/category threshold, common-evidence, bounds and maximum-regret rules are met.

### 2. The resolved-option evidence model is not populated

The method keeps seven bounded archetypes separate, but they are not exact until edition, version, topology, region, entitlement, plugin and support fields close. The current Markdown scorecards remain unscored placeholders. Use a canonical ledger keyed by `criterion_id + option_id`; preserve outcome, claim, source/version, topology, entitlement, test, artifact, reviewer role, limitation, freshness, implication, exception, and decision state.

### 3. Comparative research is deep; decision proof is still absent

The logical target is vendor-neutral, and Kong, APIM, Apigee, MuleSoft and secondary-product studies now use deep, mechanism-level dossiers, bounded archetypes, failure analysis, inline figures and Gate-1 blockers. That symmetry is E1 research design, not comparative execution. Exact physical bills of materials, organization topology, entitlement/support facts and E3 result bundles remain open.

The authoritative register contains 40 official sources: 28 source IDs are used directly by 24 findings and 12 remain unused there. The wider article corpus contains 236 unique external citations; 36 resolve to registered URLs and 200 remain explicitly contextual under the generated coverage ledger. Five of 16 aggregate PoC register items have automated baseline evidence and 11 remain not run. The 28 atomic real-world, portal and observability protocol cases are designs, not observed results; they must be executed across approved finalist options.

### 4. Organizational facts remain assumptions

All ten entries in the [assumption register](../docs/02-current-state-assumptions.md) remain open. Each needs an accountable public role or anonymized owner ID, a restricted named owner, validation evidence, target gate/date, and explicit decision impact.

### 5. Governance controls are not operational

- Category weights remain workshop defaults rather than approved decision weights.
- The steering committee has not approved an evidence-coverage threshold.
- Five ADRs remain proposed.
- Twenty risks carry RE-1 scenario likelihood/impact/exposure and owner fields, but organization calibration, acceptance, due dates and trend remain unapproved.
- Thirty-six open questions carry functional owners, due gates and decision consequences; accountable named ownership, target dates and closure evidence remain unaccepted.

### 6. Economics and deliverability remain open

Organization-specific TCO, staffing, support boundaries, commercial terms, migration effort, exit cost, and benefits realization are not complete. These are decision criteria, not post-selection implementation details.

### 7. Public/restricted evidence handling is defined but not implemented

The method now defines what may be public. A restricted evidence store, access model, retention rules, named-person mapping, non-sensitive reference convention, and review process still need to be established before quotes, NDA responses, organization topology, security findings, or raw logs are collected.

### 8. Roadmap accountability must be mobilized

The [repository roadmap](../docs/39-repository-roadmap.md) and [delivery roadmap](../docs/36-implementation-roadmap.md) now define gates, roles, and exit evidence. They remain planning scaffolds until capacity, dependencies, target dates, accountable owner IDs, approvers, and accepted artifacts are entered in the action register.

## Required remediation

1. Approve the decision contract: sponsor, decision owner, scope, non-goals, gates, weights, coverage threshold, review calendar, public/restricted boundary, dissent, and exception process.
2. Make the 30 mandatory gates observable and testable before refining lower-priority weighted criteria.
3. Resolve Gate-1 option definitions, populate the criterion-by-option evidence ledger, and generate common-evidence/category coverage, bounds, maximum-regret and sensitivity views from it.
4. Confirm organization inputs and convert assumptions into evidenced facts or explicit constraints.
5. Complete exact candidate physical bills of materials and the equivalent E1/E2 screen before selecting finalists.
6. Run the hard-gated 28-case finalist protocols using equivalent workloads, policy chains, identity/PKI controls, failure modes, validity rules and evidence capture.
7. Complete TCO, staffing, support, contract, migration, benefits, and exit analysis with organization-specific restricted inputs.
8. Rate and treat risks using approved scales; peer-review evidence and record dissent, conditions, and exceptions.
9. Populate role/owner ID, capacity, dependency, date/gate, status, exit evidence, approver, and decision impact in the action register.
10. Issue a conditional selection only after Gate 2; admit production pilots only after Gate 3; authorize migration at scale only after representative E4 evidence passes Gate 4.

## Definition of decision-ready

### Conditional selection-ready — Gate 2

A conditional selection recommendation is decision-ready only when:

- every mandatory gate is pass, fail, or supported by an approved time-bounded exception;
- the approved weighted-evidence and category thresholds are reached for every finalist;
- exact resolved options have independently reviewed scorecards generated from the canonical ledger;
- common-evidence comparison, full-weight bounds and maximum regret do not expose an unresolved rank reversal;
- representative E3 security, failure, performance, API operations, observability, and migration-pattern tests have execution artifacts;
- TCO and support assumptions use actual quotes and a documented resource model;
- sensitivity testing identifies any unstable ranking;
- architecture, security, operations, commercial, and program owners sign off or record dissent;
- the selection ADR records the recommendation, conditions, exceptions, exit path, and review date.

### Production scale-ready — Gate 4

Authorization to scale migrations additionally requires:

- the selected platform foundation has passed Gate 3 production-readiness review;
- at least two representative E4 production pilots cover gateway-dominant and integration-dominant workload patterns;
- measured SLO, security, operability, support demand, cost, rollback, and reconciliation evidence meets approved thresholds;
- platform, domain, security, SRE, commercial, and programme owners accept the migration patterns, capacity, residual risks, and benefits baseline.

Re-run this review at every roadmap gate, before conditional selection, and before Gate 4 authorizes migration at scale.
