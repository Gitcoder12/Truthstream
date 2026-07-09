"""Command-line entrypoint for local TruthStream verification."""

import argparse
import json
import sys

from truthstream.models import StreamItem
from truthstream.pipeline import VerificationPipeline
from truthstream.settings import build_evidence_retriever


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify claims in a text snippet.")
    parser.add_argument("text", nargs="?", help="Text to analyze for factual claims.")
    parser.add_argument(
        "--evidence",
        choices=("demo", "real"),
        default="demo",
        help="Evidence backend to use. Choose real for Wikipedia, Crossref, and OpenAlex.",
    )
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="Print a compact human-readable summary instead of JSON.",
    )
    args = parser.parse_args()

    text = args.text or sys.stdin.read().strip()
    retriever = build_evidence_retriever(args.evidence)
    results = VerificationPipeline(retriever=retriever).verify(StreamItem(text=text))

    if args.pretty:
        for result in results:
            print(f"Claim: {result.claim.text}")
            print(f"Status: {result.status}")
            print(f"Confidence: {result.confidence_score:.0%}")
            print(f"Explanation: {result.explanation}")
        return

    print(json.dumps([result.to_dict() for result in results], indent=2))


if __name__ == "__main__":
    main()
