"""Extended science generators — Kirchhoff circuits, astrophysics, probability, statistics, and CS.

Adds missing generators for Kirchhoff loop/junction rules (tier 5), Hubble's
law (tier 5), distance modulus (tier 6), gravitational lensing (tier 6),
Poisson distribution (tier 5), variance of distribution (tier 4), total
probability (tier 4), independence test (tier 3), hypothesis testing (tier 5),
confidence intervals (tier 5), algorithmic complexity (tier 4), 1D convolution
(tier 5), and polynomial hashing (tier 5).
"""
import math
from fractions import Fraction

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register
from engram_generator.generators.applied_math import PhysicsParameterSampler
from engram_generator.generators.physics import ScientificFormatter
from engram_generator.generators.statistics import FractionFormatter


class CircuitBuilder:
    """Builds simple resistor circuits for Kirchhoff law problems.

    Generates series/parallel resistor networks with a voltage source
    and computes branch currents using Kirchhoff's voltage and current
    laws.

    Example:
        >>> import random
        >>> rng = random.Random(42)
        >>> cb = CircuitBuilder(rng)
        >>> data = cb.build_series(3, 12)
        >>> data["total_r"] > 0
        True
    """

    def __init__(self, rng: "random.Random") -> None:
        """Initialise with a random number generator.

        Args:
            rng: Seeded Random instance.
        """
        self._rng = rng

    def build_series(self, difficulty: int,
                     voltage: int) -> dict:
        """Build a series circuit with 2-4 resistors.

        Args:
            difficulty: Controls number of resistors and values.
            voltage: Source voltage in volts.

        Returns:
            Dict with resistors, total_r, current, and voltage drops.
        """
        n = min(2 + difficulty // 3, 4)
        resistors = [
            self._rng.randint(1, 5 * max(1, difficulty))
            for _ in range(n)
        ]
        total_r = sum(resistors)
        current = Fraction(voltage, total_r)
        drops = [Fraction(r) * current for r in resistors]
        return {
            "resistors": resistors,
            "total_r": total_r,
            "current": current,
            "drops": drops,
            "voltage": voltage,
        }

    def build_parallel(self, difficulty: int,
                       voltage: int) -> dict:
        """Build a parallel circuit with 2-3 resistors.

        Args:
            difficulty: Controls number of resistors and values.
            voltage: Source voltage in volts.

        Returns:
            Dict with resistors, branch currents, and total current.
        """
        n = min(2 + difficulty // 4, 3)
        resistors = [
            self._rng.randint(2, 5 * max(1, difficulty))
            for _ in range(n)
        ]
        branch_currents = [Fraction(voltage, r) for r in resistors]
        total_current = sum(branch_currents)
        return {
            "resistors": resistors,
            "branch_currents": branch_currents,
            "total_current": total_current,
            "voltage": voltage,
        }


class ComplexityClassifier:
    """Classifies algorithmic complexity from template descriptions.

    Provides a pool of algorithm descriptions with known Big-O
    complexities, organised by difficulty level.

    Example:
        >>> import random
        >>> cc = ComplexityClassifier(random.Random(42))
        >>> desc, answer = cc.sample(1)
        >>> answer in ["O(1)", "O(n)", "O(n^2)", "O(log n)"]
        True
    """

    _EASY_ALGORITHMS: list[tuple[str, str]] = [
        ("access array element by index", "O(1)"),
        ("linear search through unsorted array", "O(n)"),
        ("sum all elements in array", "O(n)"),
        ("find maximum in unsorted array", "O(n)"),
        ("binary search in sorted array", "O(log n)"),
    ]

    _MEDIUM_ALGORITHMS: list[tuple[str, str]] = [
        ("bubble sort", "O(n^2)"),
        ("selection sort", "O(n^2)"),
        ("insertion sort", "O(n^2)"),
        ("merge sort", "O(n log n)"),
        ("check all pairs in array", "O(n^2)"),
        ("binary search tree lookup (balanced)", "O(log n)"),
    ]

    _HARD_ALGORITHMS: list[tuple[str, str]] = [
        ("matrix multiplication (naive)", "O(n^3)"),
        ("generate all subsets of a set", "O(2^n)"),
        ("generate all permutations", "O(n!)"),
        ("heap sort", "O(n log n)"),
        ("hash table lookup (average)", "O(1)"),
        ("BFS or DFS graph traversal", "O(V+E)"),
    ]

    def __init__(self, rng: "random.Random") -> None:
        """Initialise with a random number generator.

        Args:
            rng: Seeded Random instance.
        """
        self._rng = rng

    def sample(self, difficulty: int) -> tuple[str, str]:
        """Sample an algorithm description and its complexity.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (description, complexity_class).
        """
        pool = self._select_pool(difficulty)
        return self._rng.choice(pool)

    def _select_pool(self, difficulty: int) -> list[tuple[str, str]]:
        """Select algorithm pool based on difficulty.

        Args:
            difficulty: Difficulty level.

        Returns:
            List of (description, complexity) tuples.
        """
        if difficulty <= 3:
            return self._EASY_ALGORITHMS
        if difficulty <= 6:
            return self._EASY_ALGORITHMS + self._MEDIUM_ALGORITHMS
        return (
            self._EASY_ALGORITHMS
            + self._MEDIUM_ALGORITHMS
            + self._HARD_ALGORITHMS
        )


@register
class KirchhoffGenerator(StepGenerator):
    """Kirchhoff loop and junction rules for resistor circuits.

    Generates series or parallel circuits with a voltage source and
    multiple resistors. Applies Kirchhoff's voltage law (loop rule)
    for series circuits and Kirchhoff's current law (junction rule)
    for parallel circuits.

    Input format:
        ``apply kirchhoff rules to circuit``

    Target format:
        ``V=12, R_1=3, R_2=4, R_3=5 (series) <step>
        R_{total}=3+4+5=12 <step> I=V/R=12/12=1 <step>
        V_1=1*3=3 <step> V_2=1*4=4 <step> V_3=1*5=5 <step>
        I=1, V_1=3, V_2=4, V_3=5``

    Difficulty scaling:
        Difficulty 1-4: series circuits with 2-3 resistors.
        Difficulty 5-8: parallel circuits with 2-3 resistors.

    Prerequisites:
        system_equations, ohms_law.

    Example:
        >>> gen = KirchhoffGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'kirchhoff'
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "kirchhoff"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["system_equations", "ohms_law"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls circuit complexity.

        Returns:
            Natural language description.
        """
        return "apply kirchhoff rules to circuit"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a circuit and compute currents/voltages.

        Args:
            difficulty: Controls circuit type and complexity.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        sampler = PhysicsParameterSampler(self._rng)
        voltage = sampler.sample(difficulty, 6, 24)
        builder = CircuitBuilder(self._rng)

        if difficulty <= 4:
            return self._series_problem(builder, difficulty, voltage)
        return self._parallel_problem(builder, difficulty, voltage)

    def _series_problem(self, builder: CircuitBuilder,
                        difficulty: int,
                        voltage: int) -> tuple[str, dict]:
        """Build a series circuit problem.

        Args:
            builder: Circuit builder instance.
            difficulty: Controls complexity.
            voltage: Source voltage.

        Returns:
            Tuple of (problem_string, solution_data).
        """
        data = builder.build_series(difficulty, voltage)
        resistors = data["resistors"]
        r_labels = ", ".join(
            f"R_{{{i+1}}}={r}" for i, r in enumerate(resistors)
        )
        problem = f"V={voltage}, {r_labels} (series)"
        data["circuit_type"] = "series"
        return problem, data

    def _parallel_problem(self, builder: CircuitBuilder,
                          difficulty: int,
                          voltage: int) -> tuple[str, dict]:
        """Build a parallel circuit problem.

        Args:
            builder: Circuit builder instance.
            difficulty: Controls complexity.
            voltage: Source voltage.

        Returns:
            Tuple of (problem_string, solution_data).
        """
        data = builder.build_parallel(difficulty, voltage)
        resistors = data["resistors"]
        r_labels = ", ".join(
            f"R_{{{i+1}}}={r}" for i, r in enumerate(resistors)
        )
        problem = f"V={voltage}, {r_labels} (parallel)"
        data["circuit_type"] = "parallel"
        return problem, data

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Kirchhoff law computation steps.

        Args:
            data: Solution data with circuit information.

        Returns:
            Steps showing the application of loop or junction rules.
        """
        if data["circuit_type"] == "series":
            return self._series_steps(data)
        return self._parallel_steps(data)

    def _series_steps(self, data: dict) -> list[str]:
        """Generate steps for a series circuit.

        Args:
            data: Solution data.

        Returns:
            Steps showing total resistance, current, and voltage drops.
        """
        fmt = FractionFormatter()
        resistors = data["resistors"]
        total_r = data["total_r"]
        current = data["current"]
        drops = data["drops"]

        r_sum = "+".join(str(r) for r in resistors)
        steps = [
            f"R_{{total}}={r_sum}={total_r}",
            f"I=V/R={data['voltage']}/{total_r}={fmt.format(current)}",
        ]
        for i, (r, drop) in enumerate(zip(resistors, drops)):
            steps.append(
                f"V_{{{i+1}}}={fmt.format(current)}*{r}={fmt.format(drop)}"
            )
        return steps

    def _parallel_steps(self, data: dict) -> list[str]:
        """Generate steps for a parallel circuit.

        Args:
            data: Solution data.

        Returns:
            Steps showing branch currents and total current.
        """
        fmt = FractionFormatter()
        resistors = data["resistors"]
        branch_currents = data["branch_currents"]
        total_current = data["total_current"]
        voltage = data["voltage"]

        steps = []
        for i, (r, curr) in enumerate(zip(resistors, branch_currents)):
            steps.append(
                f"I_{{{i+1}}}=V/R_{{{i+1}}}={voltage}/{r}={fmt.format(curr)}"
            )
        parts = "+".join(fmt.format(c) for c in branch_currents)
        steps.append(f"I_{{total}}={parts}={fmt.format(total_current)}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the circuit solution summary.

        Args:
            data: Solution data.

        Returns:
            Summary of currents and voltage drops.
        """
        fmt = FractionFormatter()
        if data["circuit_type"] == "series":
            current = fmt.format(data["current"])
            drops = ", ".join(
                f"V_{{{i+1}}}={fmt.format(d)}"
                for i, d in enumerate(data["drops"])
            )
            return f"I={current}, {drops}"
        parts = ", ".join(
            f"I_{{{i+1}}}={fmt.format(c)}"
            for i, c in enumerate(data["branch_currents"])
        )
        total = fmt.format(data["total_current"])
        return f"{parts}, I_total={total}"


@register
class HubbleLawGenerator(StepGenerator):
    """Hubble's law v = H_0 * d for galaxy recession velocity.

    Computes recession velocity from the Hubble constant H_0 = 70
    km/s/Mpc and distance d in megaparsecs. Shows direct
    multiplication with unit conversion.

    Input format:
        ``apply hubble law``

    Target format:
        ``v = H_0 d <step> v = (70)(150) <step> v = 10500 km/s``

    Difficulty scaling:
        Difficulty 1-3: d in [10, 100] Mpc.
        Difficulty 4-6: d in [100, 1000] Mpc.
        Difficulty 7-8: d in [1000, 5000] Mpc.

    Prerequisites:
        multiplication.

    Example:
        >>> gen = HubbleLawGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'hubble_law'
    """

    _H0 = 70

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "hubble_law"

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
            difficulty: Controls distance scale.

        Returns:
            Natural language description.
        """
        return "apply hubble law"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate distance and compute recession velocity.

        Args:
            difficulty: Controls distance scale.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        d = self._sample_distance(difficulty)
        v = self._H0 * d
        return "v = H_0 d", {"H0": self._H0, "d": d, "v": v}

    def _sample_distance(self, difficulty: int) -> int:
        """Sample distance in Mpc based on difficulty.

        Args:
            difficulty: Difficulty level.

        Returns:
            Distance in megaparsecs.
        """
        if difficulty <= 3:
            return self._rng.randint(10, 100)
        if difficulty <= 6:
            return self._rng.randint(100, 1000)
        return self._rng.randint(1000, 5000)

    def _create_steps(self, data: dict) -> list[str]:
        """Generate multiplication steps.

        Args:
            data: Solution data with H0, d, and v.

        Returns:
            Steps showing the substitution and computation.
        """
        return [
            f"v = ({data['H0']})({data['d']})",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the recession velocity.

        Args:
            data: Solution data.

        Returns:
            String representation of v with units.
        """
        return f"v = {data['v']} km/s"


@register
class MagnitudeDistanceGenerator(StepGenerator):
    """Distance modulus m - M = 5 * log10(d/10).

    Computes the apparent magnitude m from absolute magnitude M and
    distance d in parsecs using the distance modulus formula.

    Input format:
        ``compute distance modulus``

    Target format:
        ``m - M = 5 \\log_{10}(d/10) <step> d/10 = 500/10 = 50
        <step> \\log_{10}(50) = 1.699 <step> 5(1.699) = 8.495
        <step> m = M + 8.495 = -2 + 8.495 = 6.495``

    Difficulty scaling:
        Difficulty 1-3: d in [10, 500] pc, M in [-2, 5].
        Difficulty 4-6: d in [100, 5000] pc, M in [-5, 5].
        Difficulty 7-8: d in [1000, 50000] pc, M in [-10, 5].

    Prerequisites:
        division, multiplication.

    Example:
        >>> gen = MagnitudeDistanceGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'magnitude_distance'
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "magnitude_distance"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["division", "multiplication"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls distance and magnitude ranges.

        Returns:
            Natural language description.
        """
        return "compute distance modulus"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate distance and absolute magnitude, then compute apparent magnitude.

        Args:
            difficulty: Controls distance scale.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        d, big_m = self._sample_parameters(difficulty)
        d_over_10 = d / 10
        log_val = round(math.log10(d_over_10), 4)
        modulus = round(5 * log_val, 4)
        apparent = round(big_m + modulus, 4)

        return "m - M = 5 \\log_{10}(d/10)", {
            "d": d, "M": big_m, "d_over_10": d_over_10,
            "log_val": log_val, "modulus": modulus, "apparent": apparent,
        }

    def _sample_parameters(self, difficulty: int) -> tuple[int, int]:
        """Sample distance and absolute magnitude.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (distance_pc, absolute_magnitude).
        """
        if difficulty <= 3:
            d = self._rng.randint(10, 500)
            big_m = self._rng.randint(-2, 5)
        elif difficulty <= 6:
            d = self._rng.randint(100, 5000)
            big_m = self._rng.randint(-5, 5)
        else:
            d = self._rng.randint(1000, 50000)
            big_m = self._rng.randint(-10, 5)
        return d, big_m

    def _create_steps(self, data: dict) -> list[str]:
        """Generate distance modulus computation steps.

        Args:
            data: Solution data with d, M, and intermediates.

        Returns:
            Steps showing division, log, and magnitude calculation.
        """
        d = data["d"]
        d10 = ScientificFormatter.format_value(data["d_over_10"])
        log_val = data["log_val"]
        modulus = data["modulus"]
        big_m = data["M"]

        return [
            f"d/10 = {d}/10 = {d10}",
            f"\\log_{{10}}({d10}) = {log_val}",
            f"5({log_val}) = {modulus}",
            f"m = M + {modulus} = {big_m} + {modulus} = {data['apparent']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the apparent magnitude.

        Args:
            data: Solution data.

        Returns:
            String representation of m.
        """
        return f"m = {data['apparent']}"


@register
class GravitationalLensingGenerator(StepGenerator):
    """Gravitational lensing deflection angle theta = 4GM/(c^2 * b).

    Computes the deflection angle for light passing at impact
    parameter b from a mass M using general relativity's prediction.
    Uses G = 6.674e-11 and c = 2.998e8 m/s.

    Input format:
        ``compute gravitational lensing angle``

    Target format:
        ``\\theta = \\frac{4GM}{c^2 b} <step>
        4GM = 4(6.674e-11)(1.989e30) = 5.309e20 <step>
        c^2 b = (8.988e16)(1e11) = 8.988e27 <step>
        \\theta = 5.309e20 / 8.988e27 = 5.907e-8 rad``

    Difficulty scaling:
        Difficulty 1-3: solar mass, b ~ 10^9 m.
        Difficulty 4-6: 10-100 solar masses, b ~ 10^10 m.
        Difficulty 7-8: 10^6 solar masses, b ~ 10^15 m.

    Prerequisites:
        gravitational_force.

    Example:
        >>> gen = GravitationalLensingGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'gravitational_lensing'
    """

    _G = 6.674e-11
    _C = 2.998e8
    _SOLAR_MASS = 1.989e30

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "gravitational_lensing"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["gravitational_force"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls mass and impact parameter scales.

        Returns:
            Natural language description.
        """
        return "compute gravitational lensing angle"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate mass and impact parameter, then compute deflection angle.

        Args:
            difficulty: Controls parameter scales.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        mass, b = self._sample_parameters(difficulty)
        four_gm = 4 * self._G * mass
        c_sq_b = self._C ** 2 * b
        theta = four_gm / c_sq_b

        return "\\theta = \\frac{4GM}{c^2 b}", {
            "M": mass, "b": b, "four_gm": four_gm,
            "c_sq_b": c_sq_b, "theta": theta,
        }

    def _sample_parameters(self, difficulty: int) -> tuple[float, float]:
        """Sample mass and impact parameter based on difficulty.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (mass_kg, impact_parameter_m).
        """
        if difficulty <= 3:
            mass = float(self._rng.randint(1, 5)) * self._SOLAR_MASS
            b = float(self._rng.randint(1, 9)) * 1e9
        elif difficulty <= 6:
            mass = float(self._rng.randint(10, 100)) * self._SOLAR_MASS
            b = float(self._rng.randint(1, 9)) * 1e10
        else:
            mass = float(self._rng.randint(1, 9)) * 1e6 * self._SOLAR_MASS
            b = float(self._rng.randint(1, 9)) * 1e15
        return mass, b

    def _create_steps(self, data: dict) -> list[str]:
        """Generate lensing angle computation steps.

        Args:
            data: Solution data with mass, impact parameter, and angle.

        Returns:
            Steps showing 4GM, c^2*b, and division.
        """
        fmt = ScientificFormatter
        g_str = fmt.format_sci(self._G)
        m_str = fmt.format_sci(data["M"])
        b_str = fmt.format_sci(data["b"])
        four_gm_str = fmt.format_sci(data["four_gm"])
        c_sq_b_str = fmt.format_sci(data["c_sq_b"])

        return [
            f"4GM = 4({g_str})({m_str}) = {four_gm_str}",
            f"c^2 b = ({fmt.format_sci(self._C ** 2)})({b_str}) = {c_sq_b_str}",
            f"\\theta = {four_gm_str} / {c_sq_b_str}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the deflection angle.

        Args:
            data: Solution data.

        Returns:
            String representation of theta with units.
        """
        return f"\\theta = {ScientificFormatter.format_sci(data['theta'])} rad"


@register
class PoissonDistGenerator(StepGenerator):
    """Poisson distribution P(X=k) = lambda^k * e^{-lambda} / k!.

    Computes the probability of observing exactly k events when the
    average rate is lambda, using the Poisson probability mass function.

    Input format:
        ``compute poisson probability``

    Target format:
        ``P(X=3), \\lambda=2 <step> \\lambda^k = 2^3 = 8
        <step> e^{-\\lambda} = e^{-2} = 0.1353
        <step> k! = 3! = 6 <step> P = 8 * 0.1353 / 6 = 0.1804 <step> 0.1804``

    Difficulty scaling:
        Difficulty 1-3: lambda in [1, 3], k in [0, 4].
        Difficulty 4-6: lambda in [2, 6], k in [0, 7].
        Difficulty 7-8: lambda in [3, 10], k in [0, 10].

    Prerequisites:
        exponentiation, division.

    Example:
        >>> gen = PoissonDistGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'poisson_dist'
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "poisson_dist"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["exponentiation", "division"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls lambda and k ranges.

        Returns:
            Natural language description.
        """
        return "compute poisson probability"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate lambda and k, then compute Poisson probability.

        Args:
            difficulty: Controls parameter ranges.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        lam, k = self._sample_parameters(difficulty)
        lam_k = lam ** k
        exp_neg_lam = round(math.exp(-lam), 4)
        k_fact = math.factorial(k)
        prob = round(lam_k * exp_neg_lam / k_fact, 4)

        return f"P(X={k}), \\lambda={lam}", {
            "lam": lam, "k": k, "lam_k": lam_k,
            "exp_neg_lam": exp_neg_lam, "k_fact": k_fact, "prob": prob,
        }

    def _sample_parameters(self, difficulty: int) -> tuple[int, int]:
        """Sample lambda and k based on difficulty.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (lambda, k).
        """
        if difficulty <= 3:
            lam = self._rng.randint(1, 3)
            k = self._rng.randint(0, 4)
        elif difficulty <= 6:
            lam = self._rng.randint(2, 6)
            k = self._rng.randint(0, 7)
        else:
            lam = self._rng.randint(3, 10)
            k = self._rng.randint(0, 10)
        return lam, k

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Poisson probability computation steps.

        Args:
            data: Solution data with lambda, k, and intermediates.

        Returns:
            Steps showing lambda^k, e^{-lambda}, k!, and final probability.
        """
        lam = data["lam"]
        k = data["k"]
        return [
            f"\\lambda^k = {lam}^{k} = {data['lam_k']}",
            f"e^{{-\\lambda}} = e^{{-{lam}}} = {data['exp_neg_lam']}",
            f"k! = {k}! = {data['k_fact']}",
            f"P = {data['lam_k']} * {data['exp_neg_lam']} / {data['k_fact']} = {data['prob']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the Poisson probability.

        Args:
            data: Solution data.

        Returns:
            String representation of the probability.
        """
        return str(data["prob"])


@register
class VarianceDistGenerator(StepGenerator):
    """Variance of a distribution Var(X) = E[X^2] - (E[X])^2.

    Computes the variance of a discrete probability distribution using
    the computational formula: first compute E[X] and E[X^2], then
    subtract the square of E[X] from E[X^2].

    Input format:
        ``compute distribution variance``

    Target format:
        ``X: (1,1/3),(2,1/3),(4,1/3) <step>
        E[X]=1(1/3)+2(1/3)+4(1/3)=7/3 <step>
        E[X^2]=1(1/3)+4(1/3)+16(1/3)=21/3=7 <step>
        Var=7-(7/3)^2=7-49/9=14/9 <step> 14/9``

    Difficulty scaling:
        Difficulty 1-3: 2-3 outcomes, values 1-6.
        Difficulty 4-6: 3-4 outcomes, values 1-10.
        Difficulty 7-8: 4-5 outcomes, values 1-20.

    Prerequisites:
        expected_value, exponentiation.

    Example:
        >>> gen = VarianceDistGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'variance_dist'
    """

    def __init__(self, **kwargs) -> None:
        """Initialise with fraction formatter.

        Args:
            **kwargs: Passed to parent constructor.
        """
        super().__init__(**kwargs)
        self._fmt = FractionFormatter()

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "variance_dist"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["expected_value", "exponentiation"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls outcome count.

        Returns:
            Natural language description.
        """
        return "compute distribution variance"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a distribution and compute its variance.

        Args:
            difficulty: Controls outcome count and value range.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        n, val_hi = self._params(difficulty)
        values = self._distinct_values(n, 1, val_hi)
        probs = self._make_distribution(n)
        ex = sum(Fraction(v) * p for v, p in zip(values, probs))
        ex2 = sum(Fraction(v * v) * p for v, p in zip(values, probs))
        variance = ex2 - ex * ex

        pairs = ",".join(
            f"({v},{self._fmt.format(p)})"
            for v, p in zip(values, probs)
        )
        return f"X: {pairs}", {
            "values": values, "probs": probs,
            "ex": ex, "ex2": ex2, "variance": variance,
        }

    def _params(self, difficulty: int) -> tuple[int, int]:
        """Map difficulty to outcome count and value range.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (num_outcomes, max_value).
        """
        if difficulty <= 3:
            return self._rng.randint(2, 3), 6
        if difficulty <= 6:
            return self._rng.randint(3, 4), 10
        return self._rng.randint(4, 5), 20

    def _distinct_values(self, n: int, lo: int, hi: int) -> list[int]:
        """Generate n distinct sorted values in [lo, hi].

        Args:
            n: Number of distinct values.
            lo: Lower bound.
            hi: Upper bound.

        Returns:
            Sorted list of distinct integers.
        """
        pool = list(range(lo, hi + 1))
        self._rng.shuffle(pool)
        return sorted(pool[:n])

    def _make_distribution(self, n: int) -> list[Fraction]:
        """Generate a probability distribution summing to 1.

        Args:
            n: Number of outcomes.

        Returns:
            List of Fractions summing to 1.
        """
        weights = [self._rng.randint(1, 5) for _ in range(n)]
        total = sum(weights)
        return [Fraction(w, total) for w in weights]

    def _create_steps(self, data: dict) -> list[str]:
        """Generate E[X], E[X^2], and variance steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing expected value computations and subtraction.
        """
        ex_str = self._fmt.format(data["ex"])
        ex2_str = self._fmt.format(data["ex2"])
        ex_sq = data["ex"] * data["ex"]
        ex_sq_str = self._fmt.format(ex_sq)
        var_str = self._fmt.format(data["variance"])

        ex_parts = "+".join(
            f"{v}({self._fmt.format(p)})"
            for v, p in zip(data["values"], data["probs"])
        )
        ex2_parts = "+".join(
            f"{v*v}({self._fmt.format(p)})"
            for v, p in zip(data["values"], data["probs"])
        )

        return [
            f"E[X]={ex_parts}={ex_str}",
            f"E[X^2]={ex2_parts}={ex2_str}",
            f"Var={ex2_str}-({ex_str})^2={ex2_str}-{ex_sq_str}={var_str}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the variance.

        Args:
            data: Solution data.

        Returns:
            Formatted fraction string.
        """
        return self._fmt.format(data["variance"])


@register
class TotalProbabilityGenerator(StepGenerator):
    """Total probability P(A) = sum P(A|B_i) P(B_i).

    Generates a partition of the sample space into 2-3 events B_i
    with known marginal probabilities P(B_i) and conditional
    probabilities P(A|B_i), then applies the law of total probability.

    Input format:
        ``apply total probability theorem``

    Target format:
        ``P(A) = \\sum P(A|B_i)P(B_i) <step>
        P(A|B_1)P(B_1) = (1/2)(1/3) = 1/6 <step>
        P(A|B_2)P(B_2) = (3/4)(2/3) = 1/2 <step>
        P(A) = 1/6 + 1/2 = 2/3 <step> 2/3``

    Difficulty scaling:
        Difficulty 1-4: 2 partition events, simple fractions.
        Difficulty 5-8: 3 partition events.

    Prerequisites:
        conditional_prob, addition.

    Example:
        >>> gen = TotalProbabilityGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'total_probability'
    """

    def __init__(self, **kwargs) -> None:
        """Initialise with fraction formatter.

        Args:
            **kwargs: Passed to parent constructor.
        """
        super().__init__(**kwargs)
        self._fmt = FractionFormatter()

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "total_probability"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["conditional_prob", "addition"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls partition size.

        Returns:
            Natural language description.
        """
        return "apply total probability theorem"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate partition probabilities and conditionals.

        Args:
            difficulty: Controls number of partition events.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        n = 3 if difficulty >= 5 else 2
        p_b = self._make_partition(n)
        p_a_given_b = [
            Fraction(self._rng.randint(1, 4), self._rng.randint(2, 5))
            for _ in range(n)
        ]
        products = [p_a_given_b[i] * p_b[i] for i in range(n)]
        total = sum(products)

        return "P(A) = \\sum P(A|B_i)P(B_i)", {
            "n": n, "p_b": p_b, "p_a_given_b": p_a_given_b,
            "products": products, "total": total,
        }

    def _make_partition(self, n: int) -> list[Fraction]:
        """Generate a partition of probability space.

        Args:
            n: Number of partition events.

        Returns:
            List of Fractions summing to 1.
        """
        weights = [self._rng.randint(1, 5) for _ in range(n)]
        total = sum(weights)
        return [Fraction(w, total) for w in weights]

    def _create_steps(self, data: dict) -> list[str]:
        """Generate per-partition multiplication and summation steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing each product and the final sum.
        """
        steps = []
        for i in range(data["n"]):
            p_a_b = self._fmt.format(data["p_a_given_b"][i])
            p_b = self._fmt.format(data["p_b"][i])
            prod = self._fmt.format(data["products"][i])
            steps.append(
                f"P(A|B_{{{i+1}}})P(B_{{{i+1}}}) = ({p_a_b})({p_b}) = {prod}"
            )
        parts = "+".join(self._fmt.format(p) for p in data["products"])
        total_str = self._fmt.format(data["total"])
        steps.append(f"P(A) = {parts} = {total_str}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the total probability.

        Args:
            data: Solution data.

        Returns:
            Formatted fraction string.
        """
        return self._fmt.format(data["total"])


@register
class IndependenceTestGenerator(StepGenerator):
    """Test if P(A intersection B) = P(A) * P(B) for independence.

    Generates probabilities P(A), P(B), and P(A intersection B),
    then checks whether the independence condition holds.

    Input format:
        ``test event independence``

    Target format:
        ``P(A)=1/3, P(B)=1/4, P(A \\cap B)=1/12 <step>
        P(A)*P(B) = (1/3)(1/4) = 1/12 <step>
        P(A \\cap B) = 1/12 <step> 1/12 = 1/12 <step> independent``

    Difficulty scaling:
        Difficulty 1-4: small denominators (2-6), always independent.
        Difficulty 5-8: larger denominators, may or may not be independent.

    Prerequisites:
        basic_prob, multiplication.

    Example:
        >>> gen = IndependenceTestGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'independence_test'
    """

    def __init__(self, **kwargs) -> None:
        """Initialise with fraction formatter.

        Args:
            **kwargs: Passed to parent constructor.
        """
        super().__init__(**kwargs)
        self._fmt = FractionFormatter()

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "independence_test"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 3

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["basic_prob", "multiplication"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls probability complexity.

        Returns:
            Natural language description.
        """
        return "test event independence"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate probabilities and test independence.

        Args:
            difficulty: Controls whether events are independent.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        p_a, p_b, p_ab, independent = self._sample_probs(difficulty)
        product = p_a * p_b

        p_a_str = self._fmt.format(p_a)
        p_b_str = self._fmt.format(p_b)
        p_ab_str = self._fmt.format(p_ab)
        problem = f"P(A)={p_a_str}, P(B)={p_b_str}, P(A \\cap B)={p_ab_str}"
        return problem, {
            "p_a": p_a, "p_b": p_b, "p_ab": p_ab,
            "product": product, "independent": independent,
        }

    def _sample_probs(self, difficulty: int) -> tuple[Fraction, Fraction, Fraction, bool]:
        """Sample probabilities with controlled independence.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (P(A), P(B), P(A inter B), is_independent).
        """
        max_den = 6 if difficulty <= 4 else 10
        p_a = Fraction(self._rng.randint(1, max_den - 1), max_den)
        p_b = Fraction(self._rng.randint(1, max_den - 1), max_den)
        product = p_a * p_b

        if difficulty <= 4 or self._rng.random() < 0.5:
            return p_a, p_b, product, True

        offset_num = self._rng.randint(1, 3)
        offset_den = product.denominator * 2
        offset = Fraction(offset_num, offset_den)
        p_ab = max(Fraction(0), min(product + offset, min(p_a, p_b)))
        if p_ab == product:
            p_ab = max(Fraction(1, offset_den), product - offset)
        independent = (p_ab == product)
        return p_a, p_b, p_ab, independent

    def _create_steps(self, data: dict) -> list[str]:
        """Generate independence test steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing the product comparison.
        """
        prod_str = self._fmt.format(data["product"])
        p_ab_str = self._fmt.format(data["p_ab"])
        p_a_str = self._fmt.format(data["p_a"])
        p_b_str = self._fmt.format(data["p_b"])
        comparison = "=" if data["independent"] else "\\neq"

        return [
            f"P(A)*P(B) = ({p_a_str})({p_b_str}) = {prod_str}",
            f"P(A \\cap B) = {p_ab_str}",
            f"{p_ab_str} {comparison} {prod_str}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return whether events are independent.

        Args:
            data: Solution data.

        Returns:
            'independent' or 'not independent'.
        """
        return "independent" if data["independent"] else "not independent"


@register
class HypothesisTestGenerator(StepGenerator):
    """One-sample t-test: compute t-statistic and compare to threshold.

    Generates a sample mean, population mean, standard deviation, and
    sample size, then computes the t-statistic and compares to a
    critical value at alpha = 0.05.

    Input format:
        ``perform hypothesis test``

    Target format:
        ``\\bar{x}=52, \\mu_0=50, s=4, n=25 <step>
        SE = s/\\sqrt{n} = 4/\\sqrt{25} = 4/5 = 0.8 <step>
        t = (52-50)/0.8 = 2/0.8 = 2.5 <step>
        |t| = 2.5 > 1.96 <step> reject H_0``

    Difficulty scaling:
        Difficulty 1-3: n = 25-36, difference = 1-3.
        Difficulty 4-6: n = 16-49, difference = 1-5.
        Difficulty 7-8: n = 9-64, difference = 1-8.

    Prerequisites:
        mean, std_dev.

    Example:
        >>> gen = HypothesisTestGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'hypothesis_test'
    """

    _CRITICAL_VALUE = 1.96

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "hypothesis_test"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["mean", "std_dev"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls parameter ranges.

        Returns:
            Natural language description.
        """
        return "perform hypothesis test"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate test parameters and compute t-statistic.

        Args:
            difficulty: Controls parameter ranges.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        n, mu0, x_bar, s = self._sample_parameters(difficulty)
        sqrt_n = math.sqrt(n)
        se = round(s / sqrt_n, 4)
        t_stat = round((x_bar - mu0) / se, 4)
        reject = abs(t_stat) > self._CRITICAL_VALUE

        problem = (
            f"\\bar{{x}}={x_bar}, \\mu_0={mu0}, s={s}, n={n}"
        )
        return problem, {
            "x_bar": x_bar, "mu0": mu0, "s": s, "n": n,
            "sqrt_n": round(sqrt_n, 4), "se": se,
            "t_stat": t_stat, "reject": reject,
        }

    def _sample_parameters(self, difficulty: int) -> tuple[int, int, int, int]:
        """Sample hypothesis test parameters.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (n, mu_0, x_bar, s).
        """
        perfect_squares = [9, 16, 25, 36, 49, 64]
        if difficulty <= 3:
            n = self._rng.choice([25, 36])
        elif difficulty <= 6:
            n = self._rng.choice([16, 25, 36, 49])
        else:
            n = self._rng.choice(perfect_squares)

        mu0 = self._rng.randint(40, 80)
        max_diff = min(3 + difficulty, 8)
        diff = self._rng.randint(1, max_diff)
        sign = self._rng.choice([-1, 1])
        x_bar = mu0 + sign * diff
        s = self._rng.randint(2, 5 + difficulty)
        return n, mu0, x_bar, s

    def _create_steps(self, data: dict) -> list[str]:
        """Generate t-test computation steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing SE, t-statistic, and decision.
        """
        n = data["n"]
        s = data["s"]
        sqrt_n = data["sqrt_n"]
        se = data["se"]
        x_bar = data["x_bar"]
        mu0 = data["mu0"]
        t_stat = data["t_stat"]
        abs_t = abs(t_stat)
        comparison = ">" if data["reject"] else "\\leq"

        return [
            f"SE = s/\\sqrt{{n}} = {s}/\\sqrt{{{n}}} = {s}/{sqrt_n} = {se}",
            f"t = ({x_bar}-{mu0})/{se} = {x_bar - mu0}/{se} = {t_stat}",
            f"|t| = {round(abs_t, 4)} {comparison} {self._CRITICAL_VALUE}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the hypothesis test decision.

        Args:
            data: Solution data.

        Returns:
            'reject H_0' or 'fail to reject H_0'.
        """
        if data["reject"]:
            return "reject H_0"
        return "fail to reject H_0"


@register
class ConfidenceIntervalGenerator(StepGenerator):
    """Confidence interval: mean +/- z * sigma / sqrt(n).

    Computes a 95% confidence interval for the population mean
    using z = 1.96 and known standard deviation.

    Input format:
        ``compute confidence interval``

    Target format:
        ``\\bar{x}=50, \\sigma=4, n=25 <step>
        SE = 4/\\sqrt{25} = 4/5 = 0.8 <step>
        ME = 1.96(0.8) = 1.568 <step>
        CI = [50-1.568, 50+1.568] = [48.432, 51.568]``

    Difficulty scaling:
        Difficulty 1-3: n = 25-36, sigma = 2-5.
        Difficulty 4-6: n = 16-49, sigma = 2-8.
        Difficulty 7-8: n = 9-64, sigma = 2-12.

    Prerequisites:
        mean, std_dev, z_score.

    Example:
        >>> gen = ConfidenceIntervalGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'confidence_interval'
    """

    _Z = 1.96

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "confidence_interval"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["mean", "std_dev", "z_score"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls parameter ranges.

        Returns:
            Natural language description.
        """
        return "compute confidence interval"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate sample parameters and compute confidence interval.

        Args:
            difficulty: Controls parameter ranges.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        n, x_bar, sigma = self._sample_parameters(difficulty)
        sqrt_n = math.sqrt(n)
        se = round(sigma / sqrt_n, 4)
        me = round(self._Z * se, 4)
        lower = round(x_bar - me, 4)
        upper = round(x_bar + me, 4)

        problem = f"\\bar{{x}}={x_bar}, \\sigma={sigma}, n={n}"
        return problem, {
            "x_bar": x_bar, "sigma": sigma, "n": n,
            "sqrt_n": round(sqrt_n, 4), "se": se, "me": me,
            "lower": lower, "upper": upper,
        }

    def _sample_parameters(self, difficulty: int) -> tuple[int, int, int]:
        """Sample confidence interval parameters.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (n, x_bar, sigma).
        """
        perfect_squares = [9, 16, 25, 36, 49, 64]
        if difficulty <= 3:
            n = self._rng.choice([25, 36])
            sigma = self._rng.randint(2, 5)
        elif difficulty <= 6:
            n = self._rng.choice([16, 25, 36, 49])
            sigma = self._rng.randint(2, 8)
        else:
            n = self._rng.choice(perfect_squares)
            sigma = self._rng.randint(2, 12)
        x_bar = self._rng.randint(30, 80)
        return n, x_bar, sigma

    def _create_steps(self, data: dict) -> list[str]:
        """Generate confidence interval computation steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing SE, margin of error, and interval.
        """
        sigma = data["sigma"]
        n = data["n"]
        sqrt_n = data["sqrt_n"]
        se = data["se"]
        me = data["me"]
        x_bar = data["x_bar"]

        return [
            f"SE = {sigma}/\\sqrt{{{n}}} = {sigma}/{sqrt_n} = {se}",
            f"ME = {self._Z}({se}) = {me}",
            f"CI = [{x_bar}-{me}, {x_bar}+{me}] = [{data['lower']}, {data['upper']}]",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the confidence interval.

        Args:
            data: Solution data.

        Returns:
            String representation of the interval.
        """
        return f"[{data['lower']}, {data['upper']}]"


@register
class BigOGenerator(StepGenerator):
    """Identify algorithmic complexity from description.

    Presents a description of an algorithm or operation and
    asks the model to identify its Big-O time complexity class.

    Input format:
        ``identify algorithmic complexity``

    Target format:
        ``algorithm: binary search in sorted array <step>
        divide search space in half each step <step>
        O(log n)``

    Difficulty scaling:
        Difficulty 1-3: O(1), O(n), O(log n) only.
        Difficulty 4-6: adds O(n^2), O(n log n).
        Difficulty 7-8: adds O(n^3), O(2^n), O(n!), O(V+E).

    Prerequisites:
        multiplication.

    Example:
        >>> gen = BigOGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'big_o'
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "big_o"

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
            difficulty: Controls complexity class range.

        Returns:
            Natural language description.
        """
        return "identify algorithmic complexity"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an algorithm description and its complexity.

        Args:
            difficulty: Controls which complexity classes appear.

        Returns:
            Tuple of (problem_string, solution_data).
        """
        classifier = ComplexityClassifier(self._rng)
        description, complexity = classifier.sample(difficulty)
        problem = f"algorithm: {description}"
        return problem, {
            "description": description, "complexity": complexity,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate reasoning step for the complexity.

        Args:
            data: Solution data.

        Returns:
            Steps showing the algorithm description.
        """
        return [
            f"analyse: {data['description']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the complexity class.

        Args:
            data: Solution data.

        Returns:
            Big-O notation string.
        """
        return data["complexity"]


@register
class ConvolutionGenerator(StepGenerator):
    """1D discrete convolution of a signal with a kernel.

    Computes the valid convolution of a signal array with a small
    kernel using the sliding dot product. Shows each position's
    dot product as a step.

    Input format:
        ``compute 1d convolution``

    Target format:
        ``signal=[1,2,3,4,5], kernel=[1,0,-1] <step>
        pos0: 1(1)+2(0)+3(-1)=-2 <step>
        pos1: 2(1)+3(0)+4(-1)=-2 <step>
        pos2: 3(1)+4(0)+5(-1)=-2 <step> [-2, -2, -2]``

    Difficulty scaling:
        Difficulty 1-3: signal length 5-6, kernel length 2-3.
        Difficulty 4-6: signal length 7-8, kernel length 3.
        Difficulty 7-8: signal length 9-10, kernel length 3-4.

    Prerequisites:
        multiplication, addition.

    Example:
        >>> gen = ConvolutionGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'convolution'
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "convolution"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["multiplication", "addition"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls signal and kernel sizes.

        Returns:
            Natural language description.
        """
        return "compute 1d convolution"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate signal and kernel, then compute convolution.

        Args:
            difficulty: Controls signal and kernel sizes.

        Returns:
            Tuple of (problem_string, solution_data).
        """
        sig_len, kern_len = self._params(difficulty)
        signal = [self._rng.randint(-5, 5) for _ in range(sig_len)]
        kernel = [self._rng.randint(-3, 3) for _ in range(kern_len)]
        result = self._convolve(signal, kernel)

        sig_str = ",".join(str(s) for s in signal)
        kern_str = ",".join(str(k) for k in kernel)
        problem = f"signal=[{sig_str}], kernel=[{kern_str}]"
        return problem, {
            "signal": signal, "kernel": kernel, "result": result,
        }

    def _params(self, difficulty: int) -> tuple[int, int]:
        """Map difficulty to signal and kernel lengths.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (signal_length, kernel_length).
        """
        if difficulty <= 3:
            return self._rng.randint(5, 6), self._rng.randint(2, 3)
        if difficulty <= 6:
            return self._rng.randint(7, 8), 3
        return self._rng.randint(9, 10), self._rng.randint(3, 4)

    def _convolve(self, signal: list[int], kernel: list[int]) -> list[int]:
        """Compute valid 1D convolution.

        Args:
            signal: Input signal array.
            kernel: Convolution kernel.

        Returns:
            Result of valid convolution.
        """
        out_len = len(signal) - len(kernel) + 1
        result = []
        for i in range(out_len):
            window = signal[i:i + len(kernel)]
            val = sum(s * k for s, k in zip(window, kernel))
            result.append(val)
        return result

    def _create_steps(self, data: dict) -> list[str]:
        """Generate per-position dot product steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing each position's computation.
        """
        signal = data["signal"]
        kernel = data["kernel"]
        result = data["result"]
        steps = []

        for i, val in enumerate(result):
            window = signal[i:i + len(kernel)]
            terms = "+".join(
                f"{s}({k})" for s, k in zip(window, kernel)
            )
            steps.append(f"pos{i}: {terms}={val}")

        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the convolution result.

        Args:
            data: Solution data.

        Returns:
            String representation of the result array.
        """
        return f"[{', '.join(str(v) for v in data['result'])}]"


@register
class PolynomialHashGenerator(StepGenerator):
    """Polynomial hash: hash = sum(c_i * p^i) mod m.

    Computes the polynomial rolling hash of a short string using
    a base p and modulus m. Shows each character's contribution.

    Input format:
        ``compute polynomial hash``

    Target format:
        ``hash("abc"), p=31, m=1000003 <step>
        c_0: 97*31^0 mod 1000003 = 97 <step>
        c_1: 98*31^1 mod 1000003 = 3038 <step>
        c_2: 99*31^2 mod 1000003 = 95139 <step>
        sum = 97+3038+95139 = 98274 <step>
        98274 mod 1000003 = 98274 <step> 98274``

    Difficulty scaling:
        Difficulty 1-3: string length 3-4, p=31.
        Difficulty 4-6: string length 5-6, p=31 or 37.
        Difficulty 7-8: string length 7-8, p=31, 37, or 53.

    Prerequisites:
        mod_pow, addition.

    Example:
        >>> gen = PolynomialHashGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'polynomial_hash'
    """

    _MODULUS = 1000003
    _BASES = [31, 37, 53]

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "polynomial_hash"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["mod_pow", "addition"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls string length and base.

        Returns:
            Natural language description.
        """
        return "compute polynomial hash"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a string and compute its polynomial hash.

        Args:
            difficulty: Controls string length and base selection.

        Returns:
            Tuple of (problem_string, solution_data).
        """
        length, p = self._params(difficulty)
        word = self._random_word(length)
        contributions = []
        for i, ch in enumerate(word):
            val = (ord(ch) * pow(p, i, self._MODULUS)) % self._MODULUS
            contributions.append(val)
        total = sum(contributions) % self._MODULUS

        problem = f'hash("{word}"), p={p}, m={self._MODULUS}'
        return problem, {
            "word": word, "p": p, "m": self._MODULUS,
            "contributions": contributions, "total": total,
        }

    def _params(self, difficulty: int) -> tuple[int, int]:
        """Map difficulty to string length and base.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (string_length, hash_base).
        """
        if difficulty <= 3:
            return self._rng.randint(3, 4), 31
        if difficulty <= 6:
            return self._rng.randint(5, 6), self._rng.choice([31, 37])
        return self._rng.randint(7, 8), self._rng.choice(self._BASES)

    def _random_word(self, length: int) -> str:
        """Generate a random lowercase word.

        Args:
            length: Number of characters.

        Returns:
            Random lowercase string.
        """
        return "".join(
            chr(self._rng.randint(97, 122)) for _ in range(length)
        )

    def _create_steps(self, data: dict) -> list[str]:
        """Generate per-character hash contribution steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing each character's contribution and final sum.
        """
        word = data["word"]
        p = data["p"]
        m = data["m"]
        contributions = data["contributions"]
        steps = []

        for i, ch in enumerate(word):
            steps.append(
                f"c_{i}: {ord(ch)}*{p}^{i} mod {m} = {contributions[i]}"
            )

        parts = "+".join(str(c) for c in contributions)
        total_sum = sum(contributions)
        steps.append(f"sum = {parts} = {total_sum}")
        steps.append(f"{total_sum} mod {m} = {data['total']}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the hash value.

        Args:
            data: Solution data.

        Returns:
            String representation of the hash.
        """
        return str(data["total"])
