"""Analytical mechanics generators -- Lagrangian through canonical transforms.

Covers Lagrangian and Hamiltonian formulations of classical mechanics:
Lagrangian construction, Euler-Lagrange equations of motion, Legendre
transforms, Hamilton's equations, Noether's theorem, phase space analysis,
normal modes of coupled oscillators, and canonical transformations.
Tiers range from 5 (Lagrangian construction) to 7 (Noether, canonical).
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


class _MechFormatter:
    """Formats numeric values for analytical mechanics problems.

    Provides consistent rounding and clean string representations
    to keep target text compact and under the 512-character limit.
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


# ---------------------------------------------------------------------------
# 1. Lagrangian  (tier 5)
# ---------------------------------------------------------------------------


@register
class LagrangianGenerator(StepGenerator):
    """Compute the Lagrangian L = T - V for simple mechanical systems.

    Generates problems involving a mass on a spring, a simple pendulum,
    or a falling body. The model must identify kinetic and potential
    energy expressions and compute L for a given state.

    Input format:
        ``compute the Lagrangian``

    Target format:
        ``L = T - V <step> T = \\frac{1}{2}mv^2 = ... <step>
        V = ... <step> L = T - V = ...``

    Difficulty scaling:
        d1-3: mass on spring with integer parameters.
        d4-6: pendulum (small angle, linearised).
        d7-8: falling body with initial velocity.

    Prerequisites:
        kinetic_energy, potential_energy.
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "lagrangian"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["kinetic_energy", "potential_energy"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls system type and parameter magnitude.

        Returns:
            Natural language description.
        """
        return "compute the Lagrangian"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a mechanical system and compute its Lagrangian.

        Args:
            difficulty: Controls system type and parameter ranges.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            return self._spring_system(difficulty)
        if difficulty <= 6:
            return self._pendulum_system(difficulty)
        return self._falling_body(difficulty)

    def _spring_system(self, difficulty: int) -> tuple[str, dict]:
        """Generate a mass-spring Lagrangian problem.

        Args:
            difficulty: Controls parameter magnitude.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        m = self._rng.randint(1, 5 * difficulty)
        k = self._rng.randint(1, 5 * difficulty)
        v = round(self._rng.uniform(0.5, 3.0 + difficulty), 2)
        x = round(self._rng.uniform(0.1, 2.0 + difficulty * 0.5), 2)
        t_val = round(0.5 * m * v * v, 4)
        v_val = round(0.5 * k * x * x, 4)
        lag = round(t_val - v_val, 4)
        return "L = T - V", {
            "system": "spring", "m": m, "k": k, "v": v, "x": x,
            "T": t_val, "V": v_val, "L": lag,
        }

    def _pendulum_system(self, difficulty: int) -> tuple[str, dict]:
        """Generate a simple pendulum Lagrangian problem.

        Args:
            difficulty: Controls parameter magnitude.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        m = self._rng.randint(1, 3 * difficulty)
        length = round(self._rng.uniform(0.5, 2.0), 2)
        theta_dot = round(self._rng.uniform(0.1, 2.0), 2)
        theta = round(self._rng.uniform(0.1, 0.5), 2)
        g = 9.8
        v_tang = round(length * theta_dot, 4)
        t_val = round(0.5 * m * v_tang * v_tang, 4)
        cos_theta = round(math.cos(theta), 4)
        v_val = round(-m * g * length * cos_theta, 4)
        lag = round(t_val - v_val, 4)
        return "L = T - V", {
            "system": "pendulum", "m": m, "l": length,
            "theta_dot": theta_dot, "theta": theta, "g": g,
            "v_tang": v_tang, "cos_theta": cos_theta,
            "T": t_val, "V": v_val, "L": lag,
        }

    def _falling_body(self, difficulty: int) -> tuple[str, dict]:
        """Generate a falling body Lagrangian problem.

        Args:
            difficulty: Controls parameter magnitude.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        m = self._rng.randint(1, 5 * difficulty)
        v = round(self._rng.uniform(1.0, 5.0 + difficulty), 2)
        h = round(self._rng.uniform(1.0, 10.0 + difficulty), 2)
        g = 9.8
        t_val = round(0.5 * m * v * v, 4)
        v_val = round(m * g * h, 4)
        lag = round(t_val - v_val, 4)
        return "L = T - V", {
            "system": "falling", "m": m, "v": v, "h": h, "g": g,
            "T": t_val, "V": v_val, "L": lag,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Lagrangian computation steps.

        Args:
            data: Solution data with T, V, and system parameters.

        Returns:
            Steps showing kinetic energy, potential energy, and L.
        """
        system = data["system"]
        t_str = _MechFormatter.fmt(data["T"])
        v_str = _MechFormatter.fmt(data["V"])
        if system == "spring":
            return [
                f"T = \\frac{{1}}{{2}}({data['m']})({data['v']})^2 = {t_str}",
                f"V = \\frac{{1}}{{2}}({data['k']})({data['x']})^2 = {v_str}",
                f"L = {t_str} - {v_str}",
            ]
        if system == "pendulum":
            return [
                f"v = l\\dot{{\\theta}} = ({data['l']})({data['theta_dot']}) = {_MechFormatter.fmt(data['v_tang'])}",
                f"T = \\frac{{1}}{{2}}({data['m']})({_MechFormatter.fmt(data['v_tang'])})^2 = {t_str}",
                f"V = -({data['m']})(9.8)({data['l']})\\cos({data['theta']}) = {v_str}",
                f"L = {t_str} - ({v_str})",
            ]
        return [
            f"T = \\frac{{1}}{{2}}({data['m']})({data['v']})^2 = {t_str}",
            f"V = ({data['m']})(9.8)({data['h']}) = {v_str}",
            f"L = {t_str} - {v_str}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the Lagrangian value.

        Args:
            data: Solution data.

        Returns:
            String representation of L.
        """
        return f"L = {_MechFormatter.fmt(data['L'])}"


# ---------------------------------------------------------------------------
# 2. Euler-Lagrange equations of motion  (tier 6)
# ---------------------------------------------------------------------------


@register
class EulerLagrangeMechGenerator(StepGenerator):
    """Derive equations of motion from a Lagrangian using Euler-Lagrange.

    Applies d/dt(dL/dq_dot) - dL/dq = 0 to simple Lagrangians of the
    form L = a*q_dot^2 + b*q^2 + c*q. The model must compute partial
    derivatives and form the equation of motion.

    Input format:
        ``derive equation of motion from Lagrangian``

    Target format:
        ``\\frac{d}{dt}\\frac{\\partial L}{\\partial \\dot{q}}
        - \\frac{\\partial L}{\\partial q} = 0 <step>
        \\frac{\\partial L}{\\partial \\dot{q}} = 2a\\dot{q} <step>
        \\frac{d}{dt}(2a\\dot{q}) = 2a\\ddot{q} <step>
        \\frac{\\partial L}{\\partial q} = 2bq + c <step>
        2a\\ddot{q} - 2bq - c = 0``

    Difficulty scaling:
        d1-3: L = a*q_dot^2 - b*q^2 (harmonic oscillator form).
        d4-6: L = a*q_dot^2 - b*q^2 + c*q (with linear term).
        d7-8: L = a*q_dot^2 + d*q*q_dot - b*q^2 (mixed term).

    Prerequisites:
        lagrangian.
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "euler_lagrange_mechanics"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["lagrangian"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls Lagrangian complexity.

        Returns:
            Natural language description.
        """
        return "derive equation of motion from Lagrangian"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Lagrangian and derive the equation of motion.

        Args:
            difficulty: Controls number of terms.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        a = self._rng.randint(1, 5 + difficulty)
        b = self._rng.randint(1, 5 + difficulty)
        c = 0
        d_coeff = 0
        if difficulty >= 4:
            c = self._rng.randint(1, 3 * difficulty)
        if difficulty >= 7:
            d_coeff = self._rng.randint(1, difficulty)

        formula = "\\frac{d}{dt}\\frac{\\partial L}{\\partial \\dot{q}} - \\frac{\\partial L}{\\partial q} = 0"
        return formula, {
            "a": a, "b": b, "c": c, "d": d_coeff,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Euler-Lagrange derivation steps.

        Args:
            data: Solution data with Lagrangian coefficients.

        Returns:
            Steps showing partial derivatives and the EOM.
        """
        a, b, c, d = data["a"], data["b"], data["c"], data["d"]
        steps = []
        if d == 0:
            lag_str = f"L = {a}\\dot{{q}}^2 - {b}q^2"
            if c != 0:
                lag_str += f" + {c}q"
            steps.append(lag_str)
            steps.append(f"\\frac{{\\partial L}}{{\\partial \\dot{{q}}}} = {2*a}\\dot{{q}}")
            steps.append(f"\\frac{{d}}{{dt}}({2*a}\\dot{{q}}) = {2*a}\\ddot{{q}}")
            dldq = f"-{2*b}q"
            if c != 0:
                dldq += f" + {c}"
            steps.append(f"\\frac{{\\partial L}}{{\\partial q}} = {dldq}")
            eom = f"{2*a}\\ddot{{q}} + {2*b}q"
            if c != 0:
                eom += f" - {c}"
            steps.append(f"{eom} = 0")
        else:
            lag_str = f"L = {a}\\dot{{q}}^2 + {d}q\\dot{{q}} - {b}q^2"
            steps.append(lag_str)
            steps.append(f"\\frac{{\\partial L}}{{\\partial \\dot{{q}}}} = {2*a}\\dot{{q}} + {d}q")
            steps.append(f"\\frac{{d}}{{dt}}(...) = {2*a}\\ddot{{q}} + {d}\\dot{{q}}")
            steps.append(f"\\frac{{\\partial L}}{{\\partial q}} = {d}\\dot{{q}} - {2*b}q")
            steps.append(f"{2*a}\\ddot{{q}} + {2*b}q = 0")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the equation of motion.

        Args:
            data: Solution data.

        Returns:
            The EOM as a string.
        """
        a, b, c, d = data["a"], data["b"], data["c"], data["d"]
        if d != 0:
            return f"{2*a}\\ddot{{q}} + {2*b}q = 0"
        eom = f"{2*a}\\ddot{{q}} + {2*b}q"
        if c != 0:
            eom += f" - {c}"
        return f"{eom} = 0"


# ---------------------------------------------------------------------------
# 3. Hamiltonian  (tier 6)
# ---------------------------------------------------------------------------


@register
class HamiltonianGenerator(StepGenerator):
    """Compute the Hamiltonian via Legendre transform: H = p*q_dot - L.

    Given a Lagrangian L(q, q_dot) = a*q_dot^2 - V(q), computes the
    conjugate momentum p = dL/dq_dot, solves for q_dot(p), and
    expresses H(q, p) = p^2/(4a) + V(q).

    Input format:
        ``compute the Hamiltonian``

    Target format:
        ``H = p\\dot{q} - L <step>
        p = \\frac{\\partial L}{\\partial \\dot{q}} = 2a\\dot{q} <step>
        \\dot{q} = p/(2a) <step>
        H = p^2/(4a) + V(q)``

    Difficulty scaling:
        d1-3: V(q) = b*q^2 (harmonic).
        d4-6: V(q) = b*q^2 - c*q (shifted harmonic).
        d7-8: V(q) = b*q^2 + c*q^4 (anharmonic).

    Prerequisites:
        lagrangian.
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "hamiltonian"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["lagrangian"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls potential complexity.

        Returns:
            Natural language description.
        """
        return "compute the Hamiltonian"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Lagrangian and compute the Hamiltonian.

        Args:
            difficulty: Controls potential function complexity.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        a = self._rng.randint(1, 3 + difficulty)
        b = self._rng.randint(1, 3 + difficulty)
        c = 0
        pot_type = "harmonic"
        if difficulty >= 4:
            c = self._rng.randint(1, difficulty)
            pot_type = "shifted"
        if difficulty >= 7:
            pot_type = "anharmonic"
        p_val = self._rng.randint(1, 5 + difficulty)
        q_val = round(self._rng.uniform(0.5, 3.0), 2)
        q_dot = round(p_val / (2.0 * a), 4)
        if pot_type == "harmonic":
            v_q = round(b * q_val * q_val, 4)
        elif pot_type == "shifted":
            v_q = round(b * q_val * q_val - c * q_val, 4)
        else:
            v_q = round(b * q_val * q_val + c * q_val ** 4, 4)
        h_val = round(p_val * p_val / (4.0 * a) + v_q, 4)
        return "H = p\\dot{q} - L", {
            "a": a, "b": b, "c": c, "pot_type": pot_type,
            "p": p_val, "q": q_val, "q_dot": q_dot,
            "V": v_q, "H": h_val,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Legendre transform steps.

        Args:
            data: Solution data with Lagrangian coefficients and H.

        Returns:
            Steps showing p, q_dot(p), and H(q, p).
        """
        a = data["a"]
        p = data["p"]
        q = data["q"]
        v_str = _MechFormatter.fmt(data["V"])
        steps = [
            f"p = \\frac{{\\partial L}}{{\\partial \\dot{{q}}}} = {2*a}\\dot{{q}}",
            f"\\dot{{q}} = p/({2*a}) = {p}/({2*a}) = {_MechFormatter.fmt(data['q_dot'])}",
            f"V(q={_MechFormatter.fmt(q)}) = {v_str}",
            f"H = p^2/(4 \\cdot {a}) + V = {p}^2/{4*a} + {v_str}",
        ]
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the Hamiltonian value.

        Args:
            data: Solution data.

        Returns:
            String representation of H.
        """
        return f"H = {_MechFormatter.fmt(data['H'])}"


# ---------------------------------------------------------------------------
# 4. Hamilton's equations  (tier 6)
# ---------------------------------------------------------------------------


@register
class HamiltonEquationsGenerator(StepGenerator):
    """Write Hamilton's equations for a given Hamiltonian.

    Given H(q, p) = p^2/(2m) + V(q), compute dq/dt = dH/dp and
    dp/dt = -dH/dq. Evaluates at a specific (q, p) point.

    Input format:
        ``compute Hamilton's equations``

    Target format:
        ``\\dot{q} = \\frac{\\partial H}{\\partial p}, \\;
        \\dot{p} = -\\frac{\\partial H}{\\partial q} <step>
        H = p^2/(2m) + b*q^2 <step>
        \\dot{q} = p/m = ... <step>
        \\dot{p} = -2bq = ...``

    Difficulty scaling:
        d1-3: V = b*q^2 (harmonic).
        d4-6: V = b*q^2 + c*q (linear + quadratic).
        d7-8: V = b*q^2 + c*q^3 (cubic potential).

    Prerequisites:
        hamiltonian.
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "hamilton_equations"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["hamiltonian"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls potential complexity.

        Returns:
            Natural language description.
        """
        return "compute Hamilton's equations"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Hamiltonian and evaluate Hamilton's equations.

        Args:
            difficulty: Controls potential function complexity.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        m = self._rng.randint(1, 3 + difficulty)
        b = self._rng.randint(1, 3 + difficulty)
        c = 0
        pot_type = "quadratic"
        if difficulty >= 4:
            c = self._rng.randint(1, difficulty)
            pot_type = "linear_quad"
        if difficulty >= 7:
            pot_type = "cubic"
        p_val = self._rng.randint(1, 5 + difficulty)
        q_val = round(self._rng.uniform(0.5, 3.0), 2)
        q_dot = round(p_val / m, 4)
        if pot_type == "quadratic":
            p_dot = round(-2 * b * q_val, 4)
        elif pot_type == "linear_quad":
            p_dot = round(-2 * b * q_val - c, 4)
        else:
            p_dot = round(-2 * b * q_val - 3 * c * q_val * q_val, 4)
        formula = "\\dot{q} = \\frac{\\partial H}{\\partial p}, \\; \\dot{p} = -\\frac{\\partial H}{\\partial q}"
        return formula, {
            "m": m, "b": b, "c": c, "pot_type": pot_type,
            "p": p_val, "q": q_val,
            "q_dot": q_dot, "p_dot": p_dot,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Hamilton's equations evaluation steps.

        Args:
            data: Solution data with Hamiltonian parameters.

        Returns:
            Steps showing derivatives and evaluation.
        """
        m, b, c = data["m"], data["b"], data["c"]
        p, q = data["p"], data["q"]
        pot = data["pot_type"]
        h_str = f"H = p^2/(2 \\cdot {m})"
        if pot == "quadratic":
            h_str += f" + {b}q^2"
        elif pot == "linear_quad":
            h_str += f" + {b}q^2 + {c}q"
        else:
            h_str += f" + {b}q^2 + {c}q^3"
        steps = [h_str]
        steps.append(f"\\dot{{q}} = p/{m} = {p}/{m} = {_MechFormatter.fmt(data['q_dot'])}")
        if pot == "quadratic":
            steps.append(f"\\dot{{p}} = -{2*b}q = -{2*b}({_MechFormatter.fmt(q)}) = {_MechFormatter.fmt(data['p_dot'])}")
        elif pot == "linear_quad":
            steps.append(f"\\dot{{p}} = -{2*b}q - {c} = {_MechFormatter.fmt(data['p_dot'])}")
        else:
            steps.append(f"\\dot{{p}} = -{2*b}q - {3*c}q^2 = {_MechFormatter.fmt(data['p_dot'])}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return Hamilton's equations evaluated at the given point.

        Args:
            data: Solution data.

        Returns:
            String with q_dot and p_dot values.
        """
        return f"\\dot{{q}} = {_MechFormatter.fmt(data['q_dot'])}, \\dot{{p}} = {_MechFormatter.fmt(data['p_dot'])}"


# ---------------------------------------------------------------------------
# 5. Noether's theorem  (tier 7)
# ---------------------------------------------------------------------------


@register
class NoetherTheoremGenerator(StepGenerator):
    """Identify conserved quantities from symmetries via Noether's theorem.

    Given a Lagrangian with a specific symmetry (time translation, space
    translation, or rotation), the model must identify the corresponding
    conserved quantity: energy, linear momentum, or angular momentum.

    Input format:
        ``identify conserved quantity from symmetry``

    Target format:
        ``L = ... <step>
        symmetry: time translation invariance <step>
        dL/dt = 0 (no explicit time dependence) <step>
        conserved quantity: energy H = T + V``

    Difficulty scaling:
        d1-3: time translation -> energy conservation.
        d4-6: space translation -> linear momentum conservation.
        d7-8: rotational symmetry -> angular momentum conservation.

    Prerequisites:
        lagrangian.
    """

    _SYMMETRIES = [
        ("time_translation", "energy", "H = T + V"),
        ("space_translation", "linear momentum", "p = m\\dot{q}"),
        ("rotation", "angular momentum", "L_z = mr^2\\dot{\\theta}"),
    ]

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "noether_theorem"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["lagrangian"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls symmetry type.

        Returns:
            Natural language description.
        """
        return "identify conserved quantity from symmetry"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Lagrangian and identify its symmetry.

        Args:
            difficulty: Controls which symmetry type is tested.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            idx = 0
        elif difficulty <= 6:
            idx = 1
        else:
            idx = 2
        sym_name, conserved, expr = self._SYMMETRIES[idx]
        m = self._rng.randint(1, 5 + difficulty)
        k = self._rng.randint(1, 5 + difficulty)
        if idx == 0:
            lag = f"L = \\frac{{1}}{{2}}({m})\\dot{{q}}^2 - \\frac{{1}}{{2}}({k})q^2"
            reason = "no explicit time dependence"
        elif idx == 1:
            lag = f"L = \\frac{{1}}{{2}}({m})\\dot{{x}}^2"
            reason = "L does not depend on x"
        else:
            lag = f"L = \\frac{{1}}{{2}}({m})(\\dot{{r}}^2 + r^2\\dot{{\\theta}}^2) - V(r)"
            reason = "L does not depend on \\theta"
        return lag, {
            "sym_name": sym_name, "conserved": conserved,
            "expression": expr, "lagrangian": lag,
            "reason": reason, "m": m, "k": k,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Noether theorem identification steps.

        Args:
            data: Solution data with symmetry and conserved quantity.

        Returns:
            Steps showing symmetry identification and conserved quantity.
        """
        return [
            data["lagrangian"],
            f"symmetry: {data['sym_name'].replace('_', ' ')}",
            data["reason"],
            f"conserved: {data['conserved']} = {data['expression']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the conserved quantity.

        Args:
            data: Solution data.

        Returns:
            String identifying the conserved quantity.
        """
        return f"conserved quantity: {data['conserved']}"


# ---------------------------------------------------------------------------
# 6. Phase space analysis  (tier 6)
# ---------------------------------------------------------------------------


@register
class PhaseSpaceGenerator(StepGenerator):
    """Classify fixed points in 1D Hamiltonian phase space.

    Given H = p^2/2 + V(q) with a polynomial potential, finds
    equilibrium points (dV/dq = 0) and classifies them as centers
    (local minima of V) or saddle points (local maxima of V).

    Input format:
        ``classify fixed points in phase space``

    Target format:
        ``H = p^2/2 + V(q) <step>
        V(q) = aq^2 + bq^4 <step>
        dV/dq = 2aq + 4bq^3 = 0 <step>
        q* = 0 <step>
        d^2V/dq^2|_{q*} = 2a > 0 -> center``

    Difficulty scaling:
        d1-3: V = a*q^2 (single center at origin).
        d4-6: V = -a*q^2 + b*q^4 (saddle at 0, centers at +/- sqrt(a/2b)).
        d7-8: V = a*q^2 + b*q^3 (asymmetric potential).

    Prerequisites:
        hamilton_equations.
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "phase_space"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["hamilton_equations"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls potential complexity.

        Returns:
            Natural language description.
        """
        return "classify fixed points in phase space"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a potential and classify its fixed points.

        Args:
            difficulty: Controls potential function complexity.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            return self._simple_harmonic(difficulty)
        if difficulty <= 6:
            return self._double_well(difficulty)
        return self._asymmetric(difficulty)

    def _simple_harmonic(self, difficulty: int) -> tuple[str, dict]:
        """Generate a simple harmonic potential analysis.

        Args:
            difficulty: Controls coefficient magnitude.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        a = self._rng.randint(1, 3 + difficulty)
        d2v = 2 * a
        return "H = p^2/2 + V(q)", {
            "V_str": f"{a}q^2", "dV": f"{2*a}q",
            "fixed_points": ["q* = 0"],
            "d2V_at_fp": [d2v],
            "types": ["center"],
        }

    def _double_well(self, difficulty: int) -> tuple[str, dict]:
        """Generate a double-well potential analysis.

        Args:
            difficulty: Controls coefficient magnitude.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        a = self._rng.randint(1, difficulty)
        b = self._rng.randint(1, difficulty)
        q_star = round(math.sqrt(a / (2.0 * b)), 4)
        d2v_0 = -2 * a
        d2v_side = round(-2 * a + 12 * b * q_star * q_star, 4)
        return "H = p^2/2 + V(q)", {
            "V_str": f"-{a}q^2 + {b}q^4",
            "dV": f"-{2*a}q + {4*b}q^3",
            "fixed_points": ["q* = 0", f"q* = +/-{_MechFormatter.fmt(q_star)}"],
            "d2V_at_fp": [d2v_0, d2v_side],
            "types": ["saddle", "center"],
        }

    def _asymmetric(self, difficulty: int) -> tuple[str, dict]:
        """Generate an asymmetric potential analysis.

        Args:
            difficulty: Controls coefficient magnitude.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        a = self._rng.randint(1, difficulty)
        b = self._rng.randint(1, difficulty)
        q_star = round(-2.0 * a / (3.0 * b), 4)
        d2v_0 = 2 * a
        d2v_q = round(2 * a + 6 * b * q_star, 4)
        t0 = "center" if d2v_0 > 0 else "saddle"
        tq = "center" if d2v_q > 0 else "saddle"
        return "H = p^2/2 + V(q)", {
            "V_str": f"{a}q^2 + {b}q^3",
            "dV": f"{2*a}q + {3*b}q^2",
            "fixed_points": ["q* = 0", f"q* = {_MechFormatter.fmt(q_star)}"],
            "d2V_at_fp": [d2v_0, d2v_q],
            "types": [t0, tq],
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate phase space analysis steps.

        Args:
            data: Solution data with fixed points and classifications.

        Returns:
            Steps showing potential, derivative, fixed points, and types.
        """
        steps = [
            f"V(q) = {data['V_str']}",
            f"dV/dq = {data['dV']} = 0",
        ]
        for fp, d2v, fp_type in zip(
            data["fixed_points"], data["d2V_at_fp"], data["types"]
        ):
            sign = "> 0" if d2v > 0 else "< 0"
            steps.append(f"{fp}: d^2V/dq^2 = {_MechFormatter.fmt(d2v)} {sign} -> {fp_type}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the fixed point classifications.

        Args:
            data: Solution data.

        Returns:
            String listing fixed points and their types.
        """
        parts = []
        for fp, fp_type in zip(data["fixed_points"], data["types"]):
            parts.append(f"{fp} ({fp_type})")
        return "; ".join(parts)


# ---------------------------------------------------------------------------
# 7. Normal modes  (tier 6)
# ---------------------------------------------------------------------------


@register
class NormalModesGenerator(StepGenerator):
    """Find normal mode frequencies of coupled oscillators.

    For two coupled masses with stiffness matrix K and mass matrix M,
    solves det(K - omega^2 * M) = 0 to find the normal mode
    frequencies omega_1 and omega_2.

    Input format:
        ``find normal mode frequencies``

    Target format:
        ``\\det(K - \\omega^2 M) = 0 <step>
        K = [[k1+k2, -k2],[-k2, k2+k3]], M = [[m1,0],[0,m2]] <step>
        (k1+k2 - m1*w^2)(k2+k3 - m2*w^2) - k2^2 = 0 <step>
        w^2 = ... <step> w_1 = ..., w_2 = ...``

    Difficulty scaling:
        d1-3: equal masses, symmetric coupling (k1 = k3).
        d4-6: unequal masses, symmetric coupling.
        d7-8: unequal masses and asymmetric coupling.

    Prerequisites:
        eigenvalue.
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "normal_modes"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["eigenvalue"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls system complexity.

        Returns:
            Natural language description.
        """
        return "find normal mode frequencies"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate coupled oscillator parameters and find normal modes.

        Args:
            difficulty: Controls symmetry of the system.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            m1 = m2 = self._rng.randint(1, 3 + difficulty)
            k1 = k3 = self._rng.randint(1, 5 + difficulty)
            k2 = self._rng.randint(1, 3 + difficulty)
        elif difficulty <= 6:
            m1 = self._rng.randint(1, 3 + difficulty)
            m2 = self._rng.randint(1, 3 + difficulty)
            k1 = k3 = self._rng.randint(1, 5 + difficulty)
            k2 = self._rng.randint(1, 3 + difficulty)
        else:
            m1 = self._rng.randint(1, 3 + difficulty)
            m2 = self._rng.randint(1, 3 + difficulty)
            k1 = self._rng.randint(1, 5 + difficulty)
            k2 = self._rng.randint(1, 5 + difficulty)
            k3 = self._rng.randint(1, 5 + difficulty)
        a11 = (k1 + k2) / m1
        a22 = (k2 + k3) / m2
        a12_sq = (k2 * k2) / (m1 * m2)
        trace = a11 + a22
        det_val = a11 * a22 - a12_sq
        disc = trace * trace - 4 * det_val
        disc = max(disc, 0.0)
        w1_sq = round((trace - math.sqrt(disc)) / 2.0, 4)
        w2_sq = round((trace + math.sqrt(disc)) / 2.0, 4)
        w1 = round(math.sqrt(max(w1_sq, 0.0)), 4)
        w2 = round(math.sqrt(max(w2_sq, 0.0)), 4)
        return "\\det(K - \\omega^2 M) = 0", {
            "m1": m1, "m2": m2, "k1": k1, "k2": k2, "k3": k3,
            "a11": round(a11, 4), "a22": round(a22, 4),
            "trace": round(trace, 4), "det": round(det_val, 4),
            "w1_sq": w1_sq, "w2_sq": w2_sq,
            "w1": w1, "w2": w2,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate normal mode frequency computation steps.

        Args:
            data: Solution data with masses, springs, and frequencies.

        Returns:
            Steps showing matrices, characteristic equation, and roots.
        """
        k1, k2, k3 = data["k1"], data["k2"], data["k3"]
        m1, m2 = data["m1"], data["m2"]
        steps = [
            f"K = [[{k1+k2}, -{k2}],[{-k2}, {k2+k3}]], M = [[{m1},0],[0,{m2}]]",
            f"trace = {_MechFormatter.fmt(data['trace'])}, det = {_MechFormatter.fmt(data['det'])}",
            f"\\omega_1^2 = {_MechFormatter.fmt(data['w1_sq'])}, \\omega_2^2 = {_MechFormatter.fmt(data['w2_sq'])}",
        ]
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the normal mode frequencies.

        Args:
            data: Solution data.

        Returns:
            String with omega_1 and omega_2 values.
        """
        return f"\\omega_1 = {_MechFormatter.fmt(data['w1'])}, \\omega_2 = {_MechFormatter.fmt(data['w2'])}"


# ---------------------------------------------------------------------------
# 8. Canonical transformation  (tier 7)
# ---------------------------------------------------------------------------


@register
class CanonicalTransformGenerator(StepGenerator):
    """Verify a transformation is canonical via the Poisson bracket.

    Given a coordinate transformation (Q(q,p), P(q,p)), checks whether
    {Q, P} = dQ/dq * dP/dp - dQ/dp * dP/dq = 1. Uses simple
    generating function forms (point transforms and exchange transforms).

    Input format:
        ``verify canonical transformation``

    Target format:
        ``\\{Q, P\\} = \\frac{\\partial Q}{\\partial q}
        \\frac{\\partial P}{\\partial p}
        - \\frac{\\partial Q}{\\partial p}
        \\frac{\\partial P}{\\partial q} <step>
        Q = ..., P = ... <step>
        dQ/dq = ..., dQ/dp = ..., dP/dq = ..., dP/dp = ... <step>
        {Q,P} = ... = 1 -> canonical``

    Difficulty scaling:
        d1-3: Q = q, P = p + a*q (simple shift).
        d4-6: Q = a*q, P = p/a (scaling).
        d7-8: Q = p, P = -q + a*p (exchange-type).

    Prerequisites:
        hamilton_equations.
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "canonical_transform"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["hamilton_equations"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls transformation complexity.

        Returns:
            Natural language description.
        """
        return "verify canonical transformation"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a transformation and compute its Poisson bracket.

        Args:
            difficulty: Controls transformation type.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            return self._shift_transform(difficulty)
        if difficulty <= 6:
            return self._scaling_transform(difficulty)
        return self._exchange_transform(difficulty)

    def _shift_transform(self, difficulty: int) -> tuple[str, dict]:
        """Generate a shifted canonical transformation.

        Args:
            difficulty: Controls shift magnitude.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        a = self._rng.randint(1, 3 + difficulty)
        dq_dq, dq_dp = 1, 0
        dp_dq, dp_dp = a, 1
        pb = dq_dq * dp_dp - dq_dp * dp_dq
        return "\\{Q, P\\} = 1", {
            "Q_str": "q", "P_str": f"p + {a}q",
            "dQ_dq": dq_dq, "dQ_dp": dq_dp,
            "dP_dq": dp_dq, "dP_dp": dp_dp,
            "poisson": pb, "canonical": pb == 1,
        }

    def _scaling_transform(self, difficulty: int) -> tuple[str, dict]:
        """Generate a scaling canonical transformation.

        Args:
            difficulty: Controls scale factor.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        a = self._rng.randint(2, 2 + difficulty)
        dq_dq, dq_dp = a, 0
        dp_dq = 0
        dp_dp_val = round(1.0 / a, 4)
        pb = round(dq_dq * dp_dp_val - dq_dp * dp_dq, 4)
        return "\\{Q, P\\} = 1", {
            "Q_str": f"{a}q", "P_str": f"p/{a}",
            "dQ_dq": dq_dq, "dQ_dp": dq_dp,
            "dP_dq": dp_dq, "dP_dp": dp_dp_val,
            "poisson": pb, "canonical": abs(pb - 1.0) < 1e-10,
        }

    def _exchange_transform(self, difficulty: int) -> tuple[str, dict]:
        """Generate an exchange-type canonical transformation.

        Args:
            difficulty: Controls coefficient.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        a = self._rng.randint(1, difficulty)
        dq_dq, dq_dp = 0, 1
        dp_dq, dp_dp = -1, a
        pb = dq_dq * dp_dp - dq_dp * dp_dq
        return "\\{Q, P\\} = 1", {
            "Q_str": "p", "P_str": f"-q + {a}p",
            "dQ_dq": dq_dq, "dQ_dp": dq_dp,
            "dP_dq": dp_dq, "dP_dp": dp_dp,
            "poisson": pb, "canonical": pb == 1,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Poisson bracket verification steps.

        Args:
            data: Solution data with transformation and derivatives.

        Returns:
            Steps showing the transformation, derivatives, and bracket.
        """
        q_str = data["Q_str"]
        p_str = data["P_str"]
        dq_dq = _MechFormatter.fmt(data["dQ_dq"])
        dq_dp = _MechFormatter.fmt(data["dQ_dp"])
        dp_dq = _MechFormatter.fmt(data["dP_dq"])
        dp_dp = _MechFormatter.fmt(data["dP_dp"])
        pb = _MechFormatter.fmt(data["poisson"])
        canon = "canonical" if data["canonical"] else "not canonical"
        return [
            f"Q = {q_str}, P = {p_str}",
            f"dQ/dq={dq_dq}, dQ/dp={dq_dp}, dP/dq={dp_dq}, dP/dp={dp_dp}",
            f"{{Q,P}} = ({dq_dq})({dp_dp}) - ({dq_dp})({dp_dq}) = {pb}",
            canon,
        ]

    def _create_answer(self, data: dict) -> str:
        """Return whether the transformation is canonical.

        Args:
            data: Solution data.

        Returns:
            String with Poisson bracket result and verdict.
        """
        pb = _MechFormatter.fmt(data["poisson"])
        verdict = "canonical" if data["canonical"] else "not canonical"
        return f"{{Q,P}} = {pb} -> {verdict}"
