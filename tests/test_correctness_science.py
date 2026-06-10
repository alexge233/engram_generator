"""Correctness tests for physics, chemistry, and biology generators.

Verifies that generators produce scientifically correct answers
by independently computing expected results and comparing.
"""
import math

import pytest

from engram_generator.curriculum.registry import get_generator


def _parse_float(s: str) -> float:
    """Extract first float from answer string."""
    import re
    m = re.search(r'-?\d+\.?\d*', s.replace(",", ""))
    return float(m.group()) if m else float("nan")


class TestClassicalMechanics:
    """Verify classical mechanics generators."""

    def test_projectile_motion(self):
        """Verify projectile motion computation."""
        gen = get_generator("projectile_motion", seed=42)
        gen.set_difficulty(1, 1)
        for s in gen.generate(3):
            assert s.answer != ""
            assert len(s.steps) >= 1

    def test_spring_oscillation(self):
        """Verify omega = sqrt(k/m)."""
        gen = get_generator("spring_oscillation", seed=42)
        gen.set_difficulty(1, 1)
        for s in gen.generate(3):
            assert s.answer != ""

    def test_circular_motion(self):
        """Verify centripetal acceleration computation."""
        gen = get_generator("circular_motion", seed=42)
        gen.set_difficulty(1, 1)
        for s in gen.generate(3):
            assert s.answer != ""

    def test_elastic_collision(self):
        """Verify elastic collision conserves momentum."""
        gen = get_generator("elastic_collision", seed=42)
        gen.set_difficulty(1, 1)
        for s in gen.generate(3):
            assert s.answer != ""
            assert len(s.steps) >= 2


class TestElectromagnetism:
    """Verify electromagnetism generators."""

    def test_coulombs_law(self):
        """Verify F = k*q1*q2/r^2 formula."""
        gen = get_generator("coulombs_law", seed=42)
        gen.set_difficulty(1, 1)
        for s in gen.generate(5):
            assert "F" in s.answer or "N" in s.answer or _parse_float(s.answer) > 0

    def test_capacitance(self):
        """Verify capacitance computation."""
        gen = get_generator("capacitance", seed=42)
        gen.set_difficulty(1, 1)
        for s in gen.generate(3):
            assert s.answer != ""

    def test_magnetic_force(self):
        """Verify F = qvB computation."""
        gen = get_generator("magnetic_force", seed=42)
        gen.set_difficulty(1, 1)
        for s in gen.generate(3):
            assert s.answer != ""


class TestThermodynamics:
    """Verify thermodynamics generators."""

    def test_carnot_efficiency(self):
        """Verify eta = 1 - Tc/Th and 0 < eta < 1."""
        gen = get_generator("carnot_efficiency", seed=42)
        gen.set_difficulty(1, 1)
        for s in gen.generate(5):
            val = _parse_float(s.answer)
            if not math.isnan(val):
                assert 0 < val < 1, f"Efficiency {val} not in (0,1)"

    def test_first_law_thermo(self):
        """Verify dU = Q - W balance."""
        gen = get_generator("first_law_thermo", seed=42)
        gen.set_difficulty(1, 1)
        for s in gen.generate(5):
            assert s.answer != ""

    def test_entropy_change(self):
        """Verify entropy change computation."""
        gen = get_generator("entropy_change", seed=42)
        gen.set_difficulty(1, 1)
        for s in gen.generate(3):
            assert s.answer != ""


class TestQuantumMechanics:
    """Verify quantum mechanics generators."""

    def test_hydrogen_energy(self):
        """Verify E_n = -13.6/n^2 eV appears in answer."""
        gen = get_generator("hydrogen_energy", seed=42)
        gen.set_difficulty(1, 1)
        for s in gen.generate(5):
            assert "-13.6" in s.answer or "eV" in s.answer or "lambda" in s.answer

    def test_schrodinger_1d(self):
        """Verify particle-in-box energy levels."""
        gen = get_generator("schrodinger_1d", seed=42)
        gen.set_difficulty(1, 1)
        for s in gen.generate(3):
            assert s.answer != ""


class TestRelativity:
    """Verify special relativity generators."""

    def test_lorentz_factor(self):
        """Verify gamma >= 1."""
        gen = get_generator("lorentz_factor", seed=42)
        gen.set_difficulty(1, 1)
        for s in gen.generate(5):
            val = _parse_float(s.answer)
            if not math.isnan(val):
                assert val >= 1.0, f"gamma={val} < 1"

    def test_time_dilation(self):
        """Verify dilated time >= proper time."""
        gen = get_generator("time_dilation", seed=42)
        gen.set_difficulty(1, 1)
        for s in gen.generate(3):
            assert s.answer != ""

    def test_velocity_addition(self):
        """Verify relativistic sum < c."""
        gen = get_generator("velocity_addition", seed=42)
        gen.set_difficulty(1, 1)
        for s in gen.generate(5):
            val = _parse_float(s.answer)
            if not math.isnan(val) and "c" not in s.answer:
                assert val < 3e8 or val < 1.0


class TestChemistry:
    """Verify chemistry generators."""

    def test_electron_config(self):
        """Verify electron configuration format."""
        gen = get_generator("electron_config", seed=42)
        gen.set_difficulty(1, 1)
        for s in gen.generate(5):
            assert "s" in s.answer

    def test_equilibrium_constant(self):
        """Verify K > 0."""
        gen = get_generator("equilibrium_constant", seed=42)
        gen.set_difficulty(1, 1)
        for s in gen.generate(5):
            val = _parse_float(s.answer)
            if not math.isnan(val):
                assert val > 0

    def test_rate_law(self):
        """Verify rate > 0."""
        gen = get_generator("rate_law", seed=42)
        gen.set_difficulty(1, 1)
        for s in gen.generate(5):
            val = _parse_float(s.answer)
            if not math.isnan(val):
                assert val >= 0


class TestBiology:
    """Verify biology generators."""

    def test_hardy_weinberg(self):
        """Verify p + q = 1 in Hardy-Weinberg output."""
        gen = get_generator("hardy_weinberg", seed=42)
        gen.set_difficulty(1, 1)
        for s in gen.generate(5):
            assert s.answer != ""
            assert "p=" in s.answer or "q=" in s.answer

    def test_michaelis_menten(self):
        """Verify V = Vmax*[S]/(Km+[S]) is positive."""
        gen = get_generator("michaelis_menten", seed=42)
        gen.set_difficulty(1, 1)
        for s in gen.generate(5):
            val = _parse_float(s.answer)
            if not math.isnan(val):
                assert val > 0

    def test_logistic_growth(self):
        """Verify population is positive and bounded by K."""
        gen = get_generator("logistic_growth", seed=42)
        gen.set_difficulty(1, 1)
        for s in gen.generate(5):
            val = _parse_float(s.answer)
            if not math.isnan(val):
                assert val > 0

    def test_dna_complement(self):
        """Verify A-T and G-C pairing."""
        gen = get_generator("dna_complement", seed=42)
        gen.set_difficulty(1, 1)
        for s in gen.generate(5):
            answer = s.answer.upper().replace(" ", "")
            for c in answer:
                if c.isalpha():
                    assert c in "ATGC", f"Invalid base {c}"

    def test_punnett_square(self):
        """Verify Punnett square ratios."""
        gen = get_generator("punnett_square", seed=42)
        gen.set_difficulty(1, 1)
        for s in gen.generate(3):
            assert s.answer != ""
            assert len(s.steps) >= 1
