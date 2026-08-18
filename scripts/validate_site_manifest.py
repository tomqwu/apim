#!/usr/bin/env python3
"""Validate static-site provenance, routes, and byte-for-byte source mirrors."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import unicodedata
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path, PurePosixPath
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_VERSION = 1
GENERATOR_PATH = "scripts/build_site.py"
CONTENT_ROOTS = (
    "docs", "architecture", "decision-matrix", "research", "poc", "mule-migration",
    "workshops", "adr", "templates", "reports",
)
PUBLISHABLE_EXTENSIONS = {
    ".md", ".mmd", ".csv", ".yaml", ".yml", ".json", ".txt", ".sh", ".py",
    ".js", ".html", ".css", ".xml", ".toml", ".ini", ".conf", ".dockerfile",
    ".pdf", ".ppt", ".pptx", ".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg",
    ".mp4", ".webm",
}
REQUIRED_ASSET_PATHS = {
    "index.html",
    "404.html",
    "assets/app.js",
    "assets/charts.js",
    "assets/styles.css",
    "assets/audiences.js",
}
ALLOWED_EXTERNAL_SCRIPTS = {
    "https://cdn.jsdelivr.net/npm/dompurify@3.2.6/dist/purify.min.js": "sha384-JEyTNhjM6R1ElGoJns4U2Ln4ofPcqzSsynQkmEc/KGy6336qAZl70tDLufbkla+3",
    "https://cdn.jsdelivr.net/npm/marked@15.0.12/marked.min.js": "sha384-948ahk4ZmxYVYOc+rxN1H2gM1EJ2Duhp7uHtZ4WSLkV4Vtx5MUqnV+l7u9B+jFv+",
    "https://cdn.jsdelivr.net/npm/mermaid@11.12.0/dist/mermaid.min.js": "sha384-o+g/BxPwhi0C3RK7oQBxQuNimeafQ3GE/ST4iT2BxVI4Wzt60SH4pq9iXVYujjaS",
}
REQUIRED_LOCAL_SCRIPTS = {"assets/app.js", "assets/charts.js", "assets/audiences.js"}
STATIC_ROUTES = {
    "#/overview",
    "#/library",
    "#/compare",
    "#/architecture",
    "#/lab",
    "#/visuals",
    "#/audiences",
}
SHA256_PATTERN = re.compile(r"[0-9a-f]{64}")
REVISION_PATTERN = re.compile(r"[0-9a-f]{40,64}")


class ValidationError(RuntimeError):
    """A deterministic site artifact failed its publication contract."""


class ScriptSourceParser(HTMLParser):
    """Collect browser-parsed script tags regardless of attribute quoting."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.scripts: list[list[tuple[str, str | None]]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() == "script":
            self.scripts.append(attrs)

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationError(message)


def run_git(*args: str) -> str:
    try:
        result = subprocess.run(
            ("git", *args),
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
    except (FileNotFoundError, subprocess.CalledProcessError) as exc:
        detail = getattr(exc, "stderr", "") or str(exc)
        raise ValidationError(f"git {' '.join(args)} failed: {detail.strip()}") from exc
    return result.stdout.strip()


def safe_path_location(name: str) -> str:
    return f"path-sha256:{hashlib.sha256(name.encode('utf-8', errors='surrogatepass')).hexdigest()[:16]}"


def reject_hidden_index_flags() -> None:
    result = subprocess.run(
        ("git", "ls-files", "-v", "-z"),
        cwd=ROOT, check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    require(result.returncode == 0, "unable to inspect Git index visibility flags")
    for entry in (value for value in result.stdout.split(b"\0") if value):
        marker = entry[:1]
        require(marker != b"S" and not marker.islower(), "Git index visibility flags hide worktree state")


def repository_candidate_paths() -> list[Path]:
    reject_hidden_index_flags()
    result = subprocess.run(
        ("git", "ls-files", "-c", "-o", "--exclude-standard", "-z"),
        cwd=ROOT, check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    require(result.returncode == 0, "unable to enumerate publishable source candidates")
    try:
        names = [value.decode("utf-8") for value in result.stdout.split(b"\0") if value]
    except UnicodeDecodeError as exc:
        raise ValidationError("publishable source path is not UTF-8") from exc
    paths: list[Path] = []
    for name in names:
        require(bool(name) and name == name.strip() and not any(unicodedata.category(character).startswith("C") for character in name), "publishable source path contains control or surrounding whitespace")
        path = ROOT / name
        require(not path.is_symlink(), f"publishable source is a symlink at {safe_path_location(name)}")
        candidate = ROOT
        for part in Path(name).parts:
            candidate /= part
            require(not candidate.is_symlink(), f"publishable source is below a symlink at {safe_path_location(name)}")
        if path.is_file():
            paths.append(path)
    return sorted(set(paths))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def raw_tracked_bytes_match(revision: str) -> bool:
    """Compare worktree bytes to revision blobs without Git content filters."""
    listed = subprocess.run(
        ("git", "ls-files", "-c", "-z"), cwd=ROOT, check=False,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    require(listed.returncode == 0, "unable to enumerate tracked raw-byte provenance")
    try:
        names = [value.decode("utf-8") for value in listed.stdout.split(b"\0") if value]
    except UnicodeDecodeError as exc:
        raise ValidationError("tracked provenance path is not UTF-8") from exc
    for name in names:
        path = ROOT / name
        if not path.is_file() or path.is_symlink():
            return False
        expected = subprocess.Popen(
            ("git", "cat-file", "blob", f"{revision}:{name}"), cwd=ROOT,
            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
        )
        expected_digest = hashlib.sha256()
        assert expected.stdout is not None
        for chunk in iter(lambda: expected.stdout.read(1024 * 1024), b""):
            expected_digest.update(chunk)
        expected.stdout.close()
        if expected.wait() != 0:
            return False
        if sha256_file(path) != expected_digest.hexdigest():
            return False
    return True


def safe_relative(value: Any, label: str) -> PurePosixPath:
    require(isinstance(value, str) and bool(value), f"{label} must be a non-empty string")
    relative = PurePosixPath(value)
    require(not relative.is_absolute(), f"{label} must be relative: {value!r}")
    require(".." not in relative.parts and "." not in relative.parts, f"{label} is not normalized: {value!r}")
    require("\\" not in value and "//" not in value, f"{label} must use a normalized POSIX path: {value!r}")
    require(relative.as_posix() == value, f"{label} must be canonical POSIX syntax: {value!r}")
    return relative


def under(base: Path, relative: PurePosixPath, label: str) -> Path:
    candidate = (base / Path(*relative.parts)).resolve()
    require(candidate.is_relative_to(base.resolve()), f"{label} escapes {base}: {relative}")
    return candidate


def unique(values: list[str], label: str) -> None:
    require(len(values) == len(set(values)), f"{label} contains duplicate values")


def publishable_source_inventory() -> set[str]:
    """Enumerate canonical publishable sources independently of the manifest."""
    inventory: set[str] = set()
    for source in repository_candidate_paths():
        relative = source.relative_to(ROOT)
        if not relative.parts or relative.parts[0] not in CONTENT_ROOTS:
            continue
        if any(part.startswith(".") for part in relative.parts):
            continue
        if source.suffix.lower() in PUBLISHABLE_EXTENSIONS or source.name == "Dockerfile":
            inventory.add(relative.as_posix())
    return inventory


def deterministic_timestamp(revision: str) -> str:
    epoch_value = os.environ.get("SOURCE_DATE_EPOCH")
    if epoch_value is None:
        epoch_value = run_git("show", "-s", "--format=%ct", revision)
    require(bool(re.fullmatch(r"\d+", epoch_value)), f"SOURCE_DATE_EPOCH is invalid: {epoch_value!r}")
    epoch = int(epoch_value)
    try:
        return datetime.fromtimestamp(epoch, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    except (OverflowError, OSError, ValueError) as exc:
        raise ValidationError(f"SOURCE_DATE_EPOCH is outside the supported timestamp range: {epoch_value!r}") from exc


def validate_metadata(manifest: dict[str, Any], expected_revision: str | None, require_clean: bool) -> None:
    require(manifest.get("schemaVersion") == SCHEMA_VERSION, f"schemaVersion must be {SCHEMA_VERSION}")
    revision = manifest.get("sourceRevision")
    require(isinstance(revision, str) and bool(REVISION_PATTERN.fullmatch(revision)), "sourceRevision must be a full lowercase Git object ID")

    head = run_git("rev-parse", "--verify", "HEAD^{commit}")
    run_git("cat-file", "-e", f"{revision}^{{commit}}")
    status = run_git("status", "--porcelain=v1", "--untracked-files=all")
    expected_dirty = bool(status) or revision != head or not raw_tracked_bytes_match(revision)
    require(type(manifest.get("sourceDirty")) is bool, "sourceDirty must be a boolean")
    require(manifest["sourceDirty"] == expected_dirty, "sourceDirty does not match the checkout, revision, and worktree state")

    if expected_revision:
        resolved_expected = run_git("rev-parse", "--verify", f"{expected_revision}^{{commit}}")
        require(revision == resolved_expected, f"manifest revision {revision} does not match expected revision {resolved_expected}")
    if require_clean:
        require(not manifest["sourceDirty"], "a clean publication was required but sourceDirty is true")

    expected_generated_at = deterministic_timestamp(revision)
    require(
        manifest.get("generatedAt") == expected_generated_at,
        f"generatedAt must be the reproducible timestamp {expected_generated_at}",
    )
    generator = manifest.get("generator")
    require(isinstance(generator, dict), "generator must contain path and SHA-256 provenance")
    require(generator.get("path") == GENERATOR_PATH, f"generator.path must be {GENERATOR_PATH}")
    generator_hash = generator.get("sha256")
    require(isinstance(generator_hash, str) and bool(SHA256_PATTERN.fullmatch(generator_hash)), "generator.sha256 is invalid")
    require(generator_hash == sha256_file(ROOT / GENERATOR_PATH), "generator SHA-256 does not match scripts/build_site.py")


def validate_items(manifest: dict[str, Any], output: Path) -> tuple[dict[str, dict[str, Any]], set[str]]:
    items = manifest.get("items")
    require(isinstance(items, list) and bool(items), "items must be a non-empty list")
    require(all(isinstance(item, dict) for item in items), "every item must be an object")

    ids = [item.get("id") for item in items]
    paths = [item.get("path") for item in items]
    content_urls = [item.get("contentUrl") for item in items]
    routes = [item.get("route") for item in items]
    for values, label in ((ids, "item IDs"), (paths, "item paths"), (content_urls, "item content URLs"), (routes, "item routes")):
        require(all(isinstance(value, str) and value for value in values), f"{label} must be non-empty strings")
        unique(values, label)
    expected_sources = publishable_source_inventory()
    require(set(paths) == expected_sources, "manifest items do not equal the independently enumerated publishable source set")

    by_id: dict[str, dict[str, Any]] = {}
    expected_copies: set[str] = set()
    for item in items:
        item_id = item["id"]
        relative = safe_relative(item["path"], f"item {item_id} path")
        content_relative = safe_relative(item["contentUrl"], f"item {item_id} contentUrl")
        expected_content = PurePosixPath("content") / relative
        require(content_relative == expected_content, f"item {item_id} contentUrl must be content/{relative}")
        require(item["route"] == f"#/doc/{item_id}", f"item {item_id} has an invalid document route")

        source = under(ROOT, relative, f"item {item_id} source")
        copy = under(output, content_relative, f"item {item_id} copy")
        require(source.is_file(), f"item {item_id} source is missing: {relative}")
        require(copy.is_file(), f"item {item_id} generated copy is missing: {content_relative}")
        digest = item.get("sha256")
        require(isinstance(digest, str) and bool(SHA256_PATTERN.fullmatch(digest)), f"item {item_id} SHA-256 is invalid")
        require(sha256_file(source) == digest, f"item {item_id} source SHA-256 does not match the manifest")
        require(sha256_file(copy) == digest, f"item {item_id} generated copy SHA-256 does not match its source")
        require(item.get("size") == source.stat().st_size == copy.stat().st_size, f"item {item_id} size metadata is invalid")
        by_id[item_id] = item
        expected_copies.add(content_relative.as_posix())

    content_root = output / "content"
    actual_copies = {
        path.relative_to(output).as_posix()
        for path in content_root.rglob("*")
        if path.is_file()
    }
    require(actual_copies == expected_copies, "generated content files and manifest items are not a one-to-one set")
    return by_id, set(routes)


def validate_assets(manifest: dict[str, Any], output: Path) -> None:
    assets = manifest.get("assets")
    require(isinstance(assets, dict), "assets must be an object keyed by generated path")
    source_asset_paths = {
        path.relative_to(ROOT / "site").as_posix()
        for path in repository_candidate_paths()
        if path.relative_to(ROOT).parts[:1] == ("site",)
    }
    expected_asset_paths = source_asset_paths | {"404.html"}
    require(REQUIRED_ASSET_PATHS.issubset(expected_asset_paths), "required site asset sources are missing")
    require(set(assets) == expected_asset_paths, "asset digest set does not match the complete site source set")

    for relative_value in sorted(expected_asset_paths):
        relative = safe_relative(relative_value, "asset path")
        generated = under(output, relative, f"asset {relative_value}")
        source_relative = PurePosixPath("index.html") if relative_value == "404.html" else relative
        source = under(ROOT / "site", source_relative, f"asset {relative_value} source")
        require(source.is_file() and generated.is_file(), f"asset {relative_value} is missing")
        metadata = assets[relative_value]
        require(isinstance(metadata, dict), f"asset {relative_value} metadata must be an object")
        digest = metadata.get("sha256")
        require(isinstance(digest, str) and bool(SHA256_PATTERN.fullmatch(digest)), f"asset {relative_value} SHA-256 is invalid")
        require(sha256_file(source) == digest, f"asset {relative_value} source SHA-256 does not match the manifest")
        require(sha256_file(generated) == digest, f"asset {relative_value} generated SHA-256 does not match the source")
        require(metadata.get("size") == source.stat().st_size == generated.stat().st_size, f"asset {relative_value} size is invalid")

    for source in sorted(
        path for path in repository_candidate_paths()
        if path.relative_to(ROOT).parts[:1] == ("site",)
    ):
        relative = source.relative_to(ROOT / "site")
        generated = output / relative
        require(generated.is_file(), f"site source was not copied: {relative.as_posix()}")
        require(sha256_file(source) == sha256_file(generated), f"site source copy differs: {relative.as_posix()}")
    require((output / ".nojekyll").is_file(), "generated site is missing .nojekyll")
    index_text = (ROOT / "site" / "index.html").read_text(encoding="utf-8")
    parser = ScriptSourceParser()
    parser.feed(index_text)
    parser.close()
    require(bool(parser.scripts), "site index must declare its runtime scripts")
    external_seen: set[str] = set()
    local_seen: set[str] = set()
    for raw_attrs in parser.scripts:
        names = [name.lower() for name, _ in raw_attrs]
        require(len(names) == len(set(names)), "script tag contains duplicate attributes")
        attrs = {name.lower(): value for name, value in raw_attrs}
        source = attrs.get("src")
        require(isinstance(source, str) and bool(source), "inline or source-less scripts are not permitted")
        if source.startswith("https://"):
            expected_integrity = ALLOWED_EXTERNAL_SCRIPTS.get(source)
            require(expected_integrity is not None, "external script is not in the exact versioned runtime allowlist")
            require(source not in external_seen, "external runtime script is declared more than once")
            require(attrs.get("integrity") == expected_integrity, "external script Subresource Integrity differs from the allowlist")
            require(attrs.get("crossorigin", "").lower() == "anonymous", "every external script must use anonymous CORS for Subresource Integrity")
            external_seen.add(source)
        else:
            require(source in REQUIRED_LOCAL_SCRIPTS, "local script source is outside the required site asset set")
            require(source not in local_seen, "local runtime script is declared more than once")
            require("integrity" not in attrs and "crossorigin" not in attrs, "local scripts must use manifest provenance rather than external SRI attributes")
            local_seen.add(source)
    require(external_seen == set(ALLOWED_EXTERNAL_SCRIPTS), "site index external runtime set differs from the exact allowlist")
    require(local_seen == REQUIRED_LOCAL_SCRIPTS, "site index local runtime set is incomplete or duplicated")


def validate_routes_and_audiences(
    manifest: dict[str, Any],
    by_id: dict[str, dict[str, Any]],
    document_routes: set[str],
) -> None:
    presentation = manifest.get("presentation")
    require(isinstance(presentation, list) and bool(presentation), "presentation must be a non-empty list")
    require(all(isinstance(slide, dict) for slide in presentation), "every presentation slide must be an object")
    slide_keys = [slide.get("key") for slide in presentation]
    require(all(isinstance(key, str) and key for key in slide_keys), "presentation keys must be non-empty strings")
    unique(slide_keys, "presentation keys")
    indices = [slide.get("index") for slide in presentation]
    require(indices == list(range(len(presentation))), "presentation indices must be unique and contiguous from zero")
    for slide in presentation:
        require(slide.get("sourceId") in by_id, f"slide {slide.get('key')} references an unknown sourceId")

    all_routes = set(document_routes)
    generic_presentation_routes = {f"#/present/{index}" for index in range(len(presentation))}
    require(not all_routes.intersection(generic_presentation_routes), "document and presentation routes collide")
    all_routes.update(generic_presentation_routes)

    audiences = manifest.get("audiences")
    require(isinstance(audiences, list) and bool(audiences), "audiences must be a non-empty list")
    require(all(isinstance(audience, dict) for audience in audiences), "every audience must be an object")
    audience_ids = [audience.get("id") for audience in audiences]
    require(all(isinstance(audience_id, str) and audience_id for audience_id in audience_ids), "audience IDs must be non-empty strings")
    unique(audience_ids, "audience IDs")

    path_to_id = {item["path"]: item_id for item_id, item in by_id.items()}
    for audience in audiences:
        audience_id = audience["id"]
        source_paths = audience.get("sourcePaths")
        source_ids = audience.get("sourceIds")
        require(isinstance(source_paths, list) and isinstance(source_ids, list), f"audience {audience_id} sources must be lists")
        require(all(isinstance(path, str) for path in source_paths), f"audience {audience_id} sourcePaths are invalid")
        require(all(isinstance(item_id, str) for item_id in source_ids), f"audience {audience_id} sourceIds are invalid")
        unique(source_paths, f"audience {audience_id} sourcePaths")
        unique(source_ids, f"audience {audience_id} sourceIds")
        expected_source_ids = [path_to_id.get(path) for path in source_paths]
        require(None not in expected_source_ids, f"audience {audience_id} references an unknown source path")
        require(source_ids == expected_source_ids, f"audience {audience_id} source IDs do not align with source paths")

        selected_slides = audience.get("presentationSlides")
        require(isinstance(selected_slides, list) and bool(selected_slides), f"audience {audience_id} has no presentation slides")
        require(all(isinstance(key, str) and key in slide_keys for key in selected_slides), f"audience {audience_id} references an unknown slide")
        unique(selected_slides, f"audience {audience_id} presentation slides")

        expected_entry_route = f"#/present/{audience_id}/0"
        require(audience.get("presentationRoute") == expected_entry_route, f"audience {audience_id} presentationRoute is invalid")
        audience_routes = {f"#/present/{audience_id}/{index}" for index in range(len(selected_slides))}
        audience_routes.add(f"#/audiences/{audience_id}")
        require(not all_routes.intersection(audience_routes), f"audience {audience_id} routes collide with another route")
        all_routes.update(audience_routes)

        recommended = audience.get("recommendedRoute")
        require(isinstance(recommended, str), f"audience {audience_id} recommendedRoute is invalid")
        normalized = recommended.split("?", 1)[0]
        require(normalized in STATIC_ROUTES or normalized in document_routes, f"audience {audience_id} recommendedRoute is unknown")


def validate(output: Path, expected_revision: str | None, require_clean: bool) -> dict[str, Any]:
    manifest_path = output / "content-manifest.json"
    require(manifest_path.is_file(), f"site manifest is missing: {manifest_path}")
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValidationError(f"site manifest is not valid UTF-8 JSON: {exc}") from exc
    require(isinstance(manifest, dict), "site manifest root must be an object")
    validate_metadata(manifest, expected_revision, require_clean)
    by_id, document_routes = validate_items(manifest, output)
    validate_assets(manifest, output)
    validate_routes_and_audiences(manifest, by_id, document_routes)
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "_site", help="Generated site directory")
    parser.add_argument(
        "--expected-revision",
        default=os.environ.get("SOURCE_REVISION") or os.environ.get("GITHUB_SHA"),
        help="Revision the manifest must identify (defaults to SOURCE_REVISION, then GITHUB_SHA)",
    )
    parser.add_argument("--require-clean", action="store_true", help="Reject a manifest built from a dirty or mismatched checkout")
    args = parser.parse_args()
    output = args.output if args.output.is_absolute() else ROOT / args.output
    try:
        manifest = validate(output.resolve(), args.expected_revision, args.require_clean)
    except ValidationError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(
        "OK: site manifest validates "
        f"{len(manifest['items'])} source copies, {len(manifest['assets'])} assets, "
        f"{len(manifest['audiences'])} audiences, and revision {manifest['sourceRevision']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
