# Decision matrix

`criteria.csv` is the canonical set of **120** evaluation criteria: 12 categories with 10 criteria each. Thirty are mandatory gates. Criteria and weights must be agreed before scored vendor workshops.

## Bounded archetypes resolved before scoring

1. Kong Konnect hybrid
2. Self-managed Kong hybrid
3. Azure APIM managed gateway
4. Azure APIM self-hosted gateway
5. Apigee X
6. Apigee Hybrid
7. MuleSoft current-state baseline

These seven rows are research archetypes. They are **not exact or scoreable** until Gate 1 freezes edition, version, topology, region, entitlement, plugin/capability package, support tier and managed/customer responsibility boundary. Copy a scorecard template only after creating a resolved option ID, then add one row per criterion. Do not use a product-family or unresolved-archetype score to paper over topology or entitlement differences.

## Canonical evidence ledger

Use [`evidence-ledger-template.csv`](evidence-ledger-template.csv) as the canonical criterion-by-option record. A complete comparison contains one row for each applicable `criterion_id + option_id` pair; family/archetype scorecards are projections, not the source of truth.

The ledger preserves the chain from business outcome and requirement through claim, evidence, test, implication, reviewer decision, exception, and freshness. For a mandatory gate, populate an observable `measure`, an approved `acceptance_threshold`, a `test_scenario_id`, the required evidence level, the accountable reviewing role, and any authorized exception reference before assigning pass or fail.

Allowed public evidence contains sanitized references, versions/topologies, evidence level, limitations, checksums/reference IDs, and reviewer roles. Quotes, NDA responses, organization topology, security findings, raw logs, private URLs, and named-person mappings remain in a restricted evidence store and are represented only by a non-sensitive `restricted_reference`.

Bounded archetype IDs, to be replaced or versioned by exact Gate-1 option IDs:

| Archetype ID | Bounded deployment archetype |
|---|---|
| `kong-konnect-hybrid` | Kong Konnect hybrid |
| `kong-self-managed-hybrid` | Self-managed Kong hybrid |
| `apim-managed` | Azure APIM managed gateway |
| `apim-self-hosted` | Azure APIM self-hosted gateway |
| `apigee-x` | Apigee X |
| `apigee-hybrid` | Apigee Hybrid |
| `mulesoft-current` | MuleSoft current-state baseline |
