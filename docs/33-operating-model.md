# Operating model

## Core roles

| Role | Accountability |
|---|---|
| API platform product owner | Outcomes, roadmap, service levels, funding |
| Platform engineering | Gateway/control plane, templates, automation, upgrades |
| API governance | Standards, lifecycle, catalog, product model |
| Security/IAM/PKI | Controls, identity, certificates, exceptions, detection |
| SRE/operations | Monitoring, capacity, incidents, DR, runbooks |
| Domain API owner | Contract, backend, SLO, consumers, change lifecycle |
| Integration engineering | Transformation, workflow, messaging, connectors |
| FinOps/vendor management | Unit economics, licenses, contracts, support |

Define a paved road, service catalog, support tiers, onboarding SLO, production readiness review, emergency change, exception expiry, and quarterly evidence review. Central governance without self-service becomes a bottleneck; federation without enforceable guardrails becomes sprawl.

## Federated decision model

```mermaid
flowchart TB
  SP["Executive sponsor<br/>investment gates and risk appetite"] --> PO["API platform product owner<br/>outcomes, roadmap, service levels"]
  PO --> DA["Design and service authority<br/>standards, exceptions, readiness"]
  DA --> PE["Platform engineering<br/>paved road and runtime"]
  DA --> CTL["Security · SRE · FinOps<br/>control and assurance"]
  DA --> GOV["API governance<br/>contracts, lifecycle, catalog"]
  PE --> DOM["Domain API teams<br/>contracts, services, consumer outcomes"]
  CTL --> DOM
  GOV --> DOM
  DOM --> CON["Consumers and partners"]
```

Public registers use accountable roles or anonymized owner IDs. The named-person assignment and capacity plan remain in restricted programme records.
