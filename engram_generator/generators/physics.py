"""Physics generators — mechanics, waves, gravity, and astrophysics.

Covers classical mechanics (kinematics, energy, momentum), wave mechanics,
gravitational physics, pendulum motion, and astrophysical quantities
(Schwarzschild radius, orbital period, redshift, stellar luminosity).
Tiers range from 4 (introductory physics) to 6 (astrophysics).
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register
from engram_generator.generators.tier4 import PhysicsParameterSampler


class ScientificFormatter:
    """Formats numbers in scientific notation and handles rounding.

    Provides consistent formatting for physics results, including
    scientific notation for very large or very small numbers and
    clean rounding for intermediate values.

    Example:
        >>> ScientificFormatter.format_sci(6.674e-11)
        '6.674 \\\\times 10^{-11}'
        >>> ScientificFormatter.format_value(22.5)
        '22.5'
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


@register
class KinematicsSGenerator(StepGenerator):
    """Kinematic displacement using s = v_0 t + (1/2) a t^2.

    Generates problems where the model must compute displacement
    given initial velocity, acceleration, and time by substituting
    into the second kinematic equation and evaluating step by step.

    Input format:
        ``compute displacement using kinematics``

    Target format:
        ``s = v_0 t + \\frac{1}{2}at^2 <step> s = 10(4) + \\frac{1}{2}(3)(4^2)
        <step> s = 40 + \\frac{1}{2}(3)(16) <step> s = 40 + 24 <step> s = 64``

    Difficulty scaling:
        Difficulty 1: v0 in [1,10], a in [1,10], t in [1,10].
        Difficulty 8: v0 in [8,80], a in [8,80], t in [8,80].
        Magnitudes scale linearly with difficulty.

    Prerequisites:
        multiplication, exponentiation.

    Example:
        >>> gen = KinematicsSGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'kinematics_displacement'
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "kinematics_displacement"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["multiplication", "exponentiation"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls parameter magnitude.

        Returns:
            Natural language description.
        """
        return "compute displacement using kinematics"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate kinematics parameters and compute displacement.

        Args:
            difficulty: Controls parameter magnitude.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        sampler = PhysicsParameterSampler(self._rng)
        v0 = sampler.sample(difficulty)
        a = sampler.sample(difficulty)
        t = sampler.sample(difficulty)
        t_sq = t * t
        v0t = v0 * t
        half_at_sq = a * t_sq / 2
        s = v0t + half_at_sq
        return "s = v_0 t + \\frac{1}{2}at^2", {
            "v0": v0, "a": a, "t": t, "t_sq": t_sq,
            "v0t": v0t, "half_at_sq": half_at_sq, "s": s,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate substitution and arithmetic steps.

        Args:
            data: Solution data with v0, a, t, and intermediates.

        Returns:
            Steps showing substitution, squaring, and addition.
        """
        v0, a, t = data["v0"], data["a"], data["t"]
        t_sq = data["t_sq"]
        v0t = data["v0t"]
        half_at_sq = data["half_at_sq"]
        return [
            f"s = {v0}({t}) + \\frac{{1}}{{2}}({a})({t}^2)",
            f"s = {v0t} + \\frac{{1}}{{2}}({a})({t_sq})",
            f"s = {v0t} + {ScientificFormatter.format_value(half_at_sq)}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the displacement.

        Args:
            data: Solution data.

        Returns:
            String representation of s.
        """
        return f"s = {ScientificFormatter.format_value(data['s'])}"


@register
class PotentialEnergyGenerator(StepGenerator):
    """Potential energy computation using PE = mgh.

    Generates problems where the model must compute gravitational
    potential energy by multiplying mass, gravitational acceleration,
    and height.

    Input format:
        ``compute potential energy``

    Target format:
        ``PE = mgh <step> PE = (5)(9.8)(10) <step> PE = (5)(98)
        <step> PE = 490``

    Difficulty scaling:
        Difficulty 1: m in [1,10], h in [1,10], g = 9.8.
        Difficulty 8: m in [8,80], h in [8,80], g = 9.8.
        Magnitudes scale linearly with difficulty.

    Prerequisites:
        multiplication.

    Example:
        >>> gen = PotentialEnergyGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'potential_energy'
    """

    _G = 9.8

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "potential_energy"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["multiplication"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls parameter magnitude.

        Returns:
            Natural language description.
        """
        return "compute potential energy"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate mass and height, then compute potential energy.

        Args:
            difficulty: Controls parameter magnitude.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        sampler = PhysicsParameterSampler(self._rng)
        m = sampler.sample(difficulty)
        h = sampler.sample(difficulty)
        gh = round(self._G * h, 2)
        pe = round(m * gh, 2)
        return "PE = mgh", {"m": m, "h": h, "g": self._G, "gh": gh, "pe": pe}

    def _create_steps(self, data: dict) -> list[str]:
        """Generate multiplication steps for PE = mgh.

        Args:
            data: Solution data with m, h, g, and intermediates.

        Returns:
            Steps showing substitution and computation.
        """
        m, h, g = data["m"], data["h"], data["g"]
        gh = data["gh"]
        return [
            f"PE = ({m})({g})({h})",
            f"PE = ({m})({gh})",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the potential energy.

        Args:
            data: Solution data.

        Returns:
            String representation of PE.
        """
        return f"PE = {ScientificFormatter.format_value(data['pe'])}"


@register
class ConservationEnergyGenerator(StepGenerator):
    """Conservation of energy: KE_1 + PE_1 = KE_2 + PE_2.

    Given three of the four energy values, solves for the fourth.
    This tests the model's ability to rearrange and substitute into
    an energy conservation equation.

    Input format:
        ``apply conservation of energy``

    Target format:
        ``KE_1 + PE_1 = KE_2 + PE_2 <step> 100 + 200 = KE_2 + 50
        <step> 300 = KE_2 + 50 <step> KE_2 = 250``

    Difficulty scaling:
        Difficulty 1: energy values in [10, 100].
        Difficulty 8: energy values in [80, 800].
        Magnitudes scale linearly with difficulty.

    Prerequisites:
        kinetic_energy, potential_energy.

    Example:
        >>> gen = ConservationEnergyGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'conservation_energy'
    """

    _SOLVE_TARGETS = ["KE_1", "PE_1", "KE_2", "PE_2"]

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "conservation_energy"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["kinetic_energy", "potential_energy"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls energy magnitude.

        Returns:
            Natural language description.
        """
        return "apply conservation of energy"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate four energy values and hide one.

        Ensures the total energy is consistent on both sides
        before hiding one variable.

        Args:
            difficulty: Controls energy magnitude.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        sampler = PhysicsParameterSampler(self._rng)
        ke1 = sampler.sample(difficulty, 10, 100)
        pe1 = sampler.sample(difficulty, 10, 100)
        total = ke1 + pe1
        pe2 = sampler.sample(difficulty, 1, max(2, total // max(1, difficulty)))
        pe2 = min(pe2, total - 1)
        ke2 = total - pe2
        target = self._rng.choice(self._SOLVE_TARGETS)
        values = {"KE_1": ke1, "PE_1": pe1, "KE_2": ke2, "PE_2": pe2}
        return "KE_1 + PE_1 = KE_2 + PE_2", {
            "values": values, "target": target, "total": total,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate rearrangement and substitution steps.

        Args:
            data: Solution data with values and target.

        Returns:
            Steps showing substitution and solving for the unknown.
        """
        values = data["values"]
        target = data["target"]
        return self._solve_for_target(values, target, data["total"])

    def _solve_for_target(self, values: dict[str, int], target: str,
                          total: int) -> list[str]:
        """Generate steps for solving the unknown energy value.

        Args:
            values: Dict of all four energy values.
            target: Name of the unknown variable.
            total: Total energy (KE_1 + PE_1).

        Returns:
            Steps showing the algebra.
        """
        known = {k: v for k, v in values.items() if k != target}
        known_labels = sorted(known.keys())
        known_strs = [f"{k}={known[k]}" for k in known_labels]
        known_summary = ", ".join(known_strs)

        if target in ("KE_1", "PE_1"):
            other_lhs = "PE_1" if target == "KE_1" else "KE_1"
            rhs_sum = values["KE_2"] + values["PE_2"]
            answer = rhs_sum - values[other_lhs]
            return [
                f"given: {known_summary}",
                f"KE_2 + PE_2 = {values['KE_2']} + {values['PE_2']} = {rhs_sum}",
                f"{target} = {rhs_sum} - {values[other_lhs]} = {answer}",
            ]

        other_rhs = "PE_2" if target == "KE_2" else "KE_2"
        lhs_sum = values["KE_1"] + values["PE_1"]
        answer = lhs_sum - values[other_rhs]
        return [
            f"given: {known_summary}",
            f"KE_1 + PE_1 = {values['KE_1']} + {values['PE_1']} = {lhs_sum}",
            f"{target} = {lhs_sum} - {values[other_rhs]} = {answer}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the solved energy value.

        Args:
            data: Solution data.

        Returns:
            String representation of the unknown energy.
        """
        target = data["target"]
        return f"{target} = {data['values'][target]}"


@register
class MomentumGenerator(StepGenerator):
    """Conservation of momentum in a two-body collision.

    Generates a collision problem where m1*v1 + m2*v2 = m1*v1' + m2*v2'.
    Given five of the six values, solves for the sixth. Demonstrates
    conservation of linear momentum in one dimension.

    Input format:
        ``apply conservation of momentum``

    Target format:
        ``m_1 v_1 + m_2 v_2 = m_1 v_1' + m_2 v_2' <step>
        (5)(10) + (3)(0) = (5)(4) + (3)(v_2') <step>
        50 + 0 = 20 + 3 v_2' <step> 30 = 3 v_2' <step> v_2' = 10``

    Difficulty scaling:
        Difficulty 1: masses in [1,10], velocities in [1,10].
        Difficulty 8: masses in [8,80], velocities in [8,80].

    Prerequisites:
        multiplication, system_equations.

    Example:
        >>> gen = MomentumGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'momentum'
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "momentum"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["multiplication", "system_equations"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls parameter magnitude.

        Returns:
            Natural language description.
        """
        return "apply conservation of momentum"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate collision parameters and solve for final velocity.

        Constructs values so that v2_final is always an integer.

        Args:
            difficulty: Controls parameter magnitude.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        sampler = PhysicsParameterSampler(self._rng)
        m1 = sampler.sample(difficulty)
        m2 = sampler.sample(difficulty)
        v1 = sampler.sample(difficulty)
        v2 = sampler.sample(difficulty, 0, 5)
        v1_final = sampler.sample(difficulty, 0, max(1, v1 - 1))
        p_initial = m1 * v1 + m2 * v2
        p1_final = m1 * v1_final
        p2_final = p_initial - p1_final
        v2_final = p2_final / m2

        return "m_1 v_1 + m_2 v_2 = m_1 v_1' + m_2 v_2'", {
            "m1": m1, "m2": m2, "v1": v1, "v2": v2,
            "v1_final": v1_final, "v2_final": v2_final,
            "p_initial": p_initial, "p1_final": p1_final,
            "p2_final": p2_final,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate momentum conservation steps.

        Args:
            data: Solution data with masses and velocities.

        Returns:
            Steps showing substitution and solving for v2'.
        """
        m1, m2 = data["m1"], data["m2"]
        v1, v2 = data["v1"], data["v2"]
        v1f = data["v1_final"]
        p_init = data["p_initial"]
        p1f = data["p1_final"]
        p2f = data["p2_final"]

        return [
            f"({m1})({v1}) + ({m2})({v2}) = ({m1})({v1f}) + ({m2})(v_2')",
            f"{p_init} = {p1f} + {m2} v_2'",
            f"{p2f} = {m2} v_2'",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the solved final velocity.

        Args:
            data: Solution data.

        Returns:
            String representation of v2'.
        """
        return f"v_2' = {ScientificFormatter.format_value(data['v2_final'])}"


@register
class WaveEquationGenerator(StepGenerator):
    """Wave equation application: v = f * lambda.

    Generates wave problems where the model solves for velocity,
    frequency, or wavelength using the fundamental wave equation.
    Randomly chooses which variable to solve for.

    Input format:
        ``apply wave equation``

    Target format:
        ``v = f \\lambda <step> v = (500)(0.68) <step> v = 340``

    Difficulty scaling:
        Difficulty 1: f in [100,500] Hz, lambda in [0.1,2.0] m.
        Difficulty 8: f in [100,5000] Hz, lambda in [0.01,10.0] m.

    Prerequisites:
        multiplication, division.

    Example:
        >>> gen = WaveEquationGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'wave_equation'
    """

    _SOLVE_TARGETS = ["v", "f", "lambda"]

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "wave_equation"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["multiplication", "division"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls parameter ranges.

        Returns:
            Natural language description.
        """
        return "apply wave equation"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate wave parameters and choose solve target.

        Args:
            difficulty: Controls parameter ranges.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        f = self._rng.randint(100, 100 + 500 * max(1, difficulty))
        lam = round(self._rng.uniform(0.1, 0.5 + difficulty * 1.2), 2)
        v = round(f * lam, 2)
        target = self._rng.choice(self._SOLVE_TARGETS)

        return "v = f \\lambda", {
            "v": v, "f": f, "lambda": lam, "target": target,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate rearrangement and substitution steps.

        Args:
            data: Solution data with v, f, lambda, and target.

        Returns:
            Steps showing formula manipulation and computation.
        """
        target = data["target"]
        if target == "v":
            return self._steps_solve_v(data)
        if target == "f":
            return self._steps_solve_f(data)
        return self._steps_solve_lambda(data)

    def _steps_solve_v(self, data: dict) -> list[str]:
        """Generate steps for solving for velocity.

        Args:
            data: Solution data.

        Returns:
            Steps for v = f * lambda.
        """
        return [
            f"v = ({data['f']})({data['lambda']})",
        ]

    def _steps_solve_f(self, data: dict) -> list[str]:
        """Generate steps for solving for frequency.

        Args:
            data: Solution data.

        Returns:
            Steps for f = v / lambda.
        """
        return [
            f"f = \\frac{{v}}{{\\lambda}}",
            f"f = \\frac{{{data['v']}}}{{{data['lambda']}}}",
        ]

    def _steps_solve_lambda(self, data: dict) -> list[str]:
        """Generate steps for solving for wavelength.

        Args:
            data: Solution data.

        Returns:
            Steps for lambda = v / f.
        """
        return [
            f"\\lambda = \\frac{{v}}{{f}}",
            f"\\lambda = \\frac{{{data['v']}}}{{{data['f']}}}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the solved variable value.

        Args:
            data: Solution data.

        Returns:
            String representation of the target variable.
        """
        target = data["target"]
        val = data[target]
        label = "\\lambda" if target == "lambda" else target
        return f"{label} = {ScientificFormatter.format_value(val)}"


@register
class GravitationalForceGenerator(StepGenerator):
    """Gravitational force using F = GMm/r^2.

    Computes the gravitational force between two masses separated
    by distance r using Newton's universal law of gravitation with
    G = 6.674e-11 N m^2/kg^2. Uses scientific notation throughout.

    Input format:
        ``compute gravitational force``

    Target format:
        ``F = \\frac{GMm}{r^2} <step>
        F = \\frac{(6.674 \\times 10^{-11})(5.97 \\times 10^{24})(70)}{(6.371 \\times 10^{6})^2}
        <step> numerator = 2.787 \\times 10^{16} <step>
        denominator = 4.059 \\times 10^{13} <step> F = 686.7 N``

    Difficulty scaling:
        Difficulty 1-3: round masses (10-100 kg), moderate distances.
        Difficulty 4-6: planetary-scale masses.
        Difficulty 7-8: stellar-scale masses.

    Prerequisites:
        multiplication, exponentiation, division.

    Example:
        >>> gen = GravitationalForceGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'gravitational_force'
    """

    _G = 6.674e-11

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "gravitational_force"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["multiplication", "exponentiation", "division"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls mass and distance scales.

        Returns:
            Natural language description.
        """
        return "compute gravitational force"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate masses and distance, then compute gravitational force.

        Args:
            difficulty: Controls parameter scales.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        big_m, small_m, r = self._sample_parameters(difficulty)
        r_sq = r * r
        numerator = self._G * big_m * small_m
        force = numerator / r_sq

        return "F = \\frac{GMm}{r^2}", {
            "G": self._G, "M": big_m, "m": small_m,
            "r": r, "r_sq": r_sq,
            "numerator": numerator, "force": force,
        }

    def _sample_parameters(self, difficulty: int) -> tuple[float, float, float]:
        """Sample mass and distance parameters scaled by difficulty.

        Args:
            difficulty: Difficulty level controlling scale.

        Returns:
            Tuple of (big_mass, small_mass, distance).
        """
        if difficulty <= 3:
            big_m = float(self._rng.randint(10, 100) * 10)
            small_m = float(self._rng.randint(1, 100))
            r = float(self._rng.randint(1, 20))
        elif difficulty <= 6:
            big_m = float(self._rng.randint(1, 9)) * 1e24
            small_m = float(self._rng.randint(10, 1000))
            r = float(self._rng.randint(1, 9)) * 1e6
        else:
            big_m = float(self._rng.randint(1, 9)) * 1e30
            small_m = float(self._rng.randint(1, 9)) * 1e24
            r = float(self._rng.randint(1, 9)) * 1e10
        return big_m, small_m, r

    def _create_steps(self, data: dict) -> list[str]:
        """Generate substitution and computation steps.

        Args:
            data: Solution data with G, M, m, r, and force.

        Returns:
            Steps showing numerator, denominator, and division.
        """
        g_str = ScientificFormatter.format_sci(data["G"])
        m_str = ScientificFormatter.format_sci(data["M"])
        sm_str = ScientificFormatter.format_sci(data["m"])
        r_str = ScientificFormatter.format_sci(data["r"])
        num_str = ScientificFormatter.format_sci(data["numerator"])
        den_str = ScientificFormatter.format_sci(data["r_sq"])

        return [
            f"F = \\frac{{({g_str})({m_str})({sm_str})}}{{({r_str})^2}}",
            f"numerator = {num_str}",
            f"denominator = {den_str}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the gravitational force.

        Args:
            data: Solution data.

        Returns:
            String representation of F with units.
        """
        return f"F = {ScientificFormatter.format_sci(data['force'])} N"


@register
class EscapeVelocityGenerator(StepGenerator):
    """Escape velocity using v = sqrt(2GM/r).

    Computes the minimum velocity needed to escape a gravitational
    field. Uses G = 6.674e-11 and scales mass and radius by
    difficulty from Earth-like to stellar-scale bodies.

    Input format:
        ``compute escape velocity``

    Target format:
        ``v = \\sqrt{\\frac{2GM}{r}} <step>
        2GM = 2(6.674 \\times 10^{-11})(5.97 \\times 10^{24}) = 7.964 \\times 10^{14}
        <step> \\frac{7.964 \\times 10^{14}}{6.371 \\times 10^{6}} = 1.25 \\times 10^{8}
        <step> v = \\sqrt{1.25 \\times 10^{8}} = 11181 m/s``

    Difficulty scaling:
        Difficulty 1-3: Earth-scale (M ~ 10^24, r ~ 10^6).
        Difficulty 4-6: gas giant scale (M ~ 10^26, r ~ 10^7).
        Difficulty 7-8: stellar scale (M ~ 10^30, r ~ 10^9).

    Prerequisites:
        gravitational_force.

    Example:
        >>> gen = EscapeVelocityGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'escape_velocity'
    """

    _G = 6.674e-11

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "escape_velocity"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["gravitational_force"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls mass and radius scales.

        Returns:
            Natural language description.
        """
        return "compute escape velocity"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate mass and radius, then compute escape velocity.

        Args:
            difficulty: Controls parameter scales.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        big_m, r = self._sample_parameters(difficulty)
        two_gm = 2 * self._G * big_m
        ratio = two_gm / r
        v_esc = math.sqrt(ratio)

        return "v = \\sqrt{\\frac{2GM}{r}}", {
            "G": self._G, "M": big_m, "r": r,
            "two_gm": two_gm, "ratio": ratio, "v_esc": v_esc,
        }

    def _sample_parameters(self, difficulty: int) -> tuple[float, float]:
        """Sample mass and radius scaled by difficulty.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (mass, radius).
        """
        if difficulty <= 3:
            big_m = float(self._rng.randint(1, 9)) * 1e24
            r = float(self._rng.randint(1, 9)) * 1e6
        elif difficulty <= 6:
            big_m = float(self._rng.randint(1, 9)) * 1e26
            r = float(self._rng.randint(1, 9)) * 1e7
        else:
            big_m = float(self._rng.randint(1, 9)) * 1e30
            r = float(self._rng.randint(1, 9)) * 1e9
        return big_m, r

    def _create_steps(self, data: dict) -> list[str]:
        """Generate computation steps for escape velocity.

        Args:
            data: Solution data with G, M, r, and intermediates.

        Returns:
            Steps showing 2GM, division by r, and square root.
        """
        g_str = ScientificFormatter.format_sci(data["G"])
        m_str = ScientificFormatter.format_sci(data["M"])
        r_str = ScientificFormatter.format_sci(data["r"])
        two_gm_str = ScientificFormatter.format_sci(data["two_gm"])
        ratio_str = ScientificFormatter.format_sci(data["ratio"])

        return [
            f"2GM = 2({g_str})({m_str}) = {two_gm_str}",
            f"\\frac{{{two_gm_str}}}{{{r_str}}} = {ratio_str}",
            f"v = \\sqrt{{{ratio_str}}}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the escape velocity.

        Args:
            data: Solution data.

        Returns:
            String representation of v_esc with units.
        """
        return f"v = {ScientificFormatter.format_value(data['v_esc'], 2)} m/s"


@register
class PendulumPeriodGenerator(StepGenerator):
    """Pendulum period using T = 2 pi sqrt(L/g).

    Computes the period of a simple pendulum given length L and
    gravitational acceleration g = 9.8 m/s^2.

    Input format:
        ``compute pendulum period``

    Target format:
        ``T = 2\\pi\\sqrt{\\frac{L}{g}} <step>
        \\frac{L}{g} = \\frac{2.5}{9.8} = 0.2551 <step>
        \\sqrt{0.2551} = 0.5051 <step>
        T = 2\\pi(0.5051) = 3.174 s``

    Difficulty scaling:
        Difficulty 1: L in [0.5, 2.0] m (short pendulums).
        Difficulty 4: L in [0.5, 5.0] m.
        Difficulty 8: L in [0.5, 50.0] m (long pendulums).

    Prerequisites:
        division, multiplication.

    Example:
        >>> gen = PendulumPeriodGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'pendulum_period'
    """

    _G = 9.8

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "pendulum_period"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["division", "multiplication"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls pendulum length range.

        Returns:
            Natural language description.
        """
        return "compute pendulum period"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate pendulum length and compute the period.

        Args:
            difficulty: Controls length range.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        max_length = 2.0 + difficulty * 6.0
        length = round(self._rng.uniform(0.5, max_length), 2)
        ratio = length / self._G
        sqrt_ratio = math.sqrt(ratio)
        period = 2 * math.pi * sqrt_ratio

        return "T = 2\\pi\\sqrt{\\frac{L}{g}}", {
            "L": length, "g": self._G,
            "ratio": round(ratio, 4),
            "sqrt_ratio": round(sqrt_ratio, 4),
            "period": round(period, 4),
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate division, square root, and multiplication steps.

        Args:
            data: Solution data with L, g, and intermediates.

        Returns:
            Steps showing L/g, sqrt, and 2*pi multiplication.
        """
        ratio = data["ratio"]
        sqrt_val = data["sqrt_ratio"]
        return [
            f"\\frac{{L}}{{g}} = \\frac{{{data['L']}}}{{{data['g']}}} = {ratio}",
            f"\\sqrt{{{ratio}}} = {sqrt_val}",
            f"T = 2\\pi({sqrt_val})",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the pendulum period.

        Args:
            data: Solution data.

        Returns:
            String representation of T with units.
        """
        return f"T = {data['period']} s"


@register
class SchwarzschildRadiusGenerator(StepGenerator):
    """Schwarzschild radius using r_s = 2GM/c^2.

    Computes the event horizon radius for a given mass using
    G = 6.674e-11 and c = 2.998e8 m/s. Primarily used for
    stellar-mass and supermassive black holes.

    Input format:
        ``compute schwarzschild radius``

    Target format:
        ``r_s = \\frac{2GM}{c^2} <step>
        2GM = 2(6.674 \\times 10^{-11})(1.989 \\times 10^{30}) = 2.655 \\times 10^{20}
        <step> c^2 = (2.998 \\times 10^{8})^2 = 8.988 \\times 10^{16}
        <step> r_s = 2954 m``

    Difficulty scaling:
        Difficulty 1-3: stellar mass (1-10 solar masses).
        Difficulty 4-6: intermediate (10-1000 solar masses).
        Difficulty 7-8: supermassive (10^6 - 10^9 solar masses).

    Prerequisites:
        gravitational_force.

    Example:
        >>> gen = SchwarzschildRadiusGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'schwarzschild_radius'
    """

    _G = 6.674e-11
    _C = 2.998e8
    _SOLAR_MASS = 1.989e30

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "schwarzschild_radius"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["gravitational_force"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls mass scale.

        Returns:
            Natural language description.
        """
        return "compute schwarzschild radius"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a mass and compute its Schwarzschild radius.

        Args:
            difficulty: Controls mass scale.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        solar_multiples = self._sample_solar_multiples(difficulty)
        mass = solar_multiples * self._SOLAR_MASS
        two_gm = 2 * self._G * mass
        c_sq = self._C ** 2
        r_s = two_gm / c_sq

        return "r_s = \\frac{2GM}{c^2}", {
            "M": mass, "solar_multiples": solar_multiples,
            "two_gm": two_gm, "c_sq": c_sq, "r_s": r_s,
        }

    def _sample_solar_multiples(self, difficulty: int) -> float:
        """Sample mass in solar mass units based on difficulty.

        Args:
            difficulty: Difficulty level.

        Returns:
            Mass as a multiple of solar mass.
        """
        if difficulty <= 3:
            return float(self._rng.randint(1, 10))
        if difficulty <= 6:
            return float(self._rng.randint(10, 1000))
        exponent = self._rng.randint(6, 9)
        mantissa = self._rng.randint(1, 9)
        return float(mantissa) * (10 ** exponent)

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Schwarzschild radius computation steps.

        Args:
            data: Solution data with mass and intermediates.

        Returns:
            Steps showing 2GM, c^2, and division.
        """
        m_str = ScientificFormatter.format_sci(data["M"])
        g_str = ScientificFormatter.format_sci(self._G)
        two_gm_str = ScientificFormatter.format_sci(data["two_gm"])
        c_str = ScientificFormatter.format_sci(self._C)
        c_sq_str = ScientificFormatter.format_sci(data["c_sq"])

        return [
            f"2GM = 2({g_str})({m_str}) = {two_gm_str}",
            f"c^2 = ({c_str})^2 = {c_sq_str}",
            f"r_s = \\frac{{{two_gm_str}}}{{{c_sq_str}}}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the Schwarzschild radius.

        Args:
            data: Solution data.

        Returns:
            String representation of r_s with units.
        """
        return f"r_s = {ScientificFormatter.format_sci(data['r_s'])} m"


@register
class OrbitalPeriodGenerator(StepGenerator):
    """Orbital period using Kepler's third law: T^2 = 4 pi^2 a^3 / (GM).

    Computes the orbital period for a body orbiting at semi-major
    axis a around mass M. Uses G = 6.674e-11.

    Input format:
        ``compute orbital period``

    Target format:
        ``T^2 = \\frac{4\\pi^2 a^3}{GM} <step>
        a^3 = (1.496 \\times 10^{11})^3 = 3.348 \\times 10^{33} <step>
        4\\pi^2 a^3 = 1.322 \\times 10^{35} <step>
        GM = 1.327 \\times 10^{20} <step>
        T^2 = 9.966 \\times 10^{14} <step> T = 3.157 \\times 10^{7} s``

    Difficulty scaling:
        Difficulty 1-3: inner solar system (a ~ 10^11 m, M = solar).
        Difficulty 4-6: outer solar system (a ~ 10^12 m).
        Difficulty 7-8: exoplanetary (variable M and a).

    Prerequisites:
        gravitational_force, exponentiation.

    Example:
        >>> gen = OrbitalPeriodGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'orbital_period'
    """

    _G = 6.674e-11
    _SOLAR_MASS = 1.989e30

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "orbital_period"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["gravitational_force", "exponentiation"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls orbital scale.

        Returns:
            Natural language description.
        """
        return "compute orbital period"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate semi-major axis and central mass, then compute period.

        Args:
            difficulty: Controls orbital parameter scales.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        big_m, a = self._sample_parameters(difficulty)
        a_cubed = a ** 3
        four_pi_sq_a3 = 4 * math.pi ** 2 * a_cubed
        gm = self._G * big_m
        t_sq = four_pi_sq_a3 / gm
        period = math.sqrt(t_sq)

        return "T^2 = \\frac{4\\pi^2 a^3}{GM}", {
            "M": big_m, "a": a, "a_cubed": a_cubed,
            "four_pi_sq_a3": four_pi_sq_a3, "gm": gm,
            "t_sq": t_sq, "period": period,
        }

    def _sample_parameters(self, difficulty: int) -> tuple[float, float]:
        """Sample central mass and semi-major axis by difficulty.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (central_mass, semi_major_axis).
        """
        if difficulty <= 3:
            big_m = self._SOLAR_MASS
            a = float(self._rng.randint(1, 5)) * 1e11
        elif difficulty <= 6:
            big_m = self._SOLAR_MASS
            a = float(self._rng.randint(1, 9)) * 1e12
        else:
            big_m = float(self._rng.randint(1, 9)) * self._SOLAR_MASS
            a = float(self._rng.randint(1, 9)) * 1e11
        return big_m, a

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Kepler's third law computation steps.

        Args:
            data: Solution data with a, M, and intermediates.

        Returns:
            Steps showing a^3, 4pi^2 a^3, GM, T^2, and T.
        """
        a_str = ScientificFormatter.format_sci(data["a"])
        a3_str = ScientificFormatter.format_sci(data["a_cubed"])
        num_str = ScientificFormatter.format_sci(data["four_pi_sq_a3"])
        gm_str = ScientificFormatter.format_sci(data["gm"])
        tsq_str = ScientificFormatter.format_sci(data["t_sq"])

        return [
            f"a^3 = ({a_str})^3 = {a3_str}",
            f"4\\pi^2 a^3 = {num_str}",
            f"GM = {gm_str}",
            f"T^2 = {tsq_str}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the orbital period.

        Args:
            data: Solution data.

        Returns:
            String representation of T with units.
        """
        return f"T = {ScientificFormatter.format_sci(data['period'])} s"


@register
class RedshiftGenerator(StepGenerator):
    """Cosmological redshift using z = (lambda_obs - lambda_emit) / lambda_emit.

    Computes the redshift of an astronomical object from observed
    and emitted wavelengths. Uses nanometre-scale wavelengths for
    optical observations.

    Input format:
        ``compute cosmological redshift``

    Target format:
        ``z = \\frac{\\lambda_{obs} - \\lambda_{emit}}{\\lambda_{emit}}
        <step> \\lambda_{obs} - \\lambda_{emit} = 700 - 500 = 200
        <step> z = \\frac{200}{500} <step> z = 0.4``

    Difficulty scaling:
        Difficulty 1-3: small redshift (z < 1), simple wavelengths.
        Difficulty 4-6: moderate redshift (z ~ 1-3).
        Difficulty 7-8: high redshift (z ~ 3-10).

    Prerequisites:
        subtraction, division.

    Example:
        >>> gen = RedshiftGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'redshift'
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "redshift"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["subtraction", "division"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls redshift magnitude.

        Returns:
            Natural language description.
        """
        return "compute cosmological redshift"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate emitted and observed wavelengths, then compute redshift.

        Args:
            difficulty: Controls redshift magnitude.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        lam_emit, lam_obs = self._sample_wavelengths(difficulty)
        delta = lam_obs - lam_emit
        z = round(delta / lam_emit, 4)

        formula = "z = \\frac{\\lambda_{obs} - \\lambda_{emit}}{\\lambda_{emit}}"
        return formula, {
            "lam_emit": lam_emit, "lam_obs": lam_obs,
            "delta": delta, "z": z,
        }

    def _sample_wavelengths(self, difficulty: int) -> tuple[int, int]:
        """Sample emitted and observed wavelengths in nm.

        Args:
            difficulty: Controls the redshift magnitude.

        Returns:
            Tuple of (emitted_wavelength, observed_wavelength).
        """
        lam_emit = self._rng.randint(300, 700)
        if difficulty <= 3:
            z_target = round(self._rng.uniform(0.1, 0.9), 1)
        elif difficulty <= 6:
            z_target = round(self._rng.uniform(1.0, 3.0), 1)
        else:
            z_target = round(self._rng.uniform(3.0, 10.0), 1)
        lam_obs = int(lam_emit * (1 + z_target))
        return lam_emit, lam_obs

    def _create_steps(self, data: dict) -> list[str]:
        """Generate subtraction and division steps.

        Args:
            data: Solution data with wavelengths and redshift.

        Returns:
            Steps showing delta lambda and division.
        """
        emit = data["lam_emit"]
        obs = data["lam_obs"]
        delta = data["delta"]
        return [
            f"\\lambda_{{obs}} - \\lambda_{{emit}} = {obs} - {emit} = {delta}",
            f"z = \\frac{{{delta}}}{{{emit}}}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the redshift value.

        Args:
            data: Solution data.

        Returns:
            String representation of z.
        """
        return f"z = {data['z']}"


@register
class StellarLuminosityGenerator(StepGenerator):
    """Stellar luminosity using L = 4 pi R^2 sigma T^4.

    Computes stellar luminosity from radius and surface temperature
    using the Stefan-Boltzmann law with sigma = 5.670e-8 W/(m^2 K^4).

    Input format:
        ``compute stellar luminosity``

    Target format:
        ``L = 4\\pi R^2 \\sigma T^4 <step>
        R^2 = (6.96 \\times 10^{8})^2 = 4.844 \\times 10^{17} <step>
        T^4 = (5778)^4 = 1.115 \\times 10^{15} <step>
        L = 4\\pi(4.844 \\times 10^{17})(5.670 \\times 10^{-8})(1.115 \\times 10^{15})
        <step> L = 3.846 \\times 10^{26} W``

    Difficulty scaling:
        Difficulty 1-3: Sun-like (R ~ 10^8, T ~ 4000-6000 K).
        Difficulty 4-6: giant stars (R ~ 10^9, T ~ 3000-8000 K).
        Difficulty 7-8: supergiants (R ~ 10^11, T ~ 3000-30000 K).

    Prerequisites:
        exponentiation, multiplication.

    Example:
        >>> gen = StellarLuminosityGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'stellar_luminosity'
    """

    _SIGMA = 5.670e-8

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "stellar_luminosity"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["exponentiation", "multiplication"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls stellar parameter scales.

        Returns:
            Natural language description.
        """
        return "compute stellar luminosity"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate stellar radius and temperature, then compute luminosity.

        Args:
            difficulty: Controls parameter scales.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        radius, temp = self._sample_parameters(difficulty)
        r_sq = radius ** 2
        t_fourth = temp ** 4
        luminosity = 4 * math.pi * r_sq * self._SIGMA * t_fourth

        return "L = 4\\pi R^2 \\sigma T^4", {
            "R": radius, "T": temp, "sigma": self._SIGMA,
            "r_sq": r_sq, "t_fourth": t_fourth,
            "luminosity": luminosity,
        }

    def _sample_parameters(self, difficulty: int) -> tuple[float, float]:
        """Sample stellar radius and surface temperature by difficulty.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (radius_m, temperature_K).
        """
        if difficulty <= 3:
            radius = float(self._rng.randint(4, 9)) * 1e8
            temp = float(self._rng.randint(4000, 6000))
        elif difficulty <= 6:
            radius = float(self._rng.randint(1, 9)) * 1e9
            temp = float(self._rng.randint(3000, 8000))
        else:
            radius = float(self._rng.randint(1, 9)) * 1e11
            temp = float(self._rng.randint(3000, 30000))
        return radius, temp

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Stefan-Boltzmann law computation steps.

        Args:
            data: Solution data with R, T, and intermediates.

        Returns:
            Steps showing R^2, T^4, and luminosity calculation.
        """
        r_str = ScientificFormatter.format_sci(data["R"])
        r_sq_str = ScientificFormatter.format_sci(data["r_sq"])
        t_str = ScientificFormatter.format_value(data["T"])
        t4_str = ScientificFormatter.format_sci(data["t_fourth"])
        sigma_str = ScientificFormatter.format_sci(data["sigma"])

        return [
            f"R^2 = ({r_str})^2 = {r_sq_str}",
            f"T^4 = ({t_str})^4 = {t4_str}",
            f"L = 4\\pi({r_sq_str})({sigma_str})({t4_str})",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the stellar luminosity.

        Args:
            data: Solution data.

        Returns:
            String representation of L with units.
        """
        return f"L = {ScientificFormatter.format_sci(data['luminosity'])} W"
