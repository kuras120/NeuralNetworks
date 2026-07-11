# Release Workflow

This guide describes the manual GitHub release workflow for the `games-theory` package.

## Version Selection

Releases are started manually from the GitHub Actions `release` workflow.

The workflow exposes one optional input:

- `version`: exact release version in `X.Y.Z` format.

When `version` is empty, the workflow finds the latest semver tag without a `v` prefix and selects the next patch version:

- latest tag `0.2.4` becomes `0.2.5`
- latest tag `1.9.0` becomes `1.9.1`

If no semver tag exists, the workflow reads `pyproject.toml` and applies the same next-patch rule. The workflow rejects non-semver versions and stops if the selected tag already exists.

GitHub's manual workflow form supports only static input defaults, so the next patch version cannot be prefilled from repository tags before the run starts. Leave `version` empty for the calculated patch release, or type a higher `X.Y.Z` version when preparing a minor or major release.

## Artifact Version

`pyproject.toml` stores the latest released package version. Release tags and built artifacts remain the source of truth for what was actually published.

During the build job, GitHub Actions writes the selected version into `pyproject.toml` in the checked-out runner workspace before building the wheel and source distribution. After the GitHub release is created, the workflow opens a pull request that persists the same version in `pyproject.toml` on `master`.

Release helper scripts live under `scripts/`:

- `scripts/prepare_release.py`: selects and validates the release version.
- `scripts/set_package_version.py`: updates build metadata in the runner workspace.
- `scripts/generate_release_notes.py`: generates the Markdown release body from git commits.
- `scripts/create_version_update_pr.py`: creates the post-release pull request that persists `pyproject.toml`.

## Release Notes Format

The release title is:

```text
GamesTheory <version>
```

Visual draft: `docs/guidelines/release-notes-draft.svg`

The release body starts with the artifact header, then the changes section:

```markdown
# GamesTheory <version>

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

## Verification

Local verification can confirm the package still builds and the repository tests pass:

```bash
scripts/verify.sh
python scripts/test_release_tools.py
python -m build
```

The release itself must still be verified in GitHub Actions because GitHub supplies the manual input, repository tags, artifacts, and release permissions.
