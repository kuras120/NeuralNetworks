# Repository Guide

This guide contains the operational information needed to set up, run, test, package, and release NeuralNetworks.

## Environment And Setup

1. **Python**: 3.9+ per `pyproject.toml`.
2. **Install the production package in editable mode** for CLI work:
   ```bash
   python -m venv .venv && source .venv/bin/activate
   pip install -e .
   ```
3. **Install production verification dependencies** before running the complete repository check:
   ```bash
   pip install -r scripts/requirements.txt
   scripts/verify.sh
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

- Predictor tests cover pending-move persistence and the Q-update rule.
- Generator tests cover canonical neighbour generation for bot moves.
- State-encoding tests cover `X/O/N` normalization relative to `ai-char`.
- Coordinate tests cover legal transition validation and row-major state-to-coordinate conversion.
- Resource tests cover default copying, loading, and saving.

### Release Workflow

Releases are manual GitHub Actions runs from GitHub's built-in branch selector. Long-lived branches store the next development version in `pyproject.toml` using PEP 440 `.dev0`; leave the optional `version` input empty to release that clean base version, or enter an explicit `X.Y.Z` version to override it. The workflow builds artifacts and tags the clean release-version commit, generates a versioned, hash-verified runtime dependency lock beside the wheel, generates structured release notes from merged pull requests since the previous semver tag, and opens a post-release pull request that moves the selected branch to the next patch `.dev0` version. Release helper scripts and deterministic release tooling tests live in `scripts/workflow/`.

See `docs/guidelines/release-workflow.md` for version selection, release-note grouping, and verification details.
Pull request titles and commit subjects must follow the conventional format documented there. Pull request title prefixes drive release-note categorization, while matching commit subjects keep repository history consistent.

## Experiment Sandboxes

The experimental areas cover perceptrons and feed-forward networks, k-NN distance and voting strategies, TensorFlow/GPU checks, and small algorithm prototypes. Each area owns an independent dependency set that can be installed with:

```bash
pip install -r <area>/requirements.txt
```

Supported values for `<area>` are `nn`, `knn`, `TF`, and `scratch`. Experimental verification prioritizes algorithmic correctness and reproducibility rather than production packaging.

## Tooling And Scripts

- `games_theory/requirements.txt`: production runtime compatibility and test coverage dependencies; `pyproject.toml` remains authoritative for installed package runtime dependencies.
- `scripts/requirements.txt`: complete production-verification environment, including `games_theory/requirements.txt` and package build tooling.
- `nn/requirements.txt`, `knn/requirements.txt`, `TF/requirements.txt`, `scratch/requirements.txt`: sandbox-specific dependencies derived from each area's imports.
- `scripts/workflow/`: release automation helpers used by GitHub Actions and their deterministic checks.
- `scripts/workflow/build_dependency_lock.sh`: generates and verifies the release dependency lock in a clean environment, including universal-wheel availability and CLI smoke checks.
- `scripts/workflow/generate_dependency_lock.py`: reads runtime requirements from the built wheel metadata and uses `pip-compile` to emit exact transitive pins with SHA-256 hashes.
- `scripts/verify.sh`: repeatable verification: compile production code, run unit, release tooling tests and build package artifacts.
- `scripts/tictactoe_rebuild.sh`: reinstall package locally and optionally reset tic-tac-toe resources; pass `--reset` as the second argument for non-interactive reset.
- `scripts/tictactoe_run.sh`: run a tic-tac-toe CLI smoke command against generated resources.
- `dist/`: output of `flit build`; clean if artifacts become stale.

Shell automation is deterministic and fails safely with `set -euo pipefail`. Commands that overwrite local resources expose that behavior explicitly.
