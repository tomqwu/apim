# ADR-0001: Evidence-led gated assessment

- Status: proposed
- Date: 2026-08-17

## Decision

Define requirements and mandatory gates before vendor scoring; score exact deployment variants; use `unknown` for missing evidence; and preserve the following approval sequence:

1. Gate 0 approves the decision contract.
2. Gate 1 down-selects finalists only after an equivalent E1/E2 screen of all seven variants.
3. Gate 2 may make a conditional selection only after symmetric E3 proof, TCO/support analysis, sensitivity, and evidence review.
4. Gate 3 admits representative E4 production pilots only after the selected platform foundation is production-pilot ready.
5. Gate 4 authorizes migration at scale only after representative pilot evidence meets approved thresholds.
6. Gate 5 authorizes decommission only after dependency-zero evidence is accepted.

The conditional selection ADR must record dissent, exceptions, conditions, exit path, and review date. A Gate 2 selection is not production-scale approval.

## Consequences

The process takes longer than feature-checklist selection but makes bias, uncertainty, variant limitations, and the distinction between selection and production-scale approval visible.
