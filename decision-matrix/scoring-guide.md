# Scoring guide

## Gate evaluation

- **Pass:** acceptance test met for the exact variant with required evidence.
- **Fail:** acceptance test not met or a material limitation violates the requirement.
- **Unknown:** insufficient evidence. Unknown is never treated as pass.
- **N/A:** allowed only with recorded rationale and architecture approval.

A failed mandatory gate disqualifies the variant unless an explicit, time-bounded exception is approved. An unknown mandatory gate blocks recommendation.

## Weighted score

| Score | Meaning |
|---:|---|
| 0 | Cannot satisfy; no credible mitigation |
| 1 | Major gap; high-risk workaround |
| 2 | Partially satisfies; material customization or operations burden |
| 3 | Meets requirement with normal configuration and acceptable limits |
| 4 | Strong fit with demonstrated operational advantage |
| 5 | Exceptional, differentiated fit demonstrated in representative conditions |

For each category, compute `sum(score × criterion weight) / sum(5 × criterion weight)` across evidenced rows. Multiply by the category percentage in `weights.yaml`. Report unknown coverage separately:

`coverage = evidenced applicable weight / total applicable weight`

Do not rank a variant below the steering committee's coverage threshold. Run category-weight sensitivity at −20% and +20%, renormalize to 100%, and disclose rank changes.

## Required scorecard fields

`criterion_id, score, gate_status, evidence_level, evidence_reference, tested_version, tested_topology, limitation, reviewer, review_date`
