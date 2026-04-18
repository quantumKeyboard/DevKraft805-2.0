"""
analysis/python_parser.py
AST-based import, function, and class extraction for Python (.py) files.
Resolves relative imports to absolute paths within the repository.
"""

import ast
import os
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class ParsedFile:
    """Parsed metadata from a single source file."""

    def __init__(
        self,
        file_path: str,
        imports: list[str],
        functions: list[str],
        classes: list[str],
        raw_imports: list[str],
    ):
        self.file_path = file_path
        self.imports = imports          # Resolved import paths (within repo)
        self.functions = functions       # Top-level function names
        self.classes = classes           # Top-level class names
        self.raw_imports = raw_imports   # Original import strings (for section classifier)

    def to_dict(self) -> dict:
        return {
            "file_path": self.file_path,
            "imports": self.imports,
            "functions": self.functions,
            "classes": self.classes,
            "raw_imports": self.raw_imports,
        }


def _resolve_relative_import(
    base_path: str,
    module: Optional[str],
    level: int,
    all_paths: set[str],
) -> Optional[str]:
    """
    Try to resolve a relative import to an absolute repo path.

    Args:
        base_path: the importing file's path (e.g. "src/auth/login.py")
        module: the module name in the import statement (may be None for `from . import x`)
        level: number of dots (relative level)
        all_paths: set of all known file paths in the repo

    Returns:
        Resolved path string if found in repo, else None
    """
    # Compute base directory accounting for dotted levels
    parts = base_path.replace("\\", "/").split("/")
    # Go up `level` directories from the file's directory
    base_parts = parts[:-1]  # strip filename
    for _ in range(level - 1):
        if base_parts:
            base_parts = base_parts[:-1]

    if module:
        module_parts = module.replace(".", "/")
        candidate_base = "/".join(base_parts + [module_parts])
    else:
        candidate_base = "/".join(base_parts)

    # Try candidate_base as a .py file or as a package __init__.py
    candidates = [
        candidate_base + ".py",
        candidate_base + "/__init__.py",
    ]
    for candidate in candidates:
        if candidate in all_paths:
            return candidate

    return None


def _resolve_absolute_import(module_str: str, all_paths: set[str]) -> Optional[str]:
    """
    Try to resolve an absolute import to a repo-internal file path.
    E.g. `from core.config import Settings` → "core/config.py"
    """
    parts = module_str.replace(".", "/")
    candidates = [
        parts + ".py",
        parts + "/__init__.py",
    ]
    for candidate in candidates:
        if candidate in all_paths:
            return candidate
    return None


def parse_python_file(file_path: str, content: str, all_paths: set[str]) -> ParsedFile:
    """
    Parse a Python source file and extract imports, functions, and classes.

    Args:
        file_path: relative path of the file within the repo
        content: raw source code string
        all_paths: set of all file paths in the repo (for import resolution)

    Returns:
        ParsedFile object
    """
    resolved_imports: list[str] = []
    raw_imports: list[str] = []
    functions: list[str] = []
    classes: list[str] = []

    try:
        tree = ast.parse(content, filename=file_path)
    except SyntaxError as exc:
        logger.debug(f"SyntaxError parsing {file_path}: {exc}")
        return ParsedFile(file_path, [], [], [], [])

    for node in ast.walk(tree):
        # --- Import statements ---
        if isinstance(node, ast.Import):
            for alias in node.names:
                raw_imports.append(alias.name)
                resolved = _resolve_absolute_import(alias.name, all_paths)
                if resolved:
                    resolved_imports.append(resolved)

        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            level = node.level or 0
            raw_imports.append(f"{'.' * level}{module}")

            if level > 0:
                # Relative import
                resolved = _resolve_relative_import(
                    file_path, module or None, level, all_paths
                )
            else:
                # Absolute import
                resolved = _resolve_absolute_import(module, all_paths)

            if resolved:
                resolved_imports.append(resolved)

        # --- Top-level function and class definitions ---
        elif isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef):
            # Only capture top-level (parent is the module)
            functions.append(node.name)

        elif isinstance(node, ast.ClassDef):
            classes.append(node.name)

    # Deduplicate
    resolved_imports = list(dict.fromkeys(resolved_imports))
    # Exclude self-imports
    resolved_imports = [p for p in resolved_imports if p != file_path]

    return ParsedFile(
        file_path=file_path,
        imports=resolved_imports,
        functions=functions,
        classes=classes,
        raw_imports=raw_imports,
    )
