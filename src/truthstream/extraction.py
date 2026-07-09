"""Lightweight claim extraction for the MVP.

This module intentionally uses deterministic heuristics so the first version works
without external model keys. It can later be replaced by an NLP model behind the
same interface.
"""

import re

from truthstream.models import Claim, StreamItem

_SENTENCE_RE = re.compile(r"(?<=[.!?])\s+")
_ENTITY_RE = re.compile(r"\b[A-Z][A-Za-z0-9&.-]*(?:\s+[A-Z][A-Za-z0-9&.-]*)*\b")
_FACTUAL_CUES = (
    " is ",
    " are ",
    " was ",
    " were ",
    " has ",
    " have ",
    " will ",
    " announced ",
    " banned ",
    " reported ",
    " increased ",
    " decreased ",
)


class ClaimExtractor:
    """Extract concise factual claims from stream items."""

    def extract(self, item: StreamItem) -> list[Claim]:
        sentences = [part.strip() for part in _SENTENCE_RE.split(item.text) if part.strip()]
        claims: list[Claim] = []

        for sentence in sentences:
            normalized = f" {sentence.lower()} "
            if any(cue in normalized for cue in _FACTUAL_CUES):
                claims.append(Claim(text=sentence, entities=self._entities(sentence)))

        if not claims and item.text.strip():
            claims.append(Claim(text=item.text.strip(), entities=self._entities(item.text)))

        return claims

    @staticmethod
    def _entities(text: str) -> list[str]:
        entities = []
        for match in _ENTITY_RE.findall(text):
            if match not in entities:
                entities.append(match)
        return entities
