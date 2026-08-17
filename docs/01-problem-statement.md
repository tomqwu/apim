# Problem statement

## Decision

What target API management and integration architecture should an organization adopt to support hybrid workloads, consolidate legacy applications toward Kubernetes, reduce or retire integration-platform dependencies safely, and preserve enterprise-grade security, availability, governance, and auditability?

## In scope

- North-south enterprise APIs and selected internal API traffic.
- Kong Konnect hybrid, self-managed Kong, APIM managed gateway, APIM self-hosted gateway, Apigee X, Apigee Hybrid, and MuleSoft baseline.
- Identity, policy, network, data residency, resilience, observability, API lifecycle, developer experience, operations, support, portability, migration, and cost evidence.
- Stable facades over AKS, PCF, Mule, on-premises, SaaS, and partner backends during transition.

## Out of scope for product substitution

- Replacing application business logic with gateway policy.
- Selecting an enterprise event backbone, workflow engine, MFT platform, or universal integration runtime solely from gateway results.
- Assuming every east-west call traverses an enterprise gateway.
- Production design based on synthetic PoC performance.

## Success

A defensible decision includes traceable requirements, explicit unknowns, repeatable PoC evidence, sensitivity analysis, an actionable Mule decomposition plan, target and transition architectures, staffing/support implications, and reversible implementation waves.
