"""Fluid mechanics generators -- Bernoulli, Reynolds, continuity, drag, buoyancy.

Covers Bernoulli's equation, Reynolds number classification, the
continuity equation, drag force, Archimedes' buoyancy, and
Hagen-Poiseuille viscous flow. Tiers range from 4 (introductory
fluid statics) to 5 (viscous flow).
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


class _FluidFormatter:
    """Formats numeric values for fluid mechanics problems.

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


_f = _FluidFormatter.fmt

_G = 9.81  # gravitational acceleration (m/s^2)


# ===================================================================
# 1. Bernoulli's equation  (tier 4)
# ===================================================================

@register
class BernoulliGenerator(StepGenerator):
    """Bernoulli's equation for incompressible flow.

    P1 + 0.5*rho*v1^2 + rho*g*h1 = P2 + 0.5*rho*v2^2 + rho*g*h2.
    Given five of six quantities, solves for the missing one.

    Difficulty scaling:
        Difficulty 1-3: horizontal flow (h1=h2=0), solve for P2 or v2.
        Difficulty 4-6: include height difference.
        Difficulty 7-8: solve for any variable including rho.

    Prerequisites:
        multiplication.
    """

    _TARGETS_SIMPLE = ["P2", "v2"]
    _TARGETS_FULL = ["P1", "P2", "v1", "v2"]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "bernoulli"

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
        return "apply Bernoulli's equation"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate Bernoulli equation parameters and solve target.

        Args:
            difficulty: Controls problem complexity.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        rho = self._rng.choice([1000, 1000, 1025, 800, 13600][:min(difficulty, 5)])
        v1 = round(self._rng.uniform(1.0, 5.0 + difficulty), 1)
        v2 = round(self._rng.uniform(1.0, 5.0 + difficulty), 1)
        p1 = self._rng.randint(100, 200 + difficulty * 50) * 1000

        if difficulty <= 3:
            h1, h2 = 0.0, 0.0
        else:
            h1 = round(self._rng.uniform(0, 5.0 + difficulty), 1)
            h2 = round(self._rng.uniform(0, 5.0 + difficulty), 1)

        lhs = p1 + 0.5 * rho * v1 ** 2 + rho * _G * h1
        rhs_without_p2 = 0.5 * rho * v2 ** 2 + rho * _G * h2
        p2 = round(lhs - rhs_without_p2, 4)

        if difficulty <= 3:
            target = self._rng.choice(self._TARGETS_SIMPLE)
        else:
            target = self._rng.choice(self._TARGETS_FULL)

        return ("P_1 + \\frac{1}{2}\\rho v_1^2 + \\rho g h_1"
                " = P_2 + \\frac{1}{2}\\rho v_2^2 + \\rho g h_2"), {
            "rho": rho, "v1": v1, "v2": v2,
            "P1": p1, "P2": p2,
            "h1": h1, "h2": h2,
            "target": target,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Bernoulli substitution and solving steps.

        Args:
            data: Solution data with pressures, velocities, heights.

        Returns:
            List of step strings.
        """
        rho = data["rho"]
        ke1 = round(0.5 * rho * data["v1"] ** 2, 4)
        ke2 = round(0.5 * rho * data["v2"] ** 2, 4)
        pe1 = round(rho * _G * data["h1"], 4)
        pe2 = round(rho * _G * data["h2"], 4)
        lhs = round(data["P1"] + ke1 + pe1, 4)
        steps = [
            f"rho={rho}, v1={data['v1']}, v2={data['v2']}, "
            f"h1={data['h1']}, h2={data['h2']}",
            f"0.5*rho*v1^2 = {_f(ke1)}, 0.5*rho*v2^2 = {_f(ke2)}",
        ]
        target = data["target"]
        if target == "P2":
            steps.append(f"P2 = P1 + 0.5*rho*(v1^2-v2^2) + rho*g*(h1-h2)")
        elif target == "v2":
            delta_p = data["P1"] - data["P2"]
            delta_h = data["h1"] - data["h2"]
            steps.append(
                f"v2^2 = v1^2 + 2*(P1-P2)/rho + 2*g*(h1-h2)"
            )
        else:
            steps.append(f"LHS total = {_f(lhs)}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the solved Bernoulli variable.

        Args:
            data: Solution data.

        Returns:
            String representation of the target with units.
        """
        target = data["target"]
        val = data[target]
        if target in ("P1", "P2"):
            return f"{target} = {_f(val)} Pa"
        return f"{target} = {_f(val)} m/s"


# ===================================================================
# 2. Reynolds number  (tier 4)
# ===================================================================

@register
class ReynoldsNumberGenerator(StepGenerator):
    """Reynolds number: Re = rho * v * L / mu.

    Computes the Reynolds number and classifies the flow as
    laminar (Re < 2300) or turbulent (Re > 4000).

    Difficulty scaling:
        Difficulty 1-3: water in pipe, integer values.
        Difficulty 4-6: varied fluids (oil, glycerine).
        Difficulty 7-8: solve for velocity given Re threshold.

    Prerequisites:
        multiplication, division.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "reynolds_number"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["multiplication", "division"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute Reynolds number and classify flow"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate flow parameters and compute Reynolds number.

        Args:
            difficulty: Controls fluid type and problem variant.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            rho = 1000
            mu = 0.001
            fluid = "water"
        elif difficulty <= 5:
            rho = self._rng.choice([1000, 900, 850])
            mu = round(self._rng.uniform(0.001, 0.05), 4)
            fluid = "oil"
        else:
            rho = self._rng.choice([1000, 1260, 800])
            mu = round(self._rng.uniform(0.001, 1.0), 4)
            fluid = "fluid"

        v = round(self._rng.uniform(0.1, 5.0 + difficulty), 2)
        length = round(self._rng.uniform(0.01, 0.1 + difficulty * 0.02), 3)

        re = round(rho * v * length / mu, 4)

        if re < 2300:
            classification = "laminar"
        elif re > 4000:
            classification = "turbulent"
        else:
            classification = "transitional"

        return "Re = \\frac{\\rho v L}{\\mu}", {
            "rho": rho, "v": v, "L": length, "mu": mu,
            "Re": re, "class": classification, "fluid": fluid,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Reynolds number computation steps.

        Args:
            data: Solution data with fluid parameters.

        Returns:
            List of step strings.
        """
        num = round(data["rho"] * data["v"] * data["L"], 4)
        return [
            f"rho={data['rho']}, v={data['v']}m/s, "
            f"L={data['L']}m, mu={data['mu']} Pa*s",
            f"rho*v*L = {_f(num)}",
            f"Re = {_f(num)}/{data['mu']} = {_f(data['Re'])}",
            f"Re {'<' if data['Re'] < 2300 else '>'} "
            f"{'2300 => laminar' if data['class'] == 'laminar' else '4000 => turbulent' if data['class'] == 'turbulent' else '2300-4000 => transitional'}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the Reynolds number and classification.

        Args:
            data: Solution data.

        Returns:
            String with Re value and flow regime.
        """
        return f"Re = {_f(data['Re'])}, {data['class']}"


# ===================================================================
# 3. Continuity equation  (tier 4)
# ===================================================================

@register
class ContinuityEquationGenerator(StepGenerator):
    """Continuity equation: A1 * v1 = A2 * v2.

    For incompressible flow, the volume flow rate is conserved.
    Given three of the four quantities, computes the missing one.

    Difficulty scaling:
        Difficulty 1-3: circular pipes, integer diameters in cm.
        Difficulty 4-6: rectangular cross sections.
        Difficulty 7-8: solve for area or diameter.

    Prerequisites:
        division.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "continuity_equation"

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
        return "apply continuity equation for fluid flow"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate pipe parameters and choose solve target.

        Args:
            difficulty: Controls geometry and problem variant.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        d1_cm = self._rng.randint(2, 10 + difficulty * 2)
        d2_cm = self._rng.randint(1, max(2, d1_cm - 1))
        r1 = d1_cm / 200.0
        r2 = d2_cm / 200.0
        a1 = round(math.pi * r1 ** 2, 4)
        a2 = round(math.pi * r2 ** 2, 4)
        v1 = round(self._rng.uniform(0.5, 3.0 + difficulty), 2)
        v2 = round(a1 * v1 / a2, 4)

        target = self._rng.choice(["v1", "v2", "A1", "A2"])

        return "A_1 v_1 = A_2 v_2", {
            "d1_cm": d1_cm, "d2_cm": d2_cm,
            "A1": a1, "A2": a2,
            "v1": v1, "v2": v2,
            "Q": round(a1 * v1, 4),
            "target": target,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate continuity equation steps.

        Args:
            data: Solution data with areas and velocities.

        Returns:
            List of step strings.
        """
        steps = [
            f"d1={data['d1_cm']}cm, d2={data['d2_cm']}cm",
            f"A1={_f(data['A1'])}m^2, A2={_f(data['A2'])}m^2",
        ]
        target = data["target"]
        q = data["Q"]
        if target == "v2":
            steps.append(f"v2 = A1*v1/A2 = {_f(q)}/{_f(data['A2'])}")
        elif target == "v1":
            steps.append(f"v1 = A2*v2/A1 = {_f(q)}/{_f(data['A1'])}")
        elif target == "A2":
            steps.append(f"A2 = A1*v1/v2 = {_f(q)}/{_f(data['v2'])}")
        else:
            steps.append(f"A1 = A2*v2/v1 = {_f(q)}/{_f(data['v1'])}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the solved quantity.

        Args:
            data: Solution data.

        Returns:
            String representation of the target with units.
        """
        target = data["target"]
        val = data[target]
        if target in ("v1", "v2"):
            return f"{target} = {_f(val)} m/s"
        return f"{target} = {_f(val)} m^2"


# ===================================================================
# 4. Drag force  (tier 5)
# ===================================================================

@register
class DragForceGenerator(StepGenerator):
    """Drag force: Fd = 0.5 * Cd * rho * A * v^2.

    Computes the aerodynamic drag force on an object given
    drag coefficient, fluid density, cross-sectional area, and
    velocity.

    Difficulty scaling:
        Difficulty 1-3: sphere (Cd=0.47), standard air, low speed.
        Difficulty 4-6: varied shapes, higher velocities.
        Difficulty 7-8: solve for velocity given drag force.

    Prerequisites:
        multiplication.
    """

    _SHAPES = {
        "sphere": 0.47, "cylinder": 0.82,
        "flat_plate": 1.28, "streamlined": 0.04,
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "drag_force"

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
        return "compute drag force"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate drag force parameters.

        Args:
            difficulty: Controls shape variety and problem variant.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            shape = "sphere"
        else:
            shape = self._rng.choice(list(self._SHAPES.keys()))

        cd = self._SHAPES[shape]
        rho = round(self._rng.uniform(1.2, 1.3), 2)  # air density
        a = round(self._rng.uniform(0.01, 1.0 + difficulty * 0.5), 3)
        v = round(self._rng.uniform(5.0, 20.0 + difficulty * 10), 1)
        fd = round(0.5 * cd * rho * a * v ** 2, 4)

        if difficulty >= 7:
            return "F_d = \\frac{1}{2} C_d \\rho A v^2", {
                "shape": shape, "Cd": cd, "rho": rho,
                "A": a, "v": v, "Fd": fd, "target": "v",
            }

        return "F_d = \\frac{1}{2} C_d \\rho A v^2", {
            "shape": shape, "Cd": cd, "rho": rho,
            "A": a, "v": v, "Fd": fd, "target": "Fd",
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate drag force computation steps.

        Args:
            data: Solution data with drag parameters.

        Returns:
            List of step strings.
        """
        if data["target"] == "Fd":
            v_sq = round(data["v"] ** 2, 4)
            coeff = round(0.5 * data["Cd"] * data["rho"] * data["A"], 4)
            return [
                f"Cd={data['Cd']} ({data['shape']}), rho={data['rho']}, "
                f"A={data['A']}m^2, v={data['v']}m/s",
                f"v^2 = {_f(v_sq)}",
                f"0.5*Cd*rho*A = {_f(coeff)}",
                f"Fd = {_f(coeff)}*{_f(v_sq)}",
            ]
        # solve for v
        coeff = round(0.5 * data["Cd"] * data["rho"] * data["A"], 4)
        return [
            f"Fd={_f(data['Fd'])}N, Cd={data['Cd']}, "
            f"rho={data['rho']}, A={data['A']}m^2",
            f"v^2 = 2*Fd/(Cd*rho*A) = {_f(data['Fd'])}/{_f(coeff)}",
            f"v = sqrt(v^2)",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the drag force or velocity.

        Args:
            data: Solution data.

        Returns:
            String representation of the result with units.
        """
        if data["target"] == "Fd":
            return f"F_d = {_f(data['Fd'])} N"
        return f"v = {_f(data['v'])} m/s"


# ===================================================================
# 5. Buoyancy  (tier 4)
# ===================================================================

@register
class BuoyancyGenerator(StepGenerator):
    """Archimedes' buoyancy: Fb = rho_fluid * g * V_submerged.

    Computes the buoyant force and compares it with the object's
    weight to determine if the object floats or sinks.

    Difficulty scaling:
        Difficulty 1-3: fully submerged, simple densities.
        Difficulty 4-6: partially submerged (given fraction).
        Difficulty 7-8: compute submerged fraction for floating.

    Prerequisites:
        multiplication.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "buoyancy"

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
        return "compute buoyant force and determine if object floats"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate buoyancy problem parameters.

        Args:
            difficulty: Controls problem complexity.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        rho_fluid = self._rng.choice([1000, 1025, 13600][:min(difficulty, 3)])
        rho_obj = self._rng.randint(200, 1500 + difficulty * 200)
        vol_cm3 = self._rng.randint(10, 100 + difficulty * 50)
        vol = vol_cm3 * 1e-6  # m^3
        mass = round(rho_obj * vol, 4)
        weight = round(mass * _G, 4)

        if difficulty <= 4:
            v_sub = vol
            fraction = 1.0
        else:
            fraction = round(min(1.0, rho_obj / rho_fluid), 4)
            v_sub = round(vol * fraction, 4)

        fb = round(rho_fluid * _G * v_sub, 4)
        floats = fb >= weight

        return "F_b = \\rho_{fluid} g V_{sub}", {
            "rho_fluid": rho_fluid, "rho_obj": rho_obj,
            "vol_cm3": vol_cm3, "V": vol, "V_sub": v_sub,
            "fraction": fraction, "mass": mass,
            "W": weight, "Fb": fb, "floats": floats,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate buoyancy computation steps.

        Args:
            data: Solution data with densities, volumes, forces.

        Returns:
            List of step strings.
        """
        steps = [
            f"rho_fluid={data['rho_fluid']}, rho_obj={data['rho_obj']}, "
            f"V={data['vol_cm3']}cm^3",
            f"W = rho_obj*V*g = {_f(data['W'])} N",
            f"Fb = rho_fluid*g*V_sub = {_f(data['Fb'])} N",
        ]
        if data["floats"]:
            steps.append("Fb >= W => floats")
        else:
            steps.append("Fb < W => sinks")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the buoyant force and float/sink status.

        Args:
            data: Solution data.

        Returns:
            String with Fb and determination.
        """
        status = "floats" if data["floats"] else "sinks"
        return f"F_b = {_f(data['Fb'])} N, {status}"


# ===================================================================
# 6. Hagen-Poiseuille viscous flow  (tier 5)
# ===================================================================

@register
class ViscousFlowGenerator(StepGenerator):
    """Hagen-Poiseuille equation: Q = pi * r^4 * dP / (8 * mu * L).

    Computes the volume flow rate through a cylindrical pipe
    for laminar viscous flow.

    Difficulty scaling:
        Difficulty 1-3: water in standard pipes, integer values.
        Difficulty 4-6: varied fluids, solve for dP or r.
        Difficulty 7-8: compute resistance R = 8*mu*L/(pi*r^4).

    Prerequisites:
        multiplication.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "viscous_flow"

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
        return "compute viscous flow rate using Hagen-Poiseuille"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate pipe flow parameters and compute flow rate.

        Args:
            difficulty: Controls problem complexity.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        r_mm = round(self._rng.uniform(1.0, 5.0 + difficulty), 1)
        r = r_mm * 1e-3
        length = round(self._rng.uniform(0.1, 1.0 + difficulty * 0.5), 2)
        mu = round(self._rng.uniform(0.001, 0.01 + difficulty * 0.01), 4)
        dp = self._rng.randint(100, 1000 + difficulty * 500)

        r4 = r ** 4
        numerator = math.pi * r4 * dp
        denominator = 8 * mu * length
        q = round(numerator / denominator, 4)

        if difficulty >= 6:
            target = self._rng.choice(["Q", "dP"])
        else:
            target = "Q"

        return "Q = \\frac{\\pi r^4 \\Delta P}{8 \\mu L}", {
            "r_mm": r_mm, "r": r, "L": length,
            "mu": mu, "dP": dp, "r4": r4,
            "Q": q, "target": target,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Hagen-Poiseuille computation steps.

        Args:
            data: Solution data with pipe parameters.

        Returns:
            List of step strings.
        """
        if data["target"] == "Q":
            pi_r4 = round(math.pi * data["r4"], 4)
            denom = round(8 * data["mu"] * data["L"], 4)
            return [
                f"r={data['r_mm']}mm, L={data['L']}m, "
                f"mu={data['mu']}Pa*s, dP={data['dP']}Pa",
                f"pi*r^4 = {_f(pi_r4)}",
                f"8*mu*L = {_f(denom)}",
                f"Q = {_f(pi_r4)}*{data['dP']}/{_f(denom)}",
            ]
        # solve for dP
        pi_r4 = round(math.pi * data["r4"], 4)
        denom_q = round(8 * data["mu"] * data["L"], 4)
        return [
            f"r={data['r_mm']}mm, L={data['L']}m, "
            f"mu={data['mu']}Pa*s, Q={_f(data['Q'])}m^3/s",
            f"dP = 8*mu*L*Q/(pi*r^4)",
            f"dP = {_f(denom_q)}*{_f(data['Q'])}/{_f(pi_r4)}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the flow rate or pressure drop.

        Args:
            data: Solution data.

        Returns:
            String representation of the result with units.
        """
        if data["target"] == "Q":
            return f"Q = {_f(data['Q'])} m^3/s"
        return f"\\Delta P = {_f(data['dP'])} Pa"
