# Kong guided evaluation facilitator guide

| Field | Value |
|---|---|
| Artifact type | meeting-facilitation-guide |
| Meeting question | Should the decision owner approve, amend, or hold a bounded Kong foundation and the work required to prove it before production scale? |
| Decision owner | API-platform product owner with the accountable architecture, security/IAM, platform, SRE, migration, sourcing, FinOps, service-management, delivery, and assurance leads |
| Intended users | Meeting chair, presenter, facilitator, scribe, evidence steward, timekeeper, decision owners, and named technical or commercial challengers |
| Scope | Complete speaker notes for all 25 slides; meeting routes; bounded side talks; challenge navigation; evidence-safe responses; decision capture; parking-lot control; stop rules; and closing protocol for the Kong guided evaluation |
| Evidence state | Facilitation guidance derived from the canonical guided evaluation and its presentation notes; no new product fact, executed result, commercial conclusion, or production authorization |
| As-of date | 2026-08-20; use the current canonical study and deck revision when facilitating |
| Next gate | Record an explicit approve, amend, or hold decision; name owners, artifacts, thresholds, reviewers, due gates, and stop rules for every authorized proof item |

## Use this guide with the presentation

This document is the **complete canonical facilitation and speaker-notes companion** for the Kong guided evaluation. It contains the full `Purpose`, `Talk track`, `Ask`, `Bridge`, `Caveat`, and `Sources` blocks for every slide, plus the side talks, evidence-safe responses, follow-up probes, decision impacts, capture instructions, branches, rejoin points, and hold rules needed to run the meeting. The PowerPoint notes remain a synchronized concise projection; use this Markdown when preparing, presenting, navigating challenges, or handing the meeting to another facilitator.

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

Use the index below as the compact discussion control. The complete point-of-use notes and side talks follow it.

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

## Complete speaker notes and side talks

These sections are the complete point-of-use speaker notes. Read the six synchronized note blocks as the planned narrative, then use the side-talk fields only when the room raises the mapped challenge. A branch must return to its named rejoin slide; an issue may enter the parking lot only with a decision impact, owner, closure evidence, and re-entry condition.

### Phase 1 — Why now

#### KGE-01 · API management from platform choice to production proof

- **Phase:** `KGE-P1 — Why now`
- **Native route:** [Open slide 1](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/0) (`#/present/kong-platform-journey-guided/0`)
- **Timebox:** 4 minutes
- **Evidence state:** Guided decision brief
- **Meeting job:** Establish a decision-and-proof meeting and secure agreement on the bounded decision question.

##### Purpose

Set the scope: this is a guided decision and proof journey, not a product marketing deck.

##### Talk track

We start from the stated target operating model, explain why Kong leads under that model, and then make the ownership, migration, evidence and exit gates explicit.

##### Ask

Align on the decision question: approve a bounded Kong direction and proof programme—not critical production scale.

##### Bridge

First, make the target operating model visible because it drives the scoring and the platform fit.

##### Caveat

The sanitized supplied evaluation is stakeholder input. Its ratings and recommendation are not independent comparative proof.

##### Sources

- Canonical decision content: [Kong guided evaluation](48-kong-guided-evaluation.md).
- Supporting repository interpretation: [Kong enterprise platform deployment strategy](47-kong-enterprise-platform-strategy.md) and [Mule migration strategy](35-mule-migration-strategy.md).
- Official documented mechanism (`E1` only): [Kong deployment topologies](https://developer.konghq.com/gateway/deployment-topologies/) and [Kong hybrid mode](https://developer.konghq.com/gateway/hybrid-mode/).

##### Listen for

“This is a Kong sales deck,” “the answer is predetermined,” or a request to approve production before the evidence programme.

##### Evidence-safe response

Kong is the leading direction only under the stated priorities. The room can approve, amend, or hold that direction, and critical production scale is explicitly outside today’s authorization.

##### Follow-up probe

What condition, counter-evidence, or target-model change would cause you to amend or hold the direction?

##### Decision impact

If the room does not accept a bounded direction-plus-proof question, the remainder becomes a working session and cannot produce authorization.

##### Capture

Record the decision owner, decision authority, non-goals, explicitly unauthorized scope, and any decision-changing condition.

##### Branch/rejoin

For a bias challenge, branch to slides 2, 4, and 5; for a production-approval challenge, branch to slides 17–21. Rejoin at slide 6 for authorization or slide 21 for evidence consequences.

##### HOLD/park

HOLD if no decision owner is present. Park a bias challenge only when it has a named evidence request and re-entry at slide 6.

#### KGE-02 · The operating model—not the feature list—drives the decision

- **Phase:** `KGE-P1 — Why now`
- **Native route:** [Open slide 2](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/1) (`#/present/kong-platform-journey-guided/1`)
- **Timebox:** 4 minutes
- **Evidence state:** Stakeholder input
- **Meeting job:** Confirm, amend, or reject the stated target inputs and name accountable owners.

##### Purpose

Explain why the same product can be a good or poor choice depending on the target operating model.

##### Talk track

The supplied assessment favors Kubernetes, GitOps, platform engineering, self-service, observability and emerging AI traffic governance. Those priorities explain why Kong scores well. They should be confirmed with accountable owners.

##### Ask

Confirm or amend these target-state assumptions before using them as decision weights.

##### Bridge

The next slide shows how those priorities were encoded in the supplied scorecard.

##### Caveat

These are stakeholder-stated objectives; the document does not provide a verified workload inventory or current-state baseline.

##### Sources

- Canonical target-input record: [Kong guided evaluation — Stated target operating model](48-kong-guided-evaluation.md#stated-target-operating-model).
- Official contextual mechanism (`E1` only): [Kong deployment topologies](https://developer.konghq.com/gateway/deployment-topologies/) and [Kong hybrid mode](https://developer.konghq.com/gateway/hybrid-mode/).

##### Listen for

“This is not our current state,” “these priorities are incomplete,” or unowned statements presented as enterprise facts.

##### Evidence-safe response

Correct: the slide states target inputs to confirm, not an observed estate inventory. Amend or reject any input that lacks accountable sponsorship.

##### Follow-up probe

Which input changes, who owns it, and what observed inventory would confirm that it is a viable target rather than an aspiration?

##### Decision impact

A material target-model dispute changes the weights and can reverse the apparent platform direction.

##### Capture

For each disputed input, record confirm/amend/reject, owner, observed evidence needed, and due gate.

##### Branch/rejoin

Continue to slide 3 for weighting implications. If the dispute invalidates the decision basis, return to slide 6 only after an owner and closure action are recorded.

##### HOLD/park

HOLD scoring when a material target input is disputed without an owner. Park only bounded inventory work with a due gate and slide-6 re-entry.

#### KGE-03 · The scorecard favors cloud-native delivery

- **Phase:** `KGE-P1 — Why now`
- **Native route:** [Open slide 3](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/2) (`#/present/kong-platform-journey-guided/2`)
- **Timebox:** 4 minutes
- **Evidence state:** Stakeholder input
- **Meeting job:** Approve the weight model’s use, missing dimensions, sensitivity ranges, and dissent record.

##### Purpose

Make the decision model transparent before showing a result.

##### Talk track

Eight weighted categories sum to 100%. Developer experience and multicloud appear in the narrative but not as distinct weights. Migration effort and operating labor are also absent, so the score is a directional preference model, not a full business case.

##### Ask

Confirm the weights and add sensitivity ranges before using them as an approval mechanism.

##### Bridge

Now compare operating-model fit rather than treating these products as interchangeable feature bundles.

##### Caveat

Ratings lack a documented rubric, named scorers, evidence confidence, product edition and sensitivity analysis.

##### Sources

- Canonical weighting record: [Kong guided evaluation — Supplied weighting model](48-kong-guided-evaluation.md#supplied-weighting-model).
- Official contextual mechanism (`E1` only): [Kong deployment topologies](https://developer.konghq.com/gateway/deployment-topologies/) and [Kong hybrid mode](https://developer.konghq.com/gateway/hybrid-mode/).

##### Listen for

“The model is subjective,” “Kubernetes and GitOps bias the answer,” or a demand to use the displayed weights without sensitivity.

##### Evidence-safe response

The weights are stakeholder choices. Kubernetes plus GitOps carrying 35% explains much of the preference, but it does not establish confidence, economics, migration feasibility, or production fit.

##### Follow-up probe

Which missing dimension or plausible weight range could change the direction, and who will approve that sensitivity?

##### Decision impact

If an approved plausible sensitivity reverses the result, the direction cannot be treated as stable without an explicit business choice.

##### Capture

Record weights, ranges, missing dimensions, scorers, confidence rules, dissent, and the sensitivity owner.

##### Branch/rejoin

Branch to slide 5 for score implications or slide 25 for the raw audit. Rejoin at slide 6.

##### HOLD/park

HOLD score-based authorization when material weights, scorers, or sensitivity remain unowned. Park detailed recalculation only with an approved rubric and slide-6 re-entry.

### Phase 2 — Options and decision

#### KGE-04 · Each contender optimizes a different operating model

- **Phase:** `KGE-P2 — Options and decision`
- **Native route:** [Open slide 4](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/3) (`#/present/kong-platform-journey-guided/3`)
- **Timebox:** 5 minutes
- **Evidence state:** Conditional hypothesis
- **Meeting job:** Agree the conditions under which each option becomes stronger and convert product debate into symmetric proof questions.

##### Purpose

Reframe the product comparison as conditional operating-model choices.

##### Talk track

Kong is strongest when Kubernetes, GitOps and platform ownership dominate. Apigee is plausible when external API product management dominates. MuleSoft is plausible when Anypoint remains strategic. Azure APIM remains a no-build benchmark if Azure consolidation dominates.

##### Ask

Agree on the counterfactuals that would change the platform direction.

##### Bridge

The supplied scorecard encodes one of these preferences. We correct its arithmetic on the next slide.

##### Caveat

The qualitative ratings and cost/lock-in labels preserved in the sanitized supplied evaluation are stakeholder assessments, not independently verified facts.

##### Sources

- Canonical option hypotheses: [Kong guided evaluation — Conditional option archetypes](48-kong-guided-evaluation.md#conditional-option-archetypes).
- Official documented mechanisms (`E1` only): [Kong deployment topologies](https://developer.konghq.com/gateway/deployment-topologies/), [Apigee hybrid 1.16](https://docs.cloud.google.com/apigee/docs/hybrid/v1.16/what-is-hybrid), [MuleSoft Omni Gateway](https://docs.mulesoft.com/gateway/latest/), and [Azure API Management self-hosted gateway](https://learn.microsoft.com/en-us/azure/api-management/self-hosted-gateway-overview).

##### Listen for

“Why not Apigee, MuleSoft, or APIM?” or a feature-list objection that attempts to settle the comparison through undocumented labels.

##### Evidence-safe response

Each contender is a conditional operating-model counterfactual, not a universal rank. State the business condition that makes it stronger and test that condition symmetrically.

##### Follow-up probe

Which exact option, edition, topology, use case, and outcome would change the direction if proved?

##### Decision impact

A credible counterfactual can narrow the Kong scope, switch custody, or reopen option selection.

##### Capture

Record the reversal condition, exact option boundary, evidence request, owner, reviewer, and due gate.

##### Branch/rejoin

Branch to slides 22–24 for supplied comparison inputs. Rejoin at slide 6; do not close in the appendix.

##### HOLD/park

HOLD if an agreed mandatory condition favors another option and no comparative proof is authorized. Park feature detail only as a symmetric evidence request.

#### KGE-05 · The supplied model puts Kong first—before evidence confidence is applied

- **Phase:** `KGE-P2 — Options and decision`
- **Native route:** [Open slide 5](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/4) (`#/present/kong-platform-journey-guided/4`)
- **Timebox:** 3 minutes
- **Evidence state:** Stakeholder input
- **Meeting job:** Accept the corrected arithmetic while limiting the score to directional preference input.

##### Purpose

Use the scorecard transparently without overstating its evidentiary value.

##### Talk track

The Kong total is 93. The same formula yields 85.5 for Apigee and 77 for MuleSoft, rather than 87 and 78 in the source results table. The ordering is unchanged, but the arithmetic and evidence limits matter.

##### Ask

Treat the result as a directional preference to test, not a selection proof.

##### Bridge

We can now state a bounded decision that preserves falsifiability.

##### Caveat

No sensitivity analysis or confidence adjustment has been applied. Exact scores should stay out of external claims.

##### Sources

- Canonical arithmetic audit: [Kong guided evaluation — Supplied scoring audit](48-kong-guided-evaluation.md#supplied-scoring-audit).
- Official contextual mechanisms (`E1` only): [Kong deployment topologies](https://developer.konghq.com/gateway/deployment-topologies/), [Apigee hybrid 1.16](https://docs.cloud.google.com/apigee/docs/hybrid/v1.16/what-is-hybrid), [MuleSoft Omni Gateway](https://docs.mulesoft.com/gateway/latest/), and [Azure API Management self-hosted gateway](https://learn.microsoft.com/en-us/azure/api-management/self-hosted-gateway-overview).

##### Listen for

“A score of 93 proves fit,” or “the corrected totals invalidate the whole exercise.”

##### Evidence-safe response

The correction makes the input auditable; it does not create a rubric, confidence model, sensitivity analysis, or executed comparison. Arithmetic and evidence confidence are different questions.

##### Follow-up probe

Should this score remain a governance input, and what controls must exist before it can influence authorization?

##### Decision impact

The score may explain preference but cannot offset an unknown or failed mandatory gate.

##### Capture

Record acceptance or dispute of the arithmetic, the permitted use of the score, and the controls required for recalculation.

##### Branch/rejoin

Branch to slide 25 for raw inputs; rejoin at slide 6.

##### HOLD/park

HOLD any attempt to convert the score into production approval. Park recalculation only with named scorers, rubric, confidence, and sensitivity.

#### KGE-06 · Proceed with a bounded, reversible Kong foundation

- **Phase:** `KGE-P2 — Options and decision`
- **Native route:** [Open slide 6](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/5) (`#/present/kong-platform-journey-guided/5`)
- **Timebox:** 5 minutes
- **Evidence state:** Bounded direction
- **Meeting job:** Decide separately on the target, reversible foundation, proof programme, custody and exit benchmarks, and production-scale block.

##### Purpose

Turn the assessment recommendation into a reversible authorization boundary.

##### Talk track

Proceed with Kong as the leading planning direction, but authorize only the foundation and proof programme. Critical scale stays blocked until the outcome gates close.

##### Ask

Approve the bounded direction, owners and evidence budget.

##### Bridge

The first design decision is not topology. It is who controls and operates the management plane.

##### Caveat

This is not a universal product ranking or a claim of production readiness.

##### Sources

- Canonical authorization boundary: [Kong guided evaluation — Bounded authorization](48-kong-guided-evaluation.md#bounded-authorization).
- Official documented mechanisms (`E1` only): [Kong hybrid mode](https://developer.konghq.com/gateway/hybrid-mode/) and [Kong Gateway version support policy](https://developer.konghq.com/gateway/version-support-policy/).

##### Listen for

“Why choose before the PoC?” or “Can we approve production now?”

##### Evidence-safe response

The authorization is a reversible foundation and the work required to test it. Critical production scale remains explicitly unauthorized until reviewed target-shaped evidence closes the outcome gates.

##### Follow-up probe

For each authorization row, is the answer approve, amend, or hold—and what evidence would change it?

##### Decision impact

This is the primary authority boundary; ambiguity here contaminates every later architecture, migration, and proof discussion.

##### Capture

Record approve/amend/hold for the exact target, foundation, GEP-01–06, custody benchmark, true exit, and production-scale block, including dissent.

##### Branch/rejoin

Branch to slides 7–8 for boundary and duty or slides 17–21 for proof and outcome authority. Rejoin here for authorization and at slide 21 for evidence consequences.

##### HOLD/park

HOLD when scope, permanent duty, evidence budget, or stop authority has no accountable owner. Do not park the authorization itself.

#### KGE-07 · Choose the operating boundary before the topology

- **Phase:** `KGE-P2 — Options and decision`
- **Native route:** [Open slide 7](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/6) (`#/present/kong-platform-journey-guided/6`)
- **Timebox:** 3 minutes
- **Evidence state:** Proposed target
- **Meeting job:** Keep self-managed lead, Konnect custody benchmark, and true non-Kong exit as distinct obligations.

##### Purpose

Prevent the operating-model decision from being hidden inside an architecture diagram.

##### Talk track

The leading target is self-managed hybrid. Konnect is a same-vendor custody benchmark, not a vendor exit. A true non-Kong exit remains a separate obligation.

##### Ask

Confirm the leading target and authorize the two counterfactual benchmarks.

##### Bridge

If self-managed control leads, the enterprise must accept the permanent duty that comes with it.

##### Caveat

The option records are planning hypotheses until custody, migration and outcome evidence are executed.

##### Sources

- Canonical option and target records: [Kong multicloud study roadmap](44-kong-multicloud-study-roadmap.md), [Kong enterprise platform deployment strategy](47-kong-enterprise-platform-strategy.md), and [Kong guided evaluation](48-kong-guided-evaluation.md).
- Official documented mechanisms (`E1` only): [Kong hybrid mode](https://developer.konghq.com/gateway/hybrid-mode/) and [Kong Gateway version support policy](https://developer.konghq.com/gateway/version-support-policy/).

##### Listen for

“Konnect is the exit,” or “self-managed is obviously better because it provides control.”

##### Evidence-safe response

Konnect tests a same-vendor custody switch. A true exit tests reconstruction outside Kong. Self-managed remains a proposed target whose control benefits must be weighed against permanent duties.

##### Follow-up probe

What exact custody, offline, sovereignty, support, or operating condition would favor self-managed, Konnect, or a non-Kong option?

##### Decision impact

Conflating the three boundaries removes the evidence needed to change custody or exit safely.

##### Capture

Name the exact-target owner, Konnect benchmark owner, non-Kong exit owner, option-freeze inputs, and switching evidence.

##### Branch/rejoin

Branch to slides 8 and 12 for duty or slide 24 for economics and exit. Rejoin at slide 21.

##### HOLD/park

HOLD if the leading target lacks an exact boundary or if custody switch and platform exit are treated as the same control.

#### KGE-08 · Self-managed control works only if the enterprise funds the duty

- **Phase:** `KGE-P2 — Options and decision`
- **Native route:** [Open slide 8](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/7) (`#/present/kong-platform-journey-guided/7`)
- **Timebox:** 4 minutes
- **Evidence state:** Proposed target
- **Meeting job:** Confirm permanent platform, database, PKI, release, restore, observability, support, and on-call ownership.

##### Purpose

Make the cost side of the target operating boundary visible.

##### Talk track

The same custody that makes self-managed Kong attractive also creates permanent CP, database, PKI, upgrade, restore and 24×7 obligations. Those duties must have named owners and funded capacity.

##### Ask

Confirm whether these duties belong inside the enterprise platform operating model.

##### Bridge

With the boundary explicit, the target topology becomes simple enough to explain.

##### Caveat

Control-plane outage continuity does not imply mutation, revocation or recovery guarantees; those are separate tests.

##### Sources

- Canonical duty model: [Kong enterprise platform deployment strategy](47-kong-enterprise-platform-strategy.md) and [Kong guided evaluation](48-kong-guided-evaluation.md).
- Official documented mechanisms (`E1` only): [Kong hybrid mode](https://developer.konghq.com/gateway/hybrid-mode/) and [Kong Gateway version support policy](https://developer.konghq.com/gateway/version-support-policy/).

##### Listen for

“Cached data-plane continuity removes the duty,” “the vendor owns this,” or an assumption that the current team can absorb it without capacity evidence.

##### Evidence-safe response

Cached proxying is narrower than mutation, revocation, clean-node scale, reconciliation, recovery, and 24×7 service accountability. Vendor support does not transfer those duties.

##### Follow-up probe

Who owns each permanent duty, with what funded capacity, response objective, restore evidence, and escalation path?

##### Decision impact

Without accountable and funded duty, the self-managed target is non-admissible regardless of documented capability.

##### Capture

Record RACI, staffing and sourcing gaps, on-call coverage, restore ownership, capacity assumptions, and TCO evidence requests.

##### Branch/rejoin

Branch to slides 9–12 for architecture and ownership or slides 20 and 24 for sustainability and economics. Rejoin at slide 6 or 21.

##### HOLD/park

HOLD when any control-plane, database, PKI, release, restore, observability, support, or on-call duty lacks an accountable funded owner.

### Phase 3 — Architecture and adoption

#### KGE-09 · One control boundary; distributed request runtimes

- **Phase:** `KGE-P3 — Architecture and adoption`
- **Native route:** [Open slide 9](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/8) (`#/present/kong-platform-journey-guided/8`)
- **Timebox:** 4 minutes
- **Evidence state:** Proposed target
- **Meeting job:** Validate the control zone, data-plane cells, request lanes, evidence paths, network, and sovereignty boundaries.

##### Purpose

Give the audience a readable mental model of the target architecture.

##### Talk track

Configuration authority is centralized in the enterprise control zone. Data planes proxy near workloads using accepted cached configuration. Local collectors preserve evidence close to the runtime. This is a simplification of the canonical engineering diagram.

##### Ask

Validate control-zone ownership, data-plane placement and evidence boundaries.

##### Bridge

This topology has multiple health paths; a healthy proxy alone is not a healthy platform.

##### Caveat

Cached configuration continuity does not authorize emergency mutation or prove recovery objectives.

##### Sources

- Canonical architecture: [Kong enterprise platform deployment strategy](47-kong-enterprise-platform-strategy.md) and [Kong guided evaluation](48-kong-guided-evaluation.md).
- Official documented mechanisms (`E1` only): [Kong hybrid mode](https://developer.konghq.com/gateway/hybrid-mode/) and [Kong Gateway monitoring](https://developer.konghq.com/gateway/monitoring/).

##### Listen for

“The arrows imply a direct data-plane database path,” “the diagram proves HA,” or “multiregion failover is already solved.”

##### Evidence-safe response

The diagram is an `E1`-informed discussion view with path-specific arrows. It asserts neither a direct data-plane database path nor executed high-availability, failover, sovereignty, or recovery outcomes.

##### Follow-up probe

Which path, region, trust boundary, network dependency, or evidence flow needs to be corrected or proved once the target is frozen?

##### Decision impact

A disputed control, request, trust, or evidence boundary changes the BOM, fault model, ownership, and production proof scope.

##### Capture

Record topology disputes, region and zone placement, network/trust dependencies, sovereignty requirements, evidence paths, and owners.

##### Branch/rejoin

Branch to slides 10–11 for state and degraded behavior or slides 18–20 for target execution. Rejoin at slide 21.

##### HOLD/park

HOLD target freeze when a mandatory boundary or authority path is unknown. Park diagram detail only with a canonical-model correction or target test and re-entry at slide 21.

#### KGE-10 · Healthy proxy ≠ healthy platform

- **Phase:** `KGE-P3 — Architecture and adoption`
- **Native route:** [Open slide 10](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/9) (`#/present/kong-platform-journey-guided/9`)
- **Timebox:** 4 minutes
- **Evidence state:** Proposed target
- **Meeting job:** Separate configuration, trust, request, business, and evidence paths and decide what governs service admission.

##### Purpose

Prevent availability claims from collapsing independent health paths.

##### Talk track

Kong hybrid separates configuration distribution from request proxying. Trust admission is another path. Each can fail independently, so admission and recovery evidence must be evaluated separately.

##### Ask

Approve separate proof gates for configuration, trust and request continuity.

##### Bridge

Control-plane loss then becomes an admission-policy problem, not a binary up/down state.

##### Caveat

These states are organizational policy constructs around Kong behavior; they are not automatic product guarantees.

##### Sources

- Canonical state-and-trust model: [Kong enterprise platform deployment strategy](47-kong-enterprise-platform-strategy.md) and [Kong guided evaluation](48-kong-guided-evaluation.md).
- Official documented mechanisms (`E1` only): [Kong hybrid mode](https://developer.konghq.com/gateway/hybrid-mode/) and [Kong Gateway monitoring](https://developer.konghq.com/gateway/monitoring/).

##### Listen for

“Proxy success proves availability,” or an assumption that certificate rotation, urgent revocation, configuration freshness, backend readiness, and business correctness move together.

##### Evidence-safe response

Gateway uptime is not the API or business SLO. Configuration, trust, request, backend, business, and evidence paths require distinct state identity, probes, objectives, and reviewers.

##### Follow-up probe

Which path admits the service, what is its active-state identity, and which business probe detects false-ready behavior?

##### Decision impact

Collapsing the paths can admit a service that proxies traffic while trust, backend, business, or evidence obligations are failing.

##### Capture

Record path identities, probes, thresholds, trust age, backend readiness, business verifier, evidence-gap accounting, and owners.

##### Branch/rejoin

Branch to slide 11 for admission states or slides 17–19 for evidence and execution. Rejoin at slide 21.

##### HOLD/park

HOLD when the room cannot name the admission signal, state identity, business probe, or accountable response owner for a mandatory path.

#### KGE-11 · Control-plane loss requires explicit admission states

- **Phase:** `KGE-P3 — Architecture and adoption`
- **Native route:** [Open slide 11](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/10) (`#/present/kong-platform-journey-guided/10`)
- **Timebox:** 4 minutes
- **Evidence state:** Proposed target
- **Meeting job:** Assign continue, hold, quarantine, reconcile, override, and response authority for degraded operation.

##### Purpose

Show how degraded operation is governed without implying that proxy continuity equals full platform health.

##### Talk track

A data plane can continue proxying accepted state while isolated. Reconnection must compare desired and effective state and run business probes. Admission, hold, quarantine and stop are policy decisions with evidence.

##### Ask

Assign decision rights and response times for each state.

##### Bridge

Those decisions require a funded operating model with named owners.

##### Caveat

The state model is a target operating policy, not an out-of-the-box automated Kong workflow.

##### Sources

- Canonical degraded-state policy: [Kong enterprise platform deployment strategy](47-kong-enterprise-platform-strategy.md) and [Kong guided evaluation](48-kong-guided-evaluation.md).
- Official documented mechanisms (`E1` only): [Kong hybrid mode](https://developer.konghq.com/gateway/hybrid-mode/) and [Kong Gateway monitoring](https://developer.konghq.com/gateway/monitoring/).

##### Listen for

“Kong automates these states,” “always keep serving,” or “always stop as soon as control is lost.”

##### Evidence-safe response

These are proposed organizational policy states around documented behavior. Continue, hold, quarantine, override, stop, and reconcile must be risk-specific, time-bounded, observable, and owned.

##### Follow-up probe

Who can admit, override, or stop each state; what age or condition expires it; and what evidence proves safe reconciliation?

##### Decision impact

Unowned degraded-state authority can turn cached continuity into uncontrolled admission or unnecessary outage.

##### Capture

Record state owners, response objectives, staleness/expiry rules, break-glass authority, business probes, reconciliation evidence, and escalation.

##### Branch/rejoin

Branch to slide 12 for ownership or slides 18–19 for execution and artifacts. Rejoin at slide 21.

##### HOLD/park

HOLD when a mandatory degraded state lacks an owner, expiry, response rule, probe, or reconciliation artifact.

#### KGE-12 · Self-managed control is a funded platform service

- **Phase:** `KGE-P3 — Architecture and adoption`
- **Native route:** [Open slide 12](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/11) (`#/present/kong-platform-journey-guided/11`)
- **Timebox:** 4 minutes
- **Evidence state:** Proposed target
- **Meeting job:** Name accountable teams and funded capacity for platform lifecycle, domain correctness, admission, reliability, and escalation.

##### Purpose

Translate architecture into durable operating ownership.

##### Talk track

Self-managed Kong succeeds only when the platform team owns the service lifecycle, product teams own API outcomes, security and SRE own admission and reliability gates, and the vendor remains support—not the accountable owner.

##### Ask

Name accountable teams and capacity before foundation build starts.

##### Bridge

The adoption roadmap sequences those responsibilities and evidence gates.

##### Caveat

The exact RACI is a target model and must be reconciled with the enterprise organizational design.

##### Sources

- Canonical operating model: [Kong enterprise platform deployment strategy](47-kong-enterprise-platform-strategy.md) and [Kong guided evaluation](48-kong-guided-evaluation.md).
- Official documented mechanisms (`E1` only): [Kong hybrid mode](https://developer.konghq.com/gateway/hybrid-mode/) and [Kong Gateway monitoring](https://developer.konghq.com/gateway/monitoring/).

##### Listen for

“The vendor or service desk owns it,” “the platform team owns business correctness,” or an assumption that existing teams can absorb the duty without capacity evidence.

##### Evidence-safe response

Support can assist but does not transfer service accountability. Platform lifecycle, domain correctness, IAM/security admission, reliability, evidence, and escalation need explicit owners and funded capacity.

##### Follow-up probe

Which team is accountable for each outcome, what capacity is funded, and who acts when product, platform, security, and domain signals disagree?

##### Decision impact

Unnamed teams or heroic operating assumptions make the self-managed option non-admissible.

##### Capture

Record RACI, capacity, sourcing, service-desk boundary, vendor escalation, exceptions, and unresolved role conflicts.

##### Branch/rejoin

Branch to slide 8 for permanent duty, slide 13 for adoption gates, or slide 20 for sustainability. Rejoin at slide 6 or 21.

##### HOLD/park

HOLD when any mandatory outcome relies on an unnamed team, unfunded capacity, or a support contract in place of accountability.

#### KGE-13 · Foundation is work; scale is an outcome gate

- **Phase:** `KGE-P3 — Architecture and adoption`
- **Native route:** [Open slide 13](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/12) (`#/present/kong-platform-journey-guided/12`)
- **Timebox:** 3 minutes
- **Evidence state:** Scenario assumption
- **Meeting job:** Approve the KP0–KP5 gate sequence and the evidence needed to leave each phase without treating scenario windows as commitments.

##### Purpose

Separate foundation delivery from production scale authorization.

##### Talk track

The roadmap begins with owners and inventory, builds a reversible foundation, runs representative proof, then grows coexistence and operating scale. The source windows deliberately overlap; all 0–18 month windows are scenario assumptions, not commitments.

##### Ask

Approve the gate sequence and the evidence required to leave each phase.

##### Bridge

Selection does not authorize package-by-package migration. The migration unit is responsibility and state.

##### Caveat

The overlapping timeline windows are planning forms; actual duration depends on workload inventory, platform capacity and evidence closure.

##### Sources

- Canonical adoption sequence: [Kong enterprise platform deployment strategy](47-kong-enterprise-platform-strategy.md) and [Kong guided evaluation](48-kong-guided-evaluation.md).
- Official contextual mechanisms (`E1` only): [Kong hybrid mode](https://developer.konghq.com/gateway/hybrid-mode/) and [Kong Gateway monitoring](https://developer.konghq.com/gateway/monitoring/).

##### Listen for

“Are these committed dates?” “How many APIs move in each window?” or pressure to accelerate by removing evidence gates.

##### Evidence-safe response

The windows are synthetic planning assumptions, not current status or commitments. Progress is governed by entry and exit evidence, not elapsed time or object count.

##### Follow-up probe

What evidence must exist before each gate opens or closes, and which owner can stop progression?

##### Decision impact

Treating scenario dates as commitments can force irreversible migration or scale before ownership and proof close.

##### Capture

Record gate owner, entry evidence, exit evidence, stop authority, amended scenario assumptions, and dependencies on observed inventory.

##### Branch/rejoin

Branch to slides 14–16 for migration gates or slides 18–21 for proof-first sequencing. Rejoin at slide 6 or 21.

##### HOLD/park

HOLD any phase transition that lacks exit evidence or stop authority. Park calendar planning until workload inventory and capacity are observed.

### Phase 4 — Migration

#### KGE-14 · Move responsibilities—not Mule packages

- **Phase:** `KGE-P4 — Migration`
- **Native route:** [Open slide 14](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/13) (`#/present/kong-platform-journey-guided/13`)
- **Timebox:** 4 minutes
- **Evidence state:** Proposed migration model
- **Meeting job:** Adopt the responsibility and durable-state taxonomy and assign inventory, classification, destination, and authority owners.

##### Purpose

Change the migration unit from package to responsibility and state.

##### Talk track

Only gateway policy is unambiguously a Kong destination. Thin facades may stay at the edge or move into an owned service. Transformation, orchestration, messaging, batch and connectors require their own destination owners. Retirement occurs only after parity and route-back proof.

##### Ask

Adopt the responsibility taxonomy for inventory and wave planning.

##### Bridge

That decomposition supports bounded coexistence rather than a big-bang cutover.

##### Caveat

This is a migration doctrine. Actual destination selection requires workload-level classification and dependency evidence.

##### Sources

- Canonical migration and decision content: [Mule migration strategy](35-mule-migration-strategy.md) and [Kong guided evaluation](48-kong-guided-evaluation.md).
- Official contextual mechanisms (`E1` only): [MuleSoft Omni Gateway](https://docs.mulesoft.com/gateway/latest/) and [Kong deployment topologies](https://developer.konghq.com/gateway/deployment-topologies/).

##### Listen for

“Move Mule packages directly to Kong,” or “a Kong plugin can reproduce the transformation or orchestration, so it belongs at the edge.”

##### Evidence-safe response

The migration unit is responsibility and durable state, not package. Edge extensibility does not prove that durable or stateful business behavior belongs in gateway policy.

##### Follow-up probe

What responsibility does the component perform, where is durable truth held, who owns its side effects, and what destination preserves that authority?

##### Decision impact

Package-led movement can relocate stateful domain or integration behavior into an unsafe boundary and make route-back or reconciliation unreliable.

##### Capture

Record responsibility, state authority, destination, dependencies, business owner, data owner, and the evidence required to classify each workload.

##### Branch/rejoin

Branch to slides 15–16 for coexistence and waves or slide 23 for a customization claim. Rejoin at slide 20 or 21.

##### HOLD/park

HOLD a migration cohort when responsibility, durable-state authority, destination, or owner is unknown. Park implementation detail only after the classification decision is recorded.

#### KGE-15 · Keep the API edge stable while old and new runtimes coexist

- **Phase:** `KGE-P4 — Migration`
- **Native route:** [Open slide 15](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/14) (`#/present/kong-platform-journey-guided/14`)
- **Timebox:** 4 minutes
- **Evidence state:** Proposed migration model
- **Meeting job:** Require bounded cohorts, parity probes, reconciliation, evidence retention, and route-back while runtimes coexist.

##### Purpose

Show a safe migration control surface without tying it to a specific product claim.

##### Talk track

Consumers see a stable API edge. A bounded cohort can route to the existing Mule runtime or a new owned runtime. Parity evidence compares semantics, side effects and SLOs. Route-back remains active until the exit evidence closes.

##### Ask

Approve cohorting, parity probes and route-back as mandatory migration controls.

##### Bridge

The controls are applied in waves, each with explicit entry and exit evidence.

##### Caveat

The coexistence figure deliberately says stable API edge; the source migration strategy does not choose the exact gateway product for this pattern.

##### Sources

- Canonical coexistence and decision content: [Mule migration strategy](35-mule-migration-strategy.md) and [Kong guided evaluation](48-kong-guided-evaluation.md).
- Official contextual mechanisms (`E1` only): [MuleSoft Omni Gateway](https://docs.mulesoft.com/gateway/latest/) and [Kong deployment topologies](https://developer.konghq.com/gateway/deployment-topologies/).

##### Listen for

“Dual run is too costly,” “route-back is unnecessary,” or “the stable edge must already be Kong.”

##### Evidence-safe response

The stable-edge pattern is product-neutral and safety-driven. Dual-run and route-back cost must be compared with the business and recovery risk of irreversible semantic drift.

##### Follow-up probe

Which cohort, business verifier, side-effect comparison, SLO, reconciliation record, and route-back trigger would make coexistence safe enough?

##### Decision impact

Removing parity or route-back controls converts migration speed into unbounded business and recovery risk.

##### Capture

Record cohort boundary, business verifier, parity corpus, side-effect evidence, reconciliation owner, route-back authority, and evidence-retention period.

##### Branch/rejoin

Branch to slide 14 for classification, slide 16 for wave controls, or slide 24 for dual-run economics. Rejoin at slide 20 or 21.

##### HOLD/park

HOLD a cohort without representative parity, business correctness, reconciliation, and route-back. Park cost optimization only after the safety boundary is preserved.

#### KGE-16 · Migration advances on evidence—not time

- **Phase:** `KGE-P4 — Migration`
- **Native route:** [Open slide 16](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/15) (`#/present/kong-platform-journey-guided/15`)
- **Timebox:** 4 minutes
- **Evidence state:** Proposed migration model
- **Meeting job:** Agree evidence entry and exit controls for M0–M5 and name retirement authority.

##### Purpose

Sequence migration by evidence complexity rather than package count.

##### Talk track

M0 establishes inventory and safety; M1 handles gateway-dominant work; M2 proves representative hard integrations; M3 establishes the domain factory; M4 resolves the connector and batch tail; M5 retires the shared runtime only after dependency zero.

##### Ask

Adopt entry/exit evidence as the wave control, not elapsed time or migrated object count.

##### Bridge

The current PoC evidence is far earlier than these production gates.

##### Caveat

These phases are scenario planning. They do not assert current programme progress or duration.

##### Sources

- Canonical wave and decision content: [Mule migration strategy](35-mule-migration-strategy.md) and [Kong guided evaluation](48-kong-guided-evaluation.md).
- Official contextual mechanisms (`E1` only): [MuleSoft Omni Gateway](https://docs.mulesoft.com/gateway/latest/) and [Kong deployment topologies](https://developer.konghq.com/gateway/deployment-topologies/).

##### Listen for

“Give us committed counts and dates,” “object migration percentage proves progress,” or pressure to retire the shared runtime before dependency zero.

##### Evidence-safe response

Elapsed time and object count do not prove business parity, residual dependency, reconciliation, or safe retirement. Each wave advances only on owned entry and exit evidence.

##### Follow-up probe

What evidence opens and closes each wave, who validates dependency zero, and who can stop or reverse retirement?

##### Decision impact

Time-led progression can produce irreversible cutover while state, parity, or residual dependency remains unknown.

##### Capture

Record per-wave entry and exit evidence, dependencies, representative cases, route-back condition, retirement authority, and unresolved assumptions.

##### Branch/rejoin

Branch to slides 17–18 for the current evidence gap or slides 20–21 for outcome and retirement authority. Rejoin at slide 21.

##### HOLD/park

HOLD when business parity, state authority, reconciliation, route-back, or dependency-zero evidence is missing. Do not park an irreversible cutover risk.

### Phase 5 — Production proof

#### KGE-17 · Current PoC is a functional baseline—not KP-SMH1 proof

- **Phase:** `KGE-P5 — Production proof`
- **Native route:** [Open slide 17](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/16) (`#/present/kong-platform-journey-guided/16`)
- **Timebox:** 4 minutes
- **Evidence state:** Executed local baseline
- **Meeting job:** Establish the exact current evidence baseline without converting counts into readiness.

##### Purpose

Reset confidence before discussing production outcomes.

##### Talk track

Five of sixteen aggregate register items are automated local-baseline checks; eleven are not run. A separate protocol defines 28 atomic comparison cases. Neither system contains target-option E3/E4 results for KP-SMH1.

##### Ask

Authorize the evidence programme and keep all not-run states explicit.

##### Bridge

The gap is not a lack of scripts—it is a lack of target-aligned execution evidence. The next slide defines the proof programme.

##### Caveat

The 16 aggregate items and 28 atomic cases are different systems and must not be added together.

##### Sources

- Canonical evidence boundary: [Current PoC register](../poc/README.md), [Kong guided evaluation](48-kong-guided-evaluation.md), and [Kong enterprise platform deployment strategy](47-kong-enterprise-platform-strategy.md).
- Official contextual mechanisms (`E1` only): [Kong hybrid mode](https://developer.konghq.com/gateway/hybrid-mode/) and [Kong Gateway monitoring](https://developer.konghq.com/gateway/monitoring/).

##### Listen for

“Five of sixteen means 31% ready,” “the 28 cases are additional completed proof,” or “automated means production representative.”

##### Evidence-safe response

The 16-item register is not a readiness denominator, and the 28 atomic cases are a separate unexecuted protocol. The proposed `KP-SMH1` target still has zero E3/E4 results.

##### Follow-up probe

Which exact result ID is being relied on, what environment produced it, and what decision can that evidence state legitimately support?

##### Decision impact

Inflated counts can authorize scale on local functional evidence that does not represent target topology, failure, identity, migration, or operations.

##### Capture

Record accepted and disputed result IDs, their evidence system, environment, current state, limitations, and the target result needed.

##### Branch/rejoin

Continue to slide 18 for the target proof programme. Rejoin at slide 19 for outcome contracts or slide 21 for decision authority.

##### HOLD/park

HOLD any readiness percentage or production claim derived from these non-additive systems. Park only a specific result dispute with an artifact owner and review gate.

#### KGE-18 · The next PoC must mirror the production target

- **Phase:** `KGE-P5 — Production proof`
- **Native route:** [Open slide 18](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/17) (`#/present/kong-platform-journey-guided/17`)
- **Timebox:** 6 minutes
- **Evidence state:** Not run
- **Meeting job:** Authorize GEP-01–06 with an exact environment, owner, measure, threshold, raw artifact, reviewer, and stop rule.

##### Purpose

Turn the current evidence gap into an executable, target-shaped proof programme.

##### Talk track

This is not a larger feature demonstration. Each workstream needs a representative environment, named owner, test method, measure, acceptance artifact, threshold and stop condition. The agentic-gateway study remains separate so emerging capabilities do not inflate confidence in the core gateway.

##### Ask

Approve these six workstreams, their owners, capacity and evidence budget—not production scale.

##### Bridge

Once the proof scope is fixed, production readiness is judged through the outcome measures and acceptance artifacts that follow.

##### Caveat

These are required proof activities, not completed results. Verify the Kong Enterprise 3.14 edition, licensing and support status before claiming any capability; retain explicit not-run states.

##### Sources

- Canonical proof programme: [Kong guided evaluation — Six-workstream target-aligned proof programme](48-kong-guided-evaluation.md#six-workstream-target-aligned-proof-programme).
- Official documented mechanisms (`E1` only): [Kong Gateway version support policy](https://developer.konghq.com/gateway/version-support-policy/), [Kong hybrid mode](https://developer.konghq.com/gateway/hybrid-mode/), [Kong Gateway monitoring](https://developer.konghq.com/gateway/monitoring/), and [Kong AI Gateway](https://developer.konghq.com/ai-gateway/).

##### Listen for

“Documentation already proves 3.14,” “the existing PoC is enough,” “the programme is too broad,” or “AI capability should count toward the core decision.”

##### Evidence-safe response

Documentation supports test design, not entitlement, configured behavior, target execution, or production outcome. Narrow a workstream only when the omitted decision risk is explicit; keep agentic proof separately versioned.

##### Follow-up probe

For each GEP workstream, what exact BOM and environment, measure, threshold, raw artifact, independent reviewer, and stop rule will change the decision?

##### Decision impact

Missing target fidelity or review controls leaves documented capability unable to advance into production evidence.

##### Capture

For GEP-01–06, record owner, capacity, exact BOM/environment, method, measure, threshold, raw artifact, reviewer, due gate, and stop rule.

##### Branch/rejoin

Branch to slide 23 for the agentic study, slides 19–20 for outcome forms, or slide 24 for economics. Rejoin at slide 19 and then slide 21.

##### HOLD/park

HOLD any workstream missing its exact option, environment, measure, threshold, artifact, reviewer, or stop rule. Park scope detail only with those fields and a slide-19 re-entry.

#### KGE-19 · Five reviewable outcomes anchor production proof

- **Phase:** `KGE-P5 — Production proof`
- **Native route:** [Open slide 19](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/18) (`#/present/kong-platform-journey-guided/18`)
- **Timebox:** 4 minutes
- **Evidence state:** Proposed acceptance contract
- **Meeting job:** Agree target forms, artifacts, cadence, and owners for KO-1 through KO-5.

##### Purpose

Translate the first five production outcomes into decision evidence.

##### Talk track

Each mechanism is paired with a measurable outcome and a reviewable artifact. State fidelity, request reliability, trust admission, recovery and safe change are all separate admission dimensions.

##### Ask

Confirm target forms, artifacts, cadence and accountable owners for KO-1 through KO-5.

##### Bridge

Scale also depends on capacity, adoption, economics, exit and estate truth.

##### Caveat

The slide shows target forms, not achieved results.

##### Sources

- Canonical outcome contract: [Kong enterprise platform deployment strategy](47-kong-enterprise-platform-strategy.md) and [Kong guided evaluation](48-kong-guided-evaluation.md).
- Official documented mechanisms (`E1` only): [Kong hybrid mode](https://developer.konghq.com/gateway/hybrid-mode/), [Kong Gateway monitoring](https://developer.konghq.com/gateway/monitoring/), and [Kong AI Gateway](https://developer.konghq.com/ai-gateway/).

##### Listen for

“The mechanism should be enough,” or pressure to treat example target forms as achieved thresholds.

##### Evidence-safe response

Mechanisms are not outcomes. KO-1 through KO-5 are proposed acceptance forms whose exact thresholds, artifacts, cadence, and independent reviewers still require approval and execution.

##### Follow-up probe

Who approves each threshold, what raw artifact proves it, how often is it reviewed, and what failure forces hold or recovery?

##### Decision impact

Without pre-approved outcome contracts, a successful demonstration can be reinterpreted after the fact and cannot govern production admission.

##### Capture

Record KO-1–KO-5 threshold owner, artifact schema, cadence, reviewer, failure disposition, and unresolved target value.

##### Branch/rejoin

Branch to slide 18 for a missing workstream or continue to slide 20. Rejoin at slide 21.

##### HOLD/park

HOLD an outcome without an approved measure, threshold, raw artifact, reviewer, and failure disposition. Park only the numeric target, not the requirement for one.

#### KGE-20 · Scale depends on the whole operating system

- **Phase:** `KGE-P5 — Production proof`
- **Native route:** [Open slide 20](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/19) (`#/present/kong-platform-journey-guided/19`)
- **Timebox:** 4 minutes
- **Evidence state:** Proposed acceptance contract
- **Meeting job:** Agree KO-6–KO-11 and identify the most likely scale blocker across technology, evidence, adoption, toil, exit, and estate truth.

##### Purpose

Complete the production decision with non-functional and organizational outcomes.

##### Talk track

Capacity and evidence safety matter, but so do adoption, operating sustainability, exit readiness and accurate estate ownership. Telemetry must stay off the critical path, gaps must be quantified, and prohibited fields must remain absent.

##### Ask

Confirm which outcome is currently the likely scale blocker and who owns its evidence.

##### Bridge

The final decision must preserve four outcomes: scale, narrow, switch custody or exit.

##### Caveat

These are acceptance categories; no result is asserted on this slide.

##### Sources

- Canonical outcome contract: [Kong enterprise platform deployment strategy](47-kong-enterprise-platform-strategy.md) and [Kong guided evaluation](48-kong-guided-evaluation.md).
- Official documented mechanisms (`E1` only): [Kong hybrid mode](https://developer.konghq.com/gateway/hybrid-mode/), [Kong Gateway monitoring](https://developer.konghq.com/gateway/monitoring/), and [Kong AI Gateway](https://developer.konghq.com/ai-gateway/).

##### Listen for

“Technical health is enough,” “cost and adoption can wait,” or “exit readiness is unnecessary once the platform is selected.”

##### Evidence-safe response

Production admission is a whole-operating-system decision. Capacity, evidence safety, adoption, operating sustainability, exit, and estate ownership can each block scale even when proxy behavior is healthy.

##### Follow-up probe

Which KO-6–KO-11 outcome is most likely to block scale, what data proves it, and who has authority to act on failure?

##### Decision impact

Ignoring organizational and economic outcomes converts installation success into unsupported production confidence and weakens reversibility.

##### Capture

Record the likely blocker, owner, data source, cadence, evidence-safety control, toil and cost model, adoption measure, estate owner, and exit rehearsal.

##### Branch/rejoin

Branch to slide 12 for ownership or slide 24 for economics and exit. Rejoin at slide 21.

##### HOLD/park

HOLD scale when any mandatory outcome is failed, unknown, unowned, or offset by a weighted score. Park only a bounded target value with an owner and review date.

#### KGE-21 · Negative evidence must change the decision

- **Phase:** `KGE-P5 — Production proof`
- **Native route:** [Open slide 21](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/20) (`#/present/kong-platform-journey-guided/20`)
- **Timebox:** 4 minutes
- **Evidence state:** Proposed acceptance contract
- **Meeting job:** Pre-commit scale, narrow, switch-custody, exit, and hold authority before evidence is executed.

##### Purpose

Close with a falsifiable decision rather than a predetermined rollout.

##### Talk track

Before evidence runs, commit to four possible outcomes: scale, narrow, switch custody or exit the platform. Recommendation changes when external API governance dominates, Anypoint remains strategic, Azure consolidation outweighs neutrality, custody/offline requirements fail, or E3/E4 and TCO evidence does not close.

##### Ask

Approve the decision outcomes and the authority to stop or change course.

##### Bridge

The appendix preserves the supplied comparison inputs without presenting them as proven facts.

##### Caveat

No outcome is preselected. Konnect is a custody switch; a true platform exit remains separate.

##### Sources

- Canonical assurance and decision content: [Kong enterprise platform deployment strategy](47-kong-enterprise-platform-strategy.md) and [Kong guided evaluation](48-kong-guided-evaluation.md).
- Official documented mechanisms (`E1` only): [Kong hybrid mode](https://developer.konghq.com/gateway/hybrid-mode/), [Kong Gateway monitoring](https://developer.konghq.com/gateway/monitoring/), and [Kong AI Gateway](https://developer.konghq.com/ai-gateway/).

##### Listen for

“The selection is already fixed,” “sunk cost means we continue,” or uncertainty about who can narrow, switch, exit, or hold.

##### Evidence-safe response

No outcome is preselected. Negative evidence must change scope or direction, and sunk cost cannot waive a failed or unknown mandatory gate.

##### Follow-up probe

Who has authority for each outcome, which non-waivable condition triggers it, and what evidence will be read back to the decision forum?

##### Decision impact

Without pre-committed consequences, the proof programme becomes a demonstration whose failures cannot affect the rollout.

##### Capture

Record decision rights, non-waivable gates, scale/narrow/switch/exit/hold triggers, dissent, fallback, next forum, and read-back owner.

##### Branch/rejoin

Branch to slide 6 for the original authorization or slides 24–25 for economics and score governance. Always rejoin and close here or at slide 6.

##### HOLD/park

HOLD when failed or unknown mandatory evidence cannot change the outcome. Do not park decision authority or a non-waivable gate.

### Phase 6 — Audit appendix

#### KGE-22 · Comparison input—architecture and delivery

- **Phase:** `KGE-P6 — Audit appendix`
- **Native route:** [Open slide 22](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/21) (`#/present/kong-platform-journey-guided/21`)
- **Timebox:** On demand; 3-minute branch
- **Evidence state:** Stakeholder input
- **Meeting job:** Turn disputed architecture and delivery labels into versioned, symmetric proof questions without rescoring in the room.

##### Purpose

Preserve the sanitized supplied evaluation’s architectural comparison without turning it into a dense main-story slide.

##### Talk track

The supplied labels are shown explicitly as stakeholder assessments preserved in docs/48. Official documentation supports the high-level deployment models, but the relative ratings require an evidence rubric and versioned testing.

##### Ask

Use this table to identify proof questions, not to re-litigate the feature list in the room.

##### Bridge

The next appendix page covers API management, experience and AI claims.

##### Caveat

Qualitative ratings are not independently validated and may change by edition and release.

##### Sources

- Canonical sanitized input: [Kong guided evaluation — Supplied comparison input: architecture and delivery](48-kong-guided-evaluation.md#supplied-comparison-input-architecture-and-delivery).
- Official documented mechanisms (`E1` only): [Kong deployment topologies](https://developer.konghq.com/gateway/deployment-topologies/), [Kong hybrid mode](https://developer.konghq.com/gateway/hybrid-mode/), [Kong AI Gateway](https://developer.konghq.com/ai-gateway/), [Apigee hybrid 1.16](https://docs.cloud.google.com/apigee/docs/hybrid/v1.16/what-is-hybrid), [MuleSoft Omni Gateway](https://docs.mulesoft.com/gateway/latest/), and [Azure API Management self-hosted gateway](https://learn.microsoft.com/en-us/azure/api-management/self-hosted-gateway-overview).

##### Listen for

“Vendor documentation validates the relative labels,” or pressure to change qualitative ratings and rescore during the branch.

##### Evidence-safe response

Official documentation supports bounded mechanism interpretation, not the relative product labels. Convert the disputed label into an exact version-, topology-, and outcome-specific evidence request.

##### Follow-up probe

Which criterion, exact option, edition, topology, use case, and executed artifact would confirm or falsify the label?

##### Decision impact

A material architecture or delivery claim can change the conditional option direction, but not until symmetric evidence closes it.

##### Capture

Record the claim, current evidence state, exact option boundary, required artifact, owner, reviewer, and due gate; do not change the score in the room.

##### Branch/rejoin

Branch to slide 4 for option conditions, slide 18 for proof authorization, or slide 25 for score governance. Rejoin at slide 6.

##### HOLD/park

HOLD if a mandatory option condition depends on an unverified label. Park non-decision detail only with a versioned evidence request and slide-6 re-entry.

#### KGE-23 · Comparison input—management, experience and AI

- **Phase:** `KGE-P6 — Audit appendix`
- **Native route:** [Open slide 23](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/22) (`#/present/kong-platform-journey-guided/22`)
- **Timebox:** On demand; 3-minute branch
- **Evidence state:** Stakeholder input
- **Meeting job:** Assign exact use cases, versions, entitlements, owners, and artifacts for management, developer-experience, customization, and AI claims.

##### Purpose

Preserve the management and experience claims while making their evidence status explicit.

##### Talk track

Lifecycle, governance, portal, developer experience, AI, customization, and best-fit claims must be tested against the required use cases. AI capabilities are changing rapidly and should always be dated and versioned.

##### Ask

Move every unverified adjective into the proof backlog with an owner and artifact.

##### Bridge

The next appendix page covers lock-in, cost, the supplied overall recommendation, and the evidence ceiling.

##### Caveat

Product capability and commercial terms are edition- and date-dependent.

##### Sources

- Canonical sanitized input: [Kong guided evaluation — Supplied comparison input: management, experience, and AI](48-kong-guided-evaluation.md#supplied-comparison-input-management-experience-and-ai).
- Official documented mechanisms (`E1` only): [Kong deployment topologies](https://developer.konghq.com/gateway/deployment-topologies/), [Kong AI Gateway](https://developer.konghq.com/ai-gateway/), [Apigee hybrid 1.16](https://docs.cloud.google.com/apigee/docs/hybrid/v1.16/what-is-hybrid), [MuleSoft Omni Gateway](https://docs.mulesoft.com/gateway/latest/), and [Azure API Management self-hosted gateway](https://learn.microsoft.com/en-us/azure/api-management/self-hosted-gateway-overview).

##### Listen for

“Kong documents MCP, A2A, and AI routing, so agentic fit is proved,” or an assumption that portal, lifecycle, customization, and developer-experience claims are self-validating.

##### Evidence-safe response

Documentation permits a versioned test design. Exact use cases, edition, plugin, entitlement, data flow, threat boundary, cost, safety behavior, and catalog lifecycle remain unproved; agentic evidence cannot inflate the core gateway decision.

##### Follow-up probe

Which exact use case and version/plugin matrix matters, what is the expected outcome, and what artifact and reviewer would prove it?

##### Decision impact

An unbounded management or agentic claim can distort the platform direction, proof budget, security boundary, and economics.

##### Capture

Record use case, version, plugin, entitlement, data flow, threat and privacy boundary, cost/latency measure, content-safety outcome, catalog lifecycle, artifact, and owner.

##### Branch/rejoin

Branch to slide 18 for GEP-05 or slide 24 for commercial implications. Rejoin at slide 19 and then slide 21.

##### HOLD/park

HOLD a decision that depends on an unproved emerging feature, unsupported entitlement, unknown data flow, or critical safety/policy failure. Park only a separately versioned GEP-05 action.

#### KGE-24 · Comparison input—economics and evidence ceiling

- **Phase:** `KGE-P6 — Audit appendix`
- **Native route:** [Open slide 24](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/23) (`#/present/kong-platform-journey-guided/23`)
- **Timebox:** On demand; 3-minute branch
- **Evidence state:** Stakeholder input
- **Meeting job:** Assign fully allocated TCO, custody, support, migration, dual-run, switching, and clean-exit evidence.

##### Purpose

Expose the economic and exit claims as proof obligations rather than conclusions.

##### Talk track

Cost and lock-in cannot be inferred from topology. They require quotes, platform labor, HA/DR, support, observability, portal/product tooling, network and egress, migration effort, and an exit rehearsal.

##### Ask

Assign owners and artifacts for TCO, custody and exit evidence.

##### Bridge

The final appendix page exposes the raw score inputs and corrected arithmetic.

##### Caveat

Commercial terms and estate leverage are organization- and date-specific.

##### Sources

- Canonical sanitized input: [Kong guided evaluation — Supplied comparison input: economics and evidence ceiling](48-kong-guided-evaluation.md#supplied-comparison-input-economics-and-evidence-ceiling).
- Official contextual mechanisms (`E1` only): [Kong deployment topologies](https://developer.konghq.com/gateway/deployment-topologies/), [Kong AI Gateway](https://developer.konghq.com/ai-gateway/), [Apigee hybrid 1.16](https://docs.cloud.google.com/apigee/docs/hybrid/v1.16/what-is-hybrid), [MuleSoft Omni Gateway](https://docs.mulesoft.com/gateway/latest/), and [Azure API Management self-hosted gateway](https://learn.microsoft.com/en-us/azure/api-management/self-hosted-gateway-overview).

##### Listen for

“License price is TCO,” “Kong lock-in is low,” or “Konnect is sufficient exit evidence.”

##### Evidence-safe response

TCO requires licenses, labor, infrastructure, HA/DR, telemetry, support, migration, dual run, and exit. Konnect tests same-vendor custody, not a clean non-Kong rebuild.

##### Follow-up probe

Which cost boundary, workload volume, labor model, support assumption, switching event, and residual dependency will be measured?

##### Decision impact

Unproved economics or exit can make the self-managed benefit non-viable and can favor a custody switch, narrower scope, or different platform.

##### Capture

Record FinOps and sourcing owners, model scope, quotes and assumptions, labor, HA/DR, telemetry, support, migration, dual-run, custody-switch, and non-Kong exit artifacts.

##### Branch/rejoin

Branch to slides 7–8 for custody and duty, slide 20 for sustainability, or slide 25 for score governance. Rejoin at slide 21.

##### HOLD/park

HOLD a cost or lock-in conclusion without a fully allocated model and executable exit evidence. Park commercial detail only in the approved restricted system with a public-safe closure record.

#### KGE-25 · Raw scoring inputs—retain for audit, not as production proof

- **Phase:** `KGE-P6 — Audit appendix`
- **Native route:** [Open slide 25](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/24) (`#/present/kong-platform-journey-guided/24`)
- **Timebox:** On demand; 3-minute branch
- **Evidence state:** Stakeholder input
- **Meeting job:** Decide whether the scorecard remains a governance input and require rubric, confidence, sensitivity, and accountable sign-off.

##### Purpose

Provide an auditable record of the source scorecard without elevating it above its evidence level.

##### Talk track

The inputs are preserved from the sanitized supplied evaluation. Recalculating weight times rating yields 93 for Kong, 85.5 for Apigee and 77 for MuleSoft. This appendix preserves transparency and makes the evidence backlog explicit.

##### Ask

If the scorecard remains a governance artifact, add confidence, sensitivity and accountable sign-off.

##### Bridge

Return to the bounded decision: direction plus proof, not critical scale.

##### Caveat

Scores are illustrative author inputs, not an independent benchmark or production outcome.

##### Sources

- Canonical sanitized arithmetic audit: [Kong guided evaluation — Supplied scoring audit](48-kong-guided-evaluation.md#supplied-scoring-audit).
- Official contextual mechanisms (`E1` only): [Kong deployment topologies](https://developer.konghq.com/gateway/deployment-topologies/), [Kong AI Gateway](https://developer.konghq.com/ai-gateway/), [Apigee hybrid 1.16](https://docs.cloud.google.com/apigee/docs/hybrid/v1.16/what-is-hybrid), [MuleSoft Omni Gateway](https://docs.mulesoft.com/gateway/latest/), and [Azure API Management self-hosted gateway](https://learn.microsoft.com/en-us/azure/api-management/self-hosted-gateway-overview).

##### Listen for

“Corrected arithmetic validates the ranking,” or pressure to change ratings in the room without an approved scoring process.

##### Evidence-safe response

Correct arithmetic does not create a rubric, evidence confidence, sensitivity, benchmark, or production result. Amendments belong in a governed recalculation with named scorers and preserved dissent.

##### Follow-up probe

Who owns the rubric, what confidence rules apply, which sensitivity ranges will be run, and who signs the resulting decision use?

##### Decision impact

An uncontrolled score can conceal mandatory unknowns and create false precision around a conditional direction.

##### Capture

Record scorer, rubric, confidence, sensitivity, evidence links, dissent, permitted use, sign-off, and recalculation due gate.

##### Branch/rejoin

Branch to slides 3–5 for weights, options, and arithmetic. Never close here; rejoin at slide 6 or 21.

##### HOLD/park

HOLD score-based authorization without rubric, confidence, sensitivity, and accountable sign-off. Park recalculation only with an owner and explicit re-entry at slide 6.

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
| Navigation | Mapped slide or canonical source. |
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

The complete slide sections above are the point-of-use facilitation and speaker-notes source. The PowerPoint carries a synchronized concise projection. The canonical studies below continue to own product facts, evidence meanings, and decision content:

- [Kong guided evaluation](48-kong-guided-evaluation.md)
- [Assessment methodology](03-assessment-methodology.md)
- [Kong enterprise platform deployment strategy](47-kong-enterprise-platform-strategy.md)
- [Kong multicloud study roadmap](44-kong-multicloud-study-roadmap.md)
- [Mule migration strategy](35-mule-migration-strategy.md)
- [Current PoC register and evidence boundary](../poc/README.md)
- [Presentation artifact contract](../presentations/README.md)

This is public-safe facilitation guidance. It contains no meeting minutes, named-person assignment, commercial term, private topology, or observed production outcome. Store restricted decisions and evidence in the approved private system; publish only sanitized, authorized conclusions through the repository workflow.
