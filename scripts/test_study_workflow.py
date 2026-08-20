#!/usr/bin/env python3
"""Hermetic acceptance tests for ``scripts/study_workflow.py``.

The tests intentionally exercise the production CLI in temporary Git repositories.
They use only the Python standard library and never contact GitHub.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path
from types import SimpleNamespace
from typing import Any
from unittest import mock


SOURCE_ROOT = Path(__file__).resolve().parents[1]
PRODUCTION_CLI = SOURCE_ROOT / "scripts" / "study_workflow.py"
PAGES_VERIFIER = SOURCE_ROOT / "scripts" / "verify_pages.py"

EXPECTED_STATES = (
    "INTAKE",
    "FRAMED",
    "RESEARCHED",
    "AUTHORED",
    "PROJECTED",
    "CANDIDATE",
    "REVIEWED",
    "VALIDATED",
    "MERGED",
    "PUBLISHED",
    "CLOSED",
    "REWORK",
    "BLOCKED",
)

REPOSITORY_FIXTURES = (
    ".gitignore",
    "AGENTS.md",
    "config/public-content-allowlist.json",
    "docs/46-study-publication-workflow.md",
    "docs/47-kong-enterprise-platform-strategy.md",
    "templates/study-intake-template.md",
    ".agents/skills/publish-api-study/SKILL.md",
    ".agents/skills/publish-api-study/agents/openai.yaml",
    ".agents/skills/publish-api-study/references/repo-contract.md",
    ".github/pull_request_template.md",
    "requirements-validation.txt",
    "scripts/build_site.py",
    "scripts/repository_inventory.py",
    "scripts/study_workflow.py",
    "scripts/test_study_workflow.py",
    "scripts/validate_site_manifest.py",
    "scripts/verify_pages.py",
)

# Hermetic repositories must resolve provenance from their own Git history.
# GitHub Actions exports the synthetic pull-request merge revision to every
# child process; that object does not exist in these independently initialized
# fixture repositories and must not override their local HEAD.
OUTER_PROVENANCE_ENVIRONMENT = (
    "GITHUB_SHA",
    "SOURCE_REVISION",
    "SOURCE_DATE_EPOCH",
    "EXPECTED_MANIFEST_SHA256",
)


def load_production_module() -> Any:
    """Load constants/functions without executing the CLI entry point."""

    name = f"study_workflow_under_test_{os.getpid()}_{id(object())}"
    spec = importlib.util.spec_from_file_location(name, PRODUCTION_CLI)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {PRODUCTION_CLI}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_pages_verifier_module() -> Any:
    """Load the Pages verifier so deadline behavior can be tested without HTTP."""

    name = f"verify_pages_under_test_{os.getpid()}_{id(object())}"
    spec = importlib.util.spec_from_file_location(name, PAGES_VERIFIER)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {PAGES_VERIFIER}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def poc_projection_fixture() -> dict[str, Any]:
    tests = [
        *(
            {"id": f"POC-{index:03d}", "status": "Automated"}
            for index in range(1, 6)
        ),
        {"id": "POC-006", "status": "Not run"},
        *(
            {"id": f"POC-{index}", "status": "Not run"}
            for index in range(101, 111)
        ),
    ]
    return {
        "total": 16,
        "byStatus": [
            {"label": "Not run", "value": 11},
            {"label": "Automated", "value": 5},
        ],
        "tests": tests,
    }


class TemporaryWorkflowRepository:
    """A minimal canonical repository with deterministic Git history."""

    def __init__(self, *, local_origin: bool = False, full: bool = False) -> None:
        self._temporary = tempfile.TemporaryDirectory(prefix="study-workflow-test-")
        self.container = Path(self._temporary.name)
        self.root = self.container / "repo"
        self.root.mkdir()
        self.tool_bin = self.container / "test-bin"
        self.tool_bin.mkdir()
        self.python_bin = self.container / "python-bin"
        self.python_bin.mkdir()
        self.python_executable = self.python_bin / "python"
        self.python_executable.symlink_to(sys.executable)
        self.environment = os.environ.copy()
        for variable in OUTER_PROVENANCE_ENVIRONMENT:
            self.environment.pop(variable, None)
        self.environment.pop("GIT_NO_REPLACE_OBJECTS", None)
        self.environment.update(
            {
                "GIT_TERMINAL_PROMPT": "0",
                "LC_ALL": "C",
                "LANG": "C",
                "TZ": "UTC",
            }
        )
        fixture_paths = list(REPOSITORY_FIXTURES)
        if full:
            tracked = subprocess.run(
                ("git", "ls-files", "-z"),
                cwd=SOURCE_ROOT,
                check=True,
                stdout=subprocess.PIPE,
            ).stdout.split(b"\0")
            fixture_paths = [
                value.decode("utf-8") for value in tracked if value
            ]
            fixture_paths.extend(REPOSITORY_FIXTURES)
        for relative in sorted(set(fixture_paths)):
            source = SOURCE_ROOT / relative
            destination = self.root / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)

        if not full:
            (self.root / "Makefile").write_text(
                "validate:\n"
                "\t@if [ \"$${FAKE_MAKE_RC:-0}\" -ne 0 ]; then exit \"$${FAKE_MAKE_RC}\"; fi\n"
                "\t@if [ -n \"$$EXPECTED_PYTHON_BIN\" ]; then case \":$$PATH:\" in *\":$$EXPECTED_PYTHON_BIN:\"*) ;; *) exit 41 ;; esac; fi\n",
                encoding="utf-8",
            )

        self.git("init", "-q")
        self.git("branch", "-M", "main")
        self.git("config", "user.name", "Workflow Test")
        self.git("config", "user.email", "workflow-test@example.invalid")
        self.git("config", "commit.gpgsign", "false")
        self.git("add", ".")
        self.git("commit", "-q", "-m", "Canonical workflow baseline")
        self.base_sha = self.git("rev-parse", "HEAD").stdout.strip()

        # Every fixture gets a local bare origin behind a syntactically public
        # GitHub URL. Git's insteadOf transport keeps production identity rules
        # strict without contacting the network.
        self.origin = self.container / "origin.git"
        self._run(("git", "init", "--bare", "-q", str(self.origin)), cwd=self.container)
        self.public_remote = "git@github.com:owner/repo.git"
        self.git("config", f"url.{self.origin}.insteadOf", self.public_remote)
        self.git("remote", "add", "origin", self.public_remote)
        self.git("push", "-q", "-u", "origin", "main")
        self.environment["FAKE_MAIN_REF_JSON"] = json.dumps(
            [{"ref": "refs/heads/main", "object": {"sha": self.base_sha}}]
        )
        self.install_fake_release_tools()

    def cleanup(self) -> None:
        self._temporary.cleanup()

    def _run(
        self,
        command: tuple[str, ...],
        *,
        cwd: Path | None = None,
        environment: dict[str, str] | None = None,
    ) -> subprocess.CompletedProcess[str]:
        merged_environment = self.environment.copy()
        if environment:
            merged_environment.update(environment)
        return subprocess.run(
            command,
            cwd=cwd or self.root,
            env=merged_environment,
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    def git(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        environment = {
            "GIT_AUTHOR_DATE": "2030-01-02T03:04:05Z",
            "GIT_COMMITTER_DATE": "2030-01-02T03:04:05Z",
        }
        result = self._run(("git", *arguments), environment=environment)
        if result.returncode:
            raise AssertionError(
                f"git {' '.join(arguments)} failed ({result.returncode})\n"
                f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
            )
        return result

    def cli(
        self,
        *arguments: str,
        environment: dict[str, str] | None = None,
        python_executable: str | Path | None = None,
    ) -> subprocess.CompletedProcess[str]:
        merged = {"PATH": f"{self.tool_bin}{os.pathsep}{self.environment.get('PATH', '')}"}
        if environment:
            merged.update(environment)
        return self._run(
            (
                str(python_executable or self.python_executable),
                "-I",
                str(self.root / "scripts" / "study_workflow.py"),
                *arguments,
            ),
            environment=merged,
        )

    def write_text(self, relative: str, text: str) -> Path:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def write_bytes(self, relative: str, data: bytes) -> Path:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        return path

    def load_module(self, relative: str) -> Any:
        path = self.root / relative
        name = f"temporary_{path.stem}_{os.getpid()}_{id(path)}"
        spec = importlib.util.spec_from_file_location(name, path)
        if spec is None or spec.loader is None:
            raise RuntimeError(f"cannot load {path}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def commit_all(self, message: str) -> str:
        self.git("add", "-A")
        self.git("commit", "-q", "-m", message)
        return self.git("rev-parse", "HEAD").stdout.strip()

    def publish_pull_head(self, number: int, candidate: str) -> None:
        result = self._run(
            (
                "git", "--git-dir", str(self.origin), "update-ref",
                f"refs/pull/{number}/head", candidate,
            ),
            cwd=self.container,
        )
        if result.returncode:
            raise AssertionError(result.stdout + result.stderr)

    def new_checkpoint(
        self,
        *,
        slug: str = "workflow-test",
        write_spec: bool = False,
        title: str = "Workflow test",
        request_summary: str = "Validate a sanitized workflow fixture.",
        decision_question: str = "Does the workflow enforce its publication contract?",
        environment: dict[str, str] | None = None,
    ) -> tuple[Path, dict[str, Any], subprocess.CompletedProcess[str]]:
        arguments = [
            "new",
            "--slug",
            slug,
            "--title",
            title,
            "--source-kind",
            "chat",
            "--requested-actions",
            "research,edit,branch,commit,push,pull-request,merge,branch-cleanup,pages-verification",
            "--request-summary",
            request_summary,
            "--input-reference",
            "https://example.com/tasks/workflow-test",
            "--decision-question",
            decision_question,
            "--date",
            "20300102",
        ]
        if write_spec:
            arguments.append("--write-spec")
        main_result = self._run(("git", "ls-remote", "--heads", "origin", "refs/heads/main"))
        main_line = main_result.stdout.strip() if main_result.returncode == 0 else ""
        main_sha = main_line.split()[0] if main_line else self.base_sha
        command_environment = {
            "FAKE_MAIN_REF_JSON": json.dumps(
                [{"ref": "refs/heads/main", "object": {"sha": main_sha}}]
            )
        }
        if environment:
            command_environment.update(environment)
        result = self.cli(*arguments, environment=command_environment)
        if result.returncode:
            return Path(), {}, result
        payload = json.loads(result.stdout)
        checkpoint = self.root / payload["checkpoint"]
        return checkpoint, json.loads(checkpoint.read_text(encoding="utf-8")), result

    def replace_checkpoint(self, checkpoint: Path, data: dict[str, Any]) -> None:
        checkpoint.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    def prepare_draft(self) -> tuple[Path, dict[str, Any], str]:
        checkpoint, data, result = self.new_checkpoint()
        if result.returncode:
            raise AssertionError(result.stderr)
        self.write_text("docs/workflow-test.md", "# Workflow test\n\nPublic-safe canonical fixture.\n")
        self.write_text("site/workflow-test.json", '{"fixture": true}\n')
        head = self.commit_all("Add workflow test candidate")
        validation = self.cli(
            "record",
            "--checkpoint",
            str(checkpoint),
            "--local-validation",
            "pass",
        )
        if validation.returncode:
            raise AssertionError(validation.stdout + validation.stderr)
        data = json.loads(checkpoint.read_text(encoding="utf-8"))
        data.update(
            {
                "canonicalState": "PROJECTED",
                "statusReason": "Canonical and derived fixtures are ready for local validation.",
                "artifactType": "workflow",
                "audiences": ["repository maintainers"],
                "scopeSummary": "The deterministic study publication workflow and its gates.",
                "deltaSummary": "A canonical workflow fixture plus its derived projection.",
                "evidenceReferences": ["https://example.com/evidence/workflow-contract"],
                "canonicalPaths": ["docs/workflow-test.md"],
                "derivedPaths": ["site/workflow-test.json", "#/doc/workflow-test"],
                "nextGate": "Create the candidate commit and draft pull request.",
            }
        )
        self.replace_checkpoint(checkpoint, data)
        manifest = self.root / "_site" / "content-manifest.json"
        manifest.parent.mkdir(parents=True, exist_ok=True)
        manifest.write_text(
            json.dumps(
                {
                    "items": [
                        {
                            "path": "docs/workflow-test.md",
                            "route": "#/doc/workflow-test",
                        }
                    ],
                    "presentation": [],
                    "audiences": [],
                    "presentationDecks": [],
                }
            ),
            encoding="utf-8",
        )
        self.install_fake_release_tools()
        return checkpoint, data, head

    def prepare_candidate(self) -> tuple[Path, dict[str, Any], str]:
        checkpoint, data, head = self.prepare_draft()
        self.git("push", "-q", "origin", f"{head}:refs/heads/{data['branch']}")
        data.update(
            {
                "canonicalState": "CANDIDATE",
                "statusReason": "The draft pull request records the candidate commit.",
                "candidateSha": head,
                "prNumber": 17,
                "prUrl": "https://github.com/owner/repo/pull/17",
                "prHeadSha": head,
                "prDraft": True,
                "nextGate": "Complete independent review of the recorded candidate SHA.",
            }
        )
        data["candidateEnvelopeSha256"] = self.load_module(
            "scripts/study_workflow.py"
        ).candidate_envelope_digest(data)
        self.replace_checkpoint(checkpoint, data)
        return checkpoint, data, head

    def prepare_release(self) -> tuple[Path, dict[str, Any], str]:
        checkpoint, data, head = self.prepare_draft()
        self.git("push", "-q", "origin", f"{head}:refs/heads/{data['branch']}")
        self.publish_pull_head(17, head)
        data.update(
            {
                "canonicalState": "VALIDATED",
                "statusReason": "Independent review and required checks accept the candidate.",
                "candidateSha": head,
                "prNumber": 17,
                "prUrl": "https://github.com/owner/repo/pull/17",
                "prHeadSha": head,
                "prDraft": False,
                "reviewDisposition": "pass",
                "acceptedSha": head,
                "reviewEvidenceUrls": [
                    "https://github.com/owner/repo/pull/17#issuecomment-99"
                ],
                "checkedSha": head,
                "checkDisposition": "green",
                "checkUrls": [
                    "https://github.com/owner/repo/actions/runs/201",
                    "https://github.com/owner/repo/actions/runs/202",
                ],
                "derivedPaths": ["site/workflow-test.json", "#/doc/workflow-test"],
                "nextGate": "Merge the accepted pull request without SHA drift.",
            }
        )
        data["candidateEnvelopeSha256"] = self.load_module(
            "scripts/study_workflow.py"
        ).candidate_envelope_digest(data)
        self.replace_checkpoint(checkpoint, data)
        manifest = self.root / "_site" / "content-manifest.json"
        manifest.parent.mkdir(parents=True, exist_ok=True)
        manifest.write_text(
            json.dumps(
                {
                    "items": [
                        {
                            "path": "docs/workflow-test.md",
                            "route": "#/doc/workflow-test",
                        }
                    ],
                    "presentation": [],
                    "audiences": [],
                    "presentationDecks": [],
                }
            ),
            encoding="utf-8",
        )
        self.install_fake_release_tools()
        return checkpoint, data, head

    def install_fake_release_tools(self) -> None:
        gh = self.tool_bin / "gh"
        gh.write_text(
            "#!/usr/bin/env python3\n"
            "import os, sys\n"
            "if os.environ.get('GH_REPO') or os.environ.get('GH_HOST'):\n"
            "    raise SystemExit(73)\n"
            "args = sys.argv[1:]\n"
            "if args[:2] == ['pr', 'view']:\n"
            "    key = 'FAKE_PR_JSON'\n"
            "elif args[:2] == ['pr', 'list']:\n"
            "    key = 'FAKE_PR_LIST_JSON'\n"
            "elif args[:2] == ['repo', 'view']:\n"
            "    key = 'FAKE_REPO_JSON'\n"
            "elif args[:1] == ['api']:\n"
            "    if args[1].endswith('/pages'):\n"
            "        key = 'FAKE_PAGES_JSON'\n"
            "    elif args[1].endswith('/git/matching-refs/heads/main'):\n"
            "        key = 'FAKE_MAIN_REF_JSON'\n"
            "    elif '/git/matching-refs/heads/' in args[1]:\n"
            "        import json\n"
            "        explicit = os.environ.get('FAKE_BRANCH_REF_JSON')\n"
            "        if explicit is not None:\n"
            "            print(explicit)\n"
            "            raise SystemExit(int(os.environ.get('FAKE_BRANCH_REF_RC', '0')))\n"
            "        pr = json.loads(os.environ.get('FAKE_PR_JSON', '{}'))\n"
            "        if pr.get('state') == 'OPEN' and pr.get('headRefOid'):\n"
            "            print(json.dumps([{'ref': 'refs/heads/' + pr['headRefName'], 'object': {'sha': pr['headRefOid']}}]))\n"
            "            raise SystemExit(0)\n"
            "        print('[]')\n"
            "        raise SystemExit(0)\n"
            "    elif args[1].endswith('/100'):\n"
            "        key = 'FAKE_CLOSURE_COMMENT_JSON'\n"
            "    else:\n"
            "        key = 'FAKE_COMMENT_JSON'\n"
            "elif args[:2] == ['run', 'view']:\n"
            "    key = 'FAKE_RUN_' + args[2] + '_JSON'\n"
            "else:\n"
            "    key = 'FAKE_UNKNOWN_JSON'\n"
            "default = '[]' if key == 'FAKE_PR_LIST_JSON' else '{}'\n"
            "print(os.environ.get(key, default))\n",
            encoding="utf-8",
        )
        make = self.tool_bin / "make"
        make.write_text(
            "#!/usr/bin/env python3\n"
            "import os\n"
            "if any(os.environ.get(key) for key in ('MAKEFLAGS', 'GNUMAKEFLAGS', 'MFLAGS', 'MAKEFILES')):\n"
            "    raise SystemExit(42)\n"
            "expected = os.environ.get('EXPECTED_PYTHON_BIN')\n"
            "if expected and expected not in os.environ.get('PATH', '').split(os.pathsep):\n"
            "    raise SystemExit(41)\n"
            "raise SystemExit(int(os.environ.get('FAKE_MAKE_RC', '0')))\n",
            encoding="utf-8",
        )
        for path in (gh, make):
            path.chmod(path.stat().st_mode | stat.S_IXUSR)

    def install_fake_ssh_transport(self) -> dict[str, str]:
        ssh = self.tool_bin / "ssh"
        ssh.write_text(
            "#!/usr/bin/env python3\n"
            "import os\n"
            "os.execvp('git-upload-pack', ['git-upload-pack', os.environ['FAKE_GIT_REPOSITORY']])\n",
            encoding="utf-8",
        )
        ssh.chmod(ssh.stat().st_mode | stat.S_IXUSR)
        return {
            "FAKE_GIT_REPOSITORY": str(self.origin),
            "GIT_SSH_COMMAND": str(ssh),
            "GIT_SSH_VARIANT": "ssh",
        }

    @staticmethod
    def valid_pr_json(
        head: str,
        *,
        branch: str = "study/workflow-test",
        draft: bool = False,
        merged: bool = False,
        merge_sha: str | None = None,
    ) -> dict[str, Any]:
        return {
            "number": 17,
            "url": "https://github.com/owner/repo/pull/17",
            "title": "Publish workflow test candidate",
            "body": (
                "<!-- study-workflow-checkpoint:start -->\n"
                "sanitized checkpoint\n"
                "<!-- study-workflow-checkpoint:end -->"
            ),
            "baseRefName": "main",
            "headRefOid": head,
            "headRefName": branch,
            "headRepositoryOwner": {"login": "owner"},
            "isCrossRepository": False,
            "isDraft": draft,
            "state": "MERGED" if merged else "OPEN",
            "statusCheckRollup": [
                {
                    "name": "static-validation",
                    "conclusion": "SUCCESS",
                    "workflowName": "validate",
                    "detailsUrl": "https://github.com/owner/repo/actions/runs/201/job/2001",
                },
                {
                    "name": "docker-smoke",
                    "conclusion": "SUCCESS",
                    "workflowName": "validate",
                    "detailsUrl": "https://github.com/owner/repo/actions/runs/202/job/2002",
                },
            ],
            "mergeCommit": {"oid": merge_sha} if merge_sha else None,
        }

    def fake_github_environment(self, pr: dict[str, Any], accepted_sha: str) -> dict[str, str]:
        main_line = self.git("ls-remote", "--heads", "origin", "refs/heads/main").stdout.strip()
        main_sha = main_line.split()[0] if main_line else self.base_sha
        checkpoint_data: dict[str, Any] | None = None
        try:
            checkpoint_data = self.load_module(
                "scripts/study_workflow.py"
            ).embedded_checkpoint(pr.get("body", ""))
        except Exception:
            checkpoint_data = None
        envelope = (
            checkpoint_data.get("candidateEnvelopeSha256")
            if isinstance(checkpoint_data, dict)
            else "0" * 64
        )
        return {
            "FAKE_PR_JSON": json.dumps(pr),
            "FAKE_REPO_JSON": json.dumps({"nameWithOwner": "owner/repo"}),
            "FAKE_MAIN_REF_JSON": json.dumps([{"ref": "refs/heads/main", "object": {"sha": main_sha}}]),
            "FAKE_COMMENT_JSON": json.dumps(
                {
                    "html_url": "https://github.com/owner/repo/pull/17#issuecomment-99",
                    "issue_url": "https://api.github.com/repos/owner/repo/issues/17",
                    "body": (
                        f"Accepted head SHA: {accepted_sha}\n"
                        f"Candidate envelope SHA-256: {envelope}\n"
                        "Independent reviewer: workflow acceptance role\n"
                        "Reviewer did not author candidate: yes\n"
                        "Review disposition: pass\n"
                    ),
                }
            ),
            "FAKE_RUN_201_JSON": json.dumps(
                {
                    "headSha": accepted_sha,
                    "status": "completed",
                    "conclusion": "success",
                    "url": "https://github.com/owner/repo/actions/runs/201",
                    "workflowName": "validate",
                }
            ),
            "FAKE_RUN_202_JSON": json.dumps(
                {
                    "headSha": accepted_sha,
                    "status": "completed",
                    "conclusion": "success",
                    "url": "https://github.com/owner/repo/actions/runs/202",
                    "workflowName": "validate",
                }
            ),
            "FAKE_MAKE_RC": "0",
        }

    def with_current_checkpoint_body(
        self, pr: dict[str, Any], checkpoint: Path
    ) -> dict[str, Any]:
        rendered = self.cli("render", "--checkpoint", str(checkpoint))
        if rendered.returncode:
            return pr
        value = dict(pr)
        value["body"] = "## Operational checkpoint\n\n" + rendered.stdout.strip()
        return value


class WorkflowTestCase(unittest.TestCase):
    maxDiff = None

    def repository(
        self, *, local_origin: bool = False, full: bool = False
    ) -> TemporaryWorkflowRepository:
        repository = TemporaryWorkflowRepository(local_origin=local_origin, full=full)
        self.addCleanup(repository.cleanup)
        return repository

    def assert_deterministic_error(
        self,
        result: subprocess.CompletedProcess[str],
        *,
        returncode: int = 2,
        contains: str | None = None,
    ) -> None:
        output = result.stdout + result.stderr
        self.assertEqual(returncode, result.returncode, output)
        self.assertNotIn("Traceback (most recent call last)", output)
        if contains:
            self.assertIn(contains, output)


class CanonicalContractTests(WorkflowTestCase):
    def test_operator_contract_bootstraps_before_new_and_uses_only_isolated_cli_commands(self) -> None:
        paths = (
            "README.md",
            "docs/46-study-publication-workflow.md",
            ".agents/skills/publish-api-study/SKILL.md",
            ".agents/skills/publish-api-study/references/repo-contract.md",
            ".github/pull_request_template.md",
        )
        for relative in paths:
            with self.subTest(path=relative):
                text_value = (SOURCE_ROOT / relative).read_text(encoding="utf-8")
                self.assertIn(".venv/bin/python -I scripts/study_workflow.py", text_value)
                self.assertNotIn("python3 scripts/study_workflow.py", text_value)
        skill = (SOURCE_ROOT / ".agents/skills/publish-api-study/SKILL.md").read_text(encoding="utf-8")
        self.assertLess(skill.index("python3.12 -I -m venv .venv"), skill.index("scripts/study_workflow.py new"))
        self.assertIn(".venv/bin/python -I -m pip", skill)
        self.assertIn("--repo github.com/<owner>/<repo>", skill)

    def test_source_safety_precedes_build_and_generated_safety_follows_it(self) -> None:
        makefile = (SOURCE_ROOT / "Makefile").read_text(encoding="utf-8")
        workflow = (SOURCE_ROOT / "docs/46-study-publication-workflow.md").read_text(encoding="utf-8")
        source_readers = (
            "validate-openapi",
            "validate-yaml",
            "validate-counts",
            "validate-links",
            "validate-sources",
            "validate-source-coverage",
            "validate-visuals",
            "validate-studies",
            "lint-shell",
        )
        for target in source_readers:
            with self.subTest(target=target):
                self.assertRegex(
                    makefile,
                    rf"(?m)^{re.escape(target)}: validate-public-source$",
                )
        self.assertRegex(makefile, r"(?m)^site: validate-public-source$")
        self.assertRegex(makefile, r"(?m)^validate-public-source:\n\t@\$\(PYTHON\) scripts/study_workflow.py validate-public-content --source-only$")
        self.assertRegex(makefile, r"(?m)^validate-public-content: site$")
        self.assertIn("scans source before any content parser or generator runs", workflow)
        self.assertIn("rescans source plus generated output", workflow)

    def test_independent_review_comment_contract_is_exact_and_copyable(self) -> None:
        required_lines = (
            "Accepted head SHA:",
            "Candidate envelope SHA-256:",
            "Independent reviewer:",
            "Reviewer did not author candidate: yes",
            "Review disposition: pass",
        )
        paths = (
            "docs/46-study-publication-workflow.md",
            "templates/study-intake-template.md",
            ".agents/skills/publish-api-study/SKILL.md",
            ".agents/skills/publish-api-study/references/repo-contract.md",
            ".github/pull_request_template.md",
        )
        expected_block = "\n".join(
            (
                "Accepted head SHA: <40-character candidate SHA>",
                "Candidate envelope SHA-256: <64-character candidate-envelope digest>",
                "Independent reviewer: <reviewer identity or role>",
                "Reviewer did not author candidate: yes",
                "Review disposition: pass",
            )
        )
        for relative in paths:
            with self.subTest(path=relative):
                text_value = (SOURCE_ROOT / relative).read_text(encoding="utf-8")
                self.assertIn(expected_block, text_value)
                for line in required_lines:
                    self.assertIn(line, expected_block)

    def test_independent_review_requires_one_contiguous_ordered_exact_block(self) -> None:
        module = load_production_module()
        accepted = "a" * 40
        envelope = "b" * 64
        scrambled = (
            "Review disposition: pass\n"
            "Independent reviewer: workflow acceptance role\n"
            "Reviewer did not author candidate: yes\n"
            f"Candidate envelope SHA-256: {envelope}\n"
            f"Accepted head SHA: {accepted}\n"
        )
        with mock.patch.object(module, "fetch_same_pr_comment", return_value=scrambled):
            with self.assertRaisesRegex(module.WorkflowError, "exact contiguous five-line"):
                module.verify_review_evidence(
                    ["https://github.com/owner/repo/pull/17#issuecomment-99"],
                    17,
                    accepted,
                    envelope,
                )

    def test_mermaid_runtime_converts_and_rejects_blank_node_labels(self) -> None:
        app = (SOURCE_ROOT / "site/assets/app.js").read_text(encoding="utf-8")
        self.assertIn('template.content.querySelector("svg")', app)
        self.assertIn('.toLowerCase() === "foreignobject"', app)
        self.assertIn('new Set(["br", "div", "p", "li", "section"])', app)
        self.assertIn("htmlSvgLabelText(foreignObject)", app)
        self.assertNotIn("wrapSvgLabel(foreignObject.textContent", app)
        self.assertIn('svg.querySelectorAll("g.node")', app)
        self.assertIn("Rendered diagram is missing", app)

    def test_article_artifacts_use_semantic_overview_and_inspection_modes(self) -> None:
        app = (SOURCE_ROOT / "site/assets/app.js").read_text(encoding="utf-8")
        charts = (SOURCE_ROOT / "site/assets/charts.js").read_text(encoding="utf-8")
        styles = (SOURCE_ROOT / "site/assets/styles.css").read_text(encoding="utf-8")
        methodology = (SOURCE_ROOT / "reports/methodology-review.md").read_text(encoding="utf-8")

        self.assertIn('region.classList.toggle("artifact-shell", isWideArtifact)', app)
        self.assertIn("function setArticleTableMode", app)
        self.assertIn('comparisonWidth > availableWidth + 2', app)
        self.assertIn('const summaryIndex = isDefinition ? 1 : profiledSummaryIndex > 0 ? profiledSummaryIndex : cells.length > 1 ? 1 : -1', app)
        self.assertIn('const initiallyExpanded = isDefinition || !canCollapse || bodyRows.length <= 3 && rowIndex === 0', app)
        self.assertIn('const defaultMode = "overview"', app)
        self.assertIn('makeButton("Takeaway", "summary"', app)
        self.assertIn('makeButton("Overview", "overview"', app)
        self.assertIn('hint.hidden = !hasHorizontalOverflow', app)
        self.assertIn('const hint = document.createElement("p")', app)
        self.assertNotIn('const hint = document.createElement("figcaption")', app)
        self.assertIn('"Definition rows · all fields shown"', app)
        self.assertIn('new CustomEvent("diagram-close-request",', app)
        self.assertIn('viewport.scrollLeft += event.key === "ArrowRight"', app)
        self.assertIn('const expandedDiagram = document.querySelector(".diagram-frame.is-expanded")', app)
        self.assertIn('setTimeout(() => expand.focus({ preventScroll: true }), 0)', app)
        self.assertNotIn('This is a detailed inspection model.', app)
        self.assertIn('dataset.diagramSummary', app)
        self.assertIn('function inlineDiagramContract', app)
        self.assertIn('function enhanceDocumentSections', app)
        self.assertIn('section.dataset.sectionTitle = headingTitle', app)
        self.assertIn('`${open ? "Close" : "Open"} ${section.dataset.sectionTitle} section`', app)
        self.assertIn('headings.length >= 7', app)
        self.assertIn('proseLength >= 20000', app)
        self.assertIn('open only the evidence you need', app)
        self.assertIn("const overviewScale = () => Math.min(", app)
        self.assertIn('makeButton("Readable", "readable"', app)
        self.assertIn('makeButton("Expand", "expand"', app)
        self.assertIn('target.setAttribute("aria-modal", "true")', app)
        self.assertIn('document.body.append(target)', app)
        self.assertIn('originPlaceholder.replaceWith(target)', app)
        self.assertIn('event.stopPropagation()', app)
        self.assertIn('const scrollSurface = event.target', app)
        self.assertIn('function preparePrintArtifacts', app)
        self.assertIn('document.querySelectorAll(".viz-kps-fit-contract[name]")', app)
        self.assertIn('detail.removeAttribute("name")', app)
        self.assertIn('detail.setAttribute("name", name)', app)
        self.assertIn('window.addEventListener("afterprint", restorePrintArtifacts)', app)
        self.assertIn("previewHeight / geometry.height", app)
        self.assertIn('function visualDisclosurePanel', app)
        self.assertGreaterEqual(app.count('mode: "synopsis"'), 2)
        self.assertIn('is-kong-platform-grid', app)
        self.assertIn('index < 0 || index >= slides.length', app)
        self.assertIn('That presentation slide is outside the configured story.', app)
        self.assertNotIn('index = Math.min(Math.max(index, 0), slides.length - 1)', app)

        self.assertIn('const mode = options.mode || (options.presentation ? "presentation" : "evidence")', charts)
        self.assertIn('<details class="viz-kps-fit-contract"', charts)
        self.assertIn('mode === "presentation" ? "is-fit-contract"', charts)
        self.assertNotIn('presentationEvidence(id, row.outcome, body)', charts)

        self.assertIn(".document-shell .prose > .artifact-shell", styles)
        self.assertIn(".article-table.is-reading-mode tbody td", styles)
        self.assertIn('tbody tr[data-row-expanded="false"]', styles)
        self.assertIn(".document-section-controls", styles)
        self.assertIn(".diagram-summary", styles)
        self.assertRegex(styles, r"(?s)\.diagram-toolbar\s*\{.*?flex: 0 0 auto;")
        self.assertIn(".diagram-frame.is-overview-mode .diagram-scroll svg", styles)
        self.assertIn(".diagram-frame.is-expanded", styles)
        self.assertIn(".table-scroll-hint[hidden]", styles)
        self.assertIn(".document-evidence-panel[open]", styles)
        self.assertRegex(
            styles,
            r"(?s)@media \(min-width: 761px\) and \(max-width: 1024px\).*?\.presentation-stage\.is-kong-platform \.slide-visual\s*\{\s*max-height: none;\s*overflow: visible;",
        )
        self.assertRegex(
            styles,
            r"(?s)@media print.*?\.presentation-slide\s*\{\s*position: static;\s*inset: auto;",
        )
        self.assertRegex(
            styles,
            r"(?s)@media print.*?\.presentation-stage \*.*?color: var\(--ink\) !important;.*?\.presentation-stage \.slide-main.*?background: white !important;",
        )
        self.assertRegex(
            styles,
            r"(?s)@media print.*?\.presentation-stage \.viz-donut-core,\s*\.presentation-stage \.viz-roadmap-marker,.*?background: white !important;",
        )
        self.assertIn(".visual-atlas .atlas-panel[open]", styles)
        self.assertIn(".visual-disclosure[open]", styles)
        self.assertIn(".viz-presentation-detail", styles)
        self.assertIn(".diagram-frame .diagram-scroll[hidden]", styles)
        self.assertIn(".visual-disclosure > .visual-panel-body", styles)
        self.assertIn(".viz-kps-fit.is-synopsis", styles)
        self.assertIn(".viz-kps-fit.is-presentation .is-fit-contract", styles)
        self.assertRegex(
            styles,
            r"(?s)\.presentation-stage \.viz-kps-fit\.is-presentation \.is-fit-contract \.viz-kps-copy p\s*\{.*?font-size: clamp\(1\.125rem, 1\.25vw, 1\.5rem\);",
        )
        self.assertRegex(
            styles,
            r"(?s)@media \(min-width: 761px\) and \(max-width: 1024px\).*?\.presentation-stage \.viz-kps-fit\.is-presentation \.is-fit-contract \.viz-kps-copy p\s*\{.*?font-size: 1\.125rem;",
        )
        self.assertRegex(
            styles,
            r"(?s)@media \(min-width: 761px\) and \(max-width: 1024px\).*?\.presentation-slide:has\(\.viz-kps-fit\.is-presentation\) \.slide-metric span,.*?\.slide-source\s*\{.*?font-size: 1rem;",
        )
        self.assertRegex(
            styles,
            r"(?s)@media print.*?\.viz-kps-fit-action\s*\{\s*display: none !important;",
        )
        self.assertRegex(
            styles,
            r"(?s)@media print.*?\.viz-kps-fit-contract > \.viz-kps-fit-contract-body\s*\{\s*display: grid !important;",
        )
        self.assertRegex(
            styles,
            r"(?s)@media print.*?\.viz-kps-fit-contract:not\(\[open\]\)\s*\{\s*height: auto !important;",
        )
        self.assertNotIn(".is-methodology-review .article-table", styles)
        self.assertIn('<details class="visual-panel atlas-panel', charts)
        self.assertIn('<details class="document-visual document-evidence-panel', charts)
        self.assertIn('<details class="viz-presentation-detail">', charts)

        self.assertIn("**Figure MR-1 — Evidence gates advance the decision in four bounded stages**", methodology)
        for stage in ("1 · FRAME", "2 · PROVE", "3 · FOUNDATION", "4 · E4 PILOT", "AUTHORIZED AFTER G4"):
            self.assertIn(stage, methodology)
        mermaid = methodology.split("```mermaid\n", 1)[1].split("\n```", 1)[0]
        self.assertIn('A["G2 PASS<br/>selection ADR + exit boundary<br/>authorize foundation"]', mermaid)
        self.assertIn('H2["G2 HOLD<br/>targeted proof"]', mermaid)
        self.assertIn('H3["G3 HOLD<br/>foundation remediation"]', mermaid)
        self.assertIn('H4["G4 HOLD<br/>extend pilots"]', mermaid)
        self.assertIn('X["STOP<br/>terminal"]', mermaid)
        self.assertIn('H2 -. re-enter targeted proof .-> S2', mermaid)
        self.assertIn('H3 -. re-enter foundation remediation .-> S3', mermaid)
        self.assertIn('H4 -. re-enter pilot extension .-> S4', mermaid)
        self.assertNotRegex(mermaid, r"(?m)^\s*X\s*(?:-->|-\.)")
        self.assertNotIn("HOLD / REWORK / STOP", mermaid)

    def test_poc_status_projection_uses_one_ratio_and_grouped_scenario_ids(self) -> None:
        app = (SOURCE_ROOT / "site/assets/app.js").read_text(encoding="utf-8")
        styles = (SOURCE_ROOT / "site/assets/styles.css").read_text(encoding="utf-8")
        readme = (SOURCE_ROOT / "poc/README.md").read_text(encoding="utf-8")
        build_spec = importlib.util.spec_from_file_location("build_site_poc_contract", SOURCE_ROOT / "scripts/build_site.py")
        assert build_spec and build_spec.loader
        build_site = importlib.util.module_from_spec(build_spec)
        build_spec.loader.exec_module(build_site)
        poc = build_site.poc_visuals()
        by_status = {str(item["label"]): int(item["value"]) for item in poc["byStatus"]}
        node = next(
            (
                candidate
                for candidate in (
                    Path("/usr/bin/node"),
                    Path("/bin/node"),
                    Path("/usr/local/bin/node"),
                    Path("/opt/homebrew/bin/node"),
                )
                if candidate.is_file() and os.access(candidate, os.X_OK)
            ),
            None,
        )
        self.assertIsNotNone(node, "Node.js is required to validate the reusable chart renderer")
        script = r'''
global.window = {};
require("./site/assets/charts.js");
const data = JSON.parse(require("fs").readFileSync(0, "utf8"));
const full = window.ApiStudyCharts.render("pocStatus", data, {title: "PoC scenario state"});
const compact = window.ApiStudyCharts.render("pocStatus", data, {title: "PoC scenario state", compact: true});
process.stdout.write(JSON.stringify({full, compact}));
'''
        observed = subprocess.run(
            [str(node), "-e", script],
            cwd=SOURCE_ROOT,
            check=False,
            capture_output=True,
            input=json.dumps(poc),
            text=True,
        )
        self.assertEqual(0, observed.returncode, observed.stderr)
        payload = json.loads(observed.stdout)
        full = payload["full"]
        compact = payload["compact"]

        self.assertIn('class="viz-poc-score"', full)
        self.assertIn('class="viz-poc-rail"', full)
        self.assertIn('class="viz-poc-cohorts"', full)
        self.assertNotIn("viz-donut", full)
        self.assertIn(
            f'aria-label="{by_status["Automated"]} Automated, {by_status["Not run"]} Not run"',
            full,
        )
        self.assertLess(full.index("automated baseline"), full.index("not run"))
        self.assertNotIn("Automated · 5", full)
        for scenario_id in [str(test["id"]) for test in poc["tests"]]:
            with self.subTest(scenario_id=scenario_id):
                self.assertEqual(1, full.count(scenario_id))
                self.assertNotIn(scenario_id, compact)

        self.assertIn("five have automated local-baseline evidence and 11 are not run", readme)
        self.assertIn("pocScenarioHeadline", app)
        self.assertIn('pocStatusCount("Automated")', app)
        self.assertIn('pocStatusCount("Not run")', app)
        self.assertNotIn("Five baseline checks are automated; eleven scenarios are not run", app)
        self.assertIn("Automation does not equal representative evidence", app)
        self.assertIn("aggregate status-register items", app)
        self.assertGreaterEqual(app.count("Open scenario register"), 2)
        self.assertIn('findByPath("poc/test-plan.md")', app)
        self.assertRegex(
            app,
            r'(?s)function renderLab\(\) \{.*?const pocPlan = findByPath\("poc/test-plan\.md"\);.*?Open scenario register',
        )
        self.assertNotIn("Automated, scripted, and not-run tests", app)
        self.assertIn(".viz-poc-cohorts", styles)
        self.assertIn(".presentation-stage .viz-poc-rail > .is-automated", styles)
        self.assertRegex(styles, r"(?s)@media \(max-width: 760px\).*?\.viz-poc-cohorts\s*\{\s*grid-template-columns: 1fr;")

    def test_kong_fit_projection_is_four_bounded_complete_story_frames(self) -> None:
        fit_keys = (
            "kong-platform-fit-boundary",
            "kong-platform-fit-runtime",
            "kong-platform-fit-change",
            "kong-platform-fit-fallback",
        )
        expected_row_ids = tuple(f"KPS-FIT-{index:02d}" for index in range(1, 8))

        with tempfile.TemporaryDirectory(prefix="kong-fit-projection-") as temporary:
            output = Path(temporary) / "site"
            result = subprocess.run(
                (
                    sys.executable,
                    "-I",
                    str(SOURCE_ROOT / "scripts" / "build_site.py"),
                    "--output",
                    str(output),
                ),
                cwd=SOURCE_ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            manifest = json.loads((output / "content-manifest.json").read_text(encoding="utf-8"))

        slide_by_key = {slide["key"]: slide for slide in manifest["presentation"]}
        fit_slides = [slide_by_key[key] for key in fit_keys]
        projected_row_ids = tuple(
            row_id
            for slide in fit_slides
            for row_id in slide["rowIds"]
        )

        self.assertEqual([2, 2, 2, 1], [len(slide["rowIds"]) for slide in fit_slides])
        self.assertTrue(all(len(slide["rowIds"]) <= 2 for slide in fit_slides))
        self.assertEqual(expected_row_ids, projected_row_ids)
        self.assertEqual(len(projected_row_ids), len(set(projected_row_ids)))

        canonical_rows = manifest["visuals"]["kongPlatformStrategy"]["fit"]["rows"]
        self.assertEqual(expected_row_ids, tuple(row["projectionId"] for row in canonical_rows))
        for row in canonical_rows:
            with self.subTest(row=row["projectionId"]):
                for field in ("outcome", "mechanism", "reason", "counterfactual", "proof"):
                    self.assertTrue(str(row[field]).strip(), field)

        deck = next(
            candidate
            for candidate in manifest["presentationDecks"]
            if candidate["id"] == "kong-technical-deep-dive"
        )
        self.assertEqual(list(fit_keys), deck["presentationSlides"][1:5])
        self.assertEqual(len(deck["presentationSlides"]), deck["slideTotal"])

        audience_slides = {
            audience["id"]: tuple(audience["presentationSlides"])
            for audience in manifest["audiences"]
        }
        self.assertEqual(fit_keys, audience_slides["vp-executive"][1:5])
        self.assertEqual(fit_keys[:2], audience_slides["directors"][1:3])
        self.assertEqual(fit_keys, audience_slides["platform-teams"][:4])

    def test_temporary_repositories_drop_outer_publication_provenance(self) -> None:
        original = {
            variable: os.environ.get(variable)
            for variable in OUTER_PROVENANCE_ENVIRONMENT
        }
        try:
            for variable in OUTER_PROVENANCE_ENVIRONMENT:
                os.environ[variable] = "outer-publication-value"
            repository = self.repository()
        finally:
            for variable, value in original.items():
                if value is None:
                    os.environ.pop(variable, None)
                else:
                    os.environ[variable] = value

        for variable in OUTER_PROVENANCE_ENVIRONMENT:
            self.assertNotIn(variable, repository.environment)

    def test_pages_manual_dispatch_cannot_deploy_a_feature_ref(self) -> None:
        workflow = (SOURCE_ROOT / ".github/workflows/pages.yml").read_text(encoding="utf-8")
        self.assertIn("workflow_dispatch:", workflow)
        self.assertRegex(
            workflow,
            r"(?ms)^  build:\n    if: \$\{\{ github\.ref == 'refs/heads/main' \}\}",
        )
        self.assertRegex(
            workflow,
            r"(?ms)^  deploy:\n    if: \$\{\{ github\.ref == 'refs/heads/main' && vars\.PAGES_ENABLED == 'true' \}\}",
        )
        self.assertEqual(2, len(re.findall(r"(?m)^    timeout-minutes: 20$", workflow)))

    def test_script_document_and_template_share_the_exact_13_state_model(self) -> None:
        module = load_production_module()
        workflow = (SOURCE_ROOT / "docs/46-study-publication-workflow.md").read_text(encoding="utf-8")
        state_section = workflow.split("## Workflow states and gates", 1)[1].split("**Figure SPW-2", 1)[0]
        documented = tuple(re.findall(r"^\| `([A-Z]+)` \|", state_section, re.MULTILINE))
        template = (SOURCE_ROOT / "templates/study-intake-template.md").read_text(encoding="utf-8")
        final_state_line = [
            line for line in template.splitlines() if line.startswith("- **Canonical workflow state:**")
        ][-1]

        self.assertEqual(EXPECTED_STATES, documented)
        self.assertEqual(EXPECTED_STATES, tuple(module.STATES))
        self.assertEqual(EXPECTED_STATES, tuple(re.findall(r"`([A-Z]+)`", final_state_line)))

    def test_template_has_14_sections_and_freezes_sections_1_through_9(self) -> None:
        template = (SOURCE_ROOT / "templates/study-intake-template.md").read_text(encoding="utf-8")
        sections = tuple(int(value) for value in re.findall(r"^## (\d+)\. ", template, re.MULTILINE))
        self.assertEqual(tuple(range(1, 15)), sections)
        self.assertIn("Sections 1–9 form the public-safe intake specification", template)
        self.assertIn("Sections 10–14 define the mutable operational checkpoint", template)


class CheckpointSchemaTests(WorkflowTestCase):
    def test_new_writes_the_exact_versioned_checkpoint_schema(self) -> None:
        repository = self.repository()
        checkpoint, data, result = repository.new_checkpoint()
        self.assertEqual(0, result.returncode, result.stderr)
        module = load_production_module()

        self.assertEqual(module.CHECKPOINT_KEYS, set(data))
        self.assertEqual(module.SCHEMA_VERSION, data["schemaVersion"])
        self.assertEqual("INTAKE-20300102-workflow-test", data["intakeId"])
        self.assertEqual("INTAKE", data["canonicalState"])
        self.assertEqual("study/workflow-test", data["branch"])
        self.assertEqual(repository.base_sha, data["baseSha"])
        self.assertEqual("pending", data["localValidation"])
        self.assertIsNone(data["localValidationDigest"])
        self.assertEqual(
            [
                "research",
                "edit",
                "branch",
                "commit",
                "push",
                "pull-request",
                "merge",
                "branch-cleanup",
                "pages-verification",
            ],
            data["requestedActions"],
        )
        self.assertRegex(data["checkpointCreatedAt"], r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
        self.assertTrue(checkpoint.is_file())

    def test_load_rejects_missing_extra_and_invalid_core_schema_fields(self) -> None:
        repository = self.repository()
        checkpoint, original, result = repository.new_checkpoint()
        self.assertEqual(0, result.returncode, result.stderr)
        cases: dict[str, dict[str, Any]] = {}

        missing = dict(original)
        missing.pop("title")
        cases["missing field"] = missing
        extra = dict(original)
        extra["unexpected"] = "value"
        cases["extra field"] = extra
        version = dict(original)
        version["schemaVersion"] = 99
        cases["schema version"] = version
        state = dict(original)
        state["canonicalState"] = "DONE"
        cases["unknown state"] = state
        sha = dict(original)
        sha["baseSha"] = repository.base_sha.upper()
        cases["noncanonical SHA"] = sha
        number = dict(original)
        number["prNumber"] = True
        cases["boolean PR number"] = number

        failures: list[str] = []
        for label, candidate in cases.items():
            with self.subTest(label=label):
                repository.replace_checkpoint(checkpoint, candidate)
                observed = repository.cli("render", "--checkpoint", str(checkpoint))
                if observed.returncode != 2 or "Traceback" in observed.stderr:
                    failures.append(f"{label}: rc={observed.returncode}, stderr={observed.stderr.strip()!r}")
        self.assertEqual([], failures)

    def test_schema_rejects_untyped_or_unsafe_operational_fields(self) -> None:
        repository = self.repository()
        checkpoint, original, result = repository.new_checkpoint()
        self.assertEqual(0, result.returncode, result.stderr)
        private_key_marker = "-----BEGIN " + "PRIVATE KEY-----"
        cases = {
            "statusReason": "unsafe\nsecond record",
            "checkpointCreatedAt": "not-a-timestamp",
            "updatedAt": [],
            "derivedPaths": ["../../outside.json"],
            "checkUrls": ["http://private.invalid/check/1"],
            "manifestAssertions": ["safe assertion\nInjected assertion"],
            "residualLimitations": [private_key_marker],
            "mainValidationUrl": "http://private.invalid/main",
            "pagesRunUrl": 7,
            "closureEvidenceUrl": "http://private.invalid/closure",
            "liveBaseUrl": "https://user:" + "password@example.invalid/",
            "localValidationDigest": "not-a-sha256-digest",
        }

        accepted: list[str] = []
        for field, invalid in cases.items():
            with self.subTest(field=field):
                candidate = dict(original)
                candidate[field] = invalid
                repository.replace_checkpoint(checkpoint, candidate)
                observed = repository.cli("render", "--checkpoint", str(checkpoint))
                if observed.returncode == 0:
                    accepted.append(field)
                elif "Traceback (most recent call last)" in observed.stderr:
                    accepted.append(f"{field} (uncaught exception)")
        self.assertEqual([], accepted, f"schema accepted unsafe/ill-typed fields: {accepted}")


class CheckpointMutationTests(WorkflowTestCase):
    def test_requested_actions_replacement_requires_reason_and_current_input(self) -> None:
        repository = self.repository()
        checkpoint, original, result = repository.new_checkpoint()
        self.assertEqual(0, result.returncode, result.stderr)
        revised_actions = "research,branch"
        current_input = "https://example.com/tasks/revised-authority"
        reason = "Current authority narrows the remaining publication actions."
        missing_evidence_cases = (
            ("missing reason", ("--input-reference", current_input)),
            ("missing current input", ("--status-reason", reason)),
        )

        for label, extra_arguments in missing_evidence_cases:
            with self.subTest(case=label):
                repository.replace_checkpoint(checkpoint, original)
                observed = repository.cli(
                    "record",
                    "--checkpoint",
                    str(checkpoint),
                    "--requested-actions",
                    revised_actions,
                    *extra_arguments,
                )
                self.assert_deterministic_error(
                    observed,
                    contains="changing requested actions requires --status-reason and a current --input-reference",
                )
                self.assertEqual(
                    original,
                    json.loads(checkpoint.read_text(encoding="utf-8")),
                )

        replaced = repository.cli(
            "record",
            "--checkpoint",
            str(checkpoint),
            "--requested-actions",
            revised_actions,
            "--status-reason",
            reason,
            "--input-reference",
            current_input,
        )
        self.assertEqual(0, replaced.returncode, replaced.stdout + replaced.stderr)
        updated = json.loads(checkpoint.read_text(encoding="utf-8"))
        self.assertEqual(["research", "branch"], updated["requestedActions"])
        self.assertEqual(reason, updated["statusReason"])
        self.assertEqual([*original["inputReferences"], current_input], updated["inputReferences"])

    def test_replace_list_corrects_early_evidence_but_locks_candidate_content(self) -> None:
        repository = self.repository()
        checkpoint, projected, head = repository.prepare_draft()
        corrected_reference = "https://example.com/evidence/corrected-workflow-contract"
        correction_reason = "Replace the superseded evidence reference before candidacy."
        corrected = repository.cli(
            "replace-list",
            "--checkpoint",
            str(checkpoint),
            "--field",
            "evidenceReferences",
            "--value",
            corrected_reference,
            "--value",
            corrected_reference,
            "--status-reason",
            correction_reason,
        )
        self.assertEqual(0, corrected.returncode, corrected.stdout + corrected.stderr)
        corrected_data = json.loads(checkpoint.read_text(encoding="utf-8"))
        self.assertEqual([corrected_reference], corrected_data["evidenceReferences"])
        self.assertNotIn(projected["evidenceReferences"][0], corrected_data["evidenceReferences"])
        self.assertEqual(correction_reason, corrected_data["statusReason"])

        corrected_data.update(
            {
                "canonicalState": "CANDIDATE",
                "candidateSha": head,
                "prNumber": 17,
                "prUrl": "https://github.com/owner/repo/pull/17",
                "prHeadSha": head,
                "prDraft": True,
            }
        )
        corrected_data["candidateEnvelopeSha256"] = repository.load_module(
            "scripts/study_workflow.py"
        ).candidate_envelope_digest(corrected_data)
        repository.replace_checkpoint(checkpoint, corrected_data)
        locked = repository.cli(
            "replace-list",
            "--checkpoint",
            str(checkpoint),
            "--field",
            "evidenceReferences",
            "--value",
            "https://example.com/evidence/post-candidate-rewrite",
            "--status-reason",
            "Attempt an impermissible post-candidate content rewrite.",
        )
        self.assert_deterministic_error(
            locked,
            contains="replace evidenceReferences only before CANDIDATE or after returning to REWORK/BLOCKED",
        )
        self.assertEqual(
            corrected_data,
            json.loads(checkpoint.read_text(encoding="utf-8")),
        )

    def test_candidate_record_locks_content_lists_except_audited_authority_input(self) -> None:
        repository = self.repository()
        checkpoint, candidate, _ = repository.prepare_candidate()
        locked_appends = (
            ("audiences", "--audience", "additional audience"),
            (
                "evidenceReferences",
                "--evidence-reference",
                "https://example.com/evidence/post-candidate",
            ),
            ("canonicalPaths", "--canonical-path", "docs/post-candidate.md"),
            ("derivedPaths", "--derived-path", "site/post-candidate.json"),
            (
                "inputReferences",
                "--input-reference",
                "https://example.com/tasks/post-candidate",
            ),
        )
        for field, flag, value in locked_appends:
            with self.subTest(field=field):
                repository.replace_checkpoint(checkpoint, candidate)
                observed = repository.cli(
                    "record", "--checkpoint", str(checkpoint), flag, value
                )
                self.assert_deterministic_error(
                    observed,
                    contains=f"append {field} only before CANDIDATE or after returning to REWORK/BLOCKED",
                )
                self.assertEqual(
                    candidate,
                    json.loads(checkpoint.read_text(encoding="utf-8")),
                )

        authority_input = "https://example.com/tasks/revised-candidate-authority"
        authority_reason = "Current instruction narrows candidate publication authority."
        revised_actions = "research,edit,branch,commit,push,pull-request"
        audited = repository.cli(
            "record",
            "--checkpoint",
            str(checkpoint),
            "--requested-actions",
            revised_actions,
            "--status-reason",
            authority_reason,
            "--input-reference",
            authority_input,
        )
        self.assertEqual(0, audited.returncode, audited.stdout + audited.stderr)
        updated = json.loads(checkpoint.read_text(encoding="utf-8"))
        self.assertEqual(revised_actions.split(","), updated["requestedActions"])
        self.assertEqual(authority_reason, updated["statusReason"])
        self.assertEqual(
            [*candidate["inputReferences"], authority_input],
            updated["inputReferences"],
        )


class CheckpointRecoveryTests(WorkflowTestCase):
    def test_checkpoint_markers_must_be_ordered(self) -> None:
        repository = self.repository()
        module = repository.load_module("scripts/study_workflow.py")
        malformed = f"{module.CHECKPOINT_END}\ntext\n{module.CHECKPOINT_START}"
        with self.assertRaisesRegex(module.WorkflowError, "markers are out of order"):
            module.embedded_checkpoint(malformed)

    def test_pr_machine_payload_round_trips_and_resumes_a_missing_open_checkpoint(self) -> None:
        repository = self.repository()
        checkpoint, durable, head = repository.prepare_candidate()
        repository.git("push", "-q", "-u", "origin", durable["branch"])
        durable["repositoryRemote"] = "https://github.com/owner/repo.git"
        durable["candidateEnvelopeSha256"] = repository.load_module(
            "scripts/study_workflow.py"
        ).candidate_envelope_digest(durable)
        repository.replace_checkpoint(checkpoint, durable)
        repository.git("remote", "set-url", "origin", "git@github.com:owner/repo.git")
        transport = repository.install_fake_ssh_transport()
        rendered = repository.cli("render", "--checkpoint", str(checkpoint))
        self.assertEqual(0, rendered.returncode, rendered.stdout + rendered.stderr)
        self.assertIn("study-workflow-checkpoint-json:", rendered.stdout)

        module = repository.load_module("scripts/study_workflow.py")
        self.assertEqual(durable, module.embedded_checkpoint(rendered.stdout))
        pr = repository.valid_pr_json(head)
        pr.update(
            {
                "body": rendered.stdout.strip(),
                "isDraft": True,
                "state": "OPEN",
            }
        )

        checkpoint.unlink()
        repository.git("switch", "-q", "main")
        repository.git("branch", "-D", durable["branch"])
        self.assertFalse(checkpoint.exists())
        self.assertEqual("", repository.git("status", "--porcelain").stdout)

        wrong_data = dict(durable)
        wrong_data["repositoryRemote"] = "https://github.com/other/repo.git"
        wrong_data["candidateEnvelopeSha256"] = module.candidate_envelope_digest(wrong_data)
        wrong_pr = dict(pr)
        wrong_pr["body"] = module.rendered_checkpoint(wrong_data)
        different_repository = repository.cli(
            "resume",
            "--pr-number",
            "17",
            "--base",
            repository.base_sha,
            "--requested-actions",
            ",".join(durable["requestedActions"]),
            environment={"FAKE_PR_JSON": json.dumps(wrong_pr), **transport},
        )
        self.assert_deterministic_error(
            different_repository,
            contains="durable checkpoint remote differs from origin",
        )
        self.assertEqual("main", repository.git("branch", "--show-current").stdout.strip())
        self.assertFalse(checkpoint.exists())

        resumed = repository.cli(
            "resume",
            "--pr-number",
            "17",
            "--base",
            repository.base_sha,
            "--requested-actions",
            ",".join(durable["requestedActions"]),
            environment={"FAKE_PR_JSON": json.dumps(pr), **transport},
        )
        self.assertEqual(0, resumed.returncode, resumed.stdout + resumed.stderr)
        result = json.loads(resumed.stdout)
        restored = repository.root / result["checkpoint"]
        self.assertEqual(checkpoint.resolve(), restored.resolve())
        self.assertEqual(durable, json.loads(restored.read_text(encoding="utf-8")))
        self.assertEqual(durable["branch"], result["branch"])
        self.assertEqual(durable["branch"], repository.git("branch", "--show-current").stdout.strip())
        self.assertEqual(head, repository.git("rev-parse", "HEAD").stdout.strip())

    def test_resume_existing_checkpoint_fails_before_switching_branches(self) -> None:
        repository = self.repository()
        checkpoint, durable, head = repository.prepare_candidate()
        repository.git("push", "-q", "-u", "origin", durable["branch"])
        rendered = repository.cli("render", "--checkpoint", str(checkpoint))
        self.assertEqual(0, rendered.returncode, rendered.stdout + rendered.stderr)
        pr = repository.valid_pr_json(head)
        pr.update({"body": rendered.stdout.strip(), "isDraft": True, "state": "OPEN"})
        repository.git("switch", "-q", "main")
        before = checkpoint.read_bytes()

        resumed = repository.cli(
            "resume",
            "--pr-number",
            "17",
            "--base",
            repository.base_sha,
            "--requested-actions",
            ",".join(durable["requestedActions"]),
            environment={"FAKE_PR_JSON": json.dumps(pr)},
        )
        self.assert_deterministic_error(resumed, contains="checkpoint already exists")
        self.assertEqual("main", repository.git("branch", "--show-current").stdout.strip())
        self.assertEqual(before, checkpoint.read_bytes())

    def test_resume_rejects_malformed_late_field_before_git_mutation(self) -> None:
        repository = self.repository()
        checkpoint, durable, candidate = repository.prepare_candidate()
        repository.git("push", "-q", "-u", "origin", durable["branch"])
        malformed = dict(durable)
        malformed["manifestSha256"] = "not-a-sha256-digest"
        module = repository.load_module("scripts/study_workflow.py")
        pr = repository.valid_pr_json(candidate)
        pr.update(
            {
                "body": module.rendered_checkpoint(malformed),
                "isDraft": True,
                "state": "OPEN",
            }
        )
        checkpoint.unlink()
        repository.git("switch", "-q", "main")
        original_head = repository.git("rev-parse", "HEAD").stdout.strip()

        resumed = repository.cli(
            "resume",
            "--pr-number",
            "17",
            "--base",
            repository.base_sha,
            "--requested-actions",
            ",".join(durable["requestedActions"]),
            environment={"FAKE_PR_JSON": json.dumps(pr)},
        )
        self.assert_deterministic_error(
            resumed,
            contains="manifestSha256 is invalid",
        )
        self.assertEqual("main", repository.git("branch", "--show-current").stdout.strip())
        self.assertEqual(original_head, repository.git("rev-parse", "HEAD").stdout.strip())
        self.assertFalse(checkpoint.exists())

    def test_merged_resume_promotes_validated_payload_and_rejects_merged_mismatch(self) -> None:
        repository = self.repository()
        checkpoint, durable, candidate = repository.prepare_release()
        self.assertEqual("VALIDATED", durable["canonicalState"])
        self.assertTrue(
            {"merge", "branch-cleanup"}.issubset(durable["requestedActions"])
        )
        repository.git("push", "-q", "origin", f"{candidate}:refs/heads/main")
        rendered = repository.cli("render", "--checkpoint", str(checkpoint))
        self.assertEqual(0, rendered.returncode, rendered.stdout + rendered.stderr)
        pr = repository.valid_pr_json(candidate, merged=True, merge_sha=candidate)
        pr["body"] = rendered.stdout.strip()

        module = repository.load_module("scripts/study_workflow.py")
        mismatched = dict(durable)
        mismatched.update(
            {
                "canonicalState": "MERGED",
                "statusReason": "Durable merged fixture with a stale merge SHA.",
                "mergeSha": repository.base_sha,
                "branchCleanupStatus": "complete",
                "cleanupEvidence": [
                    "verified: local intake branch absent",
                    "verified: remote intake branch absent",
                ],
                "nextGate": "Reconcile the durable merge record.",
            }
        )
        module.validate_checkpoint_shape(mismatched)
        mismatch_pr = dict(pr)
        mismatch_pr["body"] = module.rendered_checkpoint(mismatched)

        checkpoint.unlink()
        repository.git("switch", "-q", "main")
        repository.git("branch", "-D", durable["branch"])
        repository.git("push", "-q", "origin", "--delete", durable["branch"])
        self.assertFalse(checkpoint.exists())
        self.assertNotEqual(
            0,
            repository._run(
                ("git", "show-ref", "--verify", f"refs/heads/{durable['branch']}")
            ).returncode,
        )
        self.assertEqual(
            "",
            repository.git("ls-remote", "--heads", "origin", durable["branch"]).stdout,
        )

        mismatch = repository.cli(
            "resume",
            "--pr-number",
            "17",
            "--base",
            repository.base_sha,
            "--requested-actions",
            ",".join(durable["requestedActions"]),
            environment=repository.fake_github_environment(mismatch_pr, candidate),
        )
        self.assert_deterministic_error(
            mismatch,
            contains="durable merged state differs from the actual PR merge/cleanup state",
        )
        self.assertFalse(checkpoint.exists())
        self.assertEqual("main", repository.git("branch", "--show-current").stdout.strip())

        resumed = repository.cli(
            "resume",
            "--pr-number",
            "17",
            "--base",
            repository.base_sha,
            "--requested-actions",
            ",".join(durable["requestedActions"]),
            environment=repository.fake_github_environment(pr, candidate),
        )
        self.assertEqual(0, resumed.returncode, resumed.stdout + resumed.stderr)
        result = json.loads(resumed.stdout)
        restored = repository.root / result["checkpoint"]
        restored_data = json.loads(restored.read_text(encoding="utf-8"))
        self.assertEqual("MERGED", result["state"])
        self.assertEqual("MERGED", restored_data["canonicalState"])
        self.assertEqual(candidate, restored_data["mergeSha"])
        self.assertEqual("complete", restored_data["branchCleanupStatus"])
        self.assertEqual(
            [
                "verified: local intake branch absent",
                "verified: remote intake branch absent",
            ],
            restored_data["cleanupEvidence"],
        )
        self.assertEqual("main", repository.git("branch", "--show-current").stdout.strip())
        self.assertEqual(candidate, repository.git("rev-parse", "HEAD").stdout.strip())
        validated = repository.cli("render", "--checkpoint", str(restored))
        self.assertEqual(0, validated.returncode, validated.stdout + validated.stderr)

    def test_merged_resume_rejects_local_main_ahead_or_diverged_from_origin(self) -> None:
        for mode in ("ahead", "diverged"):
            with self.subTest(mode=mode):
                repository = self.repository()
                checkpoint, durable, candidate = repository.prepare_release()
                repository.git("push", "-q", "origin", f"{candidate}:refs/heads/main")
                rendered = repository.cli("render", "--checkpoint", str(checkpoint))
                self.assertEqual(0, rendered.returncode, rendered.stdout + rendered.stderr)
                pr = repository.valid_pr_json(
                    candidate, merged=True, merge_sha=candidate
                )
                pr["body"] = rendered.stdout.strip()
                checkpoint.unlink()
                repository.git("switch", "-q", "main")
                repository.git("branch", "-D", durable["branch"])
                repository.git("push", "-q", "origin", "--delete", durable["branch"])
                if mode == "ahead":
                    repository.git("fetch", "-q", "origin", "main")
                    repository.git("merge", "-q", "--ff-only", "origin/main")
                repository.git(
                    "commit",
                    "--allow-empty",
                    "-q",
                    "-m",
                    f"Create local main {mode} fixture",
                )
                local_head = repository.git("rev-parse", "HEAD").stdout.strip()

                resumed = repository.cli(
                    "resume",
                    "--pr-number",
                    "17",
                    "--base",
                    repository.base_sha,
                    "--requested-actions",
                    ",".join(durable["requestedActions"]),
                    environment=repository.fake_github_environment(pr, candidate),
                )
                output = resumed.stdout + resumed.stderr
                self.assertEqual(2, resumed.returncode, output)
                self.assertNotIn("Traceback (most recent call last)", output)
                if mode == "ahead":
                    self.assertIn("local main must exactly equal origin/main", output)
                else:
                    self.assertIn("fast-forward", output.lower())
                self.assertEqual(
                    "main", repository.git("branch", "--show-current").stdout.strip()
                )
                self.assertEqual(local_head, repository.git("rev-parse", "HEAD").stdout.strip())
                self.assertFalse(checkpoint.exists())


class NewIntakeSynchronizationTests(WorkflowTestCase):
    def test_github_ref_lookup_fails_closed_on_api_errors_but_accepts_authenticated_absence(self) -> None:
        repository = self.repository()
        module = repository.load_module("scripts/study_workflow.py")
        failed = SimpleNamespace(returncode=1, stdout="", stderr="forbidden")
        with mock.patch.object(module, "github_owner_repo", return_value="owner/repo"), mock.patch.object(module, "run", return_value=failed):
            with self.assertRaisesRegex(module.WorkflowError, "unable to authenticate GitHub repository refs"):
                module.github_ref_sha("heads/study/workflow-test", required=False)
        absent = SimpleNamespace(returncode=0, stdout="[]", stderr="")
        with mock.patch.object(module, "github_owner_repo", return_value="owner/repo"), mock.patch.object(module, "run", return_value=absent):
            self.assertIsNone(module.github_ref_sha("heads/study/workflow-test", required=False))

    def test_new_rejects_an_intake_already_present_in_pr_history(self) -> None:
        repository = self.repository()
        repository.install_fake_release_tools()
        repository.git("remote", "set-url", "origin", "git@github.com:owner/repo.git")
        checkpoint, _, observed = repository.new_checkpoint(
            slug="durable-intake",
            environment={
                "FAKE_PR_LIST_JSON": json.dumps(
                    [
                        {
                            "number": 42,
                            "state": "MERGED",
                            "url": "https://github.com/owner/repo/pull/42",
                            "headRefName": "study/durable-intake",
                        }
                    ]
                )
            },
        )
        self.assertEqual(Path(), checkpoint)
        self.assert_deterministic_error(
            observed,
            contains="intake ID already exists in pull-request history",
        )
        self.assertEqual("main", repository.git("branch", "--show-current").stdout.strip())
        self.assertNotEqual(
            0,
            repository._run(
                ("git", "show-ref", "--verify", "refs/heads/study/durable-intake")
            ).returncode,
        )

    def test_new_rejects_credential_remote_without_persisting_or_echoing_it(self) -> None:
        repository = self.repository()
        cases = (
            ("basic-auth", "https://alice:" + "plainpassword-for-regression@github.com/owner/repo.git", "plainpassword-for-regression"),
            ("query", "https://github.com/owner/repo.git?credential=query-secret", "query-secret"),
            ("userinfo-canonical", "github.com/alice:canonical-secret@owner/repo", "canonical-secret"),
        )
        for slug, remote, secret in cases:
            with self.subTest(case=slug):
                repository.git("remote", "set-url", "origin", remote)
                checkpoint, _, observed = repository.new_checkpoint(
                    slug=f"credential-{slug}",
                    write_spec=True,
                )
                self.assertEqual(Path(), checkpoint)
                self.assert_deterministic_error(
                    observed,
                    contains="origin remote must be a credential-free GitHub repository identity",
                )
                combined = observed.stdout + observed.stderr
                self.assertNotIn(secret, combined)
                self.assertEqual("main", repository.git("branch", "--show-current").stdout.strip())
                intake = f"intake-20300102-credential-{slug}"
                self.assertFalse(
                    (repository.root / ".study-workflow" / "checkpoints" / f"{intake}.json").exists()
                )
                self.assertFalse(
                    (repository.root / "workflow" / "intakes" / f"{intake}.md").exists()
                )

    def test_new_write_spec_without_edit_authority_fails_before_branch_mutation(self) -> None:
        repository = self.repository()
        original_branch = repository.git("branch", "--show-current").stdout.strip()
        original_head = repository.git("rev-parse", "HEAD").stdout.strip()

        observed = repository.cli(
            "new",
            "--slug",
            "unauthorized-spec",
            "--title",
            "Unauthorized specification fixture",
            "--source-kind",
            "chat",
            "--requested-actions",
            "research,branch",
            "--request-summary",
            "Exercise the immutable-spec authority boundary.",
            "--input-reference",
            "https://example.com/tasks/unauthorized-spec",
            "--decision-question",
            "Can a specification be written without edit authority?",
            "--date",
            "20300102",
            "--write-spec",
        )

        self.assert_deterministic_error(
            observed,
            contains="--write-spec requires explicit edit authority",
        )
        self.assertEqual(original_branch, repository.git("branch", "--show-current").stdout.strip())
        self.assertEqual(original_head, repository.git("rev-parse", "HEAD").stdout.strip())
        self.assertNotEqual(
            0,
            repository._run(
                ("git", "show-ref", "--verify", "refs/heads/study/unauthorized-spec")
            ).returncode,
        )
        self.assertFalse(
            (repository.root / ".study-workflow/intake-20300102-unauthorized-spec.json").exists()
        )
        self.assertFalse(
            (repository.root / "workflow/intakes/intake-20300102-unauthorized-spec.md").exists()
        )

    def test_new_rejects_local_main_ahead_of_origin(self) -> None:
        repository = self.repository()
        repository.write_text("docs/local-ahead.md", "# Local-only main commit\n")
        local_head = repository.commit_all("Advance local main only")

        _, _, observed = repository.new_checkpoint(slug="ahead-main")
        self.assert_deterministic_error(
            observed,
            contains="local main must exactly equal origin/main before intake creation",
        )
        self.assertEqual("main", repository.git("branch", "--show-current").stdout.strip())
        self.assertEqual(local_head, repository.git("rev-parse", "HEAD").stdout.strip())
        branch = repository._run(
            ("git", "show-ref", "--verify", "refs/heads/study/ahead-main")
        )
        self.assertNotEqual(0, branch.returncode, branch.stdout + branch.stderr)

    def test_new_rejects_diverged_local_and_origin_main(self) -> None:
        repository = self.repository()
        repository.write_text("docs/local-divergence.md", "# Local divergence\n")
        local_head = repository.commit_all("Advance local side of divergence")

        peer = repository.container / "peer"
        clone = repository._run(
            (
                "git",
                "clone",
                "-q",
                "--branch",
                "main",
                str(repository.origin),
                str(peer),
            ),
            cwd=repository.container,
        )
        self.assertEqual(0, clone.returncode, clone.stdout + clone.stderr)

        peer_environment = {
            "GIT_AUTHOR_DATE": "2030-01-03T03:04:05Z",
            "GIT_COMMITTER_DATE": "2030-01-03T03:04:05Z",
        }

        def peer_git(*arguments: str) -> subprocess.CompletedProcess[str]:
            result = repository._run(
                ("git", *arguments), cwd=peer, environment=peer_environment
            )
            self.assertEqual(
                0,
                result.returncode,
                f"peer git {' '.join(arguments)} failed\n{result.stdout}{result.stderr}",
            )
            return result

        peer_git("config", "user.name", "Workflow Peer")
        peer_git("config", "user.email", "workflow-peer@example.invalid")
        (peer / "docs" / "origin-divergence.md").write_text(
            "# Origin divergence\n", encoding="utf-8"
        )
        peer_git("add", "docs/origin-divergence.md")
        peer_git("commit", "-q", "-m", "Advance origin side of divergence")
        peer_git("push", "-q", "origin", "main")

        _, _, observed = repository.new_checkpoint(slug="diverged-main")
        output = observed.stdout + observed.stderr
        self.assertEqual(2, observed.returncode, output)
        self.assertIn("fast-forward", output.lower())
        self.assertNotIn("Traceback (most recent call last)", output)
        self.assertEqual("main", repository.git("branch", "--show-current").stdout.strip())
        self.assertEqual(local_head, repository.git("rev-parse", "HEAD").stdout.strip())


class InputAndControlInjectionTests(WorkflowTestCase):
    def test_new_rejects_credential_urls_and_local_linux_paths_without_echoing_values(self) -> None:
        cases = (
            (
                "credential-url",
                "https://alice:" + "plainpassword@example.com/private",
                "PS025",
                "plainpassword",
            ),
            (
                "token-userinfo-url",
                "https://" + "opaque-userinfo" + "@example.com/private",
                "PS025",
                "opaque-userinfo",
            ),
            (
                "empty-user-password-url",
                "https://" + ":private-password" + "@example.com/private",
                "PS025",
                "private-password",
            ),
            (
                "linux-path",
                "/" + "home/alice/projects/private/file.txt",
                "PS026",
                "/home/alice",
            ),
        )
        for slug, reference, rule, private_value in cases:
            with self.subTest(case=slug):
                repository = self.repository()
                result = repository.cli(
                    "new",
                    "--slug",
                    slug,
                    "--title",
                    "Public safety fixture",
                    "--source-kind",
                    "chat",
                    "--requested-actions",
                    "research,branch",
                    "--request-summary",
                    "Validate checkpoint public-safety handling.",
                    "--input-reference",
                    reference,
                    "--decision-question",
                    "Does the intake reject private values before persistence?",
                )
                self.assert_deterministic_error(result, contains=rule)
                combined = result.stdout + result.stderr
                self.assertNotIn(private_value, combined)
                self.assertFalse((repository.root / ".study-workflow").exists())

    def test_new_rejects_newline_field_injection_before_writing_records(self) -> None:
        repository = self.repository()
        result = repository.cli(
            "new",
            "--slug",
            "injection-test",
            "--title",
            "Safe title\n## Injected section",
            "--source-kind",
            "chat",
            "--requested-actions",
            "research,branch",
            "--request-summary",
            "Safe request.",
            "--decision-question",
            "Does the workflow reject injected controls?",
        )
        self.assert_deterministic_error(result, contains="title contains a control/format character")
        self.assertFalse((repository.root / ".study-workflow").exists())
        self.assertFalse((repository.root / "workflow").exists())

    def test_new_rejects_nonprinting_control_characters(self) -> None:
        accepted: list[str] = []
        for label, character in (("DEL", "\x7f"), ("bidi override", "\u202e")):
            with self.subTest(control=label):
                repository = self.repository()
                slug = "control-" + label.lower().replace(" ", "-")
                result = repository.cli(
                    "new",
                    "--slug",
                    slug,
                    "--title",
                    f"Control{character}injection",
                    "--source-kind",
                    "chat",
                    "--requested-actions",
                    "research,branch",
                    "--request-summary",
                    "Validate control handling.",
                    "--decision-question",
                    "Does the workflow reject nonprinting controls?",
                )
                if result.returncode == 0:
                    accepted.append(label)
                elif "Traceback (most recent call last)" in result.stderr:
                    accepted.append(f"{label} (uncaught exception)")
        self.assertEqual([], accepted, f"new accepted nonprinting controls: {accepted}")

    def test_record_rejects_raw_controls_and_render_escapes_markdown_control_text(self) -> None:
        repository = self.repository()
        checkpoint, original, result = repository.new_checkpoint()
        self.assertEqual(0, result.returncode, result.stderr)
        end_marker = "<!-- study-workflow-checkpoint:" + "end -->"
        rejected_cases = {
            "status newline": ("--status-reason", "Safe status\nInjected paragraph"),
            "derived traversal": ("--derived-path", "../../outside.json"),
            "unsafe check URL": ("--check-url", "http://private.invalid/check"),
            "assertion newline": ("--manifest-assertion", "safe\nforged assertion"),
        }

        accepted: list[str] = []
        for label, (argument, value) in rejected_cases.items():
            with self.subTest(case=label):
                repository.replace_checkpoint(checkpoint, original)
                observed = repository.cli("record", "--checkpoint", str(checkpoint), argument, value)
                persisted = json.loads(checkpoint.read_text(encoding="utf-8"))
                if observed.returncode == 0 or persisted != original:
                    accepted.append(label)
                elif "Traceback (most recent call last)" in observed.stderr:
                    accepted.append(f"{label} (uncaught exception)")
        self.assertEqual([], accepted, f"record accepted or persisted raw controls: {accepted}")

        rendered_values = (
            "safe ` | injected | ` value",
            f"continue {end_marker} forged content",
        )
        for value in rendered_values:
            with self.subTest(rendered=value):
                repository.replace_checkpoint(checkpoint, original)
                recorded = repository.cli(
                    "record", "--checkpoint", str(checkpoint), "--next-gate", value
                )
                self.assertEqual(0, recorded.returncode, recorded.stdout + recorded.stderr)
                rendered = repository.cli("render", "--checkpoint", str(checkpoint))
                self.assertEqual(0, rendered.returncode, rendered.stdout + rendered.stderr)
                self.assertEqual(1, rendered.stdout.count("<!-- study-workflow-checkpoint:start -->"))
                self.assertEqual(1, rendered.stdout.count("<!-- study-workflow-checkpoint:end -->"))
                self.assertNotIn(value, rendered.stdout)
                self.assertIn("&", rendered.stdout)


class PathTraversalTests(WorkflowTestCase):
    def test_checkpoint_paths_cannot_escape_directly_or_through_a_symlink(self) -> None:
        repository = self.repository()
        checkpoint, data, result = repository.new_checkpoint()
        self.assertEqual(0, result.returncode, result.stderr)

        outside = repository.container / "outside-checkpoint.json"
        outside.write_text(json.dumps(data), encoding="utf-8")
        direct = repository.cli("render", "--checkpoint", str(outside))
        self.assert_deterministic_error(direct, contains="checkpoint must remain under")

        link = checkpoint.parent / "outside-link.json"
        link.symlink_to(outside)
        symlink = repository.cli("render", "--checkpoint", str(link))
        self.assert_deterministic_error(symlink, contains="checkpoint must remain under")

    def test_canonical_paths_reject_parent_absolute_backslash_and_symlink_escapes(self) -> None:
        repository = self.repository()
        checkpoint, original, result = repository.new_checkpoint()
        self.assertEqual(0, result.returncode, result.stderr)
        outside = repository.container / "outside-study.md"
        outside.write_text("# Outside\n", encoding="utf-8")
        link = repository.root / "docs" / "outside-link.md"
        link.symlink_to(outside)
        candidates = (
            "docs/../outside.md",
            str(outside),
            "docs\\outside.md",
            "docs/outside-link.md",
        )

        failures: list[str] = []
        for candidate in candidates:
            with self.subTest(path=candidate):
                repository.replace_checkpoint(checkpoint, original)
                observed = repository.cli(
                    "record", "--checkpoint", str(checkpoint), "--canonical-path", candidate
                )
                if observed.returncode != 2 or json.loads(checkpoint.read_text(encoding="utf-8")) != original:
                    failures.append(candidate)
        self.assertEqual([], failures)

    def test_derived_paths_obey_the_same_repository_relative_boundary(self) -> None:
        repository = self.repository()
        checkpoint, original, result = repository.new_checkpoint()
        self.assertEqual(0, result.returncode, result.stderr)
        outside = repository.container / "outside-derived.json"
        outside.write_text("{}\n", encoding="utf-8")
        link = repository.root / "site-link.json"
        link.symlink_to(outside)
        candidates = ("../../outside.json", str(outside), "site-link.json", "site\\projection.json")

        accepted: list[str] = []
        for candidate in candidates:
            with self.subTest(path=candidate):
                repository.replace_checkpoint(checkpoint, original)
                observed = repository.cli(
                    "record", "--checkpoint", str(checkpoint), "--derived-path", candidate
                )
                if observed.returncode == 0 or json.loads(checkpoint.read_text(encoding="utf-8")) != original:
                    accepted.append(candidate)
        self.assertEqual([], accepted, f"derived paths escaped the repository boundary: {accepted}")


class PublicContentScannerTests(WorkflowTestCase):
    def test_history_mode_lookup_treats_glob_like_names_literally(self) -> None:
        repository = self.repository()
        base = repository.base_sha
        repository.write_text(
            "docs/glob-safe.md",
            "# Safe matching path\n\nThis regular file must not mask a historical symlink.\n",
        )
        symlink = repository.root / "docs" / "glob-*.md"
        symlink.symlink_to("glob-safe.md")
        repository.commit_all("Add a glob-like historical symlink fixture")
        symlink.unlink()
        repository.commit_all("Delete the glob-like historical symlink fixture")

        module = repository.load_module("scripts/study_workflow.py")
        errors = module.public_content_errors(base, "HEAD", include_generated=False)
        self.assertTrue(any("PS022" in error for error in errors), errors)

    def test_scans_extensionless_env_key_svg_large_and_generated_text_without_echoing_values(self) -> None:
        repository = self.repository()
        github_token = "gh" + "p_" + "A" * 24
        aws_key = "AK" + "IA" + "B" * 16
        private_key_marker = "-----BEGIN " + "PRIVATE KEY-----"
        slack_token = "xo" + "xb-" + "C" * 24
        bearer_value = "D" * 32
        local_path = "/Us" + "ers/tester/private/input.txt"
        macos_attachment = "/" + "var" + "/folders/ab/session/input.txt"
        internal_host = "db.prod." + "internal:5432"
        private_address = "10" + ".23.4.5"
        root_home = "/root" + "/work/private.txt"

        repository.write_text("NOTICE", f"temporary credential {github_token}\n")
        repository.write_text(".env", f"ACCESS_KEY={aws_key}\n")
        repository.write_text("keys/release.key", private_key_marker + "\nfixture\n")
        repository.write_text("assets/diagram.svg", f"<svg><text>{slack_token}</text></svg>\n")
        large_prefix = "public fixture text\n" + ("x" * (2 * 1024 * 1024))
        repository.write_text(
            "reports/large-fixture.txt",
            large_prefix + f"\nAuthorization: Bearer {bearer_value}\n",
        )
        repository.write_text("_site/generated.html", f"<p>{local_path}</p>\n")
        repository.write_text("_site/attachment.html", f"<p>{macos_attachment}</p>\n")
        repository.write_text(
            "reports/private-topology.txt",
            f"database {internal_host}\nendpoint {private_address}\nlocal file {root_home}\n",
        )
        repository.git("add", "NOTICE", "assets/diagram.svg", "reports/large-fixture.txt")
        repository.git("add", "-f", ".env", "keys/release.key")

        result = repository.cli("validate-public-content")
        output = result.stdout + result.stderr
        self.assertEqual(1, result.returncode, output)
        expected = {
            "NOTICE": "PS002",
            ".env": "PS003",
            "keys/release.key": "PS001",
            "assets/diagram.svg": "PS004",
            "reports/large-fixture.txt": "PS009",
            "_site/generated.html": "PS005",
            "_site/attachment.html": "PS027",
            "reports/private-topology.txt": "PS030",
        }
        for path, rule in expected.items():
            with self.subTest(path=path):
                self.assertIn(rule, output)
                self.assertIn(path, output)
        for sensitive in (
            github_token,
            aws_key,
            private_key_marker,
            slack_token,
            bearer_value,
            local_path,
            macos_attachment,
            internal_host,
            private_address,
            root_home,
        ):
            self.assertNotIn(sensitive, output)
        self.assertIn("reports/large-fixture.txt:3", output)
        self.assertIn("PS031", output)
        self.assertIn("PS032", output)

    def test_base_history_scan_finds_a_secret_added_then_deleted(self) -> None:
        repository = self.repository(local_origin=True)
        checkpoint, data, result = repository.new_checkpoint()
        self.assertEqual(0, result.returncode, result.stderr)
        secret = "gh" + "p_" + "E" * 24
        repository.write_text("docs/workflow-test.md", "# Workflow test\n\nSafe current content.\n")
        repository.write_text("temporary-evidence", f"deleted credential {secret}\n")
        introduced_sha = repository.commit_all("Add temporary evidence fixture")
        (repository.root / "temporary-evidence").unlink()
        repository.commit_all("Delete temporary evidence fixture")
        data.update(
            {
                "canonicalState": "PROJECTED",
                "artifactType": "workflow",
                "audiences": ["repository maintainers"],
                "scopeSummary": "The public history scanner fixture.",
                "deltaSummary": "A deleted credential fixture in candidate history.",
                "evidenceReferences": ["https://example.com/evidence/deleted-history"],
                "canonicalPaths": ["docs/workflow-test.md"],
                "derivedPaths": ["docs/workflow-test.md", "#/doc/workflow-test"],
                "localValidation": "pass",
            }
        )
        repository.replace_checkpoint(checkpoint, data)

        observed = repository.cli(
            "check",
            "--checkpoint",
            str(checkpoint),
            "--phase",
            "draft",
            "--base",
            repository.base_sha,
        )
        output = observed.stdout + observed.stderr
        self.assertEqual(2, observed.returncode, output)
        self.assertIn("PS002", output)
        self.assertIn(f"commit {introduced_sha} temporary-evidence", output)
        self.assertNotIn(secret, output)

    def test_history_scan_ignores_local_replace_objects_and_rejects_shallow_graphs(self) -> None:
        repository = self.repository(local_origin=True)
        checkpoint, data, result = repository.new_checkpoint()
        self.assertEqual(0, result.returncode, result.stderr)
        repository.write_text("docs/workflow-test.md", "# Workflow test\n\nSafe current content.\n")
        secret = "gh" + "p_" + "R" * 24
        repository.write_text("temporary-replaced-history", f"credential {secret}\n")
        introduced = repository.commit_all("Add replace-object history fixture")
        (repository.root / "temporary-replaced-history").unlink()
        repository.commit_all("Delete replace-object history fixture")

        parent = repository.git("rev-parse", f"{introduced}^").stdout.strip()
        safe_tree = repository.git("rev-parse", f"{parent}^{{tree}}").stdout.strip()
        replacement = repository.git(
            "commit-tree", safe_tree, "-p", parent, "-m", "Safe replacement object"
        ).stdout.strip()
        repository.git("replace", introduced, replacement)
        hidden = repository._run(("git", "show", f"{introduced}:temporary-replaced-history"))
        self.assertNotEqual(0, hidden.returncode, "fixture must hide the original blob without GIT_NO_REPLACE_OBJECTS")

        module = repository.load_module("scripts/study_workflow.py")
        errors = module.public_content_errors(repository.base_sha)
        self.assertTrue(any("PS002" in error and introduced in error for error in errors), errors)
        self.assertNotIn(secret, "\n".join(errors))
        with mock.patch.object(module, "git", return_value="true"):
            with self.assertRaisesRegex(module.WorkflowError, "complete, non-shallow"):
                module.verify_history_repository()

    def test_macos_attachment_path_is_rejected_in_checkpoint_and_deleted_history(self) -> None:
        repository = self.repository(local_origin=True)
        checkpoint, data, result = repository.new_checkpoint()
        self.assertEqual(0, result.returncode, result.stderr)
        macos_attachment = "/private/" + "var" + "/folders/xy/session/input.txt"
        original = checkpoint.read_bytes()
        checkpoint_result = repository.cli(
            "record",
            "--checkpoint",
            str(checkpoint),
            "--input-reference",
            macos_attachment,
        )
        checkpoint_output = checkpoint_result.stdout + checkpoint_result.stderr
        self.assertEqual(2, checkpoint_result.returncode, checkpoint_output)
        self.assertIn("PS027", checkpoint_output)
        self.assertNotIn(macos_attachment, checkpoint_output)
        self.assertEqual(original, checkpoint.read_bytes())

        repository.write_text("docs/workflow-test.md", "# Workflow test\n\nSafe current content.\n")
        repository.write_text("temporary-attachment", f"local attachment {macos_attachment}\n")
        introduced_sha = repository.commit_all("Add temporary attachment-path fixture")
        (repository.root / "temporary-attachment").unlink()
        repository.commit_all("Delete temporary attachment-path fixture")
        validated = repository.cli(
            "record", "--checkpoint", str(checkpoint), "--local-validation", "pass"
        )
        self.assertEqual(0, validated.returncode, validated.stdout + validated.stderr)
        data = json.loads(checkpoint.read_text(encoding="utf-8"))
        data.update(
            {
                "canonicalState": "PROJECTED",
                "artifactType": "workflow",
                "audiences": ["repository maintainers"],
                "scopeSummary": "Reject local attachment paths from public workflow history.",
                "deltaSummary": "A deleted macOS attachment-path fixture.",
                "evidenceReferences": ["https://example.com/evidence/local-path-history"],
                "canonicalPaths": ["docs/workflow-test.md"],
                "derivedPaths": ["docs/workflow-test.md", "#/doc/workflow-test"],
            }
        )
        repository.replace_checkpoint(checkpoint, data)
        observed = repository.cli(
            "check",
            "--checkpoint",
            str(checkpoint),
            "--phase",
            "draft",
            "--base",
            repository.base_sha,
        )
        output = observed.stdout + observed.stderr
        self.assertEqual(2, observed.returncode, output)
        self.assertIn("PS027", output)
        self.assertIn(f"commit {introduced_sha} temporary-attachment", output)
        self.assertNotIn(macos_attachment, output)

    def test_draft_history_rejects_merge_resolution_content_even_after_deletion(self) -> None:
        repository = self.repository(local_origin=True)
        checkpoint, data, result = repository.new_checkpoint()
        self.assertEqual(0, result.returncode, result.stderr)
        study_branch = data["branch"]
        secret = "gh" + "p_" + "H" * 24

        repository.write_text(
            "docs/merge-resolution.md", "candidate-side public fixture\n"
        )
        repository.commit_all("Add candidate side of merge fixture")
        repository.git("switch", "-q", "-c", "merge-source", repository.base_sha)
        repository.write_text(
            "docs/merge-resolution.md", "source-side public fixture\n"
        )
        repository.commit_all("Add source side of merge fixture")
        repository.git("switch", "-q", study_branch)
        conflict = repository._run(
            (
                "git",
                "merge",
                "--no-ff",
                "merge-source",
                "-m",
                "Merge the resolution fixture",
            )
        )
        self.assertNotEqual(0, conflict.returncode, conflict.stdout + conflict.stderr)
        repository.write_text(
            "docs/merge-resolution.md",
            f"merge-resolution-only credential {secret}\n",
        )
        merge_sha = repository.commit_all("Resolve the merge fixture")
        parents = repository.git(
            "rev-list", "--parents", "-n", "1", merge_sha
        ).stdout.split()
        self.assertEqual(3, len(parents))
        self.assertIn(
            secret,
            repository.git("show", f"{merge_sha}:docs/merge-resolution.md").stdout,
        )
        for parent in parents[1:]:
            self.assertNotIn(
                secret,
                repository.git("show", f"{parent}:docs/merge-resolution.md").stdout,
            )

        (repository.root / "docs" / "merge-resolution.md").unlink()
        repository.write_text(
            "docs/workflow-test.md", "# Workflow test\n\nSafe post-merge content.\n"
        )
        repository.commit_all("Delete the merge-resolution fixture")
        self.assertFalse((repository.root / "docs" / "merge-resolution.md").exists())
        validated = repository.cli(
            "record",
            "--checkpoint",
            str(checkpoint),
            "--local-validation",
            "pass",
        )
        self.assertEqual(0, validated.returncode, validated.stdout + validated.stderr)
        data = json.loads(checkpoint.read_text(encoding="utf-8"))
        data.update(
            {
                "canonicalState": "PROJECTED",
                "artifactType": "workflow",
                "audiences": ["repository maintainers"],
                "scopeSummary": "Reject merge commits from linear intake history.",
                "deltaSummary": "A deleted resolution-only credential fixture.",
                "evidenceReferences": ["https://example.com/evidence/merge-history"],
                "canonicalPaths": ["docs/workflow-test.md"],
                "derivedPaths": ["docs/workflow-test.md", "#/doc/workflow-test"],
            }
        )
        repository.replace_checkpoint(checkpoint, data)
        repository.install_fake_release_tools()

        module = repository.load_module("scripts/study_workflow.py")
        history_errors = module.public_content_errors(repository.base_sha)
        self.assertTrue(
            any("PS024" in error and merge_sha in error for error in history_errors),
            history_errors,
        )
        observed = repository.cli(
            "check",
            "--checkpoint",
            str(checkpoint),
            "--phase",
            "draft",
            "--base",
            repository.base_sha,
        )
        output = observed.stdout + observed.stderr
        self.assertEqual(2, observed.returncode, output)
        self.assertIn("PS024", output)
        self.assertIn(merge_sha, output)
        self.assertNotIn(secret, output)

    def test_ignored_inputs_stay_private_but_generated_output_is_scanned(self) -> None:
        repository = self.repository()
        secret = "gh" + "p_" + "F" * 24
        private_key_marker = "-----BEGIN " + "PRIVATE KEY-----"
        repository.write_text(".env", f"ACCESS_TOKEN={secret}\n")
        repository.write_text("docs/local.key", private_key_marker + "\nfixture\n")

        for relative in (".env", "docs/local.key"):
            with self.subTest(ignored=relative):
                ignored = repository._run(("git", "check-ignore", "-q", relative))
                self.assertEqual(0, ignored.returncode, ignored.stdout + ignored.stderr)

        private_only = repository.cli("validate-public-content")
        self.assertEqual(0, private_only.returncode, private_only.stdout + private_only.stderr)

        repository.write_text("_site/generated.html", f"<p>{secret}</p>\n")
        source_only = repository.cli("validate-public-content", "--source-only")
        self.assertEqual(0, source_only.returncode, source_only.stdout + source_only.stderr)
        generated = repository.cli("validate-public-content")
        output = generated.stdout + generated.stderr
        self.assertEqual(1, generated.returncode, output)
        self.assertIn("PS002", output)
        self.assertIn("_site/generated.html", output)
        self.assertNotIn(secret, output)
        self.assertNotIn("docs/local.key", output)

    def test_public_and_generated_symlinks_are_rejected_without_following_targets(self) -> None:
        secret = "gh" + "p_" + "G" * 24

        public_repository = self.repository()
        public_target = public_repository.container / "outside-public.txt"
        public_target.write_text(f"outside credential {secret}\n", encoding="utf-8")
        public_link = public_repository.root / "docs" / "public-link.md"
        public_link.symlink_to(public_target)
        public_repository.git("add", "docs/public-link.md")
        public_result = public_repository.cli("validate-public-content")
        public_output = public_result.stdout + public_result.stderr
        self.assert_deterministic_error(public_result, contains="PS022")
        self.assertNotIn("docs/public-link.md", public_output)
        self.assertNotIn(secret, public_output)
        self.assertNotIn("PS002", public_output)

        generated_repository = self.repository()
        generated_target = generated_repository.container / "outside-generated.txt"
        generated_target.write_text(f"outside credential {secret}\n", encoding="utf-8")
        generated_link = generated_repository.root / "_site" / "generated-link.html"
        generated_link.parent.mkdir(parents=True)
        generated_link.symlink_to(generated_target)
        generated_result = generated_repository.cli("validate-public-content")
        generated_output = generated_result.stdout + generated_result.stderr
        self.assert_deterministic_error(generated_result, contains="PS022")
        self.assertIn("_site/generated-link.html", generated_output)
        self.assertNotIn(secret, generated_output)
        self.assertNotIn("PS002", generated_output)


class BuildInputBoundaryTests(WorkflowTestCase):
    def test_scanner_build_and_manifest_reject_gitlinks_and_percent_paths(self) -> None:
        gitlink_repository = self.repository()
        gitlink_repository.git(
            "update-index",
            "--add",
            "--cacheinfo",
            "160000",
            gitlink_repository.base_sha,
            "docs/vendor-module",
        )
        scanner = gitlink_repository.cli("validate-public-content", "--source-only")
        self.assert_deterministic_error(scanner, contains="PS028")
        builder = gitlink_repository.load_module("scripts/build_site.py")
        validator = gitlink_repository.load_module("scripts/validate_site_manifest.py")
        with self.assertRaisesRegex(SystemExit, "non-regular tracked Git mode"):
            builder.repository_candidate_paths()
        with self.assertRaisesRegex(validator.ValidationError, "non-regular tracked Git mode"):
            validator.repository_candidate_paths()

        percent_repository = self.repository()
        percent_repository.write_text("docs/encoded%2Fname.md", "# Encoded path fixture\n")
        percent_scanner = percent_repository.cli("validate-public-content", "--source-only")
        self.assert_deterministic_error(percent_scanner, returncode=1, contains="PS019")
        percent_builder = percent_repository.load_module("scripts/build_site.py")
        percent_validator = percent_repository.load_module("scripts/validate_site_manifest.py")
        with self.assertRaisesRegex(SystemExit, "containing percent"):
            percent_builder.repository_candidate_paths()
        with self.assertRaisesRegex(percent_validator.ValidationError, "contains percent"):
            percent_validator.repository_candidate_paths()
        verifier = load_pages_verifier_module()
        with self.assertRaisesRegex(verifier.VerificationError, "must not contain percent"):
            verifier.safe_remote_path("content/docs/encoded%2Fname.md", "fixture path")

    def test_openapi_failure_does_not_echo_absolute_paths_or_source_lines(self) -> None:
        repository = self.repository(full=True)
        marker = "PRIVATE-OPENAPI-MARKER-MUST-NOT-APPEAR"
        source = sorted((repository.root / "poc" / "apis").glob("*.yaml"))[0]
        source.write_text(f"openapi: [ {marker}\n", encoding="utf-8")
        result = repository._run(
            (sys.executable, str(repository.root / "scripts" / "validate_openapi.py"), "poc/apis")
        )
        output = result.stdout + result.stderr
        self.assertEqual(1, result.returncode, output)
        self.assertIn("invalid YAML or OpenAPI document", output)
        self.assertNotIn(marker, output)
        self.assertNotIn(str(repository.root), output)
        self.assertNotIn("Traceback (most recent call last)", output)

        source.write_bytes(b"\xffnot-utf8\n")
        invalid_utf8 = repository._run(
            (sys.executable, str(repository.root / "scripts" / "validate_openapi.py"), "poc/apis")
        )
        invalid_output = invalid_utf8.stdout + invalid_utf8.stderr
        self.assertEqual(1, invalid_utf8.returncode, invalid_output)
        self.assertIn("document is unreadable or not valid UTF-8", invalid_output)
        self.assertNotIn(str(repository.root), invalid_output)
        self.assertNotIn("Traceback (most recent call last)", invalid_output)

    def test_aggregate_validators_do_not_read_ignored_private_inputs_or_symlinks(self) -> None:
        repository = self.repository(full=True)
        excluded = repository.root / ".git" / "info" / "exclude"
        excluded.write_text(
            excluded.read_text(encoding="utf-8")
            + "\nevidence/raw/\npoc/apis/private-local.yaml\ndocs/private-local.md\narchitecture/private-local.md\n",
            encoding="utf-8",
        )
        private_marker = "PRIVATE-VALIDATOR-FIXTURE-MUST-NOT-APPEAR"
        repository.write_text("evidence/raw/invalid.yaml", f"value: [ {private_marker}\n")
        repository.write_text("poc/apis/private-local.yaml", f"openapi: [ {private_marker}\n")
        repository.write_text("docs/private-local.md", f"[{private_marker}](missing-private-target.md)\n")
        outside = repository.container / "private-visual-source.mmd"
        outside.write_text(f"flowchart LR\n  A[{private_marker}]\n", encoding="utf-8")
        visual_link = repository.root / "architecture" / "private-local.md"
        visual_link.symlink_to(outside)

        commands = (
            ("scripts/validate_yaml.py",),
            ("scripts/validate_openapi.py", "poc/apis"),
            ("scripts/validate_links.py",),
            ("scripts/validate_visuals.py",),
            ("scripts/validate_studies.py",),
            ("scripts/validate_source_coverage.py",),
        )
        for command in commands:
            with self.subTest(validator=command[0]):
                result = repository._run(
                    (sys.executable, str(repository.root / command[0]), *command[1:])
                )
                output = result.stdout + result.stderr
                self.assertEqual(0, result.returncode, output)
                self.assertNotIn(private_marker, output)
                self.assertNotIn("Traceback (most recent call last)", output)

    def test_build_and_manifest_enumerate_tracked_plus_nonignored_inputs(self) -> None:
        repository = self.repository()
        repository.write_text("docs/public-extra.md", "# Public extra\n")
        repository.write_text("docs/private.key", "private local fixture\n")
        repository.write_text("docs/.env", "PRIVATE_VALUE=fixture\n")
        repository.write_text("_site/content/stale.md", "stale generated output\n")

        builder = repository.load_module("scripts/build_site.py")
        validator = repository.load_module("scripts/validate_site_manifest.py")
        resolved_root = repository.root.resolve()
        build_paths = {
            path.relative_to(resolved_root).as_posix()
            for path in builder.repository_candidate_paths()
        }
        manifest_paths = {
            path.relative_to(resolved_root).as_posix()
            for path in validator.repository_candidate_paths()
        }

        for paths in (build_paths, manifest_paths):
            with self.subTest(enumerator="build" if paths is build_paths else "manifest"):
                self.assertIn("docs/public-extra.md", paths)
                self.assertNotIn("docs/private.key", paths)
                self.assertNotIn("docs/.env", paths)
                self.assertNotIn("_site/content/stale.md", paths)
        published = {
            path.relative_to(resolved_root).as_posix()
            for path in builder.publishable_content_sources(list(builder.repository_candidate_paths()))
        }
        self.assertIn("docs/public-extra.md", published)

    def test_build_and_manifest_reject_public_symlink_inputs(self) -> None:
        repository = self.repository()
        target = repository.container / "outside-source.md"
        target.write_text("# Outside source\n", encoding="utf-8")
        link = repository.root / "docs" / "public-link.md"
        link.symlink_to(target)
        repository.git("add", "docs/public-link.md")

        builder = repository.load_module("scripts/build_site.py")
        validator = repository.load_module("scripts/validate_site_manifest.py")
        with self.assertRaisesRegex(SystemExit, "non-regular tracked Git mode"):
            builder.repository_candidate_paths()
        with self.assertRaisesRegex(validator.ValidationError, "non-regular tracked Git mode"):
            validator.repository_candidate_paths()

    def test_scanner_build_and_manifest_reject_hidden_index_flags(self) -> None:
        repository = self.repository()
        hidden_path = "docs/46-study-publication-workflow.md"
        repository.git("update-index", "--skip-worktree", hidden_path)

        scanner = repository.cli("validate-public-content")
        self.assert_deterministic_error(scanner, contains="PS023")
        builder = repository.load_module("scripts/build_site.py")
        validator = repository.load_module("scripts/validate_site_manifest.py")
        with self.assertRaisesRegex(SystemExit, "index visibility flags hide worktree state"):
            builder.repository_candidate_paths()
        with self.assertRaisesRegex(validator.ValidationError, "index visibility flags hide worktree state"):
            validator.repository_candidate_paths()

    def test_clean_filter_cannot_hide_raw_worktree_bytes_from_provenance(self) -> None:
        repository = self.repository()
        filtered_path = "docs/filter-provenance.txt"
        repository.git("config", "filter.provenance.clean", "sed 's/^worktree-only$/canonical/'")
        repository.git("config", "filter.provenance.required", "true")
        repository.write_text(".gitattributes", f"{filtered_path} filter=provenance\n")
        tracked = repository.write_text(filtered_path, "canonical\n")
        revision = repository.commit_all("Add clean-filter provenance fixture")

        tracked.write_text("worktree-only\n", encoding="utf-8")
        # The clean filter maps the changed worktree bytes back to the committed
        # blob.  ``git add`` refreshes the stat cache without changing the index,
        # leaving ordinary status checks empty despite the raw-byte divergence.
        repository.git("add", "--", filtered_path)
        status = repository.git(
            "status", "--porcelain=v1", "--untracked-files=all"
        ).stdout
        committed = repository.git("show", f"{revision}:{filtered_path}").stdout.encode("utf-8")
        self.assertEqual("", status, "the fixture must reproduce Git's clean-filter bypass")
        self.assertNotEqual(committed, tracked.read_bytes())

        builder = repository.load_module("scripts/build_site.py")
        self.assertFalse(builder.raw_tracked_bytes_match(revision))
        self.assertTrue(builder.source_is_dirty(revision))

        output = repository.root / "_site"
        repository.write_text(
            "_site/content-manifest.json",
            json.dumps(
                {
                    "schemaVersion": 2,
                    "sourceRevision": revision,
                    "sourceDirty": True,
                }
            )
            + "\n",
        )
        validation = repository._run(
            (
                sys.executable,
                str(repository.root / "scripts" / "validate_site_manifest.py"),
                "--output",
                str(output),
                "--require-clean",
            )
        )
        self.assertEqual(1, validation.returncode, validation.stdout + validation.stderr)
        self.assertIn(
            "a clean publication was required but sourceDirty is true",
            validation.stderr,
        )
        self.assertNotIn("Traceback (most recent call last)", validation.stderr)

    def test_build_output_requires_a_safe_owned_replacement_target(self) -> None:
        repository = self.repository()
        builder = repository.load_module("scripts/build_site.py")
        default_output = repository.root / "_site"
        self.assertEqual(default_output.resolve(), builder.validated_output_path(default_output))

        default_output.mkdir()
        default_sentinel = default_output / builder.OUTPUT_SENTINEL
        default_sentinel.write_bytes(b"\xffnot-utf8\n")
        with self.assertRaisesRegex(SystemExit, "existing unowned output directory"):
            builder.validated_output_path(default_output)
        default_sentinel.unlink()
        sentinel_target = repository.container / "sentinel-target"
        sentinel_target.write_text(builder.OUTPUT_SENTINEL_VALUE, encoding="utf-8")
        default_sentinel.symlink_to(sentinel_target)
        with self.assertRaisesRegex(SystemExit, "existing unowned output directory"):
            builder.validated_output_path(default_output)
        default_sentinel.unlink()
        default_sentinel.write_text(builder.OUTPUT_SENTINEL_VALUE, encoding="utf-8")
        self.assertEqual(default_output.resolve(), builder.validated_output_path(default_output))
        shutil.rmtree(default_output)

        unowned = repository.container / "unowned-output"
        unowned.mkdir()
        with self.assertRaisesRegex(SystemExit, "existing unowned output directory"):
            builder.validated_output_path(unowned)
        (unowned / builder.OUTPUT_SENTINEL).write_text(
            builder.OUTPUT_SENTINEL_VALUE, encoding="utf-8"
        )
        self.assertEqual(unowned.resolve(), builder.validated_output_path(unowned))

        inside_repository = repository.root / "dist-site"
        with self.assertRaisesRegex(SystemExit, "may be replaced inside the repository"):
            builder.validated_output_path(inside_repository)

        redirected = repository.container / "redirected-output"
        redirected.mkdir()
        default_output.symlink_to(redirected, target_is_directory=True)
        with self.assertRaisesRegex(SystemExit, "symlinked site output"):
            builder.validated_output_path(default_output)


class ManifestRuntimeDependencyTests(WorkflowTestCase):
    def test_poc_projection_contract_rejects_local_and_pages_manifest_drift(self) -> None:
        repository = self.repository()
        validator = repository.load_module("scripts/validate_site_manifest.py")
        verifier = load_pages_verifier_module()
        valid = {"visuals": {"poc": poc_projection_fixture()}}

        validator.validate_poc_projection(valid)
        verifier.validate_poc_projection(valid)

        invalid_cases = (
            ("non-positive total", "positive integer", "positive integer"),
            ("duplicate status label", "contains duplicate", "must be unique"),
            ("status sum", "must sum", "must sum"),
            ("canonical status count", "exactly Automated=5", "exactly Automated=5"),
            ("test length", "length must equal", "length must equal"),
            ("duplicate test ID", "contains duplicate", "must be unique"),
            ("canonical test IDs", "must be exactly POC-001", "must be exactly POC-001"),
            ("undeclared test status", "is undeclared", "is undeclared"),
            ("test status aggregate", "status counts must match", "status counts must match"),
            ("canonical ID status swap", "canonical ID-to-status", "canonical ID-to-status"),
        )
        for case, local_error, pages_error in invalid_cases:
            with self.subTest(case=case):
                invalid = json.loads(json.dumps(valid))
                poc = invalid["visuals"]["poc"]
                if case == "non-positive total":
                    poc["total"] = False
                elif case == "duplicate status label":
                    poc["byStatus"][1]["label"] = "Not run"
                elif case == "status sum":
                    poc["byStatus"][0]["value"] = 10
                elif case == "canonical status count":
                    poc["byStatus"][0]["value"] = 10
                    poc["byStatus"][1]["value"] = 6
                elif case == "test length":
                    poc["tests"].pop()
                elif case == "duplicate test ID":
                    poc["tests"][-1]["id"] = poc["tests"][0]["id"]
                elif case == "canonical test IDs":
                    poc["tests"][-1]["id"] = "POC-111"
                elif case == "undeclared test status":
                    poc["tests"][0]["status"] = "Scripted"
                elif case == "test status aggregate":
                    poc["tests"][0]["status"] = "Not run"
                else:
                    poc["tests"][0]["status"], poc["tests"][5]["status"] = (
                        poc["tests"][5]["status"],
                        poc["tests"][0]["status"],
                    )

                with self.assertRaisesRegex(validator.ValidationError, local_error):
                    validator.validate_poc_projection(invalid)
                with self.assertRaisesRegex(verifier.VerificationError, pages_error):
                    verifier.validate_poc_projection(invalid)

    def test_named_presentation_deck_contract_and_route_inventory(self) -> None:
        repository = self.repository()
        validator = repository.load_module("scripts/validate_site_manifest.py")
        verifier = load_pages_verifier_module()
        items = [
            {
                "id": "source",
                "path": "docs/source.md",
                "route": "#/doc/source",
            }
        ]
        fit_rows = [
            {"projectionId": f"KPS-FIT-{index:02d}"}
            for index in range(1, 8)
        ]
        fit_slides = [
            {
                "index": 1,
                "key": "kong-platform-fit-boundary",
                "sourceId": "source",
                "visual": "kongPlatformFit",
                "rowIds": ["KPS-FIT-01", "KPS-FIT-02"],
            },
            {
                "index": 2,
                "key": "kong-platform-fit-runtime",
                "sourceId": "source",
                "visual": "kongPlatformFit",
                "rowIds": ["KPS-FIT-03", "KPS-FIT-04"],
            },
            {
                "index": 3,
                "key": "kong-platform-fit-change",
                "sourceId": "source",
                "visual": "kongPlatformFit",
                "rowIds": ["KPS-FIT-05", "KPS-FIT-06"],
            },
            {
                "index": 4,
                "key": "kong-platform-fit-fallback",
                "sourceId": "source",
                "visual": "kongPlatformFit",
                "rowIds": ["KPS-FIT-07"],
            },
        ]
        manifest = {
            "presentation": [
                {"index": 0, "key": "decision", "sourceId": "source"},
                *fit_slides,
                {"index": 5, "key": "technical", "sourceId": "source"},
            ],
            "visuals": {
                "poc": poc_projection_fixture(),
                "kongPlatformStrategy": {"fit": {"rows": fit_rows}},
            },
            "audiences": [
                {
                    "id": "architects",
                    "sourcePaths": ["docs/source.md"],
                    "sourceIds": ["source"],
                    "presentationSlides": ["technical"],
                    "presentationRoute": "#/present/architects/0",
                    "recommendedRoute": "#/architecture",
                }
            ],
            "presentationDecks": [
                {
                    "id": "kong-technical-deep-dive",
                    "sourcePaths": ["docs/source.md"],
                    "sourceIds": ["source"],
                    "audienceRoleIds": ["architects"],
                    "presentationSlides": [
                        "decision",
                        *(slide["key"] for slide in fit_slides),
                        "technical",
                    ],
                    "slideTotal": 6,
                    "presentationRoute": "#/present/kong-technical-deep-dive/0",
                    "exitRoute": "#/architecture",
                }
            ],
        }
        by_id = {"source": items[0]}

        validator.validate_routes_and_audiences(manifest, by_id, {"#/doc/source"})
        routes = verifier.validated_route_inventory(manifest, items)
        self.assertIn("#/present/kong-technical-deep-dive/0", routes)
        self.assertIn("#/present/kong-technical-deep-dive/5", routes)

        invalid_cases = (
            ("unknown slide", "unknown slide"),
            ("audience ID collision", "collide"),
            ("invalid entry route", "presentationRoute is invalid"),
            ("wrong slide total", "slideTotal"),
            ("wrong bounded rows", "bounded Kong fit contract"),
            ("removed fit slide", "removed Kong platform fit slide"),
            ("extra fit slide", "exactly the four semantic fit slide keys"),
        )
        for case, expected in invalid_cases:
            with self.subTest(case=case):
                invalid = json.loads(json.dumps(manifest))
                deck = invalid["presentationDecks"][0]
                if case == "unknown slide":
                    deck["presentationSlides"] = ["missing-slide"]
                elif case == "audience ID collision":
                    deck["id"] = "architects"
                    deck["presentationRoute"] = "#/present/architects/0"
                elif case == "invalid entry route":
                    deck["presentationRoute"] = "#/present/not-the-deck/0"
                elif case == "wrong slide total":
                    deck["slideTotal"] = 5
                elif case == "wrong bounded rows":
                    invalid["presentation"][1]["rowIds"] = ["KPS-FIT-01"]
                elif case == "removed fit slide":
                    invalid["presentation"][1]["key"] = "kong-platform-fit-1"
                else:
                    invalid["presentation"].append(
                        {
                            "index": len(invalid["presentation"]),
                            "key": "kong-platform-fit-unreferenced",
                            "sourceId": "source",
                            "visual": "kongPlatformFit",
                            "rowIds": ["KPS-FIT-01"],
                        }
                    )
                with self.assertRaisesRegex(validator.ValidationError, expected):
                    validator.validate_routes_and_audiences(
                        invalid, by_id, {"#/doc/source"}
                    )
                with self.assertRaisesRegex(verifier.VerificationError, expected):
                    verifier.validated_route_inventory(invalid, items)

    def test_built_manifest_rejects_every_undeclared_or_unsafe_output(self) -> None:
        repository = self.repository(full=True)
        builder = repository.root / "scripts" / "build_site.py"
        validator = repository.root / "scripts" / "validate_site_manifest.py"
        output = repository.root / "_site"

        def rebuild() -> None:
            built = repository._run((str(repository.python_executable), str(builder)))
            self.assertEqual(0, built.returncode, built.stdout + built.stderr)

        def validate() -> subprocess.CompletedProcess[str]:
            return repository._run(
                (
                    str(repository.python_executable),
                    str(validator),
                    "--output",
                    str(output),
                    "--require-clean",
                )
            )

        rebuild()
        baseline = validate()
        self.assertEqual(0, baseline.returncode, baseline.stdout + baseline.stderr)

        linked_output = repository.container / "linked-site-output"
        linked_output.symlink_to(output, target_is_directory=True)
        linked_validation = repository._run(
            (
                str(repository.python_executable),
                str(validator),
                "--output",
                str(linked_output),
            )
        )
        self.assert_deterministic_error(
            linked_validation,
            returncode=1,
            contains="generated output root must be a regular directory",
        )

        validator_module = repository.load_module("scripts/validate_site_manifest.py")
        for unsafe_path in ("content/item.md?download=1", "content/item.md#fragment"):
            with self.subTest(unsafe_path=unsafe_path):
                with self.assertRaisesRegex(validator_module.ValidationError, "without query or fragment"):
                    validator_module.safe_relative(unsafe_path, "fixture path")

        undeclared = (
            output / "rogue.html",
            output / "assets" / "rogue.js",
            output / ".hidden-extra",
        )
        for rogue in undeclared:
            with self.subTest(case=rogue.name):
                rebuild()
                rogue.parent.mkdir(parents=True, exist_ok=True)
                rogue.write_text("undeclared\n", encoding="utf-8")
                result = validate()
                self.assert_deterministic_error(
                    result,
                    returncode=1,
                    contains="generated output contains undeclared or missing files",
                )

        target = repository.container / "private-target"
        target.write_text("must not be read\n", encoding="utf-8")
        for relative, directory in (("rogue-link", False), ("rogue-directory", True)):
            with self.subTest(case=relative):
                rebuild()
                link = output / relative
                link.symlink_to(
                    repository.container if directory else target,
                    target_is_directory=directory,
                )
                result = validate()
                self.assert_deterministic_error(
                    result,
                    returncode=1,
                    contains="generated output contains a symlink",
                )

        rebuild()
        (output / ".api-management-studies-generated-output").write_bytes(b"\xffinvalid owner\n")
        corrupt_sentinel = validate()
        self.assert_deterministic_error(
            corrupt_sentinel,
            returncode=1,
            contains="generated output ownership sentinel is invalid",
        )

        (output / ".api-management-studies-generated-output").write_text(
            "Generated by scripts/build_site.py; safe to replace.\n",
            encoding="utf-8",
        )
        rebuild()
        (output / ".nojekyll").write_text("unexpected\n", encoding="utf-8")
        nonempty_nojekyll = validate()
        self.assert_deterministic_error(
            nonempty_nojekyll,
            returncode=1,
            contains=".nojekyll must be empty",
        )

    def test_built_manifest_rejects_quoted_unquoted_and_duplicate_script_bypasses(self) -> None:
        repository = self.repository(full=True)
        builder = repository.root / "scripts" / "build_site.py"
        validator = repository.root / "scripts" / "validate_site_manifest.py"
        output = repository.root / "_site"

        built = repository._run((str(repository.python_executable), str(builder)))
        self.assertEqual(0, built.returncode, built.stdout + built.stderr)
        baseline_validation = repository._run(
            (
                str(repository.python_executable),
                str(validator),
                "--output",
                str(output),
                "--require-clean",
            )
        )
        self.assertEqual(
            0,
            baseline_validation.returncode,
            baseline_validation.stdout + baseline_validation.stderr,
        )
        index = repository.root / "site" / "index.html"
        baseline = index.read_text(encoding="utf-8")
        self.assertIn('src="https://cdn.jsdelivr.net/', baseline)
        validator_module = repository.load_module("scripts/validate_site_manifest.py")
        external_source, integrity = next(
            iter(validator_module.ALLOWED_EXTERNAL_SCRIPTS.items())
        )
        cases = (
            (
                "single-quoted unlisted external",
                "<script src='https://cdn.jsdelivr.net/npm/unlisted-runtime@1.0.0/dist/runtime.min.js'></script>",
                "external script is not in the exact versioned runtime allowlist",
            ),
            (
                "unquoted unlisted external",
                "<script src=https://cdn.jsdelivr.net/npm/unlisted-runtime@1.0.0/dist/runtime.min.js></script>",
                "external script is not in the exact versioned runtime allowlist",
            ),
            (
                "duplicate allowed external",
                (
                    f'<script defer src="{external_source}" integrity="{integrity}" '
                    'crossorigin="anonymous"></script>'
                ),
                "external runtime script is declared more than once",
            ),
            (
                "duplicate allowed local",
                '<script defer src="assets/app.js"></script>',
                "local runtime script is declared more than once",
            ),
        )
        for label, injected_tag, expected in cases:
            with self.subTest(case=label):
                index.write_text(
                    baseline.replace("</head>", f"    {injected_tag}\n  </head>", 1),
                    encoding="utf-8",
                )
                rebuilt = repository._run(
                    (str(repository.python_executable), str(builder))
                )
                self.assertEqual(0, rebuilt.returncode, rebuilt.stdout + rebuilt.stderr)
                observed = repository._run(
                    (
                        str(repository.python_executable),
                        str(validator),
                        "--output",
                        str(output),
                    )
                )
                combined = observed.stdout + observed.stderr
                self.assertEqual(1, observed.returncode, combined)
                self.assertIn(expected, combined)
                self.assertNotIn("Traceback (most recent call last)", combined)


class StatePrerequisiteTests(WorkflowTestCase):
    def test_closed_checkpoint_rejects_all_mutation_commands(self) -> None:
        repository = self.repository(local_origin=True)
        checkpoint, data, head = repository.prepare_release()
        manifest_sha = "a" * 64
        data.update(
            {
                "canonicalState": "CLOSED",
                "mergeSha": head,
                "branchCleanupStatus": "complete",
                "cleanupEvidence": ["verified branch cleanup"],
                "mainValidationUrl": "https://github.com/owner/repo/actions/runs/101",
                "pagesRunUrl": "https://github.com/owner/repo/actions/runs/102",
                "manifestSha256": manifest_sha,
                "closureEvidenceUrl": "https://github.com/owner/repo/pull/17#issuecomment-100",
                "liveBaseUrl": "https://example.com/studies/",
                "derivedPaths": ["site/workflow-test.json", "#/doc/workflow-test"],
                "manifestAssertions": [
                    f"sourceRevision={head}", f"manifestSha256={manifest_sha}", "sourceDirty=false",
                ],
                "routeAssertions": ["#/doc/workflow-test"],
                "publicationStatus": "published",
                "residualLimitations": ["No organization-specific fit is inferred."],
                "nextGate": "Open a superseding intake for any correction.",
            }
        )
        repository.replace_checkpoint(checkpoint, data)
        before = checkpoint.read_bytes()
        for arguments in (
            ("record", "--checkpoint", str(checkpoint), "--next-gate", "Mutate closure."),
            ("replace-list", "--checkpoint", str(checkpoint), "--field", "residualLimitations", "--value", "changed", "--status-reason", "Mutate closure."),
        ):
            with self.subTest(command=arguments[0]):
                observed = repository.cli(*arguments)
                self.assert_deterministic_error(observed, contains="CLOSED is immutable")
                self.assertEqual(before, checkpoint.read_bytes())
    def test_record_rejects_every_target_state_when_its_exit_evidence_is_absent(self) -> None:
        repository = self.repository()
        checkpoint, intake, result = repository.new_checkpoint()
        self.assertEqual(0, result.returncode, result.stderr)

        accepted: list[str] = []
        for target in EXPECTED_STATES[1:]:
            with self.subTest(target=target):
                candidate = dict(intake)
                if target == "FRAMED":
                    candidate["decisionQuestion"] = ""
                repository.replace_checkpoint(checkpoint, candidate)
                observed = repository.cli(
                    "record", "--checkpoint", str(checkpoint), "--state", target
                )
                persisted = json.loads(checkpoint.read_text(encoding="utf-8"))
                if observed.returncode == 0 or persisted["canonicalState"] != "INTAKE":
                    accepted.append(target)
                elif "Traceback (most recent call last)" in observed.stderr:
                    accepted.append(f"{target} (uncaught exception)")
        self.assertEqual([], accepted, f"states accepted without their contract evidence: {accepted}")

    def test_arbitrary_jump_is_rejected_even_when_late_fields_are_prepopulated(self) -> None:
        repository = self.repository()
        checkpoint, data, head = repository.prepare_draft()
        data.update(
            {
                "canonicalState": "INTAKE",
                "candidateSha": head,
                "prNumber": 17,
                "prHeadSha": head,
                "prDraft": False,
                "reviewDisposition": "pass",
                "acceptedSha": head,
                "checkedSha": head,
                "checkDisposition": "green",
                "checkUrls": ["https://github.com/owner/repo/actions/runs/17"],
            }
        )
        repository.replace_checkpoint(checkpoint, data)
        observed = repository.cli(
            "record", "--checkpoint", str(checkpoint), "--state", "VALIDATED"
        )
        persisted = json.loads(checkpoint.read_text(encoding="utf-8"))
        self.assert_deterministic_error(observed)
        self.assertEqual("INTAKE", persisted["canonicalState"])

    def test_projected_state_requires_non_route_derived_files_to_exist(self) -> None:
        repository = self.repository()
        checkpoint, data, _ = repository.prepare_draft()
        data["derivedPaths"] = ["site/missing-projection.json", "#/doc/workflow-test"]
        repository.replace_checkpoint(checkpoint, data)

        missing = repository.cli("render", "--checkpoint", str(checkpoint))
        self.assert_deterministic_error(
            missing,
            contains="derived path does not exist as a regular file",
        )

        data["derivedPaths"] = ["#/doc/workflow-test"]
        repository.replace_checkpoint(checkpoint, data)
        route_only = repository.cli("render", "--checkpoint", str(checkpoint))
        self.assertEqual(0, route_only.returncode, route_only.stdout + route_only.stderr)

    def test_each_structured_state_rejects_its_missing_prerequisite(self) -> None:
        repository = self.repository(local_origin=True)
        checkpoint, complete, head = repository.prepare_release()
        complete.update(
            {
                "evidenceReferences": ["https://example.com/evidence/workflow-contract"],
                "prUrl": "https://github.com/owner/repo/pull/17",
                "reviewEvidenceUrls": [
                    "https://github.com/owner/repo/pull/17#issuecomment-99"
                ],
                "mergeSha": repository.base_sha,
                "branchCleanupStatus": "complete",
                "cleanupEvidence": ["https://example.com/branches/workflow-test"],
                "mainValidationUrl": "https://github.com/owner/repo/actions/runs/101",
                "pagesRunUrl": "https://github.com/owner/repo/actions/runs/102",
                "manifestSha256": "a" * 64,
                "closureEvidenceUrl": "https://github.com/owner/repo/pull/17#issuecomment-100",
                "liveBaseUrl": "https://example.com/studies/",
                "derivedPaths": [
                    "site/workflow-test.json",
                    "#/studies/workflow-test",
                    "#/presentations/workflow-test",
                ],
                "manifestAssertions": [
                    f"sourceRevision={repository.base_sha}",
                    f"manifestSha256={'a' * 64}",
                    "sourceDirty=false",
                ],
                "routeAssertions": [
                    "#/studies/workflow-test",
                    "#/presentations/workflow-test",
                ],
                "publicationStatus": "published",
                "residualLimitations": ["No organization-specific fit is inferred."],
                "nextGate": "Run the next independently reviewed evidence intake.",
                "blockerOwnerRole": "release coordinator",
                "responsibleStage": "independent review",
            }
        )
        cases: dict[str, tuple[str, dict[str, Any]]] = {
            "FRAMED requires artifact classification": ("FRAMED", {"artifactType": None}),
            "RESEARCHED requires evidence plan": ("RESEARCHED", {"evidenceReferences": []}),
            "AUTHORED requires canonical artifacts": ("AUTHORED", {"canonicalPaths": []}),
            "PROJECTED requires derived artifacts": ("PROJECTED", {"derivedPaths": []}),
            "CANDIDATE requires candidate SHA": ("CANDIDATE", {"candidateSha": None}),
            "CANDIDATE requires PR URL": ("CANDIDATE", {"prUrl": None}),
            "CANDIDATE requires a draft PR": ("CANDIDATE", {"prDraft": False}),
            "REVIEWED requires accepted review": (
                "REVIEWED",
                {"reviewDisposition": "pending", "acceptedSha": None},
            ),
            "VALIDATED requires green checked SHA": (
                "VALIDATED",
                {"checkDisposition": "pending", "checkedSha": None},
            ),
            "MERGED requires merge SHA": ("MERGED", {"mergeSha": None}),
            "PUBLISHED requires Pages proof": ("PUBLISHED", {"pagesRunUrl": None}),
            "CLOSED requires residual limitations": ("CLOSED", {"residualLimitations": []}),
            "REWORK requires defect record": ("REWORK", {"statusReason": ""}),
            "BLOCKED requires blocker record": ("BLOCKED", {"statusReason": ""}),
            "BLOCKED requires owner role": ("BLOCKED", {"blockerOwnerRole": None}),
        }

        accepted: list[str] = []
        for label, (state, changes) in cases.items():
            with self.subTest(state=state):
                candidate = dict(complete)
                candidate["canonicalState"] = state
                candidate.update(changes)
                repository.replace_checkpoint(checkpoint, candidate)
                observed = repository.cli("render", "--checkpoint", str(checkpoint))
                if observed.returncode == 0:
                    accepted.append(label)
                elif "Traceback (most recent call last)" in observed.stderr:
                    accepted.append(f"{label} (uncaught exception)")
        self.assertEqual([], accepted, f"state prerequisites were not enforced: {accepted}")


class ImmutableSpecTests(WorkflowTestCase):
    def test_spec_is_trackable_sections_1_to_9_while_checkpoint_is_ignored_and_mutable(self) -> None:
        repository = self.repository()
        checkpoint, data, result = repository.new_checkpoint(write_spec=True)
        self.assertEqual(0, result.returncode, result.stderr)
        payload = json.loads(result.stdout)
        spec = repository.root / payload["spec"]
        before = spec.read_bytes()
        before_digest = hashlib.sha256(before).hexdigest()
        text = before.decode("utf-8")

        self.assertTrue(text.startswith("<!-- Immutable public-safe intake specification"))
        self.assertIn("## 9. Multi-agent ownership and handoffs", text)
        self.assertNotIn("## 10. Local validation and PR candidate", text)
        self.assertNotIn("Candidate head SHA", text)
        self.assertNotIn("Publication status", text)
        self.assertEqual(0, repository.git("check-ignore", "-q", str(checkpoint.relative_to(repository.root))).returncode)
        check_spec = repository._run(("git", "check-ignore", "-q", str(spec.relative_to(repository.root))))
        self.assertEqual(1, check_spec.returncode)
        untracked = repository.git("ls-files", "--others", "--exclude-standard").stdout.splitlines()
        self.assertIn(spec.relative_to(repository.root).as_posix(), untracked)
        self.assertNotIn(checkpoint.relative_to(repository.root).as_posix(), untracked)

        recorded = repository.cli(
            "record",
            "--checkpoint",
            str(checkpoint),
            "--status-reason",
            "Framing remains in progress.",
            "--next-gate",
            "Complete the public-safe evidence plan.",
        )
        self.assertEqual(0, recorded.returncode, recorded.stderr)
        self.assertNotEqual(data, json.loads(checkpoint.read_text(encoding="utf-8")))
        self.assertEqual(before_digest, hashlib.sha256(spec.read_bytes()).hexdigest())
        validation = repository.cli("validate-repo")
        self.assertEqual(0, validation.returncode, validation.stdout + validation.stderr)

    def test_validate_repo_rejects_mutable_operational_sections_in_an_intake_spec(self) -> None:
        repository = self.repository()
        _, _, result = repository.new_checkpoint(write_spec=True)
        self.assertEqual(0, result.returncode, result.stderr)
        spec = repository.root / json.loads(result.stdout)["spec"]
        spec.write_text(
            spec.read_text(encoding="utf-8") + "\n## 10. Local validation and PR candidate\n\n- **Candidate head SHA:** pending\n",
            encoding="utf-8",
        )
        observed = repository.cli("validate-repo")
        self.assert_deterministic_error(
            observed,
            returncode=1,
            contains="immutable intake spec contains mutable operational fields",
        )


class DraftGateTests(WorkflowTestCase):
    def test_named_presentation_deck_routes_are_manifest_bounded(self) -> None:
        repository = self.repository(local_origin=True)
        _, data, _ = repository.prepare_draft()
        data["derivedPaths"] = [
            "site/workflow-test.json",
            "#/doc/workflow-test",
            "#/present/kong-technical-deep-dive/0",
        ]
        manifest = repository.root / "_site" / "content-manifest.json"
        manifest.write_text(
            json.dumps(
                {
                    "items": [
                        {
                            "path": "docs/workflow-test.md",
                            "route": "#/doc/workflow-test",
                        }
                    ],
                    "presentation": [
                        {"index": 0, "key": "technical"},
                    ],
                    "audiences": [
                        {
                            "id": "architects",
                            "presentationSlides": ["technical"],
                        }
                    ],
                    "presentationDecks": [
                        {
                            "id": "kong-technical-deep-dive",
                            "audienceRoleIds": ["architects"],
                            "presentationSlides": ["technical"],
                            "presentationRoute": "#/present/kong-technical-deep-dive/0",
                        }
                    ],
                }
            ),
            encoding="utf-8",
        )
        workflow = repository.load_module("scripts/study_workflow.py")
        workflow.verify_local_derived_routes(data)

        for unknown in (
            "#/present/kong-technical-deep-dive/1",
            "#/present/unknown-deck/0",
        ):
            with self.subTest(route=unknown):
                invalid = dict(data)
                invalid["derivedPaths"] = [
                    "site/workflow-test.json",
                    "#/doc/workflow-test",
                    unknown,
                ]
                with self.assertRaisesRegex(
                    workflow.WorkflowError,
                    "declared derived route is absent from the generated site manifest",
                ):
                    workflow.verify_local_derived_routes(invalid)

    def test_candidate_rejects_ignored_or_generated_nonroute_derived_files(self) -> None:
        repository = self.repository(local_origin=True)
        checkpoint, valid, _ = repository.prepare_candidate()
        fixtures = {
            "generated output": "_site/content-manifest.json",
            "ignored evidence": "evidence/raw/local-only-proof.md",
        }
        for label, relative in fixtures.items():
            with self.subTest(case=label):
                repository.write_text(relative, "Local-only derived fixture.\n")
                candidate = dict(valid)
                candidate["derivedPaths"] = [*valid["derivedPaths"], relative]
                candidate["candidateEnvelopeSha256"] = repository.load_module(
                    "scripts/study_workflow.py"
                ).candidate_envelope_digest(candidate)
                repository.replace_checkpoint(checkpoint, candidate)
                pr = repository.with_current_checkpoint_body(
                    repository.valid_pr_json(candidate["candidateSha"], draft=True), checkpoint
                )
                observed = repository.cli(
                    "check", "--checkpoint", str(checkpoint), "--phase", "draft",
                    "--base", repository.base_sha,
                    environment=repository.fake_github_environment(pr, candidate["candidateSha"]),
                )
                self.assert_deterministic_error(
                    observed,
                    contains="candidate derived path is",
                )

    def test_force_tracked_ignored_generated_file_is_not_a_candidate_artifact(self) -> None:
        repository = self.repository(local_origin=True)
        _, data, _ = repository.prepare_candidate()
        relative = "_site/content-manifest.json"
        repository.write_text(relative, '{"local": true}\n')
        repository.git("add", "-f", relative)
        repository.git("commit", "-q", "-m", "Force-track generated output fixture")
        data["candidateSha"] = repository.git("rev-parse", "HEAD").stdout.strip()
        data["derivedPaths"] = [*data["derivedPaths"], relative]
        workflow = repository.load_module("scripts/study_workflow.py")
        with self.assertRaisesRegex(workflow.WorkflowError, "generated, private, or workflow-local"):
            workflow.verify_candidate_derived_files(data)

    def test_projected_publication_requires_a_manifest_backed_route_and_canonical_path(self) -> None:
        repository = self.repository(local_origin=True)
        checkpoint, data, _ = repository.prepare_draft()

        no_route = dict(data)
        no_route["derivedPaths"] = ["site/workflow-test.json"]
        repository.replace_checkpoint(checkpoint, no_route)
        missing_route = repository.cli("render", "--checkpoint", str(checkpoint))
        self.assert_deterministic_error(
            missing_route,
            contains="at least one site route is required",
        )

        repository.replace_checkpoint(checkpoint, data)
        manifest = repository.root / "_site" / "content-manifest.json"
        manifest.write_text(
            json.dumps(
                {
                    "items": [
                        {
                            "path": "docs/another-publication.md",
                            "route": "#/doc/workflow-test",
                        }
                    ],
                    "presentation": [],
                    "audiences": [],
                    "presentationDecks": [],
                }
            ),
            encoding="utf-8",
        )
        missing_canonical = repository.cli(
            "check", "--checkpoint", str(checkpoint), "--phase", "draft", "--base", repository.base_sha
        )
        self.assert_deterministic_error(
            missing_canonical,
            contains="canonical path is absent from the generated site manifest",
        )

        repository.replace_checkpoint(checkpoint, data)
        manifest.write_text(
            json.dumps(
                {
                    "items": [
                        {
                            "path": "docs/workflow-test.md",
                            "route": "#/doc/workflow-test",
                        }
                    ],
                    "presentation": [],
                    "audiences": [],
                    "presentationDecks": [],
                }
            ),
            encoding="utf-8",
        )
        unrelated_route = dict(data)
        unrelated_route["derivedPaths"] = ["site/workflow-test.json", "#/overview"]
        repository.replace_checkpoint(checkpoint, unrelated_route)
        mismatched = repository.cli(
            "check", "--checkpoint", str(checkpoint), "--phase", "draft", "--base", repository.base_sha
        )
        self.assert_deterministic_error(
            mismatched,
            contains="canonical path manifest route is not declared as derived",
        )

    def test_draft_gate_requires_every_declared_route_in_the_generated_manifest(self) -> None:
        repository = self.repository(local_origin=True)
        checkpoint, data, _ = repository.prepare_draft()
        data["derivedPaths"] = [
            "site/workflow-test.json",
            "#/doc/workflow-test",
            "#/doc/missing-workflow-route",
        ]
        repository.replace_checkpoint(checkpoint, data)
        manifest = repository.root / "_site" / "content-manifest.json"
        manifest.parent.mkdir(parents=True, exist_ok=True)
        manifest.write_text(
            json.dumps(
                {
                    "items": [
                        {
                            "path": "docs/workflow-test.md",
                            "route": "#/doc/workflow-test",
                        }
                    ],
                    "presentation": [],
                    "audiences": [],
                    "presentationDecks": [],
                }
            ),
            encoding="utf-8",
        )
        observed = repository.cli(
            "check", "--checkpoint", str(checkpoint), "--phase", "draft", "--base", repository.base_sha
        )
        self.assert_deterministic_error(
            observed,
            contains="declared derived route is absent from the generated site manifest",
        )

    def test_candidate_framing_and_validation_digest_are_locked_until_rework(self) -> None:
        repository = self.repository(local_origin=True)
        checkpoint, _, _ = repository.prepare_candidate()
        before = checkpoint.read_bytes()
        for arguments, expected in (
            (("--scope-summary", "Changed acceptance scope."), "change framing fields only after returning to REWORK"),
            (("--local-validation", "pass"), "record local validation again only after returning to REWORK"),
        ):
            with self.subTest(arguments=arguments):
                observed = repository.cli("record", "--checkpoint", str(checkpoint), *arguments)
                self.assert_deterministic_error(observed, contains=expected)
                self.assertEqual(before, checkpoint.read_bytes())

    def test_local_validation_digest_survives_unchanged_commit_and_rejects_changed_bytes(self) -> None:
        repository = self.repository(local_origin=True)
        checkpoint, _, result = repository.new_checkpoint()
        self.assertEqual(0, result.returncode, result.stderr)
        repository.install_fake_release_tools()
        repository.write_text(
            "docs/workflow-test.md",
            "# Workflow test\n\nValidated before its candidate commit.\n",
        )
        repository.write_text("site/workflow-test.json", '{"validated": true}\n')
        manifest = repository.root / "_site" / "content-manifest.json"
        manifest.parent.mkdir(parents=True, exist_ok=True)
        manifest.write_text(
            json.dumps(
                {
                    "items": [
                        {
                            "path": "docs/workflow-test.md",
                            "route": "#/doc/workflow-test",
                        }
                    ],
                    "presentation": [],
                    "audiences": [],
                    "presentationDecks": [],
                }
            ),
            encoding="utf-8",
        )

        validated = repository.cli(
            "record",
            "--checkpoint",
            str(checkpoint),
            "--local-validation",
            "pass",
        )
        self.assertEqual(0, validated.returncode, validated.stdout + validated.stderr)
        precommit = json.loads(checkpoint.read_text(encoding="utf-8"))
        digest = precommit["localValidationDigest"]
        self.assertRegex(digest, r"^[0-9a-f]{64}$")

        repository.commit_all("Commit the unchanged prevalidated source tree")
        module = repository.load_module("scripts/study_workflow.py")
        self.assertEqual(digest, module.source_tree_digest())
        precommit.update(
            {
                "canonicalState": "PROJECTED",
                "statusReason": "The prevalidated bytes are now committed without changes.",
                "artifactType": "workflow",
                "audiences": ["repository maintainers"],
                "scopeSummary": "Binding local validation to the exact candidate source tree.",
                "deltaSummary": "A deterministic validation digest regression fixture.",
                "evidenceReferences": ["https://example.com/evidence/validation-digest"],
                "canonicalPaths": ["docs/workflow-test.md"],
                "derivedPaths": ["site/workflow-test.json", "#/doc/workflow-test"],
                "nextGate": "Create a draft candidate from the unchanged validated bytes.",
            }
        )
        repository.replace_checkpoint(checkpoint, precommit)
        unchanged = repository.cli(
            "check",
            "--checkpoint",
            str(checkpoint),
            "--phase",
            "draft",
            "--base",
            repository.base_sha,
        )
        self.assertEqual(0, unchanged.returncode, unchanged.stdout + unchanged.stderr)

        repository.write_text(
            "docs/workflow-test.md",
            "# Workflow test\n\nChanged after the recorded validation pass.\n",
        )
        changed = repository.cli(
            "check",
            "--checkpoint",
            str(checkpoint),
            "--phase",
            "draft",
            "--base",
            repository.base_sha,
        )
        self.assert_deterministic_error(
            changed,
            contains="current source tree differs from the locally validated digest",
        )

    def test_minimal_projected_checkpoint_passes_the_draft_gate(self) -> None:
        repository = self.repository(local_origin=True)
        checkpoint, _, _ = repository.prepare_draft()
        result = repository.cli(
            "check",
            "--checkpoint",
            str(checkpoint),
            "--phase",
            "draft",
            "--base",
            repository.base_sha,
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_draft_gate_rejects_validation_command_failure(self) -> None:
        repository = self.repository(local_origin=True)
        checkpoint, _, _ = repository.prepare_draft()
        result = repository.cli(
            "check",
            "--checkpoint",
            str(checkpoint),
            "--phase",
            "draft",
            "--base",
            repository.base_sha,
            environment={"FAKE_MAKE_RC": "1"},
        )
        self.assert_deterministic_error(
            result,
            contains="make validate failed during draft gate",
        )

    def test_check_accepts_equivalent_github_transport_but_rejects_another_repo(self) -> None:
        repository = self.repository(local_origin=True)
        checkpoint, data, _ = repository.prepare_draft()
        repository.git("remote", "set-url", "origin", "git@github.com:owner/repo.git")
        transport = repository.install_fake_ssh_transport()

        data["repositoryRemote"] = "https://github.com/owner/repo.git"
        repository.replace_checkpoint(checkpoint, data)
        equivalent = repository.cli(
            "check",
            "--checkpoint",
            str(checkpoint),
            "--phase",
            "draft",
            "--base",
            repository.base_sha,
            environment=transport,
        )
        self.assertEqual(0, equivalent.returncode, equivalent.stdout + equivalent.stderr)

        data["repositoryRemote"] = "https://github.com/other/repo.git"
        repository.replace_checkpoint(checkpoint, data)
        different = repository.cli(
            "check",
            "--checkpoint",
            str(checkpoint),
            "--phase",
            "draft",
            "--base",
            repository.base_sha,
            environment=transport,
        )
        self.assert_deterministic_error(
            different,
            contains="checkpoint repositoryRemote differs from origin",
        )

    def test_draft_gate_rejects_base_branch_validation_state_and_canonical_path_failures(self) -> None:
        repository = self.repository(local_origin=True)
        checkpoint, valid, head = repository.prepare_draft()
        cases: dict[str, tuple[dict[str, Any], str, str | None]] = {
            "base mismatch": ({}, head, "--base does not match checkpoint baseSha"),
            "local validation pending": (
                {"localValidation": "pending", "localValidationDigest": None},
                repository.base_sha,
                "checkpoint localValidation must be pass",
            ),
            "state too early": (
                {"canonicalState": "FRAMED"},
                repository.base_sha,
                "checkpoint state is not ready",
            ),
            "no canonical path": (
                {"canonicalPaths": []},
                repository.base_sha,
                "at least one canonical path",
            ),
            "missing canonical file": (
                {"canonicalPaths": ["docs/missing-study.md"]},
                repository.base_sha,
                "canonical path does not exist",
            ),
        }
        failures: list[str] = []
        for label, (changes, supplied_base, expected) in cases.items():
            with self.subTest(case=label):
                candidate = dict(valid)
                candidate.update(changes)
                repository.replace_checkpoint(checkpoint, candidate)
                observed = repository.cli(
                    "check",
                    "--checkpoint",
                    str(checkpoint),
                    "--phase",
                    "draft",
                    "--base",
                    supplied_base,
                )
                output = observed.stdout + observed.stderr
                if observed.returncode != 2 or expected not in output or "Traceback" in output:
                    failures.append(f"{label}: rc={observed.returncode}, output={output!r}")

        repository.replace_checkpoint(checkpoint, valid)
        repository.git("switch", "-q", "main")
        branch_candidate = dict(valid)
        branch_candidate["canonicalPaths"] = ["docs/46-study-publication-workflow.md"]
        branch_candidate["derivedPaths"] = ["#/doc/workflow-test"]
        repository.replace_checkpoint(checkpoint, branch_candidate)
        branch = repository.cli(
            "check",
            "--checkpoint",
            str(checkpoint),
            "--phase",
            "draft",
            "--base",
            repository.base_sha,
        )
        if branch.returncode != 2 or "current branch does not match" not in branch.stderr:
            failures.append(f"branch mismatch: rc={branch.returncode}, output={(branch.stdout + branch.stderr)!r}")
        self.assertEqual([], failures)

    def test_candidate_draft_gate_rejects_dirty_bytes_and_committed_head_drift(self) -> None:
        repository = self.repository(local_origin=True)
        checkpoint, _, candidate_head = repository.prepare_candidate()

        repository.write_text(
            "docs/workflow-test.md",
            "# Workflow test\n\nSafe but uncommitted candidate edit.\n",
        )
        dirty = repository.cli(
            "check",
            "--checkpoint",
            str(checkpoint),
            "--phase",
            "draft",
            "--base",
            repository.base_sha,
        )
        self.assert_deterministic_error(
            dirty,
            contains="current source tree differs from the locally validated digest",
        )

        repository.write_text(
            "docs/workflow-test.md",
            "# Workflow test\n\nPublic-safe canonical fixture.\n",
        )
        repository.git("commit", "--allow-empty", "-q", "-m", "Commit post-candidate head drift")
        drifted_head = repository.git("rev-parse", "HEAD").stdout.strip()
        self.assertNotEqual(candidate_head, drifted_head)
        drifted = repository.cli(
            "check",
            "--checkpoint",
            str(checkpoint),
            "--phase",
            "draft",
            "--base",
            repository.base_sha,
        )
        self.assert_deterministic_error(
            drifted,
            contains="draft gate candidate, PR head, and HEAD SHAs must be identical",
        )

    def test_candidate_draft_gate_requires_commit_push_and_pr_authority(self) -> None:
        repository = self.repository(local_origin=True)
        checkpoint, data, candidate = repository.prepare_candidate()
        data["requestedActions"] = ["edit", "branch"]
        repository.replace_checkpoint(checkpoint, data)
        pr = repository.with_current_checkpoint_body(
            repository.valid_pr_json(candidate, draft=True), checkpoint
        )
        observed = repository.cli(
            "check",
            "--checkpoint",
            str(checkpoint),
            "--phase",
            "draft",
            "--base",
            repository.base_sha,
            environment=repository.fake_github_environment(pr, candidate),
        )
        self.assert_deterministic_error(
            observed,
            contains="draft gate lacks explicit authority for: commit, pull-request, push",
        )

    def test_candidate_draft_gate_requires_the_actual_pr_and_exact_checkpoint_block(self) -> None:
        repository = self.repository(local_origin=True)
        checkpoint, _, head = repository.prepare_candidate()
        valid_pr = repository.with_current_checkpoint_body(
            repository.valid_pr_json(head, draft=True), checkpoint
        )

        accepted = repository.cli(
            "check",
            "--checkpoint",
            str(checkpoint),
            "--phase",
            "draft",
            "--base",
            repository.base_sha,
            environment={"FAKE_PR_JSON": json.dumps(valid_pr)},
        )
        self.assertEqual(0, accepted.returncode, accepted.stdout + accepted.stderr)

        cases: dict[str, tuple[dict[str, Any], str]] = {
            "missing PR payload": ({}, "actual PR number differs from the checkpoint"),
            "wrong PR identity": (
                {**valid_pr, "url": "https://github.com/owner/repo/pull/999"},
                "actual PR URL/repository differs from origin and the checkpoint",
            ),
            "wrong PR number": (
                {**valid_pr, "number": 99},
                "actual PR number differs from the checkpoint",
            ),
            "wrong head repository owner": (
                {**valid_pr, "headRepositoryOwner": {"login": "other-owner"}},
                "actual PR head repository owner differs from origin",
            ),
            "missing checkpoint block": (
                {**valid_pr, "body": "No durable workflow checkpoint is present."},
                "PR body must contain exactly one workflow checkpoint block",
            ),
            "stale checkpoint block": (
                {
                    **valid_pr,
                    "body": (
                        "<!-- study-workflow-checkpoint:start -->\n"
                        "stale but public-safe payload\n"
                        "<!-- study-workflow-checkpoint:end -->"
                    ),
                },
                "PR checkpoint block is stale or differs from the validated local checkpoint",
            ),
        }
        for label, (pr, expected) in cases.items():
            with self.subTest(case=label):
                observed = repository.cli(
                    "check",
                    "--checkpoint",
                    str(checkpoint),
                    "--phase",
                    "draft",
                    "--base",
                    repository.base_sha,
                    environment={"FAKE_PR_JSON": json.dumps(pr)},
                )
                self.assert_deterministic_error(observed, contains=expected)


class ValidationEnvironmentTests(WorkflowTestCase):
    def test_draft_gate_does_not_execute_an_ambient_path_make(self) -> None:
        repository = self.repository(local_origin=True)
        checkpoint, _, _ = repository.prepare_draft()
        hostile_bin = repository.container / "hostile-bin"
        hostile_bin.mkdir()
        marker = repository.container / "ambient-make-was-executed"
        hostile_make = hostile_bin / "make"
        hostile_make.write_text(
            f"#!/bin/sh\n: > {marker}\nexit 0\n",
            encoding="utf-8",
        )
        hostile_make.chmod(hostile_make.stat().st_mode | stat.S_IXUSR)
        observed = repository.cli(
            "check",
            "--checkpoint",
            str(checkpoint),
            "--phase",
            "draft",
            "--base",
            repository.base_sha,
            environment={
                "PATH": os.pathsep.join(
                    (str(hostile_bin), str(repository.tool_bin), repository.environment.get("PATH", ""))
                ),
                "FAKE_MAKE_RC": "7",
            },
        )
        self.assert_deterministic_error(
            observed,
            contains="make validate failed during draft gate",
        )
        self.assertFalse(marker.exists(), "draft gate executed ambient PATH make")

    def test_publication_commands_ignore_repository_make_gh_and_python_redirectors(self) -> None:
        repository = self.repository(local_origin=True)
        hostile_python = repository.container / "hostile-python"
        hostile_python.mkdir()
        (hostile_python / "sitecustomize.py").write_text(
            "raise SystemExit(91)\n", encoding="utf-8"
        )
        redirected_git = repository.container / "redirected.git"
        repository._run(("git", "init", "--bare", "-q", str(redirected_git)), cwd=repository.container)
        environment = {
            "GIT_DIR": str(redirected_git),
            "GIT_WORK_TREE": str(repository.container / "wrong-worktree"),
            "GIT_CONFIG_PARAMETERS": "'core.hooksPath=/definitely-not-a-workflow-hook'",
            "GIT_CONFIG_COUNT": "1",
            "GIT_CONFIG_KEY_0": "remote.origin.pushurl",
            "GIT_CONFIG_VALUE_0": str(redirected_git),
            "GIT_GLOB_PATHSPECS": "1",
            "GIT_LITERAL_PATHSPECS": "1",
            "GIT_ICASE_PATHSPECS": "1",
            "GH_REPO": "cli/cli",
            "GH_HOST": "example.invalid",
            "MAKEFLAGS": "-n -i",
            "GNUMAKEFLAGS": "-n",
            "PYTHONPATH": str(hostile_python),
            "PYTHONHOME": str(hostile_python),
        }
        checkpoint, _, created = repository.new_checkpoint(
            slug="environment-isolation", environment=environment
        )
        self.assertEqual(0, created.returncode, created.stdout + created.stderr)
        repository.write_text("docs/workflow-test.md", "# Workflow test\n\nEnvironment isolation.\n")
        validated = repository.cli(
            "record",
            "--checkpoint",
            str(checkpoint),
            "--local-validation",
            "pass",
            environment=environment,
        )
        self.assertEqual(0, validated.returncode, validated.stdout + validated.stderr)

    def test_draft_and_release_make_inherit_the_running_python_virtualenv(self) -> None:
        draft_repository = self.repository(local_origin=True)
        runtime = draft_repository.container / "workflow-runtime"
        created = draft_repository._run(
            (sys.executable, "-m", "venv", "--without-pip", str(runtime)),
            cwd=draft_repository.container,
        )
        self.assertEqual(0, created.returncode, created.stdout + created.stderr)
        runtime_python = runtime / "bin" / "python"
        runtime_bin = str(runtime_python.parent.resolve())
        self.assertNotIn(
            runtime_bin,
            draft_repository.environment.get("PATH", "").split(os.pathsep),
        )

        draft_checkpoint, _, _ = draft_repository.prepare_draft()
        draft = draft_repository.cli(
            "check",
            "--checkpoint",
            str(draft_checkpoint),
            "--phase",
            "draft",
            "--base",
            draft_repository.base_sha,
            environment={"EXPECTED_PYTHON_BIN": runtime_bin},
            python_executable=runtime_python,
        )
        self.assertEqual(0, draft.returncode, draft.stdout + draft.stderr)

        release_repository = self.repository(local_origin=True)
        release_checkpoint, _, head = release_repository.prepare_release()
        pr = release_repository.with_current_checkpoint_body(
            release_repository.valid_pr_json(head), release_checkpoint
        )
        release = release_repository.cli(
            "check",
            "--checkpoint",
            str(release_checkpoint),
            "--phase",
            "release",
            "--base",
            release_repository.base_sha,
            environment={
                **release_repository.fake_github_environment(pr, head),
                "EXPECTED_PYTHON_BIN": runtime_bin,
            },
            python_executable=runtime_python,
        )
        self.assertEqual(0, release.returncode, release.stdout + release.stderr)


class ReleaseGateTests(WorkflowTestCase):
    def test_release_gate_rejects_a_fetched_main_ref_not_authenticated_by_github(self) -> None:
        repository = self.repository(local_origin=True)
        checkpoint, _, head = repository.prepare_release()
        pr = repository.with_current_checkpoint_body(repository.valid_pr_json(head), checkpoint)
        environment = repository.fake_github_environment(pr, head)
        environment["FAKE_MAIN_REF_JSON"] = json.dumps(
            [{"ref": "refs/heads/main", "object": {"sha": head}}]
        )
        observed = repository.cli(
            "check", "--checkpoint", str(checkpoint), "--phase", "release", "--base", repository.base_sha,
            environment=environment,
        )
        self.assert_deterministic_error(
            observed,
            contains="fetched origin/main differs from the authoritative GitHub main ref",
        )

    def test_release_gate_passes_with_local_fake_pr_and_validation_tools(self) -> None:
        repository = self.repository(local_origin=True)
        checkpoint, _, head = repository.prepare_release()
        pr = repository.with_current_checkpoint_body(repository.valid_pr_json(head), checkpoint)
        environment = repository.fake_github_environment(pr, head)
        observed = repository.cli(
            "check",
            "--checkpoint",
            str(checkpoint),
            "--phase",
            "release",
            "--base",
            repository.base_sha,
            environment=environment,
        )
        self.assertEqual(0, observed.returncode, observed.stdout + observed.stderr)

    def test_release_gate_rejects_candidate_behind_current_origin_main(self) -> None:
        repository = self.repository(local_origin=True)
        checkpoint, data, head = repository.prepare_release()
        repository.git("switch", "-q", "main")
        repository.write_text("docs/concurrent-main.md", "# Concurrent main update\n")
        repository.commit_all("Advance origin main after candidate validation")
        repository.git("push", "-q", "origin", "main")
        repository.git("switch", "-q", data["branch"])

        pr = repository.with_current_checkpoint_body(
            repository.valid_pr_json(head), checkpoint
        )
        observed = repository.cli(
            "check",
            "--checkpoint",
            str(checkpoint),
            "--phase",
            "release",
            "--base",
            repository.base_sha,
            environment=repository.fake_github_environment(pr, head),
        )
        self.assert_deterministic_error(
            observed,
            contains="release candidate must be rebased onto the current origin/main",
        )

    def test_release_gate_rejects_dirty_review_check_sha_pr_state_and_validation_failures(self) -> None:
        repository = self.repository(local_origin=True)
        checkpoint, valid, head = repository.prepare_release()
        valid_pr = repository.valid_pr_json(head)

        cases: list[tuple[str, dict[str, Any], dict[str, Any], str, str]] = [
            (
                "missing edit authority",
                {"requestedActions": [value for value in valid["requestedActions"] if value != "edit"]},
                valid_pr,
                "0",
                "release gate lacks explicit authority for: edit",
            ),
            (
                "review not accepted",
                {"reviewDisposition": "conditional"},
                valid_pr,
                "0",
                "reviewDisposition must be pass",
            ),
            (
                "checks not green",
                {"checkDisposition": "failed"},
                valid_pr,
                "0",
                "checkDisposition must be green",
            ),
            (
                "recorded SHA drift",
                {"acceptedSha": repository.base_sha},
                valid_pr,
                "0",
                "acceptedSha must equal candidateSha",
            ),
            ("missing PR", {"prNumber": None}, valid_pr, "0", "prNumber is required"),
            (
                "actual PR head drift",
                {},
                {**valid_pr, "headRefOid": repository.base_sha},
                "0",
                "actual PR branch/head differs",
            ),
            (
                "actual PR remains draft",
                {},
                {**valid_pr, "isDraft": True},
                "0",
                "actual PR open/draft state differs from the checkpoint",
            ),
            (
                "actual checks missing",
                {},
                {**valid_pr, "statusCheckRollup": []},
                "0",
                "actual PR checks are missing",
            ),
            (
                "recorded check URL drift",
                {"checkUrls": ["https://github.com/owner/repo/actions/runs/999"]},
                valid_pr,
                "0",
                "recorded check URLs differ from the authenticated required runs",
            ),
            (
                "state is not validated",
                {"canonicalState": "REVIEWED"},
                valid_pr,
                "0",
                "canonicalState VALIDATED",
            ),
            ("make validate fails", {}, valid_pr, "1", "make validate failed"),
        ]

        failures: list[str] = []
        for label, changes, pr, make_rc, expected in cases:
            with self.subTest(case=label):
                candidate = dict(valid)
                candidate.update(changes)
                repository.replace_checkpoint(checkpoint, candidate)
                current_pr = repository.with_current_checkpoint_body(pr, checkpoint)
                observed = repository.cli(
                    "check",
                    "--checkpoint",
                    str(checkpoint),
                    "--phase",
                    "release",
                    "--base",
                    repository.base_sha,
                    environment={
                        **repository.fake_github_environment(current_pr, head),
                        "FAKE_MAKE_RC": make_rc,
                    },
                )
                output = observed.stdout + observed.stderr
                if observed.returncode != 2 or expected not in output or "Traceback" in output:
                    failures.append(f"{label}: rc={observed.returncode}, output={output!r}")

        repository.replace_checkpoint(checkpoint, valid)
        valid_pr = repository.with_current_checkpoint_body(valid_pr, checkpoint)
        scratch = repository.write_text("scratch.txt", "safe dirty fixture\n")
        dirty = repository.cli(
            "check",
            "--checkpoint",
            str(checkpoint),
            "--phase",
            "release",
            "--base",
            repository.base_sha,
            environment=repository.fake_github_environment(valid_pr, head),
        )
        scratch.unlink()
        if dirty.returncode != 2 or "current source tree differs from the locally validated digest" not in dirty.stderr:
            failures.append(f"dirty tree: rc={dirty.returncode}, output={(dirty.stdout + dirty.stderr)!r}")
        self.assertEqual([], failures)

    def test_release_gate_rejects_spoofed_statuses_and_action_runs_for_another_sha(self) -> None:
        repository = self.repository(local_origin=True)
        checkpoint, _, head = repository.prepare_release()
        valid_pr = repository.with_current_checkpoint_body(
            repository.valid_pr_json(head), checkpoint
        )

        spoofed = dict(valid_pr)
        spoofed["statusCheckRollup"] = [
            {
                "name": "static-validation",
                "conclusion": "SUCCESS",
                "workflowName": "external-status",
                "detailsUrl": "https://ci.example.invalid/static-validation",
            },
            {
                "name": "docker-smoke",
                "conclusion": "SUCCESS",
                "workflowName": "external-status",
                "detailsUrl": "https://ci.example.invalid/docker-smoke",
            },
        ]
        spoofed_result = repository.cli(
            "check",
            "--checkpoint",
            str(checkpoint),
            "--phase",
            "release",
            "--base",
            repository.base_sha,
            environment=repository.fake_github_environment(spoofed, head),
        )
        self.assert_deterministic_error(
            spoofed_result,
            contains="not authenticated required GitHub Actions jobs",
        )

        wrong_sha_environment = repository.fake_github_environment(valid_pr, head)
        wrong_sha_environment["FAKE_RUN_201_JSON"] = json.dumps(
            {
                "headSha": repository.base_sha,
                "status": "completed",
                "conclusion": "success",
                "url": "https://github.com/owner/repo/actions/runs/201",
                "workflowName": "validate",
            }
        )
        wrong_sha = repository.cli(
            "check",
            "--checkpoint",
            str(checkpoint),
            "--phase",
            "release",
            "--base",
            repository.base_sha,
            environment=wrong_sha_environment,
        )
        self.assert_deterministic_error(
            wrong_sha,
            contains="not authenticated required GitHub Actions jobs",
        )


class PagesDeadlineTests(unittest.TestCase):
    def test_queued_targets_cannot_extend_the_overall_deadline(self) -> None:
        verifier = load_pages_verifier_module()
        started: list[str] = []

        def slow_target(
            _base_url: str,
            target: Any,
            _token: str,
            _timeout: float,
            _deadline: float,
        ) -> None:
            started.append(target.label)
            time.sleep(0.2)

        targets = [
            verifier.Target(f"content/{index}.md", "0" * 64, 1, f"target {index}")
            for index in range(20)
        ]
        began = time.monotonic()
        with mock.patch.object(verifier, "verify_target", side_effect=slow_target):
            with self.assertRaisesRegex(verifier.VerificationError, "overall verification deadline expired"):
                verifier.verify_targets(
                    "https://example.invalid/studies/",
                    targets,
                    "deadline-test",
                    30.0,
                    1,
                    time.monotonic() + 0.03,
                )
        elapsed = time.monotonic() - began
        self.assertLess(elapsed, 0.15)
        self.assertLessEqual(len(started), 1)
        # Let the one already-running daemon-independent worker finish before the
        # temporary module is released; the assertion above measures gate latency.
        time.sleep(0.22)

    def test_published_gate_bounds_the_verifier_subprocess(self) -> None:
        workflow = load_production_module()
        data = {
            "liveBaseUrl": "https://example.invalid/studies/",
            "manifestSha256": "0" * 64,
            "canonicalPaths": ["docs/workflow-test.md"],
            "routeAssertions": ["#/doc/workflow-test"],
        }
        timeout_error = subprocess.TimeoutExpired(("python", "verify_pages.py"), 660)
        with mock.patch.object(workflow, "run", return_value=SimpleNamespace(returncode=0)), mock.patch.object(
            workflow.subprocess, "run", side_effect=timeout_error
        ) as invoked:
            self.assertFalse(workflow.run_pages_verifier(data, "1" * 40))
        self.assertEqual(660, invoked.call_args.kwargs["timeout"])


class PublishedGateTests(WorkflowTestCase):
    def prepare_published(
        self,
        repository: TemporaryWorkflowRepository,
        *,
        clean_branch: bool = True,
        deleted_sensitive_history: bool = False,
        force_tracked_ignored_artifact: bool = False,
    ) -> tuple[Path, dict[str, Any], str, str]:
        checkpoint, data, candidate = repository.prepare_release()
        if deleted_sensitive_history:
            repository.write_text(
                "docs/deleted-sensitive.md",
                "Authorization: Bearer " + "q" * 24 + "\n",
            )
            repository.commit_all("Add temporary sensitive history fixture")
            (repository.root / "docs" / "deleted-sensitive.md").unlink()
            candidate = repository.commit_all("Delete temporary sensitive history fixture")
        if force_tracked_ignored_artifact:
            ignore_path = repository.root / ".gitignore"
            repository.write_text(
                ".gitignore",
                ignore_path.read_text(encoding="utf-8") + "\nprivate-artifact.txt\n",
            )
            repository.write_text("private-artifact.txt", "safe ignored artifact fixture\n")
            repository.git("add", ".gitignore")
            repository.git("add", "-f", "private-artifact.txt")
            repository.git("commit", "-q", "-m", "Add force-tracked ignored artifact fixture")
            candidate = repository.git("rev-parse", "HEAD").stdout.strip()
        if deleted_sensitive_history or force_tracked_ignored_artifact:
            module = repository.load_module("scripts/study_workflow.py")
            data.update(
                {
                    "candidateSha": candidate,
                    "prHeadSha": candidate,
                    "acceptedSha": candidate,
                    "checkedSha": candidate,
                    "localValidationDigest": module.source_tree_digest(),
                }
            )
            data["candidateEnvelopeSha256"] = module.candidate_envelope_digest(data)
            repository.replace_checkpoint(checkpoint, data)
            repository.git("push", "-q", "origin", f"{candidate}:refs/heads/{data['branch']}")
            repository.publish_pull_head(17, candidate)
        repository.git("switch", "-q", "main")
        repository.git("merge", "-q", "--squash", candidate)
        merge_sha = repository.commit_all("Squash the accepted publication candidate")
        self.assertNotEqual(candidate, merge_sha)
        repository.git("push", "-q", "origin", "main")
        if clean_branch:
            repository.git("update-ref", "-d", "refs/heads/study/workflow-test")
            repository.git("push", "-q", "origin", "--delete", "study/workflow-test")
        manifest_sha = "b" * 64
        routes = ["#/doc/workflow-test"]
        data.update(
            {
                "canonicalState": "PUBLISHED",
                "statusReason": "Main validation, Pages, and live parity are verified.",
                "mergeSha": merge_sha,
                "branchCleanupStatus": "complete",
                "cleanupEvidence": ["https://example.com/branches/workflow-test"],
                "mainValidationUrl": "https://github.com/owner/repo/actions/runs/101",
                "pagesRunUrl": "https://github.com/owner/repo/actions/runs/102",
                "manifestSha256": manifest_sha,
                "closureEvidenceUrl": "https://github.com/owner/repo/pull/17#issuecomment-100",
                "liveBaseUrl": "https://example.com/studies/",
                "derivedPaths": ["site/workflow-test.json", *routes],
                "manifestAssertions": [
                    f"sourceRevision={merge_sha}",
                    f"manifestSha256={manifest_sha}",
                    "sourceDirty=false",
                ],
                "routeAssertions": routes,
                "publicationStatus": "published",
                "residualLimitations": ["No organization-specific fit is inferred."],
                "nextGate": "Run the next independently reviewed evidence intake.",
            }
        )
        repository.replace_checkpoint(checkpoint, data)
        return checkpoint, data, candidate, merge_sha

    def test_published_gate_accepts_clean_later_main_with_merge_as_ancestor(self) -> None:
        repository = self.repository(local_origin=True)
        repository.write_text(
            "scripts/verify_pages.py",
            "#!/usr/bin/env python3\nraise SystemExit(0)\n",
        )
        repository.base_sha = repository.commit_all(
            "Install the hermetic Pages verifier fixture"
        )
        repository.git("push", "-q", "origin", "main")
        checkpoint, data, candidate, merge_sha = self.prepare_published(repository)
        repository.write_text(
            "docs/later-main.md",
            "# Later main\n\nA safe repository change after publication.\n",
        )
        later_main = repository.commit_all("Advance main after the verified publication")
        repository.git("push", "-q", "origin", "main")
        self.assertNotEqual(merge_sha, later_main)
        self.assertEqual(
            0,
            repository._run(
                ("git", "merge-base", "--is-ancestor", merge_sha, later_main)
            ).returncode,
        )

        pr = repository.with_current_checkpoint_body(
            repository.valid_pr_json(candidate, merged=True, merge_sha=merge_sha), checkpoint
        )
        environment = repository.fake_github_environment(pr, candidate)
        environment.update(
            {
                "FAKE_RUN_101_JSON": json.dumps(
                    {
                        "headSha": merge_sha,
                        "status": "completed",
                        "conclusion": "success",
                        "url": data["mainValidationUrl"],
                        "workflowName": "validate",
                    }
                ),
                "FAKE_RUN_102_JSON": json.dumps(
                    {
                        "headSha": merge_sha,
                        "status": "completed",
                        "conclusion": "success",
                        "url": data["pagesRunUrl"],
                        "workflowName": "pages",
                    }
                ),
                "FAKE_PAGES_JSON": json.dumps({"html_url": data["liveBaseUrl"]}),
                "FAKE_CLOSURE_COMMENT_JSON": json.dumps(
                    {
                        "html_url": data["closureEvidenceUrl"],
                        "issue_url": "https://api.github.com/repos/owner/repo/issues/17",
                        "body": (
                            "Publication status: published\n"
                            f"Merge SHA: {merge_sha}\n"
                            f"Manifest SHA-256: {data['manifestSha256']}\n"
                        ),
                    }
                ),
            }
        )
        observed = repository.cli(
            "check",
            "--checkpoint",
            str(checkpoint),
            "--phase",
            "published",
            "--base",
            repository.base_sha,
            environment=environment,
        )
        self.assertEqual(0, observed.returncode, observed.stdout + observed.stderr)
        self.assertEqual(later_main, repository.git("rev-parse", "HEAD").stdout.strip())

    def test_failed_merged_publication_remains_open_until_successful_live_proof(self) -> None:
        repository = self.repository(local_origin=True)
        checkpoint, data, _, _ = self.prepare_published(repository)
        data.update(
            {
                "canonicalState": "MERGED",
                "publicationStatus": "corrective-change-required",
                "statusReason": "The merge-SHA publication requires external recovery or a successful rerun.",
                "nextGate": "Rerun the failed publication controls; do not claim closure or merge another publication.",
            }
        )
        repository.replace_checkpoint(checkpoint, data)
        before = checkpoint.read_bytes()
        observed = repository.cli(
            "record", "--checkpoint", str(checkpoint), "--state", "CLOSED"
        )
        self.assert_deterministic_error(
            observed,
            contains="invalid workflow transition: MERGED -> CLOSED",
        )
        self.assertEqual(before, checkpoint.read_bytes())

    def test_published_resume_uses_the_immutable_candidate_after_a_later_path_deletion(self) -> None:
        repository = self.repository(local_origin=True)
        checkpoint, data, candidate, merge_sha = self.prepare_published(repository)
        rendered = repository.cli("render", "--checkpoint", str(checkpoint))
        self.assertEqual(0, rendered.returncode, rendered.stdout + rendered.stderr)
        pr = repository.valid_pr_json(candidate, merged=True, merge_sha=merge_sha)
        pr["body"] = rendered.stdout.strip()

        checkpoint.unlink()
        (repository.root / "docs" / "workflow-test.md").unlink()
        later_main = repository.commit_all("Remove an old published canonical path")
        repository.git("push", "-q", "origin", "main")
        self.assertNotEqual(merge_sha, later_main)

        resumed = repository.cli(
            "resume",
            "--pr-number",
            "17",
            "--base",
            repository.base_sha,
            "--requested-actions",
            ",".join(data["requestedActions"]),
            environment=repository.fake_github_environment(pr, candidate),
        )
        self.assertEqual(0, resumed.returncode, resumed.stdout + resumed.stderr)
        result = json.loads(resumed.stdout)
        restored = repository.root / result["checkpoint"]
        restored_data = json.loads(restored.read_text(encoding="utf-8"))
        self.assertEqual("PUBLISHED", result["state"])
        self.assertEqual("PUBLISHED", restored_data["canonicalState"])
        self.assertEqual(candidate, restored_data["candidateSha"])
        self.assertEqual(merge_sha, restored_data["mergeSha"])
        self.assertFalse((repository.root / "docs" / "workflow-test.md").exists())
    def test_published_gate_rejects_an_intake_branch_that_was_not_cleaned(self) -> None:
        repository = self.repository(local_origin=True)
        checkpoint, _, candidate, merge_sha = self.prepare_published(repository, clean_branch=False)
        pr = repository.with_current_checkpoint_body(
            repository.valid_pr_json(candidate, merged=True, merge_sha=merge_sha), checkpoint
        )
        observed = repository.cli(
            "check",
            "--checkpoint",
            str(checkpoint),
            "--phase",
            "published",
            "--base",
            repository.base_sha,
            environment=repository.fake_github_environment(pr, candidate),
        )
        self.assert_deterministic_error(observed, contains="local intake branch still exists")

    def test_published_gate_rejects_a_branch_that_still_exists_on_github(self) -> None:
        repository = self.repository(local_origin=True)
        checkpoint, _, candidate, merge_sha = self.prepare_published(repository)
        pr = repository.with_current_checkpoint_body(
            repository.valid_pr_json(candidate, merged=True, merge_sha=merge_sha), checkpoint
        )
        environment = repository.fake_github_environment(pr, candidate)
        environment["FAKE_BRANCH_REF_JSON"] = json.dumps(
            [{"ref": "refs/heads/study/workflow-test", "object": {"sha": candidate}}]
        )
        observed = repository.cli(
            "check", "--checkpoint", str(checkpoint), "--phase", "published", "--base", repository.base_sha,
            environment=environment,
        )
        self.assert_deterministic_error(observed, contains="GitHub intake branch still exists")

    def test_published_gate_rejects_merge_state_status_url_assertion_and_closure_failures(self) -> None:
        repository = self.repository(local_origin=True)
        checkpoint, valid, candidate, merge_sha = self.prepare_published(repository)
        pr = repository.valid_pr_json(candidate, merged=True, merge_sha=merge_sha)
        cases: dict[str, tuple[dict[str, Any], str]] = {
            "missing merge": ({"mergeSha": None}, "mergeSha is required"),
            "unreachable merge": (
                {
                    "mergeSha": candidate,
                    "manifestAssertions": [
                        f"sourceRevision={candidate}",
                        f"manifestSha256={valid['manifestSha256']}",
                        "sourceDirty=false",
                    ],
                },
                "mergeSha is not reachable from origin/main",
            ),
            "wrong state": ({"canonicalState": "MERGED"}, "published gate requires state PUBLISHED or CLOSED"),
            "pending publication": ({"publicationStatus": "pending"}, "publicationStatus must be published"),
            "missing main validation": (
                {"mainValidationUrl": None},
                "main validation, Pages, and live URLs are required",
            ),
            "missing Pages run": (
                {"pagesRunUrl": None},
                "main validation, Pages, and live URLs are required",
            ),
            "missing live URL": (
                {"liveBaseUrl": None},
                "main validation, Pages, and live URLs are required",
            ),
            "non-public live URL": (
                {"liveBaseUrl": "http://example.invalid/studies/"},
                "must be a public HTTPS URL",
            ),
            "missing manifest assertions": (
                {"manifestAssertions": valid["manifestAssertions"][:-1]},
                "manifestAssertions must exactly bind revision, manifest digest, and clean state",
            ),
            "extra manifest assertion": (
                {"manifestAssertions": [*valid["manifestAssertions"], "resourceIdsMatch=true"]},
                "manifestAssertions must exactly bind revision, manifest digest, and clean state",
            ),
            "unknown manifest assertion": (
                {
                    "manifestAssertions": [
                        f"sourceRevision={merge_sha}",
                        f"manifestSha256={valid['manifestSha256']}",
                        "sourceDirty=unknown",
                    ]
                },
                "manifestAssertions must exactly bind revision, manifest digest, and clean state",
            ),
            "missing route assertion": (
                {"routeAssertions": valid["routeAssertions"][:-1]},
                "routeAssertions must exactly match every declared derived route",
            ),
            "extra route assertion": (
                {"routeAssertions": [*valid["routeAssertions"], "#/studies/undeclared"]},
                "routeAssertions must exactly match every declared derived route",
            ),
            "unknown route assertion": (
                {
                    "routeAssertions": [
                        valid["routeAssertions"][0],
                        "#/presentations/unknown",
                    ]
                },
                "routeAssertions must exactly match every declared derived route",
            ),
            "closed without residual limitations": (
                {"canonicalState": "CLOSED", "residualLimitations": []},
                "residual limitations are required",
            ),
            "closed without next gate": (
                {"canonicalState": "CLOSED", "nextGate": ""},
                "nextGate must be non-empty",
            ),
        }

        failures: list[str] = []
        for label, (changes, expected) in cases.items():
            with self.subTest(case=label):
                candidate_data = dict(valid)
                candidate_data.update(changes)
                repository.replace_checkpoint(checkpoint, candidate_data)
                current_pr = repository.with_current_checkpoint_body(pr, checkpoint)
                github = repository.fake_github_environment(current_pr, candidate)
                observed = repository.cli(
                    "check",
                    "--checkpoint",
                    str(checkpoint),
                    "--phase",
                    "published",
                    "--base",
                    repository.base_sha,
                    environment=github,
                )
                output = observed.stdout + observed.stderr
                if observed.returncode != 2 or expected not in output or "Traceback" in output:
                    failures.append(f"{label}: rc={observed.returncode}, output={output!r}")
        self.assertEqual([], failures)

    def test_published_gate_rejects_an_unmerged_intake_branch(self) -> None:
        repository = self.repository(local_origin=True)
        checkpoint, data, candidate, _ = self.prepare_published(repository)
        repository.replace_checkpoint(checkpoint, data)
        repository.git("switch", "-q", "-c", "study/workflow-test", candidate)
        observed = repository.cli(
            "check",
            "--checkpoint",
            str(checkpoint),
            "--phase",
            "published",
            "--base",
            repository.base_sha,
        )
        self.assert_deterministic_error(observed, contains="main")

    def test_published_gate_reauthenticates_review_checks_and_exact_durable_body(self) -> None:
        repository = self.repository(local_origin=True)
        checkpoint, _, candidate, merge_sha = self.prepare_published(repository)
        exact_pr = repository.with_current_checkpoint_body(
            repository.valid_pr_json(candidate, merged=True, merge_sha=merge_sha), checkpoint
        )
        cases = {
            "stale durable body": (
                {**exact_pr, "body": "No current workflow checkpoint."},
                {},
                "PR body must contain exactly one workflow checkpoint block",
            ),
            "missing candidate checks": (
                {**exact_pr, "statusCheckRollup": []},
                {},
                "actual PR checks are missing",
            ),
            "forged review": (
                exact_pr,
                {
                    "FAKE_COMMENT_JSON": json.dumps(
                        {
                            "html_url": "https://github.com/owner/repo/pull/17#issuecomment-99",
                            "issue_url": "https://api.github.com/repos/owner/repo/issues/17",
                            "body": "Review disposition: pass\n",
                        }
                    )
                },
                "independent review evidence",
            ),
        }
        for label, (pr, overrides, expected) in cases.items():
            with self.subTest(case=label):
                environment = repository.fake_github_environment(pr, candidate)
                environment.update(overrides)
                observed = repository.cli(
                    "check", "--checkpoint", str(checkpoint), "--phase", "published", "--base", repository.base_sha,
                    environment=environment,
                )
                self.assert_deterministic_error(observed, contains=expected)

    def test_published_gate_reauthenticates_the_raw_candidate_tree_after_squash(self) -> None:
        repository = self.repository(local_origin=True)
        checkpoint, original, candidate, merge_sha = self.prepare_published(repository)
        module = repository.load_module("scripts/study_workflow.py")

        cases = {
            "forged validation digest": (
                {"localValidationDigest": "f" * 64},
                "accepted candidate tree differs from the recorded local-validation digest",
            ),
            "generated derived artifact": (
                {"derivedPaths": [*original["derivedPaths"], "_site/content-manifest.json"]},
                "accepted derived path is generated, private, or workflow-local",
            ),
        }
        for label, (changes, expected) in cases.items():
            with self.subTest(case=label):
                rewritten = dict(original)
                rewritten.update(changes)
                rewritten["candidateEnvelopeSha256"] = module.candidate_envelope_digest(rewritten)
                repository.replace_checkpoint(checkpoint, rewritten)
                pr = repository.with_current_checkpoint_body(
                    repository.valid_pr_json(candidate, merged=True, merge_sha=merge_sha), checkpoint
                )
                observed = repository.cli(
                    "check", "--checkpoint", str(checkpoint), "--phase", "published",
                    "--base", repository.base_sha,
                    environment=repository.fake_github_environment(pr, candidate),
                )
                self.assert_deterministic_error(observed, contains=expected)

    def test_published_gate_rescans_deleted_candidate_history(self) -> None:
        repository = self.repository(local_origin=True)
        checkpoint, _, candidate, merge_sha = self.prepare_published(
            repository,
            deleted_sensitive_history=True,
        )
        pr = repository.with_current_checkpoint_body(
            repository.valid_pr_json(candidate, merged=True, merge_sha=merge_sha), checkpoint
        )
        observed = repository.cli(
            "check", "--checkpoint", str(checkpoint), "--phase", "published",
            "--base", repository.base_sha,
            environment=repository.fake_github_environment(pr, candidate),
        )
        self.assert_deterministic_error(observed, contains="PS009")

    def test_published_gate_rejects_a_force_tracked_ignored_candidate_artifact(self) -> None:
        repository = self.repository(local_origin=True)
        checkpoint, data, candidate, merge_sha = self.prepare_published(
            repository,
            force_tracked_ignored_artifact=True,
        )
        data["derivedPaths"] = [*data["derivedPaths"], "private-artifact.txt"]
        module = repository.load_module("scripts/study_workflow.py")
        data["candidateEnvelopeSha256"] = module.candidate_envelope_digest(data)
        repository.replace_checkpoint(checkpoint, data)
        pr = repository.with_current_checkpoint_body(
            repository.valid_pr_json(candidate, merged=True, merge_sha=merge_sha), checkpoint
        )
        observed = repository.cli(
            "check", "--checkpoint", str(checkpoint), "--phase", "published",
            "--base", repository.base_sha,
            environment=repository.fake_github_environment(pr, candidate),
        )
        self.assert_deterministic_error(
            observed,
            contains="accepted derived path is ignored or private",
        )

    def test_published_gate_rejects_a_pull_ref_that_differs_from_the_pr_head(self) -> None:
        repository = self.repository(local_origin=True)
        checkpoint, _, candidate, merge_sha = self.prepare_published(repository)
        repository.publish_pull_head(17, repository.base_sha)
        pr = repository.with_current_checkpoint_body(
            repository.valid_pr_json(candidate, merged=True, merge_sha=merge_sha), checkpoint
        )
        observed = repository.cli(
            "check", "--checkpoint", str(checkpoint), "--phase", "published",
            "--base", repository.base_sha,
            environment=repository.fake_github_environment(pr, candidate),
        )
        self.assert_deterministic_error(
            observed,
            contains="fetched merged-PR candidate differs from the authenticated PR head",
        )

    def test_published_gate_rejects_rewritten_candidate_envelope_metadata(self) -> None:
        repository = self.repository(local_origin=True)
        checkpoint, original, candidate, merge_sha = self.prepare_published(repository)
        original_envelope = original["candidateEnvelopeSha256"]
        rewritten = dict(original)
        rewritten["scopeSummary"] = "A materially different safe-looking publication scope."
        module = repository.load_module("scripts/study_workflow.py")
        rewritten["candidateEnvelopeSha256"] = module.candidate_envelope_digest(rewritten)
        repository.replace_checkpoint(checkpoint, rewritten)
        pr = repository.with_current_checkpoint_body(
            repository.valid_pr_json(candidate, merged=True, merge_sha=merge_sha), checkpoint
        )
        environment = repository.fake_github_environment(pr, candidate)
        environment["FAKE_COMMENT_JSON"] = json.dumps(
            {
                "html_url": "https://github.com/owner/repo/pull/17#issuecomment-99",
                "issue_url": "https://api.github.com/repos/owner/repo/issues/17",
                "body": (
                    f"Accepted head SHA: {candidate}\n"
                    f"Candidate envelope SHA-256: {original_envelope}\n"
                    "Independent reviewer: workflow acceptance role\n"
                    "Reviewer did not author candidate: yes\n"
                    "Review disposition: pass\n"
                ),
            }
        )
        observed = repository.cli(
            "check", "--checkpoint", str(checkpoint), "--phase", "published", "--base", repository.base_sha,
            environment=environment,
        )
        self.assert_deterministic_error(observed, contains="independent review evidence")


if __name__ == "__main__":
    unittest.main()
