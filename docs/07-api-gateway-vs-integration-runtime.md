# API gateway versus integration runtime

| Concern | Gateway default | Integration/domain default | Exception test |
|---|---:|---:|---|
| TLS, JWT validation, API key, rate limit, header controls | Yes | No | Identity provider owns token issuance |
| Small deterministic header/query rewrite | Yes | No | Reject if logic becomes domain-specific |
| Schema/threat validation | Yes | Sometimes | Large payload/streaming cost must be measured |
| Endpoint routing and bounded retries/timeouts | Yes | Sometimes | Never multiply retries across layers blindly |
| Complex JSON/XML/DataWeave transformation | No | Yes | Tiny compatibility shim must have retirement date |
| Multi-step orchestration/compensation | No | Yes | None |
| Queue/event/file/batch processing | No | Yes | Gateway may initiate but not execute workflow |
| Business authorization/decisioning | Coarse enforcement | Yes | External policy engine may decide |
| Long-lived state and idempotency ledger | No | Yes | Gateway only propagates idempotency key |

## Policy complexity guardrail

Reject a gateway implementation when it introduces domain branching, persistent state, multi-backend transaction logic, opaque embedded scripts, or a deployment cadence tied to business application releases. Route that capability to a domain or integration service.
