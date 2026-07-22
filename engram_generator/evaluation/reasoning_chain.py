"""Reasoning chain: parsed step-by-step solution with comparison methods.

Wraps a raw target string (with <step> delimiters) into a structured
object that supports step-level comparison, normalisation, and
alignment between ground truth and model output.
"""
from dataclasses import dataclass, field

from engram_generator.base import STEP_TOKEN
from engram_generator.evaluation.normaliser import OperationNormaliser


@dataclass
class StepComparison:
    """Result of comparing one step between expected and predicted.

    Attributes:
        position: Step index (0-based).
        expected: Ground truth step (raw).
        predicted: Model output step (raw), or None if missing.
        expected_normalised: Normalised ground truth.
        predicted_normalised: Normalised prediction.
        correct: Whether the normalised forms match.
    """

    position: int
    expected: str
    predicted: str | None
    expected_normalised: str
    predicted_normalised: str | None
    correct: bool


@dataclass
class ChainComparison:
    """Result of comparing two full reasoning chains.

    Attributes:
        steps: Per-step comparison results.
        first_failure: Index of first wrong step, or -1 if all correct.
        final_answer_correct: Whether the last step matches.
        step_accuracy: Fraction of correct steps.
        chain_correct: Whether every step is correct.
        num_expected: Total expected steps.
        num_predicted: Total predicted steps.
        expected_answer: Ground truth final answer.
        predicted_answer: Model's final answer.
    """

    steps: list[StepComparison]
    first_failure: int
    final_answer_correct: bool
    step_accuracy: float
    chain_correct: bool
    num_expected: int
    num_predicted: int
    expected_answer: str
    predicted_answer: str
    rouge_l: float = 0.0
    mean_step_similarity: float = 0.0
    step_recall: float = 0.0
    step_precision: float = 0.0


class ReasoningChain:
    """A parsed reasoning chain from a <step>-delimited string.

    Splits a target string into problem, intermediate steps, and
    final answer. Provides comparison against another chain with
    commutativity-aware normalisation.

    Attributes:
        problem: The problem statement (first segment).
        steps: Intermediate reasoning steps.
        answer: Final answer (last segment).
        raw: The original unsplit string.
    """

    def __init__(
        self,
        text: str,
        normaliser: OperationNormaliser | None = None,
        has_problem: bool = True,
    ):
        """Parse a <step>-delimited string into a reasoning chain.

        Args:
            text: Full target string with <step> delimiters.
            normaliser: Custom normaliser, or None for default.
            has_problem: If True (default), first segment is the problem
                statement. If False, all segments are reasoning steps
                (use for LLM outputs that don't repeat the problem).
        """
        self._normaliser = normaliser or OperationNormaliser()
        self._raw = text
        import re
        parts = [p.strip() for p in re.split(
            r'\s*' + re.escape(STEP_TOKEN) + r'\s*', text,
        ) if p.strip()]

        if not has_problem:
            self._problem = ""
            self._steps = parts[:-1] if len(parts) > 1 else []
            self._answer = parts[-1] if parts else ""
        elif len(parts) >= 2:
            self._problem = parts[0]
            self._steps = parts[1:-1]
            self._answer = parts[-1]
        elif len(parts) == 1:
            self._problem = ""
            self._steps = []
            self._answer = parts[0]
        else:
            self._problem = ""
            self._steps = []
            self._answer = ""

    @property
    def problem(self) -> str:
        """Return the problem statement."""
        return self._problem

    @property
    def steps(self) -> list[str]:
        """Return intermediate reasoning steps."""
        return self._steps

    @property
    def answer(self) -> str:
        """Return the final answer."""
        return self._answer

    @property
    def raw(self) -> str:
        """Return the original string."""
        return self._raw

    @property
    def all_segments(self) -> list[str]:
        """Return all segments: [problem, *steps, answer]."""
        parts = []
        if self._problem:
            parts.append(self._problem)
        parts.extend(self._steps)
        if self._answer:
            parts.append(self._answer)
        return parts

    @property
    def reasoning_segments(self) -> list[str]:
        """Return reasoning steps + answer (no problem statement)."""
        parts = list(self._steps)
        if self._answer:
            parts.append(self._answer)
        return parts

    def compare(
        self, predicted: "ReasoningChain", skip_problem: bool = True,
    ) -> ChainComparison:
        """Compare this chain (ground truth) against a predicted chain.

        Args:
            predicted: Model's output chain.
            skip_problem: If True, compare reasoning steps only
                (skip the problem statement). Default True because
                LLMs typically don't repeat the problem.

        Returns:
            ChainComparison with per-step results.
        """
        expected_parts = self.reasoning_segments if skip_problem else self.all_segments

        if skip_problem and predicted.problem:
            predicted_parts = predicted.reasoning_segments
        elif skip_problem:
            predicted_parts = predicted.all_segments
        else:
            predicted_parts = predicted.all_segments

        step_comparisons = []
        first_failure = -1

        for i in range(len(expected_parts)):
            exp = expected_parts[i]
            pred = predicted_parts[i] if i < len(predicted_parts) else None

            exp_norm = self._normaliser.normalise(exp)
            pred_norm = self._normaliser.normalise(pred) if pred else None

            correct = exp_norm == pred_norm if pred_norm is not None else False

            if not correct and first_failure == -1:
                first_failure = i

            step_comparisons.append(StepComparison(
                position=i,
                expected=exp,
                predicted=pred,
                expected_normalised=exp_norm,
                predicted_normalised=pred_norm,
                correct=correct,
            ))

        exp_answer = self._normaliser.normalise(self._answer)
        pred_answer = self._normaliser.normalise(predicted.answer)
        final_correct = exp_answer == pred_answer

        num_correct = sum(s.correct for s in step_comparisons)
        total = len(step_comparisons)

        exp_normalised = self._normaliser.normalise_chain(expected_parts)
        pred_normalised = self._normaliser.normalise_chain(predicted_parts)

        rouge = OperationNormaliser.rouge_l(exp_normalised, pred_normalised)

        similarities = []
        for i in range(min(len(expected_parts), len(predicted_parts))):
            sim = self._normaliser.step_similarity(
                expected_parts[i], predicted_parts[i],
            )
            similarities.append(sim)
        mean_sim = (
            sum(similarities) / len(similarities) if similarities else 0.0
        )

        step_recall = (
            num_correct / len(expected_parts)
            if expected_parts else 0.0
        )
        step_precision = (
            num_correct / len(predicted_parts)
            if predicted_parts else 0.0
        )

        return ChainComparison(
            steps=step_comparisons,
            first_failure=first_failure,
            final_answer_correct=final_correct,
            step_accuracy=num_correct / total if total > 0 else 0.0,
            chain_correct=first_failure == -1 and total > 0,
            num_expected=len(expected_parts),
            num_predicted=len(predicted_parts),
            expected_answer=self._answer,
            predicted_answer=predicted.answer,
            rouge_l=rouge,
            mean_step_similarity=mean_sim,
            step_recall=step_recall,
            step_precision=step_precision,
        )
