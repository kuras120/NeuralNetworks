#!/bin/bash

set -euo pipefail

if ! python3 -c 'import build' >/dev/null 2>&1; then
    echo "Missing verification dependencies. Run: pip install -r scripts/requirements.txt" >&2
    exit 1
fi

python3 -m compileall -q games_theory
python3 -m unittest discover -s games_theory/test -p 'test_*.py'
python3 scripts/workflow/test_release_tools.py
python3 -m build
