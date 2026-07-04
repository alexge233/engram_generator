"""General relativity generators -- Schwarzschild metric through cosmic distance.

Covers the Schwarzschild metric and its applications (redshift, geodesics,
perihelion precession), the Einstein tensor, Friedmann equation for
cosmological expansion, gravitational wave strain, and comoving distance
calculations. Tiers range from 6 (metric components) to 7 (geodesics,
Einstein tensor, Friedmann).
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


# Physical constants
_G = 6.674e-11
_C = 2.998e8
_C_SQ = _C ** 2
_SOLAR_MASS = 1.989e30


class _GRFormatter:
    """Formats numeric values for general relativity problems.

    Provides scientific notation for large/small numbers and clean
    decimal formatting for dimensionless quantities.
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
        sign = "-" if value < 0 else ""
        return f"{sign}{abs(mantissa)} \\times 10^{{{exponent}}}"

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
# 1. Schwarzschild metric  (tier 6)
# ---------------------------------------------------------------------------


@register
class SchwarzschildMetricGenerator(StepGenerator):
    """Compute Schwarzschild metric components at a given radius.

    Writes the full Schwarzschild line element and evaluates the
    metric tensor components g_tt and g_rr at a specific radial
    coordinate r, given the Schwarzschild radius r_s = 2GM/c^2.

    Input format:
        ``compute Schwarzschild metric components``

    Target format:
        ``ds^2 = -(1-r_s/r)c^2dt^2 + (1-r_s/r)^{-1}dr^2 + r^2 d\\Omega^2
        <step> r_s = 2GM/c^2 = ... <step>
        1 - r_s/r = ... <step>
        g_{tt} = -(1-r_s/r)c^2 = ... <step>
        g_{rr} = (1-r_s/r)^{-1} = ...``

    Difficulty scaling:
        d1-3: stellar mass (1-5 solar), r >> r_s.
        d4-6: stellar mass, r closer to r_s.
        d7-8: supermassive BH, r near a few r_s.

    Prerequisites:
        metric_tensor.
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "schwarzschild_metric"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["metric_tensor"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls mass scale and radial proximity.

        Returns:
            Natural language description.
        """
        return "compute Schwarzschild metric components"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate mass and radius, compute metric components.

        Args:
            difficulty: Controls parameter ranges.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            solar_mult = float(self._rng.randint(1, 5))
            r_mult = self._rng.randint(50, 200)
        elif difficulty <= 6:
            solar_mult = float(self._rng.randint(1, 10))
            r_mult = self._rng.randint(10, 50)
        else:
            solar_mult = float(self._rng.randint(1, 9)) * 1e6
            r_mult = self._rng.randint(3, 15)
        mass = solar_mult * _SOLAR_MASS
        r_s = 2 * _G * mass / _C_SQ
        r = r_mult * r_s
        ratio = r_s / r
        one_minus = 1.0 - ratio
        g_tt = round(-one_minus * _C_SQ, 4)
        g_rr = round(1.0 / one_minus, 4)
        m_str = _GRFormatter.format_sci(mass)
        formula = (
            "ds^2 = -(1-r_s/r)c^2dt^2 + (1-r_s/r)^{-1}dr^2 + r^2 d\\Omega^2, "
            f"M={m_str} kg, r={r_mult} r_s, "
            f"G=6.674 \\times 10^{{-11}}, c=2.998 \\times 10^{{8}}"
        )
        return formula, {
            "M": mass, "solar_mult": solar_mult,
            "r_s": r_s, "r": r, "r_mult": r_mult,
            "ratio": round(ratio, 4),
            "one_minus": round(one_minus, 4),
            "g_tt": g_tt, "g_rr": g_rr,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Schwarzschild metric computation steps.

        Args:
            data: Solution data with r_s, r, and metric components.

        Returns:
            Steps showing r_s, ratio, g_tt, and g_rr.
        """
        rs_str = _GRFormatter.format_sci(data["r_s"])
        r_str = _GRFormatter.format_sci(data["r"])
        return [
            f"r_s = 2GM/c^2 = {rs_str} m",
            f"r = {data['r_mult']} r_s = {r_str} m",
            f"1 - r_s/r = 1 - {_GRFormatter.fmt(data['ratio'])} = {_GRFormatter.fmt(data['one_minus'])}",
            f"g_{{tt}} = -{_GRFormatter.fmt(data['one_minus'])} c^2 = {_GRFormatter.format_sci(data['g_tt'])}",
            f"g_{{rr}} = 1/{_GRFormatter.fmt(data['one_minus'])} = {_GRFormatter.fmt(data['g_rr'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the metric components.

        Args:
            data: Solution data.

        Returns:
            String with g_tt and g_rr values.
        """
        return f"g_{{tt}} = {_GRFormatter.format_sci(data['g_tt'])}, g_{{rr}} = {_GRFormatter.fmt(data['g_rr'])}"


# ---------------------------------------------------------------------------
# 2. Gravitational redshift (GR)  (tier 6)
# ---------------------------------------------------------------------------


@register
class GravitationalRedshiftGRGenerator(StepGenerator):
    """Compute gravitational redshift: z = 1/sqrt(1 - r_s/r) - 1.

    Evaluates the gravitational frequency shift for a photon emitted
    at radius r in a Schwarzschild spacetime, observed at infinity.

    Input format:
        ``compute gravitational redshift``

    Target format:
        ``z = \\frac{1}{\\sqrt{1 - r_s/r}} - 1 <step>
        r_s = ... <step>
        r_s/r = ... <step>
        1 - r_s/r = ... <step>
        z = 1/\\sqrt{...} - 1 = ...``

    Difficulty scaling:
        d1-3: r >> r_s (small redshift, z << 1).
        d4-6: r ~ 10-30 r_s (moderate redshift).
        d7-8: r ~ 3-5 r_s (strong field).

    Prerequisites:
        schwarzschild_radius.
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "gravitational_redshift_gr"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["schwarzschild_radius"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls radial proximity to r_s.

        Returns:
            Natural language description.
        """
        return "compute gravitational redshift"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate mass and emission radius, compute redshift.

        Args:
            difficulty: Controls r/r_s ratio.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        solar_mult = float(self._rng.randint(1, 10))
        mass = solar_mult * _SOLAR_MASS
        r_s = 2 * _G * mass / _C_SQ
        if difficulty <= 3:
            r_mult = self._rng.randint(100, 500)
        elif difficulty <= 6:
            r_mult = self._rng.randint(10, 30)
        else:
            r_mult = self._rng.randint(3, 5)
        r = r_mult * r_s
        ratio = r_s / r
        one_minus = 1.0 - ratio
        sqrt_val = math.sqrt(one_minus)
        z = round(1.0 / sqrt_val - 1.0, 4)
        formula = "z = \\frac{1}{\\sqrt{1 - r_s/r}} - 1"
        return formula, {
            "M": mass, "solar_mult": solar_mult,
            "r_s": r_s, "r": r, "r_mult": r_mult,
            "ratio": round(ratio, 4),
            "one_minus": round(one_minus, 4),
            "sqrt_val": round(sqrt_val, 4),
            "z": z,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate gravitational redshift computation steps.

        Args:
            data: Solution data with r_s, r, and z.

        Returns:
            Steps showing r_s, ratio, sqrt, and z.
        """
        rs_str = _GRFormatter.format_sci(data["r_s"])
        return [
            f"r_s = {rs_str} m",
            f"r = {data['r_mult']} r_s, r_s/r = {_GRFormatter.fmt(data['ratio'])}",
            f"1 - r_s/r = {_GRFormatter.fmt(data['one_minus'])}",
            f"\\sqrt{{{_GRFormatter.fmt(data['one_minus'])}}} = {_GRFormatter.fmt(data['sqrt_val'])}",
            f"z = 1/{_GRFormatter.fmt(data['sqrt_val'])} - 1",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the gravitational redshift.

        Args:
            data: Solution data.

        Returns:
            String representation of z.
        """
        return f"z = {_GRFormatter.fmt(data['z'])}"


# ---------------------------------------------------------------------------
# 3. Geodesic in Schwarzschild spacetime  (tier 7)
# ---------------------------------------------------------------------------


@register
class GeodesicSchwarzschildGenerator(StepGenerator):
    """Write geodesic equations for radial motion in Schwarzschild.

    Derives dr/dtau from the effective potential for radial geodesics:
    (dr/dtau)^2 = E^2 - (1 - r_s/r)(1 + L^2/r^2), where E and L
    are constants of motion.

    Input format:
        ``compute Schwarzschild radial geodesic``

    Target format:
        ``(dr/d\\tau)^2 = E^2 - V_{eff}(r) <step>
        V_{eff} = (1 - r_s/r)(1 + L^2/r^2) <step>
        r_s = ..., E = ..., L = ... <step>
        V_{eff}(r) = ... <step>
        (dr/d\\tau)^2 = ...``

    Difficulty scaling:
        d1-3: radial free fall (L = 0).
        d4-6: nonzero angular momentum, r ~ 20 r_s.
        d7-8: near-horizon orbits, r ~ 4-6 r_s.

    Prerequisites:
        geodesic_equation.
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "geodesic_schwarzschild"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["geodesic_equation"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls angular momentum and radius.

        Returns:
            Natural language description.
        """
        return "compute Schwarzschild radial geodesic"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate geodesic parameters and compute dr/dtau.

        Args:
            difficulty: Controls L and r/r_s.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        solar_mult = float(self._rng.randint(1, 10))
        mass = solar_mult * _SOLAR_MASS
        r_s = 2 * _G * mass / _C_SQ
        e_val = round(self._rng.uniform(0.95, 1.05), 4)
        if difficulty <= 3:
            l_val = 0.0
            r_mult = self._rng.randint(20, 100)
        elif difficulty <= 6:
            l_val = round(self._rng.uniform(1.0, 5.0) * r_s, 4)
            r_mult = self._rng.randint(15, 30)
        else:
            l_val = round(self._rng.uniform(2.0, 6.0) * r_s, 4)
            r_mult = self._rng.randint(4, 6)
        r = r_mult * r_s
        ratio = r_s / r
        one_minus = 1.0 - ratio
        l_sq_over_r_sq = (l_val * l_val) / (r * r) if r > 0 else 0.0
        v_eff = one_minus * (1.0 + l_sq_over_r_sq)
        dr_dtau_sq = round(e_val * e_val - v_eff, 4)
        formula = "(dr/d\\tau)^2 = E^2 - V_{eff}(r)"
        return formula, {
            "M": mass, "solar_mult": solar_mult,
            "r_s": r_s, "r": r, "r_mult": r_mult,
            "E": e_val, "L": l_val,
            "ratio": round(ratio, 4),
            "one_minus": round(one_minus, 4),
            "V_eff": round(v_eff, 4),
            "dr_dtau_sq": dr_dtau_sq,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate geodesic computation steps.

        Args:
            data: Solution data with E, L, r, and V_eff.

        Returns:
            Steps showing r_s, V_eff, and dr/dtau^2.
        """
        rs_str = _GRFormatter.format_sci(data["r_s"])
        steps = [
            f"r_s = {rs_str}, r = {data['r_mult']} r_s",
            f"E = {_GRFormatter.fmt(data['E'])}, L = {_GRFormatter.format_sci(data['L'])}",
            f"1 - r_s/r = {_GRFormatter.fmt(data['one_minus'])}",
            f"V_{{eff}} = {_GRFormatter.fmt(data['V_eff'])}",
            f"(dr/d\\tau)^2 = {_GRFormatter.fmt(data['E'])}^2 - {_GRFormatter.fmt(data['V_eff'])}",
        ]
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return dr/dtau squared.

        Args:
            data: Solution data.

        Returns:
            String representation of (dr/dtau)^2.
        """
        return f"(dr/d\\tau)^2 = {_GRFormatter.fmt(data['dr_dtau_sq'])}"


# ---------------------------------------------------------------------------
# 4. Einstein tensor  (tier 7)
# ---------------------------------------------------------------------------


@register
class EinsteinTensorGenerator(StepGenerator):
    """Compute the Einstein tensor G_mn = R_mn - (1/2)*g_mn*R.

    For a simple diagonal metric (FLRW or spherically symmetric),
    computes components of the Einstein tensor from given Ricci tensor
    and scalar curvature values.

    Input format:
        ``compute Einstein tensor component``

    Target format:
        ``G_{mn} = R_{mn} - \\frac{1}{2}g_{mn}R <step>
        R_{00} = ..., g_{00} = ..., R = ... <step>
        G_{00} = R_{00} - (1/2)(g_{00})(R) <step>
        G_{00} = ...``

    Difficulty scaling:
        d1-3: compute G_00 with simple integer values.
        d4-6: compute G_11 with moderate values.
        d7-8: compute both G_00 and G_11.

    Prerequisites:
        ricci_tensor.
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "einstein_tensor"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["ricci_tensor"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls number of components.

        Returns:
            Natural language description.
        """
        return "compute Einstein tensor component"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate Ricci tensor values and compute Einstein tensor.

        Args:
            difficulty: Controls number of components computed.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        r_scalar = round(self._rng.uniform(-2.0, 2.0), 4)
        if difficulty <= 3:
            g_00 = round(-1.0 + self._rng.uniform(-0.3, 0.0), 4)
            r_00 = round(self._rng.uniform(-1.0, 1.0), 4)
            g_00_val = round(g_00, 4)
            g_11 = r_00_1 = g_11_val = r_11 = g_01 = g_10 = 0.0
            compute_both = False
        elif difficulty <= 6:
            g_00 = round(-1.0 + self._rng.uniform(-0.3, 0.0), 4)
            g_11 = round(1.0 + self._rng.uniform(-0.3, 0.3), 4)
            r_00 = round(self._rng.uniform(-1.0, 1.0), 4)
            r_11 = round(self._rng.uniform(-1.0, 1.0), 4)
            g_00_val = g_00
            g_11_val = g_11
            compute_both = False
        else:
            g_00 = round(-1.0 + self._rng.uniform(-0.3, 0.0), 4)
            g_11 = round(1.0 + self._rng.uniform(-0.3, 0.3), 4)
            r_00 = round(self._rng.uniform(-2.0, 2.0), 4)
            r_11 = round(self._rng.uniform(-2.0, 2.0), 4)
            g_00_val = g_00
            g_11_val = g_11
            compute_both = True
        g_00_comp = round(r_00 - 0.5 * g_00 * r_scalar, 4)
        g_11_comp = round(r_11 - 0.5 * g_11 * r_scalar, 4) if difficulty > 3 else 0.0
        formula = "G_{mn} = R_{mn} - \\frac{1}{2}g_{mn}R"
        return formula, {
            "R": r_scalar,
            "g_00": g_00, "g_11": g_11,
            "R_00": r_00, "R_11": r_11,
            "G_00": g_00_comp, "G_11": g_11_comp,
            "compute_both": compute_both,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Einstein tensor computation steps.

        Args:
            data: Solution data with Ricci and metric values.

        Returns:
            Steps showing R_mn, g_mn, R, and G_mn.
        """
        r_str = _GRFormatter.fmt(data["R"])
        steps = [f"R = {r_str}"]
        steps.append(
            f"R_{{00}} = {_GRFormatter.fmt(data['R_00'])}, "
            f"g_{{00}} = {_GRFormatter.fmt(data['g_00'])}"
        )
        half_g00_r = round(0.5 * data["g_00"] * data["R"], 4)
        steps.append(
            f"G_{{00}} = {_GRFormatter.fmt(data['R_00'])} "
            f"- (1/2)({_GRFormatter.fmt(data['g_00'])})({r_str}) "
            f"= {_GRFormatter.fmt(data['R_00'])} - ({_GRFormatter.fmt(half_g00_r)})"
        )
        if data["compute_both"]:
            half_g11_r = round(0.5 * data["g_11"] * data["R"], 4)
            steps.append(
                f"G_{{11}} = {_GRFormatter.fmt(data['R_11'])} "
                f"- (1/2)({_GRFormatter.fmt(data['g_11'])})({r_str}) "
                f"= {_GRFormatter.fmt(data['G_11'])}"
            )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the Einstein tensor components.

        Args:
            data: Solution data.

        Returns:
            String with G_00 (and optionally G_11).
        """
        result = f"G_{{00}} = {_GRFormatter.fmt(data['G_00'])}"
        if data["compute_both"]:
            result += f", G_{{11}} = {_GRFormatter.fmt(data['G_11'])}"
        return result


# ---------------------------------------------------------------------------
# 5. Cosmological expansion (Friedmann)  (tier 7)
# ---------------------------------------------------------------------------


@register
class CosmologicalExpansionGenerator(StepGenerator):
    """Compute expansion rate from the Friedmann equation.

    Uses (a_dot/a)^2 = 8*pi*G*rho/3 with different density models:
    matter-dominated (rho ~ a^{-3}), radiation-dominated (rho ~ a^{-4}),
    or mixed. Computes da/dt for a given scale factor a.

    Input format:
        ``compute cosmological expansion rate``

    Target format:
        ``(\\dot{a}/a)^2 = \\frac{8\\pi G \\rho}{3} <step>
        \\rho(a) = \\rho_0 a^{-3} <step>
        H^2 = 8\\pi G \\rho_0 / (3 a^3) <step>
        H = ..., \\dot{a} = Ha = ...``

    Difficulty scaling:
        d1-3: matter-dominated, a = 1 (present epoch).
        d4-6: radiation-dominated, variable a.
        d7-8: mixed matter + radiation.

    Prerequisites:
        diff_equation.
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "cosmological_expansion"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["diff_equation"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls density model.

        Returns:
            Natural language description.
        """
        return "compute cosmological expansion rate"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate density and scale factor, compute da/dt.

        Args:
            difficulty: Controls density model complexity.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        rho_0 = round(self._rng.uniform(1e-27, 9e-27), 30)
        if difficulty <= 3:
            model = "matter"
            a = 1.0
            rho = rho_0 * a ** (-3)
        elif difficulty <= 6:
            model = "radiation"
            a = round(self._rng.uniform(0.5, 2.0), 2)
            rho = rho_0 * a ** (-4)
        else:
            model = "mixed"
            a = round(self._rng.uniform(0.3, 1.5), 2)
            rho_m = rho_0 * a ** (-3)
            rho_r = (rho_0 * 0.1) * a ** (-4)
            rho = rho_m + rho_r
        h_sq = 8 * math.pi * _G * rho / 3.0
        h_val = math.sqrt(h_sq)
        a_dot = h_val * a
        formula = "(\\dot{a}/a)^2 = \\frac{8\\pi G \\rho}{3}"
        return formula, {
            "model": model, "rho_0": rho_0, "a": a,
            "rho": rho, "H_sq": h_sq, "H": h_val,
            "a_dot": a_dot,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Friedmann equation computation steps.

        Args:
            data: Solution data with density, H, and da/dt.

        Returns:
            Steps showing density model, H^2, H, and a_dot.
        """
        model = data["model"]
        a = _GRFormatter.fmt(data["a"])
        rho_str = _GRFormatter.format_sci(data["rho"])
        h_sq_str = _GRFormatter.format_sci(data["H_sq"])
        h_str = _GRFormatter.format_sci(data["H"])
        steps = []
        if model == "matter":
            steps.append(f"\\rho = \\rho_0 a^{{-3}}, a = {a}")
        elif model == "radiation":
            steps.append(f"\\rho = \\rho_0 a^{{-4}}, a = {a}")
        else:
            steps.append(f"\\rho = \\rho_m + \\rho_r, a = {a}")
        steps.append(f"\\rho({a}) = {rho_str} kg/m^3")
        steps.append(f"H^2 = 8\\pi G \\rho / 3 = {h_sq_str}")
        steps.append(f"H = {h_str} s^{{-1}}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the expansion rate.

        Args:
            data: Solution data.

        Returns:
            String with H and da/dt.
        """
        return f"\\dot{{a}} = {_GRFormatter.format_sci(data['a_dot'])} s^{{-1}}"


# ---------------------------------------------------------------------------
# 6. Gravitational wave strain  (tier 6)
# ---------------------------------------------------------------------------


@register
class GravitationalWaveStrainGenerator(StepGenerator):
    """Compute gravitational wave strain at a detector.

    Uses h = 4*G*M*omega^2*r_source / (c^4 * d) for a binary system,
    where M is the chirp mass, omega is the orbital frequency,
    r_source is the orbital separation, and d is distance to the source.

    Input format:
        ``compute gravitational wave strain``

    Target format:
        ``h = \\frac{4GM\\omega^2 r}{c^4 d} <step>
        M = ..., \\omega = ..., r = ..., d = ... <step>
        numerator = 4GM\\omega^2 r = ... <step>
        denominator = c^4 d = ... <step>
        h = ...``

    Difficulty scaling:
        d1-3: nearby binary (d ~ 10 kpc), large chirp mass.
        d4-6: moderate distance (d ~ 100 Mpc).
        d7-8: cosmological distance (d ~ 1 Gpc).

    Prerequisites:
        gravitational_lensing.
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "gravitational_wave_strain"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["gravitational_lensing"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls source distance.

        Returns:
            Natural language description.
        """
        return "compute gravitational wave strain"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate binary source parameters and compute strain.

        Args:
            difficulty: Controls distance and mass scales.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        chirp_mass = float(self._rng.randint(10, 50)) * _SOLAR_MASS
        omega = round(self._rng.uniform(10, 200) * 2 * math.pi, 4)
        r_source = round(self._rng.uniform(1e5, 1e6), 0)
        pc_m = 3.086e16
        if difficulty <= 3:
            d = float(self._rng.randint(1, 10)) * 1e3 * pc_m
        elif difficulty <= 6:
            d = float(self._rng.randint(10, 500)) * 1e6 * pc_m
        else:
            d = float(self._rng.randint(1, 5)) * 1e9 * pc_m
        numerator = 4 * _G * chirp_mass * omega * omega * r_source
        c4 = _C ** 4
        denominator = c4 * d
        h = numerator / denominator
        formula = "h = \\frac{4GM\\omega^2 r}{c^4 d}"
        return formula, {
            "M": chirp_mass, "omega": omega,
            "r_source": r_source, "d": d,
            "numerator": numerator,
            "denominator": denominator,
            "h": h,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate strain computation steps.

        Args:
            data: Solution data with source parameters and strain.

        Returns:
            Steps showing parameters, numerator, denominator, and h.
        """
        m_str = _GRFormatter.format_sci(data["M"])
        d_str = _GRFormatter.format_sci(data["d"])
        num_str = _GRFormatter.format_sci(data["numerator"])
        den_str = _GRFormatter.format_sci(data["denominator"])
        return [
            f"M = {m_str}, \\omega = {_GRFormatter.fmt(data['omega'])} rad/s",
            f"r = {_GRFormatter.format_sci(data['r_source'])} m, d = {d_str} m",
            f"numerator = {num_str}",
            f"denominator = c^4 d = {den_str}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the gravitational wave strain.

        Args:
            data: Solution data.

        Returns:
            String representation of h.
        """
        return f"h = {_GRFormatter.format_sci(data['h'])}"


# ---------------------------------------------------------------------------
# 7. Perihelion precession  (tier 7)
# ---------------------------------------------------------------------------


@register
class PerihelionPrecessionGenerator(StepGenerator):
    """Compute relativistic perihelion precession per orbit.

    Uses delta_phi = 6*pi*G*M / (c^2 * a * (1 - e^2)) to compute
    the GR correction to the orbital precession. Applies to planets
    and binary pulsars.

    Input format:
        ``compute perihelion precession``

    Target format:
        ``\\delta\\phi = \\frac{6\\pi GM}{c^2 a(1-e^2)} <step>
        M = ..., a = ..., e = ... <step>
        c^2 a(1-e^2) = ... <step>
        6\\pi GM = ... <step>
        \\delta\\phi = ... rad/orbit``

    Difficulty scaling:
        d1-3: Mercury-like (a ~ 5.8e10, e ~ 0.2).
        d4-6: close binary (a ~ 1e9, e ~ 0.5).
        d7-8: extreme binary (a ~ 1e8, e ~ 0.8).

    Prerequisites:
        geodesic_schwarzschild.
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "perihelion_precession"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["geodesic_schwarzschild"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls orbital parameters.

        Returns:
            Natural language description.
        """
        return "compute perihelion precession"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate orbital parameters and compute precession.

        Args:
            difficulty: Controls orbit tightness and eccentricity.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            mass = _SOLAR_MASS
            a = round(self._rng.uniform(4e10, 7e10), 0)
            e = round(self._rng.uniform(0.1, 0.3), 2)
        elif difficulty <= 6:
            mass = float(self._rng.randint(1, 5)) * _SOLAR_MASS
            a = round(self._rng.uniform(5e8, 5e9), 0)
            e = round(self._rng.uniform(0.3, 0.6), 2)
        else:
            mass = float(self._rng.randint(1, 9)) * _SOLAR_MASS
            a = round(self._rng.uniform(1e8, 5e8), 0)
            e = round(self._rng.uniform(0.6, 0.9), 2)
        one_minus_e_sq = 1.0 - e * e
        denom = _C_SQ * a * one_minus_e_sq
        numer = 6 * math.pi * _G * mass
        delta_phi = numer / denom
        formula = "\\delta\\phi = \\frac{6\\pi GM}{c^2 a(1-e^2)}"
        return formula, {
            "M": mass, "a": a, "e": e,
            "one_minus_e_sq": round(one_minus_e_sq, 4),
            "numerator": numer, "denominator": denom,
            "delta_phi": delta_phi,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate perihelion precession computation steps.

        Args:
            data: Solution data with orbital params and delta_phi.

        Returns:
            Steps showing parameters, numerator, denominator, and result.
        """
        m_str = _GRFormatter.format_sci(data["M"])
        a_str = _GRFormatter.format_sci(data["a"])
        return [
            f"M = {m_str}, a = {a_str} m, e = {data['e']}",
            f"1 - e^2 = {_GRFormatter.fmt(data['one_minus_e_sq'])}",
            f"6\\pi GM = {_GRFormatter.format_sci(data['numerator'])}",
            f"c^2 a(1-e^2) = {_GRFormatter.format_sci(data['denominator'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the precession per orbit.

        Args:
            data: Solution data.

        Returns:
            String representation of delta_phi.
        """
        return f"\\delta\\phi = {_GRFormatter.format_sci(data['delta_phi'])} rad/orbit"


# ---------------------------------------------------------------------------
# 8. Cosmic distance  (tier 6)
# ---------------------------------------------------------------------------


@register
class CosmicDistanceGenerator(StepGenerator):
    """Compute comoving distance d_C = c * integral(dz / H(z)).

    Uses a simple Hubble parameter model H(z) = H_0 * sqrt(Omega_m*(1+z)^3
    + Omega_Lambda) and performs numerical integration (trapezoidal rule)
    to compute the comoving distance.

    Input format:
        ``compute comoving distance``

    Target format:
        ``d_C = c \\int_0^z \\frac{dz'}{H(z')} <step>
        H_0 = ..., \\Omega_m = ..., \\Omega_\\Lambda = ... <step>
        H(z) = H_0 \\sqrt{\\Omega_m(1+z)^3 + \\Omega_\\Lambda} <step>
        integral \\approx ... <step>
        d_C = c \\times ... = ... Mpc``

    Difficulty scaling:
        d1-3: low redshift (z ~ 0.1-0.5), flat Lambda-CDM.
        d4-6: moderate redshift (z ~ 0.5-2.0).
        d7-8: high redshift (z ~ 2.0-5.0).

    Prerequisites:
        definite_integral.
    """

    _MPC_M = 3.086e22

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "cosmic_distance"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["definite_integral"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls target redshift.

        Returns:
            Natural language description.
        """
        return "compute comoving distance"

    def _hubble(self, z: float, h0: float, omega_m: float,
                omega_l: float) -> float:
        """Compute H(z) for a flat Lambda-CDM model.

        Args:
            z: Redshift.
            h0: Hubble constant in km/s/Mpc.
            omega_m: Matter density parameter.
            omega_l: Dark energy density parameter.

        Returns:
            H(z) in km/s/Mpc.
        """
        return h0 * math.sqrt(omega_m * (1 + z) ** 3 + omega_l)

    def _integrate_trapezoidal(self, z_max: float, h0: float,
                               omega_m: float, omega_l: float,
                               n_steps: int = 100) -> float:
        """Numerically integrate 1/H(z) from 0 to z_max.

        Args:
            z_max: Upper redshift limit.
            h0: Hubble constant in km/s/Mpc.
            omega_m: Matter density parameter.
            omega_l: Dark energy density parameter.
            n_steps: Number of trapezoids.

        Returns:
            Integral value in (km/s/Mpc)^{-1}.
        """
        dz = z_max / n_steps
        total = 0.0
        for i in range(n_steps):
            z0 = i * dz
            z1 = (i + 1) * dz
            f0 = 1.0 / self._hubble(z0, h0, omega_m, omega_l)
            f1 = 1.0 / self._hubble(z1, h0, omega_m, omega_l)
            total += 0.5 * (f0 + f1) * dz
        return total

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate cosmological parameters and compute comoving distance.

        Args:
            difficulty: Controls target redshift.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        h0 = round(self._rng.uniform(65, 75), 1)
        omega_m = round(self._rng.uniform(0.25, 0.35), 2)
        omega_l = round(1.0 - omega_m, 2)
        if difficulty <= 3:
            z_target = round(self._rng.uniform(0.1, 0.5), 2)
        elif difficulty <= 6:
            z_target = round(self._rng.uniform(0.5, 2.0), 2)
        else:
            z_target = round(self._rng.uniform(2.0, 5.0), 2)
        integral_val = self._integrate_trapezoidal(
            z_target, h0, omega_m, omega_l
        )
        c_km = _C / 1000.0
        d_c_mpc = round(c_km * integral_val, 4)
        formula = "d_C = c \\int_0^z \\frac{dz'}{H(z')}"
        return formula, {
            "H_0": h0, "Omega_m": omega_m, "Omega_L": omega_l,
            "z": z_target, "integral": round(integral_val, 4),
            "d_C_Mpc": d_c_mpc,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate comoving distance computation steps.

        Args:
            data: Solution data with cosmological params and distance.

        Returns:
            Steps showing H(z) model, integral, and d_C.
        """
        h0 = data["H_0"]
        om = data["Omega_m"]
        ol = data["Omega_L"]
        z = data["z"]
        return [
            f"H_0 = {h0} km/s/Mpc, \\Omega_m = {om}, \\Omega_\\Lambda = {ol}",
            f"z = {z}",
            f"\\int_0^{{{z}}} dz'/H(z') \\approx {_GRFormatter.fmt(data['integral'])}",
            f"d_C = c \\times {_GRFormatter.fmt(data['integral'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the comoving distance.

        Args:
            data: Solution data.

        Returns:
            String representation of d_C in Mpc.
        """
        return f"d_C = {_GRFormatter.fmt(data['d_C_Mpc'])} Mpc"
