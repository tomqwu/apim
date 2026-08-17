# Target-state vision

```mermaid
flowchart TB
  C["Customers, staff, partners, workloads"] --> E["Edge: DNS, DDoS, WAF, load balancing"]
  E --> DP["Regional/private Kong data planes"]
  CP["Approved control plane"] -->|"mTLS configuration; no request payloads"| DP
  GIT["OpenAPI + policy + route source"] --> CI["Guarded API operations pipeline"] --> CP
  DP --> AKS["AKS domain services"]
  DP --> LEG["Temporary PCF / Mule / legacy backends"]
  DP --> SAAS["Approved SaaS and partners"]
  AKS --> INT["Integration plane: services, workflow, messaging, events, adapters"]
  DP --> OBS["Metrics, logs, traces, audit"]
  INT --> OBS
```

## Planes and ownership

| Plane | Owns | Must not own |
|---|---|---|
| Edge | DDoS/WAF, public TLS, coarse routing | API product policy or business orchestration |
| API management control | catalog, configuration, policy, consumer/product lifecycle | production request payload processing |
| Gateway data | authentication enforcement, traffic controls, validation, routing, telemetry | long-lived state and complex business logic |
| Domain services | business rules and canonical domain behavior | enterprise gateway administration |
| Integration | orchestration, transformation, protocol adapters, messaging, files, batch | universal north-south policy |
| Observability/security | collection, correlation, alerting, detection, evidence | silent payload capture |

## Deployment intent

- Separate external, internal/high-trust, and nonproduction failure domains when justified by threat and scale profiles.
- Use multiple replicas, topology spread, disruption budgets, autoscaling, immutable images, and controlled upgrades.
- Keep management access private and strongly authenticated; permit data planes only the required outbound control-plane and telemetry paths.
- Use stable gateway hostnames to decouple consumers from backend movement.
- Treat east-west policy as a service-mesh or workload concern unless an enterprise API boundary is deliberate.
