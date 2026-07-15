# Agent Briefing

Use this file first to identify the required repository context. Read every document routed for the touched area before planning, reviewing, or changing it. Detailed rules and checklists belong in `docs/**`; do not duplicate them here.

## Required Workflow

- For non-trivial changes, follow `docs/guidelines/project-lifecycle.md`, including its proposal and implementation acceptance gates.
- Keep plans under `docs/projects/**` only while work is active.
- Use the smallest applicable set of documents from the routing table below; when a task crosses areas, combine their required context.
- Preserve user changes already present in the worktree and keep code, documentation, plans, and scripts in English.

## Task Routing

| Task or touched area                                                 | Read before work                                                                                                                      |
|----------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------|
| Any repository change                                                | `docs/guidelines/repository-guide.md` and `docs/guidelines/engineering-guide.md`                                                      |
| `games_theory/**`                                                    | `docs/domain/games-theory-domain.md`, `docs/guidelines/production-package-guide.md`, and relevant `docs/architecture/**` diagrams     |
| Game rules, state semantics, Q-learning meaning, or domain naming    | `docs/domain/games-theory-domain.md`                                                                                                  |
| Persistence, resource formats, service boundaries, or predictor flow | `docs/domain/games-theory-domain.md`, `docs/guidelines/production-package-guide.md`, and `docs/architecture/qlearning_algorithm.puml` |
| CLI orchestration or integration flow                                | Relevant `docs/architecture/**` diagrams and `docs/guidelines/production-package-guide.md`                                            |
| `NN/`, `knn/`, `TF/`, `scratch/`, or `data/`                         | `docs/domain/ml-sandbox-domain.md` and the experiment guidance in `docs/guidelines/repository-guide.md`                               |
| Setup, tests, packaging, repository scripts, or release work         | Relevant sections of `docs/guidelines/repository-guide.md`; for releases also read `docs/guidelines/release-workflow.md`              |
| Tool selection or previously researched automation                   | Relevant `docs/research/**` notes                                                                                                     |
| Documentation, review, or refactoring                                | Relevant standards in `docs/guidelines/engineering-guide.md` plus the guide for the touched area                                      |
| Non-trivial project planning and delivery                            | `docs/guidelines/project-lifecycle.md`                                                                                                |

## Repository-Specific Instructions

- Treat `games_theory/**` and changes to `config.json`, `state.json`, or `qtable.json` formats as production work.
- Keep repeatable verification and process automation under `scripts/**`.
- Update durable domain, guideline, or architecture documentation when behaviour, boundaries, persistence meaning, or runtime flow changes.
- During review, apply the review standard in `docs/guidelines/engineering-guide.md` and the checklist for the touched area.
