# TruthStream Local Setup Guide

**Complete instructions to run TruthStream locally with backend, frontend, and all features working.**

## Prerequisites

- Python 3.11+
- Node.js 18+
- npm or yarn
- Git

## Quick Start (5 minutes)

### Backend Setup

```bash
# 1. Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 2. Install dependencies
pip install -e '.[dev]'

# 3. Run tests
pytest
ruff check .

# 4. Start API server
uvicorn truthstream.api:app --reload
```

Backend runs at: **http://127.0.0.1:8000**

Test health: `curl http://127.0.0.1:8000/health`

### Frontend Setup (New Terminal)

```bash
# 1. Navigate to frontend
cd frontend

# 2. Install dependencies
npm install

# 3. Start dev server
npm run dev
```

Frontend runs at: **http://127.0.0.1:5173**

## Verify Everything Works

### 1. Website Opens
- Open http://127.0.0.1:5173 in your browser
- You should see the TruthStream landing page

### 2. Home Page
- Displays tagline: "Verify claims with sources, confidence, and context."
- Has "Verify a claim" and "Learn how it works" buttons
- Shows example stats

### 3. Verify Page
- Click "Verify a claim" or navigate to Verify
- Input field accepts claim text
- Example: `"India banned AI systems"`
- Click "Verify claim"
- Backend returns results with confidence, evidence, status

### 4. Claim Verification
- Try: `"Country X has banned AI systems."`
- Expected: Confidence ~0%, status "likely_false", 2 contradicting evidence items
- Evidence shows: Official Government Registry, Trusted News Wire

### 5. Evidence Display
- Green cards for supporting evidence
- Red cards for contradicting evidence
- Blue cards for neutral evidence
- Each shows: title, snippet, source, credibility %, link

### 6. Confidence Meter
- Large percentage displayed (0-100%)
- Gradient bar from red → amber → green
- Status badge (Likely True, Mixed, Likely False, Insufficient Evidence)

### 7. Source Links
- Click "Open source ↗" on evidence cards
- Opens source in new tab (where applicable)

### 8. History Page
- Verify a claim first (enables history)
- Click "History" in nav
- Previous verification appears with timestamp
- Shows full result panel
- "Clear history" button works

### 9. Settings Page
- API base URL field: shows `/api` (proxy)
- Can change to direct backend URL (e.g., `http://127.0.0.1:8000`)
- Dark mode toggle: switches theme
- Save history toggle: controls local history
- Settings persist in localStorage

### 10. Dark Mode
- Default: enabled (dark background)
- Toggle in Settings
- All pages respect theme
- Text, cards, backgrounds adjust
- Smooth transition

### 11. Responsive Layout
- Resize browser window
- Mobile (< 640px): stacked layout
- Tablet (640-1024px): 2-column where applicable
- Desktop (> 1024px): full width
- Navigation wraps on mobile
- All buttons and inputs remain accessible

### 12. About Page
- Explains 4-step verification flow
- 1. Extract claims
- 2. Retrieve evidence
- 3. Score confidence
- 4. Show the work

## Troubleshooting

### Port Conflicts
- Backend port 8000 in use?
  ```bash
  uvicorn truthstream.api:app --reload --port 8001
  ```
- Frontend port 5173 in use?
  ```bash
  cd frontend && npm run dev -- --port 5174
  ```
- Update Settings page API URL to match new backend port

### Dependency Issues
- Python: `pip install --upgrade pip setuptools wheel`
- Node: `npm install` again, delete `node_modules/` and `.npm` cache
- TypeScript errors: `cd frontend && npm run build`

### API Connection Failed
- Verify backend is running: `curl http://127.0.0.1:8000/health`
- Check Settings page API URL is correct
- Check browser console (F12) for CORS errors
- Vite proxy should handle it automatically

### Build Errors
- Frontend TypeScript: `npm run build` shows all errors
- Backend: `pytest` validates all imports

## Advanced: Real Evidence Providers

Default mode uses deterministic demo evidence. Enable real providers (Wikipedia, Crossref, OpenAlex):

```bash
TRUTHSTREAM_EVIDENCE_MODE=real uvicorn truthstream.api:app --reload
```

Results will include real scholarly and encyclopedic evidence (slower, requires network).

## CLI Usage

```bash
# Basic verification
truthstream "India banned AI systems."

# Pretty-print output
truthstream --pretty "India banned AI systems."

# Real evidence mode
truthstream --evidence real --pretty "Recent AI research increased in 2024."

# Read from stdin
echo "Country X has banned AI systems." | truthstream --pretty
```

## Project Structure

```
Truthstream/
├── src/truthstream/          # Backend
│   ├── api.py               # FastAPI app
│   ├── cli.py               # CLI entrypoint
│   ├── pipeline.py          # Verification orchestration
│   ├── extraction.py        # Claim extraction
│   ├── evidence.py          # Retriever abstractions
│   ├── providers.py         # Real evidence providers
│   ├── scoring.py           # Confidence scoring
│   ├── models.py            # Domain models
│   └── settings.py          # Config
├── tests/                   # Backend tests
├── frontend/                # Frontend
│   ├── src/
│   │   ├── pages/          # React pages (Home, Verify, History, About, Settings)
│   │   ├── components/     # Reusable UI components
│   │   ├── lib/            # Utilities (API, storage, formatting)
│   │   ├── types/          # TypeScript types
│   │   └── styles.css      # Tailwind + custom CSS
│   ├── vite.config.ts      # Vite configuration + proxy
│   └── tailwind.config.js  # Tailwind theme
├── pyproject.toml           # Python dependencies and config
├── README.md                # Project overview
└── SETUP.md                 # This file
```

## Architecture Overview

```
Incoming Claim
       ↓
Frontend (React)
       ↓
  /verify API
       ↓
Verification Pipeline
       ├── Claim Extraction (heuristic)
       ├── Evidence Retrieval (demo or real providers)
       ├── Confidence Scoring (credibility + recency weighted)
       └── Explanation Generation
       ↓
 VerificationResult
       ↓
 API Response (JSON)
       ↓
Frontend Rendering
       ├── Confidence Meter
       ├── Evidence Cards
       ├── Source Links
       └── Explanation
       ↓
 User sees result
```

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/truthstream

# Run specific test
pytest tests/test_api.py::test_verify_endpoint

# Lint
ruff check .
ruff format src/ tests/
```

## Next Steps

1. Verify all 12 features above work
2. Try different claims to see how confidence changes
3. Enable real providers for more evidence
4. Explore the codebase architecture
5. Consider adding features (e.g., persistent database, auth, more providers)

## Support

If something breaks:
1. Check Prerequisites (Python 3.11+, Node 18+)
2. Delete virtual env and node_modules, reinstall
3. Run `pytest` and `npm run build` to catch errors
4. Check issue descriptions in the codebase
