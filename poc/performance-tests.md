# Performance tests

Run k6 profiles for smoke, steady, peak, burst, soak, and degraded states. Parameterize RPS/concurrency, operation mix, payload, auth/policy chain, upstream delay/error, duration, and thresholds. Record gateway-added p50/p95/p99/p99.9, error rate, CPU/memory, saturation, scaling lag, and cost inputs.

Never publish results without environment and exact versions/configuration. The starter script is `load-testing/k6/smoke.js`.
