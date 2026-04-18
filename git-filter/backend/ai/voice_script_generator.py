"""
ai/voice_script_generator.py
Generates a structured voice guide script for the repository walkthrough.
Produces 6 sections consumed by tts_runner.py.
"""

import logging
from ai.ollama_client import call_ollama, OllamaError

logger = logging.getLogger(__name__)


def generate_voice_script(
    repo_url: str,
    graph_stats: dict,
    high_impact_files: list[dict],
    onboarding_path: list[dict],
    ai_summaries: dict[str, str],
) -> list[dict]:
    """
    Generate the complete voice guide script for TTS conversion.

    Returns a list of section dicts:
    [{"section_title": str, "script_text": str}, ...]
    """
    repo_name = repo_url.rstrip("/").split("/")[-1]
    total_files = graph_stats.get("total_nodes", 0)
    sections = graph_stats.get("sections", {})
    high_impact_names = [f["id"].split("/")[-1] for f in high_impact_files[:5]]
    onboarding_files = [step["file_path"].split("/")[-1] for step in onboarding_path[:5]]

    # Build context for LLM
    top_files_context = ""
    for f in high_impact_files[:5]:
        path = f["id"]
        summary = ai_summaries.get(path, "A core system component.")
        top_files_context += f"- {path.split('/')[-1]}: {summary[:100]}\n"

    sections_text = ", ".join(f"{k}: {v} files" for k, v in sections.items())

    script_sections = [
        {
            "section_title": "Introduction",
            "prompt": (
                f"Write a 100-word conversational introduction to a codebase called '{repo_name}'. "
                f"Describe what problem it solves and why it exists. "
                "Speak directly to a new developer in first-person perspective. "
                "Example tone: 'You're looking at a full-stack web application that handles...'"
            ),
        },
        {
            "section_title": "Architecture Overview",
            "prompt": (
                f"Write a 150-word architecture overview for '{repo_name}'. "
                f"The codebase has {total_files} files organized as: {sections_text}. "
                "Explain how the code is organized in simple terms. "
                "Speak conversationally to a developer who is new to the project."
            ),
        },
        {
            "section_title": "Core Components",
            "prompt": (
                f"Write a 200-word walkthrough of the top 5 most important files in '{repo_name}':\n"
                f"{top_files_context}\n"
                "Explain each one in 1-2 sentences. Be specific about what each file does. "
                "Speak conversationally. Use the file name when referring to each component."
            ),
        },
        {
            "section_title": "Onboarding Path",
            "prompt": (
                f"Write a 150-word onboarding reading guide for '{repo_name}'. "
                f"Tell the developer to read these files in this order: "
                f"{', '.join(onboarding_files)}. "
                "Explain briefly why each file should be read first. "
                "Speak encouragingly and conversationally."
            ),
        },
        {
            "section_title": "Risk Areas",
            "prompt": (
                f"Write a 100-word risk briefing for '{repo_name}'. "
                f"The following files are flagged as high-risk: {', '.join(high_impact_names)}. "
                "Warn the developer to be careful when modifying these files and explain why. "
                "Be direct but not alarming."
            ),
        },
        {
            "section_title": "Closing",
            "prompt": (
                f"Write a 50-word closing message for the '{repo_name}' codebase walkthrough. "
                "Tell the developer they now have a solid mental model of the project. "
                "Give them confidence. Mention one practical tip for exploring further."
            ),
        },
    ]

    result = []
    for section in script_sections:
        try:
            text = call_ollama(section["prompt"], max_tokens=300)
        except OllamaError as exc:
            logger.warning(
                f"Voice script generation failed for section '{section['section_title']}': {exc}"
            )
            text = _fallback_text(section["section_title"], repo_name)

        result.append({
            "section_title": section["section_title"],
            "script_text": text,
        })

    return result


def _fallback_text(section_title: str, repo_name: str) -> str:
    fallbacks = {
        "Introduction": f"Welcome to {repo_name}. This is a software project that you will be working with.",
        "Architecture Overview": f"The {repo_name} codebase is organized into multiple sections including the UI layer, backend services, utilities, and configuration.",
        "Core Components": f"The core components of {repo_name} include the main application entry point, the business logic layer, and the data access layer.",
        "Onboarding Path": "Start by reading the main entry point, then move to the core business logic, followed by utilities and configuration files.",
        "Risk Areas": "Take care when modifying the high-impact files as they affect many parts of the system.",
        "Closing": f"You now have a solid understanding of {repo_name}. Explore the codebase with confidence.",
    }
    return fallbacks.get(section_title, f"Section: {section_title}")
