#!/usr/bin/env python3
"""Exhaustive validation of all engram-generator training data.

Generates samples at scale, verifies every arithmetic step
computationally, and exports static lookup tables.

Usage:
    python scripts/validate_all.py --seeds 100 --output-dir validation_output
    python scripts/validate_all.py --seeds 5 --tier 0  # quick test
    python scripts/validate_all.py --seeds 100 --format csv
"""
import argparse
import sys
import time

from engram_generator.validation import ValidationRunner, Exporter


def main() -> int:
    """Run exhaustive validation and export results.

    Returns:
        Exit code: 0 if no wrong steps, 1 if any verified wrong.
    """
    parser = argparse.ArgumentParser(
        description="Validate engram-generator training data",
    )
    parser.add_argument(
        "--seeds", type=int, default=100,
        help="Seeds per difficulty level (default: 100)",
    )
    parser.add_argument(
        "--tier", type=int, default=None,
        help="Only validate this tier (default: all)",
    )
    parser.add_argument(
        "--output-dir", type=str, default="validation_output",
        help="Output directory (default: validation_output)",
    )
    parser.add_argument(
        "--format", type=str, default="both",
        choices=["jsonl", "csv", "both"],
        help="Export format (default: both)",
    )
    args = parser.parse_args()

    runner = ValidationRunner(seeds_per_difficulty=args.seeds)

    def progress(name: str, current: int, total: int) -> None:
        pct = current * 100 // total if total else 0
        print(f"\r  [{pct:3d}%] {current}/{total} {name:<40s}", end="",
              flush=True)

    print(f"Engram Generator Validation ({args.seeds} seeds/difficulty)")
    print("=" * 60)

    start = time.time()
    if args.tier is not None:
        print(f"Validating tier {args.tier}...")
        report = runner.validate_tier(args.tier, progress=progress)
    else:
        print("Validating all generators...")
        report = runner.validate_all(progress=progress)
    elapsed = time.time() - start
    print(f"\r  [100%] Done in {elapsed:.1f}s" + " " * 40)

    exporter = Exporter(report)
    if args.format in ("jsonl", "both"):
        exporter.export_jsonl(f"{args.output_dir}/jsonl")
    if args.format in ("csv", "both"):
        exporter.export_csv(f"{args.output_dir}/validation.csv")
    exporter.export_summary(f"{args.output_dir}/summary.json")

    by_status = report.count_by_status()
    print(f"\nResults ({report.total:,} samples):")
    for status, count in sorted(by_status.items()):
        pct = count * 100 / report.total if report.total else 0
        print(f"  {status:<20s} {count:>8,d}  ({pct:.1f}%)")

    wrong = by_status.get("wrong", 0)
    crashes = by_status.get("crash", 0)
    fallbacks = by_status.get("fallback", 0)

    if wrong > 0:
        print(f"\nFAILED: {wrong} samples have wrong arithmetic steps")
        summary = report.per_generator_summary()
        bad = {k: v for k, v in summary.items() if v["verified_wrong"] > 0}
        for gen, stats in sorted(bad.items(),
                                  key=lambda x: -x[1]["verified_wrong"]):
            print(f"  {gen}: {stats['verified_wrong']} wrong steps")
        return 1

    if crashes > 0:
        print(f"\nWARNING: {crashes} samples crashed")
    if fallbacks > 0:
        print(f"\nWARNING: {fallbacks} fallback samples")

    print(f"\nPASSED: no wrong arithmetic steps detected")
    print(f"Output: {args.output_dir}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
