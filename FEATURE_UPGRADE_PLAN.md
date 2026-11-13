# Truthstream — Feature Upgrade Plan

**Snapshot:** 2026-11-13

## Objective

A tool that takes a claim, finds evidence for and against it, and explains how strong that evidence is.

## P0 — data integrity and correctness

- [ ] Make evidence source, date, retrieval method and claim span explicit in every verification record.
- [ ] Test contradictory, stale, duplicated, missing and low-quality evidence; make uncertainty visible.

## P1 — core workflow

- [ ] Add pluggable source adapters with attribution, licensing and rate-limit handling.
- [ ] Build a reviewer interface that separates claim, evidence, counterevidence and conclusion.

## P2 — research and scale

- [ ] Benchmark claim extraction and evidence retrieval against a labelled dataset.
- [ ] Evaluate calibration and source coverage; publish false-positive and false-negative analysis.

## Collaboration work packages

1. Source/data validation and reproducible fixtures.
2. One isolated feature with deterministic regression tests.
3. Evaluation against a baseline or independently labelled sample.
4. Documentation of assumptions, provenance, uncertainty and limitations.

## Completion criteria

- [ ] Clean setup and one end-to-end workflow work.
- [ ] Tests cover valid, invalid, missing and adversarial inputs.
- [ ] External-data freshness and failures are visible.
- [ ] Claims are no stronger than the evidence.
