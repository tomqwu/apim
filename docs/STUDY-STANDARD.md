# Principal study standard

This standard governs every document presented as a substantive study, comparison, deep dive, architecture assessment, or recommendation input in this repository. It exists to prevent a polished page, long checklist, or collection of product claims from being mistaken for decision-grade analysis.

The standard is intentionally stricter than a writing guide. It defines the minimum argument, evidence, scenario, visual, and review structure that makes an article useful in a real platform decision.

## Core rule

A principal study must let a skeptical reviewer trace this chain without reconstructing it:

> decision question → bounded context/archetype → option-resolution state or mechanism → evidence → scenario behavior → failure consequence → operational response → measurable test → decision implication

If any link is absent, the article is incomplete. Length is not a substitute for the chain, and a diagram is not evidence merely because it renders.

## Docs-first publication and projection contract

The canonical study, guide, roadmap, comparison, or recommendation is authored and reviewed in `docs/` first. Before publication, the contributor updates `docs/README.md` and any roadmap or cross-reference that establishes how the new document participates in the study system.

The static site is a derived presentation layer. It may parse canonical tables, surface article-owned figures, generate navigational charts, tailor audience routes, and create presentation scenes, but it must not introduce a second problem taxonomy, recommendation, roadmap status, option count, evidence claim, or decision conclusion. Every site projection links back to its canonical document and is rebuilt after the document changes.

A site-only study or guide is incomplete. A diagram or chart that carries an argument belongs in the article at the point of use under the inline figure contract; the Visual Atlas, overview, comparison, audience page, and presentation remain indexes and projections of that argument.

## Language and terminology contract

Expand every unfamiliar acronym at its first visible use as **Full Name (ACRONYM)**. Apply the rule independently in every document, directly linked section, slide, table, figure, form, and speaker-note card because a reader may enter at any of those points without seeing earlier context. A glossary link or hover tooltip may supplement the expansion but cannot replace visible first-use language.

Do not reverse-engineer a long form for an internal record ID. When an identifier has no documented expansion, preserve the stable code and pair it with its canonical plain-language descriptor. Established product names, commands, and protocol spellings remain unchanged unless the canonical terminology contract explicitly defines a display form.

## Required study header

Every principal study begins with a compact metadata block containing:

| Field | Required content |
|---|---|
| Artifact type | `principal-study`, `candidate-dossier`, `architecture-study`, or `comparative-study` |
| Decision question | One question whose answer changes funding, architecture, shortlist, sequencing, or control design |
| Decision owner | Accountable role or forum, never an invented named person |
| Primary audiences | Roles expected to act on the conclusion |
| Scope | Bounded products/deployment archetypes, current option-resolution state, versions or version policy, workloads, and environments considered |
| Evidence state | `hypothesis`, `documented`, `observed`, `inconclusive`, or `approved`; mixed states are identified per claim |
| Reference case | The scenario used for analysis, including whether it is synthetic |
| As-of date | Date on which volatile product, support, and entitlement claims were checked |
| Next gate | The review, test, evidence, or approval that can change the current conclusion |

## Required argument

### 1. Answer first

Open with the provisional answer and its confidence, not a history lesson. State what can be concluded now, what cannot, and the consequence of being wrong.

An acceptable answer distinguishes documented capability from demonstrated fit. For example, an official document may confirm that a data plane can retain configuration during a control-plane interruption; only a controlled test can establish whether a new replica can start, how long stale configuration remains acceptable, or whether the recovery behavior meets the reference case.

### 2. Bound the object being evaluated

Compare deployable solution options, not brand names. A bounded archetype becomes an exact scoreable option only when its required definition is complete. That definition includes at least:

- product and edition;
- control-plane ownership and location;
- data-plane/runtime ownership and location;
- configuration authority and promotion path;
- portal, analytics, identity, and telemetry dependencies;
- cluster, region, and failure-domain topology;
- licensed or separately entitled capabilities;
- support boundary and customer operating responsibility; and
- migration role: target, coexistence component, incumbent baseline, or excluded pattern.

Where those details are unknown, the study records a bounded archetype and a Gate-1 blocker rather than calling it exact, scoring it, or collapsing it into a generic product label.

### 3. Use a scenario with operational texture

A scenario is sufficiently deep only when it includes the conditions that cause architecture choices to behave differently. The shared [enterprise reference case](41-enterprise-reference-case.md) supplies a safe baseline. A study may narrow it, but must retain the relevant complexity:

- critical and non-critical traffic classes with p50/p95/p99 behavior, bursts, payloads, protocols, and growth;
- consumer and workload identity, certificate, secret, and key-rotation dependencies;
- public, partner, private, east-west, SaaS, and legacy network paths;
- non-idempotent, ordered, asynchronous, streaming, file, and long-running workloads where applicable;
- region, zone, cluster, node, dependency, control-plane, and telemetry failure modes;
- coexistence across legacy integration runtimes, application platforms, Kubernetes, and SaaS;
- operator roles, after-hours coverage, change windows, and escalation paths;
- recovery, rollback, reconciliation, and decommission evidence; and
- explicit commercial, capacity, and support assumptions.

All invented numbers are labelled **scenario assumptions**. They may drive a model or test design, but they are never described as current-state facts or observed results.

### 4. Explain mechanisms and consequences

Do not write “supports hybrid,” “provides high availability,” or “integrates with Kubernetes” as conclusions. Explain the mechanism:

1. Which component initiates each connection?
2. Where are desired state and runtime state stored?
3. What continues during disconnection, and for how long?
4. Can existing and new replicas operate from cached state?
5. Which identity, DNS, PKI, registry, queue, database, and telemetry dependencies remain?
6. Who patches, backs up, restores, rotates, scales, and diagnoses each component?
7. What breaks first under overload or partial failure?
8. What evidence proves recovery and consistency?

The study then follows the consequence through customer impact, platform toil, security exposure, support ownership, cost, and decision criteria.

### 5. Treat counter-evidence as first-class

Every material hypothesis includes:

- the strongest reason it may be wrong;
- a credible non-fit condition;
- evidence that would falsify it;
- the test or source that could provide that evidence; and
- the decision impact of a negative result.

Alternatives receive the same questions, evidence ladder, scenario, and level of architectural detail. A dossier may conclude that an answer remains unknown; it may not fill a gap with an optimistic inference.

## Evidence contract

Each material statement is identifiable as one of the following:

| Label | Meaning | Permitted decision use |
|---|---|---|
| **Documented fact** | Supported by a current primary or official source for the stated version, edition, topology, and entitlement | Candidate screening and test design |
| **Observed result** | Produced by a reproducible execution with topology, configuration, raw output, timestamp, and reviewer | Criterion evidence within the tested boundary |
| **Interpretation** | Reasoned implication drawn from facts or results | Decision analysis when the reasoning is explicit |
| **Scenario assumption** | Invented but plausible input used to model behavior | Sensitivity analysis and PoC design only |
| **Hypothesis** | Claim awaiting evidence | Prioritizing research or experiments |
| **Open question** | Missing fact that could change the conclusion | Deferral, blocker, or evidence request |

Point-of-use links are required for material product and standards claims. A bibliography alone is insufficient because a reviewer must be able to identify which source supports which sentence. Volatile facts include version support, tier capability, entitlement, region availability, limits, topology restrictions, support policy, and pricing; each carries an as-of date and revalidation trigger.

Observed results require an evidence bundle. Screenshots and summaries may aid review but do not replace raw results, configuration, environment versions, hashes, and limitations.

## Inline figure contract

A figure belongs inside the article at the point where the text uses it. Each canonical figure includes:

- a stable figure identifier;
- an answer-first title;
- the depicted scope and excluded scope;
- source data or diagram source;
- evidence state and as-of date;
- accessible text or an equivalent data table;
- a short interpretation stating what the figure changes; and
- limitations that stop readers from overgeneralizing it.

Useful figures expose reasoning that prose hides: state ownership, trust boundaries, request versus control paths, failure propagation, recovery sequence, option-by-criterion differences, sensitivity, cost drivers, or migration dependencies. Decorative diagrams and unexplained score charts do not satisfy this contract.

## Minimum real-world challenge set

Each study addresses the applicable cases below rather than relying on a happy-path topology:

| Challenge | Required question |
|---|---|
| Control-plane interruption | Which operations continue, which stop, and what happens to configuration freshness and new replicas? |
| Identity degradation | What fails when the issuer, JWKS endpoint, certificate authority, secret store, or clock is unavailable? |
| Partial network partition | Can operators distinguish gateway, DNS, firewall, service, and telemetry failure without unrestricted access? |
| Configuration defect | How is a bad policy detected, contained, rolled back, and reconciled across runtimes? |
| Capacity shock | Which queue, connection pool, counter store, CPU path, or upstream limit saturates first? |
| Stateful business action | How are idempotency, ordering, replay, timeout ambiguity, and compensation handled outside the gateway? |
| Regional loss | Which state is recoverable, what is manually reconstructed, and how is consumer convergence proven? |
| Certificate rollover | Can old and new trust overlap without breaking long-lived clients or disconnected runtimes? |
| Telemetry backpressure | Does request handling remain safe when logs, metrics, or traces cannot be exported? |
| Mixed-platform migration | Can traffic move gradually while credentials, contracts, analytics, and rollback remain coherent? |

“Supported” is not an answer. The article explains expected behavior and identifies the proof required.

## Required closing sections

Every principal study ends with:

1. **Decision implications** — what the analysis changes now.
2. **Falsification and proof plan** — exact evidence that could change the answer, including procedure, metric, threshold, and artifact.
3. **Risks and limitations** — boundaries, stale facts, untested behavior, scenario sensitivity, and excluded concerns.
4. **Open evidence requests** — owner role, due gate, and decision impact for each material unknown.
5. **Next gate** — the forum and acceptance condition; “do more research” is not a gate.

## Review rubric

An independent reviewer records `pass`, `conditional`, or `fail` for each row.

| Dimension | Pass condition |
|---|---|
| Decision clarity | One consequential question, owner, audience, and next gate are explicit |
| Option precision | The bounded archetype and unresolved fields are explicit; any scoring or recommendation uses a complete exact option definition |
| Scenario depth | Relevant workloads, constraints, failure modes, operations, and assumptions are present |
| Evidence integrity | Material claims have point-of-use provenance and evidence labels |
| Comparative symmetry | Alternatives receive equivalent questions, detail, and proof requirements |
| Mechanism analysis | State, dependencies, ownership, failure behavior, and consequences are explained |
| Visual reasoning | Inline figures expose and interpret a decision-relevant relationship |
| Testability | Falsification procedures specify measures, thresholds, artifacts, and reviewers |
| Operational realism | Day-two operations, incidents, recovery, and support boundaries are addressed |
| Decision usefulness | The conclusion changes a gate, criterion, architecture, sequence, or evidence request |
| Limitations | Unknowns and non-fit conditions are prominent enough to prevent overclaiming |
| Traceability | The reader can follow the full decision-assurance chain |

A study is not principal-grade when any of decision clarity, option precision, evidence integrity, comparative symmetry, testability, or limitations fails. Conditional publication must display the condition and cannot be used as final recommendation evidence.

## Anti-patterns

The following do not qualify as deep analysis:

- a feature checklist with no mechanism, scenario, or consequence;
- a generic “pros and cons” table comparing brands rather than bounded archetypes and, at the scoring gate, exact resolved options;
- a topology diagram that omits state, trust, failure, or ownership boundaries;
- a vendor claim repeated without edition, topology, entitlement, and source context;
- a score whose input evidence remains unknown;
- synthetic numbers presented as a benchmark or estate inventory;
- a PoC plan described as a result;
- a migration wave based only on application count;
- an availability claim that ignores dependencies and recovery consistency;
- an executive summary that leads with repository volume rather than decision state; or
- a long article that never states what decision changes.

## Relationship to the remediation workflow

This standard implements the quality bar described by PCR-003 and supplies the article contract used by PCR-027 through PCR-045 and PCR-047 through PCR-050. Publication under this standard is implementation evidence, not closure by itself. The [remediation backlog](../reports/content-remediation-backlog.csv) remains authoritative for dependency resolution, reviewer acceptance, and disposition.
