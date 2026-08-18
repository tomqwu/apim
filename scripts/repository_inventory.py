#!/usr/bin/env python3
"""Git-aware, public-safe input inventory for repository validators."""

from __future__ import annotations

import hashlib
import os
import subprocess
import unicodedata
from pathlib import Path


class InventoryError(RuntimeError):
    """Candidate source enumeration failed closed."""


GIT_REDIRECT_VARIABLES = {
    "GIT_DIR",
    "GIT_WORK_TREE",
    "GIT_INDEX_FILE",
    "GIT_OBJECT_DIRECTORY",
    "GIT_ALTERNATE_OBJECT_DIRECTORIES",
    "GIT_COMMON_DIR",
    "GIT_CEILING_DIRECTORIES",
    "GIT_CONFIG_PARAMETERS",
    "GIT_CONFIG",
    "GIT_CONFIG_GLOBAL",
    "GIT_CONFIG_SYSTEM",
    "GIT_CONFIG_NOSYSTEM",
    "GIT_LITERAL_PATHSPECS",
    "GIT_GLOB_PATHSPECS",
    "GIT_NOGLOB_PATHSPECS",
    "GIT_ICASE_PATHSPECS",
}


def git_environment() -> dict[str, str]:
    """Preserve authentication while removing repository/index redirection."""
    environment = os.environ.copy()
    for key in tuple(environment):
        if key in GIT_REDIRECT_VARIABLES or key == "GIT_CONFIG_COUNT" or key.startswith("GIT_CONFIG_KEY_") or key.startswith("GIT_CONFIG_VALUE_"):
            environment.pop(key, None)
    environment["GIT_NO_REPLACE_OBJECTS"] = "1"
    return environment


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
        env=git_environment(),
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
        env=git_environment(),
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

    staged = subprocess.run(
        ("git", "ls-files", "-s", "-z"),
        cwd=root,
        env=git_environment(),
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if staged.returncode:
        raise InventoryError("unable to inspect tracked candidate modes")
    for entry in (value for value in staged.stdout.split(b"\0") if value):
        mode = entry.split(b" ", 1)[0]
        if mode not in {b"100644", b"100755"}:
            raise InventoryError("tracked candidate contains a non-regular Git mode")

    paths: list[Path] = []
    for name in names:
        if "%" in name or name != name.strip() or any(unicodedata.category(character).startswith("C") for character in name):
            raise InventoryError("candidate source path contains percent, control, or surrounding whitespace")
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
