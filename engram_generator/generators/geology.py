"""Geology generators -- radiometric dating, seismic waves, hardness, magnitudes.

4 generators across tiers 3-5.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


class GeologyBase(StepGenerator):
    """Base class for geology generators with shared constants.

    Provides common geological constants and helper methods used
    across dating, seismology, and mineralogy generators.
    """

    LN2 = round(math.log(2), 4)


# ===================================================================
# 1. Radiometric dating  (tier 5)
# ===================================================================

@register
class RadiometricDatingGenerator(GeologyBase):
    """Compute age from parent-daughter isotope ratio and half-life.

    Applies t = t_half * ln(1 + D/P) / ln(2) where D is the number
    of daughter atoms, P is the number of remaining parent atoms,
    and t_half is the half-life of the parent isotope.

    Difficulty scaling:
        Difficulty 1-3: simple integer D/P ratios.
        Difficulty 4-6: real-valued D/P ratios with 2 decimal places.
        Difficulty 7-8: very large half-lives (billions of years), precise ratios.

    Prerequisites:
        logarithm.
    """

    _ISOTOPES = [
        # (name, half_life_years)
        ("C-14", 5730),
        ("K-40", 1.25e9),
        ("U-238", 4.468e9),
        ("Rb-87", 4.88e10),
        ("U-235", 7.04e8),
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "radiometric_dating"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["logarithm"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "compute age from parent-daughter isotope ratio"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a radiometric dating problem.

        Selects an isotope system and creates a D/P ratio, then
        computes the age using the decay equation.

        Args:
            difficulty: Controls ratio precision and isotope selection.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            isotope_name, t_half = self._rng.choice(self._ISOTOPES[:2])
            d_over_p = round(self._rng.uniform(0.5, 3.0), 0)
        elif difficulty <= 6:
            isotope_name, t_half = self._rng.choice(self._ISOTOPES[:4])
            d_over_p = round(self._rng.uniform(0.1, 5.0), 2)
        else:
            isotope_name, t_half = self._rng.choice(self._ISOTOPES)
            d_over_p = round(self._rng.uniform(0.01, 10.0), 4)

        ln_ratio = round(math.log(1.0 + d_over_p), 4)
        age = round(t_half * ln_ratio / self.LN2, 4)

        desc = (
            f"isotope {isotope_name}, t_half = {t_half} yr, "
            f"D/P = {d_over_p}; find age"
        )
        return desc, {
            "isotope": isotope_name, "t_half": t_half,
            "d_over_p": d_over_p, "ln_ratio": ln_ratio,
            "ln2": self.LN2, "age": age,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return [
            "t = t_half * ln(1 + D/P) / ln(2)",
            f"1 + D/P = 1 + {sd['d_over_p']} = {round(1 + sd['d_over_p'], 4)}",
            f"ln({round(1 + sd['d_over_p'], 4)}) = {sd['ln_ratio']}",
            f"t = {sd['t_half']} * {sd['ln_ratio']} / {sd['ln2']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the computed age.

        Args:
            sd: Solution data.

        Returns:
            Age as a string.
        """
        return f"age = {sd['age']} yr"


# ===================================================================
# 2. Seismic velocity  (tier 4)
# ===================================================================

@register
class SeismicVelocityGenerator(GeologyBase):
    """Compute epicentral distance from P-S wave arrival time difference.

    Applies d = (t_S - t_P) * v_P * v_S / (v_S - v_P) to compute
    the distance to the earthquake epicentre from the difference in
    P-wave and S-wave arrival times.

    Difficulty scaling:
        Difficulty 1-3: simple integer velocities and times.
        Difficulty 4-6: realistic crustal velocities with decimals.
        Difficulty 7-8: varying depth layers with precise parameters.

    Prerequisites:
        multiplication.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "seismic_velocity"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["multiplication"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "compute epicentral distance from P-S wave time difference"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a seismic velocity problem.

        Creates P-wave and S-wave velocities and a time difference,
        then computes the epicentral distance.

        Args:
            difficulty: Controls parameter precision.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            v_p = round(self._rng.uniform(6.0, 8.0), 0)
            v_s = round(self._rng.uniform(3.0, 5.0), 0)
            dt = round(self._rng.uniform(5.0, 30.0), 0)
        elif difficulty <= 6:
            v_p = round(self._rng.uniform(5.5, 8.1), 2)
            v_s = round(self._rng.uniform(3.0, 4.7), 2)
            dt = round(self._rng.uniform(2.0, 60.0), 2)
        else:
            v_p = round(self._rng.uniform(5.0, 8.5), 4)
            v_s = round(self._rng.uniform(2.8, 4.9), 4)
            dt = round(self._rng.uniform(1.0, 120.0), 4)

        v_diff = round(v_p - v_s, 4)
        v_product = round(v_p * v_s, 4)
        d = round(dt * v_product / v_diff, 4)

        desc = (
            f"v_P = {v_p} km/s, v_S = {v_s} km/s, "
            f"t_S - t_P = {dt} s; find epicentral distance"
        )
        return desc, {
            "v_p": v_p, "v_s": v_s, "dt": dt,
            "v_diff": v_diff, "v_product": v_product, "d": d,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return [
            "d = (t_S - t_P) * v_P * v_S / (v_S - v_P)",
            f"v_P - v_S = {sd['v_p']} - {sd['v_s']} = {sd['v_diff']} km/s",
            f"v_P * v_S = {sd['v_p']} * {sd['v_s']} = {sd['v_product']}",
            f"d = {sd['dt']} * {sd['v_product']} / {sd['v_diff']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the epicentral distance.

        Args:
            sd: Solution data.

        Returns:
            Distance as a string.
        """
        return f"d = {sd['d']} km"


# ===================================================================
# 3. Mohs hardness  (tier 3)
# ===================================================================

@register
class MohsHardnessGenerator(GeologyBase):
    """Determine which mineral scratches which based on Mohs hardness.

    Given two minerals with known Mohs hardness values, determines
    which can scratch the other (higher hardness scratches lower).

    Difficulty scaling:
        Difficulty 1-3: well-known minerals with large hardness gap.
        Difficulty 4-6: less common minerals, smaller gap.
        Difficulty 7-8: minerals with adjacent hardness values.

    Prerequisites:
        comparison.
    """

    _MINERALS = [
        ("talc", 1), ("gypsum", 2), ("calcite", 3),
        ("fluorite", 4), ("apatite", 5), ("orthoclase", 6),
        ("quartz", 7), ("topaz", 8), ("corundum", 9),
        ("diamond", 10),
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "mohs_hardness"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 3

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["comparison"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "determine which mineral scratches the other using Mohs scale"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Mohs hardness comparison problem.

        Selects two minerals with a hardness gap controlled by
        difficulty and asks which scratches which.

        Args:
            difficulty: Controls how close the hardness values are.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            min_gap = 3
        elif difficulty <= 6:
            min_gap = 2
        else:
            min_gap = 1

        # Select two distinct minerals with the required gap
        while True:
            m1_name, m1_h = self._rng.choice(self._MINERALS)
            m2_name, m2_h = self._rng.choice(self._MINERALS)
            if m1_name != m2_name and abs(m1_h - m2_h) >= min_gap:
                break

        if m1_h > m2_h:
            scratcher = m1_name
            scratched = m2_name
        else:
            scratcher = m2_name
            scratched = m1_name

        desc = (
            f"mineral A: {m1_name} (hardness {m1_h}), "
            f"mineral B: {m2_name} (hardness {m2_h}); "
            f"which scratches which?"
        )
        return desc, {
            "m1_name": m1_name, "m1_h": m1_h,
            "m2_name": m2_name, "m2_h": m2_h,
            "scratcher": scratcher, "scratched": scratched,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return [
            f"{sd['m1_name']} has Mohs hardness {sd['m1_h']}",
            f"{sd['m2_name']} has Mohs hardness {sd['m2_h']}",
            f"{sd['m1_h']} vs {sd['m2_h']}: higher hardness scratches lower",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return which mineral scratches which.

        Args:
            sd: Solution data.

        Returns:
            Scratch relationship as a string.
        """
        return f"{sd['scratcher']} scratches {sd['scratched']}"


# ===================================================================
# 4. Richter magnitude  (tier 5)
# ===================================================================

@register
class RichterMagnitudeGenerator(GeologyBase):
    """Compute Richter magnitude or amplitude ratio from seismic data.

    Applies M = log10(A / A0) to compute magnitude from amplitude
    ratio, or computes the amplitude ratio between two earthquake
    magnitudes using A1/A2 = 10^(M1 - M2).

    Difficulty scaling:
        Difficulty 1-3: compute M from A/A0 (simple ratios).
        Difficulty 4-6: compute M from A/A0 (precise ratios).
        Difficulty 7-8: compute amplitude ratio between two magnitudes.

    Prerequisites:
        logarithm.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "richter_magnitude"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["logarithm"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "compute Richter magnitude or amplitude ratio"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Richter magnitude problem.

        At lower difficulties, provides an amplitude ratio and asks
        for magnitude. At higher difficulties, provides two magnitudes
        and asks for the amplitude ratio between them.

        Args:
            difficulty: Controls problem variant and precision.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 6:
            # Forward: compute M from A/A0
            if difficulty <= 3:
                # Use powers of 10 for clean results
                exponent = self._rng.randint(1, 5)
                ratio = round(10.0 ** exponent, 4)
            else:
                ratio = round(self._rng.uniform(10.0, 100000.0), 4)

            mag = round(math.log10(ratio), 4)

            desc = f"A/A0 = {ratio}; find Richter magnitude M"
            return desc, {
                "mode": "forward", "ratio": ratio, "M": mag,
            }

        # Inverse: compute amplitude ratio from two magnitudes
        m1 = round(self._rng.uniform(3.0, 8.0), 1)
        m2 = round(self._rng.uniform(3.0, 8.0), 1)
        while m1 == m2:
            m2 = round(self._rng.uniform(3.0, 8.0), 1)

        diff = round(m1 - m2, 4)
        ratio = round(10.0 ** diff, 4)

        desc = f"M1 = {m1}, M2 = {m2}; find A1/A2"
        return desc, {
            "mode": "inverse", "M1": m1, "M2": m2,
            "diff": diff, "ratio": ratio,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        if sd["mode"] == "forward":
            return [
                "M = log10(A / A0)",
                f"A/A0 = {sd['ratio']}",
                f"log10({sd['ratio']}) = {sd['M']}",
            ]
        return [
            "A1/A2 = 10^(M1 - M2)",
            f"M1 - M2 = {sd['M1']} - {sd['M2']} = {sd['diff']}",
            f"10^{sd['diff']} = {sd['ratio']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the magnitude or amplitude ratio.

        Args:
            sd: Solution data.

        Returns:
            Result as a string.
        """
        if sd["mode"] == "forward":
            return f"M = {sd['M']}"
        return f"A1/A2 = {sd['ratio']}"
