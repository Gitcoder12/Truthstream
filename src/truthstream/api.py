"""FastAPI application for TruthStream."""

try:
    from fastapi import FastAPI, HTTPException
except ImportError as exc:  # pragma: no cover - exercised only when optional deps are missing.
    raise RuntimeError(
        "The API requires FastAPI. Install API dependencies with `pip install -e '.[dev]'`."
    ) from exc

from truthstream.models import StreamItem
from truthstream.pipeline import VerificationPipeline
from truthstream.settings import build_evidence_retriever

app = FastAPI(
    title="TruthStream API",
    version="0.1.0",
    description="MVP API for transparent, evidence-centered claim verification.",
)
pipeline = VerificationPipeline(retriever=build_evidence_retriever())


@app.get("/health")
def health() -> dict[str, str]:
    """Return service health."""

    return {"status": "ok"}


@app.post("/verify")
def verify(item: dict[str, str]) -> list[dict[str, object]]:
    """Verify claims from an incoming stream item."""

    return _verify_item(item)


@app.post("/verify/batch")
def verify_batch(items: list[dict[str, str]]) -> list[list[dict[str, object]]]:
    """Verify multiple incoming stream items in request order."""

    if not items:
        raise HTTPException(status_code=400, detail="At least one item is required.")
    return [_verify_item(item) for item in items]


def _verify_item(item: dict[str, str]) -> list[dict[str, object]]:
    text = item.get("text", "").strip()
    if not text:
        raise HTTPException(status_code=400, detail="Item text is required.")

    results = pipeline.verify(StreamItem(text=text, source=item.get("source")))
    return [result.to_dict() for result in results]
