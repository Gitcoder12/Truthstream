"""Command-line entrypoint for local TruthStream verification."""

import argparse
import json

from truthstream.models import StreamItem
from truthstream.pipeline import VerificationPipeline


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify claims in a text snippet.")
    parser.add_argument("text", help="Text to analyze for factual claims.")
    args = parser.parse_args()

    results = VerificationPipeline().verify(StreamItem(text=args.text))
    print(json.dumps([result.to_dict() for result in results], indent=2))


if __name__ == "__main__":
    main()
