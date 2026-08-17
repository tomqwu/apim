# Kong API operations

## Promotion flow

OpenAPI lint → ownership/security metadata → route/policy render → schema/config validation → policy tests → ephemeral gateway smoke → security tests → approval → signed artifact → controlled promotion → runtime verification → evidence capture.

## Guardrails

- Exactly one authoritative writer per gateway/control plane.
- Environment overlays contain references, never secrets.
- Diff must be reviewed before synchronization; destructive drift correction requires approval.
- Production uses immutable commit/artifact identity and records actor, approver, time, diff, and outcome.
- Rollback is tested as a first-class operation, not assumed from Git history.
- Emergency changes expire and are reconciled back to source.

Kubernetes routes use Gateway API/KIC; non-Kubernetes control planes may use decK or the Konnect API. Mixing them on the same entities is prohibited unless ownership boundaries are machine-enforced.
