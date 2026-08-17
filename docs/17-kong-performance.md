# Kong performance engineering

Synthetic results are not capacity commitments. Test representative request mixes, auth/policy chains, payload sizes, keep-alive, TLS, upstream latency, error rate, and telemetry.

## Required outputs

- Environment, image/chart/plugin versions, nodes, CPU/memory, replicas, autoscaling, network path, upstream behavior, and exact configuration.
- Throughput plus p50/p95/p99/p99.9 latency, error rate, saturation, connection reuse, and resource use.
- Baseline backend versus gateway-added latency.
- Soak, burst, cold start, scale-out lag, zone loss, Redis/control/telemetry failure, and recovery results.

Capacity target: steady-state production peak at an agreed utilization ceiling while losing the largest allowed failure unit, with headroom documented.
