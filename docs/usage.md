# Usage

See the [quickstart](../README.md#quickstart) for installation. With mise, prefix commands with `mise exec --` (tasks activate `.venv-mise` automatically); otherwise activate your virtual environment.

| Command | Purpose |
| --- | --- |
| `games-theory-init [DIR]` | Default DIR is `.`. Copy packaged defaults into `DIR/data/` and set `resource_path`; preserve existing files unless `--overwrite` is given. `--generate-internals` regenerates state/Q-table without replacing existing config. |
| `games-theory PLAYER_POINTS AI_POINTS CELLS... --config DIR` | Select a move; supply `board-size²` cells in row-major order (`X`, `O`, `N`). |
| `./scripts/tictactoe_run.sh DIR` | Smoke run using the default 4×4 board. |
| `./scripts/tictactoe_rebuild.sh DIR` | Reinstall and ask whether to reset resources; `--reset` as second argument resets without prompting. |
| `mise run verify` | Run the acceptance script: compilation, unit tests, release-tool tests and package build. Install `scripts/requirements.txt`. |

The package runs independently of the repository checkout; `pyproject.toml` declares its CLI entry points and runtime dependencies. `games_theory/requirements.txt` adds verification dependencies; `scripts/requirements.txt` includes those plus build and lock-generation tools.

Cell count must match the configured square board or the CLI exits with status 2. The move is zero-based JSON `{"x": column, "y": row}`, or `null` if there is no legal move. Diagnostics go to stderr.

Edit `DIR/data/config.json` to set `board-size`, `ai-char` (`X`/`O`) and `learning`. Learning writes `state.json` and `qtable.json`; disabling it selects moves without persisting changes. See [architecture](architecture/runtime.md) for storage ownership.

| Sandbox | Entry point / purpose |
| --- | --- |
| `nn/` | `nn_main.py`: perceptron and feed-forward network experiments |
| `knn/` | `knn_main.py`: distance, voting and charting experiments |
| `TF/` | GPU checks and TensorFlow network prototypes; TensorFlow needs separate installation |
| `scratch/` | Small standalone explorations |

Install `<area>/requirements.txt` for each sandbox; inspect its local inputs before running it.
