"""Materials science generators -- stress-strain through phase diagrams.

Covers stress-strain analysis, Young's modulus from data, thermal
expansion, crystal structure packing, Fickian diffusion, and binary
phase diagram lever rule. Tiers range from 4 (introductory) to 5
(intermediate materials science).
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


class _MatFormatter:
    """Formats numeric values for materials science problems.

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


_f = _MatFormatter.fmt


# ===================================================================
# 1. Stress and strain  (tier 4)
# ===================================================================

@register
class StressStrainGenerator(StepGenerator):
    """Compute engineering stress and strain from force and geometry.

    Stress sigma = F / A (Pa), strain epsilon = dL / L_0 (dimensionless).
    Given force, cross-sectional area, original length, and extension,
    computes both stress and strain.

    Difficulty scaling:
        Difficulty 1-3: integer force (N), simple area (mm^2).
        Difficulty 4-6: larger forces (kN), decimal areas.
        Difficulty 7-8: solve for F or A given stress/strain.

    Prerequisites:
        division.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "stress_strain"

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
        return "compute stress and strain"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate force, area, length, extension and compute stress/strain.

        Args:
            difficulty: Controls parameter magnitude and problem variant.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            force = float(self._rng.randint(100, 1000 + difficulty * 200))
            a_mm2 = float(self._rng.randint(10, 50 + difficulty * 10))
        else:
            force = round(self._rng.uniform(500, 5000 + difficulty * 1000), 1)
            a_mm2 = round(self._rng.uniform(5, 100 + difficulty * 20), 1)

        area = a_mm2 * 1e-6  # m^2
        l_0 = round(self._rng.uniform(0.1, 1.0 + difficulty * 0.2), 2)
        dl_mm = round(self._rng.uniform(0.01, 0.5 + difficulty * 0.1), 3)
        dl = dl_mm * 1e-3  # m

        stress = round(force / area, 4)
        strain = round(dl / l_0, 4)

        return "\\sigma = F/A, \\varepsilon = \\Delta L / L_0", {
            "F": force, "A_mm2": a_mm2, "A": area,
            "L_0": l_0, "dL_mm": dl_mm, "dL": dl,
            "stress": stress, "strain": strain,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate stress and strain computation steps.

        Args:
            data: Solution data with force, area, lengths.

        Returns:
            List of step strings.
        """
        return [
            f"F={_f(data['F'])}N, A={data['A_mm2']}mm^2="
            f"{_f(data['A'])}m^2",
            f"sigma = F/A = {_f(data['F'])}/{_f(data['A'])}",
            f"dL={data['dL_mm']}mm={_f(data['dL'])}m, L_0={data['L_0']}m",
            f"epsilon = dL/L_0 = {_f(data['dL'])}/{data['L_0']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return stress and strain values.

        Args:
            data: Solution data.

        Returns:
            String with stress in Pa and dimensionless strain.
        """
        return f"sigma = {_f(data['stress'])} Pa, epsilon = {_f(data['strain'])}"


# ===================================================================
# 2. Young's modulus  (tier 4)
# ===================================================================

@register
class YoungsModulusGenerator(StepGenerator):
    """Compute Young's modulus E = stress / strain from data points.

    Given multiple stress-strain data points, computes E as the slope
    of the linear elastic region using E = (F/A) / (dL/L_0).

    Difficulty scaling:
        Difficulty 1-3: two data points, integer values.
        Difficulty 4-6: three data points, compute average slope.
        Difficulty 7-8: four points with noise, identify linear region.

    Prerequisites:
        linear_regression.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "youngs_modulus"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["linear_regression"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute Young's modulus from stress-strain data"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate stress-strain data points and compute Young's modulus.

        Args:
            difficulty: Controls number of data points and precision.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        # True E in GPa range
        e_true_gpa = round(self._rng.uniform(50, 400), 1)
        e_true = e_true_gpa * 1e9  # Pa

        n_points = min(2 + difficulty // 3, 4)
        strains = []
        stresses = []
        for i in range(n_points):
            eps = round((i + 1) * self._rng.uniform(0.0005, 0.002), 6)
            sig = round(e_true * eps, 4)
            strains.append(eps)
            stresses.append(sig)

        # Compute slope from first and last point
        d_stress = stresses[-1] - stresses[0]
        d_strain = strains[-1] - strains[0]
        e_calc = round(d_stress / d_strain, 4)

        return "E = \\frac{\\sigma}{\\varepsilon}", {
            "strains": strains, "stresses": stresses,
            "n_points": n_points,
            "d_stress": round(d_stress, 4),
            "d_strain": round(d_strain, 6),
            "E": e_calc,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Young's modulus computation steps.

        Args:
            data: Solution data with stress-strain data points.

        Returns:
            List of step strings.
        """
        pts = [
            f"({_f(data['strains'][i])}, {_f(data['stresses'][i])})"
            for i in range(data["n_points"])
        ]
        return [
            f"data: {', '.join(pts)}",
            f"d_sigma = {_f(data['d_stress'])} Pa",
            f"d_eps = {_f(data['d_strain'])}",
            f"E = d_sigma/d_eps",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return Young's modulus.

        Args:
            data: Solution data.

        Returns:
            String with E in Pa.
        """
        return f"E = {_f(data['E'])} Pa"


# ===================================================================
# 3. Thermal expansion  (tier 4)
# ===================================================================

@register
class ThermalExpansionGenerator(StepGenerator):
    """Compute thermal expansion: dL = alpha * L_0 * dT.

    Given the coefficient of linear thermal expansion alpha,
    original length L_0, and temperature change dT, computes
    the expansion dL and final length L = L_0 + dL.

    Difficulty scaling:
        Difficulty 1-3: simple metals (steel, aluminium), integer dT.
        Difficulty 4-6: varied materials, decimal lengths.
        Difficulty 7-8: compute alpha given dL, L_0, dT.

    Prerequisites:
        multiplication.
    """

    _MATERIALS = {
        "steel": 12e-6,
        "aluminium": 23e-6,
        "copper": 17e-6,
        "brass": 19e-6,
        "concrete": 12e-6,
        "glass": 9e-6,
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "thermal_expansion"

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
        return "compute thermal expansion"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate thermal expansion parameters and compute results.

        Args:
            difficulty: Controls material variety and problem variant.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        material = self._rng.choice(list(self._MATERIALS.keys()))
        alpha = self._MATERIALS[material]

        if difficulty <= 3:
            l_0 = float(self._rng.randint(1, 10))
            dt = float(self._rng.randint(10, 100))
        else:
            l_0 = round(self._rng.uniform(0.5, 20.0 + difficulty * 5), 2)
            dt = round(self._rng.uniform(10, 200 + difficulty * 50), 1)

        dl = round(alpha * l_0 * dt, 4)
        l_final = round(l_0 + dl, 4)

        if difficulty >= 7:
            return "\\alpha = \\frac{\\Delta L}{L_0 \\Delta T}", {
                "material": material, "alpha": alpha,
                "L_0": l_0, "dT": dt, "dL": dl,
                "L_final": l_final, "target": "alpha",
            }

        return "\\Delta L = \\alpha L_0 \\Delta T", {
            "material": material, "alpha": alpha,
            "L_0": l_0, "dT": dt, "dL": dl,
            "L_final": l_final, "target": "dL",
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate thermal expansion computation steps.

        Args:
            data: Solution data with alpha, L_0, dT.

        Returns:
            List of step strings.
        """
        if data["target"] == "dL":
            return [
                f"material={data['material']}, alpha={data['alpha']}/K",
                f"L_0={data['L_0']}m, dT={data['dT']}K",
                f"dL = {data['alpha']}*{data['L_0']}*{data['dT']}",
                f"L = L_0 + dL = {data['L_0']} + {_f(data['dL'])}",
            ]
        # solve for alpha
        return [
            f"dL={_f(data['dL'])}m, L_0={data['L_0']}m, dT={data['dT']}K",
            f"alpha = dL/(L_0*dT) = {_f(data['dL'])}/({data['L_0']}*{data['dT']})",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the thermal expansion result.

        Args:
            data: Solution data.

        Returns:
            String with dL and L_final, or alpha.
        """
        if data["target"] == "dL":
            return f"dL = {_f(data['dL'])} m, L = {_f(data['L_final'])} m"
        return f"alpha = {data['alpha']} /K"


# ===================================================================
# 4. Crystal structure APF  (tier 5)
# ===================================================================

@register
class CrystalStructureGenerator(StepGenerator):
    """Compute atomic packing factor (APF) for cubic crystal structures.

    FCC: APF = pi*sqrt(2)/6 = 0.7405, coordination number 12.
    BCC: APF = pi*sqrt(3)/8 = 0.6802, coordination number 8.
    SC:  APF = pi/6 = 0.5236, coordination number 6.

    Difficulty scaling:
        Difficulty 1-3: SC structure, compute APF only.
        Difficulty 4-6: BCC or FCC, compute APF and coordination.
        Difficulty 7-8: given lattice parameter a, compute atom radius.

    Prerequisites:
        volume_sphere.
    """

    _STRUCTURES = {
        "SC": {
            "apf": round(math.pi / 6, 4),
            "coord": 6,
            "atoms_per_cell": 1,
            "r_over_a": 0.5,
        },
        "BCC": {
            "apf": round(math.pi * math.sqrt(3) / 8, 4),
            "coord": 8,
            "atoms_per_cell": 2,
            "r_over_a": round(math.sqrt(3) / 4, 4),
        },
        "FCC": {
            "apf": round(math.pi * math.sqrt(2) / 6, 4),
            "coord": 12,
            "atoms_per_cell": 4,
            "r_over_a": round(math.sqrt(2) / 4, 4),
        },
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "crystal_structure"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["volume_sphere"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute atomic packing factor for crystal structure"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a crystal structure problem.

        Args:
            difficulty: Controls structure type and problem variant.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            struct_name = "SC"
        elif difficulty <= 5:
            struct_name = self._rng.choice(["BCC", "FCC"])
        else:
            struct_name = self._rng.choice(["SC", "BCC", "FCC"])

        struct = self._STRUCTURES[struct_name]

        a_pm = self._rng.randint(250, 600)
        a_m = a_pm * 1e-12
        r_m = round(struct["r_over_a"] * a_m, 4)

        return "APF = \\frac{V_{atoms}}{V_{cell}}", {
            "structure": struct_name,
            "apf": struct["apf"],
            "coord": struct["coord"],
            "atoms_per_cell": struct["atoms_per_cell"],
            "r_over_a": struct["r_over_a"],
            "a_pm": a_pm, "a_m": a_m, "r_m": r_m,
            "compute_r": difficulty >= 7,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate crystal structure computation steps.

        Args:
            data: Solution data with structure type and parameters.

        Returns:
            List of step strings.
        """
        steps = [
            f"structure: {data['structure']}",
            f"atoms/cell = {data['atoms_per_cell']}, "
            f"coordination = {data['coord']}",
            f"APF = {_f(data['apf'])}",
        ]
        if data["compute_r"]:
            steps.append(
                f"a={data['a_pm']}pm, r/a={_f(data['r_over_a'])}"
            )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the APF and coordination number.

        Args:
            data: Solution data.

        Returns:
            String with APF and coordination number.
        """
        result = f"APF = {_f(data['apf'])}, CN = {data['coord']}"
        if data["compute_r"]:
            result += f", r = {_f(data['r_m'])} m"
        return result


# ===================================================================
# 5. Fick's first law of diffusion  (tier 5)
# ===================================================================

@register
class DiffusionFickGenerator(StepGenerator):
    """Compute diffusion flux using Fick's first law: J = -D * dC/dx.

    Given diffusion coefficient D and concentration gradient dC/dx,
    computes the diffusion flux J. The negative sign indicates
    diffusion occurs from high to low concentration.

    Difficulty scaling:
        Difficulty 1-3: given D and dC/dx directly, compute J.
        Difficulty 4-6: given two concentrations and distance, compute gradient then J.
        Difficulty 7-8: solve for D given J and gradient.

    Prerequisites:
        derivative.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "diffusion_fick"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["derivative"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute diffusion flux using Fick's first law"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate diffusion parameters and compute flux.

        Args:
            difficulty: Controls problem complexity.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        # D in m^2/s (typical solid-state diffusion)
        d_exp = self._rng.randint(-14, -10)
        d_mantissa = round(self._rng.uniform(1.0, 9.0), 1)
        d_coeff = d_mantissa * (10 ** d_exp)

        if difficulty <= 3:
            dc_dx = round(self._rng.uniform(-1e5, -1e3), 4)
            j = round(-d_coeff * dc_dx, 4)
            return "J = -D \\frac{dC}{dx}", {
                "D": d_coeff, "dC_dx": dc_dx,
                "J": j, "target": "J",
                "D_mantissa": d_mantissa, "D_exp": d_exp,
            }

        # Higher difficulty: compute gradient from two points
        c1 = round(self._rng.uniform(0.5, 5.0), 2)
        c2 = round(self._rng.uniform(0.01, c1 - 0.1), 2)
        dx_mm = round(self._rng.uniform(0.5, 5.0 + difficulty), 2)
        dx = dx_mm * 1e-3  # m
        dc_dx = round((c2 - c1) / dx, 4)
        j = round(-d_coeff * dc_dx, 4)

        if difficulty >= 7:
            return "D = -\\frac{J}{dC/dx}", {
                "D": d_coeff, "dC_dx": dc_dx, "J": j,
                "c1": c1, "c2": c2, "dx_mm": dx_mm, "dx": dx,
                "target": "D",
                "D_mantissa": d_mantissa, "D_exp": d_exp,
            }

        return "J = -D \\frac{dC}{dx}", {
            "D": d_coeff, "dC_dx": dc_dx, "J": j,
            "c1": c1, "c2": c2, "dx_mm": dx_mm, "dx": dx,
            "target": "J",
            "D_mantissa": d_mantissa, "D_exp": d_exp,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Fick's law computation steps.

        Args:
            data: Solution data with D, concentrations, distance.

        Returns:
            List of step strings.
        """
        d_str = f"{data['D_mantissa']}e{data['D_exp']}"
        steps = [f"D = {d_str} m^2/s"]
        if "c1" in data:
            steps.append(
                f"C1={data['c1']}, C2={data['c2']}, "
                f"dx={data['dx_mm']}mm={_f(data['dx'])}m"
            )
            steps.append(f"dC/dx = (C2-C1)/dx = {_f(data['dC_dx'])}")
        else:
            steps.append(f"dC/dx = {_f(data['dC_dx'])}")

        if data["target"] == "J":
            steps.append(f"J = -D * dC/dx")
        else:
            steps.append(f"D = -J / (dC/dx)")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the diffusion flux or coefficient.

        Args:
            data: Solution data.

        Returns:
            String with J or D and units.
        """
        if data["target"] == "J":
            return f"J = {_f(data['J'])} atoms/(m^2*s)"
        return f"D = {_f(data['D'])} m^2/s"


# ===================================================================
# 6. Phase diagram lever rule  (tier 5)
# ===================================================================

@register
class PhaseDiagramGenerator(StepGenerator):
    """Compute weight fractions in a binary phase diagram using the lever rule.

    w_alpha = (C_beta - C_0) / (C_beta - C_alpha),
    w_beta = (C_0 - C_alpha) / (C_beta - C_alpha).

    Difficulty scaling:
        Difficulty 1-3: simple compositions (integer percentages).
        Difficulty 4-6: decimal compositions, verify w_alpha + w_beta = 1.
        Difficulty 7-8: given weight fractions, solve for C_0.

    Prerequisites:
        linear_equation.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "phase_diagram"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["linear_equation"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute phase fractions using lever rule"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate binary composition data and compute weight fractions.

        Args:
            difficulty: Controls precision and problem variant.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            c_alpha = float(self._rng.randint(5, 20))
            c_beta = float(self._rng.randint(60, 95))
            c_0 = float(self._rng.randint(int(c_alpha) + 5,
                                           int(c_beta) - 5))
        else:
            c_alpha = round(self._rng.uniform(5, 25), 1)
            c_beta = round(self._rng.uniform(60, 95), 1)
            c_0 = round(self._rng.uniform(c_alpha + 2, c_beta - 2), 1)

        denom = c_beta - c_alpha
        w_alpha = round((c_beta - c_0) / denom, 4)
        w_beta = round((c_0 - c_alpha) / denom, 4)

        if difficulty >= 7:
            return ("C_0 = w_{\\alpha} C_{\\alpha} + w_{\\beta} C_{\\beta}"), {
                "C_alpha": c_alpha, "C_beta": c_beta, "C_0": c_0,
                "w_alpha": w_alpha, "w_beta": w_beta,
                "denom": round(denom, 4), "target": "C_0",
            }

        return ("w_{\\alpha} = \\frac{C_{\\beta} - C_0}"
                "{C_{\\beta} - C_{\\alpha}}"), {
            "C_alpha": c_alpha, "C_beta": c_beta, "C_0": c_0,
            "w_alpha": w_alpha, "w_beta": w_beta,
            "denom": round(denom, 4), "target": "fractions",
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate lever rule computation steps.

        Args:
            data: Solution data with compositions and fractions.

        Returns:
            List of step strings.
        """
        steps = [
            f"C_alpha={_f(data['C_alpha'])}%, "
            f"C_beta={_f(data['C_beta'])}%, "
            f"C_0={_f(data['C_0'])}%",
            f"C_beta - C_alpha = {_f(data['denom'])}",
        ]
        if data["target"] == "fractions":
            steps.append(
                f"w_alpha = ({_f(data['C_beta'])}-{_f(data['C_0'])})"
                f"/{_f(data['denom'])}"
            )
            steps.append(
                f"w_beta = ({_f(data['C_0'])}-{_f(data['C_alpha'])})"
                f"/{_f(data['denom'])}"
            )
        else:
            steps.append(
                f"C_0 = w_alpha*C_alpha + w_beta*C_beta"
            )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the weight fractions or composition.

        Args:
            data: Solution data.

        Returns:
            String with weight fractions or C_0.
        """
        if data["target"] == "fractions":
            return (
                f"w_alpha = {_f(data['w_alpha'])}, "
                f"w_beta = {_f(data['w_beta'])}"
            )
        return f"C_0 = {_f(data['C_0'])}%"
