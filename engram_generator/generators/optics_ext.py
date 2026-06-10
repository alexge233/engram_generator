"""Extended optics generators -- lensmaker, diffraction, polarisation, mirrors.

Deepens the optics domain with the lensmaker's equation, two-lens
systems, single-slit diffraction, thin-film interference, Malus's
law for polarisation, Rayleigh resolving power, optical path length,
and the mirror equation. Tiers range from 4 to 5.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


class _OpticsExtFormatter:
    """Formats numeric values for extended optics problems.

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


_f = _OpticsExtFormatter.fmt


# ===================================================================
# 1. Lensmaker's equation  (tier 5)
# ===================================================================

@register
class LensMakersGenerator(StepGenerator):
    """Lensmaker's equation: 1/f = (n-1)*(1/R1 - 1/R2).

    Given refractive index n and radii of curvature R1, R2,
    computes the focal length f of the lens.

    Difficulty scaling:
        Difficulty 1-3: biconvex lens, R1>0, R2<0.
        Difficulty 4-6: plano-convex or meniscus.
        Difficulty 7-8: solve for n given f and radii.

    Prerequisites:
        snells_law.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "lens_makers"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["snells_law"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute focal length using lensmaker's equation"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate lens parameters and compute focal length.

        Args:
            difficulty: Controls lens type and problem variant.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        n = round(self._rng.uniform(1.4, 1.8), 2)

        if difficulty <= 3:
            r1 = self._rng.randint(10, 50)
            r2 = -self._rng.randint(10, 50)
        elif difficulty <= 6:
            choice = self._rng.choice(["plano", "meniscus"])
            if choice == "plano":
                r1 = self._rng.randint(10, 50)
                r2 = float("inf")
            else:
                r1 = self._rng.randint(10, 40)
                r2 = self._rng.randint(r1 + 5, 80)
        else:
            r1 = self._rng.randint(10, 50)
            r2 = -self._rng.randint(10, 50)

        nm1 = round(n - 1, 4)
        inv_r1 = round(1.0 / r1, 4) if r1 != float("inf") else 0.0
        inv_r2 = round(1.0 / r2, 4) if r2 != float("inf") else 0.0
        inv_f = round(nm1 * (inv_r1 - inv_r2), 4)
        f = round(1.0 / inv_f, 4) if abs(inv_f) > 1e-8 else float("inf")

        target = "n" if difficulty >= 7 else "f"

        return "\\frac{1}{f} = (n-1)(\\frac{1}{R_1} - \\frac{1}{R_2})", {
            "n": n, "R1": r1, "R2": r2,
            "nm1": nm1, "inv_R1": inv_r1, "inv_R2": inv_r2,
            "inv_f": inv_f, "f": f, "target": target,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate lensmaker computation steps.

        Args:
            data: Solution data with n, R1, R2.

        Returns:
            List of step strings.
        """
        r2_str = _f(data['R2']) if data['R2'] != float("inf") else "inf"
        diff = round(data["inv_R1"] - data["inv_R2"], 4)
        if data["target"] == "f":
            return [
                f"n={data['n']}, R1={data['R1']}cm, R2={r2_str}cm",
                f"1/R1 - 1/R2 = {_f(data['inv_R1'])} - {_f(data['inv_R2'])} = {_f(diff)}",
                f"1/f = {_f(data['nm1'])}*{_f(diff)} = {_f(data['inv_f'])}",
            ]
        return [
            f"f={_f(data['f'])}cm, R1={data['R1']}cm, R2={r2_str}cm",
            f"n-1 = (1/f)/(1/R1-1/R2) = {_f(data['inv_f'])}/{_f(diff)}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the focal length or refractive index.

        Args:
            data: Solution data.

        Returns:
            String with the result.
        """
        if data["target"] == "f":
            return f"f = {_f(data['f'])} cm"
        return f"n = {_f(data['n'])}"


# ===================================================================
# 2. Two-lens system  (tier 5)
# ===================================================================

@register
class TwoLensSystemGenerator(StepGenerator):
    """Two-lens system: image from lens 1 is object for lens 2.

    Given focal lengths f1, f2 and object distance do1, separation d,
    computes final image position and total magnification.

    Difficulty scaling:
        Difficulty 1-3: both convex, real images.
        Difficulty 4-6: one concave lens.
        Difficulty 7-8: virtual intermediate image.

    Prerequisites:
        thin_lens.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "two_lens_system"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["thin_lens"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute image position in two-lens system"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate two-lens parameters and trace the image.

        Args:
            difficulty: Controls lens types.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        f1 = self._rng.randint(5, 20)
        if difficulty <= 3:
            f2 = self._rng.randint(5, 20)
        else:
            f2 = self._rng.choice([-15, -10, 8, 10, 15, 20])

        do1 = self._rng.randint(f1 + 2, f1 + 30)
        di1 = round(1.0 / (1.0 / f1 - 1.0 / do1), 4)
        m1 = round(-di1 / do1, 4)

        sep = self._rng.randint(max(5, int(abs(di1)) + 2), int(abs(di1)) + 30)
        do2 = round(sep - di1, 4)

        if abs(1.0 / f2 - 1.0 / do2) < 1e-8:
            do2 = do2 + 1

        di2 = round(1.0 / (1.0 / f2 - 1.0 / do2), 4)
        m2 = round(-di2 / do2, 4)
        m_total = round(m1 * m2, 4)

        return "\\frac{1}{f} = \\frac{1}{d_o} + \\frac{1}{d_i}", {
            "f1": f1, "f2": f2, "do1": do1,
            "di1": di1, "m1": m1, "sep": sep,
            "do2": do2, "di2": di2, "m2": m2,
            "M_total": m_total,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate two-lens system computation steps.

        Args:
            data: Solution data with lens parameters.

        Returns:
            List of step strings.
        """
        return [
            f"Lens 1: f1={data['f1']}cm, do1={data['do1']}cm",
            f"di1 = 1/(1/f1-1/do1) = {_f(data['di1'])} cm",
            f"M1 = -{_f(data['di1'])}/{data['do1']} = {_f(data['m1'])}",
            f"do2 = sep-di1 = {data['sep']}-{_f(data['di1'])} = {_f(data['do2'])} cm",
            f"di2 = 1/(1/{data['f2']}-1/{_f(data['do2'])}) = {_f(data['di2'])} cm",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the final image position and total magnification.

        Args:
            data: Solution data.

        Returns:
            String with di2 and M_total.
        """
        return f"di2 = {_f(data['di2'])} cm, M = {_f(data['M_total'])}"


# ===================================================================
# 3. Single-slit diffraction  (tier 5)
# ===================================================================

@register
class SingleSlitDiffractionGenerator(StepGenerator):
    """Single-slit diffraction: minima at a*sin(theta) = m*lambda.

    Central maximum angular width = 2*lambda/a (small angle).
    On a screen at distance L, central width = 2*lambda*L/a.

    Difficulty scaling:
        Difficulty 1-3: compute first minimum angle.
        Difficulty 4-6: compute central maximum width on screen.
        Difficulty 7-8: compute m-th minimum position.

    Prerequisites:
        sin_cos_eval.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "single_slit_diffraction"

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
        return "compute single-slit diffraction pattern"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate slit parameters and compute diffraction quantities.

        Args:
            difficulty: Controls problem variant.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        lam_nm = self._rng.randint(400, 700)
        lam = lam_nm * 1e-9
        a_um = self._rng.randint(10, 100 + difficulty * 20)
        a = a_um * 1e-6
        l_m = round(self._rng.uniform(0.5, 3.0), 1)

        if difficulty <= 3:
            m = 1
        else:
            m = self._rng.randint(1, min(3, difficulty))

        sin_theta = m * lam / a
        sin_theta = min(sin_theta, 0.999)
        theta = round(math.degrees(math.asin(sin_theta)), 4)
        central_width = round(2 * lam * l_m / a, 4)

        if difficulty <= 3:
            target = "theta"
        elif difficulty <= 6:
            target = "central_width"
        else:
            target = "position"

        y_m = round(m * lam * l_m / a, 4)

        return "a \\sin\\theta = m\\lambda", {
            "lam_nm": lam_nm, "lam": lam,
            "a_um": a_um, "a": a,
            "L": l_m, "m": m,
            "sin_theta": round(sin_theta, 4),
            "theta": theta,
            "central_width": central_width,
            "y_m": y_m, "target": target,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate single-slit diffraction steps.

        Args:
            data: Solution data with slit and wavelength.

        Returns:
            List of step strings.
        """
        steps = [
            f"lambda={data['lam_nm']}nm, a={data['a_um']}um, L={data['L']}m",
        ]
        if data["target"] == "theta":
            steps.append(f"sin(theta) = m*lambda/a = {data['m']}*{data['lam_nm']}e-9/{data['a']}")
            steps.append(f"theta = arcsin({_f(data['sin_theta'])})")
        elif data["target"] == "central_width":
            steps.append(f"w = 2*lambda*L/a = 2*{data['lam_nm']}e-9*{data['L']}/{data['a']}")
        else:
            steps.append(f"y_{data['m']} = m*lambda*L/a = {data['m']}*{data['lam_nm']}e-9*{data['L']}/{data['a']}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the diffraction result.

        Args:
            data: Solution data.

        Returns:
            String with angle, width, or position.
        """
        if data["target"] == "theta":
            return f"theta_1 = {_f(data['theta'])} deg"
        if data["target"] == "central_width":
            return f"central width = {_f(data['central_width'])} m"
        return f"y_{data['m']} = {_f(data['y_m'])} m"


# ===================================================================
# 4. Thin-film interference  (tier 5)
# ===================================================================

@register
class ThinFilmInterferenceGenerator(StepGenerator):
    """Thin-film interference: constructive 2nt = (m+1/2)*lambda.

    For light reflected from a thin film of refractive index n and
    thickness t, finds wavelengths that interfere constructively
    or destructively.

    Difficulty scaling:
        Difficulty 1-3: m=0, find lambda for constructive.
        Difficulty 4-6: m=0 or 1, choose constructive or destructive.
        Difficulty 7-8: solve for film thickness given lambda.

    Prerequisites:
        multiplication.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "thin_film_interference"

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
        return "compute thin-film interference condition"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate thin-film parameters and compute interference.

        Args:
            difficulty: Controls order and problem variant.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        n = round(self._rng.uniform(1.2, 1.8), 2)
        t_nm = self._rng.randint(100, 600)
        t = t_nm * 1e-9

        if difficulty <= 3:
            m = 0
            mode = "constructive"
        elif difficulty <= 6:
            m = self._rng.randint(0, 1)
            mode = self._rng.choice(["constructive", "destructive"])
        else:
            m = self._rng.randint(0, 2)
            mode = "constructive"

        two_nt = round(2 * n * t, 4)
        if mode == "constructive":
            lam = round(two_nt / (m + 0.5), 4)
        else:
            lam = round(two_nt / max(m, 1), 4) if m > 0 else round(two_nt, 4)

        lam_nm = round(lam * 1e9, 1)

        if difficulty >= 7:
            target = "t"
        else:
            target = "lambda"

        return "2nt = (m + \\frac{1}{2})\\lambda", {
            "n": n, "t_nm": t_nm, "t": t,
            "m": m, "mode": mode,
            "two_nt": two_nt,
            "lam": lam, "lam_nm": lam_nm,
            "target": target,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate thin-film interference steps.

        Args:
            data: Solution data with film and wavelength.

        Returns:
            List of step strings.
        """
        steps = [
            f"n={data['n']}, t={data['t_nm']}nm, m={data['m']}",
            f"2nt = 2*{data['n']}*{data['t_nm']}e-9 = {_f(data['two_nt'])}",
        ]
        if data["mode"] == "constructive":
            steps.append(f"{data['mode']}: lambda = 2nt/(m+0.5) = {_f(data['two_nt'])}/{data['m']+0.5}")
        else:
            steps.append(f"{data['mode']}: lambda = 2nt/m = {_f(data['two_nt'])}/{data['m']}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the wavelength or thickness.

        Args:
            data: Solution data.

        Returns:
            String with result.
        """
        if data["target"] == "lambda":
            return f"lambda = {_f(data['lam_nm'])} nm ({data['mode']})"
        return f"t = {data['t_nm']} nm"


# ===================================================================
# 5. Polarisation (Malus's law)  (tier 4)
# ===================================================================

@register
class PolarizationGenerator(StepGenerator):
    """Malus's law: I = I_0 * cos^2(theta).

    Computes transmitted intensity through one or more polarisers.
    For N polarisers in series, applies Malus's law sequentially.

    Difficulty scaling:
        Difficulty 1-3: single polariser, standard angles.
        Difficulty 4-6: two polarisers in series.
        Difficulty 7-8: three polarisers, compute final intensity.

    Prerequisites:
        sin_cos_eval.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "polarization"

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
        return "compute transmitted intensity using Malus's law"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate polariser angles and compute transmitted intensity.

        Args:
            difficulty: Controls number of polarisers.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        i0 = round(self._rng.uniform(10.0, 100.0), 1)

        if difficulty <= 3:
            angles = [self._rng.randint(10, 80)]
        elif difficulty <= 6:
            angles = [self._rng.randint(10, 60), self._rng.randint(10, 60)]
        else:
            angles = [self._rng.randint(10, 50) for _ in range(3)]

        intensities = [i0]
        for angle in angles:
            cos_val = math.cos(math.radians(angle))
            i_next = round(intensities[-1] * cos_val ** 2, 4)
            intensities.append(i_next)

        cos_vals = [round(math.cos(math.radians(a)), 4) for a in angles]
        cos_sq = [round(c ** 2, 4) for c in cos_vals]

        return "I = I_0 \\cos^2\\theta", {
            "I0": i0, "angles": angles,
            "cos_vals": cos_vals, "cos_sq": cos_sq,
            "intensities": intensities,
            "I_final": intensities[-1],
            "n_polarisers": len(angles),
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Malus's law computation steps.

        Args:
            data: Solution data with angles and intensities.

        Returns:
            List of step strings.
        """
        steps = [f"I_0 = {data['I0']} W/m^2"]
        for i, (angle, cos_sq, i_out) in enumerate(
            zip(data["angles"], data["cos_sq"], data["intensities"][1:])
        ):
            steps.append(
                f"P{i+1}: cos^2({angle}deg) = {_f(cos_sq)}, "
                f"I = {_f(data['intensities'][i])}*{_f(cos_sq)} = {_f(i_out)}"
            )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the final transmitted intensity.

        Args:
            data: Solution data.

        Returns:
            String with I_final.
        """
        return f"I = {_f(data['I_final'])} W/m^2"


# ===================================================================
# 6. Resolving power (Rayleigh criterion)  (tier 5)
# ===================================================================

@register
class ResolvingPowerGenerator(StepGenerator):
    """Rayleigh criterion: theta_min = 1.22 * lambda / D.

    Computes the minimum angular resolution of a circular aperture
    given wavelength and aperture diameter.

    Difficulty scaling:
        Difficulty 1-3: visible light, telescope-scale apertures.
        Difficulty 4-6: varied wavelengths, smaller apertures.
        Difficulty 7-8: compute minimum separation at distance L.

    Prerequisites:
        division.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "resolving_power"

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
        return "compute angular resolution using Rayleigh criterion"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate aperture and wavelength, compute resolution.

        Args:
            difficulty: Controls ranges and problem variant.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        lam_nm = self._rng.randint(400, 700)
        lam = lam_nm * 1e-9
        d_cm = round(self._rng.uniform(1.0, 50.0 + difficulty * 10), 1)
        d = d_cm * 1e-2

        theta_rad = round(1.22 * lam / d, 4)
        theta_arcsec = round(theta_rad * 206265, 4)

        data = {
            "lam_nm": lam_nm, "lam": lam,
            "D_cm": d_cm, "D": d,
            "theta_rad": theta_rad,
            "theta_arcsec": theta_arcsec,
        }

        if difficulty >= 7:
            dist = self._rng.randint(100, 10000)
            min_sep = round(theta_rad * dist, 4)
            data["distance"] = dist
            data["min_sep"] = min_sep

        return "\\theta_{min} = 1.22 \\frac{\\lambda}{D}", data

    def _create_steps(self, data: dict) -> list[str]:
        """Generate resolving power computation steps.

        Args:
            data: Solution data with aperture and wavelength.

        Returns:
            List of step strings.
        """
        steps = [
            f"lambda = {data['lam_nm']} nm, D = {data['D_cm']} cm",
            f"theta = 1.22*{data['lam_nm']}e-9/{data['D']}",
            f"theta = {_f(data['theta_rad'])} rad = {_f(data['theta_arcsec'])} arcsec",
        ]
        if "distance" in data:
            steps.append(
                f"min sep at {data['distance']}m = {_f(data['theta_rad'])}*{data['distance']} = {_f(data['min_sep'])} m"
            )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the angular resolution.

        Args:
            data: Solution data.

        Returns:
            String with theta_min.
        """
        ans = f"theta_min = {_f(data['theta_rad'])} rad"
        if "min_sep" in data:
            ans += f", min_sep = {_f(data['min_sep'])} m"
        return ans


# ===================================================================
# 7. Optical path length  (tier 4)
# ===================================================================

@register
class OpticalPathLengthGenerator(StepGenerator):
    """Optical path length: OPL = sum(n_i * d_i).

    For one or more media, computes the total optical path length
    and the phase difference = 2*pi*OPL/lambda.

    Difficulty scaling:
        Difficulty 1-3: single medium.
        Difficulty 4-6: two media.
        Difficulty 7-8: three media, compute phase difference.

    Prerequisites:
        multiplication.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "optical_path_length"

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
        return "compute optical path length and phase difference"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate media stack and compute OPL and phase.

        Args:
            difficulty: Controls number of media.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            num_media = 1
        elif difficulty <= 6:
            num_media = 2
        else:
            num_media = 3

        lam_nm = self._rng.randint(400, 700)
        lam = lam_nm * 1e-9

        media = []
        opl = 0.0
        for _ in range(num_media):
            n = round(self._rng.uniform(1.0, 2.0), 2)
            d_mm = round(self._rng.uniform(0.1, 5.0), 2)
            d = d_mm * 1e-3
            contrib = round(n * d, 4)
            opl += contrib
            media.append({"n": n, "d_mm": d_mm, "d": d, "nd": contrib})

        opl = round(opl, 4)
        phase = round(2 * math.pi * opl / lam, 4)

        return "OPL = \\sum n_i d_i", {
            "media": media, "num_media": num_media,
            "lam_nm": lam_nm, "lam": lam,
            "OPL": opl, "phase": phase,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate OPL computation steps.

        Args:
            data: Solution data with media stack.

        Returns:
            List of step strings.
        """
        steps = []
        for i, m in enumerate(data["media"]):
            steps.append(f"layer {i+1}: n={m['n']}, d={m['d_mm']}mm, n*d={_f(m['nd'])}")
        steps.append(f"OPL = {_f(data['OPL'])} m")
        steps.append(f"phase = 2*pi*{_f(data['OPL'])}/{data['lam_nm']}e-9")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the OPL and phase difference.

        Args:
            data: Solution data.

        Returns:
            String with OPL and phase.
        """
        return f"OPL = {_f(data['OPL'])} m, phase = {_f(data['phase'])} rad"


# ===================================================================
# 8. Mirror equation  (tier 4)
# ===================================================================

@register
class MirrorEquationGenerator(StepGenerator):
    """Spherical mirror equation: 1/f = 1/do + 1/di, f = R/2.

    Given radius of curvature R and object distance do, computes
    the image distance di and magnification M = -di/do.

    Difficulty scaling:
        Difficulty 1-3: concave mirror, real image.
        Difficulty 4-6: convex mirror, virtual image.
        Difficulty 7-8: solve for R given do and di.

    Prerequisites:
        division.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "mirror_equation"

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
        return "apply spherical mirror equation"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate mirror parameters and compute image position.

        Args:
            difficulty: Controls mirror type and problem variant.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            r = self._rng.randint(10, 40)
        else:
            r = self._rng.choice([-30, -20, -10, 10, 20, 30, 40])

        f = round(r / 2, 4)
        do = self._rng.randint(abs(f) + 2, abs(f) + 40)

        inv_di = round(1.0 / f - 1.0 / do, 4)
        if abs(inv_di) < 1e-8:
            do = do + 1
            inv_di = round(1.0 / f - 1.0 / do, 4)
        di = round(1.0 / inv_di, 4)
        m = round(-di / do, 4)
        image_type = "real" if di > 0 else "virtual"

        target = "R" if difficulty >= 7 else "di"

        return "\\frac{1}{f} = \\frac{1}{d_o} + \\frac{1}{d_i}", {
            "R": r, "f": f, "do": do, "di": di,
            "inv_di": inv_di, "M": m,
            "image_type": image_type, "target": target,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate mirror equation computation steps.

        Args:
            data: Solution data with R, f, do, di.

        Returns:
            List of step strings.
        """
        if data["target"] == "di":
            return [
                f"R={data['R']}cm, f=R/2={_f(data['f'])}cm",
                f"do={data['do']}cm",
                f"1/di = 1/f - 1/do = {_f(data['inv_di'])}",
                f"M = -di/do = {_f(data['M'])}",
            ]
        return [
            f"do={data['do']}cm, di={_f(data['di'])}cm",
            f"1/f = 1/do + 1/di = {_f(round(1.0/data['f'], 4))}",
            f"R = 2f = 2*{_f(data['f'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the image position and magnification or radius.

        Args:
            data: Solution data.

        Returns:
            String with result.
        """
        if data["target"] == "di":
            return (
                f"di = {_f(data['di'])} cm ({data['image_type']}), "
                f"M = {_f(data['M'])}"
            )
        return f"R = {data['R']} cm"
