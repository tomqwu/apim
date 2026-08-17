# Kong-first hypothesis

## Hypothesis

Kong Konnect hybrid and self-managed Kong are **low-confidence priority-validation hypotheses** because they can place Kubernetes-native data planes close to cloud, on-premises, transitional legacy, or future workloads while centralizing policy and lifecycle control.

This is not evidence that Kong outperforms Azure APIM self-hosted gateway or Apigee Hybrid, both of which are legitimate hybrid alternatives. All seven exact variants receive the same E1/E2 screen before the approved finalists receive symmetric E3 PoCs.

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

## Counter-hypotheses to test

- **Azure APIM may be the better fit** if Azure-native integration, managed-service accountability, commercial alignment, and operational simplicity outweigh self-hosted workspace, topology, and feature constraints.
- **Apigee may be the better fit** if its API-product lifecycle, policy, analytics, and enterprise governance advantages justify the Kubernetes runtime footprint, Google-hosted management dependency, and support model.
- **Retaining MuleSoft may be the prudent near-term baseline** if migration risk, embedded integration logic, contract position, or staffing makes platform change uneconomic before decomposition evidence exists.
- **No current finalist may be acceptable** if mandatory residency, security, support, operability, or exit gates fail.
