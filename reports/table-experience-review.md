# Table experience review

## Review decision

The former one-size-fits-all table treatment was not acceptable for a study portal. It rendered every CSV and Markdown table as an unbounded grid inside the article column, even when the reader's task was to scan a decision register, inspect a source catalogue, or understand an empty template schema.

This release replaces that treatment with a task-oriented dataset workspace and a bounded article-table pattern. The canonical CSV files are unchanged. Presentation changes affect only how the portal helps a reader inspect them.

**Review date:** 2026-08-17  
**Baseline measured:** commit `12a476ce297c111bd2420830548d365f02148ded`  
**Scope:** ten CSV routes and the shared renderer used by Markdown tables  
**Decision state:** implemented and release-tested; the follow-on recommendations below remain open

## Measured failure state

The criteria route made the systemic problem visible:

- the eight-column table was 1,219 px wide inside an 827 px desktop reading area;
- the acceptance-test column, although initially off-screen, forced a median row height of 246.8 px;
- 120 criteria produced a 28,489 px table, with the horizontal scrollbar available only at the bottom;
- at 1,024 px, three decision fields were entirely outside the initial view;
- at 390 px, the reader saw the ID, category, and only part of the criterion;
- the scroll region had no keyboard focus, accessible name, explicit overflow cue, useful sticky header, search, or view control; and
- raw `snake_case` field names were used as oversized uppercase headings.

The defect was not limited to criteria. The remediation backlog exposed 18 columns in a 2,623 px grid; source coverage produced a roughly 30,000 px page from 436 occurrences; the risk register inherited 246 px median rows; and a zero-record migration template displayed a 35-column empty header nearly six times wider than its reading area.

## Implemented information architecture

### Dataset routes

Dataset routes now use the full document width and put the dataset before secondary visual context. A compact heading states record and field counts, followed by a text filter and, where the schema benefits from progressive disclosure, two explicit views:

- **Reading view** keeps the fields needed for scanning and comparison in the main row.
- **Supporting fields** exposes evidence, tests, URLs, notes, or workflow detail for one record without making every row as tall as its longest narrative field.
- **Full grid** retains every source column for audit and reconciliation.

The active grid is bounded to the viewport, vertically and horizontally scrollable, keyboard-focusable, explicitly labelled, and equipped with sticky column headings and a sticky row key. Human-readable headings are shown while the raw source field remains available as an abbreviation title. Search evaluates the complete record, including fields not present in the reading view.

### Route-specific patterns

| Dataset | Default reading fields | Per-record supporting fields | Full-grid purpose |
|---|---|---|---|
| Criteria | Criterion ID, criterion, category, requirement type, default weight, status | Evidence required and acceptance test | Reconcile all eight canonical fields |
| Content remediation backlog | Recommendation ID, priority, workstream, status, owner role, target gate | Problem, remediation, evidence, dependencies, review, disposition, and replacement workflow | Audit all 18 workflow fields |
| Source catalogue | Source ID, vendor, product, title, access date | URL, evidence scope, and notes | Review the complete source register |
| Source coverage | Document path, registry state, source ID, host | Cited and normalized URL | Trace every citation occurrence |
| Empty templates | Field dictionary rather than an empty grid | Field name and inferred field class | Canonical CSV remains available for download and population |

### Article tables

Markdown tables retain native table semantics. They now receive measured column widths based on field and content characteristics, a bounded overflow viewport, sticky headings, an accessible caption region, visible overflow treatment, keyboard focus, and readable wrapping. This prevents a long off-screen cell from determining the height of every row and keeps horizontal overflow local to the exhibit rather than the page.

## Acceptance evidence

The release is accepted only when all of the following remain true at desktop, tablet, and phone widths:

1. The page itself has no horizontal overflow.
2. The first and last fields remain reachable without clipping or hidden data.
3. Dataset body copy is at least 16 px and headings or metadata are at least 14 px.
4. The table viewport, not the full page, owns long vertical and horizontal scrolling.
5. The active viewport is keyboard-focusable and has a visible focus treatment.
6. Headers remain visible while the reader scrolls records inside the viewport.
7. Primary rows are content-sized and contain no blank bands created by hidden narrative fields.
8. Search, reading/full-view switching, and per-record disclosure work without changing the canonical data.
9. Empty templates render as readable schema dictionaries rather than empty ultra-wide grids.
10. Native `table`, `thead`, `tbody`, column-header, and row-header semantics remain available to assistive technology.

On the criteria route at 1,440 × 900, the reading grid occupies the full 1,337 px workspace, has no horizontal overflow, uses 16 px body text and 14 px headings, and reduces sampled primary rows from 224–247 px to approximately 47–70 px. The record area is bounded rather than extending the page by tens of thousands of pixels. At narrower widths the table remains a comparison surface with a frozen row key, explicit horizontal-scroll instruction, and supporting-field disclosures; content is not silently removed.

## Follow-on recommendations

These are durable recommendations, not claims of completion:

1. Replace the 436-occurrence source-coverage default with a grouped document/source audit and drill into occurrences on demand. The current bounded register is usable, but grouping better matches the assurance task.
2. Add schema-governed filters and sorting for high-value registers: category/type/status for criteria; priority/workstream/status/gate for remediation; vendor/product/freshness for sources.
3. Introduce paging or windowed rendering when a populated register exceeds 500 records, while preserving complete search and accessible position/count announcements.
4. Define typed article patterns for risk, assumption, question, proof-protocol, and multi-option comparison exhibits. Horizontal scrolling should remain a fallback, not the primary information architecture for every dense table.
5. Add automated visual and accessibility regression checks for row density, page overflow, sticky navigation, keyboard reachability, minimum text size, first/last-field reachability, and empty-schema presentation.
6. Drive dataset labels and controls from the governed artifact taxonomy when PCR-007 is remediated; this release does not close that recommendation.

## Release boundary

This work makes tabular evidence readable and navigable. It does not make a field observed, approve a criterion, resolve a product option, close a remediation item, or elevate evidence maturity. The CSV remains authoritative; the portal is a lossless reading and inspection layer over it.
