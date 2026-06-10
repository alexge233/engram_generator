"""Aerospace engineering generators -- thrust through lift.

Covers rocket thrust equation, Tsiolkovsky rocket equation, orbital
velocity, Hohmann transfer, drag coefficient extraction, and
aerodynamic lift. Tiers range from 5 (introductory orbital mechanics)
to 6 (Hohmann transfer).
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


class _AeroFormatter:
    """Formats numeric values for aerospace engineering problems.

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

    @staticmethod
    def sci(value: float, sig_figs: int = 4) -> str:
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


_f = _AeroFormatter.fmt
_sci = _AeroFormatter.sci

_G_CONST = 6.674e-11  # gravitational constant (N m^2/kg^2)
_M_EARTH = 5.972e24   # mass of Earth (kg)
_GM_EARTH = _G_CONST * _M_EARTH


# ===================================================================
# 1. Thrust equation  (tier 5)
# ===================================================================

@register
class ThrustEquationGenerator(StepGenerator):
    """Compute rocket thrust: F = dm/dt * v_e + (p_e - p_a) * A_e.

    Simplified vacuum form: F = dm/dt * v_e (when p_e = p_a or in vacuum).
    At lower difficulty uses vacuum form; at higher difficulty includes
    the pressure thrust term.

    Difficulty scaling:
        Difficulty 1-3: vacuum thrust only, integer values.
        Difficulty 4-6: include pressure term, decimal values.
        Difficulty 7-8: solve for v_e or dm/dt given thrust.

    Prerequisites:
        multiplication.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "thrust_equation"

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
        return "compute rocket thrust"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate thrust equation parameters and compute force.

        Args:
            difficulty: Controls whether pressure term is included.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        dm_dt = round(self._rng.uniform(50, 500 + difficulty * 100), 1)
        v_e = round(self._rng.uniform(2000, 4500 + difficulty * 200), 1)

        if difficulty <= 3:
            # Vacuum: F = dm/dt * v_e
            thrust = round(dm_dt * v_e, 4)
            return "F = \\dot{m} v_e", {
                "dm_dt": dm_dt, "v_e": v_e,
                "thrust": thrust, "mode": "vacuum",
            }

        # Include pressure term
        p_e = round(self._rng.uniform(50000, 200000), 1)
        p_a = round(self._rng.uniform(0, 101325), 1)
        a_e = round(self._rng.uniform(0.1, 2.0 + difficulty * 0.5), 2)
        momentum_thrust = dm_dt * v_e
        pressure_thrust = (p_e - p_a) * a_e
        thrust = round(momentum_thrust + pressure_thrust, 4)

        if difficulty >= 7:
            return ("F = \\dot{m} v_e + (p_e - p_a) A_e"), {
                "dm_dt": dm_dt, "v_e": v_e,
                "p_e": p_e, "p_a": p_a, "A_e": a_e,
                "momentum_thrust": round(momentum_thrust, 4),
                "pressure_thrust": round(pressure_thrust, 4),
                "thrust": thrust, "mode": "solve_ve",
            }

        return ("F = \\dot{m} v_e + (p_e - p_a) A_e"), {
            "dm_dt": dm_dt, "v_e": v_e,
            "p_e": p_e, "p_a": p_a, "A_e": a_e,
            "momentum_thrust": round(momentum_thrust, 4),
            "pressure_thrust": round(pressure_thrust, 4),
            "thrust": thrust, "mode": "full",
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate thrust computation steps.

        Args:
            data: Solution data with mass flow, exhaust velocity, pressures.

        Returns:
            List of step strings.
        """
        if data["mode"] == "vacuum":
            return [
                f"dm/dt={_f(data['dm_dt'])}kg/s, v_e={_f(data['v_e'])}m/s",
                f"F = {_f(data['dm_dt'])}*{_f(data['v_e'])}",
            ]
        steps = [
            f"dm/dt={_f(data['dm_dt'])}kg/s, v_e={_f(data['v_e'])}m/s",
            f"p_e={_f(data['p_e'])}Pa, p_a={_f(data['p_a'])}Pa, "
            f"A_e={data['A_e']}m^2",
            f"momentum = {_f(data['momentum_thrust'])} N",
            f"pressure = {_f(data['pressure_thrust'])} N",
        ]
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the thrust force.

        Args:
            data: Solution data.

        Returns:
            String with F in Newtons.
        """
        return f"F = {_f(data['thrust'])} N"


# ===================================================================
# 2. Tsiolkovsky rocket equation  (tier 5)
# ===================================================================

@register
class TsiolkovskyGenerator(StepGenerator):
    """Compute delta-v using Tsiolkovsky equation: dv = v_e * ln(m_0/m_f).

    Given exhaust velocity v_e, initial mass m_0, and final mass m_f,
    computes the achievable velocity change. At higher difficulty,
    solves for mass ratio given required delta-v.

    Difficulty scaling:
        Difficulty 1-3: simple mass ratios (integer), compute dv.
        Difficulty 4-6: realistic mass ratios, decimal v_e.
        Difficulty 7-8: given dv, find mass ratio m_0/m_f.

    Prerequisites:
        logarithm.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "tsiolkovsky"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["logarithm"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute delta-v using Tsiolkovsky equation"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate rocket mass and velocity parameters.

        Args:
            difficulty: Controls problem complexity.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        v_e = round(self._rng.uniform(2000, 4500 + difficulty * 200), 1)

        if difficulty <= 3:
            mass_ratio = self._rng.randint(2, 6)
            m_0 = float(mass_ratio * self._rng.randint(100, 500))
            m_f = m_0 / mass_ratio
        else:
            m_0 = round(self._rng.uniform(5000, 50000 + difficulty * 5000), 1)
            m_f = round(self._rng.uniform(500, m_0 * 0.4), 1)
            mass_ratio = m_0 / m_f

        ln_ratio = round(math.log(mass_ratio), 4)
        dv = round(v_e * ln_ratio, 4)

        if difficulty >= 7:
            return "\\frac{m_0}{m_f} = e^{\\Delta v / v_e}", {
                "v_e": v_e, "m_0": m_0, "m_f": m_f,
                "mass_ratio": round(mass_ratio, 4),
                "ln_ratio": ln_ratio, "dv": dv, "target": "ratio",
            }

        return "\\Delta v = v_e \\ln\\frac{m_0}{m_f}", {
            "v_e": v_e, "m_0": m_0, "m_f": m_f,
            "mass_ratio": round(mass_ratio, 4),
            "ln_ratio": ln_ratio, "dv": dv, "target": "dv",
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Tsiolkovsky equation steps.

        Args:
            data: Solution data with v_e, masses, and delta-v.

        Returns:
            List of step strings.
        """
        if data["target"] == "dv":
            return [
                f"v_e={_f(data['v_e'])}m/s, m_0={_f(data['m_0'])}kg, "
                f"m_f={_f(data['m_f'])}kg",
                f"m_0/m_f = {_f(data['mass_ratio'])}",
                f"ln({_f(data['mass_ratio'])}) = {_f(data['ln_ratio'])}",
                f"dv = {_f(data['v_e'])}*{_f(data['ln_ratio'])}",
            ]
        return [
            f"dv={_f(data['dv'])}m/s, v_e={_f(data['v_e'])}m/s",
            f"dv/v_e = {_f(data['ln_ratio'])}",
            f"m_0/m_f = e^{{{_f(data['ln_ratio'])}}}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return delta-v or mass ratio.

        Args:
            data: Solution data.

        Returns:
            String with result and units.
        """
        if data["target"] == "dv":
            return f"dv = {_f(data['dv'])} m/s"
        return f"m_0/m_f = {_f(data['mass_ratio'])}"


# ===================================================================
# 3. Orbital velocity  (tier 5)
# ===================================================================

@register
class OrbitalVelocityGenerator(StepGenerator):
    """Compute circular orbital velocity: v = sqrt(GM/r).

    Given gravitational parameter GM and orbit radius r,
    computes the velocity for a circular orbit. Compares with
    escape velocity v_esc = sqrt(2) * v_orbital.

    Difficulty scaling:
        Difficulty 1-3: LEO orbits around Earth, compute v only.
        Difficulty 4-6: varied orbit radii, compare with v_esc.
        Difficulty 7-8: compute orbit radius for given velocity.

    Prerequisites:
        escape_velocity.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "orbital_velocity"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["escape_velocity"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute orbital velocity"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate orbital parameters and compute velocity.

        Args:
            difficulty: Controls orbit type and problem variant.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            # LEO: 200-2000 km altitude
            alt_km = self._rng.randint(200, 2000)
            r = (6371 + alt_km) * 1e3  # m
            gm = _GM_EARTH
        elif difficulty <= 6:
            alt_km = self._rng.randint(200, 36000)
            r = (6371 + alt_km) * 1e3
            gm = _GM_EARTH
        else:
            # Arbitrary body
            m_kg = float(self._rng.randint(1, 9)) * 1e24
            gm = _G_CONST * m_kg
            r = float(self._rng.randint(3, 20)) * 1e6

        v_orb = round(math.sqrt(gm / r), 4)
        v_esc = round(math.sqrt(2 * gm / r), 4)

        if difficulty >= 7:
            return "r = \\frac{GM}{v^2}", {
                "GM": gm, "r": r,
                "v_orb": v_orb, "v_esc": v_esc,
                "target": "r",
            }

        return "v = \\sqrt{\\frac{GM}{r}}", {
            "GM": gm, "r": r,
            "v_orb": v_orb, "v_esc": v_esc,
            "compare": difficulty >= 4,
            "target": "v",
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate orbital velocity computation steps.

        Args:
            data: Solution data with GM, r, velocities.

        Returns:
            List of step strings.
        """
        steps = [
            f"GM = {_sci(data['GM'])}",
            f"r = {_sci(data['r'])} m",
        ]
        if data["target"] == "v":
            gm_over_r = data["GM"] / data["r"]
            steps.append(f"GM/r = {_sci(gm_over_r)}")
            steps.append(f"v = sqrt(GM/r)")
            if data.get("compare"):
                steps.append(
                    f"v_esc = sqrt(2)*v = {_f(data['v_esc'])} m/s"
                )
        else:
            steps.append(f"r = GM/v^2")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the orbital velocity or radius.

        Args:
            data: Solution data.

        Returns:
            String with result and units.
        """
        if data["target"] == "v":
            return f"v_orb = {_f(data['v_orb'])} m/s"
        return f"r = {_sci(data['r'])} m"


# ===================================================================
# 4. Hohmann transfer  (tier 6)
# ===================================================================

@register
class HohmannTransferGenerator(StepGenerator):
    """Compute Hohmann transfer delta-v between two circular orbits.

    dv1 = sqrt(GM/r1) * (sqrt(2*r2/(r1+r2)) - 1),
    dv2 = sqrt(GM/r2) * (1 - sqrt(2*r1/(r1+r2))).
    Total dv = |dv1| + |dv2|.

    Difficulty scaling:
        Difficulty 1-3: LEO to MEO, simple radii.
        Difficulty 4-6: LEO to GEO or beyond.
        Difficulty 7-8: arbitrary body, compute transfer time too.

    Prerequisites:
        orbital_velocity.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "hohmann_transfer"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["orbital_velocity"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute Hohmann transfer delta-v"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate two orbit radii and compute Hohmann transfer burns.

        Args:
            difficulty: Controls orbit selections.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            alt1_km = self._rng.randint(200, 500)
            alt2_km = self._rng.randint(2000, 10000)
        elif difficulty <= 6:
            alt1_km = self._rng.randint(200, 500)
            alt2_km = self._rng.randint(10000, 42164)
        else:
            alt1_km = self._rng.randint(200, 2000)
            alt2_km = self._rng.randint(20000, 100000)

        r1 = (6371 + alt1_km) * 1e3
        r2 = (6371 + alt2_km) * 1e3
        gm = _GM_EARTH

        v1_circ = math.sqrt(gm / r1)
        v2_circ = math.sqrt(gm / r2)

        ratio = 2 * r2 / (r1 + r2)
        dv1 = round(v1_circ * (math.sqrt(ratio) - 1), 4)

        ratio2 = 2 * r1 / (r1 + r2)
        dv2 = round(v2_circ * (1 - math.sqrt(ratio2)), 4)

        dv_total = round(abs(dv1) + abs(dv2), 4)

        # Transfer semi-major axis and period
        a_transfer = (r1 + r2) / 2
        t_transfer = round(
            math.pi * math.sqrt(a_transfer ** 3 / gm), 4
        )

        return ("\\Delta v_1 = \\sqrt{\\frac{GM}{r_1}}"
                "\\left(\\sqrt{\\frac{2r_2}{r_1+r_2}} - 1\\right)"), {
            "r1": r1, "r2": r2, "GM": gm,
            "v1_circ": round(v1_circ, 4),
            "v2_circ": round(v2_circ, 4),
            "dv1": dv1, "dv2": dv2, "dv_total": dv_total,
            "t_transfer": t_transfer,
            "show_time": difficulty >= 7,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Hohmann transfer computation steps.

        Args:
            data: Solution data with orbit radii and delta-v values.

        Returns:
            List of step strings.
        """
        steps = [
            f"r1={_sci(data['r1'])}m, r2={_sci(data['r2'])}m",
            f"v1_circ = {_f(data['v1_circ'])} m/s",
            f"dv1 = {_f(data['dv1'])} m/s",
            f"dv2 = {_f(data['dv2'])} m/s",
        ]
        if data["show_time"]:
            steps.append(f"T_transfer = {_f(data['t_transfer'])} s")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the total delta-v.

        Args:
            data: Solution data.

        Returns:
            String with total delta-v in m/s.
        """
        return f"dv_total = {_f(data['dv_total'])} m/s"


# ===================================================================
# 5. Drag coefficient  (tier 5)
# ===================================================================

@register
class DragCoefficientGenerator(StepGenerator):
    """Extract drag coefficient from drag equation: Cd = 2*Fd/(rho*A*v^2).

    Given drag force Fd, fluid density rho, reference area A, and
    velocity v, solves for the drag coefficient Cd.

    Difficulty scaling:
        Difficulty 1-3: standard air density, known force and v.
        Difficulty 4-6: varied fluid densities (air, water).
        Difficulty 7-8: given Cd and Fd, solve for velocity.

    Prerequisites:
        drag_force.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "drag_coefficient"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["drag_force"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "extract drag coefficient from measurements"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate drag measurements and extract Cd.

        Args:
            difficulty: Controls fluid type and problem variant.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            rho = 1.225  # air at sea level
            fluid = "air"
        elif difficulty <= 5:
            rho = self._rng.choice([1.225, 1.0, 1000.0])
            fluid = "air" if rho < 2 else "water"
        else:
            rho = round(self._rng.uniform(1.0, 1025.0), 2)
            fluid = "fluid"

        a = round(self._rng.uniform(0.1, 3.0 + difficulty * 0.5), 2)
        v = round(self._rng.uniform(5.0, 50.0 + difficulty * 10), 1)
        cd = round(self._rng.uniform(0.05, 1.5), 3)
        fd = round(0.5 * cd * rho * a * v ** 2, 4)

        denom = round(0.5 * rho * a * v ** 2, 4)

        if difficulty >= 7:
            return "v = \\sqrt{\\frac{2 F_d}{C_d \\rho A}}", {
                "Cd": cd, "rho": rho, "A": a, "v": v,
                "Fd": fd, "denom": denom,
                "fluid": fluid, "target": "v",
            }

        return "C_d = \\frac{2 F_d}{\\rho A v^2}", {
            "Cd": cd, "rho": rho, "A": a, "v": v,
            "Fd": fd, "denom": denom,
            "fluid": fluid, "target": "Cd",
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate drag coefficient extraction steps.

        Args:
            data: Solution data with Fd, rho, A, v.

        Returns:
            List of step strings.
        """
        v_sq = round(data["v"] ** 2, 4)
        if data["target"] == "Cd":
            return [
                f"Fd={_f(data['Fd'])}N, rho={data['rho']}kg/m^3 ({data['fluid']})",
                f"A={data['A']}m^2, v={data['v']}m/s",
                f"v^2 = {_f(v_sq)}",
                f"0.5*rho*A*v^2 = {_f(data['denom'])}",
                f"Cd = 2*Fd / (rho*A*v^2)",
            ]
        return [
            f"Fd={_f(data['Fd'])}N, Cd={data['Cd']}, "
            f"rho={data['rho']}kg/m^3",
            f"A={data['A']}m^2",
            f"v^2 = 2*Fd/(Cd*rho*A)",
            f"v = sqrt(v^2)",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the drag coefficient or velocity.

        Args:
            data: Solution data.

        Returns:
            String with Cd or v.
        """
        if data["target"] == "Cd":
            return f"C_d = {_f(data['Cd'])}"
        return f"v = {_f(data['v'])} m/s"


# ===================================================================
# 6. Lift equation  (tier 5)
# ===================================================================

@register
class LiftEquationGenerator(StepGenerator):
    """Compute aerodynamic lift: L = 0.5 * rho * v^2 * S * C_L.

    At high difficulty, solves for required velocity in level flight
    where lift equals weight (L = W).

    Difficulty scaling:
        Difficulty 1-3: compute lift directly, simple inputs.
        Difficulty 4-6: varied aircraft parameters.
        Difficulty 7-8: find v for level flight (L = W = mg).

    Prerequisites:
        multiplication.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "lift_equation"

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
        if difficulty >= 7:
            return "find velocity for level flight"
        return "compute aerodynamic lift"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate lift equation parameters and compute result.

        Args:
            difficulty: Controls problem variant.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        rho = round(self._rng.uniform(0.9, 1.225), 3)
        s = round(self._rng.uniform(10, 100 + difficulty * 20), 1)
        cl = round(self._rng.uniform(0.3, 1.8), 2)
        v = round(self._rng.uniform(30, 100 + difficulty * 30), 1)

        lift = round(0.5 * rho * v ** 2 * s * cl, 4)

        if difficulty >= 7:
            mass = round(self._rng.uniform(1000, 50000 + difficulty * 5000), 1)
            weight = round(mass * 9.81, 4)
            # v for L = W
            v_level = round(
                math.sqrt(2 * weight / (rho * s * cl)), 4
            )
            return "v = \\sqrt{\\frac{2W}{\\rho S C_L}}", {
                "rho": rho, "S": s, "C_L": cl,
                "mass": mass, "W": weight,
                "v_level": v_level,
                "target": "v",
            }

        return "L = \\frac{1}{2} \\rho v^2 S C_L", {
            "rho": rho, "v": v, "S": s, "C_L": cl,
            "L": lift, "target": "L",
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate lift equation computation steps.

        Args:
            data: Solution data with rho, v, S, C_L.

        Returns:
            List of step strings.
        """
        if data["target"] == "L":
            v_sq = round(data["v"] ** 2, 4)
            coeff = round(0.5 * data["rho"] * data["S"] * data["C_L"], 4)
            return [
                f"rho={data['rho']}kg/m^3, v={data['v']}m/s",
                f"S={data['S']}m^2, C_L={data['C_L']}",
                f"v^2 = {_f(v_sq)}",
                f"0.5*rho*S*C_L = {_f(coeff)}",
            ]
        # solve for v in level flight
        return [
            f"W = {_f(data['mass'])}*9.81 = {_f(data['W'])} N",
            f"rho={data['rho']}, S={data['S']}m^2, C_L={data['C_L']}",
            f"v^2 = 2W/(rho*S*C_L)",
            f"v = sqrt(v^2)",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the lift force or velocity.

        Args:
            data: Solution data.

        Returns:
            String with L or v and units.
        """
        if data["target"] == "L":
            return f"L = {_f(data['L'])} N"
        return f"v = {_f(data['v_level'])} m/s"
