"""
api/routers/node.py
GET /node/{repo_id}/{node_id:path} — returns full node detail including AI summary.
"""

import urllib.parse
from fastapi import APIRouter, HTTPException, Path
from api.routers.analyze import REPO_STORE

router = APIRouter(prefix="/node", tags=["node"])


@router.get("/{repo_id}/{node_id:path}")
async def get_node_detail(repo_id: str, node_id: str):
    store = REPO_STORE.get(repo_id)
    if not store:
        raise HTTPException(status_code=404, detail="Repo ID not found.")
    if store.get("status") != "complete":
        raise HTTPException(status_code=202, detail="Analysis not yet complete.")

    graph = store.get("graph", {})
    nodes = {n["id"]: n for n in graph.get("nodes", [])}

    # node_id may be URL-encoded
    decoded_id = urllib.parse.unquote(node_id)
    node = nodes.get(decoded_id) or nodes.get(node_id)
    if not node:
        raise HTTPException(status_code=404, detail=f"Node not found: {node_id}")

    owner = store.get("owner", "")
    repo = store.get("repo", "")
    github_url = (
        f"https://github.com/{owner}/{repo}/blob/HEAD/{decoded_id}"
        if owner and repo else ""
    )

    # Build contributor info from raw commit map (if available)
    commit_map = store.get("commit_map_summary", {})
    contributor_info = [
        {"name": c, "commit_count": 1} for c in node.get("contributors", [])
    ]

    return {
        **node,
        "github_url": github_url,
        "contributors": contributor_info,
    }
