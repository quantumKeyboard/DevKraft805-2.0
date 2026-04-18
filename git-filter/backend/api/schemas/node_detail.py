"""
api/schemas/node_detail.py
Pydantic schema for full node detail response.
"""

from pydantic import BaseModel


class ContributorInfo(BaseModel):
    name: str
    commit_count: int


class NodeDetail(BaseModel):
    id: str
    label: str
    path: str
    language: str
    section: str
    impact_score: float
    is_high_impact: bool
    is_orphan: bool
    is_hot_zone: bool
    churn_score: float
    bug_commit_ratio: float
    hot_zone_score: float
    ai_summary: str
    functions: list[str]
    classes: list[str]
    depends_on: list[str]
    depended_on_by: list[str]
    contributors: list[ContributorInfo]
    contributor_count: int
    last_modified: str
    github_url: str = ""
