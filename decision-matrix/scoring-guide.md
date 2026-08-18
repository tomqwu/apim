# Scoring guide

## Gate evaluation

- **Resolution prerequisite:** no gate or weighted score is assigned until the bounded archetype has a frozen Gate-1 option record covering edition, version, topology, region, entitlement, support and operating boundary.
- **Pass:** acceptance test met for the exact resolved option with required evidence.
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

Weighted scoring is secondary to mandatory gates and does not impute an unknown. Four views travel together:

1. **Observed-evidence score—descriptive only:** for each option/category, compute `sum(score × criterion weight) / sum(5 × criterion weight)` across that option's evidenced rows. Different denominators make this view unfit for cross-option ranking.
2. **Common-evidence score:** compute the same normalized score only over criterion cells that meet the required evidence level for every compared option. Disclose the retained weight and category mix; if a material category falls below its approved floor, the comparison is inconclusive.
3. **Full-weight lower/upper bounds:** use the complete approved denominator, assign unknown non-mandatory cells `0` for the lower bound and `5` for the upper bound, and keep every mandatory unknown as a hold rather than a number.
4. **Maximum regret:** across approved weight, input and missing-evidence completion scenarios, report the largest plausible loss of each option versus the best competitor. A rank reversal inside the approved envelope blocks selection.

Report overall and per-category coverage separately:

`coverage = evidenced applicable weight / total applicable weight`

`category coverage = evidenced applicable weight in category / total applicable weight in category`

Do not rank an option below the steering committee's overall **or category** thresholds. Explicitly test missing-not-at-random patterns, such as one option lacking evidence disproportionately in security, recovery or commercial criteria. Run category-weight sensitivity at −20% and +20%, renormalize to 100%, stress organization inputs and missing-evidence completions, and disclose every decision/rank switch.

## Required scorecard fields

`option_id, criterion_id, score, gate_status, evidence_level, evidence_reference, test_scenario_id, test_status, tested_version, tested_topology, entitlement, measure, acceptance_threshold, limitation, reviewer_role, review_date, fresh_until, exception_reference, decision_status`
