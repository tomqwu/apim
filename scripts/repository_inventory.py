#!/usr/bin/env python3
"""Git-aware, public-safe input inventory for repository validators."""

from __future__ import annotations

import hashlib
import subprocess
import unicodedata
from pathlib import Path


class InventoryError(RuntimeError):
    """Candidate source enumeration failed closed."""


def safe_location(value: str) -> str:
    digest = hashlib.sha256(value.encode("utf-8", errors="surrogatepass")).hexdigest()
    return f"path-sha256:{digest[:16]}"


def _has_symlink_component(root: Path, relative: str) -> bool:
    candidate = root
    for part in Path(relative).parts:
        candidate /= part
        if candidate.is_symlink():
            return True
    return False


def candidate_files(root: Path) -> list[Path]:
    """Return tracked plus non-ignored untracked regular files.

    Ignored local evidence is deliberately absent. Public symlinks, hostile path
    names, invalid UTF-8, and hidden Git index state fail before a validator can
    read or echo their contents.
    """

    root = root.resolve()
    hidden = subprocess.run(
        ("git", "ls-files", "-v", "-z"),
        cwd=root,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if hidden.returncode:
        raise InventoryError("unable to inspect Git index visibility flags")
    if any(entry[:1] == b"S" or entry[:1].islower() for entry in hidden.stdout.split(b"\0") if entry):
        raise InventoryError("Git index visibility flags hide candidate source state")

    listed = subprocess.run(
        ("git", "ls-files", "-c", "-o", "--exclude-standard", "-z"),
        cwd=root,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if listed.returncode:
        raise InventoryError("unable to enumerate candidate source inputs")
    try:
        names = [value.decode("utf-8") for value in listed.stdout.split(b"\0") if value]
    except UnicodeDecodeError as exc:
        raise InventoryError("candidate source path is not UTF-8") from exc

    paths: list[Path] = []
    for name in names:
        if name != name.strip() or any(unicodedata.category(character).startswith("C") for character in name):
            raise InventoryError("candidate source path contains control or surrounding whitespace")
        location = safe_location(name)
        path = root / name
        if path.is_symlink() or _has_symlink_component(root, name):
            raise InventoryError(f"candidate source is symlinked at {location}")
        if path.is_file():
            paths.append(path)
    return sorted(set(paths))


def files_with_suffixes(root: Path, suffixes: set[str], within: Path | None = None) -> list[Path]:
    boundary = within.resolve() if within is not None else None
    selected: list[Path] = []
    for path in candidate_files(root):
        if boundary is not None and not path.resolve().is_relative_to(boundary):
            continue
        if path.suffix.lower() in suffixes:
            selected.append(path)
    return selected
