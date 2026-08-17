# Failure tests

Inject gateway pod, node, zone, backend, DNS, control-plane, telemetry, identity, secret, certificate, and shared counter-store failures. For each: define steady state, hypothesis, blast radius, guardrail/abort, injection, observations, recovery, SLO/RTO result, audit gaps, and follow-up.

Control-plane disconnection must distinguish existing traffic, running replica restart, new replica provisioning, configuration change, telemetry, license/certificate expiry, and reconnection.
