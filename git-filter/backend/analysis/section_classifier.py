"""
analysis/section_classifier.py
Classifies each file into exactly one architectural section.
Order: Tests → Config → External → UI → Utils → Backend (default)
"""

import os
from core.constants import (
    TESTS_PATH_KEYWORDS, TESTS_FILENAME_PREFIXES, TESTS_FILENAME_SUFFIXES,
    CONFIG_FILENAMES_EXACT, CONFIG_FILENAME_PATTERNS,
    EXTERNAL_PATH_KEYWORDS, EXTERNAL_IMPORT_THRESHOLD,
    UI_PATH_KEYWORDS, UI_EXTENSIONS,
    UTILS_PATH_KEYWORDS,
)


def classify_section(
    file_path: str,
    raw_imports: list[str] | None = None,
) -> str:
    """
    Classify a file path into one of: Tests, Config, External, UI, Utils, Backend.

    Args:
        file_path: relative path of the file in the repo (forward slashes preferred)
        raw_imports: list of raw import strings for External classification

    Returns:
        Section name as a string
    """
    path = file_path.replace("\\", "/").lower()
    filename = os.path.basename(path)
    ext = os.path.splitext(filename)[1]
    path_parts = path.split("/")

    # ── 1. Tests ──────────────────────────────────────────────────────────────
    if any(kw in path_parts for kw in TESTS_PATH_KEYWORDS):
        return "Tests"
    if any(filename.startswith(pfix) for pfix in TESTS_FILENAME_PREFIXES):
        return "Tests"
    if any(sfx in filename for sfx in TESTS_FILENAME_SUFFIXES):
        return "Tests"

    # ── 2. Config ─────────────────────────────────────────────────────────────
    if filename in CONFIG_FILENAMES_EXACT:
        return "Config"
    if any(filename.startswith(pat) for pat in CONFIG_FILENAME_PATTERNS):
        return "Config"
    if any(pat in filename for pat in [".config.js", ".config.ts", ".config.mjs"]):
        return "Config"

    # ── 3. External ───────────────────────────────────────────────────────────
    if any(kw in path_parts for kw in EXTERNAL_PATH_KEYWORDS):
        return "External"
    if raw_imports:
        # >50% non-local (non-relative) imports → External
        non_local = [i for i in raw_imports if not i.startswith(".")]
        if raw_imports and len(non_local) / len(raw_imports) > EXTERNAL_IMPORT_THRESHOLD:
            return "External"

    # ── 4. UI ─────────────────────────────────────────────────────────────────
    if ext in UI_EXTENSIONS:
        return "UI"
    if any(kw in path_parts for kw in UI_PATH_KEYWORDS):
        return "UI"

    # ── 5. Utils ──────────────────────────────────────────────────────────────
    if any(kw in path_parts for kw in UTILS_PATH_KEYWORDS):
        return "Utils"

    # ── 6. Backend (default) ──────────────────────────────────────────────────
    return "Backend"
