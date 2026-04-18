# PROJECT MAP
# git-filter — Repository Architecture Navigator

> **Purpose of this file:** This is the single source of truth for the entire git-filter project. Every team member, contributor, and AI tool participating in building this platform must treat this file as the canonical reference. No module should be designed, no file should be created, and no decision should be made that contradicts what is written here. Where items are marked ⚠️ TBD, those are open decisions that must be resolved before the relevant module is built.

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Problem Statement](#2-problem-statement)
3. [Feature Registry](#3-feature-registry)
4. [Hackathon Execution Plan (24H)](#4-hackathon-execution-plan-24h)
5. [Technology Stack](#5-technology-stack)
6. [Architecture Overview](#6-architecture-overview)
7. [Project Folder Structure](#7-project-folder-structure)
8. [Module Specifications](#8-module-specifications)
   - 8.1 Ingestion Layer
   - 8.2 Static Analysis Engine
   - 8.3 Graph Construction Layer
   - 8.4 AI Intelligence Layer (Ollama)
   - 8.5 Commit History & Prediction Engine
   - 8.6 Onboarding Path Generator
   - 8.7 Voice Guide System (TinyTTS)
   - 8.8 Report Generation
   - 8.9 Stress Simulator
   - 8.10 NL Query Engine
   - 8.11 API Layer
   - 8.12 Frontend Dashboard
9. [Data Flow — End to End](#9-data-flow--end-to-end)
10. [Graph Node & Edge Specification](#10-graph-node--edge-specification)
11. [Language Support](#11-language-support)
12. [Filter & View System Specification](#12-filter--view-system-specification)
13. [Open Decisions (TBD)](#13-open-decisions-tbd)
14. [Infrastructure & Deployment](#14-infrastructure--deployment)

---

## 1. Project Overview

**git-filter** is a developer productivity web application that ingests a public GitHub repository URL, performs static code analysis across the entire codebase, and renders an interactive visual architecture graph that makes the system immediately understandable to any developer new to the codebase.

The system extracts module relationships, file dependencies, import chains, and data flow paths from source code — then presents this as a filterable, navigable graph where developers can click any node to explore its connections, read an AI-generated plain-language summary, and understand its role in the system. High-impact files that affect multiple services are visually highlighted to signal where changes carry the most risk.

Beyond the graph, git-filter generates a recommended onboarding path, analyzes commit history to surface architectural evolution and orphaned modules, supports natural language queries about the codebase, provides a voice-guided project walkthrough for immersive onboarding, generates reports for both technical and non-technical audiences, and includes a basic hardcoded stress simulator showing how components behave under load.

**Project name:** git-filter
**Deployment:** localhost (hackathon scope)
**LLM backend:** Ollama (local LLM)
**Time budget:** 24 hours

---

## 2. Problem Statement

Onboarding a new developer onto a large codebase is one of the most expensive and disruptive processes in software engineering. Without a structural map of the system, newcomers spend weeks manually tracing imports, reading hundreds of files, and repeatedly interrupting senior engineers just to understand how the pieces fit together.

git-filter solves this by automatically extracting and visualizing the true architecture of a codebase from the code itself — producing an interactive visual architecture graph, AI-generated component summaries, a recommended onboarding reading path, commit-history-backed predictions, natural language query support, and a voice-guided tour — all without requiring any login, CI integration, or codebase modification.

---

## 3. Feature Registry

Features are categorized into three tiers. The hackathon build targets all **[CORE]** features. **[ENHANCED]** features are built if time allows. **[FUTURE]** features are documented for roadmap awareness only.

### [CORE] Features — Must Ship in 24H

| # | Feature | Description |
|---|---------|-------------|
| C-01 | GitHub Repository Ingestion | Accept a public GitHub repo URL. Clone/fetch the repository tree via the GitHub Contents API. No auth required for public repos. |
| C-02 | Static Code Analysis | Parse source files to extract: import statements, function definitions, class declarations, exported symbols. Support Python, JavaScript, TypeScript, and Java. |
| C-03 | Interactive Architecture Graph | Render a force-directed, interactive graph of all files and their dependency relationships using React Flow + D3. Clickable nodes, zoomable, pannable. |
| C-04 | Section-Based Graph Filters | Auto-classify nodes into architectural sections (UI, Backend, Utils, Config, Tests, External Integrations). Filter graph to show only selected sections. |
| C-05 | Developer-Based Filter | Filter the graph to show only files authored or primarily modified by a selected developer (from commit history). |
| C-06 | Node Detail Panel | Click any node to open a side panel showing: AI-generated summary, file path, language, dependency list (in/out), last modified, contributor list, impact score. |
| C-07 | AI-Generated Summaries (Ollama) | For every file node, generate a plain-English explanation of the file's purpose using a local Ollama LLM, grounded in the actual file content and its import context. |
| C-08 | High-Impact File Highlighting | Compute PageRank-style centrality for each node. Files with centrality above the threshold are rendered with a distinct visual highlight (enlarged node, warning ring). |
| C-09 | Onboarding Path Generator | Produce an ordered reading list: entry points → core business logic → utilities → configs. Powered by topological sort + LLM re-ranking for business logic priority. |
| C-10 | Commit History Analysis | Use the GitHub Commits API to extract: commit frequency per file, commit authors, bug-fix commit detection (keyword: fix, bug, patch, hotfix), and architecture change markers. |
| C-11 | Commit-Based Prediction | Flag files that are statistically likely to change soon based on commit velocity and churn patterns. Shown as a "predicted hot zone" overlay on the graph. |
| C-12 | Orphaned Module Detection | Identify files with zero inbound edges (nothing imports them) that are not entry points or test files. Mark them as orphaned in the graph with a visual indicator. |
| C-13 | Natural Language Query | Accept queries like "where is authentication handled?" or "show the payment flow". Return a highlighted subgraph of matching nodes using keyword matching on AI summaries + file names. |
| C-14 | Voice Guide (TinyTTS) | Generate a spoken audio walkthrough of the project using TinyTTS. The voice guide reads: project overview, key modules, onboarding path, and top-risk files in sequence. |
| C-15 | Technical Report Generation | Generate a downloadable Markdown/HTML report: graph stats, component list with summaries, high-impact files, onboarding path, orphaned modules. |
| C-16 | Non-Technical Report Generation | Generate a plain-English report for non-technical stakeholders: what the project does, its key components in plain language, risk areas in business terms, and suggested action items. |
| C-17 | Stress Simulator (Hardcoded) | A pre-defined simulation showing how major architectural components behave under LOW / MEDIUM / HIGH / PEAK stress. Renders a resource graph with per-component CPU/memory/failure-probability values. |
| C-18 | Architecture Evolution Timeline | Show a timeline of how the graph evolved based on commit history: which files were added, removed, or heavily changed at each time period. |

### [ENHANCED] Features — Build If Time Allows

| # | Feature | Description |
|---|---------|-------------|
| E-01 | Entry Point Auto-Detection | Automatically identify and visually distinguish entry points (main.py, index.js, app.tsx, server.py, etc.) with a unique node shape. |
| E-02 | Subgraph Highlight for NL Queries | Instead of just filtering, draw a colored highlight overlay on the subgraph relevant to the NL query result — while keeping the rest of the graph visible and dimmed. |
| E-03 | Contributor Heatmap Overlay | Show a color overlay on the graph based on contributor activity per file — warmer colors = more contributors. |
| E-04 | Graph Export | Export the current graph view as a PNG image or as a JSON adjacency list. |
| E-05 | File Search | Fuzzy search box to locate and fly-to any node in the graph by filename. |

### [FUTURE] Features — Roadmap Only

| # | Feature | Description |
|---|---------|-------------|
| F-01 | Private Repo Support | GitHub OAuth flow for private repository access. |
| F-02 | Stress Simulator (Live) | Replace hardcoded stress simulator with a real queueing-theory-based computation engine using the extracted architecture graph. |
| F-03 | GitLab Support | Extend ingestion to support GitLab repository URLs. |
| F-04 | Multi-language NL Query (Semantic) | Replace keyword-based NL query with embedding-based semantic search using a local embedding model via Ollama. |
| F-05 | Webhook-Based Re-analysis | Trigger re-analysis automatically when a new commit is pushed to the repository. |

---

## 4. Hackathon Execution Plan (24H)

> This section exists specifically for the hackathon. It defines the build order and time allocation to ensure all [CORE] features are shipped within 24 hours. AI tools will be used for code generation throughout.

### Phase 1 — Foundation (Hours 0–5)

**Goal:** Repo ingested, graph data structure ready, basic graph rendered.

| Task | Time |
|------|------|
| Project scaffold: FastAPI backend + React frontend + folder structure | 45 min |
| GitHub Contents API integration: fetch file tree and raw file content | 60 min |
| Static analysis engine: import/dependency extraction for Python, JS/TS | 90 min |
| Graph data structure: nodes + edges in memory | 30 min |
| React Flow basic graph render (no styling, just nodes and edges visible) | 45 min |

**Phase 1 Exit Criteria:** A GitHub URL can be submitted and a raw dependency graph is visible in the browser.

---

### Phase 2 — Core Graph Features (Hours 5–10)

**Goal:** Filters, node detail, AI summaries, high-impact highlighting all working.

| Task | Time |
|------|------|
| Auto-classify nodes into sections (UI/Backend/Utils/Config/Tests/External) | 60 min |
| Section-based filter panel (checkboxes, live graph filter) | 45 min |
| GitHub Commits API integration: per-file commit data, author data | 60 min |
| Developer filter (dropdown of contributors, filter to their files) | 30 min |
| PageRank centrality computation: high-impact node detection | 45 min |
| Node detail side panel (click node → right panel opens) | 60 min |
| Ollama integration for AI summary generation (batched, with caching) | 60 min |

**Phase 2 Exit Criteria:** Graph is filterable, clickable, nodes have AI summaries, high-impact files are highlighted.

---

### Phase 3 — Intelligence Features (Hours 10–16)

**Goal:** Onboarding path, orphan detection, NL query, commit prediction, timeline.

| Task | Time |
|------|------|
| Topological sort for onboarding path generation | 45 min |
| Ollama re-ranking of onboarding path for business logic priority | 60 min |
| Orphaned module detection + visual indicator | 30 min |
| Commit history analysis: churn scoring, bug commit detection | 60 min |
| Commit-based prediction: hot zone scoring and graph overlay | 45 min |
| NL query: keyword + file-name matching against AI summaries | 60 min |
| Architecture evolution timeline component | 60 min |

**Phase 3 Exit Criteria:** Onboarding path displayed, orphans marked, NL query returns highlighted results, commit history integrated.

---

### Phase 4 — Distinctive Features (Hours 16–21)

**Goal:** Voice guide, reports, stress simulator, UI polish.

| Task | Time |
|------|------|
| TinyTTS voice guide: script generation + audio playback UI | 90 min |
| Technical report generation (Markdown + HTML download) | 60 min |
| Non-technical report generation (plain-English HTML download) | 60 min |
| Stress simulator: hardcoded data + slider UI + resource graph | 90 min |
| Frontend UI polish: color system, layout, graph styling, typography | 60 min |

**Phase 4 Exit Criteria:** Voice guide plays, both reports downloadable, stress simulator functional, UI looks presentable.

---

### Phase 5 — Buffer, Testing, and Demo Prep (Hours 21–24)

**Goal:** Everything works end-to-end on at least 2 real GitHub repos. Demo script ready.

| Task | Time |
|------|------|
| End-to-end test on 2 sample repos (e.g., a Python repo + a JS repo) | 45 min |
| Bug fixes from testing | 45 min |
| Demo script: write the walkthrough narrative | 30 min |
| README: setup + run instructions | 30 min |

---

## 5. Technology Stack

### Core Languages
- **Python 3.11+** — entire backend
- **TypeScript** — entire frontend

### Data Collection & Analysis
| Tool | Purpose |
|------|---------|
| GitHub REST API v3 (unauthenticated) | Fetch repository file tree, raw file content, commit history, contributor list |
| `requests` / `httpx` | HTTP client for GitHub API calls |
| `ast` (Python stdlib) | Python file AST parsing for import/function/class extraction |
| `tree-sitter` with JS/TS grammar | JavaScript and TypeScript AST parsing |
| `javalang` | Java source file parsing for import/class extraction |
| `gitpython` | Optional: local git clone for repos where API has rate limits |
| `pydriller` | Git history mining: commit frequency, churn, co-changes per file |

### AI / LLM
| Tool | Purpose |
|------|---------|
| Ollama (local) | LLM inference for AI-generated summaries, onboarding path re-ranking, NL query matching, report generation |
| `ollama` Python client | Python SDK for making calls to local Ollama API |
| Model: `llama3.2` or `mistral` | Primary model. Use whichever is available and fastest on the local machine. |
| TinyTTS | Text-to-speech voice guide generation. Converts the AI-generated project walkthrough script into audio. |

### Graph Infrastructure
| Tool | Purpose |
|------|---------|
| `networkx` | In-memory graph construction, PageRank centrality computation, topological sort, orphan detection |
| `scipy` | PageRank and graph metric computation support |

### Backend API
| Tool | Purpose |
|------|---------|
| FastAPI | REST API server |
| Pydantic | Data validation and schema definition |
| `uvicorn` | ASGI server for FastAPI |
| `python-dotenv` | Environment variable loading |
| `diskcache` or `functools.lru_cache` | Caching AI summary responses to avoid re-generating for the same file |

### Frontend
| Tool | Purpose |
|------|---------|
| React 18 + TypeScript | Dashboard UI |
| Vite | Build tool and dev server |
| React Flow | Primary interactive graph rendering (nodes, edges, zoom, pan, click events) |
| D3.js | Force simulation layout calculations fed into React Flow |
| Recharts | Commit history trend charts, timeline visualization |
| TailwindCSS | Styling |
| Zustand | State management (graph data, active filters, selected node) |
| `axios` | API client |

### Report Generation
| Tool | Purpose |
|------|---------|
| Jinja2 | HTML templating for both technical and non-technical reports |
| `markdown` (Python) | Convert Markdown report to HTML for download |
| `weasyprint` | (Optional) Convert HTML to PDF if time allows; otherwise serve HTML directly |

### Infrastructure
| Tool | Purpose |
|------|---------|
| `uvicorn` | Backend server (no Docker needed for hackathon localhost) |
| `npm` / `vite dev` | Frontend dev server |
| `.env` file | Configuration (Ollama URL, GitHub token if added, model name) |

---

## 6. Architecture Overview

```
┌─────────────────────────────────────────────────┐
│         USER (Browser — React Frontend)          │
│  Enters GitHub URL → Views Graph → Filters →    │
│  Clicks Nodes → Reads Reports → Plays Voice →   │
│  Types NL Queries → Uses Stress Simulator        │
└────────────────────────┬────────────────────────┘
                         │ HTTP (REST API)
┌────────────────────────▼────────────────────────┐
│              FASTAPI BACKEND                     │
│         (All computation happens here)           │
└────────────────────────┬────────────────────────┘
                         │
          ┌──────────────┼──────────────────────────┐
          │              │                           │
┌─────────▼──────┐ ┌─────▼──────────┐ ┌────────────▼────────┐
│  INGESTION     │ │ STATIC ANALYSIS│ │  GITHUB COMMIT API  │
│  GitHub API    │ │ ENGINE         │ │  (History + Authors)│
│  File Tree +   │ │ AST Parsing    │ │  PyDriller          │
│  Raw Content   │ │ Python/JS/TS/  │ │                     │
│                │ │ Java           │ │                     │
└─────────┬──────┘ └─────┬──────────┘ └────────────┬────────┘
          └──────────────┼──────────────────────────┘
                         │
┌────────────────────────▼────────────────────────┐
│           GRAPH CONSTRUCTION (NetworkX)          │
│  Nodes: Files   Edges: Dependencies/Imports     │
│  PageRank Centrality + Topological Sort         │
│  Orphan Detection + Section Classification      │
└────────────────────────┬────────────────────────┘
                         │
┌────────────────────────▼────────────────────────┐
│         AI INTELLIGENCE LAYER (Ollama)           │
│  File Summaries + Onboarding Path Re-ranking    │
│  NL Query Matching + Report Text Generation     │
│  Voice Guide Script Generation                  │
└────────────────────────┬────────────────────────┘
                         │
          ┌──────────────┼──────────────────────────┐
          │              │                           │
┌─────────▼──────┐ ┌─────▼──────────┐ ┌────────────▼────────┐
│ VOICE GUIDE    │ │ REPORT ENGINE  │ │  STRESS SIMULATOR   │
│ TinyTTS        │ │ Jinja2 HTML    │ │  (Hardcoded)        │
│ Audio Playback │ │ Technical +    │ │                     │
│                │ │ Non-Technical  │ │                     │
└────────────────┘ └────────────────┘ └─────────────────────┘
                         │
┌────────────────────────▼────────────────────────┐
│            API RESPONSE TO FRONTEND              │
│  Graph JSON + Summaries + Reports + Audio       │
└─────────────────────────────────────────────────┘
```

---

## 7. Project Folder Structure

Every file listed below must be created at the specified path. File names are final and must not be changed without updating this document.

```
git-filter/
├── PROJECT_MAP.md                              ← This file. Never edit without team agreement.
├── README.md                                   ← Setup and run instructions
├── .env.example                                ← Environment variable template
├── .gitignore
│
├── backend/
│   ├── main.py                                 ← FastAPI app entry point. Mounts all routers.
│   ├── requirements.txt                        ← All Python dependencies
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py                           ← App config: Ollama URL, model name, GitHub token, thresholds
│   │   └── constants.py                        ← Thresholds: centrality cutoff, orphan definition, section keywords
│   │
│   ├── ingestion/
│   │   ├── __init__.py
│   │   ├── github_fetcher.py                   ← GitHub Contents API: fetch file tree + raw file content
│   │   ├── repo_validator.py                   ← Validates GitHub URL format, checks repo is public
│   │   └── commit_fetcher.py                   ← GitHub Commits API: fetch per-file commit history, authors, messages
│   │
│   ├── analysis/
│   │   ├── __init__.py
│   │   ├── python_parser.py                    ← AST-based import/function/class extraction for .py files
│   │   ├── js_ts_parser.py                     ← tree-sitter-based import/export extraction for .js, .ts, .jsx, .tsx
│   │   ├── java_parser.py                      ← javalang-based import/class extraction for .java files
│   │   ├── section_classifier.py               ← Classifies each file into: UI / Backend / Utils / Config / Tests / External
│   │   ├── churn_analyzer.py                   ← Computes churn score per file from commit history (lines added + deleted)
│   │   ├── bug_commit_detector.py              ← Scans commit messages for: fix, bug, patch, hotfix, issue, revert
│   │   └── hot_zone_predictor.py               ← Scores each file's likelihood to change soon (churn velocity + bug commit ratio)
│   │
│   ├── graph/
│   │   ├── __init__.py
│   │   ├── builder.py                          ← Builds NetworkX DiGraph from parsed file data + dependencies
│   │   ├── centrality.py                       ← PageRank centrality computation. Flags nodes above HIGH_IMPACT_THRESHOLD.
│   │   ├── orphan_detector.py                  ← Finds nodes with 0 in-degree that are not entry points or test files
│   │   ├── onboarding_path.py                  ← Topological sort → LLM re-ranking → ordered file reading list
│   │   └── serializer.py                       ← Converts NetworkX graph to JSON format for frontend (nodes + edges arrays)
│   │
│   ├── ai/
│   │   ├── __init__.py
│   │   ├── ollama_client.py                    ← Wrapper for Ollama HTTP API calls. Handles retries and timeouts.
│   │   ├── summary_generator.py                ← Generates plain-English file summaries. Batches calls. Caches results.
│   │   ├── report_generator.py                 ← Generates technical and non-technical report text via Ollama
│   │   ├── nl_query_handler.py                 ← Processes natural language queries. Matches against summaries + file names.
│   │   └── voice_script_generator.py           ← Generates the voice guide script: project overview → key modules → risks
│   │
│   ├── voice/
│   │   ├── __init__.py
│   │   └── tts_runner.py                       ← Calls TinyTTS to convert voice guide script to audio. Returns audio file path.
│   │
│   ├── reports/
│   │   ├── __init__.py
│   │   ├── technical_report.py                 ← Assembles and renders technical report (Jinja2 → HTML)
│   │   ├── nontechnical_report.py              ← Assembles and renders non-technical report (Jinja2 → HTML)
│   │   └── templates/
│   │       ├── technical_report.html.j2        ← Jinja2 HTML template: graph stats, component table, risks, onboarding path
│   │       └── nontechnical_report.html.j2     ← Jinja2 HTML template: plain English, no file names, business-language risks
│   │
│   ├── stress_simulator/
│   │   ├── __init__.py
│   │   ├── stress_levels.py                    ← Defines 4 stress levels: LOW, MEDIUM, HIGH, PEAK with descriptions
│   │   ├── resource_graph.py                   ← Pre-defined resource allocation data per section per stress level
│   │   └── simulator.py                        ← Returns hardcoded simulation result for a given stress level
│   │
│   └── api/
│       ├── __init__.py
│       ├── routers/
│       │   ├── __init__.py
│       │   ├── analyze.py                      ← POST /analyze: accepts repo URL, triggers full analysis pipeline
│       │   ├── graph.py                        ← GET /graph/{repo_id}: returns graph JSON for frontend
│       │   ├── node.py                         ← GET /node/{repo_id}/{node_id}: returns full node detail including AI summary
│       │   ├── query.py                        ← POST /query: accepts NL query, returns matching node IDs
│       │   ├── onboarding.py                   ← GET /onboarding/{repo_id}: returns ordered onboarding path
│       │   ├── reports.py                      ← GET /reports/{repo_id}/technical, GET /reports/{repo_id}/nontechnical
│       │   ├── voice.py                        ← GET /voice/{repo_id}: returns audio file of voice guide
│       │   └── stress.py                       ← GET /stress/{level}: returns hardcoded stress simulation result
│       └── schemas/
│           ├── __init__.py
│           ├── analyze.py                      ← Pydantic: AnalyzeRequest (repo_url), AnalyzeResponse (repo_id, status)
│           ├── graph.py                        ← Pydantic: GraphNode, GraphEdge, GraphResponse
│           ├── node_detail.py                  ← Pydantic: NodeDetail (summary, deps, contributors, impact_score)
│           ├── query.py                        ← Pydantic: NLQueryRequest, NLQueryResponse (matching_node_ids, explanation)
│           └── report.py                       ← Pydantic: ReportResponse (html_content, generated_at)
│
├── frontend/
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.js
│   ├── vite.config.ts
│   ├── public/
│   │   └── favicon.ico
│   └── src/
│       ├── main.tsx                            ← React entry point
│       ├── App.tsx                             ← Root component, routing (react-router-dom)
│       │
│       ├── pages/
│       │   ├── LandingPage.tsx                 ← URL input form. Project name + tagline. Single CTA: "Analyze Repository"
│       │   ├── GraphPage.tsx                   ← Main graph view. Sidebar filters + graph canvas + node detail panel.
│       │   ├── OnboardingPage.tsx              ← Displays ordered onboarding path as a readable step-by-step guide.
│       │   ├── ReportsPage.tsx                 ← Toggle: Technical / Non-Technical report view + download buttons.
│       │   ├── StressSimulatorPage.tsx         ← Stress level selector + resource graph + component stress table.
│       │   └── TimelinePage.tsx                ← Architecture evolution timeline based on commit history.
│       │
│       ├── components/
│       │   ├── graph/
│       │   │   ├── ArchitectureGraph.tsx       ← React Flow canvas: renders nodes and edges, handles zoom/pan/click
│       │   │   ├── GraphNode.tsx               ← Custom React Flow node component: name, section badge, impact ring
│       │   │   ├── GraphEdge.tsx               ← Custom React Flow edge: directed arrow, colored by relationship type
│       │   │   ├── NodeDetailPanel.tsx         ← Right panel: AI summary, in/out deps, contributors, metrics, impact score
│       │   │   └── FilterPanel.tsx             ← Left panel: section checkboxes, developer dropdown, orphan toggle, hot zone toggle
│       │   ├── voice/
│       │   │   └── VoiceGuidePlayer.tsx        ← Audio player UI: play/pause, progress bar, current section label
│       │   ├── query/
│       │   │   └── NLQueryBar.tsx              ← Search bar at top of graph page for NL queries. Shows matched node count.
│       │   ├── stress/
│       │   │   ├── StressSlider.tsx            ← Stress level selector: LOW / MEDIUM / HIGH / PEAK
│       │   │   ├── ResourceGraph.tsx           ← Bar chart per section showing CPU/memory at selected stress level
│       │   │   └── StressTable.tsx             ← Table: component | CPU | Memory | Response Time | Failure Probability
│       │   ├── timeline/
│       │   │   └── EvolutionTimeline.tsx       ← Horizontal timeline with commit milestones. Click to see graph state at that point.
│       │   ├── onboarding/
│       │   │   └── OnboardingStepList.tsx      ← Ordered list of files. Each entry: step number, file name, AI summary, section badge.
│       │   └── shared/
│       │       ├── Navbar.tsx                  ← Top navigation: logo, page links, active repo name
│       │       ├── LoadingOverlay.tsx          ← Full-screen loading animation during analysis
│       │       ├── SectionBadge.tsx            ← Color-coded pill badge for node section (UI, Backend, etc.)
│       │       └── ImpactScoreBar.tsx          ← Visual bar showing impact score 0–100 with color gradient
│       │
│       ├── store/
│       │   ├── graphStore.ts                   ← Zustand: graph nodes/edges, selected node, active filters
│       │   ├── analysisStore.ts                ← Zustand: repo URL, analysis status, repo_id, summary stats
│       │   └── queryStore.ts                   ← Zustand: NL query text, query results (highlighted node IDs)
│       │
│       └── services/
│           ├── api.ts                          ← Axios instance + all API call functions
│           └── types.ts                        ← TypeScript types for all API response shapes
│
└── docs/
    ├── PROJECT_MAP.md                          ← Canonical copy of this file
    └── README.md                               ← Setup and run instructions (copied from root)
```

---

## 8. Module Specifications

### 8.1 Ingestion Layer

**Entry point:** `backend/ingestion/repo_validator.py` → `backend/ingestion/github_fetcher.py`

**`repo_validator.py`:**
- Validates that the URL matches `https://github.com/{owner}/{repo}` format
- Makes a HEAD request to confirm the repository is publicly accessible
- Returns: `{owner, repo, api_base_url}` or raises a validation error

**`github_fetcher.py`:**
- Uses GitHub Contents API: `GET /repos/{owner}/{repo}/git/trees/{branch}?recursive=1`
- Retrieves the full file tree in a single API call (recursive mode)
- Filters to supported extensions: `.py`, `.js`, `.ts`, `.jsx`, `.tsx`, `.java`
- For each file: fetches raw content via `GET /repos/{owner}/{repo}/contents/{path}`
- Rate limiting: uses unauthenticated requests (60/hour). If a GitHub token is in `.env`, uses it (5000/hour).
- Returns: list of `{path, content, language, size}` objects

**`commit_fetcher.py`:**
- Calls `GET /repos/{owner}/{repo}/commits` with `path` parameter per file
- For each file: fetches last 50 commits (paginated if needed)
- Extracts per commit: SHA, author name, author email, timestamp, commit message
- Returns: `{file_path → [commit_list]}` mapping

---

### 8.2 Static Analysis Engine

**`python_parser.py`:**
- Uses Python `ast` module to parse `.py` files
- Extracts: all `import` and `from X import Y` statements
- Extracts: all top-level function definitions (`def`) with name
- Extracts: all class definitions with name
- Resolves relative imports to absolute paths within the repo
- Returns: `{file_path, imports: [resolved_paths], functions: [names], classes: [names]}`

**`js_ts_parser.py`:**
- Uses `tree-sitter` with the `tree-sitter-javascript` and `tree-sitter-typescript` grammars
- Extracts: all `import` statements and `require()` calls
- Extracts: all `export` declarations (named and default)
- Extracts: function and class names
- Resolves relative imports to absolute repo paths using path join logic
- Handles `.js`, `.ts`, `.jsx`, `.tsx` files
- Returns same schema as `python_parser.py`

**`java_parser.py`:**
- Uses `javalang` library to parse `.java` files
- Extracts: `import` statements
- Extracts: class and interface names
- Returns same schema as `python_parser.py`

**`section_classifier.py`:**
- Rule-based classification. Each file is assigned exactly one section.
- Classification order (first match wins):

| Section | Rules |
|---------|-------|
| `Tests` | Path contains: `test`, `spec`, `__tests__`, filename starts with `test_` or ends with `.test.` or `.spec.` |
| `Config` | Filename matches: `config.*`, `settings.*`, `.env*`, `constants.*`, `*.config.js/ts` |
| `External` | Imports from >50% non-local (non-relative) packages. Or path contains `integrations`, `external`, `third_party` |
| `UI` | Path contains: `components`, `pages`, `views`, `screens`, `ui`, `frontend`. Or file is `.jsx`, `.tsx`. |
| `Utils` | Path contains: `utils`, `helpers`, `lib`, `common`, `shared`, `tools` |
| `Backend` | Everything else (default for `.py`, `.java`, unmatched `.ts` files) |

**`churn_analyzer.py`:**
- For each file: sums lines added + lines deleted across all commits in the commit list
- Computes churn rate: total churn / days in history window
- Normalizes to 0–100 churn score (min-max scaling across all files)
- Returns: `{file_path → churn_score}`

**`bug_commit_detector.py`:**
- For each file: scans its commit messages for keywords: `fix`, `bug`, `patch`, `hotfix`, `issue`, `revert`, `error`, `crash`
- Computes bug commit ratio: bug commits / total commits
- Returns: `{file_path → bug_commit_ratio}`

**`hot_zone_predictor.py`:**
- For each file: computes hot zone score = (churn_score × 0.6) + (bug_commit_ratio × 100 × 0.4)
- Files with hot zone score > `HOT_ZONE_THRESHOLD` (default: 65) are marked as predicted hot zones
- Returns: `{file_path → hot_zone_score, is_hot_zone: bool}`

---

### 8.3 Graph Construction Layer

**`builder.py`:**
- Creates a `networkx.DiGraph`
- **Nodes:** One node per source file. Attributes: `path`, `language`, `section`, `churn_score`, `bug_commit_ratio`, `hot_zone_score`, `is_hot_zone`, `functions`, `classes`, `contributor_count`, `last_modified`
- **Edges:** One directed edge per import relationship (`importer → imported`). Attribute: `type = "imports"`
- Additional edge types from commit co-changes: if two files appear together in > 3 commits, add edge with `type = "co_changes"`
- Only edges between files within the repository are included (no edges to external packages)

**`centrality.py`:**
- Runs `networkx.pagerank(G)` on the dependency graph
- Normalizes PageRank scores to 0–100 (impact score)
- Files with impact score > `HIGH_IMPACT_THRESHOLD` (default: 70) are flagged as high-impact
- Adds `impact_score` and `is_high_impact` attributes to each node

**`orphan_detector.py`:**
- Identifies nodes where: `in_degree == 0` AND `section != "Tests"` AND file is not a known entry point
- Entry point detection: filename matches `main.py`, `index.js`, `index.ts`, `app.py`, `app.tsx`, `server.py`, `server.ts`
- Marks identified nodes with `is_orphan = True`
- Returns: list of orphaned node paths

**`onboarding_path.py`:**
- Step 1: Compute topological sort of the dependency graph (only works if no cycles; uses DFS with cycle detection fallback)
- Step 2: Filter to most important nodes: entry points, high-impact nodes, and Backend section nodes
- Step 3: Send the top-20 node list to Ollama with instruction: "Given these files in topological order with their descriptions, produce an ordered onboarding reading path that prioritizes understanding core business logic before utilities and configs. Return a JSON array of file paths in your recommended order with a one-sentence reason for each."
- Step 4: Merge LLM order with remaining files (utilities, configs appended after)
- Returns: ordered list of `{file_path, section, reason, ai_summary_excerpt}`

**`serializer.py`:**
- Converts NetworkX graph to frontend-consumable JSON:
```json
{
  "nodes": [
    {
      "id": "src/auth/login.py",
      "label": "login.py",
      "section": "Backend",
      "impact_score": 82,
      "is_high_impact": true,
      "is_orphan": false,
      "is_hot_zone": true,
      "churn_score": 74,
      "language": "python",
      "contributors": ["alice", "bob"],
      "last_modified": "2024-11-15"
    }
  ],
  "edges": [
    {
      "id": "edge-001",
      "source": "src/auth/login.py",
      "target": "src/db/models.py",
      "type": "imports"
    }
  ]
}
```

---

### 8.4 AI Intelligence Layer (Ollama)

**`ollama_client.py`:**
- Wraps the Ollama HTTP API: `POST http://localhost:11434/api/generate`
- Accepts: model name, prompt, system prompt, max_tokens
- Handles timeouts (default: 30 seconds per request)
- Handles retry (up to 2 retries on timeout)
- Returns: response text string
- All calls are synchronous in the hackathon scope (async upgrade is future scope)

**`summary_generator.py`:**
- For each file node: constructs a prompt containing the file path, its language, its list of imports/classes/functions, and the first 200 lines of file content (truncated for large files)
- Prompt template:
  ```
  You are a senior software engineer explaining a codebase to a new developer.
  File: {file_path} (Language: {language}, Section: {section})
  Imports: {import_list}
  Defines: {functions_and_classes}
  Content preview:
  {content_preview}
  
  In 2-3 sentences, explain what this file does and its role in the system.
  Be concrete and specific. Do not use phrases like "this file" or "this module".
  ```
- Implements a disk-based cache: before calling Ollama, checks if a cached summary exists for the file's content hash. If yes, returns cached. If no, calls Ollama and caches the result.
- Batches calls: processes files in groups of 5, with 500ms delay between groups to avoid overloading Ollama

**`report_generator.py`:**
- Accepts: graph summary stats, high-impact file list, orphan list, onboarding path, hot zone list
- Generates two report text blocks via Ollama:
  1. **Technical summary text:** Written for engineers. Covers: what the system does architecturally, key entry points, riskiest files, dependency density, orphaned modules.
  2. **Non-technical summary text:** Written for non-engineers. Covers: what the software does in plain language, which parts are most critical to the business, which areas need attention and why (in business terms), recommended next steps.

**`nl_query_handler.py`:**
- Accepts: query string (e.g., "where is authentication handled?")
- Step 1: Extract keywords from query using simple tokenization (split, stopword removal)
- Step 2: Score every node: match score = (keyword matches in file path) × 2 + (keyword matches in AI summary) × 3 + (keyword matches in function/class names) × 2
- Step 3: Return top-N nodes (default: 10) sorted by match score
- Step 4: Send matched nodes to Ollama with prompt: "Given these files that matched the query '{query}', write 1 sentence explaining which file is the most likely answer and why."
- Returns: `{matching_node_ids: [...], explanation: "...", primary_match: node_id}`

**`voice_script_generator.py`:**
- Generates a structured voice guide script via Ollama with sections:
  1. **Introduction** (~100 words): What is this project? What problem does it solve?
  2. **Architecture Overview** (~150 words): How is the code organized? What are the main sections?
  3. **Core Components** (~200 words): Walk through the top 5 most important files with explanations
  4. **Onboarding Path** (~150 words): Read these files in this order. Here's why.
  5. **Risk Areas** (~100 words): These files are high-risk. Be careful when modifying them.
  6. **Closing** (~50 words): You're ready. Here's how to find your way around.
- Returns: list of `{section_title, script_text}` objects

---

### 8.5 Commit History & Prediction Engine

**Data source:** `commit_fetcher.py` output — per-file commit list.

**Architecture Evolution Timeline:**
- Groups commits by month using timestamp
- For each month, computes: files added (new files first appearing in commits), files with highest churn that month, new contributors
- Returns a timeline array: `[{month: "2024-01", files_added: [...], hottest_files: [...], contributors: [...]}]`
- Frontend `EvolutionTimeline.tsx` renders this as a horizontal scrollable timeline

**Prediction Logic (`hot_zone_predictor.py`):**
- Uses the last 90 days of commit data
- Computes **commit velocity** per file: commits in last 30 days vs. prior 30 days
- Files with velocity ratio > 2× are flagged as accelerating
- Combined hot zone score = velocity × churn × bug_commit_ratio (normalized)
- Files above threshold get `is_hot_zone = True`

---

### 8.6 Onboarding Path Generator

Full specification in Section 8.3 under `onboarding_path.py`.

**Frontend rendering (`OnboardingStepList.tsx`):**
- Displays as a numbered vertical list
- Each step: step number (large, colored), file path, section badge, AI summary (2-3 sentences), "Why read this now" reason from LLM
- Steps are grouped into 4 phases: Foundation → Core Logic → Services → Configuration
- A "Start Reading" button on each step opens the GitHub file URL in a new tab

---

### 8.7 Voice Guide System (TinyTTS)

**`tts_runner.py`:**
- Accepts: list of `{section_title, script_text}` from `voice_script_generator.py`
- For each section: calls TinyTTS to synthesize speech
- Concatenates audio segments into a single audio file (WAV or MP3)
- Saves to `backend/audio_cache/{repo_id}_voice_guide.mp3`
- Returns: file path

**`VoiceGuidePlayer.tsx`:**
- Displays as a floating player in the bottom-right corner of `GraphPage.tsx`
- Controls: Play / Pause, Skip to next section (section title shown), progress bar
- Fetches audio from `GET /voice/{repo_id}`
- Section markers are time-coded: clicking a section label jumps audio to that point

**Voice script tone:** Conversational, first-person perspective ("You're looking at a full-stack web application..."). Avoid technical jargon in the non-technical sections. Use it appropriately in the architecture overview sections.

---

### 8.8 Report Generation

**Technical Report (`technical_report.py` + `technical_report.html.j2`):**

Content:
1. Repository Overview: URL, language breakdown, total files analyzed, total dependencies mapped, analysis timestamp
2. Architecture Graph Statistics: total nodes, total edges, average in-degree, average out-degree, number of isolated components
3. Section Breakdown: table of node counts per section (UI, Backend, Utils, etc.)
4. High-Impact Files: table sorted by impact score — file path, section, impact score, dependency count, churn score
5. Orphaned Modules: list of orphaned files with reasons they are orphaned
6. Hot Zone Files (Predicted): list of files predicted to change soon with hot zone scores
7. Onboarding Path: numbered list of files with reasons
8. AI-Generated Technical Summary: 3-4 paragraph technical overview of the architecture
9. Commit History Summary: most active files, most active contributors, busiest months

**Non-Technical Report (`nontechnical_report.py` + `nontechnical_report.html.j2`):**

Content:
1. What This Software Does: 2-paragraph plain-English description
2. How It's Organized: brief description of the main sections with business-language analogies
3. Key Components: the 5 most important files described in business terms (no file paths, no code)
4. Risk Areas: 3 highest-risk files described as business risks (e.g., "The payment processing component has been changed frequently by multiple team members, increasing the risk of errors reaching customers")
5. Recommended Actions: 3-5 plain-language action items
6. Health at a Glance: simple score (High/Medium/Low health) with a one-paragraph explanation

Both reports are served as HTML (download button in frontend). WeasyPrint PDF conversion is attempted if installed; otherwise HTML download is the fallback.

---

### 8.9 Stress Simulator (Hardcoded)

> ⚠️ IMPORTANT: The Stress Simulator in git-filter is **hardcoded**. All simulation results are pre-defined and do not compute live values. This is a [FUTURE] feature for real computation (F-02).

**`stress_levels.py`:**

| Level | Name | Label | Description |
|-------|------|-------|-------------|
| 1 | LOW | Normal | Regular daily traffic. Baseline operation. |
| 2 | MEDIUM | Elevated | 5× baseline. Typical peak hours. |
| 3 | HIGH | Stressed | 20× baseline. Launch event or viral traffic. |
| 4 | PEAK | Critical | 50× baseline. Worst-case scenario. |

**`resource_graph.py`:**

Pre-defined resource allocation per section per stress level:

| Section | LOW CPU | MED CPU | HIGH CPU | PEAK CPU | LOW Mem | MED Mem | HIGH Mem | PEAK Mem |
|---------|---------|---------|----------|----------|---------|---------|----------|----------|
| Backend | 15% | 45% | 78% | 95% | 512MB | 1.2GB | 2.8GB | 4.5GB |
| UI | 5% | 12% | 22% | 35% | 128MB | 256MB | 512MB | 900MB |
| External | 8% | 20% | 40% | 65% | 256MB | 512MB | 1GB | 2GB |
| Utils | 3% | 8% | 15% | 25% | 64MB | 128MB | 256MB | 512MB |
| Config | 1% | 2% | 3% | 5% | 32MB | 32MB | 64MB | 64MB |

Failure probabilities per section per stress level:
- LOW: all sections 0–2%
- MEDIUM: Backend 5%, External 8%, others 1–3%
- HIGH: Backend 22%, External 35%, Utils 5%, UI 8%, Config 1%
- PEAK: Backend 60%, External 75%, Utils 15%, UI 22%, Config 3%

**`simulator.py`:** Returns the pre-defined data for the requested stress level. No computation performed.

---

### 8.10 NL Query Engine

Full specification in Section 8.4 under `nl_query_handler.py`.

**Frontend behavior (`NLQueryBar.tsx`):**
- Search bar at the top of `GraphPage.tsx`
- On submit: calls `POST /query` with the query string
- On response: highlights matching nodes in the graph (orange glow) and dims non-matching nodes
- Shows explanation text below the search bar
- A "Clear" button resets the graph to normal view

**Example queries that must work:**
- "where is authentication handled" → matches files with auth, login, token, jwt, session in names/summaries
- "show the payment flow" → matches files with payment, checkout, stripe, billing
- "where is the database connection" → matches files with db, database, connection, models, orm
- "what handles user registration" → matches files with register, signup, user creation

---

### 8.11 API Layer

All API routes are REST. Base path: `/api/v1/`

| Method | Path | Description |
|--------|------|-------------|
| POST | `/analyze` | Submit a GitHub URL for analysis. Returns `repo_id` and triggers full pipeline. |
| GET | `/graph/{repo_id}` | Returns full graph JSON (nodes + edges with all attributes). |
| GET | `/node/{repo_id}/{node_id}` | Returns full node detail: AI summary, in/out deps, contributors, metrics. |
| POST | `/query` | Accepts `{repo_id, query}`. Returns matching node IDs + explanation. |
| GET | `/onboarding/{repo_id}` | Returns ordered onboarding path with reasons. |
| GET | `/timeline/{repo_id}` | Returns architecture evolution timeline (monthly commits summary). |
| GET | `/reports/{repo_id}/technical` | Returns HTML content of technical report. |
| GET | `/reports/{repo_id}/nontechnical` | Returns HTML content of non-technical report. |
| GET | `/voice/{repo_id}` | Returns audio file (MP3) of voice guide. |
| GET | `/stress/{level}` | Returns hardcoded stress simulation for level 1–4. |

**Analysis pipeline flow (triggered by `POST /analyze`):**
- The pipeline runs synchronously in the hackathon scope (no Celery, no async queue)
- The frontend shows a loading overlay while polling `GET /graph/{repo_id}` until it returns 200
- Total expected analysis time: 2–5 minutes for a medium-sized repo (~50–200 files), depending on Ollama speed

---

### 8.12 Frontend Dashboard

**`LandingPage.tsx`:**
- Single input field: GitHub repository URL
- CTA button: "Analyze Repository"
- On submit: calls `POST /analyze`, stores `repo_id` in Zustand, navigates to `GraphPage`
- Shows a loading overlay with animated progress indicators during analysis

**`GraphPage.tsx`:**
- Main workspace. Three-column layout:
  - Left column (240px): `FilterPanel.tsx` — section toggles, developer dropdown, orphan toggle, hot zone toggle
  - Center (flex): `ArchitectureGraph.tsx` — the React Flow canvas
  - Right column (320px, conditionally shown): `NodeDetailPanel.tsx` — appears when a node is clicked
- Top bar: `NLQueryBar.tsx` + repo name + link to other pages
- Bottom-right floating: `VoiceGuidePlayer.tsx`

**`ArchitectureGraph.tsx`:**
- Uses React Flow for rendering and interaction
- Layout: D3 force simulation runs on the graph data, produces `{x, y}` positions, fed into React Flow as initial node positions
- Node visual encoding:
  - Color by section: UI=blue, Backend=green, Utils=gray, Config=yellow, Tests=purple, External=orange
  - Size by impact score: higher impact = larger node radius
  - High-impact ring: orange pulsing border on `is_high_impact` nodes
  - Orphan indicator: dashed border on `is_orphan` nodes
  - Hot zone indicator: red flame icon overlay on `is_hot_zone` nodes
  - NL query match: bright highlight (yellow glow) on matched nodes, dimmed opacity on non-matched

**`FilterPanel.tsx`:**
- Section filter: checkboxes for each section (all checked by default). Unchecking hides those nodes.
- Developer filter: dropdown of all contributor names. Selecting a developer shows only files where they are a contributor.
- Orphan toggle: show/hide orphaned nodes
- Hot zone toggle: show/hide predicted hot zones only (hides all non-hot-zone nodes)
- Reset button: restores all filters to default

**`NodeDetailPanel.tsx`:**
- Appears on node click. Shows:
  - File path (as breadcrumb)
  - Section badge + language badge
  - Impact score bar (0–100, color-coded)
  - AI-generated summary (2–3 sentences)
  - Depends on: list of outgoing edges (files this file imports)
  - Depended on by: list of incoming edges (files that import this file)
  - Contributors: list of author names and commit counts
  - Last modified date
  - Churn score + hot zone status
  - "View on GitHub" link (opens file in GitHub)

**`StressSimulatorPage.tsx`:**
- 4-button selector for stress levels: LOW / MEDIUM / HIGH / PEAK
- `ResourceGraph.tsx`: grouped bar chart per section (CPU, Memory side by side per section)
- `StressTable.tsx`: table with all sections + their metrics at the selected level
- Warning banners for sections exceeding 50% failure probability

**`TimelinePage.tsx`:**
- `EvolutionTimeline.tsx`: horizontal scrollable timeline of months
- Each month node shows: files added, hottest file that month, active contributors
- Clicking a month filters `GraphPage.tsx` to show files active in that period (cross-page filter via Zustand)

---

## 9. Data Flow — End to End

```
Step 1: User submits GitHub URL on LandingPage
        → POST /analyze {repo_url}
        → repo_validator.py validates URL
        → repo_id generated (hash of repo URL)
        → Analysis pipeline starts

Step 2: Ingestion
        → github_fetcher.py fetches file tree + raw content for all supported files
        → commit_fetcher.py fetches commit history per file

Step 3: Static Analysis
        → python_parser.py, js_ts_parser.py, java_parser.py parse each file
        → section_classifier.py assigns section to each file
        → churn_analyzer.py computes churn scores
        → bug_commit_detector.py computes bug commit ratios
        → hot_zone_predictor.py computes hot zone scores + flags

Step 4: Graph Construction
        → builder.py creates NetworkX DiGraph (nodes + import edges + co-change edges)
        → centrality.py computes PageRank impact scores
        → orphan_detector.py marks orphaned nodes
        → onboarding_path.py generates ordered reading list (topological sort + Ollama re-ranking)

Step 5: AI Summaries (Ollama)
        → summary_generator.py generates plain-English summary for each file node
        → Cache miss → Ollama API call → Cache hit on subsequent runs

Step 6: Voice Guide
        → voice_script_generator.py generates voice guide script via Ollama
        → tts_runner.py converts script to audio via TinyTTS
        → Audio file saved to disk

Step 7: Report Generation
        → report_generator.py generates technical + non-technical text via Ollama
        → technical_report.py renders HTML with Jinja2
        → nontechnical_report.py renders HTML with Jinja2

Step 8: Serialization
        → serializer.py converts NetworkX graph to frontend JSON
        → All data stored in memory (dict keyed by repo_id) for API serving

Step 9: API Response
        → GET /graph/{repo_id} → returns graph JSON
        → Frontend renders ArchitectureGraph.tsx
        → User interacts: filters, clicks, queries, plays voice guide, downloads reports
```

---

## 10. Graph Node & Edge Specification

### Node Attributes (full schema)

| Attribute | Type | Source | Description |
|-----------|------|--------|-------------|
| `id` | string | file path | Unique identifier (relative file path) |
| `label` | string | file path | Display name (filename only) |
| `path` | string | ingestion | Full relative path from repo root |
| `language` | string | file extension | `python`, `javascript`, `typescript`, `java` |
| `section` | string | section_classifier | `UI`, `Backend`, `Utils`, `Config`, `Tests`, `External` |
| `impact_score` | float | centrality.py | PageRank-based, normalized 0–100 |
| `is_high_impact` | bool | centrality.py | True if impact_score > HIGH_IMPACT_THRESHOLD (70) |
| `is_orphan` | bool | orphan_detector.py | True if in_degree == 0 and not entry point and not test |
| `churn_score` | float | churn_analyzer.py | Normalized 0–100 churn score |
| `bug_commit_ratio` | float | bug_commit_detector.py | Ratio 0–1 |
| `hot_zone_score` | float | hot_zone_predictor.py | Composite score 0–100 |
| `is_hot_zone` | bool | hot_zone_predictor.py | True if hot_zone_score > HOT_ZONE_THRESHOLD (65) |
| `functions` | list[str] | parser | Defined function names |
| `classes` | list[str] | parser | Defined class names |
| `contributors` | list[str] | commit_fetcher | Author names who have committed to this file |
| `contributor_count` | int | commit_fetcher | Number of unique contributors |
| `last_modified` | string | commit_fetcher | ISO timestamp of most recent commit to this file |
| `ai_summary` | string | summary_generator | LLM-generated plain-English description (populated asynchronously) |
| `x` | float | D3 force | X position for graph layout |
| `y` | float | D3 force | Y position for graph layout |

### Edge Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `id` | string | `{source}→{target}` |
| `source` | string | Source node id (importer) |
| `target` | string | Target node id (imported) |
| `type` | string | `imports` or `co_changes` |
| `weight` | int | Number of co-change occurrences (for `co_changes` edges only) |

---

## 11. Language Support

| Language | Extensions | Parser | Import Resolution |
|----------|-----------|--------|------------------|
| Python | `.py` | `ast` (stdlib) | Relative and absolute imports resolved within repo |
| JavaScript | `.js`, `.jsx` | `tree-sitter` + js grammar | ES module `import` + CommonJS `require()` |
| TypeScript | `.ts`, `.tsx` | `tree-sitter` + ts grammar | ES module `import` |
| Java | `.java` | `javalang` | Package-based import resolution |

Files in other languages (`.css`, `.html`, `.json`, `.md`, `.yaml`, etc.) are included as nodes if they are imported/referenced, but are not parsed for their own dependencies.

---

## 12. Filter & View System Specification

The filter system operates entirely client-side (in Zustand state + React Flow). Filters do not trigger new API calls — they operate on the already-loaded graph data.

### Active Filters State (Zustand `graphStore.ts`)

```typescript
interface GraphFilters {
  activeSections: string[];          // e.g., ["UI", "Backend", "Utils"] — shown sections
  selectedDeveloper: string | null;  // filter to one contributor's files
  showOrphansOnly: boolean;          // show only orphaned nodes
  showHotZonesOnly: boolean;         // show only hot zone nodes
  nlQueryHighlightIds: string[];     // node IDs highlighted by NL query
}
```

### Filter Application Logic

When any filter changes, `ArchitectureGraph.tsx` re-computes visible nodes:

```
visible_nodes = all_nodes
  .filter(n => activeSections.includes(n.section))
  .filter(n => selectedDeveloper === null OR n.contributors.includes(selectedDeveloper))
  .filter(n => !showOrphansOnly OR n.is_orphan)
  .filter(n => !showHotZonesOnly OR n.is_hot_zone)

visible_edges = all_edges
  .filter(e => visible_nodes.includes(e.source) AND visible_nodes.includes(e.target))
```

NL query highlighting is applied on top of the visible node set (does not hide nodes — only adds visual highlight).

---

## 13. Open Decisions (TBD)

| # | Decision | Module Affected | Options | Status |
|---|----------|----------------|---------|--------|
| TBD-01 | Ollama model to use | `ai/ollama_client.py` | `llama3.2` (faster, smaller) vs `mistral` (better reasoning). Decision based on what's available on the build machine. | Resolve at hackathon start |
| TBD-02 | Audio format for TinyTTS | `voice/tts_runner.py` | WAV (no encoding) vs MP3 (smaller, needs lame). Use WAV if lame not installed. | Resolve during Phase 4 |
| TBD-03 | Graph layout algorithm | `ArchitectureGraph.tsx` | D3 force-directed (most flexible) vs dagre (cleaner for DAGs). Use D3 force-directed as default; add dagre toggle if time allows. | Resolve during Phase 1 |
| TBD-04 | In-memory vs SQLite storage | `api/routers/analyze.py` | Pure in-memory dict (simpler, lost on restart) vs SQLite (persists across restarts). Use in-memory for hackathon. | Decided: in-memory |
| TBD-05 | GitHub API token | `core/config.py` | Optional: if a token is in `.env`, use it (5000 req/hr). If not, unauthenticated (60 req/hr). Large repos may hit the limit. | Document clearly in README |

---

## 14. Infrastructure & Deployment

**Hackathon deployment model:** localhost only. No Docker required. Two processes: backend + frontend.

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev  # Vite dev server on port 5173
```

### Ollama

```bash
ollama pull llama3.2     # or: ollama pull mistral
ollama serve             # runs on port 11434 by default
```

### `.env.example`

```env
# Ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2

# GitHub (optional — increases rate limit from 60 to 5000 req/hr)
GITHUB_API_TOKEN=

# Analysis Configuration
HIGH_IMPACT_THRESHOLD=70        # PageRank score above which a node is high-impact
HOT_ZONE_THRESHOLD=65           # Hot zone composite score threshold
SUMMARY_CACHE_DIR=./cache/summaries
AUDIO_CACHE_DIR=./cache/audio

# CORS (for local dev)
FRONTEND_ORIGIN=http://localhost:5173
```

### `requirements.txt` (backend)

```
fastapi
uvicorn[standard]
pydantic
httpx
requests
networkx
scipy
ast (stdlib — no install needed)
tree-sitter
tree-sitter-languages
javalang
pydriller
jinja2
python-dotenv
ollama
diskcache
markdown
weasyprint
TTS  # TinyTTS
```

### Minimum System Requirements

- 8GB RAM (for Ollama LLM inference)
- 4 CPU cores
- 10GB disk (for Ollama model + audio cache)
- Python 3.11+
- Node.js 18+
- Ollama installed and running

---

*End of PROJECT_MAP.md*

*Project: git-filter*
*Version: Hackathon MVP*
*Last updated: Initial planning phase.*
*This document must be kept in sync with any structural or design decisions made during development. No module should be built that contradicts this document without first updating it.*
