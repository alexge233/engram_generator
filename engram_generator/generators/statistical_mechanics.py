"""Statistical mechanics generators -- partition functions through grand canonical.

Covers the canonical ensemble (partition function, Boltzmann probability,
average energy), quantum statistics (Fermi-Dirac, Bose-Einstein), the 1D
Ising model, entropy, equipartition theorem, specific heat, and the grand
canonical ensemble. Tiers range from 5 (basic stat-mech) to 7 (grand
canonical).
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


# Boltzmann constant in SI units
_K_B = 1.381e-23


class _StatMechFormatter:
    """Formats numeric values for statistical mechanics problems.

    Provides scientific notation for very large or small numbers and
    clean decimal formatting for dimensionless quantities.
    """

    @staticmethod
    def format_sci(value: float, sig_figs: int = 4) -> str:
        """Format a number in LaTeX scientific notation.

        Args:
            value: Number to format.
            sig_figs: Significant figures to retain.

        Returns:
            LaTeX scientific notation string.
        """
        if value == 0:
            return "0"
        exponent = int(math.floor(math.log10(abs(value))))
        mantissa = round(value / (10 ** exponent), sig_figs - 1)
        sign = "-" if value < 0 else ""
        return f"{sign}{abs(mantissa)} \\times 10^{{{exponent}}}"

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
# 1. Partition function  (tier 5)
# ---------------------------------------------------------------------------


@register
class PartitionFunctionStatGenerator(StepGenerator):
    """Compute the partition function Z = sum exp(-E_i / kT).

    Generates discrete energy level systems (2-level, 3-level, or
    harmonic oscillator truncated to N levels) and computes the
    canonical partition function at a given temperature.

    Input format:
        ``compute the partition function``

    Target format:
        ``Z = \\sum_i e^{-E_i / k_B T} <step>
        E_0 = 0, E_1 = ... <step>
        e^{-E_0/kT} = 1, e^{-E_1/kT} = ... <step>
        Z = ...``

    Difficulty scaling:
        d1-3: 2-level system with simple energy gaps.
        d4-6: 3-level system.
        d7-8: harmonic oscillator truncated to 4-5 levels.

    Prerequisites:
        exponentiation.
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "partition_function_stat"

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
            difficulty: Controls number of energy levels.

        Returns:
            Natural language description.
        """
        return "compute the partition function"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate energy levels and temperature, compute Z.

        Args:
            difficulty: Controls number of levels.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        temp = self._rng.randint(100, 500 + 100 * difficulty)
        beta = 1.0 / (_K_B * temp)
        if difficulty <= 3:
            n_levels = 2
        elif difficulty <= 6:
            n_levels = 3
        else:
            n_levels = self._rng.randint(4, 5)
        gap = round(self._rng.uniform(0.5e-21, 5.0e-21), 25)
        energies = [i * gap for i in range(n_levels)]
        boltz = [round(math.exp(-e * beta), 4) for e in energies]
        z_val = round(sum(boltz), 4)
        return "Z = \\sum_i e^{-E_i / k_B T}", {
            "T": temp, "beta": beta, "n_levels": n_levels,
            "gap": gap, "energies": energies,
            "boltzmann_factors": boltz, "Z": z_val,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate partition function computation steps.

        Args:
            data: Solution data with energies and Boltzmann factors.

        Returns:
            Steps showing energy levels, exponentials, and sum.
        """
        t = data["T"]
        energies = data["energies"]
        boltz = data["boltzmann_factors"]
        e_strs = [_StatMechFormatter.format_sci(e) for e in energies]
        steps = [f"T = {t} K, k_B = 1.381 \\times 10^{{-23}}"]
        level_str = ", ".join(f"E_{i} = {e_strs[i]}" for i in range(len(energies)))
        steps.append(level_str)
        bf_str = " + ".join(_StatMechFormatter.fmt(b) for b in boltz)
        steps.append(f"Z = {bf_str}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the partition function value.

        Args:
            data: Solution data.

        Returns:
            String representation of Z.
        """
        return f"Z = {_StatMechFormatter.fmt(data['Z'])}"


# ---------------------------------------------------------------------------
# 2. Boltzmann probability  (tier 5)
# ---------------------------------------------------------------------------


@register
class BoltzmannProbabilityGenerator(StepGenerator):
    """Compute Boltzmann occupation probabilities P_i = exp(-E_i/kT) / Z.

    Given energy levels and temperature, computes the probability of
    occupying each state in the canonical ensemble.

    Input format:
        ``compute Boltzmann probabilities``

    Target format:
        ``P_i = e^{-E_i/k_BT} / Z <step>
        Z = ... <step>
        P_0 = 1/Z = ... <step>
        P_1 = e^{-E_1/kT}/Z = ...``

    Difficulty scaling:
        d1-3: 2-level system.
        d4-6: 3-level system.
        d7-8: 4-level system.

    Prerequisites:
        partition_function_stat.
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "boltzmann_probability"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["partition_function_stat"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls number of levels.

        Returns:
            Natural language description.
        """
        return "compute Boltzmann probabilities"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate energy levels and compute occupation probabilities.

        Args:
            difficulty: Controls number of levels.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        temp = self._rng.randint(100, 400 + 100 * difficulty)
        beta = 1.0 / (_K_B * temp)
        if difficulty <= 3:
            n_levels = 2
        elif difficulty <= 6:
            n_levels = 3
        else:
            n_levels = 4
        gap = round(self._rng.uniform(0.5e-21, 4.0e-21), 25)
        energies = [i * gap for i in range(n_levels)]
        boltz = [math.exp(-e * beta) for e in energies]
        z_val = sum(boltz)
        probs = [round(b / z_val, 4) for b in boltz]
        return "P_i = \\frac{e^{-E_i/k_BT}}{Z}", {
            "T": temp, "n_levels": n_levels, "gap": gap,
            "energies": energies, "Z": round(z_val, 4),
            "probs": probs,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Boltzmann probability computation steps.

        Args:
            data: Solution data with Z and probabilities.

        Returns:
            Steps showing Z and each probability.
        """
        steps = [f"T = {data['T']} K"]
        steps.append(f"Z = {_StatMechFormatter.fmt(data['Z'])}")
        for i, p in enumerate(data["probs"]):
            steps.append(f"P_{i} = {_StatMechFormatter.fmt(p)}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the occupation probabilities.

        Args:
            data: Solution data.

        Returns:
            String listing all probabilities.
        """
        parts = [f"P_{i}={_StatMechFormatter.fmt(p)}" for i, p in enumerate(data["probs"])]
        return ", ".join(parts)


# ---------------------------------------------------------------------------
# 3. Average energy  (tier 6)
# ---------------------------------------------------------------------------


@register
class AverageEnergyGenerator(StepGenerator):
    """Compute average energy <E> = sum E_i * P_i = -d(ln Z)/d(beta).

    Computes the ensemble average energy both by direct summation and
    by verifying through the beta derivative of ln Z.

    Input format:
        ``compute average energy``

    Target format:
        ``\\langle E \\rangle = \\sum E_i P_i <step>
        Z = ..., P_i = ... <step>
        \\langle E \\rangle = E_0 P_0 + E_1 P_1 + ... <step>
        = ...``

    Difficulty scaling:
        d1-3: 2-level system.
        d4-6: 3-level system.
        d7-8: 4-level system.

    Prerequisites:
        partition_function_stat.
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "average_energy"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["partition_function_stat"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls number of levels.

        Returns:
            Natural language description.
        """
        return "compute average energy"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate energy levels and compute the average energy.

        Args:
            difficulty: Controls number of levels.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        temp = self._rng.randint(200, 500 + 100 * difficulty)
        beta = 1.0 / (_K_B * temp)
        if difficulty <= 3:
            n = 2
        elif difficulty <= 6:
            n = 3
        else:
            n = 4
        gap = round(self._rng.uniform(1.0e-21, 4.0e-21), 25)
        energies = [i * gap for i in range(n)]
        boltz = [math.exp(-e * beta) for e in energies]
        z_val = sum(boltz)
        probs = [b / z_val for b in boltz]
        avg_e = sum(e * p for e, p in zip(energies, probs))
        terms = [round(e * p, 28) for e, p in zip(energies, probs)]
        return "\\langle E \\rangle = \\sum E_i P_i", {
            "T": temp, "n": n, "gap": gap,
            "energies": energies, "Z": round(z_val, 4),
            "probs": [round(p, 4) for p in probs],
            "terms": terms, "avg_E": avg_e,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate average energy computation steps.

        Args:
            data: Solution data with energies, probabilities, and <E>.

        Returns:
            Steps showing Z, probabilities, and weighted sum.
        """
        steps = [f"T = {data['T']} K, Z = {_StatMechFormatter.fmt(data['Z'])}"]
        prob_str = ", ".join(f"P_{i}={_StatMechFormatter.fmt(p)}" for i, p in enumerate(data["probs"]))
        steps.append(prob_str)
        sum_parts = []
        for i in range(data["n"]):
            e_str = _StatMechFormatter.format_sci(data["energies"][i])
            p_str = _StatMechFormatter.fmt(data["probs"][i])
            sum_parts.append(f"({e_str})({p_str})")
        steps.append(f"\\langle E \\rangle = {' + '.join(sum_parts)}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the average energy.

        Args:
            data: Solution data.

        Returns:
            String representation of <E>.
        """
        return f"\\langle E \\rangle = {_StatMechFormatter.format_sci(data['avg_E'])} J"


# ---------------------------------------------------------------------------
# 4. Fermi-Dirac distribution  (tier 5)
# ---------------------------------------------------------------------------


@register
class FermiDiracGenerator(StepGenerator):
    """Compute Fermi-Dirac occupation: f(E) = 1/(exp((E-mu)/kT) + 1).

    Evaluates the Fermi-Dirac distribution function at a given energy,
    chemical potential, and temperature to find the occupation probability
    for a fermionic state.

    Input format:
        ``compute Fermi-Dirac occupation``

    Target format:
        ``f(E) = \\frac{1}{e^{(E-\\mu)/k_BT} + 1} <step>
        E - \\mu = ... <step>
        (E-\\mu)/k_BT = ... <step>
        e^{...} = ... <step>
        f(E) = 1/(...+1) = ...``

    Difficulty scaling:
        d1-3: E near mu (occupation ~0.5), moderate T.
        d4-6: E above mu (occupation < 0.5).
        d7-8: E far from mu, low T (sharp step).

    Prerequisites:
        exponentiation.
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "fermi_dirac"

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
            difficulty: Controls energy-mu separation.

        Returns:
            Natural language description.
        """
        return "compute Fermi-Dirac occupation"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate E, mu, T and compute the Fermi-Dirac occupation.

        Args:
            difficulty: Controls parameter ranges.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        mu = round(self._rng.uniform(1.0e-19, 5.0e-19), 23)
        if difficulty <= 3:
            temp = self._rng.randint(300, 1000)
            e_val = mu + self._rng.uniform(-0.5e-21, 0.5e-21)
        elif difficulty <= 6:
            temp = self._rng.randint(200, 800)
            e_val = mu + self._rng.uniform(0.5e-21, 3.0e-21)
        else:
            temp = self._rng.randint(50, 300)
            e_val = mu + self._rng.uniform(1.0e-21, 5.0e-21)
        e_val = round(e_val, 23)
        diff = e_val - mu
        kt = _K_B * temp
        exponent = diff / kt
        exp_val = math.exp(min(exponent, 500))
        f_val = round(1.0 / (exp_val + 1.0), 4)
        return "f(E) = \\frac{1}{e^{(E-\\mu)/k_BT} + 1}", {
            "E": e_val, "mu": mu, "T": temp,
            "diff": diff, "kT": kt,
            "exponent": round(exponent, 4),
            "exp_val": round(exp_val, 4),
            "f": f_val,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Fermi-Dirac computation steps.

        Args:
            data: Solution data with E, mu, T, and f(E).

        Returns:
            Steps showing difference, exponent, exponential, and f.
        """
        diff_str = _StatMechFormatter.format_sci(data["diff"])
        kt_str = _StatMechFormatter.format_sci(data["kT"])
        return [
            f"E - \\mu = {diff_str}",
            f"k_BT = {kt_str}",
            f"(E-\\mu)/k_BT = {_StatMechFormatter.fmt(data['exponent'])}",
            f"e^{{{_StatMechFormatter.fmt(data['exponent'])}}} = {_StatMechFormatter.fmt(data['exp_val'])}",
            f"f(E) = 1/({_StatMechFormatter.fmt(data['exp_val'])} + 1)",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the Fermi-Dirac occupation.

        Args:
            data: Solution data.

        Returns:
            String representation of f(E).
        """
        return f"f(E) = {_StatMechFormatter.fmt(data['f'])}"


# ---------------------------------------------------------------------------
# 5. Bose-Einstein distribution  (tier 5)
# ---------------------------------------------------------------------------


@register
class BoseEinsteinGenerator(StepGenerator):
    """Compute Bose-Einstein mean occupation: n(E) = 1/(exp((E-mu)/kT) - 1).

    Evaluates the Bose-Einstein distribution at a given energy, chemical
    potential, and temperature. Ensures E > mu so the occupation is positive.

    Input format:
        ``compute Bose-Einstein occupation``

    Target format:
        ``n(E) = \\frac{1}{e^{(E-\\mu)/k_BT} - 1} <step>
        E - \\mu = ... <step>
        (E-\\mu)/k_BT = ... <step>
        n(E) = ...``

    Difficulty scaling:
        d1-3: moderate E - mu, high T (small occupation).
        d4-6: smaller E - mu (moderate occupation).
        d7-8: E near mu, high T (large occupation).

    Prerequisites:
        exponentiation.
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "bose_einstein"

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
            difficulty: Controls energy-mu separation.

        Returns:
            Natural language description.
        """
        return "compute Bose-Einstein occupation"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate E, mu, T and compute Bose-Einstein mean occupation.

        Args:
            difficulty: Controls parameter ranges.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        mu = round(self._rng.uniform(1.0e-20, 1.0e-19), 23)
        if difficulty <= 3:
            temp = self._rng.randint(500, 2000)
            e_val = mu + self._rng.uniform(2.0e-21, 8.0e-21)
        elif difficulty <= 6:
            temp = self._rng.randint(300, 1000)
            e_val = mu + self._rng.uniform(1.0e-21, 4.0e-21)
        else:
            temp = self._rng.randint(500, 3000)
            e_val = mu + self._rng.uniform(0.5e-21, 2.0e-21)
        e_val = round(e_val, 23)
        diff = e_val - mu
        kt = _K_B * temp
        exponent = diff / kt
        exp_val = math.exp(exponent)
        n_val = round(1.0 / (exp_val - 1.0), 4)
        return "n(E) = \\frac{1}{e^{(E-\\mu)/k_BT} - 1}", {
            "E": e_val, "mu": mu, "T": temp,
            "diff": diff, "kT": kt,
            "exponent": round(exponent, 4),
            "exp_val": round(exp_val, 4),
            "n": n_val,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Bose-Einstein computation steps.

        Args:
            data: Solution data with E, mu, T, and n(E).

        Returns:
            Steps showing difference, exponent, exponential, and n.
        """
        diff_str = _StatMechFormatter.format_sci(data["diff"])
        kt_str = _StatMechFormatter.format_sci(data["kT"])
        return [
            f"E - \\mu = {diff_str}",
            f"k_BT = {kt_str}",
            f"(E-\\mu)/k_BT = {_StatMechFormatter.fmt(data['exponent'])}",
            f"e^{{{_StatMechFormatter.fmt(data['exponent'])}}} = {_StatMechFormatter.fmt(data['exp_val'])}",
            f"n(E) = 1/({_StatMechFormatter.fmt(data['exp_val'])} - 1)",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the Bose-Einstein mean occupation.

        Args:
            data: Solution data.

        Returns:
            String representation of n(E).
        """
        return f"n(E) = {_StatMechFormatter.fmt(data['n'])}"


# ---------------------------------------------------------------------------
# 6. 1D Ising model  (tier 6)
# ---------------------------------------------------------------------------


@register
class IsingModelGenerator(StepGenerator):
    """Compute energy of a 1D Ising chain.

    Calculates H = -J * sum(s_i * s_{i+1}) - h * sum(s_i) for a
    given spin configuration with N spins, coupling J, and external
    field h.

    Input format:
        ``compute Ising model energy``

    Target format:
        ``H = -J\\sum s_i s_{i+1} - h\\sum s_i <step>
        spins: [+1,-1,+1,...] <step>
        \\sum s_i s_{i+1} = ... <step>
        \\sum s_i = ... <step>
        H = ...``

    Difficulty scaling:
        d1-3: 4 spins, h = 0 (no external field).
        d4-6: 5-6 spins with external field.
        d7-8: 7-8 spins with external field.

    Prerequisites:
        summation.
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "ising_model"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["summation"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls chain length and field.

        Returns:
            Natural language description.
        """
        return "compute Ising model energy"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a spin configuration and compute its Ising energy.

        Args:
            difficulty: Controls chain length and external field.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            n_spins = 4
            h = 0
        elif difficulty <= 6:
            n_spins = self._rng.randint(5, 6)
            h = self._rng.randint(1, 3)
        else:
            n_spins = self._rng.randint(7, 8)
            h = self._rng.randint(1, 5)
        j_val = self._rng.randint(1, 3 + difficulty)
        spins = [self._rng.choice([-1, 1]) for _ in range(n_spins)]
        pair_sum = sum(spins[i] * spins[i + 1] for i in range(n_spins - 1))
        mag_sum = sum(spins)
        energy = -j_val * pair_sum - h * mag_sum
        return "H = -J\\sum s_i s_{i+1} - h\\sum s_i", {
            "J": j_val, "h": h, "spins": spins,
            "pair_sum": pair_sum, "mag_sum": mag_sum,
            "H": energy,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Ising energy computation steps.

        Args:
            data: Solution data with spins and sums.

        Returns:
            Steps showing spin config, pair sum, magnetisation, and H.
        """
        spin_str = "[" + ",".join(f"{s:+d}" for s in data["spins"]) + "]"
        steps = [
            f"spins: {spin_str}, J={data['J']}, h={data['h']}",
            f"\\sum s_i s_{{i+1}} = {data['pair_sum']}",
            f"\\sum s_i = {data['mag_sum']}",
            f"H = -({data['J']})({data['pair_sum']}) - ({data['h']})({data['mag_sum']})",
        ]
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the Ising energy.

        Args:
            data: Solution data.

        Returns:
            String representation of H.
        """
        return f"H = {data['H']}"


# ---------------------------------------------------------------------------
# 7. Statistical entropy  (tier 5)
# ---------------------------------------------------------------------------


@register
class EntropyStatMechGenerator(StepGenerator):
    """Compute entropy from microstates: S = k_B * ln(Omega).

    Given the number of microstates Omega for a system, computes
    the Boltzmann entropy. Uses systems with known microstate counts
    (coin flips, identical particles in boxes, spin systems).

    Input format:
        ``compute statistical entropy``

    Target format:
        ``S = k_B \\ln(\\Omega) <step>
        \\Omega = ... <step>
        \\ln(\\Omega) = ... <step>
        S = (1.381 \\times 10^{-23})(...) = ... J/K``

    Difficulty scaling:
        d1-3: Omega from small combinatorics (10-100).
        d4-6: Omega from moderate combinatorics (100-10000).
        d7-8: Omega from large combinatorics (10^4 - 10^8).

    Prerequisites:
        logarithm.
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "entropy_stat_mech"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["logarithm"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls microstate count.

        Returns:
            Natural language description.
        """
        return "compute statistical entropy"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a microstate count and compute entropy.

        Args:
            difficulty: Controls magnitude of Omega.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            omega = self._rng.randint(10, 100)
        elif difficulty <= 6:
            omega = self._rng.randint(100, 10000)
        else:
            exponent = self._rng.randint(4, 8)
            omega = self._rng.randint(1, 9) * (10 ** exponent)
        ln_omega = round(math.log(omega), 4)
        entropy = _K_B * ln_omega
        return "S = k_B \\ln(\\Omega)", {
            "omega": omega, "ln_omega": ln_omega,
            "S": entropy,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate entropy computation steps.

        Args:
            data: Solution data with Omega and entropy.

        Returns:
            Steps showing Omega, ln(Omega), and S.
        """
        return [
            f"\\Omega = {data['omega']}",
            f"\\ln({data['omega']}) = {_StatMechFormatter.fmt(data['ln_omega'])}",
            f"S = (1.381 \\times 10^{{-23}})({_StatMechFormatter.fmt(data['ln_omega'])})",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the entropy.

        Args:
            data: Solution data.

        Returns:
            String representation of S.
        """
        return f"S = {_StatMechFormatter.format_sci(data['S'])} J/K"


# ---------------------------------------------------------------------------
# 8. Equipartition theorem  (tier 5)
# ---------------------------------------------------------------------------


@register
class EquipartitionGenerator(StepGenerator):
    """Apply the equipartition theorem: E = (f/2) * k_B * T.

    Counts degrees of freedom for different molecular types
    (monatomic gas, diatomic gas, solid) and computes the
    average thermal energy per molecule.

    Input format:
        ``apply equipartition theorem``

    Target format:
        ``E = \\frac{f}{2} k_B T <step>
        molecule type: diatomic <step>
        f = 5 (3 trans + 2 rot) <step>
        E = (5/2)(1.381e-23)(T) = ...``

    Difficulty scaling:
        d1-3: monatomic (f = 3).
        d4-6: diatomic (f = 5 or 7 with vibration).
        d7-8: solid (f = 6).

    Prerequisites:
        multiplication.
    """

    _SYSTEMS = {
        "monatomic": (3, "3 translational"),
        "diatomic_no_vib": (5, "3 trans + 2 rot"),
        "diatomic_vib": (7, "3 trans + 2 rot + 2 vib"),
        "solid": (6, "6 (3 KE + 3 PE)"),
    }

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "equipartition"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["multiplication"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls molecular type.

        Returns:
            Natural language description.
        """
        return "apply equipartition theorem"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a molecular system and compute thermal energy.

        Args:
            difficulty: Controls molecular type.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        temp = self._rng.randint(100, 500 + 100 * difficulty)
        if difficulty <= 3:
            sys_key = "monatomic"
        elif difficulty <= 5:
            sys_key = "diatomic_no_vib"
        elif difficulty <= 6:
            sys_key = "diatomic_vib"
        else:
            sys_key = "solid"
        f_dof, description = self._SYSTEMS[sys_key]
        energy = f_dof / 2.0 * _K_B * temp
        return "E = \\frac{f}{2} k_B T", {
            "system": sys_key, "f": f_dof,
            "dof_desc": description, "T": temp,
            "E": energy,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate equipartition computation steps.

        Args:
            data: Solution data with dof and energy.

        Returns:
            Steps showing system type, dof count, and energy.
        """
        f = data["f"]
        t = data["T"]
        return [
            f"type: {data['system'].replace('_', ' ')}",
            f"f = {f} ({data['dof_desc']})",
            f"E = ({f}/2)(1.381 \\times 10^{{-23}})({t})",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the thermal energy per molecule.

        Args:
            data: Solution data.

        Returns:
            String representation of E.
        """
        return f"E = {_StatMechFormatter.format_sci(data['E'])} J"


# ---------------------------------------------------------------------------
# 9. Specific heat  (tier 6)
# ---------------------------------------------------------------------------


@register
class SpecificHeatGenerator(StepGenerator):
    """Compute specific heat C_V = dE/dT from an energy expression.

    Uses the Einstein model for solids: C_V = 3Nk_B * (theta_E/T)^2 *
    exp(theta_E/T) / (exp(theta_E/T) - 1)^2, where theta_E is the
    Einstein temperature. Also handles ideal gas cases.

    Input format:
        ``compute specific heat``

    Target format:
        ``C_V = dE/dT <step>
        \\theta_E/T = ... <step>
        x = \\theta_E/T, e^x = ... <step>
        C_V = 3Nk_B x^2 e^x / (e^x - 1)^2 = ...``

    Difficulty scaling:
        d1-3: ideal gas C_V = (f/2)*Nk_B.
        d4-6: Einstein solid at high T (classical limit).
        d7-8: Einstein solid at low T (quantum regime).

    Prerequisites:
        average_energy.
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "specific_heat"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["average_energy"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls model type.

        Returns:
            Natural language description.
        """
        return "compute specific heat"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate system parameters and compute C_V.

        Args:
            difficulty: Controls model (ideal gas vs Einstein solid).

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        n_atoms = self._rng.randint(1, 5)
        if difficulty <= 3:
            return self._ideal_gas(difficulty, n_atoms)
        return self._einstein_solid(difficulty, n_atoms)

    def _ideal_gas(self, difficulty: int, n: int) -> tuple[str, dict]:
        """Compute specific heat for an ideal gas.

        Args:
            difficulty: Controls molecular type.
            n: Number of moles (treated as number of molecules here).

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        f = self._rng.choice([3, 5])
        cv = f / 2.0 * n * _K_B
        return "C_V = \\frac{f}{2} N k_B", {
            "model": "ideal_gas", "f": f, "N": n,
            "C_V": cv,
        }

    def _einstein_solid(self, difficulty: int, n: int) -> tuple[str, dict]:
        """Compute specific heat using the Einstein model.

        Args:
            difficulty: Controls temperature regime.
            n: Number of atoms.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        theta_e = self._rng.randint(100, 500)
        if difficulty <= 6:
            temp = self._rng.randint(theta_e, 3 * theta_e)
        else:
            temp = self._rng.randint(max(10, theta_e // 5), theta_e // 2)
        x = theta_e / temp
        exp_x = math.exp(x)
        cv_factor = x * x * exp_x / ((exp_x - 1.0) ** 2)
        cv = round(3 * n * _K_B * cv_factor, 28)
        return "C_V = 3Nk_B (\\theta_E/T)^2 e^{\\theta_E/T}/(e^{\\theta_E/T}-1)^2", {
            "model": "einstein", "N": n, "theta_E": theta_e,
            "T": temp, "x": round(x, 4),
            "exp_x": round(exp_x, 4),
            "cv_factor": round(cv_factor, 4),
            "C_V": cv,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate specific heat computation steps.

        Args:
            data: Solution data with model parameters and C_V.

        Returns:
            Steps showing model, parameters, and C_V.
        """
        if data["model"] == "ideal_gas":
            return [
                f"ideal gas: f = {data['f']}, N = {data['N']}",
                f"C_V = ({data['f']}/2)({data['N']})(1.381 \\times 10^{{-23}})",
            ]
        return [
            f"Einstein solid: N={data['N']}, \\theta_E={data['theta_E']} K, T={data['T']} K",
            f"x = \\theta_E/T = {_StatMechFormatter.fmt(data['x'])}",
            f"e^x = {_StatMechFormatter.fmt(data['exp_x'])}",
            f"C_V factor = x^2 e^x/(e^x-1)^2 = {_StatMechFormatter.fmt(data['cv_factor'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the specific heat.

        Args:
            data: Solution data.

        Returns:
            String representation of C_V.
        """
        return f"C_V = {_StatMechFormatter.format_sci(data['C_V'])} J/K"


# ---------------------------------------------------------------------------
# 10. Grand canonical ensemble  (tier 7)
# ---------------------------------------------------------------------------


@register
class GrandCanonicalGenerator(StepGenerator):
    """Compute the grand partition function Xi = sum_N z^N * Z_N.

    For simple systems where the canonical partition function Z_N is
    known analytically, computes the grand partition function using
    the fugacity z = exp(mu / kT).

    Input format:
        ``compute grand partition function``

    Target format:
        ``\\Xi = \\sum_N z^N Z_N <step>
        z = e^{\\mu/k_BT} = ... <step>
        Z_0 = 1, Z_1 = ..., Z_2 = ... <step>
        \\Xi = z^0 Z_0 + z^1 Z_1 + z^2 Z_2 + ... = ...``

    Difficulty scaling:
        d1-3: single-site system (N = 0 or 1), Z_N simple.
        d4-6: up to N = 3 particles.
        d7-8: up to N = 4 particles with energy gaps.

    Prerequisites:
        partition_function_stat.
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "grand_canonical"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["partition_function_stat"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls maximum particle number.

        Returns:
            Natural language description.
        """
        return "compute grand partition function"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate canonical Z_N values and compute grand partition function.

        Args:
            difficulty: Controls maximum N.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        temp = self._rng.randint(200, 600 + 100 * difficulty)
        mu = round(self._rng.uniform(-3.0e-21, -0.5e-21), 24)
        kt = _K_B * temp
        z_fugacity = round(math.exp(mu / kt), 4)
        if difficulty <= 3:
            n_max = 1
        elif difficulty <= 6:
            n_max = 3
        else:
            n_max = 4
        gap = round(self._rng.uniform(0.5e-21, 3.0e-21), 24)
        z_n_list = []
        for n in range(n_max + 1):
            if n == 0:
                z_n_list.append(1.0)
            else:
                e_n = n * gap
                z_n = round(math.exp(-e_n / kt), 4)
                z_n_list.append(z_n)
        terms = []
        for n in range(n_max + 1):
            term = round((z_fugacity ** n) * z_n_list[n], 4)
            terms.append(term)
        xi = round(sum(terms), 4)
        return "\\Xi = \\sum_N z^N Z_N", {
            "T": temp, "mu": mu, "kT": kt,
            "z": z_fugacity, "n_max": n_max,
            "Z_N": [round(zn, 4) for zn in z_n_list],
            "terms": terms, "Xi": xi,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate grand partition function computation steps.

        Args:
            data: Solution data with fugacity, Z_N, and Xi.

        Returns:
            Steps showing fugacity, Z_N values, and sum.
        """
        steps = [f"T = {data['T']} K, z = e^{{\\mu/k_BT}} = {_StatMechFormatter.fmt(data['z'])}"]
        zn_str = ", ".join(f"Z_{n}={_StatMechFormatter.fmt(zn)}" for n, zn in enumerate(data["Z_N"]))
        steps.append(zn_str)
        term_parts = []
        for n, t in enumerate(data["terms"]):
            term_parts.append(f"z^{n} Z_{n} = {_StatMechFormatter.fmt(t)}")
        steps.append("; ".join(term_parts))
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the grand partition function.

        Args:
            data: Solution data.

        Returns:
            String representation of Xi.
        """
        return f"\\Xi = {_StatMechFormatter.fmt(data['Xi'])}"
