"""Aggregate reasoning metrics across multiple samples.

Computes step accuracy, first failure distribution, final answer
accuracy, per-position accuracy, and chain-level statistics.
"""
from dataclasses import dataclass, field

from engram_generator.evaluation.normaliser import OperationNormaliser
from engram_generator.evaluation.reasoning_chain import (
    ChainComparison,
    ReasoningChain,
)


@dataclass
class ReasoningReport:
    """Aggregated reasoning evaluation across multiple samples.

    Attributes:
        total_samples: Number of samples evaluated.
        final_answer_accuracy: Fraction with correct final answer.
        mean_step_accuracy: Average fraction of correct steps per sample.
        perfect_chains: Fraction with all steps correct.
        mean_first_failure: Average step index of first failure (-1 if none).
        step_accuracy_by_position: Accuracy at each step position.
        comparisons: Individual ChainComparison objects.
    """

    total_samples: int = 0
    final_answer_accuracy: float = 0.0
    mean_step_accuracy: float = 0.0
    perfect_chains: float = 0.0
    mean_first_failure: float = -1.0
    mean_rouge_l: float = 0.0
    mean_step_similarity: float = 0.0
    mean_step_recall: float = 0.0
    mean_step_precision: float = 0.0
    step_accuracy_by_position: dict[int, float] = field(default_factory=dict)
    comparisons: list[ChainComparison] = field(default_factory=list)

    def to_dict(self) -> dict:
        """Serialise to a plain dictionary for JSON output.

        Returns:
            Dict with all aggregate metrics (no per-sample data).
        """
        return {
            "total_samples": self.total_samples,
            "final_answer_accuracy": round(self.final_answer_accuracy, 4),
            "mean_step_accuracy": round(self.mean_step_accuracy, 4),
            "perfect_chains": round(self.perfect_chains, 4),
            "mean_first_failure": round(self.mean_first_failure, 2),
            "mean_rouge_l": round(self.mean_rouge_l, 4),
            "mean_step_similarity": round(self.mean_step_similarity, 4),
            "mean_step_recall": round(self.mean_step_recall, 4),
            "mean_step_precision": round(self.mean_step_precision, 4),
            "step_accuracy_by_position": {
                str(k): round(v, 4)
                for k, v in self.step_accuracy_by_position.items()
            },
        }


class ReasoningMetrics:
    """Computes reasoning chain metrics across a batch of samples.

    Attributes:
        normaliser: The operation normaliser for step comparison.
    """

    def __init__(self, normaliser: OperationNormaliser | None = None):
        """Initialise with an optional custom normaliser.

        Args:
            normaliser: Custom normaliser, or None for default.
        """
        self._normaliser = normaliser or OperationNormaliser()

    def evaluate(
        self,
        expected_texts: list[str],
        predicted_texts: list[str],
        skip_problem: bool = True,
    ) -> ReasoningReport:
        """Evaluate a batch of expected vs predicted reasoning chains.

        Args:
            expected_texts: Ground truth strings with <step> delimiters.
            predicted_texts: Model output strings with <step> delimiters.
            skip_problem: If True, skip the problem statement in
                comparison (for LLMs that don't repeat it).

        Returns:
            ReasoningReport with aggregate and per-position metrics.
        """
        comparisons = []
        for exp_text, pred_text in zip(expected_texts, predicted_texts):
            exp_chain = ReasoningChain(exp_text, self._normaliser)
            pred_chain = ReasoningChain(pred_text, self._normaliser)
            comparison = exp_chain.compare(pred_chain, skip_problem=skip_problem)
            comparisons.append(comparison)

        return self._aggregate(comparisons)

    def evaluate_sample(
        self,
        expected_text: str,
        predicted_text: str,
        skip_problem: bool = True,
    ) -> ChainComparison:
        """Evaluate a single sample.

        Args:
            expected_text: Ground truth with <step> delimiters.
            predicted_text: Model output with <step> delimiters.
            skip_problem: If True, skip the problem statement.

        Returns:
            ChainComparison with per-step results.
        """
        exp_chain = ReasoningChain(expected_text, self._normaliser)
        pred_chain = ReasoningChain(predicted_text, self._normaliser)
        return exp_chain.compare(pred_chain, skip_problem=skip_problem)

    def _aggregate(self, comparisons: list[ChainComparison]) -> ReasoningReport:
        """Aggregate per-sample comparisons into a report.

        Args:
            comparisons: List of ChainComparison objects.

        Returns:
            ReasoningReport with aggregate metrics.
        """
        if not comparisons:
            return ReasoningReport()

        total = len(comparisons)
        final_correct = sum(c.final_answer_correct for c in comparisons)
        perfect = sum(c.chain_correct for c in comparisons)

        step_accs = [c.step_accuracy for c in comparisons]

        failures = [
            c.first_failure for c in comparisons if c.first_failure >= 0
        ]

        position_correct: dict[int, int] = {}
        position_total: dict[int, int] = {}
        for c in comparisons:
            for step in c.steps:
                pos = step.position
                position_total[pos] = position_total.get(pos, 0) + 1
                if step.correct:
                    position_correct[pos] = position_correct.get(pos, 0) + 1

        position_accuracy = {
            pos: position_correct.get(pos, 0) / position_total[pos]
            for pos in sorted(position_total)
        }

        rouge_scores = [c.rouge_l for c in comparisons]
        sim_scores = [c.mean_step_similarity for c in comparisons]
        recall_scores = [c.step_recall for c in comparisons]
        precision_scores = [c.step_precision for c in comparisons]

        return ReasoningReport(
            total_samples=total,
            final_answer_accuracy=final_correct / total,
            mean_step_accuracy=sum(step_accs) / len(step_accs),
            perfect_chains=perfect / total,
            mean_first_failure=(
                sum(failures) / len(failures) if failures else -1.0
            ),
            mean_rouge_l=sum(rouge_scores) / len(rouge_scores),
            mean_step_similarity=sum(sim_scores) / len(sim_scores),
            mean_step_recall=sum(recall_scores) / len(recall_scores),
            mean_step_precision=sum(precision_scores) / len(precision_scores),
            step_accuracy_by_position=position_accuracy,
            comparisons=comparisons,
        )

    def print_report(self, report: ReasoningReport) -> None:
        """Print a human-readable summary.

        Args:
            report: ReasoningReport to display.
        """
        print(f"\n{'=' * 60}")
        print(f"  REASONING EVALUATION ({report.total_samples} samples)")
        print(f"{'=' * 60}")
        print(f"  Final answer accuracy:  {report.final_answer_accuracy:.1%}")
        print(f"  Mean step accuracy:     {report.mean_step_accuracy:.1%}")
        print(f"  Perfect chains:         {report.perfect_chains:.1%}")
        print(f"  ROUGE-L (chain):        {report.mean_rouge_l:.3f}")
        print(f"  Step similarity:        {report.mean_step_similarity:.3f}")
        print(f"  Step recall:            {report.mean_step_recall:.1%}")
        print(f"  Step precision:         {report.mean_step_precision:.1%}")
        if report.mean_first_failure >= 0:
            print(
                f"  Mean first failure at:  step {report.mean_first_failure:.1f}"
            )
        else:
            print(f"  Mean first failure at:  none (all perfect)")
        print(f"\n  Accuracy by step position:")
        for pos, acc in report.step_accuracy_by_position.items():
            print(f"    Step {pos}: {acc:.1%}")
        print(f"{'=' * 60}")

    def print_comparison(self, comparison: ChainComparison) -> None:
        """Print a detailed per-step comparison for one sample.

        Args:
            comparison: ChainComparison to display.
        """
        for step in comparison.steps:
            mark = "OK" if step.correct else "FAIL"
            pred = step.predicted if step.predicted else "---"
            print(
                f"  Step {step.position}: "
                f"expected={step.expected:25s}  "
                f"predicted={pred:25s}  [{mark}]"
            )
        print(f"  Final answer: {comparison.final_answer_correct}")
        if comparison.first_failure >= 0:
            print(f"  First failure: step {comparison.first_failure}")
