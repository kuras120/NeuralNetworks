# Project Planning

This directory stores temporary execution plans for active repository changes. Every non-trivial change should have a short plan before implementation, but completed plans are deleted after implementation and tests.

Durable knowledge must not live only in a project plan. When a project finishes, move lasting information into feature documentation, architecture docs, guidelines, or TODO sections in the relevant durable docs before deleting the plan.

## Workflow

1. **Planning**: define scope, affected files, expected behaviour, and verification commands.
2. **Implementation**: make the smallest coherent changes that satisfy the plan.
3. **Tests**: run repeatable checks, preferably through scripts in `scripts/**`.
4. **Closeout**: move durable outcomes and TODOs to the relevant documentation, then delete the project plan file.

## Plan Template

```markdown
# <Change Name>

## Status
- Phase: Planning | Implementation | Tests | Done

## Scope
- <What changes>
- <What stays out of scope>

## Implementation Plan
1. <Step>
2. <Step>

## Verification
- `<command>`

## Result
- <Temporary summary used during active work only. Delete this file after tests pass and durable documentation/TODOs are updated.>
```
