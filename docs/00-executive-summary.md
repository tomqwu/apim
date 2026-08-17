# Executive summary

## Outcome sought

An organization needs an enterprise API connectivity layer that can remain stable while workloads move from legacy platforms toward Kubernetes and fit-for-purpose integration services. The choice is larger than a reverse proxy: it includes governance, identity, product lifecycle, workload-local traffic processing, API operations, audit, resilience, and an operating model that lets domain teams move safely.

## Provisional direction

**Recommendation — provisional:** take Kong Konnect hybrid and self-managed Kong into a controlled PoC as the leading deployment variants. Benchmark them against Azure APIM managed plus self-hosted gateway and Apigee X plus Apigee Hybrid. Retain MuleSoft as the current-state baseline.

The hypothesis rests on Kong's clean separation of control and data planes, data-plane placement near workloads, native Kubernetes/Gateway API integration, and declarative workflows. It is not yet a product selection. The hypothesis must survive pass/fail security and residency gates, disconnected-control-plane tests, plugin/licensing validation, support-model review, performance tests, operating-cost analysis, and migration pilots.

## Important findings from official documentation

- **Confirmed:** Kong hybrid data planes continue proxying with cached configuration if their control plane is unavailable; configuration changes stop until connectivity returns. CP/DP communication is protected with mTLS. Hybrid mode has plugin constraints, including no cluster rate-limiting strategy and no Kong OAuth 2.0 plugin compatibility.
- **Confirmed:** Azure APIM offers a containerized self-hosted gateway for hybrid/multicloud placement. The customer owns its hosting, scaling, uptime, and complex network troubleshooting. Current APIM workspaces cannot be associated with a self-hosted gateway.
- **Confirmed:** Apigee Hybrid separates a Google-hosted management plane from a customer-managed Kubernetes runtime. Runtime services include message processors, synchronizer, Cassandra, and MART; this provides locality and control at a non-trivial operations cost.
- **Confirmed:** MuleSoft DataWeave is an application data-transformation language, while Mule API Manager policies govern gateway traffic. Therefore a Mule exit must separate gateway concerns from transformation and integration workloads.

## Architecture stance

The gateway owns transport-facing cross-cutting controls: authentication enforcement, coarse authorization, threat/schema checks, quotas, traffic management, routing, protocol-level mediation, and telemetry. Domain services or dedicated integration runtimes own business logic, complex transformation, workflow, state, batch, messaging, and connectors. Kong must not become the next Mule monolith.

## Next decision gates

1. Confirm PCF meaning, Mule inventory, traffic/SLO profiles, environments, regions, identity, and residency controls.
2. Agree mandatory gates and category weights before vendor workshops.
3. Run the baseline PoC, followed by licensed/vendor-assisted tests.
4. Pilot two representative Mule workloads: one gateway-heavy and one integration-heavy.
5. Perform TCO and contract assessment using actual quotes and staffing assumptions.
6. Issue the product recommendation only after evidence coverage reaches the agreed threshold.
