# Migration patterns

1. Gateway policy parity.
2. Stable facade plus backend relocation.
3. Extract complex transformation into a stateless service.
4. Extract orchestration into domain/workflow capability.
5. Replace queue/event adapters with approved messaging integration.
6. Replace scheduled/batch/file flows with jobs or managed transfer.
7. Retain connector-heavy Mule flow temporarily behind the gateway.
8. Retire unused APIs after consumer and traffic proof.

Each pattern requires golden tests, observability, security controls, capacity, runbook, cutover, rollback, reconciliation, and retirement evidence.
