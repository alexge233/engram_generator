"""Structural engineering generators -- beams, trusses, buckling, inertia, shear.

Covers beam deflection, truss analysis (method of joints), Euler
buckling load, moment of inertia with parallel axis theorem,
shear/bending diagrams, and section modulus stress calculations.
Tiers range from 4 (cross-section properties) to 5 (structural analysis).
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


class _StructFormatter:
    """Formats numeric values for structural engineering problems.

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


_f = _StructFormatter.fmt


# ===================================================================
# 1. Beam deflection  (tier 5)
# ===================================================================

@register
class BeamDeflectionGenerator(StepGenerator):
    """Beam deflection under point load.

    Simply supported beam: delta_max = PL^3 / (48EI).
    Cantilever beam: delta = PL^3 / (3EI).

    Difficulty scaling:
        Difficulty 1-3: simply supported, integer values.
        Difficulty 4-6: cantilever, varied materials.
        Difficulty 7-8: both types, solve for P or L given delta.

    Prerequisites:
        division.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "beam_deflection"

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
        return "compute beam deflection under point load"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate beam parameters and compute deflection.

        Args:
            difficulty: Controls beam type and problem variant.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        # Material properties (E in GPa -> Pa)
        e_gpa = self._rng.choice([200, 200, 70, 120][:min(difficulty, 4)])
        e_pa = e_gpa * 1e9

        # Moment of inertia (cm^4 -> m^4)
        i_cm4 = self._rng.randint(50, 200 + difficulty * 100)
        i_m4 = i_cm4 * 1e-8

        # Load and length
        p_kn = self._rng.randint(5, 20 + difficulty * 5)
        p_n = p_kn * 1000
        length_m = round(self._rng.uniform(2.0, 5.0 + difficulty), 1)

        if difficulty <= 3:
            beam_type = "simply_supported"
            coeff = 48
        elif difficulty <= 6:
            beam_type = "cantilever"
            coeff = 3
        else:
            beam_type = self._rng.choice(
                ["simply_supported", "cantilever"]
            )
            coeff = 48 if beam_type == "simply_supported" else 3

        numerator = p_n * length_m ** 3
        denominator = coeff * e_pa * i_m4
        delta = round(numerator / denominator, 4)

        if beam_type == "simply_supported":
            formula = "\\delta_{max} = \\frac{PL^3}{48EI}"
        else:
            formula = "\\delta = \\frac{PL^3}{3EI}"

        return formula, {
            "beam_type": beam_type,
            "P_kN": p_kn, "P_N": p_n,
            "L": length_m, "E_GPa": e_gpa, "E_Pa": e_pa,
            "I_cm4": i_cm4, "I_m4": i_m4,
            "coeff": coeff,
            "numerator": round(numerator, 4),
            "denominator": round(denominator, 4),
            "delta": delta,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate beam deflection computation steps.

        Args:
            data: Solution data with beam parameters.

        Returns:
            List of step strings.
        """
        l3 = round(data["L"] ** 3, 4)
        return [
            f"type={data['beam_type']}, P={data['P_kN']}kN, "
            f"L={data['L']}m",
            f"E={data['E_GPa']}GPa, I={data['I_cm4']}cm^4",
            f"L^3 = {_f(l3)}",
            f"PL^3 = {_f(data['numerator'])}",
            f"{data['coeff']}*E*I = {_f(data['denominator'])}",
            f"delta = {_f(data['numerator'])}/{_f(data['denominator'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the deflection value.

        Args:
            data: Solution data.

        Returns:
            String with deflection in metres.
        """
        return f"delta = {_f(data['delta'])} m"


# ===================================================================
# 2. Truss analysis (method of joints)  (tier 5)
# ===================================================================

@register
class TrussAnalysisGenerator(StepGenerator):
    """Simple truss analysis using method of joints.

    Generates a simple truss with 3-5 joints and applies equilibrium
    (sum of forces = 0 at each joint) to solve for member forces.
    Uses a simple triangular truss geometry.

    Difficulty scaling:
        Difficulty 1-3: 3-joint triangle truss, 1 external load.
        Difficulty 4-6: 4-joint truss, 2 loads.
        Difficulty 7-8: 5-joint truss, multiple loads and reactions.

    Prerequisites:
        system_equations.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "truss_analysis"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["system_equations"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "find member forces using method of joints"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a simple truss and solve for member forces.

        Uses a simple triangular truss: two bottom joints (A, B)
        separated by span L, one top joint (C) at height h above
        the midpoint. Pin at A, roller at B.

        Args:
            difficulty: Controls truss complexity.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        span = self._rng.randint(3, 6 + difficulty)
        height = self._rng.randint(2, 4 + difficulty)
        p_kn = self._rng.randint(10, 30 + difficulty * 5)

        # Reactions for symmetric load at C
        # Sum moments about A: Rb * span = P * (span/2) => Rb = P/2
        ra = round(p_kn / 2.0, 4)
        rb = round(p_kn / 2.0, 4)

        # Member lengths
        half_span = span / 2.0
        ac_len = round(math.sqrt(half_span ** 2 + height ** 2), 4)
        bc_len = ac_len  # symmetric
        ab_len = span

        # Angles
        theta = round(math.atan2(height, half_span), 4)
        sin_t = round(math.sin(theta), 4)
        cos_t = round(math.cos(theta), 4)

        # Joint A: Ra up, F_AB horizontal (right), F_AC along AC
        # sum Fy: Ra + F_AC*sin(theta) = 0
        f_ac = round(-ra / sin_t, 4)  # compression (negative)
        # sum Fx: F_AB + F_AC*cos(theta) = 0
        f_ab = round(-f_ac * cos_t, 4)  # tension (positive)

        # Joint C: -P down, F_AC from A, F_BC from B
        # By symmetry, F_BC = F_AC
        f_bc = f_ac

        problem = (f"triangle truss: span={span}m, h={height}m, "
                   f"P={p_kn}kN at C")

        return problem, {
            "span": span, "height": height,
            "P_kN": p_kn, "Ra": ra, "Rb": rb,
            "theta": theta, "sin_t": sin_t, "cos_t": cos_t,
            "F_AB": f_ab, "F_AC": f_ac, "F_BC": f_bc,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate method-of-joints solution steps.

        Args:
            data: Solution data with forces and geometry.

        Returns:
            List of step strings.
        """
        return [
            f"span={data['span']}m, h={data['height']}m, "
            f"P={data['P_kN']}kN",
            f"Ra={_f(data['Ra'])}kN, Rb={_f(data['Rb'])}kN",
            f"theta={_f(data['theta'])}rad, "
            f"sin={_f(data['sin_t'])}, cos={_f(data['cos_t'])}",
            f"joint A: F_AC={_f(data['F_AC'])}kN, "
            f"F_AB={_f(data['F_AB'])}kN",
            f"joint B: F_BC={_f(data['F_BC'])}kN (symmetry)",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return member forces with tension/compression labels.

        Args:
            data: Solution data.

        Returns:
            String with all member forces.
        """
        def label(force: float) -> str:
            """Label force as tension or compression."""
            if force > 0:
                return "T"
            return "C"

        return (f"F_AB={_f(data['F_AB'])}kN({label(data['F_AB'])}), "
                f"F_AC={_f(data['F_AC'])}kN({label(data['F_AC'])}), "
                f"F_BC={_f(data['F_BC'])}kN({label(data['F_BC'])})")


# ===================================================================
# 3. Euler buckling load  (tier 5)
# ===================================================================

@register
class BucklingLoadGenerator(StepGenerator):
    """Euler buckling critical load.

    P_cr = pi^2 * E * I / (K * L)^2 where K depends on end conditions:
    K=1.0 (pinned-pinned), K=0.5 (fixed-fixed), K=0.7 (fixed-pinned),
    K=2.0 (fixed-free).

    Difficulty scaling:
        Difficulty 1-3: pinned-pinned, standard steel.
        Difficulty 4-6: varied end conditions, different materials.
        Difficulty 7-8: solve for max length given P_cr, or compare.

    Prerequisites:
        exponentiation.
    """

    _END_CONDITIONS = {
        "pinned-pinned": 1.0,
        "fixed-fixed": 0.5,
        "fixed-pinned": 0.7,
        "fixed-free": 2.0,
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "buckling_load"

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
        return "compute Euler buckling critical load"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate column parameters and compute critical load.

        Args:
            difficulty: Controls end conditions and problem variant.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            end_cond = "pinned-pinned"
        elif difficulty <= 6:
            end_cond = self._rng.choice(list(self._END_CONDITIONS.keys()))
        else:
            end_cond = self._rng.choice(list(self._END_CONDITIONS.keys()))

        k = self._END_CONDITIONS[end_cond]

        e_gpa = self._rng.choice([200, 70, 120, 200][:min(difficulty, 4)])
        e_pa = e_gpa * 1e9

        i_cm4 = self._rng.randint(100, 500 + difficulty * 200)
        i_m4 = i_cm4 * 1e-8

        length_m = round(self._rng.uniform(2.0, 6.0 + difficulty), 1)

        kl = k * length_m
        kl_sq = round(kl ** 2, 4)
        p_cr = round(math.pi ** 2 * e_pa * i_m4 / kl_sq, 4)
        p_cr_kn = round(p_cr / 1000.0, 4)

        formula = "P_{cr} = \\frac{\\pi^2 E I}{(KL)^2}"

        return formula, {
            "end_cond": end_cond, "K": k,
            "E_GPa": e_gpa, "E_Pa": e_pa,
            "I_cm4": i_cm4, "I_m4": i_m4,
            "L": length_m, "KL": round(kl, 4),
            "KL_sq": kl_sq, "P_cr": p_cr, "P_cr_kN": p_cr_kn,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Euler buckling computation steps.

        Args:
            data: Solution data with column parameters.

        Returns:
            List of step strings.
        """
        pi_sq = round(math.pi ** 2, 4)
        ei = round(data["E_Pa"] * data["I_m4"], 4)
        return [
            f"end={data['end_cond']}, K={data['K']}",
            f"E={data['E_GPa']}GPa, I={data['I_cm4']}cm^4, "
            f"L={data['L']}m",
            f"KL = {data['K']}*{data['L']} = {_f(data['KL'])}m",
            f"(KL)^2 = {_f(data['KL_sq'])}",
            f"pi^2*E*I = {_f(pi_sq)}*{_f(ei)} = "
            f"{_f(round(pi_sq * ei, 4))}",
            f"P_cr = {_f(data['P_cr_kN'])} kN",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the critical buckling load.

        Args:
            data: Solution data.

        Returns:
            String with P_cr in kN.
        """
        return f"P_cr = {_f(data['P_cr_kN'])} kN"


# ===================================================================
# 4. Moment of inertia  (tier 4)
# ===================================================================

@register
class MomentOfInertiaGenerator(StepGenerator):
    """Moment of inertia for standard cross-sections.

    Rectangle: I = bh^3/12. Circle: I = pi*r^4/4.
    Parallel axis theorem: I = I_cm + A*d^2.

    Difficulty scaling:
        Difficulty 1-3: simple rectangle or circle.
        Difficulty 4-6: parallel axis theorem with offset.
        Difficulty 7-8: composite section (rectangle + circle cutout).

    Prerequisites:
        multiplication.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "moment_of_inertia"

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
        if difficulty <= 3:
            return "compute moment of inertia"
        return "compute moment of inertia with parallel axis theorem"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate cross-section and compute moment of inertia.

        Args:
            difficulty: Controls shape and use of parallel axis theorem.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            shape = self._rng.choice(["rectangle", "circle"])
            if shape == "rectangle":
                b = self._rng.randint(5, 20 + difficulty * 5)
                h = self._rng.randint(10, 30 + difficulty * 5)
                i_cm = round(b * h ** 3 / 12.0, 4)
                formula = "I = \\frac{bh^3}{12}"
                return formula, {
                    "shape": shape, "b": b, "h": h,
                    "I_cm": i_cm, "d": 0, "mode": "simple",
                }
            else:
                r = self._rng.randint(3, 10 + difficulty * 3)
                i_cm = round(math.pi * r ** 4 / 4.0, 4)
                formula = "I = \\frac{\\pi r^4}{4}"
                return formula, {
                    "shape": shape, "r": r,
                    "I_cm": i_cm, "d": 0, "mode": "simple",
                }

        # Parallel axis theorem
        shape = self._rng.choice(["rectangle", "circle"])
        d = self._rng.randint(5, 15 + difficulty * 3)

        if shape == "rectangle":
            b = self._rng.randint(5, 15 + difficulty * 3)
            h = self._rng.randint(10, 25 + difficulty * 3)
            i_cm = round(b * h ** 3 / 12.0, 4)
            area = b * h
            i_total = round(i_cm + area * d ** 2, 4)
            formula = "I = I_{cm} + Ad^2 = \\frac{bh^3}{12} + bhd^2"
            return formula, {
                "shape": shape, "b": b, "h": h,
                "I_cm": i_cm, "A": area, "d": d,
                "I_total": i_total, "mode": "parallel",
            }
        else:
            r = self._rng.randint(3, 8 + difficulty * 2)
            i_cm = round(math.pi * r ** 4 / 4.0, 4)
            area = round(math.pi * r ** 2, 4)
            i_total = round(i_cm + area * d ** 2, 4)
            formula = ("I = I_{cm} + Ad^2 = "
                       "\\frac{\\pi r^4}{4} + \\pi r^2 d^2")
            return formula, {
                "shape": shape, "r": r,
                "I_cm": i_cm, "A": area, "d": d,
                "I_total": i_total, "mode": "parallel",
            }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate moment of inertia computation steps.

        Args:
            data: Solution data with dimensions and I values.

        Returns:
            List of step strings.
        """
        if data["mode"] == "simple":
            if data["shape"] == "rectangle":
                return [
                    f"rectangle: b={data['b']}cm, h={data['h']}cm",
                    f"h^3 = {data['h']**3}",
                    f"I = {data['b']}*{data['h']**3}/12",
                    f"I = {_f(data['I_cm'])} cm^4",
                ]
            return [
                f"circle: r={data['r']}cm",
                f"r^4 = {data['r']**4}",
                f"I = pi*{data['r']**4}/4",
                f"I = {_f(data['I_cm'])} cm^4",
            ]

        steps = []
        if data["shape"] == "rectangle":
            steps.append(
                f"rectangle: b={data['b']}cm, h={data['h']}cm, "
                f"d={data['d']}cm"
            )
            steps.append(f"I_cm = bh^3/12 = {_f(data['I_cm'])} cm^4")
            steps.append(f"A = bh = {data['A']} cm^2")
        else:
            steps.append(
                f"circle: r={data['r']}cm, d={data['d']}cm"
            )
            steps.append(f"I_cm = pi*r^4/4 = {_f(data['I_cm'])} cm^4")
            steps.append(f"A = pi*r^2 = {_f(data['A'])} cm^2")
        steps.append(f"Ad^2 = {_f(data['A'])}*{data['d']**2}")
        steps.append(f"I = I_cm + Ad^2 = {_f(data['I_total'])} cm^4")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the moment of inertia.

        Args:
            data: Solution data.

        Returns:
            String with I value and units.
        """
        if data["mode"] == "simple":
            return f"I = {_f(data['I_cm'])} cm^4"
        return f"I = {_f(data['I_total'])} cm^4"


# ===================================================================
# 5. Shear force and bending moment  (tier 5)
# ===================================================================

@register
class ShearBendingGenerator(StepGenerator):
    """Shear force and bending moment for simply supported beam.

    Computes V(x) and M(x) for a simply supported beam with a single
    point load at position a from the left support. Span = L.
    Ra = P*(L-a)/L, Rb = P*a/L. Max moment at load point.

    Difficulty scaling:
        Difficulty 1-3: load at midspan, symmetric.
        Difficulty 4-6: load at arbitrary position.
        Difficulty 7-8: two point loads, find max moment.

    Prerequisites:
        multiplication.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "shear_bending"

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
        return "compute shear force and bending moment diagram values"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate beam loading and compute V, M.

        Args:
            difficulty: Controls load position and number of loads.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        length = self._rng.randint(4, 8 + difficulty)
        p_kn = self._rng.randint(10, 30 + difficulty * 5)

        if difficulty <= 3:
            a = length / 2.0
        else:
            a = round(self._rng.uniform(1.0, length - 1.0), 1)

        ra = round(p_kn * (length - a) / length, 4)
        rb = round(p_kn * a / length, 4)

        # Shear: V(0+) = Ra, V(a-) = Ra, V(a+) = Ra - P, V(L-) = -Rb
        v_left = ra
        v_right = round(ra - p_kn, 4)

        # Max moment at load point
        m_max = round(ra * a, 4)

        problem = (f"simply supported beam: L={length}m, "
                   f"P={p_kn}kN at x={_f(a)}m")

        return problem, {
            "L": length, "P_kN": p_kn, "a": a,
            "Ra": ra, "Rb": rb,
            "V_left": v_left, "V_right": v_right,
            "M_max": m_max,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate SFD/BMD computation steps.

        Args:
            data: Solution data with reactions and moments.

        Returns:
            List of step strings.
        """
        return [
            f"L={data['L']}m, P={data['P_kN']}kN at a={_f(data['a'])}m",
            f"Ra = P*(L-a)/L = {_f(data['Ra'])} kN",
            f"Rb = P*a/L = {_f(data['Rb'])} kN",
            f"V(0..a) = Ra = {_f(data['V_left'])} kN",
            f"V(a..L) = Ra-P = {_f(data['V_right'])} kN",
            f"M_max = Ra*a = {_f(data['M_max'])} kN*m",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the maximum bending moment.

        Args:
            data: Solution data.

        Returns:
            String with M_max value and units.
        """
        return f"M_max = {_f(data['M_max'])} kN*m"


# ===================================================================
# 6. Section modulus  (tier 4)
# ===================================================================

@register
class SectionModulusGenerator(StepGenerator):
    """Section modulus and maximum bending stress.

    S = I / c where c is the distance from the neutral axis to the
    extreme fibre. Maximum bending stress sigma = M / S.

    Difficulty scaling:
        Difficulty 1-3: given I and c directly, compute S and sigma.
        Difficulty 4-6: compute I from rectangle, then S and sigma.
        Difficulty 7-8: compare two sections, choose the stronger.

    Prerequisites:
        division.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "section_modulus"

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
        return "compute section modulus and bending stress"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate section properties and compute stress.

        Args:
            difficulty: Controls problem variant.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        m_knm = self._rng.randint(10, 50 + difficulty * 10)
        m_nm = m_knm * 1e6  # N*mm (using mm units)

        if difficulty <= 3:
            # Given I and c directly
            i_cm4 = self._rng.randint(500, 2000 + difficulty * 500)
            i_mm4 = i_cm4 * 1e4
            c_mm = self._rng.randint(50, 150 + difficulty * 20)
            s_mm3 = round(i_mm4 / c_mm, 4)
            sigma = round(m_nm / s_mm3, 4)

            formula = "\\sigma = \\frac{M}{S} = \\frac{M}{I/c}"
            return formula, {
                "mode": "direct",
                "M_kNm": m_knm, "M_Nmm": m_nm,
                "I_cm4": i_cm4, "I_mm4": i_mm4,
                "c_mm": c_mm, "S_mm3": s_mm3, "sigma": sigma,
            }

        # Compute I from rectangle
        b_mm = self._rng.randint(50, 150 + difficulty * 20)
        h_mm = self._rng.randint(100, 300 + difficulty * 30)
        i_mm4 = round(b_mm * h_mm ** 3 / 12.0, 4)
        c_mm = h_mm / 2.0
        s_mm3 = round(i_mm4 / c_mm, 4)
        sigma = round(m_nm / s_mm3, 4)

        formula = ("S = \\frac{I}{c} = \\frac{bh^3/12}{h/2} = "
                   "\\frac{bh^2}{6}")
        return formula, {
            "mode": "rectangle",
            "M_kNm": m_knm, "M_Nmm": m_nm,
            "b_mm": b_mm, "h_mm": h_mm,
            "I_mm4": i_mm4, "c_mm": c_mm,
            "S_mm3": s_mm3, "sigma": sigma,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate section modulus computation steps.

        Args:
            data: Solution data with section properties.

        Returns:
            List of step strings.
        """
        if data["mode"] == "direct":
            return [
                f"M={data['M_kNm']}kN*m, "
                f"I={data['I_cm4']}cm^4, c={data['c_mm']}mm",
                f"S = I/c = {_f(data['I_mm4'])}/{data['c_mm']}",
                f"S = {_f(data['S_mm3'])} mm^3",
                f"sigma = M/S = {_f(data['sigma'])} MPa",
            ]
        return [
            f"M={data['M_kNm']}kN*m, "
            f"b={data['b_mm']}mm, h={data['h_mm']}mm",
            f"I = bh^3/12 = {_f(data['I_mm4'])} mm^4",
            f"c = h/2 = {_f(data['c_mm'])} mm",
            f"S = I/c = {_f(data['S_mm3'])} mm^3",
            f"sigma = M/S = {_f(data['sigma'])} MPa",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the section modulus and stress.

        Args:
            data: Solution data.

        Returns:
            String with S and sigma values.
        """
        return (f"S = {_f(data['S_mm3'])} mm^3, "
                f"sigma = {_f(data['sigma'])} MPa")
