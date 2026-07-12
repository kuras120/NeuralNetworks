# Release Workflow

This guide describes the manual GitHub release workflow for the `games-theory` package.

## Version Selection

Releases are started manually from the GitHub Actions `release` workflow.

The workflow is dispatched from GitHub's built-in branch selector. Choose the branch to release in the `Run workflow from` control, for example `release/1.x` for `1.x.x` and `master` for the current major line. The workflow checks out that branch in every job, creates the release tag against that branch, and opens the post-release version update pull request back into the same branch.

The workflow exposes one optional input:

- `version`: exact release version in `X.Y.Z` format.

Target branches store the next development version in `pyproject.toml` using PEP 440 `.dev0`, for example `1.4.2.dev0`.

When `version` is empty and `pyproject.toml` contains a development version, the workflow releases the clean base version:

- `0.2.5.dev0` becomes `0.2.5`
- `1.9.1.dev0` becomes `1.9.1`

When the repository still contains a clean `X.Y.Z` version, the workflow falls back to the next patch from the latest reachable semver tag or from `pyproject.toml`. The workflow rejects non-semver release inputs and stops if the selected tag already exists. Explicit versions must be greater than the latest semver tag reachable from the selected release branch and must not be lower than the clean base version declared in `pyproject.toml`, so maintenance releases are checked against their own branch history instead of unrelated newer major lines.

After every release, the post-release pull request sets `pyproject.toml` to the next patch development version. For example, releasing `1.5.0` creates a final branch state of `1.5.1.dev0`.

The previous tag used for release notes is selected from semver tags reachable from the checked-out release `HEAD`. For explicit releases, the previous tag must also be lower than the selected version, so a `1.x` maintenance release does not use a newer `2.x` tag as its notes base.

GitHub's manual workflow form supports only static input defaults, so the next patch version cannot be prefilled from repository tags before the run starts. Leave `version` empty for the calculated patch release, or type a higher `X.Y.Z` version when preparing a minor or major release.

## Artifact Version

`pyproject.toml` on long-lived branches stores the next development version. Release tags and built artifacts remain the source of truth for what was actually published.

The workflow prepares one release update branch with two commits:

1. The release commit sets `pyproject.toml` to the clean released version.
2. The next-development commit sets `pyproject.toml` to the next `X.Y.Z.dev0` version.

The build job and GitHub release tag use the release commit SHA, so source archives and wheel/sdist metadata agree. After the GitHub release is created, the workflow opens a pull request from the same branch back into the selected release branch. Merging that pull request leaves the selected branch on the next development version.

Release helper scripts live under `scripts/`:

- `scripts/workflow/prepare_release.py`: selects and validates the release version.
- `scripts/workflow/prepare_release_branch.py`: creates the release and next-development commits.
- `scripts/workflow/set_package_version.py`: updates package metadata in local verification and helper flows.
- `scripts/workflow/generate_release_notes.py`: generates the Markdown release body from git commits.
- `scripts/workflow/create_version_update_pr.py`: creates the post-release pull request for the next development version.
- `scripts/workflow/workflow_common.py`: keeps shared version parsing and `pyproject.toml` updates out of the workflow entry points.

## Release Notes Format

The release title is:

```text
<version>
```

Visual draft: `docs/guidelines/release-notes-draft.svg`

The release body starts directly with the changes section, avoiding duplication of the version already shown in the release title:

```markdown
## What's Changed in <version>

### 🚀 Features
- feat: add new opening strategy ([#40](https://github.com/...), [abc1234](https://github.com/...))

### 🐛 Bug fixes
- fix: restore state loading ([#42](https://github.com/...), [def5678](https://github.com/...))

### 🧰 Others
- docs: refresh repository guide ([fed9012](https://github.com/...))

## Authors
- [@octocat](https://github.com/octocat)
```

Every merged pull request since the previous semver release tag is listed once. Pull requests are grouped by the pull request title:

- `Features`: titles starting with `feat:`, `feat(...):`, `feature:`, or `feature(...):`.
- `Bug fixes`: titles starting with `fix:`, `fix(...):`, `bugfix:`, or `bugfix(...):`.
- `Others`: all remaining titles.

If a category has no pull requests, the workflow writes `No changes in this category.`

Each release-note item links to the pull request. When GitHub provides a `mergeCommit.oid`, the item also links to that single merge or squash commit. The workflow never expands a pull request into all of its individual commits.

The `Authors` section lists unique pull request authors from the same release range.

## Pull Request And Commit Standard

Pull request titles must use this format because the release workflow categorizes changes from the title of each merged pull request:

```text
<type>(<optional-scope>): <short summary>
```

Rules:

- Use a lowercase type followed by an optional lowercase scope in parentheses, a colon, one space, and a concise summary.
- Use `feat` for a user-visible capability and `fix` for a defect correction. These types determine the dedicated release-note categories.
- Use `docs`, `refactor`, `test`, `chore`, `ci`, `build`, or `perf` when they describe the change more accurately. These types are grouped under `Others` by the current release workflow.
- Use a stable scope such as `cli`, `predictor`, `resources`, `release`, or `docs` when it makes the affected area clearer; omit it when the change spans the repository.
- Write the summary in imperative, present-tense English without a trailing period.
- Make the title describe the complete pull request, not an individual commit.
- Keep each pull request focused on one release-note category. Split unrelated feature and bug-fix work into separate pull requests.

Examples:

```text
feat(cli): emit selected move as JSON coordinates
fix(predictor): preserve pending move after evaluation failure
docs(release): document pull request title standard
ci: verify release tooling
```

Release-note mapping is implemented by `scripts/workflow/generate_release_notes.py`:

| PR title prefix | Release-note category |
| --- | --- |
| `feat:`, `feat(scope):`, `feature:`, `feature(scope):` | Features |
| `fix:`, `fix(scope):`, `bugfix:`, `bugfix(scope):` | Bug fixes |
| Any other title | Others |

Prefer the canonical `feat` and `fix` forms for new pull requests. The longer `feature` and `bugfix` aliases remain supported for compatibility with existing titles.

Commit subjects must follow the same `<type>(<optional-scope>): <short summary>` format so repository history and pull request titles remain consistent. Use `feat` for a capability, `fix` for a defect correction, and `chore` for maintenance work that is neither a capability nor a defect correction. Choose the type from the actual purpose of the commit; for example, a correction to release presentation uses `fix(release): ...`. Keep generated release/version commits in the existing `chore(release): ...` form.

## Verification

Local verification can confirm the package still builds and the repository tests pass:

```bash
scripts/verify.sh
python scripts/workflow/test_release_tools.py
python -m build
```

The release itself must still be verified in GitHub Actions because GitHub supplies the manual input, repository tags, artifacts, and release permissions.
