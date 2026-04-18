"""
analysis/hot_zone_predictor.py
Computes hot zone scores and flags files predicted to change soon.
hot_zone_score = (churn_score × 0.6) + (bug_commit_ratio × 100 × 0.4)
Files with score > HOT_ZONE_THRESHOLD are marked as predicted hot zones.
"""

from core.config import get_settings
from core.constants import (
    HOT_ZONE_CHURN_WEIGHT,
    HOT_ZONE_BUG_WEIGHT,
    HOT_ZONE_VELOCITY_ACCELERATION_RATIO,
)


class HotZoneResult:
    __slots__ = ("file_path", "hot_zone_score", "is_hot_zone", "velocity_ratio")

    def __init__(
        self,
        file_path: str,
        hot_zone_score: float,
        is_hot_zone: bool,
        velocity_ratio: float = 0.0,
    ):
        self.file_path = file_path
        self.hot_zone_score = hot_zone_score
        self.is_hot_zone = is_hot_zone
        self.velocity_ratio = velocity_ratio

    def to_dict(self) -> dict:
        return {
            "file_path": self.file_path,
            "hot_zone_score": self.hot_zone_score,
            "is_hot_zone": self.is_hot_zone,
            "velocity_ratio": self.velocity_ratio,
        }


def compute_hot_zones(
    churn_scores: dict[str, float],          # {file_path → 0–100}
    bug_commit_ratios: dict[str, float],      # {file_path → 0–1}
    velocity_ratios: dict[str, float] | None = None,  # {file_path → ratio}
) -> dict[str, HotZoneResult]:
    """
    Compute hot zone scores for all files.

    Formula (from spec):
        hot_zone_score = (churn_score × 0.6) + (bug_commit_ratio × 100 × 0.4)

    Velocity boost: if velocity_ratio > HOT_ZONE_VELOCITY_ACCELERATION_RATIO,
    add a 10-point bonus to the score (capped at 100).

    Returns: {file_path → HotZoneResult}
    """
    settings = get_settings()
    threshold = settings.hot_zone_threshold

    all_paths = set(churn_scores.keys()) | set(bug_commit_ratios.keys())
    results: dict[str, HotZoneResult] = {}

    for path in all_paths:
        churn = churn_scores.get(path, 0.0)
        bug_ratio = bug_commit_ratios.get(path, 0.0)
        velocity = (velocity_ratios or {}).get(path, 0.0)

        score = (churn * HOT_ZONE_CHURN_WEIGHT) + (bug_ratio * 100 * HOT_ZONE_BUG_WEIGHT)

        # Velocity acceleration bonus
        if velocity > HOT_ZONE_VELOCITY_ACCELERATION_RATIO:
            score = min(score + 10.0, 100.0)

        score = round(score, 2)
        results[path] = HotZoneResult(
            file_path=path,
            hot_zone_score=score,
            is_hot_zone=score > threshold,
            velocity_ratio=velocity,
        )

    return results
