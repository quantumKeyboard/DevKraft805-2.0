"""
reports/nontechnical_report.py
Assembles and renders the non-technical stakeholder report using Jinja2.
"""

from datetime import datetime, timezone
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape


_TEMPLATE_DIR = Path(__file__).parent / "templates"


def _compute_health(stats: dict) -> tuple[str, str]:
    """Compute a simple High/Medium/Low health label and explanation."""
    total = stats.get("total_nodes", 1)
    orphans = stats.get("orphan_count", 0)
    hot_zones = stats.get("hot_zone_count", 0)
    high_impact = stats.get("high_impact_count", 0)

    orphan_ratio = orphans / max(total, 1)
    hot_ratio = hot_zones / max(total, 1)

    if orphan_ratio > 0.2 or hot_ratio > 0.3:
        level = "Low"
        explanation = (
            "The system shows significant risk signals: a high proportion of unused components "
            "and/or many files predicted to change soon. Immediate attention is recommended."
        )
    elif orphan_ratio > 0.1 or hot_ratio > 0.15:
        level = "Medium"
        explanation = (
            "The system is stable but has moderate risk signals that should be monitored. "
            "Some cleanup and targeted testing would improve overall quality."
        )
    else:
        level = "High"
        explanation = (
            "The system is in good health. Dependencies are well-organized, "
            "orphaned code is minimal, and few components are in high-risk zones."
        )
    return level, explanation


def render_nontechnical_report(
    repo_url: str,
    graph_stats: dict,
    high_impact_nodes: list[dict],
    hot_zone_nodes: list[dict],
    ai_summary_text: str,
) -> str:
    """Render the non-technical stakeholder report as an HTML string."""

    env = Environment(
        loader=FileSystemLoader(str(_TEMPLATE_DIR)),
        autoescape=select_autoescape(["html"]),
    )
    template = env.get_template("nontechnical_report.html.j2")

    repo_name = repo_url.rstrip("/").split("/")[-1]
    health_level, health_explanation = _compute_health(graph_stats)

    # Build "what it does" paragraph from the AI summary
    # Split into two parts for the template
    summary_parts = ai_summary_text.split("\n\n")
    what_it_does = "\n\n".join(summary_parts[:2]) if len(summary_parts) > 1 else ai_summary_text

    return template.render(
        repo_url=repo_url,
        repo_name=repo_name,
        stats=graph_stats,
        sections=graph_stats.get("sections", {}),
        sections_count=len(graph_stats.get("sections", {})),
        key_components=high_impact_nodes[:5],
        risk_areas=hot_zone_nodes,
        what_it_does=what_it_does,
        ai_summary_text=ai_summary_text,
        health_level=health_level,
        health_explanation=health_explanation,
        generated_at=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
    )
