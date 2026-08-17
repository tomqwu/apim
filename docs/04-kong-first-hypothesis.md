# Kong-first hypothesis

## Hypothesis

Kong is likely to fit the target state better than a cloud-bound managed gateway because it can place Kubernetes-native data planes close to cloud, on-premises, transitional legacy, or future workloads while centralizing policy and lifecycle control.

## Supporting evidence to validate

- CP/DP request-path isolation and disconnected operation.
- Kubernetes Gateway API and declarative API operations fit.
- Consistent policy behavior across data-plane locations.
- Performance, footprint, autoscaling, and upgrade characteristics.
- Ability to integrate with enterprise identity, PKI, secrets, SIEM, APM, and network controls.
- Delegation model without control-plane sprawl.

## Falsification conditions

The hypothesis fails or requires redesign if any mandatory security/residency gate fails; critical plugins do not work in the chosen topology; disconnected behavior cannot meet RTO/RPO; operational burden exceeds benefit; portal/governance needs require unacceptable custom work; vendor support is inadequate; TCO is not justified; or Mule migration causes gateway-policy overreach.

## Known constraints from current Kong documentation

- Hybrid data planes use cached configuration when disconnected, but cannot receive updates.
- Some rate-limiting strategies are unavailable in hybrid mode; Redis or local strategy design must be intentional.
- Kong's OAuth 2.0 plugin is incompatible with hybrid mode; prefer an external authorization server and JWT/OIDC validation pattern.
- Custom plugins must be installed on both planes and create lifecycle/support burden.
- decK gateway commands require the Admin API and cannot write to DB-less gateways.

These are design inputs, not footnotes.
