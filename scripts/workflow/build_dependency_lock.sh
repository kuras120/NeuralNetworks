#!/bin/bash

set -euo pipefail

if [[ $# -ne 1 ]]; then
    echo "Usage: $0 <release-version>" >&2
    exit 2
fi

version="$1"
lock_file="dist/games-theory-${version}-requirements.lock"
verification_environment="build/release-verify"
verification_config="build/release-verify-config"

python3 scripts/workflow/generate_dependency_lock.py \
    --version "${version}"

python3 -m pip download \
    --require-hashes \
    --only-binary=:all: \
    --platform any \
    --python-version 3.9 \
    --implementation py \
    --abi none \
    --dest build/universal-dependencies \
    -r "${lock_file}"

python3 -m venv "${verification_environment}"
"${verification_environment}/bin/python" -m pip install \
    --require-hashes \
    -r "${lock_file}"

release_wheels=(dist/games_theory-"${version}"-*.whl)
if [[ ${#release_wheels[@]} -ne 1 || ! -f "${release_wheels[0]}" ]]; then
    echo "Expected exactly one games-theory ${version} wheel in dist/." >&2
    exit 1
fi

"${verification_environment}/bin/python" -m pip install \
    --no-deps \
    "${release_wheels[0]}"
"${verification_environment}/bin/python" -m pip check
"${verification_environment}/bin/games-theory-init" \
    "${verification_config}" \
    --overwrite
"${verification_environment}/bin/games-theory" \
    --config "${verification_config}" \
    0 0 N N N N N N N N N N N N N N N N
