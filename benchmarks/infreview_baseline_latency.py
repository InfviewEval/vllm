# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the vLLM project

"""Summarize per-request latency from a benchmark JSON result file."""

import argparse
import json
from pathlib import Path


def summarize_requests(records: list[dict]) -> dict[str, float]:
    """Calculate latency metrics for completed requests.

    Args:
        records: Request results with success and latency_ms fields.

    Returns:
        Successful request count, mean latency, and p95 latency.
    """
    latencies = sorted(
        float(record["latency_ms"])
        for record in records
        if record["success"]
    )
    return {
        "successful_requests": len(latencies),
        "mean_latency_ms": sum(latencies) / len(latencies),
        "p95_latency_ms": latencies[int(len(latencies) * 0.95)],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("results", type=Path, help="JSON request result list")
    args = parser.parse_args()
    records = json.loads(args.results.read_text(encoding="utf-8"))
    print(json.dumps(summarize_requests(records), indent=2))


if __name__ == "__main__":
    main()
