# Project Planning

This directory stores temporary execution plans for active repository changes. Every non-trivial change should have a short plan before implementation. After writing or updating the plan, wait for user confirmation or feedback before starting implementation.

Completed plans are deleted only after the user has had a chance to read the plan, implementation is complete, tests pass, the user accepts the implementation/test result, and durable documentation or TODOs are updated.

Durable knowledge must not live only in a project plan. When a project finishes, move lasting information into feature documentation, architecture docs, guidelines, or TODO sections in the relevant durable docs before deleting the plan.

## Workflow

1. **Planning**: define scope, affected files, expected behaviour, and verification commands.
2. **Review Gate**: share the plan with the user and wait for confirmation or requested changes.
3. **Implementation**: make the smallest coherent changes that satisfy the confirmed plan.
4. **Tests**: run repeatable checks, preferably through scripts in `scripts/**`.
5. **Acceptance Gate**: share the implementation and test results with the user, then wait for acceptance or requested changes.
6. **Closeout**: move durable outcomes and TODOs to the relevant documentation, remove temporary files, then delete the project plan file.

## Plan Template

```markdown
# <Change Name>

## Status
- Phase: Planning | Awaiting Review | Implementation | Tests | Awaiting Acceptance | Done

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
