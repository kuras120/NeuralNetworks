#!/usr/bin/env python3
"""Create the release branch commits used by the manual release workflow."""

from __future__ import annotations

import argparse
import os
import subprocess
from pathlib import Path

from workflow_common import is_clean_version, is_dev_version, set_project_version


def run(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, check=True, text=True, capture_output=True)


def has_changes() -> bool:
    return bool(run(["git", "status", "--porcelain"]).stdout.strip())


def commit_version(version: str, message: str) -> str:
    set_project_version(version)
    if has_changes():
        run(["git", "add", "pyproject.toml"])
        run(["git", "commit", "-m", message])
    return run(["git", "rev-parse", "HEAD"]).stdout.strip()


def write_github_outputs(
    branch: str,
    release_commit_sha: str,
    output_file: str | None,
) -> None:
    if not output_file:
        return

    with Path(output_file).open("a", encoding="utf-8") as file:
        file.write(f"RELEASE_UPDATE_BRANCH={branch}\n")
        file.write(f"RELEASE_COMMIT_SHA={release_commit_sha}\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Prepare release branch commits.")
    parser.add_argument("--version", required=True, help="Clean X.Y.Z release version.")
    parser.add_argument(
        "--next-dev-version",
        required=True,
        help="Next X.Y.Z.dev0 development version.",
    )
    parser.add_argument(
        "--branch",
        default="",
        help="Release update branch. Defaults to release-<version>.",
    )
    parser.add_argument(
        "--output-file",
        default=os.environ.get("GITHUB_OUTPUT", ""),
        help="GitHub Actions output file. Defaults to GITHUB_OUTPUT.",
    )
    parser.add_argument(
        "--skip-push",
        action="store_true",
        help="Create commits locally without pushing. Intended for deterministic tests.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not is_clean_version(args.version):
        raise ValueError(f"Version must use X.Y.Z semver. Got: {args.version}")
    if not is_dev_version(args.next_dev_version):
        raise ValueError(
            f"Next development version must use X.Y.Z.dev0. Got: {args.next_dev_version}"
        )

    branch = args.branch or f"release-{args.version}"
    run(["git", "config", "user.email", "github-actions[bot]@users.noreply.github.com"])
    run(["git", "config", "user.name", "github-actions[bot]"])
    run(["git", "checkout", "-B", branch])

    release_sha = commit_version(
        args.version,
        f"chore(release): set package version to {args.version}",
    )
    commit_version(
        args.next_dev_version,
        f"chore(release): start {args.next_dev_version} development",
    )

    if not args.skip_push:
        run(["git", "push", "--force-with-lease", "--set-upstream", "origin", branch])
    write_github_outputs(branch, release_sha, args.output_file)
    print(f"Prepared release branch {branch} with release commit {release_sha}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
