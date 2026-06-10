"""Extended thermodynamics generators -- cycles, real gases, and mixing.

Deepens the thermodynamics domain with Otto, Diesel, and Rankine power
cycles, refrigeration COP, throttling processes, Maxwell relations,
van der Waals equation of state, and entropy of mixing.
Tiers range from 4 (refrigeration) to 6 (Rankine, Maxwell).
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


class _ThermoExtFormatter:
    """Formats numeric values for extended thermodynamics problems.

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


_f = _ThermoExtFormatter.fmt

_R = 8.314  # J/(mol*K)


# ===================================================================
# 1. Otto cycle  (tier 5)
# ===================================================================

@register
class OttoCycleGenerator(StepGenerator):
    """Otto cycle efficiency: eta = 1 - 1/r^(gamma-1).

    Models the four-step Otto cycle (isentropic compression,
    constant-volume heat addition, isentropic expansion,
    constant-volume heat rejection) and computes the thermal
    efficiency from the compression ratio r and heat capacity
    ratio gamma.

    Difficulty scaling:
        Difficulty 1-3: small compression ratios (6-8), gamma=1.4.
        Difficulty 4-6: wider compression ratios (6-12).
        Difficulty 7-8: also compute net work from given Q_in.

    Prerequisites:
        carnot_efficiency.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "otto_cycle"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["carnot_efficiency"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute Otto cycle efficiency"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate Otto cycle parameters and compute efficiency.

        Args:
            difficulty: Controls compression ratio range.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        gamma = 1.4
        if difficulty <= 3:
            r = self._rng.randint(6, 8)
        else:
            r = self._rng.randint(6, 12)
        gm1 = round(gamma - 1, 4)
        r_pow = round(r ** gm1, 4)
        eta = round(1 - 1 / r_pow, 4)

        data = {
            "r": r, "gamma": gamma, "gm1": gm1,
            "r_pow": r_pow, "eta": eta,
        }
        if difficulty >= 7:
            q_in = self._rng.randint(500, 2000)
            w_net = round(eta * q_in, 4)
            data["Q_in"] = q_in
            data["W_net"] = w_net

        return "\\eta = 1 - \\frac{1}{r^{\\gamma-1}}", data

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Otto cycle computation steps.

        Args:
            data: Solution data with compression ratio and gamma.

        Returns:
            List of step strings.
        """
        steps = [
            f"r = {data['r']}, gamma = {data['gamma']}",
            f"r^(gamma-1) = {data['r']}^{{{data['gm1']}}} = {_f(data['r_pow'])}",
            f"eta = 1 - 1/{_f(data['r_pow'])}",
        ]
        if "Q_in" in data:
            steps.append(
                f"W_net = eta*Q_in = {_f(data['eta'])}*{data['Q_in']}"
            )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the Otto cycle efficiency and optional work.

        Args:
            data: Solution data.

        Returns:
            String with eta and optionally W_net.
        """
        ans = f"eta = {_f(data['eta'])}"
        if "W_net" in data:
            ans += f", W_net = {_f(data['W_net'])} J"
        return ans


# ===================================================================
# 2. Diesel cycle  (tier 5)
# ===================================================================

@register
class DieselCycleGenerator(StepGenerator):
    """Diesel cycle efficiency from compression and cutoff ratios.

    eta = 1 - (1/r^(gamma-1)) * (rc^gamma - 1) / (gamma*(rc - 1)).
    Given compression ratio r and cutoff ratio rc, computes the
    thermal efficiency.

    Difficulty scaling:
        Difficulty 1-3: integer r (14-18), rc near 2.
        Difficulty 4-6: wider rc range (1.5-3.5).
        Difficulty 7-8: compare with Otto cycle at same r.

    Prerequisites:
        carnot_efficiency.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "diesel_cycle"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["carnot_efficiency"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute Diesel cycle efficiency"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate Diesel cycle parameters and compute efficiency.

        Args:
            difficulty: Controls ratio ranges.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        gamma = 1.4
        r = self._rng.randint(14, 22)
        if difficulty <= 3:
            rc = round(self._rng.uniform(1.8, 2.2), 2)
        else:
            rc = round(self._rng.uniform(1.5, 3.5), 2)

        gm1 = round(gamma - 1, 4)
        r_pow = round(r ** gm1, 4)
        rc_g = round(rc ** gamma, 4)
        num = round(rc_g - 1, 4)
        den = round(gamma * (rc - 1), 4)
        bracket = round(num / den, 4)
        eta = round(1 - bracket / r_pow, 4)

        data = {
            "r": r, "rc": rc, "gamma": gamma, "gm1": gm1,
            "r_pow": r_pow, "rc_g": rc_g,
            "num": num, "den": den, "bracket": bracket,
            "eta": eta,
        }
        if difficulty >= 7:
            eta_otto = round(1 - 1 / r_pow, 4)
            data["eta_otto"] = eta_otto

        return ("\\eta = 1 - \\frac{1}{r^{\\gamma-1}}"
                "\\frac{r_c^\\gamma - 1}{\\gamma(r_c - 1)}"), data

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Diesel cycle computation steps.

        Args:
            data: Solution data with ratios and intermediates.

        Returns:
            List of step strings.
        """
        steps = [
            f"r={data['r']}, rc={data['rc']}, gamma={data['gamma']}",
            f"r^(gamma-1) = {_f(data['r_pow'])}",
            f"rc^gamma = {data['rc']}^{{{data['gamma']}}} = {_f(data['rc_g'])}",
            f"(rc^g-1)/(gamma*(rc-1)) = {_f(data['num'])}/{_f(data['den'])} = {_f(data['bracket'])}",
        ]
        if "eta_otto" in data:
            steps.append(f"Otto eta = 1 - 1/{_f(data['r_pow'])} = {_f(data['eta_otto'])}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the Diesel cycle efficiency.

        Args:
            data: Solution data.

        Returns:
            String with eta value.
        """
        ans = f"eta = {_f(data['eta'])}"
        if "eta_otto" in data:
            ans += f", Otto eta = {_f(data['eta_otto'])}"
        return ans


# ===================================================================
# 3. Rankine cycle  (tier 6)
# ===================================================================

@register
class RankineCycleGenerator(StepGenerator):
    """Rankine cycle: boiler, turbine, condenser, pump.

    Computes net work W_net = (h1-h2) - (h4-h3) and thermal
    efficiency eta = W_net / Q_in where Q_in = h1 - h4.
    Uses given enthalpy values at each state point.

    Difficulty scaling:
        Difficulty 1-4: typical steam cycle enthalpies.
        Difficulty 5-8: wider enthalpy ranges, also compute Q_out.

    Prerequisites:
        first_law_thermo.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "rankine_cycle"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["first_law_thermo"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "analyse Rankine cycle from enthalpies"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate Rankine cycle enthalpy values and compute efficiency.

        State points: 1=turbine inlet, 2=turbine exit,
        3=condenser exit, 4=pump exit.

        Args:
            difficulty: Controls enthalpy ranges.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        scale = max(1, difficulty)
        h1 = self._rng.randint(2800, 3400)
        h2 = self._rng.randint(2000, 2600)
        h3 = self._rng.randint(150, 350)
        h4 = h3 + self._rng.randint(2, 10 + scale)

        w_turbine = round(h1 - h2, 4)
        w_pump = round(h4 - h3, 4)
        w_net = round(w_turbine - w_pump, 4)
        q_in = round(h1 - h4, 4)
        eta = round(w_net / q_in, 4) if q_in > 0 else 0.0
        q_out = round(h2 - h3, 4)

        return "\\eta = \\frac{W_{net}}{Q_{in}}", {
            "h1": h1, "h2": h2, "h3": h3, "h4": h4,
            "W_turbine": w_turbine, "W_pump": w_pump,
            "W_net": w_net, "Q_in": q_in, "Q_out": q_out,
            "eta": eta,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Rankine cycle computation steps.

        Args:
            data: Solution data with enthalpies and work.

        Returns:
            List of step strings.
        """
        return [
            f"h1={data['h1']}, h2={data['h2']}, h3={data['h3']}, h4={data['h4']} kJ/kg",
            f"W_turb = h1-h2 = {data['h1']}-{data['h2']} = {_f(data['W_turbine'])}",
            f"W_pump = h4-h3 = {data['h4']}-{data['h3']} = {_f(data['W_pump'])}",
            f"W_net = {_f(data['W_turbine'])}-{_f(data['W_pump'])} = {_f(data['W_net'])}",
            f"Q_in = h1-h4 = {data['h1']}-{data['h4']} = {_f(data['Q_in'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the Rankine cycle efficiency and net work.

        Args:
            data: Solution data.

        Returns:
            String with W_net and eta.
        """
        return (
            f"W_net = {_f(data['W_net'])} kJ/kg, "
            f"eta = {_f(data['eta'])}"
        )


# ===================================================================
# 4. Refrigeration COP  (tier 4)
# ===================================================================

@register
class RefrigerationCOPGenerator(StepGenerator):
    """Carnot refrigerator COP: COP = T_cold / (T_hot - T_cold).

    Computes the coefficient of performance for a Carnot
    refrigeration cycle from hot and cold reservoir temperatures.

    Difficulty scaling:
        Difficulty 1-3: round temperatures (multiples of 50 K).
        Difficulty 4-6: arbitrary temperatures.
        Difficulty 7-8: also compute COP from Q values.

    Prerequisites:
        carnot_efficiency.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "refrigeration_cop"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["carnot_efficiency"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute Carnot refrigerator COP"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate reservoir temperatures and compute COP.

        Args:
            difficulty: Controls temperature selection.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            t_cold = self._rng.choice([200, 250, 260, 270])
            t_hot = self._rng.choice([300, 350, 400])
        else:
            t_cold = self._rng.randint(200, 280)
            t_hot = self._rng.randint(290, 400)

        dt = t_hot - t_cold
        cop = round(t_cold / dt, 4)

        data = {"T_cold": t_cold, "T_hot": t_hot, "dT": dt, "COP": cop}

        if difficulty >= 7:
            q_cold = self._rng.randint(500, 2000)
            w = round(q_cold / cop, 4)
            q_hot = round(q_cold + w, 4)
            data["Q_cold"] = q_cold
            data["W"] = w
            data["Q_hot"] = q_hot

        return "COP = \\frac{T_C}{T_H - T_C}", data

    def _create_steps(self, data: dict) -> list[str]:
        """Generate COP computation steps.

        Args:
            data: Solution data with temperatures and COP.

        Returns:
            List of step strings.
        """
        steps = [
            f"T_C = {data['T_cold']} K, T_H = {data['T_hot']} K",
            f"T_H - T_C = {data['dT']} K",
            f"COP = {data['T_cold']}/{data['dT']}",
        ]
        if "Q_cold" in data:
            steps.append(f"W = Q_cold/COP = {data['Q_cold']}/{_f(data['COP'])} = {_f(data['W'])} J")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the refrigeration COP.

        Args:
            data: Solution data.

        Returns:
            String with COP value.
        """
        ans = f"COP = {_f(data['COP'])}"
        if "W" in data:
            ans += f", W = {_f(data['W'])} J"
        return ans


# ===================================================================
# 5. Throttling process  (tier 5)
# ===================================================================

@register
class ThrottlingProcessGenerator(StepGenerator):
    """Throttling process: isenthalpic expansion with Joule-Thomson effect.

    h_1 = h_2 (constant enthalpy). Temperature drop is
    dT = mu_JT * dP where mu_JT is the Joule-Thomson coefficient.
    Given mu_JT, inlet temperature, and pressure drop, computes
    the outlet temperature.

    Difficulty scaling:
        Difficulty 1-3: positive mu_JT (cooling), moderate dP.
        Difficulty 4-6: wider pressure drops.
        Difficulty 7-8: negative mu_JT (heating), compute inversion.

    Prerequisites:
        first_law_thermo.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "throttling_process"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["first_law_thermo"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute temperature change in throttling process"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate throttling process parameters and compute T_out.

        Args:
            difficulty: Controls mu_JT sign and pressure range.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        t_in = self._rng.randint(250, 400)

        if difficulty <= 6:
            mu_jt = round(self._rng.uniform(0.1, 0.8), 3)
        else:
            mu_jt = round(self._rng.uniform(-0.05, 0.8), 3)
            if abs(mu_jt) < 0.01:
                mu_jt = 0.3

        dp = self._rng.randint(100, 500 + difficulty * 200)
        dt = round(mu_jt * dp, 4)
        t_out = round(t_in - dt, 4)

        effect = "cooling" if dt > 0 else "heating"

        return "\\Delta T = \\mu_{JT} \\Delta P", {
            "T_in": t_in, "mu_JT": mu_jt, "dP": dp,
            "dT": dt, "T_out": t_out, "effect": effect,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate throttling computation steps.

        Args:
            data: Solution data with mu_JT, dP, temperatures.

        Returns:
            List of step strings.
        """
        return [
            f"h_1 = h_2 (isenthalpic)",
            f"mu_JT = {data['mu_JT']} K/kPa, dP = {data['dP']} kPa",
            f"dT = {data['mu_JT']}*{data['dP']} = {_f(data['dT'])} K",
            f"T_out = {data['T_in']} - {_f(data['dT'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the outlet temperature and effect.

        Args:
            data: Solution data.

        Returns:
            String with T_out and cooling/heating.
        """
        return f"T_out = {_f(data['T_out'])} K ({data['effect']})"


# ===================================================================
# 6. Maxwell relations  (tier 6)
# ===================================================================

@register
class MaxwellRelationsGenerator(StepGenerator):
    """Maxwell relations derived from thermodynamic potentials.

    From dU = TdS - PdV, derives (dT/dV)_S = -(dP/dS)_V.
    Applies a randomly chosen Maxwell relation to compute one
    partial derivative from a given value of another.

    Difficulty scaling:
        Difficulty 1-4: dU-based relation, integer values.
        Difficulty 5-6: dH or dG-based relations.
        Difficulty 7-8: dA-based relation, decimal values.

    Prerequisites:
        entropy_change.
    """

    _RELATIONS = [
        {
            "potential": "U", "form": "dU = TdS - PdV",
            "lhs": "(dT/dV)_S", "rhs": "-(dP/dS)_V",
            "sign": -1,
        },
        {
            "potential": "H", "form": "dH = TdS + VdP",
            "lhs": "(dT/dP)_S", "rhs": "(dV/dS)_P",
            "sign": 1,
        },
        {
            "potential": "G", "form": "dG = -SdT + VdP",
            "lhs": "-(dS/dP)_T", "rhs": "(dV/dT)_P",
            "sign": 1,
        },
        {
            "potential": "A", "form": "dA = -SdT - PdV",
            "lhs": "(dS/dV)_T", "rhs": "(dP/dT)_V",
            "sign": 1,
        },
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "maxwell_relations"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["entropy_change"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "apply Maxwell relation to compute partial derivative"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Maxwell relation problem with given partial value.

        Args:
            difficulty: Controls which relation and value range.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 4:
            rel = self._RELATIONS[0]
        elif difficulty <= 6:
            rel = self._rng.choice(self._RELATIONS[:3])
        else:
            rel = self._rng.choice(self._RELATIONS)

        if difficulty <= 4:
            given_val = self._rng.randint(1, 20)
        else:
            given_val = round(self._rng.uniform(0.5, 15.0), 3)

        result_val = round(rel["sign"] * given_val, 4)

        return rel["form"], {
            "potential": rel["potential"],
            "lhs": rel["lhs"], "rhs": rel["rhs"],
            "sign": rel["sign"],
            "given": _f(given_val), "given_val": given_val,
            "result": _f(result_val), "result_val": result_val,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Maxwell relation steps.

        Args:
            data: Solution data with relation and values.

        Returns:
            List of step strings.
        """
        sign_str = "-" if data["sign"] == -1 else ""
        return [
            f"from {data['potential']}: {data['lhs']} = {sign_str}{data['rhs']}",
            f"given {data['rhs']} = {data['given']}",
            f"{data['lhs']} = {sign_str}{data['given']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the computed partial derivative.

        Args:
            data: Solution data.

        Returns:
            String with the partial derivative value.
        """
        return f"{data['lhs']} = {data['result']}"


# ===================================================================
# 7. Van der Waals equation  (tier 5)
# ===================================================================

@register
class VanDerWaalsGenerator(StepGenerator):
    """Van der Waals equation: (P + a/V^2)(V - b) = nRT.

    Given constants a and b for a real gas, molar volume V, and
    temperature T, computes the pressure P and compares with the
    ideal gas prediction.

    Difficulty scaling:
        Difficulty 1-3: n=1, moderate V and T.
        Difficulty 4-6: wider ranges, compute ideal comparison.
        Difficulty 7-8: multiple moles, small V (large correction).

    Prerequisites:
        division.
    """

    _GASES = [
        ("N2", 0.1408, 3.913e-5),
        ("CO2", 0.3658, 4.286e-5),
        ("O2", 0.1382, 3.186e-5),
        ("H2O", 0.5536, 3.049e-5),
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "van_der_waals"

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
        return "compute pressure using van der Waals equation"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate van der Waals parameters and compute P.

        Args:
            difficulty: Controls gas choice and volume range.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        name, a, b = self._rng.choice(self._GASES)
        if difficulty <= 6:
            n = 1
        else:
            n = self._rng.randint(1, 3)

        t = self._rng.randint(273, 500)
        v = round(self._rng.uniform(0.5e-3, 5e-3), 6)

        correction_a = round(n * n * a / (v * v), 4)
        p_vdw = round(n * _R * t / (v - n * b) - correction_a, 4)
        p_ideal = round(n * _R * t / v, 4)
        diff = round(p_vdw - p_ideal, 4)

        return "(P + \\frac{n^2 a}{V^2})(V - nb) = nRT", {
            "gas": name, "a": a, "b": b, "n": n,
            "T": t, "V": v,
            "correction_a": correction_a,
            "P_vdw": p_vdw, "P_ideal": p_ideal,
            "diff": diff,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate van der Waals computation steps.

        Args:
            data: Solution data with gas constants and state.

        Returns:
            List of step strings.
        """
        return [
            f"{data['gas']}: a={data['a']}, b={data['b']}, n={data['n']}",
            f"nRT/(V-nb) = {data['n']}*{_R}*{data['T']}/({data['V']}-{data['n']}*{data['b']})",
            f"n^2*a/V^2 = {_f(data['correction_a'])}",
            f"P_ideal = nRT/V = {_f(data['P_ideal'])} Pa",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the van der Waals pressure and ideal comparison.

        Args:
            data: Solution data.

        Returns:
            String with P_vdw and P_ideal.
        """
        return (
            f"P_vdw = {_f(data['P_vdw'])} Pa, "
            f"P_ideal = {_f(data['P_ideal'])} Pa"
        )


# ===================================================================
# 8. Entropy of mixing  (tier 5)
# ===================================================================

@register
class EntropyMixingGenerator(StepGenerator):
    """Entropy of mixing ideal gases: dS = -nR * sum(x_i * ln(x_i)).

    Given total moles n and mole fractions x_i for 2-4 components,
    computes the entropy of mixing.

    Difficulty scaling:
        Difficulty 1-3: 2 components, simple fractions.
        Difficulty 4-6: 3 components.
        Difficulty 7-8: 4 components, decimal fractions.

    Prerequisites:
        logarithm.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "entropy_mixing"

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
        return "compute entropy of mixing for ideal gases"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate mole fractions and compute entropy of mixing.

        Args:
            difficulty: Controls number of components.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            num_comp = 2
        elif difficulty <= 6:
            num_comp = 3
        else:
            num_comp = 4

        n = self._rng.randint(1, 5)
        fracs = self._generate_fractions(num_comp)
        terms = [round(x * math.log(x), 4) for x in fracs]
        s_mix = round(-n * _R * sum(terms), 4)

        return "\\Delta S_{mix} = -nR \\sum x_i \\ln x_i", {
            "n": n, "fractions": fracs, "num_comp": num_comp,
            "terms": terms, "sum_terms": round(sum(terms), 4),
            "S_mix": s_mix,
        }

    def _generate_fractions(self, num_comp: int) -> list[float]:
        """Generate random mole fractions that sum to 1.

        Args:
            num_comp: Number of components.

        Returns:
            List of mole fractions summing to 1.
        """
        raw = [self._rng.random() for _ in range(num_comp)]
        total = sum(raw)
        fracs = [round(x / total, 4) for x in raw]
        fracs[-1] = round(1.0 - sum(fracs[:-1]), 4)
        return fracs

    def _create_steps(self, data: dict) -> list[str]:
        """Generate entropy of mixing computation steps.

        Args:
            data: Solution data with fractions and terms.

        Returns:
            List of step strings.
        """
        frac_str = ", ".join(f"x_{i+1}={x}" for i, x in enumerate(data["fractions"]))
        term_strs = []
        for i, (x, t) in enumerate(zip(data["fractions"], data["terms"])):
            term_strs.append(f"{x}*ln({x})={_f(t)}")

        return [
            f"n={data['n']}, {frac_str}",
            f"x_i*ln(x_i): {', '.join(term_strs)}",
            f"sum = {_f(data['sum_terms'])}",
            f"dS = -{data['n']}*{_R}*{_f(data['sum_terms'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the entropy of mixing.

        Args:
            data: Solution data.

        Returns:
            String with dS_mix and unit.
        """
        return f"dS_mix = {_f(data['S_mix'])} J/K"
