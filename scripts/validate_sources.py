#!/usr/bin/env python3
"""Validate the decision-bearing source and finding registers."""

from __future__ import annotations

import csv
import datetime as dt
import pathlib
import re
import sys
from urllib.parse import urlparse


ROOT = pathlib.Path(__file__).resolve().parents[1]
SOURCE_PATH = ROOT / "research" / "sources.csv"
FINDING_PATH = ROOT / "research" / "findings.md"
EXPECTED_FIELDS = (
    "source_id",
    "vendor",
    "product",
    "title",
    "url",
    "access_date",
    "evidence_scope",
    "notes",
)


def markdown_rows(text: str) -> list[list[str]]:
    rows: list[list[str]] = []
    for line in text.splitlines():
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if cells and all(re.fullmatch(r":?-+:?", cell) for cell in cells):
            continue
        rows.append(cells)
    return rows


def expand_finding_reference(value: str) -> set[str]:
    value = value.strip()
    match = re.fullmatch(r"(F-\d{3})[–-](F-\d{3})", value)
    if not match:
        return {value}
    start = int(match.group(1).split("-")[1])
    end = int(match.group(2).split("-")[1])
    if end < start:
        return {value}
    return {f"F-{number:03d}" for number in range(start, end + 1)}


def main() -> None:
    errors: list[str] = []
    with SOURCE_PATH.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if tuple(reader.fieldnames or ()) != EXPECTED_FIELDS:
            errors.append(
                f"{SOURCE_PATH.relative_to(ROOT)}: expected columns {','.join(EXPECTED_FIELDS)}; "
                f"found {','.join(reader.fieldnames or [])}"
            )
        source_rows = list(reader)

    source_ids: set[str] = set()
    source_urls: set[str] = set()
    for line_number, row in enumerate(source_rows, start=2):
        if None in row:
            errors.append(f"{SOURCE_PATH.relative_to(ROOT)}:{line_number}: extra CSV cell")
        missing = [field for field in EXPECTED_FIELDS if not str(row.get(field, "")).strip()]
        if missing:
            errors.append(
                f"{SOURCE_PATH.relative_to(ROOT)}:{line_number}: blank fields {', '.join(missing)}"
            )
        source_id = str(row.get("source_id", "")).strip()
        if not re.fullmatch(r"[A-Z][A-Z0-9]*-\d{3}", source_id):
            errors.append(
                f"{SOURCE_PATH.relative_to(ROOT)}:{line_number}: invalid source_id {source_id!r}"
            )
        if source_id in source_ids:
            errors.append(
                f"{SOURCE_PATH.relative_to(ROOT)}:{line_number}: duplicate source_id {source_id}"
            )
        source_ids.add(source_id)

        url = str(row.get("url", "")).strip().rstrip("/")
        parsed = urlparse(url)
        if parsed.scheme != "https" or not parsed.netloc:
            errors.append(
                f"{SOURCE_PATH.relative_to(ROOT)}:{line_number}: source URL must be absolute HTTPS"
            )
        if url in source_urls:
            errors.append(
                f"{SOURCE_PATH.relative_to(ROOT)}:{line_number}: duplicate normalized URL {url}"
            )
        source_urls.add(url)

        access_date = str(row.get("access_date", "")).strip()
        try:
            dt.date.fromisoformat(access_date)
        except ValueError:
            errors.append(
                f"{SOURCE_PATH.relative_to(ROOT)}:{line_number}: invalid access_date {access_date!r}"
            )

    rows = markdown_rows(FINDING_PATH.read_text(encoding="utf-8"))
    if not rows or rows[0][:4] != ["ID", "State", "Claim", "Sources"]:
        errors.append(f"{FINDING_PATH.relative_to(ROOT)}: missing canonical finding table")
        finding_rows: list[list[str]] = []
    else:
        finding_rows = [row for row in rows[1:] if row and re.fullmatch(r"F-\d{3}", row[0])]

    finding_ids = {row[0] for row in finding_rows}
    if len(finding_ids) != len(finding_rows):
        errors.append(f"{FINDING_PATH.relative_to(ROOT)}: duplicate finding ID")
    used_source_ids: set[str] = set()
    allowed_states = {"Confirmed", "Interpretation", "Assumption", "Risk", "Open question"}
    for row in finding_rows:
        if len(row) != 5:
            errors.append(
                f"{FINDING_PATH.relative_to(ROOT)}: finding {row[0] if row else '?'} has "
                f"{len(row)} cells; expected 5"
            )
            continue
        finding_id, state, claim, references, implication = row
        if state not in allowed_states:
            errors.append(
                f"{FINDING_PATH.relative_to(ROOT)}: {finding_id} has unsupported state {state!r}"
            )
        if not claim or not implication:
            errors.append(f"{FINDING_PATH.relative_to(ROOT)}: {finding_id} lacks claim or implication")
        for token in (part.strip() for part in references.split(",")):
            if not token:
                errors.append(f"{FINDING_PATH.relative_to(ROOT)}: {finding_id} has blank source token")
                continue
            if token == "All":
                continue
            expanded = expand_finding_reference(token)
            if all(reference in finding_ids for reference in expanded):
                continue
            if token not in source_ids:
                errors.append(
                    f"{FINDING_PATH.relative_to(ROOT)}: {finding_id} references unknown source/finding {token}"
                )
            else:
                used_source_ids.add(token)

    if errors:
        print("ERROR:\n" + "\n".join(errors), file=sys.stderr)
        raise SystemExit(1)

    print(
        f"OK: {len(source_ids)} unique registered sources; {len(finding_ids)} findings; "
        f"{len(used_source_ids)} source IDs used directly in findings"
    )


if __name__ == "__main__":
    main()
