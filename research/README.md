# Research register

`sources.csv` is the authoritative register for sources attached to decision-bearing findings. `findings.md` maps those material conclusions to source IDs and distinguishes fact from interpretation. Principal studies can cite additional official context at the exact claim; an unregistered citation remains supporting context and must be promoted into `sources.csv` and mapped to a finding before it can affect scoring or a recommendation. Vendor notes summarize assessment implications but do not replace the linked documentation.

Research defaults to current official documentation. Revalidate time-sensitive rows before product selection, procurement, or production design.

The generated [external citation coverage report](../reports/source-coverage.md) and [usage ledger](../reports/source-coverage.csv) expose every article citation as `registered` or `contextual`. CI rejects drift between the corpus and those artifacts. This prevents an unregistered point-of-use link from silently becoming score-capable evidence while avoiding bulk registration that would confuse citation volume with decision confidence.
