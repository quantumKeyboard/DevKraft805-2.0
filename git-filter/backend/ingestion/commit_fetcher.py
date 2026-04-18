"""
ingestion/commit_fetcher.py
Fetches per-file commit history from the GitHub Commits API.
Extracts: SHA, author name, email, timestamp, commit message.
"""

import logging
from datetime import datetime
from typing import Optional
import httpx

from core.constants import GITHUB_API_BASE, GITHUB_MAX_COMMITS_PER_FILE
from core.config import get_settings

logger = logging.getLogger(__name__)


class CommitRecord:
    """A single commit record for a file."""

    __slots__ = ("sha", "author_name", "author_email", "timestamp", "message")

    def __init__(
        self,
        sha: str,
        author_name: str,
        author_email: str,
        timestamp: str,
        message: str,
    ):
        self.sha = sha
        self.author_name = author_name
        self.author_email = author_email
        self.timestamp = timestamp  # ISO 8601 string
        self.message = message

    def to_dict(self) -> dict:
        return {
            "sha": self.sha,
            "author_name": self.author_name,
            "author_email": self.author_email,
            "timestamp": self.timestamp,
            "message": self.message,
        }


def _parse_commit(commit_data: dict) -> Optional[CommitRecord]:
    """Parse a single item from the GitHub commits API response."""
    try:
        sha = commit_data["sha"]
        commit = commit_data["commit"]
        author = commit.get("author") or {}
        message = commit.get("message", "")

        # GitHub API can return null committer/author
        git_author = commit_data.get("author") or {}
        author_name = (
            git_author.get("login")
            or author.get("name")
            or "Unknown"
        )
        author_email = author.get("email", "")
        timestamp = author.get("date", "")

        return CommitRecord(
            sha=sha,
            author_name=author_name,
            author_email=author_email,
            timestamp=timestamp,
            message=message,
        )
    except (KeyError, TypeError) as exc:
        logger.debug(f"Failed to parse commit: {exc}")
        return None


def fetch_commits_for_file(
    owner: str,
    repo: str,
    file_path: str,
    token: str = "",
    max_commits: int = GITHUB_MAX_COMMITS_PER_FILE,
) -> list[CommitRecord]:
    """
    Fetch commit history for a single file path.
    Returns up to max_commits CommitRecord objects.
    """
    headers = {"Accept": "application/vnd.github.v3+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    commits: list[CommitRecord] = []
    page = 1
    per_page = min(max_commits, 100)

    with httpx.Client(headers=headers, timeout=20.0, follow_redirects=True) as client:
        while len(commits) < max_commits:
            url = (
                f"{GITHUB_API_BASE}/repos/{owner}/{repo}/commits"
                f"?path={file_path}&per_page={per_page}&page={page}"
            )
            response = client.get(url)

            if response.status_code == 409:
                # Empty repository
                break
            if response.status_code != 200:
                logger.warning(
                    f"Failed to fetch commits for {file_path}: HTTP {response.status_code}"
                )
                break

            data = response.json()
            if not data:
                break

            for item in data:
                record = _parse_commit(item)
                if record:
                    commits.append(record)
                    if len(commits) >= max_commits:
                        break

            if len(data) < per_page:
                break  # No more pages

            page += 1

    return commits


def fetch_all_file_commits(
    owner: str,
    repo: str,
    file_paths: list[str],
    token: str = "",
    max_commits_per_file: int = GITHUB_MAX_COMMITS_PER_FILE,
) -> dict[str, list[CommitRecord]]:
    """
    Fetch commit history for all provided file paths.
    Returns: {file_path → [CommitRecord, ...]}
    
    Note: This makes one API call per file. For repos with many files,
    add a GitHub API token to .env to increase the rate limit.
    """
    settings = get_settings()
    if not token:
        token = settings.github_api_token

    result: dict[str, list[CommitRecord]] = {}

    for i, path in enumerate(file_paths):
        logger.debug(f"Fetching commits for file {i+1}/{len(file_paths)}: {path}")
        commits = fetch_commits_for_file(
            owner, repo, path, token=token, max_commits=max_commits_per_file
        )
        result[path] = commits

    logger.info(
        f"Fetched commit history for {len(result)} files. "
        f"Total commits: {sum(len(v) for v in result.values())}"
    )
    return result


def extract_timeline_data(
    commit_map: dict[str, list[CommitRecord]],
) -> list[dict]:
    """
    Group commits by month across all files to produce timeline data.
    Returns: [{month: "YYYY-MM", files_added: [...], hottest_files: [...], contributors: [...]}]
    """
    # Collect all commits across all files with their file path
    monthly: dict[str, dict] = {}

    for file_path, commits in commit_map.items():
        for commit in commits:
            if not commit.timestamp:
                continue
            try:
                dt = datetime.fromisoformat(commit.timestamp.replace("Z", "+00:00"))
                month_key = dt.strftime("%Y-%m")
            except ValueError:
                continue

            if month_key not in monthly:
                monthly[month_key] = {
                    "month": month_key,
                    "files_changed": set(),
                    "contributors": set(),
                    "file_commit_counts": {},
                }

            monthly[month_key]["files_changed"].add(file_path)
            monthly[month_key]["contributors"].add(commit.author_name)
            monthly[month_key]["file_commit_counts"][file_path] = (
                monthly[month_key]["file_commit_counts"].get(file_path, 0) + 1
            )

    # Convert sets to sorted lists and find hottest file per month
    timeline = []
    for month_key in sorted(monthly.keys()):
        entry = monthly[month_key]
        file_counts = entry["file_commit_counts"]
        hottest = sorted(file_counts, key=file_counts.get, reverse=True)[:5]  # type: ignore[arg-type]

        timeline.append({
            "month": month_key,
            "files_changed": list(entry["files_changed"]),
            "hottest_files": hottest,
            "contributors": list(entry["contributors"]),
            "total_commits": sum(file_counts.values()),
        })

    return timeline
