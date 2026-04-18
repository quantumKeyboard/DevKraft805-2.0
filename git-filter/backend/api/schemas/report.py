"""
api/schemas/report.py
Pydantic schema for report responses.
"""

from pydantic import BaseModel
from datetime import datetime


class ReportResponse(BaseModel):
    html_content: str
    generated_at: str
    report_type: str  # "technical" | "nontechnical"
