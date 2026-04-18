"""
graph/centrality.py
Computes PageRank centrality for all nodes and flags high-impact files.
"""

import logging
import networkx as nx
from core.config import get_settings

logger = logging.getLogger(__name__)


def compute_centrality(G: nx.DiGraph) -> nx.DiGraph:
    """
    Run PageRank on the graph and normalize scores to 0–100.
    Updates node attributes in-place:
        - impact_score: normalized 0–100 float
        - is_high_impact: bool (True if impact_score > HIGH_IMPACT_THRESHOLD)

    Returns the modified graph.
    """
    settings = get_settings()
    threshold = settings.high_impact_threshold

    if G.number_of_nodes() == 0:
        return G

    try:
        pagerank = nx.pagerank(G, alpha=0.85, max_iter=100, tol=1e-6)
    except nx.PowerIterationFailedConvergence:
        logger.warning("PageRank did not converge. Using degree centrality as fallback.")
        degree_centrality = nx.degree_centrality(G)
        pagerank = degree_centrality

    # Normalize to 0–100
    min_pr = min(pagerank.values())
    max_pr = max(pagerank.values())

    for node in G.nodes:
        raw = pagerank.get(node, 0.0)
        if max_pr > min_pr:
            score = (raw - min_pr) / (max_pr - min_pr) * 100.0
        else:
            score = 50.0  # All nodes equal

        score = round(score, 2)
        G.nodes[node]["impact_score"] = score
        G.nodes[node]["is_high_impact"] = score > threshold

    high_impact_count = sum(
        1 for n in G.nodes if G.nodes[n].get("is_high_impact", False)
    )
    logger.info(
        f"Centrality computed. High-impact nodes: {high_impact_count}/{G.number_of_nodes()} "
        f"(threshold: {threshold})"
    )
    return G
