"""Shared helpers for release workflow scripts."""

from __future__ import annotations

import re
from pathlib import Path


CLEAN_VERSION_PATTERN = re.compile(r"^\d+\.\d+\.\d+$")
DEV_VERSION_PATTERN = re.compile(r"^\d+\.\d+\.\d+\.dev0$")
PROJECT_VERSION_PATTERN = re.compile(r'(?m)^version = "(\d+\.\d+\.\d+(?:\.dev0)?)"$')
PROJECT_VERSION_LINE_PATTERN = re.compile(
    r'(?m)^version = "\d+\.\d+\.\d+(?:\.dev0)?"$'
)
BASELINE_VERSION = "0.0.1.dev0"
PYPROJECT_PATH = Path("pyproject.toml")


def is_clean_version(version: str) -> bool:
    return bool(CLEAN_VERSION_PATTERN.fullmatch(version))


def is_dev_version(version: str) -> bool:
    return bool(DEV_VERSION_PATTERN.fullmatch(version))


def semver_tuple(version: str) -> tuple[int, int, int]:
    return tuple(int(part) for part in version.split("."))


def next_patch(base_version: str) -> str:
    major, minor, patch = semver_tuple(base_version)
    return f"{major}.{minor}.{patch + 1}"


def next_dev_version(release_version: str) -> str:
    return f"{next_patch(release_version)}.dev0"


def clean_version_base(version: str) -> str:
    if is_dev_version(version):
        return version.removesuffix(".dev0")
    return version


def project_version() -> str:
    content = PYPROJECT_PATH.read_text(encoding="utf-8")
    match = PROJECT_VERSION_PATTERN.search(content)
    if match:
        return match.group(1)
    return BASELINE_VERSION


def set_project_version(version: str) -> None:
    content = PYPROJECT_PATH.read_text(encoding="utf-8")
    next_content, count = PROJECT_VERSION_LINE_PATTERN.subn(
        f'version = "{version}"',
        content,
        count=1,
    )
    if count != 1:
        raise RuntimeError("Could not find a static project version in pyproject.toml.")
    PYPROJECT_PATH.write_text(next_content, encoding="utf-8")
