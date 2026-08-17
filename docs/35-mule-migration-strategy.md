# MuleSoft migration strategy

## Classify before migrating

- **G:** gateway-only/configuration dominant → selected gateway.
- **F:** facade plus simple mapping → gateway plus thin service if needed.
- **T:** complex transformation → AKS integration service/function.
- **O:** orchestration/workflow → domain/integration/workflow runtime.
- **M:** messaging/event → approved broker/event platform and consumers.
- **B:** batch/file/SFTP → job or managed transfer capability.
- **C:** connector-heavy → approved adapter, SaaS-native connector, or temporary coexistence.
- **R:** redundant/unused → retire after evidence and owner approval.

One Mule flow may contain several of these responsibilities. Decompose it into one or more rows before assigning target capabilities; do not force the entire flow into one primary class.

<!-- diagram-alias-source: ../architecture/diagrams/mule-decomposition.mmd -->
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

## Reversible migration waves

Wave 0 builds inventory and platform foundations. Wave 1 proves low-risk gateway parity. Wave 2 migrates representative integration patterns. Wave 3 scales a factory by pattern. Wave 4 retires shared Mule dependencies and contracts. Each wave has rollback, reconciliation, consumer communication, and decommission criteria.

```mermaid
flowchart LR
  W0["Wave 0<br/>inventory + foundations"] --> G0{"Inventory and control gate"}
  G0 --> W1["Wave 1<br/>gateway parity"] --> G1{"Production pilot gate"}
  G1 --> W2["Wave 2<br/>representative integration patterns"] --> G2{"Factory-readiness gate"}
  G2 --> W3["Wave 3<br/>pattern-based factory"] --> G3{"Dependency-zero gate"}
  G3 --> W4["Wave 4<br/>retire runtimes and contracts"]
  G1 -. "rollback" .-> W0
  G2 -. "rollback" .-> W1
  G3 -. "pause / remediate" .-> W2
```
