# Production Package Guide

Use these checks when touching `games_theory/**`. They replace the old module-local agent briefing; root `AGENTS.md` remains the only agent briefing entry point.

## Scope And Priorities

| Area               | Paths                                               | Expectations                                                                                                                                                                             |
|--------------------|-----------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Production package | `games_theory/**`                                   | Maintain installability via Flit, stable public APIs, CLI behaviour (`games-theory`, `games-theory-init`), resource/config compatibility, persistence correctness, and regression tests. |
| Shared resources   | `games_theory/resources/**`, `games_theory/test/**` | Treat as part of the production surface; ensure packaged defaults are valid and tests cover new functionality.                                                                           |

Notes:
- The package may be published independently; avoid repo-relative assumptions in package runtime code.
- Resource formats must remain backward-compatible unless migration scripts and tests are provided.

## Packaging And Release Checklist

- `pyproject.toml` matches the current version, entry points, dependencies, and supported Python version.
- `flit build` or `pip install .` succeeds without missing package files/resources when release work is in scope.

## Runtime And CLI Checklist

- `games-theory` validates inputs, loads configs, and triggers predictor flow without regressions.
- `games-theory-init` copies defaults, honours `--overwrite`, and regenerates internals only when requested.
- Resource helpers avoid corrupting or silently overwriting user data.

## Predictor And Persistence Checklist

- Changes to `DefaultPredictor`, `Generator`, repositories, or predictor policies preserve state compatibility and include tests.
- `qtable.json` and `state.json` changes are documented in `docs/domain/games-theory-domain.md` and covered by tests.
- Architecture docs are updated when predictor/control flow changes materially.

## Test Checklist

- Unit tests under `games_theory/test/**` are updated for production logic changes.
- CLI or integration smoke tests are scripted under `scripts/**` when they become repeatable verification steps.
