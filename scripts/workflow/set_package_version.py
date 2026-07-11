#!/usr/bin/env python3
"""Set build-only package version metadata before creating release artifacts."""

from __future__ import annotations

import argparse

from workflow_common import is_clean_version, is_dev_version, set_project_version


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Set package version in pyproject.toml.")
    parser.add_argument("version", help="X.Y.Z release or X.Y.Z.dev0 development version.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not (is_clean_version(args.version) or is_dev_version(args.version)):
        raise ValueError(f"Version must use X.Y.Z or X.Y.Z.dev0. Got: {args.version}")

    set_project_version(args.version)
    print(f"Set package version to {args.version}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
