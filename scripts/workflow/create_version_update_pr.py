#!/usr/bin/env python3
"""Create a pull request for the post-release development version bump."""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys


VERSION_PATTERN = re.compile(r"^\d+\.\d+\.\d+$")
DEV_VERSION_PATTERN = re.compile(r"^\d+\.\d+\.\d+\.dev0$")


def run(command: list[str], check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, check=check, text=True, capture_output=True)


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
    parser.add_argument(
        "--next-dev-version",
        required=True,
        help="Next X.Y.Z.dev0 development version.",
    )
    parser.add_argument("--base", default="master", help="Base branch for the pull request.")
    parser.add_argument("--head", required=True, help="Head branch for the pull request.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not VERSION_PATTERN.fullmatch(args.version):
        print(f"Version must use X.Y.Z semver. Got: {args.version}", file=sys.stderr)
        return 1
    if not DEV_VERSION_PATTERN.fullmatch(args.next_dev_version):
        print(
            f"Next development version must use X.Y.Z.dev0. Got: {args.next_dev_version}",
            file=sys.stderr,
        )
        return 1

    existing_url = existing_pr(args.head)
    if existing_url:
        print(f"Version update pull request already exists: {existing_url}")
        return 0

    token = os.environ.get("GH_TOKEN")
    if not token:
        print("GH_TOKEN is required to create the version update pull request.", file=sys.stderr)
        return 1

    body = (
        f"Release `{args.version}` was published from the first commit on this branch.\n\n"
        f"This pull request moves `pyproject.toml` to `{args.next_dev_version}` "
        "for the next development cycle."
    )
    run(
        [
            "gh",
            "pr",
            "create",
            "--title",
            f"chore(release): start {args.next_dev_version} development",
            "--body",
            body,
            "--base",
            args.base,
            "--head",
            args.head,
        ]
    )
    print(f"Created version update pull request for {args.next_dev_version}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
