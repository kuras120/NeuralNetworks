# NeuralNetworks

A machine-learning playground with neural-network, k-NN and TensorFlow experiments, plus an installable Q-learning backend for turn-based games in `games_theory/`.

The current practical use case is a CLI-driven predictor for games such as tic-tac-toe; the sandboxes support learning, comparison and prototyping.

## Quickstart

Python 3.14+ is supported. `mise.toml` selects 3.14 to match CI and release-lock generation. Run from the repository root:

```bash
mise trust
mise install
mise exec -- python -m pip install -e . -r scripts/requirements.txt
# Use a fresh directory for the demo resources.
mise exec -- games-theory-init ./demo
mise exec -- ./scripts/tictactoe_run.sh ./demo
```

The packaged demo uses a 4×4 board. The CLI returns a JSON move; diagnostics go to stderr. For ML experiments, install `<area>/requirements.txt` (`nn`, `knn`, `TF` or `scratch`).

Mise creates an isolated `.venv-mise` environment. Validation: `mise run verify`. Without mise, create and activate a virtual environment with a supported Python, install the same dependencies, and run `./scripts/verify.sh`.

## Links

[Usage](docs/usage.md) · [Architecture](docs/architecture/runtime.md) · [Game domain](docs/domain/games-theory-domain.md) · [ML domains](docs/domain/ml-sandbox-domain.md) · [Releases](docs/release.md) · [Research](docs/research/) · [INBOX](INBOX.md) · [Agent instructions](AGENTS.md)
