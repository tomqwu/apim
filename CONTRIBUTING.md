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

## Docs-first publication workflow

Every new study, guide, roadmap, comparison, or recommendation begins as a canonical Markdown document under `docs/` before it is projected into the site.

1. Write or revise the canonical document first. Substantive studies must satisfy [`docs/STUDY-STANDARD.md`](docs/STUDY-STANDARD.md), including point-of-use evidence, real-world failure analysis, proof gates, and article-owned figures.
2. Update [`docs/README.md`](docs/README.md) and any canonical roadmap or cross-reference that establishes the document's place in the study system.
3. Build the site from the committed document. Site cards, charts, audience routes, and presentation scenes summarize or render the canonical argument; they must not become a competing source of facts, recommendations, counts, or roadmap status.
4. Keep each diagram or chart inside the study that uses it. The Visual Atlas and presentation mode are secondary indexes and projections, not substitutes for the article.
5. Run `make validate`, inspect the rendered article and presentation at desktop and phone widths, and confirm generated counts and links before committing.

A site-only study, guide, diagram, recommendation, or roadmap is incomplete and must not be published.

## Document conventions

- **Confirmed:** directly supported by authoritative evidence.
- **Interpretation:** reasoned consequence of confirmed facts.
- **Assumption:** missing organization or vendor input that must be verified.
- **Risk:** uncertain event with material impact.
- **Recommendation:** proposed action, not an established fact.
- **Open question:** explicit discovery item with an owner and decision date.
