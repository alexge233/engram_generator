"""Oceanography generators -- Coriolis, wave speed, thermohaline, Ekman, tides, mixed layer.

6 generators covering the Coriolis parameter, deep/shallow water wave
phase speed, thermohaline density classification, Ekman layer depth,
tidal range (spring/neap), and mixed layer depth. Tiers 4-5.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


class _OceanFormatter:
    """Formats numeric values for oceanography problems.

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


_f = _OceanFormatter.fmt

# Physical constants
_OMEGA = 7.292e-5   # Earth's angular velocity (rad/s)
_G = 9.81           # gravitational acceleration (m/s^2)
_RHO_0 = 1025.0     # reference seawater density (kg/m^3)


# ===================================================================
# 1. Coriolis force  (tier 5)
# ===================================================================

@register
class CoriolisForceGenerator(StepGenerator):
    """Compute the Coriolis parameter f = 2 * Omega * sin(phi).

    Given a latitude phi in degrees, computes the Coriolis parameter
    using Earth's angular velocity Omega = 7.292e-5 rad/s.

    Difficulty scaling:
        Difficulty 1-3: standard latitudes (30, 45, 60).
        Difficulty 4-6: arbitrary integer latitudes 10-80.
        Difficulty 7-8: decimal latitudes with 1 dp.

    Prerequisites:
        sin_cos_eval.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "coriolis_force"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

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
        return "compute Coriolis parameter f = 2*Omega*sin(phi)"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate latitude and compute Coriolis parameter.

        Args:
            difficulty: Controls latitude precision.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            phi_deg = self._rng.choice([30, 45, 60])
        elif difficulty <= 6:
            phi_deg = self._rng.randint(10, 80)
        else:
            phi_deg = round(self._rng.uniform(5.0, 85.0), 1)

        phi_rad = round(math.radians(phi_deg), 4)
        sin_phi = round(math.sin(phi_rad), 4)
        f_val = round(2 * _OMEGA * sin_phi, 4)

        problem = (
            f"latitude phi = {phi_deg} deg, "
            f"Omega = {_OMEGA} rad/s; compute f"
        )
        return problem, {
            "phi_deg": phi_deg, "phi_rad": phi_rad,
            "sin_phi": sin_phi, "f": f_val,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Coriolis computation steps.

        Args:
            data: Solution data with latitude and trigonometric values.

        Returns:
            List of step strings.
        """
        return [
            f"phi = {data['phi_deg']} deg = {_f(data['phi_rad'])} rad",
            f"sin({_f(data['phi_rad'])}) = {_f(data['sin_phi'])}",
            f"f = 2 * {_OMEGA} * {_f(data['sin_phi'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the Coriolis parameter.

        Args:
            data: Solution data.

        Returns:
            String with f in s^-1.
        """
        return f"f = {_f(data['f'])} s^-1"


# ===================================================================
# 2. Ocean wave speed  (tier 4)
# ===================================================================

@register
class OceanWaveSpeedGenerator(StepGenerator):
    """Compute phase speed for deep or shallow water waves.

    Deep water: c = sqrt(g * lambda / (2 * pi)).
    Shallow water: c = sqrt(g * h).

    Difficulty scaling:
        Difficulty 1-3: shallow water with integer depths (1-10 m).
        Difficulty 4-6: deep water with wavelengths 10-200 m.
        Difficulty 7-8: mixed regime, decimal parameters.

    Prerequisites:
        square_root.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "ocean_wave_speed"

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
        if difficulty <= 3:
            return "compute shallow water wave phase speed"
        return "compute deep water wave phase speed"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate wave parameters and compute phase speed.

        Args:
            difficulty: Controls regime and parameter precision.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            h = float(self._rng.randint(1, 10))
            c = round(math.sqrt(_G * h), 4)
            inner = round(_G * h, 4)
            return "c = \\sqrt{g h}", {
                "mode": "shallow", "h": h,
                "inner": inner, "c": c,
            }

        if difficulty <= 6:
            lam = float(self._rng.randint(10, 200))
        else:
            lam = round(self._rng.uniform(5.0, 300.0), 1)

        inner = round(_G * lam / (2 * math.pi), 4)
        c = round(math.sqrt(inner), 4)
        return "c = \\sqrt{\\frac{g \\lambda}{2\\pi}}", {
            "mode": "deep", "lambda": lam,
            "inner": inner, "c": c,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate wave speed computation steps.

        Args:
            data: Solution data with mode and parameters.

        Returns:
            List of step strings.
        """
        if data["mode"] == "shallow":
            return [
                f"shallow water: c = sqrt(g*h)",
                f"g*h = {_G} * {_f(data['h'])} = {_f(data['inner'])}",
                f"c = sqrt({_f(data['inner'])}) = {_f(data['c'])}",
            ]
        return [
            f"deep water: c = sqrt(g*lambda/(2*pi))",
            f"g*lambda/(2*pi) = {_G}*{_f(data['lambda'])}/"
            f"{_f(round(2 * math.pi, 4))} = {_f(data['inner'])}",
            f"c = sqrt({_f(data['inner'])}) = {_f(data['c'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the phase speed.

        Args:
            data: Solution data.

        Returns:
            String with c in m/s.
        """
        return f"c = {_f(data['c'])} m/s"


# ===================================================================
# 3. Thermohaline density  (tier 5)
# ===================================================================

@register
class ThermohalineGenerator(StepGenerator):
    """Compute density sigma_t from temperature and salinity.

    Linear equation of state: rho = rho_0 * (1 - alpha*T + beta*S)
    where alpha = 2.0e-4 /degC and beta = 7.6e-4 /PSU.
    Classifies water mass by sigma_t range.

    Difficulty scaling:
        Difficulty 1-3: T in [0, 10], S in [34, 36] (simple).
        Difficulty 4-6: T in [-2, 25], S in [33, 37].
        Difficulty 7-8: extreme T and S with 2 dp precision.

    Prerequisites:
        multiplication.
    """

    _ALPHA = 2.0e-4   # thermal expansion coefficient (/degC)
    _BETA = 7.6e-4    # haline contraction coefficient (/PSU)

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "thermohaline"

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
        return "compute seawater density and classify water mass"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate T, S and compute density.

        Args:
            difficulty: Controls temperature and salinity ranges.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            temp = float(self._rng.randint(0, 10))
            sal = round(self._rng.uniform(34.0, 36.0), 1)
        elif difficulty <= 6:
            temp = round(self._rng.uniform(-2.0, 25.0), 1)
            sal = round(self._rng.uniform(33.0, 37.0), 1)
        else:
            temp = round(self._rng.uniform(-2.0, 30.0), 2)
            sal = round(self._rng.uniform(32.0, 38.0), 2)

        alpha_t = round(self._ALPHA * temp, 4)
        beta_s = round(self._BETA * sal, 4)
        factor = round(1.0 - alpha_t + beta_s, 4)
        rho = round(_RHO_0 * factor, 4)
        sigma_t = round(rho - 1000.0, 4)

        if sigma_t < 24.0:
            classification = "surface"
        elif sigma_t < 27.0:
            classification = "intermediate"
        else:
            classification = "deep"

        problem = (
            f"T = {temp} degC, S = {sal} PSU, "
            f"rho_0 = {_RHO_0}; classify water mass"
        )
        return problem, {
            "T": temp, "S": sal, "alpha_T": alpha_t,
            "beta_S": beta_s, "factor": factor,
            "rho": rho, "sigma_t": sigma_t,
            "classification": classification,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate thermohaline computation steps.

        Args:
            data: Solution data with T, S, and density.

        Returns:
            List of step strings.
        """
        return [
            f"alpha*T = {self._ALPHA}*{_f(data['T'])} = {_f(data['alpha_T'])}",
            f"beta*S = {self._BETA}*{_f(data['S'])} = {_f(data['beta_S'])}",
            f"rho = {_RHO_0}*(1 - {_f(data['alpha_T'])} + "
            f"{_f(data['beta_S'])}) = {_f(data['rho'])}",
            f"sigma_t = {_f(data['rho'])} - 1000 = {_f(data['sigma_t'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return density and classification.

        Args:
            data: Solution data.

        Returns:
            String with sigma_t and water mass class.
        """
        return (
            f"sigma_t = {_f(data['sigma_t'])} kg/m^3, "
            f"{data['classification']} water"
        )


# ===================================================================
# 4. Ekman depth  (tier 5)
# ===================================================================

@register
class EkmanDepthGenerator(StepGenerator):
    """Compute Ekman layer depth D_E = pi * sqrt(2 * A_z / f).

    Given eddy viscosity A_z and Coriolis parameter f, computes
    the depth of the wind-driven Ekman spiral layer.

    Difficulty scaling:
        Difficulty 1-3: A_z in [0.01, 0.05], f at standard lats.
        Difficulty 4-6: A_z in [0.005, 0.1], f computed from lat.
        Difficulty 7-8: decimal A_z and precise f values.

    Prerequisites:
        square_root.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "ekman_depth"

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
        return "compute Ekman layer depth"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate A_z and f, then compute Ekman depth.

        Args:
            difficulty: Controls parameter range and precision.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            a_z = round(self._rng.uniform(0.01, 0.05), 3)
            phi_deg = self._rng.choice([30, 45, 60])
        elif difficulty <= 6:
            a_z = round(self._rng.uniform(0.005, 0.1), 4)
            phi_deg = self._rng.randint(15, 75)
        else:
            a_z = round(self._rng.uniform(0.001, 0.15), 4)
            phi_deg = round(self._rng.uniform(10.0, 80.0), 1)

        phi_rad = round(math.radians(phi_deg), 4)
        f_val = round(2 * _OMEGA * math.sin(phi_rad), 4)
        # Ensure f is positive for meaningful Ekman depth
        f_val = max(f_val, 1e-6)
        ratio = round(2 * a_z / f_val, 4)
        sqrt_ratio = round(math.sqrt(ratio), 4)
        d_e = round(math.pi * sqrt_ratio, 4)

        problem = (
            f"A_z = {a_z} m^2/s, latitude = {phi_deg} deg; "
            f"compute Ekman depth"
        )
        return problem, {
            "A_z": a_z, "phi_deg": phi_deg, "f": f_val,
            "ratio": ratio, "sqrt_ratio": sqrt_ratio, "D_E": d_e,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Ekman depth computation steps.

        Args:
            data: Solution data with A_z, f, and D_E.

        Returns:
            List of step strings.
        """
        return [
            f"f = 2*Omega*sin(lat) = {_f(data['f'])} s^-1",
            f"2*A_z/f = 2*{_f(data['A_z'])}/{_f(data['f'])} "
            f"= {_f(data['ratio'])}",
            f"sqrt({_f(data['ratio'])}) = {_f(data['sqrt_ratio'])}",
            f"D_E = pi * {_f(data['sqrt_ratio'])} = {_f(data['D_E'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the Ekman depth.

        Args:
            data: Solution data.

        Returns:
            String with D_E in metres.
        """
        return f"D_E = {_f(data['D_E'])} m"


# ===================================================================
# 5. Tidal range  (tier 4)
# ===================================================================

@register
class TidalRangeGenerator(StepGenerator):
    """Compute spring and neap tidal ranges from M2 and S2 amplitudes.

    Spring tide range = 2 * (M2 + S2).
    Neap tide range = 2 * (M2 - S2).

    Difficulty scaling:
        Difficulty 1-3: integer amplitudes (0.5-2.0 m steps).
        Difficulty 4-6: decimal amplitudes to 1 dp.
        Difficulty 7-8: precise amplitudes to 2 dp, compute both.

    Prerequisites:
        subtraction.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "tidal_range"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["subtraction"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute spring and neap tidal ranges"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate M2 and S2 amplitudes, compute tidal ranges.

        Args:
            difficulty: Controls amplitude precision.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            m2 = round(self._rng.uniform(0.5, 2.0), 1)
            s2 = round(self._rng.uniform(0.1, m2 - 0.05), 1)
        elif difficulty <= 6:
            m2 = round(self._rng.uniform(0.3, 3.0), 1)
            s2 = round(self._rng.uniform(0.1, m2 - 0.05), 1)
        else:
            m2 = round(self._rng.uniform(0.2, 4.0), 2)
            s2 = round(self._rng.uniform(0.05, m2 - 0.02), 2)

        spring = round(2 * (m2 + s2), 4)
        neap = round(2 * (m2 - s2), 4)

        problem = f"M2 = {m2} m, S2 = {s2} m; compute tidal ranges"
        return problem, {
            "M2": m2, "S2": s2,
            "spring": spring, "neap": neap,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate tidal range computation steps.

        Args:
            data: Solution data with amplitudes and ranges.

        Returns:
            List of step strings.
        """
        m2_plus = round(data["M2"] + data["S2"], 4)
        m2_minus = round(data["M2"] - data["S2"], 4)
        return [
            f"M2 = {_f(data['M2'])} m, S2 = {_f(data['S2'])} m",
            f"M2 + S2 = {_f(m2_plus)}, spring = 2*{_f(m2_plus)} "
            f"= {_f(data['spring'])}",
            f"M2 - S2 = {_f(m2_minus)}, neap = 2*{_f(m2_minus)} "
            f"= {_f(data['neap'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return spring and neap tidal ranges.

        Args:
            data: Solution data.

        Returns:
            String with both ranges in metres.
        """
        return (
            f"spring = {_f(data['spring'])} m, "
            f"neap = {_f(data['neap'])} m"
        )


# ===================================================================
# 6. Mixed layer depth  (tier 5)
# ===================================================================

@register
class MixedLayerDepthGenerator(StepGenerator):
    """Compute mixed layer depth h = sqrt(2 * u_star^3 / (f * B_0)).

    Given friction velocity u_star, Coriolis parameter f, and
    surface buoyancy flux B_0, computes the equilibrium mixed
    layer depth.

    Difficulty scaling:
        Difficulty 1-3: standard values, integer-ish parameters.
        Difficulty 4-6: varied u_star, B_0 in [1e-8, 5e-7].
        Difficulty 7-8: precise parameters with 4 dp.

    Prerequisites:
        square_root.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "mixed_layer_depth"

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
        return "compute mixed layer depth from friction velocity and buoyancy flux"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate u_star, f, B_0 and compute mixed layer depth.

        Args:
            difficulty: Controls parameter precision.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            u_star = round(self._rng.uniform(0.005, 0.02), 3)
            phi_deg = self._rng.choice([30, 45, 60])
            b_0 = round(self._rng.uniform(1e-7, 5e-7), 4)
        elif difficulty <= 6:
            u_star = round(self._rng.uniform(0.003, 0.03), 4)
            phi_deg = self._rng.randint(20, 70)
            b_0 = round(self._rng.uniform(1e-8, 5e-7), 4)
        else:
            u_star = round(self._rng.uniform(0.001, 0.04), 4)
            phi_deg = round(self._rng.uniform(10.0, 80.0), 1)
            b_0 = round(self._rng.uniform(1e-8, 1e-6), 4)

        phi_rad = math.radians(phi_deg)
        f_val = round(2 * _OMEGA * math.sin(phi_rad), 4)
        f_val = max(f_val, 1e-6)
        b_0 = max(b_0, 1e-10)

        u_cubed = round(u_star ** 3, 4)
        numerator = round(2 * u_cubed, 4)
        denominator = round(f_val * b_0, 4)
        denominator = max(denominator, 1e-15)
        ratio = round(numerator / denominator, 4)
        h = round(math.sqrt(ratio), 4)

        problem = (
            f"u_star = {u_star} m/s, lat = {phi_deg} deg, "
            f"B_0 = {b_0} m^2/s^3; compute h"
        )
        return problem, {
            "u_star": u_star, "phi_deg": phi_deg,
            "f": f_val, "B_0": b_0,
            "u_cubed": u_cubed, "numerator": numerator,
            "denominator": denominator, "ratio": ratio, "h": h,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate mixed layer depth computation steps.

        Args:
            data: Solution data.

        Returns:
            List of step strings.
        """
        return [
            f"f = {_f(data['f'])} s^-1",
            f"u_star^3 = {_f(data['u_star'])}^3 = {_f(data['u_cubed'])}",
            f"2*u_star^3/(f*B_0) = {_f(data['numerator'])}/"
            f"{_f(data['denominator'])} = {_f(data['ratio'])}",
            f"h = sqrt({_f(data['ratio'])}) = {_f(data['h'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the mixed layer depth.

        Args:
            data: Solution data.

        Returns:
            String with h in metres.
        """
        return f"h = {_f(data['h'])} m"
