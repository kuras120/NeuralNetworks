# Repository Guide

This guide contains operational repository information for maintainers and agents. The root `README.md` is intentionally short and visitor-oriented; use this file for setup, module maps, workflows, testing, and release details.

## Quick Links

- Agent routing and review policy: `AGENTS.md`
- Game-theory domain notes: `docs/domain/games-theory-domain.md`
- ML sandbox domain notes: `docs/domain/ml-sandbox-domain.md`
- Engineering guidelines: `docs/guidelines/engineering-guidelines.md`
- Production package guidelines: `docs/guidelines/production-package.md`
- Architecture diagrams: `docs/architecture/`
- Project planning workflow: `docs/projects/project-planning.md`
- Release workflow: `docs/guidelines/release-workflow.md`

## Repository Map

| Path | Category | Notes |
| --- | --- | --- |
| `games_theory/` | Production package | CLI entry points, predictors, resource helpers, tests, release tooling. |
| `docs/domain/` | Documentation | DDD-oriented bounded contexts, ubiquitous language, and domain rules split by domain. |
| `docs/guidelines/` | Documentation | Engineering rules, anti-patterns, repository guide, and documentation standards. |
| `docs/architecture/` | Documentation | Integration and control-flow diagrams. |
| `docs/research/` | Documentation | Research notes for tool choices, release automation alternatives, and third-party workflow options. |
| `docs/projects/` | Documentation | Temporary active project plans and the project planning workflow. |
| `scripts/` | Tooling | Repeatable local automation and agent verification scripts. |
| `NN/` | Experiment | Classical perceptron and feed-forward NN utilities used by `nn_main.py`. |
| `knn/` | Experiment | NumPy-based `KnnCore`, charting, and dataset helpers used by `knn_main.py`. |
| `TF/` | Experiment | TensorFlow prototypes (`gpu_test.py`, `neural_network.py`). |
| `scratch/` | Experiment | Throwaway explorations for quick algorithm checks. |

## Environment And Setup

1. **Python**: 3.9+ per `pyproject.toml`.
2. **Install lab dependencies** for experiments and tooling:
   ```bash
   python -m venv .venv && source .venv/bin/activate
   pip install -r requirements.txt
   ```
3. **Install the production package in editable mode** for CLI testing:
   ```bash
   pip install -e .
   ```
4. **Smoke test CLIs**:
   ```bash
   games-theory-init ./demo --overwrite
   games-theory 0 0 N N N N N N N N N N N N N N N N --config ./demo
   ```

## Production Module: `games_theory`

### Responsibilities

- Provide a reusable Q-learning backend that can be embedded via CLI or directly imported.
- Manage resource files (`config.json`, `state.json`, `qtable.json`) and bootstrap defaults for new environments.
- Offer predictable release/version tooling for packaging via Flit.

### Interfaces And Workflows

- `games-theory-init [path] [--overwrite] [--generate-internals]`: copies packaged defaults into `<path>/data/`, writes `resource_path`, and optionally regenerates derived files.
- `games-theory <player_points> <ai_points> <cells...> [--config DIR]`: validates board length, loads config/resources, triggers the predictor loop, and writes the selected move as `{"x": <column>, "y": <row>}` to standard output (`null` when no legal move exists). Coordinates are zero-based from the top-left; diagnostics are written to standard error.
- `games_theory/resources/resource.py`: owns `Resource.load/save`, `copy_defaults`, `generate_qtable_file`, and `generate_state_file`.
- `games_theory/src/default_predictor.py`: orchestrates evaluation and action selection.
- `games_theory/src/config_repository.py`: loads typed game configuration for the CLI/process boundary.
- `games_theory/src/domain_types.py`: defines shared state, points, pending-move, configuration, and Q-table contracts.
- `games_theory/src/predictor/state_encoder.py`: maps external `X/O/N` boards into bot-relative canonical states.
- `games_theory/src/predictor/state_repository.py`: owns `state.json` reads/writes for pending moves.
- `games_theory/src/predictor/qtable_repository.py`: owns `qtable.json` reads/writes and lazy neighbour registration.
- `games_theory/src/generator.py`: enumerates bot moves for canonical board states.
- `games_theory/src/move_coordinate.py`: provides `MoveCoordinate`, which validates a selected transition and maps its changed row-major cell to the public `{x, y}` coordinate.

### Configuration And Data Assets

- `games_theory/resources/data/config.json`
  - `learning`: enable/disable reinforcement updates.
  - `board-size`: square board dimension.
  - `ai-char`: external board symbol used by the bot (`X` or `O`). Runtime state is normalized relative to the bot: `-1 = bot`, `1 = opponent`, `0 = empty`.
- `state.json`: stores only pending `last_move` data (`from`, `to`, `points`, `advantage`) captured from the bot turn and used for deferred 1-step updates.
- `qtable.json`: dictionary keyed by canonical board hashes; every edge represents a bot move. `games-theory-init` resets the file to `{}` and entries are created lazily.

### Runtime And Data Flow

1. Validate input in `Process.cli_main` using `ConfigRepository` for config loading.
2. Normalize incoming board into canonical `-1/0/1`; persistent state is accessed through `StateRepository` and `QTableRepository`.
3. Reward the previous move, if recorded, using delta advantage and discounted best-future reward.
4. Enumerate neighbours with `Generator.generate_neighbour_states` and choose the next move with weighted randomness.
5. Convert the selected neighbour state's changed cell to a zero-based move coordinate and emit it as JSON.
6. Persist updated Q-table and state snapshot for subsequent invocations. See `docs/architecture/qlearning_algorithm.puml`.

### Testing

- `games_theory/test/src/test_default_predictor.py`: verifies pending-move persistence and the Q-update rule.
- `games_theory/test/src/test_generator.py`: verifies canonical neighbour generation for bot moves.
- `games_theory/test/src/test_state_encoder.py`: verifies `X/O/N` to `-1/0/1` normalization relative to `ai-char`.
- `games_theory/test/src/test_move_coordinate.py`: verifies legal transition validation and row-major state-to-coordinate conversion.
- `games_theory/test/resources/`: verifies resource copy/save helpers.

### Release Workflow

Releases are manual GitHub Actions runs from GitHub's built-in branch selector. Long-lived branches store the next development version in `pyproject.toml` using PEP 440 `.dev0`; leave the optional `version` input empty to release that clean base version, or enter an explicit `X.Y.Z` version to override it. The workflow builds artifacts and tags the clean release-version commit, generates structured release notes from merged pull requests since the previous semver tag, and opens a post-release pull request that moves the selected branch to the next patch `.dev0` version. Release helper scripts and deterministic release tooling tests live in `scripts/workflow/`.

See `docs/guidelines/release-workflow.md` for version selection, release-note grouping, and verification details.
Pull request titles must follow the standard documented there because their prefixes drive release-note categorization.

## Experiment Sandboxes

- `NN/`: `Perceptron`, `NnCore`, and associated tests; invoked by `nn_main.py`.
- `knn/`: distance calculation, neighbor voting, harmonic weighting; exercised via `knn_main.py`.
- `TF/`: TensorFlow GPU validation and prototype network definitions.
- `scratch/`: quick experiments such as line separation scripts and logic gate demos.
- Testing expectation: prioritize correctness and learning value; production packaging rigor is not required unless the change crosses production boundaries.

## Tooling And Scripts

- `requirements.txt`: consolidated dependency list for experiments and tooling.
- `chess_runtime.sh`: helper script for chess-oriented experiments; inspect parameters before running.
- `scripts/workflow/`: Python helpers used by GitHub Actions release automation and their deterministic checks.
- `scripts/verify.sh`: repeatable agent verification: compile production code, run unit tests, and check diff whitespace.
- `scripts/tictactoe_rebuild.sh`: reinstall package locally and optionally reset tic-tac-toe resources; pass `--reset` as the second argument for non-interactive reset.
- `scripts/tictactoe_run.sh`: run a tic-tac-toe CLI smoke command against generated resources.
- `dist/`: output of `flit build`; clean if artifacts become stale.

## Quality Reference

- Follow `AGENTS.md` for agent routing and review policy.
- Use `docs/domain/`, `docs/guidelines/`, and `docs/architecture/` as durable design context before changing production behaviour.
- Plan non-trivial changes in `docs/projects/` before implementation, finish each process with a test phase, move durable outcomes/TODOs to docs, and delete completed plans.
- Keep repeatable automation in `scripts/`.
- Production work in `games_theory/**` demands API stability, packaging fidelity, and adequate tests.
- Experimental directories focus on correctness and learning value.
