"""Polymer science generators -- polymerisation through thermodynamics.

Covers degree of polymerisation, number/weight-average molecular weights,
Fox equation for glass transition, freely jointed chain end-to-end distance,
Mark-Houwink intrinsic viscosity, and Flory-Huggins mixing free energy.
Tiers range from 4 (introductory polymer properties) to 6 (mixing
thermodynamics).
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


class _PolyFormatter:
    """Formats numeric values for polymer science problems.

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


_f = _PolyFormatter.fmt


# ===================================================================
# 1. Degree of polymerisation  (tier 4)
# ===================================================================

@register
class DegreePolymerisationGenerator(StepGenerator):
    """Compute degree of polymerisation from molecular weights.

    DP = M_n / M_0 where M_n = number-average molecular weight,
    M_0 = monomer molecular weight.

    Difficulty scaling:
        Difficulty 1-3: integer MW values, clean division.
        Difficulty 4-6: larger MW, decimal monomer weight.
        Difficulty 7-8: also compute chain length from DP.

    Prerequisites:
        division.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "degree_polymerisation"

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
        return "compute degree of polymerisation from molecular weights"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate number-average MW and monomer MW, compute DP.

        Args:
            difficulty: Controls MW ranges and extra computations.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            m_0 = float(self._rng.choice([28, 44, 56, 100, 104]))
            dp = self._rng.randint(10, 100 + difficulty * 50)
            m_n = m_0 * dp
        elif difficulty <= 6:
            m_0 = round(self._rng.uniform(28.0, 200.0), 1)
            m_n = round(m_0 * self._rng.randint(50, 500 + difficulty * 100), 1)
        else:
            m_0 = round(self._rng.uniform(28.0, 300.0), 2)
            m_n = round(m_0 * self._rng.randint(100, 2000), 1)

        dp_val = round(m_n / m_0, 4)

        return "DP = \\frac{M_n}{M_0}", {
            "M_n": m_n, "M_0": m_0, "DP": dp_val,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate computation steps for degree of polymerisation.

        Args:
            data: Solution data from _create_problem.

        Returns:
            List of step strings.
        """
        return [
            f"M_n = {_f(data['M_n'])} g/mol, M_0 = {_f(data['M_0'])} g/mol",
            f"DP = {_f(data['M_n'])}/{_f(data['M_0'])} = {_f(data['DP'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the degree of polymerisation.

        Args:
            data: Solution data.

        Returns:
            DP as a string.
        """
        return f"DP = {_f(data['DP'])}"


# ===================================================================
# 2. Molecular weight averages  (tier 5)
# ===================================================================

@register
class MolecularWeightAvgGenerator(StepGenerator):
    """Compute number-average and weight-average molecular weights, and PDI.

    M_n = sum(N_i*M_i) / sum(N_i).
    M_w = sum(N_i*M_i^2) / sum(N_i*M_i).
    PDI = M_w / M_n.

    Difficulty scaling:
        Difficulty 1-3: 2 fractions with integer counts and weights.
        Difficulty 4-6: 3-4 fractions with decimal values.
        Difficulty 7-8: 5-6 fractions, interpret PDI breadth.

    Prerequisites:
        arithmetic_mean.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "molecular_weight_avg"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["arithmetic_mean"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute M_n, M_w, and polydispersity index"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate molecular weight fractions and compute averages.

        Args:
            difficulty: Controls number of fractions and value ranges.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            n_fracs = 2
            counts = [self._rng.randint(10, 100) for _ in range(n_fracs)]
            weights = sorted(
                [float(self._rng.randint(5, 50) * 1000) for _ in range(n_fracs)]
            )
        elif difficulty <= 6:
            n_fracs = self._rng.randint(3, 4)
            counts = [self._rng.randint(5, 200) for _ in range(n_fracs)]
            weights = sorted(
                [round(self._rng.uniform(1000, 100000), 1) for _ in range(n_fracs)]
            )
        else:
            n_fracs = self._rng.randint(5, 6)
            counts = [self._rng.randint(5, 500) for _ in range(n_fracs)]
            weights = sorted(
                [round(self._rng.uniform(5000, 500000), 1) for _ in range(n_fracs)]
            )

        sum_ni = sum(counts)
        sum_ni_mi = sum(n * m for n, m in zip(counts, weights))
        sum_ni_mi2 = sum(n * m ** 2 for n, m in zip(counts, weights))

        m_n = round(sum_ni_mi / sum_ni, 4)
        m_w = round(sum_ni_mi2 / sum_ni_mi, 4)
        pdi = round(m_w / m_n, 4)

        return ("M_n = \\frac{\\sum N_i M_i}{\\sum N_i}, "
                "M_w = \\frac{\\sum N_i M_i^2}{\\sum N_i M_i}"), {
            "counts": counts, "weights": weights,
            "sum_NiMi": round(sum_ni_mi, 4),
            "sum_Ni": sum_ni,
            "sum_NiMi2": round(sum_ni_mi2, 4),
            "M_n": m_n, "M_w": m_w, "PDI": pdi,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate averaging computation steps.

        Args:
            data: Solution data from _create_problem.

        Returns:
            List of step strings.
        """
        fracs = ", ".join(
            f"({n},{_f(m)})"
            for n, m in zip(data["counts"], data["weights"])
        )
        return [
            f"fractions (N_i, M_i): {fracs}",
            f"sum(N_i*M_i) = {_f(data['sum_NiMi'])}, "
            f"sum(N_i) = {data['sum_Ni']}",
            f"M_n = {_f(data['sum_NiMi'])}/{data['sum_Ni']} "
            f"= {_f(data['M_n'])}",
            f"M_w = {_f(data['sum_NiMi2'])}/{_f(data['sum_NiMi'])} "
            f"= {_f(data['M_w'])}",
            f"PDI = {_f(data['M_w'])}/{_f(data['M_n'])} = {_f(data['PDI'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return M_n, M_w, and PDI.

        Args:
            data: Solution data.

        Returns:
            Molecular weight averages and PDI as a string.
        """
        return (f"M_n = {_f(data['M_n'])}, M_w = {_f(data['M_w'])}, "
                f"PDI = {_f(data['PDI'])}")


# ===================================================================
# 3. Glass transition (Fox equation)  (tier 4)
# ===================================================================

@register
class GlassTransitionGenerator(StepGenerator):
    """Compute glass transition temperature of a polymer blend via Fox equation.

    1/T_g = w_1/T_g1 + w_2/T_g2 where w_i are weight fractions
    and T_gi are glass transition temperatures in Kelvin.

    Difficulty scaling:
        Difficulty 1-3: two-component blend, simple fractions.
        Difficulty 4-6: two components, decimal fractions.
        Difficulty 7-8: three-component blend (extended Fox).

    Prerequisites:
        division.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "glass_transition"

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
        return "compute blend glass transition using the Fox equation"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate component Tg values and weight fractions, compute Tg_blend.

        Args:
            difficulty: Controls number of components and precision.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            w1 = self._rng.choice([0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8])
            w2 = round(1.0 - w1, 1)
            tg1 = float(self._rng.randint(300, 500))
            tg2 = float(self._rng.randint(200, 400))
            inv_tg = w1 / tg1 + w2 / tg2
            tg_blend = round(1.0 / inv_tg, 4)
            return "\\frac{1}{T_g} = \\frac{w_1}{T_{g1}} + \\frac{w_2}{T_{g2}}", {
                "n_components": 2,
                "weights": [w1, w2], "Tgs": [tg1, tg2],
                "inv_Tg": round(inv_tg, 4), "Tg_blend": tg_blend,
            }
        elif difficulty <= 6:
            w1 = round(self._rng.uniform(0.1, 0.9), 2)
            w2 = round(1.0 - w1, 2)
            tg1 = round(self._rng.uniform(250, 500), 1)
            tg2 = round(self._rng.uniform(150, 450), 1)
            inv_tg = w1 / tg1 + w2 / tg2
            tg_blend = round(1.0 / inv_tg, 4)
            return "\\frac{1}{T_g} = \\frac{w_1}{T_{g1}} + \\frac{w_2}{T_{g2}}", {
                "n_components": 2,
                "weights": [w1, w2], "Tgs": [tg1, tg2],
                "inv_Tg": round(inv_tg, 4), "Tg_blend": tg_blend,
            }
        else:
            w1 = round(self._rng.uniform(0.1, 0.5), 3)
            w2 = round(self._rng.uniform(0.1, 0.9 - w1), 3)
            w3 = round(1.0 - w1 - w2, 3)
            tg1 = round(self._rng.uniform(250, 500), 1)
            tg2 = round(self._rng.uniform(200, 450), 1)
            tg3 = round(self._rng.uniform(150, 400), 1)
            inv_tg = w1 / tg1 + w2 / tg2 + w3 / tg3
            tg_blend = round(1.0 / inv_tg, 4)
            return ("\\frac{1}{T_g} = \\sum_i \\frac{w_i}{T_{gi}}"), {
                "n_components": 3,
                "weights": [w1, w2, w3], "Tgs": [tg1, tg2, tg3],
                "inv_Tg": round(inv_tg, 4), "Tg_blend": tg_blend,
            }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Fox equation evaluation steps.

        Args:
            data: Solution data from _create_problem.

        Returns:
            List of step strings.
        """
        comp_str = ", ".join(
            f"w_{i+1}={_f(w)}, Tg_{i+1}={_f(tg)}K"
            for i, (w, tg) in enumerate(zip(data["weights"], data["Tgs"]))
        )
        terms = " + ".join(
            f"{_f(w)}/{_f(tg)}"
            for w, tg in zip(data["weights"], data["Tgs"])
        )
        return [
            comp_str,
            f"1/Tg = {terms} = {_f(data['inv_Tg'])}",
            f"Tg = 1/{_f(data['inv_Tg'])} = {_f(data['Tg_blend'])} K",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the blend glass transition temperature.

        Args:
            data: Solution data.

        Returns:
            Tg_blend as a string.
        """
        return f"Tg = {_f(data['Tg_blend'])} K"


# ===================================================================
# 4. End-to-end distance (freely jointed chain)  (tier 5)
# ===================================================================

@register
class EndToEndDistanceGenerator(StepGenerator):
    """Compute root-mean-square end-to-end distance for a freely jointed chain.

    <r^2>^(1/2) = l * sqrt(n) where l = bond length, n = number of bonds.

    Difficulty scaling:
        Difficulty 1-3: integer n, simple l values.
        Difficulty 4-6: larger n, decimal l.
        Difficulty 7-8: also compute radius of gyration Rg = r_rms / sqrt(6).

    Prerequisites:
        exponentiation.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "end_to_end_distance"

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
        return "compute RMS end-to-end distance for a freely jointed chain"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate bond length and count, compute r_rms.

        Args:
            difficulty: Controls parameter ranges and extra outputs.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            n_bonds = self._rng.randint(10, 100 + difficulty * 50)
            bond_len = round(self._rng.uniform(0.1, 0.3), 2)
        elif difficulty <= 6:
            n_bonds = self._rng.randint(100, 1000 + difficulty * 200)
            bond_len = round(self._rng.uniform(0.1, 0.2), 3)
        else:
            n_bonds = self._rng.randint(500, 5000)
            bond_len = round(self._rng.uniform(0.12, 0.18), 4)

        r_rms = round(bond_len * math.sqrt(n_bonds), 4)
        rg = round(r_rms / math.sqrt(6.0), 4)
        compute_rg = difficulty >= 7

        return "\\langle r^2 \\rangle^{1/2} = l \\sqrt{n}", {
            "l": bond_len, "n": n_bonds,
            "r_rms": r_rms, "Rg": rg,
            "compute_Rg": compute_rg,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate chain distance computation steps.

        Args:
            data: Solution data from _create_problem.

        Returns:
            List of step strings.
        """
        steps = [
            f"l = {_f(data['l'])} nm, n = {data['n']}",
            f"r_rms = {_f(data['l'])}*sqrt({data['n']}) "
            f"= {_f(data['r_rms'])} nm",
        ]
        if data["compute_Rg"]:
            steps.append(
                f"Rg = r_rms/sqrt(6) = {_f(data['r_rms'])}/sqrt(6) "
                f"= {_f(data['Rg'])} nm"
            )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the RMS end-to-end distance.

        Args:
            data: Solution data.

        Returns:
            r_rms as a string, with Rg if applicable.
        """
        if data["compute_Rg"]:
            return (f"r_rms = {_f(data['r_rms'])} nm, "
                    f"Rg = {_f(data['Rg'])} nm")
        return f"r_rms = {_f(data['r_rms'])} nm"


# ===================================================================
# 5. Intrinsic viscosity (Mark-Houwink)  (tier 5)
# ===================================================================

@register
class ViscosityIntrinsicGenerator(StepGenerator):
    """Compute intrinsic viscosity using the Mark-Houwink equation.

    [eta] = K * M^a where K and a are polymer-solvent constants
    and M is molecular weight.

    Difficulty scaling:
        Difficulty 1-3: integer M, simple K and a values.
        Difficulty 4-6: larger M, decimal K and a.
        Difficulty 7-8: also compute viscosity-average MW from [eta].

    Prerequisites:
        exponentiation.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "viscosity_intrinsic"

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
        return "compute intrinsic viscosity using the Mark-Houwink equation"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate Mark-Houwink parameters and compute intrinsic viscosity.

        Args:
            difficulty: Controls parameter ranges and extra computations.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            k_mh = round(self._rng.uniform(0.01, 0.1), 3)
            a_mh = round(self._rng.choice([0.5, 0.6, 0.7, 0.8]), 1)
            mol_wt = float(self._rng.randint(1, 50) * 1000)
        elif difficulty <= 6:
            k_mh = round(self._rng.uniform(0.001, 0.1), 4)
            a_mh = round(self._rng.uniform(0.5, 0.9), 2)
            mol_wt = round(self._rng.uniform(5000, 200000), 1)
        else:
            k_mh = round(self._rng.uniform(0.0001, 0.05), 4)
            a_mh = round(self._rng.uniform(0.5, 0.95), 3)
            mol_wt = round(self._rng.uniform(10000, 1000000), 1)

        eta = round(k_mh * mol_wt ** a_mh, 4)

        return "[\\eta] = K M^a", {
            "K": k_mh, "a": a_mh, "M": mol_wt, "eta": eta,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate computation steps for intrinsic viscosity.

        Args:
            data: Solution data from _create_problem.

        Returns:
            List of step strings.
        """
        return [
            f"K = {_f(data['K'])}, a = {_f(data['a'])}, "
            f"M = {_f(data['M'])} g/mol",
            f"M^a = {_f(data['M'])}^{_f(data['a'])}",
            f"[eta] = {_f(data['K'])}*{_f(data['M'])}^{_f(data['a'])} "
            f"= {_f(data['eta'])} dL/g",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the intrinsic viscosity.

        Args:
            data: Solution data.

        Returns:
            Intrinsic viscosity as a string.
        """
        return f"[eta] = {_f(data['eta'])} dL/g"


# ===================================================================
# 6. Flory-Huggins mixing free energy  (tier 6)
# ===================================================================

@register
class FloryHugginsGenerator(StepGenerator):
    """Compute Flory-Huggins free energy of mixing.

    dG_mix/(nkT) = phi_1*ln(phi_1)/N_1 + phi_2*ln(phi_2)/N_2
                   + chi*phi_1*phi_2.

    phi_1 + phi_2 = 1.

    Difficulty scaling:
        Difficulty 1-3: simple fractions, small N values, integer chi.
        Difficulty 4-6: decimal fractions, larger N, decimal chi.
        Difficulty 7-8: compute each term separately, assess miscibility.

    Prerequisites:
        logarithm.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "flory_huggins"

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
        return "compute Flory-Huggins free energy of mixing"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate volume fractions, chain lengths, chi, compute dG_mix.

        Args:
            difficulty: Controls parameter ranges and detail level.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            phi_1 = self._rng.choice([0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8])
            n_1 = self._rng.randint(1, 10)
            n_2 = self._rng.randint(1, 10)
            chi = float(self._rng.randint(0, 3))
        elif difficulty <= 6:
            phi_1 = round(self._rng.uniform(0.05, 0.95), 2)
            n_1 = self._rng.randint(1, 100)
            n_2 = self._rng.randint(1, 100)
            chi = round(self._rng.uniform(0.0, 3.0), 2)
        else:
            phi_1 = round(self._rng.uniform(0.01, 0.99), 3)
            n_1 = self._rng.randint(10, 1000)
            n_2 = self._rng.randint(10, 1000)
            chi = round(self._rng.uniform(0.0, 5.0), 3)

        phi_2 = round(1.0 - phi_1, 4)

        term_1 = phi_1 * math.log(phi_1) / n_1
        term_2 = phi_2 * math.log(phi_2) / n_2
        term_3 = chi * phi_1 * phi_2
        dg_mix = round(term_1 + term_2 + term_3, 4)

        return ("\\frac{\\Delta G_{\\mathrm{mix}}}{nkT} = "
                "\\frac{\\phi_1 \\ln\\phi_1}{N_1} + "
                "\\frac{\\phi_2 \\ln\\phi_2}{N_2} + "
                "\\chi \\phi_1 \\phi_2"), {
            "phi_1": phi_1, "phi_2": phi_2,
            "N_1": n_1, "N_2": n_2, "chi": chi,
            "term_1": round(term_1, 4),
            "term_2": round(term_2, 4),
            "term_3": round(term_3, 4),
            "dG_mix": dg_mix,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Flory-Huggins computation steps.

        Args:
            data: Solution data from _create_problem.

        Returns:
            List of step strings.
        """
        return [
            f"phi_1={_f(data['phi_1'])}, phi_2={_f(data['phi_2'])}, "
            f"N_1={data['N_1']}, N_2={data['N_2']}, chi={_f(data['chi'])}",
            f"term_1 = {_f(data['phi_1'])}*ln({_f(data['phi_1'])})/"
            f"{data['N_1']} = {_f(data['term_1'])}",
            f"term_2 = {_f(data['phi_2'])}*ln({_f(data['phi_2'])})/"
            f"{data['N_2']} = {_f(data['term_2'])}",
            f"term_3 = {_f(data['chi'])}*{_f(data['phi_1'])}*"
            f"{_f(data['phi_2'])} = {_f(data['term_3'])}",
            f"dG_mix/(nkT) = {_f(data['dG_mix'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the normalised free energy of mixing.

        Args:
            data: Solution data.

        Returns:
            Free energy of mixing as a string.
        """
        return f"dG_mix/(nkT) = {_f(data['dG_mix'])}"
