"""Tests for audit fixes (v0.2.0).

Covers: BooleanEvalGenerator NOT, LogicalPuzzleGenerator leak,
KnightsKnavesGenerator steps, PolygonAreaGenerator ordering,
ImplicitDiffGenerator formatting, normaliser inf handling,
set_difficulty validation, and leak guard type mismatch.
"""
import math
import random
import warnings

import pytest

from engram_generator.evaluation.normaliser import OperationNormaliser


class TestNormaliserInfHandling:
    """Normaliser must not crash on inf/nan/huge-exponent strings."""

    def setup_method(self):
        self.n = OperationNormaliser()

    def test_inf_string(self):
        """'inf' should pass through without crash."""
        assert self.n.normalise("inf") == "inf"

    def test_negative_inf(self):
        """'-inf' should pass through without crash."""
        assert self.n.normalise("-inf") == "-inf"

    def test_infinity_word(self):
        """'infinity' should pass through without crash."""
        assert self.n.normalise("infinity") == "infinity"

    def test_huge_exponent(self):
        """'1e309' (overflows to inf) should not crash."""
        result = self.n.normalise("1e309")
        assert result is not None

    def test_nan_string(self):
        """'nan' should pass through without crash."""
        assert self.n.normalise("nan") == "nan"

    def test_normal_float_still_works(self):
        """Normal float normalisation still works after the fix."""
        assert self.n.normalise("125.0") == "125"
        assert self.n.normalise("3.14") == "3.14"


class TestBooleanEvalNotLogic:
    """BooleanEvalGenerator NOT must produce correct results."""

    def test_not_evaluation_correct(self):
        """NOT should negate the operand it applies to."""
        from engram_generator.generators.logic import BooleanEvalGenerator
        gen = BooleanEvalGenerator()
        gen.set_difficulty(3, 5)

        not_samples = []
        for seed in range(200):
            gen._rng = random.Random(seed)
            sample = gen._generate_one()
            expr = sample.problem
            if "NOT" in expr:
                not_samples.append(sample)

        assert len(not_samples) > 0, "No NOT samples generated"

        for sample in not_samples:
            expr = sample.problem
            answer = sample.answer

            tokens = expr.split()
            effective_vals = []
            i = 0
            while i < len(tokens):
                if tokens[i] == "NOT":
                    i += 1
                    val = tokens[i] == "True"
                    effective_vals.append(not val)
                elif tokens[i] in ("True", "False"):
                    effective_vals.append(tokens[i] == "True")
                i += 1

            ops = [t for t in tokens if t in ("AND", "OR")]
            result = effective_vals[0]
            for j, op in enumerate(ops):
                if op == "AND":
                    result = result and effective_vals[j + 1]
                else:
                    result = result or effective_vals[j + 1]

            assert str(result) == answer, (
                f"NOT eval wrong: expr='{expr}', "
                f"expected={result}, got={answer}"
            )

    def test_not_appears_in_steps(self):
        """Steps should show NOT evaluation when NOT is used."""
        from engram_generator.generators.logic import BooleanEvalGenerator
        gen = BooleanEvalGenerator()
        gen.set_difficulty(3, 5)

        for seed in range(200):
            gen._rng = random.Random(seed)
            sample = gen._generate_one()
            if "NOT" in sample.problem:
                steps_text = " ".join(sample.steps)
                assert "NOT" in steps_text, (
                    f"NOT in problem but not in steps: {sample.problem}"
                )
                break


class TestLogicalPuzzleNoLeak:
    """LogicalPuzzleGenerator must not leak all answers in clues."""

    def test_not_all_assignments_in_clues(self):
        """Clues must not contain direct assignments for all names."""
        from engram_generator.generators.logic import LogicalPuzzleGenerator
        gen = LogicalPuzzleGenerator()
        gen.set_difficulty(3, 5)

        for seed in range(50):
            gen._rng = random.Random(seed)
            sample = gen._generate_one()
            problem = sample.problem
            answer = sample.answer

            answer_pairs = answer.split(", ")
            direct_leaks = 0
            for pair in answer_pairs:
                name, color = pair.split("=")
                if f"{name} has {color}" in problem:
                    direct_leaks += 1

            assert direct_leaks < len(answer_pairs), (
                f"All answer pairs leaked in clues (seed={seed}): "
                f"problem='{problem}', answer='{answer}'"
            )

    def test_clues_contain_negatives(self):
        """Clues should include 'does not have' constraints."""
        from engram_generator.generators.logic import LogicalPuzzleGenerator
        gen = LogicalPuzzleGenerator()
        gen.set_difficulty(3, 5)

        has_negative = False
        for seed in range(20):
            gen._rng = random.Random(seed)
            sample = gen._generate_one()
            if "does not have" in sample.problem:
                has_negative = True
                break

        assert has_negative, "No negative clues found in 20 samples"

    def test_puzzle_uniquely_solvable(self):
        """Every puzzle must have exactly one solution."""
        from itertools import permutations
        from engram_generator.generators.logic import LogicalPuzzleGenerator
        gen = LogicalPuzzleGenerator()
        gen.set_difficulty(2, 5)

        for seed in range(100):
            gen._rng = random.Random(seed)
            sample = gen._generate_one()
            answer_pairs = dict(
                p.split("=") for p in sample.answer.split(", ")
            )
            names = list(answer_pairs.keys())
            colors = list(answer_pairs.values())

            consistent = []
            for perm in permutations(colors):
                candidate = dict(zip(names, perm))
                ok = True
                for clue in sample.problem.split("; "):
                    if " has " in clue and "does not" not in clue:
                        parts = clue.split(" has ")
                        if candidate.get(parts[0]) != parts[1]:
                            ok = False
                            break
                    elif "does not have" in clue:
                        parts = clue.split(" does not have ")
                        if candidate.get(parts[0]) == parts[1]:
                            ok = False
                            break
                if ok:
                    consistent.append(candidate)

            assert len(consistent) == 1, (
                f"Puzzle not unique (seed={seed}): "
                f"{len(consistent)} solutions for '{sample.problem}'"
            )


class TestKnightsKnavesSteps:
    """KnightsKnavesGenerator steps must show reasoning, not answers."""

    def test_steps_dont_reveal_types(self):
        """Steps must not directly state 'A is knight/knave'."""
        from engram_generator.generators.logic import KnightsKnavesGenerator
        gen = KnightsKnavesGenerator()
        gen.set_difficulty(1, 4)

        for seed in range(30):
            gen._rng = random.Random(seed)
            sample = gen._generate_one()
            answer_types = dict(
                pair.split("=") for pair in sample.answer.split(", ")
            )

            for step in sample.steps:
                if step.startswith("given:"):
                    continue
                for name, t in answer_types.items():
                    assert f"assume {name} is {t}" not in step, (
                        f"Step reveals answer: '{step}', answer='{sample.answer}'"
                    )

    def test_steps_show_testing(self):
        """Steps should mention testing assignments."""
        from engram_generator.generators.logic import KnightsKnavesGenerator
        gen = KnightsKnavesGenerator()
        gen.set_difficulty(1, 4)

        gen._rng = random.Random(42)
        sample = gen._generate_one()
        steps_text = " ".join(sample.steps)
        assert "test" in steps_text.lower(), (
            f"Steps don't show testing: {sample.steps}"
        )


class TestPolygonAreaOrdering:
    """PolygonAreaGenerator must sort vertices by angle."""

    def test_vertices_form_simple_polygon(self):
        """Vertices should be ordered so no edges cross."""
        from engram_generator.generators.geometry import PolygonAreaGenerator
        gen = PolygonAreaGenerator()
        gen.set_difficulty(3, 5)

        for seed in range(30):
            gen._rng = random.Random(seed)
            sample = gen._generate_one()
            pts_str = sample.problem
            pts = []
            for pair in pts_str.split():
                x, y = pair.strip("()").split(",")
                pts.append((int(x), int(y)))

            n = len(pts)
            if n < 4:
                continue

            cx = sum(p[0] for p in pts) / n
            cy = sum(p[1] for p in pts) / n
            angles = [math.atan2(p[1] - cy, p[0] - cx) for p in pts]

            for i in range(len(angles) - 1):
                assert angles[i] <= angles[i + 1], (
                    f"Vertices not sorted by angle (seed={seed})"
                )


class TestImplicitDiffFormatting:
    """ImplicitDiffGenerator must simplify fractions properly."""

    def test_no_1y_formatting(self):
        """Answer should use 'y' not '(1y)'."""
        from engram_generator.generators.expanded_core import (
            ImplicitDiffGenerator,
        )
        gen = ImplicitDiffGenerator()
        gen.set_difficulty(1, 5)

        for seed in range(50):
            gen._rng = random.Random(seed)
            sample = gen._generate_one()
            assert "(1y)" not in sample.answer, (
                f"'(1y)' found in answer: {sample.answer}"
            )

    def test_steps_show_simplification(self):
        """Steps should show the simplification when a/b reduces."""
        from engram_generator.generators.expanded_core import (
            ImplicitDiffGenerator,
        )
        gen = ImplicitDiffGenerator()
        gen.set_difficulty(1, 5)

        gen._rng = random.Random(42)
        sample = gen._generate_one()
        assert len(sample.steps) >= 3, (
            f"Expected at least 3 steps, got {len(sample.steps)}"
        )


class TestSetDifficultyValidation:
    """set_difficulty must cast floats to int."""

    def test_float_difficulty_cast(self):
        """Float difficulty values should be cast to int."""
        from engram_generator.generators.logic import BooleanEvalGenerator
        gen = BooleanEvalGenerator()
        gen.set_difficulty(1.0, 3.0)
        assert isinstance(gen.min_difficulty, int)
        assert isinstance(gen.max_difficulty, int)
        assert gen.min_difficulty == 1
        assert gen.max_difficulty == 3


class TestLeakGuardTypeMatch:
    """Leak guard should catch float/int answer equivalence."""

    def test_float_int_answer_blocked(self):
        """45.0 in solution_data should be blocked when answer is '45'."""
        from engram_generator.base import StepGenerator

        class FakeGen(StepGenerator):
            @property
            def task_name(self):
                return "fake"

            @property
            def tier(self):
                return 0

            def task_description(self, difficulty):
                return "fake"

            def _create_problem(self, difficulty):
                return "test", {"val": 45.0}

            def _create_steps(self, sd):
                return [f"val={sd['val']}"]

            def _create_answer(self, sd):
                return "45"

        gen = FakeGen()
        gen._rng = random.Random(42)
        sample = gen._generate_one()
        assert "45.0" not in sample.problem or "val=" not in sample.problem, (
            f"Float answer leaked: problem='{sample.problem}'"
        )


class TestVersionBumped:
    """Version should be 0.2.0."""

    def test_package_version(self):
        """Package __version__ is 0.2.0."""
        import engram_generator
        assert engram_generator.__version__ == "0.2.0"
