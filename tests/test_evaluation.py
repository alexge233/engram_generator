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


class TestLevenshteinAndRouge:
    """Tests for Levenshtein distance, step similarity, and ROUGE-L."""

    def setup_method(self):
        """Create a normaliser for each test."""
        self.n = OperationNormaliser()

    def test_levenshtein_identical(self):
        """Identical strings have zero distance."""
        assert self.n.levenshtein("abc", "abc") == 0

    def test_levenshtein_one_edit(self):
        """One character difference is distance 1."""
        assert self.n.levenshtein("abc", "adc") == 1

    def test_levenshtein_empty(self):
        """Empty vs non-empty is length of the other."""
        assert self.n.levenshtein("", "abc") == 3

    def test_step_similarity_exact(self):
        """Exact match is 1.0."""
        assert self.n.step_similarity("3*9=27", "9*3=27") == 1.0

    def test_step_similarity_partial(self):
        """Near-miss is between 0 and 1."""
        sim = self.n.step_similarity("4+5=9", "4+5=8")
        assert 0.5 < sim < 1.0

    def test_step_similarity_completely_different(self):
        """Totally different strings are near 0."""
        sim = self.n.step_similarity("abc", "xyz")
        assert sim < 0.5

    def test_rouge_l_identical(self):
        """Identical sequences score 1.0."""
        assert self.n.rouge_l(["a", "b", "c"], ["a", "b", "c"]) == 1.0

    def test_rouge_l_partial(self):
        """Partial overlap scores between 0 and 1."""
        score = self.n.rouge_l(["a", "b", "c", "d"], ["a", "c", "d"])
        assert 0.5 < score < 1.0

    def test_rouge_l_no_overlap(self):
        """No common subsequence scores 0."""
        assert self.n.rouge_l(["a", "b"], ["c", "d"]) == 0.0

    def test_rouge_l_empty(self):
        """Empty input scores 0."""
        assert self.n.rouge_l([], ["a"]) == 0.0


class TestChainMetrics:
    """Tests for ROUGE-L, similarity, recall, precision on chains."""

    def test_perfect_chain_metrics(self):
        """Perfect chain has all metrics at 1.0."""
        gt = ReasoningChain("a <step> 1+2=3 <step> 3")
        pred = ReasoningChain("a <step> 1+2=3 <step> 3")
        r = gt.compare(pred, skip_problem=True)
        assert r.rouge_l == 1.0
        assert r.mean_step_similarity == 1.0
        assert r.step_recall == 1.0
        assert r.step_precision == 1.0

    def test_partial_chain_metrics(self):
        """Wrong step reduces similarity but not to zero."""
        gt = ReasoningChain("a <step> 4+5=9 <step> 1+2=3 <step> 339")
        pred = ReasoningChain("a <step> 4+5=9 <step> 1+2=4 <step> 349")
        r = gt.compare(pred, skip_problem=True)
        assert 0.0 < r.rouge_l < 1.0
        assert 0.0 < r.mean_step_similarity < 1.0

    def test_report_includes_new_metrics(self):
        """Report includes ROUGE-L and similarity."""
        metrics = ReasoningMetrics()
        report = metrics.evaluate(
            ["a <step> x <step> y"],
            ["a <step> x <step> y"],
        )
        d = report.to_dict()
        assert "mean_rouge_l" in d
        assert "mean_step_similarity" in d
        assert "mean_step_recall" in d
        assert "mean_step_precision" in d


class TestWhitespaceHandling:
    """Tests for whitespace-insensitive step parsing."""

    def test_no_spaces_around_step(self):
        """Parses correctly without spaces around <step>."""
        chain = ReasoningChain("a<step>b<step>c")
        assert chain.problem == "a"
        assert chain.steps == ["b"]
        assert chain.answer == "c"

    def test_extra_whitespace(self):
        """Parses correctly with irregular whitespace."""
        chain = ReasoningChain("a  <step>  b  <step>  c")
        assert chain.problem == "a"
        assert chain.steps == ["b"]
        assert chain.answer == "c"

    def test_newlines_around_step(self):
        """Parses correctly with newlines around delimiter."""
        chain = ReasoningChain("a\n<step>\nb\n<step>\nc")
        assert chain.problem == "a"
        assert chain.steps == ["b"]
        assert chain.answer == "c"


class TestPredictedHasProblem:
    """Tests for predicted_has_problem in metrics."""

    def test_evaluate_sample_no_problem(self):
        """LLM output without problem parses correctly."""
        metrics = ReasoningMetrics()
        result = metrics.evaluate_sample(
            "214 + 125 <step> 4+5=9 <step> 1+2=3 <step> 339",
            "4+5=9 <step> 1+2=3 <step> 339",
            skip_problem=True,
            predicted_has_problem=False,
        )
        assert result.chain_correct

    def test_evaluate_batch_no_problem(self):
        """Batch evaluation with predicted_has_problem=False."""
        metrics = ReasoningMetrics()
        report = metrics.evaluate(
            ["a <step> 1+2=3 <step> 3"],
            ["1+2=3 <step> 3"],
            skip_problem=True,
            predicted_has_problem=False,
        )
        assert report.perfect_chains == 1.0

    def test_evaluate_length_mismatch_raises(self):
        """Mismatched list lengths raise ValueError."""
        metrics = ReasoningMetrics()
        with pytest.raises(ValueError, match="Expected 2"):
            metrics.evaluate(["a", "b"], ["c"])


class TestStepGeneratorNormalise:
    """Tests for base StepGenerator.normalise_step()."""

    def test_generator_normalise(self):
        """Generator exposes normalise_step via base class."""
        from engram_generator.curriculum.registry import get_all_generators
        gens = get_all_generators()
        gen = gens[0]
        assert gen.normalise_step("9*3=27") == "3*9=27"

    def test_generator_normalise_cached(self):
        """Normaliser is cached, not recreated per call."""
        from engram_generator.curriculum.registry import get_all_generators
        gens = get_all_generators()
        gen = gens[0]
        gen.normalise_step("1+2=3")
        gen.normalise_step("3*4=12")
        assert hasattr(gen, "_normaliser")

    def test_generator_parse_chain(self):
        """Generator can parse a target text into a chain."""
        from engram_generator.curriculum.registry import get_all_generators
        gens = get_all_generators()
        gen = gens[0]
        chain = gen.parse_chain("a <step> b <step> c")
        assert chain.problem == "a"
        assert chain.steps == ["b"]
        assert chain.answer == "c"

    def test_generator_parse_chain_no_problem(self):
        """Generator can parse without problem statement."""
        from engram_generator.curriculum.registry import get_all_generators
        gens = get_all_generators()
        gen = gens[0]
        chain = gen.parse_chain("b <step> c", has_problem=False)
        assert chain.problem == ""
        assert chain.steps == ["b"]
        assert chain.answer == "c"
