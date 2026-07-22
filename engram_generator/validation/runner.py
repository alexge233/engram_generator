"""Validation runner that generates samples and verifies them."""
import random
import re
import warnings
from typing import Callable

from engram_generator.curriculum.registry import get_all_generators
from engram_generator.evaluation.python_verifier import PythonVerifier
from engram_generator.validation.result import (
    StepResult,
    SampleResult,
    ValidationReport,
)

_LEAK_SKIP_TASKS = frozenset({
    "sorting", "comparison", "max_min", "boolean_eval", "truth_table",
    "propositional_eval", "set_operations", "string_reverse",
    "string_length", "list_operations", "subtraction", "addition",
    "multiplication", "division", "modular", "gcd",
    "computational_tradeoff",
    "method_comparison", "payoff_matrix", "cfg_derivation",
    "extensive_form", "architecture_search", "pushdown_simulate",
    "convex_check", "analytic_check", "basic_prob",
    "cardinal_arithmetic", "rock_cycle", "natural_deduction",
    "dead_code_elimination", "carmichael_number", "deformation_retract",
    "reductio_ad_absurdum", "sequent_calculus",
})


class ValidationRunner:
    """Generates samples at scale and verifies every step.

    Args:
        seeds_per_difficulty: Number of seeds to test per difficulty level.
        verifier_enabled: Whether to run PythonVerifier on steps.
    """

    def __init__(self, seeds_per_difficulty: int = 100,
                 verifier_enabled: bool = True) -> None:
        """Initialise the runner.

        Args:
            seeds_per_difficulty: Seeds per difficulty level.
            verifier_enabled: Enable computational verification.
        """
        self._seeds = seeds_per_difficulty
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            self._verifier = PythonVerifier(enabled=verifier_enabled)

    def validate_generator(self, gen, difficulty: int) -> list[SampleResult]:
        """Validate one generator at one difficulty level.

        Args:
            gen: A StepGenerator instance.
            difficulty: Difficulty level to test.

        Returns:
            List of SampleResult, one per seed.
        """
        results = []
        gen.set_difficulty(difficulty, difficulty)

        for seed in range(self._seeds):
            gen._rng = random.Random(seed)
            result = self._validate_one(gen, difficulty, seed)
            results.append(result)

        gen.set_difficulty(gen.min_difficulty, gen.max_difficulty)
        return results

    def validate_all(
        self,
        progress: Callable[[str, int, int], None] | None = None,
    ) -> ValidationReport:
        """Validate all registered generators at all difficulties.

        Args:
            progress: Optional callback(generator_name, current, total).

        Returns:
            Complete validation report.
        """
        generators = get_all_generators()
        return self._run(generators, progress)

    def validate_tier(
        self,
        tier: int,
        progress: Callable[[str, int, int], None] | None = None,
    ) -> ValidationReport:
        """Validate all generators in a specific tier.

        Args:
            tier: Tier number (0-10).
            progress: Optional callback.

        Returns:
            Validation report for the tier.
        """
        generators = [
            g for g in get_all_generators() if g.tier == tier
        ]
        return self._run(generators, progress)

    def _run(
        self,
        generators: list,
        progress: Callable[[str, int, int], None] | None,
    ) -> ValidationReport:
        """Run validation across a list of generators.

        Args:
            generators: Generator instances to validate.
            progress: Optional callback.

        Returns:
            Aggregated validation report.
        """
        report = ValidationReport()
        total = len(generators)

        for i, gen in enumerate(generators):
            name = gen.__class__.__name__
            if progress:
                progress(name, i, total)

            min_d = max(1, gen.min_difficulty)
            max_d = gen.max_difficulty
            for d in range(min_d, max_d + 1):
                results = self.validate_generator(gen, d)
                report.extend(results)

        return report

    def _validate_one(self, gen, difficulty: int,
                      seed: int) -> SampleResult:
        """Generate and validate a single sample.

        Args:
            gen: Generator instance.
            difficulty: Difficulty level.
            seed: Random seed.

        Returns:
            Validated SampleResult.
        """
        name = gen.__class__.__name__
        task = gen.task_name
        tier = gen.tier

        try:
            sample = gen._generate_one()
        except Exception as e:
            return SampleResult(
                generator=name, task_name=task, tier=tier,
                difficulty=difficulty, seed=seed,
                problem="", answer="", status="crash",
            )

        if sample.target_text.startswith("skip"):
            return SampleResult(
                generator=name, task_name=task, tier=tier,
                difficulty=difficulty, seed=seed,
                problem=sample.problem, answer=sample.answer,
                status="fallback",
            )

        if not sample.answer or not sample.problem:
            return SampleResult(
                generator=name, task_name=task, tier=tier,
                difficulty=difficulty, seed=seed,
                problem=sample.problem, answer=sample.answer,
                status="empty",
            )

        leak = self._check_leak(sample)

        step_results = []
        has_verified = False
        has_wrong = False
        for step_text in sample.steps:
            try:
                vr = self._verifier.verify_step(step_text)
                sr = StepResult(
                    text=step_text,
                    verified=vr.valid,
                    expected=vr.expected,
                    computed=vr.computed,
                    reason=vr.reason,
                )
            except Exception:
                sr = StepResult(
                    text=step_text, verified=None,
                    reason="verifier_error",
                )
            step_results.append(sr)
            if sr.verified is True:
                has_verified = True
            elif sr.verified is False:
                has_wrong = True

        if has_wrong:
            status = "wrong"
        elif leak:
            status = "leak"
        elif has_verified and not has_wrong:
            status = "all_verified" if all(
                s.verified is True for s in step_results
            ) else "partial"
        else:
            status = "unverifiable"

        return SampleResult(
            generator=name, task_name=task, tier=tier,
            difficulty=difficulty, seed=seed,
            problem=sample.problem, answer=sample.answer,
            steps=step_results, status=status,
        )

    def _check_leak(self, sample) -> bool:
        """Check if the answer leaks into the problem text.

        Args:
            sample: Generated sample.

        Returns:
            True if a leak is detected.
        """
        if sample.task_name in _LEAK_SKIP_TASKS:
            return False
        answer = str(sample.answer).strip()
        if not answer or len(answer) <= 2:
            return False
        if answer in ("True", "False"):
            return False
        if answer not in sample.problem:
            return False
        idx = sample.problem.index(answer)
        before = sample.problem[idx - 1] if idx > 0 else " "
        after_idx = idx + len(answer)
        after = sample.problem[after_idx] if after_idx < len(
            sample.problem) else " "
        if before.isdigit() or after.isdigit():
            return False
        return True
