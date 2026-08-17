# Kong deep dive

## Confirmed capabilities relevant to the hypothesis

- Kong supports traditional, DB-less, and hybrid deployment topologies. Hybrid separates configuration-bearing control planes from traffic-serving data planes.
- CP/DP connections are data-plane initiated and protected by mTLS; data planes retain last-known configuration through a control-plane interruption.
- Kong Ingress Controller translates Kubernetes Ingress, Gateway API, and Kong resources to gateway configuration. Gateway API is the preferred Kubernetes routing interface.
- decK provides declarative diff, validate, sync/apply, dump, and reset workflows against an Admin API, but cannot manage DB-less gateways through write operations.
- Prometheus and OpenTelemetry plugins support standard observability paths; plugin/topology/edition matrices must be checked feature by feature.

## PoC decision points

| Decision | Variant/test |
|---|---|
| SaaS versus enterprise-managed control | Konnect hybrid vs self-managed hybrid |
| Kubernetes ownership interface | KIC unmanaged Gateway API vs Kong Operator-managed gateways |
| Global rate limits | Local vs Redis-backed vs Advanced plugin, including Redis failure |
| API authentication | External Entra authorization server plus OIDC/JWT enforcement |
| Configuration authority | Gateway API/KIC for routes vs decK for non-Kubernetes control plane; prevent dual writers |
| Enterprise features | Licensed vendor-assisted test, never inferred from OSS baseline |

## Principal risks

Plugin licensing/topology incompatibility, custom-plugin supply chain, multiple configuration authorities, excessive cardinality, Redis dependency for distributed counters, portal/catalog gaps, and operational fragmentation across data planes.
