# AI Engineering Worklog

## Audit scope

Repository: TruthStream  
Base audited: `main`  
Working branch: `fix/api-validation-and-ci`  
Date: 2026-11-13

## Confirmed work in this branch

- Added a typed Pydantic request model for `POST /verify`.
- Rejects missing, empty, and whitespace-only claim text with FastAPI's normal 422 validation response instead of an unhandled `KeyError`.
- Preserves the optional source field.
- Added regression tests for missing and blank text.
- Added a Python 3.11/3.12 GitHub Actions workflow that installs the declared development extra, runs Ruff on source/tests, and runs pytest.

## Nine-gate audit

| Gate | Current assessment | Notes |
|---|---|---|
| Architecture | Good MVP separation | Extraction, retrieval, scoring, pipeline, API are separate modules |
| Correctness | Needs evaluation | Heuristic extraction and keyword-overlap retrieval are intentionally limited |
| Tests | Improving | Small API/pipeline tests exist; this branch adds invalid-input regression tests |
| Error handling | Improved | API request validation now returns structured 422 responses |
| Security | Review needed | Keep external retrieval/provider integrations behind explicit timeouts, input limits, and safe parsing |
| Dependencies | Reasonable MVP | Runtime and development dependencies are declared in pyproject.toml |
| Performance | Limited scope | In-memory retrieval is small; production ingestion/ranking needs bounded data and indexing |
| Documentation | Mostly aligned | README describes the in-memory retriever as a demo and avoids claiming absolute truth |
| CI/release | Added here | New workflow will provide the first reproducible lint/test gate once Actions completes |

## Research and evaluation limitations

- The default retriever is an in-memory demonstration fixture, not a production web/news retrieval system.
- Claim extraction uses deterministic sentence and cue heuristics; it is not a validated claim extraction model.
- Confidence is a normalized ratio of weighted supporting versus contradicting evidence. It is not a calibrated probability that a claim is true.
- The default fixture data is synthetic demonstration content and must not be represented as live verification evidence.
- Open issue #4 correctly calls for a versioned labeled dataset, a documented labeling protocol, and reproducible classification/ranking metrics before stronger reliability claims are made.

## Validation status

- Regression tests and CI workflow have been committed to this branch.
- CI results are pending; no passing result is claimed until the exact branch-head checks complete.

## Next actions

1. Add the labeled evaluation dataset and labeling protocol requested in issue #4.
2. Report class-wise metrics and confusion counts, including insufficient-evidence cases.
3. Add retrieval timeout/error handling when a production provider is introduced.
4. Keep the UI/API wording explicit that verification output is decision support, not proof.
