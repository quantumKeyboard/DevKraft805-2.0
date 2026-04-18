"""
api/routers/analyze.py
POST /analyze — accepts a GitHub repo URL, runs the full analysis pipeline,
and stores results in the in-memory repo store.

The pipeline runs synchronously (no Celery) as per hackathon scope.
The frontend polls GET /graph/{repo_id} until results are available.
"""

import hashlib
import logging
import threading
import time
from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException, BackgroundTasks

from api.schemas.analyze import AnalyzeRequest, AnalyzeResponse
from ingestion.repo_validator import validate_github_url, RepoValidationError
from ingestion.github_fetcher import fetch_repository_files
from ingestion.commit_fetcher import fetch_all_file_commits, extract_timeline_data
from analysis.python_parser import parse_python_file
from analysis.js_ts_parser import parse_js_ts_file
from analysis.java_parser import parse_java_file
from analysis.section_classifier import classify_section
from analysis.churn_analyzer import compute_churn_scores, compute_churn_velocity
from analysis.bug_commit_detector import compute_bug_commit_ratios
from analysis.hot_zone_predictor import compute_hot_zones
from graph.builder import build_graph
from graph.centrality import compute_centrality
from graph.orphan_detector import detect_orphans
from graph.serializer import serialize_graph, serialize_graph_stats
from ai.summary_generator import generate_all_summaries
from ai.voice_script_generator import generate_voice_script
from ai.report_generator import generate_technical_summary, generate_nontechnical_summary
from voice.tts_runner import generate_voice_guide
from reports.technical_report import render_technical_report
from reports.nontechnical_report import render_nontechnical_report
from graph.onboarding_path import generate_onboarding_path

# In-memory storage — keyed by repo_id
# Structure per repo_id:
# {
#   "status": "running" | "complete" | "error",
#   "repo_url": str,
#   "owner": str,
#   "repo": str,
#   "graph": dict (serialized),
#   "stats": dict,
#   "onboarding": list[dict],
#   "timeline": list[dict],
#   "ai_summaries": dict[str, str],
#   "technical_report_html": str,
#   "nontechnical_report_html": str,
#   "voice_guide_path": str,
#   "error_message": str,
#   "started_at": str,
#   "completed_at": str,
# }
REPO_STORE: dict[str, dict] = {}

router = APIRouter(prefix="/analyze", tags=["analyze"])
logger = logging.getLogger(__name__)


def _make_repo_id(repo_url: str) -> str:
    return hashlib.sha256(repo_url.lower().strip().encode()).hexdigest()[:16]


def _run_pipeline(repo_id: str, repo_url: str):
    """
    Full analysis pipeline — runs in a background thread.
    Updates REPO_STORE[repo_id] with results or error.
    """
    store = REPO_STORE[repo_id]
    store["status"] = "running"

    try:
        logger.info(f"[{repo_id}] Pipeline starting for: {repo_url}")

        # ── Step 1: Validate & fetch ──────────────────────────────────────────
        store["status_detail"] = "Validating repository..."
        repo_info = validate_github_url(repo_url)
        owner = repo_info["owner"]
        repo = repo_info["repo"]
        branch = repo_info["default_branch"]
        store["owner"] = owner
        store["repo"] = repo

        store["status_detail"] = "Fetching file tree and content..."
        file_data_list = fetch_repository_files(owner, repo, branch)

        if not file_data_list:
            raise ValueError("No supported source files found in the repository.")

        file_contents: dict[str, str] = {f.path: f.content for f in file_data_list}
        all_paths = set(file_contents.keys())

        # ── Step 2: Commit history ────────────────────────────────────────────
        store["status_detail"] = "Fetching commit history..."
        commit_map = fetch_all_file_commits(owner, repo, list(all_paths))
        timeline_data = extract_timeline_data(commit_map)

        # ── Step 3: Static analysis ───────────────────────────────────────────
        store["status_detail"] = "Running static analysis..."
        parsed_files = []
        section_map: dict[str, str] = {}
        language_map: dict[str, str] = {}

        for fd in file_data_list:
            path = fd.path
            language_map[path] = fd.language

            if fd.language == "python":
                pf = parse_python_file(path, fd.content, all_paths)
            elif fd.language in ("javascript", "typescript"):
                pf = parse_js_ts_file(path, fd.content, all_paths)
            elif fd.language == "java":
                pf = parse_java_file(path, fd.content, all_paths)
            else:
                continue

            parsed_files.append(pf)
            section_map[path] = classify_section(path, pf.raw_imports)

        # ── Step 4: Churn & hot zone analysis ────────────────────────────────
        store["status_detail"] = "Analyzing commit patterns..."
        churn_scores = compute_churn_scores(commit_map)
        velocity_ratios = compute_churn_velocity(commit_map)
        bug_ratios = compute_bug_commit_ratios(commit_map)
        hot_zone_results = compute_hot_zones(churn_scores, bug_ratios, velocity_ratios)

        # ── Step 5: Build graph ───────────────────────────────────────────────
        store["status_detail"] = "Building dependency graph..."
        G = build_graph(
            parsed_files=parsed_files,
            commit_map=commit_map,
            churn_scores=churn_scores,
            bug_commit_ratios=bug_ratios,
            hot_zone_results=hot_zone_results,
            section_map=section_map,
            language_map=language_map,
        )
        G = compute_centrality(G)
        detect_orphans(G)

        # ── Step 6: AI Summaries ──────────────────────────────────────────────
        store["status_detail"] = "Generating AI summaries (this may take a few minutes)..."
        node_dicts = [
            {
                "path": n,
                "language": G.nodes[n].get("language", "unknown"),
                "section": G.nodes[n].get("section", "Backend"),
                "raw_imports": G.nodes[n].get("raw_imports", []),
                "functions": G.nodes[n].get("functions", []),
                "classes": G.nodes[n].get("classes", []),
            }
            for n in G.nodes
        ]
        ai_summaries = generate_all_summaries(node_dicts, file_contents)

        # Inject summaries into graph
        for path, summary in ai_summaries.items():
            if path in G.nodes:
                G.nodes[path]["ai_summary"] = summary

        # ── Step 7: Onboarding path ───────────────────────────────────────────
        store["status_detail"] = "Generating onboarding path..."
        onboarding = generate_onboarding_path(G, file_contents, ai_summaries)

        # ── Step 8: Serialize graph ───────────────────────────────────────────
        graph_json = serialize_graph(G)
        graph_stats = serialize_graph_stats(G)

        # ── Step 9: Voice guide ───────────────────────────────────────────────
        store["status_detail"] = "Generating voice guide..."
        high_impact_nodes = [
            n for n in graph_json["nodes"] if n["is_high_impact"]
        ]
        voice_script = generate_voice_script(
            repo_url=repo_url,
            graph_stats=graph_stats,
            high_impact_files=high_impact_nodes,
            onboarding_path=onboarding,
            ai_summaries=ai_summaries,
        )
        voice_path = generate_voice_guide(repo_id, voice_script)

        # ── Step 10: Reports ──────────────────────────────────────────────────
        store["status_detail"] = "Generating reports..."
        hot_zone_nodes = [n for n in graph_json["nodes"] if n["is_hot_zone"]]
        orphan_paths = [n["id"] for n in graph_json["nodes"] if n["is_orphan"]]

        tech_text = generate_technical_summary(
            repo_url, graph_stats, high_impact_nodes, orphan_paths, hot_zone_nodes, onboarding
        )
        nontech_text = generate_nontechnical_summary(
            repo_url, graph_stats, high_impact_nodes, hot_zone_nodes, ai_summaries
        )

        tech_html = render_technical_report(
            repo_url=repo_url,
            owner=owner,
            repo=repo,
            graph_stats=graph_stats,
            high_impact_nodes=high_impact_nodes,
            orphan_paths=orphan_paths,
            hot_zone_nodes=hot_zone_nodes,
            onboarding_path=onboarding,
            ai_summary_text=tech_text,
            commit_map=commit_map,
        )
        nontech_html = render_nontechnical_report(
            repo_url=repo_url,
            graph_stats=graph_stats,
            high_impact_nodes=high_impact_nodes,
            hot_zone_nodes=hot_zone_nodes,
            ai_summary_text=nontech_text,
        )

        # ── Store results ─────────────────────────────────────────────────────
        store.update({
            "status": "complete",
            "status_detail": "Analysis complete.",
            "graph": graph_json,
            "stats": graph_stats,
            "onboarding": onboarding,
            "timeline": timeline_data,
            "ai_summaries": ai_summaries,
            "technical_report_html": tech_html,
            "nontechnical_report_html": nontech_html,
            "voice_guide_path": voice_path,
            "voice_script": voice_script,
            "completed_at": datetime.now(timezone.utc).isoformat(),
        })
        logger.info(f"[{repo_id}] Pipeline complete.")

    except RepoValidationError as exc:
        store["status"] = "error"
        store["error_message"] = str(exc)
        logger.error(f"[{repo_id}] Validation error: {exc}")
    except Exception as exc:
        store["status"] = "error"
        store["error_message"] = f"Pipeline error: {exc}"
        logger.exception(f"[{repo_id}] Unexpected pipeline error")


@router.post("", response_model=AnalyzeResponse)
async def analyze_repository(request: AnalyzeRequest, background_tasks: BackgroundTasks):
    """
    Submit a GitHub repository URL for analysis.
    Returns immediately with a repo_id for polling.
    The pipeline runs in a background thread.
    """
    repo_url = request.repo_url.strip()
    repo_id = _make_repo_id(repo_url)

    existing = REPO_STORE.get(repo_id)
    if existing and existing.get("status") in ("running", "complete"):
        return AnalyzeResponse(
            repo_id=repo_id,
            status=existing["status"],
            message="Analysis already in progress or complete." if existing["status"] == "running"
                    else "Using cached analysis results.",
        )

    # Initialize store entry
    REPO_STORE[repo_id] = {
        "status": "queued",
        "status_detail": "Queued for analysis.",
        "repo_url": repo_url,
        "owner": "",
        "repo": "",
        "started_at": datetime.now(timezone.utc).isoformat(),
    }

    # Start pipeline in a background thread
    thread = threading.Thread(
        target=_run_pipeline,
        args=(repo_id, repo_url),
        daemon=True,
    )
    thread.start()

    return AnalyzeResponse(
        repo_id=repo_id,
        status="queued",
        message="Analysis started. Poll GET /graph/{repo_id} for results.",
    )


@router.get("/status/{repo_id}")
async def get_analysis_status(repo_id: str):
    """Get the current status and progress of an analysis."""
    store = REPO_STORE.get(repo_id)
    if not store:
        raise HTTPException(status_code=404, detail="Repo ID not found.")
    return {
        "repo_id": repo_id,
        "status": store.get("status"),
        "status_detail": store.get("status_detail", ""),
        "error_message": store.get("error_message", ""),
        "started_at": store.get("started_at", ""),
        "completed_at": store.get("completed_at", ""),
    }
