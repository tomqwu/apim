# Capability mapping

Use classification codes G/F/T/O/M/B/C/R from `docs/35-mule-migration-strategy.md`. A workload may have multiple responsibility rows; do not force its whole implementation into one target merely because it is one Mule application today.

Every mapping records current behavior, target capability, rationale, owner, operational model, security/data controls, golden tests, dependencies, cutover, rollback, and decommission evidence.
