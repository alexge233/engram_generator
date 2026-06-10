"""Antenna theory generators -- directivity through effective aperture.

Covers antenna directivity, gain-efficiency relation, Friis transmission
equation, half-wave dipole radiation patterns, uniform linear array factors,
and effective aperture. Tiers range from 5 (introductory antenna parameters)
to 6 (array processing).
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


class _AntennaFormatter:
    """Formats numeric values for antenna theory problems.

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


_f = _AntennaFormatter.fmt


# ===================================================================
# 1. Antenna directivity  (tier 5)
# ===================================================================

@register
class AntennaDirectivityGenerator(StepGenerator):
    """Compute antenna directivity from radiation pattern peak and total power.

    D = 4*pi*U_max / P_rad, and also D_dBi = 10*log10(D).

    Difficulty scaling:
        Difficulty 1-3: integer U_max and P_rad values.
        Difficulty 4-6: decimal values, wider ranges.
        Difficulty 7-8: small P_rad requiring careful division.

    Prerequisites:
        division.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "antenna_directivity"

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
        return "compute antenna directivity and express in dBi"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate radiation intensity peak and total power, compute D.

        Args:
            difficulty: Controls parameter magnitude and precision.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            u_max = float(self._rng.randint(1, 10 + difficulty * 5))
            p_rad = float(self._rng.randint(1, 5 + difficulty * 3))
        elif difficulty <= 6:
            u_max = round(self._rng.uniform(0.5, 20.0 + difficulty * 5), 2)
            p_rad = round(self._rng.uniform(0.5, 10.0 + difficulty * 2), 2)
        else:
            u_max = round(self._rng.uniform(1.0, 50.0), 2)
            p_rad = round(self._rng.uniform(0.01, 1.0), 3)

        d_linear = round(4.0 * math.pi * u_max / p_rad, 4)
        d_dbi = round(10.0 * math.log10(d_linear), 4)

        return "D = \\frac{4\\pi U_{\\max}}{P_{\\mathrm{rad}}}", {
            "U_max": u_max, "P_rad": p_rad,
            "D": d_linear, "D_dBi": d_dbi,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate substitution and computation steps.

        Args:
            data: Solution data from _create_problem.

        Returns:
            List of step strings.
        """
        return [
            f"U_max={_f(data['U_max'])}, P_rad={_f(data['P_rad'])}",
            f"D = 4*pi*{_f(data['U_max'])}/{_f(data['P_rad'])}",
            f"D = {_f(data['D'])}",
            f"D_dBi = 10*log10({_f(data['D'])}) = {_f(data['D_dBi'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return directivity in linear and dBi.

        Args:
            data: Solution data.

        Returns:
            Directivity values as a string.
        """
        return f"D = {_f(data['D'])}, D_dBi = {_f(data['D_dBi'])} dBi"


# ===================================================================
# 2. Antenna gain and efficiency  (tier 5)
# ===================================================================

@register
class AntennaGainEfficiencyGenerator(StepGenerator):
    """Compute antenna gain from directivity and efficiency.

    G = eta * D where eta is radiation efficiency (0 to 1).

    Difficulty scaling:
        Difficulty 1-3: simple efficiency values (0.5, 0.8, etc.).
        Difficulty 4-6: decimal efficiency, larger directivity.
        Difficulty 7-8: also compute G in dBi.

    Prerequisites:
        multiplication.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "antenna_gain_efficiency"

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
        return "compute antenna gain from directivity and efficiency"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate directivity and efficiency, compute gain.

        Args:
            difficulty: Controls value ranges and whether dBi is needed.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            eta = self._rng.choice([0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
            d_linear = float(self._rng.randint(2, 10 + difficulty * 3))
        elif difficulty <= 6:
            eta = round(self._rng.uniform(0.3, 0.99), 2)
            d_linear = round(self._rng.uniform(1.5, 30.0 + difficulty * 5), 2)
        else:
            eta = round(self._rng.uniform(0.1, 0.99), 3)
            d_linear = round(self._rng.uniform(5.0, 100.0), 2)

        gain = round(eta * d_linear, 4)
        gain_dbi = round(10.0 * math.log10(gain), 4) if gain > 0 else 0.0
        compute_dbi = difficulty >= 7

        return "G = \\eta \\cdot D", {
            "eta": eta, "D": d_linear,
            "G": gain, "G_dBi": gain_dbi,
            "compute_dBi": compute_dbi,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate multiplication and optional dBi steps.

        Args:
            data: Solution data from _create_problem.

        Returns:
            List of step strings.
        """
        steps = [
            f"eta={_f(data['eta'])}, D={_f(data['D'])}",
            f"G = {_f(data['eta'])}*{_f(data['D'])} = {_f(data['G'])}",
        ]
        if data["compute_dBi"]:
            steps.append(
                f"G_dBi = 10*log10({_f(data['G'])}) = {_f(data['G_dBi'])}"
            )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return gain value.

        Args:
            data: Solution data.

        Returns:
            Gain as a string, with dBi if applicable.
        """
        if data["compute_dBi"]:
            return f"G = {_f(data['G'])}, G_dBi = {_f(data['G_dBi'])} dBi"
        return f"G = {_f(data['G'])}"


# ===================================================================
# 3. Friis transmission equation  (tier 5)
# ===================================================================

@register
class FriisTransmissionGenerator(StepGenerator):
    """Compute received-to-transmitted power ratio using Friis equation.

    Pr/Pt = Gt * Gr * (lambda / (4*pi*d))^2 for free-space path loss.

    Difficulty scaling:
        Difficulty 1-3: integer gains and simple distances.
        Difficulty 4-6: decimal gains and wavelengths.
        Difficulty 7-8: express result in dB.

    Prerequisites:
        division.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "friis_transmission"

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
        return "compute free-space path loss using the Friis equation"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate antenna gains, wavelength, distance, compute Pr/Pt.

        Args:
            difficulty: Controls parameter complexity and dB output.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            gt = float(self._rng.randint(2, 10))
            gr = float(self._rng.randint(2, 10))
            lam = round(self._rng.uniform(0.01, 1.0), 2)
            d = float(self._rng.randint(10, 100 + difficulty * 50))
        elif difficulty <= 6:
            gt = round(self._rng.uniform(1.5, 20.0), 2)
            gr = round(self._rng.uniform(1.5, 20.0), 2)
            lam = round(self._rng.uniform(0.001, 0.5), 3)
            d = round(self._rng.uniform(50, 500 + difficulty * 100), 1)
        else:
            gt = round(self._rng.uniform(5.0, 50.0), 2)
            gr = round(self._rng.uniform(5.0, 50.0), 2)
            lam = round(self._rng.uniform(0.001, 0.1), 4)
            d = round(self._rng.uniform(100, 5000), 1)

        ratio = lam / (4.0 * math.pi * d)
        pr_over_pt = round(gt * gr * ratio ** 2, 4)
        pr_over_pt_db = round(10.0 * math.log10(pr_over_pt), 4) if pr_over_pt > 0 else -999.0
        compute_db = difficulty >= 7

        return ("\\frac{P_r}{P_t} = G_t G_r "
                "\\left(\\frac{\\lambda}{4\\pi d}\\right)^2"), {
            "Gt": gt, "Gr": gr, "lambda": lam, "d": d,
            "ratio": round(ratio, 4),
            "Pr_over_Pt": pr_over_pt, "Pr_over_Pt_dB": pr_over_pt_db,
            "compute_dB": compute_db,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate substitution and computation steps.

        Args:
            data: Solution data from _create_problem.

        Returns:
            List of step strings.
        """
        steps = [
            f"Gt={_f(data['Gt'])}, Gr={_f(data['Gr'])}, "
            f"lambda={_f(data['lambda'])}m, d={_f(data['d'])}m",
            f"lambda/(4*pi*d) = {_f(data['ratio'])}",
            f"Pr/Pt = {_f(data['Gt'])}*{_f(data['Gr'])}*"
            f"{_f(data['ratio'])}^2 = {_f(data['Pr_over_Pt'])}",
        ]
        if data["compute_dB"]:
            steps.append(
                f"Pr/Pt_dB = 10*log10({_f(data['Pr_over_Pt'])}) "
                f"= {_f(data['Pr_over_Pt_dB'])} dB"
            )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return power ratio.

        Args:
            data: Solution data.

        Returns:
            Power ratio as a string.
        """
        if data["compute_dB"]:
            return (f"Pr/Pt = {_f(data['Pr_over_Pt'])}, "
                    f"{_f(data['Pr_over_Pt_dB'])} dB")
        return f"Pr/Pt = {_f(data['Pr_over_Pt'])}"


# ===================================================================
# 4. Dipole radiation pattern  (tier 5)
# ===================================================================

@register
class DipoleRadiationGenerator(StepGenerator):
    """Evaluate half-wave dipole radiation pattern at a given angle.

    Half-wave dipole directivity D = 1.64 (2.15 dBi).
    Power pattern: U(theta) = cos^2(pi/2 * cos(theta)) / sin^2(theta).

    Difficulty scaling:
        Difficulty 1-3: angles that give clean values (30, 45, 60, 90).
        Difficulty 4-6: arbitrary integer angles.
        Difficulty 7-8: also compute directivity contribution.

    Prerequisites:
        sin_cos_eval.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "dipole_radiation"

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
        return "evaluate half-wave dipole radiation pattern at a given angle"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an angle and evaluate the dipole power pattern.

        Args:
            difficulty: Controls angle selection and extra computations.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            theta_deg = self._rng.choice([30, 45, 60, 90])
        elif difficulty <= 6:
            theta_deg = self._rng.randint(10, 170)
            # Avoid singularities at 0 and 180
            if theta_deg < 5:
                theta_deg = 5
            elif theta_deg > 175:
                theta_deg = 175
        else:
            theta_deg = self._rng.randint(5, 175)

        theta_rad = math.radians(theta_deg)
        sin_theta = math.sin(theta_rad)
        cos_theta = math.cos(theta_rad)

        numerator = math.cos(math.pi / 2.0 * cos_theta) ** 2
        denominator = sin_theta ** 2

        u_theta = round(numerator / denominator, 4) if denominator > 1e-10 else 0.0
        d_linear = 1.64
        d_dbi = 2.15

        return ("U(\\theta) = \\frac{\\cos^2(\\frac{\\pi}{2}"
                "\\cos\\theta)}{\\sin^2\\theta}"), {
            "theta_deg": theta_deg,
            "sin_theta": round(sin_theta, 4),
            "cos_theta": round(cos_theta, 4),
            "numerator": round(numerator, 4),
            "denominator": round(denominator, 4),
            "U_theta": u_theta,
            "D": d_linear, "D_dBi": d_dbi,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate evaluation steps for the radiation pattern.

        Args:
            data: Solution data from _create_problem.

        Returns:
            List of step strings.
        """
        return [
            f"theta={data['theta_deg']}deg, sin(theta)={_f(data['sin_theta'])}, "
            f"cos(theta)={_f(data['cos_theta'])}",
            f"num = cos^2(pi/2*{_f(data['cos_theta'])}) = "
            f"{_f(data['numerator'])}",
            f"den = sin^2(theta) = {_f(data['denominator'])}",
            f"U(theta) = {_f(data['numerator'])}/{_f(data['denominator'])} "
            f"= {_f(data['U_theta'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the pattern value and dipole directivity.

        Args:
            data: Solution data.

        Returns:
            Pattern value and directivity as a string.
        """
        return (f"U({data['theta_deg']}deg) = {_f(data['U_theta'])}, "
                f"D = {_f(data['D'])} ({_f(data['D_dBi'])} dBi)")


# ===================================================================
# 5. Array factor for uniform linear array  (tier 6)
# ===================================================================

@register
class ArrayFactorGenerator(StepGenerator):
    """Compute array factor for an N-element uniform linear array.

    AF = sin(N*psi/2) / sin(psi/2) where psi = k*d*cos(theta) + beta.
    k = 2*pi/lambda is the wavenumber.

    Difficulty scaling:
        Difficulty 1-3: small N (2-4), simple angles.
        Difficulty 4-6: larger N (4-8), arbitrary angles.
        Difficulty 7-8: large N (8-16), near-grating-lobe angles.

    Prerequisites:
        sin_cos_eval.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "array_factor"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

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
        return "compute array factor for a uniform linear array"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate array parameters and evaluate AF at a given angle.

        Args:
            difficulty: Controls array size and angle complexity.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            n_elem = self._rng.randint(2, 4)
            theta_deg = self._rng.choice([30, 45, 60, 90])
        elif difficulty <= 6:
            n_elem = self._rng.randint(4, 8)
            theta_deg = self._rng.randint(10, 170)
        else:
            n_elem = self._rng.randint(8, 16)
            theta_deg = self._rng.randint(5, 175)

        lam = round(self._rng.uniform(0.01, 1.0), 3)
        d_spacing = round(self._rng.uniform(0.3, 0.7) * lam, 4)
        beta = round(self._rng.uniform(-math.pi, math.pi), 4)

        k = 2.0 * math.pi / lam
        theta_rad = math.radians(theta_deg)
        psi = k * d_spacing * math.cos(theta_rad) + beta

        sin_num = math.sin(n_elem * psi / 2.0)
        sin_den = math.sin(psi / 2.0)

        if abs(sin_den) < 1e-10:
            af = float(n_elem)
        else:
            af = round(sin_num / sin_den, 4)

        return ("AF = \\frac{\\sin(N\\psi/2)}{\\sin(\\psi/2)}, "
                "\\psi = kd\\cos\\theta + \\beta"), {
            "N": n_elem, "theta_deg": theta_deg,
            "lambda": lam, "d": d_spacing, "beta": beta,
            "k": round(k, 4), "psi": round(psi, 4),
            "sin_num": round(sin_num, 4),
            "sin_den": round(sin_den, 4),
            "AF": af,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate evaluation steps for the array factor.

        Args:
            data: Solution data from _create_problem.

        Returns:
            List of step strings.
        """
        return [
            f"N={data['N']}, d={_f(data['d'])}m, "
            f"lambda={_f(data['lambda'])}m, beta={_f(data['beta'])}",
            f"k = 2*pi/{_f(data['lambda'])} = {_f(data['k'])}",
            f"psi = {_f(data['k'])}*{_f(data['d'])}*"
            f"cos({data['theta_deg']}deg)+{_f(data['beta'])} "
            f"= {_f(data['psi'])}",
            f"AF = sin({data['N']}*{_f(data['psi'])}/2)/"
            f"sin({_f(data['psi'])}/2) = {_f(data['AF'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the array factor value.

        Args:
            data: Solution data.

        Returns:
            Array factor as a string.
        """
        return f"AF = {_f(data['AF'])}"


# ===================================================================
# 6. Effective aperture  (tier 5)
# ===================================================================

@register
class EffectiveApertureGenerator(StepGenerator):
    """Compute effective aperture from antenna gain and wavelength.

    A_e = lambda^2 * G / (4*pi).

    Difficulty scaling:
        Difficulty 1-3: integer gain, simple wavelengths.
        Difficulty 4-6: decimal gain and wavelength.
        Difficulty 7-8: small wavelengths (mm-wave), express in cm^2.

    Prerequisites:
        multiplication.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "effective_aperture"

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
        return "compute antenna effective aperture from gain and wavelength"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate gain and wavelength, compute effective aperture.

        Args:
            difficulty: Controls parameter ranges and unit conversion.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            gain = float(self._rng.randint(2, 15))
            lam = round(self._rng.uniform(0.1, 1.0), 2)
        elif difficulty <= 6:
            gain = round(self._rng.uniform(1.5, 50.0), 2)
            lam = round(self._rng.uniform(0.01, 0.5), 3)
        else:
            gain = round(self._rng.uniform(10.0, 200.0), 2)
            lam = round(self._rng.uniform(0.001, 0.05), 4)

        a_e = round(lam ** 2 * gain / (4.0 * math.pi), 4)
        a_e_cm2 = round(a_e * 1e4, 4)
        express_cm2 = difficulty >= 7

        return "A_e = \\frac{\\lambda^2 G}{4\\pi}", {
            "G": gain, "lambda": lam,
            "A_e": a_e, "A_e_cm2": a_e_cm2,
            "express_cm2": express_cm2,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate computation steps for effective aperture.

        Args:
            data: Solution data from _create_problem.

        Returns:
            List of step strings.
        """
        steps = [
            f"G={_f(data['G'])}, lambda={_f(data['lambda'])}m",
            f"A_e = {_f(data['lambda'])}^2*{_f(data['G'])}/(4*pi)",
            f"A_e = {_f(data['A_e'])} m^2",
        ]
        if data["express_cm2"]:
            steps.append(f"A_e = {_f(data['A_e_cm2'])} cm^2")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the effective aperture.

        Args:
            data: Solution data.

        Returns:
            Effective aperture as a string.
        """
        if data["express_cm2"]:
            return (f"A_e = {_f(data['A_e'])} m^2 "
                    f"= {_f(data['A_e_cm2'])} cm^2")
        return f"A_e = {_f(data['A_e'])} m^2"
