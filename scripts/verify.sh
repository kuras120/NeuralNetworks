#!/bin/bash

set -euo pipefail

python3 -m compileall -q games_theory
python3 -m unittest discover -s games_theory/test -p 'test_*.py'
python3 scripts/workflow/test_release_tools.py
python3 -m build
