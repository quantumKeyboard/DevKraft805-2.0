"""
api/routers/onboarding.py
GET /onboarding/{repo_id} — returns the ordered onboarding reading path.
"""

from fastapi import APIRouter, HTTPException
from api.routers.analyze import REPO_STORE

router = APIRouter(prefix="/onboarding", tags=["onboarding"])


@router.get("/{repo_id}")
async def get_onboarding_path(repo_id: str):
    store = REPO_STORE.get(repo_id)
    if not store:
        raise HTTPException(status_code=404, detail="Repo ID not found.")
    if store.get("status") != "complete":
        raise HTTPException(status_code=202, detail="Analysis not yet complete.")

    return {
        "repo_id": repo_id,
        "onboarding_path": store.get("onboarding", []),
    }
