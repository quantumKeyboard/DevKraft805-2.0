"""
analysis/bug_commit_detector.py
Scans commit messages for bug-fix keywords and computes a bug commit ratio per file.
"""

from core.constants import BUG_COMMIT_KEYWORDS


def compute_bug_commit_ratios(
    commit_map: dict,  # {file_path → [CommitRecord]}
) -> dict[str, float]:
    """
    Compute the bug commit ratio (0.0–1.0) for each file.
    bug_commit_ratio = bug_commits / total_commits

    A commit is "bug-related" if its message (lowercased) contains
    any BUG_COMMIT_KEYWORDS.

    Returns: {file_path → bug_commit_ratio}
    """
    result: dict[str, float] = {}

    for file_path, commits in commit_map.items():
        if not commits:
            result[file_path] = 0.0
            continue

        total = len(commits)
        bug_count = 0

        for commit in commits:
            msg = (commit.message or "").lower()
            if any(kw in msg for kw in BUG_COMMIT_KEYWORDS):
                bug_count += 1

        result[file_path] = round(bug_count / total, 4)

    return result
