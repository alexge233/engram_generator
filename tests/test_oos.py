"""Tests for out-of-set (OOS) generators used in held-out evaluation.

OOS generators produce samples from domains never seen during training.
They test whether the model can transfer reasoning to novel surface
forms that share deep structure with trained tasks.
"""
import pytest

from engram_generator.base import STEP_TOKEN
from engram_generator.curriculum.registry import get_all_oos_generators, get_all_generators


@pytest.fixture(scope="module")
def oos_generators():
    """Return all registered OOS generators.

    Returns:
        List of OOS StepGenerator instances.
    """
    return get_all_oos_generators()


class TestOOSGenerators:
    """Verify out-of-set generators produce valid held-out evaluation data.

    OOS tasks must be structurally valid (non-empty fields, step tokens)
    but must NOT appear in the main training registry. They use tier 99
    to signal they are held-out.
    """

    def test_oos_generators_exist(self, oos_generators) -> None:
        """Verify at least one OOS generator is registered."""
        assert len(oos_generators) > 0, "No OOS generators registered"

    def test_all_oos_produce_samples(self, oos_generators) -> None:
        """Verify every OOS generator produces valid samples."""
        for gen in oos_generators:
            samples = gen.generate(3)
            assert len(samples) == 3, f"{gen.task_name}: produced {len(samples)}/3"
            for s in samples:
                assert s.input_text.strip(), f"{gen.task_name}: empty input"
                assert s.target_text.strip(), f"{gen.task_name}: empty target"
                assert s.answer, f"{gen.task_name}: empty answer"

    def test_all_oos_tier_99(self, oos_generators) -> None:
        """Verify all OOS generators are at tier 99 (held-out marker)."""
        for gen in oos_generators:
            assert gen.tier == 99, (
                f"{gen.task_name}: tier {gen.tier}, expected 99"
            )

    def test_all_oos_have_step_tokens(self, oos_generators) -> None:
        """Verify all OOS targets contain at least one <step> token."""
        for gen in oos_generators:
            s = gen.generate(1)[0]
            assert STEP_TOKEN in s.target_text, (
                f"{gen.task_name}: missing <step>"
            )

    def test_oos_task_names_prefixed(self, oos_generators) -> None:
        """Verify all OOS task names start with 'oos_'."""
        for gen in oos_generators:
            assert gen.task_name.startswith("oos_"), (
                f"{gen.task_name}: missing 'oos_' prefix"
            )

    def test_oos_not_in_main_registry(self, oos_generators) -> None:
        """Verify OOS tasks are separate from the training registry."""
        main_names = {g.task_name for g in get_all_generators()}
        for gen in oos_generators:
            assert gen.task_name not in main_names, (
                f"{gen.task_name}: found in main registry"
            )

    def test_oos_deterministic(self, oos_generators) -> None:
        """Verify OOS generators are deterministic with identical seeds."""
        for gen in oos_generators:
            g1 = type(gen)(seed=42)
            g2 = type(gen)(seed=42)
            s1 = g1.generate(5)
            s2 = g2.generate(5)
            for a, b in zip(s1, s2):
                assert a.target_text == b.target_text, (
                    f"{gen.task_name}: not deterministic"
                )
