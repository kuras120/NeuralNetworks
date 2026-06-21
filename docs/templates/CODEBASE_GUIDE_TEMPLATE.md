# Codebase Guide (README) Template

Use this template when asking an agent to produce or refresh a repository README so every project ships the same structure.

```
# Codebase Guide: <Project Name>

Short paragraph that explains the mission of the repository and highlights which directories are production-ready vs. experimental. Mention that the detailed review policy lives in AGENTS.md.

---

## 1. Quick Links
- Review policy (`AGENTS.md`)
- Architecture docs / diagrams
- Release notes or changelog paths

## 2. Repository Magistrate / Map
| Path | Category | Notes |
| --- | --- | --- |
| `<dir>` | Production / Experiment / Tooling | Summary of what lives there |

## 3. Environment & Setup
- Supported runtime (Python version, Node version, etc.)
- Commands for installing dependencies, enabling virtualenvs, running quick smoke tests.

## 4. Production Modules
For each production-critical area include:
- Responsibilities / what problems it solves.
- Interfaces & workflows (CLI commands, APIs, scripts).
- Configuration + resource files.
- Runtime & data flow summary (link to diagrams).
- Testing surfaces.
- Release / deployment workflow.
- Outstanding work or TODOs that affect reliability.

## 5. Experiment Sandboxes
Describe each experimental area, how to run it, and expectations (e.g., focus on correctness over polish).

## 6. Tooling & Scripts
List helper scripts, shared requirements files, automation entry points, etc.

## 7. Review & Quality Reference
Summarize how this README ties back to AGENTS.md and remind contributors which directories require production rigor.

Closing sentence encouraging future updates when architecture changes.
```

When requesting updates, supply any project-specific details (runtime versions, main modules, release steps) so the agent can fill each section accurately.
