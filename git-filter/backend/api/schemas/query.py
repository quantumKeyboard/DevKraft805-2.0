"""
api/schemas/query.py
Pydantic schemas for the NL query endpoint.
"""

from pydantic import BaseModel


class NLQueryRequest(BaseModel):
    repo_id: str
    query: str


class NLQueryResponse(BaseModel):
    matching_node_ids: list[str]
    explanation: str
    primary_match: str | None
    keywords: list[str]
