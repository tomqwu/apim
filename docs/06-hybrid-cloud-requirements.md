# Hybrid-cloud requirements

## Mandatory candidate tests

1. Place runtime gateways in AKS and a simulated remote/private network while retaining one governance model.
2. Prove that API request bodies do not traverse the SaaS management plane in hybrid topology.
3. Interrupt control-plane connectivity, restart a running data-plane replica, and attempt clean capacity expansion.
4. Measure configuration propagation, rollback, stale-state visibility, and audit behavior.
5. Enforce least-privilege egress, private DNS, proxy, certificate rotation, and clock synchronization.
6. Demonstrate region/failure-domain isolation and document shared dependencies.
7. Validate support boundaries for Kubernetes, network plugins, service meshes, and third-party observability.
8. Record residency of configuration, consumer metadata, secrets, analytics, telemetry, support data, and backups.

## Required scenarios

- External client → edge/WAF → gateway → AKS.
- Internal client → private gateway → AKS.
- Gateway → PCF application during transition.
- Gateway → Mule API during coexistence.
- Gateway → on-premises/legacy backend.
- Gateway data plane disconnected from management plane.
- Region unavailable with DNS/edge failover.
- Backend migrates from PCF/Mule to AKS without consumer contract change.

"Hybrid" is not a yes/no feature; score each topology and failure mode separately.
