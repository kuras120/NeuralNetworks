#!/usr/bin/env python3
"""Prepare release version outputs for GitHub Actions."""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path


SEMVER_PATTERN = re.compile(r"^\d+\.\d+\.\d+$")
BASELINE_VERSION = "0.0.0"
PYPROJECT_PATH = Path("pyproject.toml")


def run_git(args: list[str], check: bool = True) -> str:
    result = subprocess.run(
        ["git", *args],
        check=check,
        text=True,
        capture_output=True,
    )
    return result.stdout.strip()


def latest_semver_tag() -> str:
    tags = run_git(["tag", "--list", "--sort=-v:refname"])
    for tag in tags.splitlines():
        if SEMVER_PATTERN.fullmatch(tag):
            return tag
    return ""


def tag_exists(version: str) -> bool:
    result = subprocess.run(
        ["git", "rev-parse", "--verify", "--quiet", f"refs/tags/{version}"],
        text=True,
        capture_output=True,
    )
    return result.returncode == 0


def next_patch(base_version: str) -> str:
    major, minor, patch = [int(part) for part in base_version.split(".")]
    return f"{major}.{minor}.{patch + 1}"


def pyproject_version() -> str:
    content = PYPROJECT_PATH.read_text(encoding="utf-8")
    match = re.search(r'(?m)^version = "(\d+\.\d+\.\d+)"$', content)
    if match:
        return match.group(1)
    return BASELINE_VERSION


def write_github_outputs(version: str, previous_tag: str, output_file: str | None) -> None:
    if not output_file:
        return

    with Path(output_file).open("a", encoding="utf-8") as file:
        file.write(f"VERSION={version}\n")
        file.write(f"PREVIOUS_TAG={previous_tag}\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Prepare release version outputs.")
    parser.add_argument(
        "--requested-version",
        default="",
        help="Optional explicit X.Y.Z release version.",
    )
    parser.add_argument(
        "--output-file",
        default=os.environ.get("GITHUB_OUTPUT", ""),
        help="GitHub Actions output file. Defaults to GITHUB_OUTPUT.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    requested_version = args.requested_version.strip()
    previous_tag = latest_semver_tag()

    if requested_version:
        release_version = requested_version
    else:
        release_version = next_patch(previous_tag or pyproject_version())

    if not SEMVER_PATTERN.fullmatch(release_version):
        print(
            f"Release version must use X.Y.Z semver without a v prefix. Got: {release_version}",
            file=sys.stderr,
        )
        return 1

    if tag_exists(release_version):
        print(f"Tag {release_version} already exists.", file=sys.stderr)
        return 1

    write_github_outputs(release_version, previous_tag, args.output_file)
    print(f"Selected release version: {release_version}")
    if previous_tag:
        print(f"Previous release tag: {previous_tag}")
    else:
        print("No previous semver release tag found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
