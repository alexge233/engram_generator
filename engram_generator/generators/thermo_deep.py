"""Deep thermodynamics generators -- cycles, potentials, and statistical thermo.

Extends the thermodynamics domain with Stirling cycle, Joule expansion,
Gibbs phase rule, chemical potential, heat pump COP, Debye temperature,
fugacity, and availability/exergy. Tiers range from 4 to 6.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register

_R = 8.314   # universal gas constant (J/(mol*K))
_KB = 1.381e-23  # Boltzmann constant (J/K)


class _ThermoDeepFormatter:
    """Formats numeric values for deep thermodynamics problems.

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


_f = _ThermoDeepFormatter.fmt


# ===================================================================
# 1. Stirling cycle  (tier 5)
# ===================================================================

@register
class StirlingCycleGenerator(StepGenerator):
    """Compute net work and efficiency of an ideal Stirling cycle.

    The Stirling cycle consists of two isothermal and two isochoric
    processes. W_net = nR(T_H - T_C) * ln(V2/V1). Efficiency equals
    Carnot for ideal regeneration: eta = 1 - T_C/T_H.

    Difficulty scaling:
        Difficulty 1-3: compute W_net with integer n, T, and volume ratio.
        Difficulty 4-6: compute W_net and compare efficiency to Carnot.
        Difficulty 7-8: non-ideal regenerator (given efficiency fraction).

    Prerequisites:
        carnot_efficiency.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "stirling_cycle"

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
        return "compute Stirling cycle work and efficiency"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate Stirling cycle parameters.

        Args:
            difficulty: Controls problem complexity.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        n = self._rng.randint(1, 3)
        t_h = self._rng.randint(400, 800)
        t_c = self._rng.randint(280, t_h - 50)
        v_ratio = self._rng.randint(2, 8)

        w_net = round(n * _R * (t_h - t_c) * math.log(v_ratio), 4)
        eta_carnot = round(1 - t_c / t_h, 4)

        if difficulty <= 3:
            return "W = nR(T_H-T_C)ln(V2/V1)", {
                "n": n, "T_H": t_h, "T_C": t_c,
                "V_ratio": v_ratio, "W_net": w_net,
                "eta_carnot": eta_carnot, "mode": "work",
            }
        if difficulty <= 6:
            return "W = nR(T_H-T_C)ln(V2/V1), eta = 1-T_C/T_H", {
                "n": n, "T_H": t_h, "T_C": t_c,
                "V_ratio": v_ratio, "W_net": w_net,
                "eta_carnot": eta_carnot, "mode": "full",
            }
        # Non-ideal regenerator
        regen_eff = round(self._rng.uniform(0.5, 0.95), 2)
        q_regen_saved = round(
            regen_eff * n * _R * (t_h - t_c) / (math.log(v_ratio)), 4
        )
        eta_actual = round(w_net / (w_net / eta_carnot - q_regen_saved * (1 - regen_eff)), 4)
        return "Stirling with non-ideal regenerator", {
            "n": n, "T_H": t_h, "T_C": t_c,
            "V_ratio": v_ratio, "W_net": w_net,
            "eta_carnot": eta_carnot,
            "regen_eff": regen_eff, "eta_actual": eta_actual,
            "mode": "non_ideal",
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Stirling cycle computation steps.

        Args:
            data: Solution data.

        Returns:
            List of step strings.
        """
        steps = [
            f"n={data['n']}mol, T_H={data['T_H']}K, T_C={data['T_C']}K",
            f"V2/V1 = {data['V_ratio']}",
            f"W = {data['n']}*{_f(_R)}*({data['T_H']}-{data['T_C']})"
            f"*ln({data['V_ratio']})",
        ]
        if data["mode"] != "work":
            steps.append(f"eta_Carnot = 1-{data['T_C']}/{data['T_H']}"
                         f" = {_f(data['eta_carnot'])}")
        if data["mode"] == "non_ideal":
            steps.append(f"Regenerator eff = {data['regen_eff']}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return cycle work and efficiency.

        Args:
            data: Solution data.

        Returns:
            Result string with units.
        """
        if data["mode"] == "work":
            return f"W_net = {_f(data['W_net'])} J"
        if data["mode"] == "full":
            return (
                f"W_net = {_f(data['W_net'])} J, "
                f"eta = {_f(data['eta_carnot'])}"
            )
        return (
            f"W_net = {_f(data['W_net'])} J, "
            f"eta_actual = {_f(data['eta_actual'])}"
        )


# ===================================================================
# 2. Joule expansion  (tier 5)
# ===================================================================

@register
class JouleExpansionGenerator(StepGenerator):
    """Compute entropy change for free (Joule) expansion of ideal gas.

    Free expansion: dT = 0 (ideal gas), dS = nR * ln(V2/V1).
    Work done W = 0, heat Q = 0, but entropy increases.

    Difficulty scaling:
        Difficulty 1-3: integer volume ratio, compute dS.
        Difficulty 4-6: decimal volumes, compute dS and dS_universe.
        Difficulty 7-8: given dS, find required volume ratio.

    Prerequisites:
        logarithm.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "joule_expansion"

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
        return "compute entropy change for Joule free expansion"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate expansion parameters.

        Args:
            difficulty: Controls problem variant.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        n = self._rng.randint(1, 5)

        if difficulty <= 3:
            v_ratio = self._rng.randint(2, 10)
            ds = round(n * _R * math.log(v_ratio), 4)
            return "dS = nR ln(V2/V1)", {
                "n": n, "V_ratio": v_ratio, "dS": ds,
                "mode": "compute",
            }
        if difficulty <= 6:
            v1 = round(self._rng.uniform(1.0, 10.0), 1)
            v2 = round(self._rng.uniform(v1 + 1, 50.0), 1)
            v_ratio = v2 / v1
            ds = round(n * _R * math.log(v_ratio), 4)
            return "dS = nR ln(V2/V1)", {
                "n": n, "V1": v1, "V2": v2,
                "V_ratio": round(v_ratio, 4), "dS": ds,
                "mode": "volumes",
            }
        # Find volume ratio for given dS
        ds_target = round(self._rng.uniform(5, 50), 1)
        v_ratio = round(math.exp(ds_target / (n * _R)), 4)
        return "V2/V1 = exp(dS/(nR))", {
            "n": n, "dS": ds_target, "V_ratio": v_ratio,
            "mode": "find_ratio",
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Joule expansion computation steps.

        Args:
            data: Solution data.

        Returns:
            List of step strings.
        """
        steps = [f"n = {data['n']} mol, W=0, Q=0, dT=0"]
        if data["mode"] == "compute":
            steps.append(f"V2/V1 = {data['V_ratio']}")
            steps.append(f"dS = {data['n']}*{_f(_R)}*ln({data['V_ratio']})")
        elif data["mode"] == "volumes":
            steps.append(f"V1={data['V1']}L, V2={data['V2']}L")
            steps.append(f"V2/V1 = {_f(data['V_ratio'])}")
            steps.append(f"dS = nR*ln(V2/V1)")
        else:
            steps.append(f"dS = {data['dS']} J/K")
            steps.append(f"V2/V1 = exp({data['dS']}/({data['n']}*{_f(_R)}))")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the entropy change or volume ratio.

        Args:
            data: Solution data.

        Returns:
            Result string with units.
        """
        if data["mode"] == "find_ratio":
            return f"V2/V1 = {_f(data['V_ratio'])}"
        return f"dS = {_f(data['dS'])} J/K"


# ===================================================================
# 3. Gibbs phase rule  (tier 4)
# ===================================================================

@register
class GibbsPhaseRuleGenerator(StepGenerator):
    """Apply the Gibbs phase rule: F = C - P + 2.

    Given the number of components C and phases P, compute the
    degrees of freedom F.

    Difficulty scaling:
        Difficulty 1-3: single-component systems (water, CO2).
        Difficulty 4-6: two-component systems, identify F.
        Difficulty 7-8: given F and C, find P (or vice versa).

    Prerequisites:
        division.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "gibbs_phase_rule"

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
        return "apply Gibbs phase rule to determine degrees of freedom"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate phase rule parameters.

        Args:
            difficulty: Controls component count and target.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            c = 1
            p = self._rng.randint(1, 3)
        elif difficulty <= 6:
            c = self._rng.randint(1, 3)
            p = self._rng.randint(1, c + 2)
        else:
            c = self._rng.randint(1, 4)
            p = self._rng.randint(1, c + 2)

        f = c - p + 2

        if difficulty <= 6:
            return "F = C - P + 2", {
                "C": c, "P": p, "F": f, "target": "F",
            }
        # Solve for P
        target = self._rng.choice(["P", "C"])
        return "F = C - P + 2", {
            "C": c, "P": p, "F": f, "target": target,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate phase rule computation steps.

        Args:
            data: Solution data.

        Returns:
            List of step strings.
        """
        if data["target"] == "F":
            return [
                f"C={data['C']}, P={data['P']}",
                f"F = {data['C']} - {data['P']} + 2 = {data['F']}",
            ]
        if data["target"] == "P":
            return [
                f"C={data['C']}, F={data['F']}",
                f"P = C - F + 2 = {data['C']} - {data['F']} + 2",
            ]
        return [
            f"P={data['P']}, F={data['F']}",
            f"C = F + P - 2 = {data['F']} + {data['P']} - 2",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the degrees of freedom, phases, or components.

        Args:
            data: Solution data.

        Returns:
            Result string.
        """
        return f"{data['target']} = {data[data['target']]}"


# ===================================================================
# 4. Chemical potential  (tier 6)
# ===================================================================

@register
class ChemicalPotentialGenerator(StepGenerator):
    """Compute chemical potential for an ideal gas.

    mu = mu_0 + RT * ln(P/P_0) where mu_0 is the standard chemical
    potential, R is the gas constant, and P_0 is standard pressure.

    Difficulty scaling:
        Difficulty 1-3: compute mu at given T and P, integer values.
        Difficulty 4-6: compute change in mu between two states.
        Difficulty 7-8: find P for given mu.

    Prerequisites:
        logarithm.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "chemical_potential"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

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
        return "compute chemical potential of ideal gas"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate chemical potential parameters.

        Args:
            difficulty: Controls problem variant.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        t = self._rng.randint(273, 600)
        mu_0 = round(self._rng.uniform(-50000, -10000), 1)
        p_0 = 1.0  # atm

        if difficulty <= 3:
            p = self._rng.randint(1, 10)
            mu = round(mu_0 + _R * t * math.log(p / p_0), 4)
            return "mu = mu_0 + RT ln(P/P_0)", {
                "T": t, "mu_0": mu_0, "P": p,
                "mu": mu, "mode": "compute",
            }
        if difficulty <= 6:
            p1 = self._rng.randint(1, 5)
            p2 = self._rng.randint(p1 + 1, 20)
            mu1 = round(mu_0 + _R * t * math.log(p1 / p_0), 4)
            mu2 = round(mu_0 + _R * t * math.log(p2 / p_0), 4)
            d_mu = round(mu2 - mu1, 4)
            return "d_mu = RT ln(P2/P1)", {
                "T": t, "P1": p1, "P2": p2,
                "mu1": mu1, "mu2": mu2, "d_mu": d_mu,
                "mode": "change",
            }
        # Find P for given mu
        mu_target = round(mu_0 + self._rng.uniform(-5000, 5000), 1)
        p_needed = round(p_0 * math.exp((mu_target - mu_0) / (_R * t)), 4)
        return "P = P_0 exp((mu-mu_0)/(RT))", {
            "T": t, "mu_0": mu_0, "mu_target": mu_target,
            "P": p_needed, "mode": "find_P",
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate chemical potential computation steps.

        Args:
            data: Solution data.

        Returns:
            List of step strings.
        """
        if data["mode"] == "compute":
            return [
                f"T={data['T']}K, mu_0={_f(data['mu_0'])} J/mol",
                f"P={data['P']} atm, P_0=1 atm",
                f"mu = {_f(data['mu_0'])} + {_f(_R)}*{data['T']}*ln({data['P']})",
            ]
        if data["mode"] == "change":
            return [
                f"T={data['T']}K, P1={data['P1']}atm, P2={data['P2']}atm",
                f"d_mu = RT*ln(P2/P1) = {_f(_R)}*{data['T']}*ln({data['P2']}/{data['P1']})",
            ]
        return [
            f"T={data['T']}K, mu_target={_f(data['mu_target'])} J/mol",
            f"P = exp((mu-mu_0)/(RT))",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the chemical potential or pressure.

        Args:
            data: Solution data.

        Returns:
            Result string with units.
        """
        if data["mode"] == "compute":
            return f"mu = {_f(data['mu'])} J/mol"
        if data["mode"] == "change":
            return f"d_mu = {_f(data['d_mu'])} J/mol"
        return f"P = {_f(data['P'])} atm"


# ===================================================================
# 5. Heat pump  (tier 4)
# ===================================================================

@register
class HeatPumpGenerator(StepGenerator):
    """Compute coefficient of performance for heat pump and refrigerator.

    COP_HP = Q_H/W = T_H/(T_H - T_C).
    COP_ref = Q_C/W = T_C/(T_H - T_C).
    Note: COP_HP = COP_ref + 1.

    Difficulty scaling:
        Difficulty 1-3: compute COP_HP from temperatures.
        Difficulty 4-6: compute both COP_HP and COP_ref.
        Difficulty 7-8: given COP and one T, find the other T.

    Prerequisites:
        division.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "heat_pump"

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
        return "compute heat pump and refrigerator COP"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate heat pump parameters.

        Args:
            difficulty: Controls problem variant.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        t_h = self._rng.randint(293, 353)  # 20-80 C in K
        t_c = self._rng.randint(253, t_h - 10)  # min 10K difference

        cop_hp = round(t_h / (t_h - t_c), 4)
        cop_ref = round(t_c / (t_h - t_c), 4)

        if difficulty <= 3:
            return "COP_HP = T_H/(T_H-T_C)", {
                "T_H": t_h, "T_C": t_c,
                "COP_HP": cop_hp, "COP_ref": cop_ref,
                "mode": "hp",
            }
        if difficulty <= 6:
            return "COP_HP = T_H/(T_H-T_C), COP_ref = T_C/(T_H-T_C)", {
                "T_H": t_h, "T_C": t_c,
                "COP_HP": cop_hp, "COP_ref": cop_ref,
                "mode": "both",
            }
        # Find T_C given COP_HP and T_H
        t_c_found = round(t_h * (1 - 1 / cop_hp), 4)
        return "T_C = T_H(1 - 1/COP_HP)", {
            "T_H": t_h, "T_C": t_c, "T_C_found": t_c_found,
            "COP_HP": cop_hp, "COP_ref": cop_ref,
            "mode": "find_T",
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate heat pump COP computation steps.

        Args:
            data: Solution data.

        Returns:
            List of step strings.
        """
        if data["mode"] in ("hp", "both"):
            steps = [
                f"T_H={data['T_H']}K, T_C={data['T_C']}K",
                f"COP_HP = {data['T_H']}/({data['T_H']}-{data['T_C']})",
            ]
            if data["mode"] == "both":
                steps.append(
                    f"COP_ref = {data['T_C']}/({data['T_H']}-{data['T_C']})"
                )
            return steps
        return [
            f"T_H={data['T_H']}K, COP_HP={_f(data['COP_HP'])}",
            f"T_C = T_H*(1 - 1/COP_HP)",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the COP values or temperature.

        Args:
            data: Solution data.

        Returns:
            Result string.
        """
        if data["mode"] == "hp":
            return f"COP_HP = {_f(data['COP_HP'])}"
        if data["mode"] == "both":
            return (
                f"COP_HP = {_f(data['COP_HP'])}, "
                f"COP_ref = {_f(data['COP_ref'])}"
            )
        return f"T_C = {_f(data['T_C_found'])} K"


# ===================================================================
# 6. Debye temperature  (tier 5)
# ===================================================================

@register
class DebyeTemperatureGenerator(StepGenerator):
    """Classify heat capacity regime and compute C_V from Debye model.

    At T >> theta_D: C_V ~ 3Nk_B (Dulong-Petit limit).
    At T << theta_D: C_V ~ (12/5)*pi^4*Nk_B*(T/theta_D)^3.

    Difficulty scaling:
        Difficulty 1-3: T >> theta_D, compute C_V = 3Nk_B.
        Difficulty 4-6: classify regime, compute C_V in either limit.
        Difficulty 7-8: given C_V and T, estimate theta_D.

    Prerequisites:
        multiplication.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "debye_temperature"

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
        return "classify Debye regime and compute heat capacity"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate Debye model parameters.

        Args:
            difficulty: Controls regime and problem variant.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        n_atoms = self._rng.randint(1, 6) * 6.022e23  # moles
        n_moles = round(n_atoms / 6.022e23)
        theta_d = self._rng.randint(100, 600)

        if difficulty <= 3:
            t = self._rng.randint(theta_d * 2, theta_d * 5)
            cv = round(3 * n_moles * _R, 4)
            return "C_V = 3NR (Dulong-Petit)", {
                "N_moles": n_moles, "theta_D": theta_d, "T": t,
                "C_V": cv, "regime": "high_T", "mode": "compute",
            }
        if difficulty <= 6:
            high_t = self._rng.choice([True, False])
            if high_t:
                t = self._rng.randint(theta_d * 2, theta_d * 5)
                cv = round(3 * n_moles * _R, 4)
                regime = "high_T"
            else:
                t = self._rng.randint(max(5, theta_d // 20), theta_d // 5)
                cv = round(
                    (12 / 5) * math.pi ** 4 * n_moles * _R
                    * (t / theta_d) ** 3, 4
                )
                regime = "low_T"
            return "Debye model C_V", {
                "N_moles": n_moles, "theta_D": theta_d, "T": t,
                "C_V": cv, "regime": regime, "mode": "classify",
            }
        # Estimate theta_D from low-T C_V
        t = self._rng.randint(10, 50)
        cv = round(self._rng.uniform(0.01, 2.0), 2)
        # C_V = (12/5)*pi^4*NR*(T/theta_D)^3 => theta_D = T * ((12/5)*pi^4*NR/C_V)^(1/3)
        theta_est = round(
            t * ((12 / 5) * math.pi ** 4 * n_moles * _R / cv) ** (1 / 3), 4
        )
        return "theta_D from low-T C_V", {
            "N_moles": n_moles, "T": t, "C_V": cv,
            "theta_D_est": theta_est, "mode": "estimate",
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Debye model computation steps.

        Args:
            data: Solution data.

        Returns:
            List of step strings.
        """
        if data["mode"] == "compute":
            return [
                f"N={data['N_moles']}mol, theta_D={data['theta_D']}K, T={data['T']}K",
                f"T >> theta_D => Dulong-Petit",
                f"C_V = 3*{data['N_moles']}*{_f(_R)}",
            ]
        if data["mode"] == "classify":
            return [
                f"N={data['N_moles']}mol, theta_D={data['theta_D']}K, T={data['T']}K",
                f"Regime: {data['regime']}",
                f"C_V = {_f(data['C_V'])} J/K",
            ]
        return [
            f"N={data['N_moles']}mol, T={data['T']}K, C_V={data['C_V']} J/K",
            f"theta_D = T*((12/5)*pi^4*NR/C_V)^(1/3)",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return C_V or estimated theta_D.

        Args:
            data: Solution data.

        Returns:
            Result string with units.
        """
        if data["mode"] == "estimate":
            return f"theta_D ~ {_f(data['theta_D_est'])} K"
        return f"C_V = {_f(data['C_V'])} J/K"


# ===================================================================
# 7. Fugacity  (tier 6)
# ===================================================================

@register
class FugacityGenerator(StepGenerator):
    """Compute fugacity and fugacity coefficient for a real gas.

    For a van der Waals gas at moderate pressure:
    ln(f/P) ~ BP/(RT) where B is the second virial coefficient.
    Fugacity coefficient phi = f/P.

    Difficulty scaling:
        Difficulty 1-3: compute f = P * exp(BP/(RT)) with given B.
        Difficulty 4-6: compute both f and phi.
        Difficulty 7-8: given two temperatures, compare fugacities.

    Prerequisites:
        exponentiation.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "fugacity"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

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
        return "compute fugacity and fugacity coefficient"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate fugacity parameters.

        Args:
            difficulty: Controls problem variant.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        t = self._rng.randint(273, 600)
        p_atm = self._rng.randint(1, 50 + difficulty * 10)
        p_pa = p_atm * 101325
        # B in cm^3/mol, convert to m^3/mol
        b_cm3 = round(self._rng.uniform(-200, -10), 1)
        b = b_cm3 * 1e-6  # m^3/mol

        exp_arg = b * p_pa / (_R * t)
        f = round(p_pa * math.exp(exp_arg), 4)
        phi = round(f / p_pa, 4)

        if difficulty <= 3:
            return "f = P exp(BP/(RT))", {
                "T": t, "P_atm": p_atm, "P_Pa": p_pa,
                "B_cm3": b_cm3, "f": f, "phi": phi,
                "mode": "f_only",
            }
        if difficulty <= 6:
            return "f = P exp(BP/(RT)), phi = f/P", {
                "T": t, "P_atm": p_atm, "P_Pa": p_pa,
                "B_cm3": b_cm3, "f": f, "phi": phi,
                "mode": "full",
            }
        # Compare at two temperatures
        t2 = self._rng.randint(t + 50, t + 200)
        exp_arg2 = b * p_pa / (_R * t2)
        f2 = round(p_pa * math.exp(exp_arg2), 4)
        phi2 = round(f2 / p_pa, 4)
        return "Compare fugacity at two temperatures", {
            "T1": t, "T2": t2, "P_atm": p_atm, "P_Pa": p_pa,
            "B_cm3": b_cm3,
            "f1": f, "phi1": phi, "f2": f2, "phi2": phi2,
            "mode": "compare",
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate fugacity computation steps.

        Args:
            data: Solution data.

        Returns:
            List of step strings.
        """
        if data["mode"] in ("f_only", "full"):
            steps = [
                f"T={data['T']}K, P={data['P_atm']}atm",
                f"B={data['B_cm3']} cm^3/mol",
                f"BP/(RT) = {data['B_cm3']}e-6*{data['P_Pa']}/({_f(_R)}*{data['T']})",
            ]
            if data["mode"] == "full":
                steps.append(f"phi = f/P = {_f(data['phi'])}")
            return steps
        return [
            f"P={data['P_atm']}atm, B={data['B_cm3']} cm^3/mol",
            f"T1={data['T1']}K: phi1={_f(data['phi1'])}",
            f"T2={data['T2']}K: phi2={_f(data['phi2'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return fugacity and coefficient.

        Args:
            data: Solution data.

        Returns:
            Result string with units.
        """
        if data["mode"] == "f_only":
            return f"f = {_f(data['f'])} Pa"
        if data["mode"] == "full":
            return f"f = {_f(data['f'])} Pa, phi = {_f(data['phi'])}"
        return (
            f"phi1 = {_f(data['phi1'])}, "
            f"phi2 = {_f(data['phi2'])}"
        )


# ===================================================================
# 8. Availability / Exergy  (tier 5)
# ===================================================================

@register
class AvailabilityExergyGenerator(StepGenerator):
    """Compute availability (exergy) of a thermodynamic system.

    A = (H - H_0) - T_0 * (S - S_0) where subscript 0 denotes
    the dead state (environment). This gives the maximum useful
    work extractable from the system.

    Difficulty scaling:
        Difficulty 1-3: given H, H_0, S, S_0, T_0, compute A directly.
        Difficulty 4-6: compute A per unit mass for steam.
        Difficulty 7-8: compute second-law efficiency eta_II = W_actual/A.

    Prerequisites:
        entropy_change.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "availability_exergy"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

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
        return "compute availability (exergy) of thermodynamic system"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate exergy parameters.

        Args:
            difficulty: Controls problem variant.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        t_0 = self._rng.randint(288, 303)  # environment temp

        if difficulty <= 3:
            h = round(self._rng.uniform(2000, 3500), 1)  # kJ/kg
            h_0 = round(self._rng.uniform(100, 500), 1)
            s = round(self._rng.uniform(6.0, 8.0), 3)  # kJ/(kg*K)
            s_0 = round(self._rng.uniform(0.3, 1.5), 3)
            a = round((h - h_0) - t_0 * (s - s_0), 4)
            return "A = (H-H_0) - T_0*(S-S_0)", {
                "H": h, "H_0": h_0, "S": s, "S_0": s_0,
                "T_0": t_0, "A": a, "mode": "direct",
            }
        if difficulty <= 6:
            h = round(self._rng.uniform(2500, 3500), 1)
            h_0 = round(self._rng.uniform(100, 400), 1)
            s = round(self._rng.uniform(6.0, 8.0), 3)
            s_0 = round(self._rng.uniform(0.3, 1.5), 3)
            a = round((h - h_0) - t_0 * (s - s_0), 4)
            return "A = (H-H_0) - T_0*(S-S_0)", {
                "H": h, "H_0": h_0, "S": s, "S_0": s_0,
                "T_0": t_0, "A": a, "mode": "steam",
            }
        # Second-law efficiency
        h = round(self._rng.uniform(2500, 3500), 1)
        h_0 = round(self._rng.uniform(100, 400), 1)
        s = round(self._rng.uniform(6.0, 8.0), 3)
        s_0 = round(self._rng.uniform(0.3, 1.5), 3)
        a = round((h - h_0) - t_0 * (s - s_0), 4)
        w_actual = round(a * self._rng.uniform(0.3, 0.9), 4)
        eta_ii = round(w_actual / a, 4)
        return "eta_II = W/A", {
            "H": h, "H_0": h_0, "S": s, "S_0": s_0,
            "T_0": t_0, "A": a,
            "W_actual": w_actual, "eta_II": eta_ii,
            "mode": "efficiency",
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate exergy computation steps.

        Args:
            data: Solution data.

        Returns:
            List of step strings.
        """
        steps = [
            f"T_0={data['T_0']}K",
            f"H={data['H']} kJ/kg, H_0={data['H_0']} kJ/kg",
            f"S={data['S']} kJ/(kg*K), S_0={data['S_0']} kJ/(kg*K)",
            f"A = ({data['H']}-{data['H_0']}) - {data['T_0']}*({data['S']}-{data['S_0']})",
        ]
        if data["mode"] == "efficiency":
            steps.append(f"A = {_f(data['A'])} kJ/kg")
            steps.append(f"W_actual = {_f(data['W_actual'])} kJ/kg")
            steps.append(f"eta_II = W/A")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the availability and optionally efficiency.

        Args:
            data: Solution data.

        Returns:
            Result string with units.
        """
        if data["mode"] == "efficiency":
            return (
                f"A = {_f(data['A'])} kJ/kg, "
                f"eta_II = {_f(data['eta_II'])}"
            )
        return f"A = {_f(data['A'])} kJ/kg"
