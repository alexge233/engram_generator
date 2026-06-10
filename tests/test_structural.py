"""Structural integrity tests for the engram generator curriculum.

Validates the skill tree graph properties, sample contracts, determinism,
and difficulty scaling across all 2022 registered generators. These tests
catch connectivity bugs, orphan tasks, dangling prerequisites, and
backwards cross-tier dependencies that would prevent the curriculum
from functioning correctly at training time.
"""
import re

import pytest

from engram_generator.base import StepGenerator, STEP_TOKEN
from engram_generator.curriculum.registry import get_all_generators


@pytest.fixture(scope="module")
def all_generators() -> list[StepGenerator]:
    """Return all registered generators, cached for the entire module.

    Returns:
        List of all 2022 StepGenerator instances with default settings.
    """
    return get_all_generators()


@pytest.fixture(scope="module")
def task_names(all_generators: list[StepGenerator]) -> set[str]:
    """Return the set of all registered task names.

    Args:
        all_generators: All generators from the fixture.

    Returns:
        Set of task name strings.
    """
    return {g.task_name for g in all_generators}


@pytest.fixture(scope="module")
def tier_map(all_generators: list[StepGenerator]) -> dict[str, int]:
    """Return a mapping from task name to tier.

    Args:
        all_generators: All generators from the fixture.

    Returns:
        Dict mapping task_name to tier int.
    """
    return {g.task_name: g.tier for g in all_generators}


class TestTierConsistency:
    """Verify all generators have valid tier assignments and prerequisites.

    The skill tree requires that every non-root task has prerequisites,
    all prerequisites point to real tasks, and no task depends on a
    higher-tier task (which would make it unreachable).
    """

    def test_no_orphans(self, all_generators: list[StepGenerator]) -> None:
        """Verify every tier > 0 generator has at least one prerequisite."""
        orphans = [
            g.task_name for g in all_generators
            if g.tier > 0 and not g.prerequisites
        ]
        assert orphans == [], f"Orphan generators (tier>0, no prereqs): {orphans}"

    def test_no_dangling_prereqs(self, all_generators: list[StepGenerator],
                                  task_names: set[str]) -> None:
        """Verify all prerequisites point to existing registered tasks."""
        dangling = [
            (g.task_name, p)
            for g in all_generators
            if g.prerequisites
            for p in g.prerequisites
            if p not in task_names
        ]
        assert dangling == [], f"Dangling prerequisites: {dangling}"

    def test_no_backwards_cross_tier(self, all_generators: list[StepGenerator],
                                      tier_map: dict[str, int]) -> None:
        """Verify no task depends on a prerequisite at a higher tier.

        A task at tier N requiring a prereq at tier N+k is unreachable
        because the prereq cannot be mastered before the task unlocks.
        """
        backwards = [
            (g.task_name, g.tier, p, tier_map[p])
            for g in all_generators
            if g.prerequisites
            for p in g.prerequisites
            if p in tier_map and tier_map[p] > g.tier
        ]
        assert backwards == [], f"Backwards cross-tier prereqs: {backwards}"

    def test_no_duplicate_names(self, all_generators: list[StepGenerator]) -> None:
        """Verify every task_name is unique across the registry."""
        from collections import Counter
        counts = Counter(g.task_name for g in all_generators)
        dupes = {n: c for n, c in counts.items() if c > 1}
        assert dupes == {}, f"Duplicate task names: {dupes}"

    def test_tier_range(self, all_generators: list[StepGenerator]) -> None:
        """Verify all tiers are in the valid range 0-10."""
        bad = [(g.task_name, g.tier) for g in all_generators
               if g.tier < 0 or g.tier > 10]
        assert bad == [], f"Generators with invalid tiers: {bad}"

    def test_every_tier_has_tasks(self, all_generators: list[StepGenerator]) -> None:
        """Verify tiers 0 through 10 each have at least one task."""
        tiers_present = {g.tier for g in all_generators}
        for t in range(11):
            assert t in tiers_present, f"Tier {t} has no generators"

    def test_total_count(self, all_generators: list[StepGenerator]) -> None:
        """Verify total generator count matches expectations."""
        assert len(all_generators) == 2022


class TestSampleContract:
    """Verify every generator produces structurally valid samples.

    Each sample must have non-empty input, target, and answer fields,
    contain at least one step token, and have a matching task name.
    """

    def test_all_produce_nonempty_input(self, all_generators: list[StepGenerator]) -> None:
        """Verify every generator produces a non-empty input_text."""
        for gen in all_generators:
            s = gen.generate(1)[0]
            assert s.input_text.strip(), f"{gen.task_name}: empty input_text"

    def test_all_produce_nonempty_target(self, all_generators: list[StepGenerator]) -> None:
        """Verify every generator produces a non-empty target_text."""
        for gen in all_generators:
            s = gen.generate(1)[0]
            assert s.target_text.strip(), f"{gen.task_name}: empty target_text"

    def test_all_produce_nonempty_answer(self, all_generators: list[StepGenerator]) -> None:
        """Verify every generator produces a non-empty answer."""
        for gen in all_generators:
            s = gen.generate(1)[0]
            assert s.answer, f"{gen.task_name}: empty answer"

    def test_all_contain_step_token(self, all_generators: list[StepGenerator]) -> None:
        """Verify every target contains at least one <step> token."""
        for gen in all_generators:
            s = gen.generate(1)[0]
            assert STEP_TOKEN in s.target_text, (
                f"{gen.task_name}: target missing <step>"
            )

    def test_task_name_matches_generator(self, all_generators: list[StepGenerator]) -> None:
        """Verify the sample's task_name matches its generator."""
        for gen in all_generators:
            s = gen.generate(1)[0]
            assert s.task_name == gen.task_name, (
                f"Expected {gen.task_name}, got {s.task_name}"
            )

    def test_difficulty_in_range(self, all_generators: list[StepGenerator]) -> None:
        """Verify sample difficulty is within the generator's range."""
        for gen in all_generators:
            s = gen.generate(1)[0]
            assert gen.min_difficulty <= s.difficulty <= gen.max_difficulty, (
                f"{gen.task_name}: difficulty {s.difficulty} outside "
                f"[{gen.min_difficulty}, {gen.max_difficulty}]"
            )


class TestDeterminism:
    """Verify generators are deterministic with identical seeds.

    Same seed must produce identical samples. Different seeds must
    produce different samples (with high probability).
    """

    def test_same_seed_same_output(self) -> None:
        """Verify two generators with the same seed produce identical output."""
        from engram_generator.generators.arithmetic_core import AdditionGenerator
        g1 = AdditionGenerator(seed=99)
        g2 = AdditionGenerator(seed=99)
        s1 = g1.generate(10)
        s2 = g2.generate(10)
        for a, b in zip(s1, s2):
            assert a.target_text == b.target_text

    def test_different_seed_different_output(self) -> None:
        """Verify two generators with different seeds produce different output."""
        from engram_generator.generators.arithmetic_core import AdditionGenerator
        g1 = AdditionGenerator(seed=1)
        g2 = AdditionGenerator(seed=2)
        s1 = g1.generate(10)
        s2 = g2.generate(10)
        targets1 = {s.target_text for s in s1}
        targets2 = {s.target_text for s in s2}
        assert targets1 != targets2


class TestDifficultyScaling:
    """Verify the difficulty parameter affects output complexity.

    Higher difficulty should, on average, produce longer targets
    (more digits, more steps, harder problems).
    """

    def test_higher_difficulty_longer_targets(self) -> None:
        """Verify difficulty 8 targets are longer than difficulty 1 on average."""
        from engram_generator.generators.arithmetic_core import AdditionGenerator
        easy = AdditionGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        hard = AdditionGenerator(min_difficulty=8, max_difficulty=8, seed=42)
        easy_avg = sum(len(s.target_text) for s in easy.generate(50)) / 50
        hard_avg = sum(len(s.target_text) for s in hard.generate(50)) / 50
        assert hard_avg > easy_avg

    def test_set_difficulty_changes_range(self) -> None:
        """Verify set_difficulty updates min and max."""
        from engram_generator.generators.arithmetic_core import AdditionGenerator
        gen = AdditionGenerator(min_difficulty=1, max_difficulty=3)
        gen.set_difficulty(5, 7)
        assert gen.min_difficulty == 5
        assert gen.max_difficulty == 7
        s = gen.generate(10)
        for sample in s:
            assert 5 <= sample.difficulty <= 7
