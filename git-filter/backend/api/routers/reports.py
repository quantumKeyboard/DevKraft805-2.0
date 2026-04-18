"""
api/routers/reports.py
GET /reports/{repo_id}/technical
GET /reports/{repo_id}/nontechnical
Returns HTML content of the generated reports.
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse
from api.routers.analyze import REPO_STORE
from datetime import datetime, timezone

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/{repo_id}/technical", response_class=HTMLResponse)
async def get_technical_report(repo_id: str):
    store = REPO_STORE.get(repo_id)
    if not store:
        raise HTTPException(status_code=404, detail="Repo ID not found.")
    if store.get("status") != "complete":
        raise HTTPException(status_code=202, detail="Analysis not yet complete.")

    html = store.get("technical_report_html", "<p>Report not available.</p>")
    return HTMLResponse(content=html)


@router.get("/{repo_id}/nontechnical", response_class=HTMLResponse)
async def get_nontechnical_report(repo_id: str):
    store = REPO_STORE.get(repo_id)
    if not store:
        raise HTTPException(status_code=404, detail="Repo ID not found.")
    if store.get("status") != "complete":
        raise HTTPException(status_code=202, detail="Analysis not yet complete.")

    html = store.get("nontechnical_report_html", "<p>Report not available.</p>")
    return HTMLResponse(content=html)
