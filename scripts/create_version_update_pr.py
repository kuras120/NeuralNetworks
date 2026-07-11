#!/usr/bin/env python3
"""Create a pull request that persists the released version in pyproject.toml."""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys


SEMVER_PATTERN = re.compile(r"^\d+\.\d+\.\d+$")


def run(command: list[str], check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, check=check, text=True, capture_output=True)


def has_changes() -> bool:
    result = run(["git", "status", "--porcelain"])
    return bool(result.stdout.strip())


def existing_pr(branch: str) -> str:
    result = run(
        [
            "gh",
            "pr",
            "list",
            "--head",
            branch,
            "--json",
            "url",
            "--jq",
            ".[0].url // \"\"",
        ],
        check=False,
    )
    return result.stdout.strip()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create version update pull request.")
    parser.add_argument("--version", required=True, help="Released X.Y.Z version.")
    parser.add_argument("--base", default="master", help="Base branch for the pull request.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not SEMVER_PATTERN.fullmatch(args.version):
        print(f"Version must use X.Y.Z semver. Got: {args.version}", file=sys.stderr)
        return 1

    if not has_changes():
        print("No version update changes to publish.")
        return 0

    branch = f"version-bump-{args.version}"
    run(["git", "config", "user.email", "github-actions[bot]@users.noreply.github.com"])
    run(["git", "config", "user.name", "github-actions[bot]"])
    run(["git", "checkout", "-B", branch])
    run(["git", "add", "pyproject.toml"])
    run(["git", "commit", "-m", f"chore(release): update package version to {args.version}"])
    run(["git", "push", "--force-with-lease", "--set-upstream", "origin", branch])

    existing_url = existing_pr(branch)
    if existing_url:
        print(f"Version update pull request already exists: {existing_url}")
        return 0

    token = os.environ.get("GH_TOKEN")
    if not token:
        print("GH_TOKEN is required to create the version update pull request.", file=sys.stderr)
        return 1

    body = (
        f"Persist the package version released as `{args.version}` in `pyproject.toml`.\n\n"
        "The release artifact and tag were already created by the manual release workflow."
    )
    run(
        [
            "gh",
            "pr",
            "create",
            "--title",
            f"chore(release): update package version to {args.version}",
            "--body",
            body,
            "--base",
            args.base,
            "--head",
            branch,
        ]
    )
    print(f"Created version update pull request for {args.version}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
