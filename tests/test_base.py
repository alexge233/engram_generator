"""Tests for the engram generator base classes and infrastructure."""
import pytest

from engram_generator.base import Sample, Atom, StepGenerator, STEP_TOKEN
from engram_generator.tokenizer import CharTokenizer
from engram_generator.curriculum.registry import get_all_generators, get_generator, list_tasks
from engram_generator.curriculum.skill_tree import SkillTree
from engram_generator.parallel import ParallelGenerator


class TestSample:
    """Tests for the Sample dataclass."""

    def test_required_fields(self) -> None:
        """Verify required fields are set on construction."""
        s = Sample(input_text="test", target_text="result", difficulty=3)
        assert s.input_text == "test"
        assert s.target_text == "result"
        assert s.difficulty == 3

    def test_default_fields(self) -> None:
        """Verify optional fields have correct defaults."""
        s = Sample(input_text="", target_text="", difficulty=1)
        assert s.task_name == ""
        assert s.tier == 0
        assert s.steps == []
        assert s.answer == ""


class TestAtom:
    """Tests for the Atom dataclass."""

    def test_construction(self) -> None:
        """Verify atom fields are set correctly."""
        a = Atom(
            atom_type="theorem", name="chain rule",
            content="f(g(x))' = f'(g(x))g'(x)",
            tier=5, domain="calculus",
        )
        assert a.atom_type == "theorem"
        assert a.tier == 5


class TestCharTokenizer:
    """Tests for the character-level tokenizer."""

    def test_vocab_size(self) -> None:
        """Verify vocabulary size includes all tokens."""
        tok = CharTokenizer()
        assert tok.vocab_size > 50

    def test_special_tokens(self) -> None:
        """Verify special token IDs are distinct."""
        tok = CharTokenizer()
        ids = {tok.pad_token_id, tok.eos_token_id, tok.step_token_id}
        assert len(ids) == 3

    def test_roundtrip(self) -> None:
        """Verify encode-decode roundtrip preserves text."""
        tok = CharTokenizer()
        text = "3x^2 + 2x - 5"
        decoded = tok.decode(tok.encode(text))
        assert decoded == text

    def test_step_token_encoding(self) -> None:
        """Verify <step> is encoded as a single token."""
        tok = CharTokenizer()
        ids = tok.encode(f"a {STEP_TOKEN} b")
        assert tok.step_token_id in ids

    def test_step_mask(self) -> None:
        """Verify step mask correctly identifies <step> positions."""
        tok = CharTokenizer()
        ids = tok.encode(f"a {STEP_TOKEN} b")
        mask = tok.get_step_mask(ids)
        step_count = sum(mask)
        assert step_count == 1

    def test_latex_roundtrip(self) -> None:
        """Verify LaTeX notation survives roundtrip."""
        tok = CharTokenizer()
        text = "\\frac{1}{2}mv^2"
        decoded = tok.decode(tok.encode(text))
        assert decoded == text


class TestRegistry:
    """Tests for the generator registry."""

    def test_all_generators_registered(self) -> None:
        """Verify all generators are accessible."""
        gens = get_all_generators()
        assert len(gens) >= 90

    def test_get_by_name(self) -> None:
        """Verify individual generator retrieval."""
        gen = get_generator("addition")
        assert gen.task_name == "addition"

    def test_unknown_name_raises(self) -> None:
        """Verify KeyError for unknown task names."""
        with pytest.raises(KeyError):
            get_generator("nonexistent_task")

    def test_list_tasks_sorted(self) -> None:
        """Verify task list is sorted by tier then name."""
        tasks = list_tasks()
        tiers = [t["tier"] for t in tasks]
        assert tiers == sorted(tiers)

    def test_all_have_tier(self) -> None:
        """Verify every generator has a valid tier."""
        for gen in get_all_generators():
            assert 0 <= gen.tier <= 10


class TestGeneratorContract:
    """Tests that all generators satisfy the StepGenerator contract."""

    @pytest.fixture
    def all_generators(self) -> list[StepGenerator]:
        """Return all registered generators."""
        return get_all_generators()

    def test_all_produce_samples(self, all_generators: list[StepGenerator]) -> None:
        """Verify every generator produces valid samples."""
        for gen in all_generators:
            samples = gen.generate(1)
            assert len(samples) == 1
            assert samples[0].input_text
            assert samples[0].target_text

    def test_all_have_step_tokens(self, all_generators: list[StepGenerator]) -> None:
        """Verify every target contains at least one <step> token."""
        for gen in all_generators:
            s = gen.generate(1)[0]
            assert STEP_TOKEN in s.target_text, f"{gen.task_name} missing <step>"

    def test_all_have_answers(self, all_generators: list[StepGenerator]) -> None:
        """Verify every sample has a non-empty answer."""
        for gen in all_generators:
            s = gen.generate(1)[0]
            assert s.answer, f"{gen.task_name} has empty answer"

    def test_all_have_task_name(self, all_generators: list[StepGenerator]) -> None:
        """Verify every sample's task_name matches the generator."""
        for gen in all_generators:
            s = gen.generate(1)[0]
            assert s.task_name == gen.task_name

    def test_all_tokenize_cleanly(self, all_generators: list[StepGenerator]) -> None:
        """Verify all samples roundtrip through the tokenizer."""
        tok = CharTokenizer()
        for gen in all_generators:
            s = gen.generate(1)[0]
            decoded = tok.decode(tok.encode(s.target_text))
            clean_target = s.target_text.replace(f" {STEP_TOKEN} ", STEP_TOKEN)
            clean_decoded = decoded.replace(f" {STEP_TOKEN} ", STEP_TOKEN)
            assert clean_decoded == clean_target, (
                f"{gen.task_name}: roundtrip mismatch"
            )

    def test_deterministic_with_seed(self, all_generators: list[StepGenerator]) -> None:
        """Verify generators are deterministic with same seed."""
        for gen in all_generators:
            gen1 = type(gen)(seed=99)
            gen2 = type(gen)(seed=99)
            s1 = gen1.generate(1)[0]
            s2 = gen2.generate(1)[0]
            assert s1.target_text == s2.target_text, (
                f"{gen.task_name}: not deterministic"
            )


class TestSkillTree:
    """Tests for the adaptive skill tree."""

    def test_tier0_unlocked_by_default(self) -> None:
        """Verify tier 0 tasks are unlocked initially."""
        gens = get_all_generators()
        tree = SkillTree(gens)
        unlocked = tree.get_unlocked_tasks()
        for gen in gens:
            if gen.tier == 0 and not gen.prerequisites:
                assert gen.task_name in unlocked

    def test_escalation(self) -> None:
        """Verify difficulty escalates when accuracy is high."""
        gens = get_all_generators()
        tree = SkillTree(gens)
        events = tree.update({"addition": 0.97})
        assert "addition" in events

    def test_mastery(self) -> None:
        """Verify tasks are marked as mastered at threshold."""
        gens = get_all_generators()
        tree = SkillTree(gens)
        tree.update({"addition": 0.95})
        mastered = tree.get_mastered_tasks()
        assert "addition" in mastered

    def test_prerequisite_unlocking(self) -> None:
        """Verify children unlock when prerequisites are mastered."""
        gens = get_all_generators()
        tree = SkillTree(gens)
        tree.update({"addition": 0.95})
        unlocked = tree.get_unlocked_tasks()
        assert "multiplication" in unlocked or "fibonacci" in unlocked

    def test_summary(self) -> None:
        """Verify summary contains expected keys."""
        gens = get_all_generators()
        tree = SkillTree(gens)
        summary = tree.summary()
        assert "total" in summary
        assert "unlocked" in summary
        assert "mastered" in summary
        assert "frontier" in summary


class TestParallelGenerator:
    """Tests for parallel sample generation."""

    def test_correct_count(self) -> None:
        """Verify parallel generation produces the right number of samples."""
        from engram_generator.generators.tier0 import AdditionGenerator
        pg = ParallelGenerator(max_workers=2)
        samples = pg.generate(AdditionGenerator, num_samples=100)
        assert len(samples) == 100

    def test_all_valid_samples(self) -> None:
        """Verify all parallel samples have valid fields."""
        from engram_generator.generators.tier0 import AdditionGenerator
        pg = ParallelGenerator(max_workers=2)
        samples = pg.generate(AdditionGenerator, num_samples=50)
        for s in samples:
            assert s.answer
            assert STEP_TOKEN in s.target_text

    def test_mixed_generation(self) -> None:
        """Verify mixed parallel generation across task types."""
        from engram_generator.generators.tier0 import AdditionGenerator, SubtractionGenerator
        pg = ParallelGenerator(max_workers=2)
        samples = pg.generate_mixed(
            [AdditionGenerator, SubtractionGenerator],
            samples_per_task=25,
        )
        assert len(samples) == 50
        task_names = {s.task_name for s in samples}
        assert "addition" in task_names
        assert "subtraction" in task_names
