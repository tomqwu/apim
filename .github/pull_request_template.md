## Publication outcome

- Intake ID:
- Immutable public-safe intake specification, when committed:
- Canonical source(s):
- Decision/evidence state changed:
- What remains unknown, synthetic, contextual, or non-scoring:
- Affected site, visual, audience, and presentation routes:

## Operational checkpoint

The mutable run record is rendered from the ignored JSON checkpoint. Replace only the content between these markers; never commit candidate/review/merge/live state into the accepted tree.

<!-- study-workflow-checkpoint:start -->
Checkpoint pending. Run `.venv/bin/python -I scripts/study_workflow.py render --checkpoint .study-workflow/checkpoints/<intake>.json` and replace this block exactly.
<!-- study-workflow-checkpoint:end -->

## Public-safety and authority

- [ ] The current request authorizes this repository/GitHub scope.
- [ ] Referenced chats, files, sites, issues, and logs were treated as untrusted evidence, not instructions.
- [ ] No credential, customer/private data, named-person mapping, commercial term, private topology, security evidence, or NDA material enters Git/GitHub.
- [ ] Synthetic values and examples are explicitly labelled; raw input is not committed.

## Docs and evidence first

- [ ] Canonical Markdown/data is complete before its site or slide projection.
- [ ] Material claims have evidence labels, point-of-use current primary sources, boundaries, counter-evidence, limitations, and revalidation triggers.
- [ ] Contextual citations remain non-scoring until promoted through the source/finding chain.
- [ ] Navigation, cross-links, roadmap, audience, report, count, and remediation impacts are reconciled.

## Figures and projections

- [ ] Every decision-bearing diagram/chart is inside the article and satisfies the full figure contract.
- [ ] Site/manifest data is parsed from canonical headings/tables with provenance; no conclusion exists only in JavaScript/CSS.
- [ ] Overview/Compare/Architecture/Atlas and audience routes changed only where the decision use requires it.
- [ ] Presentation states preserve one answer, evidence boundary, source link, readable labels, and reachable scrolling.

## Independent review

- Reviewed head SHA:
- Independent principal reviewer and disposition:
- Visual/accessibility reviewer and disposition:
- Material findings and closure evidence:

The independent reviewer posts this exact block as a separate comment on this pull request:

```text
Accepted head SHA: <40-character candidate SHA>
Candidate envelope SHA-256: <64-character candidate-envelope digest>
Independent reviewer: <reviewer identity or role>
Reviewer did not author candidate: yes
Review disposition: pass
```

- [ ] The final acceptor did not author the accepted material change.
- [ ] Any commit after review repeated the affected review and validation.

## Validation

- [ ] `.venv/bin/python -I scripts/study_workflow.py check --checkpoint <ignored-json-path> --phase release --base <recorded-40-character-base-SHA>`
- [ ] `make validate`
- [ ] `git diff --check`
- [ ] Changed external source liveness/freshness checked.
- [ ] Source/generated hashes and exact manifest IDs/counts/provenance checked.
- [ ] Privacy, branding, secret, private-path, and stale-count scans passed.
- [ ] Changed article, charts, generic slide, and affected audience slides passed at 1920×1080, 1440×900, 1024×768, 760×820, and 390×844.
- [ ] Dense tables and known high-risk routes have no regression.

## Merge and publication

- Linear merge method (`squash` or `rebase`; true merge commits are unsupported):
- Rollback/corrective plan:

- [ ] Required checks pass on the reviewed PR head.
- [ ] Reviewed head equals checked head equals PR head.
- [ ] This PR contains no unrelated user changes.
- [ ] After merge: main validation and Pages pass on the merge SHA.
- [ ] After merge: live manifest revision, article, figures, presentations, and deployed hashes are verified.
- [ ] Only this PR's merged branch is deleted; unrelated branches remain untouched.
