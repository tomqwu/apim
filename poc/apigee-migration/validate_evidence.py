#!/usr/bin/env python3
"""Fail-closed structural and threshold validation for APIG-M01 through APIG-M04."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
PROTOCOL_PATH = ROOT / "protocols.json"
FULL_SHA = re.compile(r"^[0-9a-f]{40}$")
SHA256 = re.compile(r"^[0-9a-f]{64}$")
UTC_TIME = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")


class EvidenceError(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise EvidenceError(message)


def has_symlink_component(path: Path) -> bool:
    current = Path(path.anchor) if path.is_absolute() else Path()
    for part in path.parts[1:] if path.is_absolute() else path.parts:
        current = current / part
        if current.is_symlink():
            return True
    return False


def load_json(path: Path) -> dict[str, Any]:
    require(path.is_file() and not has_symlink_component(path), f"not a regular non-symlinked file: {path}")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise EvidenceError(f"invalid JSON: {path}") from exc
    require(isinstance(value, dict), f"JSON root must be an object: {path}")
    return value


def protocol_map(spec: dict[str, Any]) -> dict[str, dict[str, Any]]:
    require(spec.get("schemaVersion") == 1, "protocol schemaVersion must be 1")
    require(spec.get("evidenceState") == "not-run", "protocol catalog must remain not-run")
    rows = spec.get("protocols")
    require(isinstance(rows, list), "protocols must be a list")
    ids = [row.get("id") for row in rows if isinstance(row, dict)]
    require(ids == ["APIG-M01", "APIG-M02", "APIG-M03", "APIG-M04"], "protocol IDs must be APIG-M01 through APIG-M04")
    return {str(row["id"]): row for row in rows}


def threshold_passes(actual: Any, operator: str, expected: Any) -> bool:
    if operator == "eq":
        return type(actual) is type(expected) and actual == expected
    if operator == "gte":
        return type(actual) in {int, float} and not isinstance(actual, bool) and actual >= expected
    raise EvidenceError(f"unsupported threshold operator: {operator}")


def validated_artifact(root: Path, row: dict[str, Any], required_name: str) -> None:
    require(row.get("name") == required_name, f"artifact order/name mismatch; expected {required_name}")
    relative = row.get("path")
    digest = row.get("sha256")
    require(isinstance(relative, str) and bool(relative) and not Path(relative).is_absolute(), f"{required_name}: path must be non-empty and relative")
    require(isinstance(digest, str) and bool(SHA256.fullmatch(digest)), f"{required_name}: invalid SHA-256")
    candidate = root / relative
    require(not has_symlink_component(candidate), f"{required_name}: artifact path contains a symlink")
    path = candidate.resolve()
    try:
        path.relative_to(root.resolve())
    except ValueError as exc:
        raise EvidenceError(f"{required_name}: path escapes evidence directory") from exc
    require(path.is_file(), f"{required_name}: artifact is missing or irregular")
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    require(actual == digest, f"{required_name}: artifact SHA-256 mismatch")


def validate_record(record: dict[str, Any], protocol: dict[str, Any], *, artifact_root: Path | None) -> None:
    protocol_id = str(protocol["id"])
    require(record.get("schemaVersion") == 1, f"{protocol_id}: schemaVersion must be 1")
    require(record.get("protocolId") == protocol_id, f"{protocol_id}: protocolId mismatch")
    require(record.get("evidenceState") == "executed", f"{protocol_id}: evidenceState must be executed")
    for key in ("exactSourceOption", "exactTargetOption"):
        value = record.get(key)
        require(isinstance(value, str) and len(value.strip()) >= 12 and "unknown" not in value.lower(), f"{protocol_id}: {key} is not exact")
    require(isinstance(record.get("executedAtUtc"), str) and bool(UTC_TIME.fullmatch(record["executedAtUtc"])), f"{protocol_id}: executedAtUtc must be an exact UTC timestamp")
    require(isinstance(record.get("candidateRevision"), str) and bool(FULL_SHA.fullmatch(record["candidateRevision"])), f"{protocol_id}: candidateRevision must be a full Git SHA")

    measurements = record.get("measurements")
    required = protocol.get("requiredMeasurements")
    require(isinstance(measurements, dict) and isinstance(required, dict), f"{protocol_id}: measurements are invalid")
    require(set(measurements) == set(required), f"{protocol_id}: measurements must exactly match the protocol")
    for name, threshold in required.items():
        require(isinstance(threshold, dict), f"{protocol_id}: invalid threshold for {name}")
        require(
            threshold_passes(measurements[name], str(threshold.get("operator")), threshold.get("expected")),
            f"{protocol_id}: threshold failed for {name}",
        )

    required_artifacts = protocol.get("requiredArtifacts")
    artifacts = record.get("artifacts")
    require(isinstance(required_artifacts, list) and isinstance(artifacts, list), f"{protocol_id}: artifacts are invalid")
    require([row.get("name") for row in artifacts if isinstance(row, dict)] == required_artifacts, f"{protocol_id}: required artifacts are incomplete or out of order")
    if artifact_root is not None:
        for row, required_name in zip(artifacts, required_artifacts):
            require(isinstance(row, dict), f"{protocol_id}: artifact entry is invalid")
            validated_artifact(artifact_root, row, str(required_name))

    review = record.get("review")
    allowed_roles = protocol.get("independentReviewerRoles")
    require(isinstance(review, dict) and isinstance(allowed_roles, list), f"{protocol_id}: review is invalid")
    require(review.get("reviewerRole") in allowed_roles, f"{protocol_id}: reviewerRole is not authorized")
    require(review.get("independent") is True, f"{protocol_id}: reviewer must be independent")
    require(review.get("disposition") == "pass", f"{protocol_id}: reviewer disposition must be pass")
    review_url = review.get("reviewUrl")
    require(isinstance(review_url, str) and review_url.startswith("https://"), f"{protocol_id}: reviewUrl must be HTTPS")


def synthetic_record(protocol: dict[str, Any]) -> dict[str, Any]:
    required = protocol["requiredMeasurements"]
    return {
        "schemaVersion": 1,
        "protocolId": protocol["id"],
        "evidenceState": "executed",
        "exactSourceOption": "Synthetic self-test source option",
        "exactTargetOption": "Synthetic self-test target option",
        "executedAtUtc": "2026-08-24T00:00:00Z",
        "candidateRevision": "0" * 40,
        "measurements": {name: threshold["expected"] for name, threshold in required.items()},
        "artifacts": [{"name": name, "path": f"{name}.json", "sha256": "0" * 64} for name in protocol["requiredArtifacts"]],
        "review": {
            "reviewerRole": protocol["independentReviewerRoles"][0],
            "independent": True,
            "disposition": "pass",
            "reviewUrl": "https://example.invalid/synthetic-validator-self-test",
        },
    }


def self_test(protocols: dict[str, dict[str, Any]]) -> None:
    assertions = 0
    for protocol in protocols.values():
        record = synthetic_record(protocol)
        validate_record(record, protocol, artifact_root=None)
        assertions += 1
        first_name = next(iter(protocol["requiredMeasurements"]))
        expected = protocol["requiredMeasurements"][first_name]["expected"]
        record["measurements"][first_name] = False if expected is True else (-1 if expected == 0 else 0)
        try:
            validate_record(record, protocol, artifact_root=None)
        except EvidenceError:
            assertions += 1
        else:
            raise EvidenceError(f"{protocol['id']}: synthetic threshold violation was accepted")
    print(f"OK: {len(protocols)} Apigee migration protocol contracts and {assertions} synthetic validator assertions; product migration evidence remains not run")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--protocols", type=Path, default=PROTOCOL_PATH)
    parser.add_argument("--evidence", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    try:
        protocols = protocol_map(load_json(args.protocols.absolute()))
        require(args.self_test != bool(args.evidence), "choose exactly one of --self-test or --evidence")
        if args.self_test:
            self_test(protocols)
            return 0
        evidence_path = args.evidence.absolute()
        record = load_json(evidence_path)
        protocol_id = record.get("protocolId")
        require(protocol_id in protocols, "evidence protocolId is unknown")
        validate_record(record, protocols[str(protocol_id)], artifact_root=evidence_path.parent)
        print(f"OK: {protocol_id} evidence bundle satisfies the structural, threshold, artifact, and independent-review gate")
        return 0
    except EvidenceError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
