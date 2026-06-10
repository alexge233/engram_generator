"""Extended solid state physics generators -- effective mass through lattice vibrations.

Covers effective mass computation, density of states, semiconductor
doping, dielectric constant, magnetic susceptibility, crystal momentum,
superconductor critical temperature, and lattice vibration regimes.
All tiers are 4-5 (intermediate solid state physics).
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

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
_HBAR = 1.0546e-34     # reduced Planck constant (J*s)
_ME = 9.109e-31        # electron mass (kg)
_PI = math.pi
_K_B = 1.381e-23       # Boltzmann constant (J/K)
_K_B_EV = 8.617e-5     # Boltzmann constant (eV/K)
_EPS_0 = 8.854e-12     # vacuum permittivity (F/m)


# ===================================================================
# 1. Effective mass  (tier 5)
# ===================================================================

@register
class EffectiveMassGenerator(StepGenerator):
    """Compute effective mass from parabolic band dispersion.

    For a parabolic band E(k) = E_0 + hbar^2*k^2/(2*m*), the effective
    mass is m* = hbar^2 / (d^2E/dk^2).  Given the curvature parameter
    alpha = d^2E/dk^2, compute m* in units of electron mass.

    Difficulty scaling:
        Difficulty 1-3: simple curvature, m* ~ 0.1-1.0 m_e.
        Difficulty 4-6: heavier effective masses, varied curvature.
        Difficulty 7-8: compute m* ratio and classify as light/heavy.

    Prerequisites:
        division.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "effective_mass"

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
        return "compute effective mass from band curvature"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an effective mass problem.

        Args:
            difficulty: Controls curvature range and output detail.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            m_star_ratio = round(self._rng.uniform(0.1, 1.0), 4)
        elif difficulty <= 6:
            m_star_ratio = round(self._rng.uniform(0.5, 5.0), 4)
        else:
            m_star_ratio = round(self._rng.uniform(0.01, 10.0), 4)

        m_star = round(m_star_ratio * _ME, 34)
        curvature = round(_HBAR ** 2 / max(m_star, 1e-40), 4)

        classify = ""
        if difficulty >= 7:
            classify = "light" if m_star_ratio < 0.5 else "heavy"

        return "m^* = \\hbar^2 / (d^2E/dk^2)", {
            "curvature": curvature,
            "m_star": m_star,
            "m_star_ratio": m_star_ratio,
            "classify": classify,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate effective mass computation steps.

        Args:
            data: Solution data with curvature and effective mass.

        Returns:
            List of step strings.
        """
        steps = [
            f"d^2E/dk^2 = {data['curvature']:.4e} J*m^2",
            f"hbar^2 = {_HBAR**2:.4e} J^2*s^2",
            f"m* = hbar^2 / (d^2E/dk^2) = {data['m_star']:.4e} kg",
            f"m*/m_e = {_fmt(data['m_star_ratio'])}",
        ]
        if data["classify"]:
            steps.append(f"carrier: {data['classify']}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the effective mass.

        Args:
            data: Solution data.

        Returns:
            String with effective mass ratio.
        """
        ans = f"m* = {_fmt(data['m_star_ratio'])} m_e"
        if data["classify"]:
            ans += f" ({data['classify']})"
        return ans


# ===================================================================
# 2. Density of states  (tier 5)
# ===================================================================

@register
class DensityOfStatesGenerator(StepGenerator):
    """Compute 3D density of states for a free-electron-like band.

    g(E) = (2*m*)^{3/2} / (2*pi^2*hbar^3) * sqrt(E).
    Given effective mass and energy, compute the DOS value.

    Difficulty scaling:
        Difficulty 1-3: m* = m_e, simple energy values.
        Difficulty 4-6: varied m*, moderate energy.
        Difficulty 7-8: compute DOS ratio at two energies.

    Prerequisites:
        square_root.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "density_of_states"

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
        return "compute density of states at given energy"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a density of states problem.

        Args:
            difficulty: Controls mass and energy range.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            m_star_ratio = 1.0
        else:
            m_star_ratio = round(self._rng.uniform(0.1, 5.0), 4)

        m_star = m_star_ratio * _ME
        energy_ev = round(self._rng.uniform(0.1, 3.0), 4)
        energy_j = energy_ev * 1.602e-19

        prefactor = (2 * m_star) ** 1.5 / (2 * _PI ** 2 * _HBAR ** 3)
        g_e = round(prefactor * math.sqrt(energy_j), 4)

        data = {
            "m_star_ratio": m_star_ratio,
            "E_eV": energy_ev,
            "E_J": energy_j,
            "prefactor": prefactor,
            "g_E": g_e,
        }

        if difficulty >= 7:
            e2_ev = round(self._rng.uniform(0.5, 5.0), 4)
            e2_j = e2_ev * 1.602e-19
            g_e2 = round(prefactor * math.sqrt(e2_j), 4)
            ratio = round(g_e2 / g_e, 4) if g_e != 0 else 0.0
            data["E2_eV"] = e2_ev
            data["g_E2"] = g_e2
            data["ratio"] = ratio

        return "g(E) = \\frac{(2m^*)^{3/2}}{2\\pi^2\\hbar^3} \\sqrt{E}", data

    def _create_steps(self, data: dict) -> list[str]:
        """Generate DOS computation steps.

        Args:
            data: Solution data with mass, energy, and DOS.

        Returns:
            List of step strings.
        """
        steps = [
            f"m* = {_fmt(data['m_star_ratio'])} m_e",
            f"E = {_fmt(data['E_eV'])} eV = {data['E_J']:.4e} J",
            f"prefactor = {data['prefactor']:.4e}",
            f"g(E) = {data['g_E']:.4e} states/(J*m^3)",
        ]
        if "ratio" in data:
            steps.append(
                f"g(E2)/g(E1) = {_fmt(data['ratio'])}"
            )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the density of states.

        Args:
            data: Solution data.

        Returns:
            String with g(E) value.
        """
        return f"g(E) = {data['g_E']:.4e} states/(J*m^3)"


# ===================================================================
# 3. Semiconductor doping  (tier 5)
# ===================================================================

@register
class SemiconductorDopingGenerator(StepGenerator):
    """Compute majority and minority carrier concentrations.

    n-type: n = N_D, p = n_i^2 / N_D.
    p-type: p = N_A, n = n_i^2 / N_A.
    Given dopant concentration and intrinsic carrier density,
    compute both carrier concentrations.

    Difficulty scaling:
        Difficulty 1-3: n-type doping, simple values.
        Difficulty 4-6: random n-type or p-type.
        Difficulty 7-8: compensated doping (both N_D and N_A).

    Prerequisites:
        division.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "semiconductor_doping"

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
        return "compute majority and minority carrier concentrations"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a semiconductor doping problem.

        Args:
            difficulty: Controls doping type and complexity.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        ni_exp = self._rng.randint(9, 11)
        ni_mantissa = round(self._rng.uniform(1.0, 9.0), 2)
        n_i = ni_mantissa * (10 ** ni_exp)

        nd_exp = self._rng.randint(14, 18)
        nd_mantissa = round(self._rng.uniform(1.0, 9.0), 2)

        if difficulty <= 3:
            doping_type = "n-type"
        elif difficulty <= 6:
            doping_type = self._rng.choice(["n-type", "p-type"])
        else:
            doping_type = "compensated"

        if doping_type == "n-type":
            n_d = nd_mantissa * (10 ** nd_exp)
            majority = n_d
            minority = round(n_i ** 2 / n_d, 4)
            return "n = N_D, p = n_i^2 / N_D", {
                "type": doping_type, "n_i": n_i,
                "N_D": n_d, "majority": majority,
                "minority": minority,
                "majority_label": "n", "minority_label": "p",
            }

        if doping_type == "p-type":
            n_a = nd_mantissa * (10 ** nd_exp)
            majority = n_a
            minority = round(n_i ** 2 / n_a, 4)
            return "p = N_A, n = n_i^2 / N_A", {
                "type": doping_type, "n_i": n_i,
                "N_A": n_a, "majority": majority,
                "minority": minority,
                "majority_label": "p", "minority_label": "n",
            }

        # Compensated
        n_d = nd_mantissa * (10 ** nd_exp)
        na_exp = self._rng.randint(14, nd_exp - 1)
        na_mantissa = round(self._rng.uniform(1.0, 9.0), 2)
        n_a = na_mantissa * (10 ** na_exp)
        net = n_d - n_a
        majority = abs(net)
        minority = round(n_i ** 2 / abs(net), 4)
        eff_type = "n-type" if net > 0 else "p-type"
        return "n_{eff} = |N_D - N_A|", {
            "type": "compensated", "n_i": n_i,
            "N_D": n_d, "N_A": n_a, "net": net,
            "eff_type": eff_type,
            "majority": majority, "minority": minority,
            "majority_label": "n" if net > 0 else "p",
            "minority_label": "p" if net > 0 else "n",
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate doping computation steps.

        Args:
            data: Solution data with concentrations.

        Returns:
            List of step strings.
        """
        steps = [f"doping: {data['type']}, n_i = {data['n_i']:.2e} cm^-3"]
        if data["type"] == "compensated":
            steps.append(f"N_D = {data['N_D']:.2e}, N_A = {data['N_A']:.2e}")
            steps.append(f"net = {data['net']:.2e} -> {data['eff_type']}")
        elif "N_D" in data:
            steps.append(f"N_D = {data['N_D']:.2e} cm^-3")
        else:
            steps.append(f"N_A = {data['N_A']:.2e} cm^-3")
        steps.append(
            f"{data['majority_label']} = {data['majority']:.2e}, "
            f"{data['minority_label']} = {data['minority']:.2e}"
        )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the carrier concentrations.

        Args:
            data: Solution data.

        Returns:
            String with majority and minority concentrations.
        """
        return (
            f"{data['majority_label']} = {data['majority']:.2e}, "
            f"{data['minority_label']} = {data['minority']:.2e} cm^-3"
        )


# ===================================================================
# 4. Dielectric constant  (tier 4)
# ===================================================================

@register
class DielectricConstantGenerator(StepGenerator):
    """Compute capacitance of a parallel-plate dielectric capacitor.

    C = epsilon_r * epsilon_0 * A / d.  Given relative permittivity,
    plate area, and separation, compute capacitance.

    Difficulty scaling:
        Difficulty 1-3: simple integer epsilon_r, round dimensions.
        Difficulty 4-6: varied materials and decimal dimensions.
        Difficulty 7-8: solve for epsilon_r given C, A, d.

    Prerequisites:
        multiplication.
    """

    _MATERIALS = [
        ("vacuum", 1.0), ("air", 1.0006), ("teflon", 2.1),
        ("glass", 5.0), ("silicon", 11.7), ("water", 80.0),
        ("BaTiO3", 1200.0), ("SiO2", 3.9),
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "dielectric_constant"

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
        return "compute capacitance of dielectric capacitor"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a dielectric capacitance problem.

        Args:
            difficulty: Controls material and problem variant.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        name, eps_r = self._rng.choice(self._MATERIALS)
        area_cm2 = round(self._rng.uniform(1.0, 100.0), 4)
        area_m2 = round(area_cm2 * 1e-4, 4)
        d_mm = round(self._rng.uniform(0.1, 5.0), 4)
        d_m = round(d_mm * 1e-3, 4)

        cap = round(eps_r * _EPS_0 * area_m2 / d_m, 4)

        return "C = \\varepsilon_r \\varepsilon_0 A / d", {
            "material": name, "eps_r": eps_r,
            "A_cm2": area_cm2, "A_m2": area_m2,
            "d_mm": d_mm, "d_m": d_m,
            "C": cap, "target": "C" if difficulty < 7 else "eps_r",
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate dielectric capacitance computation steps.

        Args:
            data: Solution data with material and dimensions.

        Returns:
            List of step strings.
        """
        steps = [
            f"material: {data['material']}, eps_r = {_fmt(data['eps_r'])}",
            f"A = {_fmt(data['A_cm2'])} cm^2 = {data['A_m2']:.4e} m^2",
            f"d = {_fmt(data['d_mm'])} mm = {data['d_m']:.4e} m",
        ]
        if data["target"] == "C":
            steps.append(f"C = eps_r*eps_0*A/d = {data['C']:.4e} F")
        else:
            steps.append(f"eps_r = C*d/(eps_0*A) = {_fmt(data['eps_r'])}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the capacitance or permittivity.

        Args:
            data: Solution data.

        Returns:
            String with result and units.
        """
        if data["target"] == "C":
            return f"C = {data['C']:.4e} F"
        return f"eps_r = {_fmt(data['eps_r'])}"


# ===================================================================
# 5. Magnetic susceptibility  (tier 5)
# ===================================================================

@register
class MagneticSusceptibilityGenerator(StepGenerator):
    """Compute and classify magnetic susceptibility.

    Paramagnetic: chi > 0, Curie law chi = C/T.
    Diamagnetic: chi < 0.
    Given Curie constant and temperature, compute susceptibility
    and classify the material.

    Difficulty scaling:
        Difficulty 1-3: paramagnetic with simple C and T.
        Difficulty 4-6: paramagnetic or diamagnetic classification.
        Difficulty 7-8: compare two materials at same temperature.

    Prerequisites:
        division.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "magnetic_susceptibility"

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
        return "compute magnetic susceptibility and classify material"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a magnetic susceptibility problem.

        Args:
            difficulty: Controls material type and problem variant.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        temp = self._rng.randint(100, 600)

        if difficulty <= 3:
            curie_c = round(self._rng.uniform(0.1, 5.0), 4)
            chi = round(curie_c / temp, 4)
            return "\\chi = C / T", {
                "mode": "single", "C": curie_c, "T": temp,
                "chi": chi, "type": "paramagnetic",
            }

        if difficulty <= 6:
            is_para = self._rng.choice([True, False])
            if is_para:
                curie_c = round(self._rng.uniform(0.1, 5.0), 4)
                chi = round(curie_c / temp, 4)
                mat_type = "paramagnetic"
            else:
                chi = round(-self._rng.uniform(1e-6, 1e-4), 4)
                curie_c = 0.0
                mat_type = "diamagnetic"
            return "\\chi \\text{ classification}", {
                "mode": "single", "C": curie_c, "T": temp,
                "chi": chi, "type": mat_type,
            }

        # Compare two materials
        c1 = round(self._rng.uniform(0.1, 5.0), 4)
        c2 = round(self._rng.uniform(0.1, 5.0), 4)
        chi1 = round(c1 / temp, 4)
        chi2 = round(c2 / temp, 4)
        stronger = "material_1" if chi1 > chi2 else "material_2"
        return "\\chi = C / T \\text{ (compare)}", {
            "mode": "compare", "T": temp,
            "C1": c1, "C2": c2,
            "chi1": chi1, "chi2": chi2,
            "stronger": stronger,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate susceptibility computation steps.

        Args:
            data: Solution data with Curie constant and temperature.

        Returns:
            List of step strings.
        """
        if data["mode"] == "single":
            steps = [f"T = {data['T']} K"]
            if data["type"] == "paramagnetic":
                steps.append(f"C = {_fmt(data['C'])}, chi = C/T = {_fmt(data['chi'])}")
            else:
                steps.append(f"chi = {_fmt(data['chi'])}")
            steps.append(f"chi {'>' if data['chi'] > 0 else '<'} 0 -> {data['type']}")
            return steps
        return [
            f"T = {data['T']} K",
            f"chi_1 = {_fmt(data['C1'])}/{data['T']} = {_fmt(data['chi1'])}",
            f"chi_2 = {_fmt(data['C2'])}/{data['T']} = {_fmt(data['chi2'])}",
            f"stronger paramagnetic: {data['stronger']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the susceptibility and classification.

        Args:
            data: Solution data.

        Returns:
            String with chi value and material type.
        """
        if data["mode"] == "single":
            return f"chi = {_fmt(data['chi'])}, {data['type']}"
        return (
            f"chi_1 = {_fmt(data['chi1'])}, chi_2 = {_fmt(data['chi2'])}, "
            f"stronger: {data['stronger']}"
        )


# ===================================================================
# 6. Crystal momentum  (tier 5)
# ===================================================================

@register
class CrystalMomentumGenerator(StepGenerator):
    """Compute crystal momentum at Brillouin zone boundary.

    p = hbar * k.  At the zone boundary k = pi/a.
    Given lattice constant a, compute momentum at zone boundary.

    Difficulty scaling:
        Difficulty 1-3: compute p at k = pi/a directly.
        Difficulty 4-6: compute p at arbitrary k within BZ.
        Difficulty 7-8: compute de Broglie wavelength from p.

    Prerequisites:
        multiplication.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "crystal_momentum"

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
        return "compute crystal momentum at Brillouin zone boundary"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a crystal momentum problem.

        Args:
            difficulty: Controls k-point and output detail.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        a_ang = round(self._rng.uniform(2.0, 6.0), 4)
        a_m = a_ang * 1e-10

        if difficulty <= 3:
            k = round(_PI / a_m, 4)
            k_label = "pi/a (zone boundary)"
        elif difficulty <= 6:
            frac = round(self._rng.uniform(0.2, 1.0), 4)
            k = round(frac * _PI / a_m, 4)
            k_label = f"{_fmt(frac)}*pi/a"
        else:
            k = round(_PI / a_m, 4)
            k_label = "pi/a (zone boundary)"

        p = round(_HBAR * k, 4)

        data = {
            "a_ang": a_ang, "a_m": a_m,
            "k": k, "k_label": k_label, "p": p,
        }

        if difficulty >= 7:
            h_full = 6.626e-34
            wavelength = round(h_full / p, 4)
            data["wavelength"] = wavelength

        return "p = \\hbar k", data

    def _create_steps(self, data: dict) -> list[str]:
        """Generate crystal momentum computation steps.

        Args:
            data: Solution data with lattice constant and wavevector.

        Returns:
            List of step strings.
        """
        steps = [
            f"a = {_fmt(data['a_ang'])} A = {data['a_m']:.4e} m",
            f"k = {data['k_label']} = {data['k']:.4e} m^-1",
            f"p = hbar*k = {_HBAR:.4e}*{data['k']:.4e} = {data['p']:.4e} kg*m/s",
        ]
        if "wavelength" in data:
            steps.append(
                f"lambda = h/p = {data['wavelength']:.4e} m"
            )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the crystal momentum.

        Args:
            data: Solution data.

        Returns:
            String with momentum value.
        """
        ans = f"p = {data['p']:.4e} kg*m/s"
        if "wavelength" in data:
            ans += f", lambda = {data['wavelength']:.4e} m"
        return ans


# ===================================================================
# 7. Superconductor critical temperature  (tier 5)
# ===================================================================

@register
class SuperconductorTcGenerator(StepGenerator):
    """Estimate superconductor critical temperature from BCS theory.

    BCS approximation: Tc ~ theta_D * exp(-1/(N(0)*V)).
    Given Debye temperature and electron-phonon coupling parameter,
    compute the critical temperature.

    Difficulty scaling:
        Difficulty 1-3: strong coupling (N(0)*V ~ 0.3-0.5).
        Difficulty 4-6: moderate coupling (N(0)*V ~ 0.2-0.4).
        Difficulty 7-8: weak coupling, compare two materials.

    Prerequisites:
        exponentiation.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "superconductor_tc"

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
        return "estimate superconductor Tc from BCS theory"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a BCS critical temperature problem.

        Args:
            difficulty: Controls coupling strength and complexity.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        theta_d = self._rng.randint(150, 500)

        if difficulty <= 3:
            nv = round(self._rng.uniform(0.3, 0.5), 4)
        elif difficulty <= 6:
            nv = round(self._rng.uniform(0.2, 0.4), 4)
        else:
            nv = round(self._rng.uniform(0.15, 0.35), 4)

        exponent = round(-1.0 / nv, 4)
        tc = round(theta_d * math.exp(exponent), 4)

        data = {
            "theta_D": theta_d, "NV": nv,
            "exponent": exponent, "Tc": tc,
        }

        if difficulty >= 7:
            theta_d2 = self._rng.randint(150, 500)
            nv2 = round(self._rng.uniform(0.15, 0.35), 4)
            exp2 = round(-1.0 / nv2, 4)
            tc2 = round(theta_d2 * math.exp(exp2), 4)
            higher = "material_1" if tc > tc2 else "material_2"
            data["theta_D2"] = theta_d2
            data["NV2"] = nv2
            data["Tc2"] = tc2
            data["higher"] = higher

        return "T_c \\sim \\Theta_D \\exp(-1/N(0)V)", data

    def _create_steps(self, data: dict) -> list[str]:
        """Generate BCS Tc computation steps.

        Args:
            data: Solution data with Debye temp and coupling.

        Returns:
            List of step strings.
        """
        steps = [
            f"theta_D = {data['theta_D']} K, N(0)V = {_fmt(data['NV'])}",
            f"exponent = -1/{_fmt(data['NV'])} = {_fmt(data['exponent'])}",
            f"Tc = {data['theta_D']}*exp({_fmt(data['exponent'])}) = {_fmt(data['Tc'])} K",
        ]
        if "higher" in data:
            steps.append(
                f"material_2: theta_D={data['theta_D2']}, "
                f"Tc2={_fmt(data['Tc2'])} K"
            )
            steps.append(f"higher Tc: {data['higher']}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the critical temperature.

        Args:
            data: Solution data.

        Returns:
            String with Tc value.
        """
        ans = f"Tc = {_fmt(data['Tc'])} K"
        if "higher" in data:
            ans += f" (higher: {data['higher']})"
        return ans


# ===================================================================
# 8. Lattice vibration regime  (tier 5)
# ===================================================================

@register
class LatticeVibrationGenerator(StepGenerator):
    """Classify lattice vibration regime using Debye temperature.

    Debye model: theta_D = hbar*omega_D / k_B.
    At T >> theta_D: C_V = 3*N*k_B (Dulong-Petit).
    At T << theta_D: C_V ~ T^3 law.
    Classify regime and compute heat capacity in the appropriate limit.

    Difficulty scaling:
        Difficulty 1-3: clear high-T or low-T regime.
        Difficulty 4-6: compute theta_D from omega_D, then classify.
        Difficulty 7-8: intermediate T, determine closest limit.

    Prerequisites:
        comparison.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "lattice_vibration"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["comparison"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "classify lattice vibration regime and compute heat capacity"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a lattice vibration regime problem.

        Args:
            difficulty: Controls temperature range and output detail.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        n_atoms = self._rng.randint(1, 10)

        if difficulty <= 3:
            theta_d = self._rng.randint(200, 500)
            high_t = self._rng.choice([True, False])
            if high_t:
                temp = self._rng.randint(theta_d * 3, theta_d * 6)
            else:
                temp = self._rng.randint(5, max(6, theta_d // 10))
        elif difficulty <= 6:
            omega_d = round(self._rng.uniform(1e12, 1e14), 4)
            theta_d = round(_HBAR * omega_d / _K_B, 4)
            theta_d = int(theta_d)
            high_t = self._rng.choice([True, False])
            if high_t:
                temp = self._rng.randint(theta_d * 2, theta_d * 5)
            else:
                temp = self._rng.randint(5, max(6, theta_d // 10))
        else:
            theta_d = self._rng.randint(200, 500)
            temp = self._rng.randint(theta_d // 3, theta_d * 2)

        t_ratio = round(temp / theta_d, 4)

        if t_ratio > 1.5:
            regime = "high-T (Dulong-Petit)"
            c_v = round(3 * n_atoms * _K_B, 4)
        elif t_ratio < 0.3:
            regime = "low-T (T^3 law)"
            prefactor = round(12 * _PI ** 4 / 5, 4)
            c_v = round(prefactor * n_atoms * _K_B * t_ratio ** 3, 4)
        else:
            regime = "intermediate"
            c_v = round(3 * n_atoms * _K_B * 0.7, 4)

        return "\\Theta_D = \\hbar\\omega_D / k_B", {
            "theta_D": theta_d, "T": temp, "N": n_atoms,
            "T_ratio": t_ratio, "regime": regime, "C_V": c_v,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate lattice vibration classification steps.

        Args:
            data: Solution data with temperatures and regime.

        Returns:
            List of step strings.
        """
        return [
            f"theta_D = {data['theta_D']} K, T = {data['T']} K, N = {data['N']}",
            f"T/theta_D = {_fmt(data['T_ratio'])}",
            f"regime: {data['regime']}",
            f"C_V = {data['C_V']:.4e} J/K",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the heat capacity and regime.

        Args:
            data: Solution data.

        Returns:
            String with C_V and regime classification.
        """
        return f"C_V = {data['C_V']:.4e} J/K ({data['regime']})"
