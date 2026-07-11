#!/usr/bin/env python3
"""Deterministic tests for release helper scripts."""

from __future__ import annotations

import json
import os
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PREPARE = ROOT / "scripts" / "prepare_release.py"
SET_VERSION = ROOT / "scripts" / "set_package_version.py"
NOTES = ROOT / "scripts" / "generate_release_notes.py"
CREATE_PR = ROOT / "scripts" / "create_version_update_pr.py"
WORKFLOW = ROOT / ".github" / "workflows" / "release.yml"


def run(
    command: list[str],
    cwd: Path,
    env: dict[str, str] | None = None,
    check: bool = True,
) -> subprocess.CompletedProcess[str]:
    merged_env = os.environ.copy()
    if env:
        merged_env.update(env)
    return subprocess.run(command, cwd=cwd, env=merged_env, text=True, capture_output=True, check=check)


def init_repo(path: Path, version: str = "0.0.0") -> None:
    run(["git", "init"], path)
    run(["git", "config", "user.name", "Test User"], path)
    run(["git", "config", "user.email", "test@example.com"], path)
    (path / "pyproject.toml").write_text(f'[project]\nname = "x"\nversion = "{version}"\n', encoding="utf-8")
    run(["git", "add", "pyproject.toml"], path)
    run(["git", "commit", "-m", "docs: initial"], path)


def test_prepare_release() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp) / "repo"
        repo.mkdir()
        init_repo(repo)

        output = repo / "outputs.txt"
        run(["python3", str(PREPARE), "--output-file", str(output)], repo)
        assert "VERSION=0.0.1" in output.read_text(encoding="utf-8")

        run(["python3", str(SET_VERSION), "1.2.3"], repo)
        run(["git", "add", "pyproject.toml"], repo)
        run(["git", "commit", "-m", "chore: set package version"], repo)
        run(["git", "tag", "1.2.3"], repo)

        output.write_text("", encoding="utf-8")
        run(["python3", str(PREPARE), "--output-file", str(output)], repo)
        content = output.read_text(encoding="utf-8")
        assert "VERSION=1.2.4" in content
        assert "PREVIOUS_TAG=1.2.3" in content

        output.write_text("", encoding="utf-8")
        run(["python3", str(PREPARE), "--requested-version", "2.0.0", "--output-file", str(output)], repo)
        assert "VERSION=2.0.0" in output.read_text(encoding="utf-8")

        duplicate = run(["python3", str(PREPARE), "--requested-version", "1.2.3"], repo, check=False)
        assert duplicate.returncode != 0


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
                        "url": "https://github.com/example/repo/pull/13",
                        "author": {"login": "carol"},
                        "mergedAt": "2026-01-04T00:00:00Z",
                    },
                ]
            ),
            encoding="utf-8",
        )
        output = workdir / "release-notes.md"
        run(["python3", str(NOTES), "--version", "1.2.4", "--fixture", str(fixture), "--output", str(output)], workdir)
        body = output.read_text(encoding="utf-8")
        assert "# GamesTheory 1.2.4" in body
        assert "### 🚀 Features" in body
        assert "- feat: add release flow ([#10](https://github.com/example/repo/pull/10), [aaaaaaa](https://github.com/example/repo/commit/aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa))" in body
        assert "### 🐛 Bug fixes" in body
        assert "- fix(release): render PR links ([#11](https://github.com/example/repo/pull/11), [bbbbbbb](https://github.com/example/repo/commit/bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb))" in body
        assert "- bugfix: repair release notes ([#12](https://github.com/example/repo/pull/12))" in body
        assert "### 🧰 Others" in body
        assert "- docs: update release guide ([#13](https://github.com/example/repo/pull/13))" in body
        assert body.count("- @alice") == 1
        assert "- @bob" in body
        assert "- @carol" in body


def test_version_update_pr_noop() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp) / "repo"
        repo.mkdir()
        init_repo(repo)
        result = run(["python3", str(CREATE_PR), "--version", "0.0.0"], repo)
        assert "No version update changes to publish." in result.stdout


def test_workflow_yaml() -> None:
    result = run(["ruby", "-e", f'require "yaml"; YAML.load_file("{WORKFLOW}")'], ROOT, check=False)
    if result.returncode != 0:
        raise AssertionError(result.stderr or result.stdout)


def main() -> int:
    test_prepare_release()
    test_generate_release_notes()
    test_version_update_pr_noop()
    test_workflow_yaml()
    print("release tooling tests OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
