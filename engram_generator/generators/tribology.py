"""Tribology generators -- friction, wear, lubrication, and contact mechanics.

Covers friction force (static/kinetic), Archard wear equation, Sommerfeld
number with lubrication regime classification, and Hertzian contact stress.
Tiers range from 4 (introductory friction) to 5 (contact mechanics).
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


class _TriboFormatter:
    """Formats numeric values for tribology problems.

    Provides consistent rounding and clean string representations
    to keep target text compact.
    """

    @staticmethod
    def fmt(value: float, decimals: int = 4) -> str:
        """Format a numeric value, stripping unnecessary trailing zeros.

        Args:
            value: Number to format.
            decimals: Maximum decimal places.

        Returns:
            Clean string representation.
        """
        rounded = round(value, decimals)
        if rounded == int(rounded):
            return str(int(rounded))
        return str(rounded)


_f = _TriboFormatter.fmt


# ===================================================================
# 1. Friction force  (tier 4)
# ===================================================================

@register
class FrictionForceGenerator(StepGenerator):
    """Compute friction force from coefficient and normal force.

    F_f = mu * N. Distinguishes static and kinetic friction.

    Difficulty scaling:
        Difficulty 1-3: integer normal force, simple mu values.
        Difficulty 4-6: decimal mu and normal force, compare static/kinetic.
        Difficulty 7-8: inclined plane with angle, N = mg*cos(theta).

    Prerequisites:
        multiplication.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "friction_force"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["multiplication"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute friction force from coefficient and normal force"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate friction coefficient and normal force, compute F_f.

        Args:
            difficulty: Controls parameter ranges and problem variant.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            mu_s = round(self._rng.choice([0.2, 0.3, 0.4, 0.5, 0.6]), 1)
            mu_k = round(mu_s - 0.1, 1)
            normal = float(self._rng.randint(10, 100 + difficulty * 50))
            variant = "simple"
        elif difficulty <= 6:
            mu_s = round(self._rng.uniform(0.15, 0.8), 2)
            mu_k = round(mu_s * self._rng.uniform(0.6, 0.9), 2)
            normal = round(self._rng.uniform(20, 500 + difficulty * 100), 1)
            variant = "compare"
        else:
            mu_s = round(self._rng.uniform(0.2, 0.7), 3)
            mu_k = round(mu_s * self._rng.uniform(0.6, 0.85), 3)
            mass = round(self._rng.uniform(5.0, 50.0), 1)
            angle_deg = self._rng.randint(10, 40)
            angle_rad = math.radians(angle_deg)
            normal = round(mass * 9.81 * math.cos(angle_rad), 4)
            variant = "incline"

        f_static = round(mu_s * normal, 4)
        f_kinetic = round(mu_k * normal, 4)

        data = {
            "mu_s": mu_s, "mu_k": mu_k, "N": normal,
            "F_static": f_static, "F_kinetic": f_kinetic,
            "variant": variant,
        }
        if variant == "incline":
            data["mass"] = mass
            data["angle_deg"] = angle_deg

        return "F_f = \\mu N", data

    def _create_steps(self, data: dict) -> list[str]:
        """Generate computation steps for friction force.

        Args:
            data: Solution data from _create_problem.

        Returns:
            List of step strings.
        """
        steps = []
        if data["variant"] == "incline":
            steps.append(
                f"m={_f(data['mass'])}kg, theta={data['angle_deg']}deg, "
                f"N = mg*cos(theta) = {_f(data['N'])} N"
            )
        else:
            steps.append(f"N = {_f(data['N'])} N")

        steps.append(
            f"mu_s={_f(data['mu_s'])}, mu_k={_f(data['mu_k'])}"
        )
        steps.append(
            f"F_static = {_f(data['mu_s'])}*{_f(data['N'])} "
            f"= {_f(data['F_static'])} N"
        )
        steps.append(
            f"F_kinetic = {_f(data['mu_k'])}*{_f(data['N'])} "
            f"= {_f(data['F_kinetic'])} N"
        )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return static and kinetic friction forces.

        Args:
            data: Solution data.

        Returns:
            Friction forces as a string.
        """
        return (f"F_static = {_f(data['F_static'])} N, "
                f"F_kinetic = {_f(data['F_kinetic'])} N")


# ===================================================================
# 2. Wear rate (Archard equation)  (tier 5)
# ===================================================================

@register
class WearRateGenerator(StepGenerator):
    """Compute wear volume using the Archard equation.

    V = K * F * s / H where K = dimensionless wear coefficient,
    F = applied force, s = sliding distance, H = hardness.

    Difficulty scaling:
        Difficulty 1-3: integer values, small ranges.
        Difficulty 4-6: decimal coefficients, larger ranges.
        Difficulty 7-8: compute specific wear rate k = K/H.

    Prerequisites:
        multiplication.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "wear_rate"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["multiplication"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute wear volume using the Archard equation"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate wear parameters and compute worn volume.

        Args:
            difficulty: Controls parameter ranges and extra computations.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            k_wear = round(self._rng.uniform(1e-4, 1e-3), 4)
            force = float(self._rng.randint(10, 100 + difficulty * 30))
            distance = float(self._rng.randint(100, 1000 + difficulty * 200))
            hardness = float(self._rng.randint(100, 500))
        elif difficulty <= 6:
            k_wear = round(self._rng.uniform(1e-5, 1e-3), 5)
            force = round(self._rng.uniform(10, 500 + difficulty * 100), 1)
            distance = round(self._rng.uniform(100, 5000), 1)
            hardness = round(self._rng.uniform(50, 1000), 1)
        else:
            k_wear = round(self._rng.uniform(1e-6, 1e-4), 6)
            force = round(self._rng.uniform(50, 2000), 1)
            distance = round(self._rng.uniform(500, 10000), 1)
            hardness = round(self._rng.uniform(100, 2000), 1)

        volume = round(k_wear * force * distance / hardness, 4)
        specific_k = round(k_wear / hardness, 4)
        compute_specific = difficulty >= 7

        return "V = \\frac{K F s}{H}", {
            "K": k_wear, "F": force, "s": distance, "H": hardness,
            "V": volume, "k_specific": specific_k,
            "compute_specific": compute_specific,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate computation steps for wear volume.

        Args:
            data: Solution data from _create_problem.

        Returns:
            List of step strings.
        """
        steps = [
            f"K={_f(data['K'])}, F={_f(data['F'])}N, "
            f"s={_f(data['s'])}m, H={_f(data['H'])}Pa",
            f"V = {_f(data['K'])}*{_f(data['F'])}*"
            f"{_f(data['s'])}/{_f(data['H'])}",
            f"V = {_f(data['V'])} m^3",
        ]
        if data["compute_specific"]:
            steps.append(
                f"k_specific = K/H = {_f(data['K'])}/{_f(data['H'])} "
                f"= {_f(data['k_specific'])}"
            )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the wear volume.

        Args:
            data: Solution data.

        Returns:
            Wear volume as a string.
        """
        if data["compute_specific"]:
            return (f"V = {_f(data['V'])} m^3, "
                    f"k = {_f(data['k_specific'])} m^3/(N*m)")
        return f"V = {_f(data['V'])} m^3"


# ===================================================================
# 3. Lubrication regime (Sommerfeld number)  (tier 5)
# ===================================================================

@register
class LubricationRegimeGenerator(StepGenerator):
    """Compute Sommerfeld number and classify lubrication regime.

    S = (mu*N_speed*D / P) * (D/c)^2 where mu = dynamic viscosity,
    N_speed = rotational speed, D = journal diameter, P = bearing pressure,
    c = radial clearance.

    Classification: S < 0.01 boundary, 0.01 <= S < 1.0 mixed,
    S >= 1.0 hydrodynamic.

    Difficulty scaling:
        Difficulty 1-3: simple values, clear regime.
        Difficulty 4-6: borderline cases, decimal parameters.
        Difficulty 7-8: very small clearances, large S values.

    Prerequisites:
        division.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "lubrication_regime"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["division"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute Sommerfeld number and classify lubrication regime"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate bearing parameters and compute Sommerfeld number.

        Args:
            difficulty: Controls parameter ranges and clearance values.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            mu_visc = round(self._rng.uniform(0.01, 0.1), 3)
            n_speed = float(self._rng.randint(5, 30))
            d_journal = round(self._rng.uniform(0.05, 0.2), 3)
            pressure = float(self._rng.randint(100, 1000))
            clearance = round(self._rng.uniform(0.001, 0.01), 4)
        elif difficulty <= 6:
            mu_visc = round(self._rng.uniform(0.005, 0.2), 4)
            n_speed = round(self._rng.uniform(5, 100), 1)
            d_journal = round(self._rng.uniform(0.02, 0.3), 3)
            pressure = round(self._rng.uniform(50, 5000), 1)
            clearance = round(self._rng.uniform(0.0005, 0.005), 4)
        else:
            mu_visc = round(self._rng.uniform(0.01, 0.5), 4)
            n_speed = round(self._rng.uniform(10, 200), 1)
            d_journal = round(self._rng.uniform(0.05, 0.5), 3)
            pressure = round(self._rng.uniform(100, 10000), 1)
            clearance = round(self._rng.uniform(0.0001, 0.002), 5)

        s_val = mu_visc * n_speed * d_journal / pressure * (d_journal / clearance) ** 2
        s_val = round(s_val, 4)

        if s_val < 0.01:
            regime = "boundary"
        elif s_val < 1.0:
            regime = "mixed"
        else:
            regime = "hydrodynamic"

        return ("S = \\frac{\\mu N D}{P}"
                "\\left(\\frac{D}{c}\\right)^2"), {
            "mu": mu_visc, "N_speed": n_speed,
            "D": d_journal, "P": pressure, "c": clearance,
            "D_over_c": round(d_journal / clearance, 4),
            "S": s_val, "regime": regime,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate computation and classification steps.

        Args:
            data: Solution data from _create_problem.

        Returns:
            List of step strings.
        """
        return [
            f"mu={_f(data['mu'])}Pa*s, N={_f(data['N_speed'])}rev/s, "
            f"D={_f(data['D'])}m, P={_f(data['P'])}Pa",
            f"c={_f(data['c'])}m, D/c = {_f(data['D_over_c'])}",
            f"S = ({_f(data['mu'])}*{_f(data['N_speed'])}*"
            f"{_f(data['D'])}/{_f(data['P'])})*"
            f"{_f(data['D_over_c'])}^2 = {_f(data['S'])}",
            f"regime: {data['regime']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return Sommerfeld number and regime classification.

        Args:
            data: Solution data.

        Returns:
            Sommerfeld number and regime as a string.
        """
        return f"S = {_f(data['S'])}, regime = {data['regime']}"


# ===================================================================
# 4. Hertzian contact  (tier 5)
# ===================================================================

@register
class HertzContactGenerator(StepGenerator):
    """Compute Hertzian contact radius and maximum pressure.

    Contact radius a = (3*F*R / (4*E*))^(1/3).
    Maximum pressure p_0 = 3*F / (2*pi*a^2).
    E* is the combined elastic modulus.

    Difficulty scaling:
        Difficulty 1-3: integer force, simple radii.
        Difficulty 4-6: decimal values, compute E* from two materials.
        Difficulty 7-8: also compute contact area and mean pressure.

    Prerequisites:
        multiplication.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "hertz_contact"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["multiplication"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute Hertzian contact radius and maximum pressure"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate force, radius, modulus and compute contact parameters.

        Args:
            difficulty: Controls parameter ranges and extra outputs.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            force = float(self._rng.randint(10, 100 + difficulty * 50))
            radius = round(self._rng.uniform(0.005, 0.05), 3)
            e_star = float(self._rng.randint(50, 300)) * 1e9
        elif difficulty <= 6:
            force = round(self._rng.uniform(10, 500 + difficulty * 100), 1)
            radius = round(self._rng.uniform(0.001, 0.1), 4)
            e1 = round(self._rng.uniform(50, 400), 1) * 1e9
            nu1 = round(self._rng.uniform(0.2, 0.4), 2)
            e2 = round(self._rng.uniform(50, 400), 1) * 1e9
            nu2 = round(self._rng.uniform(0.2, 0.4), 2)
            e_star = round(1.0 / ((1 - nu1 ** 2) / e1 + (1 - nu2 ** 2) / e2), 4)
        else:
            force = round(self._rng.uniform(50, 2000), 1)
            radius = round(self._rng.uniform(0.0005, 0.05), 4)
            e1 = round(self._rng.uniform(70, 500), 1) * 1e9
            nu1 = round(self._rng.uniform(0.15, 0.45), 3)
            e2 = round(self._rng.uniform(70, 500), 1) * 1e9
            nu2 = round(self._rng.uniform(0.15, 0.45), 3)
            e_star = round(1.0 / ((1 - nu1 ** 2) / e1 + (1 - nu2 ** 2) / e2), 4)

        a = (3.0 * force * radius / (4.0 * e_star)) ** (1.0 / 3.0)
        a = round(a, 4)

        p_0 = round(3.0 * force / (2.0 * math.pi * a ** 2), 4) if a > 0 else 0.0
        contact_area = round(math.pi * a ** 2, 4)
        p_mean = round(force / contact_area, 4) if contact_area > 0 else 0.0
        compute_extra = difficulty >= 7

        return ("a = \\left(\\frac{3FR}{4E^*}\\right)^{1/3}, "
                "p_0 = \\frac{3F}{2\\pi a^2}"), {
            "F": force, "R": radius, "E_star": e_star,
            "a": a, "p_0": p_0,
            "contact_area": contact_area, "p_mean": p_mean,
            "compute_extra": compute_extra,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate contact mechanics computation steps.

        Args:
            data: Solution data from _create_problem.

        Returns:
            List of step strings.
        """
        steps = [
            f"F={_f(data['F'])}N, R={_f(data['R'])}m, "
            f"E*={_f(data['E_star'])}Pa",
            f"a = (3*{_f(data['F'])}*{_f(data['R'])}/"
            f"(4*{_f(data['E_star'])}))^(1/3) = {_f(data['a'])}m",
            f"p_0 = 3*{_f(data['F'])}/(2*pi*{_f(data['a'])}^2) "
            f"= {_f(data['p_0'])} Pa",
        ]
        if data["compute_extra"]:
            steps.append(
                f"A_contact = pi*a^2 = {_f(data['contact_area'])} m^2, "
                f"p_mean = {_f(data['p_mean'])} Pa"
            )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return contact radius and maximum pressure.

        Args:
            data: Solution data.

        Returns:
            Contact parameters as a string.
        """
        ans = f"a = {_f(data['a'])} m, p_0 = {_f(data['p_0'])} Pa"
        if data["compute_extra"]:
            ans += f", p_mean = {_f(data['p_mean'])} Pa"
        return ans
