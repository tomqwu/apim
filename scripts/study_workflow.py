#!/usr/bin/env python3
"""Create and validate a public-safe, PR-backed study publication workflow."""

from __future__ import annotations

import argparse
import base64
import codecs
import hashlib
import html
import ipaddress
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unicodedata
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import quote, urlsplit

sys.path.insert(0, str(Path(__file__).resolve().parent))
from repository_inventory import git_environment


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "templates" / "study-intake-template.md"
CHECKPOINT_ROOT = ROOT / ".study-workflow" / "checkpoints"
SPEC_ROOT = ROOT / "workflow" / "intakes"
SCHEMA_VERSION = 2

SOURCE_KINDS = ("chat", "file", "url", "research", "poc", "repository")
ARTIFACT_TYPES = ("study", "evidence", "guide", "projection", "remediation", "workflow")
REPLACEABLE_LIST_FIELDS = (
    "audiences", "inputReferences", "evidenceReferences", "canonicalPaths", "derivedPaths",
    "reviewEvidenceUrls", "checkUrls", "cleanupEvidence", "manifestAssertions",
    "routeAssertions", "residualLimitations",
)
PHASES = ("draft", "release", "published")
STATES = (
    "INTAKE", "FRAMED", "RESEARCHED", "AUTHORED", "PROJECTED", "CANDIDATE",
    "REVIEWED", "VALIDATED", "MERGED", "PUBLISHED", "CLOSED", "REWORK", "BLOCKED",
)
REQUEST_ACTIONS = {
    "research", "edit", "branch", "commit", "push", "pull-request", "merge",
    "branch-cleanup", "pages-verification",
}
PHASE_REQUIRED_ACTIONS = {
    "draft": {"edit", "branch"},
    "release": {"edit", "branch", "commit", "push", "pull-request", "merge", "branch-cleanup"},
    "published": {"pull-request", "merge", "branch-cleanup", "pages-verification"},
}
REQUIRED_PR_CHECKS = {"static-validation", "docker-smoke"}
CANONICAL_ROOTS = {"docs", "research", "architecture", "poc", "reports", "decision-matrix", "adr", "templates"}
REQUIRED_REPO_FILES = (
    "AGENTS.md",
    "docs/46-study-publication-workflow.md",
    "templates/study-intake-template.md",
    ".agents/skills/publish-api-study/SKILL.md",
    ".agents/skills/publish-api-study/agents/openai.yaml",
    ".agents/skills/publish-api-study/references/repo-contract.md",
    ".github/pull_request_template.md",
    "config/public-content-allowlist.json",
    "scripts/repository_inventory.py",
    "scripts/validate_site_manifest.py",
    "scripts/verify_pages.py",
    "scripts/test_study_workflow.py",
    "requirements-validation.txt",
)
WORKFLOW_HEADINGS = (
    "## Non-negotiable operating contract",
    "## Workflow states and gates",
    "## Stage 0 — Preflight and authority",
    "## Stage 4 — Author canonical docs first",
    "## Stage 6 — Project the canon into site and presentation",
    "## Stage 8 — Independent review and PR validation",
    "## Stage 9 — Branch, pull request, merge, and cleanup",
    "## Stage 10 — Pages and live verification",
    "## Definition of done",
)
CHECKPOINT_KEYS = {
    "schemaVersion", "intakeId", "slug", "title", "sourceKind", "requestSummary",
    "decisionQuestion", "artifactType", "audiences", "scopeSummary", "deltaSummary",
    "requestedActions", "inputReferences", "evidenceReferences",
    "canonicalState", "statusReason", "repositoryRemote", "baseBranch", "baseSha", "branch",
    "checkpointCreatedAt", "updatedAt",
    "canonicalPaths", "derivedPaths", "localValidation", "localValidationDigest", "candidateSha", "candidateEnvelopeSha256", "prNumber",
    "prUrl", "prHeadSha", "prDraft", "reviewDisposition", "acceptedSha", "checkedSha",
    "reviewEvidenceUrls", "checkDisposition", "checkUrls", "mergeSha", "branchCleanupStatus",
    "cleanupEvidence", "mainValidationUrl", "pagesRunUrl", "manifestSha256", "closureEvidenceUrl",
    "liveBaseUrl", "manifestAssertions", "routeAssertions", "publicationStatus",
    "residualLimitations", "nextGate", "blockerOwnerRole", "responsibleStage",
}
FULL_SHA = re.compile(r"[0-9a-f]{40}")
SHA256 = re.compile(r"[0-9a-f]{64}")
SAFE_SLUG = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
UTC_TIMESTAMP = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z")
CHECKPOINT_START = "<!-- study-workflow-checkpoint:start -->"
CHECKPOINT_END = "<!-- study-workflow-checkpoint:end -->"
CHECKPOINT_PAYLOAD = "study-workflow-checkpoint-json"
CANDIDATE_ENVELOPE_FIELDS = (
    "schemaVersion", "intakeId", "slug", "title", "sourceKind", "requestSummary",
    "decisionQuestion", "artifactType", "audiences", "scopeSummary", "deltaSummary",
    "evidenceReferences", "canonicalPaths", "derivedPaths", "repositoryRemote",
    "baseBranch", "baseSha", "branch", "localValidationDigest", "candidateSha",
)
PUBLIC_ALLOWLIST = ROOT / "config" / "public-content-allowlist.json"
BINARY_EXTENSIONS = {
    ".7z", ".avi", ".doc", ".docx", ".gif", ".gz", ".ico", ".jpeg", ".jpg",
    ".mov", ".mp3", ".mp4", ".pdf", ".png", ".ppt", ".pptx", ".tar", ".webm",
    ".webp", ".xls", ".xlsx", ".zip",
}

TRANSITIONS = {
    "INTAKE": {"FRAMED", "BLOCKED"},
    "FRAMED": {"RESEARCHED", "REWORK", "BLOCKED"},
    "RESEARCHED": {"AUTHORED", "REWORK", "BLOCKED"},
    "AUTHORED": {"PROJECTED", "REWORK", "BLOCKED"},
    "PROJECTED": {"CANDIDATE", "REWORK", "BLOCKED"},
    "CANDIDATE": {"REVIEWED", "REWORK", "BLOCKED"},
    "REVIEWED": {"VALIDATED", "REWORK", "BLOCKED"},
    "VALIDATED": {"MERGED", "REWORK", "BLOCKED"},
    "MERGED": {"PUBLISHED"},
    "PUBLISHED": {"CLOSED"},
    "CLOSED": set(),
    "REWORK": {"INTAKE", "FRAMED", "RESEARCHED", "AUTHORED", "PROJECTED", "CANDIDATE", "BLOCKED"},
    "BLOCKED": {"INTAKE", "FRAMED", "RESEARCHED"},
}

# Keep rule IDs stable. Matched values are never printed.
PUBLIC_RULES = (
    ("PS001", "private key material", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
    ("PS002", "GitHub token", re.compile(r"\bgh[opusr]_[A-Za-z0-9_]{20,}\b")),
    ("PS003", "AWS access key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("PS004", "Slack token", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{20,}\b")),
    ("PS005", "local macOS path", re.compile(r"(?<![A-Za-z0-9_])/Users/[A-Za-z0-9._-]+/")),
    ("PS006", "local Windows path", re.compile(r"\b[A-Za-z]:\\Users\\[^\\\s]+\\")),
    ("PS007", "legacy organization branding", re.compile(r"\b(?:" + "E" + r"QB|" + "Equit" + r"able)\b", re.I)),
    ("PS008", "obsolete product branding", re.compile(r"\b" + "Nex" + r"us\s+API\b", re.I)),
    ("PS009", "generic bearer credential", re.compile(r"(?i)authorization\s*[:=]\s*bearer\s+[A-Za-z0-9._~+/=-]{20,}")),
    ("PS010", "private/internal hostname", re.compile(r"(?i)https?://[^\s/]+\.(?:internal|corp|local)(?::\d+)?(?:[/\s]|$)")),
    ("PS011", "GitHub fine-grained token", re.compile(r"\b" + "github" + r"_pat_[A-Za-z0-9_]{20,}\b")),
    ("PS012", "credential-bearing connection string", re.compile(r"(?i)\b(?:postgres(?:ql)?|mysql|mongodb(?:\+srv)?|redis)://[^/\s:@]+:[^@\s]+@")),
    ("PS013", "JWT-shaped credential", re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b")),
    ("PS021", "bidirectional text control", re.compile(r"[\u202a-\u202e\u2066-\u2069]")),
    ("PS025", "HTTP URL with embedded credentials", re.compile(r"(?i)\bhttps?://[^\s/?#]*@[^\s/?#]+")),
    ("PS026", "local Linux home path", re.compile(r"(?<![A-Za-z0-9_])/home/[A-Za-z0-9._-]+/")),
    (
        "PS027",
        "local macOS temporary attachment path",
        re.compile(r"(?<![A-Za-z0-9_])/(?:private/)?" + "var" + r"/folders/[A-Za-z0-9._-]+/"),
    ),
    (
        "PS030",
        "scheme-independent private hostname",
        re.compile(r"(?i)\b(?:[a-z0-9-]+\.)+(?:internal|corp|local)\b"),
    ),
    (
        "PS031",
        "RFC1918 private IPv4 address",
        re.compile(r"(?<![0-9])(?:10\.(?:[0-9]{1,3}\.){2}[0-9]{1,3}|192\.168\.(?:[0-9]{1,3}\.)[0-9]{1,3}|172\.(?:1[6-9]|2[0-9]|3[01])\.(?:[0-9]{1,3}\.)[0-9]{1,3})(?![0-9])"),
    ),
    ("PS032", "local Linux root-home path", re.compile(r"(?<![A-Za-z0-9_])/root/[A-Za-z0-9._-]+/")),
)


class WorkflowError(RuntimeError):
    """A deterministic, user-actionable workflow failure."""


def run(command: tuple[str, ...], *, check: bool = True) -> subprocess.CompletedProcess[str]:
    environment = git_environment()
    for key in (
        "PYTHONPATH", "PYTHONHOME", "PYTHONSTARTUP", "PYTHONINSPECT", "PYTHONUSERBASE",
    ):
        environment.pop(key, None)
    environment["PYTHONNOUSERSITE"] = "1"
    if command and command[0] == "gh":
        environment.pop("GH_REPO", None)
        environment.pop("GH_HOST", None)
    result = subprocess.run(
        command,
        cwd=ROOT,
        env=environment,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if check and result.returncode:
        raise WorkflowError(result.stderr.strip() or result.stdout.strip() or f"{' '.join(command)} failed")
    return result


def git(*args: str, check: bool = True) -> str:
    return run(("git", *args), check=check).stdout.strip()


def gh(*args: str, check: bool = True) -> str:
    return run(("gh", *args), check=check).stdout.strip()


def github_owner_repo() -> str:
    identity = public_repository_identity(origin_remote_url())
    return identity.removeprefix("github.com/")


def github_ref_sha(reference: str, *, required: bool = True) -> str | None:
    """Read an authoritative target-repository ref through GitHub's API."""
    fail_unless(bool(re.fullmatch(r"heads/[A-Za-z0-9._/-]+", reference)), "GitHub ref name is invalid")
    endpoint = f"repos/{github_owner_repo()}/git/matching-refs/{quote(reference, safe='/')}"
    result = run(("gh", "api", endpoint, "--hostname", "github.com"), check=False)
    fail_unless(result.returncode == 0, "unable to authenticate GitHub repository refs")
    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise WorkflowError("GitHub ref response is invalid") from exc
    fail_unless(isinstance(payload, list), "GitHub matching-ref response is invalid")
    exact = [item for item in payload if isinstance(item, dict) and item.get("ref") == f"refs/{reference}"]
    fail_unless(len(exact) <= 1, "GitHub matching-ref response contains duplicates")
    if not exact:
        fail_unless(not required, f"required GitHub ref is unavailable: {reference}")
        return None
    object_data = exact[0].get("object") if isinstance(exact[0].get("object"), dict) else None
    sha = object_data.get("sha") if isinstance(object_data, dict) else None
    return full_sha(f"GitHub {reference} ref", sha)


def fetch_authenticated_main() -> str:
    """Fetch origin/main and bind its result to the canonical GitHub repository."""
    git("fetch", "origin", "main")
    fetched = git("rev-parse", "origin/main")
    fail_unless(fetched == github_ref_sha("heads/main"), "fetched origin/main differs from the authoritative GitHub main ref")
    return fetched


def reject_existing_intake_history(intake_id: str, repository_remote: str) -> None:
    """Prevent a cleaned branch from hiding a durable intake in GitHub PR history."""
    if not repository_remote.startswith("github.com/"):
        return
    result = run(
        (
            "gh", "pr", "list", "--state", "all", "--limit", "100",
            "--search", f'"{intake_id}" in:body',
            "--json", "number,state,url,headRefName",
            "--repo", repository_remote.removeprefix("github.com/"),
        ),
        check=False,
    )
    fail_unless(result.returncode == 0, "unable to verify existing intake history on GitHub")
    try:
        matches = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise WorkflowError("GitHub intake-history response is not valid JSON") from exc
    fail_unless(isinstance(matches, list), "GitHub intake-history response is not a list")
    fail_unless(
        not matches,
        "intake ID already exists in pull-request history; resume the existing intake",
    )


def repository_identity(value: str) -> str:
    """Normalize equivalent SSH/HTTPS GitHub remotes without weakening repo identity."""
    value = value.strip().rstrip("/")
    owner = r"(?P<owner>[A-Za-z0-9](?:[A-Za-z0-9-]{0,38}))"
    repo = r"(?P<repo>[A-Za-z0-9._-]+?)(?:\.git)?"
    patterns = (
        rf"github\.com/{owner}/{repo}",
        rf"git@github\.com:{owner}/{repo}",
        rf"ssh://git@github\.com/{owner}/{repo}",
        rf"https://github\.com/{owner}/{repo}",
    )
    for pattern in patterns:
        match = re.fullmatch(pattern, value, re.I)
        if match:
            return f"github.com/{match.group('owner').lower()}/{match.group('repo').lower()}"
    if re.fullmatch(r"(?:\.\.?/)+[A-Za-z0-9._/-]+\.git", value):
        return value
    return ""


def public_repository_identity(value: str) -> str:
    """Return a credential-free durable repository identity or fail closed."""
    identity = repository_identity(value)
    fail_unless(
        identity.startswith("github.com/"),
        "origin remote must be a credential-free GitHub repository identity",
    )
    return identity


def origin_remote_url() -> str:
    """Read the configured URL without applying Git url.*.insteadOf rewrites."""
    return git("config", "--get", "remote.origin.url")


def same_repository(left: str, right: str) -> bool:
    left_identity = repository_identity(left)
    right_identity = repository_identity(right)
    return bool(left_identity and right_identity and left_identity == right_identity)


def validation_environment() -> dict[str, str]:
    """Make nested validation use the interpreter environment that launched the CLI."""
    environment = git_environment()
    # Keep the virtualenv's lexical bin path. Resolving the Python symlink can
    # jump to a framework bin directory that does not provide `python3`.
    interpreter_dir = str(Path(sys.executable).absolute().parent)
    environment["PATH"] = interpreter_dir + os.pathsep + os.defpath
    for key in (
        "MAKEFLAGS", "GNUMAKEFLAGS", "MFLAGS", "MAKEFILES", "MAKELEVEL",
        "PYTHONPATH", "PYTHONHOME", "PYTHONSTARTUP", "PYTHONINSPECT", "PYTHONUSERBASE",
    ):
        environment.pop(key, None)
    environment["PYTHONNOUSERSITE"] = "1"
    return environment


def run_make_validate() -> bool:
    make = shutil.which("make", path=os.defpath)
    fail_unless(make is not None, "trusted system make executable is unavailable")
    return subprocess.run(
        (make, "--no-print-directory", "validate"),
        cwd=ROOT,
        check=False,
        env=validation_environment(),
    ).returncode == 0


def verify_local_derived_routes(data: dict[str, Any]) -> None:
    expected = {value for value in data["derivedPaths"] if value.startswith("#/")}
    fail_unless(bool(expected), "projected publication must declare at least one site route")
    manifest_path = ROOT / "_site" / "content-manifest.json"
    fail_unless(manifest_path.is_file() and not manifest_path.is_symlink(), "derived-route validation requires the generated site manifest")
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise WorkflowError("generated site manifest is unavailable for derived-route validation") from exc
    fail_unless(isinstance(manifest, dict), "generated site manifest is invalid")
    available = {
        "#/overview", "#/library", "#/compare", "#/architecture", "#/lab",
        "#/visuals", "#/audiences",
    }
    items = manifest.get("items")
    presentations = manifest.get("presentation")
    audiences = manifest.get("audiences")
    presentation_decks = manifest.get("presentationDecks")
    fail_unless(
        isinstance(items, list)
        and isinstance(presentations, list)
        and isinstance(audiences, list)
        and isinstance(presentation_decks, list),
        "generated site route inventory is invalid",
    )
    item_routes = {
        item.get("path"): item.get("route")
        for item in items
        if isinstance(item, dict)
        and isinstance(item.get("path"), str)
        and isinstance(item.get("route"), str)
    }
    missing_canonical = sorted(set(data["canonicalPaths"]) - set(item_routes))
    if missing_canonical:
        raise WorkflowError(f"canonical path is absent from the generated site manifest: {missing_canonical[0]}")
    for canonical in data["canonicalPaths"]:
        canonical_route = item_routes[canonical]
        fail_unless(
            canonical_route in expected,
            f"canonical path manifest route is not declared as derived: {canonical} -> {canonical_route}",
        )
    available.update(item.get("route") for item in items if isinstance(item, dict) and isinstance(item.get("route"), str))
    available.update(f"#/present/{index}" for index in range(len(presentations)))
    slide_keys = [slide.get("key") for slide in presentations if isinstance(slide, dict)]
    fail_unless(
        len(slide_keys) == len(presentations)
        and all(isinstance(key, str) and key for key in slide_keys)
        and len(slide_keys) == len(set(slide_keys)),
        "generated presentation route inventory is invalid",
    )
    audience_ids: list[str] = []
    for audience in audiences:
        fail_unless(isinstance(audience, dict) and isinstance(audience.get("id"), str) and isinstance(audience.get("presentationSlides"), list), "generated audience route inventory is invalid")
        audience_id = audience["id"]
        audience_ids.append(audience_id)
        available.add(f"#/audiences/{audience_id}")
        available.update(f"#/present/{audience_id}/{index}" for index in range(len(audience["presentationSlides"])))
    fail_unless(len(audience_ids) == len(set(audience_ids)), "generated audience route inventory is invalid")
    deck_ids: list[str] = []
    for deck in presentation_decks:
        fail_unless(
            isinstance(deck, dict)
            and isinstance(deck.get("id"), str)
            and bool(deck["id"])
            and isinstance(deck.get("presentationSlides"), list)
            and bool(deck["presentationSlides"]),
            "generated presentation deck route inventory is invalid",
        )
        deck_id = deck["id"]
        selected = deck["presentationSlides"]
        fail_unless(
            all(isinstance(key, str) and key in slide_keys for key in selected)
            and len(selected) == len(set(selected)),
            "generated presentation deck route inventory is invalid",
        )
        fail_unless(
            deck.get("presentationRoute") == f"#/present/{deck_id}/0",
            "generated presentation deck entry route is invalid",
        )
        role_ids = deck.get("audienceRoleIds")
        fail_unless(
            isinstance(role_ids, list)
            and bool(role_ids)
            and all(isinstance(role_id, str) and role_id in audience_ids for role_id in role_ids)
            and len(role_ids) == len(set(role_ids)),
            "generated presentation deck audience roles are invalid",
        )
        deck_ids.append(deck_id)
        available.update(f"#/present/{deck_id}/{index}" for index in range(len(selected)))
        summary_route = deck.get("summaryRoute")
        if summary_route is not None:
            fail_unless(
                summary_route == f"#/present/{deck_id}/summary",
                "generated presentation deck summary route is invalid",
            )
            available.add(summary_route)
    fail_unless(
        len(deck_ids) == len(set(deck_ids)) and not set(deck_ids).intersection(audience_ids),
        "generated presentation deck IDs collide with another route context",
    )
    missing = sorted(expected - available)
    if missing:
        raise WorkflowError(f"declared derived route is absent from the generated site manifest: {missing[0]}")


def now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def fail_unless(condition: bool, message: str) -> None:
    if not condition:
        raise WorkflowError(message)


def safe_slug(value: str) -> str:
    slug = value.strip().lower()
    fail_unless(bool(SAFE_SLUG.fullmatch(slug)) and len(slug) <= 64, "slug must be <=64 lowercase letters/digits with single hyphens")
    return slug


def safe_line(label: str, value: str, maximum: int = 500) -> str:
    fail_unless(isinstance(value, str), f"{label} must be text")
    fail_unless(value == value.strip() and bool(value), f"{label} must be non-empty and trimmed")
    fail_unless(len(value) <= maximum and not any(unicodedata.category(char).startswith("C") for char in value), f"{label} contains a control/format character or exceeds {maximum} characters")
    findings = scan_text(value, label)
    if findings:
        raise WorkflowError(f"{label} fails public-safety rule {findings[0]}")
    return value


def safe_url(label: str, value: str) -> str:
    value = safe_line(label, value, 1000)
    split = urlsplit(value)
    fail_unless(split.scheme == "https" and bool(split.netloc) and not split.username and not split.password, f"{label} must be a public HTTPS URL")
    host = (split.hostname or "").rstrip(".").lower()
    fail_unless(bool(host) and "." in host and host != "localhost" and not host.endswith((".localhost", ".local", ".internal", ".corp", ".invalid", ".test")), f"{label} host is not public")
    try:
        address = ipaddress.ip_address(host.strip("[]"))
    except ValueError:
        address = None
    fail_unless(address is None or address.is_global, f"{label} IP address is not globally routable")
    return value


def resolve_under(path: Path, parent: Path, label: str) -> Path:
    ensure_local_root(parent, label)
    resolved = path.resolve()
    try:
        resolved.relative_to(parent.resolve())
    except ValueError as exc:
        raise WorkflowError(f"{label} must remain under {parent.relative_to(ROOT)}") from exc
    return resolved


def ensure_local_root(path: Path, label: str) -> None:
    fail_unless(path.absolute().is_relative_to(ROOT), f"{label} root must remain inside the repository")
    candidate = ROOT
    for part in path.absolute().relative_to(ROOT).parts:
        candidate /= part
        if candidate.exists():
            fail_unless(not candidate.is_symlink(), f"{label} root must not contain symlinks")
    if path.exists():
        fail_unless(path.resolve() == path.absolute(), f"{label} root is redirected")


def has_symlink_component(path: Path) -> bool:
    try:
        relative = path.absolute().relative_to(ROOT)
    except ValueError:
        return True
    candidate = ROOT
    for part in relative.parts:
        candidate /= part
        if candidate.is_symlink():
            return True
    return False


def checkpoint_path(value: str | Path) -> Path:
    path = Path(value)
    return resolve_under(path if path.is_absolute() else ROOT / path, CHECKPOINT_ROOT, "checkpoint")


def parse_actions(value: str) -> list[str]:
    actions = [item.strip().lower() for item in value.split(",") if item.strip()]
    fail_unless(bool(actions), "--requested-actions must explicitly list authorized actions")
    fail_unless(len(actions) == len(set(actions)), "--requested-actions contains duplicates")
    unknown = sorted(set(actions) - REQUEST_ACTIONS)
    fail_unless(not unknown, f"unsupported requested actions: {', '.join(unknown)}")
    fail_unless("branch" in actions, "publication intake requires explicit branch authority")
    return actions


def scan_text(text: str, location: str) -> list[str]:
    findings: list[str] = []
    for rule_id, label, pattern in PUBLIC_RULES:
        match = pattern.search(text)
        if match:
            line = text.count("\n", 0, match.start()) + 1
            findings.append(f"{rule_id} {label} at {location}:{line}")
    return findings


def git_path_names(*args: str) -> list[str]:
    result = subprocess.run(
        ("git", *args, "-z"),
        cwd=ROOT,
        env=git_environment(),
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode:
        raise WorkflowError("git path enumeration failed without exposing path bytes")
    try:
        return [value.decode("utf-8") for value in result.stdout.split(b"\0") if value]
    except UnicodeDecodeError as exc:
        raise WorkflowError("PS014 repository contains a non-UTF-8 path name") from exc


def load_binary_allowlist() -> dict[str, str]:
    fail_unless(PUBLIC_ALLOWLIST.is_file(), f"public binary allowlist is missing: {PUBLIC_ALLOWLIST.relative_to(ROOT)}")
    try:
        data = json.loads(PUBLIC_ALLOWLIST.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise WorkflowError(f"public binary allowlist is invalid: {exc}") from exc
    fail_unless(isinstance(data, dict) and set(data) == {"schemaVersion", "binaryFiles"} and data["schemaVersion"] == 1, "public binary allowlist schema is invalid")
    fail_unless(isinstance(data["binaryFiles"], list), "public binary allowlist binaryFiles must be a list")
    allowed: dict[str, str] = {}
    for entry in data["binaryFiles"]:
        fail_unless(isinstance(entry, dict) and set(entry) == {"path", "sha256", "reviewedByRole", "reason"}, "binary allowlist entry schema is invalid")
        path = derived_reference(entry["path"])
        fail_unless(isinstance(entry["sha256"], str) and bool(SHA256.fullmatch(entry["sha256"])), f"binary allowlist SHA-256 is invalid for {path}")
        safe_line("binary allowlist reviewer role", entry["reviewedByRole"], 160)
        safe_line("binary allowlist reason", entry["reason"], 500)
        fail_unless(path not in allowed, f"duplicate binary allowlist path: {path}")
        allowed[path] = entry["sha256"]
    return allowed


def load_binary_allowlist_at_commit(revision: str) -> dict[str, str]:
    relative = PUBLIC_ALLOWLIST.relative_to(ROOT).as_posix()
    result = subprocess.run(
        ("git", "show", f"{revision}:{relative}"),
        cwd=ROOT,
        env=git_environment(),
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    )
    fail_unless(
        result.returncode == 0,
        f"historical public binary allowlist is missing at commit {revision}",
    )
    try:
        data = json.loads(result.stdout.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise WorkflowError(
            f"historical public binary allowlist is invalid at commit {revision}: {exc}"
        ) from exc
    fail_unless(
        isinstance(data, dict)
        and set(data) == {"schemaVersion", "binaryFiles"}
        and data["schemaVersion"] == 1,
        f"historical public binary allowlist schema is invalid at commit {revision}",
    )
    fail_unless(
        isinstance(data["binaryFiles"], list),
        f"historical public binary allowlist binaryFiles must be a list at commit {revision}",
    )
    allowed: dict[str, str] = {}
    for entry in data["binaryFiles"]:
        fail_unless(
            isinstance(entry, dict)
            and set(entry) == {"path", "sha256", "reviewedByRole", "reason"},
            f"historical binary allowlist entry schema is invalid at commit {revision}",
        )
        path = derived_reference(entry["path"])
        fail_unless(
            isinstance(entry["sha256"], str) and bool(SHA256.fullmatch(entry["sha256"])),
            f"historical binary allowlist SHA-256 is invalid for {path} at commit {revision}",
        )
        safe_line("historical binary allowlist reviewer role", entry["reviewedByRole"], 160)
        safe_line("historical binary allowlist reason", entry["reason"], 500)
        fail_unless(
            path not in allowed,
            f"duplicate historical binary allowlist path at commit {revision}: {path}",
        )
        allowed[path] = entry["sha256"]
    return allowed


def public_source_name(name: str) -> str:
    if name.startswith("_site/content/"):
        return name.removeprefix("_site/content/")
    if name.startswith("_site/"):
        return f"site/{name.removeprefix('_site/')}"
    return name


def decode_public_bytes(data: bytes, name: str, allowed_binaries: dict[str, str], location: str | None = None) -> tuple[str | None, list[str]]:
    location = location or name
    source_name = public_source_name(name)
    if Path(source_name).suffix.lower() in BINARY_EXTENSIONS:
        expected = allowed_binaries.get(source_name)
        if expected is None:
            return None, [f"PS015 unreviewed binary public artifact at {location}"]
        if hashlib.sha256(data).hexdigest() != expected:
            return None, [f"PS016 binary public artifact hash differs from allowlist at {location}"]
        return None, []
    if b"\0" in data:
        return None, [f"PS017 NUL-containing public text artifact at {location}"]
    try:
        return data.decode("utf-8"), []
    except UnicodeDecodeError:
        return None, [f"PS018 non-UTF-8 public text artifact at {location}"]


def scan_public_file(path: Path, name: str, allowed_binaries: dict[str, str], location: str | None = None) -> list[str]:
    location = location or name
    source_name = public_source_name(name)
    if Path(source_name).suffix.lower() in BINARY_EXTENSIONS:
        expected = allowed_binaries.get(source_name)
        if expected is None:
            return [f"PS015 unreviewed binary public artifact at {location}"]
        digest = hashlib.sha256()
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
        actual = digest.hexdigest()
        return [] if actual == expected else [f"PS016 binary public artifact hash differs from allowlist at {location}"]

    errors: list[str] = []
    decoder = codecs.getincrementaldecoder("utf-8")("strict")
    tail = ""
    decoded_newlines = 0
    seen_rules: set[str] = set()
    try:
        with path.open("rb") as handle:
            for raw in iter(lambda: handle.read(1024 * 1024), b""):
                if b"\0" in raw:
                    errors.append(f"PS017 NUL-containing public text artifact at {location}")
                    return errors
                text = decoder.decode(raw, final=False)
                window = tail + text
                window_start_line = decoded_newlines - tail.count("\n") + 1
                for rule_id, label, pattern in PUBLIC_RULES:
                    match = pattern.search(window) if rule_id not in seen_rules else None
                    if match:
                        line = window_start_line + window.count("\n", 0, match.start())
                        errors.append(f"{rule_id} {label} at {location}:{line}")
                        seen_rules.add(rule_id)
                decoded_newlines += text.count("\n")
                tail = window[-4096:]
            final = decoder.decode(b"", final=True)
            window = tail + final
            window_start_line = decoded_newlines - tail.count("\n") + 1
            for rule_id, label, pattern in PUBLIC_RULES:
                match = pattern.search(window) if rule_id not in seen_rules else None
                if match:
                    line = window_start_line + window.count("\n", 0, match.start())
                    errors.append(f"{rule_id} {label} at {location}:{line}")
    except UnicodeDecodeError:
        errors.append(f"PS018 non-UTF-8 public text artifact at {location}")
    return errors


def validate_public_name(name: str) -> list[str]:
    if not name or "%" in name or name != name.strip() or any(unicodedata.category(character).startswith("C") for character in name):
        return ["PS019 public path contains percent, control, newline, or surrounding whitespace"]
    return scan_text(name, "public path")


def safe_location(name: str) -> str:
    return f"path-sha256:{hashlib.sha256(name.encode('utf-8', errors='surrogatepass')).hexdigest()[:16]}" if validate_public_name(name) else name


def public_files(include_generated: bool = True) -> list[tuple[str, Path]]:
    hidden = subprocess.run(
        ("git", "ls-files", "-v", "-z"), cwd=ROOT, env=git_environment(), check=False,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    if hidden.returncode:
        raise WorkflowError("PS023 unable to inspect Git index visibility flags")
    if any(entry[:1] == b"S" or entry[:1].islower() for entry in hidden.stdout.split(b"\0") if entry):
        raise WorkflowError("PS023 Git index visibility flags hide worktree state")
    modes = subprocess.run(
        ("git", "ls-files", "-s", "-z"),
        cwd=ROOT,
        env=git_environment(),
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if modes.returncode:
        raise WorkflowError("PS028 unable to inspect tracked Git modes")
    for entry in (value for value in modes.stdout.split(b"\0") if value):
        mode = entry.split(b" ", 1)[0]
        if mode == b"120000":
            raise WorkflowError("PS022 tracked symlink is not a public regular file")
        if mode not in {b"100644", b"100755"}:
            raise WorkflowError("PS028 tracked Git link or non-regular mode is not public content")
    names = set(git_path_names("ls-files", "-co", "--exclude-standard"))
    site = ROOT / "_site"
    if include_generated and site.exists():
        names.update(path.relative_to(ROOT).as_posix() for path in site.rglob("*") if path.is_file())
    files: list[tuple[str, Path]] = []
    for name in sorted(names):
        if name.startswith((".git/", ".study-workflow/")):
            continue
        path = ROOT / name
        if path.is_symlink() or has_symlink_component(path):
            raise WorkflowError(f"PS022 symlink public path at {safe_location(name)}")
        if path.is_file():
            files.append((name, path))
    return files


def public_content_errors(
    base: str | None = None,
    history_end: str = "HEAD",
    include_generated: bool = True,
) -> list[str]:
    errors: list[str] = []
    allowed_binaries = load_binary_allowlist()
    for name, path in public_files(include_generated):
        name_errors = validate_public_name(name)
        errors.extend(name_errors)
        errors.extend(scan_public_file(path, name, allowed_binaries, safe_location(name)))
    if base:
        commits = git("rev-list", "--reverse", f"{base}..{history_end}").splitlines()
        for commit in commits:
            historical_allowed_binaries = load_binary_allowlist_at_commit(commit)
            errors.extend(scan_text(git("show", "-s", "--format=%B", commit), f"commit {commit} message"))
            parents = git("rev-list", "--parents", "-n", "1", commit).split()
            if len(parents) > 2:
                errors.append(f"PS024 merge commits are not permitted in an intake branch at commit {commit}")
            names = git_path_names("diff-tree", "--root", "--no-commit-id", "--name-only", "-r", commit)
            tree = subprocess.run(
                ("git", "ls-tree", "-r", "-z", commit),
                cwd=ROOT,
                env=git_environment(),
                check=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            if tree.returncode:
                raise WorkflowError("PS028 unable to inspect historical Git modes")
            tree_modes: dict[str, str] = {}
            try:
                for entry in (value for value in tree.stdout.split(b"\0") if value):
                    metadata, encoded_name = entry.split(b"\t", 1)
                    tree_modes[encoded_name.decode("utf-8")] = metadata.split(b" ", 1)[0].decode("ascii")
            except (UnicodeDecodeError, ValueError) as exc:
                raise WorkflowError("PS014 historical tree contains an invalid path entry") from exc
            historical_binary_names = {
                name
                for name in tree_modes
                if Path(public_source_name(name)).suffix.lower() in BINARY_EXTENSIONS
            }
            for name in sorted(historical_binary_names):
                errors.extend(validate_public_name(name))
                location = f"commit {commit} {safe_location(name)}"
                mode = tree_modes[name]
                if mode == "120000":
                    errors.append(f"PS022 symlink public path at {location}")
                    continue
                if mode not in {"100644", "100755"}:
                    errors.append(f"PS028 non-regular tracked Git mode at {location}")
                    continue
                size_result = subprocess.run(
                    ("git", "cat-file", "-s", f"{commit}:{name}"),
                    cwd=ROOT,
                    env=git_environment(),
                    check=False,
                    text=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.DEVNULL,
                )
                if size_result.returncode:
                    raise WorkflowError(
                        f"PS028 unable to inspect historical binary blob at commit {commit}"
                    )
                if int(size_result.stdout.strip()) > 64 * 1024 * 1024:
                    errors.append(
                        f"PS020 oversized history artifact requires separate review at {location}"
                    )
                    continue
                blob = subprocess.run(
                    ("git", "show", f"{commit}:{name}"),
                    cwd=ROOT,
                    env=git_environment(),
                    check=False,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.DEVNULL,
                )
                if blob.returncode:
                    raise WorkflowError(
                        f"PS028 unable to inspect historical binary blob at commit {commit}"
                    )
                _, decode_errors = decode_public_bytes(
                    blob.stdout,
                    name,
                    historical_allowed_binaries,
                    location,
                )
                errors.extend(decode_errors)
            for name in names:
                if name in historical_binary_names:
                    continue
                name_errors = validate_public_name(name)
                errors.extend(name_errors)
                location = safe_location(name)
                mode = tree_modes.get(name, "")
                if mode == "120000":
                    errors.append(f"PS022 symlink public path in commit {commit} at {location}")
                    continue
                if mode and mode not in {"100644", "100755"}:
                    errors.append(f"PS028 non-regular tracked Git mode in commit {commit} at {location}")
                    continue
                size_result = subprocess.run(("git", "cat-file", "-s", f"{commit}:{name}"), cwd=ROOT, env=git_environment(), check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
                if size_result.returncode == 0 and int(size_result.stdout.strip()) > 64 * 1024 * 1024:
                    errors.append(f"PS020 oversized history artifact requires separate review at commit {commit}")
                    continue
                blob = subprocess.run(("git", "show", f"{commit}:{name}"), cwd=ROOT, env=git_environment(), check=False, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
                if blob.returncode == 0:
                    text, decode_errors = decode_public_bytes(
                        blob.stdout,
                        name,
                        historical_allowed_binaries,
                        location,
                    )
                    errors.extend(decode_errors)
                    if text is not None:
                        errors.extend(scan_text(text, f"commit {commit} {location}"))
    return sorted(set(errors))


def raw_tracked_bytes_match(revision: str) -> bool:
    """Compare raw worktree bytes to Git blobs without content filters."""
    listed = subprocess.run(
        ("git", "ls-files", "-c", "-z"), cwd=ROOT, env=git_environment(), check=False,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    if listed.returncode:
        raise WorkflowError("unable to enumerate tracked raw-byte provenance")
    try:
        names = [value.decode("utf-8") for value in listed.stdout.split(b"\0") if value]
    except UnicodeDecodeError as exc:
        raise WorkflowError("tracked provenance path is not UTF-8") from exc
    for name in names:
        path = ROOT / name
        if not path.is_file() or path.is_symlink():
            return False
        expected = subprocess.Popen(
            ("git", "cat-file", "blob", f"{revision}:{name}"), cwd=ROOT, env=git_environment(),
            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
        )
        digest = hashlib.sha256()
        assert expected.stdout is not None
        for chunk in iter(lambda: expected.stdout.read(1024 * 1024), b""):
            digest.update(chunk)
        expected.stdout.close()
        if expected.wait() != 0:
            return False
        actual = hashlib.sha256()
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                actual.update(chunk)
        if actual.hexdigest() != digest.hexdigest():
            return False
    return True


def source_tree_digest() -> str:
    """Digest the exact candidate source tree, independent of Git staging state."""
    digest = hashlib.sha256()
    names = sorted(set(git_path_names("ls-files", "-co", "--exclude-standard")))
    for name in names:
        if name.startswith((".git/", ".study-workflow/", "_site/")):
            continue
        path = ROOT / name
        if not path.exists():
            # A validated deletion remains absent after it is committed.
            continue
        fail_unless(path.is_file() and not path.is_symlink() and not has_symlink_component(path), "source tree contains a non-regular or symlinked candidate path")
        encoded = name.encode("utf-8")
        digest.update(len(encoded).to_bytes(8, "big"))
        digest.update(encoded)
        digest.update(b"x" if path.stat().st_mode & 0o111 else b"-")
        file_digest = hashlib.sha256()
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                file_digest.update(chunk)
        digest.update(file_digest.digest())
    return digest.hexdigest()


def commit_tree_entries(revision: str) -> dict[str, tuple[str, str, str]]:
    """Return raw Git tree metadata without applying worktree filters."""
    result = subprocess.run(
        ("git", "ls-tree", "-r", "-z", revision),
        cwd=ROOT,
        env=git_environment(),
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    fail_unless(result.returncode == 0, "unable to inspect the accepted candidate tree")
    entries: dict[str, tuple[str, str, str]] = {}
    try:
        for entry in (value for value in result.stdout.split(b"\0") if value):
            metadata, encoded_name = entry.split(b"\t", 1)
            mode, kind, object_id = metadata.decode("ascii").split(" ", 2)
            name = encoded_name.decode("utf-8")
            entries[name] = (mode, kind, object_id)
    except (UnicodeDecodeError, ValueError) as exc:
        raise WorkflowError("accepted candidate tree contains an invalid entry") from exc
    return entries


def source_tree_digest_at_commit(revision: str) -> str:
    """Recompute the local-validation digest from immutable Git blobs."""
    digest = hashlib.sha256()
    entries = commit_tree_entries(revision)
    for name in sorted(entries):
        if name.startswith((".git/", ".study-workflow/", "_site/")):
            continue
        mode, kind, object_id = entries[name]
        fail_unless(
            (mode, kind) in {("100644", "blob"), ("100755", "blob")},
            f"accepted candidate contains a non-regular source path: {safe_location(name)}",
        )
        encoded = name.encode("utf-8")
        digest.update(len(encoded).to_bytes(8, "big"))
        digest.update(encoded)
        digest.update(b"x" if mode == "100755" else b"-")
        blob = subprocess.Popen(
            ("git", "cat-file", "blob", object_id),
            cwd=ROOT,
            env=git_environment(),
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
        )
        file_digest = hashlib.sha256()
        assert blob.stdout is not None
        for chunk in iter(lambda: blob.stdout.read(1024 * 1024), b""):
            file_digest.update(chunk)
        blob.stdout.close()
        fail_unless(blob.wait() == 0, "unable to read an accepted candidate source blob")
        digest.update(file_digest.digest())
    return digest.hexdigest()


def ignored_paths_at_commit(
    entries: dict[str, tuple[str, str, str]],
    paths: set[str],
) -> set[str]:
    """Evaluate committed ignore rules without checking out or filtering content."""
    if not paths:
        return set()
    with tempfile.TemporaryDirectory(prefix="study-candidate-ignore-") as temporary:
        worktree = Path(temporary)
        for name, (mode, kind, object_id) in entries.items():
            if not (name == ".gitignore" or name.endswith("/.gitignore")):
                continue
            fail_unless((mode, kind) in {("100644", "blob"), ("100755", "blob")}, "candidate ignore rules are not regular Git blobs")
            result = subprocess.run(
                ("git", "cat-file", "blob", object_id),
                cwd=ROOT,
                env=git_environment(),
                check=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
            )
            fail_unless(result.returncode == 0 and len(result.stdout) <= 1024 * 1024, "candidate ignore rules are unavailable or oversized")
            target = worktree / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(result.stdout)
        git_dir = git("rev-parse", "--absolute-git-dir")
        ignored: set[str] = set()
        for value in sorted(paths):
            result = subprocess.run(
                (
                    "git", f"--git-dir={git_dir}", f"--work-tree={worktree}",
                    "check-ignore", "-q", "--no-index", "--", value,
                ),
                cwd=worktree,
                env=git_environment(),
                check=False,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            fail_unless(result.returncode in {0, 1}, "unable to evaluate accepted candidate ignore rules")
            if result.returncode == 0:
                ignored.add(value)
        return ignored


def working_tree_clean_at(revision: str) -> bool:
    return not git("status", "--porcelain", "--untracked-files=all") and raw_tracked_bytes_match(revision)


def atomic_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=path.parent,
            prefix=f".{path.name}.", suffix=".tmp", delete=False,
        ) as handle:
            temporary = Path(handle.name)
            json.dump(data, handle, indent=2, sort_keys=True)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def atomic_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=path.parent,
            prefix=f".{path.name}.", suffix=".tmp", delete=False,
        ) as handle:
            temporary = Path(handle.name)
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def load_checkpoint(value: str | Path) -> tuple[Path, dict[str, Any]]:
    path = checkpoint_path(value)
    fail_unless(path.is_file(), f"checkpoint does not exist: {path}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise WorkflowError(f"checkpoint is not valid UTF-8 JSON: {exc}") from exc
    validate_checkpoint_shape(data, path)
    return path, data


def full_sha(label: str, value: Any, required: bool = True) -> str | None:
    if value in (None, "") and not required:
        return None
    fail_unless(isinstance(value, str) and bool(FULL_SHA.fullmatch(value)), f"{label} must be a full lowercase 40-character commit SHA")
    return value


def canonical_path(value: str) -> str:
    fail_unless(isinstance(value, str) and value and "%" not in value and not value.startswith("/") and "\\" not in value, "canonical paths must be repository-relative POSIX paths without percent syntax")
    parts = Path(value).parts
    fail_unless(parts and parts[0] in CANONICAL_ROOTS and all(part not in {".", ".."} for part in parts), f"canonical path is outside declared roots: {value}")
    path = (ROOT / value).resolve()
    fail_unless(path.is_relative_to(ROOT.resolve()), f"canonical path escapes the repository: {value}")
    fail_unless(not has_symlink_component(ROOT / value), f"canonical path contains a symlink: {value}")
    return value


def derived_reference(value: str) -> str:
    value = safe_line("derived reference", value, 500)
    fail_unless("%" not in value, "derived references must not contain percent-encoded or literal percent syntax")
    if value.startswith("#/"):
        fail_unless(" " not in value and ".." not in value, f"derived route is invalid: {value}")
        return value
    fail_unless(not value.startswith("/") and "\\" not in value, "derived references must be routes or repository-relative POSIX paths")
    parts = Path(value).parts
    fail_unless(parts and parts[0] not in {".git", ".study-workflow"} and all(part not in {".", ".."} for part in parts), f"derived reference escapes the repository: {value}")
    fail_unless((ROOT / value).resolve().is_relative_to(ROOT.resolve()), f"derived reference escapes the repository: {value}")
    fail_unless(not has_symlink_component(ROOT / value), f"derived reference contains a symlink: {value}")
    return value


def verify_candidate_derived_files(data: dict[str, Any]) -> None:
    """Require every file-like derived artifact to exist in the reviewed commit."""
    derived_files = {value for value in data["derivedPaths"] if not value.startswith("#/")}
    if not derived_files:
        return
    for value in sorted(derived_files):
        fail_unless(
            not value.startswith(("_site/", "evidence/raw/", ".study-workflow/")),
            f"candidate derived path is generated, private, or workflow-local: {safe_location(value)}",
        )
        ignored = subprocess.run(
            ("git", "check-ignore", "-q", "--no-index", "--", value),
            cwd=ROOT,
            env=git_environment(),
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        fail_unless(ignored.returncode in {0, 1}, "unable to inspect candidate derived-path ignore rules")
        fail_unless(ignored.returncode == 1, f"candidate derived path is ignored or private: {safe_location(value)}")
    candidate = full_sha("candidateSha", data["candidateSha"])
    tree = subprocess.run(
        ("git", "ls-tree", "-r", "-z", candidate),
        cwd=ROOT,
        env=git_environment(),
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    fail_unless(tree.returncode == 0, "unable to inspect candidate derived artifacts")
    entries: dict[str, tuple[str, str]] = {}
    try:
        for entry in (value for value in tree.stdout.split(b"\0") if value):
            metadata, encoded_name = entry.split(b"\t", 1)
            mode, kind, _ = metadata.decode("ascii").split(" ", 2)
            entries[encoded_name.decode("utf-8")] = (mode, kind)
    except (UnicodeDecodeError, ValueError) as exc:
        raise WorkflowError("candidate tree contains an invalid derived-artifact entry") from exc
    for value in sorted(derived_files):
        fail_unless(
            entries.get(value) in {("100644", "blob"), ("100755", "blob")},
            f"candidate derived path is not a tracked regular blob: {safe_location(value)}",
        )


def candidate_envelope_digest(data: dict[str, Any]) -> str:
    """Bind independently reviewed framing and artifacts to one candidate."""
    payload = {key: data.get(key) for key in CANDIDATE_ENVELOPE_FIELDS}
    payload["repositoryRemote"] = repository_identity(str(data.get("repositoryRemote", "")))
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def state_evidence_errors(data: dict[str, Any], *, verify_artifacts: bool = True) -> list[str]:
    state = data["canonicalState"]
    errors: list[str] = []

    def require(condition: bool, message: str) -> None:
        if not condition:
            errors.append(f"{state}: {message}")

    framed = {"FRAMED", "RESEARCHED", "AUTHORED", "PROJECTED", "CANDIDATE", "REVIEWED", "VALIDATED", "MERGED", "PUBLISHED", "CLOSED"}
    researched = framed - {"FRAMED"}
    authored = researched - {"RESEARCHED"}
    projected = authored - {"AUTHORED"}
    candidate = projected - {"PROJECTED"}
    reviewed = candidate - {"CANDIDATE"}
    validated = reviewed - {"REVIEWED"}
    merged = validated - {"VALIDATED"}
    published = merged - {"MERGED"}

    if state in framed:
        require(bool(data["decisionQuestion"]), "decisionQuestion is required")
        require(data["artifactType"] in ARTIFACT_TYPES, "artifactType is required")
        require(bool(data["audiences"]), "at least one audience is required")
        require(bool(data["scopeSummary"]), "scopeSummary is required")
        require(bool(data["deltaSummary"]), "deltaSummary is required")
    if state in researched:
        require(bool(data["evidenceReferences"]), "at least one evidence reference is required")
    if state in authored:
        require(bool(data["canonicalPaths"]), "at least one canonical path is required")
        if verify_artifacts:
            for value in data["canonicalPaths"]:
                require((ROOT / value).is_file(), f"canonical path does not exist: {value}")
    if state in projected:
        require(bool(data["derivedPaths"]), "at least one derived path or route is required")
        require(any(value.startswith("#/") for value in data["derivedPaths"]), "at least one site route is required")
        if verify_artifacts:
            for value in data["derivedPaths"]:
                if value.startswith("#/"):
                    continue
                path = ROOT / value
                require(
                    path.is_file() and not has_symlink_component(path),
                    f"derived path does not exist as a regular file: {value}",
                )
    if state in candidate:
        require(data["localValidation"] == "pass", "localValidation must be pass")
        require(bool(data["localValidationDigest"]), "localValidationDigest is required")
        require(data["prNumber"] is not None, "prNumber is required")
        require(bool(data["prUrl"]), "prUrl is required")
        require(bool(data["candidateSha"]) and data["candidateSha"] == data["prHeadSha"], "candidateSha and prHeadSha must be identical")
        require(
            bool(data["candidateEnvelopeSha256"])
            and data["candidateEnvelopeSha256"] == candidate_envelope_digest(data),
            "candidateEnvelopeSha256 must bind the reviewed framing, artifacts, validation digest, and candidate SHA",
        )
    if state == "CANDIDATE":
        require(data["prDraft"] is True, "candidate PR must remain draft")
    if state in reviewed:
        require(data["reviewDisposition"] == "pass", "reviewDisposition must be pass")
        require(bool(data["acceptedSha"]) and data["acceptedSha"] == data["candidateSha"], "acceptedSha must equal candidateSha")
        require(bool(data["reviewEvidenceUrls"]), "independent review evidence URL is required")
    if state in validated:
        require(data["checkDisposition"] == "green", "checkDisposition must be green")
        require(bool(data["checkedSha"]) and data["checkedSha"] == data["candidateSha"], "checkedSha must equal candidateSha")
        require(bool(data["checkUrls"]), "at least one check URL is required")
        require(data["prDraft"] is False, "PR must be marked ready")
    if state in merged:
        require(bool(data["mergeSha"]), "mergeSha is required")
        require(data["branchCleanupStatus"] == "complete", "branchCleanupStatus must be complete")
        require(bool(data["cleanupEvidence"]), "branch cleanup evidence is required")
    if state in published:
        require(data["publicationStatus"] == "published", "publicationStatus must be published")
        require(all(data[key] for key in ("mainValidationUrl", "pagesRunUrl", "liveBaseUrl")), "main validation, Pages, and live URLs are required")
        require(bool(data["manifestSha256"]), "deployed manifest SHA-256 is required")
        require(bool(data["closureEvidenceUrl"]), "durable closure evidence URL is required")
        expected_manifest = {
            f"sourceRevision={data['mergeSha']}",
            f"manifestSha256={data['manifestSha256']}",
            "sourceDirty=false",
        }
        require(set(data["manifestAssertions"]) == expected_manifest, "manifestAssertions must exactly bind revision, manifest digest, and clean state")
        expected_routes = {value for value in data["derivedPaths"] if value.startswith("#/")}
        require(bool(expected_routes) and set(data["routeAssertions"]) == expected_routes, "routeAssertions must exactly match every declared derived route")
    if state == "CLOSED":
        require(bool(data["residualLimitations"]), "residual limitations are required")
        require(bool(data["nextGate"]), "next gate is required")
    if state in {"REWORK", "BLOCKED"}:
        require(bool(data["statusReason"]), "status reason is required")
        require(bool(data["nextGate"]), "next safe action is required")
        require(bool(data["blockerOwnerRole"]), "owner role is required")
        require(bool(data["responsibleStage"]), "responsible stage is required")
    return errors


def validate_checkpoint_shape(data: Any, path: Path | None = None, *, verify_artifacts: bool = True) -> None:
    label = str(path or "checkpoint")
    fail_unless(isinstance(data, dict), f"{label} root must be an object")
    fail_unless(set(data) == CHECKPOINT_KEYS, f"{label} fields differ from schema v{SCHEMA_VERSION}")
    fail_unless(data["schemaVersion"] == SCHEMA_VERSION, f"{label} schemaVersion must be {SCHEMA_VERSION}")
    fail_unless(isinstance(data["intakeId"], str) and re.fullmatch(r"INTAKE-\d{8}-[a-z0-9]+(?:-[a-z0-9]+)*", data["intakeId"]), f"{label} intakeId is invalid")
    slug = safe_slug(data["slug"])
    fail_unless(data["intakeId"].endswith(f"-{slug}"), f"{label} intakeId and slug differ")
    safe_line("checkpoint title", data["title"], 160)
    safe_line("checkpoint requestSummary", data["requestSummary"], 500)
    if data["decisionQuestion"]:
        safe_line("checkpoint decisionQuestion", data["decisionQuestion"], 500)
    fail_unless(data["artifactType"] is None or data["artifactType"] in ARTIFACT_TYPES, f"{label} artifactType is invalid")
    for key in ("scopeSummary", "deltaSummary"):
        if data[key]:
            safe_line(f"checkpoint {key}", data[key], 1000)
    fail_unless(data["sourceKind"] in SOURCE_KINDS, f"{label} sourceKind is invalid")
    fail_unless(isinstance(data["requestedActions"], list) and all(isinstance(item, str) for item in data["requestedActions"]), f"{label} requestedActions are invalid")
    fail_unless(data["requestedActions"] == parse_actions(",".join(data["requestedActions"])), f"{label} requestedActions are invalid")
    fail_unless(data["canonicalState"] in STATES, f"{label} canonicalState is invalid")
    safe_line("checkpoint statusReason", data["statusReason"], 500)
    safe_line("checkpoint nextGate", data["nextGate"], 500)
    safe_line("checkpoint repositoryRemote", data["repositoryRemote"], 500)
    fail_unless(
        bool(repository_identity(data["repositoryRemote"])),
        f"{label} repositoryRemote must be a credential-free repository identity",
    )
    fail_unless(data["baseBranch"] == "main", f"{label} baseBranch must be main")
    full_sha("baseSha", data["baseSha"])
    fail_unless(data["branch"] == f"study/{slug}", f"{label} branch must be study/{slug}")
    for key in ("checkpointCreatedAt", "updatedAt"):
        fail_unless(isinstance(data[key], str) and bool(UTC_TIMESTAMP.fullmatch(data[key])), f"{label} {key} must use UTC YYYY-MM-DDTHH:MM:SSZ")
    for key in ("audiences", "inputReferences", "evidenceReferences", "canonicalPaths", "derivedPaths", "reviewEvidenceUrls", "checkUrls", "cleanupEvidence", "manifestAssertions", "routeAssertions", "residualLimitations"):
        fail_unless(isinstance(data[key], list) and all(isinstance(item, str) for item in data[key]), f"{label} {key} must be a string list")
    for key in ("audiences", "inputReferences", "evidenceReferences", "cleanupEvidence", "manifestAssertions", "routeAssertions", "residualLimitations"):
        for item in data[key]:
            safe_line(f"checkpoint {key}", item, 1000)
    for value in data["canonicalPaths"]:
        canonical_path(value)
    for value in data["derivedPaths"]:
        derived_reference(value)
    for key in ("reviewEvidenceUrls", "checkUrls"):
        for item in data[key]:
            safe_url(f"checkpoint {key}", item)
    for key in ("candidateSha", "prHeadSha", "acceptedSha", "checkedSha", "mergeSha"):
        full_sha(key, data[key], required=False)
    fail_unless(data["localValidation"] in {"pending", "pass", "fail"}, f"{label} localValidation is invalid")
    fail_unless(data["localValidationDigest"] is None or (isinstance(data["localValidationDigest"], str) and bool(SHA256.fullmatch(data["localValidationDigest"]))), f"{label} localValidationDigest is invalid")
    fail_unless(data["localValidation"] == "pass" or data["localValidationDigest"] is None, f"{label} non-passing localValidation cannot retain a digest")
    fail_unless(data["candidateEnvelopeSha256"] is None or (isinstance(data["candidateEnvelopeSha256"], str) and bool(SHA256.fullmatch(data["candidateEnvelopeSha256"]))), f"{label} candidateEnvelopeSha256 is invalid")
    fail_unless(data["reviewDisposition"] in {"pending", "pass", "conditional", "fail"}, f"{label} reviewDisposition is invalid")
    fail_unless(data["checkDisposition"] in {"pending", "green", "failed"}, f"{label} checkDisposition is invalid")
    fail_unless(data["publicationStatus"] in {"pending", "published", "corrective-change-required"}, f"{label} publicationStatus is invalid")
    fail_unless(data["branchCleanupStatus"] in {"pending", "complete", "failed"}, f"{label} branchCleanupStatus is invalid")
    fail_unless(data["prNumber"] is None or (type(data["prNumber"]) is int and data["prNumber"] > 0), f"{label} prNumber is invalid")
    fail_unless(type(data["prDraft"]) is bool, f"{label} prDraft must be boolean")
    for key in ("prUrl", "mainValidationUrl", "pagesRunUrl", "liveBaseUrl", "closureEvidenceUrl"):
        if data[key]:
            safe_url(key, data[key])
    fail_unless(data["manifestSha256"] is None or (isinstance(data["manifestSha256"], str) and bool(SHA256.fullmatch(data["manifestSha256"]))), f"{label} manifestSha256 is invalid")
    for key in ("blockerOwnerRole", "responsibleStage"):
        if data[key]:
            safe_line(f"checkpoint {key}", data[key], 160)
    evidence_errors = state_evidence_errors(data, verify_artifacts=verify_artifacts)
    if evidence_errors:
        raise WorkflowError(evidence_errors[0])


def replace_field(text: str, field: str, value: str) -> str:
    pattern = re.compile(rf"^(?P<prefix>-?[ \t]*\*\*{re.escape(field)}:\*\*)[ \t]*.*$", re.M)
    fail_unless(bool(pattern.search(text)), f"template field is missing: {field}")
    return pattern.sub(lambda match: f"{match.group('prefix')} {value}", text)


def markdown_text(value: str) -> str:
    """Keep public-safe intake values literal inside generated Markdown."""
    escaped = value.replace("\\", "\\\\")
    for character in ("`", "*", "_", "[", "]", "<", ">", "|", "#"):
        escaped = escaped.replace(character, f"\\{character}")
    return escaped


def immutable_spec(
    args: argparse.Namespace,
    intake_id: str,
    checkpoint: Path,
    repository_remote: str,
) -> str:
    text = TEMPLATE.read_text(encoding="utf-8")
    text = text.split("\n## 10. Local validation and PR candidate", 1)[0].rstrip() + "\n"
    text = text.replace("# Study publication intake", f"# Study publication intake: {markdown_text(args.title)}", 1)
    text = text.replace("../docs/", "../../docs/").replace("../templates/", "../../templates/")
    values = {
        "Intake ID": f"`{intake_id}`", "Canonical workflow state": "`INTAKE`",
        "Checkpoint location": f"local ignored checkpoint `{checkpoint.relative_to(ROOT)}`; mirror to the draft PR",
        "Requested outcome": f"Publish a reviewed repository change for “{markdown_text(args.title)}” following the canonical workflow.",
        "Current authorized instruction": markdown_text(args.request_summary),
        "Target repository and remote": markdown_text(repository_remote),
        "Repository visibility": args.visibility, "Default branch": "main",
        "Requested actions": ", ".join(parse_actions(args.requested_actions)),
        "Public-safe title": markdown_text(args.title), "Type": args.source_kind,
        "Stable reference": markdown_text("; ".join(args.input_reference) if args.input_reference else "Current authorized task; raw chat/input is not committed."),
        "Date accessed": date.today().isoformat(),
    }
    if args.decision_question:
        values["Decision question"] = markdown_text(args.decision_question)
    for field, value in values.items():
        text = replace_field(text, field, value)
    return "<!-- Immutable public-safe intake specification: sections 1–9 only. -->\n\n" + text


def command_new(args: argparse.Namespace) -> int:
    slug = safe_slug(args.slug)
    args.title = safe_line("title", args.title, 160)
    args.request_summary = safe_line("request summary", args.request_summary, 500)
    args.decision_question = safe_line("decision question", args.decision_question, 500)
    actions = parse_actions(args.requested_actions)
    if args.write_spec:
        fail_unless("edit" in actions, "--write-spec requires explicit edit authority")
    input_references = [safe_line("input reference", value, 1000) for value in args.input_reference]
    fail_unless(not git("status", "--porcelain"), "working tree must be clean before creating an intake branch")
    branch = f"study/{slug}"
    fail_unless(git("branch", "--show-current") == "main", "new intake must start from main")
    stamp = args.date or date.today().strftime("%Y%m%d")
    fail_unless(bool(re.fullmatch(r"\d{8}", stamp)), "--date must use YYYYMMDD")
    intake_id = f"INTAKE-{stamp}-{slug}"
    ensure_local_root(CHECKPOINT_ROOT, "checkpoint")
    checkpoint = CHECKPOINT_ROOT / f"{intake_id.lower()}.json"
    fail_unless(not checkpoint.exists(), f"checkpoint already exists: {checkpoint.relative_to(ROOT)}")
    spec = SPEC_ROOT / f"{intake_id.lower()}.md" if args.write_spec else None
    if spec is not None:
        ensure_local_root(SPEC_ROOT, "intake specification")
        fail_unless(not spec.exists(), f"intake specification already exists: {spec.relative_to(ROOT)}")

    repository_remote = public_repository_identity(origin_remote_url())
    reject_existing_intake_history(intake_id, repository_remote)
    fetch_authenticated_main()
    git("merge", "--ff-only", "origin/main")
    base = git("rev-parse", "origin/main")
    fail_unless(git("rev-parse", "HEAD") == base, "local main must exactly equal origin/main before intake creation")
    fail_unless(not git("show-ref", "--verify", f"refs/heads/{branch}", check=False), f"branch already exists: {branch}; resume its existing checkpoint instead")
    fail_unless(not git("show-ref", "--verify", f"refs/remotes/origin/{branch}", check=False), f"remote branch already exists: {branch}; resume its existing checkpoint instead")
    fail_unless(github_ref_sha(f"heads/{branch}", required=False) is None, f"GitHub branch already exists: {branch}; resume its existing checkpoint instead")
    fail_unless(not git("ls-remote", "--heads", "origin", f"refs/heads/{branch}"), f"remote branch already exists: {branch}; resume its existing checkpoint instead")
    timestamp = now()
    data: dict[str, Any] = {
        "schemaVersion": SCHEMA_VERSION, "intakeId": intake_id, "slug": slug, "title": args.title,
        "sourceKind": args.source_kind, "requestSummary": args.request_summary,
        "decisionQuestion": args.decision_question, "artifactType": None, "audiences": [],
        "scopeSummary": None, "deltaSummary": None, "requestedActions": actions,
        "inputReferences": input_references, "evidenceReferences": [], "canonicalState": "INTAKE",
        "statusReason": "Authorized public-safe intake created.", "repositoryRemote": repository_remote,
        "baseBranch": "main", "baseSha": base, "branch": branch,
        "checkpointCreatedAt": timestamp, "updatedAt": timestamp, "canonicalPaths": [], "derivedPaths": [],
        "localValidation": "pending", "localValidationDigest": None, "candidateSha": None, "candidateEnvelopeSha256": None, "prNumber": None, "prUrl": None, "prHeadSha": None,
        "prDraft": True, "reviewDisposition": "pending", "acceptedSha": None, "checkedSha": None,
        "reviewEvidenceUrls": [], "checkDisposition": "pending", "checkUrls": [], "mergeSha": None,
        "branchCleanupStatus": "pending", "cleanupEvidence": [], "mainValidationUrl": None,
        "pagesRunUrl": None, "manifestSha256": None, "closureEvidenceUrl": None, "liveBaseUrl": None,
        "manifestAssertions": [], "routeAssertions": [],
        "publicationStatus": "pending", "residualLimitations": [], "nextGate": "Complete framing and evidence plan.",
        "blockerOwnerRole": None, "responsibleStage": None,
    }
    validate_checkpoint_shape(data)
    spec_text = immutable_spec(args, intake_id, checkpoint, repository_remote) if spec is not None else None
    branch_created = False
    try:
        git("switch", "-c", branch, base)
        branch_created = True
        atomic_json(checkpoint, data)
        if spec is not None and spec_text is not None:
            atomic_text(spec, spec_text)
    except Exception:
        checkpoint.unlink(missing_ok=True)
        if spec is not None:
            spec.unlink(missing_ok=True)
        if branch_created and git("branch", "--show-current", check=False) == branch:
            git("switch", "main", check=False)
            git("branch", "-d", branch, check=False)
        raise
    print(json.dumps({"checkpoint": checkpoint.relative_to(ROOT).as_posix(), "spec": spec.relative_to(ROOT).as_posix() if spec else None, "branch": branch, "baseSha": base}))
    return 0


def resolve_sha(value: str | None) -> str | None:
    if value is None:
        return None
    return git("rev-parse", "--verify", f"{value}^{{commit}}") if value == "HEAD" else full_sha("SHA", value)


def command_record(args: argparse.Namespace) -> int:
    path, data = load_checkpoint(args.checkpoint)
    previous_state = data["canonicalState"]
    fail_unless(previous_state != "CLOSED", "CLOSED is immutable; create a superseding intake for any correction")
    previous_candidate = data["candidateSha"]
    locked_states = {"CANDIDATE", "REVIEWED", "VALIDATED", "MERGED", "PUBLISHED", "CLOSED"}
    if previous_state in locked_states:
        locked_scalars = {
            "artifactType": args.artifact_type,
            "scopeSummary": args.scope_summary,
            "deltaSummary": args.delta_summary,
        }
        changed = [key for key, value in locked_scalars.items() if value is not None and value != data[key]]
        fail_unless(not changed, f"change framing fields only after returning to REWORK: {', '.join(changed)}")
        fail_unless(args.local_validation is None, "record local validation again only after returning to REWORK")
    if args.requested_actions is not None:
        fail_unless(bool(args.status_reason) and bool(args.input_reference), "changing requested actions requires --status-reason and a current --input-reference")
        data["requestedActions"] = parse_actions(args.requested_actions)
    scalar = {
        "canonicalState": args.state, "statusReason": args.status_reason,
        "artifactType": args.artifact_type, "scopeSummary": args.scope_summary,
        "deltaSummary": args.delta_summary,
        "localValidation": args.local_validation, "candidateSha": resolve_sha(args.candidate_sha),
        "prNumber": args.pr_number, "prUrl": args.pr_url,
        "prHeadSha": resolve_sha(args.pr_head_sha), "prDraft": args.pr_draft,
        "reviewDisposition": args.review_disposition, "acceptedSha": resolve_sha(args.accepted_sha),
        "checkedSha": resolve_sha(args.checked_sha), "checkDisposition": args.check_disposition,
        "mergeSha": resolve_sha(args.merge_sha), "mainValidationUrl": args.main_validation_url,
        "pagesRunUrl": args.pages_run_url, "manifestSha256": args.manifest_sha256,
        "closureEvidenceUrl": args.closure_evidence_url,
        "liveBaseUrl": args.live_base_url,
        "publicationStatus": args.publication_status, "nextGate": args.next_gate,
        "branchCleanupStatus": args.branch_cleanup_status,
        "blockerOwnerRole": args.blocker_owner_role, "responsibleStage": args.responsible_stage,
    }
    for key, value in scalar.items():
        if value is not None:
            data[key] = value
    if args.local_validation is not None:
        data["localValidationDigest"] = source_tree_digest() if args.local_validation == "pass" else None
    if args.candidate_sha is not None and data["candidateSha"] != previous_candidate:
        data.update({
            "candidateEnvelopeSha256": None,
            "acceptedSha": None, "checkedSha": None, "reviewDisposition": "pending",
            "reviewEvidenceUrls": [], "checkDisposition": "pending", "checkUrls": [],
            "mergeSha": None, "branchCleanupStatus": "pending", "cleanupEvidence": [],
            "mainValidationUrl": None, "pagesRunUrl": None, "manifestSha256": None,
            "closureEvidenceUrl": None,
            "liveBaseUrl": None, "manifestAssertions": [],
            "routeAssertions": [], "publicationStatus": "pending",
        })
    list_values = {
        "audiences": args.audience, "inputReferences": args.input_reference,
        "evidenceReferences": args.evidence_reference,
        "canonicalPaths": args.canonical_path, "derivedPaths": args.derived_path,
        "reviewEvidenceUrls": args.review_evidence_url, "checkUrls": args.check_url,
        "cleanupEvidence": args.cleanup_evidence, "manifestAssertions": args.manifest_assertion,
        "routeAssertions": args.route_assertion, "residualLimitations": args.residual_limitation,
    }
    locked_content_fields = {"audiences", "inputReferences", "evidenceReferences", "canonicalPaths", "derivedPaths"}
    for key, values in list_values.items():
        if values:
            authority_reference = key == "inputReferences" and args.requested_actions is not None
            if key in locked_content_fields and previous_state in locked_states and not authority_reference:
                raise WorkflowError(f"append {key} only before CANDIDATE or after returning to REWORK/BLOCKED")
            if key == "canonicalPaths":
                values = [canonical_path(value) for value in values]
            elif key == "derivedPaths":
                values = [derived_reference(value) for value in values]
            data[key] = list(dict.fromkeys([*data[key], *values]))
    if previous_state in {"REWORK", "BLOCKED"} and (
        args.artifact_type is not None
        or args.scope_summary is not None
        or args.delta_summary is not None
        or any((args.audience, args.evidence_reference, args.canonical_path, args.derived_path))
    ):
        data["candidateEnvelopeSha256"] = None
    for key in ("prUrl", "mainValidationUrl", "pagesRunUrl", "liveBaseUrl", "closureEvidenceUrl"):
        if data[key]:
            safe_url(key, data[key])
    next_state = data["canonicalState"]
    candidate_states = {"CANDIDATE", "REVIEWED", "VALIDATED", "MERGED", "PUBLISHED", "CLOSED"}
    if next_state in candidate_states and data["candidateEnvelopeSha256"] is None:
        data["candidateEnvelopeSha256"] = candidate_envelope_digest(data)
    data["updatedAt"] = now()
    if next_state != previous_state:
        fail_unless(next_state in TRANSITIONS[previous_state], f"invalid workflow transition: {previous_state} -> {next_state}")
    validate_checkpoint_shape(data, path)
    if data["canonicalState"] in {"CANDIDATE", "REVIEWED", "VALIDATED"}:
        verify_candidate_derived_files(data)
        fail_unless(data["localValidationDigest"] == source_tree_digest(), "candidate bytes differ from the locally validated source-tree digest")
    atomic_json(path, data)
    print(f"OK: {data['intakeId']} recorded state {data['canonicalState']}")
    return 0


def command_replace_list(args: argparse.Namespace) -> int:
    path, data = load_checkpoint(args.checkpoint)
    fail_unless(data["canonicalState"] != "CLOSED", "CLOSED is immutable; create a superseding intake for any correction")
    locked_content_fields = {"audiences", "inputReferences", "evidenceReferences", "canonicalPaths", "derivedPaths"}
    if args.field in locked_content_fields and data["canonicalState"] in {"CANDIDATE", "REVIEWED", "VALIDATED", "MERGED", "PUBLISHED", "CLOSED"}:
        raise WorkflowError(f"replace {args.field} only before CANDIDATE or after returning to REWORK/BLOCKED")
    data[args.field] = list(dict.fromkeys(args.value))
    if args.field in {"audiences", "evidenceReferences", "canonicalPaths", "derivedPaths"}:
        data["candidateEnvelopeSha256"] = None
    data["statusReason"] = safe_line("replacement reason", args.status_reason, 500)
    data["updatedAt"] = now()
    validate_checkpoint_shape(data, path)
    atomic_json(path, data)
    print(f"OK: {data['intakeId']} replaced {args.field} with {len(data[args.field])} values")
    return 0


def display(value: Any) -> str:
    if value is None:
        return "pending"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, list):
        return ", ".join(value) if value else "none"
    return str(value)


def rendered_cell(value: Any) -> str:
    escaped = html.escape(display(value), quote=True).replace("|", "&#124;").replace("`", "&#96;")
    return f"<code>{escaped}</code>"


def rendered_checkpoint(data: dict[str, Any]) -> str:
    rows = (
        ("Intake", "intakeId"), ("State", "canonicalState"), ("Base", "baseSha"),
        ("Branch", "branch"), ("Candidate", "candidateSha"), ("Candidate envelope", "candidateEnvelopeSha256"), ("Accepted", "acceptedSha"),
        ("CI checked", "checkedSha"), ("PR head", "prHeadSha"), ("PR", "prNumber"),
        ("PR URL", "prUrl"),
        ("Local validation", "localValidation"), ("Validated source tree", "localValidationDigest"),
        ("Review", "reviewDisposition"), ("Checks", "checkDisposition"), ("Merge", "mergeSha"),
        ("Publication", "publicationStatus"), ("Next gate", "nextGate"), ("Updated", "updatedAt"),
    )
    lines = [CHECKPOINT_START, "| Workflow field | Recorded value |", "|---|---|"]
    for label, key in rows:
        lines.append(f"| {label} | {rendered_cell(data[key])} |")
    payload = base64.urlsafe_b64encode(
        json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    ).decode("ascii")
    lines.append(f"<!-- {CHECKPOINT_PAYLOAD}:{payload} -->")
    lines.append(CHECKPOINT_END)
    return "\n".join(lines)


def embedded_checkpoint(body: str) -> dict[str, Any]:
    block = checkpoint_block(body)
    matches = re.findall(rf"<!-- {re.escape(CHECKPOINT_PAYLOAD)}:([A-Za-z0-9_-]+={{0,2}}) -->", block)
    fail_unless(len(matches) == 1, "PR checkpoint block must contain exactly one machine payload")
    try:
        decoded = base64.b64decode(matches[0], altchars=b"-_", validate=True)
        data = json.loads(decoded.decode("utf-8"))
    except (ValueError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise WorkflowError("PR checkpoint machine payload is invalid") from exc
    fail_unless(isinstance(data, dict) and set(data) == CHECKPOINT_KEYS, "PR checkpoint payload fields differ from the current schema")
    fail_unless(block.strip() == rendered_checkpoint(data).strip(), "PR checkpoint table and machine payload are inconsistent")
    return data


def checkpoint_block(body: str) -> str:
    """Extract one ordered durable block without leaking malformed body text."""
    fail_unless(body.count(CHECKPOINT_START) == 1 and body.count(CHECKPOINT_END) == 1, "PR body must contain exactly one workflow checkpoint block")
    start = body.find(CHECKPOINT_START)
    finish = body.find(CHECKPOINT_END)
    fail_unless(start >= 0 and finish > start, "PR workflow checkpoint markers are out of order")
    return body[start : finish + len(CHECKPOINT_END)]


def command_render(args: argparse.Namespace) -> int:
    _, data = load_checkpoint(args.checkpoint)
    print(rendered_checkpoint(data))
    return 0


def validate_repo_errors() -> list[str]:
    errors: list[str] = []
    for relative in REQUIRED_REPO_FILES:
        if not (ROOT / relative).is_file():
            errors.append(f"required workflow file is missing: {relative}")
    if git_path_names("ls-files", ".study-workflow"):
        errors.append("mutable .study-workflow checkpoint data must never be tracked")
    gitignore = ROOT / ".gitignore"
    if gitignore.is_file() and ".study-workflow/" not in gitignore.read_text(encoding="utf-8").splitlines():
        errors.append(".gitignore must exclude .study-workflow/")
    workflow = ROOT / "docs" / "46-study-publication-workflow.md"
    if workflow.is_file():
        text = workflow.read_text(encoding="utf-8")
        errors.extend(f"workflow heading is missing: {heading}" for heading in WORKFLOW_HEADINGS if heading not in text)
        errors.extend(f"workflow state is missing: {state}" for state in STATES if f"`{state}`" not in text)
    if TEMPLATE.is_file():
        text = TEMPLATE.read_text(encoding="utf-8")
        errors.extend(f"intake template section is missing: {number}" for number in range(1, 15) if not re.search(rf"^## {number}\. ", text, re.M))
        for marker in ("Candidate head SHA", "Candidate envelope SHA-256", "Validated source-tree SHA-256", "Accepted head SHA", "PR checked head SHA", "Merge/squash SHA", "Publication status"):
            if marker not in text:
                errors.append(f"intake template release field is missing: {marker}")
    skill = ROOT / ".agents" / "skills" / "publish-api-study" / "SKILL.md"
    if skill.is_file():
        skill_text = skill.read_text(encoding="utf-8")
        frontmatter = re.match(r"^---\n([\s\S]*?)\n---\n", skill_text)
        if not frontmatter or {line.split(":", 1)[0].strip() for line in frontmatter.group(1).splitlines() if ":" in line} != {"name", "description"}:
            errors.append("skill frontmatter must contain only name and description")
        for flag in ("--request-summary", "--decision-question", "--change-class", "resume --pr-number", "replace-list", "--phase draft", "--phase release", "--match-head-commit", "requirements-validation.txt"):
            if flag not in skill_text:
                errors.append(f"skill command contract is missing {flag}")
    contract = ROOT / ".agents" / "skills" / "publish-api-study" / "references" / "repo-contract.md"
    if contract.is_file():
        contract_text = contract.read_text(encoding="utf-8")
        for flag in ("--request-summary", "--decision-question", "--change-class", "resume --pr-number", "--phase draft", "--phase release", "--match-head-commit", "requirements-validation.txt"):
            if flag not in contract_text:
                errors.append(f"skill repository contract is missing {flag}")
    operator_documents = (
        ROOT / "README.md",
        workflow,
        skill,
        contract,
        TEMPLATE,
        ROOT / ".github" / "pull_request_template.md",
    )
    for document in operator_documents:
        if not document.is_file():
            continue
        operator_text = document.read_text(encoding="utf-8")
        if ".venv/bin/python -I scripts/study_workflow.py" not in operator_text:
            errors.append(f"operator workflow omits the isolated CLI invocation: {document.relative_to(ROOT)}")
        if "python3 scripts/study_workflow.py" in operator_text:
            errors.append(f"operator workflow contains a non-isolated CLI invocation: {document.relative_to(ROOT)}")
    agent_ui = ROOT / ".agents" / "skills" / "publish-api-study" / "agents" / "openai.yaml"
    if agent_ui.is_file():
        ui_text = agent_ui.read_text(encoding="utf-8")
        for marker in ("interface:", "display_name:", "short_description:", "default_prompt:", "$publish-api-study"):
            if marker not in ui_text:
                errors.append(f"skill UI metadata is missing {marker}")
    if SPEC_ROOT.exists():
        for spec in sorted(SPEC_ROOT.glob("*.md")):
            text = spec.read_text(encoding="utf-8")
            if "## 10. " in text or "Candidate head SHA" in text:
                errors.append(f"immutable intake spec contains mutable operational fields: {spec.relative_to(ROOT)}")
            if not re.search(r"\*\*Intake ID:\*\*\s*`INTAKE-\d{8}-[a-z0-9-]+`", text):
                errors.append(f"immutable intake spec has no valid Intake ID: {spec.relative_to(ROOT)}")
    errors.extend(public_content_errors())
    return sorted(set(errors))


def verify_base(data: dict[str, Any], base: str) -> str:
    full_sha("--base", base)
    git("cat-file", "-e", f"{base}^{{commit}}")
    fail_unless(data["baseSha"] == base, "--base does not match checkpoint baseSha")
    fail_unless(same_repository(data["repositoryRemote"], origin_remote_url()), "checkpoint repositoryRemote differs from origin")
    fetch_authenticated_main()
    fail_unless(run(("git", "merge-base", "--is-ancestor", base, "origin/main"), check=False).returncode == 0, "recorded base is not reachable from origin/main")
    fail_unless(run(("git", "merge-base", "--is-ancestor", base, "HEAD"), check=False).returncode == 0, "recorded base is not an ancestor of HEAD")
    return base


def verify_history_repository() -> None:
    """Reject local Git graph rewrites that can hide candidate history."""
    fail_unless(
        git("rev-parse", "--is-shallow-repository") == "false",
        "history certification requires a complete, non-shallow repository",
    )
    graft_value = git("rev-parse", "--git-path", "info/grafts")
    graft_path = Path(graft_value)
    if not graft_path.is_absolute():
        graft_path = ROOT / graft_path
    fail_unless(not graft_path.exists(), "history certification rejects legacy Git grafts")


def actual_pr(number: int) -> dict[str, Any]:
    try:
        return json.loads(gh(
            "pr", "view", str(number), "--json",
            "number,url,title,body,baseRefName,headRefOid,headRefName,headRepositoryOwner,isCrossRepository,isDraft,state,statusCheckRollup,mergeCommit",
            "--repo", github_owner_repo(),
        ))
    except json.JSONDecodeError as exc:
        raise WorkflowError("gh returned invalid PR JSON") from exc


def verify_actual_pr_checkpoint(data: dict[str, Any], pr: dict[str, Any], head: str) -> None:
    verify_pr_repository_identity(data, pr)
    fail_unless(pr.get("baseRefName") == "main", "workflow requires a PR targeting main")
    fail_unless(pr.get("isCrossRepository") is False, "workflow requires a same-repository PR")
    fail_unless(pr.get("headRefName") == data["branch"] and pr.get("headRefOid") == head, "actual PR branch/head differs from the checkpoint and HEAD")
    fail_unless(pr.get("url") == data["prUrl"], "actual PR URL differs from the checkpoint")
    fail_unless(pr.get("state") == "OPEN" and pr.get("isDraft") is data["prDraft"], "actual PR open/draft state differs from the checkpoint")
    remote_head = git("ls-remote", "--heads", "origin", f"refs/heads/{data['branch']}")
    fail_unless(bool(remote_head) and remote_head.split()[0] == head, "origin intake branch does not equal the recorded PR head")
    fail_unless(github_ref_sha(f"heads/{data['branch']}") == head, "GitHub intake branch does not equal the recorded PR head")
    verify_pr_checkpoint_body(data, pr)


def verify_pr_checkpoint_body(data: dict[str, Any], pr: dict[str, Any]) -> None:
    """Require the durable PR mirror to equal the local ignored checkpoint."""
    pr_text = f"{pr.get('title') or ''}\n{pr.get('body') or ''}"
    pr_findings = scan_text(pr_text, f"PR {data['prNumber']} title/body")
    if pr_findings:
        raise WorkflowError(pr_findings[0])
    body = pr.get("body") or ""
    fail_unless(checkpoint_block(body).strip() == rendered_checkpoint(data).strip(), "PR checkpoint block is stale or differs from the validated local checkpoint")


def verify_pr_repository_identity(data: dict[str, Any], pr: dict[str, Any]) -> None:
    """Bind a GitHub response to origin, not ambient CLI repository context."""
    owner_repo = github_owner_repo()
    owner, _ = owner_repo.split("/", 1)
    number = data.get("prNumber")
    fail_unless(type(number) is int and pr.get("number") == number, "actual PR number differs from the checkpoint")
    expected_url = f"https://github.com/{owner_repo}/pull/{number}"
    fail_unless(pr.get("url") == expected_url and data.get("prUrl") == expected_url, "actual PR URL/repository differs from origin and the checkpoint")
    head_owner = pr.get("headRepositoryOwner") if isinstance(pr.get("headRepositoryOwner"), dict) else {}
    fail_unless(str(head_owner.get("login", "")).lower() == owner.lower(), "actual PR head repository owner differs from origin")


def verify_merged_pr_checkpoint(data: dict[str, Any], pr: dict[str, Any], merge: str) -> None:
    verify_pr_repository_identity(data, pr)
    merge_commit = pr.get("mergeCommit") if isinstance(pr.get("mergeCommit"), dict) else {}
    fail_unless(pr.get("state") == "MERGED" and merge_commit.get("oid") == merge, "recorded merge SHA is not the PR merge commit")
    fail_unless(pr.get("isCrossRepository") is False, "workflow requires a same-repository merged PR")
    fail_unless(pr.get("baseRefName") == "main" and pr.get("url") == data["prUrl"], "merged PR identity/base differs from the checkpoint")
    fail_unless(pr.get("headRefName") == data["branch"] and pr.get("headRefOid") == data["candidateSha"], "merged PR head differs from the accepted candidate")
    verify_pr_checkpoint_body(data, pr)


def command_resume(args: argparse.Namespace) -> int:
    """Reconstruct an ignored checkpoint from its exact durable PR payload."""
    full_sha("--base", args.base)
    requested_actions = parse_actions(args.requested_actions)
    fail_unless(not git("status", "--porcelain", "--untracked-files=all"), "resume requires a clean working tree")
    current_branch = git("branch", "--show-current")
    fail_unless(current_branch == "main" or current_branch.startswith("study/"), "resume must start from main or an intake study branch")
    pr = actual_pr(args.pr_number)
    pr_text = f"{pr.get('title') or ''}\n{pr.get('body') or ''}"
    findings = scan_text(pr_text, f"PR {args.pr_number} title/body")
    if findings:
        raise WorkflowError(findings[0])
    body = pr.get("body")
    fail_unless(isinstance(body, str), "PR body is unavailable")
    data = embedded_checkpoint(body)
    validate_checkpoint_shape(data, verify_artifacts=False)
    slug = safe_slug(data.get("slug", ""))
    intake_id = data.get("intakeId")
    fail_unless(isinstance(intake_id, str) and bool(re.fullmatch(r"INTAKE-\d{8}-[a-z0-9]+(?:-[a-z0-9]+)*", intake_id)), "durable checkpoint intakeId is invalid")
    fail_unless(intake_id.endswith(f"-{slug}"), "durable checkpoint intakeId and slug differ")
    checkpoint = CHECKPOINT_ROOT / f"{intake_id.lower()}.json"
    ensure_local_root(CHECKPOINT_ROOT, "checkpoint")
    fail_unless(not checkpoint.exists(), f"checkpoint already exists: {checkpoint.relative_to(ROOT)}; use the existing record")
    fail_unless(data.get("branch") == f"study/{slug}", "durable checkpoint branch is invalid")
    full_sha("durable baseSha", data.get("baseSha"))
    full_sha("durable prHeadSha", data.get("prHeadSha"))
    fail_unless(data["requestedActions"] == requested_actions, "current explicit requested actions differ from the durable checkpoint")
    fail_unless(data["baseSha"] == args.base, "--base differs from the durable checkpoint")
    fail_unless(data["prNumber"] == args.pr_number and data["prUrl"] == pr.get("url"), "PR identity differs from the durable checkpoint")
    verify_pr_repository_identity(data, pr)
    fail_unless(pr.get("baseRefName") == "main" and data["baseBranch"] == "main", "resume requires a PR targeting main")
    fail_unless(pr.get("isCrossRepository") is False, "resume requires a same-repository PR")
    fail_unless(data["branch"] == pr.get("headRefName") and data["prHeadSha"] == pr.get("headRefOid"), "PR head differs from the durable checkpoint")
    fail_unless(same_repository(data["repositoryRemote"], origin_remote_url()), "durable checkpoint remote differs from origin")

    fetch_authenticated_main()
    fail_unless(run(("git", "merge-base", "--is-ancestor", args.base, "origin/main"), check=False).returncode == 0, "durable base is not reachable from origin/main")
    state = pr.get("state")
    if state == "OPEN":
        fail_unless(pr.get("isDraft") is data["prDraft"], "open PR draft state differs from the durable checkpoint")
        git("fetch", "origin", f"{data['branch']}:refs/remotes/origin/{data['branch']}")
        remote_head = git("rev-parse", f"origin/{data['branch']}")
        fail_unless(remote_head == data["prHeadSha"], "remote intake branch differs from the durable PR head")
        fail_unless(github_ref_sha(f"heads/{data['branch']}") == remote_head, "GitHub intake branch differs from the durable PR head")
        local_exists = bool(git("show-ref", "--verify", f"refs/heads/{data['branch']}", check=False))
        if local_exists:
            fail_unless(git("rev-parse", data["branch"]) == remote_head, "existing local intake branch differs from the durable PR head")
            git("switch", data["branch"])
        else:
            fail_unless(current_branch == "main", "create the missing local intake branch from main")
            git("switch", "-c", data["branch"], "--track", f"origin/{data['branch']}")
    elif state == "MERGED":
        fail_unless(current_branch == "main", "merged intake resume must start from local main")
        fail_unless(data["canonicalState"] in {"VALIDATED", "MERGED", "PUBLISHED", "CLOSED"}, "merged PR durable state was not release-validated")
        fail_unless({"merge", "branch-cleanup"}.issubset(set(data["requestedActions"])), "merged intake resume lacks merge/branch-cleanup authority")
        verify_candidate_acceptance(data, pr)
        verify_accepted_candidate_tree(data, pr)
        fail_unless(not git("show-ref", "--verify", f"refs/heads/{data['branch']}", check=False), "remove the exact local intake branch before resuming the merged PR")
        fail_unless(github_ref_sha(f"heads/{data['branch']}", required=False) is None, "GitHub intake branch still exists; complete its authorized cleanup before resume")
        fail_unless(not git("ls-remote", "--heads", "origin", data["branch"]), "remote intake branch still exists; complete its authorized cleanup before resume")
        git("merge", "--ff-only", "origin/main")
        origin_main = git("rev-parse", "origin/main")
        fail_unless(git("rev-parse", "HEAD") == origin_main, "local main must exactly equal origin/main for merged intake resume")
        merge_commit = pr.get("mergeCommit") if isinstance(pr.get("mergeCommit"), dict) else {}
        merge_sha = full_sha("merged PR mergeCommit", merge_commit.get("oid"))
        fail_unless(run(("git", "merge-base", "--is-ancestor", merge_sha, "origin/main"), check=False).returncode == 0, "merged PR commit is not reachable from origin/main")
        fail_unless(working_tree_clean_at(origin_main), "merged intake resume requires clean raw worktree bytes at current origin/main")
        if data["canonicalState"] == "VALIDATED":
            data.update({
                "canonicalState": "MERGED",
                "statusReason": "Reconciled the validated durable PR record with its verified merge and completed branch cleanup.",
                "mergeSha": merge_sha,
                "branchCleanupStatus": "complete",
                "cleanupEvidence": [
                    "verified: local intake branch absent",
                    "verified: remote intake branch absent",
                ],
                "nextGate": "Verify main validation, Pages deployment, live provenance, and closure evidence.",
                "updatedAt": now(),
            })
        else:
            fail_unless(data["mergeSha"] == merge_sha and data["branchCleanupStatus"] == "complete", "durable merged state differs from the actual PR merge/cleanup state")
    else:
        raise WorkflowError("only open or merged pull requests can be resumed")

    # Open PRs must still describe artifacts in the checked-out candidate.
    # Merged records were already re-authenticated against refs/pull/<n>/head;
    # later governed main changes must not make their durable history unrestorable.
    validate_checkpoint_shape(data, verify_artifacts=state == "OPEN")
    if state == "OPEN":
        fail_unless(working_tree_clean_at(data["prHeadSha"]), "resumed PR branch raw bytes differ from its recorded head")
        fail_unless(data["localValidationDigest"] == source_tree_digest(), "resumed PR branch differs from its locally validated source-tree digest")
        if data["canonicalState"] in {"CANDIDATE", "REVIEWED", "VALIDATED"}:
            verify_candidate_derived_files(data)
    atomic_json(checkpoint, data)
    print(json.dumps({"checkpoint": checkpoint.relative_to(ROOT).as_posix(), "branch": git("branch", "--show-current"), "prNumber": args.pr_number, "state": data["canonicalState"]}))
    return 0


def authenticated_check_urls(rollup: Any, expected_sha: str) -> set[str] | None:
    if not isinstance(rollup, list) or not rollup:
        return None
    accepted = {"SUCCESS", "NEUTRAL", "SKIPPED"}
    owner_repo = github_owner_repo()
    required_runs: dict[str, str] = {}
    for item in rollup:
        if not isinstance(item, dict):
            return None
        outcome = item.get("conclusion") or item.get("state") or ""
        if str(outcome).upper() not in accepted:
            return None
        name = item.get("name") or item.get("context")
        if isinstance(name, str) and name in REQUIRED_PR_CHECKS:
            if name in required_runs or str(outcome).upper() != "SUCCESS":
                return None
            details = item.get("detailsUrl")
            workflow = item.get("workflowName")
            if not isinstance(details, str) or str(workflow).lower() != "validate":
                return None
            split = urlsplit(details)
            match = re.fullmatch(rf"/{re.escape(owner_repo)}/actions/runs/(\d+)(?:/job/\d+)?/?", split.path)
            if split.scheme != "https" or split.netloc != "github.com" or match is None:
                return None
            required_runs[name] = f"https://github.com/{owner_repo}/actions/runs/{match.group(1)}"
    if set(required_runs) != REQUIRED_PR_CHECKS:
        return None
    try:
        for run_url in set(required_runs.values()):
            verify_action_run(run_url, expected_sha, "validate")
    except WorkflowError:
        return None
    return set(required_runs.values())


def checks_green(rollup: Any, expected_sha: str) -> bool:
    return authenticated_check_urls(rollup, expected_sha) is not None


def fetch_same_pr_comment(value: str, pr_number: int) -> str:
    owner_repo = github_owner_repo()
    split = urlsplit(value)
    path_match = re.fullmatch(rf"/{re.escape(owner_repo)}/pull/{pr_number}", split.path)
    comment_match = re.fullmatch(r"issuecomment-(\d+)", split.fragment)
    fail_unless(split.scheme == "https" and split.netloc == "github.com" and path_match is not None and comment_match is not None, "evidence URL must identify a comment on the recorded PR")
    try:
        comment = json.loads(gh("api", f"repos/{owner_repo}/issues/comments/{comment_match.group(1)}", "--hostname", "github.com"))
    except json.JSONDecodeError as exc:
        raise WorkflowError("gh returned invalid PR-comment JSON") from exc
    fail_unless(isinstance(comment, dict) and comment.get("html_url") == value and str(comment.get("issue_url", "")).endswith(f"/issues/{pr_number}"), "GitHub comment does not belong to the recorded PR")
    body = comment.get("body", "")
    fail_unless(isinstance(body, str), "PR-comment body is invalid")
    findings = scan_text(body, f"PR {pr_number} evidence")
    if findings:
        raise WorkflowError(findings[0])
    return body


def verify_review_evidence(urls: list[str], pr_number: int, accepted_sha: str, envelope_sha256: str) -> None:
    verified = False
    for value in urls:
        body = fetch_same_pr_comment(value, pr_number).replace("\r\n", "\n").replace("\r", "\n")
        exact_block = re.search(
            rf"(?m)^Accepted head SHA: {re.escape(accepted_sha)}\n"
            rf"^Candidate envelope SHA-256: {re.escape(envelope_sha256)}\n"
            r"^Independent reviewer: [^\r\n]+\n"
            r"^Reviewer did not author candidate: yes\n"
            r"^Review disposition: pass[ \t]*$",
            body,
        )
        if exact_block:
            verified = True
    fail_unless(verified, "independent review evidence must contain the exact contiguous five-line acceptance block for the accepted SHA and candidate envelope")


def verify_candidate_acceptance(data: dict[str, Any], pr: dict[str, Any]) -> None:
    """Re-authenticate the exact candidate review and CI evidence."""
    candidate = full_sha("candidateSha", data["candidateSha"])
    expected = [data[key] for key in ("acceptedSha", "checkedSha", "prHeadSha")]
    fail_unless(all(value == candidate for value in expected), "candidate, accepted, checked, and recorded PR head SHAs must be identical")
    fail_unless(data["reviewDisposition"] == "pass", "independent review disposition must be pass")
    fail_unless(data["checkDisposition"] == "green", "required check disposition must be green")
    fail_unless(data["prNumber"] is not None, "candidate acceptance requires a PR number")
    envelope = data["candidateEnvelopeSha256"]
    fail_unless(isinstance(envelope, str) and envelope == candidate_envelope_digest(data), "candidate envelope digest is missing or differs from the accepted scope")
    verify_review_evidence(data["reviewEvidenceUrls"], data["prNumber"], candidate, envelope)
    authenticated = authenticated_check_urls(pr.get("statusCheckRollup"), candidate)
    fail_unless(authenticated is not None, "actual PR checks are missing, pending, failed, or are not authenticated required GitHub Actions jobs")
    fail_unless(set(data["checkUrls"]) == authenticated, "recorded check URLs differ from the authenticated required runs")


def verify_accepted_candidate_tree(data: dict[str, Any], pr: dict[str, Any]) -> None:
    """Re-authenticate reviewed source and artifact claims after branch cleanup."""
    candidate = full_sha("candidateSha", data["candidateSha"])
    number = data.get("prNumber")
    fail_unless(type(number) is int and pr.get("number") == number, "accepted candidate PR identity is invalid")
    fail_unless(pr.get("headRefOid") == candidate, "merged PR no longer identifies the accepted candidate")
    remote_ref = f"refs/remotes/pull/{number}/head"
    fetched = run(
        (
            "git", "fetch", "--force", "origin",
            f"refs/pull/{number}/head:{remote_ref}",
        ),
        check=False,
    )
    fail_unless(fetched.returncode == 0, "unable to fetch the authenticated merged-PR candidate tree")
    fail_unless(git("rev-parse", remote_ref) == candidate, "fetched merged-PR candidate differs from the authenticated PR head")
    base = full_sha("baseSha", data["baseSha"])
    fail_unless(
        run(("git", "merge-base", "--is-ancestor", base, candidate), check=False).returncode == 0,
        "immutable base is not an ancestor of the accepted candidate",
    )
    history_errors = public_content_errors(base, candidate, include_generated=False)
    if history_errors:
        raise WorkflowError(history_errors[0])
    fail_unless(
        data["localValidationDigest"] == source_tree_digest_at_commit(candidate),
        "accepted candidate tree differs from the recorded local-validation digest",
    )
    entries = commit_tree_entries(candidate)
    for value in data["canonicalPaths"]:
        fail_unless(
            entries.get(value, (None, None, None))[:2] in {("100644", "blob"), ("100755", "blob")},
            f"accepted canonical path is not a tracked regular blob: {safe_location(value)}",
        )
    derived_files = {item for item in data["derivedPaths"] if not item.startswith("#/")}
    ignored = ignored_paths_at_commit(entries, derived_files)
    for value in sorted(derived_files):
        fail_unless(
            not value.startswith(("_site/", "evidence/raw/", ".study-workflow/")),
            f"accepted derived path is generated, private, or workflow-local: {safe_location(value)}",
        )
        fail_unless(value not in ignored, f"accepted derived path is ignored or private: {safe_location(value)}")
        fail_unless(
            entries.get(value, (None, None, None))[:2] in {("100644", "blob"), ("100755", "blob")},
            f"accepted derived path is not a tracked regular blob: {safe_location(value)}",
        )


def verify_closure_evidence(
    url: str,
    pr_number: int,
    merge_sha: str,
    manifest_sha: str,
) -> None:
    body = fetch_same_pr_comment(url, pr_number)
    fail_unless(bool(re.search(r"(?im)^Publication status:\s*published\s*$", body)), "closure comment must record published status")
    fail_unless(bool(re.search(rf"(?im)^Merge SHA:\s*{re.escape(merge_sha)}\s*$", body)), "closure comment must name the merge SHA")
    fail_unless(bool(re.search(rf"(?im)^Manifest SHA-256:\s*{re.escape(manifest_sha)}\s*$", body)), "closure comment must name the deployed manifest SHA-256")


def verify_action_run(url: str, expected_sha: str, workflow_name: str) -> None:
    split = urlsplit(url)
    match = re.search(r"/actions/runs/(\d+)(?:/|$)", split.path)
    fail_unless(split.scheme == "https" and split.netloc == "github.com" and match is not None, f"{workflow_name} run URL is not a GitHub Actions run")
    try:
        run_data = json.loads(gh("run", "view", match.group(1), "--json", "headSha,status,conclusion,url,workflowName", "--repo", github_owner_repo()))
    except json.JSONDecodeError as exc:
        raise WorkflowError(f"gh returned invalid {workflow_name} run JSON") from exc
    fail_unless(run_data.get("headSha") == expected_sha, f"{workflow_name} run did not execute the merge SHA")
    fail_unless(str(run_data.get("url", "")).rstrip("/") == url.rstrip("/"), f"{workflow_name} run URL differs from the recorded run")
    fail_unless(run_data.get("status") == "completed" and run_data.get("conclusion") == "success", f"{workflow_name} run is not successfully completed")
    fail_unless(str(run_data.get("workflowName", "")).lower() == workflow_name.lower(), f"recorded run is not the {workflow_name} workflow")


def verify_pages_identity(value: str) -> None:
    owner_repo = github_owner_repo()
    try:
        pages = json.loads(gh("api", f"repos/{owner_repo}/pages", "--hostname", "github.com"))
    except json.JSONDecodeError as exc:
        raise WorkflowError("gh returned invalid Pages identity JSON") from exc
    expected = pages.get("html_url") if isinstance(pages, dict) else None
    fail_unless(isinstance(expected, str) and expected.rstrip("/") == value.rstrip("/"), "liveBaseUrl does not equal this repository's GitHub Pages URL")


def run_pages_verifier(data: dict[str, Any], merge: str) -> bool:
    """Verify from mergeSha without requiring the shared main tip to stay frozen."""
    with tempfile.TemporaryDirectory(prefix="apim-pages-verify-") as temporary:
        worktree = Path(temporary) / "source"
        added = run(("git", "worktree", "add", "--detach", str(worktree), merge), check=False)
        fail_unless(added.returncode == 0, "unable to create an isolated verifier checkout at mergeSha")
        try:
            verifier = [
                sys.executable, str(worktree / "scripts" / "verify_pages.py"),
                "--base-url", data["liveBaseUrl"],
                "--expected-revision", merge,
                "--expected-manifest-sha256", data["manifestSha256"],
            ]
            for value in data["canonicalPaths"]:
                verifier.extend(("--study-path", value))
            for value in data["routeAssertions"]:
                verifier.extend(("--expected-route", value))
            try:
                return subprocess.run(
                    tuple(verifier),
                    cwd=worktree,
                    check=False,
                    env=validation_environment(),
                    timeout=660,
                ).returncode == 0
            except subprocess.TimeoutExpired:
                return False
        finally:
            run(("git", "worktree", "remove", "--force", str(worktree)), check=False)


def command_check(args: argparse.Namespace) -> int:
    repo_errors = validate_repo_errors()
    if repo_errors:
        for error in repo_errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    _, data = load_checkpoint(args.checkpoint)
    base = verify_base(data, args.base)
    verify_history_repository()
    required_authority = set(PHASE_REQUIRED_ACTIONS[args.phase])
    if args.phase == "draft" and data["canonicalState"] in {"CANDIDATE", "REVIEWED", "VALIDATED"}:
        required_authority.update({"commit", "push", "pull-request"})
    missing_authority = required_authority - set(data["requestedActions"])
    fail_unless(not missing_authority, f"{args.phase} gate lacks explicit authority for: {', '.join(sorted(missing_authority))}")
    history_end = data["mergeSha"] if args.phase == "published" and data["mergeSha"] else "HEAD"
    history_errors = public_content_errors(base, history_end)
    if history_errors:
        raise WorkflowError(history_errors[0])
    head = git("rev-parse", "HEAD")
    if args.phase in {"draft", "release"}:
        fail_unless(git("branch", "--show-current") == data["branch"], "current branch does not match the intake-owned study branch")
        fail_unless(data["localValidation"] == "pass", "checkpoint localValidation must be pass")
        fail_unless(data["localValidationDigest"] == source_tree_digest(), "current source tree differs from the locally validated digest")
        fail_unless(data["canonicalState"] in {"PROJECTED", "CANDIDATE", "REVIEWED", "VALIDATED", "REWORK"}, "checkpoint state is not ready for draft/release validation")
        fail_unless(bool(data["canonicalPaths"]), "checkpoint must record at least one canonical path")
        for value in data["canonicalPaths"]:
            fail_unless((ROOT / value).is_file(), f"canonical path does not exist: {value}")
    if args.phase == "draft" and data["canonicalState"] in {"CANDIDATE", "REVIEWED", "VALIDATED"}:
        fail_unless(working_tree_clean_at(head), "candidate-or-later draft gate requires raw worktree bytes to match HEAD")
        fail_unless(data["candidateSha"] == head and data["prHeadSha"] == head, "draft gate candidate, PR head, and HEAD SHAs must be identical")
        fail_unless(data["prNumber"] is not None, "candidate-or-later draft gate requires a PR number")
        verify_actual_pr_checkpoint(data, actual_pr(data["prNumber"]), head)
        verify_candidate_derived_files(data)
    if args.phase == "draft":
        fail_unless(run_make_validate(), "make validate failed during draft gate")
        verify_local_derived_routes(data)
    if args.phase == "release":
        fail_unless(
            run(("git", "merge-base", "--is-ancestor", "origin/main", head), check=False).returncode == 0,
            "release candidate must be rebased onto the current origin/main",
        )
        fail_unless(working_tree_clean_at(head), "release gate requires a clean working tree whose raw bytes match HEAD")
        fail_unless(data["prNumber"] is not None, "release gate requires a PR number")
        pr = actual_pr(data["prNumber"])
        verify_actual_pr_checkpoint(data, pr, head)
        fail_unless(data["prDraft"] is False, "release gate requires a non-draft PR checkpoint")
        verify_candidate_acceptance(data, pr)
        verify_candidate_derived_files(data)
        fail_unless(data["canonicalState"] == "VALIDATED", "release gate requires canonicalState VALIDATED")
        fail_unless(run_make_validate(), "make validate failed during release gate")
        verify_local_derived_routes(data)
    if args.phase == "published":
        merge = full_sha("mergeSha", data["mergeSha"])
        fetch_authenticated_main()
        fail_unless(run(("git", "merge-base", "--is-ancestor", merge, "origin/main"), check=False).returncode == 0, "mergeSha is not reachable from origin/main")
        origin_main = git("rev-parse", "origin/main")
        fail_unless(git("branch", "--show-current") == "main" and git("rev-parse", "HEAD") == origin_main, "published gate must run from local main exactly at current origin/main")
        fail_unless(working_tree_clean_at(origin_main), "published gate requires a clean working tree whose raw bytes match current origin/main")
        fail_unless(data["prNumber"] is not None, "published gate requires the merged PR number")
        pr = actual_pr(data["prNumber"])
        verify_merged_pr_checkpoint(data, pr, merge)
        verify_candidate_acceptance(data, pr)
        verify_accepted_candidate_tree(data, pr)
        fail_unless(not git("show-ref", "--verify", f"refs/heads/{data['branch']}", check=False), "local intake branch still exists")
        fail_unless(github_ref_sha(f"heads/{data['branch']}", required=False) is None, "GitHub intake branch still exists")
        fail_unless(not git("ls-remote", "--heads", "origin", data["branch"]), "remote intake branch still exists")
        fail_unless(data["canonicalState"] in {"PUBLISHED", "CLOSED"}, "published gate requires state PUBLISHED or CLOSED")
        fail_unless(data["publicationStatus"] == "published", "publicationStatus must be published")
        for key in ("mainValidationUrl", "pagesRunUrl", "liveBaseUrl"):
            fail_unless(bool(data[key]), f"published gate requires {key}")
            safe_url(key, data[key])
        fail_unless(bool(data["manifestAssertions"]) and bool(data["routeAssertions"]), "published gate requires manifest and route assertions")
        verify_action_run(data["mainValidationUrl"], merge, "validate")
        verify_action_run(data["pagesRunUrl"], merge, "pages")
        verify_pages_identity(data["liveBaseUrl"])
        verify_closure_evidence(data["closureEvidenceUrl"], data["prNumber"], merge, data["manifestSha256"])
        fail_unless(run_pages_verifier(data, merge), "live Pages byte/provenance verification failed")
        if data["canonicalState"] == "CLOSED":
            fail_unless(bool(data["residualLimitations"]) and bool(data["nextGate"]), "CLOSED requires residual limitations and next gate")
    print(f"OK: {data['intakeId']} satisfies the {args.phase} gate from immutable base {base}")
    return 0


def command_validate_repo(_: argparse.Namespace) -> int:
    errors = validate_repo_errors()
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    count = len(list(SPEC_ROOT.glob("*.md"))) if SPEC_ROOT.exists() else 0
    print(f"OK: publication workflow, repo skill, checkpoint schema, template, and {count} immutable intake specs validate")
    return 0


def command_validate_public(args: argparse.Namespace) -> int:
    errors = public_content_errors(include_generated=not args.source_only)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    files = public_files(include_generated=not args.source_only)
    scope = "public source files" if args.source_only else "public/generated files"
    print(f"OK: {len(files)} {scope} pass versioned safety and branding rules")
    return 0


def add_record_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--state", choices=STATES)
    parser.add_argument("--status-reason")
    parser.add_argument("--requested-actions", help="replace explicit authority; requires status reason and current input reference")
    parser.add_argument("--change-class", "--artifact-type", dest="artifact_type", choices=ARTIFACT_TYPES)
    parser.add_argument("--audience", action="append", default=[])
    parser.add_argument("--scope-summary")
    parser.add_argument("--delta-summary")
    parser.add_argument("--local-validation", choices=("pending", "pass", "fail"))
    parser.add_argument("--candidate-sha")
    parser.add_argument("--pr-number", type=int)
    parser.add_argument("--pr-url")
    parser.add_argument("--pr-head-sha")
    draft = parser.add_mutually_exclusive_group()
    draft.add_argument("--pr-draft", dest="pr_draft", action="store_true")
    draft.add_argument("--pr-ready", dest="pr_draft", action="store_false")
    parser.set_defaults(pr_draft=None)
    parser.add_argument("--review-disposition", choices=("pending", "pass", "conditional", "fail"))
    parser.add_argument("--review-evidence-url", action="append", default=[])
    parser.add_argument("--accepted-sha")
    parser.add_argument("--checked-sha")
    parser.add_argument("--check-disposition", choices=("pending", "green", "failed"))
    parser.add_argument("--check-url", action="append", default=[])
    parser.add_argument("--merge-sha")
    parser.add_argument("--branch-cleanup-status", choices=("pending", "complete", "failed"))
    parser.add_argument("--cleanup-evidence", action="append", default=[])
    parser.add_argument("--main-validation-url")
    parser.add_argument("--pages-run-url")
    parser.add_argument("--manifest-sha256")
    parser.add_argument("--closure-evidence-url")
    parser.add_argument("--live-base-url")
    parser.add_argument("--manifest-assertion", action="append", default=[])
    parser.add_argument("--route-assertion", action="append", default=[])
    parser.add_argument("--publication-status", choices=("pending", "published", "corrective-change-required"))
    parser.add_argument("--canonical-path", action="append", default=[])
    parser.add_argument("--derived-path", action="append", default=[])
    parser.add_argument("--input-reference", action="append", default=[])
    parser.add_argument("--evidence-reference", action="append", default=[])
    parser.add_argument("--residual-limitation", action="append", default=[])
    parser.add_argument("--next-gate")
    parser.add_argument("--blocker-owner-role")
    parser.add_argument("--responsible-stage")


def build_parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description=__doc__)
    commands = root.add_subparsers(dest="command", required=True)
    new = commands.add_parser("new", help="create an intake branch, ignored JSON checkpoint, and optional immutable spec")
    new.add_argument("--slug", required=True)
    new.add_argument("--title", required=True)
    new.add_argument("--source-kind", required=True, choices=SOURCE_KINDS)
    new.add_argument("--requested-actions", required=True, help="comma-separated explicitly authorized actions")
    new.add_argument("--request-summary", required=True)
    new.add_argument("--input-reference", action="append", default=[], help="public-safe reference only; raw input is never copied")
    new.add_argument("--decision-question", required=True)
    new.add_argument("--visibility", choices=("public", "private"), default="public")
    new.add_argument("--date")
    new.add_argument("--write-spec", action="store_true")
    new.set_defaults(handler=command_new)
    resume = commands.add_parser("resume", help="restore an ignored checkpoint from an exact PR-embedded payload")
    resume.add_argument("--pr-number", required=True, type=int)
    resume.add_argument("--base", required=True)
    resume.add_argument("--requested-actions", required=True, help="current explicit actions; must equal the durable checkpoint")
    resume.set_defaults(handler=command_resume)
    record = commands.add_parser("record", help="update only the ignored machine checkpoint")
    record.add_argument("--checkpoint", required=True)
    add_record_arguments(record)
    record.set_defaults(handler=command_record)
    replace_list = commands.add_parser("replace-list", help="replace or clear one repairable checkpoint list")
    replace_list.add_argument("--checkpoint", required=True)
    replace_list.add_argument("--field", required=True, choices=REPLACEABLE_LIST_FIELDS)
    replace_list.add_argument("--value", action="append", default=[])
    replace_list.add_argument("--status-reason", required=True)
    replace_list.set_defaults(handler=command_replace_list)
    render = commands.add_parser("render", help="render the marker-delimited PR checkpoint block")
    render.add_argument("--checkpoint", required=True)
    render.set_defaults(handler=command_render)
    check = commands.add_parser("check", help="validate a draft, release, or published checkpoint")
    check.add_argument("--checkpoint", "--intake", dest="checkpoint", required=True)
    check.add_argument("--phase", choices=PHASES, required=True)
    check.add_argument("--base", required=True)
    check.set_defaults(handler=command_check)
    validate_repo = commands.add_parser("validate-repo", help="validate workflow controls and immutable specs")
    validate_repo.set_defaults(handler=command_validate_repo)
    validate_public = commands.add_parser("validate-public-content", help="scan public and generated text without echoing matched values")
    validate_public.add_argument("--source-only", action="store_true", help="scan candidate source before any parser or generator runs")
    validate_public.set_defaults(handler=command_validate_public)
    return root


def main() -> int:
    args = build_parser().parse_args()
    try:
        return int(args.handler(args))
    except WorkflowError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
