# Dev Version Release Flow

## Status
- Phase: Awaiting Acceptance

## Scope
- Change the release workflow so release tags point at a source tree whose `pyproject.toml` contains the clean released version.
- Keep the selected GitHub `Run workflow from` branch as the target branch for maintenance releases.
- Move the repository version model to PEP 440 development versions, for example `1.4.1.dev0`.
- Keep a single pull request per release back into the selected target branch.
- Address shell-safety for manual `version` input by passing it through an environment variable.
- Keep release notes based on merged pull requests between the selected previous tag and the release commit.

## Out Of Scope
- Auto-merging release pull requests.
- Replacing the release workflow with a third-party release framework.
- Supporting Maven-style `-SNAPSHOT`; Python packaging should use PEP 440 `.dev0`.
- Changing tag naming or adding a `v` prefix.

## Proposed Behaviour
- A target branch stores the next development version, for example `1.4.1.dev0`.
- Empty manual `version` input releases the current development base, so `1.4.1.dev0` releases `1.4.1`.
- Explicit manual `version` input releases exactly that clean `X.Y.Z` version.
- After every release, the next development version increments the released patch by one, so an explicit `1.5.0` release produces `1.5.1.dev0`.
- The workflow creates one temporary release branch, for example `release-1.4.1`.
- The release branch gets two commits:
  1. `pyproject.toml = 1.4.1`.
  2. `pyproject.toml = 1.4.2.dev0`.
- Build and GitHub release tag use the SHA from commit 1, so source archives and wheel/sdist metadata agree.
- The pull request uses the same release branch and targets the branch selected in GitHub's built-in workflow branch selector. After merge, the target branch lands on `1.4.2.dev0`.
- If the PR is squash-merged, the target branch may not contain the exact tagged release commit, but the release tag still preserves the exact source tree used for the published artifact.

## Implementation Plan
1. [done] Update version parsing helpers to support both clean semver (`X.Y.Z`) and development versions (`X.Y.Z.dev0`).
2. [done] Update `scripts/workflow/prepare_release.py` so:
   - empty `version` releases the clean base of `pyproject.toml` when it is a dev version,
   - empty `version` falls back to next patch from the latest reachable tag when needed,
   - explicit `version` remains clean `X.Y.Z`,
   - it outputs `VERSION`, `NEXT_DEV_VERSION`, and branch-local `PREVIOUS_TAG`.
3. [done] Replace or refactor the post-release version PR script so it creates a release branch with:
   - commit 1: clean release version,
   - commit 2: next `.dev0` version,
   - outputs for release branch name and release commit SHA.
4. [done] Update `.github/workflows/release.yml` so:
   - manual `version` input is passed via `REQUESTED_VERSION` env,
   - build checks out the release commit SHA instead of modifying version locally,
   - publish checks out the same release commit SHA,
   - `softprops/action-gh-release` tags the release commit SHA,
   - the final PR targets `github.ref_name`.
5. [done] Update deterministic release tooling tests for:
   - dev version parsing,
   - default release from `X.Y.Z.dev0`,
   - next dev version calculation,
   - release branch with two commits,
   - tag SHA wiring in workflow,
   - shell-safe manual input wiring.
6. [done] Update durable docs in `docs/guidelines/release-workflow.md` and any repository guide references that describe version persistence.
7. [done] Restore explicit-version validation against the latest branch-local reachable semver tag.
8. [done] Move Python release workflow helpers under `scripts/workflow/` to separate them from local shell scripts.

## Verification
- `python3 -m py_compile scripts/workflow/prepare_release.py scripts/workflow/set_package_version.py scripts/workflow/prepare_release_branch.py scripts/workflow/generate_release_notes.py scripts/workflow/create_version_update_pr.py scripts/workflow/test_release_tools.py`
- `python3 scripts/workflow/test_release_tools.py`
- `ruby -e 'require "yaml"; YAML.load_file(".github/workflows/release.yml")'`
- `scripts/verify.sh`
- `git diff --check`
- `.venv/bin/python -m build` if isolated build dependencies are available.

## Risks And Decisions
- The release branch contains both release and next-dev commits. The tag points at the first commit, while the PR final state is the second commit.
- A failed workflow after pushing the release branch but before tagging can be rerun by force-updating the release branch.
- A failed workflow after tagging but before opening or merging the PR leaves a valid release tag and may require a manual or rerun-created next-dev PR.
- `pyproject.toml` should transition to a `.dev0` version as part of this PR so the new default release calculation has a clear source of truth.

## Result
- Implementation complete; pending user acceptance before closeout and plan removal.
