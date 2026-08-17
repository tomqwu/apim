# PCF-to-AKS transition pattern

Stable gateway route → existing PCF/Mule backend → deploy AKS backend → contract/golden tests → optional safe shadow → weighted canary → full cutover → rollback window → dependency validation → remove legacy route/DNS/certificates/monitoring/runtime.

For non-idempotent operations, do not duplicate or shadow live writes without a business-approved isolation and reconciliation design.

## Workload responsibility decomposition

<!-- diagram-source: diagrams/mule-decomposition.mmd -->
```mermaid
flowchart TD
  W["Mule workload"] --> D["Decompose into one or more responsibilities"]
  D -->|"G · gateway"| G["Selected gateway route and policy"]
  D -->|"F · simple facade"| F["Gateway plus thin service when needed"]
  D -->|"T · transformation"| T["Integration service or function"]
  D -->|"O · orchestration"| O["Domain or workflow runtime"]
  D -->|"M · messaging/events"| M["Broker/event platform and consumers"]
  D -->|"B · batch/file"| B["Job or managed transfer"]
  D -->|"C · connector-heavy"| C["Adapter, SaaS-native integration, or coexistence"]
  D -->|"R · redundant/unused"| R["Evidence-backed retirement"]
```

[Open the canonical Mermaid source](diagrams/mule-decomposition.mmd).
