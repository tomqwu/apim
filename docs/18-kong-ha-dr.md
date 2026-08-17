# Kong high availability and disaster recovery

Define separate SLOs for request path, configuration changes, administration, analytics, portal, and audit. A data plane proxying cached configuration does not mean all services are available.

## Exercises

- Kill pods and nodes; drain a zone; remove upstream endpoints.
- Break CP/DP connectivity, restart replicas, and add capacity while disconnected.
- Expire/revoke certificates; lose Redis, DNS, telemetry, registry, and secret delivery.
- Promote a second region and validate DNS/edge convergence plus client retry safety.
- Restore control-plane/database/configuration backup for self-managed variants.
- Reconcile analytics/audit gaps and demonstrate configuration consistency after recovery.

Record RTO/RPO per plane, manual dependencies, evidence owner, and last exercise date.
