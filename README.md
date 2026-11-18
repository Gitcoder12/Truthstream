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


---

## AI-maintained project notes (secondary — 2026-11-13)

This section supplements the maintainer-authored README above; it does not replace or certify original claims.

- The current source tree, runtime data and executed tests are the implementation source of truth. Roadmap items and draft PRs are not shipped functionality.
- Preserve real and maintainer-provided data. Never silently substitute generated or placeholder records; clearly label and isolate synthetic fixtures.
- Mark unverifiable sources, metrics and external claims as unknown/unverified rather than guessing.
- Verify commands, tests and public claims against the exact current commit before using this project in a job, research or academic application.
- See [MODEL_AUDIT_ROUTER.md](MODEL_AUDIT_ROUTER.md) for independent model review and the merge gate.


### Proposed provider and frontend work — open PR, not yet merged (2026-11-13)

[PR #2](https://github.com/Gitcoder12/Truthstream/pull/2) proposes Wikipedia, Crossref and OpenAlex provider adapters, batch verification, and a React/TypeScript frontend. Treat these as proposed until the PR is reviewed, merged and tested at its exact final head. The branch describes its default mode as demo evidence and its real-provider mode as optional. The example response includes an “Official Government Registry” with a null URL; that is illustrative placeholder content, not an actual source or verification record. Never present it as real evidence. Every production evidence item must carry a resolvable source URL, retrieval timestamp and provenance.

---

## Engineering Audit & Handover — 2026-11-17

**Review scope:** default branch `main`; static inspection of `src/truthstream/api.py`, `pipeline.py`, `evidence.py`, `scoring.py`, and `tests/test_api.py`. Tests were not executed.

### Confirmed findings
- The default `VerificationPipeline` uses `InMemoryEvidenceRetriever`, whose evidence is a small hardcoded demo dataset. It does not retrieve current evidence from the web or authoritative live sources.
- Evidence retrieval is keyword-overlap matching, and confidence is a weighted ratio based on configured credibility and recency values. This is an MVP heuristic, not a validated fact-checking or truth-detection system.
- The API tests assert a specific canned claim result using the demo evidence. Passing those tests would establish deterministic demo behavior, not real-world verification accuracy.
- Request text is validated as non-empty/non-whitespace, which is a useful existing safeguard.

### Next actions
1. Label outputs as demo/heuristic until connected to sourced, timestamped evidence retrieval.
2. Add provenance, source URLs, retrieval timestamps, evidence deduplication, and a reviewable explanation for every result.
3. Evaluate on a documented benchmark with human-labelled claims; report precision, recall, calibration, and abstention behavior.

**Verification status:** static source/test inspection only; `pytest`, API runtime, and any external-source integration were not run or verified.


---

## Branch Activity & Development History

**Audit date:** 2026-11-18 · **Comparison base:** `main`

| Branch | Difference from `main` | Observed work / changed paths |
|---|---:|---|
| `ai-upgrade-2026-11-13` | 2 ahead / 4 behind | Prompt and Sprint 4 checklist revisions |
| `chore/remove-emoji-glyphs-2026-11-13` | 6 / 4 | Prompt and Sprint 4 checklist glyph cleanup |
| `codex/establish-project-workflow-guidelines` | 0 / 7 | No unique commits relative to current `main`; branch is behind |
| `codex/establish-project-workflow-guidelines-l37ven` | 2 / 8 | Large backend + React frontend implementation, API, evidence extraction/scoring, provider adapters and tests; README also changed substantially |
| `copilot/productionize/Truthstream-audit` | 0 / 5 | No unique commits relative to current `main`; branch is behind |
| `docs/portfolio-operating-kit-2026-11-13` | 5 / 4 | Activity log, agent/workflow docs, worklog, company-fit notes, feature plan and skills |
| `docs/project-status-2026-11-16-truthstream` | 1 / 1 | Project status snapshot: `PROJECT_STATUS.md` |
| `docs/status-inventory-2026-11-16-v1` | 1 / 1 | Project status inventory: `PROJECT_STATUS.md` |
| `fix/api-validation-and-ci` | 4 / 5 | CI workflow, API validation, worklog and API tests |
| `sprint-4-run-stabilize` | 1 / 8 | Large backend + React frontend implementation, API, evidence extraction/scoring, provider adapters and tests; README also changed substantially |

### Open pull requests observed during this audit

- [PR #8 — project status snapshot](https://github.com/Gitcoder12/Truthstream/pull/8)
- [PR #7 — project handbook and agent contribution guide](https://github.com/Gitcoder12/Truthstream/pull/7)
- [PR #6 — remove emoji glyphs](https://github.com/Gitcoder12/Truthstream/pull/6)
- [PR #2 — Truthstream MVP implementation](https://github.com/Gitcoder12/Truthstream/pull/2)

**Review note:** The two large implementation branches change README content substantially and appear to contain overlapping frontend/backend work. Compare exact commits and run backend/frontend tests before choosing a branch or merging. No branches have been merged or deleted by this documentation update.

**Verification boundary:** Git metadata and changed paths only; this section does not certify runtime behavior, provider correctness or test success.
