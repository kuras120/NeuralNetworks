#!/bin/bash

set -euo pipefail

CONFIG_DIR="${1:-.}"

python -m pip install -e . --force-reinstall

read -r -p "Restore tic-tac-toe memory to default in '${CONFIG_DIR}'? [y/N] " restore_memory
case "${restore_memory}" in
    [yY]|[yY][eE][sS])
        games-theory-init "${CONFIG_DIR}" --overwrite
        ;;
    *)
        echo "Keeping existing tic-tac-toe memory."
        ;;
esac
