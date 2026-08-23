# Kong guided evaluation facilitator guide

| Field | Value |
|---|---|
| Artifact type | meeting-facilitation-guide |
| Meeting question | Should the decision owner approve, amend, or hold a bounded Kong foundation and the work required to prove it before production scale? |
| Decision owner | API-platform product owner with the accountable architecture, security/IAM, platform, SRE, migration, sourcing, FinOps, service-management, delivery, and assurance leads |
| Intended users | Meeting chair, presenter, facilitator, scribe, evidence steward, timekeeper, decision owners, and named technical or commercial challengers |
| Scope | Complete speaker notes for all 25 slides; four explicit early assessment gates; an 18-question local interactive contract; meeting routes; bounded side talks; challenge navigation; evidence-safe responses; decision capture; parking-lot control; stop rules; and closing protocol for the Kong guided evaluation |
| Evidence state | Facilitation guidance derived from the canonical guided evaluation and its presentation notes; no new product fact, executed result, commercial conclusion, or production authorization |
| As-of date | 2026-08-22; use the current canonical study and deck revision when facilitating |
| Next gate | Disposition `EAG-01`–`EAG-04`, then record an explicit approve, amend, or hold decision; name owners, artifacts, thresholds, reviewers, due gates, and stop rules for every authorized proof item |

## Use this guide with the presentation

This document is the **complete canonical facilitation and speaker-notes companion** for the Kong guided evaluation. It contains a meeting opening plus a natural-language `Speaker script` and compact `Talking points` for every slide. It also preserves the synchronized `Purpose`, `Talk track`, `Ask`, `Bridge`, `Caveat`, and `Sources` blocks, together with the side talks, evidence-safe responses, follow-up probes, decision impacts, capture instructions, branches, rejoin points, and hold rules needed to run the meeting. The PowerPoint notes remain a concise projection; use this Markdown when preparing, presenting, navigating challenges, or handing the meeting to another facilitator.

- [Open the native 25-slide presentation](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/0)
- [Open the PowerPoint in the repository](https://github.com/tomqwu/apim/blob/main/presentations/kong-platform-journey-guided.pptx)
- [Read the canonical guided evaluation](48-kong-guided-evaluation.md)
- [Disposition the four early assessment gates](48-kong-guided-evaluation.md#four-early-assessment-gates)
- [Apply the evidence method](03-assessment-methodology.md)
- [Inspect the Kong platform strategy](47-kong-enterprise-platform-strategy.md)
- [Inspect the Kong option register](44-kong-multicloud-study-roadmap.md)
- [Inspect the migration strategy](35-mule-migration-strategy.md)
- [Inspect the Apigee A0–A6 migration roadmap](50-apigee-migration-strategy.md)
- [Use the Kong terminology crosswalk](../research/glossary.md#kong-terminology-crosswalk)
- [Inspect the Traceable security-adjunct evidence boundary](48-kong-guided-evaluation.md#traceable-by-harness-security-adjunct-feasibility)
- [Inspect the current PoC evidence boundary](../poc/README.md)

If this guide, the PowerPoint, or the native presentation differs from a canonical study, the canonical study wins. Do not publicly link the raw supplied input; the sanitized guided evaluation preserves the admissible decision context.

### Acronym and identifier reading rule

Every speaker-note card is independently enterable. At the top of each card, the native page therefore projects the canonical slide-local terms as **Full Name (ACRONYM)** before the detailed notes use shorthand. The card kicker introduces **Kong Guided Evaluation (KGE)**, and each visible slide title expands any slide-local shorthand it contains. Stable record identifiers keep their published code plus a plain-language descriptor; the guide never invents a long form for an internal ID.

Apply the same rule in meeting artifacts and follow-up documents: expand an unfamiliar acronym at its first visible use in every independently opened document, section, slide, table, or note. A linked glossary is supporting context, not a substitute for the first-use expansion.

## Opening the meeting

### Suggested opening script — 2 to 3 minutes

Good morning. Before we discuss architecture or products, I want to be precise about the decision this meeting can make.

We are deciding whether to **approve, amend, or hold a bounded and reversible Kong foundation**, together with the work needed to prove it before production scale. We are not selecting a universal product winner. We are not treating the historical score as independent evidence. We are not approving critical production scale today.

By the end of the session, we need a decision record—not simply agreement that the slides were reviewed. That record must say what is authorized now, what remains unauthorized, who is accountable, what evidence closes each material gap, and what result would stop or reverse the direction.

Four Early Assessment Gates must be dispositioned early. `EAG-01` is multicloud operating fit. `EAG-02` is reversibility and vendor dependency. `EAG-03` is fully allocated total cost of ownership. `EAG-04` is admission of the optional Kong-plus-Traceable solution profile for study. An unknown answer remains an evidence gap; it does not become a pass because the room prefers forward motion.

Throughout the discussion, I will label the evidence ceiling. Stakeholder input can explain intent. Evidence level one, `E1`, is a documented mechanism and can support test design. Evidence level two, `E2`, is a version-, contract-, or configuration-specific answer. Evidence level three, `E3`, is a repeatable result in the frozen target-shaped lab. Evidence level four, `E4`, is representative pilot evidence. We will not promote a claim without the artifact and review required for the higher level.

Challenges are welcome. If you disagree with a claim, please state what decision would change, what evidence would close the question, who should own it, and when it must return. We can branch to a detailed slide, but every branch must rejoin either the authorization decision on slide 6 or the evidence-outcome decision on slide 21.

Before we begin, please confirm the chair, scribe, evidence steward, and timekeeper. If no accountable decision owner is present, this becomes a working session and no authorization will be issued.

With that boundary clear, let us start with the decision question and then test the operating model that makes Kong directionally attractive.

### Opening talking points

- The meeting decides **approve, amend, or hold** for a bounded foundation and proof programme.
- Direction, documented capability, executed proof, and production authorization are different states.
- Four early gates must receive an explicit disposition, owner, evidence request, due gate, and hold condition.
- Challenges must identify decision impact and closure evidence; they do not become unscheduled rescoring debates.
- Confirm the decision owner and facilitation roles before slide 1.

## What the meeting must produce

The meeting succeeds only when it produces a decision record, not when it reaches the last slide. The chair should secure:

1. an explicit **approve, amend, or hold** answer for the bounded direction;
2. a precise statement of what is authorized now and what remains unauthorized;
3. confirmed, amended, or rejected target-model assumptions plus explicit dispositions for `EAG-01` multicloud, `EAG-02` reversibility/vendor dependency, `EAG-03` fully allocated TCO/cost efficiency, and `EAG-04` Kong-plus-Traceable solution-profile admission;
4. accountable public roles for the operating boundary, permanent duties, Mule and Apigee migration safety, the seven proof workstreams, scoring governance, terminology enablement, and independent review;
5. a closure artifact, threshold, independent reviewer, due gate, and stop rule for every material evidence gap;
6. recorded dissent and the evidence that could change the answer; and
7. an agreed next decision forum and date.

The meeting does **not** authorize critical production scale, prove a universal product ranking, change a score to preserve a preferred order, convert supplied scores into observed evidence, count a third-party integration as native gateway proof, commit synthetic roadmap dates, or declare documented capability to be executed behavior.

## Roles in the room

| Role | Responsibility during the meeting |
|---|---|
| Chair / decision owner | States the decision authority, protects non-goals, resolves or holds the decision, and reads back the final authorization. |
| Facilitator / presenter | Drives the chosen route, labels evidence states, uses challenge branches, and returns the room to slides 6 or 21. |
| Scribe | Maintains the decision, evidence-gap, action, dissent, and parking-lot ledgers in real time. |
| Evidence steward | Challenges unsupported promotion from stakeholder input or documentation to proof; confirms source, result, version, topology, and limitations. |
| Timekeeper | Enforces segment timeboxes and signals when a challenge must be assigned, parked, or moved to the appendix. |
| Accountable challengers | Security/IAM, architecture, platform/database, SRE, Mule and Apigee migration, domain, sourcing, FinOps, service-management, privacy, product enablement, and independent-assurance leads test the claims their roles will own. |

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
- Keep the original scorecard intact as historical input; any recalculation is a governed follow-up with exact options, approved dimensions and weights, a rubric, evidence floor, confidence treatment, scorer panel, sensitivity, dissent, and sign-off.
- Treat Traceable by Harness as a third-party security-adjunct hypothesis. It earns no platform score and supports no security, traceability, cost, or production conclusion until GEP-07 is executed and independently reviewed.
- Treat `EAG-01`–`EAG-04` as early scope-and-evidence gates. A meeting disposition freezes the question, owner, evidence request, and hold condition; it does not prove multicloud fit, a clean exit, cost efficiency, or Kong-plus-Traceable feasibility.
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
| Open and target model | 1–3 | 12 min | Confirm the decision question and target inputs; disposition all four early gates; then review weight concerns. |
| Options and bounded decision | 4–8 | 20 min | Approve or amend the leading target, custody benchmark, true exit, and funded duties. |
| Architecture and adoption | 9–13 | 19 min | Confirm topology questions, degraded-state policy, accountable owners, and gate sequence. |
| Migration | 14–16 | 12 min | Approve the responsibility taxonomy, coexistence, route-back, and wave gates. |
| Production proof | 17–21 | 22 min | Accept the evidence baseline, fund GEP-01–07, and pre-commit possible outcomes. |
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

Use slides [1](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/0), [6](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/5), [12](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/11)–[18](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/17), [20](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/19), and [21](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/20). Required output: source-specific Mule or Apigee object/state ownership, cohort boundaries, business probes, identity and state reconciliation, route-back, wave gates, dependency-zero authority, and migration proof owners. Use the [Kong terminology crosswalk](../research/glossary.md#kong-terminology-crosswalk) when a familiar source-platform noun is being treated as a one-to-one target mapping.

### 30-minute executive route

Use slides [1](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/0), [2](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/1), [4](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/3), [6](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/5), [8](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/7), [13](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/12), [17](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/16), [18](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/17), and [21](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/20). The output is authorization scope, evidence funding, decision rights, and stop rules—not technical or production approval.

### Audit challenge route

Use slides [2](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/1)–[5](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/4), then [22](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/21)–[25](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/24), and rejoin at [6](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/5). The output is an explicit early-gate disposition plus a corrected or challenged input ledger, not a production conclusion.

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
| “Multicloud and lock-in were missing, so re-score it to make the result more convincing” | [2](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/1) → [3](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/2) → [5](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/4) → [25](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/24) | `EAG-01` and `EAG-02` put multicloud and clean exit/vendor dependency into the opening assessment. Their early dispositions create scope, owners, evidence requests, and HOLD conditions; they do not create ratings. Make the next calculation more auditable, not more favorable: approve exact options, mandatory gates, dimensions, weights/ranges, rubric, evidence floor, confidence, scorers, sensitivity, dissent, and decision rule before changing any total. | 6 |
| “A low license price proves cost efficiency” | [2](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/1) → [3](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/2) → [24](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/23) | `EAG-03` requires one time horizon and denominator across meters/quotes, platform labor, infrastructure, HA/DR, telemetry, security adjuncts, support, migration, dual run, incident exposure, custody switch, and exit. A public price or early disposition is not a TCO result. | 6, then 21 |
| “Why not Apigee, MuleSoft, or APIM?” | [4](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/3) → [22](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/21)–[24](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/23) | Each is a conditional operating-model counterfactual. State when it becomes stronger and convert that condition into symmetric evidence. | 6 |
| “Why self-managed rather than Konnect?” | [7](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/6) → [8](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/7) → [12](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/11) → [20](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/19) | Self-managed is a custody preference with permanent duty. Konnect is the same-vendor custody benchmark; a true non-Kong exit remains separate. | 21 |
| “Who carries the control-plane liability?” | [8](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/7) → [12](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/11) → [24](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/23) | The public study can allocate operational accountability and risk exposure for CP/PostgreSQL/PKI/plugin/license/audit/upgrade/restore/on-call duties. It does not make a legal-liability determination. Contractual allocation requires exact support and commercial evidence; legal liability requires counsel in the approved restricted process. | 6 or 21 |
| “Does hybrid keep running if the control plane fails?” | [9](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/8)–[11](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/10) → [17](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/16)–[19](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/18) | Cached proxying does not prove restart, clean scale, mutation, urgent revoke, reconnect, recovery, or business correctness. | 21 |
| “Terraform and decK already solve APIOps” | [10](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/9) → [18](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/17)–[19](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/18) | Tool presence is documented mechanism. The target must prove authority, deletion scope, promotion, drift, rollback, active digest, and reconciliation. | 21 |
| “Gateway authentication passed, so enterprise IAM is covered” | [10](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/9) → [12](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/11) → [18](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/17) → [19](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/18)–[21](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/20) | One authentication path does not prove organization-wide access lifecycle. Workforce, workload, consumer, and service-account inventory; join/move/leave; revoke and rotate; expiring break-glass; negative tests; attribution; owners; and independent review remain unproved. | 21 |
| “Why not migrate Mule packages directly?” | [14](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/13)–[16](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/15) | The migration unit is responsibility and state. Edge extensibility does not prove that durable or stateful business logic belongs in the gateway. | 20, then 21 |
| “Can we migrate Apigee by exporting proxy bundles?” | [16](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/15) → [22](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/21) | A proxy bundle is source evidence, not the full migration denominator. A0–A6 must also reconcile shared flows/policies, products/apps/credentials, KVM/quota/cache, targets/TLS, environment and hostname attachment, portal, analytics/audit, and Hybrid runtime dependencies before route-back or dependency zero can be claimed. | 21 |
| “What Kong object replaces this Mule or Apigee object?” | [4](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/3) → [16](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/15) | Use the terminology crosswalk as a nearest analogue, never a one-to-one conversion. Map behavior, state, authority, lifecycle, evidence, and ownership; then prove semantic parity. | 16, then 21 |
| “The PoC already proves it” | [17](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/16) → [18](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/17) | Five local checks ran and eleven did not; the 28 atomic cases are separate and unexecuted; target E3/E4 evidence remains zero. | 19–21 |
| “Kong documents MCP, A2A, and AI routing, so AI fit is proved” | [18](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/17) → [23](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/22) | Documentation permits a test design. The separately versioned agentic study cannot inflate confidence in the core gateway decision. | 19, then 21 |
| “Traceable makes Kong security and traceability fit proven” | [2](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/1) → [3](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/2) → [18](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/17) → [23](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/22) | `EAG-04` first decides whether to admit, amend, reject, or hold the optional `KP-SMH1 + GSA-01` composite profile. Traceable is a third-party adjunct with an `E1` plugin/agent integration path, not a gateway contender or native capability verdict. GEP-07 must resolve exact BOM/support, data path, protocol/body/streaming coverage, sync/async and fail behavior, overhead/scaling, privacy, evidence correlation, upgrade/rollback, uninstall, and comparison with the security baseline. | 19, then 21 |
| “Kong is cheaper” or “lock-in is low” | [2](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/1) → [3](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/2) → [24](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/23) → [20](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/19) | `EAG-02` and `EAG-03` keep clean exit and fully allocated TCO in the opening assessment. Require exact meters and quotes, labor, infrastructure, HA/DR, telemetry, security adjuncts, support, migration, dual run, incident exposure, custody switch, representative non-source rebuild, and clean-exit evidence before either claim can influence authorization. | 21 |
| “Can we approve production now?” | [6](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/5) → [17](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/16)–[21](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/20) | No. The admissible decision is a reversible foundation and proof programme. Critical scale requires reviewed target-shaped evidence. | 21 |

## Slide-by-slide facilitation index

Use the index below as the compact discussion control. The complete point-of-use notes and side talks follow it.

### Phase 1 — Why now

| Slide | Facilitation job and ask | Likely challenge and evidence reminder | Capture, branch, or rejoin |
|---|---|---|---|
| [1 · KGE-01](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/0) | Establish a decision-and-proof meeting. Ask whether the room accepts bounded direction plus proof as the decision question. | “Is this predetermined?” Stakeholder direction is not independent proof. | Capture decision owner and non-goals. Never skip. Disputed assumptions → 2; aligned → 6. |
| [2 · KGE-02](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/1) | Confirm or amend the stated target inputs, then explicitly disposition `EAG-01` multicloud, `EAG-02` clean exit/vendor dependency, `EAG-03` fully allocated TCO, and `EAG-04` Kong-plus-Traceable admission. | “This is not our current state” or “Traceable is already part of Kong.” These are target and scope inputs to confirm, not observed inventory, native capability, ratings, or executed proof. | Material target dispute or an undispositioned gate means HOLD bounded authorization; create an owner/evidence action for each open gate. |
| [3 · KGE-03](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/2) | Review the provisional 60/40 planning weights for multicloud, robustness, IAM/traceability, reversibility, full TCO, and control-plane responsibility while keeping Traceable as an unscored composite gate. | The weights are assumptions, every new product rating remains unknown, and early-gate disposition does not close the later proof obligation. | Record gate and weight accept/amend/reject/unknown states; assign decision-owner, architecture, security, FinOps, scorer, and assurance roles; uncertainty → 5 or 25; decision → 6. |

### Phase 2 — Options and decision

| Slide | Facilitation job and ask | Likely challenge and evidence reminder | Capture, branch, or rejoin |
|---|---|---|---|
| [4 · KGE-04](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/3) | Agree the business conditions under which each option becomes stronger. | “The feature list is biased or incomplete.” These are conditional archetypes, not a rank. | Convert product debate into symmetric evidence; appendix → 22–24; return → 6. |
| [5 · KGE-05](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/4) | Preserve the historical score and expose the provisional uncertainty envelope. | “Make the score more convincing.” The 60/40 scenario yields 55.8–95.8, 51.3–91.3, and 46.2–86.2; overlapping ranges mean rank instability, not a new score. | Record permitted use, scenario amendments, and roles that can replace unknowns with common evidence. Audit → 25; decision → 6. |
| [6 · KGE-06](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/5) | Decide separately on `KP-SMH1`, one reversible foundation, GEP-01–07, custody/exit benchmarks, and the block on critical scale. | “Why choose before PoC?” The authorization is foundation plus proof, not production. | Record approve/amend/hold for every row and dissent. Return here at close. |
| [7 · KGE-07](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/6) | Confirm self-managed lead, Konnect custody benchmark, and a true non-Kong exit as distinct boundaries. | “Konnect is the exit.” It is a same-vendor custody switch, not platform exit. | Name exact-option, custody-benchmark, and exit owners. Continue → 8. |
| [8 · KGE-08](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/7) | Confirm role ownership and funded capacity for control-plane, PostgreSQL, PKI, plugin/license, release, restore, audit, support, and on-call duty. | “Who carries the liability?” The slide allocates operating accountability and risk exposure; legal liability requires counsel and exact contracts. | Capture public role RACI, capacity, sourcing, support, and TCO gaps. No accountable owner = HOLD. |

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
| [16 · KGE-16](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/15) | Adopt Apigee A0–A6 as the explicit object/state migration rail; keep Mule M0–M5 as its responsibility/state counterpart. | “Exported proxies are the Apigee roadmap.” Bundles omit product/app/credential, KVM/quota/cache, portal, analytics, placement, and Hybrid state. Names are not semantic mappings. | Capture source archetype, denominator, semantic map, hard-slice corpus, coexistence ledger, timed route-back, and dependency-zero authority. |

### Phase 5 — Production proof

| Slide | Facilitation job and ask | Likely challenge and evidence reminder | Capture, branch, or rejoin |
|---|---|---|---|
| [17 · KGE-17](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/16) | Establish the exact current evidence baseline. | “5/16 means 31% ready” or “28 means more completed proof.” The 16 register and 28 atomic cases are non-additive; target E3/E4 is zero. | Capture agreement or disputed result IDs. Continue → 18. |
| [18 · KGE-18](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/17) | Authorize GEP-01–07 with role owner, environment/BOM, measure, threshold, raw artifact, reviewer, and stop rule. | Traceable is an `E1` third-party adjunct hypothesis, not platform proof; GEP-07 must resolve exact versions/support, data and failure paths, coverage, overhead, privacy, lifecycle, and baseline parity. | Missing threshold, artifact, reviewer, or stop rule = HOLD. Traceable/AI branch → 23; outcomes → 19–20. |
| [19 · KGE-19](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/18) | Agree thresholds, artifacts, cadence, and owners for KO-1–KO-5. | “The mechanism should be enough.” These are proposed target forms, not achieved results. | Capture missing thresholds and artifact schemas. Continue → 20. |
| [20 · KGE-20](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/19) | Agree KO-6–KO-11 and identify the most likely scale blocker; treat KO-7 as security traceability and evidence safety, not a product label. | “Traceable provides traceability, so KO-7 passes.” A mechanism cannot substitute for request/config/security/business correlation, quantified gaps, and prohibited-field control. | Capture likely blocker, outcome owner, data, cadence, evidence gaps, adjunct dependency, cost model, and exit rehearsal. |
| [21 · KGE-21](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/20) | Pre-commit scale, narrow, switch custody, exit, and hold authority. | “The selection is already fixed.” No outcome is preselected; negative evidence must change scope or direction. | Capture decision rights and non-waivable gates. Return to 6 and close. |

### Phase 6 — Audit appendix

| Slide | Facilitation job and ask | Likely challenge and evidence reminder | Capture, branch, or rejoin |
|---|---|---|---|
| [22 · KGE-22](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/21) | Turn architecture, multicloud, scalability, and robustness labels into symmetric proof questions. | Supplied labels are edition- and version-sensitive; scalability and robustness remain explicitly unscored. | Assign architecture/SRE evidence roles; do not rescore in the room. Rejoin → 4 or 6. |
| [23 · KGE-23](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/22) | Assign evidence for management, AI, and security traceability, including GEP-07 Kong-plus-Traceable. | A documented plugin/agent path is feasibility, not a gateway score, security result, or production recommendation. | Capture exact BOM/use cases, support, data/failure path, performance, lifecycle, artifact, reviewer, and role owner. Workstream → 18. |
| [24 · KGE-24](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/23) | Assign normalized pricing, lock-in/rebuild, control-plane duty, adjunct, migration, dual-run, and exit evidence. | Public price pages and architecture labels do not create comparable TCO or reversibility evidence. | Assign FinOps, sourcing, platform/SRE, and migration owner roles. Outcomes → 21; scoring → 25. |
| [25 · KGE-25](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/24) | Audit the 60/40 planning weights, unknown GRS ranges, mechanical envelopes, and HOLD disposition. | A midpoint is only a drawing placeholder; numerical-input coverage is 60% and common score-capable evidence coverage is 0%. | Record scenario amendments, evidence/scorer ownership, dissent, and due gate. Never finish here; return → 6 or 21. |

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

We start from the stated target operating model, disposition four early gates for multicloud, clean exit/vendor dependency, fully allocated TCO, and the optional Kong-plus-Traceable solution profile, and then make the ownership, migration, execution evidence and production gates explicit.

##### Speaker script

*If you delivered the full meeting opening, use the first paragraph as the handoff and move directly to the final paragraph. Use the complete script when slide 1 is the opening.*

Welcome to the Kong Guided Evaluation. The question in front of us is deliberately narrower than “Which application programming interface platform wins?” We are deciding whether to approve, amend, or hold a bounded Kong foundation and the proof programme required before production scale.

The journey begins with the stated operating model because that is what makes Kong appear directionally attractive. We then disposition four Early Assessment Gates: multicloud operating fit, reversibility and vendor dependency, fully allocated total cost of ownership, and admission of the optional Kong-plus-Traceable solution profile. From there, we test the operating boundary, permanent ownership, architecture, adoption, MuleSoft and Apigee migration, and target-shaped production evidence.

The important distinction is between choosing a direction and proving an outcome. The supplied evaluation is stakeholder input. It can explain why the organization prefers Kubernetes, Git-reviewed delivery, platform ownership, and distributed runtimes. It cannot independently prove product superiority or production readiness.

If this feels predetermined, tell us which target assumption or counter-evidence would reverse the direction. We will record that condition and turn it into a proof obligation. Today’s acceptable result is an explicit bounded authorization, amendment, or hold—not an unqualified endorsement.

##### Talking points

- Direction plus proof, not product marketing.
- The four early gates must be dispositioned before bounded authorization.
- Critical production scale remains outside today’s authority.

##### Ask

Align on the decision question: disposition the early gates, then approve a bounded Kong direction and proof programme—not critical production scale.

##### Bridge

First, make the target operating model and the four early assessment gates visible because they drive scope, evidence requests, scoring governance, and platform fit.

##### Caveat

The sanitized supplied evaluation is stakeholder input. Its ratings and recommendation are not independent comparative proof.

##### Sources

- Canonical decision content: [Kong guided evaluation](48-kong-guided-evaluation.md), including [Four early assessment gates](48-kong-guided-evaluation.md#four-early-assessment-gates).
- Supporting repository interpretation: [Kong enterprise platform deployment strategy](47-kong-enterprise-platform-strategy.md) and [Mule migration strategy](35-mule-migration-strategy.md).
- Official contextual mechanisms (`E1` only): [Kong deployment topologies](https://developer.konghq.com/gateway/deployment-topologies/), [Kong hybrid mode](https://developer.konghq.com/gateway/hybrid-mode/), [Traceable Kong integration](https://docs.traceable.ai/kong), [Harness WAAP plugin](https://developer.konghq.com/plugins/harness-waap/), and [Kong pricing](https://konghq.com/pricing).

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

#### KGE-02 · The operating model and four early gates drive the decision

- **Phase:** `KGE-P1 — Why now`
- **Native route:** [Open slide 2](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/1) (`#/present/kong-platform-journey-guided/1`)
- **Timebox:** 4 minutes
- **Evidence state:** Stakeholder input plus early-gate contract
- **Meeting job:** Confirm, amend, or reject the stated target inputs; disposition `EAG-01`–`EAG-04`; and name accountable owners and evidence requests.

##### Purpose

Explain why the same product can be a good or poor choice depending on the target operating model, and force four material concerns into the assessment before bounded authorization.

##### Talk track

The supplied assessment favors Kubernetes, GitOps, platform engineering, self-service, observability, multicloud placement and emerging AI traffic governance. Those priorities explain why Kong scores well, but they must be confirmed with accountable owners. Before the room interprets scores or funds a proof programme, it must also disposition four early gates: `EAG-01` multicloud operating fit, `EAG-02` reversibility and vendor dependency, `EAG-03` cost efficiency and fully allocated TCO, and `EAG-04` admission of the optional `KP-SMH1 + GSA-01` Kong-plus-Traceable solution profile.

##### Speaker script

This slide separates the target model from evidence about whether a product meets it. Read the nine target-model records in three lanes. Delivery records cover Azure Kubernetes Service, Spring Boot modernization, and Git-reviewed application programming interface operations. Platform records cover product ownership, internal-platform integration, and governed self-service. Control records cover organization-wide security and observability, multicloud and private placement, and artificial-intelligence traffic governance.

These are target inputs to confirm or amend; they are not an observed current-state inventory. Before we use them to support a direction, we must disposition four Early Assessment Gates. The first asks whether the exact placements and dependencies really support multicloud operations. The second separates a custody change from a true non-Kong exit. The third requires a common, fully allocated total cost of ownership denominator. The fourth decides whether the self-managed hybrid target plus the Traceable security-adjunct hypothesis is admitted for study.

For every gate, the required output is confirm, amend, reject, or unknown—plus an accountable role, evidence request, due gate, and hold condition. Admission creates work; it does not create proof or score.

##### Talking points

- Confirm the target model before interpreting product fit.
- Early Assessment Gates are scope-and-evidence gates, not product ratings.
- Traceable remains an optional composite profile, not native Kong capability.

##### Ask

Confirm or amend the nine target-state inputs. Then confirm, amend, reject, or leave explicitly unknown each early gate, with a public role owner, evidence request, due gate, and hold condition.

##### Bridge

The next slide shows how the priorities were encoded in the supplied scorecard, where the added dimensions remain unknown and Traceable stays outside the platform score.

##### Caveat

These are stakeholder-stated objectives and early scope dispositions; the document does not provide a verified workload inventory, multicloud outcome, clean exit, normalized TCO, or executed Kong-plus-Traceable result. Early disposition creates a proof obligation, not evidence that the gate passed.

##### Sources

- Canonical target and gate records: [Kong guided evaluation — Stated target operating model](48-kong-guided-evaluation.md#stated-target-operating-model) and [Four early assessment gates](48-kong-guided-evaluation.md#four-early-assessment-gates).
- Official contextual mechanisms (`E1` only): [Kong deployment topologies](https://developer.konghq.com/gateway/deployment-topologies/), [Kong hybrid mode](https://developer.konghq.com/gateway/hybrid-mode/), [Traceable Kong integration](https://docs.traceable.ai/kong), [Harness WAAP plugin](https://developer.konghq.com/plugins/harness-waap/), and [Kong pricing](https://konghq.com/pricing).

##### Listen for

“This is not our current state,” “these priorities are incomplete,” “Traceable is already a Kong capability,” “multicloud is just deployment,” “lock-in is low,” or “license price proves cost efficiency.”

##### Evidence-safe response

Correct: the slide states target and early-gate inputs to disposition, not observed outcomes. `EAG-04` admits or rejects an optional composite profile; it never turns Traceable into native Kong capability or score. Amend, reject, or leave unknown any input or gate that lacks accountable sponsorship and a closure path.

##### Follow-up probe

Which target input or early gate changes, who owns it, what exact option/profile is in scope, and what evidence would prove multicloud fit, a clean exit, fully allocated TCO, or Kong-plus-Traceable feasibility rather than merely restating an aspiration?

##### Decision impact

A material target-model dispute or unresolved early gate can reverse the apparent platform direction, exclude the composite profile, narrow the authorized foundation, or hold the decision before scoring.

##### Capture

For every target input and `EAG-01`–`EAG-04`, record confirm/amend/reject/unknown, exact scope, public role owner, evidence request, due gate, hold condition, and dissent. For `EAG-04`, record whether `KP-SMH1 + GSA-01` is admitted as an optional composite profile without platform-score credit.

##### Branch/rejoin

Continue to slide 3 for weighting and unscored-adjunct implications. For deeper multicloud, adjunct, exit, or TCO challenges, branch to slides 22–24. If a dispute invalidates the decision basis, return to slide 6 only after an owner and closure action are recorded.

##### HOLD/park

HOLD bounded authorization when a material target input or applicable early gate is undispositioned, unknown without accountable closure, or being treated as already proved. Park only bounded inventory or evidence work with a due gate and slide-6 re-entry.

#### KGE-03 · The scorecard favors cloud-native delivery

- **Phase:** `KGE-P1 — Why now`
- **Native route:** [Open slide 3](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/2) (`#/present/kong-platform-journey-guided/2`)
- **Timebox:** 4 minutes
- **Evidence state:** Stakeholder input plus early-gate contract
- **Meeting job:** Review the provisional 60/40 planning weights, preserve the four early-gate dispositions, and assign approval ownership without inventing product ratings or adjunct credit.

##### Purpose

Make the historical weighting model transparent, expose the dimensions required for a governed re-score, and keep Traceable as a separate unscored solution-profile gate.

##### Talk track

Eight supplied categories sum to 100%, and Kubernetes plus GitOps carry 35%. The provisional planning scenario rebases those historical categories to 60% and allocates 40% across multicloud, scalability/robustness, enterprise IAM and traceability, reversibility/vendor dependency, fully allocated TCO, and control-plane operating responsibility. This makes the meeting feedback visible without changing the historical ratings. The 40% split is an assumption to approve or amend; every new product rating remains unknown. `EAG-04` stays separate: admitting `KP-SMH1 + GSA-01` for GEP-07 study cannot add native Kong points.

##### Speaker script

This slide explains why the supplied scorecard points toward Kong without claiming that it proves Kong is best. The eight supplied-weight records total 100 percent. Kubernetes and Git-reviewed operations alone carry 35 percent, so the historical model strongly reflects a cloud-native delivery preference.

The proposed planning scenario does not rewrite those ratings. It rebases the historical block to 60 percent and reserves 40 percent for six missing dimensions: multicloud operating fit; scalability and robustness; enterprise identity and access management plus end-to-end traceability; reversibility and vendor dependency; fully allocated total cost of ownership; and control-plane operating responsibility. Every product rating in that new block remains unknown.

The early gates put these concerns into the meeting now, but their disposition cannot manufacture a score. Admitting the optional Kong-plus-Traceable profile for a security-adjunct study also gives Kong no native platform points.

The decision here is whether this is the right governed scoring specification: exact options, mandatory gates, evidence floor, rubric, scorers, confidence treatment, sensitivity analysis, dissent, and approval authority. The objective is a more auditable comparison, not a more convincing number.

##### Talking points

- Historical weighting explains preference; it does not prove fit.
- Six missing dimensions remain wholly unscored.
- Optional security tooling cannot inflate the native gateway score.

##### Ask

Approve, amend, or reject the provisional weights and double-counting rules; confirm that `EAG-01`–`EAG-03` remain early gates as well as later evidence dimensions and that `EAG-04` remains unscored; then assign the exact-option boundary, mandatory gates, evidence floor, scorer and approver panel, rating authority, confidence treatment, sensitivity method, dissent rule, and permitted decision use.

##### Bridge

Now compare operating-model fit rather than treating products or optional adjuncts as interchangeable feature bundles.

##### Caveat

The provisional weights are a scenario, not an approved model or revised ranking. The new ratings remain unknown, 30 mandatory gates remain unknown, and common score-capable evidence coverage is 0%. An early-gate disposition is meeting governance input; it cannot narrow a rating range or close an `E2`–`E4` proof obligation.

##### Sources

- Canonical weighting record: [Kong guided evaluation — Supplied weighting model](48-kong-guided-evaluation.md#supplied-weighting-model).
- Feedback-to-criteria mapping and scenario: [Meeting-feedback assurance crosswalk](48-kong-guided-evaluation.md#meeting-feedback-assurance-crosswalk), [Provisional weighting and uncertainty scenario](48-kong-guided-evaluation.md#provisional-weighting-and-uncertainty-scenario), and [Proposed governed re-score](48-kong-guided-evaluation.md#proposed-governed-re-score).
- Early scope and evidence boundary: [Four early assessment gates](48-kong-guided-evaluation.md#four-early-assessment-gates) and [Traceable by Harness security-adjunct feasibility](48-kong-guided-evaluation.md#traceable-by-harness-security-adjunct-feasibility).
- Existing score governance: [Decision-matrix scoring guide](../decision-matrix/scoring-guide.md).
- Official contextual mechanisms (`E1` only): [Kong deployment topologies](https://developer.konghq.com/gateway/deployment-topologies/), [Kong hybrid mode](https://developer.konghq.com/gateway/hybrid-mode/), [Traceable Kong integration](https://docs.traceable.ai/kong), [Harness WAAP plugin](https://developer.konghq.com/plugins/harness-waap/), and [Kong pricing](https://konghq.com/pricing).

##### Listen for

“The model is subjective,” “Kubernetes and GitOps bias the answer,” “multicloud, lock-in, or cost efficiency were omitted from the whole assessment,” “Traceable should increase Kong's score,” or “re-score it to make the recommendation more convincing.”

##### Evidence-safe response

The original weights are stakeholder choices and remain an audit record. Multicloud, vendor dependency, and cost efficiency now appear both as opening gates and later evidence dimensions; the early disposition does not create a rating. Traceable remains an optional composite profile with no native Kong score. The correction is a more auditable decision process, not a more favorable total. No score changes until exact options, mandatory gates, dimensions, weights/ranges, rubric, evidence floor, confidence, scorers, sensitivity, and dissent are approved.

##### Follow-up probe

Which proposed dimension or early gate could change the authorization, what score-capable or admission evidence would it require, and which decision-owner, enterprise-architecture, security, FinOps, and independent-assurance roles approve the method?

##### Decision impact

Until the governed model is approved and run, the historical ranking can explain preference but cannot establish rank stability. If plausible ranges, evidence confidence, bounds, or maximum regret reverse the direction, the room must make that trade-off explicitly.

##### Capture

Record the `EAG-01`–`EAG-04` dispositions, the accepted `GRS-01`–`GRS-06` dimensions, exact options, mandatory gates, evidence floor, rubric owner, weight/range approver, scorer roles, confidence and unknown treatment, sensitivity and bounds method, dissent, due gate, and permitted decision use. Use public roles only; keep named-person assignment in the approved restricted system.

##### Branch/rejoin

Branch to slide 5 for score implications or slide 25 for the raw audit. Rejoin at slide 6.

##### HOLD/park

HOLD score-based authorization while an applicable early gate is undispositioned or any exact option, mandatory gate, dimension, weight/range, rubric, evidence floor, confidence rule, scorer role, sensitivity method, dissent rule, or approval authority remains unresolved. Park recalculation only with a governed work item and slide-6 re-entry.

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

##### Speaker script

Here we are deliberately not comparing feature counts. The four option archetypes describe conditions under which each option could become the stronger operating-model fit.

Kong leads when Kubernetes, Git-reviewed operations, platform engineering, management-state custody, and distributed runtime ownership dominate. Apigee becomes stronger when external application programming interface product management, governance, analytics, and Google-aligned management services dominate. MuleSoft becomes stronger when Anypoint remains the strategic integration and application programming interface platform. Azure API Management becomes stronger when Azure consolidation matters more than platform neutrality.

Those are counterfactual hypotheses, not verified rankings. “Keep as a counterfactual” means preserve an option as a condition that could change the answer. Excluding it from the leading build is a scope choice, not a verdict that the product lacks capability.

If someone believes a feature list is incomplete or biased, the useful response is not to trade brochures. State the exact edition, topology, use case, operating condition, and measurable outcome that would reverse the direction. We can then create one symmetric evidence request and apply it to all admitted options. The output of this slide is a set of reversal conditions and proof obligations—not a winner declared from qualitative labels.

##### Talking points

- Compare operating models, not inventories of features.
- Every contender remains a legitimate counterfactual under stated conditions.
- Exclusion from the leading build is not a capability verdict.

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

#### KGE-05 · Preserve the historical score; expose the uncertainty

- **Phase:** `KGE-P2 — Options and decision`
- **Native route:** [Open slide 5](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/4) (`#/present/kong-platform-journey-guided/4`)
- **Timebox:** 3 minutes
- **Evidence state:** Provisional scenario over stakeholder input
- **Meeting job:** Preserve the corrected historical arithmetic and show why the new dimensions leave the ranking unstable until evidence replaces their unknown ranges.

##### Purpose

Use the scorecard transparently without overstating its evidentiary value.

##### Talk track

The historical inputs recalculate to 93 for Kong, 85.5 for Apigee, and 77 for MuleSoft. Under the provisional 60/40 weighting, their historical-input contributions are 55.8, 51.3, and 46.2. Leaving the added 40% honestly unknown produces ranges of 55.8–95.8, 51.3–91.3, and 46.2–86.2. The overlap is the finding: a modest advantage on the missing dimensions can reverse the historical order, so the deck does not publish a new decision score.

##### Speaker script

This slide keeps the historical scorecard visible but gives it an honest evidence ceiling. Recalculation preserves Kong at 93 and corrects Apigee to 85.5 and MuleSoft to 77. Those remain assertion-only inputs because the original model has no approved rubric, common evidence set, exact edition freeze, confidence method, or independent scorer panel.

Under the provisional 60/40 scenario, the fixed historical contributions become 55.8 for Kong, 51.3 for Apigee, and 46.2 for MuleSoft. The proposed re-score block remains unknown from zero to 40 points, creating the displayed envelopes. The ranges overlap. That is the useful finding: each option can still rank first under permitted unknown completions, so the current ordering is unstable.

The midpoint shown for visualization is not a score. The endpoints are not forecasts or probabilities. Strong historical inputs also cannot average away an unknown or failed mandatory gate.

If the request is to make the recommendation more convincing, the answer is better governance and common evidence—not tuned weights. We must decide how the historical score may be used, who can replace unknowns, and which independent assurance role confirms that the approved method was followed.

##### Talking points

- Correct arithmetic does not improve evidence confidence.
- Overlapping envelopes expose rank instability.
- No new decision score exists until the governed comparison is executed.

##### Ask

Confirm that the historical score remains directional input only, review the scenario assumptions, and assign the evidence and scorer roles that can narrow the ranges without protecting a preferred order.

##### Bridge

We can now state a bounded decision that preserves falsifiability.

##### Caveat

The arithmetic scenario has been run; the governed product comparison has not. The midpoint is not a score, the endpoints are not forecasts, and the historical values remain unverified `E0` input rather than an independent benchmark or production-fit result.

##### Sources

- Canonical arithmetic audit: [Kong guided evaluation — Supplied scoring audit](48-kong-guided-evaluation.md#supplied-scoring-audit).
- Scenario and pending score governance: [Kong guided evaluation — Provisional weighting and uncertainty scenario](48-kong-guided-evaluation.md#provisional-weighting-and-uncertainty-scenario), [Proposed governed re-score](48-kong-guided-evaluation.md#proposed-governed-re-score), and [Decision-matrix scoring guide](../decision-matrix/scoring-guide.md).
- Official contextual mechanisms (`E1` only): [Kong deployment topologies](https://developer.konghq.com/gateway/deployment-topologies/), [Apigee hybrid 1.16](https://docs.cloud.google.com/apigee/docs/hybrid/v1.16/what-is-hybrid), [MuleSoft Omni Gateway](https://docs.mulesoft.com/gateway/latest/), and [Azure API Management self-hosted gateway](https://learn.microsoft.com/en-us/azure/api-management/self-hosted-gateway-overview).

##### Listen for

“A score of 93 proves fit,” “the corrected totals invalidate the whole exercise,” or “change the criteria and ratings until the recommendation is more convincing.”

##### Evidence-safe response

The correction makes the historical input auditable. It does not create exact options, mandatory-gate results, a rubric, common evidence, confidence, sensitivity, bounds, maximum regret, or an executed comparison. A governed re-score is valuable only if it can expose instability or reverse the direction; it must not be tuned to defend a preferred rank.

##### Follow-up probe

Should the historical score remain an explanatory input, what evidence ceiling applies, and which independent scoring-assurance role will attest that the future recalculation used the pre-approved method?

##### Decision impact

The score may explain preference but cannot offset an unknown or failed mandatory gate. Until the governed recalculation closes, no new total can influence option authorization.

##### Capture

Record acceptance or dispute of the arithmetic, permitted use, exact-option and mandatory-gate prerequisites, approved dimensions and weight ranges, rubric, evidence floor, confidence/unknown treatment, scorer and approver roles, sensitivity, bounds/regret method, dissent, assurance reviewer, and due gate.

##### Branch/rejoin

Branch to slide 25 for raw inputs; rejoin at slide 6.

##### HOLD/park

HOLD any attempt to convert the historical score into selection or production approval, or to change weights/ratings before the governed method closes. Park recalculation only with public role owners, an approved specification, and a slide-6 re-entry.

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

##### Speaker script

This is the main authorization slide, and the rows need separate decisions. First, freeze the self-managed hybrid target as the leading exact option to test—not as a universal winner. Second, authorize one reversible foundation with named owners and explicit support, recovery, trust, change, evidence, and route-back obligations. Third, fund the seven proof workstreams, each with a measure, threshold, artifact, independent reviewer, and stop rule. Fourth, allow only bounded MuleSoft or Apigee migration cohorts with coexistence and route-back. Fifth, preserve Konnect as the same-vendor custody benchmark and a true non-Kong exit as a separate obligation.

What remains unauthorized is equally important: critical production scale, broad migration factories, or conclusions based only on documentation, integrations, and scripts.

The evidence progression is explicit. A version- or contract-specific answer can close a narrow question. Repeatable target-shaped laboratory evidence can prove behavior inside the frozen boundary. Representative pilot evidence is required for the strongest pre-scale conclusion.

If the challenge is “Why choose before the proof of concept?”, the answer is that we are choosing what to build and test reversibly. For each row, I need an approve, amend, or hold decision and the evidence that could change it.

##### Talking points

- Authorize foundation and proof—not critical scale.
- Decide separately on target, foundation, proof, migration, and alternatives.
- Every authorization remains reversible and evidence-gated.

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

Record approve/amend/hold for the exact target, foundation, GEP-01–07, custody benchmark, true exit, and production-scale block, including dissent.

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

##### Speaker script

This slide separates three operating boundaries that are easy to blur together.

The leading boundary is self-managed hybrid: the enterprise operates the management boundary while data planes serve requests in approved locations. The second is the Konnect custody benchmark: Kong operates the control plane and database while customer-hosted data planes remain. That is a same-vendor custody switch, not an exit. The third is a true platform exit: rebuild a representative application programming interface, policy, identity, evidence, and runtime boundary on a non-Kong target, prove route-back, and account for semantic loss.

A managed-runtime multicloud option, which also moves runtime custody, is a different benchmark and should not be substituted for Konnect.

The question is not whether self-management sounds like “more control.” The question is which exact custody, sovereignty, offline, support, recovery, or operating condition makes each boundary preferable—and what evidence permits a safe switch. Current official documentation can define mechanisms to test, but it cannot establish operational fit.

If someone says “Konnect is our exit,” correct the category: it changes custody within Kong. A non-Kong reconstruction is the evidence needed to test vendor dependency. Name separate owners and switching evidence for all three boundaries.

##### Talking points

- Self-managed lead, Konnect custody switch, and non-Kong exit are distinct.
- Same-vendor custody transfer does not prove portability.
- Each boundary needs its own owner, trigger, and route-back evidence.

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

#### KGE-08 · Control-plane custody transfers operating accountability

- **Phase:** `KGE-P2 — Options and decision`
- **Native route:** [Open slide 8](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/7) (`#/present/kong-platform-journey-guided/7`)
- **Timebox:** 4 minutes
- **Evidence state:** Proposed target
- **Meeting job:** Confirm funded role ownership for permanent CP, PostgreSQL, PKI, plugin/license, release, restore, observability/audit, support, upgrade, and on-call accountability.

##### Purpose

Make the accountability, risk, and fully allocated cost side of the target operating boundary visible without making an unsupported legal conclusion.

##### Talk track

The same custody that makes self-managed Kong attractive transfers permanent CP, PostgreSQL, PKI, Admin API, plugin/license, audit, upgrade, restore, support, and 24×7 service duties to enterprise roles. Cached data-plane service narrows one failure consequence; it does not remove control-plane recovery, urgent mutation/revocation, clean-node scale, reconciliation, or service accountability.

##### Speaker script

This is where the self-managed preference meets its permanent operating cost. Customer custody of the control plane also means enterprise accountability for PostgreSQL, private Admin application programming interface access, control-plane and data-plane public key infrastructure, licensing, plugin lifecycle, backups, upgrades, restore, audit evidence, observability, support coordination, and continuous response.

Hybrid data planes can cache accepted configuration and may continue proxying during a control-plane interruption. That narrows one failure consequence; it does not prove restart, clean-node scaling, urgent mutation or revocation, certificate renewal, reconciliation, isolated recovery, or business correctness. A healthy proxy therefore cannot be treated as a healthy platform.

The room must confirm accountable and funded roles across platform product, database and Site Reliability Engineering, security and public key infrastructure, release engineering, service management, sourcing and financial operations, and vendor support. For each duty, ask for capacity, response and recovery objectives, upgrade and restore evidence, escalation paths, and decision authority during degradation.

If the question becomes legal liability, keep the boundary precise. This slide allocates operational accountability and risk exposure. Contractual allocation requires exact commercial and support evidence; legal liability requires qualified counsel. Architecture language cannot settle it.

##### Talking points

- Control-plane custody brings permanent, funded enterprise duties.
- Cached proxy continuity does not prove platform recoverability.
- Operational accountability is not a legal-liability determination.

##### Ask

Confirm whether platform product, database/SRE, PKI/security, release engineering, service management, sourcing/FinOps, and support roles accept the duty, capacity, objectives, evidence, and escalation path.

##### Bridge

With the boundary explicit, the target topology becomes simple enough to explain.

##### Caveat

This is an operating-accountability and risk-exposure statement. Contractual allocation depends on exact support and commercial evidence; legal liability requires counsel in the approved restricted process. Control-plane continuity does not imply mutation, revocation, clean-node admission, or recovery guarantees.

##### Sources

- Canonical duty model: [Kong enterprise platform deployment strategy](47-kong-enterprise-platform-strategy.md) and [Kong guided evaluation](48-kong-guided-evaluation.md).
- Terminology and non-equivalence: [Kong terminology crosswalk](../research/glossary.md#kong-terminology-crosswalk).
- Official documented mechanisms (`E1` only): [Kong hybrid mode](https://developer.konghq.com/gateway/hybrid-mode/) and [Kong Gateway version support policy](https://developer.konghq.com/gateway/version-support-policy/).

##### Listen for

“Cached data-plane continuity removes the duty,” “the vendor owns this,” “who carries the liability?” or an assumption that the current team can absorb it without capacity evidence.

##### Evidence-safe response

Cached proxying is narrower than mutation, revocation, clean-node scale, reconciliation, recovery, and 24×7 service accountability. Vendor support can supply an escalation path but does not transfer the enterprise service duty. The public decision can allocate operational ownership and cost; it cannot adjudicate legal liability.

##### Follow-up probe

Which public role owns each permanent duty, with what funded capacity, response/recovery objective, restore and upgrade evidence, vendor escalation path, contractual assumption, and decision authority during degraded state?

##### Decision impact

Without accountable and funded duty, the self-managed target is non-admissible regardless of documented capability. If contractual or legal allocation could change the answer, hold that branch for sourcing or counsel evidence rather than resolving it through architecture language.

##### Capture

Record public role RACI, staffing and sourcing gaps, on-call coverage, restore/upgrade ownership, response objectives, support handoff, capacity assumptions, fully allocated TCO evidence, and any restricted contractual/legal referral. Do not publish named-person assignments.

##### Branch/rejoin

Branch to slides 9–12 for architecture and ownership or slides 20 and 24 for sustainability and economics. Rejoin at slide 6 or 21.

##### HOLD/park

HOLD when any CP, PostgreSQL, PKI, plugin/license, release, restore, audit/observability, upgrade, support, or on-call duty lacks an accountable funded role, measurable objective, evidence obligation, or escalation path. Do not park unresolved operating accountability as a legal question.

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

##### Speaker script

Let me start with the architectural bargain shown here. One enterprise control boundary owns approved gateway intent, while distributed data-plane cells serve requests close to workloads. The control plane and PostgreSQL are management dependencies; they are not intended to sit in the ordinary application programming interface request path. Local collectors keep operational evidence near each runtime, while enterprise public key infrastructure, identity, Domain Name System, traffic steering, and network controls remain explicit dependencies.

That gives us centralized authority without forcing every request through one central runtime. It does not give us proven high availability or multiregion recovery. This is still a proposed target informed by current official documentation, not an executed design. The picture does not select regions, replica counts, database replication, failover automation, capacity, sovereignty treatment, or clean-node behavior during isolation.

If someone reads these arrows as proof that failover is solved, the answer is: the diagram defines what we must test; it is not the result. I need the room to validate five things—control-zone ownership, data-plane placement, request locality, trust paths, and evidence custody. Any disagreement changes the bill of materials, failure model, ownership, and proof programme. If a mandatory boundary remains unknown, we hold the target freeze.

##### Talking points

- Centralize approved intent; distribute request handling and evidence.
- The diagram defines test boundaries; it does not prove resilience.
- Confirm ownership, placement, locality, trust, and evidence custody.

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

##### Speaker script

I want to retire one dangerous sentence: “The proxy is healthy, therefore the service is healthy.” This model separates the paths that sentence collapses. Configuration can be accepted while its freshness is aging. A data plane can receive a request while its identity provider, JSON Web Key Set, or client certificate authority is degraded. A backend can return an apparently successful response while the durable business action is absent, duplicated, or ambiguous. Request handling can also remain green while required audit or security evidence is being dropped.

These are examples of independent failure paths, not claims that any one is occurring today. The model is proposed and must be tested against the exact option. The service-level objective for the business journey is therefore not the same as gateway uptime.

If the room says this creates too many probes, narrow them to the mandatory journeys and risks—do not collapse them into one misleading signal. For each admitted service, name the configuration identity, trust-age rule, backend-readiness test, business verifier, evidence-gap signal, threshold, and response owner. The decision here is whether those paths receive separate proof gates. Without them, we can admit traffic into a false-ready service and discover the failure only after customer or audit impact.

##### Talking points

- A successful gateway request proves only that one path worked.
- Configuration, trust, backend, business, and evidence health are separate.
- Each mandatory journey needs independent signals and owners.

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

##### Speaker script

Once we separate the health paths, control-plane loss stops being a simple up-or-down event. An existing data plane may keep serving accepted configuration after losing its control-plane connection. A restarted node may be a candidate if it can recover an approved state. A clean or empty node is different: it should not be admitted merely because the process is running. Configuration age, urgent revocation, incompatible identity, missing evidence, or failed business probes may move a cell from continue to hold or quarantine.

The key point is that the platform does not automatically make all of these organizational risk decisions for us. “Always serve” can preserve traffic while extending an unsafe policy. “Always stop” can turn a manageable management-plane interruption into an unnecessary business outage. The correct response depends on the journey, allowed staleness, revocation risk, and recovery evidence.

For every state, the room must assign an owner, expiry condition, response objective, break-glass authority, and stop rule. Reconnection alone is not recovery: desired and effective state must reconcile, evidence gaps must be declared, and an outside-in business probe must pass. If any mandatory state lacks an owner, clock, probe, or reconciliation artifact, the architecture remains on hold.

##### Talking points

- Cached continuity requires pre-agreed continue, hold, quarantine, and stop states.
- Reconnection is not the same as recovery.
- Every state needs an owner, clock, probe, and reconciliation artifact.

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

##### Speaker script

This slide is where architecture becomes an operating commitment. It does not describe a shared cluster that application teams simply consume. It describes a funded platform product and a continuous service. The platform team owns Kong lifecycle, control-plane and database operations, release engineering, recovery, upgrade, evidence, and vendor escalation. Domain teams retain application programming interface contracts, business authorization, data correctness, and customer outcomes. Identity and access management, public key infrastructure, and security teams own trust profiles, rotation, revocation, and exceptions. Site Reliability Engineering, network, and database teams operate the failure seams with the platform.

Vendor support is an escalation path; it does not become the enterprise’s accountable service owner. That is an operating-model statement, not a legal-liability conclusion. Contractual liability belongs with sourcing, risk, and qualified counsel.

The challenge I expect is: “Can existing teams absorb this?” We should not answer by assumption. We need funded capacity, on-call coverage, response and recovery objectives, restore and upgrade evidence, and an explicit responsible, accountable, consulted, and informed model. We also need one authority for incidents where platform, security, and domain signals disagree. If a permanent duty has no funded accountable role, the self-managed target is non-admissible regardless of product capability.

##### Talking points

- Self-management is a funded service, not merely a topology choice.
- Vendor support does not replace enterprise accountability.
- An unfunded permanent duty makes the target non-admissible.

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

##### Speaker script

Please read this as a sequence of earned decisions, not as a Gantt chart. The adoption stages deliberately overlap because discovery, foundation work, proof, enablement, and migration can proceed in parallel. The displayed zero-to-eighteen-month windows are scenario assumptions. They are not current status, approved dates, workload commitments, or evidence that any phase has passed.

The first stage freezes the self-managed hybrid target, owners, bill of materials, critical journeys, and stop rules. The second builds a reversible, evidence-producing foundation. The third executes hard failure seams and seeks repeatable laboratory evidence. The fourth opens bounded paved roads and a migration capability only after ownership and controls work. The fifth seeks representative pilot evidence from materially different production patterns. The final stage is the decision to scale, narrow, switch custody, retain exceptions, or exit—not an automatic expansion step.

If the challenge is “Can we move faster?”, the answer is yes where work is parallelizable, but not by removing evidence dependencies. Every stage needs entry evidence, exit evidence, a funded owner, and stop authority. The room should approve that gate logic today. Calendar planning follows observed inventory and capacity; it cannot substitute for proof.

##### Talking points

- Adoption stages are evidence gates, not calendar commitments.
- Work may overlap, but evidence dependencies remain.
- Scale is a decision earned by outcomes, not the next scheduled phase.

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

##### Speaker script

A MuleSoft application is a packaging boundary, not necessarily an architectural responsibility. This model asks us to decompose each application before choosing destinations. Gateway policy—authentication, request limits, routing, and cross-cutting headers—is the only responsibility that is unambiguously an application programming interface edge concern. A thin facade may remain at the edge or become an owned service, depending on semantics and ownership. Transformation, orchestration, messaging, scheduled or file work, connectors, replay, and durable state need destination owners suited to those responsibilities.

Consider a package that authenticates a client, transforms a payload, schedules a file pickup, and records an idempotency watermark. Calling that one “API migration” hides four different state, recovery, and ownership questions. A plugin may technically reproduce some behavior, but extensibility does not prove that durable business or integration logic belongs in gateway policy.

For each component, ask: what does it do, where is durable truth held, who owns its side effects, how does it recover, and which target preserves that authority? Retirement is a separate decision requiring dependency and route-back evidence; absence of recent traffic is not enough. If responsibility, state authority, destination, or owner is unknown, that workload stays out of a migration cohort.

##### Talking points

- Migrate responsibilities and durable state—not packages.
- Extensibility does not prove that logic belongs at the gateway edge.
- Unknown ownership or state authority blocks cohort admission.

##### Ask

Adopt the responsibility taxonomy for inventory and wave planning.

##### Bridge

That decomposition supports bounded coexistence rather than a big-bang cutover.

##### Caveat

This is a migration doctrine. Actual destination selection requires workload-level classification and dependency evidence.

##### Sources

- Canonical migration and decision content: [Mule migration strategy](35-mule-migration-strategy.md), [Kong terminology crosswalk](../research/glossary.md#kong-terminology-crosswalk), and [Kong guided evaluation](48-kong-guided-evaluation.md).
- Official contextual mechanisms (`E1` only): [MuleSoft Omni Gateway](https://docs.mulesoft.com/gateway/latest/), [Kong entities](https://developer.konghq.com/gateway/entities/), [Kong plugin scope](https://developer.konghq.com/gateway/entities/plugin/), [Kong deployment topologies](https://developer.konghq.com/gateway/deployment-topologies/), [Apigee proxy-bundle export and import](https://docs.cloud.google.com/apigee/docs/api-platform/fundamentals/download-api-proxies), and [Apigee proxy configuration](https://docs.cloud.google.com/apigee/docs/api-platform/reference/api-proxy-configuration-reference).

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

##### Speaker script

This coexistence model keeps the external application programming interface edge stable while a bounded cohort moves between the existing MuleSoft runtime and a new owned runtime. The stable edge is deliberately product-neutral; this picture does not declare that the edge is already Kong. Its purpose is to reduce consumer change while we compare old and new behavior under controlled routing.

The parity question is larger than response-code matching. We need contract and error semantics, identity propagation, side effects, ordering, idempotency, latency, service-level objectives, evidence production, and the durable business outcome. A route-back trigger and decision owner remain active until those results reconcile. Moving traffic back is not sufficient if credentials, counters, state, or an irreversible backend action have diverged.

The expected objection is that dual run costs too much. That cost is real and belongs in the fully allocated migration model. But it must be compared with the business, security, and recovery exposure of an irreversible cutover whose semantic drift has not been measured. The room should approve bounded cohorts, representative parity corpora, business verification, reconciliation, evidence retention, and timed route-back as mandatory controls. A cohort remains on hold until its verifier, owner, stop condition, and route-back evidence are explicit.

##### Talking points

- Coexistence is a controlled experiment, not duplicate routing.
- Parity includes business outcome, identity, side effects, and evidence.
- Route-back remains active until state and outcomes reconcile.

##### Ask

Approve cohorting, parity probes and route-back as mandatory migration controls.

##### Bridge

The controls are applied in waves, each with explicit entry and exit evidence.

##### Caveat

The coexistence figure deliberately says stable API edge; the source migration strategy does not choose the exact gateway product for this pattern.

##### Sources

- Canonical coexistence and decision content: [Mule migration strategy](35-mule-migration-strategy.md) and [Kong guided evaluation](48-kong-guided-evaluation.md).
- Official contextual mechanisms (`E1` only): [MuleSoft Omni Gateway](https://docs.mulesoft.com/gateway/latest/), [Kong entities](https://developer.konghq.com/gateway/entities/), [Kong plugin scope](https://developer.konghq.com/gateway/entities/plugin/), [Kong deployment topologies](https://developer.konghq.com/gateway/deployment-topologies/), [Apigee proxy-bundle export and import](https://docs.cloud.google.com/apigee/docs/api-platform/fundamentals/download-api-proxies), and [Apigee proxy configuration](https://docs.cloud.google.com/apigee/docs/api-platform/reference/api-proxy-configuration-reference).

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

#### KGE-16 · Apigee A0–A6 moves the full object and state graph

- **Phase:** `KGE-P4 — Migration`
- **Native route:** [Open slide 16](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/15) (`#/present/kong-platform-journey-guided/15`)
- **Timebox:** 4 minutes
- **Evidence state:** Proposed migration model
- **Meeting job:** Make the Apigee A0–A6 roadmap explicit, then relate it to Mule M0–M5 without collapsing either source into a proxy-package conversion exercise.

##### Purpose

Use one stable-edge and evidence-gate doctrine while preserving the different migration units and state boundaries of Mule and Apigee.

##### Talk track

For Apigee, A0 inventories the complete object/state graph; A1 classifies semantic disposition; A2 builds a reversible target; A3 proves a hard representative slice; A4 runs bounded coexistence; A5 collects production-canary evidence; and A6 closes technical, operating, recovery, data, support, and commercial dependency zero. Mule uses a different M0–M5 responsibility/state rail. Both share reconciled source truth, semantic proof, a stable edge, business verification, timed route-back, state reconciliation and dependency-zero authority.

##### Speaker script

Apigee needs its own migration rail because its migration unit is a connected object and state graph, not a proxy bundle. Phase A0 reconciles the source archetype, active objects, state, traffic, owners, and dependencies. A1 classifies each behavior as direct map, configure, rewrite, retain, or retire. A2 builds a reversible target with executable infrastructure, configuration promotion, identity, restore, evidence, support, cost, and route-back controls. A3 proves one hard representative slice, including product and application credentials, key-value or quota state, transformations, errors, failure, load, and business semantics. A4 moves bounded cohorts while identity, state, outcomes, and evidence reconcile. A5 seeks representative pilot evidence. A6 permits retirement only after technical, operating, recovery, data, support, and commercial dependency zero.

MuleSoft uses a different responsibility-and-state rail because the source structures differ. The common doctrine is stable edge, reconciled source truth, semantic proof, business verification, timed route-back, and independent exit authority.

If someone proposes measuring progress by exported proxies, packages, or elapsed time, none of those proves identity, runtime state, portal or analytics continuity, business parity, or safe retirement. These phases are proposed and not run. Today we choose the applicable source rail, owners, denominators, entry and exit evidence, and stop authority—we do not authorize irreversible cutover.

##### Talking points

- Apigee migration moves a connected object and state graph.
- MuleSoft and Apigee use distinct source rails with common evidence gates.
- Exported objects and elapsed time do not prove safe retirement.

##### Ask

Confirm the actual source archetype, choose the relevant rail, and adopt entry/exit evidence rather than elapsed time, package count, or exported proxy count. Assign migration architecture, API product, IAM/security, SRE, domain, FinOps/sourcing, and independent-review roles.

##### Bridge

The current PoC evidence is far earlier than these production gates.

##### Caveat

These phases are proposed and not run. They do not assert current programme progress, duration, object count, converter success, or semantic parity. The terminology crosswalk supplies nearest analogues only; each mapping still requires behavior, state, lifecycle, authority, evidence, and ownership proof.

##### Sources

- Canonical wave and decision content: [Apigee migration strategy](50-apigee-migration-strategy.md#proposed-a0a6-migration-roadmap), [Mule migration strategy](35-mule-migration-strategy.md), and [Kong guided evaluation](48-kong-guided-evaluation.md).
- Mapping aid: [Kong terminology crosswalk](../research/glossary.md#kong-terminology-crosswalk).
- Official contextual mechanisms (`E1` only): [MuleSoft Omni Gateway](https://docs.mulesoft.com/gateway/latest/), [Apigee proxy-bundle export and import](https://docs.cloud.google.com/apigee/docs/api-platform/fundamentals/download-api-proxies), [Apigee proxy configuration](https://docs.cloud.google.com/apigee/docs/api-platform/reference/api-proxy-configuration-reference), [Kong entities](https://developer.konghq.com/gateway/entities/), [Kong plugin scope](https://developer.konghq.com/gateway/entities/plugin/), and [Kong deployment topologies](https://developer.konghq.com/gateway/deployment-topologies/).

##### Listen for

“Give us committed counts and dates,” “object migration percentage proves progress,” “Apigee proxy export is the roadmap,” “this source object maps directly to a same-named Kong entity,” or pressure to retire the source before dependency zero.

##### Evidence-safe response

Elapsed time, package count, and proxy bundles do not prove business parity, identity/product state, KVM/quota/cache behavior, portal/evidence continuity, residual dependency, reconciliation, or safe retirement. A source term is a mapping prompt, not a semantic result. Each rail advances only on source-specific, owned entry and exit evidence.

##### Follow-up probe

Which source archetype and object/state denominator apply, what evidence opens and closes each wave, which business and identity/state probes govern route-back, who validates dependency zero, and which role can stop or reverse retirement?

##### Decision impact

Time-led or proxy-only progression can produce irreversible cutover while semantics, identity, runtime state, evidence history, support, cost, or residual dependency remains unknown.

##### Capture

Record source archetype, reconciled object/state/traffic/owner denominator, terminology non-equivalences, per-wave entry and exit evidence, representative hard cases, identity/state authority, business probes, route-back and reconciliation conditions, dependency-zero definition, public role owners, independent reviewers, and unresolved assumptions.

##### Branch/rejoin

Branch to slides 14–15 for responsibility/coexistence, slides 17–18 for the current evidence gap, or slides 20–21 for outcome and retirement authority. Use the Apigee roadmap and terminology crosswalk as the detailed side talk; rejoin at slide 21.

##### HOLD/park

HOLD when source archetype, object/state denominator, semantic parity, identity/state authority, business probes, reconciliation, route-back, or dependency-zero evidence is missing. An exported bundle or name mapping cannot close the hold. Do not park an irreversible cutover risk.

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

##### Speaker script

This slide resets our confidence before we ask for more investment. The current proof of concept contains 16 aggregate scenario records. Five are automated local-baseline checks and 11 are explicitly not run. A separate comparison protocol defines 28 atomic cases. That is useful structure, but it is not evidence that the proposed self-managed hybrid target has passed.

The two denominators also answer different questions. The 16 records describe scenario state. The 28 cases describe a future comparison protocol. We must not merge them, convert them into a readiness percentage, or imply that defined tests were executed. For the exact target option, there are currently no repeatable target-shaped laboratory results and no representative pilot results.

The correct conclusion is not that the proof of concept failed. It established a functional baseline and exposed the work that remains. The evidence ceiling simply prevents us from overclaiming.

Ask the evidence steward to confirm three ledgers separately: what was automated and passed, what was scripted but not run, and what has not yet been designed against the frozen target. If someone proposes a readiness percentage, ask for the denominator, exact environment, raw artifacts, repeatability, reviewer, and link to the production decision it supports. Until those exist, the authorization remains foundation and proof only.

##### Talking points

- Five automated local checks are not production-target proof.
- The 16 scenario records and 28 atomic cases are separate denominators.
- No readiness percentage or production conclusion is supported yet.

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
- **Meeting job:** Authorize GEP-01–07 with an exact environment, public role owner, measure, threshold, raw artifact, independent reviewer, and stop rule.

##### Purpose

Turn the current evidence gap into an executable, target-shaped proof programme.

##### Talk track

This is not a larger feature demonstration. GEP-01–06 prove the target, APIOps, regional resilience, enterprise IAM, separate agentic study, and evidence-gated recommendation. GEP-07 is a separate security-adjunct feasibility line for Kong plus Traceable against the security team’s Mule baseline. Each workstream needs a representative environment, public role owner, exact BOM, method, measure, acceptance artifact, threshold, independent reviewer, and stop condition.

##### Speaker script

The next proof of concept is not a larger feature demonstration. It must mirror the proposed production boundary closely enough that a result can change the decision. Seven proof-workstream records define that programme.

The first freezes and runs the target-aligned hybrid topology. The second makes Terraform provisioning and decK application programming interface operations executable, including validation, difference review, promotion, drift detection, and scoped recovery. The third executes multiregion failure, isolated recovery, reconciliation, and scaling under representative load. The fourth exercises the enterprise identity and access lifecycle across workforce, workload, consumer, application programming interface, and service-account identities. The fifth is a separate agentic-gateway study covering Model Context Protocol, agent-to-agent communication, model routing, semantic caching, content safety, and agent and Model Context Protocol catalogs. The sixth requires the recommendation to follow executed results. The seventh evaluates Kong plus Traceable as a security adjunct against the security team’s MuleSoft baseline; documentation only establishes feasibility to test.

Every workstream needs an exact bill of materials, representative environment, accountable public role, method, measure, threshold, raw artifact, independent reviewer, and stop condition. If any of those is missing, we have an interesting demo—not decision-capable evidence.

##### Talking points

- Mirror the proposed production boundary; do not enlarge a generic demo.
- Each workstream needs a measure, threshold, artifact, reviewer, and stop rule.
- Kong plus Traceable is a separate adjunct study and earns no native score.

##### Ask

Approve these seven workstreams, their role owners, capacity, evidence budget, reviewers, and stop authority—not production scale and not a Traceable production recommendation.

##### Bridge

Once the proof scope is fixed, production readiness is judged through the outcome measures and acceptance artifacts that follow.

##### Caveat

These are required proof activities, not completed results. For GEP-07, current documentation supports only an `E1` plugin/agent feasibility path. It does not certify the exact Kong Enterprise 3.14 patch, plugin/TPA/EDS BOM, topology, entitlement, support, performance, protocol/payload/streaming coverage, data handling, fail behavior, comparative parity, lifecycle, cost, or production outcome.

##### Sources

- Canonical proof programme: [Kong guided evaluation — Seven-workstream target-aligned proof programme](48-kong-guided-evaluation.md#seven-workstream-target-aligned-proof-programme).
- Traceable evidence boundary: [Traceable by Harness security-adjunct feasibility](48-kong-guided-evaluation.md#traceable-by-harness-security-adjunct-feasibility).
- Official documented mechanisms (`E1` only): [Kong Gateway version support policy](https://developer.konghq.com/gateway/version-support-policy/), [Kong hybrid mode](https://developer.konghq.com/gateway/hybrid-mode/), [Kong Gateway monitoring](https://developer.konghq.com/gateway/monitoring/), [Kong AI Gateway](https://developer.konghq.com/ai-gateway/), [Traceable Kong integration](https://docs.traceable.ai/kong), and [Harness WAAP plugin](https://developer.konghq.com/plugins/harness-waap/).

##### Listen for

“Documentation already proves 3.14,” “the existing PoC is enough,” “Traceable makes the security team’s Mule use case feasible by definition,” “add Traceable as a scored Kong capability,” “the programme is too broad,” or “AI capability should count toward the core decision.”

##### Evidence-safe response

Documentation supports test design, not entitlement, configured behavior, target execution, or production outcome. Traceable is a third-party adjunct rather than a gateway option or native score: freeze its Kong/plugin/TPA/EDS BOM and support, trace the request/response/security-decision/data paths, classify protocol/body/streaming coverage, execute sync/async and fail-open/closed cases, measure latency/CPU/memory/throughput and agent scaling, verify privacy and correlation, and rehearse upgrade, rollback, uninstall, and route-back. Keep both GEP-05 agentic proof and GEP-07 adjunct proof separately versioned.

##### Follow-up probe

For each GEP workstream, what exact BOM/environment, measure, threshold, raw artifact, independent reviewer, and stop rule will change the decision? For GEP-07, which security architecture, platform product, SRE/performance, privacy, support, and independent-assurance roles own the test and the baseline comparison?

##### Decision impact

Missing target fidelity or review controls leaves documented capability unable to advance into production evidence. Missing GEP-07 evidence excludes the adjunct from security, traceability, parity, price, and production conclusions; it does not by itself reject Kong as a gateway.

##### Capture

For GEP-01–07, record public role owner, capacity, exact BOM/environment, method, measure, threshold, raw artifact, independent reviewer, due gate, and stop rule. For GEP-07 also record source baseline, plugin/agent versions and checksums, support statement, data classification and flow, mode/failure policy, coverage corpus, resource envelope, privacy control, support RACI, and rollback/removal evidence. Keep named-person mappings restricted.

##### Branch/rejoin

Branch to slide 23 for agentic or Traceable mechanism questions, slide 20 for security traceability and evidence safety, or slide 24 for fully allocated economics. Rejoin at slide 19 and then slide 21.

##### HOLD/park

HOLD any workstream missing its exact option, environment, measure, threshold, artifact, reviewer, or stop rule. HOLD GEP-07 on unsupported BOM, unauthorized pass, prohibited data flow, unbounded overhead, unclassified required protocol/use case, unowned support seam, or no safe rollback/removal. Park scope detail only with those fields and a slide-19 re-entry.

#### KGE-19 · Five reviewable outcomes anchor production proof

- **Phase:** `KGE-P5 — Production proof`
- **Native route:** [Open slide 19](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/18) (`#/present/kong-platform-journey-guided/18`)
- **Timebox:** 4 minutes
- **Evidence state:** Proposed acceptance contract
- **Meeting job:** Agree target forms, artifacts, cadence, and owners for KO-1 through KO-5.

##### Purpose

Translate the first five production outcomes into decision evidence.

##### Talk track

Each mechanism is paired with a measurable outcome and a reviewable artifact. Trustworthy active state, business reliability, trust integrity, management recoverability and safe change are all separate admission dimensions.

##### Speaker script

This slide changes the conversation from “Does the mechanism exist?” to “Did the intended outcome occur?” The first five outcomes must be reviewed independently.

Trustworthy active state means the effective configuration and trust material are identifiable, current enough for the journey, and reconciled with approved intent. Business reliability means the customer or operational transaction completes correctly—not merely that the proxy returns a success code. Trust integrity means authentication, authorization, certificate, secret, and revocation behavior remain correct through normal and degraded states. Management recoverability means the control plane, PostgreSQL, credentials, and evidence can be restored and reconciled within approved objectives. Safe change means promotion, rollback, drift handling, and emergency change produce the intended state without hidden residue.

For each outcome, pre-approve the measure, threshold, observation window, raw artifact, independent reviewer, and failure disposition before execution. Otherwise the team can redefine success after seeing the result.

If someone asks for a single pass/fail light, resist collapsing these outcomes. A green request path can coexist with stale policy, broken recovery, missing evidence, or an incorrect business outcome. The decision needs to show which outcome passed, which remains unknown, and which blocks admission.

##### Talking points

- Pair every mechanism with an observable outcome and reviewable artifact.
- Proxy success, business correctness, trust, recovery, and safe change are distinct.
- Define thresholds and failure dispositions before running the test.

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
- **Meeting job:** Agree KO-6–KO-11 and identify the most likely scale blocker across capacity, security traceability/evidence safety, adoption, toil, exit, and estate truth.

##### Purpose

Complete the production decision with non-functional and organizational outcomes.

##### Talk track

Capacity isolation and evidence safety matter, but so do platform adoption, operating sustainability, reversibility and estate truth. KO-7 is an outcome: administrative/configuration audit, request and security-decision correlation, business evidence, quantified produced/queued/dropped/delivered gaps, and prohibited-field control. Traceable may be one candidate mechanism, but no product name can make KO-7 pass.

##### Speaker script

The second outcome set asks whether the whole operating system can scale, not merely whether gateway throughput rises. Capacity and fault isolation must show headroom, saturation order, noisy-neighbor behavior, clean-node scale, and recovery under the frozen topology. Traceability and evidence safety must correlate administrative change, request handling, security decisions, and business evidence while quantifying produced, queued, dropped, and delivered gaps and protecting prohibited fields.

Platform adoption asks whether teams can use the paved road without bespoke intervention. Operating sustainability asks whether staffing, on-call, upgrades, support, infrastructure, and fully allocated total cost of ownership remain viable. Reversibility asks whether we can switch custody or reconstruct a representative boundary on a non-Kong target without unacceptable semantic loss. Estate truth asks whether inventory, owners, versions, dependencies, exceptions, and retirement state remain reconciled.

Traceable may be one candidate mechanism for part of the traceability and security-evidence outcome. It cannot define that outcome, make it pass by presence, or substitute adjunct telemetry for business verification. Likewise, a load-test headline cannot prove sustainable scale.

For each outcome, identify the operational consumer of the evidence and the decision it enables. If nobody will act on the signal, or the artifact cannot be independently reviewed, the proof design is incomplete.

##### Talking points

- Scale depends on capacity, adoption, operations, economics, reversibility, and estate truth.
- Traceability is an end-to-end outcome, not a product line item.
- Every signal needs an owner and a decision it can trigger.

##### Ask

Confirm which outcome is currently the likely scale blocker, which public role owns it, and whether any Traceable dependency is being treated as a mechanism to prove rather than an achieved outcome.

##### Bridge

The final decision must preserve four outcomes: scale, narrow, switch custody or exit.

##### Caveat

These are acceptance categories; no result is asserted on this slide. GEP-07 evidence may inform KO-7 only inside its exact tested boundary and cannot substitute for configuration audit, signal-gap accounting, business correlation, or enterprise evidence controls.

##### Sources

- Canonical outcome contract: [Kong enterprise platform deployment strategy](47-kong-enterprise-platform-strategy.md) and [Kong guided evaluation](48-kong-guided-evaluation.md).
- Traceable evidence boundary: [Kong guided evaluation — Traceable by Harness security-adjunct feasibility](48-kong-guided-evaluation.md#traceable-by-harness-security-adjunct-feasibility).
- Official documented mechanisms (`E1` only): [Kong hybrid mode](https://developer.konghq.com/gateway/hybrid-mode/), [Kong Gateway monitoring](https://developer.konghq.com/gateway/monitoring/), [Kong AI Gateway](https://developer.konghq.com/ai-gateway/), [Traceable Kong integration](https://docs.traceable.ai/kong), and [Harness WAAP plugin](https://developer.konghq.com/plugins/harness-waap/).

##### Listen for

“Technical health is enough,” “Traceable means traceability is covered,” “cost and adoption can wait,” or “exit readiness is unnecessary once the platform is selected.”

##### Evidence-safe response

Production admission is a whole-operating-system decision. Capacity, security traceability/evidence safety, adoption, operating sustainability, exit, and estate ownership can each block scale even when proxy behavior is healthy. Traceable is an adjunct hypothesis with its own data, failure, coverage, performance, support, and lifecycle risks; it is not the definition of traceability.

##### Follow-up probe

Which KO-6–KO-11 outcome is most likely to block scale, what end-to-end data proves it, which gaps are quantified, and which role has authority to act on failure? If Traceable is proposed, which KO-7 fields remain outside it?

##### Decision impact

Ignoring organizational, evidence, and economic outcomes converts installation success into unsupported production confidence and weakens reversibility. Treating one adjunct as the outcome can also hide audit, correlation, privacy, or signal-loss gaps.

##### Capture

Record the likely blocker, public role owner, data source, correlation query, produced/queued/dropped/delivered accounting, prohibited-field control, cadence, adjunct dependency and limitation, toil and cost model, adoption measure, estate owner, and exit rehearsal.

##### Branch/rejoin

Branch to slide 12 for ownership, slide 18 or 23 for GEP-07 and Traceable, or slide 24 for economics and exit. Rejoin at slide 21.

##### HOLD/park

HOLD scale when any mandatory outcome is failed, unknown, unowned, or offset by a weighted score or product label. HOLD KO-7 on unexplained signal gaps, prohibited data, broken correlation, unsafe failure behavior, or an unproved critical adjunct dependency. Park only a bounded target value with a role owner and review date.

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

##### Speaker script

This is the point where we protect the evaluation from becoming a one-way ratchet. Before evidence runs, the decision owner must pre-commit to the outcomes the evidence can produce.

Scale means the admitted target and representative cohorts meet their mandatory outcomes and the organization funds the operating model. Narrow means Kong remains useful for a bounded set of patterns while exceptions stay elsewhere. Switch custody means the Kong boundary remains, but management responsibility moves—for example to the Konnect benchmark. Exit means a representative non-Kong reconstruction and route-back obligation become the direction. Hold means the evidence is insufficient, contradictory, or blocked by an unowned mandatory gate.

Negative evidence must be allowed to change the recommendation. External application programming interface governance may make Apigee stronger. Continued strategic dependence on Anypoint may make MuleSoft stronger. Azure consolidation may make Azure API Management the better benchmark. Failed custody, offline, recovery, security, cost, adoption, or reversibility evidence may narrow or reverse Kong.

Do not confuse a same-vendor custody switch with a non-Kong exit. They close different risks. I need the decision owner to name who can invoke each outcome, what threshold triggers it, what work stops, and what artifact records the transition. Without that authority, the proof programme can generate evidence but cannot govern a decision.

##### Talking points

- Pre-commit to scale, narrow, switch custody, exit, or hold.
- Negative evidence must be allowed to change direction and funding.
- Konnect custody switch and non-Kong exit remain separate outcomes.

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

#### KGE-22 · Comparison input — architecture, multicloud and robustness

- **Phase:** `KGE-P6 — Audit appendix`
- **Native route:** [Open slide 22](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/21) (`#/present/kong-platform-journey-guided/21`)
- **Timebox:** On demand; 3-minute branch
- **Evidence state:** Stakeholder input
- **Meeting job:** Turn disputed architecture, delivery, multicloud, scalability, and robustness labels into versioned, symmetric proof questions without rescoring in the room.

##### Purpose

Preserve the sanitized supplied evaluation’s architectural comparison while making the new multicloud, scalability, and robustness obligations explicit.

##### Talk track

The supplied labels remain stakeholder assessments preserved in docs/48. Official documentation supports high-level deployment mechanisms, not relative outcomes. GEC-19 keeps scalability and robustness explicitly unscored until equivalent target-shaped load, saturation, clean-node scale, failure, recovery, and reconciliation evidence exists. Multicloud must separate runtime placement from management dependency, sovereignty, failure independence, support, and operating cost.

##### Speaker script

This appendix slide is an audit branch, not a place to rescore products in the room. The supplied architecture labels are stakeholder assessments preserved for traceability. Current official documentation can confirm high-level deployment mechanisms, but it cannot establish relative production outcomes.

For multicloud, separate runtime placement from management dependency, sovereignty, failure independence, network and identity dependencies, support, and operating cost. A product that can place data planes in several clouds has not automatically proved independent operation across them. For scalability and robustness, require equivalent target-shaped evidence for every admitted option: workload mix, load ramp, headroom, saturation order, noisy-neighbor behavior, clean-node scale, region or dependency failure, recovery, reconciliation, and the business service-level objective.

Symmetry matters. The same scenario, measurement rules, evidence floor, and independent review must apply to Kong, Apigee, MuleSoft, and any approved benchmark. If one option is tested in a target-shaped lab while another is described from documentation, the comparison is not score-capable.

When challenged on a label, capture the exact option, edition, topology, workload, fault profile, measure, threshold, artifact, owner, and reviewer. Return that evidence request to the governed comparison; do not repair the label with an opinion or a new score during this branch.

##### Talking points

- Appendix labels are preserved input, not validated product outcomes.
- Multicloud placement is not the same as failure independence or portability.
- Use exact, symmetric tests and never rescore in the room.

##### Ask

Use this table to assign symmetric architecture/SRE proof questions, not to add favorable labels or ratings in the room.

##### Bridge

The next appendix page covers API management, experience and AI claims.

##### Caveat

Qualitative ratings are not independently validated and may change by exact edition, release, topology, entitlement, workload, region, dependency, and operating model. “Multicloud” and “scalable” are not scoreable yes/no features.

##### Sources

- Canonical sanitized input: [Kong guided evaluation — Supplied comparison input: architecture and delivery](48-kong-guided-evaluation.md#supplied-comparison-input-architecture-and-delivery).
- Feedback-to-proof mapping: [Meeting-feedback assurance crosswalk](48-kong-guided-evaluation.md#meeting-feedback-assurance-crosswalk) and [Proposed governed re-score](48-kong-guided-evaluation.md#proposed-governed-re-score).
- Official documented mechanisms (`E1` only): [Kong deployment topologies](https://developer.konghq.com/gateway/deployment-topologies/), [Kong hybrid mode](https://developer.konghq.com/gateway/hybrid-mode/), [Kong AI Gateway](https://developer.konghq.com/ai-gateway/), [Apigee hybrid 1.16](https://docs.cloud.google.com/apigee/docs/hybrid/v1.16/what-is-hybrid), [MuleSoft Omni Gateway](https://docs.mulesoft.com/gateway/latest/), and [Azure API Management self-hosted gateway](https://learn.microsoft.com/en-us/azure/api-management/self-hosted-gateway-overview).

##### Listen for

“Vendor documentation validates the relative labels,” “Kubernetes proves multicloud,” “the product is known to scale,” or pressure to change qualitative ratings and rescore during the branch.

##### Evidence-safe response

Official documentation supports bounded mechanism interpretation, not relative product labels. Runtime placement does not prove sovereignty, failure independence, or portability; generic scale claims do not prove business SLO, headroom, saturation order, recovery, or clean-node behavior. Convert each disputed label into an exact option-, topology-, workload-, failure-, and outcome-specific evidence request.

##### Follow-up probe

Which canonical criterion, exact option, edition, topology, workload/fault profile, measure, threshold, and executed artifact would confirm or falsify the label under common evidence?

##### Decision impact

A material architecture, multicloud, scalability, or robustness result can change the conditional direction and future governed score, but not until symmetric evidence closes it.

##### Capture

Record the claim, mapped canonical criterion, current evidence state, exact option boundary, workload/fault profile, measure, threshold, required artifact, architecture/SRE role owner, independent reviewer, and due gate; do not change the score in the room.

##### Branch/rejoin

Branch to slide 4 for option conditions, slide 18 for proof authorization, or slide 25 for score governance. Rejoin at slide 6.

##### HOLD/park

HOLD if a mandatory option condition depends on an unverified label, generic scale claim, or unproved multicloud assumption. Park non-decision detail only with a versioned symmetric evidence request and slide-6 re-entry.

#### KGE-23 · Comparison input — management, AI and security traceability

- **Phase:** `KGE-P6 — Audit appendix`
- **Native route:** [Open slide 23](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/22) (`#/present/kong-platform-journey-guided/22`)
- **Timebox:** On demand; 3-minute branch
- **Evidence state:** Mixed documented mechanism and stakeholder input
- **Meeting job:** Assign exact use cases, versions, entitlements, support boundaries, public role owners, and artifacts for management, developer experience, AI, customization, and GEP-07 Kong-plus-Traceable claims.

##### Purpose

Preserve the management and experience claims while making emerging AI and third-party security-adjunct evidence boundaries explicit.

##### Talk track

Lifecycle, governance, portal, developer experience, AI, customization, and best-fit claims must be tested against required use cases. GEC-20 records Kong-plus-Traceable as documented feasibility only: a plugin/agent path does not prove exact 3.14 support, security effectiveness, traceability, data safety, performance, scaling, comparative parity, cost, or safe lifecycle behavior.

##### Speaker script

This appendix branch covers management, artificial intelligence, and security-traceability claims. Treat every adjective—easy, complete, native, secure, observable, scalable—as a hypothesis tied to an exact use case, version, entitlement, topology, and support boundary.

Current Traceable documentation describes a Kong plugin and agent path, including deployment choices that can support a test design. That is evidence of a documented mechanism only. It does not prove compatibility with the frozen Kong Gateway Enterprise 3.14 bill of materials, security effectiveness, end-to-end traceability, prohibited-field protection, performance, scaling, comparative parity with the MuleSoft security baseline, fully allocated cost, or safe upgrade and removal.

The dedicated security-adjunct workstream must freeze the Kong, plugin, platform-agent, and supporting-service versions; map request, response, security-decision, and prohibited-data paths; exercise approved synchronous and asynchronous modes and fail behavior; classify protocol, body, and streaming coverage; measure latency and resources; verify privacy and correlation; and rehearse upgrade, rollback, uninstall, and route-back.

Keep the scoring boundary clear. The adjunct may help satisfy an outcome, but it is not native Kong capability and cannot add gateway points. The separate agentic-gateway study must follow the same rule: documented Model Context Protocol, agent-to-agent, routing, caching, and safety features create tests—not proof.

##### Talking points

- Product and adjunct claims require exact use cases, versions, and support boundaries.
- A documented plugin or agent path is feasibility evidence, not an executed result.
- Traceable and agentic evidence cannot inflate the core gateway score.

##### Ask

Move every unverified adjective into the proof backlog with a public role owner, exact option/BOM, artifact, reviewer, and stop rule. Confirm that Traceable remains GEP-07 rather than a gateway option or score.

##### Bridge

The next appendix page covers lock-in, cost, the supplied overall recommendation, and the evidence ceiling.

##### Caveat

Product, plugin, agent, entitlement, support, and commercial terms are edition-, version-, topology-, and date-dependent. Current Traceable/Kong documentation is `E1` mechanism evidence only.

##### Sources

- Canonical sanitized input: [Kong guided evaluation — Supplied comparison input: management, experience, and AI](48-kong-guided-evaluation.md#supplied-comparison-input-management-experience-and-ai).
- Canonical adjunct boundary: [Traceable by Harness security-adjunct feasibility](48-kong-guided-evaluation.md#traceable-by-harness-security-adjunct-feasibility).
- Official documented mechanisms (`E1` only): [Kong deployment topologies](https://developer.konghq.com/gateway/deployment-topologies/), [Kong AI Gateway](https://developer.konghq.com/ai-gateway/), [Traceable Kong integration](https://docs.traceable.ai/kong), [Harness WAAP plugin](https://developer.konghq.com/plugins/harness-waap/), [Traceable rule-evaluation matrix](https://docs.traceable.ai/docs/tracing-agents-rule-evaluation-for-protection), [Apigee hybrid 1.16](https://docs.cloud.google.com/apigee/docs/hybrid/v1.16/what-is-hybrid), [MuleSoft Omni Gateway](https://docs.mulesoft.com/gateway/latest/), and [Azure API Management self-hosted gateway](https://learn.microsoft.com/en-us/azure/api-management/self-hosted-gateway-overview).

##### Listen for

“Kong documents MCP, A2A, and AI routing, so agentic fit is proved,” “Traceable makes Kong secure and traceable,” “Traceable should increase Kong’s score,” or an assumption that portal, lifecycle, customization, and developer-experience claims are self-validating.

##### Evidence-safe response

Documentation permits versioned test design. For Traceable, freeze the Kong/plugin/TPA/EDS BOM and support; map request, response, decision, and prohibited-field paths; execute sync/async and approved fail behavior; classify protocol/body/streaming coverage; measure latency/resources and scaling; verify privacy and correlation; and rehearse upgrade, rollback, uninstall, and route-back against the security baseline. Until then, the adjunct cannot support a platform score or security, traceability, cost, parity, or production conclusion. Agentic evidence likewise cannot inflate the core gateway decision.

##### Follow-up probe

Which exact use case and version/plugin/agent matrix matters, what is the expected outcome and failure rule, and what artifact and independent reviewer would prove it? Which result belongs to gateway fit versus the adjunct only?

##### Decision impact

An unbounded management, agentic, or adjunct claim can distort the platform direction, proof budget, security/privacy boundary, evidence model, and economics.

##### Capture

Record use case, exact option/BOM and checksums, plugin/agent versions, entitlement/support, data and failure paths, protocol/body/streaming coverage, threat/privacy boundary, cost/latency/resource measure, content-safety or security outcome, evidence correlation, catalog/lifecycle, upgrade/rollback/removal, artifact, independent reviewer, and public role owner. Suggested GEP-07 roles are security architecture plus platform product, with SRE/performance, privacy, support, and independent security assurance.

##### Branch/rejoin

Branch to slide 18 for GEP-05 or GEP-07, slide 20 for KO-7 security traceability/evidence safety, or slide 24 for commercial implications. Rejoin at slide 19 and then slide 21.

##### HOLD/park

HOLD a decision that depends on an unproved emerging feature or adjunct, unsupported BOM/entitlement, unknown or prohibited data flow, unauthorized pass, unbounded overhead, unclassified required protocol/use case, critical safety/policy failure, unowned support seam, or no safe rollback/removal. Park only a separately versioned GEP-05 or GEP-07 action.

#### KGE-24 · Comparison input — pricing, lock-in and operating duty

- **Phase:** `KGE-P6 — Audit appendix`
- **Native route:** [Open slide 24](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/23) (`#/present/kong-platform-journey-guided/23`)
- **Timebox:** On demand; 3-minute branch
- **Evidence state:** Stakeholder input with documented pricing boundaries
- **Meeting job:** Assign normalized pricing, fully allocated TCO, reversibility/vendor dependency, control-plane duty, security-adjunct, migration, dual-run, switching, and clean-exit evidence.

##### Purpose

Expose pricing, operating-duty, adjunct-cost, lock-in, and exit claims as separate proof obligations rather than conclusions.

##### Talk track

Public price pages define meters or quote boundaries, not a comparable price rank. Fully allocated TCO requires exact options and quotes plus infrastructure, PostgreSQL, PKI, platform/SRE/on-call labor, HA/DR, telemetry, portal/product tooling, network/egress, plugins and security adjuncts, support, migration, dual run, incident exposure, custody switch, and clean exit. Lock-in requires an observed representative non-source rebuild and a ledger of configuration/policy, identity/product state, data/analytics, plugin, procedure, support, and commercial dependencies.

##### Speaker script

A public price page can identify a meter or quote boundary. It cannot establish which option is cheaper for this organization. A comparable total cost of ownership model needs the exact options and commercial terms plus infrastructure, PostgreSQL, public key infrastructure, platform engineering, Site Reliability Engineering and on-call labor, high availability and disaster recovery, telemetry, portal and product tooling, network and egress, plugins and security adjuncts, support, migration, dual run, incident exposure, custody switching, and clean exit.

Use one time horizon and one workload denominator, with low, base, and high cases. Keep restricted quotes in the approved commercial system while publishing assumptions, boundaries, evidence state, accountable roles, and disposition in the study.

Vendor dependency also needs executed evidence. Konnect is the same-vendor custody benchmark; only an executed and reviewed transition can demonstrate the switch, and it still would not prove a non-Kong exit. Rebuild a representative application programming interface, policy, identity, product state, evidence, and runtime boundary on an approved non-source target. Record semantic loss, rewrite effort, state and history loss, procedural dependency, support and contract dependency, route-back, and residual coupling.

Finally, keep operational responsibility and legal liability separate. This study can expose duties, cost, risk, and contractual questions. It cannot make a legal determination. If an economics or exit conclusion lacks normalized evidence and an independent reviewer, it remains unknown and blocks that rating.

##### Talking points

- Public pricing is not fully allocated total cost of ownership.
- Measure lock-in through custody switch and representative non-Kong rebuild evidence.
- Operating risk is not a legal-liability verdict.

##### Ask

Assign public FinOps, sourcing, platform/SRE, security-adjunct, migration, and independent-review roles for the normalized low/base/high model, rebuild, custody switch, and clean-exit evidence.

##### Bridge

The final appendix page exposes the raw score inputs and corrected arithmetic.

##### Caveat

Commercial terms and estate leverage are organization- and date-specific. Do not publish restricted quotes. The public record should expose meter/quote boundaries, assumptions, role ownership, evidence state, and disposition only. Operating accountability is not a legal-liability verdict.

##### Sources

- Canonical sanitized input: [Kong guided evaluation — Supplied comparison input: economics and evidence ceiling](48-kong-guided-evaluation.md#supplied-comparison-input-economics-and-evidence-ceiling).
- Governed economics and reversibility dimensions: [Proposed governed re-score](48-kong-guided-evaluation.md#proposed-governed-re-score).
- Official pricing and topology boundaries (`E1` only): [Kong pricing](https://konghq.com/pricing), [Apigee pricing](https://cloud.google.com/apigee/pricing), [MuleSoft pricing](https://www.mulesoft.com/anypoint-pricing), [Kong deployment topologies](https://developer.konghq.com/gateway/deployment-topologies/), [Apigee hybrid 1.16](https://docs.cloud.google.com/apigee/docs/hybrid/v1.16/what-is-hybrid), and [Traceable Kong integration](https://docs.traceable.ai/kong).

##### Listen for

“The public price page proves Kong is cheaper,” “license price is TCO,” “Kong lock-in is low,” “the Traceable adjunct is free operationally,” “vendor support removes the control-plane duty,” or “Konnect is sufficient exit evidence.”

##### Evidence-safe response

TCO requires exact quotes/meters, labor, infrastructure, HA/DR, telemetry, adjuncts, support, migration, dual run, incident exposure, and exit. Konnect tests same-vendor custody, not a clean non-Kong rebuild. Lock-in is observed rewrite, state/history loss, support/contract dependency, and route-back effort—not a feature label. Vendor support provides escalation; it does not erase enterprise operating accountability.

##### Follow-up probe

Which exact option and meter/quote boundary, workload volume, low/base/high horizon, labor model, infrastructure/HA/DR design, adjunct dependency, support assumption, incident exposure, switching event, representative rebuild, and residual dependency will be measured?

##### Decision impact

Unproved economics, operating duty, adjunct cost, or exit can make the self-managed benefit non-viable and can favor a custody switch, narrower scope, or different platform. It also prevents the governed re-score from publishing a cost-efficiency or reversibility rating.

##### Capture

Record public FinOps and sourcing role owners, model scope and horizon, restricted quote references and public assumptions, infrastructure, labor/on-call, HA/DR, telemetry, plugin/adjunct, support, migration, dual-run, incident, custody-switch, representative rebuild, non-Kong exit artifacts, independent reviewer, and due gate.

##### Branch/rejoin

Branch to slides 7–8 for custody and duty, slide 20 for sustainability, or slide 25 for score governance. Rejoin at slide 21.

##### HOLD/park

HOLD a price, cost-efficiency, operating-duty, or lock-in conclusion without exact options, a normalized fully allocated model, and executable rebuild/exit evidence. Park commercial and legal detail only in the approved restricted system with a public-safe closure record.

#### KGE-25 · Historical audit; provisional uncertainty envelope

- **Phase:** `KGE-P6 — Audit appendix`
- **Native route:** [Open slide 25](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/24) (`#/present/kong-platform-journey-guided/24`)
- **Timebox:** On demand; 3-minute branch
- **Evidence state:** Provisional scenario over stakeholder input
- **Meeting job:** Preserve the historical score audit, review the transparent 60/40 planning weights and uncertainty range, and keep the decision on HOLD until the governed re-score contract and score-capable evidence close.

##### Purpose

Provide an auditable record of the source scorecard while showing what the newly requested dimensions can do to the ranking when their ratings are honestly left unknown.

##### Talk track

The sanitized inputs still recalculate to 93 for Kong, 85.5 for Apigee, and 77 for MuleSoft. The provisional scenario rebases those historical ratings to 60% and assigns 40% to `GRS-01`–`GRS-06`: multicloud, scalability/robustness, enterprise IAM and traceability, reversibility/vendor dependency, fully allocated TCO, and control-plane operating responsibility. Every new product rating remains `Unknown [0,10]`. That produces mechanical envelopes of 55.8–95.8 for Kong, 51.3–91.3 for Apigee, and 46.2–86.2 for MuleSoft. The ranges overlap completely enough that every option can still rank first. A midpoint of 5 is only a neutral drawing aid, not an assigned score.

##### Speaker script

This final appendix slide preserves two things at once: the historical arithmetic and the uncertainty that remains after the meeting feedback is added.

The supplied ratings still recalculate to 93 for Kong, 85.5 for Apigee, and 77 for MuleSoft. Under the provisional 60/40 planning scenario, their fixed historical contributions become 55.8, 51.3, and 46.2. The remaining 40 percent covers six proposed dimensions—multicloud; scalability and robustness; enterprise identity and access management plus traceability; reversibility and vendor dependency; fully allocated total cost of ownership; and control-plane operating responsibility. Every product rating in that block is still unknown from zero to ten.

The displayed envelopes therefore overlap enough that every option can still rank first. That does not mean the products are equal. It means the current evidence does not stabilize the ranking. The midpoint of five is only a drawing aid. It is not a score, estimate, forecast, or probability.

Do not close the meeting here. This is audit evidence about why governed comparison work remains necessary. Capture approval or amendment of the scoring method, exact options, mandatory gates, common evidence, confidence rules, scorer and assurance roles, sensitivity analysis, dissent, and permitted use. Then return to slide 6 for authorization or slide 21 for outcome authority.

##### Talking points

- Preserve historical arithmetic while exposing unresolved uncertainty.
- Overlap means rank instability, not product equality.
- The midpoint is not a score; close on slides 6 or 21, never in the appendix.

##### Ask

Review or amend the provisional weight split and double-counting rules, then assign accountable approval for exact options, mandatory gates, rubric, common evidence, ratings, confidence, scorers, sensitivity, bounds, regret, dissent and sign-off. Do not call the neutral midpoint or either range endpoint a product score.

##### Bridge

Return to the bounded decision: direction plus proof, not critical scale.

##### Caveat

The 0–10 bounds are uncertainty limits, not performance estimates or probabilities. Numerical-input coverage is 60%, common score-capable evidence coverage is 0%, and 30 mandatory gates remain unknown. Traceable earns no native Kong points. Control-plane responsibility is an operating-risk and cost input, not a legal-liability conclusion.

##### Sources

- Canonical sanitized arithmetic audit: [Kong guided evaluation — Supplied scoring audit](48-kong-guided-evaluation.md#supplied-scoring-audit).
- Provisional scenario and pending recalculation contract: [Kong guided evaluation — Provisional weighting and uncertainty scenario](48-kong-guided-evaluation.md#provisional-weighting-and-uncertainty-scenario), [Proposed governed re-score](48-kong-guided-evaluation.md#proposed-governed-re-score), and [Decision-matrix scoring guide](../decision-matrix/scoring-guide.md).
- Official contextual mechanisms (`E1` only): [Kong deployment topologies](https://developer.konghq.com/gateway/deployment-topologies/), [Kong AI Gateway](https://developer.konghq.com/ai-gateway/), [Kong pricing](https://konghq.com/pricing), [Apigee hybrid 1.16](https://docs.cloud.google.com/apigee/docs/hybrid/v1.16/what-is-hybrid), [Apigee pricing](https://cloud.google.com/apigee/pricing), [MuleSoft Omni Gateway](https://docs.mulesoft.com/gateway/latest/), [MuleSoft pricing](https://www.mulesoft.com/anypoint-pricing), and [Azure API Management self-hosted gateway](https://learn.microsoft.com/en-us/azure/api-management/self-hosted-gateway-overview).

##### Listen for

“The midpoint is the new score,” “the wide range proves every product is equal,” “choose the top historical total anyway,” or pressure to narrow a product's range without approved evidence and scoring roles.

##### Evidence-safe response

The calculation is complete as an uncertainty scenario, not as a governed product ranking. Its useful result is rank instability: Apigee needs only a 1.125-point higher average across the new 40% block to reverse Kong's historical-input lead; MuleSoft needs 2.4 points. The answer becomes more convincing only when equivalent evidence replaces those unknown ranges under independent scoring and preserved dissent.

##### Follow-up probe

Which decision-owner, enterprise-architecture, FinOps, criterion-owner, scorer, and independent-assurance roles own the method; what evidence and confidence rules apply; which sensitivity, bounds, and regret analyses will run; and who approves the resulting decision use?

##### Decision impact

An uncontrolled score can conceal mandatory unknowns, reward missing evidence, and create false precision around a conditional direction. A governed result may confirm, narrow, reverse, or leave the direction unresolved.

##### Capture

Record whether the room accepts, amends, or rejects the 60/40 planning split; the double-counting rule; exact options; mandatory gates; `GRS-01`–`GRS-06` disposition; rating and evidence authority; confidence and unknown handling; scorer and approver roles; sensitivity, bounds and regret; dissent; permitted use; and the governed recalculation due gate. Keep named-person assignments out of the public guide.

##### Branch/rejoin

Branch to slides 3–5 for weights, options, and arithmetic. Never close here; rejoin at slide 6 or 21.

##### HOLD/park

HOLD score-based authorization while ranges overlap, common score-capable evidence is 0%, or exact options, mandatory gates, approved weights/ratings, rubric, scorer independence, sensitivity, dissent and sign-off remain open. Park the governed recalculation only with role owners and explicit re-entry at slide 6.

## Local interactive assessment contract

This contract supports a public-safe, local-only meeting capture alongside the native presentation. Answers are **meeting input only**: they can record authorization, amendment, dissent, a hold, or an evidence request, but they are never evidence or scores and never become criterion gate results, confidence, or readiness. `Unanswered` is an interaction state and is not the same as the explicit `unknown` choice. No answer may upgrade the slide's evidence state or bypass the canonical option-resolution, evidence-ledger, mandatory-gate, scoring, or independent-review rules.

The generated public manifest exposes this question, choice-set, and reviewability definition; it never includes participant responses. A conforming interaction layer keeps responses in volatile memory or browser-local storage until the participant explicitly exports them; it does not send responses to a server or write them into the repository. Controlled role selectors accept only the canonical public-role values below and reject named-person assignments. Before storage or export, the interaction layer removes an affected value when it detects an obvious email, private URL, IP address, credential, phone number, or commercial-quote pattern. Automated filtering is not exhaustive: participants must not enter names, customer or organization identifiers, private topology, security findings, credentials, commercial quotes or terms, private URLs, raw logs, payloads, or restricted evidence. Use controlled restricted-reference IDs instead.

`Minimum evidence` is the floor required before the question's subject may influence the named decision; it is not evidence supplied by the answer. `Mandatory` means the question must be dispositioned on the full decision route. Route-specific questions may remain not assessed when that scope is not authorized. The full contract contains 18 questions; Phase 1 carries six, including one explicit question for each early gate. A completed question count is meeting progress only: never calculate or display a readiness percentage.

### Assessment interface terminology

The assessment drawer and summary project this ordered terminology rail before any form or export control that uses the token. It defines interface language only; the question and slide evidence boundaries remain authoritative.

| Token | Exact visible term | Interface purpose |
|---|---|---|
| API | application programming interface (API) | Assessment prompt and target context |
| EAG | Early Assessment Gate (EAG) | Phase 1 scope and evidence-gate identifiers |
| APIM | Azure API Management (APIM) | Phase 2 counterfactual option identifier |
| E0 | assertion-only evidence (E0) | Participant evidence-level selector |
| E1 | current official documentation (E1) | Participant evidence-level selector |
| E2 | vendor answer with named version or contract term (E2) | Participant evidence-level selector |
| E3 | repeatable lab evidence (E3) | Participant evidence-level selector |
| E4 | representative pilot evidence (E4) | Participant evidence-level selector |
| ID | identifier (ID) | Public-safe target and artifact fields |
| BOM | bill of materials (BOM) | Exact-option field guidance |
| JSON | JavaScript Object Notation (JSON) | Structured local-export format |
| URL | uniform resource locator (URL) | Privacy warning and public references |
| IP | Internet Protocol (IP) | Privacy warning |
| IAM | identity and access management (IAM) | Controlled public-role label |
| SRE | site reliability engineering (SRE) | Controlled public-role label |
| FinOps | financial operations (FinOps) | Controlled public-role label |
| N/A | not applicable (N/A) | Explicit route-specific response state |
| TCO | total cost of ownership (TCO) | Phase 1 cost question and summary |
| HA | high availability (HA) | Phase 1 cost question and summary |
| DR | disaster recovery (DR) | Phase 1 cost question and summary |

### Assessment questions

| Question ID | Phase ID | Slide IDs | Existing target IDs | Prompt | Decision use | Evidence boundary | Minimum evidence | Mandatory | Choice set ID | Hold rule |
|---|---|---|---|---|---|---|---|---|---|---|
| KGE-P1-Q01 | KGE-P1 | KGE-01 | KGE-AUTH-01..KGE-AUTH-05 | Does the room approve, amend, or hold the bounded decision question, authority, non-goals, and explicitly unauthorized scope? | Establish whether the meeting can authorize a bounded direction and proof programme. | A meeting authorization is governance input; it does not prove platform fit or production readiness. | E1 | true | KGE-CS-AUTHORIZATION | HOLD without a decision owner or an accepted bounded decision question. |
| KGE-P1-Q02 | KGE-P1 | KGE-02; KGE-03 | GTM-01..GTM-09 | Which target operating-model inputs are confirmed, amended, rejected, or unknown? | Freeze the target inputs that define the decision boundary before weights or option fit are interpreted. | Stakeholder confirmation does not create observed-estate evidence, assign product ratings, approve a governed score, or make the target viable. | E1 | true | KGE-CS-INPUT | HOLD weighting and option-fit interpretation when a material target input lacks an accountable owner and closure evidence. |
| KGE-P1-Q03 | KGE-P1 | KGE-02; KGE-03 | EAG-04; GSA-01; GEP-07; GEC-20 | Is the optional `KP-SMH1 + GSA-01` Kong-plus-Traceable solution profile confirmed for bounded study, amended, rejected, or unknown? | Decide whether the third-party adjunct profile enters the proof programme and freeze its baseline, exact boundary, owners, evidence request, and safe-removal obligation. | Early admission is scope input only; Traceable remains a third-party `E1` feasibility hypothesis and earns no native Kong score, security conclusion, traceability conclusion, cost conclusion, or production authorization. | E1 | true | KGE-CS-INPUT | HOLD composite-profile authorization when the profile is undispositioned, counted as native Kong capability or score, or lacks a frozen baseline, data/failure boundary, owner, support/cost request, and safe-removal obligation. |
| KGE-P1-Q04 | KGE-P1 | KGE-02; KGE-03 | EAG-01; GTM-08; GRS-01; GEC-07 | Are the required multicloud/private placements, request locality, management dependencies, sovereignty, failure independence, support boundary, and per-cell cost confirmed, amended, rejected, or unknown? | Freeze the multicloud operating-fit question and the representative failure, recovery, scaling, and cost evidence request before bounded authorization. | An early placement disposition is not executed multicloud fit, resilience, scale, sovereignty, support, or cost evidence and cannot create a product rating. | E1 | true | KGE-CS-INPUT | HOLD bounded authorization when a mandatory placement, data flow, dependency, owner, support boundary, or proof obligation is unknown. |
| KGE-P1-Q05 | KGE-P1 | KGE-02; KGE-03 | EAG-02; GRS-04; GEC-16 | Is the required clean-exit profile—configuration, policy, identity/product state, data/history, plugins, evidence, procedures, rebuild denominator, route-back, and residual dependency—confirmed, amended, rejected, or unknown? | Distinguish a same-vendor custody switch from true non-Kong exit and freeze the reversible-foundation obligation. | A portability statement or meeting preference is not an executed non-source rebuild, semantic-loss measure, timed route-back, residual-dependency result, or exit-cost finding. | E1 | true | KGE-CS-INPUT | HOLD bounded authorization when the proposed foundation lacks a named exit profile, reversal trigger, rebuild denominator, owner, or safe route-back obligation. |
| KGE-P1-Q06 | KGE-P1 | KGE-02; KGE-03 | EAG-03; GEW-08; GRS-05; GEC-17 | Is the common fully allocated TCO denominator—time horizon, low/base/high cases, meters/quotes, labor, infrastructure, HA/DR, telemetry, adjuncts, support, migration, dual run, incident exposure, custody switch, and exit—confirmed, amended, rejected, or unknown? | Freeze the cost-efficiency question, FinOps/sourcing ownership, evidence references, and sensitivity method before a price or cost claim influences authorization. | Public pricing, license inputs, or an early denominator choice are not comparable TCO, unit-economics, negotiated-terms, or production-cost evidence. | E1 | true | KGE-CS-INPUT | HOLD any price or cost claim that influences authorization without a common denominator, FinOps/sourcing owner, evidence request, and sensitivity method. |
| KGE-P2-Q01 | KGE-P2 | KGE-04 | GEO-KONG; GEO-APIGEE; GEO-MULE; GEO-APIM | Which conditional option counterfactuals stay in scope, require symmetric evidence, or are excluded with an explicit rationale? | Record the conditions that could narrow Kong, switch custody, or reopen option selection. | A fit condition or exclusion is meeting scope, not comparative product evidence or a rank. | E1 | true | KGE-CS-COUNTERFACTUAL | HOLD if an agreed mandatory counterfactual condition is unresolved without symmetric evidence. |
| KGE-P2-Q02 | KGE-P2 | KGE-05; KGE-06; KGE-07; KGE-08 | GEW-01..GEW-08; KGE-AUTH-01..KGE-AUTH-05; GEB-01..GEB-03; KMC-1; KMC-3; KPS-FIT-01; KPS-FIT-02 | Does the room approve, amend, or hold the historical score's audit-only use, bounded authorization, operating boundary, custody benchmark, true exit, and funded duty? | Set the authorization boundary and accountable operating commitments without manufacturing a new total. | Historical ratings remain stakeholder input; role acceptance and architecture preference are not E2/E3 behavior, economics, or legal conclusions. | E2 | true | KGE-CS-AUTHORIZATION | HOLD if the score is used for authorization or the exact boundary, funded duty, custody benchmark, or true exit lacks an owner. |
| KGE-P3-Q01 | KGE-P3 | KGE-09; KGE-10; KGE-11 | KPS-1; KPS-2; KPS-4 | Are the control, request, trust, evidence, degraded-admission, probe, threshold, owner, and reconciliation boundaries accepted, amended, held, or unknown? | Freeze the target-shaped architecture and admission questions that the proof programme must test. | An accepted model remains proposed until the exact option executes the linked tests with reviewable artifacts. | E3 | true | KGE-CS-REVIEW | HOLD target freeze when a mandatory boundary, probe, state identity, response owner, or reconciliation rule is unknown. |
| KGE-P3-Q02 | KGE-P3 | KGE-12; KGE-13 | KPS-3; KPS-5; KP0..KP5 | Are the funded ownership model and each adoption gate's entry evidence, exit evidence, and stop authority accepted, amended, held, or unknown? | Decide whether foundation and later phase transitions have accountable owners and evidence exits. | Role and gate agreement does not show that a gate has passed or that a scenario window is a commitment. | E3 | true | KGE-CS-REVIEW | HOLD a phase transition that lacks funded ownership, exit evidence, or stop authority. |
| KGE-P4-Q01 | KGE-P4 | KGE-14; KGE-16 | MULE-2; MULE-6; A0..A6 | Which source archetype applies, and is its responsibility, durable-state, destination, ownership, and object-state denominator sufficiently classified? | Select the applicable migration rail and create bounded classification work. | A selected source or taxonomy is not observed workload parity, converter success, migration progress, or decommission evidence. | E3 | false | KGE-CS-SOURCE | When migration is in scope, HOLD if source, responsibility, durable state, destination, denominator, or owner is unknown. |
| KGE-P4-Q02 | KGE-P4 | KGE-15; KGE-16 | MULE-3; MULE-6; A2..A6 | Are cohorting, parity, business verification, reconciliation, route-back, per-wave evidence, and dependency-zero controls accepted, amended, held, or unknown? | Determine whether a migration cohort or wave can be designed without authorizing irreversible cutover. | A control design or exported bundle is not executed parity, safe rollback, or dependency-zero evidence. | E3 | false | KGE-CS-REVIEW | When migration is in scope, HOLD a cohort without parity, business verification, reconciliation, route-back, and dependency-zero evidence. |
| KGE-P5-Q01 | KGE-P5 | KGE-17 | KGE-PROOF-01..KGE-PROOF-03 | Does the room accept the current non-additive evidence baseline, dispute a specific result state, or leave it unknown? | Freeze the starting evidence boundary before authorizing new proof. | Acceptance preserves the recorded state and limitations; it does not convert local checks, protocols, or counts into target-option evidence. | E3 | true | KGE-CS-EVIDENCE | HOLD any readiness percentage or production claim derived from the non-additive baseline systems. |
| KGE-P5-Q02 | KGE-P5 | KGE-18 | GEP-01..GEP-07; GSA-01 | Does each proof workstream have an authorized exact option or BOM, method, measure, threshold, raw artifact, reviewer, due gate, and stop rule? | Authorize, amend, or hold target-shaped proof work without authorizing production scale. | Authorizing a test is not executing it; GEP-07 remains adjunct feasibility until independently reviewed evidence closes its exact boundary. | E3 | true | KGE-CS-AUTHORIZATION | HOLD a workstream missing its exact option, environment, measure, threshold, artifact, reviewer, or stop rule. |
| KGE-P5-Q03 | KGE-P5 | KGE-19; KGE-20 | KO-1..KO-11 | Is each outcome contract ready, or does its measure, target, artifact, cadence, owner, reviewer, or failure disposition require amendment, hold, or an unknown state? | Freeze the acceptance contract before demonstrations can be interpreted as outcomes. | `contract-ready` describes the test contract only; it is never a pass, achieved result, platform score, or production-readiness claim. | E3 | true | KGE-CS-CONTRACT | HOLD an outcome without an approved measure, threshold, raw artifact, reviewer, and failure disposition. |
| KGE-P5-Q04 | KGE-P5 | KGE-21 | KPS-6; KGE-AUTH-01..KGE-AUTH-05 | Does the room approve, amend, or hold the authority and triggers to scale, narrow, switch custody, exit, or hold? | Pre-commit evidence consequences, dissent handling, fallback, and the next decision forum. | Decision authority cannot substitute for E3/E4 outcome evidence; critical production scale remains unauthorized until its gates close. | E3 | true | KGE-CS-AUTHORIZATION | HOLD when failed or unknown mandatory evidence cannot change the outcome. |
| KGE-P6-Q01 | KGE-P6 | KGE-22; KGE-23; KGE-24 | GEC-01..GEC-20 | Should each supplied comparison claim remain stakeholder input, become a symmetric evidence request, be rejected, or remain unknown? | Preserve the audit trail and move unverified claims into governed proof without scoring in the room. | Retaining or questioning a claim does not promote it to documented fact, observed result, comparative proof, price rank, or production conclusion. | E1 | false | KGE-CS-CLAIM | HOLD if a mandatory decision depends on an unverified claim, label, price, or generic scale assertion. |
| KGE-P6-Q02 | KGE-P6 | KGE-25 | GEW-01..GEW-08; GRS-01..GRS-06 | Does the room accept, amend, or reject the provisional weights and uncertainty treatment, and what remains before a governed re-score? | Preserve scenario amendments and authorize the exact-option, gate, evidence, scorer, sensitivity, dissent, and sign-off work. | This response cannot assign product ratings, criterion results, confidence, rank, or a new decision score; meeting input cannot narrow the unknown ranges. | E3 | false | KGE-CS-AUTHORIZATION | HOLD score-based authorization until common score-capable evidence, approved ratings, independent scoring, rank-stability analysis, dissent, and sign-off close. |

### Stable choice sets

Choice outcomes describe meeting workflow only. `pass` means that the room affirmatively dispositioned the meeting question; it does not mean a criterion or gate passed and never upgrades evidence, readiness, confidence, or score. `inform` records a non-blocking scope or follow-up disposition. `Unknown` must be chosen explicitly and creates the evidence-gap treatment described by the question's hold rule. `Not assessed` is permitted only for route-specific scope and is not evidence-level `unknown` or criterion `not-applicable`.

| Choice set ID | Label | Choice value | Choice label | Outcome |
|---|---|---|---|---|
| KGE-CS-AUTHORIZATION | Authorization disposition | approve | Approve the bounded item | pass |
| KGE-CS-AUTHORIZATION | Authorization disposition | amend | Amend before authorization | amend |
| KGE-CS-AUTHORIZATION | Authorization disposition | hold | Hold the item | hold |
| KGE-CS-INPUT | Input disposition | confirm | Confirm as meeting input | pass |
| KGE-CS-INPUT | Input disposition | amend | Amend the input | amend |
| KGE-CS-INPUT | Input disposition | reject | Reject the input | amend |
| KGE-CS-INPUT | Input disposition | unknown | Unknown; create an evidence gap | unknown |
| KGE-CS-COUNTERFACTUAL | Counterfactual disposition | retain-counterfactual | Retain as a bounded counterfactual | pass |
| KGE-CS-COUNTERFACTUAL | Counterfactual disposition | authorize-symmetric-evidence | Authorize a symmetric evidence request | pass |
| KGE-CS-COUNTERFACTUAL | Counterfactual disposition | exclude-with-rationale | Exclude with an explicit rationale and reversal condition | inform |
| KGE-CS-COUNTERFACTUAL | Counterfactual disposition | unknown | Unknown; keep the option question open | unknown |
| KGE-CS-REVIEW | Contract review | accept | Accept the proposed contract boundary | pass |
| KGE-CS-REVIEW | Contract review | amend | Amend the contract boundary | amend |
| KGE-CS-REVIEW | Contract review | hold | Hold the affected authorization | hold |
| KGE-CS-REVIEW | Contract review | unknown | Unknown; create an evidence gap | unknown |
| KGE-CS-SOURCE | Source archetype | mule | Mule source rail applies | inform |
| KGE-CS-SOURCE | Source archetype | apigee | Apigee source rail applies | inform |
| KGE-CS-SOURCE | Source archetype | both | Both source rails apply separately | inform |
| KGE-CS-SOURCE | Source archetype | not-assessed | Migration is not assessed on this route | not-applicable |
| KGE-CS-SOURCE | Source archetype | unknown | Source archetype remains unknown | unknown |
| KGE-CS-EVIDENCE | Evidence-baseline review | accept-current-state | Accept the recorded state and limitations | pass |
| KGE-CS-EVIDENCE | Evidence-baseline review | dispute | Dispute a specific result state | amend |
| KGE-CS-EVIDENCE | Evidence-baseline review | unknown | Current state remains unknown | unknown |
| KGE-CS-CONTRACT | Outcome-contract readiness | contract-ready | Contract fields are defined for later execution | pass |
| KGE-CS-CONTRACT | Outcome-contract readiness | amend | Amend one or more contract fields | amend |
| KGE-CS-CONTRACT | Outcome-contract readiness | hold | Hold the outcome contract | hold |
| KGE-CS-CONTRACT | Outcome-contract readiness | unknown | One or more contract fields remain unknown | unknown |
| KGE-CS-CLAIM | Supplied-claim treatment | retain-as-stakeholder-input | Retain as stakeholder input only | pass |
| KGE-CS-CLAIM | Supplied-claim treatment | create-evidence-request | Create a symmetric evidence request | inform |
| KGE-CS-CLAIM | Supplied-claim treatment | reject | Reject the supplied claim | amend |
| KGE-CS-CLAIM | Supplied-claim treatment | unknown | Claim treatment remains unknown | unknown |

### Reviewability requirements

These fields make reviewability auditable; they do not make an answer evidence or authorize production. `holdRuleStatus` has the controlled values `open` and `closed`. `closed` means the canonical question hold rule has been dispositioned; it never means an evidence, criterion, or production gate passed. A HOLD state exists when the meeting decision is HOLD, a selected choice has the `hold` outcome, or any applicable hold rule remains `open`.

| Manifest field | Applies when | Canonical values | Rule |
|---|---|---|---|
| reviewRequirements.sessionRequired | Every assessment session | meetingDecision; decisionOwnerRole; authorizedScope; unauthorizedScope; nextForum | The session is not reviewable until every field is present and the meeting decision records an explicit approve, amend, or hold disposition. |
| reviewRequirements.mandatoryResponseRequired | Every answered mandatory question | rationale; ownerRole; dueGate; holdRuleStatus | An answered mandatory question is not reviewable until every field is present and `holdRuleStatus` is `closed`. |
| reviewRequirements.evidenceClaimRequired | Any participant `evidenceLevel` claim equal to or above the question's `minimumEvidence` | evidenceReference | The reference is required for gap triage, remains user-provided and unverified, and cannot upgrade canonical evidence. |
| reviewRequirements.holdStateRequired | Any HOLD state | holdReason | Record one public-safe session-level reason that explains the unresolved hold; an empty reason keeps the session on HOLD. |
| reviewRequirements.sessionExportFields | Every local export and generated summary | deckRevision; meetingDecision; decisionOwnerRole; authorizedScope; unauthorizedScope; assumptions; actions; dissent; nextForum; holdReason | Preserve these as distinct session fields; do not synthesize them from response counts or free-form notes. |
| reviewRequirements.responseExportFields | Every answered question in a local export or generated summary | choice; evidenceLevel; evidenceReference; criterionId; optionId; evidenceRequest; restrictedReferenceId; rationale; ownerRole; dueGate; holdRuleStatus; dissent; nextForum | Preserve these as distinct response fields; empty optional values remain explicit and never inherit from another response. |
| reviewRequirements.privacyControls | Before browser-local storage and before export | controlled-role-selectors; remove-obvious-email-patterns; remove-obvious-private-url-patterns; remove-obvious-ip-address-patterns; remove-obvious-credential-patterns; remove-obvious-phone-number-patterns; remove-obvious-commercial-quote-patterns; automated-filtering-not-exhaustive | Role selectors reject named-person assignments; affected values matching obvious personal or restricted patterns are removed, and the UI warns that automatic filtering cannot identify every sensitive value. |
| publicRoles | Any session or response role field | Decision owner; Enterprise architecture; Platform product; Security architecture; IAM; SRE/performance; FinOps; Migration lead; Independent assurance; Legal/procurement; Service owner; Unassigned role | Store and export only one of these public role values; use `Unassigned role` instead of a person's name or an invented role label. `Unassigned role` remains unresolved and cannot satisfy a required role field. |

### Local-only storage and export boundary

| Boundary | Required behavior |
|---|---|
| Runtime storage | Keep response state in volatile memory or browser-local storage for the current user. Bind each record's immutable `deckRevision` to the exact built manifest `sourceRevision`. Do not transmit, synchronize, publish, or write responses into the generated manifest or repository. |
| Unanswered state | Store a missing response as `unanswered` with no inferred choice. Only an explicit `unknown` response creates an unknown disposition and its evidence-gap or hold treatment. |
| Local export | Export only on an explicit user action. Include the exact `deckRevision`; session timestamps; question, phase, slide, and target IDs; selected choice; and every canonical session and response export field above. |
| Evidence linkage | Export controlled canonical `criterionId`, exact `optionId`, `evidenceRequest`, and `restrictedReferenceId` only when supplied. A response-level `evidenceLevel` (`E0`–`E4`) or `evidenceReference` is a user-provided, unverified claim for gap triage: it never writes or upgrades the canonical evidence ledger and cannot change slide or criterion evidence. A response never writes `score` or `gate_status`. |
| Summary | Report the distinct session fields `authorizedScope`, `unauthorizedScope`, `assumptions`, `actions`, `dissent`, `nextForum`, and `holdReason`, plus response-level dissent, evidence gaps, and actions. Do not report a readiness percentage, inferred product confidence, or a rank from response counts. |
| Privacy | Use only controlled public-role selectors. Remove affected values containing obvious personal or restricted patterns before storage and again before export, and warn that automated filtering is not exhaustive. |

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

Seed the ledger with eight records: `EAG-01` for multicloud operating fit, `EAG-02` for clean exit/vendor dependency, `EAG-03` for fully allocated TCO/cost efficiency, and `EAG-04` for Kong-plus-Traceable composite admission on slides 2–3; `D-001` for the bounded decision on slide 6; `E-001` for a not-run workstream on slide 18; `A-001` for a target or timeline assumption on slide 13; and `X-001` for a decision-changing counter-hypothesis on slide 21.

Seed these public-safe follow-up actions when the corresponding scope remains authorized. Public artifacts use accountable roles only; named-person assignments belong in the approved restricted system.

| Action ID | Public-safe action | Status to preserve | Accountable role and contributors | Due gate | Closure evidence |
|---|---|---|---|---|---|
| KGE-ACT-01 | Disposition `EAG-04`, then define and execute GEP-07 Kong-plus-Traceable feasibility against the security team’s Mule baseline when the composite profile remains admitted | Early admission and proof contract published; execution not started | Security architecture and platform product; SRE/performance, privacy, support, FinOps, and independent security assurance contribute | EAG-04 at KP0; execution at KP1/KP2 | Admission record plus certified exact BOM/support, data/failure-path review, coverage corpus, raw security/performance/fault results, correlation, lifecycle, cost, rollback/removal, and disposition |
| KGE-ACT-02 | Disposition `EAG-01`–`EAG-03`, then approve the multicloud, scalability/robustness, security/traceability, reversibility/vendor-dependency, full-TCO, and control-plane-responsibility re-score dimensions | Early gates and provisional 60/40 weights documented; accountable approval remains open | Decision owner and enterprise architecture with security, FinOps and independent assessment assurance | KP0 | Explicit early-gate dispositions plus approved `GRS-01`–`GRS-06` specification, exact options, mandatory gates, rubric, evidence floor, confidence, weights/ranges, sensitivity, dissent, and decision rule |
| KGE-ACT-03 | Execute and independently assure the governed recalculation | Provisional uncertainty envelope calculated; governed re-score remains open until method, evidence, independent scoring and sign-off close | Independent assessment assurance with criterion owners and approved scorer/approver roles | After method and evidence freeze | Reproducible inputs/calculation, evidence links, lower/upper bounds, maximum regret, rank-stability sensitivity, dissent, reviewer record, and permitted use |
| KGE-ACT-04 | Use and distribute the Kong terminology crosswalk for the stakeholder follow-up | Public follow-up package prepared; delivery awaits recipient and approved channel | Platform product enablement with Mule/Apigee migration architecture | Post-meeting enablement gate | Public crosswalk link, recorded non-equivalences, owner for unresolved mappings, and mapping evidence request |
| KGE-ACT-05 | Apply the Apigee A0–A6 migration roadmap before any source wave design | Roadmap and migration-factory control pack published; execution not started | Migration architecture with API product, IAM/security, SRE, domains, sourcing/FinOps, and independent assurance | Before Apigee wave authorization | Source-archetype and object/state denominator, semantic map, parity corpus, coexistence, reconciliation, route-back, and dependency-zero evidence contract |

### Ready-to-send terminology follow-up

Use the public-safe message below after replacing the bracketed role greeting. Do not add customer names, private topology, commercial terms, security findings, or meeting-only details. External delivery is complete only when the approved recipient and channel are recorded in the restricted action system.

**Subject:** Kong terminology crosswalk and migration questions

> Hello [role/team],
>
> Following our API-platform discussion, here is the Kong terminology crosswalk: <https://tomqwu.github.io/apim/#/doc/research-glossary>.
>
> The mappings are nearest operating analogues, not one-to-one translations. In particular, a Kong Gateway Service is not the complete API product or contract; a Consumer is not automatically the portal application or workforce identity; a Workspace is not by itself a capacity, network, recovery, or legal boundary; and decK does not manage every platform artifact or make multiple writers safe.
>
> Please review the non-equivalence column and identify any MuleSoft or Apigee object whose owner, state authority, lifecycle, policy precedence, audit requirement, or migration destination remains unclear. The detailed Apigee A0–A6 roadmap is here: <https://tomqwu.github.io/apim/#/doc/docs-50-apigee-migration-strategy>. The guided deck is here: <https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/0>.
>
> Requested response: source term/object, required behavior and state, current owner, proposed Kong or enterprise destination, unresolved non-equivalence, and the evidence needed to approve the mapping.

Repository references: [terminology crosswalk](../research/glossary.md#kong-terminology-crosswalk), [Apigee migration strategy](50-apigee-migration-strategy.md), and [guided evaluation](48-kong-guided-evaluation.md).

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
- “These concerns are absent or compressed in the supplied scorecard, not the canonical matrix.”
- “`EAG-01`–`EAG-04` are opening scope-and-evidence gates; their disposition is not proof that the subject passed.”
- “The governed re-score is pending; no weight, rating, or total is being changed in this meeting.”
- “Traceable documents a third-party integration path; GEP-07 must prove the required outcome in the exact target.”
- “Self-managed custody transfers operating accountability and risk exposure; this is not a legal-liability determination.”
- “The terminology crosswalk provides nearest analogues, not one-to-one migration mappings.”

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
- “We dispositioned the early gate, so multicloud, clean exit, cost efficiency, or Traceable fit is proved.”
- “Traceable makes Kong security and traceability proven.”
- “Traceable is another gateway contender or earns Kong platform points.”
- “The re-score should make the recommendation more convincing.”
- “An exported Apigee proxy bundle is the migration roadmap.”
- “The architecture determines legal liability.”
- Any Kong Enterprise 3.14 claim that omits the exact patch, entitlement, plugin, topology, support, and as-of boundary required by the decision.

## Stop and hold rules

Stop the decision or record **HOLD** when:

- the target assumptions are materially disputed and have no owner or closure evidence—do not continue to weights or scoring;
- any applicable `EAG-01`–`EAG-04` question is undispositioned, explicitly unknown without accountable closure, or being treated as executed evidence;
- multicloud placement, a clean exit, cost efficiency, or Kong-plus-Traceable fit is asserted from an early meeting disposition rather than the linked `E2`–`E4` evidence;
- self-managed control has no funded, accountable owner for control-plane, database, PKI, release, restore, observability, support, or on-call duties;
- the exact target option, environment, measure, threshold, artifact, reviewer, or stop rule is not frozen—do not call the work proof;
- a migration cohort lacks business parity, durable-state authority, reconciliation, or route-back;
- an unknown or failed mandatory gate is being offset by a weighted score;
- a historical score is being recalculated before exact options, added dimensions, weights/ranges, rubric, score-capable evidence, confidence, scorer independence, sensitivity/bounds/regret, and dissent rules are approved;
- Traceable is being treated as a gateway option or as proof of security, traceability, parity, cost, or production fit without independently reviewed GEP-07 evidence;
- an Apigee wave is being authorized from proxy bundles without the object/state denominator, semantic mapping, identity/state reconciliation, route-back, and dependency-zero contract;
- the evidence does not preserve failed runs, gaps, dissent, and limitations; or
- negative evidence is not permitted to narrow, switch custody, exit, or hold.

## Close the meeting

The chair should read back only:

1. what is approved now;
2. what remains explicitly unauthorized;
3. which assumptions were amended or rejected;
4. how `EAG-01` multicloud, `EAG-02` clean exit/vendor dependency, `EAG-03` fully allocated TCO, and `EAG-04` Kong-plus-Traceable admission were dispositioned;
5. which evidence requests, owners, reviewers, thresholds, due gates, and stop rules were created;
6. which public role owns each requested follow-up, including scoring governance, GEP-07, terminology enablement, and Apigee migration planning; and
7. whether the next state is proceed, amend, or hold.

Recommended close:

> We are approving a reversible direction and the work required to test it. Critical production scale remains blocked until reviewed target-shaped evidence changes that status.

End on [slide 6](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/5) when the decision is about authorization, or [slide 21](https://tomqwu.github.io/apim/#/present/kong-platform-journey-guided/20) when it is about evidence consequences. Never end on a raw score or appendix label.

## References and limitations

The complete slide sections above are the point-of-use facilitation and speaker-notes source. The PowerPoint carries a synchronized concise projection. The canonical studies below continue to own product facts, evidence meanings, and decision content:

- [Kong guided evaluation](48-kong-guided-evaluation.md), including [Four early assessment gates](48-kong-guided-evaluation.md#four-early-assessment-gates)
- [Assessment methodology](03-assessment-methodology.md)
- [Kong enterprise platform deployment strategy](47-kong-enterprise-platform-strategy.md)
- [Kong multicloud study roadmap](44-kong-multicloud-study-roadmap.md)
- [Mule migration strategy](35-mule-migration-strategy.md)
- [Apigee migration strategy](50-apigee-migration-strategy.md)
- [Kong terminology crosswalk](../research/glossary.md#kong-terminology-crosswalk)
- [Traceable by Harness security-adjunct feasibility](48-kong-guided-evaluation.md#traceable-by-harness-security-adjunct-feasibility)
- [Traceable Kong integration documentation](https://docs.traceable.ai/kong)
- [Current PoC register and evidence boundary](../poc/README.md)
- [Presentation artifact contract](../presentations/README.md)

This is public-safe facilitation guidance. It contains no meeting minutes, named-person assignment, commercial term, private topology, or observed production outcome. Store restricted decisions and evidence in the approved private system; publish only sanitized, authorized conclusions through the repository workflow.
