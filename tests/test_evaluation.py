"""Tests for the reasoning evaluation module."""
import pytest

from engram_generator.evaluation.normaliser import OperationNormaliser
from engram_generator.evaluation.reasoning_chain import ReasoningChain
from engram_generator.evaluation.metrics import ReasoningMetrics


class TestOperationNormaliser:
    """Tests for step normalisation."""

    def setup_method(self):
        """Create a normaliser for each test."""
        self.n = OperationNormaliser()

    def test_pure_integer(self):
        """Integer strings pass through."""
        assert self.n.normalise("339") == "339"

    def test_float_to_int(self):
        """Float equal to integer normalises to int."""
        assert self.n.normalise("125.0") == "125"
        assert self.n.normalise("125.000") == "125"

    def test_float_stays_float(self):
        """Non-integer float stays as-is."""
        assert self.n.normalise("123.89") == "123.89"

    def test_commutative_multiplication(self):
        """Multiplication operands are sorted."""
        assert self.n.normalise("9*3=27") == "3*9=27"
        assert self.n.normalise("3*9=27") == "3*9=27"

    def test_commutative_addition(self):
        """Addition operands are sorted."""
        assert self.n.normalise("2+1=3") == "1+2=3"

    def test_commutative_multi_operand(self):
        """Multi-operand addition is sorted."""
        assert self.n.normalise("2+1+1=4") == "1+1+2=4"
        assert self.n.normalise("1+2+1=4") == "1+1+2=4"

    def test_non_commutative_division(self):
        """Division stays ordered."""
        assert self.n.normalise("5/13=0r5") == "5/13=0r5"

    def test_non_commutative_mod(self):
        """Modular stays ordered."""
        assert self.n.normalise("48\\mod18=12") == "48\\mod18=12"

    def test_subtraction_stays_ordered(self):
        """Subtraction stays ordered."""
        assert self.n.normalise("9-3=6") == "9-3=6"

    def test_whitespace_stripped(self):
        """Whitespace is removed."""
        assert self.n.normalise(" 3 * 9 = 27 ") == "3*9=27"

    def test_commas_stripped(self):
        """Commas are removed."""
        assert self.n.normalise("1,234") == "1234"

    def test_empty_string(self):
        """Empty string returns empty."""
        assert self.n.normalise("") == ""

    def test_steps_match(self):
        """steps_match correctly identifies equivalent steps."""
        assert self.n.steps_match("3*9=27", "9*3=27")
        assert not self.n.steps_match("3*9=27", "3*9=28")

    def test_mixed_ops_no_sort(self):
        """Mixed operators prevent sorting."""
        result = self.n.normalise("3+4*2=14")
        assert result == "3+4*2=14"


class TestReasoningChain:
    """Tests for reasoning chain parsing and comparison."""

    def test_parse_full_chain(self):
        """Parses problem, steps, and answer."""
        chain = ReasoningChain(
            "214 + 125 <step> 4+5=9 <step> 1+2=3 <step> 2+1=3 <step> 339"
        )
        assert chain.problem == "214 + 125"
        assert chain.steps == ["4+5=9", "1+2=3", "2+1=3"]
        assert chain.answer == "339"

    def test_parse_answer_only(self):
        """Single value parses as answer."""
        chain = ReasoningChain("42")
        assert chain.problem == ""
        assert chain.steps == []
        assert chain.answer == "42"

    def test_all_segments(self):
        """all_segments returns everything."""
        chain = ReasoningChain("a <step> b <step> c <step> d")
        assert chain.all_segments == ["a", "b", "c", "d"]

    def test_reasoning_segments(self):
        """reasoning_segments excludes the problem."""
        chain = ReasoningChain("a <step> b <step> c <step> d")
        assert chain.reasoning_segments == ["b", "c", "d"]

    def test_compare_perfect(self):
        """Perfect match produces all-correct comparison."""
        gt = ReasoningChain(
            "214 + 125 <step> 4+5=9 <step> 1+2=3 <step> 339"
        )
        pred = ReasoningChain(
            "214 + 125 <step> 4+5=9 <step> 1+2=3 <step> 339"
        )
        result = gt.compare(pred)
        assert result.chain_correct
        assert result.final_answer_correct
        assert result.first_failure == -1

    def test_compare_wrong_step(self):
        """Wrong intermediate step is detected."""
        gt = ReasoningChain("a <step> 4+5=9 <step> 1+2=3 <step> 339")
        pred = ReasoningChain("a <step> 4+5=8 <step> 1+2=3 <step> 339")
        result = gt.compare(pred)
        assert not result.chain_correct
        assert result.first_failure == 0
        assert result.final_answer_correct

    def test_compare_commutative(self):
        """Commutative steps match after normalisation."""
        gt = ReasoningChain("a <step> 3*9=27 <step> 27")
        pred = ReasoningChain("a <step> 9*3=27 <step> 27")
        result = gt.compare(pred)
        assert result.chain_correct
        assert result.step_accuracy == 1.0

    def test_compare_skip_problem(self):
        """skip_problem drops the problem from comparison."""
        gt = ReasoningChain("214 + 125 <step> 4+5=9 <step> 1+2=3 <step> 339")
        pred = ReasoningChain(
            "4+5=9 <step> 1+2=3 <step> 339", has_problem=False,
        )
        result = gt.compare(pred, skip_problem=True)
        assert result.chain_correct

    def test_compare_missing_steps(self):
        """Missing predicted steps are marked as failures."""
        gt = ReasoningChain("a <step> step1 <step> step2 <step> 42")
        pred = ReasoningChain("a <step> 42")
        result = gt.compare(pred, skip_problem=True)
        assert not result.chain_correct
        assert result.final_answer_correct

    def test_compare_right_answer_wrong_reasoning(self):
        """Right final answer but wrong intermediate steps."""
        gt = ReasoningChain("a <step> 9*3=27 <step> 27*3=81 <step> 81")
        pred = ReasoningChain("a <step> 3*3=9 <step> 9*9=81 <step> 81")
        result = gt.compare(pred)
        assert result.final_answer_correct
        assert not result.chain_correct


class TestReasoningMetrics:
    """Tests for aggregate reasoning metrics."""

    def setup_method(self):
        """Create a metrics instance for each test."""
        self.metrics = ReasoningMetrics()

    def test_single_sample(self):
        """Evaluate a single sample."""
        result = self.metrics.evaluate_sample(
            "a <step> 1+2=3 <step> 3",
            "a <step> 1+2=3 <step> 3",
        )
        assert result.chain_correct
        assert result.final_answer_correct

    def test_batch_evaluation(self):
        """Evaluate a batch with mixed results."""
        report = self.metrics.evaluate(
            [
                "a <step> 1+2=3 <step> 3",
                "b <step> 4+5=9 <step> 9",
                "c <step> 7+8=15 <step> 15",
            ],
            [
                "a <step> 1+2=3 <step> 3",
                "b <step> 4+5=8 <step> 8",
                "c <step> 7+8=15 <step> 15",
            ],
        )
        assert report.total_samples == 3
        assert report.final_answer_accuracy == pytest.approx(2 / 3, abs=0.01)
        assert report.perfect_chains == pytest.approx(2 / 3, abs=0.01)

    def test_position_accuracy(self):
        """Per-position accuracy is computed correctly."""
        report = self.metrics.evaluate(
            [
                "a <step> s1 <step> s2 <step> ans",
                "b <step> s1 <step> s2 <step> ans",
            ],
            [
                "a <step> s1 <step> wrong <step> ans",
                "b <step> s1 <step> s2 <step> ans",
            ],
        )
        assert report.step_accuracy_by_position[0] == 1.0
        assert report.step_accuracy_by_position[1] == 0.5
        assert report.step_accuracy_by_position[2] == 1.0

    def test_to_dict(self):
        """Report serialises to dict."""
        report = self.metrics.evaluate(
            ["a <step> 1 <step> 2"],
            ["a <step> 1 <step> 2"],
        )
        d = report.to_dict()
        assert "final_answer_accuracy" in d
        assert "mean_step_accuracy" in d
        assert "step_accuracy_by_position" in d

    def test_empty_batch(self):
        """Empty batch produces zero report."""
        report = self.metrics.evaluate([], [])
        assert report.total_samples == 0


class TestStepGeneratorNormalise:
    """Tests for base StepGenerator.normalise_step()."""

    def test_generator_normalise(self):
        """Generator exposes normalise_step via base class."""
        from engram_generator.curriculum.registry import get_all_generators
        gens = get_all_generators()
        gen = gens[0]
        assert gen.normalise_step("9*3=27") == "3*9=27"

    def test_generator_parse_chain(self):
        """Generator can parse a target text into a chain."""
        from engram_generator.curriculum.registry import get_all_generators
        gens = get_all_generators()
        gen = gens[0]
        chain = gen.parse_chain("a <step> b <step> c")
        assert chain.problem == "a"
        assert chain.steps == ["b"]
        assert chain.answer == "c"
