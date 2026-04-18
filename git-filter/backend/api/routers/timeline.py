"""
api/routers/timeline.py
GET /timeline/{repo_id} — returns architecture evolution timeline.
"""

from fastapi import APIRouter, HTTPException
from api.routers.analyze import REPO_STORE

router = APIRouter(prefix="/timeline", tags=["timeline"])


@router.get("/{repo_id}")
async def get_timeline(repo_id: str):
    store = REPO_STORE.get(repo_id)
    if not store:
        raise HTTPException(status_code=404, detail="Repo ID not found.")
    if store.get("status") != "complete":
        raise HTTPException(status_code=202, detail="Analysis not yet complete.")

    return {
        "repo_id": repo_id,
        "timeline": store.get("timeline", []),
    }
