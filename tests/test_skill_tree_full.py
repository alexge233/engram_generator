"""Comprehensive tests for the adaptive skill tree curriculum manager.

Validates tree construction, mastery tracking, difficulty escalation,
prerequisite-based unlocking, sampling weights, and summary reporting.
"""
import pytest

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import get_all_generators
from engram_generator.curriculum.skill_tree import SkillTree, SkillNode


@pytest.fixture
def tree() -> SkillTree:
    """Create a skill tree from all registered generators.

    Returns:
        SkillTree initialised with the full 2022-task curriculum.
    """
    return SkillTree(get_all_generators())


class TestSkillTreeConstruction:
    """Verify the skill tree initialises correctly from generators."""

    def test_all_tasks_present(self, tree: SkillTree) -> None:
        """Verify every registered task has a node in the tree."""
        summary = tree.summary()
        assert summary["total"] == 2022

    def test_tier0_unlocked_initially(self, tree: SkillTree) -> None:
        """Verify tier 0 tasks without prerequisites start unlocked."""
        unlocked = set(tree.get_unlocked_tasks())
        gens = get_all_generators()
        for g in gens:
            if g.tier == 0 and not g.prerequisites:
                assert g.task_name in unlocked, (
                    f"Tier 0 task {g.task_name} should be unlocked"
                )

    def test_locked_tasks_not_in_unlocked(self, tree: SkillTree) -> None:
        """Verify high-tier tasks are locked at initialisation."""
        unlocked = set(tree.get_unlocked_tasks())
        assert "architecture_analysis" not in unlocked


class TestEscalation:
    """Verify difficulty escalation on high accuracy."""

    def test_escalation_increments_difficulty(self, tree: SkillTree) -> None:
        """Verify difficulty increases when accuracy hits the escalation threshold.

        Note: 0.97 also triggers mastery, which overwrites the escalation
        event in the events dict. We check difficulty increment directly.
        """
        before = tree.get_difficulty_for("addition")
        tree.update({"addition": 0.97})
        after = tree.get_difficulty_for("addition")
        assert after == before + 1

    def test_no_escalation_below_threshold(self, tree: SkillTree) -> None:
        """Verify difficulty stays the same below the escalation threshold."""
        before = tree.get_difficulty_for("addition")
        tree.update({"addition": 0.80})
        after = tree.get_difficulty_for("addition")
        assert after == before


class TestMastery:
    """Verify task mastery detection and prerequisite unlocking."""

    def test_mastery_at_threshold(self, tree: SkillTree) -> None:
        """Verify task is mastered when accuracy reaches mastery threshold."""
        tree.update({"addition": 0.95})
        assert "addition" in tree.get_mastered_tasks()

    def test_not_mastered_below_threshold(self, tree: SkillTree) -> None:
        """Verify task is not mastered below mastery threshold."""
        tree.update({"addition": 0.85})
        assert "addition" not in tree.get_mastered_tasks()

    def test_prerequisite_unlocking_chain(self, tree: SkillTree) -> None:
        """Verify mastering a prerequisite unlocks dependent tasks."""
        tree.update({"addition": 0.95})
        unlocked = set(tree.get_unlocked_tasks())
        gens = get_all_generators()
        addition_dependents = [
            g.task_name for g in gens
            if "addition" in g.prerequisites
        ]
        for dep in addition_dependents:
            g = next(g for g in gens if g.task_name == dep)
            all_prereqs_mastered = all(
                p in tree.get_mastered_tasks() or p == "addition"
                for p in g.prerequisites
            )
            if all_prereqs_mastered and len(g.prerequisites) == 1:
                assert dep in unlocked, (
                    f"{dep} should be unlocked after addition mastery"
                )


class TestSamplingWeights:
    """Verify sampling weight logic for curriculum training."""

    def test_locked_weight_zero(self, tree: SkillTree) -> None:
        """Verify locked tasks get zero sampling weight."""
        weights = tree.get_sampling_weights()
        assert weights.get("architecture_analysis", 0) == 0.0

    def test_mastered_weight_reduced(self, tree: SkillTree) -> None:
        """Verify mastered tasks get reduced (retention) weight."""
        tree.update({"addition": 0.95})
        weights = tree.get_sampling_weights()
        assert weights["addition"] < 1.0

    def test_struggling_weight_boosted(self, tree: SkillTree) -> None:
        """Verify low-accuracy tasks get boosted sampling weight."""
        tree.update({"addition": 0.30})
        weights = tree.get_sampling_weights()
        assert weights["addition"] >= 3.0

    def test_frontier_weight_normal(self, tree: SkillTree) -> None:
        """Verify frontier tasks (unlocked, not mastered) get standard weight."""
        tree.update({"addition": 0.70})
        weights = tree.get_sampling_weights()
        assert weights["addition"] == 2.0


class TestSummaryAndQueries:
    """Verify tree summary and query methods."""

    def test_summary_keys(self, tree: SkillTree) -> None:
        """Verify summary dict contains all expected keys."""
        summary = tree.summary()
        for key in ("total", "unlocked", "mastered", "frontier", "locked",
                     "max_tier_reached"):
            assert key in summary, f"Missing key: {key}"

    def test_frontier_tasks(self, tree: SkillTree) -> None:
        """Verify frontier = unlocked minus mastered."""
        frontier = set(tree.get_frontier_tasks())
        unlocked = set(tree.get_unlocked_tasks())
        mastered = set(tree.get_mastered_tasks())
        assert frontier == unlocked - mastered

    def test_get_difficulty_unknown_task(self, tree: SkillTree) -> None:
        """Verify unknown task returns default difficulty 1."""
        assert tree.get_difficulty_for("nonexistent_task") == 1

    def test_unknown_task_in_update_ignored(self, tree: SkillTree) -> None:
        """Verify updating an unregistered task doesn't crash."""
        events = tree.update({"fake_task_xyz": 0.99})
        assert "fake_task_xyz" not in events
