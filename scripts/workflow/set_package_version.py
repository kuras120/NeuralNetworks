#!/usr/bin/env python3
"""Set build-only package version metadata before creating release artifacts."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


VERSION_PATTERN = re.compile(r"^\d+\.\d+\.\d+(?:\.dev0)?$")
PYPROJECT_PATH = Path("pyproject.toml")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Set package version in pyproject.toml.")
    parser.add_argument("version", help="X.Y.Z release or X.Y.Z.dev0 development version.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not VERSION_PATTERN.fullmatch(args.version):
        raise ValueError(f"Version must use X.Y.Z or X.Y.Z.dev0. Got: {args.version}")

    content = PYPROJECT_PATH.read_text(encoding="utf-8")
    next_content, count = re.subn(
        r'(?m)^version = "\d+\.\d+\.\d+(?:\.dev0)?"$',
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
