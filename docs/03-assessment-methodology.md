# Assessment methodology

## Sequence

1. **Frame:** confirm outcomes, scope, constraints, mandatory gates, and evidence owners.
2. **Discover:** inventory the present estate and representative workloads.
3. **Research:** record official claims with version, access date, and interpretation.
4. **Test:** execute equivalent scenarios; keep screenshots/logs/configuration sanitized and reproducible.
5. **Score:** fail gates first; score only evidenced criteria; calculate coverage and sensitivity.
6. **Decide:** document recommendation, dissent, exceptions, conditions, and exit options in an ADR.
7. **Pilot:** migrate low-risk but representative workloads before scaling a factory.

## Evidence levels

| Level | Evidence | Permitted score confidence |
|---|---|---|
| E0 | Marketing or assertion only | Unknown |
| E1 | Current official documentation | Low–medium |
| E2 | Vendor answer with named version/contract term | Medium |
| E3 | Repeatable lab execution with artifacts | High for tested scope |
| E4 | Representative enterprise pilot under expected controls/load | Highest |

## Scoring guardrails

- Mandatory criteria are pass/fail/unknown and are not averaged away.
- Weighted criteria use 0–5 only after evidence is attached.
- `Unknown` is not zero; it is excluded from normalized scoring and reported as an evidence gap.
- A candidate cannot be recommended when a mandatory criterion is failed or when evidence coverage is below the steering committee threshold.
- Run sensitivity at ±20% for category weights and record rank instability.
- Product variants are scored separately; family-level scores hide deployment differences.

See `decision-matrix/scoring-guide.md` for the exact algorithm.
