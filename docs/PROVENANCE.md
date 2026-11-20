# Evidence provenance contract

TruthStream's confidence score and status are evidence-weighted heuristic outputs. They are not a guarantee of truth.

Each serialized verification result includes a `provenance` summary:
- `source_backed`: every returned evidence item has a stable evidence ID, HTTPS source URL, and timezone-aware retrieval timestamp.
- `demo_or_incomplete`: at least one item lacks one or more required provenance fields.
- `no_evidence`: no evidence items were returned.

The evidence model exposes optional `evidence_id` and `retrieved_at` fields. Retrieval adapters must populate these from the actual retrieval operation. Do not fabricate IDs, timestamps, source URLs, credibility values, or retrieval history.

The default in-memory demo retriever intentionally lacks source URLs, evidence IDs, and retrieval timestamps. Its output must remain classified as `demo_or_incomplete`; it must never be represented as live or authoritative evidence.

## What this does not establish

Provenance completeness does not authenticate a publisher, establish independence between sources, validate the contents of a source, or prove that a claim is true. Distinct URL hosts are not necessarily independent organizations. Consumers must apply their own trust policy and must not use TruthStream output as proof that an agent performed a runtime action.

Production providers should preserve the canonical URL, retrieval timestamp, stable evidence identifier, source identity, and the retrieval method. Verification benchmarks and human-labelled evaluation are still required before describing scores as calibrated accuracy.
