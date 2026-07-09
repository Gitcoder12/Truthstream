# TruthStream

**Real-time claim verification and evidence analysis for streaming information.**

TruthStream continuously monitors incoming information streams, extracts factual claims,
gathers supporting and contradicting evidence from trusted sources, and generates confidence
scores with transparent explanations.

Instead of asking:

> "Is this true?"

TruthStream asks:

> "What evidence supports this claim, and how strong is that evidence?"

## Current State

TruthStream is now an MVP product foundation. It includes:

- A deterministic claim extraction pipeline.
- A pluggable evidence retrieval interface with demo and real provider modes.
- Real evidence providers for Wikipedia, Crossref, and OpenAlex with in-memory request caching.
- Evidence-weighted confidence scoring with structured evidence summaries.
- A FastAPI service with `/health`, `/verify`, and `/verify/batch` endpoints.
- A CLI for local claim verification with JSON, stdin, and pretty-print output modes.
- A React + TypeScript + Tailwind frontend with Home, Verify, History, About, and Settings pages.
- Automated tests for the core pipeline and API.

The MVP intentionally avoids external model or search dependencies so it can run locally and in CI.
Future implementations can replace the extractor and retriever with NLP models, search APIs,
stream processors, and persistent storage without changing the public API contract.

## Why TruthStream?

Information spreads faster than verification.

News articles, social media posts, blogs, and public announcements can reach millions of people
before fact-checkers have time to investigate. TruthStream helps bridge this gap by providing
automated, evidence-based verification for information as it appears.

## MVP Architecture

```text
Incoming Text
    ↓
Claim Extraction
    ↓
Evidence Retrieval
    ↓
Confidence Scoring
    ↓
Explanation Generation
    ↓
API / CLI Output
```

Core modules:

- `truthstream.extraction`: deterministic claim and entity extraction heuristics.
- `truthstream.evidence`: retriever protocols, composite retrieval, and demo fallback retriever.
- `truthstream.providers`: cached Wikipedia, Crossref, and OpenAlex provider integrations.
- `truthstream.settings`: runtime selection for demo or real evidence modes.
- `truthstream.scoring`: source-credibility and recency weighted confidence scoring.
- `truthstream.pipeline`: orchestration layer that composes extraction, retrieval, scoring, and explanation.
- `truthstream.api`: FastAPI application.
- `truthstream.cli`: command-line entrypoint.

## Quickstart

### 1. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -e '.[dev]'
```

### 3. Run tests

```bash
pytest
ruff check .
```

### 4. Run the API

```bash
uvicorn truthstream.api:app --reload
```

By default the API uses deterministic demo evidence for offline development. To enable real
Wikipedia, Crossref, and OpenAlex providers, set:

```bash
TRUTHSTREAM_EVIDENCE_MODE=real uvicorn truthstream.api:app --reload
```

Then verify text:

```bash
curl -X POST http://127.0.0.1:8000/verify \
  -H 'Content-Type: application/json' \
  -d '{"text":"Country X has banned AI systems."}'
```

Batch verification is also available:

```bash
curl -X POST http://127.0.0.1:8000/verify/batch \
  -H 'Content-Type: application/json' \
  -d '[{"text":"Country X has banned AI systems."},{"text":"The moon has a new public library."}]'
```

### 5. Run the frontend

```bash
cd frontend
npm install
npm run dev
```

Open http://127.0.0.1:5173. The Vite dev server proxies `/api` requests to the FastAPI backend by default.

### 6. Run the CLI

```bash
truthstream "Country X has banned AI systems."
truthstream --pretty "Country X has banned AI systems."
truthstream --evidence real --pretty "Recent research on multilingual misinformation is rising."
echo "Country X has banned AI systems." | truthstream --pretty
```

## Frontend

The frontend lives in `frontend/` and is built with React, TypeScript, Vite, and Tailwind CSS.
It connects to the existing backend API instead of replacing it. The Verify page posts claims to
`/verify`, displays loading and error states, renders a confidence meter, separates supporting,
contradicting, and neutral evidence, links to sources, and stores optional local history.

## Evidence Provider System

TruthStream now separates retrieval orchestration from source-specific integrations:

- `EvidenceProvider` defines the provider contract.
- `CachedEvidenceProvider` adds TTL caching around any provider.
- `CompositeEvidenceRetriever` queries multiple providers and keeps working if one provider fails.
- `WikipediaEvidenceProvider` retrieves encyclopedia search results.
- `CrossrefEvidenceProvider` retrieves scholarly work metadata.
- `OpenAlexEvidenceProvider` retrieves open scholarly graph results.

Remote provider evidence is returned as neutral evidence candidates. This keeps retrieval
deterministic and leaves support/contradiction classification to the verification/ranking layer.
The original in-memory retriever remains available for tests, demos, and offline development.

## Example API Response

```json
[
  {
    "claim": {
      "text": "Country X has banned AI systems.",
      "entities": ["Country X", "AI"]
    },
    "confidence_score": 0.0,
    "status": "likely_false",
    "supporting_evidence": [],
    "contradicting_evidence": [
      {
        "source": {
          "name": "Official Government Registry",
          "url": null,
          "credibility": 0.95
        },
        "title": "No nationwide AI ban has been issued",
        "snippet": "The registry lists AI safety guidance but no blanket ban on AI systems.",
        "stance": "contradicts",
        "recency_score": 1.0
      }
    ],
    "neutral_evidence": [],
    "explanation": "Confidence is 0% with stronger contradicting evidence, based on 0 supporting item(s) from 0 source(s) and 2 contradicting item(s) from 2 source(s).",
    "evidence_summary": {
      "supporting_count": 0,
      "contradicting_count": 2,
      "neutral_count": 0,
      "supporting_weight": 0,
      "contradicting_weight": 1.724
    }
  }
]
```

## Long-Term Vision

TruthStream is not designed to determine absolute truth. Its goal is to provide transparent,
evidence-based confidence assessments by continuously analyzing information from multiple
independent sources.

Planned capabilities include:

- Multi-language verification.
- Real-time misinformation alerts.
- Stream ingestion using Kafka or equivalent event queues.
- Knowledge graph integration.
- Cross-source contradiction detection.
- Source credibility learning.
- Public API and dashboard.
- Browser extension.
- Research paper support.

## License

MIT License
