"""Sanity tests for every registered generator.

Generates samples at low and high difficulty for each generator and verifies:
1. Answer is non-empty and not 'skip'
2. Steps are non-empty
3. Answer characters are in tokenizer vocabulary
4. Problem is non-empty
5. Answer is consistent across same seed (determinism)
6. Target length is under 512 chars
7. Numerical answers (where parseable) are finite (not inf/nan)

This ensures no generator produces absolute nonsense.
"""
import math
import re

import pytest

from engram_generator.curriculum.registry import get_all_generators
from engram_generator.tokenizer import CharTokenizer


_TOKENIZER = CharTokenizer()
_VALID_CHARS = set(_TOKENIZER.CHARS)


def _all_generator_names():
    """Return sorted list of all generator task names."""
    return sorted(g.task_name for g in get_all_generators())


def _parse_numbers(s: str) -> list[float]:
    """Extract all numbers from a string."""
    return [float(m) for m in re.findall(r'-?\d+\.?\d*(?:e[+-]?\d+)?', s)]


@pytest.fixture(scope="module")
def all_gens():
    """Instantiate all generators once for the module."""
    return {g.task_name: g for g in get_all_generators()}


class TestAllGeneratorsLowDifficulty:
    """Sanity check every generator at difficulty 1."""

    @pytest.mark.parametrize("task_name", _all_generator_names())
    def test_generator_sanity_low(self, task_name, all_gens):
        """Verify generator produces valid output at low difficulty.

        Args:
            task_name: The generator's task name.
            all_gens: Fixture with all generators.
        """
        gen = all_gens[task_name]
        gen.set_difficulty(1, 1)
        samples = gen.generate(3)

        for s in samples:
            assert s.answer != "", f"{task_name}: empty answer"
            assert s.answer != "skip", f"{task_name}: skip answer"
            assert s.problem != "", f"{task_name}: empty problem"
            assert len(s.steps) >= 1, f"{task_name}: no steps"
            assert len(s.target_text) <= 512, \
                f"{task_name}: target too long ({len(s.target_text)})"

            for c in s.target_text:
                assert c in _VALID_CHARS, \
                    f"{task_name}: invalid char {repr(c)} (U+{ord(c):04X})"

            nums = _parse_numbers(s.answer)
            for n in nums:
                assert math.isfinite(n), \
                    f"{task_name}: non-finite number {n} in answer"


class TestAllGeneratorsHighDifficulty:
    """Sanity check every generator at difficulty 8."""

    @pytest.mark.parametrize("task_name", _all_generator_names())
    def test_generator_sanity_high(self, task_name, all_gens):
        """Verify generator produces valid output at high difficulty.

        Args:
            task_name: The generator's task name.
            all_gens: Fixture with all generators.
        """
        gen = all_gens[task_name]
        gen.set_difficulty(8, 8)
        samples = gen.generate(2)

        for s in samples:
            assert s.answer != "", f"{task_name} d8: empty answer"
            assert s.answer != "skip", f"{task_name} d8: skip answer"
            assert s.problem != "", f"{task_name} d8: empty problem"
            assert len(s.steps) >= 1, f"{task_name} d8: no steps"
            assert len(s.target_text) <= 512, \
                f"{task_name} d8: target too long ({len(s.target_text)})"


class TestAllGeneratorsDeterminism:
    """Verify every generator is deterministic with same seed."""

    @pytest.mark.parametrize("task_name", _all_generator_names())
    def test_deterministic(self, task_name):
        """Verify same seed produces same output.

        Args:
            task_name: The generator's task name.
        """
        from engram_generator.curriculum.registry import get_generator
        gen1 = get_generator(task_name, seed=99)
        gen1.set_difficulty(3, 3)
        s1 = gen1.generate(1)[0]

        gen2 = get_generator(task_name, seed=99)
        gen2.set_difficulty(3, 3)
        s2 = gen2.generate(1)[0]

        assert s1.target_text == s2.target_text, \
            f"{task_name}: not deterministic"
