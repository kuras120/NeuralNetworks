#!/usr/bin/env python3
"""Generate Markdown release notes from merged pull requests."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any


FEATURE_PATTERN = re.compile(r"^(feat|feature)(\([^)]+\))?:", re.IGNORECASE)
BUGFIX_PATTERN = re.compile(r"^(fix|bugfix)(\([^)]+\))?:", re.IGNORECASE)


@dataclass(frozen=True)
class PullRequest:
    number: int
    title: str
    url: str
    author: str
    merged_at: str
    merge_commit: str = ""


def run(command: list[str]) -> str:
    result = subprocess.run(command, check=True, text=True, capture_output=True)
    return result.stdout.strip()


def release_range(previous_tag: str) -> tuple[str, str]:
    head_sha = run(["git", "rev-parse", "HEAD"])
    if not previous_tag:
        return "", head_sha
    previous_sha = run(["git", "rev-list", "-n", "1", previous_tag])
    return previous_sha, head_sha


def load_pull_requests_from_fixture(path: str) -> list[PullRequest]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return parse_pull_requests(data)


def load_pull_requests_from_github(previous_tag: str) -> list[PullRequest]:
    base_sha, head_sha = release_range(previous_tag)
    repository = os.environ["GITHUB_REPOSITORY"]
    payload = run(
        [
            "gh",
            "api",
            "--method",
            "GET",
            "--paginate",
            f"repos/{repository}/pulls",
            "-f",
            "state=closed",
            "-f",
            "sort=updated",
            "-f",
            "direction=desc",
            "-f",
            "per_page=100",
            "--slurp",
        ]
    )
    prs = parse_pull_requests(load_paginated_payload(payload))
    revision_range = f"{base_sha}..{head_sha}" if base_sha else head_sha
    commits = set(run(["git", "rev-list", revision_range]).splitlines())
    return [
        pr
        for pr in prs
        if pr.merged_at and pr.merge_commit and pr.merge_commit in commits
    ]


def load_paginated_payload(payload: str) -> list[dict[str, Any]]:
    pages = json.loads(payload)
    if not pages:
        return []
    if isinstance(pages[0], dict):
        return pages
    return [item for page in pages for item in page]


def pull_request_url(item: dict[str, Any]) -> str:
    return str(item.get("html_url") or item.get("url") or "")


def pull_request_author(item: dict[str, Any]) -> str:
    author = item.get("author") or item.get("user") or {}
    if isinstance(author, dict):
        return str(author.get("login") or item.get("authorLogin") or "unknown")
    return str(author or item.get("authorLogin") or "unknown")


def pull_request_merge_commit(item: dict[str, Any]) -> str:
    merge_commit = item.get("mergeCommit") or {}
    if isinstance(merge_commit, dict):
        return str(
            merge_commit.get("oid")
            or item.get("merge_commit_sha")
            or item.get("mergeCommitOid")
            or ""
        )
    return str(item.get("merge_commit_sha") or item.get("mergeCommitOid") or "")


def parse_pull_requests(data: list[dict[str, Any]]) -> list[PullRequest]:
    pull_requests: list[PullRequest] = []
    for item in data:
        pr = PullRequest(
            number=int(item["number"]),
            title=str(item["title"]).strip(),
            url=pull_request_url(item),
            author=pull_request_author(item),
            merged_at=str(item.get("mergedAt") or item.get("merged_at") or ""),
            merge_commit=pull_request_merge_commit(item),
        )
        pull_requests.append(pr)
    return sorted(pull_requests, key=lambda pr: pr.merged_at)


def render_prs(pull_requests: list[PullRequest]) -> str:
    if not pull_requests:
        return "- No changes in this category."
    return "\n".join(render_pr(pr) for pr in pull_requests)


def render_pr(pr: PullRequest) -> str:
    links = [f"[#{pr.number}]({pr.url})"]
    if pr.merge_commit:
        commit_url = pr.url.rsplit("/pull/", 1)[0] + f"/commit/{pr.merge_commit}"
        links.append(f"[{pr.merge_commit[:7]}]({commit_url})")
    return f"- {pr.title} ({', '.join(links)})"


def render_authors(pull_requests: list[PullRequest]) -> str:
    authors: dict[str, str] = {}
    for pr in pull_requests:
        authors.setdefault(pr.author, pr.author)

    if not authors:
        return "- No authors found for this release."
    return "\n".join(f"- @{author}" if author != "unknown" else "- unknown" for author in authors)


def grouped_pull_requests(pull_requests: list[PullRequest]) -> dict[str, list[PullRequest]]:
    groups = {"features": [], "bugfixes": [], "others": []}
    for pr in pull_requests:
        if FEATURE_PATTERN.match(pr.title):
            groups["features"].append(pr)
        elif BUGFIX_PATTERN.match(pr.title):
            groups["bugfixes"].append(pr)
        else:
            groups["others"].append(pr)
    return groups


def generate_notes(version: str, pull_requests: list[PullRequest]) -> str:
    groups = grouped_pull_requests(pull_requests)

    return "\n".join(
        [
            f"## What's Changed in {version}",
            "",
            "### 🚀 Features",
            render_prs(groups["features"]),
            "",
            "### 🐛 Bug fixes",
            render_prs(groups["bugfixes"]),
            "",
            "### 🧰 Others",
            render_prs(groups["others"]),
            "",
            "## Authors",
            render_authors(pull_requests),
            "",
        ]
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate release notes from merged pull requests."
    )
    parser.add_argument("--version", required=True, help="Release version.")
    parser.add_argument("--previous-tag", default="", help="Previous release tag.")
    parser.add_argument(
        "--output",
        default="release-notes.md",
        help="Output Markdown file.",
    )
    parser.add_argument(
        "--fixture",
        default="",
        help="Optional JSON fixture for deterministic tests.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.fixture:
        pull_requests = load_pull_requests_from_fixture(args.fixture)
    else:
        pull_requests = load_pull_requests_from_github(args.previous_tag)
    notes = generate_notes(args.version, pull_requests)
    Path(args.output).write_text(notes, encoding="utf-8")
    print(f"Release notes written to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
