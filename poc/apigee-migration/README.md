# Apigee-to-Kong migration evidence harness

This public-safe harness makes proof records `APIG-M01` through `APIG-M04` mechanically checkable. It does **not** connect to Apigee or Kong, convert a proxy, execute a migration, or establish parity. Every protocol remains **Not run** until a separately authorized execution supplies exact source and target options, raw artifacts, measurements, and an independent review.

## What is executable

[`validate_evidence.py`](validate_evidence.py) validates a produced evidence bundle against the objective thresholds and artifact requirements in [`protocols.json`](protocols.json). It fails when:

- the source or target option is not exact;
- a required measurement is missing or outside its threshold;
- a required artifact is absent, escapes its evidence directory, is symlinked, or has the wrong Secure Hash Algorithm 256-bit (SHA-256) digest;
- the candidate revision is not a full Git commit identifier;
- the execution timestamp is not a timezone-qualified Coordinated Universal Time (UTC) value; or
- the review is missing, non-independent, or not a pass.

The repository validation runs only the harness self-test:

```sh
python3 -I poc/apigee-migration/validate_evidence.py --self-test
```

That command uses synthetic in-memory records to prove that each protocol accepts its threshold boundary and rejects one deliberate violation. Its success is evidence about the validator, not about either product or a migration.

## Validate a governed execution bundle

Place the execution record and its referenced artifacts in one controlled directory, then run:

```sh
python3 -I poc/apigee-migration/validate_evidence.py \
  --evidence /path/to/controlled-evidence/APIG-M02.json
```

The evidence JSON must contain:

- `schemaVersion`, `protocolId`, `evidenceState`, `exactSourceOption`, and `exactTargetOption`;
- `executedAtUtc` and the 40-character `candidateRevision` tested;
- every protocol-specific measurement;
- every required artifact, with a relative path and SHA-256 digest; and
- an independent reviewer role, independence flag, disposition, and review URL.

Raw evidence can contain restricted information and therefore belongs outside this public repository. Only sanitized conclusions and controlled artifact identifiers may be published.

## Protocol boundary

| Protocol | Decision gate | Objective pass boundary | Current state |
|---|---|---|---|
| `APIG-M01` | Source denominator and dependency closure | 100% required inventory coverage; zero unexplained or unowned active objects; all shared cut sets reviewed | Not run |
| `APIG-M02` | Representative semantic and authorization parity | 100% required corpus coverage; zero unaccepted critical variance, unauthorized success, or unexplained state divergence | Not run |
| `APIG-M03` | Bounded coexistence and route-back | Zero orphan credentials, ambiguous business outcomes, unreconciled state records, or evidence-continuity gaps; route-back meets the approved objective | Not run |
| `APIG-M04` | Dependency-zero retirement | Zero unresolved dependencies and every closure or retained-boundary decision independently approved | Not run |

The canonical interpretation, mapping, gates, and limitations remain in the [Apigee migration strategy](../../docs/50-apigee-migration-strategy.md).
