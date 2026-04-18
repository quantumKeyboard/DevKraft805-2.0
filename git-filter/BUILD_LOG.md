# git-filter — Build Progress Log

> **Purpose:** This file tracks the implementation status of every module, component, and feature in the git-filter project. Future AI tools and contributors should read this file before making changes to understand what's done, what's in progress, and what still needs building.

---

## Legend

| Symbol | Meaning |
|--------|---------|
| ✅ | Fully implemented |
| 🔶 | Partially implemented (notes below) |
| ❌ | Not yet implemented |
| 🔧 | Needs integration/wiring |

---

## Build Sessions

### Session 1 — 2026-04-18 (Initial Base Build)

**Goal:** Create the complete project skeleton, implement all hard-to-build backend logic, and set up the full frontend architecture.

---

## Backend Status

### `core/`
| File | Status | Notes |
|------|--------|-------|
| `config.py` | ✅ | Pydantic Settings, all env vars, LRU cache singleton |
| `constants.py` | ✅ | Section rules, entry points, bug keywords, language extensions |

### `ingestion/`
| File | Status | Notes |
|------|--------|-------|
| `repo_validator.py` | ✅ | Regex URL parse, HEAD check, default branch detection |
| `github_fetcher.py` | ✅ | Git Trees API (recursive), base64 decode, rate limit courtesy sleep |
| `commit_fetcher.py` | ✅ | Per-file commit fetch, pagination, timeline grouping |

### `analysis/`
| File | Status | Notes |
|------|--------|-------|
| `python_parser.py` | ✅ | Full AST walk, relative + absolute import resolution |
| `js_ts_parser.py` | ✅ | tree-sitter (primary) + regex fallback; handles .js/.ts/.jsx/.tsx |
| `java_parser.py` | ✅ | javalang (primary) + regex fallback |
| `section_classifier.py` | ✅ | First-match-wins rules: Tests→Config→External→UI→Utils→Backend |
| `churn_analyzer.py` | ✅ | Commit-count proxy + min-max normalization + velocity computation |
| `bug_commit_detector.py` | ✅ | Keyword scan against commit messages |
| `hot_zone_predictor.py` | ✅ | Composite formula (churn×0.6 + bug×0.4) + velocity acceleration bonus |

### `graph/`
| File | Status | Notes |
|------|--------|-------|
| `builder.py` | ✅ | NetworkX DiGraph, import edges + co-change edges |
| `centrality.py` | ✅ | PageRank + min-max normalization + degree centrality fallback |
| `orphan_detector.py` | ✅ | in_degree==0, not entry point, not test |
| `onboarding_path.py` | ✅ | Topological sort + LLM re-ranking + impact-score fallback |
| `serializer.py` | ✅ | Full node/edge JSON + graph stats computation |

### `ai/`
| File | Status | Notes |
|------|--------|-------|
| `ollama_client.py` | ✅ | HTTP wrapper, timeout/retry, health check, model list |
| `summary_generator.py` | ✅ | Disk cache (diskcache), batched 5 files, 500ms delay, fallback |
| `nl_query_handler.py` | ✅ | Stop-word removal, weighted scoring (path×2/summary×3/defines×2), LLM explanation |
| `report_generator.py` | ✅ | Technical + non-technical summary text via Ollama |
| `voice_script_generator.py` | ✅ | 6-section script (Intro/Architecture/Components/Onboarding/Risks/Closing) |

### `voice/`
| File | Status | Notes |
|------|--------|-------|
| `tts_runner.py` | ✅ | Coqui TTS WAV generation + concatenation; .txt fallback when not installed |

### `reports/`
| File | Status | Notes |
|------|--------|-------|
| `technical_report.py` | ✅ | Jinja2 render with full context |
| `nontechnical_report.py` | ✅ | Jinja2 render + automated health scoring |
| `templates/technical_report.html.j2` | ✅ | Full HTML report with tables, badges, impact scores |
| `templates/nontechnical_report.html.j2` | ✅ | Plain-English stakeholder report |

### `stress_simulator/`
| File | Status | Notes |
|------|--------|-------|
| `stress_levels.py` | ✅ | 4 levels with metadata |
| `resource_graph.py` | ✅ | Hardcoded per-section per-level resource data (exact spec values) |
| `simulator.py` | ✅ | Returns assembled result with is_critical/is_warning flags |

### `api/routers/`
| File | Status | Notes |
|------|--------|-------|
| `analyze.py` | ✅ | Full 10-step pipeline in background thread, REPO_STORE, status polling |
| `graph.py` | ✅ | Graph JSON with status check |
| `node.py` | ✅ | Node detail + GitHub URL |
| `query.py` | ✅ | NL query delegation |
| `onboarding.py` | ✅ | Returns onboarding path |
| `reports.py` | ✅ | Technical + non-technical HTML |
| `voice.py` | ✅ | Audio file or JSON script fallback |
| `stress.py` | ✅ | Level 1–4 simulation |
| `timeline.py` | ✅ | Monthly timeline data |

### `api/schemas/`
| File | Status | Notes |
|------|--------|-------|
| `analyze.py` | ✅ | AnalyzeRequest + AnalyzeResponse |
| `graph.py` | ✅ | GraphNode, GraphEdge, GraphResponse |
| `node_detail.py` | ✅ | NodeDetail with ContributorInfo |
| `query.py` | ✅ | NLQueryRequest + NLQueryResponse |
| `report.py` | ✅ | ReportResponse |

### `main.py`
| Status | Notes |
|--------|-------|
| ✅ | All routers mounted, CORS configured, health check endpoint |

---

## Frontend Status

### `services/`
| File | Status | Notes |
|------|--------|-------|
| `types.ts` | ✅ | All API response shapes as TypeScript interfaces |
| `api.ts` | ✅ | Axios client with typed functions for all endpoints |

### `store/`
| File | Status | Notes |
|------|--------|-------|
| `graphStore.ts` | ✅ | Zustand: nodes/edges/stats, filters, client-side filter application |
| `analysisStore.ts` | ✅ | Zustand: repo URL/ID/owner, status |
| `queryStore.ts` | ✅ | Zustand: NL query text, result IDs, loading |

### `components/graph/`
| File | Status | Notes |
|------|--------|-------|
| `ArchitectureGraph.tsx` | ✅ | React Flow + D3 force layout, all visual encodings, legend panel |
| `NodeDetailPanel.tsx` | ✅ | Full detail panel: AI summary, deps, metrics grid, contributors, GitHub link |
| `FilterPanel.tsx` | ✅ | Section toggles, developer dropdown, orphan/hot-zone toggles, stats summary |

### `components/query/`
| File | Status | Notes |
|------|--------|-------|
| `NLQueryBar.tsx` | ✅ | Search input, submit, results summary, clear button |

### `components/voice/`
| File | Status | Notes |
|------|--------|-------|
| `VoiceGuidePlayer.tsx` | ✅ | Floating player, Web Speech API fallback, section navigation |

### `components/stress/`
| File | Status | Notes |
|------|--------|-------|
| `StressSlider.tsx` | ✅ | 4 colored level buttons |
| `ResourceGraph.tsx` | ✅ | Recharts grouped bar chart |
| `StressTable.tsx` | ✅ | Metrics table with color-coded status badges |

### `components/timeline/`
| File | Status | Notes |
|------|--------|-------|
| `EvolutionTimeline.tsx` | ✅ | Horizontal scrollable bar chart with hover tooltips |

### `components/onboarding/`
| File | Status | Notes |
|------|--------|-------|
| `OnboardingStepList.tsx` | ✅ | 4-phase grouped list with step numbers and GitHub links |

### `components/shared/`
| File | Status | Notes |
|------|--------|-------|
| `Navbar.tsx` | ✅ | Logo, repo breadcrumb, page nav links |
| `LoadingOverlay.tsx` | ✅ | Full-screen loader with step tracker + progress bar |
| `SectionBadge.tsx` | ✅ | Color-coded section pill |
| `ImpactScoreBar.tsx` | ✅ | Gradient progress bar 0–100 |

### `pages/`
| File | Status | Notes |
|------|--------|-------|
| `LandingPage.tsx` | ✅ | URL input, polling, example repos, feature grid |
| `GraphPage.tsx` | ✅ | 3-column layout + voice guide integration |
| `OnboardingPage.tsx` | ✅ | Fetches + displays onboarding path |
| `ReportsPage.tsx` | ✅ | Tab toggle + iframe preview + download |
| `StressSimulatorPage.tsx` | ✅ | Level selector + banners + chart + table |
| `TimelinePage.tsx` | ✅ | Timeline chart + month detail panel |

### Config files
| File | Status | Notes |
|------|--------|-------|
| `tailwind.config.js` | ✅ | Section color tokens |
| `postcss.config.js` | ✅ | Tailwind + autoprefixer |
| `vite.config.ts` | ✅ | React plugin + proxy to :8000 |
| `index.css` | ✅ | Inter font, dark scrollbars, React Flow overrides |
| `App.tsx` | ✅ | BrowserRouter + all routes |
| `main.tsx` | ✅ | React 18 entry point |

---

## Features vs. PROJECT_MAP

### [CORE] Features

| ID | Feature | Status | Notes |
|----|---------|--------|-------|
| C-01 | GitHub Repository Ingestion | ✅ | github_fetcher.py + repo_validator.py |
| C-02 | Static Code Analysis | ✅ | Python/JS/TS/Java parsers implemented |
| C-03 | Interactive Architecture Graph | ✅ | React Flow + D3 force layout |
| C-04 | Section-Based Graph Filters | ✅ | Client-side in graphStore.ts |
| C-05 | Developer-Based Filter | ✅ | Contributor dropdown in FilterPanel |
| C-06 | Node Detail Panel | ✅ | NodeDetailPanel.tsx |
| C-07 | AI-Generated Summaries (Ollama) | ✅ | summary_generator.py with disk cache |
| C-08 | High-Impact File Highlighting | ✅ | PageRank + orange pulsing ring |
| C-09 | Onboarding Path Generator | ✅ | Topo sort + LLM re-ranking |
| C-10 | Commit History Analysis | ✅ | commit_fetcher.py |
| C-11 | Commit-Based Prediction | ✅ | hot_zone_predictor.py + graph overlay |
| C-12 | Orphaned Module Detection | ✅ | orphan_detector.py + dashed border |
| C-13 | Natural Language Query | ✅ | nl_query_handler.py + NLQueryBar |
| C-14 | Voice Guide (TinyTTS) | ✅ | tts_runner.py + Web Speech fallback |
| C-15 | Technical Report | ✅ | Jinja2 HTML report |
| C-16 | Non-Technical Report | ✅ | Jinja2 plain-English report |
| C-17 | Stress Simulator (Hardcoded) | ✅ | simulator.py + StressSimulatorPage |
| C-18 | Architecture Evolution Timeline | ✅ | commit_fetcher + EvolutionTimeline |

### [ENHANCED] Features

| ID | Feature | Status | Notes |
|----|---------|--------|-------|
| E-01 | Entry Point Auto-Detection | 🔶 | Detected in orphan_detector.py; no distinct visual shape yet |
| E-02 | Subgraph Highlight for NL Queries | ✅ | Dim non-matching nodes + glow on matches |
| E-03 | Contributor Heatmap Overlay | ❌ | Not yet implemented |
| E-04 | Graph Export | ❌ | Not yet implemented |
| E-05 | File Search | ❌ | Not yet implemented |

---

## What Still Needs Work (Todo List)

### High Priority (for hackathon demo)
- [ ] **Tailwind CSS**: Run `npx tailwindcss init` or confirm PostCSS is wired correctly in the Vite build
- [ ] **Install packages**: Run `pip install -r requirements.txt` in backend venv
- [ ] **Test end-to-end** with a small Python repo (e.g. `https://github.com/pallets/flask`)
- [ ] **Verify Ollama** is running and the configured model is pulled

### Medium Priority
- [ ] **E-01 Entry point node shape**: Add a distinct diamond/star shape to React Flow for entry point nodes
- [ ] **E-04 Graph Export**: Add a PNG export button (React Flow has a built-in `getViewport` + canvas method)
- [ ] **E-05 File Search**: Add fuzzy search input in FilterPanel that flies to the matching node
- [ ] **GraphEdge.tsx**: Custom edge component (currently using React Flow defaults)
- [ ] **GraphNode.tsx**: Custom node component with flame icon for hot zones

### Low Priority / Nice to Have
- [ ] **E-03 Contributor Heatmap**: Color overlay based on contributor_count
- [ ] **Timeline → Graph cross-filter**: Click a timeline month to filter GraphPage to files active that month (Zustand cross-store action needed)
- [ ] **PDF export**: WeasyPrint integration for report PDF download
- [ ] **Async pipeline**: Convert to Celery or FastAPI BackgroundTasks fully async for better UX

---

## Known Issues / Gotchas

1. **tree-sitter**: On Windows, `tree-sitter-languages` may need Visual C++ build tools. If install fails, the JS/TS parser automatically falls back to regex.
2. **Coqui TTS**: Very large install (~2GB). If not installed, the app uses browser Web Speech API instead.
3. **GitHub rate limit**: Unauthenticated = 60 req/hr. Large repos with many files will hit this quickly. Always add a `GITHUB_API_TOKEN` to `.env` for serious use.
4. **Ollama timeout**: For very large repos with 200+ files, AI summary generation can take 10–30 minutes. The `OLLAMA_TIMEOUT` can be increased in `.env`.
5. **React Flow peer deps**: Installed with `--legacy-peer-deps` due to React 18 compatibility. This is safe.
6. **In-memory store**: All analysis results are lost on backend restart. This is by design (hackathon scope).

---

*Last updated: 2026-04-18 (Session 1 — Initial Build)*
*Next session should start from the "What Still Needs Work" section above.*
