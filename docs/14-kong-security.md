# Kong security assessment

## Control families

- **Identity:** external IdP token issuance; JWT/OIDC validation, issuer/audience/expiry/skew/algorithm controls; mTLS for high-trust clients; separate admin identity.
- **Authorization:** coarse scopes/claims at gateway, domain decisions downstream, policy-as-code where justified.
- **Transport:** TLS baseline, trusted CA lifecycle, upstream TLS/SNI, CP/DP mTLS, certificate inventory and rotation.
- **Threat protection:** size/time limits, schema/content-type validation, injection testing, rate/connection limits, WAF division of responsibility.
- **Secrets:** no literals in manifests; approved secret manager, short-lived workload identity, rotation evidence.
- **Supply chain:** pinned images/charts, signatures/SBOM/CVE gates, plugin provenance, emergency patch path.
- **Audit/privacy:** immutable configuration/audit records, payload minimization, field redaction, retention, access controls, SIEM detection.

OIDC and enterprise request validation are architecture backlog items until licensed execution evidence is captured. The OSS PoC uses key-auth only to exercise a negative/positive authentication path.
