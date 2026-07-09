"""FastAPI application for TruthStream."""

try:
    from fastapi import FastAPI
except ImportError as exc:  # pragma: no cover - exercised only when optional deps are missing.
    raise RuntimeError(
        "The API requires FastAPI. Install API dependencies with `pip install -e '.[dev]'`."
    ) from exc

from truthstream.models import StreamItem
from truthstream.pipeline import VerificationPipeline

app = FastAPI(
    title="TruthStream API",
    version="0.1.0",
    description="MVP API for transparent, evidence-centered claim verification.",
)
pipeline = VerificationPipeline()


@app.get("/health")
def health() -> dict[str, str]:
    """Return service health."""

    return {"status": "ok"}


@app.post("/verify")
def verify(item: dict[str, str]) -> list[dict[str, object]]:
    """Verify claims from an incoming stream item."""

    results = pipeline.verify(StreamItem(text=item["text"], source=item.get("source")))
    return [result.to_dict() for result in results]
