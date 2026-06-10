"""Continuum mechanics generators -- stress, strain, Hooke, Mohr, von Mises, moduli.

6 generators covering principal stresses from a 2D stress tensor,
strain from displacement gradients, 3D Hooke's law for isotropic
materials, Mohr's circle, von Mises yield criterion, and elastic
moduli relations. Tiers 5-6.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


class _CMFormatter:
    """Formats numeric values for continuum mechanics problems.

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


_f = _CMFormatter.fmt


# ===================================================================
# 1. Stress tensor (principal stresses)  (tier 6)
# ===================================================================

@register
class StressTensorGenerator(StepGenerator):
    """Compute principal stresses from a 2D stress tensor.

    Given [[sigma_xx, tau_xy], [tau_xy, sigma_yy]], the principal
    stresses are the eigenvalues:
    sigma_1,2 = (sigma_xx + sigma_yy)/2 +/- sqrt(((sigma_xx - sigma_yy)/2)^2 + tau_xy^2).

    Difficulty scaling:
        Difficulty 1-3: integer stress components, small values.
        Difficulty 4-6: decimal stresses, moderate range.
        Difficulty 7-8: large stress values with 2 dp precision.

    Prerequisites:
        eigenvalue.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "stress_tensor"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["eigenvalue"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute principal stresses from 2D stress tensor"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate 2D stress tensor and compute principal stresses.

        Args:
            difficulty: Controls stress magnitudes and precision.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            sxx = float(self._rng.randint(10, 100))
            syy = float(self._rng.randint(10, 100))
            txy = float(self._rng.randint(5, 50))
        elif difficulty <= 6:
            sxx = round(self._rng.uniform(-50, 200), 1)
            syy = round(self._rng.uniform(-50, 200), 1)
            txy = round(self._rng.uniform(-80, 80), 1)
        else:
            sxx = round(self._rng.uniform(-200, 500), 2)
            syy = round(self._rng.uniform(-200, 500), 2)
            txy = round(self._rng.uniform(-150, 150), 2)

        avg = round((sxx + syy) / 2, 4)
        diff_half = round((sxx - syy) / 2, 4)
        r = round(math.sqrt(diff_half ** 2 + txy ** 2), 4)
        sigma_1 = round(avg + r, 4)
        sigma_2 = round(avg - r, 4)

        problem = (
            f"sigma_xx = {sxx} MPa, sigma_yy = {syy} MPa, "
            f"tau_xy = {txy} MPa; find principal stresses"
        )
        return problem, {
            "sxx": sxx, "syy": syy, "txy": txy,
            "avg": avg, "diff_half": diff_half,
            "R": r, "sigma_1": sigma_1, "sigma_2": sigma_2,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate principal stress computation steps.

        Args:
            data: Solution data with tensor components and eigenvalues.

        Returns:
            List of step strings.
        """
        r_sq = round(data["diff_half"] ** 2 + data["txy"] ** 2, 4)
        return [
            f"avg = ({_f(data['sxx'])} + {_f(data['syy'])})/2 "
            f"= {_f(data['avg'])}",
            f"((sxx-syy)/2)^2 + txy^2 = {_f(data['diff_half'])}^2 + "
            f"{_f(data['txy'])}^2 = {_f(r_sq)}",
            f"R = sqrt({_f(r_sq)}) = {_f(data['R'])}",
            f"sigma_1 = {_f(data['avg'])} + {_f(data['R'])} "
            f"= {_f(data['sigma_1'])}",
            f"sigma_2 = {_f(data['avg'])} - {_f(data['R'])} "
            f"= {_f(data['sigma_2'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the principal stresses.

        Args:
            data: Solution data.

        Returns:
            String with sigma_1 and sigma_2 in MPa.
        """
        return (
            f"sigma_1 = {_f(data['sigma_1'])} MPa, "
            f"sigma_2 = {_f(data['sigma_2'])} MPa"
        )


# ===================================================================
# 2. Strain tensor  (tier 6)
# ===================================================================

@register
class StrainTensorGenerator(StepGenerator):
    """Compute strain components from a linear displacement field.

    For displacement u_i = a_i + b_ij * x_j, the strain tensor is
    epsilon_ij = (1/2)(du_i/dx_j + du_j/dx_i) = (1/2)(b_ij + b_ji).

    Difficulty scaling:
        Difficulty 1-3: 2D, small integer coefficients.
        Difficulty 4-6: 2D, decimal coefficients.
        Difficulty 7-8: 3D displacement field.

    Prerequisites:
        partial_derivative.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "strain_tensor"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["partial_derivative"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute strain tensor from displacement gradient"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate displacement gradient and compute strain tensor.

        Args:
            difficulty: Controls dimensionality and coefficient precision.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            b11 = float(self._rng.randint(1, 10)) * 1e-3
            b12 = float(self._rng.randint(1, 10)) * 1e-3
            b21 = float(self._rng.randint(1, 10)) * 1e-3
            b22 = float(self._rng.randint(1, 10)) * 1e-3
        elif difficulty <= 6:
            b11 = round(self._rng.uniform(-5, 10) * 1e-3, 4)
            b12 = round(self._rng.uniform(-5, 10) * 1e-3, 4)
            b21 = round(self._rng.uniform(-5, 10) * 1e-3, 4)
            b22 = round(self._rng.uniform(-5, 10) * 1e-3, 4)
        else:
            b11 = round(self._rng.uniform(-10, 10) * 1e-3, 4)
            b12 = round(self._rng.uniform(-10, 10) * 1e-3, 4)
            b21 = round(self._rng.uniform(-10, 10) * 1e-3, 4)
            b22 = round(self._rng.uniform(-10, 10) * 1e-3, 4)

        e_xx = round(b11, 4)
        e_yy = round(b22, 4)
        e_xy = round(0.5 * (b12 + b21), 4)

        problem = (
            f"du1/dx1 = {b11}, du1/dx2 = {b12}, "
            f"du2/dx1 = {b21}, du2/dx2 = {b22}; "
            f"compute strain tensor"
        )
        return problem, {
            "b11": b11, "b12": b12, "b21": b21, "b22": b22,
            "e_xx": e_xx, "e_yy": e_yy, "e_xy": e_xy,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate strain tensor computation steps.

        Args:
            data: Solution data with displacement gradients and strains.

        Returns:
            List of step strings.
        """
        b12_plus_b21 = round(data["b12"] + data["b21"], 4)
        return [
            "epsilon_ij = (1/2)(du_i/dx_j + du_j/dx_i)",
            f"e_xx = du1/dx1 = {_f(data['b11'])}",
            f"e_yy = du2/dx2 = {_f(data['b22'])}",
            f"e_xy = (1/2)({_f(data['b12'])} + {_f(data['b21'])}) "
            f"= (1/2)*{_f(b12_plus_b21)} = {_f(data['e_xy'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the strain tensor components.

        Args:
            data: Solution data.

        Returns:
            String with strain components.
        """
        return (
            f"e_xx = {_f(data['e_xx'])}, "
            f"e_yy = {_f(data['e_yy'])}, "
            f"e_xy = {_f(data['e_xy'])}"
        )


# ===================================================================
# 3. Hooke's law 3D  (tier 6)
# ===================================================================

@register
class HookesLaw3DGenerator(StepGenerator):
    """Compute 3D stress from strain using isotropic Hooke's law.

    sigma_xx = lambda*(e_xx + e_yy + e_zz) + 2*mu*e_xx
    where lambda and mu are Lame parameters.

    Difficulty scaling:
        Difficulty 1-3: integer strains (*1e-3), standard Lame params.
        Difficulty 4-6: decimal strains, varied Lame parameters.
        Difficulty 7-8: compute all three normal stresses.

    Prerequisites:
        multiplication.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "hookes_law_3d"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

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
        return "compute 3D stress from strain using Hooke's law"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate strains and Lame parameters, compute stresses.

        Args:
            difficulty: Controls parameter precision and targets.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            e_xx = float(self._rng.randint(1, 5)) * 1e-3
            e_yy = float(self._rng.randint(1, 5)) * 1e-3
            e_zz = float(self._rng.randint(1, 5)) * 1e-3
            lam = 50e9   # Pa
            mu = 26e9    # Pa
        elif difficulty <= 6:
            e_xx = round(self._rng.uniform(-3, 5) * 1e-3, 4)
            e_yy = round(self._rng.uniform(-3, 5) * 1e-3, 4)
            e_zz = round(self._rng.uniform(-3, 5) * 1e-3, 4)
            lam = round(self._rng.uniform(30e9, 80e9), 4)
            mu = round(self._rng.uniform(20e9, 50e9), 4)
        else:
            e_xx = round(self._rng.uniform(-5, 8) * 1e-3, 4)
            e_yy = round(self._rng.uniform(-5, 8) * 1e-3, 4)
            e_zz = round(self._rng.uniform(-5, 8) * 1e-3, 4)
            lam = round(self._rng.uniform(10e9, 120e9), 4)
            mu = round(self._rng.uniform(10e9, 80e9), 4)

        vol_strain = round(e_xx + e_yy + e_zz, 4)
        lam_vol = round(lam * vol_strain, 4)
        s_xx = round(lam_vol + 2 * mu * e_xx, 4)
        s_yy = round(lam_vol + 2 * mu * e_yy, 4)
        s_zz = round(lam_vol + 2 * mu * e_zz, 4)

        problem = (
            f"e_xx={e_xx}, e_yy={e_yy}, e_zz={e_zz}, "
            f"lambda={lam} Pa, mu={mu} Pa"
        )
        return problem, {
            "e_xx": e_xx, "e_yy": e_yy, "e_zz": e_zz,
            "lam": lam, "mu": mu, "vol_strain": vol_strain,
            "lam_vol": lam_vol,
            "s_xx": s_xx, "s_yy": s_yy, "s_zz": s_zz,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Hooke's law computation steps.

        Args:
            data: Solution data with strains and stresses.

        Returns:
            List of step strings.
        """
        two_mu_exx = round(2 * data["mu"] * data["e_xx"], 4)
        return [
            f"vol_strain = {_f(data['e_xx'])} + {_f(data['e_yy'])} + "
            f"{_f(data['e_zz'])} = {_f(data['vol_strain'])}",
            f"lambda*vol = {_f(data['lam'])} * {_f(data['vol_strain'])} "
            f"= {_f(data['lam_vol'])}",
            f"2*mu*e_xx = 2*{_f(data['mu'])}*{_f(data['e_xx'])} "
            f"= {_f(two_mu_exx)}",
            f"sigma_xx = {_f(data['lam_vol'])} + {_f(two_mu_exx)} "
            f"= {_f(data['s_xx'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the computed stresses.

        Args:
            data: Solution data.

        Returns:
            String with stress components in Pa.
        """
        return (
            f"sigma_xx = {_f(data['s_xx'])} Pa, "
            f"sigma_yy = {_f(data['s_yy'])} Pa, "
            f"sigma_zz = {_f(data['s_zz'])} Pa"
        )


# ===================================================================
# 4. Mohr circle  (tier 5)
# ===================================================================

@register
class MohrCircleGenerator(StepGenerator):
    """Compute Mohr's circle centre and radius for 2D stress state.

    Centre C = (sigma_x + sigma_y) / 2.
    Radius R = sqrt(((sigma_x - sigma_y)/2)^2 + tau_xy^2).

    Difficulty scaling:
        Difficulty 1-3: integer stresses, small values.
        Difficulty 4-6: decimal stresses, moderate range.
        Difficulty 7-8: negative stresses, high precision.

    Prerequisites:
        division.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "mohr_circle"

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
        return "compute Mohr's circle centre and radius"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate stress state and compute Mohr's circle parameters.

        Args:
            difficulty: Controls stress magnitudes and precision.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            sx = float(self._rng.randint(20, 100))
            sy = float(self._rng.randint(10, 80))
            txy = float(self._rng.randint(5, 40))
        elif difficulty <= 6:
            sx = round(self._rng.uniform(-30, 200), 1)
            sy = round(self._rng.uniform(-30, 200), 1)
            txy = round(self._rng.uniform(-60, 60), 1)
        else:
            sx = round(self._rng.uniform(-100, 300), 2)
            sy = round(self._rng.uniform(-100, 300), 2)
            txy = round(self._rng.uniform(-100, 100), 2)

        centre = round((sx + sy) / 2, 4)
        diff_half = round((sx - sy) / 2, 4)
        r_sq = round(diff_half ** 2 + txy ** 2, 4)
        r = round(math.sqrt(r_sq), 4)

        problem = (
            f"sigma_x = {sx} MPa, sigma_y = {sy} MPa, "
            f"tau_xy = {txy} MPa; find Mohr's circle C and R"
        )
        return problem, {
            "sx": sx, "sy": sy, "txy": txy,
            "centre": centre, "diff_half": diff_half,
            "R_sq": r_sq, "R": r,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Mohr's circle computation steps.

        Args:
            data: Solution data with stresses and circle parameters.

        Returns:
            List of step strings.
        """
        return [
            f"C = ({_f(data['sx'])} + {_f(data['sy'])})/2 "
            f"= {_f(data['centre'])}",
            f"(sx-sy)/2 = ({_f(data['sx'])} - {_f(data['sy'])})/2 "
            f"= {_f(data['diff_half'])}",
            f"R^2 = {_f(data['diff_half'])}^2 + {_f(data['txy'])}^2 "
            f"= {_f(data['R_sq'])}",
            f"R = sqrt({_f(data['R_sq'])}) = {_f(data['R'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the Mohr's circle centre and radius.

        Args:
            data: Solution data.

        Returns:
            String with C and R in MPa.
        """
        return f"C = {_f(data['centre'])} MPa, R = {_f(data['R'])} MPa"


# ===================================================================
# 5. Von Mises yield criterion  (tier 6)
# ===================================================================

@register
class VonMisesGenerator(StepGenerator):
    """Compute von Mises equivalent stress and check yielding.

    sigma_vm = sqrt(0.5*((s1-s2)^2 + (s2-s3)^2 + (s3-s1)^2)).
    Compares with yield stress sigma_y to determine if yielding occurs.

    Difficulty scaling:
        Difficulty 1-3: integer principal stresses, common yield stress.
        Difficulty 4-6: decimal stresses, varied yield stress.
        Difficulty 7-8: negative principal stresses, high precision.

    Prerequisites:
        stress_tensor.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "von_mises"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["stress_tensor"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute von Mises stress and check yield"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate principal stresses and yield stress, check yielding.

        Args:
            difficulty: Controls stress magnitudes and precision.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            s1 = float(self._rng.randint(50, 200))
            s2 = float(self._rng.randint(20, 150))
            s3 = float(self._rng.randint(0, 100))
            sigma_y = float(self._rng.choice([250, 300, 350]))
        elif difficulty <= 6:
            s1 = round(self._rng.uniform(-50, 300), 1)
            s2 = round(self._rng.uniform(-50, 250), 1)
            s3 = round(self._rng.uniform(-50, 200), 1)
            sigma_y = round(self._rng.uniform(200, 500), 1)
        else:
            s1 = round(self._rng.uniform(-100, 400), 2)
            s2 = round(self._rng.uniform(-100, 300), 2)
            s3 = round(self._rng.uniform(-100, 250), 2)
            sigma_y = round(self._rng.uniform(150, 600), 2)

        d12 = round((s1 - s2) ** 2, 4)
        d23 = round((s2 - s3) ** 2, 4)
        d31 = round((s3 - s1) ** 2, 4)
        inner = round(0.5 * (d12 + d23 + d31), 4)
        sigma_vm = round(math.sqrt(inner), 4)
        yields = sigma_vm >= sigma_y

        problem = (
            f"s1={s1}, s2={s2}, s3={s3} MPa, "
            f"sigma_y={sigma_y} MPa; check yield"
        )
        return problem, {
            "s1": s1, "s2": s2, "s3": s3, "sigma_y": sigma_y,
            "d12": d12, "d23": d23, "d31": d31,
            "inner": inner, "sigma_vm": sigma_vm, "yields": yields,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate von Mises computation steps.

        Args:
            data: Solution data with stresses and yield check.

        Returns:
            List of step strings.
        """
        sum_sq = round(data["d12"] + data["d23"] + data["d31"], 4)
        cmp = ">=" if data["yields"] else "<"
        result = "yields" if data["yields"] else "safe"
        return [
            f"(s1-s2)^2 = {_f(data['d12'])}, "
            f"(s2-s3)^2 = {_f(data['d23'])}, "
            f"(s3-s1)^2 = {_f(data['d31'])}",
            f"sum = {_f(sum_sq)}, 0.5*sum = {_f(data['inner'])}",
            f"sigma_vm = sqrt({_f(data['inner'])}) = {_f(data['sigma_vm'])}",
            f"{_f(data['sigma_vm'])} {cmp} {_f(data['sigma_y'])} => {result}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return von Mises stress and yield status.

        Args:
            data: Solution data.

        Returns:
            String with sigma_vm and yield determination.
        """
        status = "yields" if data["yields"] else "safe"
        return f"sigma_vm = {_f(data['sigma_vm'])} MPa, {status}"


# ===================================================================
# 6. Elastic moduli relations  (tier 5)
# ===================================================================

@register
class ElasticModuliGenerator(StepGenerator):
    """Compute the third elastic modulus from two known moduli.

    Relations: E = 2*G*(1+nu), K = E/(3*(1-2*nu)).
    Given two of (E, G, K, nu), computes the remaining ones.

    Difficulty scaling:
        Difficulty 1-3: given E and nu, compute G and K.
        Difficulty 4-6: given G and nu, compute E and K.
        Difficulty 7-8: given E and G, compute nu and K.

    Prerequisites:
        division.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "elastic_moduli"

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
        return "compute elastic moduli from known material properties"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate elastic moduli problem.

        Args:
            difficulty: Controls which pair is given.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        # Poisson's ratio must be in (0, 0.5) for physical materials
        nu = round(self._rng.uniform(0.15, 0.45), 4)

        if difficulty <= 3:
            e_gpa = float(self._rng.randint(50, 300))
            g_gpa = round(e_gpa / (2 * (1 + nu)), 4)
            mode = "E_nu"
        elif difficulty <= 6:
            g_gpa = round(self._rng.uniform(20, 120), 1)
            e_gpa = round(2 * g_gpa * (1 + nu), 4)
            mode = "G_nu"
        else:
            e_gpa = round(self._rng.uniform(50, 400), 2)
            g_gpa = round(e_gpa / (2 * (1 + nu)), 4)
            mode = "E_G"

        denom_k = round(3 * (1 - 2 * nu), 4)
        k_gpa = round(e_gpa / denom_k, 4)

        problem_parts = {
            "E_nu": f"E = {e_gpa} GPa, nu = {nu}; find G and K",
            "G_nu": f"G = {g_gpa} GPa, nu = {nu}; find E and K",
            "E_G": f"E = {e_gpa} GPa, G = {g_gpa} GPa; find nu and K",
        }
        return problem_parts[mode], {
            "mode": mode, "E": e_gpa, "G": g_gpa,
            "nu": nu, "K": k_gpa, "denom_K": denom_k,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate elastic moduli computation steps.

        Args:
            data: Solution data with moduli and Poisson's ratio.

        Returns:
            List of step strings.
        """
        mode = data["mode"]
        if mode == "E_nu":
            denom_g = round(2 * (1 + data["nu"]), 4)
            return [
                f"G = E/(2*(1+nu)) = {_f(data['E'])}/"
                f"{_f(denom_g)} = {_f(data['G'])} GPa",
                f"K = E/(3*(1-2*nu)) = {_f(data['E'])}/"
                f"{_f(data['denom_K'])} = {_f(data['K'])} GPa",
            ]
        if mode == "G_nu":
            factor = round(2 * (1 + data["nu"]), 4)
            return [
                f"E = 2*G*(1+nu) = 2*{_f(data['G'])}*"
                f"{_f(round(1 + data['nu'], 4))} = {_f(data['E'])} GPa",
                f"K = E/(3*(1-2*nu)) = {_f(data['E'])}/"
                f"{_f(data['denom_K'])} = {_f(data['K'])} GPa",
            ]
        # mode == "E_G"
        return [
            f"nu = E/(2*G) - 1 = {_f(data['E'])}/(2*{_f(data['G'])}) - 1 "
            f"= {_f(data['nu'])}",
            f"K = E/(3*(1-2*nu)) = {_f(data['E'])}/"
            f"{_f(data['denom_K'])} = {_f(data['K'])} GPa",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the computed moduli.

        Args:
            data: Solution data.

        Returns:
            String with all four elastic constants.
        """
        return (
            f"E = {_f(data['E'])} GPa, G = {_f(data['G'])} GPa, "
            f"K = {_f(data['K'])} GPa, nu = {_f(data['nu'])}"
        )
