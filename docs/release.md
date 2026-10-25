# Releases

Run the manual [release workflow](../.github/workflows/release.yml) on the intended branch using GitHub's branch selector.

| Stage | Behaviour |
| --- | --- |
| Version | Empty `version` releases the base of `X.Y.Z.dev0`; clean-version branches fall back to the next patch. Optional `X.Y.Z` overrides must exceed reachable release tags and not precede the declared base; existing tags and invalid versions are rejected. |
| Prepare | Create a release commit and a following next-patch `.dev0` commit on an update branch. |
| Build and publish | Build wheel/sdist and tag the release commit; publish a GitHub release with artifacts. |
| Follow-up | Open a PR back to the selected branch, leaving it on the next development version after merge. |

Release tags/titles use bare semver (`1.2.3`). Notes list merged PRs since the previous reachable semver tag, grouped by title, with PR/merge-commit links and unique authors. For an explicit version, the previous tag must also be lower than that version; maintenance branches use their own reachable history. Each PR is listed once, without expanding its commits. Empty categories say `No changes in this category.`

| PR title prefix | Notes category |
| --- | --- |
| `feat:` / `feat(scope):` | Features |
| `fix:` / `fix(scope):` | Bug fixes |
| Other types | Others |

The body starts with `What's Changed in X.Y.Z`, followed by the three categories and Authors; the title carries the version.

Legacy `feature` and `bugfix` aliases are supported. Use English PR titles and commit subjects in `<type>(optional-scope): summary` form, such as `fix(cli): preserve JSON output`. Release commits use `chore(release): ...`.

[Visual reference](design/release-notes-draft.svg) · [Tool research](research/release-automation-tools.md) · [Release helpers and tests](../scripts/workflow/)

Run `mise run verify` locally; the release itself is checked in GitHub Actions.

Each release also publishes `games-theory-X.Y.Z-requirements.lock`: exact transitive runtime pins and SHA-256 hashes derived from the release wheel. Install dependencies with `pip install --require-hashes -r games-theory-X.Y.Z-requirements.lock`, then install the matching wheel with `pip install --no-deps WHEEL`. Consumers package the installed environment for offline use.

Release tooling pins a compatible `pip`/`pip-tools` pair in `scripts/requirements.txt`. The lock excludes test/build dependencies. Version mismatches, missing hashes, unsupported environment markers, unavailable universal wheels and failed installation or smoke checks stop publication. Lock generation uses Python 3.14 and requires universal dependency wheels, a clean hash-checked install, `pip check` and CLI smoke checks before publication. Helpers: `scripts/workflow/generate_dependency_lock.py` and `scripts/workflow/build_dependency_lock.sh`.
