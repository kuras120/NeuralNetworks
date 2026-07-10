# NeuralNetworks

NeuralNetworks is a machine-learning playground and a growing game-theory package. The repository combines exploratory ML experiments with a production-oriented Python library for Q-learning in turn-based games.

The main practical target today is a reusable Q-learning backend for games like tic-tac-toe. The longer-term direction is to keep extending the same ideas toward richer turn-based domains, including chess experiments.

## What Is Inside

- `games_theory/`: installable Python package with CLI tools, resource management, and a Q-learning predictor loop.
- `NN/`, `knn/`, `TF/`, `scratch/`: experimental sandboxes for neural networks, k-NN, TensorFlow checks, and quick prototypes.
- `docs/`: domain notes, engineering guidelines, architecture diagrams, and project planning workflow.
- `scripts/`: repeatable local automation and verification scripts.

## Documentation

- Game-theory domain model: [`docs/domain/games-theory-domain.md`](docs/domain/games-theory-domain.md)
- ML sandbox domain model: [`docs/domain/ml-sandbox-domain.md`](docs/domain/ml-sandbox-domain.md)
- Repository guide: [`docs/guidelines/repository-guide.md`](docs/guidelines/repository-guide.md)
- Engineering guidelines: [`docs/guidelines/engineering-guidelines.md`](docs/guidelines/engineering-guidelines.md)
- Production package guidelines: [`docs/guidelines/production-package.md`](docs/guidelines/production-package.md)
- Architecture diagrams: [`docs/architecture/`](docs/architecture/)
- Project planning workflow: [`docs/projects/project-planning.md`](docs/projects/project-planning.md)
- Agent workflow: [`AGENTS.md`](AGENTS.md)

## Quick Start

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
./scripts/tictactoe_rebuild.sh ./demo --reset
./scripts/tictactoe_run.sh ./demo
```

For CLI examples and detailed workflows, use the repository guide.
