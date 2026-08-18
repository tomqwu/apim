#!/usr/bin/env python3
import csv
import pathlib
import re
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from repository_inventory import git_environment


root = pathlib.Path(__file__).resolve().parents[1]
with (root / "decision-matrix" / "criteria.csv").open(newline="", encoding="utf-8") as handle:
    criteria = list(csv.DictReader(handle))
questions = (root / "workshops" / "question-bank.md").read_text(encoding="utf-8")
question_ids = re.findall(r"^Q-(\d{3})\.", questions, flags=re.MULTILINE)

errors = []
if len(criteria) != 120:
    errors.append(f"expected 120 criteria; found {len(criteria)}")
if len({row["criterion_id"] for row in criteria}) != 120:
    errors.append("criterion IDs are not unique")
if len(question_ids) != 180:
    errors.append(f"expected 180 questions; found {len(question_ids)}")
if len(set(question_ids)) != 180:
    errors.append("question IDs are not unique")

review_path = root / "reports" / "content-research-principal-review.md"
backlog_path = root / "reports" / "content-remediation-backlog.csv"
if not review_path.exists():
    errors.append("missing canonical content/research principal review")
if not backlog_path.exists():
    errors.append("missing content remediation backlog")

backlog = []
if backlog_path.exists():
    required_field_order = [
        "recommendation_id",
        "priority",
        "workstream",
        "scope",
        "current_problem",
        "required_remediation",
        "acceptance_evidence",
        "dependencies",
        "owner_role",
        "status",
        "target_gate",
        "target_date",
        "closure_evidence",
        "reviewer_role",
        "review_status",
        "blocker",
        "disposition",
        "replacement_id",
    ]
    with backlog_path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        actual_field_order = reader.fieldnames or []
        backlog = list(reader)
    required_fields = set(required_field_order)
    actual_fields = set(actual_field_order)
    if actual_field_order != required_field_order:
        errors.append("content remediation backlog columns must exactly match the governed 18-column order")
    missing_fields = sorted(required_fields - actual_fields)
    if missing_fields:
        errors.append(f"content remediation backlog is missing fields: {', '.join(missing_fields)}")
    unexpected_fields = sorted((actual_fields - required_fields), key=str)
    if unexpected_fields:
        errors.append(
            "content remediation backlog has unexpected fields: "
            + ", ".join(str(field) for field in unexpected_fields)
        )
    for row_number, row in enumerate(backlog, start=2):
        if None in row or set(row) != required_fields:
            errors.append(f"content remediation backlog row {row_number} does not have exactly 18 cells")

    backlog_ids = [row.get("recommendation_id", "") for row in backlog]
    if not backlog:
        errors.append("content remediation backlog is empty")
    if len(backlog_ids) != len(set(backlog_ids)):
        errors.append("content remediation recommendation IDs are not unique")
    invalid_ids = sorted(identifier for identifier in backlog_ids if not re.fullmatch(r"PCR-\d{3}", identifier))
    if invalid_ids:
        errors.append(f"invalid content remediation recommendation IDs: {', '.join(invalid_ids)}")
    expected_ids = [f"PCR-{index:03d}" for index in range(1, len(backlog_ids) + 1)]
    if backlog_ids != expected_ids:
        errors.append("content remediation recommendation IDs must remain consecutive and ordered")
    protected_ids = {f"PCR-{index:03d}" for index in range(1, 69)}
    missing_protected_ids = sorted(protected_ids - set(backlog_ids))
    if missing_protected_ids:
        errors.append(
            "canonical baseline recommendation IDs cannot be removed: "
            + ", ".join(missing_protected_ids)
        )
    backlog_id_set = set(backlog_ids)

    try:
        tracked_result = subprocess.run(
            ["git", "ls-files", "-z"],
            cwd=root,
            env=git_environment(),
            check=True,
            capture_output=True,
            text=True,
        )
        tracked_paths = {path for path in tracked_result.stdout.split("\0") if path}
    except (OSError, subprocess.CalledProcessError):
        tracked_paths = set()
        errors.append("cannot inspect tracked files for remediation closure evidence")

    def validate_closure_reference(identifier, value):
        references = [reference.strip() for reference in value.split(";") if reference.strip()]
        if not references:
            errors.append(f"{identifier} has no parseable closure evidence references")
            return
        for reference in references:
            if reference.startswith("path:"):
                raw_path = reference.removeprefix("path:")
                if "#" in raw_path:
                    errors.append(f"{identifier} closure evidence path does not support fragments: {reference}")
                    continue
                relative_path = pathlib.PurePosixPath(raw_path)
                if not raw_path or relative_path.is_absolute() or ".." in relative_path.parts:
                    errors.append(f"{identifier} has unsafe closure evidence path {reference}")
                    continue
                normalized_path = relative_path.as_posix()
                candidate = (root / normalized_path).resolve()
                try:
                    candidate.relative_to(root.resolve())
                except ValueError:
                    errors.append(f"{identifier} closure evidence escapes the repository: {reference}")
                    continue
                if normalized_path not in tracked_paths or not candidate.is_file():
                    errors.append(f"{identifier} closure evidence path is not a tracked file: {reference}")
            elif reference.startswith("commit:"):
                commit = reference.removeprefix("commit:")
                if not re.fullmatch(r"[0-9a-fA-F]{40}", commit):
                    errors.append(f"{identifier} has invalid immutable commit reference {reference}")
                    continue
                result = subprocess.run(
                    ["git", "cat-file", "-e", f"{commit}^{{commit}}"],
                    cwd=root,
                    env=git_environment(),
                    capture_output=True,
                    text=True,
                )
                if result.returncode != 0:
                    errors.append(f"{identifier} closure evidence commit does not resolve: {reference}")
            elif reference.startswith("restricted:"):
                restricted_reference = reference.removeprefix("restricted:")
                if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._:/-]+", restricted_reference):
                    errors.append(f"{identifier} has invalid restricted evidence reference {reference}")
            elif reference.startswith("external:"):
                if not re.fullmatch(r"external:https://\S+#sha256=[0-9a-fA-F]{64}", reference):
                    errors.append(f"{identifier} external closure evidence requires HTTPS and sha256: {reference}")
            else:
                errors.append(
                    f"{identifier} closure evidence must use path:, commit:, restricted:, or external: reference syntax"
                )

    allowed_priorities = {"P0", "P1", "P2"}
    allowed_statuses = {"backlog", "in-progress", "blocked", "done"}
    allowed_review_statuses = {"not-reviewed", "pending", "accepted", "changes-requested"}
    allowed_dispositions = {"open", "accepted", "superseded", "rejected"}
    dependency_graph = {}
    replacement_graph = {}
    for row in backlog:
        identifier = row.get("recommendation_id", "<missing>")
        if row.get("priority") not in allowed_priorities:
            errors.append(f"{identifier} has invalid priority")
        if row.get("status") not in allowed_statuses:
            errors.append(f"{identifier} has invalid status")
        if row.get("review_status") not in allowed_review_statuses:
            errors.append(f"{identifier} has invalid review_status")
        if row.get("disposition") not in allowed_dispositions:
            errors.append(f"{identifier} has invalid disposition")
        for field in required_fields:
            value = row.get(field)
            if not isinstance(value, str) or not value.strip():
                errors.append(f"{identifier} has empty {field}")

        dependency_value = row.get("dependencies") or ""
        dependency_value = dependency_value.strip()
        dependencies = [] if dependency_value == "none" else dependency_value.split(";")
        dependency_graph[identifier] = dependencies
        for dependency in dependencies:
            if dependency not in backlog_id_set:
                errors.append(f"{identifier} references unknown dependency {dependency}")
            if dependency == identifier:
                errors.append(f"{identifier} cannot depend on itself")

        status = row.get("status")
        review_status = row.get("review_status")
        disposition = row.get("disposition")
        blocker = row.get("blocker")
        replacement_id = row.get("replacement_id")
        if status in {"in-progress", "done"} and row.get("target_gate") == "TBD" and row.get("target_date") == "TBD":
            errors.append(f"{identifier} requires a target gate or date before work starts")
        if status == "blocked" and blocker == "none":
            errors.append(f"{identifier} requires a blocker reason when blocked")
        if status == "done":
            if row.get("closure_evidence") == "none":
                errors.append(f"{identifier} requires closure evidence before done")
            else:
                validate_closure_reference(identifier, row.get("closure_evidence") or "")
            if review_status != "accepted":
                errors.append(f"{identifier} requires independent accepted review before done")
            if disposition not in {"accepted", "superseded", "rejected"}:
                errors.append(f"{identifier} requires a closed disposition before done")
            if blocker != "none":
                errors.append(f"{identifier} cannot be done with an active blocker")
            if row.get("reviewer_role") == row.get("owner_role"):
                errors.append(f"{identifier} closure reviewer must be independent of owner role")
        elif disposition != "open":
            errors.append(f"{identifier} cannot have a closed disposition before done")
        if review_status == "accepted" and status != "done":
            errors.append(f"{identifier} cannot have accepted closure review before done")
        if disposition == "superseded":
            if replacement_id == "none":
                errors.append(f"{identifier} requires replacement_id when superseded")
            elif replacement_id not in backlog_id_set:
                errors.append(f"{identifier} references unknown replacement_id {replacement_id}")
            elif replacement_id == identifier:
                errors.append(f"{identifier} cannot supersede itself")
            else:
                replacement_graph[identifier] = replacement_id
        elif replacement_id != "none":
            errors.append(f"{identifier} has replacement_id without superseded disposition")

    visiting = set()
    visited = set()

    def visit_dependency(identifier, path):
        if identifier in visiting:
            cycle = " -> ".join(path + [identifier])
            errors.append(f"content remediation dependency cycle: {cycle}")
            return
        if identifier in visited:
            return
        visiting.add(identifier)
        for dependency in dependency_graph.get(identifier, []):
            if dependency in dependency_graph:
                visit_dependency(dependency, path + [identifier])
        visiting.remove(identifier)
        visited.add(identifier)

    for identifier in backlog_ids:
        visit_dependency(identifier, [])

    replacement_visiting = set()
    replacement_visited = set()

    def visit_replacement(identifier, path):
        if identifier in replacement_visiting:
            cycle = " -> ".join(path + [identifier])
            errors.append(f"content remediation replacement cycle: {cycle}")
            return
        if identifier in replacement_visited:
            return
        replacement_visiting.add(identifier)
        replacement = replacement_graph.get(identifier)
        if replacement:
            visit_replacement(replacement, path + [identifier])
        replacement_visiting.remove(identifier)
        replacement_visited.add(identifier)

    for identifier in backlog_ids:
        visit_replacement(identifier, [])

    row_by_id = {row.get("recommendation_id"): row for row in backlog}

    def resolves_to_accepted(identifier, path=None):
        path = path or set()
        if identifier in path:
            return False
        row = row_by_id.get(identifier, {})
        if row.get("status") != "done" or row.get("review_status") != "accepted":
            return False
        disposition = row.get("disposition")
        if disposition == "accepted":
            return True
        if disposition == "superseded":
            replacement = row.get("replacement_id")
            if not replacement or replacement == "none":
                return False
            return resolves_to_accepted(replacement, path | {identifier})
        return False

    for row in backlog:
        if row.get("status") != "done":
            continue
        identifier = row.get("recommendation_id", "<missing>")
        if row.get("disposition") == "superseded" and not resolves_to_accepted(identifier):
            errors.append(f"{identifier} supersession chain must resolve to an independently accepted replacement")
        for dependency in dependency_graph.get(identifier, []):
            if not resolves_to_accepted(dependency):
                errors.append(
                    f"{identifier} cannot close before dependency {dependency} resolves to an independently accepted disposition"
                )

    if review_path.exists():
        review_text = review_path.read_text(encoding="utf-8")
        review_entries = re.findall(
            r"^###\s+(PCR-\d{3})\s+—\s+.+\s+\((P[0-2])\)\s*$",
            review_text,
            flags=re.MULTILINE,
        )
        review_heading_ids = [identifier for identifier, _ in review_entries]
        review_ids = set(re.findall(r"\bPCR-\d{3}\b", review_text))
        backlog_id_set = set(backlog_ids)
        missing_from_review = sorted(backlog_id_set - review_ids)
        missing_from_backlog = sorted(review_ids - backlog_id_set)
        if missing_from_review:
            errors.append(f"backlog IDs missing from principal review: {', '.join(missing_from_review)}")
        if missing_from_backlog:
            errors.append(f"principal review IDs missing from backlog: {', '.join(missing_from_backlog)}")
        if review_heading_ids != backlog_ids:
            errors.append("principal review recommendation headings must match backlog ID order")
        report_sections = re.split(
            r"(?=^###\s+PCR-\d{3}\s+—\s+)",
            review_text,
            flags=re.MULTILINE,
        )
        section_by_id = {}
        for section in report_sections:
            match = re.match(r"^###\s+(PCR-\d{3})\s+—\s+.+\s+\((P[0-2])\)\s*$", section, flags=re.MULTILINE)
            if match:
                section_by_id[match.group(1)] = section

        report_field_labels = {
            "Workstream": "workstream",
            "Scope": "scope",
            "Finding": "current_problem",
            "Required remediation": "required_remediation",
            "Exit evidence": "acceptance_evidence",
            "Dependencies": "dependencies",
            "Accountable role": "owner_role",
        }
        for row, (identifier, priority) in zip(backlog, review_entries):
            if row.get("recommendation_id") != identifier or row.get("priority") != priority:
                errors.append(f"{identifier} priority differs between principal review and backlog")
            section = section_by_id.get(identifier, "")
            for label, field in report_field_labels.items():
                match = re.search(rf"^- \*\*{re.escape(label)}:\*\* (.+)$", section, flags=re.MULTILINE)
                if not match:
                    errors.append(f"{identifier} is missing report field {label}")
                elif match.group(1).strip() != row.get(field, "").strip():
                    errors.append(f"{identifier} {field} differs between principal review and backlog")

if errors:
    print("ERROR: " + "; ".join(errors), file=sys.stderr)
    raise SystemExit(1)
print(
    "OK: 120 unique criteria, 180 unique workshop questions, "
    f"and {len(backlog)} traceable content-remediation recommendations"
)
