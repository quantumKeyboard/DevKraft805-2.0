"""
api/routers/query.py
POST /query — accepts NL query, returns matching node IDs.
"""

from fastapi import APIRouter, HTTPException
from api.schemas.query import NLQueryRequest, NLQueryResponse
from api.routers.analyze import REPO_STORE
from ai.nl_query_handler import process_nl_query

router = APIRouter(prefix="/query", tags=["query"])


@router.post("", response_model=NLQueryResponse)
async def nl_query(request: NLQueryRequest):
    store = REPO_STORE.get(request.repo_id)
    if not store:
        raise HTTPException(status_code=404, detail="Repo ID not found.")
    if store.get("status") != "complete":
        raise HTTPException(status_code=202, detail="Analysis not yet complete.")

    graph = store.get("graph", {})
    nodes = graph.get("nodes", [])

    result = process_nl_query(request.query, nodes)
    return NLQueryResponse(**result)
