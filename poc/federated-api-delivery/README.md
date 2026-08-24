# Federated application programming interface (API) delivery reference

| Field | Value |
|---|---|
| Artifact type | public-safe executable proof-of-concept harness |
| Decision question | Can application teams own OpenAPI-first application programming interface (API) intent in their repositories while one central platform pipeline prevents policy weakening and remains the only Kong runtime writer? |
| Evidence state | Offline executable harness evidence for validation, deterministic composition, planning and supplied-active-snapshot drift detection; no decK, Kong Control Plane, Data Plane, Terraform or network execution |
| Reference case | Synthetic `orders-v1` application programming interface (API); all names, hosts, identities, routes and commits are invented documentation fixtures |
| As-of date | 2026-08-24 |
| Next gate | Run the same controls with a frozen Kong/decK bill of materials, a platform deployment identity, a reviewed decK diff and a captured active configuration |

## Answer first

This reference demonstrates the **governance seam**, not a deployed Kong outcome. An application repository can own OpenAPI, bounded Service/Route intent, owner/support metadata and behavior cases. A separately versioned central policy bundle supplies mandatory plugins and route rules. The offline compiler rejects missing owners, unsafe routes, prohibited or reserved plugins, expired exceptions and conflicting writers before producing a deterministic Kong candidate and review plan.

Only the platform pipeline may apply the result to a Kong Control Plane (CP). The application workflow never receives a Kong Admin application programming interface (API) credential and never copies centrally owned plugin configuration. Production evidence is complete only when it binds the application commit, central-policy version, generated configuration, reviewed decK diff or equivalent plan, target CP and active configuration digest.

The governing design is in the [Kong platform ownership matrix](../../docs/47-kong-enterprise-platform-strategy.md#federated-application-repository-delivery). Portal and consumer-application consequences are in [Developer portal and API products](../../docs/30-developer-portal-api-products.md#federated-api-publication-is-separate-from-consumer-application-access).

## Repository boundary

This application programming interface (API) reference separates producer-owned material from centrally owned policy and deployment authority:

```text
federated-api-delivery/
├── app/
│   ├── openapi.json             # producer-owned API contract
│   ├── api-intent.json          # bounded Kong Service/Route intent
│   ├── metadata.json            # durable owner, lifecycle and support references
│   └── tests.json               # operation and negative behavior cases
├── platform/
│   ├── policy-bundles/
│   │   └── baseline-2026-08-24.1.json
│   ├── exceptions.json          # centrally reviewed, time-bounded exceptions
│   ├── target.json              # approved lifecycle Control Plane and deployment writer
│   └── writer-registry.json     # one source writer per generated entity
├── fixtures/
│   └── current-empty.json       # synthetic current state for plan generation
├── tools/
│   └── federate.py              # standard-library validator/compiler/attestor
├── tests/
│   └── test_federate.py         # positive and fail-closed cases
└── Makefile
```

The OpenAPI document is encoded as JavaScript Object Notation (JSON), which OpenAPI permits, so the reference can run with Python's standard library and no YAML parser. Production teams may use YAML after the governed pipeline pins and runs an OpenAPI semantic validator.

## Ownership and write authority

| Layer | Source authority | Runtime writer | What is prohibited |
|---|---|---|---|
| OpenAPI, application programming interface (API) metadata and API-specific behavior cases | Application repository | None; these are inputs | Central edits that silently change domain semantics |
| Service/Route request | Application repository within central bounds | `platform:api-release` | Direct application write to a Control Plane (CP), unreserved host/path or unmanaged target |
| Mandatory authentication, correlation and telemetry profile | Central policy bundle | `platform:api-release` | Application copy, override, removal, version substitution or reserved-plugin declaration |
| Application-selectable plugin | Application repository from the central catalog | `platform:api-release` | Unlisted plugin or configuration outside the published bounds |
| Exception | Central exception ledger after independent review | Compiler applies only while valid | Exception to a non-exemptible control, missing compensating control, broad scope or expired lease |
| Active state | Target Control Plane | `platform:api-release`; break glass is separately leased | Unknown writer, unreviewed change or unreconciled drift |

Source ownership is therefore federated; deployment authority is not. `writer-registry.json` makes the source writer for each entity explicit, while `target.json` names the single platform deployment writer.

## Offline execution

From this directory:

```sh
make check
make demo
```

`make check` runs the positive composition case and negative cases for:

- missing ownership metadata;
- unsafe or wildcard routing;
- prohibited plugin selection;
- application attempts to own a mandatory plugin;
- conflicting source writers;
- expired exceptions;
- unapproved plan evidence; and
- active-configuration drift.

`make demo` writes ignored files under `.work/`:

| File | Meaning |
|---|---|
| `kong.json` | Deterministically composed application programming interface (API)-specific Kong declarative candidate |
| `provenance.json` | Entity-level application-versus-platform source authority |
| `deployment-plan.json` | Equivalent offline create/change/delete plan against the supplied current snapshot |
| `evidence-pending.json` | Evidence envelope with application commit, policy version, generated digest, target Control Plane (CP) and **pending** review/active fields |

The demo does not pretend that its plan was reviewed or deployed. A production pipeline must run a real decK validation/diff against the frozen target, record an approval for that exact plan digest, apply through the platform identity, capture active state, and then run `attest`:

```sh
python3 -I tools/federate.py attest \
  --root . \
  --generated .work/kong.json \
  --plan .work/deployment-plan.json \
  --pending-evidence .work/evidence-pending.json \
  --review approved-plan.json \
  --active active-kong-snapshot.json \
  --output release-evidence.json
```

The review record must contain `status: approved`, the exact plan Secure Hash Algorithm 256-bit (SHA-256) digest, reviewer role, review identifier, review time and target Control Plane. `attest` fails when the review is incomplete, the target differs or the API-scoped active digest does not equal the generated digest. The tests exercise this gate with temporary synthetic records; the repository contains no fabricated approval.

## Standard production pipeline

For an application programming interface (API) release:

1. **Validate producer input.** Run a pinned OpenAPI semantic validator, compatibility checks, metadata rules and the offline governance checks here.
2. **Compose centrally.** Resolve one writer per entity and combine the application commit with one immutable central policy bundle. Do not merge plugin files copied from the application repository.
3. **Validate the target candidate.** Run the frozen decK version's validation against the exact Kong edition, version and plugin schemas.
4. **Plan and review.** Produce a scoped decK diff or equivalent create/change/delete plan. The review binds the plan digest and named Control Plane (CP); it does not approve a moving branch.
5. **Deploy once.** A platform-owned workload identity applies the accepted candidate. Terraform remains the central owner for Control Plane/Data Plane infrastructure and deployment permissions; decK remains the declared writer for the governed Kong entity scope.
6. **Prove active state.** Capture the API-scoped active configuration, compare its digest, run outside-in routing/security cases, and store the native deployment receipt.
7. **Reconcile continuously.** Detect drift or another writer without silently rewriting evidence. Break-glass change expires and returns to the same source authority.

The immutable release evidence chain is:

```text
application commit
  + central policy version and digest
  + generated Kong configuration digest
  + reviewed plan/diff digest and decision
  + target Control Plane
  + native deployment receipt
  + active configuration digest
  + outside-in behavior results
```

## Exception contract

`platform/exceptions.json` is intentionally empty. A real record is admitted only when all of these fields are present and approved centrally:

- stable exception identifier and an explicitly exception-eligible control;
- exact application programming interface (API) scope;
- accountable owner and removal owner;
- reviewer role and `approved` status;
- expiry later than the policy bundle's as-of date;
- compensating controls and their test; and
- audit reference and closure result.

Mandatory authentication, traceability, sensitive-data and writer controls in this reference are non-exemptible. An exception cannot change the required plugin configuration; it can only authorize a bounded alternative for a rule the central bundle marks exception-eligible.

## Evidence boundary and limitations

- All values use reserved `.example.test` hosts and synthetic identifiers. They are not private topology or current-state evidence.
- The compiler validates the small reference schema, not all OpenAPI or Kong schemas. decK and exact-option schema validation remain mandatory.
- The offline plan is reviewable but is not a decK result. Its purpose is to make create/change/delete impact deterministic before the production adapter runs.
- Digest equality proves only that the supplied application programming interface (API)-scoped snapshot matches the generated candidate. It does not prove traffic, identity, availability, recovery, product entitlement or business correctness.
- Passing `make check` is harness execution evidence, not reproducible target lab evidence (E3), representative production-pilot evidence (E4), or production approval.
