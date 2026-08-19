#!/usr/bin/env python3
"""Verify that GitHub Pages serves one clean, byte-exact repository revision."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import time
from concurrent.futures import FIRST_COMPLETED, ThreadPoolExecutor, wait
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode, urljoin, urlsplit, urlunsplit
from urllib.request import Request, urlopen

sys.path.insert(0, str(Path(__file__).resolve().parent))
from repository_inventory import git_environment


SCHEMA_VERSION = 2
SHA256_PATTERN = re.compile(r"[0-9a-f]{64}")
REVISION_PATTERN = re.compile(r"[0-9a-f]{40,64}")
GENERATED_AT_PATTERN = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z")
REQUIRED_ASSETS = {
    "index.html",
    "404.html",
    "assets/app.js",
    "assets/charts.js",
    "assets/styles.css",
    "assets/audiences.js",
}
MAX_METADATA_BYTES = 16 * 1024 * 1024
MAX_TARGET_BYTES = 64 * 1024 * 1024
STATIC_ROUTES = {
    "#/overview", "#/library", "#/compare", "#/architecture", "#/lab",
    "#/visuals", "#/audiences",
}
KONG_PLATFORM_FIT_SLIDE_KEYS = (
    "kong-platform-fit-boundary",
    "kong-platform-fit-runtime",
    "kong-platform-fit-change",
    "kong-platform-fit-fallback",
)
KONG_PLATFORM_FIT_IDS = tuple(f"KPS-FIT-{index:02d}" for index in range(1, 8))
KONG_PLATFORM_FIT_SLIDE_ROWS = {
    "kong-platform-fit-boundary": ("KPS-FIT-01", "KPS-FIT-02"),
    "kong-platform-fit-runtime": ("KPS-FIT-03", "KPS-FIT-04"),
    "kong-platform-fit-change": ("KPS-FIT-05", "KPS-FIT-06"),
    "kong-platform-fit-fallback": ("KPS-FIT-07",),
}
REMOVED_KONG_PLATFORM_FIT_SLIDE_KEYS = frozenset({"kong-platform-fit-1", "kong-platform-fit-2"})
ROOT = Path(__file__).resolve().parents[1]


class VerificationError(RuntimeError):
    """The deployed Pages artifact does not match its provenance contract."""


@dataclass(frozen=True)
class Target:
    relative: str
    sha256: str
    size: int
    label: str


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    file_digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            file_digest.update(chunk)
    return file_digest.hexdigest()


def validate_kong_platform_fit_slides(
    manifest: dict[str, Any],
    presentation: list[dict[str, Any]],
) -> None:
    """Bind every deployed Kong fit slide to the canonical seven-row projection."""
    visuals = manifest.get("visuals")
    require(isinstance(visuals, dict), "manifest visuals must be an object")
    strategy = visuals.get("kongPlatformStrategy")
    require(isinstance(strategy, dict), "manifest visuals.kongPlatformStrategy must be an object")
    fit = strategy.get("fit")
    require(isinstance(fit, dict), "manifest visuals.kongPlatformStrategy.fit must be an object")
    rows = fit.get("rows")
    require(isinstance(rows, list) and bool(rows), "manifest canonical Kong platform fit rows must be a non-empty list")
    require(all(isinstance(row, dict) for row in rows), "manifest canonical Kong platform fit rows must be objects")
    canonical_ids = [row.get("projectionId") for row in rows]
    require(
        all(isinstance(row_id, str) and row_id for row_id in canonical_ids),
        "manifest canonical Kong platform fit IDs must be non-empty strings",
    )
    require(
        len(canonical_ids) == len(set(canonical_ids)),
        "manifest canonical Kong platform fit IDs must be unique",
    )
    require(
        len(canonical_ids) == len(KONG_PLATFORM_FIT_IDS)
        and set(canonical_ids) == set(KONG_PLATFORM_FIT_IDS),
        "manifest canonical Kong platform fit IDs must be exactly KPS-FIT-01 through KPS-FIT-07",
    )

    slides_by_key = {slide["key"]: slide for slide in presentation}
    require(
        not REMOVED_KONG_PLATFORM_FIT_SLIDE_KEYS.intersection(slides_by_key),
        "manifest presentation retains a removed Kong platform fit slide",
    )
    fit_slide_keys = {
        slide["key"]
        for slide in presentation
        if slide.get("visual") == "kongPlatformFit"
    }
    require(
        fit_slide_keys == set(KONG_PLATFORM_FIT_SLIDE_KEYS),
        "manifest Kong platform fit slides must be exactly the four semantic fit slide keys",
    )
    require(
        all(key in slides_by_key for key in KONG_PLATFORM_FIT_SLIDE_KEYS),
        "manifest presentation must contain the four semantic Kong platform fit slides",
    )
    for key in KONG_PLATFORM_FIT_SLIDE_KEYS:
        require(
            slides_by_key[key].get("visual") == "kongPlatformFit",
            f"manifest slide {key} must use the kongPlatformFit visual",
        )
        require(
            tuple(slides_by_key[key].get("rowIds", ())) == KONG_PLATFORM_FIT_SLIDE_ROWS[key],
            f"manifest slide {key} rowIds do not match its bounded Kong fit contract",
        )

    canonical_id_set = set(canonical_ids)
    for slide in presentation:
        if slide.get("visual") != "kongPlatformFit":
            continue
        key = slide["key"]
        row_ids = slide.get("rowIds")
        require(isinstance(row_ids, list) and bool(row_ids), f"manifest slide {key} rowIds must be a non-empty list")
        require(
            all(isinstance(row_id, str) and row_id for row_id in row_ids),
            f"manifest slide {key} rowIds must be non-empty strings",
        )
        require(len(row_ids) == len(set(row_ids)), f"manifest slide {key} rowIds must be unique")
        require(
            set(row_ids).issubset(canonical_id_set),
            f"manifest slide {key} rowIds reference an unknown canonical Kong platform fit ID",
        )

    semantic_row_ids = [
        row_id
        for key in KONG_PLATFORM_FIT_SLIDE_KEYS
        for row_id in slides_by_key[key]["rowIds"]
    ]
    require(
        len(semantic_row_ids) == len(KONG_PLATFORM_FIT_IDS)
        and set(semantic_row_ids) == set(KONG_PLATFORM_FIT_IDS),
        "manifest semantic Kong platform fit slides must cover KPS-FIT-01 through KPS-FIT-07 exactly once",
    )


def run_git(*args: str) -> str:
    try:
        result = subprocess.run(
            ("git", *args),
            cwd=ROOT,
            env=git_environment(),
            check=True,
            capture_output=True,
            text=True,
        )
    except (FileNotFoundError, subprocess.CalledProcessError) as exc:
        detail = getattr(exc, "stderr", "") or str(exc)
        raise VerificationError(f"git {' '.join(args)} failed: {detail.strip()}") from exc
    return result.stdout.strip()


def verify_local_checkout(expected_revision: str) -> None:
    head = run_git("rev-parse", "--verify", "HEAD^{commit}")
    require(head == expected_revision, f"verifier checkout is {head}; expected {expected_revision}")
    status = run_git("status", "--porcelain=v1", "--untracked-files=all")
    require(not status, "verifier checkout is dirty")


def safe_remote_path(value: Any, label: str) -> str:
    require(isinstance(value, str) and bool(value), f"{label} must be a non-empty string")
    split = urlsplit(value)
    require(not split.scheme and not split.netloc and not split.query and not split.fragment, f"{label} must be a relative path")
    require(not split.path.startswith("/") and "\\" not in split.path, f"{label} must be a normalized relative path")
    require("%" not in split.path, f"{label} must not contain percent-encoded or literal percent syntax")
    parts = split.path.split("/")
    require(all(part not in {"", ".", ".."} for part in parts), f"{label} contains an unsafe path segment")
    return split.path


def validated_route_inventory(manifest: dict[str, Any], items: list[dict[str, Any]]) -> set[str]:
    """Validate every manifest-backed SPA route and return its exact inventory."""
    item_ids = [item.get("id") for item in items]
    item_paths = [item.get("path") for item in items]
    item_routes = [item.get("route") for item in items]
    path_to_id = dict(zip(item_paths, item_ids))

    presentation = manifest.get("presentation")
    require(isinstance(presentation, list) and bool(presentation), "manifest presentation must be a non-empty list")
    require(all(isinstance(slide, dict) for slide in presentation), "manifest presentation slide must be an object")
    slide_keys = [slide.get("key") for slide in presentation]
    require(all(isinstance(key, str) and key for key in slide_keys), "manifest presentation keys must be non-empty strings")
    require(len(slide_keys) == len(set(slide_keys)), "manifest presentation keys must be unique")
    require(
        [slide.get("index") for slide in presentation] == list(range(len(presentation))),
        "manifest presentation indices must be unique and contiguous from zero",
    )
    require(
        all(slide.get("sourceId") in item_ids for slide in presentation),
        "manifest presentation references an unknown sourceId",
    )
    validate_kong_platform_fit_slides(manifest, presentation)

    content_routes = set(STATIC_ROUTES).union(item_routes)
    routes = set(STATIC_ROUTES)
    require(not routes.intersection(item_routes), "manifest static and document routes collide")
    routes.update(item_routes)
    generic_routes = {f"#/present/{index}" for index in range(len(presentation))}
    require(not routes.intersection(generic_routes), "manifest document and presentation routes collide")
    routes.update(generic_routes)

    audiences = manifest.get("audiences")
    require(isinstance(audiences, list) and bool(audiences), "manifest audiences must be a non-empty list")
    require(all(isinstance(audience, dict) for audience in audiences), "manifest audience must be an object")
    audience_ids = [audience.get("id") for audience in audiences]
    require(all(isinstance(audience_id, str) and audience_id for audience_id in audience_ids), "manifest audience IDs must be non-empty strings")
    require(len(audience_ids) == len(set(audience_ids)), "manifest audience IDs must be unique")

    def validate_sources(subject: dict[str, Any], label: str, *, require_nonempty: bool = False) -> list[str]:
        source_paths = subject.get("sourcePaths")
        source_ids = subject.get("sourceIds")
        require(isinstance(source_paths, list) and isinstance(source_ids, list), f"{label} sources must be lists")
        if require_nonempty:
            require(bool(source_paths), f"{label} must declare at least one source")
        require(all(isinstance(path, str) for path in source_paths), f"{label} sourcePaths are invalid")
        require(all(isinstance(item_id, str) for item_id in source_ids), f"{label} sourceIds are invalid")
        require(len(source_paths) == len(set(source_paths)), f"{label} sourcePaths must be unique")
        require(len(source_ids) == len(set(source_ids)), f"{label} sourceIds must be unique")
        expected_ids = [path_to_id.get(path) for path in source_paths]
        require(None not in expected_ids, f"{label} references an unknown source path")
        require(source_ids == expected_ids, f"{label} source IDs do not align with source paths")
        return source_ids

    for audience in audiences:
        audience_id = audience["id"]
        validate_sources(audience, f"manifest audience {audience_id}")
        selected = audience.get("presentationSlides")
        require(isinstance(selected, list) and bool(selected), f"manifest audience {audience_id} has no presentation slides")
        require(all(isinstance(key, str) for key in selected), f"manifest audience {audience_id} presentation slides are invalid")
        require(
            not any(key in REMOVED_KONG_PLATFORM_FIT_SLIDE_KEYS for key in selected),
            f"manifest audience {audience_id} retains a removed Kong platform fit slide",
        )
        require(all(key in slide_keys for key in selected), f"manifest audience {audience_id} references an unknown slide")
        require(len(selected) == len(set(selected)), f"manifest audience {audience_id} presentation slides must be unique")
        require(audience.get("presentationRoute") == f"#/present/{audience_id}/0", f"manifest audience {audience_id} presentationRoute is invalid")
        audience_routes = {f"#/present/{audience_id}/{index}" for index in range(len(selected))}
        audience_routes.add(f"#/audiences/{audience_id}")
        require(not routes.intersection(audience_routes), f"manifest audience {audience_id} routes collide")
        routes.update(audience_routes)
        recommended = audience.get("recommendedRoute")
        require(isinstance(recommended, str), f"manifest audience {audience_id} recommendedRoute is invalid")
        require(recommended.split("?", 1)[0] in content_routes, f"manifest audience {audience_id} recommendedRoute is unknown")

    decks = manifest.get("presentationDecks")
    require(isinstance(decks, list) and bool(decks), "manifest presentationDecks must be a non-empty list")
    require(all(isinstance(deck, dict) for deck in decks), "manifest presentation deck must be an object")
    deck_ids = [deck.get("id") for deck in decks]
    require(all(isinstance(deck_id, str) and deck_id for deck_id in deck_ids), "manifest presentation deck IDs must be non-empty strings")
    require(len(deck_ids) == len(set(deck_ids)), "manifest presentation deck IDs must be unique")
    require(not set(deck_ids).intersection(audience_ids), "manifest presentation deck IDs must not collide with audience IDs")

    for deck in decks:
        deck_id = deck["id"]
        source_ids = validate_sources(deck, f"manifest presentation deck {deck_id}", require_nonempty=True)
        selected = deck.get("presentationSlides")
        require(isinstance(selected, list) and bool(selected), f"manifest presentation deck {deck_id} has no presentation slides")
        require(all(isinstance(key, str) for key in selected), f"manifest presentation deck {deck_id} presentation slides are invalid")
        require(
            not any(key in REMOVED_KONG_PLATFORM_FIT_SLIDE_KEYS for key in selected),
            f"manifest presentation deck {deck_id} retains a removed Kong platform fit slide",
        )
        require(all(key in slide_keys for key in selected), f"manifest presentation deck {deck_id} references an unknown slide")
        require(len(selected) == len(set(selected)), f"manifest presentation deck {deck_id} presentation slides must be unique")
        require(
            type(deck.get("slideTotal")) is int and deck["slideTotal"] == len(selected),
            f"manifest presentation deck {deck_id} slideTotal must equal its presentation slide count",
        )
        selected_source_ids = {
            slide["sourceId"] for slide in presentation if slide["key"] in selected
        }
        require(
            selected_source_ids.issubset(set(source_ids)),
            f"manifest presentation deck {deck_id} sources do not cover its selected slides",
        )
        role_ids = deck.get("audienceRoleIds")
        require(isinstance(role_ids, list) and bool(role_ids), f"manifest presentation deck {deck_id} audienceRoleIds must be a non-empty list")
        require(
            all(isinstance(role_id, str) and role_id in audience_ids for role_id in role_ids),
            f"manifest presentation deck {deck_id} references an unknown audience role",
        )
        require(len(role_ids) == len(set(role_ids)), f"manifest presentation deck {deck_id} audienceRoleIds must be unique")
        require(deck.get("presentationRoute") == f"#/present/{deck_id}/0", f"manifest presentation deck {deck_id} presentationRoute is invalid")
        deck_routes = {f"#/present/{deck_id}/{index}" for index in range(len(selected))}
        require(not routes.intersection(deck_routes), f"manifest presentation deck {deck_id} routes collide")
        routes.update(deck_routes)
        exit_route = deck.get("exitRoute")
        require(isinstance(exit_route, str), f"manifest presentation deck {deck_id} exitRoute is invalid")
        require(exit_route.split("?", 1)[0] in content_routes, f"manifest presentation deck {deck_id} exitRoute is unknown")

    return routes


def request_url(base_url: str, relative: str, token: str) -> str:
    encoded_path = "/".join(quote(part, safe="") for part in relative.split("/") if part)
    absolute = urljoin(base_url, encoded_path)
    split = urlsplit(absolute)
    query = urlencode({"provenance": token})
    return urlunsplit((split.scheme, split.netloc, split.path, query, ""))


def remaining_timeout(deadline: float, requested_timeout: float) -> float:
    """Return a per-operation timeout that cannot outlive the global deadline."""
    remaining = deadline - time.monotonic()
    require(remaining > 0, "overall verification deadline expired")
    return min(requested_timeout, remaining)


def read_limited(response: Any, limit: int, label: str, deadline: float, timeout: float) -> bytes:
    length = response.headers.get("Content-Length")
    if length is not None:
        try:
            require(int(length) <= limit, f"{label} exceeds its bounded response size")
        except ValueError as exc:
            raise VerificationError(f"{label} has an invalid Content-Length") from exc
    chunks: list[bytes] = []
    total = 0
    read_chunk = getattr(response, "read1", response.read)
    while True:
        remaining_timeout(deadline, timeout)
        chunk = read_chunk(min(1024 * 1024, limit - total + 1))
        remaining_timeout(deadline, timeout)
        if not chunk:
            break
        total += len(chunk)
        require(total <= limit, f"{label} exceeds its bounded response size")
        chunks.append(chunk)
    return b"".join(chunks)


def fetch(
    base_url: str,
    relative: str,
    token: str,
    timeout: float,
    deadline: float,
    max_bytes: int = MAX_METADATA_BYTES,
) -> tuple[int, bytes]:
    url = request_url(base_url, relative, token)
    request = Request(
        url,
        headers={
            "Accept": "application/json,text/html,*/*",
            "Cache-Control": "no-cache, no-store, max-age=0",
            "Pragma": "no-cache",
            "User-Agent": "api-management-studies-pages-verifier/1",
        },
    )
    try:
        with urlopen(request, timeout=remaining_timeout(deadline, timeout)) as response:
            return response.status, read_limited(response, max_bytes, relative or "site root", deadline, timeout)
    except HTTPError as exc:
        try:
            return exc.code, read_limited(exc, max_bytes, relative or "site root", deadline, timeout)
        finally:
            exc.close()
    except (URLError, TimeoutError, OSError) as exc:
        raise VerificationError(f"request failed for {relative}: {exc}") from exc


def load_manifest(base_url: str, token: str, timeout: float, deadline: float) -> tuple[dict[str, Any], bytes]:
    status, raw = fetch(base_url, "content-manifest.json", token, timeout, deadline)
    require(status == 200, f"content-manifest.json returned HTTP {status}")
    try:
        manifest = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise VerificationError(f"content-manifest.json is not valid UTF-8 JSON: {exc}") from exc
    require(isinstance(manifest, dict), "content-manifest.json root must be an object")
    return manifest, raw


def validate_manifest_shape(
    manifest: dict[str, Any],
    expected_revision: str,
    study_paths: list[str],
    expected_routes: list[str],
) -> list[Target]:
    require(manifest.get("schemaVersion") == SCHEMA_VERSION, f"schemaVersion must be {SCHEMA_VERSION}")
    revision = manifest.get("sourceRevision")
    require(isinstance(revision, str) and bool(REVISION_PATTERN.fullmatch(revision)), "sourceRevision is invalid")
    require(revision == expected_revision, f"Pages serves revision {revision}; expected {expected_revision}")
    require(manifest.get("sourceDirty") is False, "Pages manifest is not a clean build")
    require(
        isinstance(manifest.get("generatedAt"), str) and bool(GENERATED_AT_PATTERN.fullmatch(manifest["generatedAt"])),
        "generatedAt is not a deterministic UTC timestamp",
    )
    epoch = os.environ.get("SOURCE_DATE_EPOCH") or run_git("show", "-s", "--format=%ct", expected_revision)
    require(bool(re.fullmatch(r"\d+", epoch)), f"SOURCE_DATE_EPOCH is invalid: {epoch!r}")
    try:
        expected_generated_at = datetime.fromtimestamp(int(epoch), tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    except (OverflowError, OSError, ValueError) as exc:
        raise VerificationError(f"SOURCE_DATE_EPOCH is outside the supported timestamp range: {epoch!r}") from exc
    require(manifest["generatedAt"] == expected_generated_at, f"generatedAt must be {expected_generated_at}")
    generator = manifest.get("generator")
    require(isinstance(generator, dict) and generator.get("path") == "scripts/build_site.py", "generator provenance is invalid")
    require(
        isinstance(generator.get("sha256"), str) and bool(SHA256_PATTERN.fullmatch(generator["sha256"])),
        "generator SHA-256 is invalid",
    )
    require(generator["sha256"] == sha256_file(ROOT / "scripts/build_site.py"), "generator SHA-256 differs from the verifier checkout")

    assets = manifest.get("assets")
    local_asset_paths = {
        path.relative_to(ROOT / "site").as_posix()
        for path in (ROOT / "site").rglob("*")
        if path.is_file()
    } | {"404.html"}
    require(REQUIRED_ASSETS.issubset(local_asset_paths), "required assets are missing from the verifier checkout")
    require(isinstance(assets, dict) and set(assets) == local_asset_paths, "manifest asset digest set differs from the verifier checkout")
    items = manifest.get("items")
    require(isinstance(items, list) and bool(items), "manifest items must be a non-empty list")

    item_paths: list[str] = []
    item_ids: list[str] = []
    content_urls: list[str] = []
    targets: list[Target] = []
    for item in items:
        require(isinstance(item, dict), "manifest item must be an object")
        item_id = item.get("id")
        item_path = safe_remote_path(item.get("path"), "item path")
        content_url = safe_remote_path(item.get("contentUrl"), f"item {item_id} contentUrl")
        require(isinstance(item_id, str) and bool(item_id), "item ID must be a non-empty string")
        require(content_url == f"content/{item_path}", f"item {item_id} contentUrl does not match its path")
        require(item.get("route") == f"#/doc/{item_id}", f"item {item_id} route is invalid")
        item_digest = item.get("sha256")
        item_size = item.get("size")
        require(isinstance(item_digest, str) and bool(SHA256_PATTERN.fullmatch(item_digest)), f"item {item_id} SHA-256 is invalid")
        require(type(item_size) is int and item_size >= 0, f"item {item_id} size is invalid")
        local_source = ROOT / item_path
        require(local_source.is_file(), f"item {item_id} is missing from the verifier checkout")
        require(local_source.stat().st_size == item_size, f"item {item_id} size differs from the verifier checkout")
        require(sha256_file(local_source) == item_digest, f"item {item_id} SHA-256 differs from the verifier checkout")
        item_paths.append(item_path)
        item_ids.append(item_id)
        content_urls.append(content_url)
        targets.append(Target(content_url, item_digest, item_size, f"content item {item_path}"))

    require(len(item_paths) == len(set(item_paths)), "manifest contains duplicate item paths")
    require(len(item_ids) == len(set(item_ids)), "manifest contains duplicate item IDs")
    require(len(content_urls) == len(set(content_urls)), "manifest contains duplicate content URLs")
    for study_path in study_paths:
        normalized = safe_remote_path(study_path, "study path")
        require(normalized in item_paths, f"requested study path is not published: {normalized}")

    available_routes = validated_route_inventory(manifest, items)
    for route in expected_routes:
        require(isinstance(route, str) and route.startswith("#/") and route in available_routes, f"requested derived route is not published: {route}")

    for relative, metadata in assets.items():
        safe_remote_path(relative, "asset path")
        require(isinstance(metadata, dict), f"asset {relative} metadata is invalid")
        asset_digest = metadata.get("sha256")
        asset_size = metadata.get("size")
        require(isinstance(asset_digest, str) and bool(SHA256_PATTERN.fullmatch(asset_digest)), f"asset {relative} SHA-256 is invalid")
        require(type(asset_size) is int and asset_size >= 0, f"asset {relative} size is invalid")
        source_relative = "index.html" if relative == "404.html" else relative
        local_source = ROOT / "site" / source_relative
        require(local_source.is_file(), f"asset {relative} is missing from the verifier checkout")
        require(local_source.stat().st_size == asset_size, f"asset {relative} size differs from the verifier checkout")
        require(sha256_file(local_source) == asset_digest, f"asset {relative} SHA-256 differs from the verifier checkout")
        if relative not in {"index.html", "404.html"}:
            targets.append(Target(relative, asset_digest, asset_size, f"asset {relative}"))
    return targets


def fetch_target_digest(
    base_url: str,
    target: Target,
    token: str,
    timeout: float,
    deadline: float,
) -> tuple[int, int, str]:
    require(target.size <= MAX_TARGET_BYTES, f"{target.label} exceeds the public artifact size limit")
    url = request_url(base_url, target.relative, token)
    request = Request(
        url,
        headers={
            "Accept": "*/*",
            "Cache-Control": "no-cache, no-store, max-age=0",
            "Pragma": "no-cache",
            "User-Agent": "api-management-studies-pages-verifier/1",
        },
    )
    try:
        response = urlopen(request, timeout=remaining_timeout(deadline, timeout))
    except HTTPError as exc:
        try:
            return exc.code, 0, digest(b"")
        finally:
            exc.close()
    except (URLError, TimeoutError, OSError) as exc:
        raise VerificationError(f"request failed for {target.relative}: {exc}") from exc
    with response:
        length = response.headers.get("Content-Length")
        if length is not None:
            try:
                require(int(length) == target.size, f"{target.label} Content-Length differs from the manifest")
            except ValueError as exc:
                raise VerificationError(f"{target.label} has an invalid Content-Length") from exc
        file_digest = hashlib.sha256()
        size = 0
        read_chunk = getattr(response, "read1", response.read)
        while True:
            remaining_timeout(deadline, timeout)
            chunk = read_chunk(min(1024 * 1024, target.size - size + 1))
            remaining_timeout(deadline, timeout)
            if not chunk:
                break
            size += len(chunk)
            require(size <= target.size, f"{target.label} size exceeds the manifest")
            file_digest.update(chunk)
        return response.status, size, file_digest.hexdigest()


def verify_target(base_url: str, target: Target, token: str, timeout: float, deadline: float) -> None:
    status, size, target_digest = fetch_target_digest(base_url, target, token, timeout, deadline)
    require(status == 200, f"{target.label} returned HTTP {status}")
    require(size == target.size, f"{target.label} size differs from the manifest")
    require(target_digest == target.sha256, f"{target.label} SHA-256 differs from the manifest")


def verify_targets(
    base_url: str,
    targets: list[Target],
    token: str,
    timeout: float,
    workers: int,
    deadline: float,
) -> None:
    """Verify the target set without letting queued futures extend the deadline."""
    failures: list[str] = []
    executor = ThreadPoolExecutor(max_workers=workers)
    future_targets = {
        executor.submit(verify_target, base_url, target, f"{token}-{index}", timeout, deadline): target
        for index, target in enumerate(targets)
    }
    pending = set(future_targets)
    timed_out = False
    try:
        while pending:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                timed_out = True
                raise VerificationError("overall verification deadline expired")
            done, not_done = wait(pending, timeout=remaining, return_when=FIRST_COMPLETED)
            if not done:
                timed_out = True
                raise VerificationError("overall verification deadline expired")
            pending = set(not_done)
            for future in done:
                target = future_targets[future]
                try:
                    future.result()
                except Exception as exc:  # Report every concurrently observed mismatch together.
                    failures.append(f"{target.label}: {exc}")
    finally:
        for future in pending:
            future.cancel()
        executor.shutdown(wait=not timed_out, cancel_futures=True)
    require(not failures, "; ".join(sorted(failures)))


def verify_once(
    base_url: str,
    expected_revision: str,
    study_paths: list[str],
    attempt: int,
    timeout: float,
    workers: int,
    expected_manifest_sha256: str | None,
    expected_routes: list[str],
    deadline: float,
) -> tuple[int, int]:
    token = f"{expected_revision}-{attempt}"
    manifest, manifest_bytes = load_manifest(base_url, token, timeout, deadline)
    if expected_manifest_sha256:
        require(digest(manifest_bytes) == expected_manifest_sha256, "deployed manifest SHA-256 differs from the build artifact")
    targets = validate_manifest_shape(manifest, expected_revision, study_paths, expected_routes)
    assets = manifest["assets"]

    root_status, root = fetch(base_url, "", token, timeout, deadline, assets["index.html"]["size"] + 1)
    require(root_status == 200, f"site root returned HTTP {root_status}")
    require(len(root) == assets["index.html"]["size"], "site root size differs from index.html provenance")
    require(digest(root) == assets["index.html"]["sha256"], "site root does not match index.html provenance")

    missing_path = f"__pages_provenance_{expected_revision}_{attempt}.html"
    missing_status, missing = fetch(
        base_url, missing_path, token, timeout, deadline, assets["404.html"]["size"] + 1
    )
    require(missing_status == 404, f"unknown Pages path returned HTTP {missing_status}, expected 404")
    require(len(missing) == assets["404.html"]["size"], "404 response size differs from 404.html provenance")
    require(digest(missing) == assets["404.html"]["sha256"], "404 response does not match 404.html provenance")

    verify_targets(base_url, targets, token, timeout, workers, deadline)
    return len(manifest["items"]), len(manifest["assets"])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", required=True, help="Deployed Pages URL, including any repository base path")
    parser.add_argument(
        "--expected-revision",
        default=os.environ.get("SOURCE_REVISION") or os.environ.get("GITHUB_SHA"),
        help="Full revision GitHub Pages must serve (defaults to SOURCE_REVISION, then GITHUB_SHA)",
    )
    parser.add_argument("--study-path", action="append", default=[], help="Require this repository study path; repeat as needed")
    parser.add_argument("--expected-route", action="append", default=[], help="Require this exact manifest-backed SPA route; repeat as needed")
    parser.add_argument(
        "--expected-manifest-sha256",
        default=os.environ.get("EXPECTED_MANIFEST_SHA256"),
        help="SHA-256 of the manifest produced by the build job",
    )
    parser.add_argument("--retries", type=int, default=18, help="Maximum deployment-read attempts")
    parser.add_argument("--delay", type=float, default=10.0, help="Seconds between attempts")
    parser.add_argument("--timeout", type=float, default=30.0, help="Per-request timeout in seconds")
    parser.add_argument("--overall-timeout", type=float, default=600.0, help="Overall verification deadline in seconds")
    parser.add_argument("--workers", type=int, default=8, help="Concurrent content verification requests")
    args = parser.parse_args()

    require(args.expected_revision is not None, "--expected-revision is required when no revision environment variable is set")
    expected_revision = args.expected_revision.lower()
    require(bool(REVISION_PATTERN.fullmatch(expected_revision)), "--expected-revision must be a full hexadecimal Git object ID")
    if args.expected_manifest_sha256 is not None:
        require(
            bool(SHA256_PATTERN.fullmatch(args.expected_manifest_sha256)),
            "--expected-manifest-sha256 must be a lowercase SHA-256 digest",
        )
    require(args.retries > 0 and args.delay >= 0 and args.timeout > 0 and args.overall_timeout > 0 and args.workers > 0, "retry, delay, timeout, and worker values are invalid")
    split = urlsplit(args.base_url)
    require(split.scheme in {"http", "https"} and bool(split.netloc), "--base-url must be an absolute HTTP(S) URL")
    base_url = args.base_url.rstrip("/") + "/"
    verify_local_checkout(expected_revision)

    last_error: Exception | None = None
    deadline = time.monotonic() + args.overall_timeout
    for attempt in range(1, args.retries + 1):
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            last_error = VerificationError("overall verification deadline expired")
            break
        try:
            item_count, asset_count = verify_once(
                base_url,
                expected_revision,
                args.study_path,
                attempt,
                min(args.timeout, remaining),
                args.workers,
                args.expected_manifest_sha256,
                args.expected_route,
                deadline,
            )
            print(
                f"OK: Pages serves clean revision {expected_revision}; "
                f"root, 404, {item_count} content items, and {asset_count} assets match"
            )
            return 0
        except VerificationError as exc:
            last_error = exc
            if attempt == args.retries:
                break
            print(f"WAIT: Pages verification attempt {attempt}/{args.retries} did not converge: {exc}")
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                last_error = VerificationError("overall verification deadline expired")
                break
            time.sleep(min(args.delay, remaining))
    print(f"ERROR: Pages did not serve the expected artifact: {last_error}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except VerificationError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
