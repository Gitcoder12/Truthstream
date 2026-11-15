# Project Status — Truthstream

**Snapshot date:** 2026-11-16  
**Status type:** Initial documentation and repository-tree assessment  
**Default branch:** main  
**Review completeness:** Partial — not a code audit or release certification

## Project purpose
MVP backend foundation for extracting claims, retrieving evidence, scoring support/contradiction and exposing FastAPI/CLI interfaces.

## Current maturity (README-declared or visible scaffolding; not independently verified)
README describes deterministic extraction heuristics, pluggable retrieval protocol with an in-memory demo retriever, evidence-weighted scoring, API, CLI and automated tests. Root includes src/, tests/ and pyproject.toml.

## Observed repository structure
src/, tests/, pyproject.toml, AI_WORKLOG.md, PROMPTS.md, SETUP.md and sprint checklist.

## Known issues and risks to investigate
The in-memory retriever is explicitly a demo and must not be presented as live evidence retrieval. The README example uses placeholder-like claim/source text and potentially self-contradictory evidence counts; verify examples before trust demonstrations. Confidence scores are heuristics unless calibrated against labeled data. No tests were run in this pass.

## Recommended next actions
Run pytest and Ruff; inspect claim segmentation and evidence-source provenance; enforce URL and retrieval timestamps; add test cases for no evidence, contradictory sources, stale evidence and source independence; calibrate confidence against adjudicated claims before calling scores probabilities.

## Verification record
| Check | Result |
|---|---|
| Default-branch top-level tree | Inspected |
| README | Inspected |
| Deep source review | Not performed |
| Tests / build / runtime | Not run |
| Security / dependency audit | Not run |
| Live deployment / API checks | Not run |
| Independent review | Not performed |

## Change log
- 2026-11-16: Added this initial status snapshot on a review branch. No application code or existing data changed.

> Update this file only after the corresponding inspection or verification has actually been performed. Distinguish observed facts, README claims, hypotheses and unrun checks.