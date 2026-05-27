"""End-to-end tests — full pipeline from generation through tokenisation."""
import pytest

from engram_generator.base import STEP_TOKEN
from engram_generator.curriculum.registry import get_all_generators, get_generator
from engram_generator.curriculum.skill_tree import SkillTree
from engram_generator.tokenizer import CharTokenizer


class TestEndToEndPipeline:
    """Tests the full pipeline: generate → tokenise → mask → decode."""

    def test_generate_tokenise_mask_decode(self) -> None:
        """Verify complete pipeline for a representative task."""
        gen = get_generator("addition", seed=42)
        tok = CharTokenizer()

        sample = gen.generate(1)[0]
        input_ids = tok.encode(sample.input_text)
        target_ids = tok.encode(sample.target_text)
        step_mask = tok.get_step_mask(target_ids)

        assert len(input_ids) > 0
        assert len(target_ids) > 0
        assert any(step_mask)

        content_ids = [
            tid for tid, is_step in zip(target_ids, step_mask)
            if not is_step and tid != tok.pad_token_id and tid != tok.eos_token_id
        ]
        assert len(content_ids) > 0

    def test_step_tokens_excluded_from_content(self) -> None:
        """Verify <step> tokens can be masked out cleanly."""
        tok = CharTokenizer()

        for gen in get_all_generators():
            sample = gen.generate(1)[0]
            ids = tok.encode(sample.target_text)
            mask = tok.get_step_mask(ids)

            masked_ids = [
                -100 if is_step else tid
                for tid, is_step in zip(ids, mask)
            ]
            assert -100 in masked_ids, f"{gen.task_name}: no <step> to mask"

            content_count = sum(1 for mid in masked_ids if mid != -100)
            assert content_count > 0, f"{gen.task_name}: all tokens masked"

    def test_answer_appears_in_target_end(self) -> None:
        """Verify the answer is the last segment of the target."""
        for gen in get_all_generators():
            sample = gen.generate(1)[0]
            segments = sample.target_text.split(f" {STEP_TOKEN} ")
            last_segment = segments[-1].strip()
            assert last_segment == sample.answer.strip(), (
                f"{gen.task_name}: answer '{sample.answer}' != last segment '{last_segment}'"
            )

    def test_problem_is_first_segment(self) -> None:
        """Verify the problem statement is the first segment."""
        for gen in get_all_generators():
            sample = gen.generate(1)[0]
            segments = sample.target_text.split(f" {STEP_TOKEN} ")
            first_segment = segments[0].strip()
            assert first_segment == sample.problem.strip(), (
                f"{gen.task_name}: problem mismatch"
            )


class TestEndToEndSkillTree:
    """Tests the skill tree lifecycle end-to-end."""

    def test_full_mastery_progression(self) -> None:
        """Simulate mastering tier 0 and verify tier 1 unlocks."""
        gens = get_all_generators()
        tree = SkillTree(gens, retention_ratio=0.1)

        tier0_tasks = [g.task_name for g in gens if g.tier == 0 and not g.prerequisites]
        initial_unlocked = set(tree.get_unlocked_tasks())
        for task in tier0_tasks:
            assert task in initial_unlocked

        accuracy = {task: 0.96 for task in tier0_tasks}
        tree.update(accuracy)

        new_unlocked = set(tree.get_unlocked_tasks())
        assert len(new_unlocked) > len(initial_unlocked)

    def test_difficulty_escalation_chain(self) -> None:
        """Verify difficulty escalates across multiple epochs."""
        gens = get_all_generators()
        tree = SkillTree(gens)

        initial_diff = tree.get_difficulty_for("addition")

        for _ in range(5):
            tree.update({"addition": 0.97})

        final_diff = tree.get_difficulty_for("addition")
        assert final_diff > initial_diff

    def test_sampling_weights_reflect_state(self) -> None:
        """Verify sampling weights change with mastery state."""
        gens = get_all_generators()
        tree = SkillTree(gens, retention_ratio=0.1)

        weights_before = tree.get_sampling_weights()
        tree.update({"addition": 0.96})
        weights_after = tree.get_sampling_weights()

        assert weights_after["addition"] < weights_before["addition"]

    def test_locked_tasks_have_zero_weight(self) -> None:
        """Verify locked tasks cannot be sampled."""
        gens = get_all_generators()
        tree = SkillTree(gens)
        weights = tree.get_sampling_weights()

        locked = [
            g.task_name for g in gens
            if g.task_name not in tree.get_unlocked_tasks()
        ]
        for task in locked:
            assert weights[task] == 0.0, f"{task} is locked but has weight {weights[task]}"

    def test_frontier_tasks_identified(self) -> None:
        """Verify frontier tasks are unlocked but not mastered."""
        gens = get_all_generators()
        tree = SkillTree(gens)

        frontier = tree.get_frontier_tasks()
        unlocked = set(tree.get_unlocked_tasks())
        mastered = set(tree.get_mastered_tasks())

        for task in frontier:
            assert task in unlocked
            assert task not in mastered


class TestEndToEndMultiTierProgression:
    """Tests multi-tier progression through the skill tree."""

    def test_progress_through_three_tiers(self) -> None:
        """Simulate mastering tiers 0-2 and verify tier 3 tasks unlock."""
        gens = get_all_generators()
        tree = SkillTree(gens)

        for _ in range(3):
            unlocked = tree.get_unlocked_tasks()
            accuracy = {task: 0.96 for task in unlocked}
            tree.update(accuracy)

        summary = tree.summary()
        assert summary["max_tier_reached"] >= 2
        assert summary["mastered"] > 10

    def test_summary_counts_are_consistent(self) -> None:
        """Verify summary counts add up correctly."""
        gens = get_all_generators()
        tree = SkillTree(gens)

        summary = tree.summary()
        total = summary["unlocked"] + summary["locked"]
        assert total == summary["total"]
        assert summary["frontier"] == summary["unlocked"] - summary["mastered"]
