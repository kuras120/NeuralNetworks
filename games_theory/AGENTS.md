# Agent Briefing: `games_theory`

Use this module-specific policy together with the repository-wide guide in [`../README.md`](../README.md) (see sections 4–7 for architecture, resources, and testing workflows).

---

## 1. Review Scope & Priorities

| Area                   | Directories                                         | Expectations                                                                                                                                                                                                                          |
|------------------------|-----------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Production Package** | `games_theory/**`                                   | Maintain installability via Flit, stable public APIs, CLI behaviour (`games-theory`, `games-theory-init`), resource/config compatibility (`config.json`, `state.json`, `qtable.json`), persistence correctness, and regression tests. |
| **Shared resources**   | `games_theory/resources/**`, `games_theory/test/**` | Treat as part of the production surface; ensure packaging includes defaults and tests cover new functionality.                                                                                                                        |

Notes:
- This module is published independently; no repo-relative assumptions or hard-coded local paths.
- Resource formats must remain backward-compatible unless migration scripts/tests are provided.

---

## 2. Review Checklist

### Packaging & Release
- ✅ `pyproject.toml` matches reality (entry points, dependencies, Python version).
- ✅ `games_theory/__init__.py` version increments with releases and changelog entries.
- ✅ `flit build` / `pip install .` succeed (no missing files/resources).

### Runtime & CLI
- ✅ `games-theory` validates inputs, loads configs, and triggers predictor flow without regressions.
- ✅ `games-theory-init` copies defaults, honours `--overwrite`, and optionally regenerates internals.
- ✅ Resource helpers never corrupt or silently overwrite user data.

### Predictors & Logic
- ✅ Changes to `DefaultPredictor`, `Generator`, or helpers preserve state compatibility and include tests.
- ✅ Q-table / state persistence handles new fields safely.
- ✅ Architecture docs are updated when the control flow changes materially.

### Tests
- ✅ Unit tests updated/added (`games_theory/test/**`).
- ✅ CLI / integration smoke tests are documented or automated when behavior changes.

---

## 3. Review Style
- Prioritize functional correctness, installability, and user data safety over refactoring.
- Provide actionable findings referencing files/lines and describe impact (e.g., “breaks CLI contract”, “corrupts qtable state”).
- Cosmetic nits are acceptable only when they hide bugs or confuse packaging.

---

If new rules emerge, update both this file and the root templates in `docs/templates/` to keep future projects consistent.
