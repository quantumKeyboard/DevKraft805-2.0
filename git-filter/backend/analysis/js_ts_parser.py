"""
analysis/js_ts_parser.py
tree-sitter-based import/export extraction for JavaScript and TypeScript files.
Handles .js, .ts, .jsx, .tsx files.
Falls back to regex-based parsing if tree-sitter is unavailable.
"""

import re
import os
import logging
from typing import Optional

logger = logging.getLogger(__name__)

# ─── tree-sitter Setup ────────────────────────────────────────────────────────

_TREE_SITTER_AVAILABLE = False
_js_parser = None
_ts_parser = None

try:
    from tree_sitter_languages import get_language, get_parser

    _js_language = get_language("javascript")
    _ts_language = get_language("typescript")
    _js_parser = get_parser("javascript")
    _ts_parser = get_parser("typescript")
    _TREE_SITTER_AVAILABLE = True
    logger.info("tree-sitter parsers loaded successfully.")
except Exception as exc:
    logger.warning(
        f"tree-sitter not available ({exc}). Falling back to regex-based JS/TS parsing."
    )

# ─── Regex Fallback ───────────────────────────────────────────────────────────

# Matches: import ... from 'path', import 'path'
_IMPORT_FROM_RE = re.compile(
    r"""(?:import|export)\s+(?:[\w*{},\s]+\s+from\s+)?['"]([^'"]+)['"]""",
    re.MULTILINE,
)
# Matches: require('path')
_REQUIRE_RE = re.compile(r"""require\s*\(\s*['"]([^'"]+)['"]\s*\)""")
# Matches: export function/class/const/var/let Name
_EXPORT_DECL_RE = re.compile(
    r"""export\s+(?:default\s+)?(?:function|class|const|let|var|async\s+function)\s+(\w+)"""
)
# Matches: function Name / class Name at top level
_FUNC_RE = re.compile(r"""^(?:export\s+)?(?:async\s+)?function\s+(\w+)\s*[(<]""", re.MULTILINE)
_CLASS_RE = re.compile(r"""^(?:export\s+)?(?:default\s+)?class\s+(\w+)""", re.MULTILINE)


def _resolve_js_import(
    base_path: str,
    import_path: str,
    all_paths: set[str],
) -> Optional[str]:
    """
    Resolve a JS/TS relative import path to an absolute repo path.
    Handles: ./foo, ../bar, etc.
    Skips bare module specifiers (no dot prefix) that are npm packages.
    """
    if not import_path.startswith("."):
        return None  # External npm package, not a repo file

    base_dir = "/".join(base_path.replace("\\", "/").split("/")[:-1])
    # Normalize the joined path
    joined = os.path.normpath(os.path.join(base_dir, import_path)).replace("\\", "/")

    # Try with various extensions and index files
    candidates = [
        joined,
        joined + ".js",
        joined + ".ts",
        joined + ".jsx",
        joined + ".tsx",
        joined + "/index.js",
        joined + "/index.ts",
        joined + "/index.jsx",
        joined + "/index.tsx",
    ]

    for candidate in candidates:
        if candidate in all_paths:
            return candidate

    return None


def _parse_with_regex(
    file_path: str, content: str, all_paths: set[str]
) -> tuple[list[str], list[str], list[str], list[str]]:
    """Regex-based fallback parser. Returns (resolved_imports, raw_imports, functions, classes)."""
    raw_imports: list[str] = []
    resolved_imports: list[str] = []
    functions: list[str] = []
    classes: list[str] = []

    for match in _IMPORT_FROM_RE.finditer(content):
        src = match.group(1)
        raw_imports.append(src)
        resolved = _resolve_js_import(file_path, src, all_paths)
        if resolved:
            resolved_imports.append(resolved)

    for match in _REQUIRE_RE.finditer(content):
        src = match.group(1)
        raw_imports.append(src)
        resolved = _resolve_js_import(file_path, src, all_paths)
        if resolved:
            resolved_imports.append(resolved)

    for match in _FUNC_RE.finditer(content):
        functions.append(match.group(1))

    for match in _CLASS_RE.finditer(content):
        classes.append(match.group(1))

    return (
        list(dict.fromkeys(resolved_imports)),
        list(dict.fromkeys(raw_imports)),
        list(dict.fromkeys(functions)),
        list(dict.fromkeys(classes)),
    )


def _parse_with_treesitter(
    file_path: str, content: str, all_paths: set[str], is_typescript: bool
) -> tuple[list[str], list[str], list[str], list[str]]:
    """tree-sitter-based parser."""
    parser = _ts_parser if is_typescript else _js_parser

    raw_imports: list[str] = []
    resolved_imports: list[str] = []
    functions: list[str] = []
    classes: list[str] = []

    try:
        tree = parser.parse(content.encode("utf-8"))
        root = tree.root_node

        def walk(node):
            if node.type in ("import_statement", "import_declaration"):
                # Extract the source string
                for child in node.children:
                    if child.type == "string":
                        src = child.text.decode("utf-8").strip("'\"")
                        raw_imports.append(src)
                        resolved = _resolve_js_import(file_path, src, all_paths)
                        if resolved:
                            resolved_imports.append(resolved)
                        break

            elif node.type == "call_expression":
                # require('path')
                func = node.child_by_field_name("function")
                args = node.child_by_field_name("arguments")
                if func and func.text == b"require" and args:
                    for arg in args.children:
                        if arg.type == "string":
                            src = arg.text.decode("utf-8").strip("'\"")
                            raw_imports.append(src)
                            resolved = _resolve_js_import(file_path, src, all_paths)
                            if resolved:
                                resolved_imports.append(resolved)

            elif node.type in ("function_declaration", "function_definition"):
                name_node = node.child_by_field_name("name")
                if name_node:
                    functions.append(name_node.text.decode("utf-8"))

            elif node.type == "class_declaration":
                name_node = node.child_by_field_name("name")
                if name_node:
                    classes.append(name_node.text.decode("utf-8"))

            for child in node.children:
                walk(child)

        walk(root)
    except Exception as exc:
        logger.debug(f"tree-sitter parse error for {file_path}: {exc}")

    return (
        list(dict.fromkeys(resolved_imports)),
        list(dict.fromkeys(raw_imports)),
        list(dict.fromkeys(functions)),
        list(dict.fromkeys(classes)),
    )


def parse_js_ts_file(
    file_path: str, content: str, all_paths: set[str]
) -> "ParsedFile":  # noqa: F821 — imported at runtime
    """
    Parse a JS/TS source file. Uses tree-sitter if available, falls back to regex.
    """
    from analysis.python_parser import ParsedFile  # Re-use same schema

    is_ts = file_path.endswith((".ts", ".tsx"))

    if _TREE_SITTER_AVAILABLE:
        resolved, raw, funcs, classes = _parse_with_treesitter(
            file_path, content, all_paths, is_ts
        )
    else:
        resolved, raw, funcs, classes = _parse_with_regex(file_path, content, all_paths)

    # Remove self-reference
    resolved = [p for p in resolved if p != file_path]

    return ParsedFile(
        file_path=file_path,
        imports=resolved,
        functions=funcs,
        classes=classes,
        raw_imports=raw,
    )
