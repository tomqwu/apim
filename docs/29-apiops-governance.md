# API operations and governance

## Federated model

- Platform team owns gateway classes, shared infrastructure, mandatory controls, schemas, templates, guardrails, evidence, and support.
- Domain teams own API contracts, implementation, non-mandatory route policy, SLOs, consumer documentation, and lifecycle.
- Security owns control objectives and exceptions; operations owns production health and incident response.

Required pipeline checks include ownership, versioning, breaking change, style, security scheme, sensitive-data metadata, route collision, policy compatibility, secret detection, configuration validation, test evidence, approvals, signed artifacts, promotion, and rollback.
