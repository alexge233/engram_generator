#!/usr/bin/env python3
"""Double-blind verification using textbook examples from knowledge atoms.

Independently recomputes formula results using hardcoded textbook
inputs and compares against the known expected output. No generator
code is called -- this verifies the FORMULA, not the generator.

Usage:
    python scripts/verify_examples.py
    python scripts/verify_examples.py --task rate_law
"""
import argparse
import sys

from engram_generator.validation.example_verifier import ExampleVerifier


def main() -> int:
    """Run example verification and report results.

    Returns:
        Exit code: 0 if all match, 1 if mismatches found.
    """
    parser = argparse.ArgumentParser(
        description="Verify formulas against textbook examples",
    )
    parser.add_argument("--task", type=str, default=None,
                        help="Verify a single task")
    args = parser.parse_args()

    verifier = ExampleVerifier()

    if args.task:
        result = verifier.verify(args.task)
        print(f"{result.task_name}: match={result.match}")
        print(f"  inputs:   {result.inputs}")
        print(f"  expected: {result.expected}")
        print(f"  computed: {result.computed}")
        if result.reason:
            print(f"  reason:   {result.reason}")
        return 0 if result.match else 1

    results = verifier.verify_all()

    print(f"Double-Blind Example Verification")
    print(f"Tasks with examples: {len(results)}")
    print("=" * 60)

    matched = 0
    mismatched = 0
    errors = 0

    for r in results:
        if r.match is True:
            matched += 1
            status = "OK"
        elif r.match is False:
            mismatched += 1
            status = "MISMATCH"
        else:
            errors += 1
            status = "ERROR"
        print(f"  {r.task_name:<35s} {status}")
        if r.match is False:
            print(f"    inputs:   {r.inputs}")
            print(f"    expected: {r.expected}")
            print(f"    computed: {r.computed}")

    print(f"\nResults ({len(results)} examples):")
    print(f"  Matched:    {matched:>4d}")
    print(f"  Mismatched: {mismatched:>4d}")
    print(f"  Errors:     {errors:>4d}")

    if mismatched > 0:
        print(f"\nFAILED: {mismatched} formulas disagree with textbook")
        return 1

    print(f"\nPASSED: all {matched} formulas match textbook examples")
    return 0


if __name__ == "__main__":
    sys.exit(main())
