#!/usr/bin/env python3
"""On-demand library verification of engram-generator training data.

Independently recomputes answers using third-party libraries
(sympy, numpy, scipy, networkx) and compares to generator output.
No generator logic is reused -- the library IS the ground truth.

This script is never run during training or evaluation.

Usage:
    python scripts/verify_libraries.py                    # all tiers
    python scripts/verify_libraries.py --tier 0           # tier 0 only
    python scripts/verify_libraries.py --seeds 10         # quick check
    python scripts/verify_libraries.py --task addition    # single task
"""
import argparse
import json
import random
import sys
import time

from engram_generator.curriculum.registry import get_all_generators
from engram_generator.validation.library_verifier import LibraryVerifier


def main() -> int:
    """Run library verification and report results.

    Returns:
        Exit code: 0 if all match, 1 if mismatches found.
    """
    parser = argparse.ArgumentParser(
        description="Verify generator answers against independent libraries",
    )
    parser.add_argument("--tier", type=int, default=None,
                        help="Only verify this tier")
    parser.add_argument("--seeds", type=int, default=20,
                        help="Seeds per difficulty (default: 20)")
    parser.add_argument("--task", type=str, default=None,
                        help="Verify a single task by name")
    parser.add_argument("--output", type=str, default=None,
                        help="Write results to JSON file")
    args = parser.parse_args()

    verifier = LibraryVerifier()
    generators = get_all_generators()

    if args.task:
        generators = [g for g in generators if g.task_name == args.task]
    elif args.tier is not None:
        generators = [g for g in generators if g.tier == args.tier]

    verifiable = [g for g in generators if verifier.can_verify(g.task_name)]

    print(f"Library Verification ({args.seeds} seeds/difficulty)")
    print(f"Generators: {len(generators)} total, "
          f"{len(verifiable)} with library handlers")
    print("=" * 60)

    total = 0
    matched = 0
    mismatched = 0
    errors = 0
    mismatch_details = []

    start = time.time()
    for gi, gen in enumerate(verifiable):
        task = gen.task_name
        min_d = max(1, gen.min_difficulty)
        max_d = gen.max_difficulty
        task_mismatches = 0

        for d in range(min_d, max_d + 1):
            gen.set_difficulty(d, d)
            for seed in range(args.seeds):
                gen._rng = random.Random(seed)
                try:
                    problem, solution_data = gen._create_problem(d)
                    answer = gen._create_answer(solution_data)
                    answer = gen._cap_decimals(answer)

                    result = verifier.verify(task, solution_data, answer)
                    total += 1

                    if result.match is True:
                        matched += 1
                    elif result.match is False:
                        mismatched += 1
                        task_mismatches += 1
                        if len(mismatch_details) < 50:
                            mismatch_details.append({
                                "task": task,
                                "difficulty": d,
                                "seed": seed,
                                "expected": result.expected,
                                "computed": result.computed,
                                "solution_data_keys": list(
                                    solution_data.keys()),
                            })
                    else:
                        errors += 1
                except Exception:
                    errors += 1

            gen.set_difficulty(min_d, max_d)

        status = "OK" if task_mismatches == 0 else f"MISMATCH ({task_mismatches})"
        pct = (gi + 1) * 100 // len(verifiable)
        print(f"\r  [{pct:3d}%] {task:<40s} {status}", flush=True)

    elapsed = time.time() - start
    print(f"\r  [100%] Done in {elapsed:.1f}s" + " " * 40)

    print(f"\nResults ({total:,} verifications):")
    print(f"  Matched:    {matched:>8,d}  ({matched*100//total if total else 0}%)")
    print(f"  Mismatched: {mismatched:>8,d}  ({mismatched*100//total if total else 0}%)")
    print(f"  Errors:     {errors:>8,d}  ({errors*100//total if total else 0}%)")

    if mismatch_details:
        print(f"\nMismatch details (first {len(mismatch_details)}):")
        for m in mismatch_details[:20]:
            print(f"  {m['task']} d={m['difficulty']} s={m['seed']}: "
                  f"gen='{m['expected']}' lib='{m['computed']}'")

    if args.output:
        with open(args.output, "w") as f:
            json.dump({
                "total": total,
                "matched": matched,
                "mismatched": mismatched,
                "errors": errors,
                "mismatches": mismatch_details,
            }, f, indent=2)
        print(f"\nResults written to {args.output}")

    if mismatched > 0:
        print(f"\nFAILED: {mismatched} answers disagree with library")
        return 1

    print(f"\nPASSED: all {matched} verified answers match libraries")
    return 0


if __name__ == "__main__":
    sys.exit(main())
