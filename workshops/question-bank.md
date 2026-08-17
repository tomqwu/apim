# Enterprise API platform workshop question bank

> 180 questions across nine workshops. Assign an owner, evidence reference, and due date to every question selected for the assessment. Answers without evidence remain provisional.

## Current state and Mule/PCF

Q-001. What business outcomes and deadlines drive this assessment?

Q-002. What does PCF mean in the current estate and which foundations, spaces, and routes remain?

Q-003. Which Mule applications APIs flows and shared domains exist by environment?

Q-004. Who owns each Mule workload and who supports it after hours?

Q-005. Which workloads are gateway-only versus transformation orchestration messaging batch file or connector heavy?

Q-006. Which DataWeave modules contain canonical or business rules?

Q-007. Which Mule policies contracts consumers and credentials are attached to each API?

Q-008. What are the transaction volumes payload sizes latency percentiles and seasonal peaks?

Q-009. What incidents capacity constraints and recurring manual tasks occur today?

Q-010. Which Mule and PCF versions are in use and what are their support deadlines?

Q-011. Which backends consumers certificates queues databases and SaaS systems depend on each workload?

Q-012. Which workloads are stateful or require idempotency reconciliation and compensation?

Q-013. Which APIs can be retired merged or replaced by SaaS-native capabilities?

Q-014. What current costs include licenses infrastructure support partners and internal staffing?

Q-015. Which deployment promotion rollback and emergency-change practices exist?

Q-016. What audit data and runtime logs are required and where are gaps today?

Q-017. Which PCF applications will move to AKS and in what dependency order?

Q-018. Which existing routes or consumer contracts cannot change during migration?

Q-019. What evidence is required to declare a Mule or PCF component decommissioned?

Q-020. Which two representative workloads should be used for gateway-heavy and integration-heavy pilots?

## Hybrid cloud and target architecture

Q-021. Which regions clouds data centres and network zones must host gateway data planes?

Q-022. Which traffic classes are external partner internal privileged or machine-to-machine?

Q-023. Which request payloads, metadata, configuration, analytics, or support data may leave approved regions?

Q-024. What control-plane and request-path SLOs must be defined separately?

Q-025. What RTO and RPO apply to traffic configuration administration portal analytics and audit?

Q-026. Must data planes start or scale while disconnected from the management plane?

Q-027. How long may a data plane operate on stale configuration?

Q-028. Which management telemetry identity PKI DNS registry and time-service egress paths are allowed?

Q-029. What stable hostname and edge-routing strategy will hide backend movement?

Q-030. Where are WAF DDoS CDN load balancing and TLS termination responsibilities placed?

Q-031. Which north-south and east-west flows belong at the enterprise gateway?

Q-032. How many independent failure domains and trust zones are required?

Q-033. How will configuration remain consistent across data-plane groups?

Q-034. How will a second region be promoted and how quickly must clients converge?

Q-035. Which traffic or metadata must stay within an enterprise-controlled runtime?

Q-036. How will on-premises PCF Mule legacy and SaaS backends be reached privately?

Q-037. What is the exit path if the SaaS control plane or vendor is no longer acceptable?

Q-038. Which parts of routing policy and API contracts must remain portable?

Q-039. What shared services could create cross-region or cross-cloud coupling?

Q-040. Which failure scenarios must be demonstrated before architecture approval?

## Security IAM privacy and compliance

Q-041. Which identity providers issue tokens to customers staff partners and workloads?

Q-042. Which OAuth grants issuers audiences scopes claims algorithms and lifetimes are approved?

Q-043. Where is mTLS mandatory and which PKI owns issuance rotation and revocation?

Q-044. How are administrator SSO MFA RBAC privileged access and break-glass controlled?

Q-045. Can gateway workloads use workload identity instead of stored credentials?

Q-046. Which secret manager key vault and certificate-delivery patterns are approved?

Q-047. Which payload sizes schemas content types and threat controls are mandatory?

Q-048. Where does business authorization execute and what coarse decisions may the gateway enforce?

Q-049. Which fields tokens headers and identifiers must be redacted from logs and traces?

Q-050. What audit events must be immutable and how long are they retained?

Q-051. What encryption key residency ownership and rotation requirements apply?

Q-052. What software signing SBOM vulnerability and patch-time objectives apply?

Q-053. Are custom or third-party plugins allowed and what review process governs them?

Q-054. Which tenant isolation and noisy-neighbour controls are required?

Q-055. How are consumer keys applications subscriptions and certificates approved and revoked?

Q-056. What security evidence must vendors provide for SaaS runtime and support access?

Q-057. How are data subject privacy retention deletion and support-bundle requirements handled?

Q-058. What fail-open or fail-closed behavior is required when identity or policy dependencies fail?

Q-059. Which penetration abuse and negative tests are mandatory for the PoC?

Q-060. What conditions would immediately disqualify a deployment variant?

## Networking and platform

Q-061. What is the target AKS version region topology node pool and network plugin?

Q-062. Which ingress internal-load-balancer and private-link patterns are approved?

Q-063. What DNS zones resolvers split-horizon rules and failover controls apply?

Q-064. Which firewalls proxies NAT gateways and egress allow lists are in the path?

Q-065. Must the original client IP be preserved and which proxy headers are trusted?

Q-066. What TLS versions ciphers SNI and custom CA trust requirements apply?

Q-067. Which HTTP versions gRPC WebSocket streaming or non-HTTP protocols are required?

Q-068. What connection keep-alive pooling timeout and maximum-request limits are needed?

Q-069. Which backends use private endpoints overlapping addresses or asymmetric paths?

Q-070. How will health readiness and endpoint removal integrate with load balancers?

Q-071. What Kubernetes RBAC namespace and tenancy boundaries map to platform and domain teams?

Q-072. What Pod Security NetworkPolicy admission and image-registry controls are mandatory?

Q-073. What topology spread anti-affinity disruption and graceful-shutdown controls are required?

Q-074. Which metrics drive autoscaling and what scale-out time is acceptable?

Q-075. How are gateway and controller upgrades coordinated with AKS upgrades?

Q-076. Are service meshes present and where must gateway and mesh responsibilities meet?

Q-077. Who supports CNI DNS firewall load balancer and controller failures end to end?

Q-078. What network test environment can represent PCF on-premises and partner paths?

Q-079. How will packet captures and diagnostic bundles be sanitized?

Q-080. Which network dependencies must be included in resilience game days?

## API lifecycle developer experience and governance

Q-081. Who may create approve publish change deprecate and retire an API?

Q-082. What OpenAPI style versioning compatibility and documentation standards apply?

Q-083. How is API ownership and data classification made machine-readable?

Q-084. Which breaking-change checks and consumer communication periods are required?

Q-085. What API product plan subscription and entitlement models exist?

Q-086. What differs across internal partner open-banking and public developer journeys?

Q-087. How do developers discover request access and receive credentials safely?

Q-088. Which approvals terms sandbox and onboarding integrations are required?

Q-089. How are consumer applications owners contacts and credential expiry tracked?

Q-090. What portal SSO branding accessibility language and custom-domain requirements apply?

Q-091. How are APIs delegated to domains while mandatory policy remains centrally enforced?

Q-092. What reusable templates examples SDKs and mock environments are expected?

Q-093. How are duplicate APIs zombie versions and unused products detected?

Q-094. Which catalog or enterprise architecture systems must integrate?

Q-095. How are product usage adoption latency errors and consumer experience measured?

Q-096. What emergency lifecycle operations can bypass normal workflow and for how long?

Q-097. How are policy exceptions approved monitored and expired?

Q-098. What metadata must be exportable for vendor exit or disaster recovery?

Q-099. What onboarding lead time and platform service SLO should be targeted?

Q-100. Which two complete developer journeys must each vendor demonstrate?

## API operations observability and SRE

Q-101. Which Git platform pipeline engine and artifact registry are standards?

Q-102. Which source is authoritative for routes policies contracts and consumers?

Q-103. How are configuration diff validation promotion approval and rollback performed?

Q-104. How will concurrent writers and out-of-band portal changes be prevented?

Q-105. Which evidence links commit artifact deployment actor approver and runtime state?

Q-106. What functional policy security performance and contract tests gate promotion?

Q-107. How are secrets referenced across environments without entering source or artifacts?

Q-108. What dashboards cover request rate errors latency and upstream versus gateway time?

Q-109. Which log fields and trace attributes are required at controlled cardinality?

Q-110. How is W3C trace context propagated through gateway services and integration runtimes?

Q-111. Which control-plane data-plane sync version and certificate signals are alerted?

Q-112. How do telemetry pipelines buffer sample redact and degrade during failure?

Q-113. What SLO burn-rate saturation anomaly and security alerts page operators?

Q-114. How are tenant teams restricted to their own logs metrics and configuration?

Q-115. Which operational runbooks are mandatory before production onboarding?

Q-116. How are upgrades canaries rollback and fleet version drift managed?

Q-117. What incident command vendor escalation and evidence preservation processes apply?

Q-118. What diagnostic data can be shared with vendors and how is it approved?

Q-119. How will capacity forecasts and per-API unit costs be calculated?

Q-120. What quarterly controls and disaster-recovery evidence must the platform produce?

## Performance resilience and disaster recovery

Q-121. What representative traffic mix concurrency payload and policy chain should be tested?

Q-122. What p50 p95 p99 p99.9 latency and error targets apply?

Q-123. What steady peak burst and growth throughput must be supported?

Q-124. What utilization headroom is required while one failure unit is lost?

Q-125. How long must soak tests run and which leaks or degradation signals matter?

Q-126. How quickly must autoscaling react without causing connection or latency instability?

Q-127. What happens when a gateway pod node zone cluster or region fails?

Q-128. What happens when the management or configuration endpoint is unreachable?

Q-129. Can existing data planes restart and can new replicas start while disconnected?

Q-130. What happens when DNS identity PKI secrets registry time or telemetry fails?

Q-131. What happens when a shared Redis or counter store is slow partitioned or unavailable?

Q-132. How are retry budgets coordinated across client edge gateway service and integration layers?

Q-133. Which non-idempotent payment or transfer operations require idempotency controls?

Q-134. How are configuration errors detected contained and rolled back?

Q-135. What backup content encryption frequency retention restore and testing apply?

Q-136. What evidence proves configuration and consumer state consistency after recovery?

Q-137. How are analytics or audit gaps reconciled after a prolonged disconnection?

Q-138. Which manual recovery dependencies create unacceptable RTO risk?

Q-139. How frequently will node zone and region game days run?

Q-140. What objective abort and pass criteria govern every failure test?

## Mule migration factory and PCF-to-AKS transition

Q-141. What taxonomy will classify every Mule responsibility and migration destination?

Q-142. Which golden input output and side-effect tests capture current behavior?

Q-143. How will stable gateway routes be introduced without consumer changes?

Q-144. What distinguishes a simple gateway transformation from code that must move to a service?

Q-145. Which workflow messaging batch file and connector patterns need target platforms?

Q-146. How are retries idempotency ordering replay and compensation preserved?

Q-147. How will Mule-hosted backends coexist behind the new gateway?

Q-148. How will PCF and AKS backends receive weighted or reversible traffic?

Q-149. What shadow traffic or dual-run patterns are safe for banking workloads?

Q-150. How are consumer credentials subscriptions quotas and analytics migrated?

Q-151. What data reconciliation proves no transactions were lost or duplicated?

Q-152. What cutover monitoring and abort thresholds are required?

Q-153. How long may rollback routes remain and who authorizes their removal?

Q-154. Which shared Mule domains connectors or libraries block workload retirement?

Q-155. How are environment certificates firewall rules DNS and schedules decommissioned?

Q-156. What artifacts templates automation and training form the migration factory?

Q-157. How will wave complexity capacity risk and business value be prioritized?

Q-158. What production-readiness criteria must each migrated workload meet?

Q-159. What evidence closes licenses infrastructure support and data-retention obligations?

Q-160. How are benefits incidents lead time and technical-debt burn-down measured?

## Vendor product commercial and decision

Q-161. Which exact product edition topology version and entitlement is being proposed?

Q-162. Which features in the demonstration are preview licensed separately or topology-limited?

Q-163. What data categories and telemetry reach vendor-operated services and regions?

Q-164. What availability support response and service-credit commitments are contractual?

Q-165. Which Kubernetes versions platforms and upgrade windows are supported?

Q-166. What customer responsibilities fall outside normal vendor support?

Q-167. How are CVEs advisories emergency patches and end-of-support communicated?

Q-168. What are licensing meters overages nonproduction DR and growth assumptions?

Q-169. What three-to-five-year costs include infrastructure people support and migration?

Q-170. What price protection renewal and audit provisions apply?

Q-171. What product roadmap dependencies could materially affect the target architecture?

Q-172. How are configuration products consumers credentials analytics and audit exported?

Q-173. What exit assistance data deletion and post-termination access are contractual?

Q-174. Which subprocessors support locations and privileged-access controls apply?

Q-175. What comparable customers operate the proposed topology under financial controls?

Q-176. What hands-on vendor support will be provided for the PoC and first migrations?

Q-177. Which mandatory requirements cannot be met today and what workaround is proposed?

Q-178. Which claims can be demonstrated under failure rather than only in a presentation?

Q-179. What evidence would the vendor accept as a product defect or SLA breach?

Q-180. What facts should cause the organization to choose a competitor instead?

## Capture fields

For each answer record: `question_id`, `owner`, `answer`, `evidence_state`, `evidence_reference`, `decision_impact`, `follow_up`, and `due_date`.
