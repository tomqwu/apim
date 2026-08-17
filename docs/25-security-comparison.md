# Security comparison

Score with negative tests and operational evidence, not feature presence.

| Domain | Required proof |
|---|---|
| Admin identity | SSO/MFA, granular RBAC, service identity, emergency access, audit |
| Client identity | OAuth/OIDC/JWT, mTLS, key lifecycle, revocation, clock/algorithm checks |
| Authorization | scope/claim enforcement, policy externalization, least privilege |
| TLS/PKI | inbound/upstream/plane TLS, CA trust, rotation, revocation, expiry alert |
| Threat protection | sizes, schemas, content types, malicious payloads, resource exhaustion |
| Secrets | external secret manager/workload identity, no export/log leakage |
| Supply chain | SBOM, signing, CVE response, plugin provenance, patch SLA |
| Audit/privacy | immutable admin/config/access evidence, redaction, retention, residency |
| Tenant isolation | control/runtime blast radius, quotas, noisy-neighbor tests |
| Incident response | forensic evidence, kill/revoke, rollback, vendor escalation |

Mandatory failures cannot be compensated by product features elsewhere.
