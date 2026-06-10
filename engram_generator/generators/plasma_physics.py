"""Plasma physics generators -- Debye length, plasma frequency, MHD.

6 generators at tier 5 covering fundamental plasma parameters,
cyclotron motion, plasma beta, Coulomb logarithm, and Alfven waves.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


def _fmt(value: float, decimals: int = 4) -> str:
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


# Physical constants
_EPS_0 = 8.854e-12   # vacuum permittivity (F/m)
_K_B = 1.381e-23     # Boltzmann constant (J/K)
_E = 1.602e-19       # elementary charge (C)
_M_E = 9.109e-31     # electron mass (kg)
_MU_0 = 1.257e-6     # vacuum permeability (H/m)
_M_P = 1.673e-27     # proton mass (kg)


# ===================================================================
# 1. Debye length  (tier 5)
# ===================================================================

@register
class DebyeLengthGenerator(StepGenerator):
    """Debye length: lambda_D = sqrt(epsilon_0 * k_B * T / (n_e * e^2)).

    Computes the Debye screening length for a plasma given
    electron temperature T and electron density n_e.

    Difficulty scaling:
        Difficulty 1-3: laboratory plasma (T~1eV, n~1e16-1e18).
        Difficulty 4-6: fusion plasma (T~10keV, n~1e19-1e20).
        Difficulty 7-8: astrophysical plasma (T~1e6K, n~1e6).

    Prerequisites:
        square_root.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "debye_length"

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
        return "compute Debye screening length for a plasma"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Debye length problem.

        Args:
            difficulty: Controls plasma regime.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            t_ev = round(self._rng.uniform(0.5, 5.0), 2)
            n_e_exp = self._rng.randint(16, 18)
        elif difficulty <= 6:
            t_ev = round(self._rng.uniform(1.0, 20.0), 2)
            n_e_exp = self._rng.randint(18, 20)
        else:
            t_ev = round(self._rng.uniform(10.0, 1000.0), 2)
            n_e_exp = self._rng.randint(6, 14)

        t_kelvin = round(t_ev * _E / _K_B, 4)
        n_e_coeff = round(self._rng.uniform(1.0, 9.0), 2)
        n_e = n_e_coeff * 10 ** n_e_exp

        numerator = _EPS_0 * _K_B * t_kelvin
        denominator = n_e * _E ** 2
        lambda_d = round(math.sqrt(numerator / denominator), 4)

        desc = f"T={_fmt(t_ev)} eV, n_e={_fmt(n_e_coeff)}e{n_e_exp} m^-3"
        return "\\lambda_D = \\sqrt{\\epsilon_0 k_B T / (n_e e^2)}", {
            "t_ev": t_ev, "t_kelvin": round(t_kelvin, 4),
            "n_e_coeff": n_e_coeff, "n_e_exp": n_e_exp, "n_e": n_e,
            "numerator": round(numerator, 4),
            "denominator": round(denominator, 4),
            "lambda_d": lambda_d,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Debye length computation steps.

        Args:
            data: Solution data.

        Returns:
            List of step strings.
        """
        return [
            f"T = {_fmt(data['t_ev'])} eV = {_fmt(data['t_kelvin'])} K",
            f"n_e = {_fmt(data['n_e_coeff'])}e{data['n_e_exp']} m^-3",
            f"num = eps0*kB*T = {_fmt(data['numerator'])}",
            f"den = n_e*e^2 = {_fmt(data['denominator'])}",
            f"lambda_D = sqrt(num/den)",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the Debye length.

        Args:
            data: Solution data.

        Returns:
            Debye length in metres.
        """
        return f"lambda_D = {_fmt(data['lambda_d'])} m"


# ===================================================================
# 2. Plasma frequency  (tier 5)
# ===================================================================

@register
class PlasmaFrequencyGenerator(StepGenerator):
    """Plasma frequency: omega_pe = sqrt(n_e * e^2 / (epsilon_0 * m_e)).

    Computes the electron plasma frequency and corresponding
    cutoff wavelength lambda_c = 2*pi*c / omega_pe.

    Difficulty scaling:
        Difficulty 1-3: compute omega_pe only.
        Difficulty 4-6: compute omega_pe and cutoff wavelength.
        Difficulty 7-8: two densities, compare cutoffs.

    Prerequisites:
        square_root.
    """

    _C = 3.0e8  # speed of light (m/s)

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "plasma_frequency"

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
        return "compute electron plasma frequency and cutoff wavelength"

    def _compute_omega(self, n_e: float) -> float:
        """Compute plasma frequency for given density.

        Args:
            n_e: Electron density in m^-3.

        Returns:
            Plasma frequency in rad/s.
        """
        return round(math.sqrt(n_e * _E ** 2 / (_EPS_0 * _M_E)), 4)

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a plasma frequency problem.

        Args:
            difficulty: Controls problem scope.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        n_e_exp = self._rng.randint(10, 20)
        n_e_coeff = round(self._rng.uniform(1.0, 9.0), 2)
        n_e = n_e_coeff * 10 ** n_e_exp

        omega = self._compute_omega(n_e)
        lambda_c = round(2 * math.pi * self._C / omega, 4) if omega > 0 else 0

        desc = f"n_e = {_fmt(n_e_coeff)}e{n_e_exp} m^-3"

        return "\\omega_{pe} = \\sqrt{n_e e^2 / (\\epsilon_0 m_e)}", {
            "n_e_coeff": n_e_coeff, "n_e_exp": n_e_exp, "n_e": n_e,
            "omega": omega, "lambda_c": lambda_c,
            "compute_cutoff": difficulty > 3,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate plasma frequency computation steps.

        Args:
            data: Solution data.

        Returns:
            List of step strings.
        """
        steps = [
            f"n_e = {_fmt(data['n_e_coeff'])}e{data['n_e_exp']} m^-3",
            f"omega_pe = sqrt(n_e*e^2/(eps0*m_e))",
            f"omega_pe = {_fmt(data['omega'])} rad/s",
        ]
        if data["compute_cutoff"]:
            steps.append(
                f"lambda_c = 2*pi*c/omega_pe = {_fmt(data['lambda_c'])} m"
            )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the plasma frequency and optional cutoff.

        Args:
            data: Solution data.

        Returns:
            Plasma frequency and cutoff wavelength.
        """
        ans = f"omega_pe = {_fmt(data['omega'])} rad/s"
        if data["compute_cutoff"]:
            ans += f", lambda_c = {_fmt(data['lambda_c'])} m"
        return ans


# ===================================================================
# 3. Cyclotron frequency  (tier 5)
# ===================================================================

@register
class CyclotronFrequencyGenerator(StepGenerator):
    """Cyclotron frequency: omega_c = eB/m and gyro-radius r_L = v_perp/omega_c.

    Computes the cyclotron frequency for electrons or ions in a
    magnetic field, and the Larmor (gyro) radius.

    Difficulty scaling:
        Difficulty 1-3: electron, compute omega_c.
        Difficulty 4-6: electron, compute omega_c and r_L.
        Difficulty 7-8: compare electron and ion cyclotron.

    Prerequisites:
        division.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "cyclotron_frequency"

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
        return "compute cyclotron frequency and gyro-radius"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a cyclotron frequency problem.

        Args:
            difficulty: Controls particle type and scope.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        b_field = round(self._rng.uniform(0.01, 5.0), 4)
        v_perp = round(self._rng.uniform(1e5, 1e7), 4)

        # Electron cyclotron
        omega_e = round(_E * b_field / _M_E, 4)
        r_le = round(v_perp / omega_e, 4) if omega_e > 0 else 0

        if difficulty <= 3:
            desc = f"B={_fmt(b_field)} T, electron; find omega_c"
            return "\\omega_c = eB/m", {
                "b_field": b_field, "particle": "electron",
                "mass": _M_E, "omega_c": omega_e,
                "v_perp": v_perp, "r_l": r_le,
                "show_radius": False, "show_ion": False,
            }

        if difficulty <= 6:
            desc = (f"B={_fmt(b_field)} T, v_perp={_fmt(v_perp)} m/s, "
                    f"electron; find omega_c, r_L")
            return "\\omega_c = eB/m, r_L = v_{\\perp}/\\omega_c", {
                "b_field": b_field, "particle": "electron",
                "mass": _M_E, "omega_c": omega_e,
                "v_perp": v_perp, "r_l": r_le,
                "show_radius": True, "show_ion": False,
            }

        # Compare electron and proton
        omega_p = round(_E * b_field / _M_P, 4)
        r_lp = round(v_perp / omega_p, 4) if omega_p > 0 else 0
        desc = (f"B={_fmt(b_field)} T, v_perp={_fmt(v_perp)} m/s; "
                f"compare electron and proton")
        return "\\omega_c = eB/m, r_L = v_{\\perp}/\\omega_c", {
            "b_field": b_field, "particle": "both",
            "mass": _M_E, "omega_c": omega_e,
            "v_perp": v_perp, "r_l": r_le,
            "show_radius": True, "show_ion": True,
            "omega_p": omega_p, "r_lp": r_lp,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate cyclotron frequency computation steps.

        Args:
            data: Solution data.

        Returns:
            List of step strings.
        """
        steps = [
            f"B = {_fmt(data['b_field'])} T",
            f"electron: omega_c = e*B/m_e = {_fmt(data['omega_c'])} rad/s",
        ]
        if data["show_radius"]:
            steps.append(
                f"r_L(e) = {_fmt(data['v_perp'])}/{_fmt(data['omega_c'])}"
                f" = {_fmt(data['r_l'])} m"
            )
        if data["show_ion"]:
            steps.append(
                f"proton: omega_c = e*B/m_p = {_fmt(data['omega_p'])} rad/s"
            )
            steps.append(
                f"r_L(p) = {_fmt(data['v_perp'])}/{_fmt(data['omega_p'])}"
                f" = {_fmt(data['r_lp'])} m"
            )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the cyclotron frequency and gyro-radius.

        Args:
            data: Solution data.

        Returns:
            Results string.
        """
        ans = f"omega_c(e) = {_fmt(data['omega_c'])} rad/s"
        if data["show_radius"]:
            ans += f", r_L(e) = {_fmt(data['r_l'])} m"
        if data["show_ion"]:
            ans += (f"; omega_c(p) = {_fmt(data['omega_p'])} rad/s, "
                    f"r_L(p) = {_fmt(data['r_lp'])} m")
        return ans


# ===================================================================
# 4. Plasma beta  (tier 5)
# ===================================================================

@register
class PlasmaBetaGenerator(StepGenerator):
    """Plasma beta: beta = n*k_B*T / (B^2 / (2*mu_0)).

    Computes the ratio of plasma pressure to magnetic pressure
    and classifies the regime.

    Difficulty scaling:
        Difficulty 1-3: single species, classify.
        Difficulty 4-6: compute both pressures explicitly.
        Difficulty 7-8: two conditions, compare betas.

    Prerequisites:
        division.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "plasma_beta"

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
        return "compute plasma beta and classify regime"

    def _compute_beta(self, n: float, t_ev: float, b: float) -> dict:
        """Compute plasma beta for given parameters.

        Args:
            n: Particle density in m^-3.
            t_ev: Temperature in eV.
            b: Magnetic field in Tesla.

        Returns:
            Dictionary with pressures and beta.
        """
        t_joule = t_ev * _E
        p_plasma = round(n * _K_B * (t_joule / _K_B), 4)  # n * T in Joules
        p_mag = round(b ** 2 / (2 * _MU_0), 4)
        beta = round(p_plasma / p_mag, 4) if p_mag > 0 else 0

        if beta > 10:
            regime = "pressure-dominated"
        elif beta < 0.1:
            regime = "magnetic-dominated"
        else:
            regime = "intermediate"

        return {
            "p_plasma": p_plasma, "p_mag": p_mag,
            "beta": beta, "regime": regime,
        }

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a plasma beta problem.

        Args:
            difficulty: Controls problem scope.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        n_exp = self._rng.randint(16, 20)
        n_coeff = round(self._rng.uniform(1.0, 9.0), 2)
        n = n_coeff * 10 ** n_exp
        t_ev = round(self._rng.uniform(0.5, 50.0), 2)
        b = round(self._rng.uniform(0.01, 5.0), 4)

        result = self._compute_beta(n, t_ev, b)

        desc = (f"n={_fmt(n_coeff)}e{n_exp} m^-3, "
                f"T={_fmt(t_ev)} eV, B={_fmt(b)} T")
        return "\\beta = \\frac{n k_B T}{B^2/(2\\mu_0)}", {
            "n_coeff": n_coeff, "n_exp": n_exp, "n": n,
            "t_ev": t_ev, "b": b, **result,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate plasma beta computation steps.

        Args:
            data: Solution data.

        Returns:
            List of step strings.
        """
        return [
            f"n={_fmt(data['n_coeff'])}e{data['n_exp']}, "
            f"T={_fmt(data['t_ev'])} eV, B={_fmt(data['b'])} T",
            f"P_plasma = n*k_B*T = {_fmt(data['p_plasma'])} Pa",
            f"P_mag = B^2/(2*mu_0) = {_fmt(data['p_mag'])} Pa",
            f"beta = {_fmt(data['p_plasma'])}/{_fmt(data['p_mag'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the plasma beta and regime.

        Args:
            data: Solution data.

        Returns:
            Beta value and regime classification.
        """
        return f"beta = {_fmt(data['beta'])} ({data['regime']})"


# ===================================================================
# 5. Coulomb logarithm  (tier 5)
# ===================================================================

@register
class CoulombLogarithmGenerator(StepGenerator):
    """Coulomb logarithm: ln(Lambda) = ln(12*pi*n*lambda_D^3).

    Computes the Coulomb logarithm for a plasma given the
    electron density and Debye length.

    Difficulty scaling:
        Difficulty 1-3: given lambda_D directly.
        Difficulty 4-6: compute lambda_D from T, n_e first.
        Difficulty 7-8: two plasma conditions, compare.

    Prerequisites:
        logarithm.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "coulomb_logarithm"

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
        return "compute Coulomb logarithm for plasma collisions"

    def _compute_debye(self, t_ev: float, n_e: float) -> float:
        """Compute Debye length from temperature and density.

        Args:
            t_ev: Temperature in eV.
            n_e: Electron density in m^-3.

        Returns:
            Debye length in metres.
        """
        t_kelvin = t_ev * _E / _K_B
        return round(math.sqrt(_EPS_0 * _K_B * t_kelvin / (n_e * _E ** 2)), 4)

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Coulomb logarithm problem.

        Args:
            difficulty: Controls problem scope.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        n_e_exp = self._rng.randint(14, 20)
        n_e_coeff = round(self._rng.uniform(1.0, 9.0), 2)
        n_e = n_e_coeff * 10 ** n_e_exp
        t_ev = round(self._rng.uniform(0.5, 100.0), 2)

        lambda_d = self._compute_debye(t_ev, n_e)
        n_d_cube = round(n_e * lambda_d ** 3, 4)
        argument = round(12 * math.pi * n_d_cube, 4)
        ln_lambda = round(math.log(argument), 4) if argument > 0 else 0

        if difficulty <= 3:
            desc = (f"n_e={_fmt(n_e_coeff)}e{n_e_exp} m^-3, "
                    f"lambda_D={_fmt(lambda_d)} m")
            given_lambda = True
        else:
            desc = (f"n_e={_fmt(n_e_coeff)}e{n_e_exp} m^-3, "
                    f"T={_fmt(t_ev)} eV")
            given_lambda = False

        return "\\ln\\Lambda = \\ln(12\\pi n \\lambda_D^3)", {
            "n_e_coeff": n_e_coeff, "n_e_exp": n_e_exp, "n_e": n_e,
            "t_ev": t_ev, "lambda_d": lambda_d,
            "n_d_cube": n_d_cube, "argument": argument,
            "ln_lambda": ln_lambda, "given_lambda": given_lambda,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Coulomb logarithm computation steps.

        Args:
            data: Solution data.

        Returns:
            List of step strings.
        """
        steps = []
        if not data["given_lambda"]:
            steps.append(
                f"lambda_D = sqrt(eps0*kB*T/(n_e*e^2)) = "
                f"{_fmt(data['lambda_d'])} m"
            )
        steps.extend([
            f"n*lambda_D^3 = {_fmt(data['n_e_coeff'])}e{data['n_e_exp']}"
            f"*{_fmt(data['lambda_d'])}^3 = {_fmt(data['n_d_cube'])}",
            f"12*pi*n*lambda_D^3 = {_fmt(data['argument'])}",
            f"ln(Lambda) = ln({_fmt(data['argument'])})",
        ])
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the Coulomb logarithm.

        Args:
            data: Solution data.

        Returns:
            ln(Lambda) value.
        """
        return f"ln(Lambda) = {_fmt(data['ln_lambda'])}"


# ===================================================================
# 6. MHD Alfven speed  (tier 5)
# ===================================================================

@register
class MhdAlfvenGenerator(StepGenerator):
    """Alfven speed: v_A = B / sqrt(mu_0 * rho).

    Computes the Alfven speed for given magnetic field B and
    mass density rho.

    Difficulty scaling:
        Difficulty 1-3: given B and rho directly.
        Difficulty 4-6: compute rho from n and ion mass.
        Difficulty 7-8: two conditions, compare Alfven speeds.

    Prerequisites:
        square_root.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "mhd_alfven"

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
        return "compute Alfven speed for magnetised plasma"

    def _compute_alfven(self, b: float, rho: float) -> float:
        """Compute Alfven speed.

        Args:
            b: Magnetic field in Tesla.
            rho: Mass density in kg/m^3.

        Returns:
            Alfven speed in m/s.
        """
        return round(b / math.sqrt(_MU_0 * rho), 4)

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an Alfven speed problem.

        Args:
            difficulty: Controls problem scope.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        b = round(self._rng.uniform(1e-4, 5.0), 4)

        if difficulty <= 3:
            rho_exp = self._rng.randint(-12, -6)
            rho_coeff = round(self._rng.uniform(1.0, 9.0), 2)
            rho = rho_coeff * 10 ** rho_exp
            v_a = self._compute_alfven(b, rho)

            desc = (f"B={_fmt(b)} T, rho={_fmt(rho_coeff)}e{rho_exp} kg/m^3")
            return "v_A = B/\\sqrt{\\mu_0 \\rho}", {
                "b": b, "rho_coeff": rho_coeff, "rho_exp": rho_exp,
                "rho": rho, "v_a": v_a, "from_density": True,
            }

        # Compute rho from ion density and mass
        n_exp = self._rng.randint(16, 22)
        n_coeff = round(self._rng.uniform(1.0, 9.0), 2)
        n_i = n_coeff * 10 ** n_exp
        # Hydrogen plasma: rho = n_i * m_p
        rho = round(n_i * _M_P, 4)
        v_a = self._compute_alfven(b, rho)

        desc = (f"B={_fmt(b)} T, n_i={_fmt(n_coeff)}e{n_exp} m^-3, "
                f"hydrogen plasma")
        return "v_A = B/\\sqrt{\\mu_0 \\rho}, \\rho = n_i m_p", {
            "b": b, "n_coeff": n_coeff, "n_exp": n_exp,
            "n_i": n_i, "rho": rho, "v_a": v_a,
            "from_density": False,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Alfven speed computation steps.

        Args:
            data: Solution data.

        Returns:
            List of step strings.
        """
        steps = [f"B = {_fmt(data['b'])} T"]
        if data["from_density"]:
            steps.append(
                f"rho = {_fmt(data['rho_coeff'])}e{data['rho_exp']} kg/m^3"
            )
        else:
            steps.append(
                f"rho = n_i*m_p = {_fmt(data['n_coeff'])}e{data['n_exp']}"
                f"*{_M_P} = {_fmt(data['rho'])} kg/m^3"
            )
        mu0_rho = round(_MU_0 * data["rho"], 4)
        steps.append(f"mu_0*rho = {_fmt(mu0_rho)}")
        steps.append(f"v_A = {_fmt(data['b'])}/sqrt({_fmt(mu0_rho)})")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the Alfven speed.

        Args:
            data: Solution data.

        Returns:
            Alfven speed in m/s.
        """
        return f"v_A = {_fmt(data['v_a'])} m/s"
