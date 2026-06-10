"""Thermodynamics generators -- laws, cycles, and phase transitions.

Covers the first and second laws of thermodynamics, work-energy
calculations, heat capacity, Carnot efficiency, entropy, Gibbs free
energy, the Clausius inequality, phase transitions, adiabatic
processes, and multi-step heat engine cycles.
Tiers range from 4 (introductory) to 6 (multi-step cycles).
"""
import math
from fractions import Fraction

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


class _ThermoFormatter:
    """Formats numeric values for thermodynamics problems.

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


# ---------------------------------------------------------------------------
# 1. First Law of Thermodynamics  (tier 4)
# ---------------------------------------------------------------------------


@register
class FirstLawGenerator(StepGenerator):
    """First law of thermodynamics: dU = Q - W.

    Given two of Q (heat added), W (work done by system), and dU
    (change in internal energy), computes the third quantity.
    Randomly selects which variable is the unknown.

    Input format:
        ``apply first law of thermodynamics``

    Target format:
        ``dU = Q - W <step> dU = 500 - 200 <step> dU = 300 J``

    Difficulty scaling:
        Difficulty 1: values in [10, 100].
        Difficulty 8: values in [80, 800].

    Prerequisites:
        addition, subtraction.
    """

    _UNKNOWNS = ["dU", "Q", "W"]

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "first_law_thermo"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["addition", "subtraction"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls parameter magnitude.

        Returns:
            Natural language description.
        """
        return "apply first law of thermodynamics"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate Q, W, dU values and hide one.

        Args:
            difficulty: Controls parameter magnitude.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        scale = max(1, difficulty)
        q = self._rng.randint(10 * scale, 100 * scale)
        w = self._rng.randint(1 * scale, q)
        du = q - w
        unknown = self._rng.choice(self._UNKNOWNS)
        return "dU = Q - W", {"Q": q, "W": w, "dU": du, "unknown": unknown}

    def _create_steps(self, data: dict) -> list[str]:
        """Generate substitution steps for the first law.

        Args:
            data: Solution data with Q, W, dU, and unknown.

        Returns:
            Steps showing rearrangement and substitution.
        """
        unknown = data["unknown"]
        q, w, du = data["Q"], data["W"], data["dU"]
        if unknown == "dU":
            return [
                f"dU = Q - W",
                f"dU = {q} - {w}",
            ]
        if unknown == "Q":
            return [
                "Q = dU + W",
                f"Q = {du} + {w}",
            ]
        return [
            "W = Q - dU",
            f"W = {q} - {du}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the solved variable.

        Args:
            data: Solution data.

        Returns:
            String with the unknown value and unit.
        """
        unknown = data["unknown"]
        return f"{unknown} = {data[unknown]} J"


# ---------------------------------------------------------------------------
# 2. Work from PV processes  (tier 5)
# ---------------------------------------------------------------------------


@register
class WorkPVGenerator(StepGenerator):
    """Work from pressure-volume processes: W = P * dV (isobaric) or
    W = nRT ln(V2/V1) (isothermal).

    Generates isobaric or isothermal expansion/compression problems
    and computes the work done by the gas.

    Input format:
        ``compute work in a PV process``

    Target format (isobaric):
        ``W = P \\Delta V <step> \\Delta V = 0.5 - 0.2 = 0.3
        <step> W = 101325(0.3) <step> W = 30397.5 J``

    Target format (isothermal):
        ``W = nRT \\ln(V_2/V_1) <step> nRT = 2(8.314)(350) = 5819.8
        <step> \\ln(0.8/0.4) = 0.6931 <step> W = 4032.47 J``

    Difficulty scaling:
        Difficulty 1-4: isobaric only, small volumes.
        Difficulty 5-8: isothermal or isobaric, larger ranges.

    Prerequisites:
        definite_integral.
    """

    _R = 8.314  # J/(mol*K)

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "work_pv"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["definite_integral"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls process type and magnitude.

        Returns:
            Natural language description.
        """
        return "compute work in a PV process"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate PV process parameters and compute work.

        Chooses isobaric for low difficulty, either process for high.

        Args:
            difficulty: Controls process type and magnitude.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 4 or self._rng.random() < 0.5:
            return self._isobaric(difficulty)
        return self._isothermal(difficulty)

    def _isobaric(self, difficulty: int) -> tuple[str, dict]:
        """Generate an isobaric expansion problem.

        Args:
            difficulty: Controls volume range.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        scale = max(1, difficulty)
        p = self._rng.randint(50000, 50000 + 50000 * scale)
        v1 = round(self._rng.uniform(0.1, 0.5 * scale), 2)
        dv = round(self._rng.uniform(0.05, 0.3 * scale), 2)
        v2 = round(v1 + dv, 2)
        w = round(p * dv, 4)
        return "W = P \\Delta V", {
            "process": "isobaric", "P": p, "V1": v1, "V2": v2,
            "dV": dv, "W": w,
        }

    def _isothermal(self, difficulty: int) -> tuple[str, dict]:
        """Generate an isothermal expansion problem.

        Args:
            difficulty: Controls parameter ranges.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        n = self._rng.randint(1, max(1, difficulty))
        t = self._rng.randint(250, 250 + 50 * max(1, difficulty))
        v1 = round(self._rng.uniform(0.2, 1.0), 2)
        ratio = round(self._rng.uniform(1.5, 2.0 + difficulty * 0.5), 2)
        v2 = round(v1 * ratio, 2)
        nrt = round(n * self._R * t, 4)
        ln_ratio = round(math.log(v2 / v1), 4)
        w = round(nrt * ln_ratio, 4)
        return "W = nRT \\ln(V_2/V_1)", {
            "process": "isothermal", "n": n, "T": t, "R": self._R,
            "V1": v1, "V2": v2, "nRT": nrt,
            "ln_ratio": ln_ratio, "W": w,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate computation steps for the PV work.

        Args:
            data: Solution data with process type and intermediates.

        Returns:
            Steps showing the work calculation.
        """
        if data["process"] == "isobaric":
            return [
                f"\\Delta V = {data['V2']} - {data['V1']} = {data['dV']}",
                f"W = {data['P']}({data['dV']})",
            ]
        return [
            f"nRT = {data['n']}({data['R']})({data['T']}) = {_ThermoFormatter.fmt(data['nRT'])}",
            f"\\ln({data['V2']}/{data['V1']}) = {data['ln_ratio']}",
            f"W = {_ThermoFormatter.fmt(data['nRT'])}({data['ln_ratio']})",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the work done.

        Args:
            data: Solution data.

        Returns:
            String with W and unit.
        """
        return f"W = {_ThermoFormatter.fmt(data['W'])} J"


# ---------------------------------------------------------------------------
# 3. Heat Capacity  (tier 4)
# ---------------------------------------------------------------------------


@register
class HeatCapacityGenerator(StepGenerator):
    """Heat transfer using Q = mc dT or Q = nC dT.

    Computes the heat required to change the temperature of a
    substance, using either specific heat capacity (per mass) or
    molar heat capacity (per mole).

    Input format:
        ``compute heat transfer using heat capacity``

    Target format:
        ``Q = mc \\Delta T <step> \\Delta T = 80 - 20 = 60
        <step> Q = 2(4186)(60) <step> Q = 502320 J``

    Difficulty scaling:
        Difficulty 1-4: mass-based (Q = mc dT), small masses.
        Difficulty 5-8: molar-based (Q = nC dT) or larger masses.

    Prerequisites:
        multiplication.
    """

    # Specific heats in J/(kg*K)
    _SPECIFIC_HEATS = [
        ("water", 4186),
        ("aluminum", 897),
        ("iron", 449),
        ("copper", 385),
        ("lead", 128),
    ]
    # Molar heat capacities in J/(mol*K)
    _MOLAR_HEATS = [
        ("helium", 20.8),
        ("nitrogen", 29.1),
        ("oxygen", 29.4),
        ("carbon dioxide", 37.1),
    ]

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "heat_capacity"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["multiplication"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls whether mass or molar form is used.

        Returns:
            Natural language description.
        """
        return "compute heat transfer using heat capacity"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate heat capacity problem parameters.

        Args:
            difficulty: Controls form and magnitude.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 4 or self._rng.random() < 0.5:
            return self._mass_form(difficulty)
        return self._molar_form(difficulty)

    def _mass_form(self, difficulty: int) -> tuple[str, dict]:
        """Generate a mass-based heat capacity problem.

        Args:
            difficulty: Controls mass and temperature ranges.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        scale = max(1, difficulty)
        name, c = self._rng.choice(self._SPECIFIC_HEATS)
        m = round(self._rng.uniform(0.5, 2.0 * scale), 2)
        t1 = self._rng.randint(10, 30)
        t2 = self._rng.randint(t1 + 10 * scale, t1 + 50 * scale)
        dt = t2 - t1
        q = round(m * c * dt, 4)
        return "Q = mc \\Delta T", {
            "form": "mass", "substance": name, "m": m, "c": c,
            "T1": t1, "T2": t2, "dT": dt, "Q": q,
        }

    def _molar_form(self, difficulty: int) -> tuple[str, dict]:
        """Generate a molar heat capacity problem.

        Args:
            difficulty: Controls moles and temperature ranges.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        scale = max(1, difficulty)
        name, c_m = self._rng.choice(self._MOLAR_HEATS)
        n = self._rng.randint(1, 2 * scale)
        t1 = self._rng.randint(200, 400)
        t2 = self._rng.randint(t1 + 10, t1 + 30 * scale)
        dt = t2 - t1
        q = round(n * c_m * dt, 4)
        return "Q = nC \\Delta T", {
            "form": "molar", "substance": name, "n": n, "C": c_m,
            "T1": t1, "T2": t2, "dT": dt, "Q": q,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate multiplication steps for heat transfer.

        Args:
            data: Solution data with form and parameters.

        Returns:
            Steps showing dT calculation and multiplication.
        """
        dt = data["dT"]
        t1, t2 = data["T1"], data["T2"]
        if data["form"] == "mass":
            m, c = data["m"], data["c"]
            return [
                f"\\Delta T = {t2} - {t1} = {dt}",
                f"Q = {m}({c})({dt})",
            ]
        n, c_m = data["n"], data["C"]
        return [
            f"\\Delta T = {t2} - {t1} = {dt}",
            f"Q = {n}({c_m})({dt})",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the heat transferred.

        Args:
            data: Solution data.

        Returns:
            String with Q and unit.
        """
        return f"Q = {_ThermoFormatter.fmt(data['Q'])} J"


# ---------------------------------------------------------------------------
# 4. Carnot Efficiency  (tier 4)
# ---------------------------------------------------------------------------


@register
class CarnotEfficiencyGenerator(StepGenerator):
    """Carnot efficiency: eta = 1 - T_cold / T_hot.

    Computes the maximum theoretical efficiency of a heat engine
    operating between two temperature reservoirs. All temperatures
    are in Kelvin.

    Input format:
        ``compute carnot efficiency``

    Target format:
        ``\\eta = 1 - \\frac{T_C}{T_H} <step>
        \\frac{T_C}{T_H} = \\frac{300}{600} = 0.5
        <step> \\eta = 1 - 0.5 = 0.5``

    Difficulty scaling:
        Difficulty 1-3: round temperatures (multiples of 50 K).
        Difficulty 4-6: less round temperatures.
        Difficulty 7-8: close temperatures (small efficiency).

    Prerequisites:
        division.
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "carnot_efficiency"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["division"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls temperature ranges.

        Returns:
            Natural language description.
        """
        return "compute carnot efficiency"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate hot and cold reservoir temperatures and compute efficiency.

        Args:
            difficulty: Controls temperature selection.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        t_cold, t_hot = self._sample_temperatures(difficulty)
        ratio = Fraction(t_cold, t_hot)
        eta = 1 - float(ratio)
        return "\\eta = 1 - \\frac{T_C}{T_H}", {
            "T_cold": t_cold, "T_hot": t_hot,
            "ratio": round(float(ratio), 4),
            "eta": round(eta, 4),
        }

    def _sample_temperatures(self, difficulty: int) -> tuple[int, int]:
        """Sample cold and hot temperatures in Kelvin.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (T_cold, T_hot) in Kelvin.
        """
        if difficulty <= 3:
            t_cold = self._rng.choice([200, 250, 300, 350])
            t_hot = self._rng.choice([500, 600, 700, 800, 900, 1000])
        elif difficulty <= 6:
            t_cold = self._rng.randint(200, 400)
            t_hot = self._rng.randint(500, 1200)
        else:
            # Close temperatures -> small efficiency, harder arithmetic
            t_cold = self._rng.randint(300, 600)
            t_hot = t_cold + self._rng.randint(20, 100)
        return t_cold, t_hot

    def _create_steps(self, data: dict) -> list[str]:
        """Generate division and subtraction steps.

        Args:
            data: Solution data with temperatures and ratio.

        Returns:
            Steps showing ratio and subtraction from 1.
        """
        tc, th = data["T_cold"], data["T_hot"]
        ratio = data["ratio"]
        return [
            f"\\frac{{T_C}}{{T_H}} = \\frac{{{tc}}}{{{th}}} = {ratio}",
            f"\\eta = 1 - {ratio}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the Carnot efficiency.

        Args:
            data: Solution data.

        Returns:
            String with eta value.
        """
        return f"\\eta = {_ThermoFormatter.fmt(data['eta'])}"


# ---------------------------------------------------------------------------
# 5. Entropy Change  (tier 5)
# ---------------------------------------------------------------------------


@register
class EntropyChangeGenerator(StepGenerator):
    """Entropy change for a reversible process: dS = Q_rev / T or
    dS = nC ln(T2/T1) for temperature change.

    Computes entropy change from heat and temperature or from a
    temperature ratio using the logarithmic form.

    Input format:
        ``compute entropy change``

    Target format (simple):
        ``\\Delta S = \\frac{Q_{rev}}{T} <step>
        \\Delta S = \\frac{5000}{350} <step> \\Delta S = 14.2857 J/K``

    Target format (log):
        ``\\Delta S = nC \\ln(T_2/T_1) <step>
        nC = 2(29.1) = 58.2 <step>
        \\ln(500/300) = 0.5108 <step> \\Delta S = 29.73 J/K``

    Difficulty scaling:
        Difficulty 1-4: simple Q/T form.
        Difficulty 5-8: logarithmic form with nC.

    Prerequisites:
        division, logarithm.
    """

    _MOLAR_HEATS = [
        ("helium", 20.8),
        ("nitrogen", 29.1),
        ("oxygen", 29.4),
        ("argon", 20.8),
    ]

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "entropy_change"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["division", "logarithm"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls which form is used.

        Returns:
            Natural language description.
        """
        return "compute entropy change"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate entropy change problem parameters.

        Args:
            difficulty: Controls form and magnitude.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 4:
            return self._simple_form(difficulty)
        return self._log_form(difficulty)

    def _simple_form(self, difficulty: int) -> tuple[str, dict]:
        """Generate a simple Q_rev / T entropy problem.

        Args:
            difficulty: Controls magnitude.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        scale = max(1, difficulty)
        q = self._rng.randint(500 * scale, 5000 * scale)
        t = self._rng.randint(250, 600)
        ds = round(q / t, 4)
        return "\\Delta S = \\frac{Q_{rev}}{T}", {
            "form": "simple", "Q": q, "T": t, "dS": ds,
        }

    def _log_form(self, difficulty: int) -> tuple[str, dict]:
        """Generate a logarithmic entropy change problem.

        Args:
            difficulty: Controls parameter ranges.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        name, c_m = self._rng.choice(self._MOLAR_HEATS)
        n = self._rng.randint(1, max(1, difficulty - 2))
        t1 = self._rng.randint(200, 400)
        t2 = self._rng.randint(t1 + 50, t1 + 200)
        nc = round(n * c_m, 4)
        ln_ratio = round(math.log(t2 / t1), 4)
        ds = round(nc * ln_ratio, 4)
        return "\\Delta S = nC \\ln(T_2/T_1)", {
            "form": "log", "substance": name, "n": n, "C": c_m,
            "T1": t1, "T2": t2, "nC": nc,
            "ln_ratio": ln_ratio, "dS": ds,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate computation steps for entropy change.

        Args:
            data: Solution data with form and parameters.

        Returns:
            Steps showing the entropy calculation.
        """
        if data["form"] == "simple":
            return [
                f"\\Delta S = \\frac{{{data['Q']}}}{{{data['T']}}}",
            ]
        return [
            f"nC = {data['n']}({data['C']}) = {_ThermoFormatter.fmt(data['nC'])}",
            f"\\ln({data['T2']}/{data['T1']}) = {data['ln_ratio']}",
            f"\\Delta S = {_ThermoFormatter.fmt(data['nC'])}({data['ln_ratio']})",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the entropy change.

        Args:
            data: Solution data.

        Returns:
            String with dS and unit.
        """
        return f"\\Delta S = {_ThermoFormatter.fmt(data['dS'])} J/K"


# ---------------------------------------------------------------------------
# 6. Gibbs Free Energy  (tier 5)
# ---------------------------------------------------------------------------


@register
class FreeEnergyGenerator(StepGenerator):
    """Gibbs free energy: dG = dH - T * dS.

    Computes the change in Gibbs free energy and determines whether
    the process is spontaneous (dG < 0), non-spontaneous (dG > 0),
    or at equilibrium (dG = 0).

    Input format:
        ``compute gibbs free energy change``

    Target format:
        ``\\Delta G = \\Delta H - T \\Delta S <step>
        T \\Delta S = 298(0.15) = 44.7 <step>
        \\Delta G = -50 - 44.7 = -94.7 kJ <step> spontaneous``

    Difficulty scaling:
        Difficulty 1-4: integer kJ values, moderate temperatures.
        Difficulty 5-8: decimal values, wider ranges.

    Prerequisites:
        first_law_thermo, entropy_change.
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "free_energy"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["first_law_thermo", "entropy_change"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls parameter ranges.

        Returns:
            Natural language description.
        """
        return "compute gibbs free energy change"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate dH, T, dS and compute dG with spontaneity.

        Args:
            difficulty: Controls value ranges.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 4:
            dh = self._rng.randint(-200, 200)
            ds = round(self._rng.uniform(-0.5, 0.5), 2)
        else:
            dh = round(self._rng.uniform(-500, 500), 1)
            ds = round(self._rng.uniform(-1.0, 1.0), 3)
        t = self._rng.randint(250, 400 + difficulty * 50)
        t_ds = round(t * ds, 4)
        dg = round(dh - t_ds, 4)
        if abs(dg) < 0.01:
            spontaneity = "equilibrium"
        elif dg < 0:
            spontaneity = "spontaneous"
        else:
            spontaneity = "non-spontaneous"
        return "\\Delta G = \\Delta H - T \\Delta S", {
            "dH": dh, "T": t, "dS": ds, "TdS": t_ds,
            "dG": dg, "spontaneity": spontaneity,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate computation steps for Gibbs free energy.

        Args:
            data: Solution data with dH, T, dS, and intermediates.

        Returns:
            Steps showing TdS and subtraction.
        """
        t, ds = data["T"], data["dS"]
        t_ds = data["TdS"]
        dh = data["dH"]
        return [
            f"T \\Delta S = {t}({ds}) = {_ThermoFormatter.fmt(t_ds)}",
            f"\\Delta G = {_ThermoFormatter.fmt(dh)} - {_ThermoFormatter.fmt(t_ds)}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the Gibbs free energy change and spontaneity.

        Args:
            data: Solution data.

        Returns:
            String with dG, unit, and spontaneity.
        """
        dg = _ThermoFormatter.fmt(data["dG"])
        return f"\\Delta G = {dg} kJ, {data['spontaneity']}"


# ---------------------------------------------------------------------------
# 7. Clausius Inequality  (tier 6)
# ---------------------------------------------------------------------------


@register
class ClausiusInequalityGenerator(StepGenerator):
    """Clausius inequality: verify sum(Q_i / T_i) <= 0 for a cycle.

    Generates a thermodynamic cycle with 2-4 heat exchange steps and
    checks whether the Clausius inequality holds (reversible if = 0,
    irreversible if < 0, impossible if > 0).

    Input format:
        ``verify clausius inequality for a cycle``

    Target format:
        ``\\sum \\frac{Q_i}{T_i} \\leq 0 <step>
        \\frac{500}{600} + \\frac{-400}{300} = 0.8333 + (-1.3333) = -0.5
        <step> -0.5 \\leq 0: irreversible``

    Difficulty scaling:
        Difficulty 1-3: 2 steps, round numbers.
        Difficulty 4-6: 3 steps.
        Difficulty 7-8: 4 steps, tighter values.

    Prerequisites:
        entropy_change.
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "clausius_inequality"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["entropy_change"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls number of cycle steps.

        Returns:
            Natural language description.
        """
        return "verify clausius inequality for a cycle"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate heat exchange steps and compute the Clausius sum.

        Args:
            difficulty: Controls number of steps and magnitude.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            n_steps = 2
        elif difficulty <= 6:
            n_steps = 3
        else:
            n_steps = 4
        scale = max(1, difficulty)
        exchanges = []
        for _ in range(n_steps):
            q = self._rng.randint(-500 * scale, 500 * scale)
            if q == 0:
                q = 100
            t = self._rng.randint(200, 800)
            exchanges.append((q, t))
        ratios = [round(q / t, 4) for q, t in exchanges]
        total = round(sum(ratios), 4)
        if abs(total) < 1e-6:
            verdict = "reversible"
        elif total < 0:
            verdict = "irreversible"
        else:
            verdict = "impossible"
        return "\\sum \\frac{Q_i}{T_i} \\leq 0", {
            "exchanges": exchanges, "ratios": ratios,
            "total": total, "verdict": verdict,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate step-by-step Clausius sum computation.

        Args:
            data: Solution data with exchanges and ratios.

        Returns:
            Steps showing each Q/T term and the sum.
        """
        exchanges = data["exchanges"]
        ratios = data["ratios"]
        terms = []
        for (q, t), r in zip(exchanges, ratios):
            terms.append(f"\\frac{{{q}}}{{{t}}} = {r}")
        sum_expr = " + ".join(f"{r}" for r in ratios)
        return [
            " + ".join(terms),
            f"{sum_expr} = {_ThermoFormatter.fmt(data['total'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the Clausius sum and verdict.

        Args:
            data: Solution data.

        Returns:
            String with total and classification.
        """
        total = _ThermoFormatter.fmt(data["total"])
        return f"\\sum Q_i/T_i = {total}, {data['verdict']}"


# ---------------------------------------------------------------------------
# 8. Phase Transition  (tier 6)
# ---------------------------------------------------------------------------


@register
class PhaseTransitionGenerator(StepGenerator):
    """Phase transition: Q = mL for latent heat, or Clausius-Clapeyron
    dP/dT = L / (T * dV) for phase boundary slope.

    Generates latent heat or Clausius-Clapeyron problems for
    common phase transitions.

    Input format:
        ``compute phase transition quantity``

    Target format (latent heat):
        ``Q = mL <step> Q = 2(2260000) <step> Q = 4520000 J``

    Target format (Clausius-Clapeyron):
        ``\\frac{dP}{dT} = \\frac{L}{T \\Delta V} <step>
        T \\Delta V = 373(0.0305) = 11.3765 <step>
        \\frac{dP}{dT} = \\frac{2260000}{11.3765} = 198663.68 Pa/K``

    Difficulty scaling:
        Difficulty 1-4: latent heat (Q = mL).
        Difficulty 5-8: Clausius-Clapeyron.

    Prerequisites:
        derivative.
    """

    _TRANSITIONS = [
        {"name": "water boiling", "L": 2260000, "T": 373, "dV": 0.0305},
        {"name": "water freezing", "L": 334000, "T": 273, "dV": -0.0000905},
        {"name": "ethanol boiling", "L": 846000, "T": 351, "dV": 0.0280},
    ]

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "phase_transition"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["derivative"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls which form is used.

        Returns:
            Natural language description.
        """
        return "compute phase transition quantity"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a phase transition problem.

        Args:
            difficulty: Controls form selection.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 4:
            return self._latent_heat(difficulty)
        return self._clausius_clapeyron(difficulty)

    def _latent_heat(self, difficulty: int) -> tuple[str, dict]:
        """Generate a latent heat problem Q = mL.

        Args:
            difficulty: Controls mass range.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        trans = self._rng.choice(self._TRANSITIONS)
        scale = max(1, difficulty)
        m = round(self._rng.uniform(0.5, 2.0 * scale), 2)
        q = round(m * trans["L"], 4)
        return "Q = mL", {
            "form": "latent", "substance": trans["name"],
            "m": m, "L": trans["L"], "Q": q,
        }

    def _clausius_clapeyron(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Clausius-Clapeyron problem.

        Args:
            difficulty: Controls which transition is used.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        trans = self._rng.choice(self._TRANSITIONS)
        latent = trans["L"]
        t = trans["T"]
        dv = abs(trans["dV"])
        t_dv = round(t * dv, 4)
        dp_dt = round(latent / t_dv, 4)
        return "\\frac{dP}{dT} = \\frac{L}{T \\Delta V}", {
            "form": "clausius_clapeyron", "substance": trans["name"],
            "L": latent, "T": t, "dV": dv, "TdV": t_dv, "dPdT": dp_dt,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate computation steps for the phase transition.

        Args:
            data: Solution data with form and parameters.

        Returns:
            Steps showing the calculation.
        """
        if data["form"] == "latent":
            return [
                f"Q = {data['m']}({data['L']})",
            ]
        return [
            f"T \\Delta V = {data['T']}({data['dV']}) = {_ThermoFormatter.fmt(data['TdV'])}",
            f"\\frac{{dP}}{{dT}} = \\frac{{{data['L']}}}{{{_ThermoFormatter.fmt(data['TdV'])}}}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the computed phase transition quantity.

        Args:
            data: Solution data.

        Returns:
            String with the answer and unit.
        """
        if data["form"] == "latent":
            return f"Q = {_ThermoFormatter.fmt(data['Q'])} J"
        return f"dP/dT = {_ThermoFormatter.fmt(data['dPdT'])} Pa/K"


# ---------------------------------------------------------------------------
# 9. Adiabatic Process  (tier 5)
# ---------------------------------------------------------------------------


@register
class AdiabaticProcessGenerator(StepGenerator):
    """Adiabatic process relations: P1 V1^gamma = P2 V2^gamma and
    T V^(gamma-1) = const.

    Given initial state and one final-state variable, computes the
    remaining final-state variable using adiabatic relations for
    an ideal gas.

    Input format:
        ``compute adiabatic process variable``

    Target format (PV):
        ``P_1 V_1^\\gamma = P_2 V_2^\\gamma <step>
        V_1^\\gamma = 2^{1.4} = 2.6390 <step>
        P_1 V_1^\\gamma = 101325(2.6390) = 267397.18 <step>
        V_2^\\gamma = 1^{1.4} = 1 <step> P_2 = 267397.18``

    Difficulty scaling:
        Difficulty 1-4: PV relation, simple volumes.
        Difficulty 5-8: TV relation, wider ranges.

    Prerequisites:
        exponentiation.
    """

    _GAMMA_VALUES = [
        ("monatomic", Fraction(5, 3)),
        ("diatomic", Fraction(7, 5)),
    ]

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "adiabatic_process"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["exponentiation"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls which relation is used.

        Returns:
            Natural language description.
        """
        return "compute adiabatic process variable"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate adiabatic process parameters and solve.

        Args:
            difficulty: Controls relation type and ranges.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 4 or self._rng.random() < 0.5:
            return self._pv_relation(difficulty)
        return self._tv_relation(difficulty)

    def _pv_relation(self, difficulty: int) -> tuple[str, dict]:
        """Generate a PV adiabatic problem: solve for P2.

        Args:
            difficulty: Controls volume ranges.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        gas_name, gamma_frac = self._rng.choice(self._GAMMA_VALUES)
        gamma = float(gamma_frac)
        scale = max(1, difficulty)
        p1 = self._rng.randint(50000, 50000 + 50000 * scale)
        v1 = round(self._rng.uniform(1.0, 2.0 * scale), 2)
        v2 = round(self._rng.uniform(0.3, v1 - 0.1), 2)
        v1_g = round(v1 ** gamma, 4)
        v2_g = round(v2 ** gamma, 4)
        pv_const = round(p1 * v1_g, 4)
        p2 = round(pv_const / v2_g, 4)
        return "P_1 V_1^\\gamma = P_2 V_2^\\gamma", {
            "relation": "PV", "gas": gas_name,
            "gamma": round(gamma, 4), "P1": p1,
            "V1": v1, "V2": v2, "V1_g": v1_g, "V2_g": v2_g,
            "PV_const": pv_const, "P2": p2,
        }

    def _tv_relation(self, difficulty: int) -> tuple[str, dict]:
        """Generate a TV adiabatic problem: solve for T2.

        Args:
            difficulty: Controls temperature and volume ranges.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        gas_name, gamma_frac = self._rng.choice(self._GAMMA_VALUES)
        gamma = float(gamma_frac)
        gm1 = round(gamma - 1, 4)
        scale = max(1, difficulty)
        t1 = self._rng.randint(300, 300 + 100 * scale)
        v1 = round(self._rng.uniform(1.0, 2.0 * scale), 2)
        v2 = round(self._rng.uniform(0.3, v1 - 0.1), 2)
        v1_gm1 = round(v1 ** gm1, 4)
        v2_gm1 = round(v2 ** gm1, 4)
        tv_const = round(t1 * v1_gm1, 4)
        t2 = round(tv_const / v2_gm1, 4)
        return "T_1 V_1^{\\gamma-1} = T_2 V_2^{\\gamma-1}", {
            "relation": "TV", "gas": gas_name,
            "gamma": round(gamma, 4), "gm1": gm1,
            "T1": t1, "V1": v1, "V2": v2,
            "V1_gm1": v1_gm1, "V2_gm1": v2_gm1,
            "TV_const": tv_const, "T2": t2,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate computation steps for the adiabatic relation.

        Args:
            data: Solution data with relation type and parameters.

        Returns:
            Steps showing exponentiation and division.
        """
        if data["relation"] == "PV":
            gamma = data["gamma"]
            return [
                f"V_1^\\gamma = {data['V1']}^{{{gamma}}} = {data['V1_g']}",
                f"P_1 V_1^\\gamma = {data['P1']}({data['V1_g']}) = {_ThermoFormatter.fmt(data['PV_const'])}",
                f"V_2^\\gamma = {data['V2']}^{{{gamma}}} = {data['V2_g']}",
            ]
        gm1 = data["gm1"]
        return [
            f"V_1^{{\\gamma-1}} = {data['V1']}^{{{gm1}}} = {data['V1_gm1']}",
            f"T_1 V_1^{{\\gamma-1}} = {data['T1']}({data['V1_gm1']}) = {_ThermoFormatter.fmt(data['TV_const'])}",
            f"V_2^{{\\gamma-1}} = {data['V2']}^{{{gm1}}} = {data['V2_gm1']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the solved adiabatic variable.

        Args:
            data: Solution data.

        Returns:
            String with the answer and unit.
        """
        if data["relation"] == "PV":
            return f"P_2 = {_ThermoFormatter.fmt(data['P2'])} Pa"
        return f"T_2 = {_ThermoFormatter.fmt(data['T2'])} K"


# ---------------------------------------------------------------------------
# 10. Heat Engine Cycle  (tier 6)
# ---------------------------------------------------------------------------


@register
class HeatEngineCycleGenerator(StepGenerator):
    """Multi-step heat engine cycle: compute W_net, Q_in, and efficiency.

    Generates a thermodynamic cycle with 2-4 steps, each involving
    heat exchange and work. Computes net work, total heat input,
    and thermal efficiency eta = W_net / Q_in.

    Input format:
        ``analyse heat engine cycle``

    Target format:
        ``\\eta = \\frac{W_{net}}{Q_{in}} <step>
        step 1: Q=500 W=200 <step> step 2: Q=-300 W=0 <step>
        W_{net} = 200 + 0 = 200 <step>
        Q_{in} = 500 <step> \\eta = 200/500 = 0.4``

    Difficulty scaling:
        Difficulty 1-3: 2-step cycle, round numbers.
        Difficulty 4-6: 3-step cycle.
        Difficulty 7-8: 4-step cycle, larger values.

    Prerequisites:
        work_pv.
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "heat_engine_cycle"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["work_pv"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls number of cycle steps.

        Returns:
            Natural language description.
        """
        return "analyse heat engine cycle"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a multi-step heat engine cycle.

        Ensures W_net > 0 and Q_in > 0 for a valid engine cycle.

        Args:
            difficulty: Controls number of steps and magnitude.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            n_steps = 2
        elif difficulty <= 6:
            n_steps = 3
        else:
            n_steps = 4
        scale = max(1, difficulty)
        steps = self._generate_cycle(n_steps, scale)
        w_net = sum(s["W"] for s in steps)
        q_in = sum(s["Q"] for s in steps if s["Q"] > 0)
        # Ensure valid engine: W_net > 0 and Q_in > 0
        if w_net <= 0 or q_in <= 0:
            steps[0]["Q"] = abs(w_net) + 100 * scale
            steps[0]["W"] = abs(w_net) + 50 * scale
            w_net = sum(s["W"] for s in steps)
            q_in = sum(s["Q"] for s in steps if s["Q"] > 0)
        eta = round(w_net / q_in, 4) if q_in > 0 else 0.0
        return "\\eta = \\frac{W_{net}}{Q_{in}}", {
            "steps": steps, "W_net": w_net, "Q_in": q_in, "eta": eta,
        }

    def _generate_cycle(self, n_steps: int, scale: int) -> list[dict]:
        """Generate individual cycle steps with Q and W values.

        The first step always absorbs heat (Q > 0, W > 0).
        Subsequent steps may reject heat.

        Args:
            n_steps: Number of thermodynamic steps in the cycle.
            scale: Magnitude scale factor.

        Returns:
            List of dicts with Q and W for each step.
        """
        steps = []
        # First step: heat absorption
        q1 = self._rng.randint(200 * scale, 800 * scale)
        w1 = self._rng.randint(50 * scale, q1)
        steps.append({"Q": q1, "W": w1})
        # Remaining steps
        for _ in range(n_steps - 1):
            q = self._rng.randint(-400 * scale, 100 * scale)
            w = self._rng.randint(0, max(1, abs(q) // 2))
            if q < 0:
                w = -w  # Work done on system during rejection
            steps.append({"Q": q, "W": w})
        return steps

    def _create_steps(self, data: dict) -> list[str]:
        """Generate step-by-step cycle analysis.

        Args:
            data: Solution data with cycle steps and totals.

        Returns:
            Steps listing each process, then W_net, Q_in, eta.
        """
        result = []
        for i, s in enumerate(data["steps"], 1):
            result.append(f"step {i}: Q={s['Q']}, W={s['W']}")
        w_terms = " + ".join(str(s["W"]) for s in data["steps"])
        result.append(f"W_{{net}} = {w_terms} = {data['W_net']}")
        q_pos = [s["Q"] for s in data["steps"] if s["Q"] > 0]
        q_terms = " + ".join(str(q) for q in q_pos)
        result.append(f"Q_{{in}} = {q_terms} = {data['Q_in']}")
        return result

    def _create_answer(self, data: dict) -> str:
        """Return the cycle efficiency.

        Args:
            data: Solution data.

        Returns:
            String with W_net, Q_in, and eta.
        """
        return (
            f"\\eta = {data['W_net']}/{data['Q_in']}"
            f" = {_ThermoFormatter.fmt(data['eta'])}"
        )
