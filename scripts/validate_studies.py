#!/usr/bin/env python3
"""Enforce the opt-in principal-study contract for substantive Markdown."""

from __future__ import annotations

import pathlib
import re
import sys


ROOT = pathlib.Path(__file__).resolve().parents[1]
MARKER = "<!-- study-contract: principal -->"
PROTOCOL_MARKER = "<!-- protocol-contract: decision-grade -->"
MIN_WORDS = 900
MIN_PROTOCOL_WORDS = 1500
MIN_CONTRACT_STUDIES = 41
MIN_CONTRACT_PROTOCOLS = 3
REQUIRED_STUDY_PREFIXES = {
    *(f"{number:02d}-" for number in range(37)),
    "41-",
    "42-",
    "43-",
    "44-",
}
ALLOWED_ARTIFACT_TYPES = {
    "principal-study",
    "candidate-dossier",
    "architecture-study",
    "comparative-study",
}

MERMAID_RE = re.compile(
    r"^```mermaid[^\n]*\n.*?^```[ \t]*$",
    flags=re.MULTILINE | re.DOTALL,
)
FIGURE_TITLE_RE = re.compile(
    r"^\*\*(Figure|Chart)\s+([A-Za-z0-9][A-Za-z0-9._-]*)\s+—\s+(\S.*?)\*\*\s*$",
    flags=re.MULTILINE,
)
FIGURE_FIELD_RES = {
    "Depicted scope": re.compile(
        r"^- \*\*Depicted scope:\*\*\s+\S.*$",
        flags=re.MULTILINE,
    ),
    "Excluded scope": re.compile(
        r"^- \*\*Excluded scope:\*\*\s+\S.*$",
        flags=re.MULTILINE,
    ),
    "Source, evidence state and as-of": re.compile(
        r"^- \*\*(?:Diagram|Chart) source, evidence state and as-of:\*\*\s+\S.*$",
        flags=re.MULTILINE,
    ),
    "Accessible equivalent": re.compile(
        r"^- \*\*Accessible equivalent:\*\*\s+\S.*$",
        flags=re.MULTILINE,
    ),
}
FIGURE_INTERPRETATION_RE = re.compile(
    r"^\*\*(?:Figure|Chart) interpretation:\*\*\s+\S.*$",
    flags=re.MULTILINE,
)
FIGURE_LIMITATION_RE = re.compile(
    r"^\*\*(?:Figure|Chart) limitation:\*\*\s+\S.*$",
    flags=re.MULTILINE,
)
ISO_DATE_RE = re.compile(r"\b20\d{2}-\d{2}-\d{2}\b")


def headings(text: str) -> list[str]:
    return [match.group(1).strip().lower() for match in re.finditer(r"^#{2,4}\s+(.+?)\s*$", text, flags=re.MULTILINE)]


def has_heading(names: list[str], *needles: str) -> bool:
    return any(any(needle in name for needle in needles) for name in names)


def table_count(text: str) -> int:
    return len(re.findall(r"^\s*\|(?:\s*:?-+:?\s*\|){2,}\s*$", text, flags=re.MULTILINE))


def has_contract_marker(text: str, marker: str) -> bool:
    return bool(re.search(rf"^\s*{re.escape(marker)}\s*$", text, flags=re.MULTILINE))


def validate_figure_contracts(
    text: str,
    relative: pathlib.Path,
    errors: list[str],
    figure_ids: dict[str, str],
) -> int:
    """Validate one visible, ordered metadata contract around every Mermaid fence."""
    mermaids = list(MERMAID_RE.finditer(text))
    titles = list(FIGURE_TITLE_RE.finditer(text))
    global_fields = {
        label: list(pattern.finditer(text)) for label, pattern in FIGURE_FIELD_RES.items()
    }
    interpretations = list(FIGURE_INTERPRETATION_RE.finditer(text))
    limitations = list(FIGURE_LIMITATION_RE.finditer(text))

    expected = len(mermaids)
    counts = {
        "Figure/Chart ID and title": len(titles),
        **{label: len(matches) for label, matches in global_fields.items()},
        "Figure/Chart interpretation": len(interpretations),
        "Figure/Chart limitation": len(limitations),
    }
    for label, count in counts.items():
        if count != expected:
            errors.append(
                f"{relative}: {expected} Mermaid exhibits require exactly {expected} visible "
                f"{label} fields; found {count}"
            )

    previous_mermaid_end = 0
    for index, mermaid in enumerate(mermaids, start=1):
        next_mermaid_start = mermaids[index].start() if index < len(mermaids) else len(text)
        pre = text[previous_mermaid_end : mermaid.start()]
        post = text[mermaid.end() : next_mermaid_start]
        line = text.count("\n", 0, mermaid.start()) + 1
        context = f"{relative}: Mermaid {index} at line {line}"

        pre_matches: list[tuple[str, re.Match[str]]] = []
        title_matches = list(FIGURE_TITLE_RE.finditer(pre))
        if len(title_matches) != 1:
            errors.append(
                f"{context}: requires exactly one preceding `**Figure/Chart ID — title.**`; "
                f"found {len(title_matches)}"
            )
        else:
            title = title_matches[0]
            pre_matches.append(("title", title))
            figure_id = title.group(2)
            location = f"{relative}:{line}"
            if figure_id in figure_ids:
                errors.append(
                    f"{context}: duplicate figure ID {figure_id!r}; first used at "
                    f"{figure_ids[figure_id]}"
                )
            else:
                figure_ids[figure_id] = location

        source_match: re.Match[str] | None = None
        for label, pattern in FIGURE_FIELD_RES.items():
            matches = list(pattern.finditer(pre))
            if len(matches) != 1:
                errors.append(
                    f"{context}: requires exactly one preceding `{label}` field; "
                    f"found {len(matches)}"
                )
                continue
            pre_matches.append((label, matches[0]))
            if label == "Source, evidence state and as-of":
                source_match = matches[0]

        expected_order = [
            "title",
            "Depicted scope",
            "Excluded scope",
            "Source, evidence state and as-of",
            "Accessible equivalent",
        ]
        if len(pre_matches) == len(expected_order):
            actual_order = [
                label for label, _ in sorted(pre_matches, key=lambda item: item[1].start())
            ]
            if actual_order != expected_order:
                errors.append(
                    f"{context}: visible pre-figure fields are out of order; expected "
                    f"{' -> '.join(expected_order)}"
                )
        if source_match and not ISO_DATE_RE.search(source_match.group(0)):
            errors.append(
                f"{context}: source/evidence/as-of field requires an ISO as-of date"
            )

        interpretation_matches = list(FIGURE_INTERPRETATION_RE.finditer(post))
        limitation_matches = list(FIGURE_LIMITATION_RE.finditer(post))
        if len(interpretation_matches) != 1:
            errors.append(
                f"{context}: requires exactly one following `Figure/Chart interpretation`; "
                f"found {len(interpretation_matches)}"
            )
        if len(limitation_matches) != 1:
            errors.append(
                f"{context}: requires exactly one following `Figure/Chart limitation`; "
                f"found {len(limitation_matches)}"
            )
        if (
            len(interpretation_matches) == 1
            and len(limitation_matches) == 1
            and interpretation_matches[0].start() > limitation_matches[0].start()
        ):
            errors.append(
                f"{context}: interpretation must precede limitation"
            )

        previous_mermaid_end = mermaid.end()

    return expected


def main() -> None:
    errors: list[str] = []
    studies: list[tuple[pathlib.Path, int]] = []
    protocols: list[tuple[pathlib.Path, int]] = []
    figure_ids: dict[str, str] = {}
    document_paths = sorted((ROOT / "docs").glob("*.md"))
    for prefix in sorted(REQUIRED_STUDY_PREFIXES):
        matches = [path for path in document_paths if path.name.startswith(prefix)]
        if len(matches) != 1:
            errors.append(
                f"docs/{prefix}*: expected exactly one required principal study; found {len(matches)}"
            )
            continue
        if not has_contract_marker(matches[0].read_text(encoding="utf-8"), MARKER):
            errors.append(f"{matches[0].relative_to(ROOT)}: required principal-study marker is missing")

    for path in document_paths:
        text = path.read_text(encoding="utf-8")
        if not has_contract_marker(text, MARKER):
            continue
        words = len(re.findall(r"\b[\w][\w’'/-]*\b", text))
        studies.append((path, words))
        relative = path.relative_to(ROOT)
        names = headings(text)

        if words < MIN_WORDS:
            errors.append(f"{relative}: principal study has {words} words; minimum is {MIN_WORDS}")
        for field in (
            "Artifact type",
            "Decision question",
            "Decision owner",
            "Primary audiences",
            "Scope",
            "Evidence state",
            "Reference case",
            "As-of date",
            "Next gate",
        ):
            if not re.search(rf"^\|\s*{re.escape(field)}\s*\|", text, flags=re.MULTILINE | re.IGNORECASE):
                errors.append(f"{relative}: missing study-header field {field}")

        required_heading_groups = (
            ("provisional answer", "executive answer", "answer first"),
            ("scenario", "reference case"),
            ("mechanism", "architecture analysis", "operating model"),
            ("failure", "edge case", "challenge"),
            ("decision implications",),
            ("falsification", "proof plan", "validation plan"),
            ("risk", "limitation"),
            ("open evidence",),
            ("next gate",),
        )
        for group in required_heading_groups:
            if not has_heading(names, *group):
                errors.append(f"{relative}: missing required heading concept {'/'.join(group)}")

        mermaid_count = validate_figure_contracts(text, relative, errors, figure_ids)
        if not mermaid_count:
            errors.append(f"{relative}: requires an inline Mermaid exhibit")
        if table_count(text) < 2:
            errors.append(f"{relative}: requires at least two inline data/evidence tables")
        if "scenario assumption" not in text.lower():
            errors.append(f"{relative}: must label synthetic numeric inputs as scenario assumptions")
        if not re.search(
            r"documented fact|observed result|interpretation|hypothesis|open question|evidence state",
            text,
            flags=re.IGNORECASE,
        ):
            errors.append(f"{relative}: missing explicit evidence-state language")

        artifact_match = re.search(r"^\|\s*Artifact type\s*\|\s*([^|]+)", text, flags=re.MULTILINE | re.IGNORECASE)
        artifact_type = artifact_match.group(1).strip().lower() if artifact_match else ""
        if artifact_type and artifact_type not in ALLOWED_ARTIFACT_TYPES:
            errors.append(
                f"{relative}: unsupported Artifact type {artifact_type!r}; "
                f"expected one of {', '.join(sorted(ALLOWED_ARTIFACT_TYPES))}"
            )
        if not re.search(
            r"\bnon-fit\b|counter-(?:hypoth|evidence)|\bcounterfactual",
            text,
            flags=re.IGNORECASE,
        ):
            errors.append(f"{relative}: missing explicit counter-hypothesis, counter-evidence, or non-fit analysis")
        proof_terms = ("procedure", "measure", "threshold", "artifact", "reviewer")
        missing_proof_terms = [
            term for term in proof_terms if not re.search(rf"\b{term}\w*\b", text, flags=re.IGNORECASE)
        ]
        if missing_proof_terms:
            errors.append(
                f"{relative}: proof plan is missing {', '.join(missing_proof_terms)}"
            )
        if artifact_type in {"candidate-dossier", "comparative-study"}:
            links = set(re.findall(r"https://[^)\s|>]+", text))
            if len(links) < 3:
                errors.append(f"{relative}: {artifact_type} requires at least three point-of-use primary-source links")

    for path in sorted((ROOT / "poc").glob("*.md")):
        text = path.read_text(encoding="utf-8")
        if not has_contract_marker(text, PROTOCOL_MARKER):
            continue
        words = len(re.findall(r"\b[\w][\w’'/-]*\b", text))
        protocols.append((path, words))
        relative = path.relative_to(ROOT)
        names = headings(text)

        if words < MIN_PROTOCOL_WORDS:
            errors.append(
                f"{relative}: decision-grade protocol has {words} words; minimum is {MIN_PROTOCOL_WORDS}"
            )
        protocol_heading_groups = (
            ("purpose",),
            ("experiment", "scenario coverage"),
            ("evidence", "run record"),
            ("gate",),
        )
        for group in protocol_heading_groups:
            if not has_heading(names, *group):
                errors.append(f"{relative}: missing protocol heading concept {'/'.join(group)}")
        mermaid_count = validate_figure_contracts(text, relative, errors, figure_ids)
        if not mermaid_count:
            errors.append(f"{relative}: decision-grade protocol requires an inline Mermaid exhibit")
        if table_count(text) < 2:
            errors.append(f"{relative}: decision-grade protocol requires at least two control/evidence tables")
        for term in ("scenario assumption", "abort", "independent"):
            if term not in text.lower():
                errors.append(f"{relative}: decision-grade protocol must define {term!r}")
        if not re.search(r"not[- ]run|not run|no observed", text, flags=re.IGNORECASE):
            errors.append(f"{relative}: protocol must distinguish planned work from observed results")

    if len(studies) < MIN_CONTRACT_STUDIES:
        errors.append(
            f"principal-study contract covers only {len(studies)} documents; expected at least {MIN_CONTRACT_STUDIES}"
        )
    if len(protocols) < MIN_CONTRACT_PROTOCOLS:
        errors.append(
            f"decision-grade protocol contract covers only {len(protocols)} documents; "
            f"expected at least {MIN_CONTRACT_PROTOCOLS}"
        )

    template = ROOT / "templates" / "principal-study-template.md"
    if not template.exists() or not has_contract_marker(template.read_text(encoding="utf-8"), MARKER):
        errors.append("templates/principal-study-template.md is missing the principal-study marker")

    if errors:
        print("ERROR: " + "; ".join(errors), file=sys.stderr)
        raise SystemExit(1)
    total_words = sum(words for _, words in studies)
    protocol_words = sum(words for _, words in protocols)
    print(
        f"OK: {len(studies)} principal studies ({total_words} words) and "
        f"{len(protocols)} decision-grade protocols ({protocol_words} words) satisfy the content contracts"
    )


if __name__ == "__main__":
    main()
