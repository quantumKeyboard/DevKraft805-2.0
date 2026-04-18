"""
api/routers/graph.py
GET /graph/{repo_id} — returns full graph JSON for the frontend.
"""

from fastapi import APIRouter, HTTPException
from api.routers.analyze import REPO_STORE

router = APIRouter(prefix="/graph", tags=["graph"])


@router.get("/{repo_id}")
async def get_graph(repo_id: str):
    store = REPO_STORE.get(repo_id)
    if not store:
        raise HTTPException(status_code=404, detail="Repo ID not found. Run /analyze first.")

    status = store.get("status")
    if status == "running" or status == "queued":
        return {
            "repo_id": repo_id,
            "status": status,
            "status_detail": store.get("status_detail", ""),
            "nodes": [],
            "edges": [],
            "stats": {},
        }
    if status == "error":
        raise HTTPException(
            status_code=422,
            detail=f"Analysis failed: {store.get('error_message', 'Unknown error')}",
        )

    graph = store.get("graph", {"nodes": [], "edges": []})
    return {
        "repo_id": repo_id,
        "status": "complete",
        "nodes": graph.get("nodes", []),
        "edges": graph.get("edges", []),
        "stats": store.get("stats", {}),
        "repo_url": store.get("repo_url", ""),
        "owner": store.get("owner", ""),
        "repo": store.get("repo", ""),
    }
