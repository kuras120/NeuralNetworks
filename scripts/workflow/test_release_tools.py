#!/usr/bin/env python3
"""Deterministic tests for release helper scripts."""

from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
WORKFLOW_SCRIPTS = ROOT / "scripts" / "workflow"
PREPARE = WORKFLOW_SCRIPTS / "prepare_release.py"
PREPARE_BRANCH = WORKFLOW_SCRIPTS / "prepare_release_branch.py"
SET_VERSION = WORKFLOW_SCRIPTS / "set_package_version.py"
NOTES = WORKFLOW_SCRIPTS / "generate_release_notes.py"
CREATE_PR = WORKFLOW_SCRIPTS / "create_version_update_pr.py"
WORKFLOW = ROOT / ".github" / "workflows" / "release.yml"


def load_release_notes_module():
    spec = importlib.util.spec_from_file_location("generate_release_notes", NOTES)
    if spec is None or spec.loader is None:
        raise RuntimeError("Cannot load generate_release_notes.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


GENERATE_RELEASE_NOTES = load_release_notes_module()


def run(
    command: list[str],
    cwd: Path,
    env: dict[str, str] | None = None,
    check: bool = True,
) -> subprocess.CompletedProcess[str]:
    merged_env = os.environ.copy()
    if env:
        merged_env.update(env)
    return subprocess.run(
        command,
        cwd=cwd,
        env=merged_env,
        text=True,
        capture_output=True,
        check=check,
    )


def init_repo(path: Path, version: str = "0.0.0") -> None:
    run(["git", "init"], path)
    run(["git", "config", "user.name", "Test User"], path)
    run(["git", "config", "user.email", "test@example.com"], path)
    (path / "pyproject.toml").write_text(
        f'[project]\nname = "x"\nversion = "{version}"\n',
        encoding="utf-8",
    )
    run(["git", "add", "pyproject.toml"], path)
    run(["git", "commit", "-m", "docs: initial"], path)


def test_prepare_release() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp) / "repo"
        repo.mkdir()
        init_repo(repo)

        output = repo / "outputs.txt"
        run(["python3", str(PREPARE), "--output-file", str(output)], repo)
        content = output.read_text(encoding="utf-8")
        assert "VERSION=0.0.1" in content
        assert "NEXT_DEV_VERSION=0.0.2.dev0" in content

        repo_dev = Path(tmp) / "repo-dev"
        repo_dev.mkdir()
        init_repo(repo_dev, version="0.4.2.dev0")
        dev_output = repo_dev / "outputs.txt"
        run(["python3", str(PREPARE), "--output-file", str(dev_output)], repo_dev)
        dev_content = dev_output.read_text(encoding="utf-8")
        assert "VERSION=0.4.2" in dev_content
        assert "NEXT_DEV_VERSION=0.4.3.dev0" in dev_content

        run(["python3", str(SET_VERSION), "1.2.3"], repo)
        run(["git", "add", "pyproject.toml"], repo)
        run(["git", "commit", "-m", "chore: set package version"], repo)
        run(["git", "tag", "1.2.3"], repo)

        output.write_text("", encoding="utf-8")
        run(["python3", str(PREPARE), "--output-file", str(output)], repo)
        content = output.read_text(encoding="utf-8")
        assert "VERSION=1.2.4" in content
        assert "NEXT_DEV_VERSION=1.2.5.dev0" in content
        assert "PREVIOUS_TAG=1.2.3" in content

        output.write_text("", encoding="utf-8")
        run(
            [
                "python3",
                str(PREPARE),
                "--requested-version",
                "2.0.0",
                "--output-file",
                str(output),
            ],
            repo,
        )
        content = output.read_text(encoding="utf-8")
        assert "VERSION=2.0.0" in content
        assert "NEXT_DEV_VERSION=2.0.1.dev0" in content

        duplicate = run(
            ["python3", str(PREPARE), "--requested-version", "1.2.3"],
            repo,
            check=False,
        )
        assert duplicate.returncode != 0


def test_prepare_release_uses_branch_local_previous_tag() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp) / "repo"
        repo.mkdir()
        init_repo(repo)

        run(["python3", str(SET_VERSION), "1.3.0"], repo)
        run(["git", "add", "pyproject.toml"], repo)
        run(["git", "commit", "-m", "chore: set 1.3.0"], repo)
        run(["git", "tag", "1.3.0"], repo)

        run(["python3", str(SET_VERSION), "1.4.0"], repo)
        run(["git", "add", "pyproject.toml"], repo)
        run(["git", "commit", "-m", "chore: set 1.4.0"], repo)
        run(["git", "tag", "1.4.0"], repo)

        run(["git", "checkout", "-b", "release-1"], repo)
        run(["git", "checkout", "-b", "mainline"], repo)
        run(["python3", str(SET_VERSION), "2.0.0"], repo)
        run(["git", "add", "pyproject.toml"], repo)
        run(["git", "commit", "-m", "chore: set 2.0.0"], repo)
        run(["git", "tag", "2.0.0"], repo)
        run(["git", "checkout", "release-1"], repo)

        output = repo / "outputs.txt"
        run(
            [
                "python3",
                str(PREPARE),
                "--requested-version",
                "1.4.1",
                "--output-file",
                str(output),
            ],
            repo,
        )
        content = output.read_text(encoding="utf-8")
        assert "VERSION=1.4.1" in content
        assert "PREVIOUS_TAG=1.4.0" in content


def test_prepare_release_rejects_branch_local_downgrade() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp) / "repo"
        repo.mkdir()
        init_repo(repo)

        run(["python3", str(SET_VERSION), "1.5.1"], repo)
        run(["git", "add", "pyproject.toml"], repo)
        run(["git", "commit", "-m", "chore: set 1.5.1"], repo)
        run(["git", "tag", "1.5.1"], repo)

        run(["git", "checkout", "-b", "release-1"], repo)
        run(["git", "checkout", "-b", "mainline"], repo)
        run(["python3", str(SET_VERSION), "2.0.0"], repo)
        run(["git", "add", "pyproject.toml"], repo)
        run(["git", "commit", "-m", "chore: set 2.0.0"], repo)
        run(["git", "tag", "2.0.0"], repo)
        run(["git", "checkout", "release-1"], repo)

        rejected = run(
            ["python3", str(PREPARE), "--requested-version", "1.4.2"],
            repo,
            check=False,
        )
        assert rejected.returncode != 0
        assert "must be greater than latest reachable tag 1.5.1" in rejected.stderr

        output = repo / "outputs.txt"
        run(
            [
                "python3",
                str(PREPARE),
                "--requested-version",
                "1.5.2",
                "--output-file",
                str(output),
            ],
            repo,
        )
        content = output.read_text(encoding="utf-8")
        assert "VERSION=1.5.2" in content
        assert "PREVIOUS_TAG=1.5.1" in content


def test_prepare_release_branch() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp) / "repo"
        repo.mkdir()
        init_repo(repo, version="1.4.0.dev0")

        output = repo / "outputs.txt"
        run(
            [
                "python3",
                str(PREPARE_BRANCH),
                "--version",
                "1.4.0",
                "--next-dev-version",
                "1.4.1.dev0",
                "--output-file",
                str(output),
                "--skip-push",
            ],
            repo,
        )

        content = output.read_text(encoding="utf-8")
        assert "RELEASE_UPDATE_BRANCH=release-1.4.0" in content
        release_sha = next(
            line.split("=", 1)[1]
            for line in content.splitlines()
            if line.startswith("RELEASE_COMMIT_SHA=")
        )
        release_tree = run(
            ["git", "show", f"{release_sha}:pyproject.toml"],
            repo,
        ).stdout
        head_tree = run(["git", "show", "HEAD:pyproject.toml"], repo).stdout
        assert 'version = "1.4.0"' in release_tree
        assert 'version = "1.4.1.dev0"' in head_tree
        assert run(["git", "rev-list", "--count", "HEAD"], repo).stdout.strip() == "3"


def test_generate_release_notes() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        workdir = Path(tmp)
        fixture = workdir / "prs.json"
        fixture.write_text(
            json.dumps(
                [
                    {
                        "number": 10,
                        "title": "feat: add release flow",
                        "url": "https://github.com/example/repo/pull/10",
                        "author": {"login": "alice"},
                        "mergedAt": "2026-01-01T00:00:00Z",
                        "mergeCommit": {"oid": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"},
                    },
                    {
                        "number": 11,
                        "title": "fix(release): render PR links",
                        "url": "https://github.com/example/repo/pull/11",
                        "author": {"login": "bob"},
                        "mergedAt": "2026-01-02T00:00:00Z",
                        "mergeCommit": {"oid": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"},
                    },
                    {
                        "number": 12,
                        "title": "bugfix: repair release notes",
                        "url": "https://github.com/example/repo/pull/12",
                        "author": {"login": "alice"},
                        "mergedAt": "2026-01-03T00:00:00Z",
                    },
                    {
                        "number": 13,
                        "title": "docs: update release guide",
                        "url": "https://api.github.com/repos/example/repo/pulls/13",
                        "html_url": "https://github.com/example/repo/pull/13",
                        "user": {"login": "carol"},
                        "merged_at": "2026-01-04T00:00:00Z",
                        "merge_commit_sha": "cccccccccccccccccccccccccccccccccccccccc",
                    },
                ]
            ),
            encoding="utf-8",
        )
        output = workdir / "release-notes.md"
        run(
            [
                "python3",
                str(NOTES),
                "--version",
                "1.2.4",
                "--fixture",
                str(fixture),
                "--output",
                str(output),
            ],
            workdir,
        )
        body = output.read_text(encoding="utf-8")
        assert "# GamesTheory 1.2.4" in body
        assert "### 🚀 Features" in body
        assert (
            "- feat: add release flow "
            "([#10](https://github.com/example/repo/pull/10), "
            "[aaaaaaa](https://github.com/example/repo/commit/"
            "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa))"
        ) in body
        assert "### 🐛 Bug fixes" in body
        assert (
            "- fix(release): render PR links "
            "([#11](https://github.com/example/repo/pull/11), "
            "[bbbbbbb](https://github.com/example/repo/commit/"
            "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb))"
        ) in body
        assert (
            "- bugfix: repair release notes "
            "([#12](https://github.com/example/repo/pull/12))"
        ) in body
        assert "### 🧰 Others" in body
        assert (
            "- docs: update release guide "
            "([#13](https://github.com/example/repo/pull/13), "
            "[ccccccc](https://github.com/example/repo/commit/"
            "cccccccccccccccccccccccccccccccccccccccc))"
        ) in body
        assert body.count("- @alice") == 1
        assert "- @bob" in body
        assert "- @carol" in body


def test_paginated_pull_request_payload() -> None:
    payload = json.dumps(
        [
            [{"number": 1, "title": "feat: one"}],
            [{"number": 2, "title": "fix: two"}],
        ]
    )
    flattened = GENERATE_RELEASE_NOTES.load_paginated_payload(payload)
    assert [item["number"] for item in flattened] == [1, 2]


def test_first_release_filters_prs_to_head_history() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp) / "repo"
        repo.mkdir()
        init_repo(repo)
        in_history = run(["git", "rev-parse", "HEAD"], repo).stdout.strip()
        outside_history = "d" * 40

        original_release_range = GENERATE_RELEASE_NOTES.release_range
        original_run = GENERATE_RELEASE_NOTES.run
        original_loader = GENERATE_RELEASE_NOTES.load_paginated_payload
        original_repository = os.environ.get("GITHUB_REPOSITORY")

        def fake_run(command: list[str]) -> str:
            if command[:2] == ["gh", "api"]:
                return "[]"
            if command == ["git", "rev-list", in_history]:
                return in_history
            return original_run(command)

        GENERATE_RELEASE_NOTES.release_range = lambda _: ("", in_history)
        GENERATE_RELEASE_NOTES.run = fake_run
        GENERATE_RELEASE_NOTES.load_paginated_payload = lambda _: [
            {
                "number": 1,
                "title": "feat: included",
                "html_url": "https://github.com/example/repo/pull/1",
                "user": {"login": "alice"},
                "merged_at": "2026-01-01T00:00:00Z",
                "merge_commit_sha": in_history,
            },
            {
                "number": 2,
                "title": "feat: outside",
                "html_url": "https://github.com/example/repo/pull/2",
                "user": {"login": "bob"},
                "merged_at": "2026-01-02T00:00:00Z",
                "merge_commit_sha": outside_history,
            },
        ]
        os.environ["GITHUB_REPOSITORY"] = "example/repo"
        try:
            prs = GENERATE_RELEASE_NOTES.load_pull_requests_from_github("")
        finally:
            GENERATE_RELEASE_NOTES.release_range = original_release_range
            GENERATE_RELEASE_NOTES.run = original_run
            GENERATE_RELEASE_NOTES.load_paginated_payload = original_loader
            if original_repository is None:
                os.environ.pop("GITHUB_REPOSITORY", None)
            else:
                os.environ["GITHUB_REPOSITORY"] = original_repository

        assert [pr.number for pr in prs] == [1]


def test_version_update_pr_rejects_invalid_version() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp) / "repo"
        repo.mkdir()
        init_repo(repo)
        result = run(
            [
                "python3",
                str(CREATE_PR),
                "--version",
                "0.0.0.dev0",
                "--next-dev-version",
                "0.0.1.dev0",
                "--base",
                "master",
                "--head",
                "release-0.0.0",
            ],
            repo,
            check=False,
        )
        assert result.returncode != 0


def test_workflow_yaml() -> None:
    result = run(
        ["ruby", "-e", f'require "yaml"; YAML.load_file("{WORKFLOW}")'],
        ROOT,
        check=False,
    )
    if result.returncode != 0:
        raise AssertionError(result.stderr or result.stdout)


def test_release_workflow_branch_input() -> None:
    content = WORKFLOW.read_text(encoding="utf-8")
    assert 'description: "Branch to release from' not in content
    assert "RELEASE_BRANCH: ${{ github.ref_name }}" in content
    assert "REQUESTED_VERSION: ${{ inputs.version }}" in content
    assert "NEXT_DEV_VERSION: ${{ steps.version.outputs.NEXT_DEV_VERSION }}" in content
    assert "release_branch:" in content
    assert "RELEASE_COMMIT_SHA: ${{ steps.release_branch.outputs.RELEASE_COMMIT_SHA }}" in content
    assert "ref: ${{ env.RELEASE_BRANCH }}" in content
    assert "ref: ${{ env.RELEASE_COMMIT_SHA }}" in content
    assert "target_commitish: ${{ env.RELEASE_COMMIT_SHA }}" in content
    assert '--base "${{ env.RELEASE_BRANCH }}"' in content
    assert '--head "${{ env.RELEASE_UPDATE_BRANCH }}"' in content


def main() -> int:
    test_prepare_release()
    test_prepare_release_uses_branch_local_previous_tag()
    test_prepare_release_rejects_branch_local_downgrade()
    test_prepare_release_branch()
    test_generate_release_notes()
    test_paginated_pull_request_payload()
    test_first_release_filters_prs_to_head_history()
    test_version_update_pr_rejects_invalid_version()
    test_workflow_yaml()
    test_release_workflow_branch_input()
    print("release tooling tests OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
