# Findings and claim register

| ID | State | Claim | Sources | Organizational implication |
|---|---|---|---|---|
| F-001 | Confirmed | Kong hybrid separates configuration control planes from traffic-serving data planes and secures their connection with mTLS. | K-001,K-002,K-003 | Strong topology fit; validate allowed egress, residency, and certificate operations. |
| F-002 | Confirmed | Kong hybrid data planes keep serving cached configuration during CP loss, but changes cannot propagate. | K-001 | Define separate traffic/change SLOs and test restart/scale-out. |
| F-003 | Confirmed | Kong hybrid limits some plugin strategies and does not support its OAuth 2.0 plugin. | K-001 | Build authentication on enterprise IdP plus OIDC/JWT; test every critical plugin/topology. |
| F-004 | Confirmed | Kong KIC supports Gateway API, while unmanaged gateways merge routes handled by a controller into its external gateway deployment. | K-004,K-005 | Choose and document ownership/lifecycle model; do not assume automatic provisioning. |
| F-005 | Confirmed | decK gateway operations require an Admin API and cannot write DB-less gateways. | K-006 | Avoid incompatible API operations design and dual writers. |
| F-006 | Confirmed | APIM self-hosted gateway is a containerized hybrid runtime managed from Azure. | M-001,M-002 | APIM is a legitimate hybrid candidate, not a managed-only service. |
| F-007 | Confirmed | Customer owns self-hosted gateway hosting, capacity, uptime, and much Kubernetes/network troubleshooting. | M-003 | Compare operational/support burden honestly with Kong and Apigee. |
| F-008 | Confirmed | APIM workspace cannot currently associate with a self-hosted gateway. | M-004 | Potential blocker for combined federated-workspace plus workload-local gateway model. |
| F-009 | Confirmed | Apigee Hybrid keeps traffic in a customer-managed Kubernetes runtime while Google operates management services. | G-001 | Validate metadata/analytics residency and cross-cloud control dependency. |
| F-010 | Confirmed | Apigee Hybrid runtime includes Cassandra and MART alongside processors/synchronizer. | G-001,G-002 | Material platform operations and upgrade footprint to cost/test. |
| F-011 | Confirmed | DataWeave provides application-level data transformation; API Manager policies govern traffic. | MU-001,MU-002 | Mule replacement must split integration runtime from gateway migration. |
| F-012 | Confirmed | Gateway API is role-oriented and portable, but implementation-specific extensions remain vendor-specific. | K8S-001 | Use portable routing intent and track policy lock-in separately. |
| F-013 | Interpretation | Kong currently best matches the stated Kubernetes/hybrid hypothesis. | F-001–F-005 | Advance to PoC; do not award a final recommendation. |
| F-014 | Risk | Product documentation can change between assessment and procurement. | All | Revalidate volatile facts, versions, entitlements, limits, and support terms at each gate. |
