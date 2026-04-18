"""
ingestion/repo_validator.py
Validates GitHub URL format and checks that the repository is publicly accessible.
"""

import re
import httpx
from typing import TypedDict
from core.config import get_settings


class RepoInfo(TypedDict):
    owner: str
    repo: str
    api_base_url: str
    default_branch: str


GITHUB_URL_PATTERN = re.compile(
    r"^https?://github\.com/(?P<owner>[^/]+)/(?P<repo>[^/\s]+?)(?:\.git)?/?$"
)


class RepoValidationError(Exception):
    """Raised when a repository URL is invalid or inaccessible."""


def validate_github_url(url: str) -> RepoInfo:
    """
    Validate the GitHub URL and check that the repo is publicly accessible.

    Args:
        url: GitHub repository URL (e.g. https://github.com/owner/repo)

    Returns:
        RepoInfo dict with owner, repo, api_base_url, and default_branch

    Raises:
        RepoValidationError: if the URL is malformed or the repo is unreachable
    """
    url = url.strip()

    match = GITHUB_URL_PATTERN.match(url)
    if not match:
        raise RepoValidationError(
            f"Invalid GitHub URL format: '{url}'. "
            "Expected: https://github.com/owner/repo"
        )

    owner = match.group("owner")
    repo = match.group("repo")
    api_base_url = f"https://api.github.com/repos/{owner}/{repo}"

    # Check the repo is publicly accessible via the GitHub API
    token = get_settings().github_api_token
    headers = {"Accept": "application/vnd.github.v3+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    try:
        response = httpx.get(api_base_url, headers=headers, timeout=10.0, follow_redirects=True)
    except httpx.RequestError as exc:
        raise RepoValidationError(
            f"Could not reach GitHub API: {exc}"
        ) from exc

    if response.status_code == 404:
        raise RepoValidationError(
            f"Repository not found or is private: {owner}/{repo}"
        )
    if response.status_code == 403:
        raise RepoValidationError(
            "GitHub API rate limit exceeded. Add a GITHUB_API_TOKEN to .env to increase limits."
        )
    if response.status_code != 200:
        raise RepoValidationError(
            f"GitHub API returned status {response.status_code} for {owner}/{repo}"
        )

    repo_data = response.json()
    default_branch = repo_data.get("default_branch", "main")

    return RepoInfo(
        owner=owner,
        repo=repo,
        api_base_url=api_base_url,
        default_branch=default_branch,
    )
