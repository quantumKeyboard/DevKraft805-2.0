"""
analysis/churn_analyzer.py
Computes churn score per file from commit history.
Churn = total lines added + deleted across all commits (normalized 0-100).
"""

import logging
from datetime import datetime, timezone

logger = logging.getLogger(__name__)


def compute_churn_scores(
    commit_map: dict,  # {file_path → [CommitRecord]}
) -> dict[str, float]:
    """
    Compute normalized churn score (0–100) for each file.

    Strategy:
    - For each file: approximate churn as total commit count as a proxy
      (line-level diff data requires an extra API call per commit; avoided for rate-limit reasons).
    - Normalizes across all files via min-max scaling.

    Returns:
        {file_path → churn_score (0–100)}
    """
    raw_churn: dict[str, float] = {}

    for file_path, commits in commit_map.items():
        if not commits:
            raw_churn[file_path] = 0.0
            continue

        # Use commit count as churn proxy (simple and fast within API constraints)
        raw_churn[file_path] = float(len(commits))

    if not raw_churn:
        return {}

    min_c = min(raw_churn.values())
    max_c = max(raw_churn.values())

    if max_c == min_c:
        # All files have the same churn — assign 50 to everyone
        return {path: 50.0 for path in raw_churn}

    return {
        path: round((v - min_c) / (max_c - min_c) * 100, 2)
        for path, v in raw_churn.items()
    }


def compute_churn_velocity(
    commit_map: dict,  # {file_path → [CommitRecord]}
    lookback_days: int = 90,
    window_days: int = 30,
) -> dict[str, float]:
    """
    Compute commit velocity ratio for each file:
        velocity = commits in last `window_days` / commits in previous `window_days`
    
    Used by hot_zone_predictor for accelerating files.
    Returns: {file_path → velocity_ratio}
    """
    now = datetime.now(timezone.utc)
    velocities: dict[str, float] = {}

    for file_path, commits in commit_map.items():
        recent = 0
        prior = 0
        for commit in commits:
            if not commit.timestamp:
                continue
            try:
                ts = datetime.fromisoformat(commit.timestamp.replace("Z", "+00:00"))
                age_days = (now - ts).days
                if age_days <= window_days:
                    recent += 1
                elif age_days <= window_days * 2:
                    prior += 1
            except ValueError:
                continue

        if prior == 0:
            velocity = float(recent) if recent > 0 else 0.0
        else:
            velocity = recent / prior

        velocities[file_path] = round(velocity, 4)

    return velocities
