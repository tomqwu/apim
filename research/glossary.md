# Glossary

| Term | Meaning in this repository |
|---|---|
| API operations / APIOps | Reviewed automation of API contracts, gateway configuration, policy, tests, promotion, and evidence |
| Control plane (CP) | Management/configuration plane; exact vendor scope varies |
| Data plane (DP) | Traffic-processing gateway/runtime |
| Gateway API | Kubernetes SIG Network resources for role-oriented service networking; not itself an API management product |
| Golden tests | Curated input/output cases proving migrated behavior |
| Hybrid | Management and runtime components placed across vendor and customer locations; never a single yes/no capability |
| KIC | Kong Ingress Controller |
| MART | Apigee Management API for Runtime data |
| PCF | Assumed Pivotal Cloud Foundry pending organizational confirmation |
| RTO/RPO | Recovery time/recovery point objective |
| SLO | Service-level objective |
| Strangler | Incrementally redirect functionality from a legacy implementation behind a stable boundary |

## Kong terminology crosswalk

Use this as a **nearest operating analogue**, not a one-to-one translation. A familiar MuleSoft or Apigee noun can hide a different state boundary, lifecycle, scope, or ownership model. The target mapping must therefore connect each source object to the exact Kong entities, source-controlled artifact, identity record, runtime state, evidence, and owner that replace its behavior.

| Kong term | Meaning in the proposed self-managed hybrid target | Nearest MuleSoft / Apigee analogue | Important non-equivalence and migration question |
|---|---|---|---|
| Gateway Service | Connectivity metadata for an upstream application; Routes send matched requests to it | Mule API instance or proxy endpoint; Apigee TargetEndpoint/proxy target relationship | A Gateway Service is not the API contract, catalog entry, product, consumer agreement, or application runtime. Which source objects and owners supply those missing layers? |
| Route | Request match and ingress behavior attached to a Gateway Service; Route-scoped plugins can transform or govern traffic | Mule proxy endpoint/listener and policy scope; Apigee ProxyEndpoint base path and conditional flows | Match priority, path/host rewriting, environment attachment, flow conditions, and error behavior require golden-corpus tests rather than a name mapping. |
| Consumer | A client identity record used by gateway authentication and policy plugins | Mule client application/contract principal; Apigee developer app credential principal | A Consumer is not a workforce operator or automatically the portal application/owner record. How are portal registration, credentials, ownership, join/move/leave, and runtime denial reconciled? |
| Consumer Group | A collection used to apply shared plugin configuration and policy | Mule client tier/group convention; Apigee API-product/app grouping | Group membership, plugin precedence, quota semantics, and commercial/SLA contracts are not equivalent. Which system remains authoritative for each? |
| Plugin | Request/response lifecycle extension attached globally or to supported entity scopes | Mule Gateway policy/custom policy; Apigee policy/shared flow/callout | Policy names do not prove semantic parity. Confirm scope, precedence, failure mode, performance, upgrade/support boundary, and whether durable business logic must move to an owned service instead. |
| Upstream | Kong load-balancer abstraction that points to Targets | Mule backend endpoint pool; Apigee target server/load-balancing relationship | Health, circuit breaking, retry, discovery, non-idempotent request behavior, and cross-region steering must be proved against the exact design. |
| Target | One host/IP and port inside an Upstream | Mule backend instance; Apigee target-server endpoint | A Target is runtime reachability, not the owning service, contract, readiness state, or business-outcome authority. |
| Workspace | Administrative namespace for many Kong entities | Mule business group/environment; Apigee organization/environment/space | Workspaces do not create a complete product, capacity, network, recovery, or legal boundary. Choose the repository, RBAC, CP, cluster, and owner combination deliberately. |
| Control Plane (CP) | Customer-operated Kong configuration and administration nodes backed by PostgreSQL in `KP-SMH1` | Anypoint management plane; Apigee management services | The proposed target transfers CP, PostgreSQL, PKI, backup/restore, upgrade, audit, plugin, license, and 24×7 operating accountability to the enterprise. This is an operating-risk statement, not a legal-liability conclusion. |
| Data Plane (DP) | Request-serving Kong nodes that receive and cache accepted CP configuration | Mule Gateway/Omni Gateway runtime; Apigee Message Processor/runtime plane | Existing cached service, restart, clean-node scaling, urgent mutation/revocation, license, and telemetry behavior differ during CP loss and require separate admission rules. |
| Kong Manager / Admin API | Human and programmable administration surfaces for a self-managed CP | Anypoint API Manager; Apigee UI/API | The Admin API is full-control infrastructure. UI/API presence does not define Git authority, approval, deletion safety, audit completeness, or organizational access lifecycle. |
| decK | Declarative Kong entity validation, diff, apply/sync, dump, and related APIOps tooling | Mule CLI/policy deployment automation; Apigee API/proxy bundle pipeline | decK does not manage every platform artifact, and `sync` can delete unmanaged entities. Define one writer per entity and prove deletion preview, rollback, drift, active digest, and restore. |
| KIC | Controller that reconciles Kubernetes ingress/Gateway API intent into Kong configuration | Mule Kubernetes deployment/operator path; Apigee hybrid ingress/runtime controllers | Kubernetes resources and decK/Admin API must not become competing writers for the same entity. Confirm conformance, attachment policy, status truth, CRD lifecycle, and exact support. |
| Kong Operator | Kubernetes operator for supported Kong resource and lifecycle patterns | Mule/Apigee deployment operators and Helm controllers | Operator ownership is not automatic platform ownership. Freeze supported versions, authority, privileges, upgrade/rollback, recovery, and support responsibility. |
| API contract / catalog product | Remains a source-controlled OpenAPI/RAML contract plus the chosen catalog/product and owner system | Mule API asset/version and Exchange/API Manager product surface; Apigee API product/catalog | No single Gateway Service, Route, or Workspace replaces the full asset/product/subscription lifecycle. Keep contract, catalog, entitlement, consumer, and runtime identities linked by immutable IDs. |

Official point-of-use references: [Kong Gateway entities](https://developer.konghq.com/gateway/entities/), [plugin scope and precedence](https://developer.konghq.com/gateway/entities/plugin/), [hybrid mode](https://developer.konghq.com/gateway/hybrid-mode/), [decK Gateway commands](https://developer.konghq.com/deck/gateway/), [MuleSoft API instances](https://docs.mulesoft.com/api-manager/latest/api-instance-landing-page), [MuleSoft gateway policies](https://docs.mulesoft.com/mule-gateway/policies-policy-overview), and [Apigee proxy configuration](https://docs.cloud.google.com/apigee/docs/api-platform/reference/api-proxy-configuration-reference).
