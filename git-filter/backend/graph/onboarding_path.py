"""
graph/onboarding_path.py
Generates an ordered onboarding reading list:
  Step 1: Topological sort of the dependency graph
  Step 2: Filter to entry points, high-impact, and Backend section nodes (top 20)
  Step 3: LLM re-ranking via Ollama for business logic priority
  Step 4: Merge with remaining files
"""

import json
import logging
import networkx as nx

from core.constants import ENTRY_POINT_FILENAMES, ONBOARDING_PATH_TOP_N
from ai.ollama_client import call_ollama

logger = logging.getLogger(__name__)


def _is_entry_point(node: str) -> bool:
    filename = node.split("/")[-1].lower()
    return filename in ENTRY_POINT_FILENAMES


def _topological_sort_with_fallback(G: nx.DiGraph) -> list[str]:
    """
    Attempt topological sort. On cycle detection, use a linearized DFS order instead.
    """
    try:
        return list(nx.topological_sort(G))
    except nx.NetworkXUnfeasible:
        logger.warning("Graph has cycles — using DFS linearization for onboarding path.")
        return list(nx.dfs_preorder_nodes(G))


def generate_onboarding_path(
    G: nx.DiGraph,
    file_contents: dict[str, str],   # {file_path → raw content}
    ai_summaries: dict[str, str],     # {file_path → ai_summary} (may be empty initially)
) -> list[dict]:
    """
    Generate the ordered onboarding reading path.

    Returns: list of {file_path, section, reason, ai_summary_excerpt}
    """
    topo_order = _topological_sort_with_fallback(G)

    # Step 2: Filter to important nodes
    priority_nodes = [
        n for n in topo_order
        if (
            _is_entry_point(n)
            or G.nodes[n].get("is_high_impact", False)
            or G.nodes[n].get("section") == "Backend"
        )
    ]

    # Take top N for LLM re-ranking
    top_nodes = priority_nodes[:ONBOARDING_PATH_TOP_N]

    # Build node descriptions for LLM
    node_descriptions = []
    for path in top_nodes:
        attrs = G.nodes[path]
        summary = ai_summaries.get(path, "")
        functions = attrs.get("functions", [])
        classes = attrs.get("classes", [])
        node_descriptions.append({
            "file_path": path,
            "section": attrs.get("section", "Backend"),
            "impact_score": attrs.get("impact_score", 0),
            "summary": summary or f"Defines: {', '.join(functions[:3] + classes[:3])}",
        })

    # Step 3: LLM re-ranking
    llm_order = _llm_rerank(node_descriptions)

    # Step 4: Merge with remaining files
    llm_paths = [item["file_path"] for item in llm_order]
    remaining = [
        n for n in topo_order
        if n not in set(llm_paths) and not G.nodes[n].get("section") in ("Tests",)
    ]

    final_path = llm_order + [
        {
            "file_path": n,
            "section": G.nodes[n].get("section", "Backend"),
            "reason": "Supporting module — read after understanding core business logic.",
            "ai_summary_excerpt": ai_summaries.get(n, "")[:200],
        }
        for n in remaining
    ]

    return final_path


def _llm_rerank(node_descriptions: list[dict]) -> list[dict]:
    """
    Send top nodes to Ollama for onboarding path re-ranking.
    Falls back to impact_score ordering if LLM fails.
    """
    if not node_descriptions:
        return []

    prompt = (
        "You are helping a new developer onboard to a codebase.\n"
        "Given these files in approximate topological dependency order with their descriptions,\n"
        "produce an ordered onboarding reading path that prioritizes understanding "
        "core business logic before utilities and configs.\n\n"
        "Files:\n"
    )
    for item in node_descriptions:
        prompt += (
            f"- {item['file_path']} ({item['section']}, impact: {item['impact_score']:.0f}): "
            f"{item['summary'][:100]}\n"
        )
    prompt += (
        "\nReturn ONLY a JSON array of objects with keys: "
        '"file_path", "reason" (one sentence). '
        "Order from most important for onboarding first."
    )

    try:
        response = call_ollama(prompt, max_tokens=1000)
        # Extract JSON array from response
        start = response.find("[")
        end = response.rfind("]") + 1
        if start >= 0 and end > start:
            items = json.loads(response[start:end])
            # Validate and enrich
            result = []
            for item in items:
                fp = item.get("file_path", "")
                if not fp:
                    continue
                # Find the original node's section
                original = next(
                    (n for n in node_descriptions if n["file_path"] == fp), None
                )
                result.append({
                    "file_path": fp,
                    "section": original["section"] if original else "Backend",
                    "reason": item.get("reason", "High-importance module."),
                    "ai_summary_excerpt": original["summary"][:200] if original else "",
                })
            return result
    except Exception as exc:
        logger.warning(f"LLM onboarding re-ranking failed: {exc}. Using fallback order.")

    # Fallback: sort by impact score descending
    sorted_nodes = sorted(node_descriptions, key=lambda x: x["impact_score"], reverse=True)
    return [
        {
            "file_path": n["file_path"],
            "section": n["section"],
            "reason": "High-impact file — critical to understand early.",
            "ai_summary_excerpt": n["summary"][:200],
        }
        for n in sorted_nodes
    ]
