# Performance and resilience comparison

Apply an identical workload model and policy chain to each variant. Report gateway-added latency, throughput, errors, saturation, recovery, and cost at representative steady, peak, burst, soak, and degraded states.

Failure tests cover pod/node/zone/region, control-plane connectivity, configuration store, shared counter store, DNS, PKI, identity, telemetry, load balancer, backend, and operator error. Retries must be bounded by one end-to-end budget and tested for non-idempotent operations.
