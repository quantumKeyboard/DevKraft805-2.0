"""
graph/builder.py
Builds a NetworkX DiGraph from parsed file data.
Nodes: one per source file.
Edges: import relationships + commit co-change relationships.
"""

import logging
from collections import defaultdict

import networkx as nx

from core.constants import CO_CHANGE_MIN_OCCURRENCES

logger = logging.getLogger(__name__)


def build_graph(
    parsed_files: list,          # list[ParsedFile]
    commit_map: dict,            # {file_path → [CommitRecord]}
    churn_scores: dict,          # {file_path → float}
    bug_commit_ratios: dict,     # {file_path → float}
    hot_zone_results: dict,      # {file_path → HotZoneResult}
    section_map: dict,           # {file_path → section_str}
    language_map: dict,          # {file_path → language_str}
) -> nx.DiGraph:
    """
    Build and return the full dependency graph.

    Node attributes (per spec Section 10):
        path, language, section, churn_score, bug_commit_ratio,
        hot_zone_score, is_hot_zone, functions, classes,
        contributor_count, contributors, last_modified,
        ai_summary (empty until summary_generator runs)
        
    Edge types:
        "imports"    — static import relationship from parser
        "co_changes" — files that appear together in >CO_CHANGE_MIN_OCCURRENCES commits
    """
    G = nx.DiGraph()

    # ── Add Nodes ─────────────────────────────────────────────────────────────
    for pf in parsed_files:
        path = pf.file_path
        commits = commit_map.get(path, [])
        contributors = list(dict.fromkeys(c.author_name for c in commits if c.author_name))
        last_modified = commits[0].timestamp if commits else ""
        hot_zone = hot_zone_results.get(path)

        G.add_node(
            path,
            # Identification
            path=path,
            label=path.split("/")[-1],
            language=language_map.get(path, "unknown"),
            section=section_map.get(path, "Backend"),
            # Code metadata
            functions=pf.functions,
            classes=pf.classes,
            raw_imports=pf.raw_imports,
            # Commit-derived
            contributors=contributors,
            contributor_count=len(contributors),
            last_modified=last_modified,
            churn_score=churn_scores.get(path, 0.0),
            bug_commit_ratio=bug_commit_ratios.get(path, 0.0),
            # Hot zone
            hot_zone_score=hot_zone.hot_zone_score if hot_zone else 0.0,
            is_hot_zone=hot_zone.is_hot_zone if hot_zone else False,
            # Set by centrality.py later
            impact_score=0.0,
            is_high_impact=False,
            # Set by orphan_detector.py later
            is_orphan=False,
            # Set by summary_generator.py later
            ai_summary="",
        )

    # ── Add Import Edges ──────────────────────────────────────────────────────
    all_nodes = set(G.nodes)
    for pf in parsed_files:
        for dep_path in pf.imports:
            if dep_path in all_nodes and dep_path != pf.file_path:
                if not G.has_edge(pf.file_path, dep_path):
                    G.add_edge(
                        pf.file_path,
                        dep_path,
                        type="imports",
                        weight=1,
                    )

    # ── Add Co-change Edges ───────────────────────────────────────────────────
    # Build a map: commit_sha → set of files changed in that commit
    sha_to_files: dict[str, set[str]] = defaultdict(set)
    for file_path, commits in commit_map.items():
        if file_path not in all_nodes:
            continue
        for commit in commits:
            sha_to_files[commit.sha].add(file_path)

    # Count how many commits each file pair appears together in
    co_change_counts: dict[tuple[str, str], int] = defaultdict(int)
    for sha, files in sha_to_files.items():
        file_list = sorted(files)
        for i, f1 in enumerate(file_list):
            for f2 in file_list[i + 1:]:
                co_change_counts[(f1, f2)] += 1

    # Add co-change edges where count > threshold
    for (f1, f2), count in co_change_counts.items():
        if count >= CO_CHANGE_MIN_OCCURRENCES:
            # Add undirected by adding both directions, but only if import edge doesn't exist
            for src, tgt in [(f1, f2), (f2, f1)]:
                if not G.has_edge(src, tgt):
                    G.add_edge(src, tgt, type="co_changes", weight=count)

    logger.info(
        f"Graph built: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges "
        f"(import + co-change)"
    )
    return G
