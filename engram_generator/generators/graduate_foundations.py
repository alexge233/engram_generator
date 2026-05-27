"""Tier 6 generators — graduate-level mathematics and algorithms.

Unlocks when Tier 0-5 tasks are mastered. Introduces Euler's totient
function, Chinese Remainder Theorem, primality testing, prime
factorisation, topological sort, Catalan numbers, derangements,
0/1 knapsack, longest common subsequence, longest increasing
subsequence, polynomial multiplication, and Bayes' theorem.
These tasks require deep prerequisite chains and multi-step
reasoning over number theory, combinatorics, dynamic programming,
and probability.
"""
import math
from fractions import Fraction

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


class PrimePool:
    """Provides small primes and prime-power factorisation utilities.

    Offers methods for sampling primes, building composite numbers
    from known prime factors, and computing Euler's totient function
    from a factorisation.

    Example:
        >>> import random
        >>> pool = PrimePool(random.Random(42))
        >>> pool.small_primes[:5]
        [2, 3, 5, 7, 11]
        >>> pool.totient_from_factors({2: 2, 3: 1})
        4
    """

    small_primes: list[int] = [2, 3, 5, 7, 11, 13, 17, 19, 23]

    def __init__(self, rng: "random.Random") -> None:
        """Initialise with a random number generator.

        Args:
            rng: Seeded Random instance.
        """
        self._rng = rng

    def sample_primes(self, count: int, max_index: int = 6) -> list[int]:
        """Sample distinct primes from the pool.

        Args:
            count: Number of primes to sample.
            max_index: Upper bound on the index into small_primes.

        Returns:
            List of distinct primes.
        """
        indices = self._rng.sample(
            range(min(max_index, len(self.small_primes))), count,
        )
        return [self.small_primes[i] for i in sorted(indices)]

    def build_number(self, factors: dict[int, int]) -> int:
        """Compute the product from a prime factorisation.

        Args:
            factors: Mapping of prime to exponent.

        Returns:
            The composite number.
        """
        result = 1
        for p, e in factors.items():
            result *= p ** e
        return result

    def totient_from_factors(self, factors: dict[int, int]) -> int:
        """Compute Euler's totient from a known factorisation.

        Uses phi(p^k) = p^k - p^(k-1) and multiplicativity.

        Args:
            factors: Mapping of prime to exponent.

        Returns:
            Euler's totient value.
        """
        result = 1
        for p, e in factors.items():
            result *= p ** e - p ** (e - 1)
        return result


class DAGBuilder:
    """Builds random directed acyclic graphs for topological sort tasks.

    Generates a DAG by assigning nodes to layers and adding edges
    only from earlier layers to later layers, guaranteeing acyclicity.

    Example:
        >>> import random
        >>> builder = DAGBuilder(random.Random(42))
        >>> adj, nodes = builder.build(5)
        >>> len(nodes)
        5
    """

    def __init__(self, rng: "random.Random") -> None:
        """Initialise with a random number generator.

        Args:
            rng: Seeded Random instance.
        """
        self._rng = rng

    def build(self, num_nodes: int) -> tuple[dict[str, list[str]], list[str]]:
        """Build a random DAG with the given number of nodes.

        Ensures every node has at least one incoming or outgoing edge
        so the graph is non-trivial.

        Args:
            num_nodes: Number of nodes in the graph.

        Returns:
            Tuple of (adjacency_dict, node_list).
        """
        nodes = [chr(65 + i) for i in range(num_nodes)]
        adj: dict[str, list[str]] = {n: [] for n in nodes}
        self._add_spine(adj, nodes)
        self._add_extra_edges(adj, nodes)
        return adj, nodes

    def _add_spine(self, adj: dict[str, list[str]],
                   nodes: list[str]) -> None:
        """Add a guaranteed path through all nodes.

        Args:
            adj: Adjacency dict to modify in place.
            nodes: Ordered node list.
        """
        for i in range(len(nodes) - 1):
            if nodes[i + 1] not in adj[nodes[i]]:
                adj[nodes[i]].append(nodes[i + 1])

    def _add_extra_edges(self, adj: dict[str, list[str]],
                         nodes: list[str]) -> None:
        """Add random forward edges to increase graph density.

        Args:
            adj: Adjacency dict to modify in place.
            nodes: Ordered node list.
        """
        num_extra = self._rng.randint(0, max(1, len(nodes) - 2))
        for _ in range(num_extra):
            i = self._rng.randint(0, len(nodes) - 2)
            j = self._rng.randint(i + 1, len(nodes) - 1)
            if nodes[j] not in adj[nodes[i]]:
                adj[nodes[i]].append(nodes[j])


class DPTableFormatter:
    """Formats dynamic programming table rows as step strings.

    Provides consistent formatting for DP-based generators
    such as knapsack, LCS, and LIS.

    Example:
        >>> f = DPTableFormatter()
        >>> f.format_row("dp", 3, 7)
        'dp[3]=7'
    """

    def format_row(self, prefix: str, index: int, value: int) -> str:
        """Format a single DP cell as a step string.

        Args:
            prefix: Label prefix (e.g. 'dp', 'tails').
            index: Cell index.
            value: Cell value.

        Returns:
            Formatted string like 'dp[3]=7'.
        """
        return f"{prefix}[{index}]={value}"

    def format_2d_row(self, row_idx: int, row: list[int]) -> str:
        """Format a full DP table row.

        Args:
            row_idx: Row index.
            row: List of cell values.

        Returns:
            Formatted string like 'row0: 0,1,2,3'.
        """
        values = ",".join(str(v) for v in row)
        return f"row{row_idx}: {values}"


@register
class TotientGenerator(StepGenerator):
    """Compute Euler's totient function via prime factorisation.

    Generates a composite number from a known prime factorisation,
    then computes phi(n) using the multiplicative formula
    phi(p^k) = p^k - p^(k-1). Shows the factorisation, each
    prime-power totient, and the final product.

    Input format:
        ``compute euler totient``

    Target format:
        ``\\phi(36) <step> 36=2^2 \\cdot 3^2 <step> \\phi(2^2)=2
        <step> \\phi(3^2)=6 <step> 2*6=12 <step> 12``

    Difficulty scaling:
        Difficulty 1: 2 primes, exponents 1.
        Difficulty 4: 2-3 primes, exponents 1-2.
        Difficulty 8: 3-4 primes, exponents 1-3.
        Larger exponents and more prime factors increase the number
        of steps and the magnitude of the result.

    Prerequisites:
        factorisation, multiplication.

    Example:
        >>> gen = TotientGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'totient'
    """

    _NUM_PRIMES = {
        1: (2, 2), 2: (2, 2), 3: (2, 3), 4: (2, 3),
        5: (2, 3), 6: (3, 3), 7: (3, 4), 8: (3, 4),
    }

    _MAX_EXP = {
        1: 1, 2: 1, 3: 2, 4: 2,
        5: 2, 6: 2, 7: 3, 8: 3,
    }

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "totient"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["factorisation", "multiplication"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls prime count and exponent range.

        Returns:
            Natural language description.
        """
        return "compute euler totient"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a composite number with known factorisation.

        Args:
            difficulty: Controls number of primes and exponents.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        pool = PrimePool(self._rng)
        factors = self._sample_factors(difficulty, pool)
        n = pool.build_number(factors)
        phi = pool.totient_from_factors(factors)
        return f"\\phi({n})", {"n": n, "factors": factors, "phi": phi}

    def _sample_factors(self, difficulty: int,
                        pool: PrimePool) -> dict[int, int]:
        """Sample a prime factorisation for the given difficulty.

        Args:
            difficulty: Difficulty level.
            pool: PrimePool instance for sampling primes.

        Returns:
            Dict mapping prime to exponent.
        """
        lo, hi = self._NUM_PRIMES.get(difficulty, (2, 3))
        num_primes = self._rng.randint(lo, hi)
        primes = pool.sample_primes(num_primes)
        max_exp = self._MAX_EXP.get(difficulty, 2)
        return {p: self._rng.randint(1, max_exp) for p in primes}

    def _create_steps(self, data: dict) -> list[str]:
        """Generate factorisation and per-prime totient steps.

        Args:
            data: Solution data with factors and totient.

        Returns:
            Steps showing factorisation, each phi(p^k), and product.
        """
        factors = data["factors"]
        steps: list[str] = [self._format_factorisation(data["n"], factors)]
        phi_values = self._compute_phi_steps(factors, steps)
        steps.append(self._format_product(phi_values))
        return steps

    def _format_factorisation(self, n: int,
                              factors: dict[int, int]) -> str:
        """Format the prime factorisation as a LaTeX string.

        Args:
            n: The composite number.
            factors: Prime factorisation dict.

        Returns:
            Step string like '36=2^2 \\cdot 3^2'.
        """
        parts = [f"{p}^{e}" if e > 1 else str(p) for p, e in factors.items()]
        joined = " \\cdot ".join(parts)
        return f"{n}={joined}"

    def _compute_phi_steps(self, factors: dict[int, int],
                           steps: list[str]) -> list[int]:
        """Compute and record phi(p^k) for each prime power.

        Args:
            factors: Prime factorisation dict.
            steps: List to append step strings to.

        Returns:
            List of per-prime-power totient values.
        """
        phi_values: list[int] = []
        for p, e in factors.items():
            phi_pk = p ** e - p ** (e - 1)
            phi_values.append(phi_pk)
            steps.append(f"\\phi({p}^{e})={phi_pk}")
        return phi_values

    def _format_product(self, phi_values: list[int]) -> str:
        """Format the multiplication of all phi(p^k) values.

        Args:
            phi_values: List of per-prime-power totient values.

        Returns:
            Step string like '2*6=12'.
        """
        product = 1
        for v in phi_values:
            product *= v
        parts = "*".join(str(v) for v in phi_values)
        return f"{parts}={product}"

    def _create_answer(self, data: dict) -> str:
        """Return Euler's totient value.

        Args:
            data: Solution data.

        Returns:
            String representation of phi(n).
        """
        return str(data["phi"])


@register
class CRTGenerator(StepGenerator):
    """Solve systems of congruences using the Chinese Remainder Theorem.

    Generates 2-4 congruences with pairwise coprime moduli drawn
    from a small prime pool. Shows the construction steps: compute
    the product of moduli, per-congruence partial products, modular
    inverses, and the final combination.

    Input format:
        ``solve using chinese remainder theorem``

    Target format:
        ``x \\equiv 2 \\pmod{3}, x \\equiv 3 \\pmod{5} <step>
        M=15 <step> M_1=5, M_1^{-1}=2 \\pmod{3} <step>
        M_2=3, M_2^{-1}=2 \\pmod{5} <step>
        x=2*5*2+3*3*2=38 <step> x \\equiv 8 \\pmod{15} <step> 8``

    Difficulty scaling:
        Difficulty 1-2: 2 congruences, small primes.
        Difficulty 3-5: 2-3 congruences.
        Difficulty 6-8: 3-4 congruences.

    Prerequisites:
        mod_inv, modular.

    Example:
        >>> gen = CRTGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'crt'
    """

    _NUM_CONGRUENCES = {
        1: 2, 2: 2, 3: 2, 4: 3,
        5: 3, 6: 3, 7: 4, 8: 4,
    }

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "crt"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["mod_inv", "modular"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls number of congruences.

        Returns:
            Natural language description.
        """
        return "solve using chinese remainder theorem"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a CRT system with pairwise coprime moduli.

        Args:
            difficulty: Controls number of congruences.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        num_cong = self._NUM_CONGRUENCES.get(difficulty, 3)
        moduli = self._sample_coprime_moduli(num_cong)
        remainders = [self._rng.randint(0, m - 1) for m in moduli]
        big_m = self._product(moduli)
        solution = self._solve_crt(remainders, moduli, big_m)
        problem = self._format_system(remainders, moduli)
        return problem, {
            "remainders": remainders, "moduli": moduli,
            "big_m": big_m, "solution": solution,
        }

    def _sample_coprime_moduli(self, count: int) -> list[int]:
        """Sample pairwise coprime moduli from a prime pool.

        Args:
            count: Number of moduli needed.

        Returns:
            List of pairwise coprime moduli.
        """
        pool = PrimePool(self._rng)
        primes = pool.sample_primes(count)
        return primes

    def _product(self, values: list[int]) -> int:
        """Compute the product of a list of integers.

        Args:
            values: List of positive integers.

        Returns:
            Product of all values.
        """
        result = 1
        for v in values:
            result *= v
        return result

    def _solve_crt(self, remainders: list[int], moduli: list[int],
                   big_m: int) -> int:
        """Solve the CRT system and return the unique solution mod M.

        Args:
            remainders: List of remainders.
            moduli: List of moduli.
            big_m: Product of all moduli.

        Returns:
            Unique solution in [0, big_m).
        """
        result = 0
        for r, m in zip(remainders, moduli):
            mi = big_m // m
            inv = pow(mi, -1, m)
            result += r * mi * inv
        return result % big_m

    def _format_system(self, remainders: list[int],
                       moduli: list[int]) -> str:
        """Format the congruence system as LaTeX.

        Args:
            remainders: List of remainders.
            moduli: List of moduli.

        Returns:
            LaTeX string of the system.
        """
        parts = [
            f"x \\equiv {r} \\pmod{{{m}}}"
            for r, m in zip(remainders, moduli)
        ]
        return ", ".join(parts)

    def _create_steps(self, data: dict) -> list[str]:
        """Generate CRT construction steps.

        Args:
            data: Solution data with remainders, moduli, big_m.

        Returns:
            Steps showing M, each M_i and inverse, and combination.
        """
        remainders = data["remainders"]
        moduli = data["moduli"]
        big_m = data["big_m"]
        steps: list[str] = [f"M={big_m}"]
        terms: list[str] = []

        for i, (r, m) in enumerate(zip(remainders, moduli)):
            mi = big_m // m
            inv = pow(mi, -1, m)
            steps.append(f"M_{{{i+1}}}={mi}, M_{{{i+1}}}^{{-1}}={inv} \\pmod{{{m}}}")
            terms.append(f"{r}*{mi}*{inv}")

        raw_sum = sum(
            r * (big_m // m) * pow(big_m // m, -1, m)
            for r, m in zip(remainders, moduli)
        )
        steps.append(f"x={'+'.join(terms)}={raw_sum}")
        steps.append(f"x \\equiv {data['solution']} \\pmod{{{big_m}}}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the CRT solution.

        Args:
            data: Solution data.

        Returns:
            String representation of the solution.
        """
        return str(data["solution"])


@register
class PrimalityGenerator(StepGenerator):
    """Primality test via trial division up to sqrt(n).

    Generates a number that is either prime or composite (50/50 split)
    and shows trial division by primes up to sqrt(n). For composites,
    shows the first divisor found. For primes, shows all trials pass.

    Input format:
        ``test if number is prime``

    Target format:
        ``\\text{prime}(97) <step> 97/2: no <step> 97/3: no <step>
        97/5: no <step> 97/7: no <step> \\sqrt{97}<10: done <step> yes``

    Difficulty scaling:
        Difficulty 1-2: numbers in [10, 50].
        Difficulty 3-4: numbers in [30, 150].
        Difficulty 5-6: numbers in [100, 500].
        Difficulty 7-8: numbers in [200, 1000].

    Prerequisites:
        division, modular.

    Example:
        >>> gen = PrimalityGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'primality'
    """

    _RANGE: dict[int, tuple[int, int]] = {
        1: (10, 50), 2: (10, 50),
        3: (30, 150), 4: (30, 150),
        5: (100, 500), 6: (100, 500),
        7: (200, 1000), 8: (200, 1000),
    }

    _TRIAL_PRIMES: list[int] = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "primality"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["division", "modular"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls number range.

        Returns:
            Natural language description.
        """
        return "test if number is prime"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a number to test for primality.

        Selects prime or composite with equal probability.

        Args:
            difficulty: Controls number range.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        lo, hi = self._RANGE.get(difficulty, self._RANGE[8])
        want_prime = self._rng.random() < 0.5
        n = self._find_number(lo, hi, want_prime)
        is_prime = self._is_prime(n)
        sqrt_n = int(math.isqrt(n))
        return (
            f"\\text{{prime}}({n})",
            {"n": n, "is_prime": is_prime, "sqrt_n": sqrt_n},
        )

    def _find_number(self, lo: int, hi: int,
                     want_prime: bool) -> int:
        """Find a prime or composite in the given range.

        Args:
            lo: Lower bound.
            hi: Upper bound.
            want_prime: Whether to search for a prime.

        Returns:
            A number matching the primality requirement.
        """
        for _ in range(200):
            n = self._rng.randint(lo, hi)
            if self._is_prime(n) == want_prime:
                return n
        return self._rng.randint(lo, hi)

    def _is_prime(self, n: int) -> bool:
        """Check if n is prime via trial division.

        Args:
            n: Number to test.

        Returns:
            True if n is prime.
        """
        if n < 2:
            return False
        for p in self._TRIAL_PRIMES:
            if p * p > n:
                break
            if n % p == 0:
                return n == p
        return True

    def _create_steps(self, data: dict) -> list[str]:
        """Generate trial division steps.

        Args:
            data: Solution data with n and primality result.

        Returns:
            Steps showing each trial division.
        """
        n = data["n"]
        sqrt_n = data["sqrt_n"]
        steps: list[str] = []

        for p in self._TRIAL_PRIMES:
            if p * p > n:
                break
            if n % p == 0 and n != p:
                steps.append(f"{n}/{p}: yes, {n}={p}*{n // p}")
                return steps
            steps.append(f"{n}/{p}: no")

        steps.append(f"\\sqrt{{{n}}}<{sqrt_n + 1}: done")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return 'yes' or 'no' for primality.

        Args:
            data: Solution data.

        Returns:
            'yes' if prime, 'no' if composite.
        """
        return "yes" if data["is_prime"] else "no"


@register
class FactorisationGenerator(StepGenerator):
    """Prime factorisation by trial division.

    Builds a composite number from small primes so the factorisation
    is known. Shows the trial division process: repeatedly divide by
    the smallest prime factor until the quotient reaches 1.

    Input format:
        ``find prime factorisation``

    Target format:
        ``\\text{factor}(60) <step> 60/2=30 <step> 30/2=15 <step>
        15/3=5 <step> 5/5=1 <step> 2^2 \\cdot 3 \\cdot 5``

    Difficulty scaling:
        Difficulty 1-2: 2-3 prime factors, exponents 1.
        Difficulty 3-4: 2-3 primes, exponents 1-2.
        Difficulty 5-6: 3-4 primes, exponents 1-2.
        Difficulty 7-8: 3-4 primes, exponents 1-3.

    Prerequisites:
        division, primality.

    Example:
        >>> gen = FactorisationGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'factorisation'
    """

    _NUM_PRIMES = {
        1: (2, 3), 2: (2, 3), 3: (2, 3), 4: (2, 3),
        5: (3, 4), 6: (3, 4), 7: (3, 4), 8: (3, 4),
    }

    _MAX_EXP = {
        1: 1, 2: 1, 3: 2, 4: 2,
        5: 2, 6: 2, 7: 3, 8: 3,
    }

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "factorisation"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["division", "primality"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls factor count and exponent range.

        Returns:
            Natural language description.
        """
        return "find prime factorisation"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a composite number with known factorisation.

        Args:
            difficulty: Controls prime count and exponents.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        pool = PrimePool(self._rng)
        factors = self._sample_factors(difficulty, pool)
        n = pool.build_number(factors)
        return f"\\text{{factor}}({n})", {"n": n, "factors": factors}

    def _sample_factors(self, difficulty: int,
                        pool: PrimePool) -> dict[int, int]:
        """Sample a prime factorisation for the given difficulty.

        Args:
            difficulty: Difficulty level.
            pool: PrimePool instance.

        Returns:
            Dict mapping prime to exponent.
        """
        lo, hi = self._NUM_PRIMES.get(difficulty, (2, 3))
        num_primes = self._rng.randint(lo, hi)
        primes = pool.sample_primes(num_primes)
        max_exp = self._MAX_EXP.get(difficulty, 2)
        return {p: self._rng.randint(1, max_exp) for p in primes}

    def _create_steps(self, data: dict) -> list[str]:
        """Generate trial division steps.

        Args:
            data: Solution data with n and factors.

        Returns:
            Steps showing each division until quotient reaches 1.
        """
        n = data["n"]
        factors = data["factors"]
        return self._trial_division_steps(n, factors)

    def _trial_division_steps(self, n: int,
                              factors: dict[int, int]) -> list[str]:
        """Perform trial division and record each step.

        Args:
            n: The composite number to factor.
            factors: Known factorisation for verification.

        Returns:
            Step strings showing each division.
        """
        steps: list[str] = []
        current = n
        for p in sorted(factors.keys()):
            for _ in range(factors[p]):
                quotient = current // p
                steps.append(f"{current}/{p}={quotient}")
                current = quotient
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the prime factorisation as a LaTeX string.

        Args:
            data: Solution data.

        Returns:
            Factorisation like '2^2 \\cdot 3 \\cdot 5'.
        """
        factors = data["factors"]
        parts: list[str] = []
        for p in sorted(factors.keys()):
            e = factors[p]
            parts.append(f"{p}^{e}" if e > 1 else str(p))
        return " \\cdot ".join(parts)


@register
class TopoSortGenerator(StepGenerator):
    """Topological sort of a DAG via Kahn's algorithm.

    Generates a directed acyclic graph and shows node-by-node
    removal in Kahn's algorithm order: repeatedly remove a node
    with in-degree zero and add it to the output ordering.

    Input format:
        ``find topological ordering of dag``

    Target format:
        ``A:B,C;B:D;C:D;D: <step> remove A (in-deg 0) <step>
        remove B (in-deg 0) <step> remove C (in-deg 0) <step>
        remove D (in-deg 0) <step> A,B,C,D``

    Difficulty scaling:
        Difficulty 1-2: 4-5 nodes.
        Difficulty 3-4: 5-6 nodes.
        Difficulty 5-6: 6-7 nodes.
        Difficulty 7-8: 7-8 nodes.

    Prerequisites:
        graph_reach.

    Example:
        >>> gen = TopoSortGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'topo_sort'
    """

    _NODE_COUNTS = {
        1: (4, 5), 2: (4, 5), 3: (5, 6), 4: (5, 6),
        5: (6, 7), 6: (6, 7), 7: (7, 8), 8: (7, 8),
    }

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "topo_sort"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["graph_reach"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls graph size.

        Returns:
            Natural language description.
        """
        return "find topological ordering of dag"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a DAG and compute a topological ordering.

        Args:
            difficulty: Controls number of nodes.

        Returns:
            Tuple of (graph_description, solution_data).
        """
        lo, hi = self._NODE_COUNTS.get(difficulty, (5, 6))
        num_nodes = self._rng.randint(lo, hi)
        builder = DAGBuilder(self._rng)
        adj, nodes = builder.build(num_nodes)
        ordering = self._kahn_sort(adj, nodes)
        graph_str = self._format_graph(adj, nodes)
        return graph_str, {"adj": adj, "nodes": nodes, "ordering": ordering}

    def _format_graph(self, adj: dict[str, list[str]],
                      nodes: list[str]) -> str:
        """Format adjacency list as a compact string.

        Args:
            adj: Adjacency dict.
            nodes: Ordered node list.

        Returns:
            String like 'A:B,C;B:D;C:D;D:'.
        """
        parts: list[str] = []
        for n in nodes:
            neighbors = ",".join(adj[n])
            parts.append(f"{n}:{neighbors}")
        return ";".join(parts)

    def _kahn_sort(self, adj: dict[str, list[str]],
                   nodes: list[str]) -> list[str]:
        """Perform topological sort using Kahn's algorithm.

        Args:
            adj: Adjacency dict.
            nodes: All node labels.

        Returns:
            Topologically sorted list of nodes.
        """
        in_degree = self._compute_in_degrees(adj, nodes)
        queue = sorted([n for n in nodes if in_degree[n] == 0])
        result: list[str] = []

        while queue:
            node = queue.pop(0)
            result.append(node)
            for neighbor in adj[node]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
            queue.sort()

        return result

    def _compute_in_degrees(self, adj: dict[str, list[str]],
                            nodes: list[str]) -> dict[str, int]:
        """Compute in-degree for each node.

        Args:
            adj: Adjacency dict.
            nodes: All node labels.

        Returns:
            Dict mapping node to its in-degree.
        """
        in_degree: dict[str, int] = {n: 0 for n in nodes}
        for n in nodes:
            for neighbor in adj[n]:
                in_degree[neighbor] += 1
        return in_degree

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Kahn's algorithm removal steps.

        Args:
            data: Solution data with ordering.

        Returns:
            Steps showing each node removal.
        """
        return [f"remove {node} (in-deg 0)" for node in data["ordering"]]

    def _create_answer(self, data: dict) -> str:
        """Return the topological ordering.

        Args:
            data: Solution data.

        Returns:
            Comma-separated node labels in topological order.
        """
        return ",".join(data["ordering"])


@register
class CatalanGenerator(StepGenerator):
    """Compute the nth Catalan number via C(2n,n)/(n+1).

    Uses the binomial coefficient formula to compute Catalan numbers.
    Shows the binomial coefficient computation and the final division.

    Input format:
        ``compute catalan number``

    Target format:
        ``C_5 = \\frac{1}{6}\\binom{10}{5} <step> \\binom{10}{5}=252
        <step> 252/6=42 <step> 42``

    Difficulty scaling:
        Difficulty 1-2: n in [2, 4].
        Difficulty 3-4: n in [3, 6].
        Difficulty 5-6: n in [5, 8].
        Difficulty 7-8: n in [6, 10].

    Prerequisites:
        binomial.

    Example:
        >>> gen = CatalanGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'catalan'
    """

    _N_RANGES = {
        1: (2, 4), 2: (2, 4), 3: (3, 6), 4: (3, 6),
        5: (5, 8), 6: (5, 8), 7: (6, 10), 8: (6, 10),
    }

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "catalan"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["binomial"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls the value of n.

        Returns:
            Natural language description.
        """
        return "compute catalan number"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Catalan number problem.

        Args:
            difficulty: Controls the range of n.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        lo, hi = self._N_RANGES.get(difficulty, (3, 6))
        n = self._rng.randint(lo, hi)
        binom = math.comb(2 * n, n)
        catalan = binom // (n + 1)
        return (
            f"C_{n} = \\frac{{1}}{{{n + 1}}}\\binom{{{2 * n}}}{{{n}}}",
            {"n": n, "binom": binom, "catalan": catalan},
        )

    def _create_steps(self, data: dict) -> list[str]:
        """Generate binomial and division steps.

        Args:
            data: Solution data with n, binom, catalan.

        Returns:
            Steps showing binomial coefficient and division.
        """
        n = data["n"]
        binom = data["binom"]
        catalan = data["catalan"]
        return [
            f"\\binom{{{2 * n}}}{{{n}}}={binom}",
            f"{binom}/{n + 1}={catalan}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the Catalan number.

        Args:
            data: Solution data.

        Returns:
            String representation of C_n.
        """
        return str(data["catalan"])


@register
class DerangementGenerator(StepGenerator):
    """Compute D(n) using the recurrence D(n) = (n-1)(D(n-1) + D(n-2)).

    Shows the base cases D(0)=1, D(1)=0 and each recurrence step
    building up to D(n). The derangement count is the number of
    permutations with no fixed point.

    Input format:
        ``compute number of derangements``

    Target format:
        ``D(5) <step> D(0)=1 <step> D(1)=0 <step>
        D(2)=1*(0+1)=1 <step> D(3)=2*(1+0)=2 <step>
        D(4)=3*(2+1)=9 <step> D(5)=4*(9+2)=44 <step> 44``

    Difficulty scaling:
        Difficulty 1-2: n in [3, 5].
        Difficulty 3-4: n in [4, 7].
        Difficulty 5-6: n in [6, 9].
        Difficulty 7-8: n in [8, 12].

    Prerequisites:
        permutation, subtraction.

    Example:
        >>> gen = DerangementGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'derangement'
    """

    _N_RANGES = {
        1: (3, 5), 2: (3, 5), 3: (4, 7), 4: (4, 7),
        5: (6, 9), 6: (6, 9), 7: (8, 12), 8: (8, 12),
    }

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "derangement"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["permutation", "subtraction"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls the value of n.

        Returns:
            Natural language description.
        """
        return "compute number of derangements"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a derangement count problem.

        Args:
            difficulty: Controls the range of n.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        lo, hi = self._N_RANGES.get(difficulty, (4, 7))
        n = self._rng.randint(lo, hi)
        sequence = self._compute_derangements(n)
        return f"D({n})", {"n": n, "sequence": sequence}

    def _compute_derangements(self, n: int) -> list[int]:
        """Compute derangement values from D(0) to D(n).

        Args:
            n: Target index.

        Returns:
            List of derangement counts [D(0), D(1), ..., D(n)].
        """
        if n == 0:
            return [1]
        if n == 1:
            return [1, 0]
        seq = [1, 0]
        for i in range(2, n + 1):
            seq.append((i - 1) * (seq[i - 1] + seq[i - 2]))
        return seq

    def _create_steps(self, data: dict) -> list[str]:
        """Generate recurrence steps showing each D(i).

        Args:
            data: Solution data with the full sequence.

        Returns:
            Steps showing base cases and each recurrence application.
        """
        seq = data["sequence"]
        steps: list[str] = ["D(0)=1", "D(1)=0"]
        for i in range(2, len(seq)):
            steps.append(
                f"D({i})={i - 1}*({seq[i - 1]}+{seq[i - 2]})={seq[i]}"
            )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return D(n).

        Args:
            data: Solution data.

        Returns:
            String representation of D(n).
        """
        return str(data["sequence"][-1])


@register
class KnapsackGenerator(StepGenerator):
    """0/1 knapsack problem solved via dynamic programming.

    Generates a small set of items with weights and values, and a
    capacity constraint. Shows the DP table construction row by row,
    then reports the maximum achievable value.

    Input format:
        ``solve knapsack problem``

    Target format:
        ``knap(10;3:4,4:5,5:7) <step> dp[3]=4 <step> dp[4]=5
        <step> dp[5]=7 <step> ... <step> 12``

    Difficulty scaling:
        Difficulty 1-2: 2-3 items, capacity 5-10.
        Difficulty 3-4: 3-4 items, capacity 8-15.
        Difficulty 5-6: 4-5 items, capacity 12-20.
        Difficulty 7-8: 5-6 items, capacity 15-25.

    Prerequisites:
        addition.

    Example:
        >>> gen = KnapsackGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'knapsack'
    """

    _ITEM_COUNTS = {
        1: (2, 3), 2: (2, 3), 3: (3, 4), 4: (3, 4),
        5: (4, 5), 6: (4, 5), 7: (5, 6), 8: (5, 6),
    }

    _CAPACITY_RANGES = {
        1: (5, 10), 2: (5, 10), 3: (8, 15), 4: (8, 15),
        5: (12, 20), 6: (12, 20), 7: (15, 25), 8: (15, 25),
    }

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "knapsack"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["addition"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls item count and capacity.

        Returns:
            Natural language description.
        """
        return "solve knapsack problem"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate items and capacity, then solve via DP.

        Args:
            difficulty: Controls item count and capacity range.

        Returns:
            Tuple of (problem_string, solution_data).
        """
        items = self._generate_items(difficulty)
        cap_lo, cap_hi = self._CAPACITY_RANGES.get(difficulty, (8, 15))
        capacity = self._rng.randint(cap_lo, cap_hi)
        dp = self._solve_knapsack(items, capacity)
        problem_str = self._format_problem(capacity, items)
        return problem_str, {"items": items, "capacity": capacity, "dp": dp}

    def _generate_items(self, difficulty: int) -> list[tuple[int, int]]:
        """Generate (weight, value) pairs for items.

        Args:
            difficulty: Controls number of items.

        Returns:
            List of (weight, value) tuples.
        """
        lo, hi = self._ITEM_COUNTS.get(difficulty, (3, 4))
        n = self._rng.randint(lo, hi)
        return [
            (self._rng.randint(1, 8), self._rng.randint(1, 15))
            for _ in range(n)
        ]

    def _format_problem(self, capacity: int,
                        items: list[tuple[int, int]]) -> str:
        """Format the knapsack problem description.

        Args:
            capacity: Knapsack capacity.
            items: List of (weight, value) pairs.

        Returns:
            String like 'knap(10;3:4,4:5,5:7)'.
        """
        items_str = ",".join(f"{w}:{v}" for w, v in items)
        return f"knap({capacity};{items_str})"

    def _solve_knapsack(self, items: list[tuple[int, int]],
                        capacity: int) -> list[int]:
        """Solve 0/1 knapsack and return the DP table.

        Args:
            items: List of (weight, value) pairs.
            capacity: Knapsack capacity.

        Returns:
            1D DP table where dp[w] is max value for capacity w.
        """
        dp = [0] * (capacity + 1)
        for weight, value in items:
            for w in range(capacity, weight - 1, -1):
                dp[w] = max(dp[w], dp[w - weight] + value)
        return dp

    def _create_steps(self, data: dict) -> list[str]:
        """Generate DP table update steps for significant cells.

        Args:
            data: Solution data with items, capacity, and DP table.

        Returns:
            Steps showing key DP cell updates.
        """
        items = data["items"]
        capacity = data["capacity"]
        steps: list[str] = []
        dp = [0] * (capacity + 1)

        for weight, value in items:
            for w in range(capacity, weight - 1, -1):
                new_val = dp[w - weight] + value
                if new_val > dp[w]:
                    dp[w] = new_val
                    steps.append(f"dp[{w}]={dp[w]}")

        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the maximum knapsack value.

        Args:
            data: Solution data.

        Returns:
            String representation of the optimal value.
        """
        return str(data["dp"][data["capacity"]])


@register
class LCSGenerator(StepGenerator):
    """Longest common subsequence length via dynamic programming.

    Generates two short strings and computes the LCS length using
    a 2D DP table. Shows each row of the DP table as a step.

    Input format:
        ``find longest common subsequence length``

    Target format:
        ``lcs(abcde,ace) <step> row0: 0,0,0,0 <step>
        row1: 0,1,1,1 <step> ... <step> 3``

    Difficulty scaling:
        Difficulty 1-2: strings of length 3-4.
        Difficulty 3-4: strings of length 4-6.
        Difficulty 5-6: strings of length 5-7.
        Difficulty 7-8: strings of length 7-10.

    Prerequisites:
        edit_distance.

    Example:
        >>> gen = LCSGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'lcs'
    """

    _LEN_RANGES = {
        1: (3, 4), 2: (3, 4), 3: (4, 6), 4: (4, 6),
        5: (5, 7), 6: (5, 7), 7: (7, 10), 8: (7, 10),
    }

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "lcs"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["edit_distance"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls string length.

        Returns:
            Natural language description.
        """
        return "find longest common subsequence length"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate two strings and compute their LCS length.

        Args:
            difficulty: Controls string length.

        Returns:
            Tuple of (problem_string, solution_data).
        """
        lo, hi = self._LEN_RANGES.get(difficulty, (4, 6))
        len_a = self._rng.randint(lo, hi)
        len_b = self._rng.randint(lo, hi)
        a = self._random_word(len_a)
        b = self._random_word(len_b)
        dp = self._compute_dp(a, b)
        return f"lcs({a},{b})", {"a": a, "b": b, "dp": dp}

    def _random_word(self, length: int) -> str:
        """Generate a random lowercase word from a small alphabet.

        Uses a-f to increase matching probability for interesting LCS.

        Args:
            length: Number of characters.

        Returns:
            Random string.
        """
        return "".join(chr(self._rng.randint(97, 102)) for _ in range(length))

    def _compute_dp(self, a: str, b: str) -> list[list[int]]:
        """Compute the LCS DP table.

        Args:
            a: First string.
            b: Second string.

        Returns:
            2D DP table.
        """
        m, n = len(a), len(b)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if a[i - 1] == b[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1] + 1
                else:
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
        return dp

    def _create_steps(self, data: dict) -> list[str]:
        """Generate row-by-row DP table steps.

        Args:
            data: Solution data with the DP table.

        Returns:
            Steps showing each row of the table.
        """
        dp = data["dp"]
        formatter = DPTableFormatter()
        return [formatter.format_2d_row(i, row) for i, row in enumerate(dp)]

    def _create_answer(self, data: dict) -> str:
        """Return the LCS length.

        Args:
            data: Solution data.

        Returns:
            String representation of the LCS length.
        """
        return str(data["dp"][-1][-1])


@register
class LISGenerator(StepGenerator):
    """Longest increasing subsequence length via patience sorting.

    Generates a sequence of integers and finds the LIS length using
    patience sorting (tails array). Shows each element processed
    and the state of the tails array.

    Input format:
        ``find length of longest increasing subsequence``

    Target format:
        ``lis(3,1,4,1,5) <step> tails=[3] <step> tails=[1] <step>
        tails=[1,4] <step> tails=[1,4] <step> tails=[1,4,5]
        <step> 3``

    Difficulty scaling:
        Difficulty 1-2: 4-6 elements, values 1-20.
        Difficulty 3-4: 6-8 elements, values 1-50.
        Difficulty 5-6: 8-10 elements, values 1-100.
        Difficulty 7-8: 10-14 elements, values 1-200.

    Prerequisites:
        sorting.

    Example:
        >>> gen = LISGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'lis'
    """

    _LEN_RANGES = {
        1: (4, 6), 2: (4, 6), 3: (6, 8), 4: (6, 8),
        5: (8, 10), 6: (8, 10), 7: (10, 14), 8: (10, 14),
    }

    _VAL_RANGES = {
        1: (1, 20), 2: (1, 20), 3: (1, 50), 4: (1, 50),
        5: (1, 100), 6: (1, 100), 7: (1, 200), 8: (1, 200),
    }

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "lis"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["sorting"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls sequence length.

        Returns:
            Natural language description.
        """
        return "find length of longest increasing subsequence"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a sequence and compute LIS length.

        Args:
            difficulty: Controls sequence length and value range.

        Returns:
            Tuple of (problem_string, solution_data).
        """
        len_lo, len_hi = self._LEN_RANGES.get(difficulty, (6, 8))
        val_lo, val_hi = self._VAL_RANGES.get(difficulty, (1, 50))
        length = self._rng.randint(len_lo, len_hi)
        seq = [self._rng.randint(val_lo, val_hi) for _ in range(length)]
        tails_history = self._patience_sort(seq)
        seq_str = ",".join(str(x) for x in seq)
        return f"lis({seq_str})", {
            "seq": seq, "tails_history": tails_history,
        }

    def _patience_sort(self, seq: list[int]) -> list[list[int]]:
        """Run patience sorting and record tails state after each element.

        Args:
            seq: Input sequence.

        Returns:
            List of tails array snapshots (one per element).
        """
        tails: list[int] = []
        history: list[list[int]] = []
        for val in seq:
            pos = self._bisect_left(tails, val)
            if pos == len(tails):
                tails.append(val)
            else:
                tails[pos] = val
            history.append(list(tails))
        return history

    def _bisect_left(self, arr: list[int], val: int) -> int:
        """Find leftmost position where val can be inserted.

        Args:
            arr: Sorted array.
            val: Value to insert.

        Returns:
            Insertion index.
        """
        lo, hi = 0, len(arr)
        while lo < hi:
            mid = (lo + hi) // 2
            if arr[mid] < val:
                lo = mid + 1
            else:
                hi = mid
        return lo

    def _create_steps(self, data: dict) -> list[str]:
        """Generate patience sorting steps.

        Args:
            data: Solution data with tails history.

        Returns:
            Steps showing the tails array after each element.
        """
        seq = data["seq"]
        history = data["tails_history"]
        steps: list[str] = []
        for val, tails in zip(seq, history):
            tails_str = ",".join(str(t) for t in tails)
            steps.append(f"process {val}: tails=[{tails_str}]")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the LIS length.

        Args:
            data: Solution data.

        Returns:
            String representation of the LIS length.
        """
        return str(len(data["tails_history"][-1]))


@register
class PolynomialMultiplyGenerator(StepGenerator):
    """Multiply two polynomials term by term.

    Generates two polynomials with small integer coefficients
    and shows each pairwise term multiplication followed by
    collection of like terms.

    Input format:
        ``multiply two polynomials``

    Target format:
        ``(x+2)(x-3) <step> x \\cdot x=x^2 <step> x \\cdot(-3)=-3x
        <step> 2 \\cdot x=2x <step> 2 \\cdot(-3)=-6 <step> x^2-x-6``

    Difficulty scaling:
        Difficulty 1-2: two linear polynomials (degree 1).
        Difficulty 3-4: one linear, one quadratic.
        Difficulty 5-6: two quadratics.
        Difficulty 7-8: one quadratic, one cubic.

    Prerequisites:
        polynomial_eval, multiplication.

    Example:
        >>> gen = PolynomialMultiplyGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'polynomial_multiply'
    """

    _DEGREE_PAIRS = {
        1: (1, 1), 2: (1, 1), 3: (1, 2), 4: (1, 2),
        5: (2, 2), 6: (2, 2), 7: (2, 3), 8: (2, 3),
    }

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "polynomial_multiply"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["polynomial_eval", "multiplication"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls polynomial degrees.

        Returns:
            Natural language description.
        """
        return "multiply two polynomials"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate two polynomials and compute their product.

        Args:
            difficulty: Controls degree of the polynomials.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        d1, d2 = self._DEGREE_PAIRS.get(difficulty, (1, 2))
        p1 = self._random_poly(d1)
        p2 = self._random_poly(d2)
        product = self._multiply(p1, p2)
        p1_str = self._format_poly(p1)
        p2_str = self._format_poly(p2)
        return (
            f"({p1_str})({p2_str})",
            {"p1": p1, "p2": p2, "product": product,
             "p1_str": p1_str, "p2_str": p2_str},
        )

    def _random_poly(self, degree: int) -> list[tuple[int, int]]:
        """Generate a polynomial as a list of (coeff, power) pairs.

        Coefficients are non-zero integers in [-5, 5].

        Args:
            degree: Maximum degree of the polynomial.

        Returns:
            List of (coefficient, power) pairs, highest power first.
        """
        terms: list[tuple[int, int]] = []
        for power in range(degree, -1, -1):
            coeff = self._rng.randint(-5, 5)
            if coeff == 0:
                coeff = 1
            terms.append((coeff, power))
        return terms

    def _multiply(self, p1: list[tuple[int, int]],
                  p2: list[tuple[int, int]]) -> list[tuple[int, int]]:
        """Multiply two polynomials and collect like terms.

        Args:
            p1: First polynomial as (coeff, power) pairs.
            p2: Second polynomial as (coeff, power) pairs.

        Returns:
            Product polynomial as sorted (coeff, power) pairs.
        """
        result: dict[int, int] = {}
        for c1, e1 in p1:
            for c2, e2 in p2:
                power = e1 + e2
                result[power] = result.get(power, 0) + c1 * c2
        return [
            (c, p) for p, c in sorted(result.items(), reverse=True)
            if c != 0
        ]

    def _format_poly(self, poly: list[tuple[int, int]]) -> str:
        """Format a polynomial as a string.

        Args:
            poly: List of (coefficient, power) pairs.

        Returns:
            Formatted polynomial string.
        """
        parts: list[str] = []
        for i, (c, p) in enumerate(poly):
            parts.append(self._format_term(c, p, is_first=(i == 0)))
        return "".join(parts) if parts else "0"

    def _format_term(self, coeff: int, power: int,
                     is_first: bool) -> str:
        """Format a single polynomial term.

        Args:
            coeff: Coefficient value.
            power: Exponent.
            is_first: Whether this is the leading term.

        Returns:
            Formatted term string.
        """
        sign = self._sign_prefix(coeff, is_first)
        body = self._term_body(abs(coeff), power)
        return f"{sign}{body}"

    def _sign_prefix(self, coeff: int, is_first: bool) -> str:
        """Determine the sign prefix for a term.

        Args:
            coeff: Coefficient value.
            is_first: Whether this is the leading term.

        Returns:
            Sign string.
        """
        if is_first:
            return "-" if coeff < 0 else ""
        return "-" if coeff < 0 else "+"

    def _term_body(self, abs_coeff: int, power: int) -> str:
        """Format the body of a polynomial term.

        Args:
            abs_coeff: Absolute coefficient value.
            power: Exponent.

        Returns:
            Term body string.
        """
        if power == 0:
            return str(abs_coeff)
        if power == 1:
            return "x" if abs_coeff == 1 else f"{abs_coeff}x"
        if abs_coeff == 1:
            return f"x^{power}"
        return f"{abs_coeff}x^{power}"

    def _create_steps(self, data: dict) -> list[str]:
        """Generate pairwise multiplication steps.

        Args:
            data: Solution data with both polynomials and product.

        Returns:
            Steps showing each term multiplication.
        """
        p1, p2 = data["p1"], data["p2"]
        steps: list[str] = []
        for c1, e1 in p1:
            for c2, e2 in p2:
                steps.append(self._format_mult_step(c1, e1, c2, e2))
        return steps

    def _format_mult_step(self, c1: int, e1: int,
                          c2: int, e2: int) -> str:
        """Format one term-by-term multiplication step.

        Args:
            c1: Coefficient of first term.
            e1: Exponent of first term.
            c2: Coefficient of second term.
            e2: Exponent of second term.

        Returns:
            Step string showing the multiplication.
        """
        t1 = self._term_body(abs(c1), e1)
        if c1 < 0:
            t1 = f"(-{t1})"
        t2 = self._term_body(abs(c2), e2)
        if c2 < 0:
            t2 = f"(-{t2})"
        product_c = c1 * c2
        product_e = e1 + e2
        result = self._term_body(abs(product_c), product_e)
        if product_c < 0:
            result = f"-{result}"
        return f"{t1} \\cdot {t2}={result}"

    def _create_answer(self, data: dict) -> str:
        """Return the product polynomial.

        Args:
            data: Solution data.

        Returns:
            Formatted product polynomial string.
        """
        return self._format_poly(data["product"])


@register
class BayesTheoremGenerator(StepGenerator):
    """Apply Bayes' theorem to compute a posterior probability.

    Generates prior P(A), likelihood P(B|A), and marginal P(B)
    using simple fractions for clean computation. Shows the
    formula substitution and arithmetic steps.

    Input format:
        ``apply bayes theorem``

    Target format:
        ``P(A|B) = \\frac{P(B|A)P(A)}{P(B)} <step>
        P(B|A)P(A)=\\frac{3}{4} \\cdot \\frac{1}{3}=\\frac{1}{4}
        <step> P(B)=\\frac{1}{2} <step>
        \\frac{1/4}{1/2}=\\frac{1}{2} <step> 1/2``

    Difficulty scaling:
        Difficulty 1-2: denominators from [2, 4].
        Difficulty 3-4: denominators from [2, 6].
        Difficulty 5-6: denominators from [2, 8].
        Difficulty 7-8: denominators from [2, 10].

    Prerequisites:
        multiplication, division.

    Example:
        >>> gen = BayesTheoremGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'bayes_theorem'
    """

    _DENOM_RANGES = {
        1: (2, 4), 2: (2, 4), 3: (2, 6), 4: (2, 6),
        5: (2, 8), 6: (2, 8), 7: (2, 10), 8: (2, 10),
    }

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "bayes_theorem"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["multiplication", "division"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls fraction complexity.

        Returns:
            Natural language description.
        """
        return "apply bayes theorem"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate Bayes' theorem problem with simple fractions.

        Ensures P(B) >= P(B|A)*P(A) for valid probabilities and
        that all values are proper fractions.

        Args:
            difficulty: Controls denominator range.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        lo, hi = self._DENOM_RANGES.get(difficulty, (2, 6))
        p_a, p_ba, p_b, posterior = self._sample_valid_probabilities(lo, hi)
        return (
            f"P(A|B) = \\frac{{P(B|A)P(A)}}{{P(B)}}",
            {"p_a": p_a, "p_ba": p_ba, "p_b": p_b, "posterior": posterior},
        )

    def _sample_valid_probabilities(self, lo: int, hi: int
                                    ) -> tuple[Fraction, Fraction, Fraction, Fraction]:
        """Sample valid probability fractions for Bayes' theorem.

        Ensures all probabilities are in (0, 1] and P(B) >= P(B|A)*P(A).

        Args:
            lo: Minimum denominator.
            hi: Maximum denominator.

        Returns:
            Tuple of (P(A), P(B|A), P(B), posterior).
        """
        for _ in range(200):
            p_a = self._random_fraction(lo, hi)
            p_ba = self._random_fraction(lo, hi)
            numerator = p_ba * p_a
            if numerator <= 0:
                continue
            p_b = self._random_fraction_gte(numerator, lo, hi)
            if p_b is None or p_b > 1:
                continue
            posterior = numerator / p_b
            if posterior <= 1:
                return p_a, p_ba, p_b, posterior
        return (
            Fraction(1, 2), Fraction(1, 2),
            Fraction(1, 2), Fraction(1, 2),
        )

    def _random_fraction(self, lo: int, hi: int) -> Fraction:
        """Generate a random proper fraction.

        Args:
            lo: Minimum denominator.
            hi: Maximum denominator.

        Returns:
            Fraction in (0, 1].
        """
        denom = self._rng.randint(lo, hi)
        numer = self._rng.randint(1, denom)
        return Fraction(numer, denom)

    def _random_fraction_gte(self, minimum: Fraction, lo: int,
                             hi: int) -> Fraction | None:
        """Generate a random fraction >= minimum and <= 1.

        Args:
            minimum: Lower bound for the fraction.
            lo: Minimum denominator.
            hi: Maximum denominator.

        Returns:
            Fraction >= minimum, or None if no valid fraction found.
        """
        for _ in range(50):
            f = self._random_fraction(lo, hi)
            if f >= minimum:
                return f
        return None

    def _format_fraction(self, f: Fraction) -> str:
        """Format a Fraction as a LaTeX string.

        Args:
            f: Fraction to format.

        Returns:
            LaTeX fraction string.
        """
        if f.denominator == 1:
            return str(f.numerator)
        return f"\\frac{{{f.numerator}}}{{{f.denominator}}}"

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Bayes' theorem computation steps.

        Args:
            data: Solution data with probabilities.

        Returns:
            Steps showing numerator, denominator, and division.
        """
        p_a = data["p_a"]
        p_ba = data["p_ba"]
        p_b = data["p_b"]
        numerator = p_ba * p_a
        posterior = data["posterior"]

        return [
            f"P(B|A)P(A)={self._format_fraction(p_ba)} \\cdot {self._format_fraction(p_a)}={self._format_fraction(numerator)}",
            f"P(B)={self._format_fraction(p_b)}",
            f"\\frac{{{self._format_fraction(numerator)}}}{{{self._format_fraction(p_b)}}}={self._format_fraction(posterior)}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the posterior probability.

        Args:
            data: Solution data.

        Returns:
            Fraction string of the posterior.
        """
        p = data["posterior"]
        if p.denominator == 1:
            return str(p.numerator)
        return f"{p.numerator}/{p.denominator}"
