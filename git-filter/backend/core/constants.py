"""
core/constants.py
All thresholds, section keywords, and hard-coded constants.
"""

# ─── Section Classification Rules ────────────────────────────────────────────

# Path segments / filename patterns that identify each section.
# Order matters: first match wins (see section_classifier.py).

TESTS_PATH_KEYWORDS = ["test", "spec", "__tests__", "tests"]
TESTS_FILENAME_PREFIXES = ["test_"]
TESTS_FILENAME_SUFFIXES = [".test.", ".spec."]

CONFIG_FILENAMES_EXACT = {
    "config.py", "settings.py", "constants.py",
    "config.js", "config.ts", "settings.js",
    "constants.js", "constants.ts",
}
CONFIG_FILENAME_PATTERNS = [
    "config.", "settings.", ".env", "constants.",
    ".config.js", ".config.ts",
]

EXTERNAL_PATH_KEYWORDS = ["integrations", "external", "third_party", "vendors", "adapters"]
EXTERNAL_IMPORT_THRESHOLD = 0.5  # >50% non-local imports → External

UI_PATH_KEYWORDS = ["components", "pages", "views", "screens", "ui", "frontend"]
UI_EXTENSIONS = {".jsx", ".tsx"}

UTILS_PATH_KEYWORDS = ["utils", "helpers", "lib", "common", "shared", "tools"]

# ─── Entry Points ─────────────────────────────────────────────────────────────

ENTRY_POINT_FILENAMES = {
    "main.py", "index.js", "index.ts", "app.py",
    "app.tsx", "server.py", "server.ts", "index.jsx",
    "manage.py",  # Django
}

# ─── Bug Commit Keywords ──────────────────────────────────────────────────────

BUG_COMMIT_KEYWORDS = ["fix", "bug", "patch", "hotfix", "issue", "revert", "error", "crash"]

# ─── Hot Zone Prediction ──────────────────────────────────────────────────────

HOT_ZONE_CHURN_WEIGHT = 0.6
HOT_ZONE_BUG_WEIGHT = 0.4
HOT_ZONE_VELOCITY_LOOKBACK_DAYS = 90
HOT_ZONE_VELOCITY_WINDOW_DAYS = 30
HOT_ZONE_VELOCITY_ACCELERATION_RATIO = 2.0  # commits in last 30d / prior 30d

# ─── Graph ────────────────────────────────────────────────────────────────────

CO_CHANGE_MIN_OCCURRENCES = 3  # min shared commits to create a co_change edge
ONBOARDING_PATH_TOP_N = 20     # nodes sent to LLM for re-ranking
NL_QUERY_TOP_N = 10            # top N nodes returned for NL queries

# ─── Language Extensions ──────────────────────────────────────────────────────

SUPPORTED_EXTENSIONS = {".py", ".js", ".ts", ".jsx", ".tsx", ".java"}

EXTENSION_TO_LANGUAGE = {
    ".py": "python",
    ".js": "javascript",
    ".jsx": "javascript",
    ".ts": "typescript",
    ".tsx": "typescript",
    ".java": "java",
}

# ─── GitHub API ───────────────────────────────────────────────────────────────

GITHUB_API_BASE = "https://api.github.com"
GITHUB_MAX_COMMITS_PER_FILE = 50
GITHUB_DEFAULT_BRANCH_CANDIDATES = ["main", "master", "develop"]
