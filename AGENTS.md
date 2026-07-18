# Agent Briefing

Use this file first to identify the required repository context. Read every document routed for the touched area before planning, reviewing, or changing it. Detailed rules and checklists belong in `docs/**`; do not duplicate them here.

## Required Workflow

- For non-trivial changes, follow `docs/guidelines/project-lifecycle.md`, including its proposal and implementation acceptance gates.
- Keep plans under `docs/projects/**` only while work is active.
- Use the smallest applicable set of documents from the routing table below; when a task crosses areas, combine their required context.
- Preserve user changes already present in the worktree and keep code, documentation, plans, and scripts in English.

## Repository Map

| Path | Responsibility |
| --- | --- |
| `README.md` | Short human-facing project purpose, maturity, documentation links, and quick start. |
| `pyproject.toml` | Package metadata, runtime dependencies, Python compatibility, CLI entry points, and build configuration. |
| `games_theory/process.py` | CLI validation, configuration loading, predictor orchestration, and JSON result output. |
| `games_theory/resources/**` | Packaged defaults, resource initialization, copying, loading, and saving. |
| `games_theory/src/config_repository.py` | Typed configuration loading at the process boundary. |
| `games_theory/src/domain_types.py` | Shared state, points, pending-move, configuration, coordinate, and Q-table contracts. |
| `games_theory/src/default_predictor.py` | Evaluation, action selection, and persistence orchestration. |
| `games_theory/src/predictor/**` | State encoding, reward policy, scoring, action selection, and state/Q-table repositories. |
| `games_theory/src/generator.py` | Legal bot-move generation from canonical states. |
| `games_theory/src/move_coordinate_deriver.py` | Selected-transition validation and public coordinate derivation. |
| `games_theory/test/**` | Production package unit, resource, predictor, and CLI tests. |
| `games_theory/README.md`, `games_theory/changelog` | Package-local usage and historical package changes. |
| `nn/**` | Perceptron and feed-forward neural-network experiments. |
| `knn/**` | k-NN experiments, dataset helpers, and charting. |
| `TF/**` | TensorFlow and GPU prototypes. |
| `scratch/**` | Disposable algorithm checks and prototypes. |
| `data/**` | Local runtime configuration, pending-move state, and learned Q-table; treat as user data and do not modify unless explicitly requested. |
| `docs/domain/games-theory-domain.md` | Game rules, Q-learning language, state semantics, and persistence meaning. |
| `docs/domain/ml-sandbox-domain.md` | Experiment boundaries, terminology, and sandbox expectations. |
| `docs/guidelines/repository-guide.md` | Environment, commands, module operation, testing, tooling, and release overview. |
| `docs/guidelines/engineering-guide.md` | Application design, coding, testing, and review rules. |
| `docs/guidelines/production-package-guide.md` | Production package, CLI, persistence, packaging, and verification checklist. |
| `docs/guidelines/project-lifecycle.md` | Proposal, approval, implementation, and closeout process. |
| `docs/guidelines/release-workflow.md` | Versioning, release notes, and publication process. |
| `docs/architecture/**` | Runtime and integration diagrams. |
| `docs/projects/**` | Temporary plans for active non-trivial work. |
| `docs/research/**` | Durable investigations and evaluated tooling alternatives. |
| `scripts/verify.sh`, `scripts/requirements.txt` | Complete local verification entry point and its dependencies. |
| `scripts/tictactoe_*.sh` | Repeatable local package rebuild and CLI smoke workflows. |
| `scripts/workflow/**` | Release preparation, dependency locking, release-note generation, version PR creation, and deterministic tooling tests. |
| `.github/workflows/test.yml` | Repository test workflow. |
| `.github/workflows/release.yml` | Manual package build and GitHub release workflow. |
| `dist/**` | Generated package artifacts; do not review or commit. |

## Task Routing

| Task or touched area                                                 | Read before work                                                                                                                      |
|----------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------|
| Any repository change                                                | `docs/guidelines/repository-guide.md` and `docs/guidelines/engineering-guide.md`                                                      |
| `games_theory/**`                                                    | `docs/domain/games-theory-domain.md`, `docs/guidelines/production-package-guide.md`, and relevant `docs/architecture/**` diagrams     |
| Game rules, state semantics, Q-learning meaning, or domain naming    | `docs/domain/games-theory-domain.md`                                                                                                  |
| Persistence, resource formats, service boundaries, or predictor flow | `docs/domain/games-theory-domain.md`, `docs/guidelines/production-package-guide.md`, and `docs/architecture/qlearning_algorithm.puml` |
| CLI orchestration or integration flow                                | `docs/guidelines/repository-guide.md`, relevant `docs/architecture/**` diagrams, and `docs/guidelines/production-package-guide.md`     |
| `nn/`, `knn/`, `TF/`, or `scratch/`                                  | `docs/domain/ml-sandbox-domain.md` and the experiment guidance in `docs/guidelines/repository-guide.md`                               |
| Root `data/**`                                                       | `docs/domain/games-theory-domain.md`, `docs/guidelines/production-package-guide.md`, and `docs/architecture/qlearning_algorithm.puml` |
| Setup, tests, packaging, or repository scripts                       | Relevant sections of `docs/guidelines/repository-guide.md`; add the guide for the touched code area                                  |
| Release workflow, versioning, release notes, or dependency locks     | `docs/guidelines/repository-guide.md`, `docs/guidelines/release-workflow.md`, and relevant `docs/research/**` notes                    |
| Tool selection or previously researched automation                   | Relevant `docs/research/**` notes                                                                                                     |
| Root `README.md`                                                     | Relevant domain documents plus user-facing setup and interfaces in `docs/guidelines/repository-guide.md`                              |
| Domain or terminology documentation                                  | Relevant `docs/domain/**` document and implemented behavior                                                                          |
| Engineering standards, review, or refactoring                        | `docs/guidelines/engineering-guide.md` plus the domain and production guide for the touched area                                      |
| Operational documentation                                            | `docs/guidelines/repository-guide.md` plus the implementation and scripts being documented                                            |
| Architecture documentation                                          | Relevant `docs/architecture/**`, domain guide, and implemented runtime flow                                                           |
| Non-trivial project planning and delivery                            | `docs/guidelines/project-lifecycle.md`                                                                                                |

## Repository-Specific Instructions

- Treat `games_theory/**` and changes to `config.json`, `state.json`, or `qtable.json` formats as production work.
- Keep repeatable verification and process automation under `scripts/**`.
- Update durable domain, guideline, or architecture documentation when behaviour, boundaries, persistence meaning, or runtime flow changes.
- During review, apply the review standard in `docs/guidelines/engineering-guide.md` and the checklist for the touched area.
