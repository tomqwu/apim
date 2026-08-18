# Kong Gateway research evidence ledger

## Purpose and decision boundary

This is the supporting evidence ledger for the principal studies [10](../docs/10-kong-deep-dive.md) through [18](../docs/18-kong-ha-dr.md), the [Kong long-term multicloud study roadmap](../docs/44-kong-multicloud-study-roadmap.md), and the [Kong enterprise platform deployment strategy](../docs/47-kong-enterprise-platform-strategy.md). It records bounded variant boundaries, primary-source claims, counter-evidence and proof gaps. It does not repeat the study arguments, score a vendor, or report tests.

**As of:** 2026-08-18

**Evidence state:** `E1 — documented` unless a row says otherwise. `E2 — contractual`, `E3 — reproducible lab`, and `E4 — representative pilot/operating` evidence are absent.

**Reference case:** [RE-1 enterprise reference case](../docs/41-enterprise-reference-case.md) is synthetic and non-organizational. Its numbers are **scenario assumptions**, not estate facts, vendor limits or observed results.
**Version baseline:** customer-hosted analysis uses the Kong Gateway Enterprise **3.14 LTS version line**, with an exact patch/image digest still to be frozen. Kong 3.15 is currently supported but is not silently substituted into that baseline.

**Current planning posture:** stakeholders intend to proceed with Kong. `KV-1` self-managed hybrid is the leading custody target for a bounded, reversible foundation; it is not an `E3`/`E4` result. `KV-2` Konnect hybrid is the mandatory same-vendor operating benchmark if customer control-plane custody does not justify its PostgreSQL, PKI, upgrade, backup, recovery, observability, and on-call burden. A separate non-Kong rebuild remains the true platform-exit proof.

## Bounded deployable-archetype register

KV-1 through KV-8 keep materially different authorities and runtime owners separate. They are not yet exact deployable options: each still requires an immutable patch/image/chart/substrate/configuration record or vendor-managed service configuration, plus region/network, plugin, objective, entitlement and support evidence at Gate 1.

| Variant ID | Bounded deployable archetype | Configuration authority | Request runtime and owner | Evidence boundary |
|---|---|---|---|---|
| KV-1 | Self-managed Kong Gateway Enterprise hybrid | Customer CP/Admin API and PostgreSQL; one approved pipeline | Customer-hosted DPs on AKS/other supported substrate | CP/DB/PKI/license/cache/plugin/backup/DR are customer obligations |
| KV-2 | Konnect standard CP with customer-hosted DPs | Regional Konnect CP and approved API/decK/Terraform path | Customer-hosted DPs | Payload locality does not settle Konnect metadata/telemetry/support data handling |
| KV-3 | Konnect Dedicated Cloud Gateway | Konnect CP | Kong-operated single-tenant DP environment in selected supported cloud/region | Network/region/plugin/upgrade/autoscale/evidence and E2 terms are service-specific |
| KV-4 | DB-less Gateway with KIC 3.5 and Gateway API 1.3 | Kubernetes resources reconciled by KIC | Customer-hosted DB-less Gateway 3.14 LTS-policy pods | Kubernetes/controller scope is authoritative; decK writes are excluded |
| KV-5 | DB-less Gateway without KIC | Versioned whole declarative configuration | Customer-hosted DB-less pods | Customer owns artifact distribution/reload/memory/replica consistency |
| KV-6 | Kong Operator 2.2.1-managed Gateway/DataPlane | Kubernetes CRDs/reconciliation according to the selected Operator pattern | Customer-hosted or Konnect-attached DPs according to resource model | Current public Kubernetes-compatibility table lacks an explicit 2.2 row; `Open question` |
| KV-7 | Konnect Serverless Gateway | Konnect | Automatically provisioned/updated lightweight DPs | Screening-level only until public networking, limit, plugin and RE-1 workload fit are proven |
| KV-8 | Traditional database-backed Gateway | Admin API/database-backed authority | Each customer-operated proxy connects to shared PostgreSQL | Retained only when a required database-writing plugin/topology justifies it |

No evidence from KV-7 can establish KV-2 or KV-3 behavior. No result from KV-4 can establish hybrid cached-state behavior. Managed and self-managed variants receive the same RE-1 proof thresholds.

## Claim and primary-source register

IDs K-001 through K-015 already exist in `research/sources.csv`. IDs marked **proposed** below are exact additions for the repository source register; this file does not edit that shared CSV.

| Claim ID | Exact claim usable in decision design | Primary/official source | State and revalidation trigger |
|---|---|---|---|
| K-001 | Hybrid separates CP configuration/Admin API from DP traffic; DPs cache configuration, can restart disconnected, and a new DP can be seeded from LMDB or declarative fallback | [Hybrid mode](https://developer.konghq.com/gateway/hybrid-mode/) | `E1`; recheck per Gateway release/cache format |
| K-002 | DPs initiate the CP connection; CP/DP traffic uses mutual TLS and persistent control communication | [CP/DP communication](https://developer.konghq.com/gateway/cp-dp-communication/) | `E1`; recheck endpoints/certificate mode |
| K-003 | Traditional, DB-less and hybrid are different topologies with different state and plugin behavior | [Deployment topologies](https://developer.konghq.com/gateway/deployment-topologies/) | `E1`; recheck candidate version |
| K-004 | Unmanaged KIC does not create Gateway Deployments/Services and can merge watched Gateway API resources into generated configuration | [KIC Gateway API](https://developer.konghq.com/kubernetes-ingress-controller/gateway-api/) | `E1`; recheck controller/Gateway API versions |
| K-006 | decK targets Admin/Konnect APIs for database-backed topologies and does not write DB-less Gateway state | [decK Gateway](https://developer.konghq.com/deck/gateway/) | `E1`; recheck exact decK/Gateway pair |
| K-007 | Prometheus metrics are node-level; all nodes need discovery/scrape; CP exposes DP last-seen/hash/sync/certificate metrics where applicable | [Prometheus plugin](https://developer.konghq.com/plugins/prometheus/) | `E1`; recheck plugin/version/topology |
| K-008 | OpenTelemetry export uses per-worker, memory-only queues; warnings start at 80% and oldest entries are removed at capacity | [OpenTelemetry plugin](https://developer.konghq.com/plugins/opentelemetry/) | `E1`; queue loss must be E3-tested |
| K-009 | Request Validator is Enterprise-labelled and validates supported request schema/parameters | [Request Validator](https://developer.konghq.com/plugins/request-validator/) | `E1`; E2 entitlement and exact schema coverage required |
| K-010 | Rate Limiting exposes strategy-dependent behavior and must be interpreted with topology | [Rate Limiting plugin](https://developer.konghq.com/plugins/rate-limiting/) | `E1`; exact plugin/version/config required |
| K-011 | Current release and security behavior can change at patch level | [Gateway changelog](https://developer.konghq.com/gateway/changelog/) | `E1`, highly volatile; check before every freeze |
| K-013 | Self-managed hybrid installation requires CP database configuration and CP/DP clustering certificates | [Hybrid installation](https://developer.konghq.com/gateway/install/hybrid/) | `E1`; tutorial is not production topology proof |
| K-014 | Self-hosted, Dedicated and Serverless DPs are distinct hosting modes | [DP hosting options](https://developer.konghq.com/gateway/topology-hosting-options/) | `E1`; recheck service offering and region |
| K-015 | Kong Operator is a separate Kubernetes reconciliation/lifecycle component | [Operator overview](https://developer.konghq.com/operator/) | `E1`; exact release/support/CRDs required |
| K-016 **proposed** | Kong 3.14 is an LTS line; supported releases/targets and EOL dates are version-specific | [Gateway support policy](https://developer.konghq.com/gateway/version-support-policy/) | `E1`, volatile; check at BOM freeze |
| K-017 **proposed** | Database-native backup is primary for database-backed modes; declarative export is secondary/incomplete; key/config materials need separate handling | [Backup and restore](https://developer.konghq.com/gateway/upgrade/backup-and-restore/) | `E1`; E3 isolated restore required |
| K-018 **proposed** | Konnect hybrid uses regional endpoints/ports and a DP-initiated service connection | [Konnect networking](https://developer.konghq.com/konnect-platform/network/) | `E1`, volatile; exact geo/endpoints at freeze |
| K-019 **proposed** | Konnect lists geo-specific Gateway/consumer/API/portal objects while authentication, billing and usage are shared between geos | [Konnect geos](https://developer.konghq.com/konnect-platform/geos/) | `E1`; E2 DPA/location terms govern decision use |
| K-020 **proposed** | Dedicated Cloud Gateways run in Kong-managed single-tenant DP environments while the Konnect CP remains multi-tenant | [Dedicated Cloud Gateways](https://developer.konghq.com/dedicated-cloud-gateways/) | `E1`; service/entitlement/region revalidation |
| K-021 **proposed** | Dedicated public/private networking features differ by cloud and a CP can manage deployments across clouds | [Dedicated network architecture](https://developer.konghq.com/dedicated-cloud-gateways/network-architecture/) | `E1`, volatile; exact cloud/region proof required |
| K-022 **proposed** | DB-less holds entities in memory, uses whole declarative config, exposes read-only entity administration and is incompatible with decK/Konnect | [DB-less mode](https://developer.konghq.com/gateway/db-less-mode/) | `E1`; memory/config distribution need E3 |
| K-023 **proposed** | KIC treats Kubernetes resources as source of truth and configures, but does not proxy, request traffic | [KIC architecture](https://developer.konghq.com/kubernetes-ingress-controller/architecture/) | `E1`; controller scope/ownership need E3 |
| K-024 **proposed** | KIC 3.5 supports Gateway API 1.3; Gateway/Kubernetes compatibility is table-driven | [KIC compatibility](https://developer.konghq.com/kubernetes-ingress-controller/version-compatibility/) | `E1`, volatile; exact AKS/KIC/Gateway intersection |
| K-025 **proposed** | Serverless is automatically provisioned/updated and currently documents public networking plus bounded request/payload/custom-plugin behavior | [Serverless reference](https://developer.konghq.com/serverless-gateways/reference/) | `E1`, highly volatile; screening only |
| K-026 **proposed** | Traditional mode connects every Gateway node to shared PostgreSQL and caches entities locally | [Traditional mode](https://developer.konghq.com/gateway/traditional-mode/) | `E1`; DB/plugin/runtime behavior needs exact proof |
| K-027 **proposed** | Redis rate-limit disconnection can fall back to node-local counters, permitting more total requests than the shared limit | [Rate-limiting strategies](https://developer.konghq.com/gateway/rate-limiting/strategies/) | `E1`; mandatory E3 security/capacity test |
| K-028 **proposed** | Hybrid upgrades CP before DP; database migrations are not reversible; DP/DB-less uses rolling strategy | [Gateway upgrades](https://developer.konghq.com/gateway/upgrade/) | `E1`; exact path/plugin/backup test required |
| K-029 **proposed** | Plugin support differs by self-managed topology and Konnect hosting mode | [Plugin compatibility](https://developer.konghq.com/plugins/compatibility/) | `E1`, highly volatile; E2 entitlement required |
| K-030 **proposed** | Self-managed nodes load/distribute Enterprise licenses according to deployment method; expiry affects writes/startup differently by topology/version | [Gateway licenses](https://developer.konghq.com/gateway/entities/license/) | `E1`; exact-version E3 continuity drill |
| K-031 **proposed** | Mixed DP versions expose a compatibility subset and incompatible configurations may be rejected | [DP version compatibility](https://developer.konghq.com/gateway/data-plane-version-compatibility/) | `E1`; recheck exact CP/DP versions |
| K-032 **proposed** | Operator 2.2 is supported but no LTS Operator line exists; releases have independent support clocks | [Operator support policy](https://developer.konghq.com/operator/support-policy/) | `E1`, volatile; compatibility confirmation needed |
| K-033 **proposed** | `/status` liveness differs from `/status/ready`; hybrid/DB-less readiness checks valid non-empty config/workers/plugins but not external network/upstream health | [Gateway probes](https://developer.konghq.com/gateway/traffic-control/health-check-probes/) | `E1`; outside-in E3 probes required |
| K-034 **proposed** | Enterprise OIDC caches discovery/JWKS; storage/TTL/rediscovery behavior differs between DB and DB-less | [OIDC plugin](https://developer.konghq.com/plugins/openid-connect/) | `E1`; E2 entitlement and E3 rollover/outage |
| K-035 **proposed** | Enterprise mTLS Auth validates against configured CAs and requests a client certificate during every handshake when configured on any Route/Service | [mTLS Auth](https://developer.konghq.com/plugins/mtls-auth/) | `E1`; shared-listener/client impact E3 |
| K-036 **proposed** | mTLS revocation modes can prefer strict availability loss or more permissive network-error handling | [mTLS Auth configuration](https://developer.konghq.com/plugins/mtls-auth/reference/) | `E1`; risk policy and E3 failure matrix required |
| K-037 **proposed** | Secret-management capability differs by OSS/Enterprise and supports references only in eligible fields | [Secrets management](https://developer.konghq.com/gateway/secrets-management/) | `E1`; entitlement/backends/identity require proof |
| K-038 **proposed** | Vault references, refresh, provider support and bootstrap limitations are field/backend/version-specific | [Vault entity](https://developer.konghq.com/gateway/entities/vault/) | `E1`; E3 clean-pod/rotation/denial test |
| K-039 **proposed** | Self-managed Gateway audit entries can be read/exported through the Admin API | [Gateway audit logs](https://developer.konghq.com/gateway/audit-logs/) | `E1`; entitlement, completeness, retention E2/E3 |
| K-040 **proposed** | Konnect has control-plane and service-specific predefined roles | [Konnect teams and roles](https://developer.konghq.com/konnect-platform/teams-and-roles/) | `E1`; organization mapping/SoD E3 |
| K-041 **proposed** | Custom plugins execute in request lifecycle phases with defined priority and use the PDK | [Custom plugin handler](https://developer.konghq.com/custom-plugins/handler.lua/) | `E1`; supply-chain/performance/support E2/E3 |
| K-042 **proposed** | decK tags scope partial management but require consistent selection and careful cross-entity references | [decK tags](https://developer.konghq.com/deck/gateway/tags/) | `E1`; destructive/foreign-key E3 test |
| K-043 **proposed** | Gateway logs expose configurable latency/request data and can contain sensitive request details | [Gateway logs](https://developer.konghq.com/gateway/logs/) | `E1`; schema/redaction/version E3 |
| K-044 **proposed** | Serialized log context can include sensitive headers/query/identity; only specified authentication headers are redacted by default | [`kong.log` PDK](https://developer.konghq.com/gateway/pdk/reference/kong.log/) | `E1`; privacy scan required |
| K-045 **proposed** | Kong's benchmark method separates request termination, bare proxy and added configuration and requires repeated stable runs | [Establish a benchmark](https://developer.konghq.com/gateway/performance/establish-a-benchmark/) | `E1`; method page excludes Konnect and is not capacity evidence |
| K-046 **proposed** | Performance characterization must isolate workers/CPU, client/upstream, custom plugins, autoscaling, configuration change and third-party bottlenecks | [Optimize performance](https://developer.konghq.com/gateway/performance/optimize/) | `E1`; translate to exact E3 topology |
| K-047 **proposed** | Resource requirements vary with entities, workers, cache, plugins and queues; published bands are starting guidance | [Resource sizing](https://developer.konghq.com/gateway/resource-sizing-guidelines/) | `E1`; no decision use without E3 |
| K-048 **proposed** | Larger payloads and buffering/streaming choices materially change memory/disk/latency behavior | [Large-payload tuning](https://developer.konghq.com/gateway/performance/large-payloads/) | `E1`; J-04/J-05 exact payload E3 |
| K-049 **proposed** | CP/traditional blue-green upgrade has limited support and database migration finalization changes rollback | [Blue-green upgrade](https://developer.konghq.com/gateway/upgrade/blue-green/) | `E1`; exact upgrade plan/support statement required |
| K-050 **proposed** | Konnect maintains a topology-specific Gateway compatibility policy; vendor-managed Dedicated and Serverless runtimes cannot be assumed to follow customer-hosted DP version control | [Konnect compatibility](https://developer.konghq.com/konnect-platform/compatibility/) | `E1`, volatile; record policy and resolved service version at option freeze |
| K-051 **proposed** | New data planes normally cannot become configured during a CP outage; object-store fallback adds exact-version, IAM/encryption, exporter, one-shot import and maintenance obligations | [Control-plane outage management](https://developer.konghq.com/gateway/cp-outage/) | `E1`; prove no-fallback and fallback paths independently |
| K-052 **proposed** | Self-managed hybrid/traditional configuration can be migrated to Konnect, but RBAC, workspaces/control planes, certificates, custom plugins and data planes require explicit transformation and validation | [Self-managed migration to Konnect](https://developer.konghq.com/gateway/self-managed-migration/) | `E1`; same-vendor custody benchmark, not true platform exit |
| K-053 **proposed** | The self-managed Admin API has full control and requires a private authenticated boundary; Enterprise RBAC and audit behavior must be explicitly configured and tested | [Secure the Admin API](https://developer.konghq.com/gateway/secure-the-admin-api/), [RBAC](https://developer.konghq.com/gateway/entities/rbac/), [audit logs](https://developer.konghq.com/gateway/audit-logs/) | `E1`; entitlement/configuration plus negative-access and export proof required |

## External platform sources needed by the AKS study

These are primary/official sources and also need source-register rows if not added elsewhere:

| Proposed ID | Claim | Source | Evidence use |
|---|---|---|---|
| AZK-001 | AKS workloads require explicit replicas, probes, resources, disruption budgets and topology rules | [AKS deployment and cluster reliability](https://learn.microsoft.com/en-us/azure/aks/best-practices-app-cluster-reliability) | `E1`; design input, not implemented state |
| AZK-002 | AKS baseline separates network, identity, workload, secret, upgrade and continuity responsibilities | [AKS baseline architecture](https://learn.microsoft.com/en-us/azure/architecture/reference-architectures/containers/aks/baseline-aks) | `E1`; landing-zone input only |
| K8S-005 | Topology spread depends on labels/domains and has scale-from-zero/imbalance limitations | [Kubernetes topology spread](https://kubernetes.io/docs/concepts/scheduling-eviction/topology-spread-constraints/) | `E1`; exact-version scheduling E3 required |

Existing `K8S-002` (disruptions/PDB) and `K8S-003` (HPA) remain relevant and should be retained; no duplicate source row is needed.

## State, dependency, and ownership ledger

| State/dependency | Authority | Runtime copy | Failure consequence | Proof reference |
|---|---|---|---|---|
| Gateway entities in hybrid | self-managed PostgreSQL/CP or Konnect CP | per-DP memory/LMDB | cached traffic can outlive change path; clean scale needs seed | CPDP-P01/P02, KDR-P02 |
| DB-less/KIC entities | Kubernetes resources/controller-generated config | per-DP in-memory configuration | controller/API loss freezes change; cross-scope merge can widen blast radius | AKS-P04, KOPS-P01/P02 |
| License | self-managed distribution/entity/file/env according to topology | node startup/runtime state | change and restart behavior can diverge on expiry | CPDP-P02, KDR-P04 |
| CP/DP trust | clustering cert/PKI/Konnect-issued or supplied credential | each DP | config/telemetry stop while cached proxying may continue | CPDP-P03, KSEC-P02 |
| Consumer/identity trust | CP entities plus IdP/PKI/vault | OIDC/CA/secret caches | revocation/change may be stale or unavailable | KSEC-P01/P02/P04 |
| Quota | local worker/node or Redis according to plugin policy | local counters/cache | failover/partition can weaken global accuracy | KONG-P02, KSEC-P03 |
| PostgreSQL | self-managed database | CP caches plus DP config cache | authority/admin/backup/migration failure; runtime can mask it | KDR-P03/P06 |
| Custom plugin | signed artifact repository and deployment manifests | CP and every DP in hybrid | missing/divergent code, startup or semantic defect | KSEC-P05, KPERF-P01 |
| Telemetry | DP worker queues, CP/collector/SIEM | non-durable queues | oldest loss and audit/analytics gaps | KOBS-P03, KDR-P05 |
| Business outcome | service ledger/database/queue | never authoritative at Gateway | I-01/I-06 ambiguity and stale data | KDR-P01/P05 |

## RE-1 evidence traceability

| Journey/failure | Product mechanism to test | Counter-evidence that prevents overclaim | Principal proof IDs |
|---|---|---|---|
| J-01 / I-01 | identity/policy/routing/correlation | Gateway status cannot prove a money-transfer outcome or make retries idempotent | KSEC-P01, KOBS-P01, KDR-P01 |
| J-02 | routing, auth, optional cache | response cache can violate freshness/privacy and hide regional stale data | KPERF-P01, KDR-P05 |
| J-03 / I-03 | OIDC, mTLS, CA/JWKS cache, quota | chain-valid identity is not transaction authorization; revocation and pinned clients can fail | KSEC-P01/P02/P03 |
| J-04 | validation, size/time controls and buffering | schema-valid is not semantically safe; large bodies alter disk/memory/latency | KSEC-P05, KPERF-P01/P04 |
| J-05 | optional control API | request gateway is not durable file transfer, malware scanning or batch reconciliation | workload disposition required before performance/DR test |
| J-06 / I-02 | decK/CP or KIC authority, DP sync/cache/hash | source merge/API acceptance is not runtime convergence; clean DP differs from cached DP | CPDP-P01/P02, KOPS-P01/P05 |
| I-04 | replica/isolation and rate/Redis policy | shared CPU/DNS/Redis/collector/CP can cross tenant boundaries | AKS-P05, KPERF-P04 |
| I-05 | OTel/analytics buffers and standard signals | queues are non-durable and can delete oldest records | KOBS-P03/P05 |
| I-06 | regional DPs and edge steering | config hash/pod readiness does not prove identity, business data or client convergence | KDR-P05 |
| I-07 | Gateway validation and versioned route | parser/schema/service versions can accept different contracts | KOPS-P03 |
| I-08 | configuration rollback/upgrade backup | Gateway revert cannot undo service data/schema or irreversible DB migration | KOPS-P04, KDR-P06 |

## Counter-hypothesis and non-fit register

| Counter-hypothesis | Current evidence | Falsifier/non-fit threshold owner |
|---|---|---|
| Konnect CP necessarily carries business payloads | KV-2 DPs proxy customer traffic locally, but telemetry/config metadata remain | Privacy/security approve field-level flow capture plus E2 terms |
| Cached hybrid is equivalent to autonomous/air-gapped service | Clean scale, emergency change, license, identity, registry and analytics remain dependencies | Resilience/security define disconnected envelope; CPDP-P01/P02 |
| AKS/KIC automatically creates HA and federation | scheduling, controllers and watched-resource aggregation create their own failure/blast radius | SRE/architecture approve AKS-P02/P04/P05 |
| Redis guarantees a hard global quota | documented Redis-disconnect fallback allows more aggregate requests | Risk/service owner sets acceptable degradation; KSEC-P03 |
| Enterprise plugin availability equals entitled/supported use | plugin pages/matrix are public product docs, not a purchase/support contract | Procurement/vendor manager supplies E2 matrix |
| Vendor benchmark equals RE-1 capacity | published method/environment differs from exact variant and workload | Performance board approves KPERF-P01–P05 |
| Declarative export equals backup/exit | database-native backup is primary and exports omit state/history/semantics | DR/architecture approve isolated restore and exit diff |
| More Kong detail is evidence of superiority | documentation depth is editorial scope, not observed fit | Comparative review applies the same proof/evidence ladder to all candidates |

## Validation status and evidence gaps

| Evidence layer | Status | Missing artifact |
|---|---|---|
| E1 official mechanism | Current as of 2026-08-18 | Revalidate at variant freeze; several pages are release/service volatile |
| E2 entitlement/support/privacy/SLA | Not obtained | quote/order, support matrix, DPA/location, SLA/remedy, audit/export, managed responsibility |
| E3 lab | Not run | KONG/CPDP/KVS/AKS/KSEC/KOPS/KOBS/KPERF/KDR proof bundles from docs 10–18 |
| E4 representative pilot/operations | Not run | estate workload, operator toil, incident/support, capacity/cost and migration evidence |

The next evidence action is not another feature list. It is to freeze `KP-SMH1` and the Konnect benchmark as exact option/BOM records, approve RE-1 and platform-outcome thresholds, add the decision-bearing proposed Kong and external-platform rows to `research/sources.csv` when promoted, and execute the existing dossier plus KPS proof plans with independent review.
