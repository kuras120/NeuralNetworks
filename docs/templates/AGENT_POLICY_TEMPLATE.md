# Agent Briefing (AGENTS.md) Template

Use this structure to align all repositories on the same review policy format.

```
# Agent Briefing

State that this file complements the Codebase Guide (README) and link to it (e.g., "See README §2–§7 for architecture details").

---

## 1. Review Scope & Priorities
| Area | Directories | Expectations |
| --- | --- | --- |
| Production | `<production paths>` | List priorities (API stability, packaging, tests, etc.). |
| Experimental | `<experimental paths>` | Emphasize correctness & speed, less process overhead. |

Add clarifying notes (e.g., when to escalate to product owners, how to treat shared data directories).

---

## 2. Review Checklist
Split into sections (Production vs. Experimental). Use checklist bullets that reviewers can copy/paste (✅ style).

Examples:
- ✅ Keep CLI contracts stable.
- ✅ Update changelog when versioning changes.
- ✅ Focus on correctness, skip cosmetic nitpicks.

---

## 3. Review Style
Capture global expectations: actionable findings, cite impact, avoid cosmetic-only feedback.

---

Close with guidance on where to find reusable templates (e.g., docs/templates) or whom to contact for policy updates.
```

When setting up a new project, edit the directories and bullet points to reflect that repo’s structure, but keep the headings identical for consistency.
