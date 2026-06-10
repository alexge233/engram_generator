"""Special relativity generators -- Lorentz factor through four-momentum.

Covers the core phenomena of Einstein's special relativity: Lorentz
factor computation, time dilation, length contraction, relativistic
energy, spacetime intervals, Lorentz transformations, relativistic
velocity addition, and four-momentum.  All velocities are expressed
as fractions of c = 3e8 m/s.  Tiers range from 5 (introductory
relativity) to 6 (Lorentz transforms and four-momentum).
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


class RelativityFormatter:
    """Formats numbers for special relativity calculations.

    Provides scientific notation for large energies and momenta,
    and clean decimal formatting for dimensionless quantities
    like the Lorentz factor and velocity fractions.
    """

    @staticmethod
    def format_sci(value: float, sig_figs: int = 4) -> str:
        """Format a number in LaTeX scientific notation.

        Args:
            value: Number to format.
            sig_figs: Significant figures to retain.

        Returns:
            LaTeX scientific notation string.
        """
        if value == 0:
            return "0"
        exponent = int(math.floor(math.log10(abs(value))))
        mantissa = round(value / (10 ** exponent), sig_figs - 1)
        return f"{mantissa} \\times 10^{{{exponent}}}"

    @staticmethod
    def format_value(value: float, decimals: int = 4) -> str:
        """Format a numeric value, removing unnecessary trailing zeros.

        Args:
            value: Number to format.
            decimals: Maximum decimal places.

        Returns:
            Clean string representation.
        """
        if isinstance(value, float) and value == int(value):
            return str(int(value))
        rounded = round(value, decimals)
        if rounded == int(rounded):
            return str(int(rounded))
        return str(rounded)


class VelocitySampler:
    """Samples velocities as fractions of c scaled by difficulty.

    Provides consistent velocity generation across all relativity
    generators, ensuring velocities stay physically meaningful
    (strictly less than c) and scale appropriately with difficulty.

    Attributes:
        _rng: Seeded random number generator.
    """

    _C = 3e8

    def __init__(self, rng) -> None:
        """Initialise with a random number generator.

        Args:
            rng: A seeded random.Random instance.
        """
        self._rng = rng

    def sample_beta(self, difficulty: int) -> float:
        """Sample a velocity as a fraction of c (beta = v/c).

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Beta value in [0.1, 0.99].
        """
        if difficulty <= 3:
            return round(self._rng.uniform(0.1, 0.5), 2)
        if difficulty <= 6:
            return round(self._rng.uniform(0.5, 0.9), 2)
        return round(self._rng.uniform(0.9, 0.99), 2)

    def beta_to_velocity(self, beta: float) -> float:
        """Convert a beta value to velocity in m/s.

        Args:
            beta: Fraction of c.

        Returns:
            Velocity in m/s.
        """
        return beta * self._C


def _compute_gamma(beta: float) -> float:
    """Compute the Lorentz factor for a given beta.

    Args:
        beta: Velocity as a fraction of c (v/c).

    Returns:
        Lorentz factor gamma = 1 / sqrt(1 - beta^2).
    """
    return 1.0 / math.sqrt(1.0 - beta * beta)


# ---------------------------------------------------------------------------
# 1. Lorentz factor
# ---------------------------------------------------------------------------

@register
class LorentzFactorGenerator(StepGenerator):
    """Compute the Lorentz factor gamma = 1 / sqrt(1 - v^2/c^2).

    Given a velocity expressed as a fraction of c, the model must
    compute beta^2, subtract from 1, take the square root, and
    invert to obtain gamma.

    Input format:
        ``compute the Lorentz factor``

    Target format:
        ``\\gamma = \\frac{1}{\\sqrt{1 - v^2/c^2}} <step>
        \\beta = v/c = 0.6 <step>
        \\beta^2 = 0.36 <step>
        1 - \\beta^2 = 0.64 <step>
        \\sqrt{0.64} = 0.8 <step>
        \\gamma = 1/0.8 = 1.25``

    Difficulty scaling:
        d1-3: beta in [0.1, 0.5] (gamma near 1).
        d4-6: beta in [0.5, 0.9] (moderate gamma).
        d7-8: beta in [0.9, 0.99] (large gamma).

    Prerequisites:
        square_root.
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "lorentz_factor"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["square_root"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls velocity range.

        Returns:
            Natural language description.
        """
        return "compute the Lorentz factor"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a velocity and compute the Lorentz factor.

        Args:
            difficulty: Controls velocity range.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        sampler = VelocitySampler(self._rng)
        beta = sampler.sample_beta(difficulty)
        beta_sq = round(beta * beta, 4)
        one_minus = round(1.0 - beta_sq, 4)
        sqrt_val = round(math.sqrt(one_minus), 4)
        gamma = round(1.0 / sqrt_val, 4)

        return "\\gamma = \\frac{1}{\\sqrt{1 - v^2/c^2}}", {
            "beta": beta,
            "beta_sq": beta_sq,
            "one_minus": one_minus,
            "sqrt_val": sqrt_val,
            "gamma": gamma,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate step-by-step Lorentz factor computation.

        Args:
            data: Solution data with beta and intermediates.

        Returns:
            Steps showing beta^2, subtraction, sqrt, and inversion.
        """
        beta = data["beta"]
        beta_sq = data["beta_sq"]
        one_minus = data["one_minus"]
        sqrt_val = data["sqrt_val"]
        gamma = data["gamma"]
        return [
            f"\\beta = v/c = {beta}",
            f"\\beta^2 = {beta_sq}",
            f"1 - \\beta^2 = {one_minus}",
            f"\\sqrt{{{one_minus}}} = {sqrt_val}",
            f"\\gamma = 1/{sqrt_val} = {gamma}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the Lorentz factor.

        Args:
            data: Solution data.

        Returns:
            String representation of gamma.
        """
        return f"\\gamma = {data['gamma']}"


# ---------------------------------------------------------------------------
# 2. Time dilation
# ---------------------------------------------------------------------------

@register
class TimeDilationGenerator(StepGenerator):
    """Compute dilated time using dt' = gamma * dt_proper.

    Given a proper time interval (measured in the rest frame) and a
    velocity, the model computes the Lorentz factor and multiplies
    it by the proper time to obtain the dilated time observed in the
    lab frame.

    Input format:
        ``compute time dilation``

    Target format:
        ``\\Delta t' = \\gamma \\Delta t_0 <step>
        \\beta = 0.8 <step>
        \\gamma = 1/\\sqrt{1 - 0.64} = 1.6667 <step>
        \\Delta t' = 1.6667 \\times 5 = 8.3335 s``

    Difficulty scaling:
        d1-3: beta in [0.1, 0.5], proper time 1-10 s.
        d4-6: beta in [0.5, 0.9], proper time 1-100 s.
        d7-8: beta in [0.9, 0.99], proper time 1-1000 s.

    Prerequisites:
        lorentz_factor.
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "time_dilation"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["lorentz_factor"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls velocity and time ranges.

        Returns:
            Natural language description.
        """
        return "compute time dilation"

    def _sample_proper_time(self, difficulty: int) -> float:
        """Sample a proper time interval scaled by difficulty.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Proper time in seconds.
        """
        if difficulty <= 3:
            return float(self._rng.randint(1, 10))
        if difficulty <= 6:
            return float(self._rng.randint(1, 100))
        return float(self._rng.randint(1, 1000))

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate velocity and proper time, compute dilated time.

        Args:
            difficulty: Controls parameter ranges.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        sampler = VelocitySampler(self._rng)
        beta = sampler.sample_beta(difficulty)
        dt_proper = self._sample_proper_time(difficulty)
        gamma = round(_compute_gamma(beta), 4)
        dt_dilated = round(gamma * dt_proper, 4)

        return "\\Delta t' = \\gamma \\Delta t_0", {
            "beta": beta,
            "gamma": gamma,
            "dt_proper": dt_proper,
            "dt_dilated": dt_dilated,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate time dilation computation steps.

        Args:
            data: Solution data with beta, gamma, and times.

        Returns:
            Steps showing beta, gamma calculation, and multiplication.
        """
        beta = data["beta"]
        gamma = data["gamma"]
        dt0 = RelativityFormatter.format_value(data["dt_proper"])
        dt_prime = RelativityFormatter.format_value(data["dt_dilated"])
        beta_sq = round(beta * beta, 4)
        one_minus = round(1.0 - beta_sq, 4)
        return [
            f"\\beta = {beta}",
            f"\\gamma = 1/\\sqrt{{1 - {beta_sq}}} = {gamma}",
            f"\\Delta t' = {gamma} \\times {dt0} = {dt_prime} s",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the dilated time.

        Args:
            data: Solution data.

        Returns:
            String representation of the dilated time.
        """
        return (
            f"\\Delta t' = "
            f"{RelativityFormatter.format_value(data['dt_dilated'])} s"
        )


# ---------------------------------------------------------------------------
# 3. Length contraction
# ---------------------------------------------------------------------------

@register
class LengthContractionGenerator(StepGenerator):
    """Compute contracted length using L' = L_proper / gamma.

    Given a proper length (measured in the rest frame of the object)
    and a velocity, the model computes the Lorentz factor and divides
    the proper length by it to obtain the contracted length observed
    in the lab frame.

    Input format:
        ``compute length contraction``

    Target format:
        ``L' = L_0 / \\gamma <step>
        \\beta = 0.6 <step>
        \\gamma = 1/\\sqrt{1 - 0.36} = 1.25 <step>
        L' = 100 / 1.25 = 80 m``

    Difficulty scaling:
        d1-3: beta in [0.1, 0.5], length 10-100 m.
        d4-6: beta in [0.5, 0.9], length 10-1000 m.
        d7-8: beta in [0.9, 0.99], length 10-10000 m.

    Prerequisites:
        lorentz_factor.
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "length_contraction"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["lorentz_factor"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls velocity and length ranges.

        Returns:
            Natural language description.
        """
        return "compute length contraction"

    def _sample_proper_length(self, difficulty: int) -> float:
        """Sample a proper length scaled by difficulty.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Proper length in metres.
        """
        if difficulty <= 3:
            return float(self._rng.randint(10, 100))
        if difficulty <= 6:
            return float(self._rng.randint(10, 1000))
        return float(self._rng.randint(10, 10000))

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate velocity and proper length, compute contracted length.

        Args:
            difficulty: Controls parameter ranges.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        sampler = VelocitySampler(self._rng)
        beta = sampler.sample_beta(difficulty)
        length_proper = self._sample_proper_length(difficulty)
        gamma = round(_compute_gamma(beta), 4)
        length_contracted = round(length_proper / gamma, 4)

        return "L' = L_0 / \\gamma", {
            "beta": beta,
            "gamma": gamma,
            "length_proper": length_proper,
            "length_contracted": length_contracted,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate length contraction computation steps.

        Args:
            data: Solution data with beta, gamma, and lengths.

        Returns:
            Steps showing beta, gamma calculation, and division.
        """
        beta = data["beta"]
        gamma = data["gamma"]
        l0 = RelativityFormatter.format_value(data["length_proper"])
        l_prime = RelativityFormatter.format_value(data["length_contracted"])
        beta_sq = round(beta * beta, 4)
        return [
            f"\\beta = {beta}",
            f"\\gamma = 1/\\sqrt{{1 - {beta_sq}}} = {gamma}",
            f"L' = {l0} / {gamma} = {l_prime} m",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the contracted length.

        Args:
            data: Solution data.

        Returns:
            String representation of the contracted length.
        """
        return (
            f"L' = "
            f"{RelativityFormatter.format_value(data['length_contracted'])} m"
        )


# ---------------------------------------------------------------------------
# 4. Relativistic energy
# ---------------------------------------------------------------------------

@register
class RelativisticEnergyGenerator(StepGenerator):
    """Compute relativistic total and kinetic energy.

    Total energy E = gamma * m * c^2 and kinetic energy
    KE = (gamma - 1) * m * c^2.  Rest mass is given in kg and
    energy is expressed in Joules.

    Input format:
        ``compute relativistic energy``

    Target format:
        ``E = \\gamma m c^2, \\; KE = (\\gamma - 1) m c^2 <step>
        \\beta = 0.8 <step>
        \\gamma = 1.6667 <step>
        m c^2 = 1e-27 \\times (3 \\times 10^8)^2 = 9 \\times 10^{-11} J
        <step> E = 1.6667 \\times 9 \\times 10^{-11} = 1.5 \\times 10^{-10} J
        <step> KE = 0.6667 \\times 9 \\times 10^{-11} = 6 \\times 10^{-11} J``

    Difficulty scaling:
        d1-3: beta in [0.1, 0.5], mass ~ 1e-27 to 1e-25 kg.
        d4-6: beta in [0.5, 0.9], mass ~ 1e-27 to 1e-20 kg.
        d7-8: beta in [0.9, 0.99], mass ~ 1e-27 to 1e-15 kg.

    Prerequisites:
        lorentz_factor.
    """

    _C = 3e8

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "relativistic_energy"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["lorentz_factor"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls velocity and mass ranges.

        Returns:
            Natural language description.
        """
        return "compute relativistic energy"

    def _sample_mass(self, difficulty: int) -> float:
        """Sample a rest mass in kg scaled by difficulty.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Rest mass in kg.
        """
        if difficulty <= 3:
            exponent = self._rng.randint(-27, -25)
        elif difficulty <= 6:
            exponent = self._rng.randint(-27, -20)
        else:
            exponent = self._rng.randint(-27, -15)
        mantissa = self._rng.randint(1, 9)
        return float(mantissa) * (10 ** exponent)

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate velocity and mass, compute total and kinetic energy.

        Args:
            difficulty: Controls parameter ranges.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        sampler = VelocitySampler(self._rng)
        beta = sampler.sample_beta(difficulty)
        mass = self._sample_mass(difficulty)
        gamma = round(_compute_gamma(beta), 4)
        c_sq = self._C ** 2
        mc2 = mass * c_sq
        total_energy = gamma * mc2
        kinetic_energy = (gamma - 1.0) * mc2

        return "E = \\gamma m c^2, \\; KE = (\\gamma - 1) m c^2", {
            "beta": beta,
            "gamma": gamma,
            "mass": mass,
            "c_sq": c_sq,
            "mc2": mc2,
            "total_energy": total_energy,
            "kinetic_energy": kinetic_energy,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate relativistic energy computation steps.

        Args:
            data: Solution data with beta, gamma, mass, and energies.

        Returns:
            Steps showing gamma, mc^2, total energy, and kinetic energy.
        """
        beta = data["beta"]
        gamma = data["gamma"]
        m_str = RelativityFormatter.format_sci(data["mass"])
        mc2_str = RelativityFormatter.format_sci(data["mc2"])
        e_str = RelativityFormatter.format_sci(data["total_energy"])
        ke_str = RelativityFormatter.format_sci(data["kinetic_energy"])
        gamma_minus_1 = round(gamma - 1.0, 4)
        return [
            f"\\beta = {beta}, \\gamma = {gamma}",
            f"mc^2 = ({m_str})(9 \\times 10^{{16}}) = {mc2_str} J",
            f"E = {gamma} \\times {mc2_str} = {e_str} J",
            f"KE = {gamma_minus_1} \\times {mc2_str} = {ke_str} J",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the total and kinetic energy.

        Args:
            data: Solution data.

        Returns:
            String with both E and KE.
        """
        e_str = RelativityFormatter.format_sci(data["total_energy"])
        ke_str = RelativityFormatter.format_sci(data["kinetic_energy"])
        return f"E = {e_str} J, KE = {ke_str} J"


# ---------------------------------------------------------------------------
# 5. Spacetime interval
# ---------------------------------------------------------------------------

@register
class SpacetimeIntervalGenerator(StepGenerator):
    """Compute the spacetime interval and classify it.

    Given two events with coordinate differences (dt, dx, dy, dz),
    compute ds^2 = -c^2 dt^2 + dx^2 + dy^2 + dz^2 and classify
    the interval as timelike (ds^2 < 0), spacelike (ds^2 > 0),
    or lightlike (ds^2 = 0).

    Input format:
        ``compute the spacetime interval``

    Target format:
        ``ds^2 = -c^2 \\Delta t^2 + \\Delta x^2 + \\Delta y^2
        + \\Delta z^2 <step>
        -c^2 \\Delta t^2 = -(3e8)^2(2)^2 = -3.6e17 <step>
        \\Delta x^2 + \\Delta y^2 + \\Delta z^2 = 1e16 <step>
        ds^2 = -3.5e17 <step> timelike (ds^2 < 0)``

    Difficulty scaling:
        d1-3: dy = dz = 0, small dt and dx.
        d4-6: one nonzero transverse component.
        d7-8: all three spatial components nonzero.

    Prerequisites:
        exponentiation.
    """

    _C = 3e8

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "spacetime_interval"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["exponentiation"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls dimensionality of the problem.

        Returns:
            Natural language description.
        """
        return "compute the spacetime interval"

    def _sample_events(self, difficulty: int) -> tuple[float, float, float, float]:
        """Sample coordinate differences for two events.

        Args:
            difficulty: Controls which spatial components are nonzero.

        Returns:
            Tuple of (dt, dx, dy, dz) in SI units.
        """
        dt = round(self._rng.uniform(0.5, 5.0), 2)
        dx = round(self._rng.uniform(1e7, 1e9), 0)
        if difficulty <= 3:
            dy = 0.0
            dz = 0.0
        elif difficulty <= 6:
            dy = round(self._rng.uniform(1e6, 1e8), 0)
            dz = 0.0
        else:
            dy = round(self._rng.uniform(1e6, 1e8), 0)
            dz = round(self._rng.uniform(1e6, 1e8), 0)
        return dt, dx, dy, dz

    def _classify_interval(self, ds_sq: float) -> str:
        """Classify the spacetime interval.

        Args:
            ds_sq: The computed interval ds^2.

        Returns:
            Classification string: timelike, spacelike, or lightlike.
        """
        if abs(ds_sq) < 1e-6:
            return "lightlike"
        if ds_sq < 0:
            return "timelike"
        return "spacelike"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate events and compute the spacetime interval.

        Args:
            difficulty: Controls dimensionality.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        dt, dx, dy, dz = self._sample_events(difficulty)
        c_sq = self._C ** 2
        time_term = -c_sq * dt * dt
        space_term = dx * dx + dy * dy + dz * dz
        ds_sq = time_term + space_term
        classification = self._classify_interval(ds_sq)

        formula = (
            "ds^2 = -c^2 \\Delta t^2 + \\Delta x^2"
            " + \\Delta y^2 + \\Delta z^2"
        )
        return formula, {
            "dt": dt, "dx": dx, "dy": dy, "dz": dz,
            "time_term": time_term,
            "space_term": space_term,
            "ds_sq": ds_sq,
            "classification": classification,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate spacetime interval computation steps.

        Args:
            data: Solution data with event separations and interval.

        Returns:
            Steps showing time term, space term, sum, and classification.
        """
        dt = data["dt"]
        dx = RelativityFormatter.format_sci(data["dx"])
        time_str = RelativityFormatter.format_sci(data["time_term"])
        space_str = RelativityFormatter.format_sci(data["space_term"])
        ds_str = RelativityFormatter.format_sci(data["ds_sq"])
        cls = data["classification"]
        steps = [
            f"-c^2 \\Delta t^2 = -(3 \\times 10^8)^2({dt})^2 = {time_str}",
            f"\\Delta x^2 + \\Delta y^2 + \\Delta z^2 = {space_str}",
            f"ds^2 = {time_str} + {space_str} = {ds_str}",
        ]
        if cls == "timelike":
            steps.append(f"{cls} (ds^2 < 0)")
        elif cls == "spacelike":
            steps.append(f"{cls} (ds^2 > 0)")
        else:
            steps.append(f"{cls} (ds^2 = 0)")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the interval value and classification.

        Args:
            data: Solution data.

        Returns:
            String with ds^2 value and classification.
        """
        ds_str = RelativityFormatter.format_sci(data["ds_sq"])
        return f"ds^2 = {ds_str}, {data['classification']}"


# ---------------------------------------------------------------------------
# 6. Lorentz transformation
# ---------------------------------------------------------------------------

@register
class LorentzTransformGenerator(StepGenerator):
    """Apply a Lorentz boost to transform coordinates.

    Given event coordinates (t, x) in frame S and a relative
    velocity v between frames, compute the transformed coordinates
    (t', x') in frame S' using x' = gamma(x - vt) and
    t' = gamma(t - vx/c^2).

    Input format:
        ``apply Lorentz transformation``

    Target format:
        ``x' = \\gamma(x - vt), \\; t' = \\gamma(t - vx/c^2) <step>
        \\beta = 0.6, \\gamma = 1.25 <step>
        x - vt = 1e8 - (1.8e8)(2) = -2.6e8 <step>
        x' = 1.25 \\times (-2.6e8) = -3.25e8 m <step>
        t - vx/c^2 = 2 - (1.8e8)(1e8)/(9e16) = 1.8 <step>
        t' = 1.25 \\times 1.8 = 2.25 s``

    Difficulty scaling:
        d1-3: beta in [0.1, 0.5], small coordinates.
        d4-6: beta in [0.5, 0.9], moderate coordinates.
        d7-8: beta in [0.9, 0.99], large coordinates.

    Prerequisites:
        lorentz_factor.
    """

    _C = 3e8

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "lorentz_transform"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["lorentz_factor"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls velocity and coordinate ranges.

        Returns:
            Natural language description.
        """
        return "apply Lorentz transformation"

    def _sample_coordinates(self, difficulty: int) -> tuple[float, float]:
        """Sample event coordinates (t, x) in SI units.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (time_s, position_m).
        """
        t = round(self._rng.uniform(0.5, 5.0), 2)
        if difficulty <= 3:
            x = round(self._rng.uniform(1e7, 5e8), 0)
        elif difficulty <= 6:
            x = round(self._rng.uniform(1e8, 5e9), 0)
        else:
            x = round(self._rng.uniform(1e9, 5e10), 0)
        return t, x

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate coordinates and velocity, apply Lorentz transform.

        Args:
            difficulty: Controls parameter ranges.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        sampler = VelocitySampler(self._rng)
        beta = sampler.sample_beta(difficulty)
        v = beta * self._C
        gamma = round(_compute_gamma(beta), 4)
        t, x = self._sample_coordinates(difficulty)
        c_sq = self._C ** 2

        x_minus_vt = x - v * t
        x_prime = round(gamma * x_minus_vt, 4)
        t_minus_vx_c2 = t - v * x / c_sq
        t_prime = round(gamma * t_minus_vx_c2, 4)

        return "x' = \\gamma(x - vt), \\; t' = \\gamma(t - vx/c^2)", {
            "beta": beta,
            "v": v,
            "gamma": gamma,
            "t": t,
            "x": x,
            "x_minus_vt": x_minus_vt,
            "x_prime": x_prime,
            "t_minus_vx_c2": round(t_minus_vx_c2, 4),
            "t_prime": t_prime,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Lorentz transformation computation steps.

        Args:
            data: Solution data with coordinates and intermediates.

        Returns:
            Steps showing gamma, spatial transform, and time transform.
        """
        beta = data["beta"]
        gamma = data["gamma"]
        v_str = RelativityFormatter.format_sci(data["v"])
        t = data["t"]
        x_str = RelativityFormatter.format_sci(data["x"])
        x_vt_str = RelativityFormatter.format_sci(data["x_minus_vt"])
        x_p_str = RelativityFormatter.format_sci(data["x_prime"])
        t_vx_str = RelativityFormatter.format_value(data["t_minus_vx_c2"])
        t_p_str = RelativityFormatter.format_value(data["t_prime"])
        return [
            f"\\beta = {beta}, \\gamma = {gamma}",
            f"x - vt = {x_str} - ({v_str})({t}) = {x_vt_str}",
            f"x' = {gamma} \\times {x_vt_str} = {x_p_str} m",
            f"t - vx/c^2 = {t_vx_str}",
            f"t' = {gamma} \\times {t_vx_str} = {t_p_str} s",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the transformed coordinates.

        Args:
            data: Solution data.

        Returns:
            String with (t', x') values.
        """
        x_p = RelativityFormatter.format_sci(data["x_prime"])
        t_p = RelativityFormatter.format_value(data["t_prime"])
        return f"x' = {x_p} m, t' = {t_p} s"


# ---------------------------------------------------------------------------
# 7. Relativistic velocity addition
# ---------------------------------------------------------------------------

@register
class VelocityAdditionGenerator(StepGenerator):
    """Compute relativistic velocity addition.

    Given two velocities u and v (as fractions of c), compute the
    relativistic sum u' = (u + v) / (1 + uv/c^2).  Since u and v
    are expressed as beta values, this simplifies to
    beta' = (beta_u + beta_v) / (1 + beta_u * beta_v).

    Input format:
        ``compute relativistic velocity addition``

    Target format:
        ``u' = \\frac{u + v}{1 + uv/c^2} <step>
        \\beta_u = 0.6, \\beta_v = 0.8 <step>
        \\beta_u + \\beta_v = 1.4 <step>
        \\beta_u \\beta_v = 0.48 <step>
        1 + 0.48 = 1.48 <step>
        \\beta' = 1.4 / 1.48 = 0.9459``

    Difficulty scaling:
        d1-3: both betas in [0.1, 0.5].
        d4-6: betas in [0.3, 0.8].
        d7-8: betas in [0.7, 0.99].

    Prerequisites:
        division.
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "velocity_addition"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["division"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls velocity ranges.

        Returns:
            Natural language description.
        """
        return "compute relativistic velocity addition"

    def _sample_two_betas(self, difficulty: int) -> tuple[float, float]:
        """Sample two velocity fractions scaled by difficulty.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (beta_u, beta_v).
        """
        if difficulty <= 3:
            beta_u = round(self._rng.uniform(0.1, 0.5), 2)
            beta_v = round(self._rng.uniform(0.1, 0.5), 2)
        elif difficulty <= 6:
            beta_u = round(self._rng.uniform(0.3, 0.8), 2)
            beta_v = round(self._rng.uniform(0.3, 0.8), 2)
        else:
            beta_u = round(self._rng.uniform(0.7, 0.99), 2)
            beta_v = round(self._rng.uniform(0.7, 0.99), 2)
        return beta_u, beta_v

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate two velocities and compute their relativistic sum.

        Args:
            difficulty: Controls velocity ranges.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        beta_u, beta_v = self._sample_two_betas(difficulty)
        numerator = round(beta_u + beta_v, 4)
        product = round(beta_u * beta_v, 4)
        denominator = round(1.0 + product, 4)
        beta_result = round(numerator / denominator, 4)

        return "u' = \\frac{u + v}{1 + uv/c^2}", {
            "beta_u": beta_u,
            "beta_v": beta_v,
            "numerator": numerator,
            "product": product,
            "denominator": denominator,
            "beta_result": beta_result,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate velocity addition computation steps.

        Args:
            data: Solution data with betas and intermediates.

        Returns:
            Steps showing sum, product, denominator, and division.
        """
        bu = data["beta_u"]
        bv = data["beta_v"]
        num = data["numerator"]
        prod = data["product"]
        denom = data["denominator"]
        result = data["beta_result"]
        return [
            f"\\beta_u = {bu}, \\beta_v = {bv}",
            f"\\beta_u + \\beta_v = {num}",
            f"\\beta_u \\beta_v = {prod}",
            f"1 + {prod} = {denom}",
            f"\\beta' = {num} / {denom} = {result}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the combined velocity as a fraction of c.

        Args:
            data: Solution data.

        Returns:
            String representation of beta'.
        """
        return f"\\beta' = {data['beta_result']}c"


# ---------------------------------------------------------------------------
# 8. Four-momentum
# ---------------------------------------------------------------------------

@register
class FourMomentumGenerator(StepGenerator):
    """Compute the four-momentum and verify the energy-momentum relation.

    Given a rest mass m and velocity v (as a fraction of c), compute
    the four-momentum (E/c, px, py, pz) where the motion is along
    the x-axis (py = pz = 0).  Then verify E^2 = (pc)^2 + (mc^2)^2.

    Input format:
        ``compute four-momentum``

    Target format:
        ``p^\\mu = (E/c, p_x, 0, 0) <step>
        \\beta = 0.8, \\gamma = 1.6667 <step>
        E = \\gamma m c^2 = ... <step>
        p_x = \\gamma m v = ... <step>
        p^\\mu = (E/c, p_x, 0, 0) <step>
        verify: E^2 = (p_x c)^2 + (mc^2)^2``

    Difficulty scaling:
        d1-3: beta in [0.1, 0.5], mass ~ 1e-27 kg.
        d4-6: beta in [0.5, 0.9], mass ~ 1e-27 to 1e-20 kg.
        d7-8: beta in [0.9, 0.99], mass ~ 1e-27 to 1e-15 kg.

    Prerequisites:
        relativistic_energy.
    """

    _C = 3e8

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "four_momentum"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["relativistic_energy"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls velocity and mass ranges.

        Returns:
            Natural language description.
        """
        return "compute four-momentum"

    def _sample_mass(self, difficulty: int) -> float:
        """Sample a rest mass in kg scaled by difficulty.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Rest mass in kg.
        """
        if difficulty <= 3:
            exponent = -27
        elif difficulty <= 6:
            exponent = self._rng.randint(-27, -20)
        else:
            exponent = self._rng.randint(-27, -15)
        mantissa = self._rng.randint(1, 9)
        return float(mantissa) * (10 ** exponent)

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate mass and velocity, compute four-momentum components.

        Args:
            difficulty: Controls parameter ranges.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        sampler = VelocitySampler(self._rng)
        beta = sampler.sample_beta(difficulty)
        v = beta * self._C
        mass = self._sample_mass(difficulty)
        gamma = round(_compute_gamma(beta), 4)
        c_sq = self._C ** 2

        energy = gamma * mass * c_sq
        e_over_c = energy / self._C
        px = gamma * mass * v
        mc2 = mass * c_sq
        pc_sq = (px * self._C) ** 2
        mc2_sq = mc2 ** 2
        e_sq = energy ** 2
        check = pc_sq + mc2_sq

        return "p^\\mu = (E/c, p_x, 0, 0)", {
            "beta": beta,
            "v": v,
            "gamma": gamma,
            "mass": mass,
            "energy": energy,
            "e_over_c": e_over_c,
            "px": px,
            "mc2": mc2,
            "e_sq": e_sq,
            "check": check,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate four-momentum computation and verification steps.

        Args:
            data: Solution data with mass, velocity, and momentum.

        Returns:
            Steps showing gamma, energy, momentum, four-vector, and check.
        """
        beta = data["beta"]
        gamma = data["gamma"]
        m_str = RelativityFormatter.format_sci(data["mass"])
        e_str = RelativityFormatter.format_sci(data["energy"])
        ec_str = RelativityFormatter.format_sci(data["e_over_c"])
        px_str = RelativityFormatter.format_sci(data["px"])
        mc2_str = RelativityFormatter.format_sci(data["mc2"])
        e_sq_str = RelativityFormatter.format_sci(data["e_sq"])
        chk_str = RelativityFormatter.format_sci(data["check"])
        return [
            f"\\beta = {beta}, \\gamma = {gamma}",
            f"E = \\gamma m c^2 = {gamma}({m_str})(9 \\times 10^{{16}}) = {e_str} J",
            f"p_x = \\gamma m v = {px_str} kg m/s",
            f"p^\\mu = ({ec_str}, {px_str}, 0, 0)",
            f"E^2 = {e_sq_str}, (p_x c)^2 + (mc^2)^2 = {chk_str}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the four-momentum components.

        Args:
            data: Solution data.

        Returns:
            String representation of the four-momentum.
        """
        ec_str = RelativityFormatter.format_sci(data["e_over_c"])
        px_str = RelativityFormatter.format_sci(data["px"])
        return f"p^\\mu = ({ec_str}, {px_str}, 0, 0)"
