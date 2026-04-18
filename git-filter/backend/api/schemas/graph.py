"""
api/schemas/graph.py
Pydantic schemas for graph data.
"""

from pydantic import BaseModel
from typing import Any


class GraphNode(BaseModel):
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
    functions: list[str]
    classes: list[str]
    contributors: list[str]
    contributor_count: int
    last_modified: str
    ai_summary: str
    depends_on: list[str]
    depended_on_by: list[str]


class GraphEdge(BaseModel):
    id: str
    source: str
    target: str
    type: str
    weight: int = 1


class GraphResponse(BaseModel):
    repo_id: str
    nodes: list[GraphNode]
    edges: list[GraphEdge]
    stats: dict[str, Any] = {}
