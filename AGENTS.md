# Agent Briefing

Use this document alongside the Codebase Guide in [`README.md`](README.md). The README’s sections 2–7 explain the repository map, workflows, and release process referenced below.

---

## 1. Review Scope & Priorities

| Area                                           | Directories                                   | Expectations                                                                                                                                                |
|------------------------------------------------|-----------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Production**                                 | `games_theory/**`                             | Treat as shipping library: maintain API stability, packaging correctness, CLI compatibility, resource integrity, and tests.                                 |
| Documentation (treated as production-adjacent) | `architecture/*.puml`, `docs/**`, `AGENTS.md` | Keep diagrams/examples in sync with code, document any new exchanges or workflows before enabling in prod.                                                  |
| **Experimental**                               | `NN/`, `knn/`, `TF/`, `scratch/`, `data/`     | Focus on algorithmic correctness and clarity. Enterprise patterns, heavy refactors, or strict packaging polish are optional unless needed to fix real bugs. |

Notes:
- When in doubt, defer to README §4 (Production Module) for intended behavior and release flow.
- Experiments can evolve rapidly; keep changes localized and avoid blocking research velocity.

---

## 2. Review Checklist

### Production (`games_theory/**`)
- ✅ Verify CLI contracts (`games-theory`, `games-theory-init`) remain backward compatible.
- ✅ Ensure resource handling (`config.json`, `state.json`, `qtable.json`) remains durable (no data loss, safe overwrite semantics).
- ✅ Confirm tests exist/updated when modifying predictors, generators, or resource utilities.
- ✅ Check packaging metadata (`pyproject.toml`, version bump, changelog) when building releases.

### Experimental Areas
- ✅ Prioritize correctness of algorithms / experiments.
- ✅ Accept lightweight structure; avoid large-scale refactors purely for style.
- ✅ Document non-obvious behaviours in-line (short comments or README updates).

---

## 3. Review Style
- Focus on real bugs, behavioural regressions, and missing tests.
- Keep findings actionable: explain risk/impact and point to specific files/lines.
- Avoid cosmetic nitpicks unless they hide a functional issue.

---

When onboarding agents to other projects, reuse the templates in `docs/templates/` to keep README and AGENT briefings consistent.
