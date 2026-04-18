"""
analysis/java_parser.py
javalang-based import and class extraction for Java (.java) files.
"""

import logging
from typing import Optional

logger = logging.getLogger(__name__)

_JAVALANG_AVAILABLE = False
try:
    import javalang
    _JAVALANG_AVAILABLE = True
except ImportError:
    logger.warning("javalang not installed. Java file parsing will be skipped.")


def _import_to_path(import_str: str, all_paths: set[str]) -> Optional[str]:
    """
    Try to resolve a Java import like com.myapp.service.UserService
    to a file path like src/main/java/com/myapp/service/UserService.java
    found in all_paths.
    """
    parts = import_str.replace(".", "/")
    # Try exact match / suffix match
    for path in all_paths:
        if path.endswith(parts + ".java"):
            return path
    # Try just the class name at any depth
    class_name = import_str.split(".")[-1]
    if class_name and class_name[0].isupper():
        for path in all_paths:
            if path.endswith(f"/{class_name}.java") or path.endswith(f"\\{class_name}.java"):
                return path
    return None


def parse_java_file(
    file_path: str, content: str, all_paths: set[str]
) -> "ParsedFile":  # noqa: F821
    """
    Parse a Java source file and extract imports and class names.
    Falls back to regex-based extraction if javalang is unavailable.
    """
    from analysis.python_parser import ParsedFile

    resolved_imports: list[str] = []
    raw_imports: list[str] = []
    functions: list[str] = []
    classes: list[str] = []

    if _JAVALANG_AVAILABLE:
        try:
            tree = javalang.parse.parse(content)

            for imp in tree.imports:
                raw_imports.append(imp.path)
                resolved = _import_to_path(imp.path, all_paths)
                if resolved:
                    resolved_imports.append(resolved)

            for _, node in tree.filter(javalang.tree.ClassDeclaration):
                classes.append(node.name)
            for _, node in tree.filter(javalang.tree.InterfaceDeclaration):
                classes.append(node.name)
            for _, node in tree.filter(javalang.tree.MethodDeclaration):
                functions.append(node.name)

        except Exception as exc:
            logger.debug(f"javalang parse error for {file_path}: {exc}")
            # Fall through to regex below
    
    if not _JAVALANG_AVAILABLE or (not raw_imports and not classes):
        # Regex fallback
        import re
        for match in re.finditer(r"^import\s+([\w.]+);", content, re.MULTILINE):
            imp = match.group(1)
            raw_imports.append(imp)
            resolved = _import_to_path(imp, all_paths)
            if resolved:
                resolved_imports.append(resolved)

        for match in re.finditer(r"(?:public\s+)?(?:class|interface|enum)\s+(\w+)", content):
            classes.append(match.group(1))

        for match in re.finditer(
            r"(?:public|private|protected|static|\s)+[\w<>\[\]]+\s+(\w+)\s*\(", content
        ):
            functions.append(match.group(1))

    return ParsedFile(
        file_path=file_path,
        imports=list(dict.fromkeys(p for p in resolved_imports if p != file_path)),
        functions=list(dict.fromkeys(functions)),
        classes=list(dict.fromkeys(classes)),
        raw_imports=list(dict.fromkeys(raw_imports)),
    )
