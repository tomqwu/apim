#!/usr/bin/env python3
"""Build the API Management Studies static site with Python's standard library."""

from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SITE_SOURCE = ROOT / "site"
CONTENT_ROOTS = (
    "docs",
    "architecture",
    "decision-matrix",
    "research",
    "poc",
    "mule-migration",
    "workshops",
    "adr",
    "templates",
    "reports",
)
TEXT_EXTENSIONS = {
    ".md",
    ".mmd",
    ".csv",
    ".yaml",
    ".yml",
    ".json",
    ".txt",
    ".sh",
    ".py",
    ".js",
    ".html",
    ".css",
    ".xml",
    ".toml",
    ".ini",
    ".conf",
    ".dockerfile",
}
MEDIA_EXTENSIONS = {
    ".pdf",
    ".ppt",
    ".pptx",
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".webp",
    ".svg",
    ".mp4",
    ".webm",
}
TYPE_NAMES = {
    ".md": "markdown",
    ".mmd": "mermaid",
    ".csv": "csv",
    ".yaml": "yaml",
    ".yml": "yaml",
    ".json": "json",
    ".pdf": "pdf",
    ".ppt": "presentation",
    ".pptx": "presentation",
    ".html": "html",
    ".sh": "shell",
    ".py": "python",
    ".js": "javascript",
    ".svg": "image",
    ".png": "image",
    ".jpg": "image",
    ".jpeg": "image",
    ".gif": "image",
    ".webp": "image",
    ".mp4": "video",
    ".webm": "video",
}
SECTION_LABELS = {
    "docs": "Studies",
    "architecture": "Architecture",
    "decision-matrix": "Compare",
    "research": "Research",
    "poc": "PoC & Examples",
    "mule-migration": "Migration",
    "workshops": "Workshops",
    "adr": "Decisions",
    "templates": "Templates",
    "reports": "Reports",
}
TAG_RULES = {
    "kong": ("kong",),
    "azure apim": ("azure apim", "azure api management"),
    "apigee": ("apigee",),
    "mulesoft": ("mulesoft", "mule ", "mule/"),
    "kubernetes": ("kubernetes", "aks", "gateway api"),
    "security": ("security", "oauth", "oidc", "jwt", "mtls", "identity"),
    "architecture": ("architecture", "topology", "control plane", "data plane"),
    "migration": ("migration", "modernization", "decommission", "strangler"),
    "apiops": ("apiops", "pipeline", "declarative configuration"),
    "observability": ("observability", "telemetry", "prometheus", "logging", "metrics"),
    "resilience": ("resilience", "failover", "disaster recovery", "ha/dr"),
    "governance": ("governance", "operating model", "guardrail"),
}

DIAGRAM_COMPANIONS = {
    "architecture/diagrams/apiops-flow.mmd": "architecture/apiops-architecture.md",
    "architecture/diagrams/current-state.mmd": "architecture/current-state.md",
    "architecture/diagrams/dr-failover.mmd": "architecture/ha-dr-architecture.md",
    "architecture/diagrams/east-west.mmd": "architecture/network-architecture.md",
    "architecture/diagrams/hybrid-data-plane.mmd": "architecture/kong-hybrid-architecture.md",
    "architecture/diagrams/kong-control-data-plane.mmd": "architecture/kong-hybrid-architecture.md",
    "architecture/diagrams/mule-decomposition.mmd": "architecture/pcf-aks-transition.md",
    "architecture/diagrams/north-south.mmd": "architecture/network-architecture.md",
    "architecture/diagrams/observability-flow.mmd": "architecture/observability-architecture.md",
    "architecture/diagrams/security-flow.mmd": "architecture/security-architecture.md",
    "architecture/diagrams/target-state.mmd": "architecture/target-state.md",
    "architecture/diagrams/transition-state.mmd": "architecture/transition-state.md",
}


def slug(value: str) -> str:
    value = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return value or "document"


def safe_text(path: Path) -> str:
    if path.suffix.lower() not in TEXT_EXTENSIONS and path.name != "Dockerfile":
        return ""
    try:
        return path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return ""


def clean_inline(value: str) -> str:
    value = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", value)
    value = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", value)
    value = re.sub(r"[`*_>#|]", " ", value)
    return re.sub(r"\s+", " ", value).strip(" -")


def document_title(path: Path, text: str) -> str:
    if path.suffix.lower() == ".md":
        heading = re.search(r"^#\s+(.+)$", text, flags=re.MULTILINE)
        if heading:
            return clean_inline(heading.group(1))
    if path.suffix.lower() in {".yaml", ".yml"}:
        info_title = re.search(r"^\s{2}title:\s*[\"']?(.+?)[\"']?\s*$", text, flags=re.MULTILINE)
        if info_title:
            return clean_inline(info_title.group(1))
    return re.sub(r"^\d{2,4}[-_]", "", path.stem).replace("-", " ").replace("_", " ").title()


def document_summary(path: Path, text: str, title: str) -> str:
    if path.suffix.lower() == ".md":
        blocks = re.split(r"\n\s*\n", text)
        for block in blocks:
            candidate = clean_inline(block)
            if not candidate or candidate == title or block.lstrip().startswith(("#", "```", "|")):
                continue
            return candidate[:260] + ("…" if len(candidate) > 260 else "")
    if path.suffix.lower() == ".mmd":
        return f"Source diagram for {title}. Open it in the architecture gallery to render the model."
    if path.suffix.lower() == ".csv":
        return f"Structured dataset for {title}, available as a filterable table and download."
    if path.suffix.lower() in {".yaml", ".yml"} and re.search(r"^openapi:\s*", text, flags=re.MULTILINE):
        return f"OpenAPI contract for {title}."
    return f"Repository resource: {title}."


def item_type(path: Path, text: str) -> str:
    suffix = path.suffix.lower()
    if suffix in {".yaml", ".yml"} and re.search(r"^openapi:\s*", text, flags=re.MULTILINE):
        return "openapi"
    if path.name == "Dockerfile":
        return "dockerfile"
    return TYPE_NAMES.get(suffix, "resource")


def item_order(path: Path) -> int:
    match = re.match(r"^(\d+)", path.name)
    return int(match.group(1)) if match else 9999


def make_tags(relative: Path, text: str, section: str) -> list[str]:
    haystack = f"{relative.as_posix()}\n{text[:30000]}".lower()
    tags = [section.lower()]
    for label, needles in TAG_RULES.items():
        if any(needle in haystack for needle in needles):
            tags.append(label)
    return list(dict.fromkeys(tags))[:7]


def collect_items(output: Path) -> list[dict[str, object]]:
    items: list[dict[str, object]] = []
    seen_ids: set[str] = set()
    for root_name in CONTENT_ROOTS:
        source_root = ROOT / root_name
        if not source_root.exists():
            continue
        for source in sorted(path for path in source_root.rglob("*") if path.is_file()):
            if source.name.startswith(".") or any(part.startswith(".") for part in source.relative_to(ROOT).parts):
                continue
            if source.suffix.lower() not in TEXT_EXTENSIONS | MEDIA_EXTENSIONS and source.name != "Dockerfile":
                continue
            relative = source.relative_to(ROOT)
            destination = output / "content" / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)
            text = safe_text(source)
            title = document_title(source, text)
            section = SECTION_LABELS[root_name]
            kind = item_type(source, text)
            item_id = slug(relative.with_suffix("").as_posix())
            if item_id in seen_ids:
                item_id = f"{item_id}-{len(items)}"
            seen_ids.add(item_id)
            search_text = clean_inline(text[:50000])
            items.append(
                {
                    "id": item_id,
                    "title": title,
                    "path": relative.as_posix(),
                    "contentUrl": f"content/{relative.as_posix()}",
                    "section": section,
                    "type": kind,
                    "order": item_order(source),
                    "tags": make_tags(relative, text, section),
                    "summary": document_summary(source, text, title),
                    "searchText": search_text,
                    "size": source.stat().st_size,
                }
            )
    items.sort(key=lambda item: (CONTENT_ROOTS.index(str(item["path"]).split("/", 1)[0]), int(item["order"]), str(item["title"])))
    by_path = {str(item["path"]): item for item in items}
    for diagram_path, companion_path in DIAGRAM_COMPANIONS.items():
        diagram = by_path.get(diagram_path)
        companion = by_path.get(companion_path)
        if diagram and companion:
            diagram["companionId"] = companion["id"]
            diagram["companionPath"] = companion_path
    return items


def count_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def markdown_row(line: str) -> list[str]:
    """Split a pipe-delimited Markdown table row, preserving escaped pipes."""
    stripped = line.strip()
    if not stripped.startswith("|"):
        return []
    stripped = stripped[1:]
    if stripped.endswith("|"):
        stripped = stripped[:-1]
    return [cell.replace(r"\|", "|").strip() for cell in re.split(r"(?<!\\)\|", stripped)]


def markdown_tables(text: str) -> list[list[dict[str, str]]]:
    """Return all well-formed leading-pipe Markdown tables in a document."""
    lines = text.splitlines()
    tables: list[list[dict[str, str]]] = []
    index = 0
    while index + 1 < len(lines):
        headers = markdown_row(lines[index])
        separator = markdown_row(lines[index + 1])
        if (
            not headers
            or len(headers) != len(separator)
            or not all(re.fullmatch(r":?-{3,}:?", re.sub(r"\s+", "", cell)) for cell in separator)
        ):
            index += 1
            continue
        rows: list[dict[str, str]] = []
        cursor = index + 2
        while cursor < len(lines):
            cells = markdown_row(lines[cursor])
            if not cells:
                break
            if len(cells) < len(headers):
                cells.extend([""] * (len(headers) - len(cells)))
            rows.append(dict(zip(headers, cells[: len(headers)])))
            cursor += 1
        tables.append(rows)
        index = cursor
    return tables


def markdown_table(text: str, required_columns: tuple[str, ...]) -> list[dict[str, str]]:
    """Find a Markdown table by column names instead of by document position."""
    required = {column.casefold() for column in required_columns}
    for rows in markdown_tables(text):
        if not rows:
            continue
        columns = {column.casefold() for column in rows[0]}
        if required.issubset(columns):
            return rows
    return []


def row_value(row: dict[str, str], column: str) -> str:
    """Read a Markdown table cell case-insensitively."""
    target = column.casefold()
    for key, value in row.items():
        if key.casefold() == target:
            return value.strip()
    return ""


def integer(value: str) -> int:
    try:
        return int(value.strip())
    except (AttributeError, TypeError, ValueError):
        return 0


def label_for(value: str) -> str:
    labels = {
        "api-lifecycle": "API lifecycle",
        "apiops": "APIOps",
        "kubernetes": "Kubernetes",
        "mule-migration": "Mule migration",
        "operations-support": "Operations & support",
        "resilience-performance": "Resilience & performance",
        "traffic-policy": "Traffic & policy",
    }
    return labels.get(value.casefold(), value.replace("-", " ").capitalize())


def count_series(values: list[str]) -> list[dict[str, object]]:
    counts = Counter(value.strip() for value in values if value and value.strip())
    return [
        {"label": label, "value": value}
        for label, value in sorted(counts.items(), key=lambda item: (-item[1], item[0].casefold()))
    ]


def simple_yaml_numbers(path: Path) -> dict[str, int]:
    """Parse the repository's flat numeric weight map without a YAML dependency."""
    values: dict[str, int] = {}
    for line in safe_text(path).splitlines():
        match = re.match(r"^\s*([a-z0-9-]+)\s*:\s*(\d+)\s*(?:#.*)?$", line, flags=re.IGNORECASE)
        if match:
            values[match.group(1)] = int(match.group(2))
    return values


def criteria_visuals() -> dict[str, object]:
    rows = count_csv_rows(ROOT / "decision-matrix" / "criteria.csv")
    category_weights = simple_yaml_numbers(ROOT / "decision-matrix" / "weights.yaml")
    categories: dict[str, list[dict[str, str]]] = {}
    for row in rows:
        category = row.get("category", "").strip()
        if category:
            categories.setdefault(category, []).append(row)

    category_rows: list[dict[str, object]] = []
    for category, criteria in categories.items():
        requirement_types = [row.get("requirement_type", "").strip().casefold() for row in criteria]
        category_rows.append(
            {
                "id": category,
                "label": label_for(category),
                "total": len(criteria),
                "mandatory": requirement_types.count("mandatory"),
                "weighted": requirement_types.count("weighted"),
                "criterionWeight": sum(integer(row.get("default_weight", "")) for row in criteria),
                "categoryWeight": category_weights.get(category),
            }
        )

    requirement_types = [row.get("requirement_type", "").strip().casefold() for row in rows]
    return {
        "total": len(rows),
        "mandatory": requirement_types.count("mandatory"),
        "weighted": requirement_types.count("weighted"),
        "statuses": count_series([label_for(row.get("status", "")) for row in rows]),
        "categories": category_rows,
        "categoryWeightStatus": "Workshop defaults; not approved",
        "categoryWeightTotal": sum(category_weights.values()),
    }


def scorecard_status(path: Path) -> tuple[str, str]:
    text = safe_text(path)
    match = re.search(r"^Status:\s*\*\*([^*]+)\*\*\.?\s*(.*)$", text, flags=re.MULTILINE | re.IGNORECASE)
    if not match:
        return "Unscored", "Awaiting criterion-level evidence."
    source_status = clean_inline(match.group(1)).casefold()
    if source_status in {"not scored", "unscored"}:
        status = "Unscored"
    elif source_status.startswith("awaiting"):
        # "Awaiting evidence" is still an unscored decision state. Keep the
        # evidence condition in its own field so the comparison view does not
        # imply that one candidate has progressed further than the others.
        status = "Unscored"
    else:
        status = label_for(source_status)
    note = re.sub(r"\s+([.,;:])", r"\1", clean_inline(match.group(2))) or "Awaiting criterion-level evidence."
    return status, note


def variant_scorecard(name: str) -> Path | None:
    normalized = name.casefold()
    if "kong" in normalized:
        return ROOT / "decision-matrix" / "kong-scorecard.md"
    if "apim" in normalized:
        return ROOT / "decision-matrix" / "azure-apim-scorecard.md"
    if "apigee" in normalized:
        return ROOT / "decision-matrix" / "apigee-scorecard.md"
    if "mulesoft" in normalized:
        return ROOT / "decision-matrix" / "mulesoft-baseline.md"
    return None


def variants_visuals() -> list[dict[str, object]]:
    text = safe_text(ROOT / "decision-matrix" / "README.md")
    section = re.search(r"^##\s+Variants scored separately\s*$([\s\S]*?)(?=^##\s+|\Z)", text, flags=re.MULTILINE | re.IGNORECASE)
    variant_names = re.findall(r"^\s*\d+\.\s+(.+?)\s*$", section.group(1), flags=re.MULTILINE) if section else []
    variants: list[dict[str, object]] = []
    for raw_name in variant_names:
        name = clean_inline(raw_name)
        scorecard = variant_scorecard(name)
        if scorecard and scorecard.exists():
            status, note = scorecard_status(scorecard)
            source = scorecard.relative_to(ROOT).as_posix()
        else:
            status = "Unscored"
            note = "Awaiting criterion-level evidence; no populated scorecard is present."
            source = "decision-matrix/README.md"
        variants.append(
            {
                "name": name,
                "status": status,
                "note": note,
                "evidenceStatus": "Awaiting evidence",
                "source": source,
            }
        )
    return variants


def sources_visuals() -> dict[str, object]:
    rows = count_csv_rows(ROOT / "research" / "sources.csv")
    findings_text = safe_text(ROOT / "research" / "findings.md")
    source_ids = [row.get("source_id", "").strip() for row in rows if row.get("source_id", "").strip()]
    used_ids = [
        source_id
        for source_id in source_ids
        if re.search(rf"(?<![A-Z0-9-]){re.escape(source_id)}(?![A-Z0-9-])", findings_text, flags=re.IGNORECASE)
    ]
    used_set = set(used_ids)
    unused_ids = [source_id for source_id in source_ids if source_id not in used_set]
    return {
        "total": len(rows),
        "byVendor": count_series([row.get("vendor", "") for row in rows]),
        "byProduct": count_series([row.get("product", "") for row in rows]),
        "usedInFindings": len(used_ids),
        "unusedInFindings": len(unused_ids),
        "usedSourceIds": used_ids,
        "unusedSourceIds": unused_ids,
        "usageDefinition": "Explicit source IDs cited in research/findings.md; aggregate labels such as 'All' are not expanded.",
    }


def findings_visuals() -> dict[str, object]:
    text = safe_text(ROOT / "research" / "findings.md")
    rows = markdown_table(text, ("ID", "State", "Claim", "Sources"))
    return {
        "total": len(rows),
        "byState": count_series([row_value(row, "State") for row in rows]),
    }


def poc_visuals() -> dict[str, object]:
    text = safe_text(ROOT / "poc" / "test-plan.md")
    rows = markdown_table(text, ("ID", "Test", "Baseline status", "Exit evidence"))
    tests = [
        {
            "id": row_value(row, "ID"),
            "label": row_value(row, "Test"),
            "status": row_value(row, "Baseline status"),
            "evidence": row_value(row, "Exit evidence"),
        }
        for row in rows
    ]
    return {
        "total": len(tests),
        "byStatus": count_series([str(test["status"]) for test in tests]),
        "tests": tests,
    }


def governance_visuals() -> dict[str, object]:
    assumptions_text = safe_text(ROOT / "docs" / "02-current-state-assumptions.md")
    assumption_rows = markdown_table(assumptions_text, ("ID", "Assumption", "Status"))

    adr_statuses: list[str] = []
    for path in sorted((ROOT / "adr").glob("*.md")):
        if path.name.casefold() == "readme.md":
            continue
        match = re.search(r"^-\s*Status:\s*(.+?)\s*$", safe_text(path), flags=re.MULTILINE | re.IGNORECASE)
        if match:
            adr_statuses.append(label_for(clean_inline(match.group(1))))

    risks_text = safe_text(ROOT / "docs" / "37-risks.md")
    risk_rows = markdown_table(risks_text, ("ID", "Risk", "Owner"))
    questions_text = safe_text(ROOT / "docs" / "38-open-questions.md")
    open_questions = len(re.findall(r"^\s*\d+\.\s+\S", questions_text, flags=re.MULTILINE))
    return {
        "assumptions": count_series([label_for(row_value(row, "Status")) for row in assumption_rows]),
        "adrs": count_series(adr_statuses),
        "risksByOwner": count_series([row_value(row, "Owner") for row in risk_rows]),
        "openQuestions": open_questions,
        "assumptionTotal": len(assumption_rows),
        "adrTotal": len(adr_statuses),
        "riskTotal": len(risk_rows),
    }


def library_visuals(items: list[dict[str, object]]) -> dict[str, object]:
    return {
        "bySection": count_series([str(item.get("section", "")) for item in items]),
        "byType": count_series([str(item.get("type", "")) for item in items]),
    }


def roadmap_visuals() -> dict[str, object]:
    text = safe_text(ROOT / "docs" / "36-implementation-roadmap.md")
    rows = markdown_table(text, ("Phase", "Indicative duration", "Exit criteria"))
    return {
        "phases": [
            {
                "label": row_value(row, "Phase"),
                "duration": clean_inline(row_value(row, "Indicative duration")),
                "exitCriteria": row_value(row, "Exit criteria"),
            }
            for row in rows
        ]
    }


def repository_roadmap_visuals() -> dict[str, object]:
    text = safe_text(ROOT / "docs" / "39-repository-roadmap.md")
    rows = markdown_table(text, ("Phase", "Status", "Primary outcome", "Exit gate"))
    return {
        "phases": [
            {
                "label": row_value(row, "Phase"),
                "duration": clean_inline(row_value(row, "Status")),
                "exitCriteria": (
                    f"{row_value(row, 'Primary outcome')} — {row_value(row, 'Exit gate')}"
                ).strip(" —"),
            }
            for row in rows
        ]
    }


def methodology_visuals() -> dict[str, object]:
    text = safe_text(ROOT / "docs" / "03-assessment-methodology.md")
    sequence = re.search(r"^##\s+Sequence\s*$([\s\S]*?)(?=^##\s+|\Z)", text, flags=re.MULTILINE | re.IGNORECASE)
    steps: list[dict[str, str]] = []
    if sequence:
        for label, description in re.findall(
            r"^\s*\d+\.\s+\*\*(.+?)\*\*:?\s*(.+?)\s*$", sequence.group(1), flags=re.MULTILINE
        ):
            steps.append({"label": clean_inline(label).rstrip(":"), "description": clean_inline(description)})

    level_rows = markdown_table(text, ("Level", "Evidence", "Permitted score confidence"))
    evidence_levels = [
        {
            "level": clean_inline(row_value(row, "Level")),
            "label": row_value(row, "Evidence"),
            "confidence": row_value(row, "Permitted score confidence"),
        }
        for row in level_rows
    ]
    return {"steps": steps, "evidenceLevels": evidence_levels}


def review_visuals() -> dict[str, object]:
    text = safe_text(ROOT / "reports" / "methodology-review.md")
    rows = markdown_table(text, ("Decision", "Principal recommendation", "Status", "Exit evidence"))
    return {
        "decisions": [
            {
                "name": row_value(row, "Decision"),
                "status": row_value(row, "Status"),
                "recommendation": row_value(row, "Principal recommendation"),
                "exitEvidence": row_value(row, "Exit evidence"),
                "evidenceStatus": (
                    f"{row_value(row, 'Principal recommendation')} — Exit: {row_value(row, 'Exit evidence')}"
                ).strip(" —"),
            }
            for row in rows
        ]
    }


def visual_provenance(items: list[dict[str, object]]) -> dict[str, dict[str, object]]:
    by_path = {str(item["path"]): str(item["id"]) for item in items}
    source_paths = {
        "criteria": ("decision-matrix/criteria.csv", "decision-matrix/weights.yaml"),
        "variants": ("decision-matrix/README.md",),
        "sources": ("research/sources.csv", "research/findings.md"),
        "findings": ("research/findings.md",),
        "poc": ("poc/test-plan.md",),
        "governance": ("docs/02-current-state-assumptions.md", "adr/README.md", "docs/37-risks.md", "docs/38-open-questions.md"),
        "roadmap": ("docs/36-implementation-roadmap.md",),
        "repositoryRoadmap": ("docs/39-repository-roadmap.md",),
        "methodology": ("docs/03-assessment-methodology.md",),
        "review": ("reports/methodology-review.md",),
    }
    provenance: dict[str, dict[str, object]] = {}
    for key, paths in source_paths.items():
        available = [path for path in paths if path in by_path]
        if not available:
            continue
        provenance[key] = {
            "sourcePath": available[0],
            "sourceId": by_path[available[0]],
            "sourcePaths": available,
            "sourceIds": [by_path[path] for path in available],
        }
    provenance["library"] = {
        "sourcePath": "content-manifest.json",
        "sourceHref": "content-manifest.json",
        "sourcePaths": ["content-manifest.json"],
        "sourceIds": [],
    }
    return provenance


def build_visuals(items: list[dict[str, object]]) -> dict[str, object]:
    """Build chart-ready data exclusively from tracked repository content."""
    return {
        "criteria": criteria_visuals(),
        "variants": variants_visuals(),
        "sources": sources_visuals(),
        "findings": findings_visuals(),
        "poc": poc_visuals(),
        "governance": governance_visuals(),
        "library": library_visuals(items),
        "roadmap": roadmap_visuals(),
        "repositoryRoadmap": repository_roadmap_visuals(),
        "methodology": methodology_visuals(),
        "review": review_visuals(),
        "provenance": visual_provenance(items),
    }


def build_audiences(
    items: list[dict[str, object]],
    stats: dict[str, int],
    visuals: dict[str, object],
    presentation: list[dict[str, object]],
) -> list[dict[str, object]]:
    """Build six role-specific lenses over the same canonical evidence."""
    by_path = {str(item["path"]): str(item["id"]) for item in items}
    valid_slide_keys = {str(slide.get("key", "")) for slide in presentation}

    criteria = visuals.get("criteria", {})
    criteria = criteria if isinstance(criteria, dict) else {}
    variants = visuals.get("variants", [])
    variants = variants if isinstance(variants, list) else []
    methodology = visuals.get("methodology", {})
    methodology = methodology if isinstance(methodology, dict) else {}
    repository_roadmap = visuals.get("repositoryRoadmap", {})
    repository_roadmap = repository_roadmap if isinstance(repository_roadmap, dict) else {}
    poc = visuals.get("poc", {})
    poc = poc if isinstance(poc, dict) else {}
    governance = visuals.get("governance", {})
    governance = governance if isinstance(governance, dict) else {}

    def length(value: object) -> int:
        return len(value) if isinstance(value, list) else 0

    def series_value(value: object, label: str) -> int:
        if not isinstance(value, list):
            return 0
        for item in value:
            if isinstance(item, dict) and str(item.get("label", "")).casefold() == label.casefold():
                count = item.get("value", 0)
                return count if isinstance(count, int) else 0
        return 0

    def audience(
        *,
        audience_id: str,
        label: str,
        short_label: str,
        group: str,
        verb: str,
        framing: str,
        decision: str,
        action: str,
        questions: tuple[str, ...],
        signals: tuple[tuple[str, int], ...],
        source_paths: tuple[str, ...],
        recommended_route: str,
        visual: str,
        presentation_slides: tuple[str, ...],
    ) -> dict[str, object]:
        missing_sources = [path for path in source_paths if path not in by_path]
        if missing_sources:
            raise ValueError(f"Audience {audience_id} references missing sources: {missing_sources}")
        missing_slides = [key for key in presentation_slides if key not in valid_slide_keys]
        if missing_slides:
            raise ValueError(f"Audience {audience_id} references unknown slides: {missing_slides}")
        return {
            "id": audience_id,
            "label": label,
            "shortLabel": short_label,
            "group": group,
            "verb": verb,
            "framing": framing,
            "decision": decision,
            "action": action,
            "questions": list(questions),
            "signals": [{"label": signal_label, "value": value} for signal_label, value in signals],
            "sourceIds": [by_path[path] for path in source_paths],
            "sourcePaths": list(source_paths),
            "recommendedRoute": recommended_route,
            "visual": visual,
            "presentationSlides": list(presentation_slides),
            "presentationRoute": f"#/present/{audience_id}/0",
        }

    unscored_variants = sum(
        1
        for variant in variants
        if isinstance(variant, dict) and str(variant.get("status", "")).casefold() == "unscored"
    )
    unknown_criteria = series_value(criteria.get("statuses"), "Unknown")
    evidenced_criteria = max(stats.get("criteria", 0) - unknown_criteria, 0)
    not_run_scenarios = series_value(poc.get("byStatus"), "Not run")
    automated_scenarios = series_value(poc.get("byStatus"), "Automated")
    open_assumptions = series_value(governance.get("assumptions"), "Open")
    proposed_adrs = series_value(governance.get("adrs"), "Proposed")

    return [
        audience(
            audience_id="vp-executive",
            label="VP / Executive",
            short_label="Executive",
            group="Leadership",
            verb="Decide",
            framing="Decision, risk, and investment view of the API management study.",
            decision="Is a platform decision supportable now, and which gates must close before investment is approved?",
            action="Approve the decision contract and 90-day evidence-closure phase—not a vendor selection.",
            questions=(
                "What decision is requested now, and what is explicitly not being approved?",
                "Which mandatory gates, risks, economics, and exit conditions can still change the direction?",
                "Who owns the decision, evidence threshold, funding, and review date?",
            ),
            signals=(("Criteria with evidence", evidenced_criteria), ("Mandatory gates", stats.get("mandatoryGates", 0)), ("Unscored variants", unscored_variants), ("PoC scenarios not run", not_run_scenarios)),
            source_paths=("docs/00-executive-summary.md", "reports/methodology-review.md", "reports/evidence-state.md", "decision-matrix/findings.md", "decision-matrix/README.md", "docs/37-risks.md", "docs/36-implementation-roadmap.md", "docs/39-repository-roadmap.md"),
            recommended_route="#/compare",
            visual="executive",
            presentation_slides=("decision", "landscape", "evidence", "delivery", "next"),
        ),
        audience(
            audience_id="directors",
            label="Directors",
            short_label="Directors",
            group="Leadership",
            verb="Mobilize",
            framing="Portfolio, operating-model, capacity, and delivery-accountability view.",
            decision="What must be funded, staffed, governed, sequenced, and evidenced before the next investment gate?",
            action="Turn the roadmap into an accountable plan with public roles or owner IDs, restricted named owners, dates, capacity, dependencies, and exit evidence.",
            questions=("Who owns each workstream, assumption, risk, acceptance decision, and dependency?", "Which environments, people, commercial inputs, and pilots must be funded now?", "What evidence must each phase produce before the program receives more capacity?"),
            signals=(("Open assumptions", open_assumptions), ("Registered risks", stats.get("risks", 0)), ("Proposed ADRs", proposed_adrs), ("Repository phases", length(repository_roadmap.get("phases")))),
            source_paths=("docs/02-current-state-assumptions.md", "docs/33-operating-model.md", "docs/36-implementation-roadmap.md", "docs/37-risks.md", "docs/38-open-questions.md", "docs/39-repository-roadmap.md", "workshops/README.md", "mule-migration/migration-factory.md"),
            recommended_route="#/doc/docs-33-operating-model",
            visual="directors",
            presentation_slides=("decision", "evidence", "proof", "delivery", "next"),
        ),
        audience(
            audience_id="architects",
            label="Architects",
            short_label="Architects",
            group="Architecture",
            verb="Design",
            framing="Logical, deployment, transition, security, network, observability, and resilience view.",
            decision="Does the vendor-neutral logical architecture—and each candidate topology—satisfy the constraints?",
            action="Approve the capability boundary and vendor-neutral logical model before candidate physical topologies are scored.",
            questions=("Where is the gateway/integration boundary, and what must never move into policy?", "Which locality, residency, isolation, identity, network, and recovery constraints shape placement?", "Which current-state, data-flow, transition, and failure assumptions require evidence?"),
            signals=(("Architecture diagrams", stats.get("diagrams", 0)), ("Assessment categories", length(criteria.get("categories"))), ("Mandatory gates", stats.get("mandatoryGates", 0)), ("Evidence levels", length(methodology.get("evidenceLevels")))),
            source_paths=("architecture/current-state.md", "architecture/target-state.md", "docs/06-hybrid-cloud-requirements.md", "docs/07-api-gateway-vs-integration-runtime.md", "architecture/network-architecture.md", "architecture/security-architecture.md", "architecture/ha-dr-architecture.md", "adr/README.md"),
            recommended_route="#/architecture",
            visual="architects",
            presentation_slides=("decision", "target-state", "landscape", "system", "evidence", "proof"),
        ),
        audience(
            audience_id="developers",
            label="Developers",
            short_label="Developers",
            group="Engineering",
            verb="Build & consume",
            framing="API contract, APIOps, developer experience, policy boundary, and runnable proof view.",
            decision="Can teams design, publish, discover, secure, consume, change, and roll back APIs safely?",
            action="Prove the complete producer and consumer journeys, including approval, promotion, rollback, discovery, and credentials.",
            questions=("How does an API move from contract to production with ownership and breaking-change controls?", "How does a consumer discover, request, test, rotate credentials, and receive support?", "Which behavior belongs in gateway policy versus domain or integration code?"),
            signals=(("API contracts", stats.get("apiContracts", 0)), ("PoC scenarios", int(poc.get("total", 0)) if isinstance(poc.get("total", 0), int) else 0), ("Automated scenarios", automated_scenarios), ("Scenarios not run", not_run_scenarios)),
            source_paths=("docs/07-api-gateway-vs-integration-runtime.md", "docs/29-apiops-governance.md", "docs/30-developer-portal-api-products.md", "poc/README.md", "poc/apis/README.md", "poc/apiops-tests.md", "docs/35-mule-migration-strategy.md", "mule-migration/migration-patterns.md"),
            recommended_route="#/lab",
            visual="developers",
            presentation_slides=("decision", "system", "proof", "delivery"),
        ),
        audience(
            audience_id="devops-sre",
            label="DevOps / SRE",
            short_label="DevOps / SRE",
            group="Operations",
            verb="Operate & recover",
            framing="Runtime, delivery automation, telemetry, failure, performance, support, and recovery view.",
            decision="Can the runtime be operated, observed, recovered, upgraded, and supported under representative conditions?",
            action="Run Kubernetes, disconnection, failure, soak, telemetry, redaction, and recovery exercises against approved SLOs.",
            questions=("What happens during control-plane loss, restart, scaling, dependency failure, and recovery?", "Do telemetry, redaction, runbooks, support boundaries, and on-call demand meet the operating contract?", "Which SLO, RTO, RPO, load, and failure conditions must a representative pilot prove?"),
            signals=(("PoC scenarios", stats.get("pocScenarios", 0)), ("Scenarios not run", not_run_scenarios), ("Recorded risks", stats.get("risks", 0)), ("Architecture diagrams", stats.get("diagrams", 0))),
            source_paths=("architecture/observability-architecture.md", "architecture/ha-dr-architecture.md", "architecture/network-architecture.md", "poc/failure-tests.md", "poc/performance-tests.md", "poc/observability/README.md", "poc/kubernetes/README.md", "reports/validation-report.md"),
            recommended_route="#/lab",
            visual="devops-sre",
            presentation_slides=("target-state", "system", "proof", "delivery", "next"),
        ),
        audience(
            audience_id="platform-teams",
            label="Platform Teams",
            short_label="Platform",
            group="Platform enablement",
            verb="Enable & govern",
            framing="Platform-product, paved-road, tenancy, automation, governance, migration, and adoption view.",
            decision="What service catalogue, paved road, tenancy model, automation, and support contract can teams adopt repeatedly?",
            action="Define the platform product, support tiers, onboarding SLO, tenancy model, decision rights, and unit economics.",
            questions=("Where do platform and domain ownership, standards, shared services, and exceptions divide?", "Which exact variant has a sustainable upgrade, support, staffing, and cost model?", "What is the paved road for onboarding, tenancy, API operations, policy, and migration?"),
            signals=(("Unscored variants", unscored_variants), ("Current-state assumptions", stats.get("assumptions", 0)), ("Proposed ADRs", proposed_adrs), ("Decision criteria", stats.get("criteria", 0))),
            source_paths=("docs/33-operating-model.md", "docs/29-apiops-governance.md", "architecture/apiops-architecture.md", "architecture/kong-aks-architecture.md", "docs/12-kong-konnect-vs-self-managed.md", "decision-matrix/README.md", "poc/apiops-tests.md", "docs/39-repository-roadmap.md"),
            recommended_route="#/doc/docs-33-operating-model",
            visual="platform-teams",
            presentation_slides=("target-state", "landscape", "system", "proof", "delivery"),
        ),
    ]


def build_stats(items: list[dict[str, object]]) -> dict[str, int]:
    criteria = count_csv_rows(ROOT / "decision-matrix" / "criteria.csv")
    sources = count_csv_rows(ROOT / "research" / "sources.csv")
    question_text = safe_text(ROOT / "workshops" / "question-bank.md")
    scenario_text = safe_text(ROOT / "poc" / "test-plan.md")
    risks_text = safe_text(ROOT / "docs" / "37-risks.md")
    assumptions_text = safe_text(ROOT / "docs" / "02-current-state-assumptions.md")
    questions_text = safe_text(ROOT / "docs" / "38-open-questions.md")
    scenario_rows = markdown_table(scenario_text, ("ID", "Test", "Baseline status", "Exit evidence"))
    risk_rows = markdown_table(risks_text, ("ID", "Risk", "Early indicator", "Mitigation", "Owner"))
    assumption_rows = markdown_table(assumptions_text, ("ID", "Assumption", "Validation owner", "Status"))
    return {
        "resources": len(items),
        "studies": sum(1 for item in items if str(item["path"]).startswith("docs/") and re.match(r"docs/\d{2}-", str(item["path"]))),
        "diagrams": sum(1 for item in items if item["type"] == "mermaid"),
        "criteria": len(criteria),
        "mandatoryGates": sum(1 for row in criteria if row.get("requirement_type", "").lower() == "mandatory"),
        "sources": len(sources),
        "workshops": sum(1 for item in items if re.match(r"workshops/\d{2}-", str(item["path"]))),
        "questions": len(re.findall(r"^Q-\d{3}\.", question_text, flags=re.MULTILINE)),
        "apiContracts": sum(1 for item in items if item["type"] == "openapi"),
        "pocScenarios": len(scenario_rows),
        "risks": len(risk_rows),
        "assumptions": len(assumption_rows),
        "openQuestions": len(re.findall(r"^\s*\d+\.\s+", questions_text, flags=re.MULTILINE)),
    }


def make_presentation(items: list[dict[str, object]], stats: dict[str, int], visuals: dict[str, object]) -> list[dict[str, object]]:
    by_path = {str(item["path"]): str(item["id"]) for item in items}
    variant_total = len(visuals.get("variants", []))
    variant_scope = f"all {variant_total} variants" if variant_total else "all variants"
    roadmap_phase_total = len(visuals.get("roadmap", {}).get("phases", []))
    specs = [
        ("orientation", "Orientation", "A living evidence base for API management decisions", "Research, architecture, proof, and reusable delivery material in one navigable system.", "docs/00-executive-summary.md", stats["resources"], "indexed resources", "composition"),
        ("decision", "Decision", "Approve evidence closure—not platform selection", f"Run one evidence-led screen across {variant_scope}, then fund symmetric proof only for approved finalists. Kong remains a low-confidence priority-validation hypothesis, not a selection.", "reports/methodology-review.md", "NOW", "evidence closure", "recommendation"),
        ("target-state", "Target state", "Workload-local data planes, centrally governed", "A vendor-neutral logical view keeps latency and failure boundaries near workloads while governance stays coherent; candidate physical views must prove their own control, persistence, telemetry, and support boundaries.", "architecture/diagrams/target-state.mmd", stats["diagrams"], "architecture views", "architectureDiagram"),
        ("landscape", "Landscape", "One hypothesis, several serious benchmarks", "Kong is the current priority-validation hypothesis; Azure API Management, Apigee, and the MuleSoft baseline remain explicit comparison points through the evidence-led down-select.", "docs/09-product-shortlist.md", variant_total, "deployment variants", "statusMatrix"),
        ("system", "System", "Make the transition reversible", "The transition view makes coexistence, weighted cutover, integration decomposition, rollback, and retirement evidence visible.", "architecture/diagrams/transition-state.mmd", stats["diagrams"], "renderable diagrams", "architectureDiagram"),
        ("evidence", "Evidence", "Unknown stays unknown", "Mandatory gates are scored before weighted preferences. Claims require authoritative evidence or execution proof.", "decision-matrix/criteria.csv", stats["mandatoryGates"], "mandatory gates", "donut"),
        ("research", "Research", "Trace claims back to sources", "The source register and finding states separate confirmed facts from interpretation, assumptions, risks, and recommendations.", "research/findings.md", stats["sources"], "official sources", "sourceBalance"),
        ("proof", "Proof", "Turn architecture claims into tests", "The PoC provides synthetic APIs, gateway configuration, observability hooks, and explicit security, performance, failure, and migration tests.", "poc/test-plan.md", stats["pocScenarios"], "PoC scenarios", "pocStatus"),
        ("delivery", "Delivery", "Move in controlled waves", "The roadmap combines discovery, evidence closure, PoC execution, operating-model design, migration waves, and decision gates.", "docs/36-implementation-roadmap.md", roadmap_phase_total, "roadmap phases", "roadmap"),
        ("next", "Next", "Close the evidence gaps that can change the decision", "Open questions remain first-class work. The portal is designed to expose uncertainty, not decorate it.", "docs/38-open-questions.md", stats["openQuestions"], "open questions", "governance"),
    ]
    return [
        {
            "index": index,
            "key": key,
            "eyebrow": eyebrow,
            "title": title,
            "body": body,
            "sourceId": by_path.get(path, ""),
            "metric": metric,
            "metricLabel": metric_label,
            "visual": visual,
        }
        for index, (key, eyebrow, title, body, path, metric, metric_label, visual) in enumerate(specs)
    ]


def build(output: Path) -> None:
    if not SITE_SOURCE.exists():
        raise SystemExit(f"Site source is missing: {SITE_SOURCE}")
    if output.exists():
        shutil.rmtree(output)
    shutil.copytree(SITE_SOURCE, output)
    items = collect_items(output)
    stats = build_stats(items)
    visuals = build_visuals(items)
    presentation = make_presentation(items, stats, visuals)
    manifest = {
        "site": {"title": "API Management Studies", "description": "A living research, architecture, comparison, and proof-of-concept library."},
        "generatedAt": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "stats": stats,
        "visuals": visuals,
        "audiences": build_audiences(items, stats, visuals, presentation),
        "items": items,
        "presentation": presentation,
    }
    (output / "content-manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (output / ".nojekyll").touch()
    shutil.copy2(output / "index.html", output / "404.html")
    print(f"Built {output} with {len(items)} resources")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "_site", help="Output directory")
    args = parser.parse_args()
    output = args.output if args.output.is_absolute() else ROOT / args.output
    build(output.resolve())


if __name__ == "__main__":
    main()
