"""
graph/orphan_detector.py
Identifies orphaned nodes: files that nothing imports, that are not
known entry points or test files.
"""

import logging
import networkx as nx
from core.constants import ENTRY_POINT_FILENAMES

logger = logging.getLogger(__name__)


def detect_orphans(G: nx.DiGraph) -> list[str]:
    """
    Mark orphaned nodes in the graph.
    
    A node is orphaned if:
        in_degree == 0
        AND section != "Tests"
        AND filename not in ENTRY_POINT_FILENAMES

    Updates node attribute `is_orphan = True` for orphaned nodes.
    Returns list of orphaned file paths.
    """
    orphans: list[str] = []

    for node in G.nodes:
        attrs = G.nodes[node]
        filename = node.split("/")[-1].lower()
        section = attrs.get("section", "")

        if (
            G.in_degree(node) == 0
            and section != "Tests"
            and filename not in ENTRY_POINT_FILENAMES
        ):
            G.nodes[node]["is_orphan"] = True
            orphans.append(node)
        else:
            G.nodes[node]["is_orphan"] = False

    logger.info(f"Orphan detection: {len(orphans)} orphaned modules found.")
    return orphans
