# Target-state architecture

The target separates edge, API management control, gateway data, domain services, integration, and observability/security planes. Data planes are deployed by trust zone/failure domain near workloads; a reviewed control plane distributes configuration without entering the client request path. Stable API contracts decouple consumers from AKS or legacy backend location.

See `diagrams/target-state.mmd` and `docs/05-target-state-vision.md`.
