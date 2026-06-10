"""Deep optics generators -- interferometry, fibers, beams, and polarisation.

Extends the optics domain with Michelson interferometer, Fabry-Perot
cavity, Gaussian beam propagation, coherence length, optical fiber
modes, Jones matrix polarisation, Abbe diffraction limit, and prism
dispersion. Tiers range from 4 to 6.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register

_C = 3e8  # speed of light (m/s)


class _OpticsDeepFormatter:
    """Formats numeric values for deep optics problems.

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


_f = _OpticsDeepFormatter.fmt


# ===================================================================
# 1. Michelson interferometer  (tier 5)
# ===================================================================

@register
class MichelsonInterferometerGenerator(StepGenerator):
    """Compute fringe shift in a Michelson interferometer.

    N = 2 * d * n / lambda where d is mirror displacement, n is
    refractive index, and lambda is wavelength.

    Difficulty scaling:
        Difficulty 1-3: n=1 (air), integer displacement in um.
        Difficulty 4-6: n > 1 (glass cell inserted), decimal displacement.
        Difficulty 7-8: given fringe count, solve for displacement.

    Prerequisites:
        division.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "michelson_interferometer"

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
        return "compute fringe shift in Michelson interferometer"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate interferometer parameters and compute fringe shift.

        Args:
            difficulty: Controls refractive index and problem variant.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        lam_nm = self._rng.randint(400, 700)
        lam = lam_nm * 1e-9

        if difficulty <= 3:
            n = 1.0
            d_um = self._rng.randint(1, 50)
            d = d_um * 1e-6
            n_fringes = round(2 * d * n / lam, 4)
            return "N = 2dn/lambda", {
                "lam_nm": lam_nm, "n": n, "d_um": d_um, "d": d,
                "N": n_fringes, "mode": "fringes",
            }
        if difficulty <= 6:
            n = round(self._rng.uniform(1.0, 1.6), 2)
            d_um = round(self._rng.uniform(1.0, 100.0), 1)
            d = d_um * 1e-6
            n_fringes = round(2 * d * n / lam, 4)
            return "N = 2dn/lambda", {
                "lam_nm": lam_nm, "n": n, "d_um": d_um, "d": d,
                "N": n_fringes, "mode": "fringes",
            }
        # Solve for d
        n = 1.0
        n_fringes = self._rng.randint(10, 200)
        d = round(n_fringes * lam / (2 * n), 4)
        d_um = round(d * 1e6, 4)
        return "d = N*lambda/(2n)", {
            "lam_nm": lam_nm, "n": n, "N": n_fringes,
            "d": d, "d_um": d_um, "mode": "find_d",
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate interferometer computation steps.

        Args:
            data: Solution data.

        Returns:
            List of step strings.
        """
        if data["mode"] == "fringes":
            return [
                f"lambda={data['lam_nm']}nm, n={data['n']}, d={data['d_um']}um",
                f"N = 2*{data['d_um']}e-6*{data['n']}/{data['lam_nm']}e-9",
            ]
        return [
            f"N={data['N']}, lambda={data['lam_nm']}nm, n={data['n']}",
            f"d = {data['N']}*{data['lam_nm']}e-9/(2*{data['n']})",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the fringe count or displacement.

        Args:
            data: Solution data.

        Returns:
            Result string.
        """
        if data["mode"] == "fringes":
            return f"N = {_f(data['N'])} fringes"
        return f"d = {_f(data['d_um'])} um"


# ===================================================================
# 2. Fabry-Perot  (tier 6)
# ===================================================================

@register
class FabryPerotGenerator(StepGenerator):
    """Compute Fabry-Perot cavity finesse and free spectral range.

    Finesse F = pi * sqrt(R) / (1 - R). FSR = c / (2 * n * L).
    Given mirror reflectivity R and cavity length L, compute both.

    Difficulty scaling:
        Difficulty 1-3: compute FSR only, integer L in cm.
        Difficulty 4-6: compute finesse and FSR.
        Difficulty 7-8: compute resolving power F * m_max.

    Prerequisites:
        square_root.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "fabry_perot"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

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
        return "compute Fabry-Perot finesse and free spectral range"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate Fabry-Perot parameters.

        Args:
            difficulty: Controls problem complexity.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        r_pct = self._rng.randint(80, 99)
        r = r_pct / 100.0
        l_cm = round(self._rng.uniform(1.0, 20.0), 1)
        l = l_cm * 1e-2
        n = round(self._rng.uniform(1.0, 1.5), 2) if difficulty > 3 else 1.0

        fsr = round(_C / (2 * n * l), 4)
        finesse = round(math.pi * math.sqrt(r) / (1 - r), 4)

        if difficulty <= 3:
            return "FSR = c/(2nL)", {
                "R_pct": r_pct, "R": r, "L_cm": l_cm, "n": n,
                "FSR": fsr, "finesse": finesse, "mode": "fsr",
            }
        if difficulty <= 6:
            return "F = pi*sqrt(R)/(1-R), FSR = c/(2nL)", {
                "R_pct": r_pct, "R": r, "L_cm": l_cm, "n": n,
                "FSR": fsr, "finesse": finesse, "mode": "full",
            }
        # Resolving power
        lam_nm = self._rng.randint(400, 700)
        lam = lam_nm * 1e-9
        m_max = int(2 * n * l / lam)
        resolving_power = round(finesse * m_max, 4)
        return "RP = F * m", {
            "R_pct": r_pct, "R": r, "L_cm": l_cm, "n": n,
            "FSR": fsr, "finesse": finesse,
            "lam_nm": lam_nm, "m_max": m_max,
            "RP": resolving_power, "mode": "resolving",
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Fabry-Perot computation steps.

        Args:
            data: Solution data.

        Returns:
            List of step strings.
        """
        steps = [
            f"R={data['R_pct']}%, L={data['L_cm']}cm, n={data['n']}",
        ]
        if data["mode"] != "fsr":
            steps.append(f"F = pi*sqrt({data['R']})/(1-{data['R']})")
            steps.append(f"F = {_f(data['finesse'])}")
        steps.append(f"FSR = c/(2*{data['n']}*{data['L_cm']}e-2)")
        if data["mode"] == "resolving":
            steps.append(f"m_max = 2nL/lambda = {data['m_max']}")
            steps.append(f"RP = F*m = {_f(data['finesse'])}*{data['m_max']}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return cavity parameters.

        Args:
            data: Solution data.

        Returns:
            Result string with computed values.
        """
        if data["mode"] == "fsr":
            return f"FSR = {_f(data['FSR'])} Hz"
        if data["mode"] == "full":
            return f"F = {_f(data['finesse'])}, FSR = {_f(data['FSR'])} Hz"
        return (
            f"F = {_f(data['finesse'])}, "
            f"RP = {_f(data['RP'])}"
        )


# ===================================================================
# 3. Gaussian beam  (tier 6)
# ===================================================================

@register
class GaussianBeamGenerator(StepGenerator):
    """Compute Gaussian beam parameters: waist, Rayleigh range, divergence.

    w(z) = w_0 * sqrt(1 + (z/z_R)^2) where z_R = pi * w_0^2 / lambda.
    Divergence theta = lambda / (pi * w_0).

    Difficulty scaling:
        Difficulty 1-3: compute z_R from w_0 and lambda.
        Difficulty 4-6: compute w(z) at given distance.
        Difficulty 7-8: compute beam radius, divergence, and spot size.

    Prerequisites:
        square_root.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "gaussian_beam"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

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
        return "compute Gaussian beam waist and divergence"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate Gaussian beam parameters.

        Args:
            difficulty: Controls problem complexity.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        lam_nm = self._rng.randint(400, 1550)
        lam = lam_nm * 1e-9
        w0_um = round(self._rng.uniform(5.0, 500.0), 1)
        w0 = w0_um * 1e-6
        z_r = round(math.pi * w0 ** 2 / lam, 4)

        if difficulty <= 3:
            return "z_R = pi*w_0^2/lambda", {
                "lam_nm": lam_nm, "w0_um": w0_um, "w0": w0,
                "z_R": z_r, "mode": "rayleigh",
            }
        if difficulty <= 6:
            z_cm = round(self._rng.uniform(1.0, 100.0), 1)
            z = z_cm * 1e-2
            w_z = round(w0 * math.sqrt(1 + (z / z_r) ** 2), 4)
            return "w(z) = w_0 sqrt(1 + (z/z_R)^2)", {
                "lam_nm": lam_nm, "w0_um": w0_um, "w0": w0,
                "z_R": z_r, "z_cm": z_cm, "z": z,
                "w_z": w_z, "mode": "spot",
            }
        theta = round(lam / (math.pi * w0), 4)
        theta_mrad = round(theta * 1e3, 4)
        z_cm = round(self._rng.uniform(10.0, 500.0), 1)
        z = z_cm * 1e-2
        w_z = round(w0 * math.sqrt(1 + (z / z_r) ** 2), 4)
        return "theta = lambda/(pi*w_0)", {
            "lam_nm": lam_nm, "w0_um": w0_um, "w0": w0,
            "z_R": z_r, "theta": theta, "theta_mrad": theta_mrad,
            "z_cm": z_cm, "w_z": w_z, "mode": "full",
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Gaussian beam computation steps.

        Args:
            data: Solution data.

        Returns:
            List of step strings.
        """
        steps = [
            f"lambda={data['lam_nm']}nm, w_0={data['w0_um']}um",
            f"z_R = pi*({data['w0_um']}e-6)^2/{data['lam_nm']}e-9"
            f" = {_f(data['z_R'])} m",
        ]
        if data["mode"] == "spot":
            steps.append(f"z = {data['z_cm']}cm")
            steps.append(f"w(z) = {data['w0_um']}e-6 * sqrt(1+(z/z_R)^2)")
        elif data["mode"] == "full":
            steps.append(f"theta = lambda/(pi*w_0) = {_f(data['theta_mrad'])} mrad")
            steps.append(f"w({data['z_cm']}cm) = {_f(data['w_z'])} m")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return beam parameters.

        Args:
            data: Solution data.

        Returns:
            Result string.
        """
        if data["mode"] == "rayleigh":
            return f"z_R = {_f(data['z_R'])} m"
        if data["mode"] == "spot":
            return f"w(z) = {_f(data['w_z'])} m"
        return (
            f"z_R = {_f(data['z_R'])} m, "
            f"theta = {_f(data['theta_mrad'])} mrad"
        )


# ===================================================================
# 4. Coherence length  (tier 5)
# ===================================================================

@register
class CoherenceLengthGenerator(StepGenerator):
    """Compute coherence length of a light source.

    l_c = c / delta_f = lambda^2 / delta_lambda. Given spectral
    bandwidth (in frequency or wavelength), compute coherence length.

    Difficulty scaling:
        Difficulty 1-3: given delta_f directly, compute l_c = c/delta_f.
        Difficulty 4-6: given delta_lambda and lambda, compute l_c.
        Difficulty 7-8: compare coherence lengths of two sources.

    Prerequisites:
        division.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "coherence_length"

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
        return "compute coherence length from spectral bandwidth"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate bandwidth parameters and compute coherence length.

        Args:
            difficulty: Controls bandwidth type and variant.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            # Frequency bandwidth
            df_GHz = self._rng.randint(1, 100)
            df = df_GHz * 1e9
            lc = round(_C / df, 4)
            return "l_c = c/delta_f", {
                "df_GHz": df_GHz, "df": df, "l_c": lc,
                "mode": "freq",
            }
        lam_nm = self._rng.randint(400, 1550)
        lam = lam_nm * 1e-9
        if difficulty <= 6:
            dlam_nm = round(self._rng.uniform(0.01, 10.0), 2)
            dlam = dlam_nm * 1e-9
            lc = round(lam ** 2 / dlam, 4)
            return "l_c = lambda^2/delta_lambda", {
                "lam_nm": lam_nm, "dlam_nm": dlam_nm,
                "l_c": lc, "mode": "wavelength",
            }
        # Compare two sources
        dlam1_nm = round(self._rng.uniform(0.01, 1.0), 2)
        dlam2_nm = round(self._rng.uniform(1.0, 20.0), 1)
        lc1 = round(lam ** 2 / (dlam1_nm * 1e-9), 4)
        lc2 = round(lam ** 2 / (dlam2_nm * 1e-9), 4)
        return "l_c = lambda^2/delta_lambda", {
            "lam_nm": lam_nm,
            "dlam1_nm": dlam1_nm, "dlam2_nm": dlam2_nm,
            "l_c1": lc1, "l_c2": lc2,
            "mode": "compare",
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate coherence length computation steps.

        Args:
            data: Solution data.

        Returns:
            List of step strings.
        """
        if data["mode"] == "freq":
            return [
                f"delta_f = {data['df_GHz']} GHz",
                f"l_c = c/delta_f = {_f(_C)}/{_f(data['df'])}",
            ]
        if data["mode"] == "wavelength":
            return [
                f"lambda={data['lam_nm']}nm, delta_lambda={data['dlam_nm']}nm",
                f"l_c = ({data['lam_nm']}e-9)^2/({data['dlam_nm']}e-9)",
            ]
        return [
            f"lambda = {data['lam_nm']}nm",
            f"Source 1: delta_lambda={data['dlam1_nm']}nm, l_c1={_f(data['l_c1'])}m",
            f"Source 2: delta_lambda={data['dlam2_nm']}nm, l_c2={_f(data['l_c2'])}m",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the coherence length.

        Args:
            data: Solution data.

        Returns:
            Result string with units.
        """
        if data["mode"] == "compare":
            return f"l_c1 = {_f(data['l_c1'])} m, l_c2 = {_f(data['l_c2'])} m"
        return f"l_c = {_f(data['l_c'])} m"


# ===================================================================
# 5. Optical fiber modes  (tier 5)
# ===================================================================

@register
class OpticalFiberModesGenerator(StepGenerator):
    """Compute V-number and number of modes in an optical fiber.

    V = (2*pi*a/lambda) * NA. Number of modes ~ V^2 / 2.
    Single mode if V < 2.405.

    Difficulty scaling:
        Difficulty 1-3: compute V only, given a, lambda, NA.
        Difficulty 4-6: compute V and classify single/multi mode.
        Difficulty 7-8: compute number of modes and cutoff wavelength.

    Prerequisites:
        multiplication.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "optical_fiber_modes"

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
        return "compute V-number and modes in optical fiber"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate fiber parameters and compute V-number.

        Args:
            difficulty: Controls problem complexity.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        a_um = round(self._rng.uniform(2.0, 50.0), 1)
        a = a_um * 1e-6
        lam_nm = self._rng.randint(800, 1550)
        lam = lam_nm * 1e-9
        na = round(self._rng.uniform(0.1, 0.3), 2)

        v = round(2 * math.pi * a * na / lam, 4)
        single_mode = v < 2.405
        n_modes = max(1, int(v ** 2 / 2))

        if difficulty <= 3:
            return "V = 2*pi*a*NA/lambda", {
                "a_um": a_um, "lam_nm": lam_nm, "NA": na,
                "V": v, "mode": "V_only",
            }
        if difficulty <= 6:
            return "V = 2*pi*a*NA/lambda", {
                "a_um": a_um, "lam_nm": lam_nm, "NA": na,
                "V": v, "single_mode": single_mode,
                "mode": "classify",
            }
        # Cutoff wavelength for single mode
        lam_c = round(2 * math.pi * a * na / 2.405, 4)
        lam_c_nm = round(lam_c * 1e9, 4)
        return "lambda_c = 2*pi*a*NA/2.405", {
            "a_um": a_um, "lam_nm": lam_nm, "NA": na,
            "V": v, "N_modes": n_modes,
            "lam_c_nm": lam_c_nm, "mode": "cutoff",
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate fiber mode computation steps.

        Args:
            data: Solution data.

        Returns:
            List of step strings.
        """
        steps = [
            f"a={data['a_um']}um, lambda={data['lam_nm']}nm, NA={data['NA']}",
            f"V = 2*pi*{data['a_um']}e-6*{data['NA']}/{data['lam_nm']}e-9"
            f" = {_f(data['V'])}",
        ]
        if data["mode"] == "classify":
            label = "single-mode" if data["single_mode"] else "multi-mode"
            steps.append(f"V {'<' if data['single_mode'] else '>'} 2.405 => {label}")
        elif data["mode"] == "cutoff":
            steps.append(f"N_modes ~ V^2/2 = {data['N_modes']}")
            steps.append(f"lambda_c = 2*pi*a*NA/2.405 = {_f(data['lam_c_nm'])} nm")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return V-number and mode classification.

        Args:
            data: Solution data.

        Returns:
            Result string.
        """
        if data["mode"] == "V_only":
            return f"V = {_f(data['V'])}"
        if data["mode"] == "classify":
            label = "single-mode" if data["single_mode"] else "multi-mode"
            return f"V = {_f(data['V'])}, {label}"
        return (
            f"V = {_f(data['V'])}, N = {data['N_modes']}, "
            f"lambda_c = {_f(data['lam_c_nm'])} nm"
        )


# ===================================================================
# 6. Jones matrix  (tier 5)
# ===================================================================

@register
class JonesMatrixGenerator(StepGenerator):
    """Apply Jones matrix to compute output polarisation state.

    Polariser: [[1,0],[0,0]]. QWP at 0 deg: [[1,0],[0,j]].
    HWP at 0 deg: [[1,0],[0,-1]]. Apply to input Jones vector
    [Ex, Ey] via matrix multiplication.

    Difficulty scaling:
        Difficulty 1-3: horizontal polariser on linearly polarised input.
        Difficulty 4-6: QWP applied to 45-degree linear polarisation.
        Difficulty 7-8: cascaded elements (polariser + QWP).

    Prerequisites:
        multiplication.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "jones_matrix"

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
        return "apply Jones matrix to polarisation state"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate Jones vector and optical element.

        Args:
            difficulty: Controls element type and complexity.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            # Linear polariser on arbitrary linear input
            theta_deg = self._rng.choice([0, 30, 45, 60, 90])
            theta = math.radians(theta_deg)
            ex = round(math.cos(theta), 4)
            ey = round(math.sin(theta), 4)
            # H-polariser: output = [ex, 0]
            out_x = ex
            out_y = 0.0
            intensity = round(out_x ** 2 + out_y ** 2, 4)
            return "J_out = P_H * J_in", {
                "theta_deg": theta_deg, "Ex": ex, "Ey": ey,
                "out_x": round(out_x, 4), "out_y": out_y,
                "I_out": intensity, "element": "H-polariser",
                "mode": "polariser",
            }
        if difficulty <= 6:
            # QWP on 45-degree linear
            ex = round(1 / math.sqrt(2), 4)
            ey = round(1 / math.sqrt(2), 4)
            # QWP: [ex, j*ey] => circular
            out_x = ex
            out_y_imag = ey  # imaginary part
            intensity = round(out_x ** 2 + out_y_imag ** 2, 4)
            return "J_out = QWP * J_in", {
                "Ex": ex, "Ey": ey,
                "out_x": out_x, "out_y_imag": round(out_y_imag, 4),
                "I_out": intensity, "element": "QWP",
                "mode": "qwp",
            }
        # Cascaded: polariser then QWP
        theta_deg = self._rng.choice([30, 45, 60])
        theta = math.radians(theta_deg)
        ex = round(math.cos(theta), 4)
        ey = round(math.sin(theta), 4)
        # After H-polariser
        mid_x = ex
        mid_y = 0.0
        # After QWP
        out_x = mid_x
        out_y_imag = 0.0
        intensity = round(out_x ** 2, 4)
        return "J_out = QWP * P_H * J_in", {
            "theta_deg": theta_deg, "Ex": ex, "Ey": ey,
            "mid_x": round(mid_x, 4), "mid_y": mid_y,
            "out_x": round(out_x, 4), "out_y_imag": out_y_imag,
            "I_out": intensity, "element": "H-pol+QWP",
            "mode": "cascade",
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Jones matrix computation steps.

        Args:
            data: Solution data.

        Returns:
            List of step strings.
        """
        steps = [f"J_in = [{_f(data['Ex'])}, {_f(data['Ey'])}]"]
        if data["mode"] == "polariser":
            steps.append(f"P_H = [[1,0],[0,0]]")
            steps.append(f"J_out = [{_f(data['out_x'])}, {_f(data['out_y'])}]")
        elif data["mode"] == "qwp":
            steps.append(f"QWP = [[1,0],[0,j]]")
            steps.append(f"J_out = [{_f(data['out_x'])}, j*{_f(data['out_y_imag'])}]")
        else:
            steps.append(f"After P_H: [{_f(data['mid_x'])}, 0]")
            steps.append(f"After QWP: [{_f(data['out_x'])}, j*{_f(data['out_y_imag'])}]")
        steps.append(f"I = |Ex|^2+|Ey|^2 = {_f(data['I_out'])}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the output Jones vector and intensity.

        Args:
            data: Solution data.

        Returns:
            Result string.
        """
        return f"I_out = {_f(data['I_out'])}"


# ===================================================================
# 7. Abbe diffraction limit  (tier 4)
# ===================================================================

@register
class AbbeDiffractionLimitGenerator(StepGenerator):
    """Compute Abbe diffraction-limited resolution.

    d_min = lambda / (2 * NA). Given wavelength and numerical
    aperture, compute the minimum resolvable feature size.

    Difficulty scaling:
        Difficulty 1-3: visible light, standard NA, compute d_min.
        Difficulty 4-6: vary NA and wavelength, also compute in um.
        Difficulty 7-8: given d_min, solve for required NA or lambda.

    Prerequisites:
        division.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "abbe_diffraction_limit"

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
        return "compute Abbe diffraction limit for microscope"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate microscope parameters and compute resolution.

        Args:
            difficulty: Controls problem variant.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        lam_nm = self._rng.randint(400, 700)
        lam = lam_nm * 1e-9
        na = round(self._rng.uniform(0.1, 1.4), 2)

        d_min = round(lam / (2 * na), 4)
        d_min_nm = round(d_min * 1e9, 4)

        if difficulty <= 6:
            return "d_min = lambda/(2*NA)", {
                "lam_nm": lam_nm, "NA": na,
                "d_min": d_min, "d_min_nm": d_min_nm,
                "mode": "compute",
            }
        # Solve for NA given d_min
        target_d_nm = self._rng.randint(150, 500)
        target_d = target_d_nm * 1e-9
        na_needed = round(lam / (2 * target_d), 4)
        return "NA = lambda/(2*d_min)", {
            "lam_nm": lam_nm, "target_d_nm": target_d_nm,
            "NA_needed": na_needed, "mode": "find_NA",
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Abbe limit computation steps.

        Args:
            data: Solution data.

        Returns:
            List of step strings.
        """
        if data["mode"] == "compute":
            return [
                f"lambda={data['lam_nm']}nm, NA={data['NA']}",
                f"d_min = {data['lam_nm']}e-9/(2*{data['NA']})",
                f"d_min = {_f(data['d_min_nm'])} nm",
            ]
        return [
            f"lambda={data['lam_nm']}nm, target d={data['target_d_nm']}nm",
            f"NA = {data['lam_nm']}e-9/(2*{data['target_d_nm']}e-9)",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the resolution limit or required NA.

        Args:
            data: Solution data.

        Returns:
            Result string.
        """
        if data["mode"] == "compute":
            return f"d_min = {_f(data['d_min_nm'])} nm"
        return f"NA = {_f(data['NA_needed'])}"


# ===================================================================
# 8. Prism dispersion  (tier 5)
# ===================================================================

@register
class PrismDispersionGenerator(StepGenerator):
    """Compute prism deviation and angular dispersion.

    For a thin prism: delta = (n - 1) * A where A is the apex angle.
    Angular dispersion: d(delta)/d(lambda) = A * dn/d(lambda).

    Difficulty scaling:
        Difficulty 1-3: compute deviation delta for given n and A.
        Difficulty 4-6: compute deviation and angular dispersion.
        Difficulty 7-8: compute for two wavelengths and find delta(delta).

    Prerequisites:
        multiplication.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "prism_dispersion"

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
        return "compute prism deviation and angular dispersion"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate prism parameters and compute deviation.

        Args:
            difficulty: Controls problem complexity.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        a_deg = self._rng.randint(5, 15)
        a_rad = math.radians(a_deg)
        n = round(self._rng.uniform(1.4, 1.8), 3)

        delta_rad = (n - 1) * a_rad
        delta_deg = round(math.degrees(delta_rad), 4)

        if difficulty <= 3:
            return "delta = (n-1)*A", {
                "A_deg": a_deg, "n": n, "delta_deg": delta_deg,
                "mode": "deviation",
            }
        # Angular dispersion
        dn_dlam = round(self._rng.uniform(-0.05, -0.005), 4)
        # dn/dlambda in 1/nm, angular dispersion in deg/nm
        ang_disp = round(a_rad * dn_dlam, 4)  # rad/nm
        ang_disp_deg = round(math.degrees(ang_disp), 4)

        if difficulty <= 6:
            return "delta = (n-1)*A, D = A*dn/dlambda", {
                "A_deg": a_deg, "n": n, "delta_deg": delta_deg,
                "dn_dlam": dn_dlam, "ang_disp_deg": ang_disp_deg,
                "mode": "dispersion",
            }
        # Two wavelengths
        n2 = round(n + dn_dlam * self._rng.randint(50, 200), 3)
        delta2_deg = round(math.degrees((n2 - 1) * a_rad), 4)
        dd = round(abs(delta_deg - delta2_deg), 4)
        return "delta = (n-1)*A for two wavelengths", {
            "A_deg": a_deg, "n1": n, "n2": n2,
            "delta1_deg": delta_deg, "delta2_deg": delta2_deg,
            "dd_deg": dd, "mode": "two_wave",
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate prism dispersion computation steps.

        Args:
            data: Solution data.

        Returns:
            List of step strings.
        """
        if data["mode"] == "deviation":
            return [
                f"A={data['A_deg']}deg, n={data['n']}",
                f"delta = ({data['n']}-1)*{data['A_deg']}",
            ]
        if data["mode"] == "dispersion":
            return [
                f"A={data['A_deg']}deg, n={data['n']}",
                f"delta = {_f(data['delta_deg'])} deg",
                f"dn/dlambda = {data['dn_dlam']} /nm",
                f"D = A*dn/dlambda = {_f(data['ang_disp_deg'])} deg/nm",
            ]
        return [
            f"A={data['A_deg']}deg",
            f"n1={data['n1']}: delta1={_f(data['delta1_deg'])} deg",
            f"n2={data['n2']}: delta2={_f(data['delta2_deg'])} deg",
            f"|delta1-delta2| = {_f(data['dd_deg'])} deg",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the deviation and/or dispersion.

        Args:
            data: Solution data.

        Returns:
            Result string.
        """
        if data["mode"] == "deviation":
            return f"delta = {_f(data['delta_deg'])} deg"
        if data["mode"] == "dispersion":
            return (
                f"delta = {_f(data['delta_deg'])} deg, "
                f"D = {_f(data['ang_disp_deg'])} deg/nm"
            )
        return f"angular spread = {_f(data['dd_deg'])} deg"
