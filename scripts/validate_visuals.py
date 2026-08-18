#!/usr/bin/env python3
"""Validate Markdown/site visual parity and data-backed Markdown charts."""

from __future__ import annotations

import csv
import pathlib
import re
import sys
from collections import Counter

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from repository_inventory import InventoryError, candidate_files


ROOT = pathlib.Path(__file__).resolve().parents[1]
ARCHITECTURE = ROOT / "architecture"


try:
    CANDIDATE_FILES = candidate_files(ROOT)
except InventoryError as exc:
    print(f"ERROR: {exc}", file=sys.stderr)
    raise SystemExit(1)
CANDIDATE_FILE_SET = set(CANDIDATE_FILES)


def table_rows(path: pathlib.Path, required_header: str) -> list[dict[str, str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    for index, line in enumerate(lines[:-1]):
        if not line.lstrip().startswith("|"):
            continue
        headers = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if required_header not in headers:
            continue
        if not re.fullmatch(r"[|:\-\s]+", lines[index + 1]):
            continue
        rows: list[dict[str, str]] = []
        for candidate in lines[index + 2 :]:
            if not candidate.lstrip().startswith("|"):
                break
            cells = [cell.strip() for cell in candidate.strip().strip("|").split("|")]
            rows.append(dict(zip(headers, cells)))
        return rows
    return []


def expected_charts() -> dict[str, Counter[str]]:
    with (ROOT / "decision-matrix" / "criteria.csv").open(newline="", encoding="utf-8") as handle:
        criteria = list(csv.DictReader(handle))
    criterion_types = Counter(row["requirement_type"].strip().capitalize() for row in criteria)

    poc_rows = table_rows(ROOT / "poc" / "test-plan.md", "Baseline status")
    poc_status = Counter(row["Baseline status"].strip() for row in poc_rows)

    with (ROOT / "research" / "sources.csv").open(newline="", encoding="utf-8") as handle:
        sources = list(csv.DictReader(handle))
    findings = (ROOT / "research" / "findings.md").read_text(encoding="utf-8")
    source_ids = [row["source_id"].strip() for row in sources if row.get("source_id", "").strip()]
    used = sum(
        bool(re.search(rf"(?<![A-Z0-9-]){re.escape(source_id)}(?![A-Z0-9-])", findings, flags=re.IGNORECASE))
        for source_id in source_ids
    )
    source_use = Counter({"Used in findings": used, "Not yet used": len(source_ids) - used})

    return {
        "criteria-requirement-type": criterion_types,
        "poc-execution": poc_status,
        "source-use": source_use,
    }


def validate_diagram_mirrors(errors: list[str]) -> int:
    pattern = re.compile(
        r"<!--\s*diagram-source:\s*([^\s]+)\s*-->\s*```mermaid\s*\n(.*?)\n```",
        flags=re.DOTALL,
    )
    mirrors: dict[str, list[tuple[pathlib.Path, str]]] = {}
    for markdown in sorted(path for path in CANDIDATE_FILES if path.parent == ARCHITECTURE and path.suffix.lower() == ".md"):
        text = markdown.read_text(encoding="utf-8")
        for source, block in pattern.findall(text):
            mirrors.setdefault(source, []).append((markdown, block.strip()))

    diagram_root = ARCHITECTURE / "diagrams"
    expected = {
        path.relative_to(ARCHITECTURE).as_posix()
        for path in CANDIDATE_FILES
        if path.parent == diagram_root and path.suffix.lower() == ".mmd"
    }
    actual = set(mirrors)
    for source in sorted(expected - actual):
        errors.append(f"architecture diagram has no Markdown mirror: {source}")
    for source in sorted(actual - expected):
        errors.append(f"Markdown mirror references a missing diagram: {source}")

    for source, locations in sorted(mirrors.items()):
        if len(locations) != 1:
            errors.append(f"diagram must have exactly one Markdown mirror: {source} ({len(locations)} found)")
            continue
        markdown, block = locations[0]
        source_path = ARCHITECTURE / source
        if source_path not in CANDIDATE_FILE_SET:
            continue
        canonical = source_path.read_text(encoding="utf-8").strip()
        if block != canonical:
            errors.append(f"Markdown mirror differs from {source}: {markdown.relative_to(ROOT)}")
    return len(actual)


def validate_diagram_aliases(errors: list[str]) -> int:
    pattern = re.compile(
        r"<!--\s*diagram-alias-source:\s*([^\s]+)\s*-->\s*```mermaid\s*\n(.*?)\n```",
        flags=re.DOTALL,
    )
    count = 0
    for markdown in sorted(path for path in CANDIDATE_FILES if path.suffix.lower() == ".md"):
        text = markdown.read_text(encoding="utf-8")
        for source, block in pattern.findall(text):
            count += 1
            source_path = (markdown.parent / source).resolve()
            if not source_path.is_relative_to(ROOT) or source_path not in CANDIDATE_FILE_SET:
                errors.append(f"diagram alias references a missing source: {markdown.relative_to(ROOT)} -> {source}")
                continue
            canonical = source_path.read_text(encoding="utf-8").strip()
            if block.strip() != canonical:
                errors.append(f"diagram alias differs from {source}: {markdown.relative_to(ROOT)}")
    return count


def validate_data_charts(errors: list[str]) -> int:
    report = ROOT / "reports" / "evidence-state.md"
    text = report.read_text(encoding="utf-8")
    pattern = re.compile(
        r"<!--\s*chart-source:\s*([^\s]+)\s*-->\s*```mermaid\s*\n(.*?)\n```",
        flags=re.DOTALL,
    )
    charts = {name: block for name, block in pattern.findall(text)}
    expected = expected_charts()
    if set(charts) != set(expected):
        errors.append(
            "evidence-state chart markers differ: "
            f"expected {sorted(expected)}, found {sorted(charts)}"
        )
    for name, counts in expected.items():
        block = charts.get(name, "")
        actual = Counter(
            {label: int(value) for label, value in re.findall(r'^\s*"([^"]+)"\s*:\s*(\d+)\s*$', block, flags=re.MULTILINE)}
        )
        if actual != counts:
            errors.append(f"chart {name} is stale: expected {dict(counts)}, found {dict(actual)}")
    return len(charts)


def main() -> None:
    errors: list[str] = []
    diagram_count = validate_diagram_mirrors(errors)
    alias_count = validate_diagram_aliases(errors)
    chart_count = validate_data_charts(errors)
    if errors:
        print("ERROR: " + "; ".join(errors), file=sys.stderr)
        raise SystemExit(1)
    print(
        f"OK: {diagram_count} Mermaid mirrors, {alias_count} canonical aliases, "
        f"and {chart_count} data-backed Markdown charts"
    )


if __name__ == "__main__":
    main()
