#!/usr/bin/env python3
"""Set build-only package version metadata before creating release artifacts."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


SEMVER_PATTERN = re.compile(r"^\d+\.\d+\.\d+$")
PYPROJECT_PATH = Path("pyproject.toml")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Set package version in pyproject.toml.")
    parser.add_argument("version", help="X.Y.Z release version.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not SEMVER_PATTERN.fullmatch(args.version):
        raise ValueError(f"Release version must use X.Y.Z semver. Got: {args.version}")

    content = PYPROJECT_PATH.read_text(encoding="utf-8")
    next_content, count = re.subn(
        r'(?m)^version = "\d+\.\d+\.\d+"$',
        f'version = "{args.version}"',
        content,
        count=1,
    )
    if count != 1:
        raise RuntimeError("Could not find a static project version in pyproject.toml.")

    PYPROJECT_PATH.write_text(next_content, encoding="utf-8")
    print(f"Set package version to {args.version}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
