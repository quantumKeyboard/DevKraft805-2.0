"""
ai/nl_query_handler.py
Processes natural language queries against the repository graph.
Step 1: Keyword extraction + scoring
Step 2: Top-N node retrieval  
Step 3: LLM explanation of primary match
"""

import logging
import re
from ai.ollama_client import call_ollama, OllamaError
from core.constants import NL_QUERY_TOP_N

logger = logging.getLogger(__name__)

# Common English stop words to remove from query keywords
_STOP_WORDS = {
    "a", "an", "the", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "will", "would", "could",
    "should", "may", "might", "shall", "can", "need", "dare", "ought",
    "used", "to", "of", "in", "for", "on", "with", "at", "by", "from",
    "up", "about", "into", "through", "during", "before", "after",
    "above", "below", "between", "out", "off", "over", "under", "again",
    "further", "then", "once", "where", "which", "who", "whom", "what",
    "this", "that", "these", "those", "i", "me", "my", "myself", "we",
    "our", "you", "your", "it", "its", "they", "them", "their",
    "show", "find", "get", "how", "handled", "handle", "handles",
    "located", "located", "file", "files", "code", "module",
}


def _extract_keywords(query: str) -> list[str]:
    """Extract meaningful keywords from a natural language query."""
    tokens = re.findall(r"\w+", query.lower())
    return [t for t in tokens if t not in _STOP_WORDS and len(t) > 2]


def _score_node(
    node_id: str,
    attrs: dict,
    keywords: list[str],
) -> float:
    """
    Compute match score for a node against the query keywords.
    Scoring weights (from spec Section 8.10):
        path match   × 2
        summary match × 3
        func/class match × 2
    """
    score = 0.0
    path_lower = node_id.lower()
    summary_lower = attrs.get("ai_summary", "").lower()
    defines_lower = " ".join(
        attrs.get("functions", []) + attrs.get("classes", [])
    ).lower()
    label_lower = attrs.get("label", "").lower()

    for kw in keywords:
        if kw in path_lower or kw in label_lower:
            score += 2.0
        if kw in summary_lower:
            score += 3.0
        if kw in defines_lower:
            score += 2.0

    return score


def process_nl_query(
    query: str,
    graph_nodes: list[dict],   # serialized node dicts from serializer
    top_n: int = NL_QUERY_TOP_N,
) -> dict:
    """
    Process a natural language query and return matching nodes.

    Returns:
    {
        "matching_node_ids": [...],
        "explanation": "...",
        "primary_match": "...",
        "keywords": [...]
    }
    """
    keywords = _extract_keywords(query)
    if not keywords:
        return {
            "matching_node_ids": [],
            "explanation": "No meaningful keywords found in query.",
            "primary_match": None,
            "keywords": [],
        }

    # Score all nodes
    scored = []
    for node in graph_nodes:
        score = _score_node(node["id"], node, keywords)
        if score > 0:
            scored.append((node["id"], score, node))

    scored.sort(key=lambda x: x[1], reverse=True)
    top_matches = scored[:top_n]

    if not top_matches:
        return {
            "matching_node_ids": [],
            "explanation": f"No files matched the query: '{query}'",
            "primary_match": None,
            "keywords": keywords,
        }

    matching_ids = [m[0] for m in top_matches]
    primary_match = matching_ids[0]

    # LLM explanation
    explanation = _get_llm_explanation(query, top_matches[:5])

    return {
        "matching_node_ids": matching_ids,
        "explanation": explanation,
        "primary_match": primary_match,
        "keywords": keywords,
    }


def _get_llm_explanation(query: str, top_matches: list) -> str:
    """Generate a one-sentence LLM explanation of the primary match."""
    if not top_matches:
        return ""

    file_list = "\n".join(
        f"- {m[0]} (score: {m[1]:.1f}): {m[2].get('ai_summary', '')[:100]}"
        for m in top_matches
    )
    prompt = (
        f"A developer searched for: \"{query}\"\n"
        f"The following files matched (ordered by relevance):\n{file_list}\n\n"
        "In exactly one sentence, explain which file is the most likely answer to the "
        "developer's question and why."
    )

    try:
        return call_ollama(prompt, max_tokens=100)
    except OllamaError as exc:
        logger.warning(f"NL query LLM explanation failed: {exc}")
        top_file = top_matches[0][0].split("/")[-1]
        return f"'{top_file}' is the most relevant file based on keyword matching."
