"""FastAPI application for TruthStream."""

try:
    from fastapi import FastAPI
    from pydantic import BaseModel, Field, field_validator
except ImportError as exc:  # pragma: no cover - exercised only when optional deps are missing.
    raise RuntimeError(
        "The API requires FastAPI and Pydantic. Install API dependencies with "
        "`pip install -e '.[dev]'`."
    ) from exc

from truthstream.models import StreamItem
from truthstream.pipeline import VerificationPipeline


class VerifyRequest(BaseModel):
    """Validated request body for the claim-verification endpoint."""

    text: str = Field(min_length=1)
    source: str | None = None

    @field_validator("text")
    @classmethod
    def text_must_not_be_blank(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("text must contain non-whitespace characters")
        return normalized


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
def verify(item: VerifyRequest) -> list[dict[str, object]]:
    """Verify claims from an incoming stream item."""

    results = pipeline.verify(StreamItem(text=item.text, source=item.source))
    return [result.to_dict() for result in results]
