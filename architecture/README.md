# Architecture views

These are reference architectures and transition patterns, not approved organizational network designs. Replace assumption-labelled nodes with confirmed inventories and security zones.

The standalone Mermaid files are the canonical visual sources. Each is mirrored in a companion Markdown note so the same view renders in GitHub and the study site; repository validation prevents the copies from drifting.

## Diagram catalog

| Decision use | Maturity | Companion note | Mermaid source |
|---|---|---|---|
| Unvalidated current-state assumption map | Discovery required | [Current state](current-state.md) | [Source](diagrams/current-state.mmd) |
| Vendor-neutral logical target | Proposed logical model | [Target state](target-state.md) | [Source](diagrams/target-state.mmd) |
| Reversible coexistence and cutover | Proposed transition pattern | [Transition state](transition-state.md) | [Source](diagrams/transition-state.mmd) |
| Contract-to-runtime promotion and rollback | Proposed control pattern | [API operations](apiops-architecture.md) | [Source](diagrams/apiops-flow.mmd) |
| North–south and east–west boundaries | Proposed boundary model | [Network](network-architecture.md) | [North–south](diagrams/north-south.mmd) / [east–west](diagrams/east-west.mmd) |
| Authentication, enforcement, and response path | Proposed security flow | [Security](security-architecture.md) | [Source](diagrams/security-flow.mmd) |
| Telemetry collection and destinations | Proposed observability flow | [Observability](observability-architecture.md) | [Source](diagrams/observability-flow.mmd) |
| Regional request-path failover | Proposed recovery pattern | [HA/DR](ha-dr-architecture.md) | [Source](diagrams/dr-failover.mmd) |
| Workload responsibility decomposition | Proposed migration decision tree | [PCF-to-AKS transition](pcf-aks-transition.md) | [Source](diagrams/mule-decomposition.mmd) |
| Kong control/data separation | Candidate-specific hypothesis | [Kong hybrid](kong-hybrid-architecture.md) | [Source](diagrams/kong-control-data-plane.mmd) |
| Kong hybrid data-plane placement | Candidate-specific hypothesis | [Kong hybrid](kong-hybrid-architecture.md) | [Source](diagrams/hybrid-data-plane.mmd) |

## Comparative architecture rule

The [vendor-neutral logical target](target-state.md) is the canonical target architecture. Candidate physical views must use an equivalent frame: ownership boundary, request path, configuration flow, metadata/telemetry flow, persistence, locality, support boundary, assumptions, and required validation evidence.

The current Kong physical views document a priority-validation hypothesis, not a selection. Equivalent APIM, Apigee, and retained-Mule views are roadmap work and should be published only after their official topology and entitlement evidence is captured.
