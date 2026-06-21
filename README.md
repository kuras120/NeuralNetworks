# Codebase Guide: NeuralNetworks

This repository contains two personas:
- **Production surface – `games_theory/`**: a Flit-packaged Q-learning backend with CLI tooling, resource loaders, and release automation.
- **Experiment sandboxes – `NN/`, `knn/`, `TF/`, `scratch/`**: self-contained research playgrounds for neural networks, k-NN, TensorFlow, and quick prototypes.

For review expectations see `AGENTS.md`; this README focuses on how to navigate and operate the codebase.

---

## 1. Quick Links
- **Review Policy:** [`AGENTS.md`](AGENTS.md)
- **Architecture Diagrams:** [`games_theory/architecture/`](architecture/)
- **Changelog & Release Scripts:** [`games_theory/changelog`](games_theory/changelog), [`games_theory/generate_changelog.sh`](games_theory/generate_changelog.sh), [`games_theory/version_bump.py`](games_theory/version_bump.py)

---

## 2. Repository Map

| Path            | Category           | Notes                                                                                      |
|-----------------|--------------------|--------------------------------------------------------------------------------------------|
| `games_theory/` | Production package | CLI entry points, predictors, resource helpers, architecture docs, tests, release tooling. |
| `NN/`           | Experiment         | Classical perceptron / feed-forward NN utilities used by `nn_main.py`.                     |
| `knn/`          | Experiment         | NumPy-based `KnnCore`, charting, and dataset helpers used by `knn_main.py`.                |
| `TF/`           | Experiment         | TensorFlow prototypes (`gpu_test.py`, `neural_network.py`).                                |
| `scratch/`      | Experiment         | Throwaway explorations (line separation, logic gates, etc.).                               |

---

## 3. Environment & Setup
1. **Python**: 3.9+ (per `pyproject.toml`).
2. **Install lab dependencies** (experiments + tooling):
   ```bash
   python -m venv .venv && source .venv/bin/activate
   pip install -r requirements.txt
   ```
3. **Install the production package in editable mode** (for CLI testing):
   ```bash
   pip install -e .
   ```
4. **Smoke test CLIs**:
   ```bash
   games-theory-init ./demo --overwrite
   games-theory 0 0 N N N N N N N N N N N N N N N N --config ./demo
   ```

---

## 4. Production Module – `games_theory`

### 4.1 Responsibilities
- Provide a reusable Q-learning backend that can be embedded via CLI or directly imported.
- Manage resource files (`config.json`, `state.json`, `qtable.json`) and bootstrap defaults for new environments.
- Offer predictable release/version tooling for packaging via Flit.

### 4.2 Interfaces & Workflows
- **CLIs (declared in `pyproject.toml`):**
  - `games-theory-init [path] [--overwrite] [--generate-internals]`
    - Copies packaged defaults into `<path>/data/`, writes `resource_path`, optionally regenerates derived files.
  - `games-theory <player_points> <ai_points> <cells...> [--config DIR]`
    - Validates board length, loads config/resources, prints the state, and triggers the predictor loop.
- **Resource helpers (`games_theory/resources/resource.py`):** `Resource.load/save`, `copy_defaults`, and `generate_internal_files`.
- **Predictor pipeline (`games_theory/src/`):**
  - `default_predictor.py` orchestrates evaluation + action selection.
  - `predictor/state_encoder.py` maps external `X/O/N` boards into bot-relative canonical states.
  - `generator.py` enumerates bot moves for canonical board states.
  - Tests cover persistence (`test/resources`) and source behavior (`test/src`).

### 4.3 Configuration & Data Assets
- `games_theory/resources/data/config.json`
  - `learning`: enable/disable reinforcement updates.
  - `board-size`: board dimension (square).
  - `ai-char`: symbol used by the bot on the external board (`X` or `O`). CLI input still uses `X/O/N`, but runtime state is normalized relative to the bot: `-1 = bot`, `1 = opponent`, `0 = empty`.
- Derived files:
- `state.json`: stores only the pending `last_move` payload (`from`, `to`, `points`, `advantage`) captured from the bot turn and used for the deferred 1-step update after the opponent move.
  - `qtable.json`: dictionary keyed by canonical board hashes, where every edge represents a bot move. `games-theory-init` resets the file to `{}`; entries are created lazily when a state is evaluated for the first time.

### 4.4 Runtime & Data Flow
1. **Input validation** via `Process.cli_main`.
2. **State bootstrap**: load matrices, Q-table, optional `state.json`, then normalize the incoming board into the canonical `-1/0/1` representation.
3. **Reward previous move** (if recorded) using delta advantage and discounted best-future reward (implemented in `DefaultPredictor.evaluate`).
4. **Enumerate neighbours** (`Generator.generate_neighbour_states`) and choose the next move with weighted randomness (`DefaultPredictor.predict`).
5. **Persist** updated Q-table and state snapshot for subsequent invocations. (See `architecture/qlearning_algorithm.puml`.)

### 4.5 Testing
- `games_theory/test/src/test_default_predictor.py` – verifies persistence of pending moves and the Q-update rule.
- `games_theory/test/src/test_generator.py` – verifies canonical neighbour generation for bot moves.
- `games_theory/test/src/test_state_encoder.py` – verifies `X/O/N -> -1/0/1` normalization relative to `ai-char`.
- `games_theory/test/resources/` – ensures resource copy/save helpers behave correctly.
- `games_theory/test/test_generate_changelog.sh` – future smoke test for a release script.

### 4.6 Release Workflow
1. Update changelog entries in `games_theory/changelog`.
2. Run `python games_theory/version_bump.py bump` (or `version` to read).
3. Build artifacts via `flit build` (requires `flit_core` per `pyproject.toml`).
4. `generate_changelog.sh $VERSION` is used in CI to push notes into `$GITHUB_ENV`.

### 4.7 Outstanding Work
- Extend packaged resources if additional heuristics or pretrained tables are required.
- Continue fleshing out predictor policies beyond a single-step weighted choice if new games demand it.

---

## 5. Experiment Sandboxes
- **`NN/`** – `Perceptron`, `NnCore`, and associated tests; invoked by `nn_main.py`.
- **`knn/`** – Distance calculation, neighbor voting, harmonic weighting; exercised via `knn_main.py`.
- **`TF/`** – TensorFlow GPU validation + prototype network definitions.
- **`scratch/`** – Quick experiments (line separation scripts, logic gate demos).
- **Testing expectations**: prioritize correctness of experiments, but heavy production hygiene is not required (see `AGENTS.md`).

---

## 6. Tooling & Scripts
- `requirements.txt` – consolidated dependency list for experiments and tooling (NumPy, matplotlib, scikit-learn, jsbeautifier, coverage, etc.).
- `chess_runtime.sh` – helper script to orchestrate chess-oriented experiments (inspect parameters before running).
- `dist/` – output of `flit build`; clean if artifacts become stale.

---

## 7. Review & Quality Reference
- Follow the scoped policy in `AGENTS.md`.
- Production work (`games_theory/**`) demands API stability, packaging fidelity, and adequate tests.
- Experimental directories focus on correctness and learning value—avoid over-refactoring or applying enterprise patterns unless needed for clarity.

---

Keep this Codebase Guide synchronized with major architecture or workflow changes so contributors and agents can self-serve quickly.
