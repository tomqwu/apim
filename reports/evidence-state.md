# Evidence-state snapshot

- Snapshot date: 2026-08-17
- Scope: canonical tracked repository data
- Decision use: show what can and cannot be concluded; this is not a platform score or ranking

The charts below are portable Markdown Mermaid views. Repository validation checks their values against the same CSV and Markdown sources used by the site Visual Atlas.

## Decision criteria structure

There are 120 criteria across 12 categories: 30 mandatory gates and 90 weighted criteria. All 120 evidence states remain `unknown`; the category weights are workshop defaults and are not approved.

<!-- chart-source: criteria-requirement-type -->
```mermaid
pie showData
  title Criteria by requirement type
  "Mandatory" : 30
  "Weighted" : 90
```

Source: [criteria.csv](../decision-matrix/criteria.csv) and [weights.yaml](../decision-matrix/weights.yaml).

## PoC execution state

Five of 14 scenarios have automated baseline evidence. Nine scenarios are not run, including the live-cluster Gateway API acceptance/programming scenario. Configuration or a runnable script is not counted as execution.

<!-- chart-source: poc-execution -->
```mermaid
pie showData
  title PoC scenario execution state
  "Automated" : 5
  "Not run" : 9
```

Source: [PoC test plan](../poc/test-plan.md) and [validation report](validation-report.md).

## Official-source use

The source register contains 27 official sources. Fifteen source IDs are explicitly cited in the claim register; twelve are registered but not yet decision-bearing there. Source volume is not criterion coverage.

<!-- chart-source: source-use -->
```mermaid
pie showData
  title Registered official sources
  "Used in findings" : 15
  "Not yet used" : 12
```

Source: [sources.csv](../research/sources.csv) and [findings.md](../research/findings.md).

## Decision-readiness register

| Indicator | Current state | Implication |
|---|---:|---|
| Exact deployment variants | 7 | Every variant requires its own criterion-level evidence |
| Populated exact-variant scorecards | 0 | No comparative ranking is supportable |
| Mandatory gates | 30 unknown | Product selection remains blocked |
| Assumptions | 10 open | Organization context is not yet confirmed |
| ADRs | 5 proposed | Evaluation and architecture decisions are not accepted |
| Risks | 12 identified, not rated | A heatmap or aggregate exposure claim would be premature |
| Open questions | 10 decision-critical | Owners, deadlines, evidence, and decision impact must be assigned |

The [principal review](methodology-review.md) converts this state into a steering recommendation. The [repository roadmap](../docs/39-repository-roadmap.md) defines the evidence-system gates, and the [delivery roadmap](../docs/36-implementation-roadmap.md) defines the organization delivery gates.
