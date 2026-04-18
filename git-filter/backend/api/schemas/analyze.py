"""
api/schemas/analyze.py
Pydantic schemas for the /analyze endpoint.
"""

from pydantic import BaseModel, HttpUrl, field_validator


class AnalyzeRequest(BaseModel):
    repo_url: str

    @field_validator("repo_url")
    @classmethod
    def validate_github_url(cls, v: str) -> str:
        v = v.strip()
        if "github.com" not in v:
            raise ValueError("Only GitHub repository URLs are supported.")
        return v


class AnalyzeResponse(BaseModel):
    repo_id: str
    status: str          # "queued" | "running" | "complete" | "error"
    message: str = ""
