"""
ai/report_generator.py
Generates technical and non-technical report text via Ollama.
"""

import logging
from ai.ollama_client import call_ollama, OllamaError

logger = logging.getLogger(__name__)


def generate_technical_summary(
    repo_url: str,
    graph_stats: dict,
    high_impact_files: list[dict],
    orphaned_files: list[str],
    hot_zone_files: list[dict],
    onboarding_path: list[dict],
) -> str:
    """
    Generate an AI-written technical architecture summary (3–4 paragraphs).
    Used in the technical report.
    """
    high_impact_names = [f["id"].split("/")[-1] for f in high_impact_files[:5]]
    hot_zone_names = [f["id"].split("/")[-1] for f in hot_zone_files[:5]]

    prompt = (
        f"You are writing a technical architecture overview for a software team.\n\n"
        f"Repository: {repo_url}\n"
        f"Total files analyzed: {graph_stats.get('total_nodes', 0)}\n"
        f"Total dependencies mapped: {graph_stats.get('total_edges', 0)}\n"
        f"Sections: {graph_stats.get('sections', {})}\n"
        f"Languages: {graph_stats.get('languages', {})}\n"
        f"High-impact files (most central): {', '.join(high_impact_names)}\n"
        f"Predicted hot zones (likely to change): {', '.join(hot_zone_names)}\n"
        f"Orphaned modules: {len(orphaned_files)}\n"
        f"Onboarding entry point: {onboarding_path[0]['file_path'] if onboarding_path else 'N/A'}\n\n"
        "Write a 3–4 paragraph technical summary covering:\n"
        "1. What this system does architecturally\n"
        "2. Key entry points and dependency density\n"
        "3. Risk areas (high-churn files, high-impact files)\n"
        "4. Orphaned modules and recommended cleanup\n"
        "Be specific and technical. Write for experienced engineers."
    )

    try:
        return call_ollama(prompt, max_tokens=600)
    except OllamaError as exc:
        logger.warning(f"Technical summary generation failed: {exc}")
        return (
            f"This repository contains {graph_stats.get('total_nodes', 0)} analyzed files "
            f"across {len(graph_stats.get('sections', {}))} architectural sections. "
            f"There are {graph_stats.get('high_impact_count', 0)} high-impact files "
            f"and {graph_stats.get('orphan_count', 0)} orphaned modules."
        )


def generate_nontechnical_summary(
    repo_url: str,
    graph_stats: dict,
    high_impact_files: list[dict],
    hot_zone_files: list[dict],
    ai_summaries: dict[str, str],
) -> str:
    """
    Generate an AI-written non-technical summary in plain business language.
    Used in the non-technical report.
    """
    # Describe high-impact files in plain language using their AI summaries
    key_components = []
    for f in high_impact_files[:5]:
        path = f["id"]
        summary = ai_summaries.get(path, "A key system component.")
        key_components.append(f"- {summary[:120]}")

    components_text = "\n".join(key_components) if key_components else "- Core system components"

    prompt = (
        "You are writing a report for a non-technical business stakeholder.\n\n"
        f"Repository: {repo_url}\n"
        f"Total code files: {graph_stats.get('total_nodes', 0)}\n\n"
        f"Key components (in plain terms):\n{components_text}\n\n"
        f"Number of high-risk areas: {graph_stats.get('hot_zone_count', 0)}\n\n"
        "Write a plain-English summary that explains:\n"
        "1. What this software does (2 sentences, no technical jargon)\n"
        "2. How it is organized (use business analogies, not file paths)\n"
        "3. Which parts carry the most risk and why (in business terms)\n"
        "4. 3 recommended actions\n\n"
        "Avoid all technical jargon. Write as if explaining to a CEO or product manager."
    )

    try:
        return call_ollama(prompt, max_tokens=600)
    except OllamaError as exc:
        logger.warning(f"Non-technical summary generation failed: {exc}")
        return (
            "This software system has been analyzed. "
            f"It contains {graph_stats.get('total_nodes', 0)} components. "
            f"There are {graph_stats.get('hot_zone_count', 0)} areas flagged as high-risk "
            "that may need attention."
        )
