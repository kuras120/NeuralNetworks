# NeuralNetworks

NeuralNetworks is a Python project for exploring machine-learning algorithms and developing a reusable Q-learning backend for turn-based games. It combines lightweight neural-network, k-NN, and TensorFlow experiments with the production-oriented `games-theory` package.

The current practical use case is a CLI-driven predictor for games such as tic-tac-toe. The experimental areas remain intentionally small and support learning, comparison, and prototyping rather than production deployment.

## Documentation

- Repository guide: [`docs/guidelines/repository-guide.md`](docs/guidelines/repository-guide.md)
- Game-theory domain: [`docs/domain/games-theory-domain.md`](docs/domain/games-theory-domain.md)
- Machine-learning sandbox domain: [`docs/domain/ml-sandbox-domain.md`](docs/domain/ml-sandbox-domain.md)

## Quick Start

```bash
python -m venv .venv && source .venv/bin/activate
./scripts/tictactoe_rebuild.sh ./demo --reset
./scripts/tictactoe_run.sh ./demo
```

The repository guide contains setup, CLI, testing, packaging, and release details.
