# Kong guided evaluation facilitator guide

| Field | Value |
|---|---|
| Artifact type | meeting-facilitation-guide |
| Meeting question | Should we approve, change, or hold a small, reversible Kong start and the tests needed before production scale? |
| Decision owner | Application programming interface (API) platform product owner, supported by architecture, security, platform, reliability, migration, sourcing, finance, service-management, delivery, and independent-review leads |
| Intended users | Product owner, meeting chair, presenter, note taker, evidence reviewer, timekeeper, and the technical or commercial leads who will own follow-up work |
| Scope | Meeting opening, full scripts and three talking points for all 25 slides, four early questions, an 18-question local assessment, meeting routes, challenge responses, decision capture, stop conditions, and a closing checklist |
| Evidence state | Meeting guidance based on the guided evaluation and slide notes. It adds no new product claim, test result, price conclusion, or production approval. |
| As-of date | 2026-08-22; use the current canonical study and deck revision when facilitating |
| Next gate | Answer Early Assessment Gate (EAG) 01–04, then record approve, change, or hold. For every approved test, name its owner, measure, proof, reviewer, due date, and stop condition. |

## Use this guide with the presentation

This is the **complete meeting and speaker-notes guide** for the Kong evaluation. Every slide has a ready-to-say script and three short talking points. It also includes the purpose, question to ask, transition, caution, sources, likely challenges, safe responses, follow-up questions, decisions to capture, and places to pause. Use this page to prepare the meeting, present the story, handle challenges, or hand the meeting to another facilitator.

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
- [Inspect the current Proof of Concept (PoC) evidence boundary](../poc/README.md)

If this guide and a source study disagree, use the source study. Do not publicly link the raw supplied input; the public guided evaluation contains the safe decision context.

### Acronym and identifier reading rule

Every speaker-note card is independently enterable. At the top of each card, the native page therefore projects the canonical slide-local terms as **Full Name (ACRONYM)** before the detailed notes use shorthand. The card kicker introduces **Kong Guided Evaluation (KGE)**, and each visible slide title expands any slide-local shorthand it contains. Stable record identifiers keep their published code plus a plain-language descriptor; the guide never invents a long form for an internal ID.

Apply the same rule in meeting artifacts and follow-up documents: expand an unfamiliar acronym at its first visible use in every independently opened document, section, slide, table, or note. A linked glossary is supporting context, not a substitute for the first-use expansion.

### Plain-language decision words

In the room, say **approve, change, or hold**. In the formal assessment record and export, **change** is stored as **amend**, and a request to **pause** is stored as **hold**. This is one three-state decision vocabulary, not two different decision models.

## Opening the meeting

### Suggested opening script — 2 to 3 minutes

Good morning. Today we are testing a clear working thesis: if the product owner's priorities are Kubernetes-based delivery, Git-reviewed change, distributed gateways, and accountable platform ownership, Kong is the strongest strategic fit for the application programming interface (API) platform we want to build. We will first confirm those priorities, then decide whether to fund a controlled first implementation to test the thesis.

If those priorities hold, Kong is the better strategic fit because its operating model aligns with them. It could give teams faster delivery, stronger control over where traffic runs, and a more portable foundation for modernization. These are the outcomes we want; they are not results we have proved. If the priorities change, the recommendation can change too.

We also need to test the cost of that control. Self-managed Kong creates ongoing responsibility for operations, recovery, security, upgrades, support, and evidence. Four Early Assessment Gates (EAGs) bring the biggest open questions into the discussion now: multicloud fit, the ability to change providers or exit, full Total Cost of Ownership (TCO), and whether to include Kong with Traceable by Harness as an optional security add-on in the study.

By the end of the meeting, we need one of three outcomes: approve a small, controlled Kong foundation and test plan; change the proposal; or hold it. We also need owners, proof, due dates, and clear reasons to stop or change direction. We are not approving critical production scale today.

I will keep the strength of each claim visible. Documentation can tell us what to test. A version-specific answer can close a narrow question. A repeatable result in a production-like lab is stronger, and a representative pilot is stronger again. We will not call a capability proven until the evidence supports that conclusion.

Challenges are welcome. If you disagree, please say what decision could change and what evidence would settle the question. Each slide follows the same path: business outcome → why Kong fits → what could change the answer → decision. We can open a detailed slide, but we will return to slide 6 for authorization or slide 21 for the final outcome.

Before we begin, please confirm the decision owner, scribe, evidence reviewer, and timekeeper. Then we will start with why Kong fits the strategy and what must be true for us to proceed.

### Opening talking points

- Working thesis: if the stated priorities hold, Kong is the leading strategic fit because its operating model aligns with them.
- The meeting decides whether to approve, change, or hold a controlled implementation and test plan—not production scale.
- Every open risk needs an owner, evidence, due date, and a clear condition that would stop or change the direction.

## What the meeting must produce

The meeting succeeds only when it produces a decision record, not when it reaches the last slide. The chair should secure:

1. an explicit **approve, change, or hold** answer for the small Kong start;
2. a clear statement of what may begin now and what may not;
3. an answer for `EAG-01` multicloud fit, `EAG-02` ease of exit and vendor dependency, `EAG-03` full Total Cost of Ownership (TCO), and `EAG-04` the optional Kong-plus-Traceable study;
4. named role owners for ongoing operations, MuleSoft and Apigee migration safety, the seven test workstreams, scoring, terminology support, and independent review;
5. a measure, result record, reviewer, due date, and stop condition for every important unknown;
6. any disagreement and the evidence that could change the answer; and
7. the date and forum for the next decision.

The meeting does **not** approve broad production scale, declare a universal product winner, change a score to protect a preferred result, treat old ratings as new evidence, count a third-party integration as native Kong capability, promise unsupported roadmap dates, or treat documentation as a completed test.

## Roles in the room

| Role | Responsibility during the meeting |
|---|---|
| Chair / decision owner | States what the meeting may decide, keeps the discussion in scope, makes or pauses the decision, and reads back the result. |
| Facilitator / presenter | Guides the chosen route, explains how strong each claim is, handles challenges, and returns the room to slide 6 or 21. |
| Note taker | Records decisions, open evidence, actions, disagreements, and parked topics as they happen. |
| Evidence reviewer | Challenges unsupported claims and confirms the source, product version, test result, setup, and limits. |
| Timekeeper | Protects each timebox and signals when a challenge needs an owner, should be parked, or belongs in the appendix. |
| Accountable leads | Security and Identity and Access Management (IAM), architecture, platform and database, Site Reliability Engineering (SRE), migration, sourcing, Financial Operations (FinOps), service management, privacy, product enablement, and independent review test the claims they will own. |

Before opening slide 1, name the chair, scribe, evidence steward, and timekeeper. A meeting without a decision owner should be converted to a working session and must not produce an authorization.

## Evidence vocabulary and room rules

Use the evidence ladder consistently:

| Evidence state | What it can support | What it cannot support |
|---|---|---|
| Stakeholder input | Priorities, intent, questions, and ideas to test | Independent product fit or a proven outcome |
| `E1` documented mechanism | Designing a useful test | Proof that the purchased version, configured setup, operations, cost, or production outcome will work |
| `E2` specific answer | Closing a narrow version, contract, support, or configuration question | Repeatable behavior in the proposed setup |
| `E3` production-like lab result | Repeatable behavior inside the agreed test setup | Representative production performance or adoption |
| `E4` representative pilot | The strongest evidence before broad scale, under expected controls, load, and operations | Proof that the result applies outside what was observed |

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

**Terms used in this section:** current official documentation (`E1`); vendor answer with a named version or contract term (`E2`); repeatable lab evidence (`E3`); representative pilot evidence (`E4`); Early Assessment Gate (`EAG`); high availability (`HA`); disaster recovery (`DR`); Total Cost of Ownership (`TCO`); Azure API Management (`APIM`); control plane (`CP`); Public Key Infrastructure (`PKI`); application programming interface operations (`APIOps`); Identity and Access Management (`IAM`); key-value map (`KVM`); Transport Layer Security (`TLS`); Proof of Concept (`PoC`); Model Context Protocol (`MCP`); Agent2Agent Protocol (`A2A`); artificial intelligence (`AI`); and bill of materials (`BOM`). Stable record identifiers refer to the self-managed hybrid target (`KP-SMH1`), security-adjunct hypothesis record `GSA-01`, proof-workstream record `GEP-07`, and Apigee migration roadmap (`A0`–`A6`). `GSA` and `GEP` are stable record prefixes, not acronyms with invented long forms.

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

Welcome to the Kong Guided Evaluation (KGE). Today we are testing a working thesis: if the product owner's priorities hold, Kong is the best fit for the application programming interface (API) platform we want to build.

Those stated priorities are Kubernetes, Git-reviewed delivery, distributed gateways, and platform ownership. Kong's operating model aligns with them. That could help teams deliver APIs faster, run traffic closer to workloads, and keep more control over placement and operations.

This is a starting thesis, not a settled conclusion. Slide 2 asks the room to confirm, change, or reject the priorities. If they hold, the fit supports a controlled test—not broad production approval. We still need proof for multicloud operation, recovery, security, full cost, migration, and control-plane operations.

If another option could produce a better outcome, name the business condition and evidence that would change the direction. We will record it and test it fairly. Decide whether to approve the controlled Kong foundation and test plan, change it, or hold it.

##### Talking points

- If the stated priorities hold, Kong fits the target model of Kubernetes, Git-managed change, distributed gateways, and platform ownership.
- Strategic fit supports a controlled implementation; it does not prove production readiness.
- Decide whether to approve, change, or hold the Kong foundation and test plan.

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

This slide explains why Kong is the leading fit before we discuss product features. The target model has three priorities. First, delivery should run on Azure Kubernetes Service, support Spring Boot modernization, and use Git-reviewed application programming interface (API) changes. Second, the API platform should be owned as a product and offer governed self-service. Third, security, observability, multicloud placement, and artificial intelligence traffic need organization-wide control.

Kong aligns well with that model because it is designed for Kubernetes-based operations, automated configuration, and distributed runtimes. Four Early Assessment Gates (EAGs) could still change the direction. We must confirm that the proposed setup works across the required clouds, that we can change custody or exit without unacceptable effort, that the full Total Cost of Ownership (TCO) is viable, and that Kong with Traceable by Harness should be included as an optional security add-on study.

For each gate, decide: confirm, change, reject, or mark unknown. Then name the owner, evidence, due date, and reason to stop. Including a question in the study creates work; it does not create a score or proof.

##### Talking points

- Kong leads because its operating model matches the organization’s delivery, platform, and control priorities.
- Four early questions—multicloud, exit, full cost, and the optional Traceable study—could still change that direction.
- Decide each question now and assign its owner, proof, due date, and stop condition.

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

The original score favors Kong for a clear reason: 35 percent of the weighting rewards Kubernetes and Git-reviewed operations. Those are central to the organization’s target model, so the result supports Kong as the current strategic leader.

But the score does not yet answer six important questions. Forty percent of the proposed comparison is reserved for multicloud operation, scalability and resilience, enterprise Identity and Access Management (IAM) and end-to-end traceability, ease of exit, full Total Cost of Ownership (TCO), and the work required to run the control plane. Every product score in that new block is still unknown.

That uncertainty could confirm Kong’s lead, narrow it, or reverse it. The optional Traceable by Harness study must also remain separate; a third-party add-on cannot be counted as native Kong capability.

The decision is whether these are the right criteria and scoring rules. We need the same product boundaries, must-pass conditions, proof requirements, and independent reviewers for every option. The goal is to learn whether Kong is truly better for our priorities—not to adjust the model until Kong wins.

##### Talking points

- Kong leads the original score because the model strongly values Kubernetes and Git-managed delivery.
- Forty percent of the proposed comparison still covers unanswered strategic and operating risks.
- Approve fair scoring rules that can confirm, narrow, or reverse Kong’s lead.

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

This comparison starts with operating outcomes, not feature counts. Kong is the strongest fit when Kubernetes, Git-reviewed delivery, platform engineering, distributed runtimes, and enterprise control matter most. Those are the priorities we have heard, which is why Kong leads the current direction.

The alternatives become stronger under different conditions. Apigee may lead when external application programming interface (API) products, analytics, and Google-managed services dominate. MuleSoft may lead when Anypoint remains the strategic integration platform. Azure API Management may lead when Azure consolidation matters more than platform independence.

Keeping those alternatives visible is not indecision. It gives us a clear way to test the Kong recommendation. If another option would deliver a better business outcome for an agreed condition, name the specific product version, deployment model, use case, and measure. We will apply the same test and evidence standard to every option.

The decision here is to agree on the conditions that make Kong better for us and the conditions that could change that answer. Excluding an alternative from the first implementation is a scope decision, not a claim that it lacks capability.

##### Talking points

- Kong leads when cloud-native delivery, platform ownership, and distributed runtimes are the priorities.
- Other products become stronger when different business and operating conditions dominate.
- Agree on the measurable conditions that could confirm or change Kong’s lead.

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

The historical score gives Kong a clear lead: 93, compared with 85.5 for Apigee and 77 for MuleSoft. That result is useful because it shows how strongly the original evaluation values cloud-native delivery. It is not yet enough to prove that Kong is the best production choice, because the products were not scored against one approved rulebook and common evidence set.

In the proposed 60/40 scenario, the historical contribution becomes 55.8 for Kong, 51.3 for Apigee, and 46.2 for MuleSoft. The remaining 40 points cover important questions that are still unknown. That creates overlapping ranges, so any option could still finish first when those questions are answered.

The message is not that the products are equal. It is that Kong’s current advantage is promising but not stable enough for a broad commitment. The midpoint on the chart is only a drawing aid, not a forecast or final score.

Decide how the historical score may guide planning, who can replace unknowns with evidence, and who will check that the same scoring rules were applied to every option.

##### Talking points

- The historical score explains why Kong leads the current direction.
- Missing evidence could confirm, narrow, or reverse that lead.
- Approve one fair scoring method before any new total affects the decision.

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

This is the main decision slide. Kong is the leading choice because it best matches the target operating model, but we should move in a way that protects the organization if the evidence changes.

First, agree on the specific self-managed hybrid version and deployment model to test. Second, approve a small foundation with named owners for support, recovery, security, change, and evidence. Third, fund the seven proof workstreams with clear measures, pass conditions, reviewable records, independent reviewers, and reasons to stop. Fourth, limit MuleSoft and Apigee migration to controlled groups with a tested rollback path. Fifth, keep Konnect as the managed Kong comparison and a non-Kong rebuild as the true exit test.

We are not approving critical production scale, a large migration factory, or claims based only on documents and demos.

Choosing Kong now means choosing what to build and test safely. It does not lock in the final production decision. For each row, decide whether to approve it, change it, or hold it, and state what evidence could change that answer.

##### Talking points

- Kong is the leading fit, but the first commitment stays small and controlled.
- Approve the target, foundation, tests, migration limits, and alternatives separately.
- Critical production scale waits for reviewed, production-like evidence.

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

This slide separates three choices about who runs what. The leading option is self-managed hybrid: the enterprise operates Kong’s management layer while data planes handle requests in approved locations. This gives us more control over placement, offline operation, and operating policy, which is a major reason Kong fits the strategy.

The second choice is Konnect. Kong operates the control plane and database while customer-hosted data planes remain. That can reduce our operating work, but it is still a move within Kong. It does not prove that we can leave the platform.

The third choice is a true exit. We rebuild a representative application programming interface (API), its policies, identity, evidence, and runtime on a non-Kong target, then measure behavior changes, effort, and rollback.

The strategic question is whether the value of self-management is greater than its cost and risk. Documentation tells us what each model supports, but only testing can show which works for us. Confirm the leading model and name separate owners, triggers, and evidence for self-management, Konnect, and a non-Kong exit.

##### Talking points

- Self-managed Kong offers control, but the value must outweigh the ongoing work.
- Konnect changes who operates Kong; it does not prove a non-Kong exit.
- Approve separate owners, triggers, tests, and rollback paths for all three choices.

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

Self-managed Kong gives the enterprise more control, but it also gives us the work. We would own the control plane, PostgreSQL, protected administrative access, certificates, licenses, plugins, backups, upgrades, recovery, monitoring, audit records, support coordination, and round-the-clock response.

Kong’s hybrid model has a useful strength: a data plane can keep serving previously accepted configuration during some control-plane interruptions. That can protect customer traffic. It does not prove that a new node can start safely, an urgent security change can be applied, certificates can be renewed, or the platform can be fully recovered. A working proxy is not the same as a healthy service.

The decision is whether the organization is willing and able to fund these ongoing responsibilities. Name the platform, database, Site Reliability Engineering (SRE), security, release, service-management, finance, and support roles that own the work. Confirm capacity, response and recovery targets, and proof of upgrades and restores.

This slide assigns operating responsibility and exposes risk. Contract terms require sourcing evidence, and legal liability requires qualified counsel. Neither can be settled by the architecture diagram.

##### Talking points

- Self-managed Kong offers control and continuity, but it creates ongoing enterprise work.
- A working data plane does not prove safe change, scaling, or full recovery.
- Approve the owners, capacity, recovery targets, and support model—or hold the self-managed choice.

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

This diagram shows the main architectural reason Kong fits the strategy. One enterprise control zone manages approved gateway policy, while distributed data-plane cells handle application programming interface (API) requests close to workloads. That supports central governance without forcing every request through one central runtime. Local evidence collection also keeps operational records close to where traffic runs.

The control plane and PostgreSQL support management; they are not meant to sit in the normal request path. Enterprise certificates, identity, Domain Name System (DNS), traffic steering, and networks remain important dependencies.

This design could improve placement flexibility, fault isolation, and multicloud operation. The diagram does not prove those outcomes. We still need to choose regions, capacity, database replication, failover behavior, sovereignty rules, and what happens when a new node starts during isolation.

Please confirm five things: who owns the control zone, where data planes run, whether requests stay local, how trust is managed, and where evidence is stored. A disagreement changes the components, risks, owners, and tests. If a must-have boundary is still unknown, decide to hold the target design.

##### Talking points

- Kong can centralize policy while running traffic and collecting evidence close to workloads.
- That design supports the strategy, but resilience and multicloud operation still require testing.
- Confirm ownership, placement, locality, trust, and evidence storage before locking the design.

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

Kong can keep application programming interface (API) traffic moving even when parts of the management system are unavailable. That is valuable, but it creates a risk: a healthy gateway does not always mean a healthy customer journey.

Configuration may be old. The identity provider, JSON Web Key Set (JWKS), or certificate authority may be unavailable. A backend may return success even though the business action was missed or duplicated. Traffic may also look healthy while required security or audit records are being lost.

These are risks to test, not claims about the current environment. The business Service-Level Objective (SLO) must therefore include more than gateway uptime.

For each critical service, choose the few signals that show real readiness: approved configuration, valid trust, a ready backend, a completed business transaction, and complete evidence. Give each signal a threshold and an owner. Kong’s ability to separate these paths is useful only if we monitor and govern them separately.

The decision is whether every critical journey needs these independent checks before traffic is admitted. Without them, we could send customers to a service that looks available but is not working correctly.

##### Talking points

- Kong can keep traffic moving, but gateway uptime alone does not prove the business outcome.
- Configuration, identity, backend, transaction, and evidence health can fail separately.
- Approve independent checks and owners for every critical journey.

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

When the control plane is unavailable, Kong does not become simply “up” or “down.” An existing data plane may keep serving its last approved configuration. A restarted node may be safe if it can recover that approved state. A new or empty node is different and should not receive traffic just because its process is running.

This flexibility can protect continuity, which is one of Kong’s strengths. It also means the organization must decide when to continue, pause, isolate, or stop a service. Always serving could keep an unsafe policy active. Always stopping could turn a manageable control-plane interruption into a customer outage.

The right response depends on the business journey, how old configuration may become, whether an urgent security change is waiting, and what recovery proof is available.

For each state, name the owner, time limit, response target, emergency authority, and reason to stop. A restored connection is not enough; the intended and actual state must match, missing evidence must be declared, and an outside-in business check must pass. If those controls are missing, decide to hold the design.

##### Talking points

- Kong’s cached configuration can protect continuity, but the response rules belong to the organization.
- A restored connection is not a completed recovery.
- Approve an owner, time limit, business check, and stop rule for every degraded state.

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

Kong’s self-managed model can give the enterprise strong control over application programming interface (API) delivery, but only if we run it as a funded platform service. It is not simply a shared cluster that application teams consume.

The platform team would own Kong’s lifecycle, control plane, database operations, releases, recovery, upgrades, evidence, and vendor escalation. Domain teams would continue to own API contracts, business rules, data correctness, and customer outcomes. Identity and Access Management (IAM), certificate, and security teams would own trust, rotation, revocation, and exceptions. Site Reliability Engineering (SRE), network, and database teams would operate the failure points with the platform team.

Vendor support helps when problems escalate, but it does not run the service for us. Contract and legal questions remain with sourcing, risk, and qualified counsel.

The decision is whether existing teams have funded capacity, on-call coverage, recovery targets, and proof that upgrades and restores work. We also need one authority when platform, security, and business signals disagree. If any ongoing responsibility has no funded owner, decide to hold the self-managed Kong choice.

##### Talking points

- Self-managed Kong can deliver control only when it is funded as an ongoing platform service.
- Platform, business, security, reliability, and vendor roles must remain clear.
- Approve named teams and capacity before the foundation build begins.

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

This roadmap shows how Kong can move from strategic fit to a safe production decision. It is a sequence of earned choices, not a fixed schedule. Discovery, foundation work, testing, team enablement, and migration can overlap. The zero-to-eighteen-month windows are planning assumptions, not committed dates or proof of progress.

First, agree on the self-managed hybrid design, owners, exact component list, critical journeys, and reasons to stop. Next, build a small foundation that produces reviewable evidence and can be rolled back. Then test the hard failure points in a production-like lab. Only after ownership and controls work should we open standard delivery paths and a migration service. Representative pilots follow, using different workload patterns.

The final stage is a decision: scale Kong, narrow its use, move management to Konnect, keep exceptions elsewhere, or exit. Expansion is not automatic.

We can move faster by doing independent work in parallel, but not by skipping proof that later stages depend on. Approve the entry and exit evidence, funded owner, and stop authority for each stage. Detailed dates should follow real inventory and capacity.

##### Talking points

- Kong adoption moves through evidence-based stages, not a fixed rollout calendar.
- Work can run in parallel, but later decisions still depend on earlier proof.
- Approve the go/no-go evidence, owner, and stop authority for every stage.

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

A MuleSoft application is a package, but that does not mean every part belongs in Kong. We first separate what the package does, where it stores important state, and who owns the business result.

Gateway policy—authentication, request limits, routing, and shared headers—is a natural Kong responsibility. A thin application programming interface (API) facade may stay at the edge or move into an owned service. Transformation, orchestration, messaging, scheduled jobs, file handling, connectors, replay, and durable state need destinations designed for those jobs.

For example, one MuleSoft package might authenticate a client, change a payload, schedule a file pickup, and record whether work has already been completed. Calling that one API migration hides four different ownership and recovery decisions. A Kong plugin may reproduce some behavior, but technical possibility does not prove that long-lived business logic belongs in the gateway.

For each component, decide what it does, where the source of truth lives, who owns side effects, how it recovers, and which destination preserves that responsibility. If any answer is unknown, keep that workload out of the migration group.

##### Talking points

- Move only true gateway responsibilities into Kong; do not copy whole MuleSoft packages.
- Technical extensibility does not prove that business or stateful logic belongs at the edge.
- Approve a migration group only when responsibility, state, destination, and owner are clear.

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

This approach keeps the external application programming interface (API) edge stable while a small group of services moves from MuleSoft to a new runtime. Kong may become that stable edge, but the safety pattern does not depend on choosing it in advance. The outcome is less consumer disruption and a controlled way to compare old and new behavior.

Matching response codes is not enough. We must compare contracts, errors, identity, side effects, ordering, duplicate protection, latency, Service-Level Objectives (SLOs), evidence, and the final business result. A rollback trigger and decision owner remain active until those results match. Sending traffic back is not enough if credentials, counters, state, or an irreversible backend action have already changed.

Running both paths costs money, and that belongs in the migration cost model. The alternative is an irreversible cutover before business differences are understood. Decide whether small migration groups, representative test cases, business verification, state checks, evidence retention, and timed rollback are required controls. Hold a group until its verifier, owner, stop condition, and rollback proof are clear.

##### Talking points

- A stable edge lets Kong and existing runtimes coexist with less consumer disruption.
- Matching means the business result, identity, side effects, performance, and evidence agree.
- Approve controlled groups and keep rollback active until old and new states match.

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

Apigee migration involves much more than exporting proxy files. Products, applications, credentials, shared policies, key-value data, quotas, caches, targets, portals, analytics, and runtime dependencies can all affect the business outcome. Kong may be the destination, but a safe move must account for that full picture.

The A0–A6 roadmap makes the work understandable. A0 inventories what exists. A1 decides what can map directly, needs configuration, must be rewritten, stays temporarily, or can retire. A2 builds a controlled Kong target with automation, identity, recovery, support, cost, and rollback. A3 proves one difficult representative service. A4 moves small groups while identity, state, outcomes, and evidence are compared. A5 runs a representative pilot. A6 retires Apigee only when no technical, operating, recovery, data, support, or commercial dependency remains.

MuleSoft uses a different roadmap because its source model is different, but both migrations need a stable edge, accurate inventory, business verification, state comparison, timed rollback, and independent approval to exit. Decide which roadmap applies and who owns each gate. Export counts and elapsed time do not prove safe retirement.

##### Talking points

- Moving from Apigee to Kong includes identities, state, policies, portals, analytics, and runtime dependencies.
- Apigee and MuleSoft need different roadmaps but the same business and rollback controls.
- Approve retirement only when reviewed evidence shows no remaining dependency.

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

This slide gives us an honest starting point before we invest more in Kong. The current Proof of Concept (PoC) has 16 high-level scenario records. Five automated local checks ran, and 11 did not. A separate comparison plan defines 28 detailed future tests. Both are useful, but neither proves that the proposed self-managed hybrid setup is ready.

The numbers answer different questions. Sixteen describes the status of broad scenarios. Twenty-eight describes tests that could be run later. We must not add them together or turn them into a readiness percentage. For the proposed Kong setup, we currently have no repeatable production-like lab result and no representative pilot result.

That does not mean the PoC failed. It confirmed a basic functional starting point and showed what work remains. The decision is to use the result for planning without claiming more than it shows.

Confirm three lists separately: what passed, what was prepared but not run, and what has not yet been designed for the agreed production setup. Approve further investment only against named tests, environments, reviewable records, repeatability, reviewers, and the production decision each result supports.

##### Talking points

- The current Kong PoC proves a basic starting point, not production readiness.
- The 16 scenarios and 28 future tests are different lists and must stay separate.
- Approve the next investment against named tests, environments, results, and reviewers.

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

The next Kong Proof of Concept (PoC) must look enough like production that its results can change the decision. It is not simply a larger feature demo.

The seven workstreams answer four business questions. First, can the self-managed hybrid design and its Terraform and decK automation be built, promoted, recovered, and kept free of unwanted change? Second, can it survive regional failure, recover in isolation, and scale under realistic load? Third, can it manage the full Identity and Access Management (IAM) lifecycle for employees, workloads, consumers, application programming interfaces (APIs), and service accounts? Fourth, do the separate artificial intelligence and Traceable by Harness studies deliver useful outcomes without unacceptable security, privacy, performance, support, or cost trade-offs?

The Traceable study remains an optional third-party security add-on comparison with the MuleSoft baseline. It cannot add native Kong points. Documentation tells us what can be tested; it does not prove the result.

For each workstream, decide the exact components, environment, owner, method, measure, pass condition, reviewable record, independent reviewer, and reason to stop. Without those items, approve it only as a demo—not as evidence for production.

##### Talking points

- The next Kong PoC must answer production decisions, not demonstrate more features.
- Group the work around automation, resilience, identity, and separate emerging-capability studies.
- Approve every workstream with a measure, pass condition, reviewable result, reviewer, and stop rule.

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

This slide asks whether Kong produces the outcomes we need, not simply whether a feature exists. Five results must be checked separately.

First, the active configuration and security material must be known, approved, and current enough for the business journey. Second, the customer or operational transaction must finish correctly; a successful proxy response is not enough. Third, authentication, authorization, certificates, secrets, and revocation must remain correct during normal and degraded operation. Fourth, the control plane, PostgreSQL, credentials, and evidence must recover within approved targets. Fifth, normal, emergency, and rollback changes must leave the intended state without hidden leftovers.

Before testing, decide the measure, pass condition, observation period, reviewable record, independent reviewer, and response to failure for each outcome. Otherwise success can be redefined after the result is known.

Do not reduce these checks to one green light. Kong could serve traffic while policy is old, recovery is broken, evidence is missing, or the business result is wrong. Approve each outcome separately and state which failure would block production use.

##### Talking points

- Judge Kong by business and operating outcomes, not by the presence of features.
- Business correctness, trust, recovery, and safe change must pass separately.
- Approve each measure, pass condition, reviewer, and response to failure before testing.

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

Kong is ready to scale only when the whole operating model works, not simply when gateway throughput increases. We can group the remaining outcomes into three questions.

Can we run it safely? Capacity tests must show headroom, fault isolation, new-node scaling, and recovery. Traceability must connect administrative changes, requests, security decisions, and business records while showing what was produced, delayed, lost, or delivered and protecting prohibited data.

Can teams adopt it sustainably? Delivery teams should use the standard path without constant expert help. Staffing, on-call work, upgrades, support, infrastructure, and full Total Cost of Ownership (TCO) must remain practical.

Can we change direction safely? We need current inventory and ownership, a tested move to a managed Kong model, and a representative rebuild outside Kong with acceptable behavior change and effort.

Traceable by Harness may help with part of the security and traceability outcome, but an installed add-on does not make that outcome pass. A load-test headline also does not prove sustainable scale. Decide who uses each result, what action it triggers, and which failure blocks expansion.

##### Talking points

- Kong can scale only when it is safe to run, sustainable to adopt, and practical to change or exit.
- Traceability is an end-to-end outcome; Traceable by Harness is only one possible mechanism.
- Decide who owns each result, what action it triggers, and which failure blocks expansion.

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

This slide keeps the Kong recommendation honest. Before testing begins, the decision owner must agree on every result the evidence can produce.

Scale means Kong meets the must-pass outcomes for representative services and the organization funds the operating model. Narrow means Kong remains valuable for selected patterns while exceptions stay elsewhere. Switch management means Kong stays, but the control plane moves to a managed model such as Konnect. Exit means the direction changes to a representative non-Kong platform with a tested rollback path. Hold means the evidence is incomplete, conflicting, or blocked by an unowned risk.

Unfavorable evidence must be allowed to change the recommendation. Stronger external application programming interface (API) product needs may favor Apigee. Continued reliance on Anypoint may favor MuleSoft. Azure consolidation may favor Azure API Management. Failure on recovery, security, cost, adoption, offline operation, or exit may narrow or reverse Kong.

A move to Konnect and an exit from Kong solve different risks. Decide who can choose each outcome, what result triggers it, what work stops, and which reviewable record confirms the change. Without that authority, testing becomes a demonstration rather than a decision process.

##### Talking points

- Decide in advance whether evidence can scale, narrow, move management, exit, or hold Kong.
- Unfavorable evidence must be able to change scope, funding, or platform direction.
- A move to Konnect and a non-Kong exit remain separate choices.

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

This appendix answers a strategic question: does Kong’s distributed design produce better multicloud operation and resilience for our workloads? Kong can place data planes close to workloads while centralizing policy. That is a strong fit for the target model, but deployment flexibility alone does not prove independent operation across clouds.

We must test runtime placement, management dependencies, data location, network and identity dependencies, support, and operating cost. Resilience testing should use the same workload mix, load increase, capacity headroom, shared-resource pressure, new-node scaling, regional or dependency failure, recovery, and business Service-Level Objective (SLO) for every option.

Fairness matters. Kong, Apigee, MuleSoft, and any approved benchmark must face the same scenario, measures, minimum proof, and independent review. A production-like Kong test cannot be compared with a brochure description for another product.

When someone challenges a label, decide which specific version, deployment model, workload, failure, measure, pass condition, reviewable record, owner, and reviewer would settle it. Send that question back to the formal comparison. Do not change a score in the room based on opinion.

##### Talking points

- Kong’s distributed design is promising for multicloud use, but placement alone does not prove resilience.
- Compare every option with the same workloads, failures, measures, and independent review.
- Approve the test question in the room; do not change product scores from opinion.

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

This appendix keeps two separate studies outside the core gateway decision: Kong's artificial intelligence capabilities and the third-party Kong-plus-Traceable by Harness security-adjunct hypothesis. Product words such as easy, complete, secure, observable, and scalable are questions to test, not results.

Traceable documentation shows a Kong plugin and agent path. That is enough to design a study, but it does not prove that the exact Kong Gateway Enterprise 3.14 setup will be supported, effective, private, fast, scalable, affordable, or easy to upgrade and remove.

The Traceable study should answer four questions. Does it cover the required protocols, bodies, streams, and security decisions? What happens in synchronous, asynchronous, and failure modes? What are the latency, resource, scaling, privacy, and data-handling effects? Can we upgrade, roll back, remove it, and return safely to the baseline?

The artificial intelligence study should separately test Model Context Protocol (MCP), agent-to-agent communication, model routing, semantic caching, content safety, and catalogs. Decide which outcomes matter and how they will be measured. Neither study may add native Kong points until executed evidence supports the specific outcome.

##### Talking points

- Kong's artificial intelligence capabilities and the third-party Kong-plus-Traceable security-adjunct hypothesis require separate studies.
- Test coverage, failure behavior, performance, privacy, support, and safe removal.
- Approve outcome measures without adding unproved points to Kong’s core score.

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

Kong may be cost-effective, but a lower license price would not prove it. We need one Total Cost of Ownership (TCO) comparison covering six areas: commercial terms, infrastructure, people and on-call work, migration and dual running, security and monitoring tools, and the cost of incidents or exit. Use the same time period and workload basis for low, expected, and high cases. Keep confidential quotes in the approved commercial system and publish only safe assumptions and conclusions.

Vendor dependency needs a practical test. Moving the control plane to Konnect would show whether management responsibility can move within Kong. It would not prove that we can leave Kong. A true exit test rebuilds a representative application programming interface (API), policies, identity, product state, evidence, and runtime on an approved alternative. It records behavior changes, rewrite effort, lost history, remaining procedures, support or contract dependencies, and rollback.

The business decision is whether Kong’s control and flexibility are worth the full operating and exit cost. Operating responsibility is not the same as legal liability; legal conclusions require qualified counsel. Approve a cost or exit rating only when the comparison is normalized and independently reviewed.

##### Talking points

- Judge Kong on full operating cost, not license price alone.
- Test both a move to Konnect and a representative non-Kong rebuild.
- Approve cost and exit ratings only with comparable evidence and independent review.

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

This final appendix keeps the original scores visible while showing how much remains unknown. Kong still leads at 93, compared with 85.5 for Apigee and 77 for MuleSoft. In the proposed 60/40 planning model, the known contributions become 55.8, 51.3, and 46.2.

The remaining 40 percent covers multicloud operation, scalability and resilience, enterprise Identity and Access Management (IAM) and traceability, ease of exit, full Total Cost of Ownership (TCO), and control-plane responsibility. Every product rating in that block is still unknown from zero to ten.

The possible ranges overlap, so every option could still finish first. That does not mean the products are equal. It means Kong’s current lead is strategic and promising, but the missing evidence could confirm, narrow, or reverse it. The midpoint of five is only a drawing aid, not a score or forecast.

Do not make the final decision on this appendix slide. Decide whether to approve or change the scoring method, product boundaries, must-pass conditions, common evidence, reviewers, and rules for uncertainty. Then return to slide 6 for the Kong authorization or slide 21 for the evidence outcome.

##### Talking points

- Kong leads the historical score, but important questions remain unscored.
- Overlapping ranges mean the lead could be confirmed, narrowed, or reversed.
- Approve the comparison method here, then make the decision on slide 6 or 21.

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
