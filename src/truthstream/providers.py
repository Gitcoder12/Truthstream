"""Modular evidence providers for real-world source integrations.

Providers intentionally return neutral evidence. They retrieve potentially relevant,
deterministic source material; support/contradiction classification can later be handled by a
separate ranking or stance-detection component without changing the provider interface.
"""

from __future__ import annotations

import json
import time
from collections.abc import Callable, Iterable
from dataclasses import dataclass
from typing import Any, Protocol
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from truthstream.models import Claim, Evidence, EvidenceStance, Source

JsonOpener = Callable[[str, dict[str, str], float], dict[str, Any]]


class EvidenceProvider(Protocol):
    """Fetch evidence candidates for a claim from one source family."""

    name: str

    def fetch(self, claim: Claim) -> list[Evidence]:
        """Return evidence candidates for the supplied claim."""


@dataclass(slots=True)
class ProviderConfig:
    """Network and result-limit settings shared by HTTP evidence providers."""

    timeout_seconds: float = 5.0
    max_results: int = 5
    user_agent: str = "TruthStream/0.1 (+https://github.com/truthstream)"


@dataclass(slots=True)
class CacheEntry:
    """In-memory cache entry for provider responses."""

    expires_at: float
    evidence: list[Evidence]


class CachedEvidenceProvider:
    """TTL cache wrapper for provider responses."""

    def __init__(self, provider: EvidenceProvider, ttl_seconds: int = 900) -> None:
        self.provider = provider
        self.name = provider.name
        self._ttl_seconds = ttl_seconds
        self._cache: dict[str, CacheEntry] = {}

    def fetch(self, claim: Claim) -> list[Evidence]:
        cache_key = claim.text.strip().lower()
        now = time.time()
        cached = self._cache.get(cache_key)
        if cached and cached.expires_at > now:
            return list(cached.evidence)

        evidence = self.provider.fetch(claim)
        self._cache[cache_key] = CacheEntry(
            expires_at=now + self._ttl_seconds,
            evidence=list(evidence),
        )
        return evidence


class WikipediaEvidenceProvider:
    """Evidence provider backed by Wikipedia's public REST search endpoint."""

    name = "wikipedia"
    base_url = "https://en.wikipedia.org/w/rest.php/v1/search/page"

    def __init__(
        self,
        config: ProviderConfig | None = None,
        opener: JsonOpener | None = None,
    ) -> None:
        self.config = config or ProviderConfig()
        self._opener = opener or _get_json

    def fetch(self, claim: Claim) -> list[Evidence]:
        payload = self._opener(
            f"{self.base_url}?{urlencode({'q': claim.text, 'limit': self.config.max_results})}",
            {"User-Agent": self.config.user_agent},
            self.config.timeout_seconds,
        )
        pages = payload.get("pages", [])
        return [
            Evidence(
                source=Source(
                    name="Wikipedia",
                    url=f"https://en.wikipedia.org/wiki/{page.get('key', '')}",
                    credibility=0.72,
                ),
                title=str(page.get("title", "Wikipedia result")),
                snippet=_clean_snippet(str(page.get("excerpt", ""))),
                stance=EvidenceStance.NEUTRAL,
                recency_score=0.7,
            )
            for page in pages[: self.config.max_results]
            if page.get("title")
        ]


class CrossrefEvidenceProvider:
    """Evidence provider backed by Crossref works search."""

    name = "crossref"
    base_url = "https://api.crossref.org/works"

    def __init__(
        self,
        config: ProviderConfig | None = None,
        opener: JsonOpener | None = None,
    ) -> None:
        self.config = config or ProviderConfig()
        self._opener = opener or _get_json

    def fetch(self, claim: Claim) -> list[Evidence]:
        payload = self._opener(
            f"{self.base_url}?{urlencode({'query': claim.text, 'rows': self.config.max_results})}",
            {"User-Agent": self.config.user_agent},
            self.config.timeout_seconds,
        )
        items = payload.get("message", {}).get("items", [])
        evidence = []
        for item in items[: self.config.max_results]:
            title = _first(item.get("title"), "Crossref work")
            evidence.append(
                Evidence(
                    source=Source(name="Crossref", url=item.get("URL"), credibility=0.84),
                    title=title,
                    snippet=_first(item.get("container-title"), "Scholarly metadata result."),
                    stance=EvidenceStance.NEUTRAL,
                    recency_score=0.75,
                )
            )
        return evidence


class OpenAlexEvidenceProvider:
    """Evidence provider backed by OpenAlex works search."""

    name = "openalex"
    base_url = "https://api.openalex.org/works"

    def __init__(
        self,
        config: ProviderConfig | None = None,
        opener: JsonOpener | None = None,
    ) -> None:
        self.config = config or ProviderConfig()
        self._opener = opener or _get_json

    def fetch(self, claim: Claim) -> list[Evidence]:
        query = urlencode({"search": claim.text, "per-page": self.config.max_results})
        payload = self._opener(
            f"{self.base_url}?{query}",
            {"User-Agent": self.config.user_agent},
            self.config.timeout_seconds,
        )
        results = payload.get("results", [])
        evidence = []
        for item in results[: self.config.max_results]:
            evidence.append(
                Evidence(
                    source=Source(
                        name="OpenAlex",
                        url=item.get("id") or item.get("doi"),
                        credibility=0.83,
                    ),
                    title=str(item.get("display_name", "OpenAlex work")),
                    snippet=_openalex_snippet(item),
                    stance=EvidenceStance.NEUTRAL,
                    recency_score=0.75,
                )
            )
        return evidence


def default_providers(config: ProviderConfig | None = None) -> list[EvidenceProvider]:
    """Return the default real evidence providers with caching enabled."""

    provider_config = config or ProviderConfig()
    providers: Iterable[EvidenceProvider] = (
        WikipediaEvidenceProvider(provider_config),
        CrossrefEvidenceProvider(provider_config),
        OpenAlexEvidenceProvider(provider_config),
    )
    return [CachedEvidenceProvider(provider) for provider in providers]


def _get_json(url: str, headers: dict[str, str], timeout_seconds: float) -> dict[str, Any]:
    request = Request(url, headers=headers)
    try:
        with urlopen(request, timeout=timeout_seconds) as response:  # noqa: S310 - trusted URLs.
            return json.loads(response.read().decode("utf-8"))
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError):
        return {}


def _first(value: Any, default: str) -> str:
    if isinstance(value, list) and value:
        return str(value[0])
    if isinstance(value, str) and value:
        return value
    return default


def _clean_snippet(snippet: str) -> str:
    return snippet.replace("<span class=\"searchmatch\">", "").replace("</span>", "")


def _openalex_snippet(item: dict[str, Any]) -> str:
    publication_year = item.get("publication_year")
    source = item.get("primary_location", {}).get("source", {}) or {}
    source_name = source.get("display_name")
    pieces = [str(piece) for piece in (publication_year, source_name) if piece]
    return " | ".join(pieces) if pieces else "OpenAlex scholarly metadata result."
