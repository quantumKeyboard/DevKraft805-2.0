# git-filter — Hackathon Pitch Deck Content

---

## Slide 1 — Title

**git-filter**
> *Instantly understand any GitHub codebase.*

**Tagline:**
Paste a GitHub link. Get a living map of the code with AI explanations, onboarding paths, risk predictions, and a voice guide. In minutes.

**Event:** DevKraft 2.0 Hackathon | April 2026

---

## Slide 2 — The Problem

**Developers waste weeks just "figuring out" a codebase.**

- A new hire reads code for **2–4 weeks** before writing a single line
- Senior devs can't answer "what does this file do?" without reading it
- Dependency spaghetti is invisible until something breaks
- Code reviews guess at impact — they don't *know* it
- Non-technical stakeholders have zero visibility into technical risk

> "The most expensive code is code nobody understands."

---

## Slide 3 — The Solution

**git-filter is a repository architecture navigator.**

Paste any public GitHub URL and the system automatically produces:

- 🕸 **Interactive dependency graph** of every file
- 🤖 **AI-written plain-English summaries** per file
- 🗺 **Recommended reading order** for new developers
- 🔥 **Hot zone prediction** — which files are about to change
- 🎙 **Voice guide** that narrates the codebase to you
- ⚡ **Stress simulator** showing component risk under load
- 📄 **Downloadable reports** for both engineers and managers

*No installation. No code. Just a URL.*

---

## Slide 4 — How It Works

**10-step automated pipeline (runs in the background)**

```
GitHub URL
    1. Validate repo & detect default branch
    2. Fetch full file tree (Git Trees API)
    3. Fetch commit history per file
    4. Static analysis — extract imports, functions, classes
    5. Classify each file into architectural sections
       (UI / Backend / Utils / Config / Tests / External)
    6. Compute churn scores, bug-commit ratios, hot zones
    7. Build NetworkX dependency + co-change graph
    8. Generate AI summaries via Ollama (local LLM, cached)
    9. LLM-ranked onboarding reading path
   10. Voice script, HTML reports, stress simulation
           ↓
     Interactive graph appears in the UI
```

The result appears in the UI automatically — no refresh needed.

---

## Slide 5 — Features That Set It Apart

| Feature | git-filter | GitHub native | Code search tools |
|---------|-----------|---------------|-------------------|
| Interactive live dependency graph | ✅ | ❌ | ❌ |
| AI summary per file | ✅ | ❌ | ❌ |
| Onboarding reading path | ✅ | ❌ | ❌ |
| Hot zone prediction from commits | ✅ | ❌ | ❌ |
| Orphaned module detection | ✅ | ❌ | ❌ |
| Natural language search | ✅ | Limited | ❌ |
| Voice guide | ✅ | ❌ | ❌ |
| Non-technical stakeholder report | ✅ | ❌ | ❌ |
| Stress simulator | ✅ | ❌ | ❌ |
| Works on any public repo | ✅ | ✅ | Partial |

**We don't just show the code — we explain it.**

---

## Slide 6 — AI Intelligence

**Powered by a local Ollama LLM (llama3.2) — no API keys, no cloud cost.**

### File Summaries
- Every file gets a 2–3 sentence plain-English explanation
- Generated from: file path + imports + function names + code preview
- **Cached on disk** — never regenerated for unchanged files

### Natural Language Query
- Ask: *"Where is authentication handled?"*
- System extracts keywords → scores all nodes → LLM explains the top match
- Matching nodes **glow** on the graph, non-matches dim out

### Onboarding Path Re-ranking
- Topological sort gives a dependency-safe reading order
- LLM re-ranks it with reasons: *"Start here — this is the entry point for data flow"*
- Each step includes an AI-written justification

### Report Generation
- **Technical report:** architecture risk, centrality analysis, hot zones
- **Non-technical report:** plain English, business analogies, health score (High/Medium/Low)

### Voice Guide Script
- LLM writes 6 narration sections: Intro → Architecture → Core Files → Onboarding → Risks → Closing
- Delivered via browser Web Speech API — zero install required

---

## Slide 7 — Tech Stack

### Backend
| Component | Technology |
|-----------|------------|
| API Framework | **FastAPI** (Python) |
| Graph Engine | **NetworkX** (PageRank, topo sort) |
| AI / LLM | **Ollama** — llama3.2, runs locally |
| GitHub Ingestion | GitHub REST API (Git Trees API) |
| Python Parsing | `ast` (stdlib — zero deps) |
| JS/TS Parsing | `tree-sitter` + regex fallback |
| Java Parsing | `javalang` + regex fallback |
| Report Rendering | **Jinja2** HTML templates |
| AI Summary Cache | `diskcache` (content-hash keyed) |

### Frontend
| Component | Technology |
|-----------|------------|
| Framework | **React + Vite + TypeScript** |
| Graph Visualisation | **React Flow** |
| Physics Layout | **D3 force simulation** |
| Charts | **Recharts** |
| State Management | **Zustand** |
| Styling | **Tailwind CSS v4** |

### Architecture Decisions
- Background thread pipeline — no Celery or Redis needed
- Client-side filtering via Zustand — zero re-fetches on filter changes
- Fully local AI — no OpenAI/Anthropic cost

---

## Slide 8 — Live Demo

**Demo flow (3 minutes):**

1. Paste `https://github.com/pallets/flask` → hit Analyze
2. Watch the loading overlay step through all 10 pipeline stages
3. Interactive graph loads — coloured nodes by section, dependency edges
4. Click any node → AI summary, metrics, in/out dependency list, GitHub link
5. Type NL query: *"where are routes defined?"* → matching nodes glow
6. Toggle **Hot Zones Only** → risk files isolated on the canvas
7. **Onboarding page** → 4-phase reading path with LLM reasoning per step
8. **Reports page** → flip between technical and stakeholder views (download)
9. **Stress simulator** → switch to PEAK → External sections go critical
10. **Voice guide** → hit play → hear the codebase architecture narrated

*All of this from a single URL, with zero setup.*

---

## Slide 9 — Impact

### Why This Matters

| Metric | Data |
|--------|------|
| Avg. developer onboarding time | **2–4 weeks** |
| Time spent reading vs. writing code | **58% reading** (JetBrains 2023) |
| Avg. cost of a misunderstood dependency | **$1,500–$10,000** per bug |
| Codebases with up-to-date documentation | **< 30%** of projects |

### What git-filter Changes
- **Onboarding:** weeks → hours with a prioritised AI reading path
- **Documentation:** auto-generated from live code — always current
- **Risk detection:** flags hot zones and high-centrality files before disaster
- **Stakeholder bridge:** non-technical report with health score + action items
- **Cost:** fully local AI — $0 in LLM API fees

---

## Slide 10 — Summary & Roadmap

### Built in 24 hours
- ✅ Full-stack app: FastAPI backend + React/Vite frontend
- ✅ 10-step automated analysis pipeline (Python, JS, TS, Java)
- ✅ Interactive graph with D3 force layout
- ✅ 5 AI-powered features (summaries, NL query, onboarding, reports, voice)
- ✅ Stress simulator + commit timeline + downloadable HTML reports
- ✅ Works on any public GitHub repository — no setup

### Roadmap
- 🔜 Private repo support via GitHub OAuth
- 🔜 VS Code extension — live sidebar graph while you code
- 🔜 CI/CD webhook — graph auto-updates on every push
- 🔜 Shareable links + team annotations on graph nodes
- 🔜 Language expansion: Go, Rust, C#
- 🔜 PDF export of both reports

---

### Closing Line

> **git-filter turns any codebase from a black box into an open book.**
>
> *Understand it. Navigate it. Share it.*

---
*Built at DevKraft 2.0 | April 2026*
