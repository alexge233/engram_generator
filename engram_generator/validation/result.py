"""Data classes for validation results."""
from dataclasses import dataclass, field
from collections import defaultdict


@dataclass
class StepResult:
    """Verification result for a single reasoning step.

    Attributes:
        text: The raw step string.
        verified: True if correct, False if wrong, None if unparseable.
        expected: Value stated in the step (if parseable).
        computed: Value computed by Python (if parseable).
        reason: Explanation for None/False results.
    """

    text: str
    verified: bool | None = None
    expected: float | None = None
    computed: float | None = None
    reason: str | None = None

    def to_dict(self) -> dict:
        """Serialise to a dictionary."""
        d = {"text": self.text, "verified": self.verified}
        if self.computed is not None:
            d["computed"] = self.computed
        if self.expected is not None:
            d["expected"] = self.expected
        if self.reason:
            d["reason"] = self.reason
        return d


@dataclass
class SampleResult:
    """Validation result for one generated sample.

    Attributes:
        generator: Class name of the generator.
        task_name: Unique task identifier.
        tier: Skill tree tier (0-10).
        difficulty: Difficulty level.
        seed: Random seed used.
        problem: Problem statement text.
        steps: List of StepResult for each reasoning step.
        answer: Final answer string.
        status: Overall validation status.
    """

    generator: str
    task_name: str
    tier: int
    difficulty: int
    seed: int
    problem: str
    steps: list[StepResult] = field(default_factory=list)
    answer: str = ""
    status: str = "unverifiable"

    def to_dict(self) -> dict:
        """Serialise to a dictionary."""
        return {
            "generator": self.generator,
            "task": self.task_name,
            "tier": self.tier,
            "difficulty": self.difficulty,
            "seed": self.seed,
            "problem": self.problem,
            "steps": [s.to_dict() for s in self.steps],
            "answer": self.answer,
            "status": self.status,
        }


class ValidationReport:
    """Aggregated validation results across generators.

    Attributes:
        results: All SampleResult objects.
    """

    def __init__(self) -> None:
        """Initialise an empty report."""
        self.results: list[SampleResult] = []

    def add(self, result: SampleResult) -> None:
        """Add a single sample result.

        Args:
            result: Validated sample result.
        """
        self.results.append(result)

    def extend(self, results: list[SampleResult]) -> None:
        """Add multiple sample results.

        Args:
            results: List of validated sample results.
        """
        self.results.extend(results)

    @property
    def total(self) -> int:
        """Return total number of samples."""
        return len(self.results)

    def count_by_status(self) -> dict[str, int]:
        """Count samples by status.

        Returns:
            Dict mapping status string to count.
        """
        counts: dict[str, int] = defaultdict(int)
        for r in self.results:
            counts[r.status] += 1
        return dict(counts)

    def per_generator_summary(self) -> dict[str, dict]:
        """Compute per-generator statistics.

        Returns:
            Dict mapping generator name to stats dict.
        """
        by_gen: dict[str, list[SampleResult]] = defaultdict(list)
        for r in self.results:
            by_gen[r.generator].append(r)

        summary = {}
        for gen_name, samples in sorted(by_gen.items()):
            statuses = defaultdict(int)
            verified_steps = 0
            wrong_steps = 0
            total_steps = 0
            for s in samples:
                statuses[s.status] += 1
                for step in s.steps:
                    total_steps += 1
                    if step.verified is True:
                        verified_steps += 1
                    elif step.verified is False:
                        wrong_steps += 1

            summary[gen_name] = {
                "total_samples": len(samples),
                "tier": samples[0].tier,
                "task": samples[0].task_name,
                "statuses": dict(statuses),
                "total_steps": total_steps,
                "verified_correct": verified_steps,
                "verified_wrong": wrong_steps,
                "pass_rate": 1.0 - (wrong_steps / total_steps)
                if total_steps > 0 else 1.0,
            }
        return summary

    def per_tier_summary(self) -> dict[int, dict]:
        """Compute per-tier statistics.

        Returns:
            Dict mapping tier to stats dict.
        """
        by_tier: dict[int, list[SampleResult]] = defaultdict(list)
        for r in self.results:
            by_tier[r.tier].append(r)

        summary = {}
        for tier, samples in sorted(by_tier.items()):
            statuses = defaultdict(int)
            wrong = 0
            for s in samples:
                statuses[s.status] += 1
                wrong += sum(1 for st in s.steps if st.verified is False)

            summary[tier] = {
                "total_samples": len(samples),
                "generators": len({s.generator for s in samples}),
                "statuses": dict(statuses),
                "wrong_steps": wrong,
            }
        return summary

    def summary_dict(self) -> dict:
        """Produce a full summary dictionary.

        Returns:
            Dict with top-level stats, per-generator, and per-tier.
        """
        return {
            "total_samples": self.total,
            "by_status": self.count_by_status(),
            "per_generator": self.per_generator_summary(),
            "per_tier": self.per_tier_summary(),
        }
