# TruthStream

**Real-time claim verification and evidence analysis for streaming information.**

TruthStream continuously monitors incoming information streams, extracts factual claims, gathers supporting and contradicting evidence from trusted sources, and generates confidence scores with transparent explanations.

Instead of asking:

> "Is this true?"

TruthStream asks:

> "What evidence supports this claim, and how strong is that evidence?"

---

## Why TruthStream?

Information spreads faster than verification.

News articles, social media posts, blogs, and public announcements can reach millions of people before fact-checkers have time to investigate.

TruthStream helps bridge this gap by providing automated, evidence-based verification for information as it appears.

---

## Features

### Real-Time Stream Processing

Monitor live information sources including:

* News feeds
* Social media streams
* Public announcements
* Government releases
* Research publications

### Claim Extraction

Automatically identifies factual claims from incoming text using Natural Language Processing (NLP).

### Evidence Retrieval

Searches trusted sources for supporting and contradicting information.

### Confidence Scoring

Assigns a confidence score based on:

* Source credibility
* Evidence consistency
* Number of supporting sources
* Number of contradicting sources
* Information recency

### Explainable Results

Provides transparent reasoning instead of a simple true/false label.

Example:

Claim:
"Country X has banned AI systems."

Result:

* Confidence Score: 12%
* Supporting Sources: 0
* Contradicting Sources: 5
* Status: Likely False

Reason:
No official government announcement found. Multiple trusted news organizations report no such policy.

### Analytics Dashboard

Visualize:

* Trending claims
* Verification status
* Evidence graphs
* Misinformation spikes
* Source reliability metrics

---

## System Architecture

Incoming Stream
↓
Claim Extraction
↓
Evidence Retrieval
↓
Source Evaluation
↓
Confidence Scoring
↓
Explanation Generation
↓
Dashboard & Alerts

---

## Use Cases

### Misinformation Detection

Identify potentially misleading claims before they spread widely.

### Journalism

Assist reporters with rapid claim verification.

### Research

Study information propagation and verification dynamics.

### Public Transparency

Provide evidence-based verification of public statements and announcements.

### Open Source Intelligence (OSINT)

Track and evaluate claims across multiple public information channels.

---

## Technology Stack

Frontend:

* React
* TypeScript
* Tailwind CSS

Backend:

* Python
* FastAPI

Data Streaming:

* Apache Kafka
* Apache Flink

AI & NLP:

* DeepSeek/OpenAI
* Sentence Transformers
* Named Entity Recognition
* Claim Extraction Models

Storage:

* PostgreSQL
* Redis

Visualization:

* Chart.js
* D3.js

---

## Future Roadmap

* Multi-language verification
* Real-time misinformation alerts
* Knowledge graph integration
* Cross-source contradiction detection
* Source credibility learning system
* Public API
* Browser extension
* Research paper support

---

## Research Vision

TruthStream is not designed to determine absolute truth.

Its goal is to provide transparent, evidence-based confidence assessments by continuously analyzing information from multiple independent sources.

The focus is on verifiability, evidence strength, and explainability rather than binary judgments.

---

## License

MIT License
