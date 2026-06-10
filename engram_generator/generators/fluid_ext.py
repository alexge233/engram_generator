"""Extended fluid mechanics generators -- pipe flow, Venturi, Stokes, hydraulics.

Deepens the fluid mechanics domain with Darcy-Weisbach pipe friction,
Venturi meter flow measurement, Stokes drag and terminal velocity,
hydraulic jumps, Manning's open channel flow, and pump power
calculations. Tiers range from 4 to 5.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


class _FluidExtFormatter:
    """Formats numeric values for extended fluid mechanics problems.

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


_f = _FluidExtFormatter.fmt

_G = 9.81  # gravitational acceleration (m/s^2)


# ===================================================================
# 1. Pipe flow (Darcy-Weisbach)  (tier 5)
# ===================================================================

@register
class PipeFlowGenerator(StepGenerator):
    """Darcy-Weisbach head loss: h_f = f * L * v^2 / (D * 2g).

    Given friction factor f, pipe length L, velocity v, and pipe
    diameter D, computes the friction head loss h_f.

    Difficulty scaling:
        Difficulty 1-3: standard values, compute h_f.
        Difficulty 4-6: wider ranges, also compute pressure drop.
        Difficulty 7-8: solve for maximum velocity given h_f limit.

    Prerequisites:
        bernoulli.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "pipe_flow"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["bernoulli"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute friction head loss using Darcy-Weisbach"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate pipe parameters and compute head loss.

        Args:
            difficulty: Controls ranges and problem variant.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        f_factor = round(self._rng.uniform(0.01, 0.05), 4)
        length = self._rng.randint(10, 100 + difficulty * 50)
        d_cm = self._rng.randint(5, 30 + difficulty * 5)
        d = d_cm / 100.0
        v = round(self._rng.uniform(0.5, 3.0 + difficulty), 2)

        v_sq = round(v ** 2, 4)
        h_f = round(f_factor * length * v_sq / (d * 2 * _G), 4)

        rho = 1000
        dp = round(rho * _G * h_f, 4)

        if difficulty >= 7:
            target = "v_max"
            h_f_limit = self._rng.randint(5, 20)
            v_max = round(math.sqrt(h_f_limit * d * 2 * _G / (f_factor * length)), 4)
            return "h_f = \\frac{f L v^2}{D \\cdot 2g}", {
                "f": f_factor, "L": length, "D_cm": d_cm, "D": d,
                "v": v, "v_sq": v_sq, "h_f": h_f, "dP": dp,
                "h_f_limit": h_f_limit, "v_max": v_max,
                "target": target,
            }

        return "h_f = \\frac{f L v^2}{D \\cdot 2g}", {
            "f": f_factor, "L": length, "D_cm": d_cm, "D": d,
            "v": v, "v_sq": v_sq, "h_f": h_f, "dP": dp,
            "target": "h_f",
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Darcy-Weisbach computation steps.

        Args:
            data: Solution data with pipe parameters.

        Returns:
            List of step strings.
        """
        if data["target"] == "h_f":
            two_gd = round(data["D"] * 2 * _G, 4)
            return [
                f"f={data['f']}, L={data['L']}m, D={data['D_cm']}cm, v={data['v']}m/s",
                f"v^2 = {_f(data['v_sq'])}",
                f"D*2g = {_f(two_gd)}",
                f"h_f = {data['f']}*{data['L']}*{_f(data['v_sq'])}/{_f(two_gd)}",
            ]
        two_gd = round(data["D"] * 2 * _G, 4)
        return [
            f"h_f_max={data['h_f_limit']}m, f={data['f']}, L={data['L']}m, D={data['D_cm']}cm",
            f"v^2 = h_f*D*2g/(f*L) = {data['h_f_limit']}*{_f(two_gd)}/({data['f']}*{data['L']})",
            f"v = sqrt(v^2) = {_f(data['v_max'])} m/s",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the head loss or maximum velocity.

        Args:
            data: Solution data.

        Returns:
            String with result.
        """
        if data["target"] == "h_f":
            return f"h_f = {_f(data['h_f'])} m, dP = {_f(data['dP'])} Pa"
        return f"v_max = {_f(data['v_max'])} m/s"


# ===================================================================
# 2. Venturi meter  (tier 5)
# ===================================================================

@register
class VenturiMeterGenerator(StepGenerator):
    """Venturi meter: Q = A_2 * sqrt(2*g*h / (1 - (A_2/A_1)^2)).

    Computes the volumetric flow rate from the pressure head
    difference h between the wide and narrow sections.

    Difficulty scaling:
        Difficulty 1-3: given areas directly.
        Difficulty 4-6: compute areas from diameters.
        Difficulty 7-8: include discharge coefficient Cd.

    Prerequisites:
        bernoulli.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "venturi_meter"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["bernoulli"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute flow rate using Venturi meter"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate Venturi meter parameters and compute flow rate.

        Args:
            difficulty: Controls input format and Cd.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        d1_cm = self._rng.randint(8, 20 + difficulty * 2)
        d2_cm = self._rng.randint(3, max(4, d1_cm - 3))
        d1 = d1_cm / 100.0
        d2 = d2_cm / 100.0
        a1 = round(math.pi * (d1 / 2) ** 2, 4)
        a2 = round(math.pi * (d2 / 2) ** 2, 4)

        h = round(self._rng.uniform(0.1, 2.0 + difficulty * 0.5), 2)

        ratio_sq = round((a2 / a1) ** 2, 4)
        denom = round(1 - ratio_sq, 4)
        q_ideal = round(a2 * math.sqrt(2 * _G * h / denom), 4)

        if difficulty >= 7:
            cd = round(self._rng.uniform(0.95, 0.99), 3)
        else:
            cd = 1.0

        q = round(cd * q_ideal, 4)

        return "Q = C_d A_2 \\sqrt{\\frac{2gh}{1-(A_2/A_1)^2}}", {
            "d1_cm": d1_cm, "d2_cm": d2_cm,
            "d1": d1, "d2": d2,
            "A1": a1, "A2": a2,
            "h": h, "ratio_sq": ratio_sq,
            "denom": denom, "Cd": cd,
            "Q_ideal": q_ideal, "Q": q,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Venturi meter computation steps.

        Args:
            data: Solution data with areas and head.

        Returns:
            List of step strings.
        """
        steps = [
            f"d1={data['d1_cm']}cm, d2={data['d2_cm']}cm, h={data['h']}m",
            f"A1={_f(data['A1'])}m^2, A2={_f(data['A2'])}m^2",
            f"(A2/A1)^2 = {_f(data['ratio_sq'])}",
            f"2gh/(1-ratio^2) = 2*{_G}*{data['h']}/{_f(data['denom'])}",
        ]
        if data["Cd"] < 1.0:
            steps.append(f"Cd = {data['Cd']}, Q = Cd*Q_ideal")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the flow rate.

        Args:
            data: Solution data.

        Returns:
            String with Q.
        """
        return f"Q = {_f(data['Q'])} m^3/s"


# ===================================================================
# 3. Stokes drag  (tier 4)
# ===================================================================

@register
class StokesDragGenerator(StepGenerator):
    """Stokes drag: F_d = 6*pi*mu*r*v.

    Terminal velocity: v_t = 2*r^2*(rho_p - rho_f)*g / (9*mu).
    Computes drag force or terminal velocity for a sphere in
    viscous flow.

    Difficulty scaling:
        Difficulty 1-3: compute F_d given v.
        Difficulty 4-6: compute terminal velocity.
        Difficulty 7-8: compute settling time for given distance.

    Prerequisites:
        division.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "stokes_drag"

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
        return "compute Stokes drag or terminal velocity"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate sphere and fluid parameters.

        Args:
            difficulty: Controls problem variant.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        mu = round(self._rng.uniform(0.001, 0.1), 4)
        r_mm = round(self._rng.uniform(0.1, 2.0), 2)
        r = r_mm * 1e-3
        rho_p = self._rng.randint(2000, 8000)
        rho_f = self._rng.choice([1000, 1025, 900, 800])

        v_t = round(2 * r ** 2 * (rho_p - rho_f) * _G / (9 * mu), 4)
        fd = round(6 * math.pi * mu * r * v_t, 4)

        data = {
            "mu": mu, "r_mm": r_mm, "r": r,
            "rho_p": rho_p, "rho_f": rho_f,
            "v_t": v_t, "Fd": fd,
        }

        if difficulty <= 3:
            v_given = round(self._rng.uniform(0.001, v_t), 4)
            fd_given = round(6 * math.pi * mu * r * v_given, 4)
            data["v_given"] = v_given
            data["Fd_given"] = fd_given
            data["target"] = "Fd"
        elif difficulty <= 6:
            data["target"] = "v_t"
        else:
            dist = round(self._rng.uniform(0.1, 2.0), 2)
            settle_time = round(dist / v_t, 4) if v_t > 0 else float("inf")
            data["distance"] = dist
            data["settle_time"] = settle_time
            data["target"] = "settle"

        return "F_d = 6\\pi\\mu r v", data

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Stokes drag computation steps.

        Args:
            data: Solution data with sphere and fluid parameters.

        Returns:
            List of step strings.
        """
        steps = [
            f"mu={data['mu']}Pa*s, r={data['r_mm']}mm, "
            f"rho_p={data['rho_p']}, rho_f={data['rho_f']}",
        ]
        if data["target"] == "Fd":
            steps.append(f"v={_f(data['v_given'])}m/s")
            steps.append(f"Fd = 6*pi*{data['mu']}*{data['r']}*{_f(data['v_given'])}")
        elif data["target"] == "v_t":
            steps.append(f"drho = {data['rho_p']}-{data['rho_f']} = {data['rho_p']-data['rho_f']}")
            steps.append(f"v_t = 2*r^2*drho*g/(9*mu)")
        else:
            steps.append(f"v_t = {_f(data['v_t'])} m/s")
            steps.append(f"t = d/v_t = {data['distance']}/{_f(data['v_t'])}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the drag force, terminal velocity, or settling time.

        Args:
            data: Solution data.

        Returns:
            String with result.
        """
        if data["target"] == "Fd":
            return f"F_d = {_f(data['Fd_given'])} N"
        if data["target"] == "v_t":
            return f"v_t = {_f(data['v_t'])} m/s"
        return f"v_t = {_f(data['v_t'])} m/s, t = {_f(data['settle_time'])} s"


# ===================================================================
# 4. Hydraulic jump  (tier 5)
# ===================================================================

@register
class HydraulicJumpGenerator(StepGenerator):
    """Hydraulic jump: y2/y1 = 0.5*(sqrt(1 + 8*Fr1^2) - 1).

    Given upstream depth y1 and Froude number Fr1, computes the
    downstream depth y2 after a hydraulic jump.

    Difficulty scaling:
        Difficulty 1-3: moderate Fr (1.5-3).
        Difficulty 4-6: wider Fr range, also compute energy loss.
        Difficulty 7-8: given v1 and y1, compute Fr1 first.

    Prerequisites:
        square_root.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "hydraulic_jump"

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
        return "compute downstream depth after hydraulic jump"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate hydraulic jump parameters and compute y2.

        Args:
            difficulty: Controls Froude number range.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        y1 = round(self._rng.uniform(0.1, 1.0), 2)

        if difficulty <= 3:
            fr1 = round(self._rng.uniform(1.5, 3.0), 2)
        else:
            fr1 = round(self._rng.uniform(1.5, 6.0 + difficulty), 2)

        v1 = round(fr1 * math.sqrt(_G * y1), 4)
        inner = round(1 + 8 * fr1 ** 2, 4)
        sqrt_inner = round(math.sqrt(inner), 4)
        ratio = round(0.5 * (sqrt_inner - 1), 4)
        y2 = round(y1 * ratio, 4)

        data = {
            "y1": y1, "Fr1": fr1, "v1": v1,
            "inner": inner, "sqrt_inner": sqrt_inner,
            "ratio": ratio, "y2": y2,
        }

        if difficulty >= 4:
            de = round((y2 - y1) ** 3 / (4 * y1 * y2), 4)
            data["energy_loss"] = de

        return "\\frac{y_2}{y_1} = \\frac{1}{2}(\\sqrt{1+8Fr_1^2}-1)", data

    def _create_steps(self, data: dict) -> list[str]:
        """Generate hydraulic jump computation steps.

        Args:
            data: Solution data with y1, Fr1.

        Returns:
            List of step strings.
        """
        steps = [
            f"y1={data['y1']}m, Fr1={data['Fr1']}",
            f"1+8*Fr1^2 = 1+8*{data['Fr1']}^2 = {_f(data['inner'])}",
            f"sqrt({_f(data['inner'])}) = {_f(data['sqrt_inner'])}",
            f"y2/y1 = 0.5*({_f(data['sqrt_inner'])}-1) = {_f(data['ratio'])}",
        ]
        if "energy_loss" in data:
            steps.append(f"dE = (y2-y1)^3/(4*y1*y2) = {_f(data['energy_loss'])} m")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the downstream depth.

        Args:
            data: Solution data.

        Returns:
            String with y2.
        """
        ans = f"y2 = {_f(data['y2'])} m"
        if "energy_loss" in data:
            ans += f", dE = {_f(data['energy_loss'])} m"
        return ans


# ===================================================================
# 5. Open channel (Manning's equation)  (tier 5)
# ===================================================================

@register
class OpenChannelGenerator(StepGenerator):
    """Manning's equation: v = (1/n) * R_h^(2/3) * S^(1/2).

    Given Manning's roughness n, hydraulic radius R_h, and slope S,
    computes the flow velocity. For rectangular channels, also
    computes R_h from width and depth.

    Difficulty scaling:
        Difficulty 1-3: given R_h directly.
        Difficulty 4-6: rectangular channel, compute R_h.
        Difficulty 7-8: trapezoidal channel geometry.

    Prerequisites:
        exponentiation.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "open_channel"

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
        return "compute flow velocity using Manning's equation"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate channel parameters and compute velocity.

        Args:
            difficulty: Controls channel geometry type.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        n_manning = round(self._rng.uniform(0.01, 0.05), 3)
        slope = round(self._rng.uniform(0.0005, 0.01), 4)

        if difficulty <= 3:
            r_h = round(self._rng.uniform(0.2, 2.0), 2)
            data = {
                "n": n_manning, "S": slope, "R_h": r_h,
                "geometry": "given",
            }
        else:
            width = round(self._rng.uniform(1.0, 5.0 + difficulty), 1)
            depth = round(self._rng.uniform(0.3, 2.0), 2)
            area = round(width * depth, 4)
            perimeter = round(width + 2 * depth, 4)
            r_h = round(area / perimeter, 4)
            data = {
                "n": n_manning, "S": slope, "R_h": r_h,
                "geometry": "rectangular",
                "width": width, "depth": depth,
                "area": area, "perimeter": perimeter,
            }

        r_h_23 = round(data["R_h"] ** (2 / 3), 4)
        s_12 = round(slope ** 0.5, 4)
        v = round((1 / n_manning) * r_h_23 * s_12, 4)
        q = round(v * data.get("area", data["R_h"] * 3.0), 4)

        data["R_h_23"] = r_h_23
        data["S_12"] = s_12
        data["v"] = v
        data["Q"] = q

        return "v = \\frac{1}{n} R_h^{2/3} S^{1/2}", data

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Manning's equation steps.

        Args:
            data: Solution data with channel parameters.

        Returns:
            List of step strings.
        """
        steps = [f"n={data['n']}, S={data['S']}"]
        if data["geometry"] == "rectangular":
            steps.append(
                f"w={data['width']}m, d={data['depth']}m, "
                f"A={_f(data['area'])}m^2, P={_f(data['perimeter'])}m"
            )
            steps.append(f"R_h = A/P = {_f(data['R_h'])} m")
        else:
            steps.append(f"R_h = {data['R_h']} m")
        steps.append(f"R_h^(2/3) = {_f(data['R_h_23'])}")
        steps.append(f"S^(1/2) = {_f(data['S_12'])}")
        steps.append(f"v = (1/{data['n']})*{_f(data['R_h_23'])}*{_f(data['S_12'])}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the flow velocity.

        Args:
            data: Solution data.

        Returns:
            String with v.
        """
        return f"v = {_f(data['v'])} m/s"


# ===================================================================
# 6. Pump power  (tier 4)
# ===================================================================

@register
class PumpPowerGenerator(StepGenerator):
    """Pump power: P = rho * g * Q * H / eta.

    Given fluid density, flow rate Q, total head H, and pump
    efficiency eta, computes the required pump power.

    Difficulty scaling:
        Difficulty 1-3: water, simple values.
        Difficulty 4-6: varied fluids, compute head from pressures.
        Difficulty 7-8: solve for required Q given power budget.

    Prerequisites:
        multiplication.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "pump_power"

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
        return "compute pump power requirement"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate pump parameters and compute power.

        Args:
            difficulty: Controls fluid type and problem variant.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            rho = 1000
            fluid = "water"
        else:
            rho = self._rng.choice([1000, 900, 850, 1025])
            fluid = "fluid"

        q = round(self._rng.uniform(0.001, 0.1 + difficulty * 0.02), 4)
        h = round(self._rng.uniform(5.0, 30.0 + difficulty * 10), 1)
        eta = round(self._rng.uniform(0.6, 0.9), 2)

        p_hydraulic = round(rho * _G * q * h, 4)
        p_input = round(p_hydraulic / eta, 4)

        if difficulty >= 7:
            target = "Q"
            p_budget = self._rng.randint(500, 5000)
            q_max = round(p_budget * eta / (rho * _G * h), 4)
            return "P = \\frac{\\rho g Q H}{\\eta}", {
                "rho": rho, "fluid": fluid,
                "Q": q, "H": h, "eta": eta,
                "P_hydraulic": p_hydraulic,
                "P_input": p_input,
                "P_budget": p_budget, "Q_max": q_max,
                "target": target,
            }

        return "P = \\frac{\\rho g Q H}{\\eta}", {
            "rho": rho, "fluid": fluid,
            "Q": q, "H": h, "eta": eta,
            "P_hydraulic": p_hydraulic,
            "P_input": p_input,
            "target": "P",
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate pump power computation steps.

        Args:
            data: Solution data with pump parameters.

        Returns:
            List of step strings.
        """
        if data["target"] == "P":
            return [
                f"rho={data['rho']}, Q={_f(data['Q'])}m^3/s, "
                f"H={data['H']}m, eta={data['eta']}",
                f"P_hyd = rho*g*Q*H = {data['rho']}*{_G}*{_f(data['Q'])}*{data['H']}",
                f"P_hyd = {_f(data['P_hydraulic'])} W",
                f"P_input = P_hyd/eta = {_f(data['P_hydraulic'])}/{data['eta']}",
            ]
        return [
            f"P_budget={data['P_budget']}W, rho={data['rho']}, "
            f"H={data['H']}m, eta={data['eta']}",
            f"Q = P*eta/(rho*g*H) = {data['P_budget']}*{data['eta']}/({data['rho']}*{_G}*{data['H']})",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the pump power or maximum flow rate.

        Args:
            data: Solution data.

        Returns:
            String with result.
        """
        if data["target"] == "P":
            return f"P = {_f(data['P_input'])} W"
        return f"Q_max = {_f(data['Q_max'])} m^3/s"
