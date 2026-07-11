#!/usr/bin/env python3
"""Prepare release version outputs for GitHub Actions."""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path


CLEAN_VERSION_PATTERN = re.compile(r"^\d+\.\d+\.\d+$")
DEV_VERSION_PATTERN = re.compile(r"^\d+\.\d+\.\d+\.dev0$")
PROJECT_VERSION_PATTERN = re.compile(r'(?m)^version = "(\d+\.\d+\.\d+(?:\.dev0)?)"$')
BASELINE_VERSION = "0.0.1.dev0"
PYPROJECT_PATH = Path("pyproject.toml")


def run_git(args: list[str], check: bool = True) -> str:
    result = subprocess.run(
        ["git", *args],
        check=check,
        text=True,
        capture_output=True,
    )
    return result.stdout.strip()


def semver_tuple(version: str) -> tuple[int, int, int]:
    return tuple(int(part) for part in version.split("."))


def reachable_semver_tags() -> list[str]:
    tags = run_git(["tag", "--merged", "HEAD", "--list", "--sort=-v:refname"])
    return [tag for tag in tags.splitlines() if CLEAN_VERSION_PATTERN.fullmatch(tag)]


def previous_tag_for_release(version: str) -> str:
    release_parts = semver_tuple(version)
    for tag in reachable_semver_tags():
        if semver_tuple(tag) < release_parts:
            return tag
    return ""


def latest_semver_tag() -> str:
    tags = reachable_semver_tags()
    return tags[0] if tags else ""


def release_version_is_after_latest_reachable_tag(version: str) -> bool:
    latest_tag = latest_semver_tag()
    if not latest_tag:
        return True
    return semver_tuple(version) > semver_tuple(latest_tag)


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


def next_dev_version(release_version: str) -> str:
    return f"{next_patch(release_version)}.dev0"


def clean_version_base(version: str) -> str:
    if DEV_VERSION_PATTERN.fullmatch(version):
        return version.removesuffix(".dev0")
    return version


def pyproject_version() -> str:
    content = PYPROJECT_PATH.read_text(encoding="utf-8")
    match = PROJECT_VERSION_PATTERN.search(content)
    if match:
        return match.group(1)
    return BASELINE_VERSION


def default_release_version() -> str:
    project_version = pyproject_version()
    if DEV_VERSION_PATTERN.fullmatch(project_version):
        return clean_version_base(project_version)

    latest_tag = latest_semver_tag()
    return next_patch(latest_tag or project_version)


def write_github_outputs(
    version: str,
    next_dev: str,
    previous_tag: str,
    output_file: str | None,
) -> None:
    if not output_file:
        return

    with Path(output_file).open("a", encoding="utf-8") as file:
        file.write(f"VERSION={version}\n")
        file.write(f"NEXT_DEV_VERSION={next_dev}\n")
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

    if requested_version:
        release_version = requested_version
    else:
        release_version = default_release_version()

    if not CLEAN_VERSION_PATTERN.fullmatch(release_version):
        print(
            f"Release version must use X.Y.Z semver without a v prefix. Got: {release_version}",
            file=sys.stderr,
        )
        return 1

    if requested_version and not release_version_is_after_latest_reachable_tag(
        release_version
    ):
        print(
            f"Release version {release_version} must be greater than "
            f"latest reachable tag {latest_semver_tag()}.",
            file=sys.stderr,
        )
        return 1

    next_dev = next_dev_version(release_version)
    previous_tag = previous_tag_for_release(release_version)

    if tag_exists(release_version):
        print(f"Tag {release_version} already exists.", file=sys.stderr)
        return 1

    write_github_outputs(release_version, next_dev, previous_tag, args.output_file)
    print(f"Selected release version: {release_version}")
    print(f"Next development version: {next_dev}")
    if previous_tag:
        print(f"Previous release tag: {previous_tag}")
    else:
        print("No previous semver release tag found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
