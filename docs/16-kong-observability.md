# Kong observability

## Minimum telemetry

- Request rate, status, gateway/upstream latency, bytes, retries, connection state, rate-limit decisions, authentication failures, and route/service/consumer identity at controlled cardinality.
- CP/DP connectivity, last configuration hash/time, certificate expiry, telemetry queue/drop, pod restart, saturation, and availability.
- Trace context propagation with W3C headers and correlation ID returned to clients.
- Structured logs with no tokens, credentials, account identifiers, or unrestricted payloads.

## Design

Use Prometheus-compatible metrics and OpenTelemetry to feed enterprise-standard platforms. The collector is a policy boundary for batching, redaction, sampling, enrichment, buffering, and fan-out. Validate failure/backpressure behavior; observability must not take down the request path.
