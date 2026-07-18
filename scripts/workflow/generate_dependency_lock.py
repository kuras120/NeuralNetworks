#!/usr/bin/env python3
"""Generate a hashed runtime dependency lock from a release wheel."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
import tempfile
import zipfile
from email.parser import BytesParser
from email.policy import default
from pathlib import Path


PACKAGE_NAME = "games-theory"
LOCK_SUFFIX = "requirements.lock"
HASH_PATTERN = re.compile(r"--hash=sha256:[0-9a-f]{64}\b")
PIN_PATTERN = re.compile(r"^([A-Za-z0-9][A-Za-z0-9._-]*)==([^\s\\]+)")


def canonicalize_name(name: str) -> str:
    return re.sub(r"[-_.]+", "-", name).lower()


def lock_artifact_name(version: str) -> str:
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        raise ValueError(f"Release version must use X.Y.Z semver. Got: {version}")
    return f"{PACKAGE_NAME}-{version}-{LOCK_SUFFIX}"


def find_release_wheel(dist_dir: Path, version: str) -> Path:
    normalized_version = version.replace("-", "_")
    candidates = sorted(dist_dir.glob(f"games_theory-{normalized_version}-*.whl"))
    if len(candidates) != 1:
        raise ValueError(
            f"Expected exactly one games-theory {version} wheel in {dist_dir}; "
            f"found {len(candidates)}."
        )
    return candidates[0]


def read_wheel_runtime_requirements(
    wheel: Path,
    expected_version: str,
) -> list[str]:
    with zipfile.ZipFile(wheel) as archive:
        metadata_files = [
            name for name in archive.namelist() if name.endswith(".dist-info/METADATA")
        ]
        if len(metadata_files) != 1:
            raise ValueError(
                f"Expected exactly one METADATA file in {wheel}; "
                f"found {len(metadata_files)}."
            )
        metadata = BytesParser(policy=default).parsebytes(
            archive.read(metadata_files[0])
        )

    package_name = metadata.get("Name", "")
    if canonicalize_name(package_name) != PACKAGE_NAME:
        raise ValueError(f"Unexpected wheel package name: {package_name or '<missing>'}")

    wheel_version = metadata.get("Version", "")
    if wheel_version != expected_version:
        raise ValueError(
            f"Wheel version {wheel_version or '<missing>'} does not match "
            f"release version {expected_version}."
        )

    requirements = sorted(set(metadata.get_all("Requires-Dist", [])))
    marked = [requirement for requirement in requirements if ";" in requirement]
    if marked:
        raise ValueError(
            "Environment-marked runtime dependencies require an explicit target "
            f"compatibility design: {', '.join(marked)}"
        )
    return requirements


def compile_command(source: Path, output: Path) -> list[str]:
    return [
        sys.executable,
        "-m",
        "piptools",
        "compile",
        "--no-config",
        "--generate-hashes",
        "--no-header",
        "--no-annotate",
        "--no-emit-index-url",
        "--no-emit-trusted-host",
        "--strip-extras",
        "--resolver",
        "backtracking",
        "--output-file",
        str(output),
        str(source),
    ]


def logical_requirement_blocks(content: str) -> list[str]:
    blocks: list[str] = []
    current: list[str] = []
    for raw_line in content.splitlines():
        stripped = raw_line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        current.append(stripped.removesuffix("\\").strip())
        if not stripped.endswith("\\"):
            blocks.append(" ".join(current))
            current = []
    if current:
        raise ValueError("Lockfile ends with an incomplete line continuation.")
    return blocks


def validate_lock_content(content: str, expected_packages: set[str] | None = None) -> set[str]:
    blocks = logical_requirement_blocks(content)
    packages: set[str] = set()
    for block in blocks:
        match = PIN_PATTERN.match(block)
        if match is None:
            raise ValueError(f"Lock entry is not an exact == pin: {block}")
        package = canonicalize_name(match.group(1))
        if package in packages:
            raise ValueError(f"Duplicate package in lockfile: {package}")
        if not HASH_PATTERN.search(block):
            raise ValueError(f"Lock entry has no SHA-256 hash: {package}")
        if ";" in block or " @ " in block:
            raise ValueError(f"Target-dependent or direct dependency is unsupported: {block}")
        packages.add(package)

    if expected_packages is not None and packages != expected_packages:
        raise ValueError(
            "Locked package set does not match expected dependency closure: "
            f"expected {sorted(expected_packages)}, got {sorted(packages)}"
        )
    return packages


def generate_lock(wheel: Path, version: str, output: Path) -> None:
    requirements = read_wheel_runtime_requirements(wheel, version)
    output.parent.mkdir(parents=True, exist_ok=True)

    if not requirements:
        output.write_text("", encoding="utf-8")
        return

    with tempfile.TemporaryDirectory(prefix="games-theory-lock-") as tmp:
        temp_dir = Path(tmp)
        source = temp_dir / "runtime-requirements.in"
        compiled = temp_dir / "runtime-requirements.lock"
        source.write_text("\n".join(requirements) + "\n", encoding="utf-8")
        subprocess.run(compile_command(source, compiled), check=True)
        content = compiled.read_text(encoding="utf-8")

    validate_lock_content(content)
    output.write_text(content.rstrip() + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate a hashed runtime dependency lock from a release wheel."
    )
    parser.add_argument("--version", required=True, help="Clean X.Y.Z release version.")
    parser.add_argument(
        "--dist-dir",
        type=Path,
        default=Path("dist"),
        help="Directory containing the built release wheel.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Output lock path. Defaults to the versioned release asset name.",
    )
    args = parser.parse_args()

    try:
        artifact_name = lock_artifact_name(args.version)
        wheel = find_release_wheel(args.dist_dir, args.version)
        output = args.output or args.dist_dir / artifact_name
        generate_lock(wheel, args.version, output)
    except (OSError, ValueError, zipfile.BadZipFile) as error:
        print(error, file=sys.stderr)
        return 1

    print(f"Generated dependency lock: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
