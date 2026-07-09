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

TruthStream is now an MVP backend foundation. It includes:

- A deterministic claim extraction pipeline.
- A pluggable evidence retrieval interface with an in-memory demo retriever.
- Evidence-weighted confidence scoring.
- A FastAPI service with `/health` and `/verify` endpoints.
- A CLI for local claim verification.
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
- `truthstream.evidence`: evidence retriever protocol and in-memory demo retriever.
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

Then verify text:

```bash
curl -X POST http://127.0.0.1:8000/verify \
  -H 'Content-Type: application/json' \
  -d '{"text":"Country X has banned AI systems."}'
```

### 5. Run the CLI

```bash
truthstream "Country X has banned AI systems."
```

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
    "explanation": "Confidence is 0% based on 0 supporting item(s) from 0 source(s) and 2 contradicting item(s) from 2 source(s)."
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
