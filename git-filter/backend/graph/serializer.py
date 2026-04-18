"""
graph/serializer.py
Converts a NetworkX DiGraph to the JSON format consumed by the frontend.
Produces the exact shape specified in Section 8.3 of the PROJECT_MAP.
"""

import networkx as nx


def serialize_graph(G: nx.DiGraph) -> dict:
    """
    Convert the NetworkX graph to frontend-consumable JSON.

    Returns:
    {
        "nodes": [...],
        "edges": [...]
    }
    """
    nodes = []
    for node_id in G.nodes:
        attrs = G.nodes[node_id]
        nodes.append({
            "id": node_id,
            "label": attrs.get("label", node_id.split("/")[-1]),
            "path": attrs.get("path", node_id),
            "language": attrs.get("language", "unknown"),
            "section": attrs.get("section", "Backend"),
            "impact_score": attrs.get("impact_score", 0.0),
            "is_high_impact": attrs.get("is_high_impact", False),
            "is_orphan": attrs.get("is_orphan", False),
            "is_hot_zone": attrs.get("is_hot_zone", False),
            "churn_score": attrs.get("churn_score", 0.0),
            "bug_commit_ratio": attrs.get("bug_commit_ratio", 0.0),
            "hot_zone_score": attrs.get("hot_zone_score", 0.0),
            "functions": attrs.get("functions", []),
            "classes": attrs.get("classes", []),
            "contributors": attrs.get("contributors", []),
            "contributor_count": attrs.get("contributor_count", 0),
            "last_modified": attrs.get("last_modified", ""),
            "ai_summary": attrs.get("ai_summary", ""),
            # Dependency lists computed from edges
            "depends_on": [t for _, t, d in G.out_edges(node_id, data=True)],
            "depended_on_by": [s for s, _, d in G.in_edges(node_id, data=True)],
        })

    edges = []
    for i, (source, target, data) in enumerate(G.edges(data=True)):
        edges.append({
            "id": f"edge-{i:05d}",
            "source": source,
            "target": target,
            "type": data.get("type", "imports"),
            "weight": data.get("weight", 1),
        })

    return {"nodes": nodes, "edges": edges}


def serialize_graph_stats(G: nx.DiGraph) -> dict:
    """
    Compute and return summary statistics about the graph.
    Used in report generation.
    """
    if G.number_of_nodes() == 0:
        return {}

    sections: dict[str, int] = {}
    languages: dict[str, int] = {}
    high_impact = 0
    orphans = 0
    hot_zones = 0

    for node_id in G.nodes:
        attrs = G.nodes[node_id]
        section = attrs.get("section", "Backend")
        lang = attrs.get("language", "unknown")
        sections[section] = sections.get(section, 0) + 1
        languages[lang] = languages.get(lang, 0) + 1
        if attrs.get("is_high_impact"):
            high_impact += 1
        if attrs.get("is_orphan"):
            orphans += 1
        if attrs.get("is_hot_zone"):
            hot_zones += 1

    in_degrees = [d for _, d in G.in_degree()]
    out_degrees = [d for _, d in G.out_degree()]

    return {
        "total_nodes": G.number_of_nodes(),
        "total_edges": G.number_of_edges(),
        "high_impact_count": high_impact,
        "orphan_count": orphans,
        "hot_zone_count": hot_zones,
        "sections": sections,
        "languages": languages,
        "avg_in_degree": round(sum(in_degrees) / len(in_degrees), 2) if in_degrees else 0,
        "avg_out_degree": round(sum(out_degrees) / len(out_degrees), 2) if out_degrees else 0,
        "isolated_components": nx.number_weakly_connected_components(G),
    }
