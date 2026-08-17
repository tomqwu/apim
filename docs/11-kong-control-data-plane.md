# Kong control-plane/data-plane design

## Proposed test topology

- One logically isolated control plane per lifecycle/security boundary unless evidence justifies more.
- At least two data-plane replicas per production failure domain.
- Data-plane-initiated mTLS connectivity through allow-listed egress; no inbound management path from SaaS.
- Local readiness/liveness and cached configuration; a tested fallback configuration only for approved emergency recovery.
- Separate configuration and telemetry monitoring, including last sync, hash, certificate expiry, and dropped telemetry behavior.

## Failure matrix

| Failure | Expected behavior | Required evidence |
|---|---|---|
| Control plane unavailable | Existing data planes continue with cached config; changes stop | Traffic, restart, sync-age logs |
| Data-plane replica fails | Load balancer removes it; remaining capacity meets SLO | Failure injection and latency |
| CP/DP certificate expires | Connection fails safely with advance alert | Rotation/revocation test |
| Configuration error | Admission/validation blocks, or promotion rolls back | Pipeline and runtime evidence |
| Telemetry destination fails | Request processing continues within approved buffer/drop policy | Backpressure and loss evidence |

Control-plane outage survival is not equivalent to change-plane availability; both require SLOs.
