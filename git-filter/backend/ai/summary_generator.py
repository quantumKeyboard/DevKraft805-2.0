"""
ai/summary_generator.py
Generates plain-English AI summaries for each file node using Ollama.
Implements disk-based caching (via diskcache) and batched processing.
"""

import hashlib
import logging
import time
from pathlib import Path

from core.config import get_settings
from ai.ollama_client import call_ollama, OllamaError

logger = logging.getLogger(__name__)

_SUMMARY_PROMPT_TEMPLATE = """\
You are a senior software engineer explaining a codebase to a new developer.

File: {file_path}
Language: {language}
Section: {section}
Imports: {imports}
Defines: {defines}

Content preview:
{content_preview}

In 2-3 sentences, explain what this file does and its role in the system.
Be concrete and specific. Do not use phrases like "this file" or "this module".\
"""

_MAX_CONTENT_LINES = 200


def _get_cache():
    """Lazily initialise the diskcache.Cache."""
    try:
        import diskcache
        settings = get_settings()
        cache_dir = Path(settings.summary_cache_dir)
        cache_dir.mkdir(parents=True, exist_ok=True)
        return diskcache.Cache(str(cache_dir))
    except ImportError:
        logger.warning("diskcache not installed — AI summaries will not be cached.")
        return None


def _content_hash(content: str) -> str:
    return hashlib.md5(content.encode()).hexdigest()


def _build_prompt(
    file_path: str,
    language: str,
    section: str,
    imports: list[str],
    functions: list[str],
    classes: list[str],
    content: str,
) -> str:
    content_lines = content.splitlines()[:_MAX_CONTENT_LINES]
    content_preview = "\n".join(content_lines)

    defines = ", ".join(functions[:10] + classes[:10]) or "(none detected)"
    import_str = ", ".join(imports[:15]) or "(none)"

    return _SUMMARY_PROMPT_TEMPLATE.format(
        file_path=file_path,
        language=language,
        section=section,
        imports=import_str,
        defines=defines,
        content_preview=content_preview,
    )


def generate_summary(
    file_path: str,
    language: str,
    section: str,
    imports: list[str],
    functions: list[str],
    classes: list[str],
    content: str,
    cache=None,
) -> str:
    """
    Generate (or retrieve from cache) an AI summary for a single file.
    Returns the summary string, or a fallback placeholder on failure.
    """
    content_key = _content_hash(content)
    cache_key = f"summary:{content_key}"

    if cache is not None:
        cached = cache.get(cache_key)
        if cached:
            logger.debug(f"Cache hit for summary: {file_path}")
            return cached

    prompt = _build_prompt(
        file_path, language, section, imports, functions, classes, content
    )

    try:
        summary = call_ollama(prompt, max_tokens=200)
        if cache is not None:
            cache.set(cache_key, summary, expire=None)  # Never expire
        return summary
    except OllamaError as exc:
        logger.warning(f"Ollama summary failed for {file_path}: {exc}")
        return _fallback_summary(file_path, section, functions, classes)


def _fallback_summary(
    file_path: str, section: str, functions: list[str], classes: list[str]
) -> str:
    name = file_path.split("/")[-1]
    defines = ""
    if classes:
        defines = f"Contains: {', '.join(classes[:3])}."
    elif functions:
        defines = f"Provides: {', '.join(functions[:3])}."
    return f"{name} is a {section.lower()} module. {defines}"


def generate_all_summaries(
    file_nodes: list[dict],   # list of node attribute dicts from graph
    file_contents: dict[str, str],  # {file_path → raw content}
) -> dict[str, str]:
    """
    Generate AI summaries for all file nodes in batches.

    Args:
        file_nodes: list of dicts with keys: path, language, section,
                    raw_imports, functions, classes
        file_contents: mapping of file path to raw content string

    Returns:
        {file_path → ai_summary}
    """
    settings = get_settings()
    batch_size = settings.summary_batch_size
    batch_delay = settings.summary_batch_delay_ms / 1000.0

    cache = _get_cache()
    summaries: dict[str, str] = {}

    for i, node in enumerate(file_nodes):
        path = node["path"]
        content = file_contents.get(path, "")

        summary = generate_summary(
            file_path=path,
            language=node.get("language", "unknown"),
            section=node.get("section", "Backend"),
            imports=node.get("raw_imports", []),
            functions=node.get("functions", []),
            classes=node.get("classes", []),
            content=content,
            cache=cache,
        )
        summaries[path] = summary

        # Batch delay: pause after every `batch_size` files to avoid overloading Ollama
        if (i + 1) % batch_size == 0 and i + 1 < len(file_nodes):
            logger.debug(f"Batch {(i+1)//batch_size} complete. Pausing {batch_delay}s...")
            time.sleep(batch_delay)

    logger.info(f"Generated {len(summaries)} summaries.")
    return summaries
