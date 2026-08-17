# Security tests

- Missing, malformed, expired, wrong issuer/audience/algorithm/scope token.
- API key/certificate issue, rotation, expiry, revocation, and cross-tenant use.
- Client and upstream mTLS trust, SNI, expiry, revoked CA, and rotation.
- Oversized body/header/URL, wrong content type, invalid schema, malformed encodings, request smuggling and injection test corpus.
- Admin/status/metrics/debug access from unauthorized networks and identities.
- Secret and sensitive-field leakage through logs, traces, metrics, errors, config export, and support bundle.
- Image/plugin signature, SBOM, CVE gate, non-root/restricted runtime, RBAC and NetworkPolicy tests.
- Identity/secrets/PKI unavailable: verify approved fail-safe behavior.

Use approved security tooling and synthetic payloads in an isolated environment.
