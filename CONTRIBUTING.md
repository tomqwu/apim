# Contributing

## Safety and evidence

- Use synthetic data only. Never commit client records, credentials, private hostnames, tenant identifiers, certificates, or proprietary vendor material.
- Label claims with their evidence state and record official sources in `research/sources.csv`.
- Keep unexecuted capabilities as `not-tested` or `unknown`; an example configuration is not test evidence.
- Update the access date and revalidate volatile claims before a decision gate.

## Change workflow

1. Open an issue or ADR for material architecture changes.
2. Keep OpenAPI, gateway configuration, Kubernetes resources, tests, and documentation synchronized.
3. Run `make validate`; run the relevant PoC target when runtime behavior changes.
4. Attach sanitized evidence to the review and record the test environment.
5. Require platform, security, architecture, and service-owner approval for production policy changes.

## Document conventions

- **Confirmed:** directly supported by authoritative evidence.
- **Interpretation:** reasoned consequence of confirmed facts.
- **Assumption:** missing organization or vendor input that must be verified.
- **Risk:** uncertain event with material impact.
- **Recommendation:** proposed action, not an established fact.
- **Open question:** explicit discovery item with an owner and decision date.
