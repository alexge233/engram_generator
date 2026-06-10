"""Classical mechanics extension generators -- projectile to two-body.

Deepens the existing classical mechanics domain with projectile motion,
circular motion, elastic/inelastic collisions, spring oscillation,
torque, moment of inertia, angular momentum conservation, damped
oscillations, and the two-body problem. Tiers range from 4 to 6.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register
from engram_generator.generators.physics import ScientificFormatter

_fmt = ScientificFormatter.format_sci
_fval = ScientificFormatter.format_value

_G_GRAVITY = 9.8  # gravitational acceleration (m/s^2)
_G_NEWTON = 6.674e-11  # gravitational constant (N m^2/kg^2)


# ===================================================================
# 1. Projectile motion (tier 4)
# ===================================================================

@register
class ProjectileMotionGenerator(StepGenerator):
    """Compute projectile range, max height, and time of flight.

    Uses x = v0*cos(theta)*t, y = v0*sin(theta)*t - g*t^2/2.
    Range R = v0^2*sin(2*theta)/g, max height H = v0^2*sin^2(theta)/(2g),
    time of flight T = 2*v0*sin(theta)/g.

    Difficulty scaling:
        Difficulty 1-3: v0 in [5,30] m/s, theta in {30,45,60}.
        Difficulty 4-6: v0 in [10,60] m/s, theta in {15,30,45,60,75}.
        Difficulty 7-8: v0 in [20,100] m/s, arbitrary angles.

    Prerequisites:
        sin_cos_eval.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "projectile_motion"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["sin_cos_eval"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute projectile range, max height, and time of flight"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate projectile parameters and compute trajectory quantities.

        Args:
            difficulty: Controls parameter ranges.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            v0 = self._rng.randint(5, 30)
            theta_deg = self._rng.choice([30, 45, 60])
        elif difficulty <= 6:
            v0 = self._rng.randint(10, 60)
            theta_deg = self._rng.choice([15, 30, 45, 60, 75])
        else:
            v0 = self._rng.randint(20, 100)
            theta_deg = self._rng.randint(10, 80)

        theta_rad = math.radians(theta_deg)
        sin_t = math.sin(theta_rad)
        cos_t = math.cos(theta_rad)
        sin_2t = math.sin(2 * theta_rad)

        t_flight = round(2 * v0 * sin_t / _G_GRAVITY, 4)
        max_height = round(v0 ** 2 * sin_t ** 2 / (2 * _G_GRAVITY), 4)
        range_val = round(v0 ** 2 * sin_2t / _G_GRAVITY, 4)

        return "R = v_0^2 \\sin(2\\theta)/g", {
            "v0": v0, "theta_deg": theta_deg,
            "sin_t": round(sin_t, 4), "cos_t": round(cos_t, 4),
            "sin_2t": round(sin_2t, 4),
            "t_flight": t_flight, "max_height": max_height,
            "range": range_val,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate projectile computation steps.

        Args:
            data: Solution data with v0, theta, and results.

        Returns:
            List of step strings.
        """
        return [
            f"v_0={data['v0']}m/s, theta={data['theta_deg']}deg",
            f"sin({data['theta_deg']})={_fval(data['sin_t'])}, "
            f"cos({data['theta_deg']})={_fval(data['cos_t'])}",
            f"T = 2*{data['v0']}*{_fval(data['sin_t'])}/{_G_GRAVITY}"
            f" = {_fval(data['t_flight'])} s",
            f"H = {data['v0']}^2*{_fval(data['sin_t'])}^2"
            f"/(2*{_G_GRAVITY}) = {_fval(data['max_height'])} m",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the projectile results.

        Args:
            data: Solution data.

        Returns:
            Range, max height, and time of flight.
        """
        return (
            f"R={_fval(data['range'])}m, "
            f"H={_fval(data['max_height'])}m, "
            f"T={_fval(data['t_flight'])}s"
        )


# ===================================================================
# 2. Circular motion (tier 4)
# ===================================================================

@register
class CircularMotionGenerator(StepGenerator):
    """Compute centripetal acceleration and period for circular motion.

    a_c = v^2/r = omega^2*r. Period T = 2*pi/omega.

    Difficulty scaling:
        Difficulty 1-3: v in [2,20], r in [1,10].
        Difficulty 4-6: v in [5,50], r in [1,30].
        Difficulty 7-8: v in [10,100], r in [1,50].

    Prerequisites:
        division.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "circular_motion"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

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
        return "compute centripetal acceleration and period"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate circular motion parameters and compute results.

        Args:
            difficulty: Controls parameter ranges.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            v = self._rng.randint(2, 20)
            r = self._rng.randint(1, 10)
        elif difficulty <= 6:
            v = self._rng.randint(5, 50)
            r = self._rng.randint(1, 30)
        else:
            v = self._rng.randint(10, 100)
            r = self._rng.randint(1, 50)

        a_c = round(v ** 2 / r, 4)
        omega = round(v / r, 4)
        period = round(2 * math.pi / omega, 4)

        return "a_c = v^2/r", {
            "v": v, "r": r, "a_c": a_c,
            "omega": omega, "period": period,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate circular motion computation steps.

        Args:
            data: Solution data with v, r, a_c, omega, period.

        Returns:
            List of step strings.
        """
        return [
            f"v={data['v']}m/s, r={data['r']}m",
            f"a_c = {data['v']}^2/{data['r']} = {_fval(data['a_c'])} m/s^2",
            f"omega = v/r = {_fval(data['omega'])} rad/s",
            f"T = 2pi/omega = {_fval(data['period'])} s",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return centripetal acceleration and period.

        Args:
            data: Solution data.

        Returns:
            a_c and T as a string.
        """
        return (
            f"a_c={_fval(data['a_c'])}m/s^2, "
            f"T={_fval(data['period'])}s"
        )


# ===================================================================
# 3. Elastic collision (tier 5)
# ===================================================================

@register
class ElasticCollisionGenerator(StepGenerator):
    """Compute final velocities in a 1D elastic collision.

    v1' = (m1-m2)/(m1+m2)*v1 + 2*m2/(m1+m2)*v2.
    v2' = 2*m1/(m1+m2)*v1 + (m2-m1)/(m1+m2)*v2.

    Difficulty scaling:
        Difficulty 1-3: masses in [1,10], velocities in [1,10].
        Difficulty 4-6: masses in [1,20], velocities in [-10,20].
        Difficulty 7-8: masses in [1,50], velocities in [-20,40].

    Prerequisites:
        momentum.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "elastic_collision"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["momentum"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute final velocities in 1D elastic collision"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate elastic collision parameters and compute final velocities.

        Args:
            difficulty: Controls parameter ranges.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            m1 = self._rng.randint(1, 10)
            m2 = self._rng.randint(1, 10)
            v1 = self._rng.randint(1, 10)
            v2 = self._rng.randint(0, 5)
        elif difficulty <= 6:
            m1 = self._rng.randint(1, 20)
            m2 = self._rng.randint(1, 20)
            v1 = self._rng.randint(-10, 20)
            v2 = self._rng.randint(-10, 20)
        else:
            m1 = self._rng.randint(1, 50)
            m2 = self._rng.randint(1, 50)
            v1 = self._rng.randint(-20, 40)
            v2 = self._rng.randint(-20, 40)

        m_total = m1 + m2
        v1f = round(((m1 - m2) / m_total) * v1 + (2 * m2 / m_total) * v2, 4)
        v2f = round((2 * m1 / m_total) * v1 + ((m2 - m1) / m_total) * v2, 4)

        return "v_1' = \\frac{m_1-m_2}{m_1+m_2}v_1 + \\frac{2m_2}{m_1+m_2}v_2", {
            "m1": m1, "m2": m2, "v1": v1, "v2": v2,
            "m_total": m_total, "v1f": v1f, "v2f": v2f,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate elastic collision computation steps.

        Args:
            data: Solution data with masses and velocities.

        Returns:
            List of step strings.
        """
        m1, m2 = data["m1"], data["m2"]
        v1, v2 = data["v1"], data["v2"]
        mt = data["m_total"]
        return [
            f"m1={m1}kg, m2={m2}kg, v1={v1}m/s, v2={v2}m/s",
            f"m1+m2={mt}",
            f"v1' = ({m1}-{m2})/{mt}*{v1} + 2*{m2}/{mt}*{v2}",
            f"v1' = {_fval(data['v1f'])} m/s",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the final velocities.

        Args:
            data: Solution data.

        Returns:
            v1' and v2' as a string.
        """
        return (
            f"v1'={_fval(data['v1f'])}m/s, "
            f"v2'={_fval(data['v2f'])}m/s"
        )


# ===================================================================
# 4. Inelastic collision (tier 4)
# ===================================================================

@register
class InelasticCollisionGenerator(StepGenerator):
    """Compute final velocity and energy lost in perfectly inelastic collision.

    m1*v1 + m2*v2 = (m1+m2)*v_f. Energy lost = KE_i - KE_f.

    Difficulty scaling:
        Difficulty 1-3: masses in [1,10], velocities in [1,10].
        Difficulty 4-6: masses in [1,30], velocities in [-10,20].
        Difficulty 7-8: masses in [1,50], velocities in [-20,40].

    Prerequisites:
        momentum.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "inelastic_collision"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["momentum"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute final velocity and energy lost in inelastic collision"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate inelastic collision parameters and compute results.

        Args:
            difficulty: Controls parameter ranges.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            m1 = self._rng.randint(1, 10)
            m2 = self._rng.randint(1, 10)
            v1 = self._rng.randint(1, 10)
            v2 = self._rng.randint(0, 5)
        elif difficulty <= 6:
            m1 = self._rng.randint(1, 30)
            m2 = self._rng.randint(1, 30)
            v1 = self._rng.randint(-10, 20)
            v2 = self._rng.randint(-10, 20)
        else:
            m1 = self._rng.randint(1, 50)
            m2 = self._rng.randint(1, 50)
            v1 = self._rng.randint(-20, 40)
            v2 = self._rng.randint(-20, 40)

        m_total = m1 + m2
        p_total = m1 * v1 + m2 * v2
        v_f = round(p_total / m_total, 4)
        ke_i = round(0.5 * m1 * v1 ** 2 + 0.5 * m2 * v2 ** 2, 4)
        ke_f = round(0.5 * m_total * v_f ** 2, 4)
        energy_lost = round(ke_i - ke_f, 4)

        return "m_1 v_1 + m_2 v_2 = (m_1+m_2)v_f", {
            "m1": m1, "m2": m2, "v1": v1, "v2": v2,
            "m_total": m_total, "p_total": p_total,
            "v_f": v_f, "ke_i": ke_i, "ke_f": ke_f,
            "energy_lost": energy_lost,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate inelastic collision computation steps.

        Args:
            data: Solution data with masses, velocities, and energies.

        Returns:
            List of step strings.
        """
        return [
            f"m1={data['m1']}kg, m2={data['m2']}kg, "
            f"v1={data['v1']}m/s, v2={data['v2']}m/s",
            f"p = {data['m1']}*{data['v1']}+{data['m2']}*{data['v2']}"
            f" = {data['p_total']}",
            f"v_f = {data['p_total']}/{data['m_total']}"
            f" = {_fval(data['v_f'])} m/s",
            f"KE_i={_fval(data['ke_i'])}J, KE_f={_fval(data['ke_f'])}J",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the final velocity and energy lost.

        Args:
            data: Solution data.

        Returns:
            v_f and energy lost as a string.
        """
        return (
            f"v_f={_fval(data['v_f'])}m/s, "
            f"dE={_fval(data['energy_lost'])}J"
        )


# ===================================================================
# 5. Spring oscillation (tier 4)
# ===================================================================

@register
class SpringOscillationGenerator(StepGenerator):
    """Compute spring oscillation parameters.

    x(t) = A*cos(omega*t + phi), omega = sqrt(k/m), T = 2*pi/omega.

    Difficulty scaling:
        Difficulty 1-3: k in [10,100] N/m, m in [0.1,5] kg.
        Difficulty 4-6: k in [10,500] N/m, m in [0.1,10] kg.
        Difficulty 7-8: k in [10,1000] N/m, m in [0.1,20] kg.

    Prerequisites:
        exponentiation.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "spring_oscillation"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["exponentiation"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute spring oscillation frequency and period"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate spring parameters and compute oscillation quantities.

        Args:
            difficulty: Controls parameter ranges.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            k = self._rng.randint(10, 100)
            m = round(self._rng.uniform(0.1, 5.0), 1)
        elif difficulty <= 6:
            k = self._rng.randint(10, 500)
            m = round(self._rng.uniform(0.1, 10.0), 1)
        else:
            k = self._rng.randint(10, 1000)
            m = round(self._rng.uniform(0.1, 20.0), 1)

        omega = round(math.sqrt(k / m), 4)
        period = round(2 * math.pi / omega, 4)
        freq = round(1.0 / period, 4)

        return "\\omega = \\sqrt{k/m}, T = 2\\pi/\\omega", {
            "k": k, "m": m, "omega": omega,
            "period": period, "freq": freq,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate spring oscillation computation steps.

        Args:
            data: Solution data with k, m, omega, period, freq.

        Returns:
            List of step strings.
        """
        return [
            f"k={data['k']}N/m, m={data['m']}kg",
            f"omega = sqrt({data['k']}/{data['m']})"
            f" = {_fval(data['omega'])} rad/s",
            f"T = 2pi/{_fval(data['omega'])}"
            f" = {_fval(data['period'])} s",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return oscillation angular frequency and period.

        Args:
            data: Solution data.

        Returns:
            omega, T, and f as a string.
        """
        return (
            f"omega={_fval(data['omega'])}rad/s, "
            f"T={_fval(data['period'])}s"
        )


# ===================================================================
# 6. Torque and rotation (tier 5)
# ===================================================================

@register
class TorqueRotationGenerator(StepGenerator):
    """Compute angular acceleration from torque and moment of inertia.

    tau = r*F*sin(theta) = I*alpha. Given I and tau, compute alpha.

    Difficulty scaling:
        Difficulty 1-3: r in [0.1,1], F in [5,50], theta=90.
        Difficulty 4-6: r in [0.1,2], F in [5,100], theta in {30,45,60,90}.
        Difficulty 7-8: r in [0.1,3], F in [10,200], arbitrary theta.

    Prerequisites:
        multiplication.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "torque_rotation"

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
        return "compute torque and angular acceleration"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate torque parameters and compute angular acceleration.

        Args:
            difficulty: Controls parameter ranges.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            r = round(self._rng.uniform(0.1, 1.0), 2)
            f_val = self._rng.randint(5, 50)
            theta_deg = 90
        elif difficulty <= 6:
            r = round(self._rng.uniform(0.1, 2.0), 2)
            f_val = self._rng.randint(5, 100)
            theta_deg = self._rng.choice([30, 45, 60, 90])
        else:
            r = round(self._rng.uniform(0.1, 3.0), 2)
            f_val = self._rng.randint(10, 200)
            theta_deg = self._rng.randint(10, 90)

        sin_theta = round(math.sin(math.radians(theta_deg)), 4)
        tau = round(r * f_val * sin_theta, 4)
        inertia = round(self._rng.uniform(0.5, 10.0 + difficulty * 2), 2)
        alpha = round(tau / inertia, 4)

        return "\\tau = rF\\sin\\theta = I\\alpha", {
            "r": r, "F": f_val, "theta_deg": theta_deg,
            "sin_theta": sin_theta, "tau": tau,
            "I": inertia, "alpha": alpha,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate torque computation steps.

        Args:
            data: Solution data with r, F, theta, I, alpha.

        Returns:
            List of step strings.
        """
        return [
            f"r={data['r']}m, F={data['F']}N, "
            f"theta={data['theta_deg']}deg",
            f"tau = {data['r']}*{data['F']}*{_fval(data['sin_theta'])}"
            f" = {_fval(data['tau'])} Nm",
            f"I={data['I']}kg*m^2",
            f"alpha = tau/I = {_fval(data['tau'])}/{data['I']}"
            f" = {_fval(data['alpha'])} rad/s^2",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the torque and angular acceleration.

        Args:
            data: Solution data.

        Returns:
            tau and alpha as a string.
        """
        return (
            f"tau={_fval(data['tau'])}Nm, "
            f"alpha={_fval(data['alpha'])}rad/s^2"
        )


# ===================================================================
# 7. Moment of inertia (tier 5)
# ===================================================================

@register
class MomentOfInertiaPhysicsGenerator(StepGenerator):
    """Compute moment of inertia for standard shapes with parallel axis.

    Rod: I = ML^2/12, Disk: I = MR^2/2, Sphere: I = 2MR^2/5.
    Parallel axis: I = I_cm + Md^2.

    Difficulty scaling:
        Difficulty 1-3: single shape, compute I_cm only.
        Difficulty 4-6: single shape with parallel axis.
        Difficulty 7-8: larger masses and offsets.

    Prerequisites:
        multiplication.
    """

    _SHAPES = ["rod", "disk", "sphere"]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "moment_of_inertia_physics"

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
        return "compute moment of inertia for a rigid body"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate moment of inertia parameters.

        Args:
            difficulty: Controls shape and parallel axis usage.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        shape = self._rng.choice(self._SHAPES)
        mass = round(self._rng.uniform(1.0, 5.0 + difficulty * 2), 2)

        if shape == "rod":
            length = round(self._rng.uniform(0.5, 2.0 + difficulty * 0.5), 2)
            i_cm = round(mass * length ** 2 / 12, 4)
            dim_label = f"L={length}m"
            formula = "I_{{cm}} = ML^2/12"
        elif shape == "disk":
            radius = round(self._rng.uniform(0.1, 1.0 + difficulty * 0.3), 2)
            i_cm = round(mass * radius ** 2 / 2, 4)
            dim_label = f"R={radius}m"
            formula = "I_{{cm}} = MR^2/2"
        else:
            radius = round(self._rng.uniform(0.1, 1.0 + difficulty * 0.3), 2)
            i_cm = round(2 * mass * radius ** 2 / 5, 4)
            dim_label = f"R={radius}m"
            formula = "I_{{cm}} = 2MR^2/5"

        use_parallel = difficulty >= 4
        if use_parallel:
            d = round(self._rng.uniform(0.1, 1.0 + difficulty * 0.2), 2)
            i_total = round(i_cm + mass * d ** 2, 4)
        else:
            d = 0.0
            i_total = i_cm

        return formula, {
            "shape": shape, "M": mass, "dim_label": dim_label,
            "I_cm": i_cm, "d": d, "I_total": i_total,
            "parallel": use_parallel,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate moment of inertia computation steps.

        Args:
            data: Solution data with shape, mass, I_cm, and d.

        Returns:
            List of step strings.
        """
        steps = [
            f"{data['shape']}: M={data['M']}kg, {data['dim_label']}",
            f"I_cm = {_fval(data['I_cm'])} kg*m^2",
        ]
        if data["parallel"]:
            steps.append(
                f"I = I_cm + Md^2 = {_fval(data['I_cm'])} + "
                f"{data['M']}*{data['d']}^2"
            )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the moment of inertia.

        Args:
            data: Solution data.

        Returns:
            I as a string with units.
        """
        return f"I = {_fval(data['I_total'])} kg*m^2"


# ===================================================================
# 8. Angular momentum conservation (tier 5)
# ===================================================================

@register
class AngularMomentumConservationGenerator(StepGenerator):
    """Compute new angular velocity via conservation of angular momentum.

    L = I*omega = const. I1*omega1 = I2*omega2.
    Ice skater problem: reducing I increases omega.

    Difficulty scaling:
        Difficulty 1-3: I1 in [2,10], omega1 in [1,5], I2 in [1,I1-1].
        Difficulty 4-6: I1 in [5,50], omega1 in [1,10], I2 in [1,I1-1].
        Difficulty 7-8: I1 in [10,100], omega1 in [1,20], I2 in [1,I1-1].

    Prerequisites:
        division.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "angular_momentum_conservation"

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
        return "apply conservation of angular momentum"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate angular momentum conservation parameters.

        Args:
            difficulty: Controls parameter ranges.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            i1 = self._rng.randint(2, 10)
            omega1 = self._rng.randint(1, 5)
            i2 = self._rng.randint(1, max(1, i1 - 1))
        elif difficulty <= 6:
            i1 = self._rng.randint(5, 50)
            omega1 = self._rng.randint(1, 10)
            i2 = self._rng.randint(1, max(1, i1 - 1))
        else:
            i1 = self._rng.randint(10, 100)
            omega1 = self._rng.randint(1, 20)
            i2 = self._rng.randint(1, max(1, i1 - 1))

        l_val = round(i1 * omega1, 4)
        omega2 = round(l_val / i2, 4)

        return "I_1\\omega_1 = I_2\\omega_2", {
            "I1": i1, "omega1": omega1,
            "I2": i2, "L": l_val, "omega2": omega2,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate angular momentum conservation steps.

        Args:
            data: Solution data with I1, omega1, I2, omega2.

        Returns:
            List of step strings.
        """
        return [
            f"I1={data['I1']}kg*m^2, omega1={data['omega1']}rad/s",
            f"L = I1*omega1 = {_fval(data['L'])} kg*m^2/s",
            f"I2={data['I2']}kg*m^2",
            f"omega2 = L/I2 = {_fval(data['L'])}/{data['I2']}"
            f" = {_fval(data['omega2'])} rad/s",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the new angular velocity.

        Args:
            data: Solution data.

        Returns:
            omega2 as a string.
        """
        return f"omega2 = {_fval(data['omega2'])} rad/s"


# ===================================================================
# 9. Damped oscillation (tier 5)
# ===================================================================

@register
class DampedOscillationGenerator(StepGenerator):
    """Classify and compute damped oscillation parameters.

    x(t) = A*e^(-gamma*t)*cos(omega_d*t).
    omega_d = sqrt(omega_0^2 - gamma^2).
    Under-damped: gamma < omega_0.
    Critically damped: gamma = omega_0.
    Over-damped: gamma > omega_0.

    Difficulty scaling:
        Difficulty 1-3: always under-damped, omega_0 in [5,20].
        Difficulty 4-6: random regime, omega_0 in [5,30].
        Difficulty 7-8: all regimes, larger parameters.

    Prerequisites:
        exponentiation.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "damped_oscillation"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["exponentiation"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "classify and compute damped oscillation parameters"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate damped oscillation parameters and classify the regime.

        Args:
            difficulty: Controls parameter ranges and regime selection.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            omega_0 = round(self._rng.uniform(5.0, 20.0), 2)
            gamma = round(self._rng.uniform(0.5, omega_0 * 0.8), 2)
        elif difficulty <= 6:
            omega_0 = round(self._rng.uniform(5.0, 30.0), 2)
            regime = self._rng.choice(["under", "critical", "over"])
            gamma = self._select_gamma(omega_0, regime)
        else:
            omega_0 = round(self._rng.uniform(5.0, 50.0), 2)
            regime = self._rng.choice(["under", "critical", "over"])
            gamma = self._select_gamma(omega_0, regime)

        if abs(gamma - omega_0) < 0.01:
            classification = "critically damped"
            omega_d = 0.0
        elif gamma < omega_0:
            classification = "under-damped"
            omega_d = round(math.sqrt(omega_0 ** 2 - gamma ** 2), 4)
        else:
            classification = "over-damped"
            omega_d = 0.0

        return "\\omega_d = \\sqrt{\\omega_0^2 - \\gamma^2}", {
            "omega_0": omega_0, "gamma": gamma,
            "omega_d": omega_d, "classification": classification,
        }

    def _select_gamma(self, omega_0: float, regime: str) -> float:
        """Select gamma to achieve the desired damping regime.

        Args:
            omega_0: Natural frequency.
            regime: One of 'under', 'critical', 'over'.

        Returns:
            Damping coefficient gamma.
        """
        if regime == "critical":
            return omega_0
        if regime == "under":
            return round(self._rng.uniform(0.5, omega_0 * 0.8), 2)
        return round(self._rng.uniform(omega_0 * 1.2, omega_0 * 2.0), 2)

    def _create_steps(self, data: dict) -> list[str]:
        """Generate damped oscillation computation steps.

        Args:
            data: Solution data with omega_0, gamma, and classification.

        Returns:
            List of step strings.
        """
        steps = [
            f"omega_0={_fval(data['omega_0'])} rad/s, "
            f"gamma={_fval(data['gamma'])} s^-1",
            f"omega_0^2 - gamma^2 = "
            f"{round(data['omega_0'] ** 2 - data['gamma'] ** 2, 4)}",
        ]
        if data["omega_d"] > 0:
            steps.append(f"omega_d = {_fval(data['omega_d'])} rad/s")
        steps.append(f"regime: {data['classification']}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the classification and damped frequency.

        Args:
            data: Solution data.

        Returns:
            Classification and omega_d as a string.
        """
        if data["omega_d"] > 0:
            return (
                f"{data['classification']}, "
                f"omega_d={_fval(data['omega_d'])}rad/s"
            )
        return data["classification"]


# ===================================================================
# 10. Two-body problem (tier 6)
# ===================================================================

@register
class TwoBodyProblemGenerator(StepGenerator):
    """Compute reduced mass and orbital energy for the two-body problem.

    Reduced mass mu = m1*m2/(m1+m2). For gravitational orbit:
    E = -G*m1*m2/(2*a) where a is the semi-major axis.

    Difficulty scaling:
        Difficulty 1-3: small masses in [1,50] kg, a in [1,10] m.
        Difficulty 4-6: planetary masses (~10^24 kg), a ~ 10^11 m.
        Difficulty 7-8: stellar masses (~10^30 kg), a ~ 10^12 m.

    Prerequisites:
        conservation_energy.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "two_body_problem"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["conservation_energy"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute reduced mass and orbital energy"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate two-body problem parameters and compute results.

        Args:
            difficulty: Controls mass and distance scales.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            m1 = float(self._rng.randint(1, 50))
            m2 = float(self._rng.randint(1, 50))
            a = float(self._rng.randint(1, 10))
        elif difficulty <= 6:
            m1 = float(self._rng.randint(1, 9)) * 1e24
            m2 = float(self._rng.randint(1, 9)) * 1e24
            a = float(self._rng.randint(1, 9)) * 1e11
        else:
            m1 = float(self._rng.randint(1, 9)) * 1e30
            m2 = float(self._rng.randint(1, 9)) * 1e30
            a = float(self._rng.randint(1, 9)) * 1e12

        mu = m1 * m2 / (m1 + m2)
        energy = -_G_NEWTON * m1 * m2 / (2 * a)

        return "\\mu = \\frac{m_1 m_2}{m_1+m_2}", {
            "m1": m1, "m2": m2, "a": a,
            "mu": mu, "energy": energy,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate two-body problem computation steps.

        Args:
            data: Solution data with masses, a, mu, and energy.

        Returns:
            List of step strings.
        """
        return [
            f"m1={_fmt(data['m1'])}, m2={_fmt(data['m2'])}",
            f"mu = m1*m2/(m1+m2) = {_fmt(data['mu'])} kg",
            f"a={_fmt(data['a'])} m",
            f"E = -Gm1m2/(2a) = {_fmt(data['energy'])} J",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the reduced mass and orbital energy.

        Args:
            data: Solution data.

        Returns:
            mu and E as a string.
        """
        return (
            f"mu={_fmt(data['mu'])}kg, "
            f"E={_fmt(data['energy'])}J"
        )
