#!/bin/bash

set -euo pipefail

CONFIG_DIR="${1:-.}"

if ! command -v games-theory >/dev/null 2>&1; then
    echo "games-theory CLI is not installed. Run ./scripts/tictactoe_rebuild.sh first." >&2
    exit 127
fi

if [[ ! -f "${CONFIG_DIR}/data/config.json" || ! -f "${CONFIG_DIR}/data/qtable.json" || ! -f "${CONFIG_DIR}/data/state.json" ]]; then
    echo "Tic-tac-toe data files are missing in '${CONFIG_DIR}'. Run ./scripts/tictactoe_rebuild.sh first." >&2
    exit 1
fi

games-theory --config "${CONFIG_DIR}" 0 0 N N N N N X N N N N N N N N N N
