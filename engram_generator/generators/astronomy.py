"""Astronomy generators -- stellar distances, classification, magnitudes, velocities.

6 generators across tiers 4-5.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


# Physical constants
_C_KM_S = 299792.458  # speed of light in km/s


class AstronomyBase(StepGenerator):
    """Base class for astronomy generators with shared constants.

    Provides common astronomical constants and helper methods used
    across stellar, galactic, and cosmological generators.
    """

    LN10 = round(math.log(10), 4)


# ===================================================================
# 1. Parallax distance  (tier 4)
# ===================================================================

@register
class ParallaxDistanceGenerator(AstronomyBase):
    """Compute distance in parsecs from parallax angle.

    Applies d(pc) = 1 / p(arcsec) to convert a measured stellar
    parallax angle into distance in parsecs.

    Difficulty scaling:
        Difficulty 1-3: parallax 0.1-1.0 arcsec (nearby stars).
        Difficulty 4-6: parallax 0.01-0.1 arcsec (intermediate).
        Difficulty 7-8: parallax 0.001-0.01 arcsec (distant stars).

    Prerequisites:
        division.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "parallax_distance"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["division"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "compute stellar distance from parallax angle"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a parallax distance problem.

        Creates a parallax angle appropriate for the difficulty level
        and computes the corresponding distance in parsecs.

        Args:
            difficulty: Controls the parallax magnitude.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            p = round(self._rng.uniform(0.1, 1.0), 4)
        elif difficulty <= 6:
            p = round(self._rng.uniform(0.01, 0.1), 4)
        else:
            p = round(self._rng.uniform(0.001, 0.01), 4)

        d = round(1.0 / p, 4)

        desc = f"parallax p = {p} arcsec; find distance in parsecs"
        return desc, {"p": p, "d": d}

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return [
            "d(pc) = 1 / p(arcsec)",
            f"d = 1 / {sd['p']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the distance in parsecs.

        Args:
            sd: Solution data.

        Returns:
            Distance as a string.
        """
        return f"d = {sd['d']} pc"


# ===================================================================
# 2. HR diagram classification  (tier 4)
# ===================================================================

@register
class HRDiagramGenerator(AstronomyBase):
    """Classify a star on the Hertzsprung-Russell diagram.

    Given surface temperature (K) and luminosity (solar luminosities),
    classifies the star as main sequence, giant, supergiant, or
    white dwarf based on standard HR diagram regions.

    Difficulty scaling:
        Difficulty 1-3: clear-cut main sequence or giant.
        Difficulty 4-6: supergiants and white dwarfs added.
        Difficulty 7-8: borderline cases requiring careful comparison.

    Prerequisites:
        comparison.
    """

    _REGIONS = [
        ("main_sequence", 3000, 30000, 0.01, 100.0),
        ("giant", 3500, 6000, 10.0, 1000.0),
        ("supergiant", 3000, 30000, 10000.0, 500000.0),
        ("white_dwarf", 7000, 40000, 0.0001, 0.01),
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "hr_diagram"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

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
        return "classify star on the HR diagram given temperature and luminosity"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an HR diagram classification problem.

        Selects a star region appropriate for difficulty, then generates
        a temperature-luminosity pair within that region.

        Args:
            difficulty: Controls which regions are available.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            pool = self._REGIONS[:2]
        elif difficulty <= 6:
            pool = self._REGIONS
        else:
            pool = self._REGIONS

        region_name, t_lo, t_hi, l_lo, l_hi = self._rng.choice(pool)

        temp = self._rng.randint(t_lo, t_hi)
        lum = round(self._rng.uniform(l_lo, l_hi), 4)

        desc = f"T = {temp} K, L = {lum} L_sun; classify the star"
        return desc, {
            "temp": temp, "lum": lum, "classification": region_name,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        steps = [
            f"temperature = {sd['temp']} K",
            f"luminosity = {sd['lum']} L_sun",
        ]

        if sd["classification"] == "white_dwarf":
            steps.append("high T but very low L => white dwarf")
        elif sd["classification"] == "supergiant":
            steps.append("very high L (>10000 L_sun) => supergiant")
        elif sd["classification"] == "giant":
            steps.append("moderate T with high L (10-1000 L_sun) => giant")
        else:
            steps.append(
                "T and L consistent with main sequence band"
            )

        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the stellar classification.

        Args:
            sd: Solution data.

        Returns:
            Classification string.
        """
        return f"classification = {sd['classification']}"


# ===================================================================
# 3. Absolute magnitude  (tier 5)
# ===================================================================

@register
class AbsoluteMagnitudeGenerator(AstronomyBase):
    """Compute absolute magnitude from apparent magnitude and distance.

    Applies M = m - 5 * log10(d / 10) where m is apparent magnitude,
    d is distance in parsecs, and M is absolute magnitude.

    Difficulty scaling:
        Difficulty 1-3: nearby stars (d < 100 pc).
        Difficulty 4-6: intermediate distances (100-1000 pc).
        Difficulty 7-8: distant objects (1000-10000 pc).

    Prerequisites:
        logarithm.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "absolute_magnitude"

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
        return "compute absolute magnitude from apparent magnitude and distance"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an absolute magnitude problem.

        Creates apparent magnitude and distance values, then computes
        absolute magnitude using the distance modulus formula.

        Args:
            difficulty: Controls distance range.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        m = round(self._rng.uniform(-2.0, 12.0), 4)

        if difficulty <= 3:
            d = round(self._rng.uniform(5.0, 100.0), 4)
        elif difficulty <= 6:
            d = round(self._rng.uniform(100.0, 1000.0), 4)
        else:
            d = round(self._rng.uniform(1000.0, 10000.0), 4)

        d_over_10 = round(d / 10.0, 4)
        log_term = round(math.log10(d_over_10), 4)
        distance_modulus = round(5.0 * log_term, 4)
        abs_mag = round(m - distance_modulus, 4)

        desc = f"m = {m}, d = {d} pc; find absolute magnitude M"
        return desc, {
            "m": m, "d": d, "d_over_10": d_over_10,
            "log_term": log_term, "distance_modulus": distance_modulus,
            "M": abs_mag,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return [
            "M = m - 5 * log10(d / 10)",
            f"d / 10 = {sd['d']} / 10 = {sd['d_over_10']}",
            f"log10({sd['d_over_10']}) = {sd['log_term']}",
            f"5 * {sd['log_term']} = {sd['distance_modulus']}",
            f"M = {sd['m']} - {sd['distance_modulus']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the absolute magnitude.

        Args:
            sd: Solution data.

        Returns:
            Absolute magnitude as a string.
        """
        return f"M = {sd['M']}"


# ===================================================================
# 4. Doppler velocity  (tier 5)
# ===================================================================

@register
class DopplerVelocityGenerator(AstronomyBase):
    """Compute recession velocity from cosmological redshift.

    Applies v = c * z for small redshift values, where c is the speed
    of light and z is the measured redshift.

    Difficulty scaling:
        Difficulty 1-3: very small z (0.001-0.01).
        Difficulty 4-6: moderate z (0.01-0.1).
        Difficulty 7-8: larger z (0.1-0.3), still within linear regime.

    Prerequisites:
        redshift.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "doppler_velocity"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["redshift"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "compute recession velocity from redshift"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Doppler velocity problem.

        Creates a redshift value appropriate for the difficulty and
        computes the recession velocity in km/s.

        Args:
            difficulty: Controls redshift magnitude.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            z = round(self._rng.uniform(0.001, 0.01), 4)
        elif difficulty <= 6:
            z = round(self._rng.uniform(0.01, 0.1), 4)
        else:
            z = round(self._rng.uniform(0.1, 0.3), 4)

        v = round(_C_KM_S * z, 4)

        desc = f"redshift z = {z}; find recession velocity"
        return desc, {"z": z, "c": _C_KM_S, "v": v}

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return [
            "v = c * z (low-z approximation)",
            f"c = {sd['c']} km/s",
            f"v = {sd['c']} * {sd['z']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the recession velocity.

        Args:
            sd: Solution data.

        Returns:
            Velocity as a string.
        """
        return f"v = {sd['v']} km/s"


# ===================================================================
# 5. Tidal force  (tier 5)
# ===================================================================

@register
class TidalForceGenerator(AstronomyBase):
    """Compute tidal acceleration difference across an extended body.

    Applies dF = 2 * G * M * dr / r^3 to compute the differential
    tidal acceleration across an object of extent dr at distance r
    from a mass M.

    Difficulty scaling:
        Difficulty 1-3: Earth-Moon system with small dr.
        Difficulty 4-6: Jupiter-Io or Sun-Earth with moderate dr.
        Difficulty 7-8: compact objects (neutron stars) with large dr.

    Prerequisites:
        gravitational_force.
    """

    _G = 6.6743e-11  # gravitational constant (m^3 kg^-1 s^-2)

    _SCENARIOS = [
        # (name, M_kg, r_m, dr_m)  -- representative scales
        ("Earth-Moon", 5.972e24, 3.844e8, 1.0e6),
        ("Sun-Earth", 1.989e30, 1.496e11, 1.274e7),
        ("Jupiter-Io", 1.898e27, 4.217e8, 3.643e6),
        ("Neutron-star", 2.8e30, 1.0e4, 10.0),
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "tidal_force"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["gravitational_force"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "compute tidal acceleration difference across an object"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a tidal force problem.

        Selects a scenario based on difficulty, adds random perturbation
        to parameters, and computes the tidal acceleration.

        Args:
            difficulty: Controls scenario complexity.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            scenario = self._SCENARIOS[0]
        elif difficulty <= 6:
            idx = self._rng.choice([1, 2])
            scenario = self._SCENARIOS[idx]
        else:
            scenario = self._SCENARIOS[3]

        name, m_base, r_base, dr_base = scenario

        # Add mild random perturbation
        m = round(m_base * self._rng.uniform(0.8, 1.2), 4)
        r = round(r_base * self._rng.uniform(0.9, 1.1), 4)
        dr = round(dr_base * self._rng.uniform(0.5, 1.5), 4)

        r_cubed = round(r ** 3, 4)
        numerator = round(2.0 * self._G * m * dr, 4)
        df = round(numerator / r_cubed, 4)

        desc = (
            f"{name}: M = {m:.4e} kg, r = {r:.4e} m, "
            f"dr = {dr:.4e} m; find tidal acceleration"
        )
        return desc, {
            "name": name, "M": m, "r": r, "dr": dr,
            "G": self._G, "r_cubed": r_cubed,
            "numerator": numerator, "dF": df,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return [
            "dF = 2 * G * M * dr / r^3",
            f"r^3 = ({sd['r']:.4e})^3 = {sd['r_cubed']:.4e}",
            f"numerator = 2 * {sd['G']:.4e} * {sd['M']:.4e} * {sd['dr']:.4e} = {sd['numerator']:.4e}",
            f"dF = {sd['numerator']:.4e} / {sd['r_cubed']:.4e}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the tidal acceleration difference.

        Args:
            sd: Solution data.

        Returns:
            Tidal acceleration as a string.
        """
        return f"dF = {sd['dF']:.4e} m/s^2"


# ===================================================================
# 6. Drake equation  (tier 4)
# ===================================================================

@register
class DrakeEquationGenerator(AstronomyBase):
    """Estimate number of communicating civilisations via the Drake equation.

    Applies N = R* * fp * ne * fl * fi * fc * L to multiply seven
    factors representing star formation rate, fraction with planets,
    habitable planets per system, fraction developing life, fraction
    developing intelligence, fraction communicating, and civilisation
    lifetime.

    Difficulty scaling:
        Difficulty 1-3: factors are simple round numbers.
        Difficulty 4-6: factors have 2 decimal places.
        Difficulty 7-8: factors have 4 decimal places.

    Prerequisites:
        multiplication.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "drake_equation"

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
        return "estimate communicating civilisations using the Drake equation"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Drake equation problem.

        Creates seven factor values appropriate for the difficulty
        level and multiplies them together.

        Args:
            difficulty: Controls factor precision.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            decimals = 0
        elif difficulty <= 6:
            decimals = 2
        else:
            decimals = 4

        r_star = round(self._rng.uniform(1.0, 10.0), decimals)
        fp = round(self._rng.uniform(0.1, 1.0), max(decimals, 1))
        ne = round(self._rng.uniform(0.1, 5.0), max(decimals, 1))
        fl = round(self._rng.uniform(0.01, 1.0), max(decimals, 2))
        fi = round(self._rng.uniform(0.01, 1.0), max(decimals, 2))
        fc = round(self._rng.uniform(0.01, 1.0), max(decimals, 2))
        big_l = self._rng.randint(100, 10000 * max(1, difficulty))

        factors = [r_star, fp, ne, fl, fi, fc, big_l]
        product = r_star
        partials = [r_star]
        for f in factors[1:]:
            product = round(product * f, 4)
            partials.append(product)

        desc = (
            f"R*={r_star}, fp={fp}, ne={ne}, fl={fl}, "
            f"fi={fi}, fc={fc}, L={big_l}; find N"
        )
        return desc, {
            "R_star": r_star, "fp": fp, "ne": ne, "fl": fl,
            "fi": fi, "fc": fc, "L": big_l,
            "partials": partials, "N": partials[-1],
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        labels = ["R*", "R**fp", "...*ne", "...*fl", "...*fi", "...*fc", "...*L"]
        steps = ["N = R* * fp * ne * fl * fi * fc * L"]
        for label, val in zip(labels, sd["partials"]):
            steps.append(f"{label} = {val}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the estimated number of civilisations.

        Args:
            sd: Solution data.

        Returns:
            N as a string.
        """
        return f"N = {sd['N']}"
