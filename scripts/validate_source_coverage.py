#!/usr/bin/env python3
"""Inventory article citations and keep the source-promotion boundary explicit."""

from __future__ import annotations

import argparse
import csv
import io
import pathlib
import re
import sys
from collections import Counter, defaultdict
from urllib.parse import urlsplit, urlunsplit

from repository_inventory import InventoryError, candidate_files


ROOT = pathlib.Path(__file__).resolve().parents[1]
try:
    CANDIDATE_FILES = candidate_files(ROOT)
except InventoryError as exc:
    print(f"ERROR: {exc}", file=sys.stderr)
    raise SystemExit(1)
REGISTER = ROOT / "research" / "sources.csv"
REPORT_CSV = ROOT / "reports" / "source-coverage.csv"
REPORT_MD = ROOT / "reports" / "source-coverage.md"
URL_PATTERN = re.compile(r"https?://[^\s<>\]\[\"'`]+")
LOCAL_HOSTS = {"localhost", "127.0.0.1", "0.0.0.0"}


def normalize_url(raw: str) -> str:
    value = raw.rstrip(".,;:!?")
    while value.endswith(")") and value.count("(") < value.count(")"):
        value = value[:-1]
    parsed = urlsplit(value)
    host = (parsed.hostname or "").lower()
    netloc = host
    if parsed.port and not (
        parsed.scheme.lower() == "https" and parsed.port == 443
    ):
        netloc = f"{host}:{parsed.port}"
    path = parsed.path or "/"
    if path != "/":
        path = path.rstrip("/")
    return urlunsplit((parsed.scheme.lower(), netloc, path, parsed.query, ""))


def article_paths() -> list[pathlib.Path]:
    paths: list[pathlib.Path] = []
    for path in CANDIDATE_FILES:
        if path.suffix.lower() != ".md":
            continue
        relative = path.relative_to(ROOT)
        if relative.parts[:1] == ("docs",) and re.fullmatch(r"[0-9][0-9]-.*\.md", path.name):
            paths.append(path)
        elif relative.parts[:1] == ("poc",) and len(relative.parts) == 2:
            paths.append(path)
        elif relative.parts[:1] == ("research",) and len(relative.parts) == 2 and path.name not in {"README.md", "findings.md"}:
            paths.append(path)
        elif relative.as_posix() in {"reports/methodology-review.md", "reports/evidence-state.md"}:
            paths.append(path)
    return sorted(paths)


def registered_sources() -> tuple[dict[str, str], str]:
    by_url: dict[str, str] = {}
    latest_access = ""
    with REGISTER.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            normalized = normalize_url(row["url"])
            by_url[normalized] = row["source_id"].strip()
            latest_access = max(latest_access, row["access_date"].strip())
    return by_url, latest_access


def collect_rows() -> tuple[list[dict[str, str]], list[str], str]:
    registered, latest_access = registered_sources()
    rows: list[dict[str, str]] = []
    errors: list[str] = []
    for path in article_paths():
        relative = path.relative_to(ROOT).as_posix()
        seen: set[str] = set()
        for match in URL_PATTERN.finditer(path.read_text(encoding="utf-8")):
            raw = match.group(0)
            normalized = normalize_url(raw)
            parsed = urlsplit(normalized)
            if parsed.hostname in LOCAL_HOSTS:
                continue
            if parsed.scheme != "https":
                errors.append(f"{relative}: external citation must use HTTPS: {raw}")
                continue
            if not parsed.hostname:
                errors.append(f"{relative}: malformed external citation: {raw}")
                continue
            if normalized in seen:
                continue
            seen.add(normalized)
            source_id = registered.get(normalized, "")
            rows.append(
                {
                    "document_path": relative,
                    "cited_url": raw.rstrip(".,;:!?"),
                    "normalized_url": normalized,
                    "registry_state": "registered" if source_id else "contextual",
                    "source_id": source_id,
                    "host": parsed.hostname.lower(),
                }
            )
    rows.sort(key=lambda row: (row["document_path"], row["normalized_url"]))
    return rows, errors, latest_access


def csv_text(rows: list[dict[str, str]]) -> str:
    buffer = io.StringIO(newline="")
    fields = (
        "document_path",
        "cited_url",
        "normalized_url",
        "registry_state",
        "source_id",
        "host",
    )
    writer = csv.DictWriter(buffer, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return buffer.getvalue()


def markdown_text(rows: list[dict[str, str]], latest_access: str) -> str:
    unique_urls = {row["normalized_url"] for row in rows}
    registered_urls = {
        row["normalized_url"] for row in rows if row["registry_state"] == "registered"
    }
    contextual_urls = unique_urls - registered_urls
    by_document: dict[str, Counter[str]] = defaultdict(Counter)
    contextual_hosts: Counter[str] = Counter()
    for row in rows:
        by_document[row["document_path"]][row["registry_state"]] += 1
        if row["registry_state"] == "contextual":
            contextual_hosts[row["host"]] += 1

    lines = [
        "# External citation coverage and source-promotion debt",
        "",
        "This report is generated from the article corpus by `scripts/validate_source_coverage.py`. It distinguishes the authoritative decision-bearing source chain from additional point-of-use context. It is a coverage inventory, not a liveness result or evidence-quality score.",
        "",
        "## Decision rule",
        "",
        "- A citation marked `registered` resolves to `research/sources.csv`; it may support a decision-bearing finding only when `research/findings.md` maps the relevant source ID and the claim preserves its version, topology, evidence state and limitation.",
        "- A citation marked `contextual` can explain a mechanism at the point of argument, but it cannot affect a criterion score, rank, gate disposition or recommendation until it is promoted into the register and finding chain.",
        "- Counts measure unique normalized URLs in each document. They do not imply that document volume or citation volume increases confidence.",
        "- Network liveness is deliberately outside deterministic CI; time-sensitive sources must be rechecked at the next decision gate.",
        "",
        "## Current inventory",
        "",
        f"| Measure | Count |",
        "|---|---:|",
        f"| Article files scanned | {len(article_paths())} |",
        f"| Article files containing external citations | {len(by_document)} |",
        f"| Unique external citations | {len(unique_urls)} |",
        f"| Unique registered citations used by articles | {len(registered_urls)} |",
        f"| Unique contextual citations awaiting promotion if decision-bearing | {len(contextual_urls)} |",
        f"| Latest access date in authoritative register | {latest_access or 'unknown'} |",
        "",
        "## Coverage by article",
        "",
        "| Article | Registered links | Contextual links | Boundary |",
        "|---|---:|---:|---|",
    ]
    for document, counts in sorted(by_document.items()):
        contextual = counts["contextual"]
        boundary = "promotion debt visible" if contextual else "registered citations only"
        lines.append(
            f"| `{document}` | {counts['registered']} | {contextual} | {boundary} |"
        )
    lines.extend(
        [
            "",
            "## Contextual-source concentration",
            "",
            "This table helps evidence owners batch promotion and freshness work. A high count is not a criticism when the links remain non-scoring context.",
            "",
            "| Host | Article-link occurrences |",
            "|---|---:|",
        ]
    )
    for host, count in sorted(contextual_hosts.items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"| `{host}` | {count} |")
    lines.extend(
        [
            "",
            "The machine-readable usage ledger is [`reports/source-coverage.csv`](source-coverage.csv). Promote only claims that can change the decision, and add the source ID to a specific finding rather than bulk-registering links to create an appearance of rigor.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="refresh committed coverage artifacts")
    args = parser.parse_args()

    rows, errors, latest_access = collect_rows()
    if errors:
        print("ERROR:\n" + "\n".join(errors), file=sys.stderr)
        raise SystemExit(1)

    expected_csv = csv_text(rows)
    expected_md = markdown_text(rows, latest_access)
    if args.write:
        REPORT_CSV.write_text(expected_csv, encoding="utf-8")
        REPORT_MD.write_text(expected_md, encoding="utf-8")
    else:
        for path, expected in ((REPORT_CSV, expected_csv), (REPORT_MD, expected_md)):
            if not path.exists():
                errors.append(f"{path.relative_to(ROOT)}: missing; run with --write")
            elif path.read_text(encoding="utf-8") != expected:
                errors.append(f"{path.relative_to(ROOT)}: stale; run with --write")
    if errors:
        print("ERROR:\n" + "\n".join(errors), file=sys.stderr)
        raise SystemExit(1)

    unique = {row["normalized_url"] for row in rows}
    registered = {row["normalized_url"] for row in rows if row["registry_state"] == "registered"}
    print(
        f"OK: {len(article_paths())} article files; {len(unique)} unique external citations; "
        f"{len(registered)} registered and {len(unique - registered)} contextual"
    )


if __name__ == "__main__":
    main()
