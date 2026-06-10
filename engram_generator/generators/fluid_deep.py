"""Deep fluid mechanics generators -- compressible flow, turbulence, and waves.

Extends the fluid mechanics domain with Mach number classification,
isentropic flow relations, normal shock waves, boundary layers,
orifice flow, water hammer, Froude number, and weir flow.
Tiers range from 4 to 6.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register

_G = 9.81  # gravitational acceleration (m/s^2)


class _FluidDeepFormatter:
    """Formats numeric values for deep fluid mechanics problems.

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


_f = _FluidDeepFormatter.fmt


# ===================================================================
# 1. Mach number  (tier 5)
# ===================================================================

@register
class MachNumberGenerator(StepGenerator):
    """Compute Mach number and classify flow regime.

    M = v / a where a = sqrt(gamma * R * T / M_mol). Classify as
    subsonic (M<0.8), transonic (0.8-1.2), supersonic (1.2-5),
    or hypersonic (M>5).

    Difficulty scaling:
        Difficulty 1-3: air at standard conditions, integer velocity.
        Difficulty 4-6: variable temperature, compute a first.
        Difficulty 7-8: given M and T, find required velocity.

    Prerequisites:
        square_root.
    """

    _GAMMA_AIR = 1.4
    _R_SPECIFIC_AIR = 287.05  # J/(kg*K)

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "mach_number"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["square_root"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute Mach number and classify flow regime"

    def _classify(self, m: float) -> str:
        """Classify flow regime from Mach number.

        Args:
            m: Mach number.

        Returns:
            Flow regime label.
        """
        if m < 0.8:
            return "subsonic"
        if m < 1.2:
            return "transonic"
        if m < 5.0:
            return "supersonic"
        return "hypersonic"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate velocity and temperature, compute Mach number.

        Args:
            difficulty: Controls problem variant.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            t = 288  # standard atmosphere
            v = self._rng.randint(50, 400)
        elif difficulty <= 6:
            t = self._rng.randint(200, 400)
            v = self._rng.randint(100, 2000)
        else:
            t = self._rng.randint(200, 350)
            target_m = round(self._rng.uniform(0.3, 6.0), 1)
            a = math.sqrt(self._GAMMA_AIR * self._R_SPECIFIC_AIR * t)
            v = round(target_m * a, 4)
            a_val = round(a, 4)
            m = round(v / a, 4)
            regime = self._classify(m)
            return "v = M * a", {
                "T": t, "a": a_val, "v": v, "M": m,
                "regime": regime, "mode": "find_v",
            }

        a = round(math.sqrt(self._GAMMA_AIR * self._R_SPECIFIC_AIR * t), 4)
        m = round(v / a, 4)
        regime = self._classify(m)
        return "M = v/a, a = sqrt(gamma*R*T)", {
            "T": t, "a": a, "v": v, "M": m,
            "regime": regime, "mode": "compute",
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Mach number computation steps.

        Args:
            data: Solution data.

        Returns:
            List of step strings.
        """
        steps = [f"T={data['T']}K, gamma=1.4, R=287.05 J/(kg*K)"]
        steps.append(f"a = sqrt(1.4*287.05*{data['T']}) = {_f(data['a'])} m/s")
        if data["mode"] == "compute":
            steps.append(f"M = {data['v']}/{_f(data['a'])} = {_f(data['M'])}")
        else:
            steps.append(f"v = {_f(data['M'])}*{_f(data['a'])} = {_f(data['v'])} m/s")
        steps.append(f"Regime: {data['regime']}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the Mach number and flow regime.

        Args:
            data: Solution data.

        Returns:
            Result string.
        """
        if data["mode"] == "find_v":
            return f"v = {_f(data['v'])} m/s, {data['regime']}"
        return f"M = {_f(data['M'])}, {data['regime']}"


# ===================================================================
# 2. Isentropic flow  (tier 6)
# ===================================================================

@register
class IsentropicFlowGenerator(StepGenerator):
    """Compute isentropic flow relations for compressible gas.

    T/T_0 = (1 + (gamma-1)/2 * M^2)^(-1).
    P/P_0 = (T/T_0)^(gamma/(gamma-1)).
    rho/rho_0 = (T/T_0)^(1/(gamma-1)).

    Difficulty scaling:
        Difficulty 1-3: compute T/T_0 from M.
        Difficulty 4-6: compute T/T_0 and P/P_0.
        Difficulty 7-8: compute all ratios and find M from T/T_0.

    Prerequisites:
        exponentiation.
    """

    _GAMMA = 1.4

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "isentropic_flow"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

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
        return "compute isentropic flow temperature and pressure ratios"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate Mach number and compute isentropic ratios.

        Args:
            difficulty: Controls which ratios to compute.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        g = self._GAMMA
        m = round(self._rng.uniform(0.3, 3.0 + difficulty * 0.3), 2)

        t_ratio = round((1 + (g - 1) / 2 * m ** 2) ** (-1), 4)
        p_ratio = round(t_ratio ** (g / (g - 1)), 4)
        rho_ratio = round(t_ratio ** (1 / (g - 1)), 4)

        if difficulty <= 3:
            return "T/T_0 = (1+(g-1)/2*M^2)^{-1}", {
                "M": m, "T_ratio": t_ratio,
                "P_ratio": p_ratio, "rho_ratio": rho_ratio,
                "mode": "T_only",
            }
        if difficulty <= 6:
            return "T/T_0, P/P_0 isentropic relations", {
                "M": m, "T_ratio": t_ratio,
                "P_ratio": p_ratio, "rho_ratio": rho_ratio,
                "mode": "TP",
            }
        # Find M from T/T_0
        t_ratio_given = round(self._rng.uniform(0.3, 0.95), 2)
        m_found = round(
            math.sqrt(2 / (g - 1) * (1 / t_ratio_given - 1)), 4
        )
        p_ratio_found = round(t_ratio_given ** (g / (g - 1)), 4)
        return "M from T/T_0", {
            "T_ratio_given": t_ratio_given, "M_found": m_found,
            "P_ratio_found": p_ratio_found,
            "mode": "find_M",
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate isentropic flow computation steps.

        Args:
            data: Solution data.

        Returns:
            List of step strings.
        """
        if data["mode"] in ("T_only", "TP"):
            steps = [
                f"M = {data['M']}, gamma = 1.4",
                f"T/T_0 = (1+0.2*{data['M']}^2)^(-1) = {_f(data['T_ratio'])}",
            ]
            if data["mode"] == "TP":
                steps.append(f"P/P_0 = (T/T_0)^3.5 = {_f(data['P_ratio'])}")
            return steps
        return [
            f"T/T_0 = {data['T_ratio_given']}",
            f"M = sqrt(5*(1/{data['T_ratio_given']}-1))"
            f" = {_f(data['M_found'])}",
            f"P/P_0 = {data['T_ratio_given']}^3.5"
            f" = {_f(data['P_ratio_found'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the isentropic ratios or Mach number.

        Args:
            data: Solution data.

        Returns:
            Result string.
        """
        if data["mode"] == "T_only":
            return f"T/T_0 = {_f(data['T_ratio'])}"
        if data["mode"] == "TP":
            return (
                f"T/T_0 = {_f(data['T_ratio'])}, "
                f"P/P_0 = {_f(data['P_ratio'])}"
            )
        return (
            f"M = {_f(data['M_found'])}, "
            f"P/P_0 = {_f(data['P_ratio_found'])}"
        )


# ===================================================================
# 3. Normal shock  (tier 6)
# ===================================================================

@register
class NormalShockGenerator(StepGenerator):
    """Compute post-shock Mach number across a normal shock.

    M_2^2 = (1 + (gamma-1)/2 * M_1^2) / (gamma * M_1^2 - (gamma-1)/2).
    Also compute pressure and temperature ratios across the shock.

    Difficulty scaling:
        Difficulty 1-3: compute M_2 from M_1, gamma = 1.4.
        Difficulty 4-6: compute M_2 and pressure ratio P2/P1.
        Difficulty 7-8: compute all ratios (M2, P2/P1, T2/T1, rho2/rho1).

    Prerequisites:
        division.
    """

    _GAMMA = 1.4

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "normal_shock"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

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
        return "compute post-shock conditions across normal shock"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate pre-shock Mach and compute post-shock conditions.

        Args:
            difficulty: Controls which quantities to compute.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        g = self._GAMMA
        m1 = round(self._rng.uniform(1.1, 4.0 + difficulty * 0.5), 2)

        m2_sq = (1 + (g - 1) / 2 * m1 ** 2) / (g * m1 ** 2 - (g - 1) / 2)
        m2 = round(math.sqrt(m2_sq), 4)

        # Pressure ratio
        p_ratio = round(1 + 2 * g / (g + 1) * (m1 ** 2 - 1), 4)

        # Temperature ratio
        t_ratio = round(
            p_ratio * (2 + (g - 1) * m1 ** 2) / ((g + 1) * m1 ** 2), 4
        )

        # Density ratio
        rho_ratio = round((g + 1) * m1 ** 2 / (2 + (g - 1) * m1 ** 2), 4)

        if difficulty <= 3:
            return "M_2^2 = (1+(g-1)/2*M_1^2)/(g*M_1^2-(g-1)/2)", {
                "M1": m1, "M2": m2, "mode": "M2_only",
            }
        if difficulty <= 6:
            return "Normal shock relations", {
                "M1": m1, "M2": m2, "P_ratio": p_ratio,
                "mode": "M2_P",
            }
        return "Normal shock relations", {
            "M1": m1, "M2": m2, "P_ratio": p_ratio,
            "T_ratio": t_ratio, "rho_ratio": rho_ratio,
            "mode": "full",
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate normal shock computation steps.

        Args:
            data: Solution data.

        Returns:
            List of step strings.
        """
        steps = [
            f"M_1 = {data['M1']}, gamma = 1.4",
            f"M_2^2 = (1+0.2*{data['M1']}^2)/(1.4*{data['M1']}^2-0.2)",
            f"M_2 = {_f(data['M2'])}",
        ]
        if data["mode"] in ("M2_P", "full"):
            steps.append(f"P2/P1 = 1+2.333*(M1^2-1) = {_f(data['P_ratio'])}")
        if data["mode"] == "full":
            steps.append(f"T2/T1 = {_f(data['T_ratio'])}")
            steps.append(f"rho2/rho1 = {_f(data['rho_ratio'])}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return post-shock quantities.

        Args:
            data: Solution data.

        Returns:
            Result string.
        """
        if data["mode"] == "M2_only":
            return f"M_2 = {_f(data['M2'])}"
        if data["mode"] == "M2_P":
            return (
                f"M_2 = {_f(data['M2'])}, "
                f"P2/P1 = {_f(data['P_ratio'])}"
            )
        return (
            f"M_2 = {_f(data['M2'])}, P2/P1 = {_f(data['P_ratio'])}, "
            f"T2/T1 = {_f(data['T_ratio'])}"
        )


# ===================================================================
# 4. Boundary layer  (tier 5)
# ===================================================================

@register
class BoundaryLayerGenerator(StepGenerator):
    """Compute Blasius boundary layer thickness for flat plate.

    delta ~ 5x / sqrt(Re_x). Displacement thickness
    delta* = 1.72x / sqrt(Re_x). Re_x = rho * U * x / mu.

    Difficulty scaling:
        Difficulty 1-3: compute Re_x and delta at given x.
        Difficulty 4-6: compute delta and delta*.
        Difficulty 7-8: find x where delta reaches given thickness.

    Prerequisites:
        square_root.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "boundary_layer"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["square_root"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute Blasius boundary layer thickness"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate flat plate flow parameters and compute BL thickness.

        Args:
            difficulty: Controls problem variant.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        rho = round(self._rng.uniform(1.0, 1.3), 2)  # kg/m^3 (air)
        u = round(self._rng.uniform(5.0, 50.0), 1)     # m/s
        mu = 1.81e-5  # Pa*s (air at ~20C)
        x = round(self._rng.uniform(0.1, 2.0), 2)       # m

        re_x = round(rho * u * x / mu, 4)
        sqrt_re = math.sqrt(re_x)
        delta = round(5 * x / sqrt_re, 4)
        delta_star = round(1.72 * x / sqrt_re, 4)

        if difficulty <= 3:
            return "delta = 5x/sqrt(Re_x)", {
                "rho": rho, "U": u, "mu": mu, "x": x,
                "Re_x": re_x, "delta": delta,
                "delta_star": delta_star, "mode": "delta",
            }
        if difficulty <= 6:
            return "delta = 5x/sqrt(Re_x), delta* = 1.72x/sqrt(Re_x)", {
                "rho": rho, "U": u, "mu": mu, "x": x,
                "Re_x": re_x, "delta": delta,
                "delta_star": delta_star, "mode": "both",
            }
        # Find x for target delta
        target_mm = round(self._rng.uniform(1.0, 10.0), 1)
        target = target_mm * 1e-3
        # delta = 5x/sqrt(rho*U*x/mu) = 5*sqrt(mu*x/(rho*U))
        # => x = (delta/5)^2 * rho*U/mu
        x_needed = round((target / 5) ** 2 * rho * u / mu, 4)
        return "x for target delta", {
            "rho": rho, "U": u, "mu": mu,
            "target_mm": target_mm, "x_needed": x_needed,
            "mode": "find_x",
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate boundary layer computation steps.

        Args:
            data: Solution data.

        Returns:
            List of step strings.
        """
        if data["mode"] in ("delta", "both"):
            steps = [
                f"rho={data['rho']}kg/m^3, U={data['U']}m/s, x={data['x']}m",
                f"Re_x = rho*U*x/mu = {_f(data['Re_x'])}",
                f"delta = 5*{data['x']}/sqrt({_f(data['Re_x'])}) = {_f(data['delta'])} m",
            ]
            if data["mode"] == "both":
                steps.append(f"delta* = 1.72*{data['x']}/sqrt(Re_x) = {_f(data['delta_star'])} m")
            return steps
        return [
            f"rho={data['rho']}kg/m^3, U={data['U']}m/s",
            f"target delta = {data['target_mm']}mm",
            f"x = (delta/5)^2 * rho*U/mu",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return boundary layer thickness or position.

        Args:
            data: Solution data.

        Returns:
            Result string with units.
        """
        if data["mode"] == "delta":
            return f"delta = {_f(data['delta'])} m"
        if data["mode"] == "both":
            return (
                f"delta = {_f(data['delta'])} m, "
                f"delta* = {_f(data['delta_star'])} m"
            )
        return f"x = {_f(data['x_needed'])} m"


# ===================================================================
# 5. Orifice flow  (tier 4)
# ===================================================================

@register
class OrificeFlowGenerator(StepGenerator):
    """Compute volumetric flow rate through an orifice plate.

    Q = C_d * A * sqrt(2 * dP / rho) where C_d is the discharge
    coefficient, A is the orifice area, dP is the pressure drop,
    and rho is the fluid density.

    Difficulty scaling:
        Difficulty 1-3: given all parameters, compute Q directly.
        Difficulty 4-6: compute A from orifice diameter, then Q.
        Difficulty 7-8: given Q, find required orifice diameter.

    Prerequisites:
        square_root.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "orifice_flow"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["square_root"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute flow rate through orifice plate"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate orifice parameters and compute flow rate.

        Args:
            difficulty: Controls problem variant.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        cd = round(self._rng.uniform(0.6, 0.65), 2)
        rho = round(self._rng.uniform(900, 1100), 1)  # kg/m^3 (liquid)
        dp_kpa = self._rng.randint(10, 200)
        dp = dp_kpa * 1e3  # Pa

        if difficulty <= 3:
            a_cm2 = self._rng.randint(1, 20)
            a = a_cm2 * 1e-4
            q = round(cd * a * math.sqrt(2 * dp / rho), 4)
            return "Q = C_d*A*sqrt(2*dP/rho)", {
                "C_d": cd, "A_cm2": a_cm2, "A": a,
                "dP_kPa": dp_kpa, "rho": rho,
                "Q": q, "mode": "compute",
            }
        if difficulty <= 6:
            d_mm = self._rng.randint(10, 100)
            d = d_mm * 1e-3
            a = round(math.pi * (d / 2) ** 2, 4)
            q = round(cd * a * math.sqrt(2 * dp / rho), 4)
            return "Q = C_d*A*sqrt(2*dP/rho)", {
                "C_d": cd, "d_mm": d_mm, "A": a,
                "dP_kPa": dp_kpa, "rho": rho,
                "Q": q, "mode": "from_d",
            }
        # Find d for target Q
        q_target = round(self._rng.uniform(0.001, 0.1), 4)
        a_needed = q_target / (cd * math.sqrt(2 * dp / rho))
        d_needed = round(2 * math.sqrt(a_needed / math.pi), 4)
        d_needed_mm = round(d_needed * 1e3, 4)
        return "d for target Q", {
            "C_d": cd, "dP_kPa": dp_kpa, "rho": rho,
            "Q_target": q_target,
            "d_needed_mm": d_needed_mm, "mode": "find_d",
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate orifice flow computation steps.

        Args:
            data: Solution data.

        Returns:
            List of step strings.
        """
        if data["mode"] == "compute":
            return [
                f"C_d={data['C_d']}, A={data['A_cm2']}cm^2, "
                f"dP={data['dP_kPa']}kPa, rho={data['rho']}kg/m^3",
                f"Q = {data['C_d']}*{_f(data['A'])}*sqrt(2*{data['dP_kPa']}e3/{data['rho']})",
            ]
        if data["mode"] == "from_d":
            return [
                f"d={data['d_mm']}mm, C_d={data['C_d']}",
                f"A = pi*(d/2)^2 = {_f(data['A'])} m^2",
                f"Q = C_d*A*sqrt(2*dP/rho)",
            ]
        return [
            f"Q_target={data['Q_target']} m^3/s, C_d={data['C_d']}",
            f"A = Q/(C_d*sqrt(2*dP/rho))",
            f"d = 2*sqrt(A/pi)",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the flow rate or orifice diameter.

        Args:
            data: Solution data.

        Returns:
            Result string with units.
        """
        if data["mode"] == "find_d":
            return f"d = {_f(data['d_needed_mm'])} mm"
        return f"Q = {_f(data['Q'])} m^3/s"


# ===================================================================
# 6. Water hammer  (tier 5)
# ===================================================================

@register
class WaterHammerGenerator(StepGenerator):
    """Compute pressure surge from water hammer in a pipe.

    Pressure surge: dP = rho * a * dv where a is the wave speed.
    For a rigid pipe: a = sqrt(K / rho) where K is the bulk modulus.

    Difficulty scaling:
        Difficulty 1-3: given a directly, compute dP.
        Difficulty 4-6: compute a from K and rho, then dP.
        Difficulty 7-8: compute force on a pipe section from dP.

    Prerequisites:
        multiplication.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "water_hammer"

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
        return "compute water hammer pressure surge"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate pipe flow parameters and compute pressure surge.

        Args:
            difficulty: Controls problem variant.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        rho = round(self._rng.uniform(990, 1010), 1)
        dv = round(self._rng.uniform(0.5, 5.0), 1)

        if difficulty <= 3:
            a = self._rng.randint(1200, 1500)
            dp = round(rho * a * dv, 4)
            dp_kpa = round(dp / 1e3, 4)
            return "dP = rho*a*dv", {
                "rho": rho, "a": a, "dv": dv,
                "dP": dp, "dP_kPa": dp_kpa, "mode": "simple",
            }
        k_gpa = round(self._rng.uniform(2.0, 2.3), 1)
        k = k_gpa * 1e9
        a = round(math.sqrt(k / rho), 4)
        dp = round(rho * a * dv, 4)
        dp_kpa = round(dp / 1e3, 4)

        if difficulty <= 6:
            return "a = sqrt(K/rho), dP = rho*a*dv", {
                "rho": rho, "K_GPa": k_gpa, "a": a, "dv": dv,
                "dP": dp, "dP_kPa": dp_kpa, "mode": "from_K",
            }
        # Force on pipe section
        d_mm = self._rng.randint(50, 300)
        d = d_mm * 1e-3
        area = round(math.pi * (d / 2) ** 2, 4)
        force = round(dp * area, 4)
        return "F = dP * A_pipe", {
            "rho": rho, "K_GPa": k_gpa, "a": a, "dv": dv,
            "dP": dp, "dP_kPa": dp_kpa,
            "d_mm": d_mm, "A_pipe": area, "F": force,
            "mode": "force",
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate water hammer computation steps.

        Args:
            data: Solution data.

        Returns:
            List of step strings.
        """
        steps = [f"rho={data['rho']}kg/m^3, dv={data['dv']}m/s"]
        if data["mode"] == "simple":
            steps.append(f"a={data['a']}m/s (given)")
        else:
            steps.append(f"K={data['K_GPa']}GPa")
            steps.append(f"a = sqrt(K/rho) = {_f(data['a'])} m/s")
        steps.append(f"dP = rho*a*dv = {_f(data['dP_kPa'])} kPa")
        if data["mode"] == "force":
            steps.append(f"d={data['d_mm']}mm, A={_f(data['A_pipe'])} m^2")
            steps.append(f"F = dP*A")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the pressure surge and optionally force.

        Args:
            data: Solution data.

        Returns:
            Result string with units.
        """
        if data["mode"] == "force":
            return (
                f"dP = {_f(data['dP_kPa'])} kPa, "
                f"F = {_f(data['F'])} N"
            )
        return f"dP = {_f(data['dP_kPa'])} kPa"


# ===================================================================
# 7. Froude number  (tier 4)
# ===================================================================

@register
class FroudeNumberGenerator(StepGenerator):
    """Compute Froude number and classify open channel flow.

    Fr = v / sqrt(g * h). Subcritical if Fr < 1, critical if Fr = 1,
    supercritical if Fr > 1.

    Difficulty scaling:
        Difficulty 1-3: integer velocity and depth, classify flow.
        Difficulty 4-6: decimal values, compute Fr and classify.
        Difficulty 7-8: given Fr, find critical depth or velocity.

    Prerequisites:
        square_root.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "froude_number"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["square_root"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute Froude number and classify channel flow"

    def _classify(self, fr: float) -> str:
        """Classify flow regime from Froude number.

        Args:
            fr: Froude number.

        Returns:
            Flow regime label.
        """
        if fr < 0.99:
            return "subcritical"
        if fr <= 1.01:
            return "critical"
        return "supercritical"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate channel flow parameters.

        Args:
            difficulty: Controls problem variant.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            v = self._rng.randint(1, 10)
            h = self._rng.randint(1, 5)
        elif difficulty <= 6:
            v = round(self._rng.uniform(0.5, 8.0), 1)
            h = round(self._rng.uniform(0.5, 5.0), 1)
        else:
            # Find critical depth for given v
            v = round(self._rng.uniform(1.0, 10.0), 1)
            h_c = round(v ** 2 / _G, 4)
            fr = 1.0
            return "h_c = v^2/g (critical depth)", {
                "v": v, "h_c": h_c, "Fr": fr,
                "regime": "critical", "mode": "find_hc",
            }

        fr = round(v / math.sqrt(_G * h), 4)
        regime = self._classify(fr)
        return "Fr = v/sqrt(g*h)", {
            "v": v, "h": h, "Fr": fr,
            "regime": regime, "mode": "compute",
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Froude number computation steps.

        Args:
            data: Solution data.

        Returns:
            List of step strings.
        """
        if data["mode"] == "compute":
            return [
                f"v={data['v']}m/s, h={data['h']}m",
                f"Fr = {data['v']}/sqrt({_f(_G)}*{data['h']})"
                f" = {_f(data['Fr'])}",
                f"Regime: {data['regime']}",
            ]
        return [
            f"v={data['v']}m/s, Fr=1 (critical)",
            f"h_c = v^2/g = {data['v']}^2/{_f(_G)}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the Froude number and classification.

        Args:
            data: Solution data.

        Returns:
            Result string.
        """
        if data["mode"] == "find_hc":
            return f"h_c = {_f(data['h_c'])} m"
        return f"Fr = {_f(data['Fr'])}, {data['regime']}"


# ===================================================================
# 8. Weir flow  (tier 4)
# ===================================================================

@register
class WeirFlowGenerator(StepGenerator):
    """Compute flow rate over a weir.

    Rectangular weir: Q = C * L * H^(3/2).
    V-notch weir: Q = C * tan(theta/2) * H^(5/2).

    Difficulty scaling:
        Difficulty 1-3: rectangular weir, integer dimensions.
        Difficulty 4-6: rectangular weir, decimal values.
        Difficulty 7-8: V-notch weir with given angle.

    Prerequisites:
        exponentiation.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "weir_flow"

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
        return "compute flow rate over a weir"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate weir parameters and compute flow rate.

        Args:
            difficulty: Controls weir type and parameter precision.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            c = round(self._rng.uniform(1.7, 1.9), 2)
            l = self._rng.randint(1, 5)
            h = round(self._rng.uniform(0.1, 1.0), 1)
            q = round(c * l * h ** 1.5, 4)
            return "Q = C*L*H^{3/2}", {
                "C": c, "L": l, "H": h, "Q": q,
                "mode": "rect_simple",
            }
        if difficulty <= 6:
            c = round(self._rng.uniform(1.7, 1.9), 2)
            l = round(self._rng.uniform(0.5, 5.0), 1)
            h = round(self._rng.uniform(0.05, 1.5), 2)
            q = round(c * l * h ** 1.5, 4)
            return "Q = C*L*H^{3/2}", {
                "C": c, "L": l, "H": h, "Q": q,
                "mode": "rect",
            }
        # V-notch
        c = round(self._rng.uniform(1.35, 1.45), 2)
        theta_deg = self._rng.choice([60, 90, 120])
        theta_rad = math.radians(theta_deg)
        h = round(self._rng.uniform(0.05, 0.5), 2)
        q = round(c * math.tan(theta_rad / 2) * h ** 2.5, 4)
        return "Q = C*tan(theta/2)*H^{5/2}", {
            "C": c, "theta_deg": theta_deg, "H": h, "Q": q,
            "mode": "vnotch",
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate weir flow computation steps.

        Args:
            data: Solution data.

        Returns:
            List of step strings.
        """
        if data["mode"] in ("rect_simple", "rect"):
            return [
                f"C={data['C']}, L={data['L']}m, H={data['H']}m",
                f"Q = {data['C']}*{data['L']}*{data['H']}^(3/2)",
            ]
        return [
            f"C={data['C']}, theta={data['theta_deg']}deg, H={data['H']}m",
            f"tan(theta/2) = {_f(math.tan(math.radians(data['theta_deg']) / 2))}",
            f"Q = C*tan(theta/2)*H^(5/2)",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the flow rate.

        Args:
            data: Solution data.

        Returns:
            Q as a string with units.
        """
        return f"Q = {_f(data['Q'])} m^3/s"
