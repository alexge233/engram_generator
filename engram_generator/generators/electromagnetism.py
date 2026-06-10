"""Electromagnetism generators -- Coulomb's law through Maxwell's equations.

Covers electrostatics (Coulomb, electric field, Gauss, potential),
circuits (capacitance, RC, RLC, AC power), magnetism (Lorentz force,
Faraday induction), and electromagnetic waves. Tiers range from 4
(introductory) to 6 (Maxwell-level).
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register
from engram_generator.generators.physics import ScientificFormatter

# ---------------------------------------------------------------------------
# Physical constants
# ---------------------------------------------------------------------------
_K = 8.99e9            # Coulomb constant  (N m^2 / C^2)
_EPSILON_0 = 8.854e-12  # vacuum permittivity (F/m)
_MU_0 = 4 * math.pi * 1e-7  # vacuum permeability (H/m)
_C = 3e8               # speed of light (m/s)

_fmt = ScientificFormatter.format_sci
_fval = ScientificFormatter.format_value


# ===================================================================
# 1. Coulomb's law  (tier 4)
# ===================================================================

@register
class CoulombsLawGenerator(StepGenerator):
    """Compute electrostatic force between point charges using Coulomb's law.

    F = k * |q1 * q2| / r^2 where k = 8.99e9 N*m^2/C^2.

    Difficulty scaling:
        Difficulty 1-3: integer charges in microcoulombs, integer distances.
        Difficulty 4-6: fractional charges, decimal distances.
        Difficulty 7-8: multiple charges (superposition of two forces).

    Prerequisites:
        multiplication, division.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "coulombs_law"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["multiplication", "division"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute electrostatic force between point charges"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate charge and distance values, then compute force.

        Args:
            difficulty: Controls parameter complexity.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            q1_uC = self._rng.randint(1, 10)
            q2_uC = self._rng.randint(1, 10)
            r = self._rng.randint(1, 5)
            q1 = q1_uC * 1e-6
            q2 = q2_uC * 1e-6
            r_float = float(r)
        elif difficulty <= 6:
            q1_uC = round(self._rng.uniform(0.5, 10.0), 1)
            q2_uC = round(self._rng.uniform(0.5, 10.0), 1)
            r_float = round(self._rng.uniform(0.5, 5.0), 1)
            q1 = q1_uC * 1e-6
            q2 = q2_uC * 1e-6
        else:
            # Superposition: two forces on a test charge
            q1_uC = round(self._rng.uniform(1.0, 8.0), 1)
            q2_uC = round(self._rng.uniform(1.0, 8.0), 1)
            q3_uC = round(self._rng.uniform(1.0, 8.0), 1)
            r1 = round(self._rng.uniform(0.5, 3.0), 1)
            r2 = round(self._rng.uniform(0.5, 3.0), 1)
            q1 = q1_uC * 1e-6
            q2 = q2_uC * 1e-6
            q3 = q3_uC * 1e-6
            f1 = _K * abs(q1 * q3) / r1 ** 2
            f2 = _K * abs(q2 * q3) / r2 ** 2
            f_total = round(f1 + f2, 4)
            return "F = k|q_1 q_3|/r_1^2 + k|q_2 q_3|/r_2^2", {
                "q1_uC": q1_uC, "q2_uC": q2_uC, "q3_uC": q3_uC,
                "r1": r1, "r2": r2,
                "f1": round(f1, 4), "f2": round(f2, 4),
                "force": f_total, "superposition": True,
            }

        force = round(_K * abs(q1 * q2) / r_float ** 2, 4)
        return "F = k\\frac{|q_1 q_2|}{r^2}", {
            "q1_uC": q1_uC, "q2_uC": q2_uC,
            "r": r_float, "force": force, "superposition": False,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate substitution and computation steps.

        Args:
            data: Solution data from _create_problem.

        Returns:
            List of step strings.
        """
        if data["superposition"]:
            return [
                f"F_1 = k|q_1 q_3|/r_1^2, q_1={data['q1_uC']}uC, "
                f"q_3={data['q3_uC']}uC, r_1={data['r1']}m",
                f"F_1 = {_fval(data['f1'])} N",
                f"F_2 = k|q_2 q_3|/r_2^2, q_2={data['q2_uC']}uC, "
                f"r_2={data['r2']}m",
                f"F_2 = {_fval(data['f2'])} N",
            ]
        return [
            f"q_1={data['q1_uC']}uC, q_2={data['q2_uC']}uC, "
            f"r={data['r']}m",
            f"F = (8.99e9)|({data['q1_uC']}e-6)({data['q2_uC']}e-6)|"
            f"/{data['r']}^2",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the final force value.

        Args:
            data: Solution data.

        Returns:
            Force as a string with units.
        """
        return f"F = {_fval(data['force'])} N"


# ===================================================================
# 2. Electric field  (tier 5)
# ===================================================================

@register
class ElectricFieldGenerator(StepGenerator):
    """Compute electric field at a point from one or more charges.

    E = k * q / r^2 for a single charge. For multiple charges the
    fields are summed as vectors along the line.

    Difficulty scaling:
        Difficulty 1-3: single charge, integer microcoulombs.
        Difficulty 4-6: single charge, decimal values.
        Difficulty 7-8: two charges, superposition along a line.

    Prerequisites:
        coulombs_law.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "electric_field"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["coulombs_law"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute electric field at a point"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate charge(s) and distance(s), then compute E.

        Args:
            difficulty: Controls parameter complexity.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            q_uC = self._rng.randint(1, 10)
            r = self._rng.randint(1, 5)
        elif difficulty <= 6:
            q_uC = round(self._rng.uniform(0.5, 10.0), 1)
            r = round(self._rng.uniform(0.5, 5.0), 1)
        else:
            q1_uC = round(self._rng.uniform(1.0, 8.0), 1)
            q2_uC = round(self._rng.uniform(1.0, 8.0), 1)
            r1 = round(self._rng.uniform(0.5, 3.0), 1)
            r2 = round(self._rng.uniform(0.5, 3.0), 1)
            q1 = q1_uC * 1e-6
            q2 = q2_uC * 1e-6
            e1 = _K * abs(q1) / r1 ** 2
            e2 = _K * abs(q2) / r2 ** 2
            e_total = round(e1 + e2, 4)
            return "E = k|q_1|/r_1^2 + k|q_2|/r_2^2", {
                "q1_uC": q1_uC, "q2_uC": q2_uC,
                "r1": r1, "r2": r2,
                "e1": round(e1, 4), "e2": round(e2, 4),
                "E": e_total, "multi": True,
            }

        q = q_uC * 1e-6
        e_field = round(_K * abs(q) / float(r) ** 2, 4)
        return "E = k\\frac{|q|}{r^2}", {
            "q_uC": q_uC, "r": r, "E": e_field, "multi": False,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate computation steps.

        Args:
            data: Solution data.

        Returns:
            List of step strings.
        """
        if data["multi"]:
            return [
                f"E_1 = k|{data['q1_uC']}e-6|/{data['r1']}^2 = "
                f"{_fval(data['e1'])} N/C",
                f"E_2 = k|{data['q2_uC']}e-6|/{data['r2']}^2 = "
                f"{_fval(data['e2'])} N/C",
                f"E = E_1 + E_2",
            ]
        return [
            f"q={data['q_uC']}uC, r={data['r']}m",
            f"E = (8.99e9)|{data['q_uC']}e-6|/{data['r']}^2",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the electric field magnitude.

        Args:
            data: Solution data.

        Returns:
            E as a string with units.
        """
        return f"E = {_fval(data['E'])} N/C"


# ===================================================================
# 3. Gauss's law  (tier 5)
# ===================================================================

@register
class GaussLawGenerator(StepGenerator):
    """Apply Gauss's law for symmetric charge distributions.

    Phi_E = Q_enc / epsilon_0. Uses symmetry (sphere, cylinder, plane)
    to derive E from enclosed charge.

    Difficulty scaling:
        Difficulty 1-3: spherical shell, integer charge in microcoulombs.
        Difficulty 4-5: infinite cylinder (linear charge density).
        Difficulty 6-8: infinite plane (surface charge density).

    Prerequisites:
        electric_field.
    """

    _GEOMETRIES = ["sphere", "cylinder", "plane"]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "gauss_law"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["electric_field"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "apply Gauss's law for symmetric charge distribution"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Gauss's law problem for a chosen geometry.

        Args:
            difficulty: Controls geometry selection and parameters.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            return self._sphere_problem(difficulty)
        if difficulty <= 5:
            return self._cylinder_problem(difficulty)
        return self._plane_problem(difficulty)

    def _sphere_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a spherical Gauss's law problem.

        Args:
            difficulty: Controls charge magnitude.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        q_uC = self._rng.randint(1, 5 + difficulty * 2)
        r = round(self._rng.uniform(0.1, 1.0 + difficulty * 0.5), 2)
        q = q_uC * 1e-6
        e_field = round(q / (4 * math.pi * _EPSILON_0 * r ** 2), 4)
        return "\\Phi_E = Q_{enc}/\\varepsilon_0", {
            "geometry": "sphere", "q_uC": q_uC, "r": r,
            "q": q, "E": e_field,
        }

    def _cylinder_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a cylindrical Gauss's law problem.

        Args:
            difficulty: Controls charge density and radius.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        lam_nCm = self._rng.randint(1, 10 * difficulty)  # nC/m
        r = round(self._rng.uniform(0.01, 0.5), 2)
        lam = lam_nCm * 1e-9  # C/m
        e_field = round(lam / (2 * math.pi * _EPSILON_0 * r), 4)
        return "E = \\lambda/(2\\pi\\varepsilon_0 r)", {
            "geometry": "cylinder", "lam_nCm": lam_nCm, "r": r,
            "lam": lam, "E": e_field,
        }

    def _plane_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an infinite plane Gauss's law problem.

        Args:
            difficulty: Controls surface charge density.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        sigma_nCm2 = self._rng.randint(1, 5 * difficulty)  # nC/m^2
        sigma = sigma_nCm2 * 1e-9
        e_field = round(sigma / (2 * _EPSILON_0), 4)
        return "E = \\sigma/(2\\varepsilon_0)", {
            "geometry": "plane", "sigma_nCm2": sigma_nCm2,
            "sigma": sigma, "E": e_field,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Gauss's law steps for the chosen geometry.

        Args:
            data: Solution data with geometry and parameters.

        Returns:
            List of step strings.
        """
        geom = data["geometry"]
        if geom == "sphere":
            return [
                f"Q_enc = {data['q_uC']}uC = {_fmt(data['q'])} C",
                f"E = Q/(4pi eps_0 r^2), r={data['r']}m",
            ]
        if geom == "cylinder":
            return [
                f"lambda = {data['lam_nCm']} nC/m",
                f"E = lambda/(2pi eps_0 r), r={data['r']}m",
            ]
        return [
            f"sigma = {data['sigma_nCm2']} nC/m^2",
            "E = sigma/(2 eps_0)",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the electric field from Gauss's law.

        Args:
            data: Solution data.

        Returns:
            E as a string with units.
        """
        return f"E = {_fval(data['E'])} N/C"


# ===================================================================
# 4. Electric potential  (tier 5)
# ===================================================================

@register
class ElectricPotentialGenerator(StepGenerator):
    """Compute electric potential V = k*q/r with superposition.

    For a single charge V = k*q/r. For multiple charges
    the potentials are summed as scalars.

    Difficulty scaling:
        Difficulty 1-3: single charge, integer microcoulombs.
        Difficulty 4-6: two charges, superposition.
        Difficulty 7-8: three charges, superposition.

    Prerequisites:
        coulombs_law.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "electric_potential"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["coulombs_law"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute electric potential at a point"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate charge(s) and distance(s), then compute V.

        Args:
            difficulty: Controls number of charges.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            n_charges = 1
        elif difficulty <= 6:
            n_charges = 2
        else:
            n_charges = 3

        charges_uC: list[float] = []
        distances: list[float] = []
        potentials: list[float] = []

        for _ in range(n_charges):
            q_uC = round(self._rng.uniform(1.0, 10.0), 1)
            r = round(self._rng.uniform(0.5, 5.0), 1)
            sign = self._rng.choice([-1, 1])
            q_uC *= sign
            q = q_uC * 1e-6
            v_i = _K * q / r
            charges_uC.append(q_uC)
            distances.append(r)
            potentials.append(round(v_i, 4))

        v_total = round(sum(potentials), 4)
        return "V = k\\sum q_i/r_i", {
            "charges_uC": charges_uC, "distances": distances,
            "potentials": potentials, "V": v_total,
            "n": n_charges,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate potential superposition steps.

        Args:
            data: Solution data with charges, distances, potentials.

        Returns:
            List of step strings.
        """
        steps: list[str] = []
        for i in range(data["n"]):
            steps.append(
                f"V_{i+1} = k({data['charges_uC'][i]}e-6)/"
                f"{data['distances'][i]} = {_fval(data['potentials'][i])} V"
            )
        if data["n"] > 1:
            terms = " + ".join(f"V_{i+1}" for i in range(data["n"]))
            steps.append(f"V = {terms}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the total electric potential.

        Args:
            data: Solution data.

        Returns:
            V as a string with units.
        """
        return f"V = {_fval(data['V'])} V"


# ===================================================================
# 5. Capacitance  (tier 4)
# ===================================================================

@register
class CapacitanceGenerator(StepGenerator):
    """Compute capacitance for parallel plates and series/parallel combos.

    C = epsilon_0 * A / d for a parallel plate capacitor.
    Series: 1/C = sum(1/C_i). Parallel: C = sum(C_i).

    Difficulty scaling:
        Difficulty 1-3: single parallel plate, integer area and distance.
        Difficulty 4-6: two capacitors in series or parallel.
        Difficulty 7-8: three capacitors mixed series-parallel.

    Prerequisites:
        division, multiplication.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "capacitance"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["division", "multiplication"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute capacitance"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate capacitance problem based on difficulty.

        Args:
            difficulty: Controls problem type.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            return self._parallel_plate(difficulty)
        if difficulty <= 6:
            return self._two_cap_combo(difficulty)
        return self._three_cap_combo(difficulty)

    def _parallel_plate(self, difficulty: int) -> tuple[str, dict]:
        """Generate a parallel plate capacitance problem.

        Args:
            difficulty: Controls plate dimensions.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        a_cm2 = self._rng.randint(10, 50 + difficulty * 20)
        d_mm = self._rng.randint(1, 5 + difficulty)
        a = a_cm2 * 1e-4  # m^2
        d = d_mm * 1e-3   # m
        cap = round(_EPSILON_0 * a / d, 4)
        return "C = \\varepsilon_0 A/d", {
            "mode": "plate", "a_cm2": a_cm2, "d_mm": d_mm,
            "a": a, "d": d, "C": cap,
        }

    def _two_cap_combo(self, difficulty: int) -> tuple[str, dict]:
        """Generate a two-capacitor series or parallel problem.

        Args:
            difficulty: Controls capacitor values.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        c1_uF = self._rng.randint(1, 5 + difficulty)
        c2_uF = self._rng.randint(1, 5 + difficulty)
        combo = self._rng.choice(["series", "parallel"])
        c1 = c1_uF * 1e-6
        c2 = c2_uF * 1e-6
        if combo == "series":
            c_total = round(1.0 / (1.0 / c1 + 1.0 / c2), 4)
            formula = "1/C = 1/C_1 + 1/C_2"
        else:
            c_total = round(c1 + c2, 4)
            formula = "C = C_1 + C_2"
        return formula, {
            "mode": combo, "c1_uF": c1_uF, "c2_uF": c2_uF,
            "C": c_total,
        }

    def _three_cap_combo(self, difficulty: int) -> tuple[str, dict]:
        """Generate a three-capacitor mixed series-parallel problem.

        C1 and C2 in parallel, then in series with C3.

        Args:
            difficulty: Controls capacitor values.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        c1_uF = self._rng.randint(1, 5 + difficulty)
        c2_uF = self._rng.randint(1, 5 + difficulty)
        c3_uF = self._rng.randint(1, 5 + difficulty)
        c12 = (c1_uF + c2_uF) * 1e-6  # parallel
        c3 = c3_uF * 1e-6
        c_total = round(1.0 / (1.0 / c12 + 1.0 / c3), 4)
        return "C_{12} = C_1 + C_2, 1/C = 1/C_{12} + 1/C_3", {
            "mode": "mixed",
            "c1_uF": c1_uF, "c2_uF": c2_uF, "c3_uF": c3_uF,
            "c12_uF": c1_uF + c2_uF,
            "C": c_total,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate capacitance computation steps.

        Args:
            data: Solution data with mode and capacitor values.

        Returns:
            List of step strings.
        """
        mode = data["mode"]
        if mode == "plate":
            return [
                f"A={data['a_cm2']}cm^2={_fmt(data['a'])}m^2, "
                f"d={data['d_mm']}mm={_fmt(data['d'])}m",
                f"C = eps_0 * A / d",
            ]
        if mode == "series":
            return [
                f"C_1={data['c1_uF']}uF, C_2={data['c2_uF']}uF",
                f"1/C = 1/{data['c1_uF']}uF + 1/{data['c2_uF']}uF",
            ]
        if mode == "parallel":
            return [
                f"C_1={data['c1_uF']}uF, C_2={data['c2_uF']}uF",
                f"C = {data['c1_uF']} + {data['c2_uF']} uF",
            ]
        # mixed
        return [
            f"C_1={data['c1_uF']}uF, C_2={data['c2_uF']}uF, "
            f"C_3={data['c3_uF']}uF",
            f"C_12 = {data['c1_uF']} + {data['c2_uF']} = "
            f"{data['c12_uF']}uF",
            f"1/C = 1/{data['c12_uF']}uF + 1/{data['c3_uF']}uF",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the total capacitance.

        Args:
            data: Solution data.

        Returns:
            C as a string with units.
        """
        return f"C = {_fmt(data['C'])} F"


# ===================================================================
# 6. RC circuit  (tier 5)
# ===================================================================

@register
class RCCircuitGenerator(StepGenerator):
    """Compute RC time constant and voltage during charging/discharging.

    tau = R * C. Charging: V(t) = V0 * (1 - e^(-t/RC)).
    Discharging: V(t) = V0 * e^(-t/RC).

    Difficulty scaling:
        Difficulty 1-3: compute tau only, integer R and C.
        Difficulty 4-6: compute V(t) for charging.
        Difficulty 7-8: compute V(t) for discharging at given time.

    Prerequisites:
        ohms_law, capacitance.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "rc_circuit"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["ohms_law", "capacitance"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "analyse RC circuit transient response"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate RC circuit parameters and compute results.

        Args:
            difficulty: Controls problem complexity.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        r_kohm = self._rng.randint(1, 10 + difficulty * 2)
        c_uF = self._rng.randint(1, 10 + difficulty * 2)
        r = r_kohm * 1e3
        c = c_uF * 1e-6
        tau = round(r * c, 4)

        if difficulty <= 3:
            return "\\tau = RC", {
                "r_kohm": r_kohm, "c_uF": c_uF,
                "R": r, "C": c, "tau": tau,
                "mode": "tau",
            }

        v0 = self._rng.randint(5, 25)
        # Pick t as a multiple of tau for cleaner numbers
        t_mult = round(self._rng.uniform(0.5, 3.0), 1)
        t = round(t_mult * tau, 4)

        if difficulty <= 6:
            # Charging
            v_t = round(v0 * (1 - math.exp(-t / tau)), 4)
            return "V(t) = V_0(1 - e^{-t/RC})", {
                "r_kohm": r_kohm, "c_uF": c_uF,
                "R": r, "C": c, "tau": tau,
                "V0": v0, "t": t, "V_t": v_t,
                "mode": "charge",
            }

        # Discharging
        v_t = round(v0 * math.exp(-t / tau), 4)
        return "V(t) = V_0 e^{-t/RC}", {
            "r_kohm": r_kohm, "c_uF": c_uF,
            "R": r, "C": c, "tau": tau,
            "V0": v0, "t": t, "V_t": v_t,
            "mode": "discharge",
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate RC circuit computation steps.

        Args:
            data: Solution data with R, C, and mode.

        Returns:
            List of step strings.
        """
        steps = [
            f"R={data['r_kohm']}kohm, C={data['c_uF']}uF",
            f"tau = RC = {_fval(data['tau'])} s",
        ]
        if data["mode"] == "tau":
            return steps
        steps.append(f"V0={data['V0']}V, t={_fval(data['t'])}s")
        if data["mode"] == "charge":
            steps.append(f"V(t) = {data['V0']}(1 - e^(-{_fval(data['t'])}/{_fval(data['tau'])}))")
        else:
            steps.append(f"V(t) = {data['V0']} e^(-{_fval(data['t'])}/{_fval(data['tau'])})")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the RC circuit result.

        Args:
            data: Solution data.

        Returns:
            Tau or V(t) as a string with units.
        """
        if data["mode"] == "tau":
            return f"tau = {_fval(data['tau'])} s"
        return f"V(t) = {_fval(data['V_t'])} V"


# ===================================================================
# 7. Magnetic force on moving charge  (tier 5)
# ===================================================================

@register
class MagneticForceGenerator(StepGenerator):
    """Compute magnetic force on a moving charge: F = qv x B.

    |F| = |q| * v * B * sin(theta). Generates problems with
    varying angles between velocity and magnetic field.

    Difficulty scaling:
        Difficulty 1-3: theta = 90 deg (sin=1), integer values.
        Difficulty 4-6: theta = 30 or 60 deg.
        Difficulty 7-8: arbitrary angle, compute direction.

    Prerequisites:
        cross_product.
    """

    _SPECIAL_ANGLES = {
        30: 0.5,
        45: math.sqrt(2) / 2,
        60: math.sqrt(3) / 2,
        90: 1.0,
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "magnetic_force"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["cross_product"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute magnetic force on a moving charge"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate charge, velocity, B-field, angle and compute force.

        Args:
            difficulty: Controls angle complexity.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        q_uC = round(self._rng.uniform(1.0, 10.0), 1)
        v = self._rng.randint(100, 1000 + difficulty * 500)
        b_mT = round(self._rng.uniform(0.1, 5.0), 1)

        if difficulty <= 3:
            theta = 90
        elif difficulty <= 6:
            theta = self._rng.choice([30, 60])
        else:
            theta = self._rng.choice([30, 45, 60, 90])

        q = q_uC * 1e-6
        b = b_mT * 1e-3
        sin_theta = round(math.sin(math.radians(theta)), 4)
        force = round(abs(q) * v * b * sin_theta, 4)

        return "F = |q|vB\\sin\\theta", {
            "q_uC": q_uC, "v": v, "b_mT": b_mT,
            "theta": theta, "sin_theta": sin_theta,
            "force": force,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate magnetic force computation steps.

        Args:
            data: Solution data with q, v, B, theta.

        Returns:
            List of step strings.
        """
        steps = [
            f"q={data['q_uC']}uC, v={data['v']}m/s, "
            f"B={data['b_mT']}mT, theta={data['theta']}deg",
            f"sin({data['theta']}) = {_fval(data['sin_theta'])}",
            f"F = |{data['q_uC']}e-6|*{data['v']}*"
            f"{data['b_mT']}e-3*{_fval(data['sin_theta'])}",
        ]
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the magnetic force magnitude.

        Args:
            data: Solution data.

        Returns:
            F as a string with units.
        """
        return f"F = {_fval(data['force'])} N"


# ===================================================================
# 8. Faraday's law  (tier 6)
# ===================================================================

@register
class FaradayLawGenerator(StepGenerator):
    """Compute induced EMF from changing magnetic flux (Faraday's law).

    EMF = -N * d(Phi_B)/dt where Phi_B = B * A * cos(theta).

    Difficulty scaling:
        Difficulty 1-3: single loop, B changes linearly, theta=0.
        Difficulty 4-6: N turns, B changes linearly, theta=0.
        Difficulty 7-8: N turns, area changes, arbitrary angle.

    Prerequisites:
        derivative.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "faraday_law"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

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
        return "compute induced EMF using Faraday's law"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate Faraday's law problem parameters.

        Args:
            difficulty: Controls problem complexity.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            n = 1
            theta = 0
        elif difficulty <= 6:
            n = self._rng.randint(10, 50 + difficulty * 10)
            theta = 0
        else:
            n = self._rng.randint(10, 100)
            theta = self._rng.choice([0, 30, 45, 60])

        cos_theta = round(math.cos(math.radians(theta)), 4)

        # B changes linearly: dB/dt
        b_initial = round(self._rng.uniform(0.1, 2.0), 2)
        b_final = round(self._rng.uniform(0.1, 2.0), 2)
        while b_final == b_initial:
            b_final = round(self._rng.uniform(0.1, 2.0), 2)
        dt = round(self._rng.uniform(0.01, 1.0), 2)

        a_cm2 = self._rng.randint(10, 100 + difficulty * 20)
        a = a_cm2 * 1e-4

        db_dt = (b_final - b_initial) / dt
        dphi_dt = db_dt * a * cos_theta
        emf = round(-n * dphi_dt, 4)

        return "EMF = -N \\frac{d\\Phi_B}{dt}", {
            "N": n, "theta": theta, "cos_theta": cos_theta,
            "B_i": b_initial, "B_f": b_final, "dt": dt,
            "a_cm2": a_cm2, "A": a,
            "dB_dt": round(db_dt, 4),
            "dPhi_dt": round(dphi_dt, 4),
            "EMF": emf,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Faraday's law computation steps.

        Args:
            data: Solution data with N, B, A, dt.

        Returns:
            List of step strings.
        """
        steps = [
            f"N={data['N']}, A={data['a_cm2']}cm^2, "
            f"B: {data['B_i']}T -> {data['B_f']}T in {data['dt']}s",
            f"dB/dt = ({data['B_f']}-{data['B_i']})/{data['dt']} = "
            f"{_fval(data['dB_dt'])} T/s",
        ]
        if data["theta"] != 0:
            steps.append(f"cos({data['theta']}) = {_fval(data['cos_theta'])}")
        steps.append(
            f"EMF = -{data['N']} * {_fval(data['dB_dt'])} * "
            f"{_fmt(data['A'])}"
        )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the induced EMF.

        Args:
            data: Solution data.

        Returns:
            EMF as a string with units.
        """
        return f"EMF = {_fval(data['EMF'])} V"


# ===================================================================
# 9. RLC impedance  (tier 6)
# ===================================================================

@register
class RLCImpedanceGenerator(StepGenerator):
    """Compute impedance of a series RLC circuit.

    Z = sqrt(R^2 + (X_L - X_C)^2) where X_L = omega*L,
    X_C = 1/(omega*C), and omega = 2*pi*f.

    Difficulty scaling:
        Difficulty 1-3: RL circuit only (C=0 => X_C=0).
        Difficulty 4-6: full RLC with integer component values.
        Difficulty 7-8: full RLC with decimal values, compute phase.

    Prerequisites:
        complex_arithmetic.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "rlc_impedance"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["complex_arithmetic"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute impedance of RLC circuit"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate RLC circuit values and compute impedance.

        Args:
            difficulty: Controls circuit complexity.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        r = self._rng.randint(10, 100 + difficulty * 50)
        f_hz = self._rng.randint(50, 500 + difficulty * 200)
        omega = 2 * math.pi * f_hz

        l_mH = self._rng.randint(10, 100 + difficulty * 20)
        l_val = l_mH * 1e-3
        x_l = round(omega * l_val, 4)

        if difficulty <= 3:
            x_c = 0.0
            c_uF = 0
        else:
            c_uF = self._rng.randint(1, 50 + difficulty * 10)
            c_val = c_uF * 1e-6
            x_c = round(1.0 / (omega * c_val), 4)

        x_net = round(x_l - x_c, 4)
        z = round(math.sqrt(r ** 2 + x_net ** 2), 4)
        phi_rad = math.atan2(x_net, r)
        phi_deg = round(math.degrees(phi_rad), 4)

        return "Z = \\sqrt{R^2 + (X_L - X_C)^2}", {
            "R": r, "f": f_hz, "omega": round(omega, 4),
            "L_mH": l_mH, "C_uF": c_uF,
            "X_L": x_l, "X_C": x_c, "X_net": x_net,
            "Z": z, "phi_deg": phi_deg,
            "has_C": difficulty > 3,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate impedance computation steps.

        Args:
            data: Solution data with R, L, C, frequency.

        Returns:
            List of step strings.
        """
        steps = [
            f"f={data['f']}Hz, omega={_fval(data['omega'])} rad/s",
            f"X_L = omega*L = {_fval(data['X_L'])} ohm",
        ]
        if data["has_C"]:
            steps.append(f"X_C = 1/(omega*C) = {_fval(data['X_C'])} ohm")
        steps.append(
            f"X_L - X_C = {_fval(data['X_net'])} ohm"
        )
        steps.append(
            f"Z = sqrt({data['R']}^2 + {_fval(data['X_net'])}^2)"
        )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the impedance magnitude.

        Args:
            data: Solution data.

        Returns:
            Z as a string with units.
        """
        return f"Z = {_fval(data['Z'])} ohm"


# ===================================================================
# 10. AC power  (tier 6)
# ===================================================================

@register
class ACPowerGenerator(StepGenerator):
    """Compute AC power: real, reactive, and apparent.

    P = V*I*cos(phi), Q = V*I*sin(phi), S = V*I.

    Difficulty scaling:
        Difficulty 1-3: compute real power only, phi given.
        Difficulty 4-6: compute P, Q, and S.
        Difficulty 7-8: derive phi from R, X_L, X_C first.

    Prerequisites:
        rlc_impedance.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "ac_power"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["rlc_impedance"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute AC power quantities"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate AC power problem parameters.

        Args:
            difficulty: Controls what to compute.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        v_rms = self._rng.randint(50, 240)
        i_rms = round(self._rng.uniform(0.5, 10.0), 1)

        if difficulty <= 6:
            phi_deg = self._rng.choice([0, 30, 45, 60])
        else:
            # Derive phi from circuit elements
            r = self._rng.randint(10, 100)
            x_net = self._rng.randint(-50, 50)
            phi_deg = round(math.degrees(math.atan2(x_net, r)), 4)

        phi_rad = math.radians(phi_deg)
        cos_phi = round(math.cos(phi_rad), 4)
        sin_phi = round(math.sin(phi_rad), 4)

        s = round(v_rms * i_rms, 4)
        p = round(s * cos_phi, 4)
        q = round(s * sin_phi, 4)

        return "P = VI\\cos\\phi, Q = VI\\sin\\phi, S = VI", {
            "V": v_rms, "I": i_rms, "phi_deg": phi_deg,
            "cos_phi": cos_phi, "sin_phi": sin_phi,
            "P": p, "Q": q, "S": s,
            "full": difficulty > 3,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate AC power computation steps.

        Args:
            data: Solution data with V, I, phi.

        Returns:
            List of step strings.
        """
        steps = [
            f"V={data['V']}V, I={data['I']}A, "
            f"phi={_fval(data['phi_deg'])}deg",
            f"cos(phi) = {_fval(data['cos_phi'])}, "
            f"sin(phi) = {_fval(data['sin_phi'])}",
            f"S = V*I = {_fval(data['S'])} VA",
            f"P = S*cos(phi) = {_fval(data['P'])} W",
        ]
        if data["full"]:
            steps.append(f"Q = S*sin(phi) = {_fval(data['Q'])} VAR")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the AC power result.

        Args:
            data: Solution data.

        Returns:
            P (and Q, S if full) as a string.
        """
        if data["full"]:
            return (
                f"P = {_fval(data['P'])} W, "
                f"Q = {_fval(data['Q'])} VAR, "
                f"S = {_fval(data['S'])} VA"
            )
        return f"P = {_fval(data['P'])} W"


# ===================================================================
# 11. Maxwell displacement current  (tier 6)
# ===================================================================

@register
class MaxwellDisplacementGenerator(StepGenerator):
    """Compute displacement current from a changing electric field.

    I_d = epsilon_0 * d(Phi_E)/dt where Phi_E = E * A.
    The displacement current completes Ampere's law for
    time-varying fields.

    Difficulty scaling:
        Difficulty 1-3: uniform E changing linearly, given area.
        Difficulty 4-6: E changes linearly, compute d(Phi_E)/dt.
        Difficulty 7-8: E given as function, compute rate and I_d.

    Prerequisites:
        faraday_law.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "maxwell_displacement"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["faraday_law"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute displacement current from changing E field"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate displacement current problem parameters.

        Args:
            difficulty: Controls problem complexity.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        # Area of capacitor plate
        a_cm2 = self._rng.randint(5, 50 + difficulty * 15)
        a = a_cm2 * 1e-4  # m^2

        # E field changes linearly
        e_initial = self._rng.randint(100, 1000 + difficulty * 500)
        e_final = self._rng.randint(100, 1000 + difficulty * 500)
        while e_final == e_initial:
            e_final = self._rng.randint(100, 1000 + difficulty * 500)

        dt_ms = self._rng.randint(1, 10 + difficulty * 5)
        dt = dt_ms * 1e-3

        de_dt = (e_final - e_initial) / dt
        dphi_e_dt = de_dt * a
        i_d = round(_EPSILON_0 * dphi_e_dt, 4)

        return "I_d = \\varepsilon_0 \\frac{d\\Phi_E}{dt}", {
            "a_cm2": a_cm2, "A": a,
            "E_i": e_initial, "E_f": e_final,
            "dt_ms": dt_ms, "dt": dt,
            "dE_dt": round(de_dt, 4),
            "dPhi_E_dt": round(dphi_e_dt, 4),
            "I_d": i_d,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate displacement current computation steps.

        Args:
            data: Solution data with E, A, dt.

        Returns:
            List of step strings.
        """
        return [
            f"A={data['a_cm2']}cm^2={_fmt(data['A'])}m^2",
            f"dE/dt = ({data['E_f']}-{data['E_i']})/{_fval(data['dt'])}s "
            f"= {_fval(data['dE_dt'])} V/(m*s)",
            f"dPhi_E/dt = dE/dt * A = {_fval(data['dPhi_E_dt'])} V*m/s",
            f"I_d = eps_0 * dPhi_E/dt",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the displacement current.

        Args:
            data: Solution data.

        Returns:
            I_d as a string with units.
        """
        return f"I_d = {_fmt(data['I_d'])} A"


# ===================================================================
# 12. Electromagnetic wave  (tier 5)
# ===================================================================

@register
class ElectromagneticWaveGenerator(StepGenerator):
    """Compute EM wave properties: E/B = c, c = f*lambda.

    Relates electric and magnetic field amplitudes via the speed
    of light, and connects frequency to wavelength.

    Difficulty scaling:
        Difficulty 1-3: given f, find lambda (or vice versa).
        Difficulty 4-6: given E0, find B0 = E0/c.
        Difficulty 7-8: combine both relations, compute energy density.

    Prerequisites:
        wave_equation.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "electromagnetic_wave"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["wave_equation"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute electromagnetic wave properties"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate EM wave problem parameters.

        Args:
            difficulty: Controls what to compute.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            return self._freq_wavelength_problem(difficulty)
        if difficulty <= 6:
            return self._field_ratio_problem(difficulty)
        return self._combined_problem(difficulty)

    def _freq_wavelength_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a frequency-wavelength conversion problem.

        Args:
            difficulty: Controls magnitude of frequency.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        # Choose to solve for f or lambda
        solve_for = self._rng.choice(["f", "lambda"])
        if solve_for == "lambda":
            f_MHz = self._rng.randint(1, 100 + difficulty * 100)
            f = f_MHz * 1e6
            lam = round(_C / f, 4)
            return "c = f\\lambda", {
                "mode": "find_lambda", "f_MHz": f_MHz, "f": f,
                "lambda": lam,
            }
        # solve for f
        lam_nm = self._rng.randint(100, 800)
        lam = lam_nm * 1e-9
        f = round(_C / lam, 4)
        return "c = f\\lambda", {
            "mode": "find_f", "lam_nm": lam_nm, "lambda": lam,
            "f": f,
        }

    def _field_ratio_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an E/B = c problem.

        Args:
            difficulty: Controls E field magnitude.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        e0 = self._rng.randint(100, 5000 + difficulty * 1000)
        b0 = round(e0 / _C, 4)
        return "E_0/B_0 = c", {
            "mode": "field_ratio", "E0": e0, "B0": b0,
        }

    def _combined_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a combined freq-wavelength and field ratio problem.

        Args:
            difficulty: Controls parameter ranges.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        f_GHz = round(self._rng.uniform(1.0, 100.0), 1)
        f = f_GHz * 1e9
        lam = round(_C / f, 4)
        e0 = self._rng.randint(500, 5000)
        b0 = round(e0 / _C, 4)
        # Energy density: u = epsilon_0 * E0^2 / 2
        u = round(_EPSILON_0 * e0 ** 2 / 2, 4)
        return "c = f\\lambda, E_0/B_0 = c", {
            "mode": "combined", "f_GHz": f_GHz, "f": f,
            "lambda": lam, "E0": e0, "B0": b0,
            "u": u,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate EM wave computation steps.

        Args:
            data: Solution data with mode and parameters.

        Returns:
            List of step strings.
        """
        mode = data["mode"]
        if mode == "find_lambda":
            return [
                f"f = {data['f_MHz']}MHz = {_fmt(data['f'])} Hz",
                f"lambda = c/f = {_fmt(_C)}/{_fmt(data['f'])}",
            ]
        if mode == "find_f":
            return [
                f"lambda = {data['lam_nm']}nm = {_fmt(data['lambda'])} m",
                f"f = c/lambda = {_fmt(_C)}/{_fmt(data['lambda'])}",
            ]
        if mode == "field_ratio":
            return [
                f"E_0 = {data['E0']} V/m",
                f"B_0 = E_0/c = {data['E0']}/{_fmt(_C)}",
            ]
        # combined
        return [
            f"f = {data['f_GHz']}GHz = {_fmt(data['f'])} Hz",
            f"lambda = c/f = {_fmt(data['lambda'])} m",
            f"B_0 = E_0/c = {data['E0']}/{_fmt(_C)} = {_fmt(data['B0'])} T",
            f"u = eps_0*E_0^2/2 = {_fmt(data['u'])} J/m^3",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the EM wave result.

        Args:
            data: Solution data.

        Returns:
            Result string appropriate to the mode.
        """
        mode = data["mode"]
        if mode == "find_lambda":
            return f"lambda = {_fmt(data['lambda'])} m"
        if mode == "find_f":
            return f"f = {_fmt(data['f'])} Hz"
        if mode == "field_ratio":
            return f"B_0 = {_fmt(data['B0'])} T"
        return (
            f"lambda = {_fmt(data['lambda'])} m, "
            f"B_0 = {_fmt(data['B0'])} T"
        )
