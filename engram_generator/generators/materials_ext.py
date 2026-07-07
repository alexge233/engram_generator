"""Extended materials science generators -- hardness through grain size.

Covers Brinell hardness testing, fatigue S-N curves, creep rate via
Arrhenius, fracture toughness, corrosion rate, composite rule of
mixtures, heat treatment classification, and Hall-Petch grain size
strengthening.  Tiers range from 4 to 5 (intermediate materials
engineering).
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


_PI = math.pi
_R_GAS = 8.314  # universal gas constant (J/(mol*K))


# ===================================================================
# 1. Hardness test (Brinell)  (tier 4)
# ===================================================================

@register
class HardnessTestGenerator(StepGenerator):
    """Compute Brinell hardness number from indentation test.

    BHN = 2*F / (pi*D*(D - sqrt(D^2 - d^2))).
    Given applied force F (N), ball diameter D (mm), and indentation
    diameter d (mm), compute BHN.

    Difficulty scaling:
        Difficulty 1-3: simple integer values, small d.
        Difficulty 4-6: decimal values, varied ball sizes.
        Difficulty 7-8: solve for F given BHN, D, d.

    Prerequisites:
        division.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "hardness_test"

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
        return "compute Brinell hardness number from indentation"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Brinell hardness problem.

        Args:
            difficulty: Controls parameter precision and variant.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        big_d = self._rng.choice([5.0, 10.0])
        max_d = big_d * 0.9

        if difficulty <= 3:
            force = float(self._rng.randint(500, 3000))
            small_d = round(self._rng.uniform(1.0, max_d * 0.6), 1)
        else:
            force = round(self._rng.uniform(500, 30000), 4)
            small_d = round(self._rng.uniform(1.0, max_d * 0.8), 4)

        inner = round(big_d ** 2 - small_d ** 2, 4)
        sqrt_inner = round(math.sqrt(inner), 4)
        denom = round(_PI * big_d * (big_d - sqrt_inner), 4)
        bhn = round(2 * force / denom, 4)

        target = "BHN" if difficulty < 7 else "F"

        return "BHN = \\frac{2F}{\\pi D (D - \\sqrt{D^2 - d^2})}", {
            "F": force, "D": big_d, "d": small_d,
            "inner": inner, "sqrt_inner": sqrt_inner,
            "denom": denom, "BHN": bhn, "target": target,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Brinell hardness computation steps.

        Args:
            data: Solution data with force, diameters, and BHN.

        Returns:
            List of step strings.
        """
        steps = [
            f"F = {_fmt(data['F'])} N, D = {_fmt(data['D'])} mm, "
            f"d = {_fmt(data['d'])} mm",
            f"D^2 - d^2 = {_fmt(data['inner'])}",
            f"sqrt({_fmt(data['inner'])}) = {_fmt(data['sqrt_inner'])}",
            f"denom = pi*{_fmt(data['D'])}*({_fmt(data['D'])}-{_fmt(data['sqrt_inner'])})"
            f" = {_fmt(data['denom'])}",
        ]
        if data["target"] == "BHN":
            steps.append(f"BHN = 2*{_fmt(data['F'])}/{_fmt(data['denom'])} = {_fmt(data['BHN'])}")
        else:
            steps.append(f"F = BHN*denom/2 = {_fmt(data['F'])} N")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the Brinell hardness or force.

        Args:
            data: Solution data.

        Returns:
            String with BHN or F.
        """
        if data["target"] == "BHN":
            return f"BHN = {_fmt(data['BHN'])}"
        return f"F = {_fmt(data['F'])} N"


# ===================================================================
# 2. Fatigue S-N curve  (tier 5)
# ===================================================================

@register
class FatigueSNCurveGenerator(StepGenerator):
    """Fit S-N fatigue curve and predict life.

    S-N relation: S = a * N^b (log-log linear).
    Given two (S, N) data points, find a and b, then predict N
    at a new stress level S.

    Difficulty scaling:
        Difficulty 1-3: two points with large N separation.
        Difficulty 4-6: predict N at intermediate stress.
        Difficulty 7-8: predict endurance limit (N -> 10^7).

    Prerequisites:
        logarithm.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "fatigue_sn_curve"

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
        return "fit S-N curve and predict fatigue life"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a fatigue S-N curve problem.

        Args:
            difficulty: Controls data complexity and prediction target.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        # Two data points (S in MPa, N in cycles)
        s1 = round(self._rng.uniform(200, 600), 4)
        n1 = self._rng.randint(1000, 10000)
        s2 = round(self._rng.uniform(100, s1 - 30), 4)
        n2 = self._rng.randint(100000, 1000000)

        log_s1 = round(math.log10(s1), 4)
        log_s2 = round(math.log10(s2), 4)
        log_n1 = round(math.log10(n1), 4)
        log_n2 = round(math.log10(n2), 4)

        b = round((log_s1 - log_s2) / (log_n1 - log_n2), 4)
        log_a = round(log_s1 - b * log_n1, 4)
        a = round(10 ** log_a, 4)

        # Prediction
        s_pred = round(self._rng.uniform(s2, s1), 4)
        log_s_pred = round(math.log10(s_pred), 4)
        log_n_pred = round((log_s_pred - log_a) / b, 4)
        n_pred = round(10 ** log_n_pred, 4)

        return "S = a \\cdot N^b", {
            "S1": s1, "N1": n1, "S2": s2, "N2": n2,
            "b": b, "log_a": log_a, "a": a,
            "S_pred": s_pred, "N_pred": n_pred,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate S-N curve fitting steps.

        Args:
            data: Solution data with data points and fit parameters.

        Returns:
            List of step strings.
        """
        return [
            f"point 1: S={_fmt(data['S1'])} MPa, N={data['N1']}",
            f"point 2: S={_fmt(data['S2'])} MPa, N={data['N2']}",
            f"b = (log(S1)-log(S2))/(log(N1)-log(N2)) = {_fmt(data['b'])}",
            f"a = {_fmt(data['a'])}",
            f"predict N at S={_fmt(data['S_pred'])} MPa",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the predicted fatigue life.

        Args:
            data: Solution data.

        Returns:
            String with N prediction.
        """
        return f"N = {data['N_pred']:.4e} cycles at S = {_fmt(data['S_pred'])} MPa"


# ===================================================================
# 3. Creep rate  (tier 5)
# ===================================================================

@register
class CreepRateGenerator(StepGenerator):
    """Compute steady-state creep rate via Arrhenius equation.

    epsilon_dot = A * sigma^n * exp(-Q/(R*T)).
    Given pre-exponential factor A, stress sigma, stress exponent n,
    activation energy Q, and temperature T, compute strain rate.

    Difficulty scaling:
        Difficulty 1-3: simple exponent (n=1), moderate T.
        Difficulty 4-6: n=3-5, varied T.
        Difficulty 7-8: compare creep rates at two temperatures.

    Prerequisites:
        exponentiation.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "creep_rate"

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
        return "compute steady-state creep rate"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a creep rate problem.

        Args:
            difficulty: Controls stress exponent and comparison.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        a_pre = round(self._rng.uniform(1e-5, 1e-2), 4)
        sigma = round(self._rng.uniform(50, 300), 4)
        q_kj = round(self._rng.uniform(100, 400), 4)
        q_j = q_kj * 1e3

        if difficulty <= 3:
            n_exp = 1
            temp = self._rng.randint(500, 800)
        elif difficulty <= 6:
            n_exp = self._rng.randint(3, 5)
            temp = self._rng.randint(600, 1200)
        else:
            n_exp = self._rng.randint(3, 7)
            temp = self._rng.randint(600, 1200)

        exponent = round(-q_j / (_R_GAS * temp), 4)
        sigma_term = round(sigma ** n_exp, 4)
        eps_dot = round(a_pre * sigma_term * math.exp(exponent), 4)

        data = {
            "A": a_pre, "sigma": sigma, "n": n_exp,
            "Q_kJ": q_kj, "T": temp,
            "exponent": exponent, "eps_dot": eps_dot,
        }

        if difficulty >= 7:
            t2 = self._rng.randint(600, 1200)
            exp2 = round(-q_j / (_R_GAS * t2), 4)
            eps2 = round(a_pre * sigma_term * math.exp(exp2), 4)
            ratio = round(eps2 / eps_dot, 4) if eps_dot != 0 else 0.0
            data["T2"] = t2
            data["eps_dot2"] = eps2
            data["ratio"] = ratio

        return "\\dot{\\varepsilon} = A \\sigma^n \\exp(-Q/RT)", data

    def _create_steps(self, data: dict) -> list[str]:
        """Generate creep rate computation steps.

        Args:
            data: Solution data with parameters and strain rate.

        Returns:
            List of step strings.
        """
        steps = [
            f"A = {data['A']:.4e}, sigma = {_fmt(data['sigma'])} MPa, n = {data['n']}",
            f"Q = {_fmt(data['Q_kJ'])} kJ/mol, T = {data['T']} K",
            f"exp(-Q/RT) = exp({_fmt(data['exponent'])})",
            f"eps_dot = {data['eps_dot']:.4e} s^-1",
        ]
        if "T2" in data:
            steps.append(
                f"T2={data['T2']}K: eps_dot2 = {data['eps_dot2']:.4e} s^-1"
            )
            steps.append(f"ratio = {_fmt(data['ratio'])}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the creep rate.

        Args:
            data: Solution data.

        Returns:
            String with strain rate.
        """
        ans = f"eps_dot = {data['eps_dot']:.4e} s^-1"
        if "ratio" in data:
            ans += f", ratio(T2/T1) = {_fmt(data['ratio'])}"
        return ans


# ===================================================================
# 4. Fracture toughness  (tier 5)
# ===================================================================

@register
class FractureToughnessGenerator(StepGenerator):
    """Compute stress intensity factor and compare with K_Ic.

    K = sigma * sqrt(pi*a) * Y.  Given applied stress sigma, crack
    half-length a, and geometry factor Y, compute K and compare
    with the critical K_Ic to determine if fracture occurs.

    Difficulty scaling:
        Difficulty 1-3: Y=1 (centre crack), simple values.
        Difficulty 4-6: varied Y factors.
        Difficulty 7-8: compute critical crack length a_c.

    Prerequisites:
        multiplication.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "fracture_toughness"

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
        return "compute stress intensity factor and check fracture"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a fracture toughness problem.

        Args:
            difficulty: Controls geometry factor and problem variant.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        sigma = round(self._rng.uniform(50, 400), 4)
        a_mm = round(self._rng.uniform(0.5, 10.0), 4)
        a_m = round(a_mm * 1e-3, 4)
        k_ic = round(self._rng.uniform(20, 100), 4)

        if difficulty <= 3:
            y_factor = 1.0
        else:
            y_factor = round(self._rng.uniform(1.0, 1.5), 4)

        k_applied = round(sigma * math.sqrt(_PI * a_m) * y_factor, 4)
        fracture = k_applied >= k_ic

        data = {
            "sigma": sigma, "a_mm": a_mm, "a_m": a_m,
            "Y": y_factor, "K_Ic": k_ic,
            "K": k_applied, "fracture": fracture,
        }

        if difficulty >= 7:
            a_c = round((k_ic / (sigma * y_factor)) ** 2 / _PI, 4)
            a_c_mm = round(a_c * 1e3, 4)
            data["a_c"] = a_c
            data["a_c_mm"] = a_c_mm

        return "K = \\sigma \\sqrt{\\pi a} \\cdot Y", data

    def _create_steps(self, data: dict) -> list[str]:
        """Generate fracture toughness computation steps.

        Args:
            data: Solution data with stress, crack length, and K.

        Returns:
            List of step strings.
        """
        steps = [
            f"sigma = {_fmt(data['sigma'])} MPa, a = {_fmt(data['a_mm'])} mm, Y = {_fmt(data['Y'])}",
            f"K = {_fmt(data['sigma'])}*sqrt(pi*{data['a_m']:.4e})*{_fmt(data['Y'])}",
            f"K = {_fmt(data['K'])} MPa*sqrt(m)",
            f"K_Ic = {_fmt(data['K_Ic'])} MPa*sqrt(m)",
        ]
        status = "fracture" if data["fracture"] else "safe"
        steps.append(f"K {'>' if data['fracture'] else '<='} K_Ic -> {status}")
        if "a_c" in data:
            steps.append(f"a_c = {_fmt(data['a_c_mm'])} mm")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the stress intensity and fracture assessment.

        Args:
            data: Solution data.

        Returns:
            String with K and outcome.
        """
        status = "fracture" if data["fracture"] else "safe"
        ans = f"K = {_fmt(data['K'])} MPa*sqrt(m), {status}"
        if "a_c_mm" in data:
            ans += f", a_c = {_fmt(data['a_c_mm'])} mm"
        return ans


# ===================================================================
# 5. Corrosion rate  (tier 4)
# ===================================================================

@register
class CorrosionRateGenerator(StepGenerator):
    """Compute corrosion penetration rate from weight loss.

    CR = K * W / (A * t * rho).
    Given weight loss W (g), surface area A (cm^2), exposure time t (h),
    density rho (g/cm^3), and constant K, compute penetration rate.

    Difficulty scaling:
        Difficulty 1-3: simple integer values, K=87600 (mm/yr).
        Difficulty 4-6: decimal values.
        Difficulty 7-8: solve for time t given target CR.

    Prerequisites:
        division.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "corrosion_rate"

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
        return "compute corrosion penetration rate from weight loss"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a corrosion rate problem.

        Args:
            difficulty: Controls parameter precision and variant.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        k_const = 87600  # mm/yr conversion factor

        if difficulty <= 3:
            weight_loss = round(self._rng.uniform(0.5, 5.0), 1)
            area = round(self._rng.uniform(10, 100), 0)
            time_h = round(self._rng.uniform(100, 1000), 0)
            rho = round(self._rng.uniform(2.5, 8.5), 1)
        else:
            weight_loss = round(self._rng.uniform(0.1, 10.0), 4)
            area = round(self._rng.uniform(5, 200), 4)
            time_h = round(self._rng.uniform(24, 2000), 4)
            rho = round(self._rng.uniform(2.0, 9.0), 4)

        denom = round(area * time_h * rho, 4)
        cr = round(k_const * weight_loss / denom, 4)

        target = "CR" if difficulty < 7 else "t"

        return "CR = K \\cdot W / (A \\cdot t \\cdot \\rho)", {
            "K": k_const, "W": weight_loss,
            "A": area, "t": time_h, "rho": rho,
            "denom": denom, "CR": cr, "target": target,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate corrosion rate computation steps.

        Args:
            data: Solution data with weight loss and parameters.

        Returns:
            List of step strings.
        """
        steps = [
            f"W = {_fmt(data['W'])} g, A = {_fmt(data['A'])} cm^2, "
            f"t = {_fmt(data['t'])} h, rho = {_fmt(data['rho'])} g/cm^3",
            f"denom = A*t*rho = {_fmt(data['denom'])}",
        ]
        if data["target"] == "CR":
            steps.append(f"CR = {data['K']}*{_fmt(data['W'])}/{_fmt(data['denom'])}")
            steps.append(f"CR = {_fmt(data['CR'])} mm/yr")
        else:
            steps.append(f"t = K*W/(A*CR*rho) = {_fmt(data['t'])} h")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the corrosion rate or time.

        Args:
            data: Solution data.

        Returns:
            String with CR or t.
        """
        if data["target"] == "CR":
            return f"CR = {_fmt(data['CR'])} mm/yr"
        return f"t = {_fmt(data['t'])} h"


# ===================================================================
# 6. Composite rule of mixtures  (tier 4)
# ===================================================================

@register
class CompositeRuleMixturesGenerator(StepGenerator):
    """Compute composite modulus using rule of mixtures (upper bound).

    E_c = E_f * V_f + E_m * V_m, where V_m = 1 - V_f.
    Given fibre and matrix moduli and volume fraction, compute
    composite modulus.

    Difficulty scaling:
        Difficulty 1-3: simple round numbers.
        Difficulty 4-6: decimal values.
        Difficulty 7-8: compute V_f for target E_c.

    Prerequisites:
        multiplication.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "composite_rule_mixtures"

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
        return "compute composite modulus using rule of mixtures"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a rule of mixtures problem.

        Args:
            difficulty: Controls parameter precision and variant.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        e_f = round(self._rng.uniform(70, 400), 4)
        e_m = round(self._rng.uniform(2, 30), 4)
        v_f = round(self._rng.uniform(0.1, 0.7), 4)
        v_m = round(1 - v_f, 4)

        e_c = round(e_f * v_f + e_m * v_m, 4)

        target = "E_c" if difficulty < 7 else "V_f"

        return "E_c = E_f V_f + E_m V_m", {
            "E_f": e_f, "E_m": e_m,
            "V_f": v_f, "V_m": v_m,
            "E_c": e_c, "target": target,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate rule of mixtures steps.

        Args:
            data: Solution data with moduli and volume fractions.

        Returns:
            List of step strings.
        """
        steps = [
            f"E_f = {_fmt(data['E_f'])} GPa, E_m = {_fmt(data['E_m'])} GPa",
            f"V_f = {_fmt(data['V_f'])}, V_m = {_fmt(data['V_m'])}",
        ]
        if data["target"] == "E_c":
            steps.append(
                f"E_c = {_fmt(data['E_f'])}*{_fmt(data['V_f'])} + "
                f"{_fmt(data['E_m'])}*{_fmt(data['V_m'])}"
            )
            steps.append(f"E_c = {_fmt(data['E_c'])} GPa")
        else:
            steps.append(
                f"V_f = (E_c - E_m)/(E_f - E_m) = {_fmt(data['V_f'])}"
            )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the composite modulus or volume fraction.

        Args:
            data: Solution data.

        Returns:
            String with E_c or V_f.
        """
        if data["target"] == "E_c":
            return f"E_c = {_fmt(data['E_c'])} GPa"
        return f"V_f = {_fmt(data['V_f'])}"


# ===================================================================
# 7. Heat treatment  (tier 4)
# ===================================================================

@register
class HeatTreatmentGenerator(StepGenerator):
    """Predict material properties from heat treatment type.

    Quench -> martensite: high hardness, low toughness.
    Temper -> tempered martensite: moderate hardness, improved toughness.
    Anneal -> pearlite/ferrite: low hardness, high ductility.
    Normalise -> fine pearlite: moderate properties.

    Difficulty scaling:
        Difficulty 1-3: quench or anneal (extremes).
        Difficulty 4-6: all four treatments.
        Difficulty 7-8: rank multiple treatments by hardness.

    Prerequisites:
        comparison.
    """

    _TREATMENTS = {
        "quench": {
            "structure": "martensite",
            "hardness": "high (50-65 HRC)",
            "toughness": "low",
            "ductility": "low",
        },
        "temper": {
            "structure": "tempered martensite",
            "hardness": "moderate (30-50 HRC)",
            "toughness": "moderate",
            "ductility": "moderate",
        },
        "anneal": {
            "structure": "pearlite + ferrite",
            "hardness": "low (10-25 HRC)",
            "toughness": "high",
            "ductility": "high",
        },
        "normalise": {
            "structure": "fine pearlite",
            "hardness": "moderate (20-35 HRC)",
            "toughness": "moderate-high",
            "ductility": "moderate",
        },
    }

    _HARDNESS_RANK = ["quench", "temper", "normalise", "anneal"]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "heat_treatment"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

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
        return "predict material properties from heat treatment"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a heat treatment classification problem.

        Args:
            difficulty: Controls treatment pool and problem variant.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            pool = ["quench", "anneal"]
        elif difficulty <= 6:
            pool = list(self._TREATMENTS.keys())
        else:
            pool = list(self._TREATMENTS.keys())

        if difficulty >= 7:
            treatments = self._rng.sample(pool, min(3, len(pool)))
            ranking = sorted(
                treatments,
                key=lambda t: self._HARDNESS_RANK.index(t),
            )
            props = {t: self._TREATMENTS[t] for t in treatments}
            info = "; ".join(
                f"{t}: {props[t]['hardness']}" for t in treatments
            )
            return f"rank treatments by hardness: {info}", {
                "mode": "rank", "treatments": treatments,
                "ranking": ranking, "props": props,
            }

        treatment = self._rng.choice(pool)
        props = self._TREATMENTS[treatment]
        return (
            f"treatment: {treatment}, "
            f"produces {props['structure']}, "
            f"hardness {props['hardness']}",
            {"mode": "single", "treatment": treatment, "props": props},
        )

    def _create_steps(self, data: dict) -> list[str]:
        """Generate heat treatment classification steps.

        Args:
            data: Solution data with treatment and properties.

        Returns:
            List of step strings.
        """
        if data["mode"] == "single":
            p = data["props"]
            return [
                f"treatment: {data['treatment']}",
                f"structure: {p['structure']}",
                f"hardness: {p['hardness']}",
                f"toughness: {p['toughness']}, ductility: {p['ductility']}",
            ]
        steps = []
        for t in data["treatments"]:
            p = data["props"][t]
            steps.append(f"{t}: {p['structure']}, hardness {p['hardness']}")
        steps.append(f"hardness ranking: {' > '.join(data['ranking'])}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the properties or ranking.

        Args:
            data: Solution data.

        Returns:
            String with result.
        """
        if data["mode"] == "single":
            p = data["props"]
            return (
                f"{data['treatment']}: {p['structure']}, "
                f"hardness={p['hardness']}"
            )
        return f"hardness: {' > '.join(data['ranking'])}"


# ===================================================================
# 8. Grain size (Hall-Petch)  (tier 5)
# ===================================================================

@register
class GrainSizeGenerator(StepGenerator):
    """Compute yield stress from grain size via Hall-Petch equation.

    sigma_y = sigma_0 + k_y / sqrt(d).
    Given friction stress sigma_0, Hall-Petch slope k_y, and grain
    diameter d, compute yield stress.

    Difficulty scaling:
        Difficulty 1-3: simple grain sizes (10-100 um).
        Difficulty 4-6: fine grains (1-50 um).
        Difficulty 7-8: nanocrystalline (<1 um), solve for d.

    Prerequisites:
        division.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "grain_size"

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
        return "compute yield stress from grain size via Hall-Petch"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Hall-Petch grain size problem.

        Args:
            difficulty: Controls grain size range and variant.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        sigma_0 = round(self._rng.uniform(20, 100), 4)
        k_y = round(self._rng.uniform(0.1, 1.0), 4)

        if difficulty <= 3:
            d_um = round(self._rng.uniform(10, 100), 4)
        elif difficulty <= 6:
            d_um = round(self._rng.uniform(1, 50), 4)
        else:
            d_um = round(self._rng.uniform(0.05, 1.0), 4)

        d_m = round(d_um * 1e-6, 4)
        sqrt_d = round(math.sqrt(d_m), 4)
        hp_term = round(k_y / sqrt_d, 4)
        sigma_y = round(sigma_0 + hp_term, 4)

        target = "sigma_y" if difficulty < 7 else "d"

        return "\\sigma_y = \\sigma_0 + k_y / \\sqrt{d}", {
            "sigma_0": sigma_0, "k_y": k_y,
            "d_um": d_um, "d_m": d_m,
            "sqrt_d": sqrt_d, "hp_term": hp_term,
            "sigma_y": sigma_y, "target": target,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Hall-Petch computation steps.

        Args:
            data: Solution data with sigma_0, k_y, grain size.

        Returns:
            List of step strings.
        """
        steps = [
            f"sigma_0 = {_fmt(data['sigma_0'])} MPa, k_y = {_fmt(data['k_y'])} MPa*m^0.5",
            f"d = {_fmt(data['d_um'])} um = {data['d_m']:.4e} m",
            f"sqrt(d) = {data['sqrt_d']:.4e} m^0.5",
            f"k_y/sqrt(d) = {_fmt(data['hp_term'])} MPa",
        ]
        if data["target"] == "sigma_y":
            steps.append(f"sigma_y = {_fmt(data['sigma_0'])} + {_fmt(data['hp_term'])} = {_fmt(data['sigma_y'])} MPa")
        else:
            steps.append(f"d = (k_y/(sigma_y-sigma_0))^2 = {_fmt(data['d_um'])} um")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the yield stress or grain size.

        Args:
            data: Solution data.

        Returns:
            String with sigma_y or d.
        """
        if data["target"] == "sigma_y":
            return f"sigma_y = {_fmt(data['sigma_y'])} MPa"
        return f"d = {_fmt(data['d_um'])} um"
