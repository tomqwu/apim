# Executive summary

## Outcome sought

An organization needs an enterprise API connectivity layer that can remain stable while workloads move from legacy platforms toward Kubernetes and fit-for-purpose integration services. The choice is larger than a reverse proxy: it includes governance, identity, product lifecycle, workload-local traffic processing, API operations, audit, resilience, and an operating model that lets domain teams move safely.

## Provisional direction

**Recommendation — provisional:** approve a stage-gated evidence-closure programme, not a product selection. Screen all seven exact deployment variants at E1/E2. Subject to that screen, take Kong Konnect hybrid and self-managed Kong into controlled E3 PoCs as low-confidence priority-validation hypotheses; benchmark approved finalist variants from Azure APIM and Apigee symmetrically; retain MuleSoft as the current-state baseline.

The hypothesis rests on Kong's clean separation of control and data planes, data-plane placement near workloads, native Kubernetes/Gateway API integration, and declarative workflows. It is not yet a product selection. A Gate 2 conditional selection requires pass/fail security and residency dispositions, disconnected-control-plane tests, plugin/licensing validation, support-model review, performance tests, and operating-cost analysis. Gate 4 approval to scale additionally requires representative E4 production-pilot evidence.

The formal steering recommendation, excluded decisions, conditions, and exit evidence are in the [principal methodology and decision-assurance review](../reports/methodology-review.md).

## Important findings from official documentation

- **Confirmed:** Kong hybrid data planes continue proxying with cached configuration if their control plane is unavailable; configuration changes stop until connectivity returns. CP/DP communication is protected with mTLS. Hybrid mode has plugin constraints, including no cluster rate-limiting strategy and no Kong OAuth 2.0 plugin compatibility.
- **Confirmed:** Azure APIM offers a containerized self-hosted gateway for hybrid/multicloud placement. The customer owns its hosting, scaling, uptime, and complex network troubleshooting. Current APIM workspaces cannot be associated with a self-hosted gateway.
- **Confirmed:** Apigee Hybrid separates a Google-hosted management plane from a customer-managed Kubernetes runtime. Runtime services include message processors, synchronizer, Cassandra, and MART; this provides locality and control at a non-trivial operations cost.
- **Confirmed:** MuleSoft DataWeave is an application data-transformation language, while Mule API Manager policies govern gateway traffic. Therefore a Mule exit must separate gateway concerns from transformation and integration workloads.

## Architecture stance

The gateway owns transport-facing cross-cutting controls: authentication enforcement, coarse authorization, threat/schema checks, quotas, traffic management, routing, protocol-level mediation, and telemetry. Domain services or dedicated integration runtimes own business logic, complex transformation, workflow, state, batch, messaging, and connectors. Kong must not become the next Mule monolith.

## Next decision gates

1. **Gate 0 — decision contract:** confirm scope, PCF meaning, Mule inventory, traffic/SLO profiles, environments, regions, identity, residency controls, mandatory gates, weights, evidence threshold, and decision rights.
2. **Gate 1 — finalist down-select:** apply an equivalent E1/E2 screen to all seven exact variants and approve the symmetric finalist proof scope.
3. **Gate 2 — conditional selection:** run equivalent E3 tests and complete TCO, contract/support, staffing, risk, and sensitivity analysis using actual organization inputs.
4. **Gate 3 — production-pilot readiness:** build the selected platform foundation, controls, support model, runbooks, and tested rollback.
5. **Gate 4 — migration-at-scale approval:** pilot at least two representative Mule workloads—one gateway-dominant and one integration-dominant—and accept measured SLO, cost, operability, rollback, and reconciliation evidence.
6. **Gate 5 — decommission authorization:** prove dependency zero, archive required evidence, revalidate controls, and close legacy contracts before retirement.
