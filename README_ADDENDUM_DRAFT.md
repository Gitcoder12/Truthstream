# Truthstream — README Explanation Draft

> Check against the actual source before merging into the main README.

## Plain-language explanation

A tool that takes a claim, finds evidence for and against it, and explains how strong that evidence is.

## Current implementation

MVP backend foundation with deterministic claim extraction, a pluggable evidence-retrieval interface, an in-memory demo retriever, evidence-weighted confidence scoring, FastAPI /health and /verify endpoints, CLI and automated tests. Demo retrieval is not proof of real-time or comprehensive fact-checking.

## Technical/research explanation

Document the data flow, API contracts, source adapters, scoring/calibration logic, dependencies and error handling. Show a concrete example from input to output.

## Reproducibility

State exact setup/test commands, versions, dataset or API source, retrieval timestamp, configuration and expected output. Link benchmark results only when independently reproducible.

## Limitations

Explain missing sources, stale data, heuristic scores, uncertainty and unsupported use cases. For security and safety work, state that outputs are triage aids, not autonomous incident decisions.

## Contribution path

See FEATURE_UPGRADE_PLAN.md, CONTRIBUTING.md and ACTIVITY_LOG.md.
