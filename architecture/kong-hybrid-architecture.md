# Kong hybrid reference architecture

- Konnect or self-managed control plane is selected through residency, operations, support, and TCO evidence.
- Data-plane groups are isolated by environment and trust/failure domain, with two or more replicas and no public Admin API.
- CP/DP configuration and telemetry connections use mTLS; data-plane egress is allow-listed.
- Redis is introduced only where global/distributed policy semantics require it and is failure-tested.
- KIC/Gateway API owns Kubernetes routes; decK/Terraform/API ownership is partitioned to avoid conflicting writers.
- Logs, metrics, traces, configuration identity, certificate expiry, and sync health feed enterprise controls.
