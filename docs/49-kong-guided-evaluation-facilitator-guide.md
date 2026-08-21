# Kong guided evaluation facilitator guide

| Field | Value |
|---|---|
| Artifact type | meeting-facilitation-guide |
| Meeting question | Should the decision owner approve, amend, or hold a bounded Kong foundation and the work required to prove it before production scale? |
| Decision owner | API-platform product owner with the accountable architecture, security/IAM, platform, SRE, migration, sourcing, FinOps, service-management, delivery, and assurance leads |
| Intended users | Meeting chair, presenter, facilitator, scribe, evidence steward, timekeeper, decision owners, and named technical or commercial challengers |
| Scope | Meeting routes, challenge navigation, evidence-safe responses, decision capture, parking-lot control, stop rules, and closing protocol for the 25-slide Kong guided evaluation |
| Evidence state | Facilitation guidance derived from the canonical guided evaluation and its presentation notes; no new product fact, executed result, commercial conclusion, or production authorization |
| As-of date | 2026-08-20; use the current canonical study and deck revision when facilitating |
| Next gate | Record an explicit approve, amend, or hold decision; name owners, artifacts, thresholds, reviewers, due gates, and stop rules for every authorized proof item |

## Use this guide with the presentation

This document is the **meeting control surface** for the Kong guided evaluation. It complements rather than replaces the slide-level PowerPoint notes. Every PowerPoint slide already contains `Purpose`, `Talk track`, `Ask`, `Bridge`, `Caveat`, and `Sources` blocks. Use those notes for the slide narrative; use this guide to control time, route challenges, protect the evidence boundary, and leave the room with accountable decisions.

- [Open the native 25-slide presentation](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/0)
- [Open the PowerPoint in the repository](https://github.com/tomqwu/apim/blob/main/presentations/kong-platform-journey-guided.pptx)
- [Read the canonical guided evaluation](48-kong-guided-evaluation.md)
- [Apply the evidence method](03-assessment-methodology.md)
- [Inspect the Kong platform strategy](47-kong-enterprise-platform-strategy.md)
- [Inspect the Kong option register](44-kong-multicloud-study-roadmap.md)
- [Inspect the migration strategy](35-mule-migration-strategy.md)
- [Inspect the current PoC evidence boundary](../poc/README.md)

If this guide, the PowerPoint, or the native presentation differs from a canonical study, the canonical study wins. Do not publicly link the raw supplied input; the sanitized guided evaluation preserves the admissible decision context.

## What the meeting must produce

The meeting succeeds only when it produces a decision record, not when it reaches the last slide. The chair should secure:

1. an explicit **approve, amend, or hold** answer for the bounded direction;
2. a precise statement of what is authorized now and what remains unauthorized;
3. confirmed, amended, or rejected target-model assumptions;
4. named owners for the operating boundary, permanent duties, migration safety, and six proof workstreams;
5. a closure artifact, threshold, independent reviewer, due gate, and stop rule for every material evidence gap;
6. recorded dissent and the evidence that could change the answer; and
7. an agreed next decision forum and date.

The meeting does **not** authorize critical production scale, prove a universal product ranking, convert supplied scores into observed evidence, commit synthetic roadmap dates, or declare documented capability to be executed behavior.

## Roles in the room

| Role | Responsibility during the meeting |
|---|---|
| Chair / decision owner | States the decision authority, protects non-goals, resolves or holds the decision, and reads back the final authorization. |
| Facilitator / presenter | Drives the chosen route, labels evidence states, uses challenge branches, and returns the room to slides 6 or 21. |
| Scribe | Maintains the decision, evidence-gap, action, dissent, and parking-lot ledgers in real time. |
| Evidence steward | Challenges unsupported promotion from stakeholder input or documentation to proof; confirms source, result, version, topology, and limitations. |
| Timekeeper | Enforces segment timeboxes and signals when a challenge must be assigned, parked, or moved to the appendix. |
| Accountable challengers | Security/IAM, architecture, platform/database, SRE, migration, domain, sourcing, FinOps, service-management, and assurance leads test the claims they will own. |

Before opening slide 1, name the chair, scribe, evidence steward, and timekeeper. A meeting without a decision owner should be converted to a working session and must not produce an authorization.

## Evidence vocabulary and room rules

Use the evidence ladder consistently:

| Evidence state | What it can support | What it cannot support |
|---|---|---|
| Stakeholder input | Preference, target intent, questions, and hypotheses | Independent product fit or achieved outcome |
| `E1` documented mechanism | Test design and bounded mechanism interpretation | Entitlement, configured behavior, operations, economics, or production outcome |
| `E2` attributable answer | Version-, contract-, support-, or configuration-specific closure | Repeatable behavior under the target topology |
| `E3` target-shaped lab result | Reproducible behavior inside the frozen test boundary | Representative production performance or adoption |
| `E4` representative pilot | The strongest pre-scale evidence under expected controls, load, and operations | Universal fit outside the observed boundary |

Room rules:

- Challenge claims, assumptions, thresholds, and implications—not people.
- Keep **documented**, **proposed**, **not run**, **executed**, and **accepted** visibly distinct.
- For every challenge, record what is known, what is unknown, the decision impact, the closure artifact or test, the owner, and the due gate.
- Never settle an evidence gap by changing a score in the room.
- Do not average away a failed or unknown mandatory gate with a strong weighted category.
- Appendix slides 22–25 are challenge-on-demand audit material. Do not make them the default close.

## Navigation quick reference

The native deck uses zero-based routes: presentation slide `N` is route `N−1`. Use the linked slide numbers in this guide for direct jumps. Browser Back returns to the prior discussion branch.

| Need | Control |
|---|---|
| Next / previous slide | On-screen controls, Right/Left Arrow, Page Down/Page Up, or Space/Shift+Space when focus is not inside an interactive or scrollable control |
| Jump to a phase | Select a phase in the presentation's top menu to open that phase's first slide; Browser Back returns to the exact prior discussion slide |
| Jump to an exact slide | Select a linked slide number in this guide or change the final route number |
| Inspect a dense model | Use the slide's Overview/Takeaway, Readable, and Expand controls |
| Close an expanded model | Escape or Close; focus returns to Expand |
| Exit the presentation | Escape when no modal or disclosure is open |
| Return after a challenge | Rejoin at [slide 6](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/5) for authorization or [slide 21](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/20) for outcome authority |

## Choose the meeting route

### 90-minute decision route

| Segment | Slides | Time | Required output |
|---|---:|---:|---|
| Open and target model | 1–3 | 12 min | Confirm the decision question, target inputs, and weight concerns. |
| Options and bounded decision | 4–8 | 20 min | Approve or amend the leading target, custody benchmark, true exit, and funded duties. |
| Architecture and adoption | 9–13 | 19 min | Confirm topology questions, degraded-state policy, accountable owners, and gate sequence. |
| Migration | 14–16 | 12 min | Approve the responsibility taxonomy, coexistence, route-back, and wave gates. |
| Production proof | 17–21 | 22 min | Accept the evidence baseline, fund GEP-01–06, and pre-commit possible outcomes. |
| Decision recap | Return to 6 and 21 | 5 min | Read back approve/amend/hold, owners, evidence requests, stop rules, and dissent. |
| Appendix | 22–25 | On demand | Resolve an audit challenge without displacing the decision close. |

Suggested per-slide timing is `4,4,4 / 5,3,5,3,4 / 4,4,4,4,3 / 4,4,4 / 4,6,4,4,4` minutes. Treat the appendix as branch time, not additional scheduled time.

### 60-minute working decision route

Use slides [1](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/0)–[4](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/3), [6](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/5), [8](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/7)–[10](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/9), [12](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/11)–[18](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/17), and [21](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/20). Treat slides 5, 7, 11, and 19–20 as challenge branches. Skip slides 22–25 unless challenged.

Default cadence:

- 0–5 minutes: intent and authority, slides 1–2;
- 5–13: preference and bounded decision, slides 3–4 and 6;
- 13–28: duty, topology, and ownership, slides 8–10 and 12;
- 28–39: adoption and migration, slides 13–16;
- 39–53: evidence baseline, proof scope, and decision outcomes, slides 17–18 and 21; and
- 53–60: decisions, owners, dissent, and open gates.

### 45-minute architecture route

Use slides [1](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/0), [6](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/5)–[12](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/11), and [17](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/16)–[21](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/20). Required output: disputed boundaries, owners, failure/admission questions, proof artifacts, and the authority to hold scale.

### 45-minute migration route

Use slides [1](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/0), [6](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/5), [12](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/11)–[18](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/17), [20](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/19), and [21](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/20). Required output: responsibility ownership, cohort boundaries, business probes, route-back, reconciliation, wave gates, and migration proof owners.

### 30-minute executive route

Use slides [1](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/0), [2](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/1), [4](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/3), [6](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/5), [8](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/7), [13](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/12), [17](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/16), [18](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/17), and [21](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/20). The output is authorization scope, evidence funding, decision rights, and stop rules—not technical or production approval.

### Audit challenge route

Use slides [3](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/2)–[5](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/4), then [22](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/21)–[25](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/24), and rejoin at [6](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/5). The output is a corrected or challenged input ledger, not a production conclusion.

## Challenge-handling protocol

When a challenge interrupts the planned route:

1. **Acknowledge** the concern without defending the slide.
2. **Restate the decision impact**: what answer could change if the challenge is true?
3. **Label the current evidence state**: stakeholder input, `E1`, `E2`, `E3`, `E4`, proposed, not run, or accepted.
4. **Ask what would close it**: which artifact, test, measure, threshold, and independent reviewer would change the answer?
5. **Jump to the mapped slide** and timebox the branch.
6. **Capture** the owner, due gate, stop rule, and dissent.
7. **Rejoin** at slide 6 or 21. Do not let a branch silently become the close.

| Challenge | Jump route | Evidence-safe response | Rejoin |
|---|---|---|---:|
| “This is a Kong sales deck” or “the answer was predetermined” | [1](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/0) → [2](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/1) → [4](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/3) → [5](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/4) | The supplied model explains preference; it does not provide independent proof. Record the condition or sensitivity that would reverse the direction. | 6, then 21 |
| “Why not Apigee, MuleSoft, or APIM?” | [4](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/3) → [22](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/21)–[24](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/23) | Each is a conditional operating-model counterfactual. State when it becomes stronger and convert that condition into symmetric evidence. | 6 |
| “Why self-managed rather than Konnect?” | [7](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/6) → [8](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/7) → [12](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/11) → [20](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/19) | Self-managed is a custody preference with permanent duty. Konnect is the same-vendor custody benchmark; a true non-Kong exit remains separate. | 21 |
| “Does hybrid keep running if the control plane fails?” | [9](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/8)–[11](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/10) → [17](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/16)–[19](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/18) | Cached proxying does not prove restart, clean scale, mutation, urgent revoke, reconnect, recovery, or business correctness. | 21 |
| “Terraform and decK already solve APIOps” | [10](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/9) → [18](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/17)–[19](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/18) | Tool presence is documented mechanism. The target must prove authority, deletion scope, promotion, drift, rollback, active digest, and reconciliation. | 21 |
| “Gateway authentication passed, so enterprise IAM is covered” | [10](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/9) → [12](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/11) → [18](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/17) → [19](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/18)–[21](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/20) | One authentication path does not prove organization-wide access lifecycle. Workforce, workload, consumer, and service-account inventory; join/move/leave; revoke and rotate; expiring break-glass; negative tests; attribution; owners; and independent review remain unproved. | 21 |
| “Why not migrate Mule packages directly?” | [14](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/13)–[16](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/15) | The migration unit is responsibility and state. Edge extensibility does not prove that durable or stateful business logic belongs in the gateway. | 20, then 21 |
| “The PoC already proves it” | [17](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/16) → [18](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/17) | Five local checks ran and eleven did not; the 28 atomic cases are separate and unexecuted; target E3/E4 evidence remains zero. | 19–21 |
| “Kong documents MCP, A2A, and AI routing, so AI fit is proved” | [18](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/17) → [23](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/22) | Documentation permits a test design. The separately versioned agentic study cannot inflate confidence in the core gateway decision. | 19, then 21 |
| “Kong is cheaper” or “lock-in is low” | [8](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/7) → [24](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/23) → [20](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/19) | Require quotes, labor, infrastructure, HA/DR, telemetry, support, migration, dual run, custody switch, and clean exit evidence. | 21 |
| “Can we approve production now?” | [6](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/5) → [17](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/16)–[21](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/20) | No. The admissible decision is a reversible foundation and proof programme. Critical scale requires reviewed target-shaped evidence. | 21 |

## Slide-by-slide facilitation index

Use the embedded notes for the full talk track and sources. The index below controls the discussion.

### Phase 1 — Why now

| Slide | Facilitation job and ask | Likely challenge and evidence reminder | Capture, branch, or rejoin |
|---|---|---|---|
| [1 · KGE-01](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/0) | Establish a decision-and-proof meeting. Ask whether the room accepts bounded direction plus proof as the decision question. | “Is this predetermined?” Stakeholder direction is not independent proof. | Capture decision owner and non-goals. Never skip. Disputed assumptions → 2; aligned → 6. |
| [2 · KGE-02](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/1) | Confirm or amend the stated target inputs and their owners. | “This is not our current state.” Correct: these are target inputs to confirm, not observed inventory. | Material dispute means hold scoring and create an owner/evidence action. |
| [3 · KGE-03](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/2) | Approve the weights, missing dimensions, and sensitivity work. | “The model is subjective.” It has no rubric, named scorers, confidence, or sensitivity. | Record alternate weights/ranges and dissent. Implications → 4; raw audit → 25. |

### Phase 2 — Options and decision

| Slide | Facilitation job and ask | Likely challenge and evidence reminder | Capture, branch, or rejoin |
|---|---|---|---|
| [4 · KGE-04](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/3) | Agree the business conditions under which each option becomes stronger. | “The feature list is biased or incomplete.” These are conditional archetypes, not a rank. | Convert product debate into symmetric evidence; appendix → 22–24; return → 6. |
| [5 · KGE-05](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/4) | Treat the corrected score as directional preference input only. | “93 proves fit.” Correct arithmetic is 93, 85.5, and 77, but confidence and sensitivity are missing. | Record acceptance of arithmetic and limits. Audit → 25; decision → 6. |
| [6 · KGE-06](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/5) | Decide separately on `KP-SMH1`, one reversible foundation, GEP-01–06, custody/exit benchmarks, and the block on critical scale. | “Why choose before PoC?” The authorization is foundation plus proof, not production. | Record approve/amend/hold for every row and dissent. Return here at close. |
| [7 · KGE-07](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/6) | Confirm self-managed lead, Konnect custody benchmark, and a true non-Kong exit as distinct boundaries. | “Konnect is the exit.” It is a same-vendor custody switch, not platform exit. | Name exact-option, custody-benchmark, and exit owners. Continue → 8. |
| [8 · KGE-08](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/7) | Confirm permanent control-plane, database, PKI, release, restore, support, and on-call ownership. | “Cached DP continuity removes the duty.” It is narrower than mutation, recovery, and 24×7 ownership. | Capture RACI, capacity, sourcing, and TCO gaps. No accountable owner = HOLD. |

### Phase 3 — Architecture and adoption

| Slide | Facilitation job and ask | Likely challenge and evidence reminder | Capture, branch, or rejoin |
|---|---|---|---|
| [9 · KGE-09](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/8) | Validate control zone, DP cells, request lanes, evidence paths, network, and sovereignty boundaries. | “The diagram oversimplifies HA or database behavior.” It is an E1-informed discussion view; inspect canonical `KPS-1`. | Capture topology disputes. Do not infer a DP database path or uniform arrow semantics. Continue → 10. |
| [10 · KGE-10](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/9) | Separate configuration, trust, request, business, and evidence paths. Ask which path governs service admission. | “Proxy success proves availability.” Gateway uptime is not the API or business SLO. | Capture probes, state identity, trust age, backend readiness, and owners. Resilience → 11 or 17–19. |
| [11 · KGE-11](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/10) | Assign continue, hold, quarantine, reconcile, override, and response authority. | “Kong automates these states.” They are a proposed organizational policy around documented behavior. | Capture state owners, objectives, break-glass, and reconciliation. Continue → 12. |
| [12 · KGE-12](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/11) | Name the teams and capacity for platform lifecycle, domain correctness, security admission, reliability, and escalation. | “The vendor or a ticket queue owns it.” Support does not transfer service accountability. | Capture RACI and staffing exceptions. Unnamed teams or heroics = HOLD. |
| [13 · KGE-13](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/12) | Approve the KP0–KP5 gate sequence and evidence needed to leave each phase. | “Are these dates committed?” The overlapping 0–18 month windows are scenario assumptions. | Replace date debate with entry/exit evidence. Migration → 14; proof-first → 18. |

### Phase 4 — Migration

| Slide | Facilitation job and ask | Likely challenge and evidence reminder | Capture, branch, or rejoin |
|---|---|---|---|
| [14 · KGE-14](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/13) | Adopt the responsibility and durable-state taxonomy. | “Move Mule packages to Kong.” Only gateway policy is unambiguous; facade is conditional and other duties need owned destinations. | Name inventory, classification, destination, and state-authority owners. Continue → 15. |
| [15 · KGE-15](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/14) | Require bounded cohorts, parity probes, reconciliation, and route-back. | “Dual run is too costly” or “the edge must already be Kong.” The stable-edge pattern is product-neutral and safety-driven. | Capture cohort, business-verifier, route-back, and evidence-retention owners. Continue → 16. |
| [16 · KGE-16](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/15) | Agree evidence entry and exit controls for M0–M5. | “Give counts and committed dates.” Elapsed time and object count do not prove parity or dependency zero. | Capture per-wave evidence and retirement authority. Unknown state or irreversible cutover = HOLD. |

### Phase 5 — Production proof

| Slide | Facilitation job and ask | Likely challenge and evidence reminder | Capture, branch, or rejoin |
|---|---|---|---|
| [17 · KGE-17](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/16) | Establish the exact current evidence baseline. | “5/16 means 31% ready” or “28 means more completed proof.” The 16 register and 28 atomic cases are non-additive; target E3/E4 is zero. | Capture agreement or disputed result IDs. Continue → 18. |
| [18 · KGE-18](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/17) | Authorize GEP-01–06 with owner, environment/BOM, measure, threshold, raw artifact, reviewer, and stop rule. | “Documentation already proves 3.14” or “AI should decide.” All workstreams are not run; exact version/entitlement/support must be frozen; agentic proof stays separate. | Missing threshold, artifact, reviewer, or stop rule = HOLD. AI branch → 23; rejoin → 19. |
| [19 · KGE-19](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/18) | Agree thresholds, artifacts, cadence, and owners for KO-1–KO-5. | “The mechanism should be enough.” These are proposed target forms, not achieved results. | Capture missing thresholds and artifact schemas. Continue → 20. |
| [20 · KGE-20](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/19) | Agree KO-6–KO-11 and identify the most likely scale blocker. | “Technical health is enough.” Admission also includes evidence safety, adoption, toil, exit, and estate truth. | Capture likely blocker, owner, data, cadence, cost model, and exit rehearsal. Continue → 21. |
| [21 · KGE-21](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/20) | Pre-commit scale, narrow, switch custody, exit, and hold authority. | “The selection is already fixed.” No outcome is preselected; negative evidence must change scope or direction. | Capture decision rights and non-waivable gates. Return to 6 and close. |

### Phase 6 — Audit appendix

| Slide | Facilitation job and ask | Likely challenge and evidence reminder | Capture, branch, or rejoin |
|---|---|---|---|
| [22 · KGE-22](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/21) | Turn disputed architecture/delivery labels into proof questions. | Supplied labels are edition- and version-sensitive and unverified. | Add evidence backlog; do not rescore in the room. Rejoin → 4 or 6. |
| [23 · KGE-23](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/22) | Assign owners and artifacts for management, developer-experience, customization, and AI claims. | AI and product claims change with edition, version, topology, and date. | Capture exact use cases and version/plugin matrix. Workstream → 18; economics → 24. |
| [24 · KGE-24](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/23) | Assign TCO, custody, support, migration, and exit evidence. | “License price is TCO” or “low lock-in is obvious.” No commercial or clean-exit proof exists. | Name FinOps/sourcing owner and assumptions. Outcomes → 21; scoring → 25. |
| [25 · KGE-25](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/24) | Decide whether the scorecard remains a governance input and audit its arithmetic. | Corrected arithmetic does not create a rubric, confidence model, sensitivity, or benchmark. | Capture scorer, rubric, confidence, sensitivity, and sign-off. Never finish here; return → 6 or 21. |

## Decision, evidence, and parking-lot ledgers

Keep one visible ledger during the meeting. Do not hide unresolved challenge work in free-form notes.

| Ledger field | Required content |
|---|---|
| Identity | Stable ID, slide, and record type: decision, evidence gap, assumption, dissent, or action. |
| Statement | The exact decision or challenge in neutral language. |
| Evidence | Current state and source or result boundary. |
| Impact | What authorization, scope, or outcome changes if the item is true or remains unknown. |
| Closure | Artifact or test, measure, pre-approved threshold, and independent reviewer. |
| Accountability | Owner, due gate or date, and escalation forum. |
| Disposition | Open, approved, amended, held, closed, or resulting scope: scale, narrow, switch, exit, or hold. |

Seed the ledger with four records: `D-001` for the bounded decision on slide 6; `E-001` for a not-run workstream on slide 18; `A-001` for a target or timeline assumption on slide 13; and `X-001` for a decision-changing counter-hypothesis on slide 21.

Parking-lot minimum fields:

| Field | Required content |
|---|---|
| Issue and impact | What is disputed and why it matters to the decision. |
| Navigation | Mapped slide or source document. |
| Closure | Requested artifact or test and the evidence state it must reach. |
| Accountability | Owner and due date or gate. |
| Re-entry | Slide 6 for authorization or slide 21 for evidence consequences. |

An item belongs in the parking lot only when it has an owner and re-entry condition. Otherwise it remains an unresolved decision blocker.

## Language guardrails

Prefer:

- “The supplied evaluation states…”
- “The repository proposes…”
- “Current official documentation describes…”
- “The local baseline shows…”
- “This has not been run in the frozen target…”
- “The decision requested today is…”
- “This evidence would cause us to narrow, switch, exit, or hold…”

Avoid:

- “Kong is proven best.”
- “Hybrid guarantees uptime.”
- “A score of 93 means 93% fit.”
- “Five of sixteen means 31% ready.”
- “The 28 cases are additional completed tests.”
- “Konnect is vendor exit.”
- “Mule packages all move to Kong.”
- “The roadmap dates are commitments.”
- “The documented feature proves our configured behavior.”
- Any Kong Enterprise 3.14 claim that omits the exact patch, entitlement, plugin, topology, support, and as-of boundary required by the decision.

## Stop and hold rules

Stop the decision or record **HOLD** when:

- the target assumptions are materially disputed and have no owner or closure evidence—do not continue to weights or scoring;
- self-managed control has no funded, accountable owner for control-plane, database, PKI, release, restore, observability, support, or on-call duties;
- the exact target option, environment, measure, threshold, artifact, reviewer, or stop rule is not frozen—do not call the work proof;
- a migration cohort lacks business parity, durable-state authority, reconciliation, or route-back;
- an unknown or failed mandatory gate is being offset by a weighted score;
- the evidence does not preserve failed runs, gaps, dissent, and limitations; or
- negative evidence is not permitted to narrow, switch custody, exit, or hold.

## Close the meeting

The chair should read back only:

1. what is approved now;
2. what remains explicitly unauthorized;
3. which assumptions were amended or rejected;
4. which evidence requests, owners, reviewers, thresholds, due gates, and stop rules were created; and
5. whether the next state is proceed, amend, or hold.

Recommended close:

> We are approving a reversible direction and the work required to test it. Critical production scale remains blocked until reviewed target-shaped evidence changes that status.

End on [slide 6](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/5) when the decision is about authorization, or [slide 21](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/20) when it is about evidence consequences. Never end on a raw score or appendix label.

## References and limitations

The slide-level PowerPoint notes contain the point-of-use purpose, talk track, ask, bridge, caveat, and source list. This guide intentionally does not duplicate those 25 source blocks. Its canonical references are:

- [Kong guided evaluation](48-kong-guided-evaluation.md)
- [Assessment methodology](03-assessment-methodology.md)
- [Kong enterprise platform deployment strategy](47-kong-enterprise-platform-strategy.md)
- [Kong multicloud study roadmap](44-kong-multicloud-study-roadmap.md)
- [Mule migration strategy](35-mule-migration-strategy.md)
- [Current PoC register and evidence boundary](../poc/README.md)
- [Presentation artifact contract](../presentations/README.md)

This is public-safe facilitation guidance. It contains no meeting minutes, named-person assignment, commercial term, private topology, or observed production outcome. Store restricted decisions and evidence in the approved private system; publish only sanitized, authorized conclusions through the repository workflow.
