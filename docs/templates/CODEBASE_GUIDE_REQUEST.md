# Request Template: Codebase Guide + Agent Briefing

Copy/paste (and edit placeholders) when asking an AI agent to align README + AGENTS across a new project.

```
I need a standardized Codebase Guide (README) and AGENTS.md for <project>.

Requirements:
- Follow the shared structure in docs/templates/CODEBASE_GUIDE_TEMPLATE.md (sections: Quick Links, Repo Map, Environment, Production Modules, Experiments, Tooling, Review Reference).
- AGENTS.md must follow docs/templates/AGENT_POLICY_TEMPLATE.md (link back to README, include scope table, production vs experimental checklists, review style).
- Emphasize that <list production directories> are production-ready and <list experimental directories> are exploratory.
- Mention any special workflows (e.g., CLI names, release steps) in the README’s Production Modules section.
- Provide TODOs / outstanding work items relevant to this repo.
- Update or create any missing template files if helpful.

Context you can include:
- Runtime versions (Python/Node/etc.).
- Key modules/packages.
- Testing or release commands.

Deliverables:
1. Updated README.md (Codebase Guide).
2. Updated AGENTS.md referencing README sections.
3. (Optional) Template files or notes for reuse in other repositories.
```

Adjust the placeholders (project name, directories, workflows) before sending the prompt to keep generated docs accurate.
