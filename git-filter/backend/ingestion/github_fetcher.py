"""
ingestion/github_fetcher.py
Fetches the full file tree and raw file content from a public GitHub repository
using the GitHub Contents API (no authentication required for public repos).
"""

import base64
import logging
import time
from typing import Optional
import httpx

from core.constants import SUPPORTED_EXTENSIONS, EXTENSION_TO_LANGUAGE, GITHUB_API_BASE
from core.config import get_settings

logger = logging.getLogger(__name__)


class FileData:
    """Represents a single source file fetched from GitHub."""

    __slots__ = ("path", "content", "language", "size")

    def __init__(self, path: str, content: str, language: str, size: int):
        self.path = path
        self.content = content
        self.language = language
        self.size = size

    def to_dict(self) -> dict:
        return {
            "path": self.path,
            "content": self.content,
            "language": self.language,
            "size": self.size,
        }


def _make_headers(token: str = "") -> dict:
    headers = {"Accept": "application/vnd.github.v3+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def _get_client(token: str = "") -> httpx.Client:
    return httpx.Client(
        headers=_make_headers(token),
        timeout=30.0,
        follow_redirects=True,
    )


def fetch_file_tree(
    owner: str,
    repo: str,
    branch: str,
    token: str = "",
) -> list[dict]:
    """
    Fetch the complete file tree via the Git Trees API (recursive=1).

    Returns a list of tree items for supported source files only.
    Each item: {"path": str, "size": int}
    """
    url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/git/trees/{branch}?recursive=1"

    with _get_client(token) as client:
        response = client.get(url)
        response.raise_for_status()
        data = response.json()

    if data.get("truncated"):
        logger.warning(
            "GitHub file tree was truncated! Large repository. Some files may be missing."
        )

    tree = data.get("tree", [])
    supported = [
        item for item in tree
        if item.get("type") == "blob"
        and any(item["path"].endswith(ext) for ext in SUPPORTED_EXTENSIONS)
    ]

    logger.info(
        f"Found {len(supported)} supported source files out of {len(tree)} total tree items."
    )
    return supported


def fetch_file_content(
    owner: str,
    repo: str,
    path: str,
    token: str = "",
) -> Optional[str]:
    """
    Fetch the raw content of a single file from GitHub.
    Returns the decoded string content, or None if the file cannot be fetched.
    """
    url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/contents/{path}"

    with _get_client(token) as client:
        response = client.get(url)

    if response.status_code == 404:
        logger.warning(f"File not found on GitHub: {path}")
        return None
    if response.status_code != 200:
        logger.warning(f"Failed to fetch {path}: HTTP {response.status_code}")
        return None

    data = response.json()
    encoding = data.get("encoding", "")

    if encoding == "base64":
        try:
            content = base64.b64decode(data["content"]).decode("utf-8", errors="replace")
            return content
        except Exception as exc:
            logger.warning(f"Failed to decode content for {path}: {exc}")
            return None

    # For very large files, GitHub may return a download_url instead
    download_url = data.get("download_url")
    if download_url:
        with _get_client(token) as client:
            dl_response = client.get(download_url)
        if dl_response.status_code == 200:
            return dl_response.text

    return None


def fetch_repository_files(
    owner: str,
    repo: str,
    branch: str,
    token: str = "",
    max_file_size_bytes: int = 500_000,  # skip files > 500 KB
) -> list[FileData]:
    """
    Full pipeline: fetch file tree → for each supported file, fetch raw content.

    Returns a list of FileData objects.
    """
    settings = get_settings()
    if not token:
        token = settings.github_api_token

    tree_items = fetch_file_tree(owner, repo, branch, token=token)

    files: list[FileData] = []
    for i, item in enumerate(tree_items):
        path = item["path"]
        size = item.get("size", 0)
        ext = "." + path.rsplit(".", 1)[-1] if "." in path else ""
        language = EXTENSION_TO_LANGUAGE.get(ext, "unknown")

        if size > max_file_size_bytes:
            logger.info(f"Skipping large file ({size} bytes): {path}")
            continue

        content = fetch_file_content(owner, repo, path, token=token)
        if content is None:
            continue

        files.append(FileData(path=path, content=content, language=language, size=size))

        # Minimal rate-limit courtesy sleep every 10 files for unauthenticated requests
        if not token and (i + 1) % 10 == 0:
            time.sleep(0.5)

    logger.info(f"Successfully fetched content for {len(files)} files.")
    return files
