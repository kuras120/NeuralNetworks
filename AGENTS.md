# Agent Briefing

This file orchestrates agent work in the repository. Use it first, then open the referenced domain, guideline, architecture, project-plan, and repository-guide resources that match the task.

---

## 1. Repository Map

| Area | Paths | Required context |
| --- | --- | --- |
| Production package | `games_theory/**` | Read `docs/guidelines/repository-guide.md`, `docs/domain/games-theory-domain.md`, `docs/guidelines/engineering-guidelines.md`, `docs/guidelines/production-package.md`, and relevant diagrams in `docs/architecture/**`. |
| Domain documentation | `docs/domain/**` | Read before changing business language, game rules, persistence meaning, or DDD boundaries. |
| Engineering guidelines | `docs/guidelines/**` | Read before refactors, service extraction, persistence changes, review work, or documentation changes. |
| Architecture and integrations | `docs/architecture/**` | Read before changing runtime flow, integrations, CLI orchestration, or predictor/control-flow design. |
| Project plans | `docs/projects/**` | Read or create a temporary plan before every non-trivial implementation change; wait for user confirmation or feedback before implementation; wait again for implementation/test acceptance before cleanup; delete completed plans after user review, implementation, tests, and durable documentation updates. |
| Automation scripts | `scripts/**` | Store repeatable process automation and agent verification scripts here. |
| Repository guide | `docs/guidelines/repository-guide.md` | Read for repository setup, module map, workflows, tests, and release process. |
| Experimental sandboxes | `NN/`, `knn/`, `TF/`, `scratch/`, `data/` | Read local code, `docs/domain/ml-sandbox-domain.md`, and `docs/guidelines/repository-guide.md` experiment notes unless the change crosses production boundaries. |

---

## 2. Review Scope & Priorities

| Area | Directories | Expectations |
| --- | --- | --- |
| **Production** | `games_theory/**` | Treat as shipping library: maintain API stability, packaging correctness, CLI compatibility, resource integrity, and tests. |
| **Documentation** | `docs/**`, `AGENTS.md`, `README.md` | Keep domain notes, guidelines, diagrams, plans, and workflows synchronized with code. |
| **Automation** | `scripts/**` | Keep repeatable process automation and verification scripts here; prefer scripts over ad hoc repeated command sequences. |
| **Experimental** | `NN/`, `knn/`, `TF/`, `scratch/`, `data/` | Focus on algorithmic correctness and clarity. Enterprise patterns, heavy refactors, or strict packaging polish are optional unless needed to fix real bugs. |

Notes:
- When in doubt, defer to `docs/guidelines/repository-guide.md` for production-module behaviour and release flow.
- Experiments can evolve rapidly; keep changes localized and avoid blocking research velocity.
- Resource format changes (`config.json`, `state.json`, `qtable.json`) are production changes.
- Documentation, plans, scripts, and code must be written in English.

---

## 3. Task Routing

- **Changing game rules, state semantics, Q-learning meaning, or naming:** read `docs/domain/games-theory-domain.md` first.
- **Changing ML sandbox experiment structure, datasets, or prototype semantics:** read `docs/domain/ml-sandbox-domain.md` first.
- **Changing persistence, service boundaries, composition, anti-pattern cleanup, or documentation standards:** read `docs/guidelines/engineering-guidelines.md` first.
- **Changing runtime flow, CLI orchestration, integration points, or predictor loop:** read `docs/architecture/**` first, especially `docs/architecture/qlearning_algorithm.puml`.
- **Changing `games_theory/**`:** also read `docs/guidelines/production-package.md`.
- **Changing setup, scripts, tests, packaging, or release process:** read `docs/guidelines/repository-guide.md`.
- **Making a non-trivial change:** create or update a temporary plan under `docs/projects/**`, share it with the user, and wait for confirmation or feedback before implementation. After implementation and tests, share the result and wait for user acceptance before deleting the plan, removing temporary files, or moving final notes into durable docs.
- **Adding repeatable verification or process automation:** add or update a script under `scripts/**`.
- **Reviewing code:** use the delivery workflow, review checklist, and relevant guideline docs for touched paths.
- **Documenting changes:** every change must be documented in the location selected from the repository map. Prefer a focused Markdown file in the relevant `docs/**` subdirectory over adding unrelated details to an existing catch-all document.

---

## 4. Delivery Workflow

Every non-trivial change follows the same sequence:

1. **Planning**: write or update a short plan in `docs/projects/**` with scope, implementation steps, and verification commands.
2. **Review Gate**: share the plan with the user and wait for confirmation or requested changes before implementation.
3. **Implementation**: apply the planned changes with the smallest coherent code/docs/script diff.
4. **Tests**: run repeatable verification, preferably through `scripts/**`.
5. **Acceptance Gate**: share the implementation and test results with the user, then wait for acceptance or requested changes.
6. **Closeout**: move durable outcomes and TODOs into the relevant docs, remove temporary files, then delete the completed project plan.

For small one-line fixes, an in-message plan is enough, but the same order still applies: plan first, implement second, test last.

---

## 5. Review Checklist

### Production (`games_theory/**`)
- ✅ Verify CLI contracts (`games-theory`, `games-theory-init`) remain backward compatible.
- ✅ Ensure resource handling (`config.json`, `state.json`, `qtable.json`) remains durable and avoids accidental data loss.
- ✅ Confirm tests exist or are updated when modifying predictors, generators, repositories, or resource utilities.
- ✅ Check packaging metadata (`pyproject.toml`, version bump, changelog) when building releases.
- ✅ Update `docs/domain/**`, `docs/guidelines/**`, or `docs/architecture/**` when behaviour, boundaries, or flow changes.

### Experimental Areas
- ✅ Prioritize correctness of algorithms and experiments.
- ✅ Accept lightweight structure; avoid large-scale refactors purely for style.
- ✅ Document non-obvious behaviour inline or in the nearest README/doc when it affects future work.

### Documentation
- ✅ Keep links current after moves or renames.
- ✅ Prefer stable docs under `docs/domain/**`, `docs/guidelines/**`, and `docs/architecture/**` instead of one-off notes.
- ✅ Root `AGENTS.md` should route agents to resources; detailed system descriptions belong in the referenced docs.
- ✅ Keep active change plans under `docs/projects/**` for non-trivial work, and remove them after implementation and tests.
- ✅ Keep all documentation and plans in English.

### Automation
- ✅ Put repeatable workflows, smoke tests, and agent verification commands in `scripts/**`.
- ✅ Keep scripts deterministic, shell-safe (`set -euo pipefail` for Bash), and documented from `README.md` or `docs/guidelines/repository-guide.md` when user-facing.

---

## 6. Review Style

- Focus on real bugs, behavioural regressions, data-loss risks, and missing tests.
- Keep findings actionable: explain risk/impact and point to specific files/lines.
- Avoid cosmetic nitpicks unless they hide a functional issue or make domain/persistence semantics unclear.

---

## 7. Documentation Authoring Instructions

Use these instructions when creating or refreshing visitor READMEs, repository guides, and agent policies. Keep the guidance here so agents do not have to discover a separate template directory.

### README / Visitor Overview
- Keep root `README.md` short and human-facing. It is not the AI-agent entry point.
- Describe the project motivation, current purpose, and major directories at a high level.
- Link to concrete documentation files under `docs/**` for operational details.
- Avoid embedding repository maps, long setup workflows, review policies, or release details in root `README.md`; put those in `docs/guidelines/repository-guide.md`.

### Repository Guide
- Store detailed setup, module maps, workflows, testing, tooling, and release information in `docs/guidelines/repository-guide.md`.
- Include these sections when refreshing it:
  1. `Quick Links` - agent routing, domain docs, architecture docs/diagrams, release notes or changelog paths.
  2. `Repository Map` - table with path, category, and notes.
  3. `Environment And Setup` - supported runtimes, dependency install, virtualenv/setup, smoke tests.
  4. `Production Module` - responsibilities, interfaces/workflows, configuration/resources, runtime/data flow, tests, release/deployment, outstanding work.
  5. `Experiment Sandboxes` - each experimental area, how to run it, and expectations.
  6. `Tooling And Scripts` - helper scripts, requirements, automation entry points under `scripts/**`.
  7. `Quality Reference` - how repository work ties back to `AGENTS.md`.
- Close by reminding contributors to keep docs synchronized with architecture changes.

### AGENTS / Agent Briefing
- Use the title format `# Agent Briefing`.
- State that the file orchestrates agent work and links to the repository guide plus relevant docs.
- Include:
  1. review scope/priorities table,
  2. production and experimental checklists,
  3. review style expectations,
  4. repository-specific routing to detailed docs.
- Keep findings/action guidance focused on correctness, regressions, user data safety, and missing tests.

### Request Template For New Repositories
When asking an agent to align README + AGENTS in another project, provide:
- project name and mission,
- production directories and experimental directories,
- runtime versions and dependency setup,
- key modules/packages,
- testing and release commands,
- special workflows such as CLIs, packaging, or deployment.

Required deliverables:
1. Updated root `README.md` as a short visitor overview.
2. Updated repository guide under `docs/guidelines/**` for detailed operational docs.
3. Updated `AGENTS.md` routing agents to relevant docs and checklists.
4. Optional docs under `docs/domain/**`, `docs/guidelines/**`, or `docs/architecture/**` when the project needs durable design context.
