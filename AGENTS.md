# Agent Briefing

Before implementation, share a short temporary Markdown plan and wait for user confirmation or feedback. Use tables or diagrams where helpful, without a fixed section template. Track implementation as checklist items and update them as work progresses. Remove the plan before opening a PR.

Find the acceptance checks in `mise.toml` and run the relevant tasks before completion; report failures or unavailable checks. No separate human acceptance gate is required.

| Task | Context |
| --- | --- |
| Game rules, state, learning | [Game domain](docs/domain/games-theory-domain.md) |
| Runtime, CLI, persistence | [Architecture](docs/architecture/runtime.md), [usage](docs/usage.md) |
| ML experiments | [Sandbox domain](docs/domain/ml-sandbox-domain.md), local code |
| Releases | [Release workflow](docs/release.md), `scripts/workflow/` |
| Tool choices | [Research](docs/research/) |
| Future work | [INBOX](INBOX.md): short actionable items, not a requirements index |

- Preserve public APIs, CLI output and user resources in `games_theory/`; test behaviour changes.
- Keep experiments in `nn/`, `knn/`, `TF/` and `scratch/` lightweight and focused on correctness.
- Keep documentation concise, human-facing and synchronized with behaviour. Prefer tables and diagrams when they improve clarity.
- Keep repeatable checks in `scripts/` and expose acceptance tasks through `mise.toml`.
- Review for bugs, regressions, data loss and missing tests; give actionable findings with file/line references.
- Write code, documentation and plans in English.
