"""Targeted tests for uncovered code paths across all modules."""
import pytest

from engram_generator.base import StepGenerator, STEP_TOKEN
from engram_generator.curriculum.registry import get_all_generators, get_generator
from engram_generator.curriculum.skill_tree import SkillTree, SkillNode
from engram_generator.tokenizer import CharTokenizer
from engram_generator.parallel import ParallelGenerator


class TestBaseEdgeCases:
    """Cover edge cases in base.py."""

    def test_max_difficulty_property(self) -> None:
        """Verify max_difficulty property returns correct value."""
        gen = get_generator("addition", min_difficulty=3, max_difficulty=7)
        assert gen.max_difficulty == 7

    def test_min_difficulty_property(self) -> None:
        """Verify min_difficulty property returns correct value."""
        gen = get_generator("addition", min_difficulty=3, max_difficulty=7)
        assert gen.min_difficulty == 3


class TestSkillTreeEdgeCases:
    """Cover uncovered branches in skill_tree.py."""

    def test_update_unknown_task_ignored(self) -> None:
        """Verify updating an unknown task name is silently ignored."""
        gens = get_all_generators()
        tree = SkillTree(gens)
        events = tree.update({"nonexistent_task_xyz": 0.99})
        assert "nonexistent_task_xyz" not in events

    def test_update_locked_task_ignored(self) -> None:
        """Verify updating a locked task records accuracy but doesn't escalate."""
        gens = get_all_generators()
        tree = SkillTree(gens)
        locked_tasks = [
            g.task_name for g in gens
            if g.task_name not in tree.get_unlocked_tasks()
        ]
        if locked_tasks:
            events = tree.update({locked_tasks[0]: 0.99})
            assert locked_tasks[0] not in events

    def test_low_accuracy_gets_frontier_weight(self) -> None:
        """Verify a task with < 50% accuracy gets 3x weight."""
        gens = get_all_generators()
        tree = SkillTree(gens)
        tree.update({"addition": 0.3})
        weights = tree.get_sampling_weights()
        assert weights["addition"] == 3.0

    def test_get_difficulty_unknown_task(self) -> None:
        """Verify get_difficulty_for returns 1 for unknown task."""
        gens = get_all_generators()
        tree = SkillTree(gens)
        assert tree.get_difficulty_for("totally_unknown") == 1

    def test_skill_node_defaults(self) -> None:
        """Verify SkillNode has sensible defaults."""
        node = SkillNode(task_name="test")
        assert node.tier == 0
        assert node.current_difficulty == 1
        assert not node.unlocked
        assert not node.mastered


class TestTokenizerEdgeCases:
    """Cover uncovered branch in tokenizer.py."""

    def test_unknown_char_skipped(self) -> None:
        """Verify characters not in vocabulary are silently skipped."""
        tok = CharTokenizer()
        ids = tok.encode("abc\x00def")
        decoded = tok.decode(ids)
        assert decoded == "abcdef"


class TestParallelEdgeCases:
    """Cover uncovered branches in parallel.py."""

    def test_generate_mixed_empty_list(self) -> None:
        """Verify empty generator list returns empty samples."""
        pg = ParallelGenerator(max_workers=2)
        samples = pg.generate_mixed([], samples_per_task=10)
        assert samples == []


class TestGeneratorDifficultyEdgeCases:
    """Test generators at extreme difficulties to cover branch paths.

    Many uncovered lines are edge cases that only trigger at
    specific difficulty levels (e.g., 3x3 matrices at d>=5,
    negative coefficients, special formula paths).
    """

    @pytest.fixture(scope="class")
    def all_generators(self) -> list:
        """Return all generators."""
        return get_all_generators()

    def test_all_at_difficulty_1(self, all_generators) -> None:
        """Generate at minimum difficulty for each generator."""
        for gen in all_generators:
            gen.set_difficulty(1, 1)
            samples = gen.generate(5)
            for s in samples:
                assert s.answer, f"{gen.task_name} d=1 empty answer"

    def test_all_at_difficulty_8(self, all_generators) -> None:
        """Generate at maximum difficulty for each generator."""
        for gen in all_generators:
            gen.set_difficulty(8, 8)
            samples = gen.generate(5)
            for s in samples:
                assert s.answer, f"{gen.task_name} d=8 empty answer"

    def test_all_at_difficulty_4(self, all_generators) -> None:
        """Generate at mid difficulty — triggers many branch transitions."""
        for gen in all_generators:
            gen.set_difficulty(4, 4)
            samples = gen.generate(5)
            for s in samples:
                assert s.answer, f"{gen.task_name} d=4 empty answer"

    def test_all_at_difficulty_6(self, all_generators) -> None:
        """Generate at difficulty 6 — triggers 3x3 matrices, larger graphs."""
        for gen in all_generators:
            gen.set_difficulty(6, 6)
            samples = gen.generate(5)
            for s in samples:
                assert s.answer, f"{gen.task_name} d=6 empty answer"

    def test_high_volume_per_generator(self, all_generators) -> None:
        """Generate 20 samples per generator to hit rare branches."""
        failures: list[str] = []
        for gen in all_generators:
            gen.set_difficulty(1, 8)
            try:
                samples = gen.generate(20)
                for s in samples:
                    if not s.answer:
                        failures.append(f"{gen.task_name}: empty answer")
                    if STEP_TOKEN not in s.target_text:
                        failures.append(f"{gen.task_name}: missing <step>")
            except Exception as e:
                failures.append(f"{gen.task_name}: {type(e).__name__}: {e}")

        assert not failures, f"{len(failures)} failures:\n" + "\n".join(failures[:20])


class TestCLIDirectImport:
    """Test CLI functions directly to get coverage on cli.py."""

    def test_validate_task_returns_dict(self) -> None:
        """Verify validate_task returns a results dict."""
        from engram_generator.cli import validate_task
        results = validate_task("addition", 5, None, 128, 256, False)
        assert results["task"] == "addition"
        assert results["generated"] == 5
        assert results["format_ok"] == 5

    def test_validate_task_with_difficulty(self) -> None:
        """Verify validate_task with difficulty override."""
        from engram_generator.cli import validate_task
        results = validate_task("subtraction", 3, 5, 128, 256, False)
        assert results["generated"] == 3

    def test_validate_task_verbose(self, capsys) -> None:
        """Verify verbose mode prints sample details."""
        from engram_generator.cli import validate_task
        validate_task("addition", 3, None, 128, 256, True)
        captured = capsys.readouterr()
        assert "Input:" in captured.out

    def test_print_results_pass(self, capsys) -> None:
        """Verify print_results reports PASS for valid results."""
        from engram_generator.cli import print_results
        results = {
            "task": "test", "tier": 0, "generated": 5,
            "format_ok": 5, "tokens_ok": 5,
            "input_length_ok": 5, "target_length_ok": 5,
            "has_steps": 5, "has_answer": 5,
            "gen_time_ms": 1.0, "max_input_tokens": 20,
            "max_target_tokens": 50, "errors": [],
        }
        passed = print_results(results)
        assert passed

    def test_print_results_fail(self, capsys) -> None:
        """Verify print_results reports FAIL for invalid results."""
        from engram_generator.cli import print_results
        results = {
            "task": "test", "tier": 0, "generated": 5,
            "format_ok": 3, "tokens_ok": 5,
            "input_length_ok": 5, "target_length_ok": 5,
            "has_steps": 5, "has_answer": 5,
            "gen_time_ms": 1.0, "max_input_tokens": 20,
            "max_target_tokens": 50,
            "errors": ["sample 0: missing step", "sample 1: missing step"],
        }
        passed = print_results(results)
        assert not passed

    def test_print_skill_tree(self, capsys) -> None:
        """Verify _print_skill_tree outputs tier structure."""
        from engram_generator.cli import _print_skill_tree
        _print_skill_tree()
        captured = capsys.readouterr()
        assert "TIER" in captured.out
        assert "addition" in captured.out
