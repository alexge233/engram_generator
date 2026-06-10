"""Solid state physics generators -- Bragg diffraction through Debye model.

Covers Bragg diffraction, Miller indices, reciprocal lattice vectors,
band gap classification, Fermi level computation, phonon dispersion,
Hall effect, and Debye model heat capacity.  All tiers are 4-6
(intermediate to advanced).
"""
import math
from fractions import Fraction

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


def _gcd(a: int, b: int) -> int:
    """Compute greatest common divisor of two positive integers.

    Args:
        a: First integer.
        b: Second integer.

    Returns:
        GCD of a and b.
    """
    while b:
        a, b = b, a % b
    return a


# Physical constants
_K_B = 8.617e-5   # Boltzmann constant in eV/K
_Q = 1.602e-19     # electron charge in C
_PI = math.pi


# ===================================================================
# 1. Bragg diffraction  (tier 5)
# ===================================================================

@register
class BraggDiffractionGenerator(StepGenerator):
    """Compute diffraction angle from Bragg's law.

    2*d*sin(theta) = n*lambda.  Given d-spacing and wavelength,
    compute the diffraction angle theta for order n.

    Difficulty scaling:
        Difficulty 1-3: first order (n=1), simple d-spacing.
        Difficulty 4-6: higher orders (n=1-3).
        Difficulty 7-8: compute d from crystal parameters.

    Prerequisites:
        sin_cos_eval.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "bragg_diffraction"

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
        return "compute Bragg diffraction angle"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Bragg diffraction problem.

        Args:
            difficulty: Controls order and complexity.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        # d-spacing in Angstroms, wavelength in Angstroms
        d = round(self._rng.uniform(1.0, 5.0), 4)
        wavelength = round(self._rng.uniform(0.5, 2.0), 4)

        if difficulty <= 3:
            n = 1
        elif difficulty <= 6:
            n = self._rng.randint(1, 3)
        else:
            n = self._rng.randint(1, 4)

        sin_theta = round(n * wavelength / (2 * d), 4)
        if sin_theta > 1.0:
            # Ensure valid angle by adjusting
            n = 1
            sin_theta = round(wavelength / (2 * d), 4)
            if sin_theta > 1.0:
                wavelength = round(d * 0.8, 4)
                sin_theta = round(wavelength / (2 * d), 4)

        theta_rad = round(math.asin(sin_theta), 4)
        theta_deg = round(math.degrees(theta_rad), 4)

        return "2d \\sin\\theta = n\\lambda", {
            "d": d, "wavelength": wavelength, "n": n,
            "sin_theta": sin_theta,
            "theta_rad": theta_rad, "theta_deg": theta_deg,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Bragg diffraction computation steps.

        Args:
            data: Solution data with d, wavelength, theta.

        Returns:
            List of step strings.
        """
        return [
            f"d = {_fmt(data['d'])} A, lambda = {_fmt(data['wavelength'])} A, "
            f"n = {data['n']}",
            f"sin(theta) = n*lambda/(2*d) = "
            f"{data['n']}*{_fmt(data['wavelength'])}/(2*{_fmt(data['d'])})"
            f" = {_fmt(data['sin_theta'])}",
            f"theta = arcsin({_fmt(data['sin_theta'])})"
            f" = {_fmt(data['theta_rad'])} rad",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the diffraction angle.

        Args:
            data: Solution data.

        Returns:
            String with theta in degrees.
        """
        return f"theta = {_fmt(data['theta_deg'])} deg"


# ===================================================================
# 2. Miller indices  (tier 4)
# ===================================================================

@register
class MillerIndicesGenerator(StepGenerator):
    """Convert crystal plane intercepts to Miller indices.

    Take reciprocals of fractional intercepts (a/h, b/k, c/l),
    then clear fractions using GCD to get integer (hkl).

    Difficulty scaling:
        Difficulty 1-3: simple intercepts (1, 2, 3).
        Difficulty 4-6: one intercept at infinity (parallel plane).
        Difficulty 7-8: fractional intercepts requiring clearing.

    Prerequisites:
        gcd.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "miller_indices"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["gcd"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "convert intercepts to Miller indices"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Miller indices conversion problem.

        Args:
            difficulty: Controls intercept complexity.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            intercepts = [
                self._rng.randint(1, 4),
                self._rng.randint(1, 4),
                self._rng.randint(1, 4),
            ]
            reciprocals = [1.0 / i for i in intercepts]
        elif difficulty <= 6:
            # One intercept at infinity
            idx = self._rng.randint(0, 2)
            intercepts_raw = [self._rng.randint(1, 4) for _ in range(3)]
            intercepts = list(intercepts_raw)
            intercepts[idx] = float("inf")
            reciprocals = [0.0 if i == float("inf") else 1.0 / i for i in intercepts]
        else:
            # Fractional intercepts
            intercepts = [
                self._rng.randint(1, 3) + 0.5 * self._rng.randint(0, 1)
                for _ in range(3)
            ]
            if all(i == 0 for i in intercepts):
                intercepts[0] = 1.0
            reciprocals = [1.0 / i if i != 0 else 0.0 for i in intercepts]

        # Clear fractions: multiply by LCM of denominators
        fracs = []
        for r in reciprocals:
            fracs.append(Fraction(r).limit_denominator(100))

        if all(f == 0 for f in fracs):
            fracs[0] = Fraction(1)

        # Find LCM of denominators
        lcm_denom = 1
        for f in fracs:
            d = f.denominator
            lcm_denom = lcm_denom * d // _gcd(lcm_denom, d)

        miller_raw = [int(f * lcm_denom) for f in fracs]

        # Reduce by GCD
        g = abs(miller_raw[0]) if miller_raw[0] != 0 else 1
        for m in miller_raw[1:]:
            if m != 0:
                g = _gcd(g, abs(m))
        if g > 0:
            miller = [m // g for m in miller_raw]
        else:
            miller = miller_raw

        intercept_strs = [
            "inf" if i == float("inf") else _fmt(i) for i in intercepts
        ]

        return "(hkl) \\text{ from intercepts}", {
            "intercepts": intercept_strs,
            "reciprocals": [_fmt(r) for r in reciprocals],
            "miller": miller,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Miller indices computation steps.

        Args:
            data: Solution data with intercepts and indices.

        Returns:
            List of step strings.
        """
        return [
            f"intercepts: ({', '.join(data['intercepts'])})",
            f"reciprocals: ({', '.join(data['reciprocals'])})",
            f"clear fractions and reduce",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the Miller indices.

        Args:
            data: Solution data.

        Returns:
            String with (hkl) notation.
        """
        h, k, l = data["miller"]
        return f"({h} {k} {l})"


# ===================================================================
# 3. Reciprocal lattice  (tier 6)
# ===================================================================

@register
class ReciprocalLatticeGenerator(StepGenerator):
    """Compute reciprocal lattice vectors for cubic lattice.

    b_i = 2*pi*(a_j x a_k) / (a_i . (a_j x a_k)).
    For simple cubic with lattice constant a: b = (2*pi/a) along each axis.

    Difficulty scaling:
        Difficulty 1-3: simple cubic lattice.
        Difficulty 4-6: BCC lattice.
        Difficulty 7-8: FCC lattice.

    Prerequisites:
        cross_product.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "reciprocal_lattice"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

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
        return "compute reciprocal lattice vectors"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a reciprocal lattice problem.

        Args:
            difficulty: Controls lattice type.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        a_const = round(self._rng.uniform(2.0, 6.0), 4)

        if difficulty <= 3:
            # Simple cubic
            lattice = "simple cubic"
            a1 = [a_const, 0, 0]
            a2 = [0, a_const, 0]
            a3 = [0, 0, a_const]
            vol = a_const ** 3
            b1 = [round(2 * _PI / a_const, 4), 0, 0]
            b2 = [0, round(2 * _PI / a_const, 4), 0]
            b3 = [0, 0, round(2 * _PI / a_const, 4)]
        elif difficulty <= 6:
            # BCC: a1=(a,0,0), a2=(0,a,0), a3=(a/2,a/2,a/2)
            lattice = "BCC"
            h = round(a_const / 2, 4)
            a1 = [a_const, 0, 0]
            a2 = [0, a_const, 0]
            a3 = [h, h, h]
            vol = round(a_const * a_const * h, 4)
            b_mag = round(2 * _PI / a_const, 4)
            b1 = [b_mag, 0, round(-b_mag, 4)]
            b2 = [0, b_mag, round(-b_mag, 4)]
            b3 = [0, 0, round(2 * 2 * _PI / a_const, 4)]
        else:
            # FCC: a1=(0,a/2,a/2), a2=(a/2,0,a/2), a3=(a/2,a/2,0)
            lattice = "FCC"
            h = round(a_const / 2, 4)
            a1 = [0, h, h]
            a2 = [h, 0, h]
            a3 = [h, h, 0]
            vol = round(a_const ** 3 / 4, 4)
            b_mag = round(2 * _PI / a_const, 4)
            b1 = [round(-b_mag, 4), b_mag, b_mag]
            b2 = [b_mag, round(-b_mag, 4), b_mag]
            b3 = [b_mag, b_mag, round(-b_mag, 4)]

        def vec_str(v):
            return f"({_fmt(v[0])}, {_fmt(v[1])}, {_fmt(v[2])})"

        return "b_i = \\frac{2\\pi (a_j \\times a_k)}{a_i \\cdot (a_j \\times a_k)}", {
            "lattice": lattice, "a": a_const,
            "a1": a1, "a2": a2, "a3": a3,
            "vol": round(vol, 4),
            "b1": b1, "b2": b2, "b3": b3,
            "b1_str": vec_str(b1),
            "b2_str": vec_str(b2),
            "b3_str": vec_str(b3),
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate reciprocal lattice computation steps.

        Args:
            data: Solution data with lattice vectors.

        Returns:
            List of step strings.
        """
        return [
            f"{data['lattice']}, a = {_fmt(data['a'])} A",
            f"V = a_1 . (a_2 x a_3) = {_fmt(data['vol'])} A^3",
            f"b_1 = {data['b1_str']}",
            f"b_2 = {data['b2_str']}",
            f"b_3 = {data['b3_str']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the reciprocal lattice vectors.

        Args:
            data: Solution data.

        Returns:
            String with b vectors.
        """
        return (
            f"b1={data['b1_str']}, b2={data['b2_str']}, "
            f"b3={data['b3_str']}"
        )


# ===================================================================
# 4. Band gap  (tier 5)
# ===================================================================

@register
class BandGapGenerator(StepGenerator):
    """Classify material by band gap.

    Conductor: E_g < 0.1 eV.  Semiconductor: 0.1 <= E_g <= 4 eV.
    Insulator: E_g > 4 eV.  May include temperature dependence
    at higher difficulty.

    Difficulty scaling:
        Difficulty 1-3: classify from given E_g value.
        Difficulty 4-6: given E_g and T, check if thermal excitation matters.
        Difficulty 7-8: compare two materials, determine which conducts.

    Prerequisites:
        comparison.
    """

    _MATERIALS = [
        ("silicon", 1.12),
        ("germanium", 0.67),
        ("diamond", 5.47),
        ("GaAs", 1.43),
        ("InSb", 0.17),
        ("copper", 0.0),
        ("SiO2", 9.0),
        ("GaN", 3.4),
        ("SiC", 3.26),
        ("tin (alpha)", 0.08),
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "band_gap"

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
        return "classify material by band gap"

    @staticmethod
    def _classify(e_g: float) -> str:
        """Classify material based on band gap energy.

        Args:
            e_g: Band gap energy in eV.

        Returns:
            Classification string.
        """
        if e_g < 0.1:
            return "conductor"
        if e_g <= 4.0:
            return "semiconductor"
        return "insulator"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a band gap classification problem.

        Args:
            difficulty: Controls problem complexity.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            name, e_g = self._rng.choice(self._MATERIALS)
            classification = self._classify(e_g)
            return f"E_g({name}) = {e_g} \\text{{ eV}}", {
                "name": name, "E_g": e_g,
                "classification": classification,
                "mode": "single",
            }

        if difficulty <= 6:
            name, e_g = self._rng.choice(self._MATERIALS)
            temp = self._rng.randint(200, 500)
            kt = round(_K_B * temp, 4)
            ratio = round(e_g / kt, 4) if kt > 0 else float("inf")
            thermal = "significant" if ratio < 20 else "negligible"
            classification = self._classify(e_g)
            return f"E_g = {e_g} \\text{{ eV}}, T = {temp} \\text{{ K}}", {
                "name": name, "E_g": e_g, "T": temp, "kT": kt,
                "ratio": ratio, "thermal": thermal,
                "classification": classification,
                "mode": "thermal",
            }

        # Compare two materials
        mat1 = self._rng.choice(self._MATERIALS)
        mat2 = self._rng.choice(self._MATERIALS)
        while mat1[0] == mat2[0]:
            mat2 = self._rng.choice(self._MATERIALS)
        cls1 = self._classify(mat1[1])
        cls2 = self._classify(mat2[1])
        better = mat1[0] if mat1[1] < mat2[1] else mat2[0]

        return f"E_g({mat1[0]})={mat1[1]}, E_g({mat2[0]})={mat2[1]}", {
            "mat1": mat1[0], "E_g1": mat1[1], "cls1": cls1,
            "mat2": mat2[0], "E_g2": mat2[1], "cls2": cls2,
            "better_conductor": better,
            "mode": "compare",
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate band gap classification steps.

        Args:
            data: Solution data with band gap and classification.

        Returns:
            List of step strings.
        """
        mode = data["mode"]
        if mode == "single":
            return [
                f"E_g = {_fmt(data['E_g'])} eV",
                f"0.1 <= E_g <= 4 -> semiconductor; >4 -> insulator; <0.1 -> conductor",
                f"{data['name']}: {data['classification']}",
            ]
        if mode == "thermal":
            return [
                f"E_g = {_fmt(data['E_g'])} eV, T = {data['T']} K",
                f"kT = {_fmt(data['kT'])} eV",
                f"E_g/kT = {_fmt(data['ratio'])}",
                f"thermal excitation: {data['thermal']}",
            ]
        # compare
        return [
            f"{data['mat1']}: E_g={_fmt(data['E_g1'])} eV -> {data['cls1']}",
            f"{data['mat2']}: E_g={_fmt(data['E_g2'])} eV -> {data['cls2']}",
            f"better conductor: {data['better_conductor']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the classification result.

        Args:
            data: Solution data.

        Returns:
            String with classification.
        """
        mode = data["mode"]
        if mode == "single":
            return f"{data['name']}: {data['classification']}"
        if mode == "thermal":
            return (
                f"{data['name']}: {data['classification']}, "
                f"thermal: {data['thermal']}"
            )
        return f"better conductor: {data['better_conductor']}"


# ===================================================================
# 5. Fermi level  (tier 6)
# ===================================================================

@register
class FermiLevelGenerator(StepGenerator):
    """Compute Fermi level for intrinsic semiconductor.

    E_F = (E_C + E_V)/2 + (kT/2)*ln(m_h*/m_e*).  For equal
    effective masses, E_F is at midgap.

    Difficulty scaling:
        Difficulty 1-3: equal effective masses (E_F at midgap).
        Difficulty 4-6: m_h*/m_e* between 1.0 and 3.0.
        Difficulty 7-8: temperature dependence, compute shift from midgap.

    Prerequisites:
        logarithm, division.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "fermi_level"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["logarithm", "division"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute Fermi level for intrinsic semiconductor"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Fermi level computation.

        Args:
            difficulty: Controls effective mass ratio.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        e_v = 0.0
        e_c = round(self._rng.uniform(0.5, 3.0), 4)
        temp = self._rng.randint(200, 500)
        kt = round(_K_B * temp, 4)

        if difficulty <= 3:
            mass_ratio = 1.0
        elif difficulty <= 6:
            mass_ratio = round(self._rng.uniform(1.0, 3.0), 4)
        else:
            mass_ratio = round(self._rng.uniform(0.3, 5.0), 4)

        midgap = round((e_c + e_v) / 2, 4)
        ln_ratio = round(math.log(mass_ratio), 4)
        shift = round(0.5 * kt * ln_ratio, 4)
        e_f = round(midgap + shift, 4)

        return "E_F = \\frac{E_C + E_V}{2} + \\frac{kT}{2} \\ln\\frac{m_h^*}{m_e^*}", {
            "E_V": e_v, "E_C": e_c, "T": temp, "kT": kt,
            "mass_ratio": mass_ratio, "midgap": midgap,
            "ln_ratio": ln_ratio, "shift": shift, "E_F": e_f,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Fermi level computation steps.

        Args:
            data: Solution data with band edges and temperature.

        Returns:
            List of step strings.
        """
        return [
            f"E_V={_fmt(data['E_V'])}, E_C={_fmt(data['E_C'])} eV, "
            f"T={data['T']} K",
            f"midgap = ({_fmt(data['E_C'])} + {_fmt(data['E_V'])})/2"
            f" = {_fmt(data['midgap'])} eV",
            f"kT = {_fmt(data['kT'])} eV",
            f"m_h*/m_e* = {_fmt(data['mass_ratio'])}, "
            f"ln = {_fmt(data['ln_ratio'])}",
            f"shift = 0.5*{_fmt(data['kT'])}*{_fmt(data['ln_ratio'])}"
            f" = {_fmt(data['shift'])} eV",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the Fermi level.

        Args:
            data: Solution data.

        Returns:
            String with E_F value.
        """
        return f"E_F = {_fmt(data['E_F'])} eV"


# ===================================================================
# 6. Phonon dispersion  (tier 6)
# ===================================================================

@register
class PhononDispersionGenerator(StepGenerator):
    """Compute phonon frequency for 1D monatomic chain.

    omega(k) = 2*sqrt(C/m)*|sin(k*a/2)| where C is spring constant,
    m is atom mass, a is lattice constant, k is wavevector.

    Difficulty scaling:
        Difficulty 1-3: k at zone boundary (k = pi/a).
        Difficulty 4-6: arbitrary k in first Brillouin zone.
        Difficulty 7-8: compute group velocity d(omega)/dk.

    Prerequisites:
        sin_cos_eval.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "phonon_dispersion"

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
        return "compute phonon frequency in 1D chain"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a phonon dispersion problem.

        Args:
            difficulty: Controls k-point selection.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        spring_c = round(self._rng.uniform(1.0, 50.0), 4)
        mass = round(self._rng.uniform(1.0, 10.0), 4)
        a_const = round(self._rng.uniform(2.0, 6.0), 4)

        omega_max = round(2 * math.sqrt(spring_c / mass), 4)

        if difficulty <= 3:
            k = round(_PI / a_const, 4)
        elif difficulty <= 6:
            frac = round(self._rng.uniform(0.1, 0.9), 4)
            k = round(frac * _PI / a_const, 4)
        else:
            frac = round(self._rng.uniform(0.1, 0.9), 4)
            k = round(frac * _PI / a_const, 4)

        sin_val = round(abs(math.sin(k * a_const / 2)), 4)
        omega = round(omega_max * sin_val, 4)

        data = {
            "C": spring_c, "m": mass, "a": a_const,
            "k": k, "omega_max": omega_max,
            "sin_val": sin_val, "omega": omega,
        }

        if difficulty >= 7:
            # Group velocity: v_g = d(omega)/dk = omega_max * a/2 * |cos(ka/2)|
            cos_val = round(abs(math.cos(k * a_const / 2)), 4)
            v_g = round(omega_max * a_const / 2 * cos_val, 4)
            data["cos_val"] = cos_val
            data["v_g"] = v_g

        return "\\omega(k) = 2\\sqrt{C/m} |\\sin(ka/2)|", data

    def _create_steps(self, data: dict) -> list[str]:
        """Generate phonon dispersion computation steps.

        Args:
            data: Solution data with spring constant, mass, and k.

        Returns:
            List of step strings.
        """
        steps = [
            f"C={_fmt(data['C'])}, m={_fmt(data['m'])}, a={_fmt(data['a'])} A",
            f"omega_max = 2*sqrt({_fmt(data['C'])}/{_fmt(data['m'])})"
            f" = {_fmt(data['omega_max'])}",
            f"k = {_fmt(data['k'])}, sin(ka/2) = {_fmt(data['sin_val'])}",
            f"omega = {_fmt(data['omega_max'])}*{_fmt(data['sin_val'])}",
        ]
        if "v_g" in data:
            steps.append(
                f"v_g = {_fmt(data['omega_max'])}*{_fmt(data['a'])}/2"
                f"*{_fmt(data['cos_val'])} = {_fmt(data['v_g'])}"
            )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the phonon frequency.

        Args:
            data: Solution data.

        Returns:
            String with omega value.
        """
        ans = f"omega = {_fmt(data['omega'])} rad/s"
        if "v_g" in data:
            ans += f", v_g = {_fmt(data['v_g'])} A/s"
        return ans


# ===================================================================
# 7. Hall effect  (tier 5)
# ===================================================================

@register
class HallEffectGenerator(StepGenerator):
    """Compute Hall coefficient and carrier density.

    R_H = 1/(n*q).  Hall voltage V_H = I*B/(n*q*t) where t is
    sample thickness.  Determine carrier type from sign.

    Difficulty scaling:
        Difficulty 1-3: compute R_H from given n.
        Difficulty 4-6: compute n from V_H, I, B, t.
        Difficulty 7-8: determine carrier type and mobility.

    Prerequisites:
        division.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "hall_effect"

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
        return "compute Hall effect parameters"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Hall effect problem.

        Args:
            difficulty: Controls problem variant.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        # Carrier density in m^-3
        exp = self._rng.randint(20, 28)
        mantissa = self._rng.randint(1, 9)
        n = float(mantissa) * (10 ** exp)
        carrier = self._rng.choice(["electron", "hole"])
        sign = -1 if carrier == "electron" else 1

        r_h = round(sign / (n * _Q), 4)

        if difficulty <= 3:
            return "R_H = \\frac{1}{nq}", {
                "n": n, "carrier": carrier, "R_H": r_h,
                "mode": "R_H",
            }

        # Hall voltage measurement
        current = round(self._rng.uniform(0.001, 0.1), 4)
        b_field = round(self._rng.uniform(0.1, 2.0), 4)
        thickness = round(self._rng.uniform(0.001, 0.01), 4)
        v_h = round(current * b_field / (n * _Q * thickness), 4)
        v_h_signed = round(sign * abs(v_h), 4)

        if difficulty <= 6:
            return "V_H = \\frac{IB}{nqt}", {
                "n": n, "carrier": carrier, "R_H": r_h,
                "I": current, "B": b_field, "t": thickness,
                "V_H": v_h_signed,
                "mode": "V_H",
            }

        # With mobility
        conductivity = round(self._rng.uniform(1.0, 1000.0), 4)
        mobility = round(abs(r_h) * conductivity, 4)

        return "\\mu = |R_H| \\sigma", {
            "n": n, "carrier": carrier, "R_H": r_h,
            "I": current, "B": b_field, "t": thickness,
            "V_H": v_h_signed,
            "sigma": conductivity, "mobility": mobility,
            "mode": "mobility",
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Hall effect computation steps.

        Args:
            data: Solution data with carrier density and Hall parameters.

        Returns:
            List of step strings.
        """
        mode = data["mode"]
        if mode == "R_H":
            return [
                f"n = {data['n']:.2e} m^-3, carrier: {data['carrier']}",
                f"R_H = 1/(n*q) = 1/({data['n']:.2e}*{_Q})",
                f"R_H = {_fmt(data['R_H'])} m^3/C",
            ]
        steps = [
            f"I={_fmt(data['I'])} A, B={_fmt(data['B'])} T, "
            f"t={_fmt(data['t'])} m",
            f"V_H = I*B/(n*q*t) = {_fmt(data['V_H'])} V",
            f"carrier: {data['carrier']}",
        ]
        if mode == "mobility":
            steps.append(
                f"mu = |R_H|*sigma = {_fmt(abs(data['R_H']))}*"
                f"{_fmt(data['sigma'])} = {_fmt(data['mobility'])} m^2/Vs"
            )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the Hall effect result.

        Args:
            data: Solution data.

        Returns:
            String with Hall coefficient or carrier properties.
        """
        mode = data["mode"]
        if mode == "R_H":
            return f"R_H = {_fmt(data['R_H'])} m^3/C ({data['carrier']})"
        if mode == "V_H":
            return f"V_H = {_fmt(data['V_H'])} V ({data['carrier']})"
        return (
            f"V_H = {_fmt(data['V_H'])} V, "
            f"mu = {_fmt(data['mobility'])} m^2/Vs"
        )


# ===================================================================
# 8. Debye model  (tier 6)
# ===================================================================

@register
class DebyeModelGenerator(StepGenerator):
    """Classify heat capacity regime using Debye model.

    At high T (T >> Theta_D): C_V -> 3*N*k_B (Dulong-Petit).
    At low T (T << Theta_D): C_V ~ (12/5)*pi^4*N*k_B*(T/Theta_D)^3.
    Classify the regime and compute the appropriate limit.

    Difficulty scaling:
        Difficulty 1-3: high-T limit, just verify Dulong-Petit.
        Difficulty 4-6: low-T limit, compute T^3 scaling.
        Difficulty 7-8: intermediate T, identify which limit applies.

    Prerequisites:
        comparison.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "debye_model"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

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
        return "classify heat capacity regime using Debye model"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Debye model heat capacity problem.

        Args:
            difficulty: Controls temperature regime.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        theta_d = self._rng.randint(100, 500)
        n_atoms = self._rng.randint(1, 10)

        if difficulty <= 3:
            # High T: T >> Theta_D
            temp = self._rng.randint(theta_d * 2, theta_d * 5)
            regime = "high-T (Dulong-Petit)"
            # C_V = 3Nk_B in eV/K
            c_v = round(3 * n_atoms * _K_B, 4)
            t_ratio = round(temp / theta_d, 4)
            return "C_V = 3Nk_B \\text{ (high T)}", {
                "Theta_D": theta_d, "T": temp, "N": n_atoms,
                "regime": regime, "C_V": c_v,
                "T_ratio": t_ratio,
            }

        if difficulty <= 6:
            # Low T: T << Theta_D
            temp = self._rng.randint(5, max(6, theta_d // 10))
            regime = "low-T (T^3 law)"
            t_ratio = round(temp / theta_d, 4)
            prefactor = round(12 * _PI ** 4 / 5, 4)
            c_v = round(prefactor * n_atoms * _K_B * t_ratio ** 3, 4)
            return "C_V \\sim \\frac{12\\pi^4}{5} Nk_B (T/\\Theta_D)^3", {
                "Theta_D": theta_d, "T": temp, "N": n_atoms,
                "regime": regime, "C_V": c_v,
                "T_ratio": t_ratio, "prefactor": prefactor,
            }

        # Intermediate: determine which limit
        temp = self._rng.randint(theta_d // 5, theta_d * 2)
        t_ratio = round(temp / theta_d, 4)
        if t_ratio > 1.5:
            regime = "high-T (Dulong-Petit)"
            c_v = round(3 * n_atoms * _K_B, 4)
        elif t_ratio < 0.3:
            regime = "low-T (T^3 law)"
            prefactor = round(12 * _PI ** 4 / 5, 4)
            c_v = round(prefactor * n_atoms * _K_B * t_ratio ** 3, 4)
        else:
            regime = "intermediate (full integral needed)"
            c_v_high = round(3 * n_atoms * _K_B, 4)
            c_v = round(c_v_high * 0.7, 4)

        return "C_V(T) \\text{ Debye model}", {
            "Theta_D": theta_d, "T": temp, "N": n_atoms,
            "regime": regime, "C_V": c_v,
            "T_ratio": t_ratio,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Debye model classification steps.

        Args:
            data: Solution data with temperature and regime.

        Returns:
            List of step strings.
        """
        return [
            f"Theta_D = {data['Theta_D']} K, T = {data['T']} K, "
            f"N = {data['N']}",
            f"T/Theta_D = {_fmt(data['T_ratio'])}",
            f"regime: {data['regime']}",
            f"C_V = {_fmt(data['C_V'])} eV/K",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the heat capacity and regime.

        Args:
            data: Solution data.

        Returns:
            String with C_V and regime classification.
        """
        return f"C_V = {_fmt(data['C_V'])} eV/K ({data['regime']})"
