# Project lifecycle

Use this workflow for non-trivial changes, including changes that require
architectural or product decisions before implementation.

## 1. Project proposal

Create one Markdown file under `docs/projects`. The proposal must describe:

- the problem and intended outcome;
- confirmed decisions and assumptions;
- affected components and boundaries;
- the proposed runtime or data flow;
- failure handling and user-visible behavior;
- implementation stages;
- tests and acceptance criteria;
- open questions that require a decision.

The proposal has status `PROPOSED`. No production implementation starts during
this stage.

## 2. Proposal review

The repository owner reviews the project file. Discussion and corrections are
applied to the proposal itself so the accepted design is explicit.

Implementation starts only after the repository owner accepts the proposal.
Change its status to `APPROVED FOR IMPLEMENTATION` when approval is given.

## 3. Implementation

Implement only the accepted scope. Keep the project file during development and
record material deviations or newly discovered risks in it. Do not update the
permanent domain and guideline documentation yet.

Run verification proportionate to the change and prepare a concise review
summary containing:

- changed files and behavior;
- design deviations, if any;
- automated test results;
- manual verification still required;
- known limitations and follow-up work.

Set the project status to `IMPLEMENTED`.

## 4. Implementation review

The repository owner reviews the implementation and its verification results.
Requested changes return to the implementation stage.

Do not finalize documentation or delete the project file until the repository
owner explicitly accepts the implementation.

Set the project status to `APPROVED FOR DOCUMENTATION`.

## 5. Documentation and cleanup

After implementation acceptance:

1. update the relevant permanent documents under `docs/domain`,
   `docs/guidelines` and `docs/architecture`;
2. update `README.md` only if user-facing product or quick-start information
   changed;
3. update `AGENTS.md` if repository routing changed;
4. remove the completed project file from `docs/projects`;
5. run link, formatting, and relevant build checks;
6. present the final diff for commit or publication approval.

The Git history preserves the reviewed plan while the working tree retains only
current documentation.

## Rules

- A proposal is not authorization to implement.
- Implementation acceptance is not implicit in a passing build.
- Permanent documentation describes implemented behavior, not planned behavior.
- One project file should cover one cohesive change.
- Unrelated improvements discovered during implementation become separate
  projects or follow-up tasks.

## Project Template

```markdown
# <Change Name>

## Status
- Phase: PROPOSED | APPROVED FOR IMPLEMENTATION | IMPLEMENTED | APPROVED FOR DOCUMENTATION | DONE

## Scope
- <What changes>
- <What stays out of scope>

## Implementation Plan
1. [pending] <Step>
2. [pending] <Step>

Mark steps as `[pending]`, `[in-progress]`, or `[done]` as work progresses so interrupted or extended work remains easy to resume.

## Verification
- `<command>`

## Result
- <Temporary summary used during active work only. Delete this file after user acceptance, cleanup, and durable documentation/TODOs are updated.>
```
