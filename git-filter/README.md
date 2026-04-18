# git-filter — Repository Architecture Navigator

> Instantly understand any public GitHub codebase through interactive dependency graphs, AI-generated summaries, onboarding paths, voice guides, and more.

## Prerequisites

| Requirement | Version |
|-------------|---------|
| Python | 3.11+ |
| Node.js | 18+ |
| Ollama | Latest |
| RAM | 8 GB minimum |

---

## Quick Start

### 1. Clone & enter the project

```bash
git clone <repo-url>
cd git-filter
```

### 2. Set up the backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # macOS/Linux

pip install -r requirements.txt

# Copy and configure the environment file
copy ..\\.env.example .env      # Windows  
# cp ../.env.example .env       # macOS/Linux
```

Edit `.env` and (optionally) add your GitHub API token:

```env
GITHUB_API_TOKEN=ghp_your_token_here
OLLAMA_MODEL=llama3.2
```

### 3. Start Ollama

```bash
ollama pull llama3.2    # or: ollama pull mistral
ollama serve            # runs on port 11434
```

### 4. Start the backend

```bash
# From the backend/ directory with venv active
uvicorn main:app --reload --port 8000
```

Visit [http://localhost:8000/docs](http://localhost:8000/docs) to verify the API is running.

### 5. Set up and start the frontend

```bash
cd ../frontend
npm install
npm run dev
```

Open [http://localhost:5173](http://localhost:5173) in your browser.

---

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/v1/analyze` | Submit GitHub URL for analysis |
| `GET` | `/api/v1/analyze/status/{repo_id}` | Poll analysis status |
| `GET` | `/api/v1/graph/{repo_id}` | Get full dependency graph |
| `GET` | `/api/v1/node/{repo_id}/{node_id}` | Get node detail with AI summary |
| `POST` | `/api/v1/query` | Natural language query |
| `GET` | `/api/v1/onboarding/{repo_id}` | Onboarding reading path |
| `GET` | `/api/v1/timeline/{repo_id}` | Architecture evolution timeline |
| `GET` | `/api/v1/reports/{repo_id}/technical` | Technical HTML report |
| `GET` | `/api/v1/reports/{repo_id}/nontechnical` | Non-technical HTML report |
| `GET` | `/api/v1/voice/{repo_id}` | Voice guide audio |
| `GET` | `/api/v1/stress/{level}` | Stress simulation (level 1–4) |
| `GET` | `/health` | Health check (Ollama status) |

---

## Configuration

All settings are in `backend/.env` (copy from `.env.example`):

| Variable | Default | Description |
|----------|---------|-------------|
| `OLLAMA_BASE_URL` | `http://localhost:11434` | Ollama server URL |
| `OLLAMA_MODEL` | `llama3.2` | LLM model to use |
| `GITHUB_API_TOKEN` | *(empty)* | Optional: raises rate limit from 60→5000 req/hr |
| `HIGH_IMPACT_THRESHOLD` | `70` | PageRank score above which a node is high-impact |
| `HOT_ZONE_THRESHOLD` | `65` | Composite score above which a node is a hot zone |

---

## Supported Languages

| Language | Extensions | Parser |
|----------|-----------|--------|
| Python | `.py` | `ast` (stdlib) |
| JavaScript | `.js`, `.jsx` | `tree-sitter` + regex fallback |
| TypeScript | `.ts`, `.tsx` | `tree-sitter` + regex fallback |
| Java | `.java` | `javalang` + regex fallback |

---

## Architecture

```
LandingPage (URL input)
  → POST /analyze → Background thread runs 10-step pipeline
  → Poll GET /analyze/status/{repo_id}
  → On complete: GET /graph/{repo_id}
  → GraphPage (3-column: FilterPanel | ArchitectureGraph | NodeDetailPanel)
  → Other pages: Onboarding, Timeline, Reports, Stress Simulator
```

---

## Notes

- **Rate limits**: Unauthenticated GitHub API = 60 requests/hour. Add a token for 5000/hr.
- **Analysis time**: 2–5 minutes for a medium repo (~100 files) depending on Ollama speed.
- **AI features**: Require Ollama running locally. The app degrades gracefully if Ollama is unavailable.
- **TTS**: Voice guide requires Coqui TTS (`pip install TTS`). Falls back to browser Web Speech API.
