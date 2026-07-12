# Release Automation Tools Research

This note compares ready-made release automation tools that could replace or reduce custom release scripts.

## Current Repository Requirements

- Manual GitHub Actions release trigger.
- Optional explicit `X.Y.Z` version, with empty input defaulting to the next patch.
- `pyproject.toml` should be updated to the released version through a pull request.
- GitHub release body should include:
  - a `What's Changed in <version>` heading without repeating the release title,
  - grouped pull request list based on PR title prefixes,
  - Markdown links to each pull request,
  - authors for pull requests in the release range.
- Existing tag format is bare semver, for example `0.0.2`, without a `v` prefix.
- GitHub release titles use the same bare semver as the tag.

## Options

### GitHub Automatically Generated Release Notes

GitHub can generate release notes when creating a release, and supports a repository-level configuration file for categories and exclusions.

Fit:
- Good for standard GitHub releases.
- Low maintenance.
- Native GitHub feature, no extra runtime dependency.

Gaps:
- Does not update `pyproject.toml`.
- Less control over the exact body layout and PR-title prefix grouping.
- Manual version defaulting still needs workflow logic.

Source: [GitHub Docs - Automatically generated release notes](https://docs.github.com/en/repositories/releasing-projects-on-github/automatically-generated-release-notes)

### Release Drafter

Release Drafter keeps a draft release updated as pull requests are merged. It supports templates, categories, contributors, and next-version template variables such as next patch/minor/major.

Fit:
- Strong release-note templating.
- Supports contributors.
- Supports next patch version variables.
- Good if the workflow becomes PR-oriented and label-oriented.

Gaps:
- Works primarily from merged pull requests and labels, which is closer now that release notes are PR-based.
- Does not update `pyproject.toml` by itself.
- It drafts releases continuously, while this repository currently releases from a manual workflow run.

Source: [release-drafter/release-drafter](https://github.com/release-drafter/release-drafter)

### Release Please

Release Please parses Conventional Commits, maintains release pull requests, updates changelogs/version files, creates GitHub releases, and supports Python release types.

Fit:
- Handles version bumps through release PRs.
- Handles changelog/release note generation.
- Supports Python projects and `pyproject.toml`.
- Mature GitHub Action.

Gaps:
- Assumes Conventional Commits semantics: `feat` usually means minor and `fix` usually means patch.
- Current desired policy is always next patch by default unless manually overridden.
- It changes the workflow model to release PRs that are kept up to date, not a simple manual "run release now" with optional version input.
- Custom section rules such as `bugfix:` may require configuration or may not match cleanly.

Source: [googleapis/release-please-action](https://github.com/googleapis/release-please-action)

### Python Semantic Release

Python Semantic Release is Python-focused. It can determine the next version, stamp `pyproject.toml`, build artifacts, generate changelogs, tag, push, and create GitHub releases. It supports `version_toml = ["pyproject.toml:project.version"]`.

Fit:
- Best Python-native option.
- Explicitly supports stamping `project.version` in `pyproject.toml`.
- Provides GitHub Actions integration.
- Provides no-op/local test modes for release configuration.

Gaps:
- Designed around semantic version calculation from commit parser rules.
- Current desired policy is mostly manual/patch-driven, not fully semantic.
- Adopting it would add a larger tool and configuration surface than the current small scripts.
- Exact release-note layout and custom `bugfix:` section may require template customization.

Source: [Python Semantic Release - Getting Started](https://python-semantic-release.readthedocs.io/en/latest/concepts/getting_started.html) and [GitHub Actions](https://python-semantic-release.readthedocs.io/en/latest/configuration/automatic-releases/github-actions.html)

### semantic-release

semantic-release is a mature release automation framework that determines next versions, generates release notes, publishes packages, and supports plugins.

Fit:
- Mature ecosystem.
- Strong conventional-commit release-note generation.
- Can be extended with plugins.

Gaps:
- JavaScript/Node-centric by default.
- Python packaging and `pyproject.toml` updates need extra plugin/configuration work.
- Fully automated semantic versioning does not match the current manual release input requirement.

Source: [semantic-release documentation](https://semantic-release.gitbook.io/semantic-release/)

## Recommendation

Keep the current lightweight scripts for now.

Reasoning:
- The repository wants manual release control with optional explicit version input.
- The default version policy is next patch, independent of Conventional Commit semantic bump rules.
- The release note sections are custom and based on exact pull request title prefixes.
- `pyproject.toml` persistence can be handled by a small post-release PR script without adopting a larger release framework.

After switching release notes from raw commits to merged pull requests, Release Drafter becomes a closer fit for the release-notes part because it is PR-oriented, supports templates, contributors, and next patch version variables. It still does not persist `pyproject.toml`, and it relies heavily on labels/categories rather than exact title prefixes.

Recommendation remains to keep the lightweight scripts for now. If the repository later accepts label-based PR categorization, Release Drafter is worth revisiting. If the repository later moves to Conventional Commits as the source of truth for version semantics, revisit Python Semantic Release first because it can stamp `pyproject.toml`, build, tag, publish, and create GitHub releases.
