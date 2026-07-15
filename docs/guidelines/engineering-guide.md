# Engineering Guide

Use these guidelines when designing or reviewing changes. `AGENTS.md` decides which guideline applies to a task; this file captures project-level rules that should not be scattered through implementation comments.

## Design Principles

- Keep production code in `games_theory/**` explicit about persistence, CLI contracts, and resource ownership.
- Put lifecycle and mode decisions in the upper-level orchestrator; lower-level services should expose explicit operations instead of boolean switches that change persistence or side effects.
- Prefer small composed services over broad classes when a component owns a distinct persistence or policy concern.
- Keep experimental directories lightweight; do not introduce production-grade structure there unless it fixes a concrete problem.
- Update documentation in the same change when behaviour, public CLI usage, persistence format, or architecture flow changes.
- Plan non-trivial changes in `docs/projects/**` before implementation, finish with a test phase, then delete completed project plans after durable docs/TODOs are updated.
- Store repeatable process automation and verification commands under `scripts/**`.
- Write documentation, plans, scripts, and code in English.

## Anti-patterns

- Do not read/write `config.json`, `state.json`, or `qtable.json` directly from orchestration code when a repository/service exists.
- Do not duplicate current state across multiple resource files unless the lifecycle is intentionally different and documented.
- Do not make Q-table semantics depend on external symbols (`X`/`O`) when canonical bot-relative state is available.
- Do not silently overwrite user resources outside explicit init/reset workflows.
- Do not hide write/read-only mode changes behind generic boolean flags inside lower-level services; split the operation and let the orchestrator choose.

## Documentation Standard

- Root `README.md` is a short visitor overview: motivation, purpose, and links to concrete docs.
- Root `AGENTS.md` is the agent orchestrator: it contains task-to-document routing and repository-specific agent instructions, while detailed standards and checklists live under `docs/**`.
- `docs/domain/**` contains domain language, rules, and bounded-context notes split by concrete domain.
- `docs/guidelines/**` contains engineering rules, review expectations, documentation standards, repository guide, and anti-patterns.
- `docs/architecture/**` contains diagrams and integration/control-flow descriptions.
- `docs/projects/**` contains temporary active project plans; completed plans are deleted after tests.
- `docs/guidelines/repository-guide.md` contains repository map, setup, workflows, testing, tooling, and release notes.
- `scripts/**` contains repeatable automation and verification entry points.

When changing documentation:

- Keep links current after moves or renames.
- Put durable information in the most focused domain, guideline, architecture, or research document instead of a temporary plan or catch-all file.
- Keep active plans under `docs/projects/**` and remove them only through the project lifecycle closeout.
- Write documentation and plans in English.

## Review Standard

- Focus on correctness, behavioural regressions, user-data loss, persistence safety, public contract changes, and missing tests.
- Make findings actionable by explaining the impact and pointing to specific files and lines.
- Avoid cosmetic findings unless they hide a functional problem or make domain or persistence semantics unclear.
- For production changes, use `docs/guidelines/production-package-guide.md` as the detailed checklist.
- For experimental code, prioritize algorithmic correctness and clarity; require production-grade structure only when a concrete risk justifies it.
- For documentation changes, verify ownership, consistency, and links rather than duplicating the same guidance across entry points.
