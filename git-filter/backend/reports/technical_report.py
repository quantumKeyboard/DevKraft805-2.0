"""
reports/technical_report.py
Assembles and renders the technical report using Jinja2.
"""

from datetime import datetime, timezone
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape


_TEMPLATE_DIR = Path(__file__).parent / "templates"


def render_technical_report(
    repo_url: str,
    owner: str,
    repo: str,
    graph_stats: dict,
    high_impact_nodes: list[dict],
    orphan_paths: list[str],
    hot_zone_nodes: list[dict],
    onboarding_path: list[dict],
    ai_summary_text: str,
    commit_map: dict,
) -> str:
    """Render the technical report as an HTML string."""

    env = Environment(
        loader=FileSystemLoader(str(_TEMPLATE_DIR)),
        autoescape=select_autoescape(["html"]),
    )
    template = env.get_template("technical_report.html.j2")

    languages = graph_stats.get("languages", {})
    languages_str = ", ".join(f"{k} ({v})" for k, v in languages.items())

    return template.render(
        repo_url=repo_url,
        repo_name=repo,
        owner=owner,
        repo=repo,
        stats=graph_stats,
        languages_str=languages_str,
        sections=graph_stats.get("sections", {}),
        high_impact_nodes=high_impact_nodes,
        orphan_paths=orphan_paths,
        hot_zone_nodes=hot_zone_nodes,
        onboarding_path=list(enumerate(onboarding_path)),
        ai_summary_text=ai_summary_text,
        generated_at=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
    )
