"""Generators for tasks related to open problems in mathematics.

The model cannot solve the open problems themselves, but learns the
mathematical structures they are built on: partial sums, primality
testing, factorisation, modular arithmetic, and number-theoretic
predicates.

Open problems represented:
    Riemann Hypothesis (zeta partial sums, Euler product)
    Goldbach's Conjecture (prime partition of even numbers)
    Twin Prime Conjecture (searching for twin prime pairs)
    Erdos-Straus Conjecture (Egyptian fraction decomposition)
    Legendre's Conjecture (primes between consecutive squares)
    Waring's Problem (sums of k-th powers)
    ABC Conjecture (radical of product, quality of triples)
    Beal's Conjecture (perfect power sums and common factors)
    Brocard's Problem (n! + 1 perfect square check)
    P vs NP (SAT instance verification)
    Perfect Numbers (sum of divisors, Mersenne connection)
"""
import math
from fractions import Fraction

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


class PrimeHelper:
    """Shared prime utilities for open problem generators.

    Provides primality testing, factorisation, and prime generation
    used across multiple generators in this module.
    """

    @staticmethod
    def is_prime(n: int) -> bool:
        """Test primality by trial division.

        Args:
            n: Integer to test.

        Returns:
            True if n is prime.
        """
        if n < 2:
            return False
        if n < 4:
            return True
        if n % 2 == 0 or n % 3 == 0:
            return False
        i = 5
        while i * i <= n:
            if n % i == 0 or n % (i + 2) == 0:
                return False
            i += 6
        return True

    @staticmethod
    def prime_factors(n: int) -> list[int]:
        """Return sorted list of distinct prime factors.

        Args:
            n: Positive integer to factorise.

        Returns:
            Sorted list of distinct primes dividing n.
        """
        factors = set()
        d = 2
        temp = n
        while d * d <= temp:
            while temp % d == 0:
                factors.add(d)
                temp //= d
            d += 1
        if temp > 1:
            factors.add(temp)
        return sorted(factors)

    @staticmethod
    def primes_up_to(limit: int) -> list[int]:
        """Generate all primes up to limit using sieve.

        Args:
            limit: Upper bound (inclusive).

        Returns:
            List of primes up to limit.
        """
        if limit < 2:
            return []
        sieve = [True] * (limit + 1)
        sieve[0] = sieve[1] = False
        for i in range(2, int(limit**0.5) + 1):
            if sieve[i]:
                for j in range(i * i, limit + 1, i):
                    sieve[j] = False
        return [i for i in range(2, limit + 1) if sieve[i]]

    @staticmethod
    def proper_divisors(n: int) -> list[int]:
        """Return sorted proper divisors of n (excluding n itself).

        Args:
            n: Positive integer.

        Returns:
            Sorted list of proper divisors.
        """
        if n <= 1:
            return []
        divs = [1]
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                divs.append(i)
                if i != n // i:
                    divs.append(n // i)
        return sorted(divs)


@register
class ZetaPartialSumGenerator(StepGenerator):
    """Compute partial sums of the Riemann zeta function.

    Evaluates zeta_k(s) = sum_{n=1}^{k} 1/n^s as an exact fraction,
    connecting to the Riemann Hypothesis which governs the behaviour
    of the full infinite sum.

    Difficulty scaling:
        Difficulty 1-3: s=2, k=2-4 terms.
        Difficulty 4-6: s=2-3, k=3-6 terms.
        Difficulty 7-8: s=2-4, k=4-8 terms.

    Prerequisites:
        exponentiation, division, addition.
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "zeta_partial_sum"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["exponentiation", "division", "addition"]

    def task_description(self, difficulty: int) -> str:
        """Generate a task description.

        Args:
            difficulty: Problem difficulty level.

        Returns:
            Natural language description.
        """
        return "compute partial sum of Riemann zeta function"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a zeta partial sum problem.

        Args:
            difficulty: Controls s and k ranges.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            s = 2
            k = self._rng.randint(2, 2 + difficulty)
        elif difficulty <= 6:
            s = self._rng.randint(2, 3)
            k = self._rng.randint(3, 3 + difficulty)
        else:
            s = self._rng.randint(2, 4)
            k = self._rng.randint(4, 4 + difficulty)

        terms = []
        total = Fraction(0)
        for n in range(1, k + 1):
            term = Fraction(1, n ** s)
            terms.append(term)
            total += term

        problem = (
            f"\\zeta_{{{k}}}({s}) = "
            f"\\sum_{{n=1}}^{{{k}}} \\frac{{1}}{{n^{{{s}}}}}"
        )
        return problem, {"s": s, "k": k, "terms": terms, "total": total}

    def _create_steps(self, data: dict) -> list[str]:
        """Generate step-by-step partial sum computation.

        Args:
            data: Solution data with terms and total.

        Returns:
            Steps showing each term and running sum.
        """
        steps = []
        running = Fraction(0)
        for i, term in enumerate(data["terms"]):
            n = i + 1
            running += term
            steps.append(f"n={n}: 1/{n}^{data['s']} = {term}")
        steps.append(f"sum = {data['total']}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the partial sum as a fraction.

        Args:
            data: Solution data.

        Returns:
            Fraction string in lowest terms.
        """
        t = data["total"]
        return f"{t.numerator}/{t.denominator}"


@register
class EulerProductGenerator(StepGenerator):
    """Compute Euler product approximation of the zeta function.

    Evaluates prod_{p<=P} 1/(1 - p^{-s}) for the first k primes,
    demonstrating Euler's proof that the zeta function encodes
    prime distribution.

    Difficulty scaling:
        Difficulty 1-3: k=2 primes, s=2.
        Difficulty 4-6: k=2-3 primes, s=2-3.
        Difficulty 7-8: k=3-4 primes, s=2-4.

    Prerequisites:
        primality, exponentiation, multiplication.
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "euler_product"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["primality", "exponentiation", "multiplication"]

    def task_description(self, difficulty: int) -> str:
        """Generate a task description.

        Args:
            difficulty: Problem difficulty level.

        Returns:
            Natural language description.
        """
        return "compute Euler product for zeta function"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an Euler product problem.

        Args:
            difficulty: Controls number of primes and s value.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            k, s = 2, 2
        elif difficulty <= 6:
            k = self._rng.randint(2, 3)
            s = self._rng.randint(2, 3)
        else:
            k = self._rng.randint(3, 4)
            s = self._rng.randint(2, 4)

        primes = [2, 3, 5, 7, 11][:k]
        factors = []
        product = Fraction(1)
        for p in primes:
            denom = 1 - Fraction(1, p ** s)
            factor = Fraction(1) / denom
            factors.append((p, factor))
            product *= factor

        prime_str = ", ".join(str(p) for p in primes)
        problem = (
            f"\\prod_{{p \\in \\{{{prime_str}\\}}}} "
            f"\\frac{{1}}{{1 - p^{{-{s}}}}}"
        )
        return problem, {
            "s": s, "primes": primes,
            "factors": factors, "product": product,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate step-by-step Euler product computation.

        Args:
            data: Solution data with factors.

        Returns:
            Steps showing each prime's factor and running product.
        """
        steps = []
        running = Fraction(1)
        for p, factor in data["factors"]:
            running *= factor
            steps.append(
                f"p={p}: 1/(1 - 1/{p}^{data['s']}) = {factor}"
            )
        steps.append(f"product = {data['product']}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the Euler product as a fraction.

        Args:
            data: Solution data.

        Returns:
            Fraction string in lowest terms.
        """
        p = data["product"]
        return f"{p.numerator}/{p.denominator}"


@register
class GoldbachPartitionGenerator(StepGenerator):
    """Find two primes that sum to an even number (Goldbach's conjecture).

    Given even n >= 4, find primes p1 <= p2 such that p1 + p2 = n.
    Goldbach's conjecture (1742) states this is always possible.
    Verified up to 4*10^18 but unproven.

    Difficulty scaling:
        Difficulty 1-3: n = 6-20.
        Difficulty 4-6: n = 20-100.
        Difficulty 7-8: n = 100-500.

    Prerequisites:
        primality, addition.
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "goldbach_partition"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["primality", "addition"]

    def task_description(self, difficulty: int) -> str:
        """Generate a task description.

        Args:
            difficulty: Problem difficulty level.

        Returns:
            Natural language description.
        """
        return "find two primes that sum to the given even number"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Goldbach partition problem.

        Args:
            difficulty: Controls the size of n.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            n = self._rng.randrange(6, 22, 2)
        elif difficulty <= 6:
            n = self._rng.randrange(20, 102, 2)
        else:
            n = self._rng.randrange(100, 502, 2)

        p1, p2 = self._find_partition(n)
        tested = []
        for candidate in range(2, n):
            if PrimeHelper.is_prime(candidate):
                complement = n - candidate
                tested.append(candidate)
                if PrimeHelper.is_prime(complement) and candidate <= complement:
                    break

        problem = f"{n} = p_1 + p_2"
        return problem, {
            "n": n, "p1": p1, "p2": p2, "tested": tested,
        }

    def _find_partition(self, n: int) -> tuple[int, int]:
        """Find the smallest prime pair summing to n.

        Args:
            n: Even integer >= 4.

        Returns:
            Tuple (p1, p2) with p1 <= p2.
        """
        for p in range(2, n):
            if PrimeHelper.is_prime(p) and PrimeHelper.is_prime(n - p):
                return (p, n - p)
        return (0, 0)

    def _create_steps(self, data: dict) -> list[str]:
        """Generate search steps showing tested primes.

        Args:
            data: Solution data with tested primes.

        Returns:
            Steps showing the search process.
        """
        steps = []
        n = data["n"]
        for p in data["tested"]:
            complement = n - p
            is_p = PrimeHelper.is_prime(complement)
            status = "prime" if is_p else "not prime"
            steps.append(f"try {p}: {n}-{p}={complement} ({status})")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the prime partition.

        Args:
            data: Solution data.

        Returns:
            String 'p1 + p2'.
        """
        return f"{data['p1']} + {data['p2']}"


@register
class TwinPrimeSearchGenerator(StepGenerator):
    """Find the next twin prime pair after a given number.

    Twin primes are pairs (p, p+2) where both are prime.
    The Twin Prime Conjecture states there are infinitely many.
    Proven: infinitely many pairs with gap <= 246 (Zhang/Maynard).

    Difficulty scaling:
        Difficulty 1-3: search from n = 1-20.
        Difficulty 4-6: search from n = 20-100.
        Difficulty 7-8: search from n = 100-500.

    Prerequisites:
        primality.
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "twin_prime_search"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["primality"]

    def task_description(self, difficulty: int) -> str:
        """Generate a task description.

        Args:
            difficulty: Problem difficulty level.

        Returns:
            Natural language description.
        """
        return "find the next twin prime pair (p, p+2) after n"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a twin prime search problem.

        Args:
            difficulty: Controls the starting point.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            n = self._rng.randint(1, 20)
        elif difficulty <= 6:
            n = self._rng.randint(20, 100)
        else:
            n = self._rng.randint(100, 500)

        p, tested = self._find_twin_after(n)
        problem = f"\\text{{twin prime pair after }} {n}"
        return problem, {"n": n, "p": p, "tested": tested}

    def _find_twin_after(self, n: int) -> tuple[int, list[int]]:
        """Find the first twin prime pair (p, p+2) with p > n.

        Args:
            n: Starting point.

        Returns:
            Tuple of (p, list_of_candidates_tested).
        """
        tested = []
        candidate = n + 1
        while True:
            if PrimeHelper.is_prime(candidate):
                tested.append(candidate)
                if PrimeHelper.is_prime(candidate + 2):
                    return candidate, tested
            candidate += 1

    def _create_steps(self, data: dict) -> list[str]:
        """Generate search steps.

        Args:
            data: Solution data with tested candidates.

        Returns:
            Steps showing tested primes.
        """
        steps = []
        for p in data["tested"]:
            twin_prime = PrimeHelper.is_prime(p + 2)
            status = "twin!" if twin_prime else f"{p+2} not prime"
            steps.append(f"p={p}: p+2={p+2} ({status})")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the twin prime pair.

        Args:
            data: Solution data.

        Returns:
            String '(p, p+2)'.
        """
        p = data["p"]
        return f"({p}, {p + 2})"


@register
class PerfectNumberCheckGenerator(StepGenerator):
    """Check if a number is perfect (equals sum of proper divisors).

    Connected to Mersenne primes: every even perfect number has
    form 2^{p-1}(2^p - 1) where 2^p - 1 is prime. Whether odd
    perfect numbers exist is an open problem (none found).

    Difficulty scaling:
        Difficulty 1-3: n in 1-30 (includes 6, 28).
        Difficulty 4-6: n in 10-200 (includes 496 at high end).
        Difficulty 7-8: n in 50-1000.

    Prerequisites:
        division, addition.
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "perfect_number_check"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["division", "addition"]

    def task_description(self, difficulty: int) -> str:
        """Generate a task description.

        Args:
            difficulty: Problem difficulty level.

        Returns:
            Natural language description.
        """
        return "check if number is perfect (sum of proper divisors)"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a perfect number check problem.

        Mixes known perfect numbers with non-perfect numbers
        for balanced training.

        Args:
            difficulty: Controls number range.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        perfects = [6, 28, 496, 8128]
        if difficulty <= 3:
            pool = list(range(2, 31))
        elif difficulty <= 6:
            pool = list(range(10, 201))
        else:
            pool = list(range(50, 501))

        for p in perfects:
            if p not in pool and p <= max(pool):
                pool.append(p)

        n = self._rng.choice(pool)
        divisors = PrimeHelper.proper_divisors(n)
        div_sum = sum(divisors)
        is_perfect = div_sum == n

        problem = f"\\sigma_0({n}) = {n}?"
        return problem, {
            "n": n, "divisors": divisors,
            "div_sum": div_sum, "is_perfect": is_perfect,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate steps showing divisor computation.

        Args:
            data: Solution data with divisors.

        Returns:
            Steps showing divisors and their sum.
        """
        n = data["n"]
        divs = data["divisors"]
        steps = [
            f"proper divisors of {n}: {', '.join(str(d) for d in divs)}",
            f"sum = {' + '.join(str(d) for d in divs)} = {data['div_sum']}",
        ]
        if data["is_perfect"]:
            steps.append(f"{data['div_sum']} = {n}, perfect")
        else:
            steps.append(f"{data['div_sum']} != {n}, not perfect")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return perfect number verdict.

        Args:
            data: Solution data.

        Returns:
            'perfect' or 'not perfect, sum=X'.
        """
        if data["is_perfect"]:
            return "perfect"
        return f"not perfect, sum={data['div_sum']}"


@register
class ErdosStrausGenerator(StepGenerator):
    """Decompose 4/n into a sum of three unit fractions.

    The Erdos-Straus conjecture (1948) states that for every n >= 2,
    4/n = 1/a + 1/b + 1/c has a solution in positive integers.
    Verified for n up to 10^17 but unproven.

    Difficulty scaling:
        Difficulty 1-3: n = 2-10.
        Difficulty 4-6: n = 10-50.
        Difficulty 7-8: n = 50-200.

    Prerequisites:
        division, addition.
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "erdos_straus"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["division", "addition"]

    def task_description(self, difficulty: int) -> str:
        """Generate a task description.

        Args:
            difficulty: Problem difficulty level.

        Returns:
            Natural language description.
        """
        return "decompose 4/n as sum of three unit fractions"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an Erdos-Straus decomposition problem.

        Args:
            difficulty: Controls n range.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            n = self._rng.randint(2, 10)
        elif difficulty <= 6:
            n = self._rng.randint(10, 50)
        else:
            n = self._rng.randint(50, 200)

        a, b, c = self._find_decomposition(n)
        problem = f"\\frac{{4}}{{{n}}} = \\frac{{1}}{{a}} + \\frac{{1}}{{b}} + \\frac{{1}}{{c}}"
        return problem, {"n": n, "a": a, "b": b, "c": c}

    def _find_decomposition(self, n: int) -> tuple[int, int, int]:
        """Find a, b, c such that 4/n = 1/a + 1/b + 1/c.

        Uses a greedy approach: try small values of a, then solve
        the remaining 2-fraction Egyptian fraction problem.

        Args:
            n: Denominator (>= 2).

        Returns:
            Tuple (a, b, c) with a <= b <= c.
        """
        target = Fraction(4, n)
        ceil_recip = math.ceil(1 / float(target))
        for a in range(ceil_recip, 10 * n):
            remainder = target - Fraction(1, a)
            if remainder <= 0:
                continue
            ceil_b = math.ceil(1 / float(remainder))
            for b in range(max(a, ceil_b), 10 * n):
                rest = remainder - Fraction(1, b)
                if rest <= 0:
                    continue
                if rest.numerator == 1:
                    c = rest.denominator
                    return (a, b, c)
        return (1, 1, 1)

    def _create_steps(self, data: dict) -> list[str]:
        """Generate decomposition steps.

        Args:
            data: Solution data with a, b, c.

        Returns:
            Steps showing the decomposition and verification.
        """
        n, a, b, c = data["n"], data["a"], data["b"], data["c"]
        total = Fraction(1, a) + Fraction(1, b) + Fraction(1, c)
        return [
            f"4/{n} = 1/{a} + 1/{b} + 1/{c}",
            f"verify: 1/{a} + 1/{b} + 1/{c} = {total}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the unit fraction decomposition.

        Args:
            data: Solution data.

        Returns:
            String '1/a + 1/b + 1/c'.
        """
        return f"1/{data['a']} + 1/{data['b']} + 1/{data['c']}"


@register
class LegendrePrimeGenerator(StepGenerator):
    """Find a prime between consecutive perfect squares.

    Legendre's conjecture (1798) states that for every n >= 1,
    there exists a prime p with n^2 < p < (n+1)^2.
    Unproven, though Ingham (1937) showed there is always a
    prime between n^3 and (n+1)^3.

    Difficulty scaling:
        Difficulty 1-3: n = 1-5.
        Difficulty 4-6: n = 5-15.
        Difficulty 7-8: n = 15-30.

    Prerequisites:
        exponentiation, primality.
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "legendre_prime"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["exponentiation", "primality"]

    def task_description(self, difficulty: int) -> str:
        """Generate a task description.

        Args:
            difficulty: Problem difficulty level.

        Returns:
            Natural language description.
        """
        return "find a prime between n^2 and (n+1)^2"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Legendre's conjecture problem.

        Args:
            difficulty: Controls n range.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            n = self._rng.randint(1, 5)
        elif difficulty <= 6:
            n = self._rng.randint(5, 15)
        else:
            n = self._rng.randint(15, 30)

        lo = n * n
        hi = (n + 1) * (n + 1)
        primes_in_range = [
            p for p in range(lo + 1, hi) if PrimeHelper.is_prime(p)
        ]
        chosen = self._rng.choice(primes_in_range)

        problem = f"{lo} < p < {hi}"
        return problem, {
            "n": n, "lo": lo, "hi": hi,
            "prime": chosen, "all_primes": primes_in_range,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate search steps.

        Args:
            data: Solution data with bounds and primes.

        Returns:
            Steps showing bounds computation and prime found.
        """
        n = data["n"]
        return [
            f"n={n}: n^2={data['lo']}, (n+1)^2={data['hi']}",
            f"primes in ({data['lo']}, {data['hi']}): "
            f"{', '.join(str(p) for p in data['all_primes'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return a prime between the consecutive squares.

        Args:
            data: Solution data.

        Returns:
            The chosen prime as a string.
        """
        return str(data["prime"])


@register
class WaringRepresentationGenerator(StepGenerator):
    """Express a number as a sum of k-th powers (Waring's problem).

    Waring's problem (1770): for each k, what is the minimum g(k)
    such that every positive integer is a sum of at most g(k) k-th
    powers? Solved for g(k) but the related G(k) (sufficiently
    large n) is still open for most k.

    Difficulty scaling:
        Difficulty 1-3: squares (k=2), n = 1-30.
        Difficulty 4-6: cubes (k=3), n = 1-50.
        Difficulty 7-8: 4th powers (k=4), n = 1-100.

    Prerequisites:
        exponentiation, subtraction.
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "waring_representation"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["exponentiation", "subtraction"]

    def task_description(self, difficulty: int) -> str:
        """Generate a task description.

        Args:
            difficulty: Problem difficulty level.

        Returns:
            Natural language description.
        """
        return "express number as sum of minimum k-th powers"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Waring representation problem.

        Args:
            difficulty: Controls k and n ranges.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            k = 2
            n = self._rng.randint(1, 30)
        elif difficulty <= 6:
            k = 3
            n = self._rng.randint(1, 50)
        else:
            k = 4
            n = self._rng.randint(1, 100)

        terms = self._greedy_decompose(n, k)
        problem = f"{n} = \\sum a_i^{{{k}}}"
        return problem, {"n": n, "k": k, "terms": terms}

    def _greedy_decompose(self, n: int, k: int) -> list[int]:
        """Decompose n into k-th powers using greedy algorithm.

        Takes the largest k-th power that fits at each step.

        Args:
            n: Number to decompose.
            k: Power to use.

        Returns:
            List of bases whose k-th powers sum to n.
        """
        remainder = n
        terms = []
        while remainder > 0:
            base = int(remainder ** (1.0 / k))
            while (base + 1) ** k <= remainder:
                base += 1
            terms.append(base)
            remainder -= base ** k
        return terms

    def _create_steps(self, data: dict) -> list[str]:
        """Generate decomposition steps.

        Args:
            data: Solution data with terms.

        Returns:
            Steps showing greedy decomposition.
        """
        steps = []
        remainder = data["n"]
        k = data["k"]
        for base in data["terms"]:
            power = base ** k
            steps.append(f"{base}^{k}={power}, remainder={remainder - power}")
            remainder -= power
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the power sum representation.

        Args:
            data: Solution data.

        Returns:
            String like '3^2 + 2^2 + 1^2'.
        """
        k = data["k"]
        parts = [f"{b}^{k}" for b in data["terms"]]
        return " + ".join(parts)


@register
class ABCTripleGenerator(StepGenerator):
    """Compute the radical and quality of an ABC triple.

    The ABC conjecture (Masser-Oesterle, 1985) states that for
    coprime a + b = c, the radical rad(abc) is usually not much
    smaller than c. Quality q = log(c)/log(rad(abc)).
    A triple with q > 1 is called an ABC hit.

    Difficulty scaling:
        Difficulty 1-3: a, b in 1-20.
        Difficulty 4-6: a, b in 10-100.
        Difficulty 7-8: a, b in 50-300.

    Prerequisites:
        factorisation, gcd.
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "abc_triple"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["factorisation", "gcd"]

    def task_description(self, difficulty: int) -> str:
        """Generate a task description.

        Args:
            difficulty: Problem difficulty level.

        Returns:
            Natural language description.
        """
        return "compute radical and quality of ABC triple"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an ABC triple problem with coprime a, b.

        Args:
            difficulty: Controls value ranges.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            lo, hi = 1, 20
        elif difficulty <= 6:
            lo, hi = 10, 100
        else:
            lo, hi = 50, 300

        for _ in range(100):
            a = self._rng.randint(lo, hi)
            b = self._rng.randint(lo, hi)
            if a != b and math.gcd(a, b) == 1:
                break

        if a > b:
            a, b = b, a
        c = a + b

        all_factors = set()
        for x in [a, b, c]:
            all_factors.update(PrimeHelper.prime_factors(x))
        radical = 1
        for p in all_factors:
            radical *= p

        quality = math.log(c) / math.log(radical) if radical > 1 else 0

        problem = f"a={a}, b={b}, c=a+b={c}"
        return problem, {
            "a": a, "b": b, "c": c,
            "factors_a": PrimeHelper.prime_factors(a),
            "factors_b": PrimeHelper.prime_factors(b),
            "factors_c": PrimeHelper.prime_factors(c),
            "radical": radical,
            "quality": quality,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate steps showing factorisation and radical.

        Args:
            data: Solution data with factors and radical.

        Returns:
            Steps showing the computation.
        """
        return [
            f"a={data['a']}: primes={data['factors_a']}",
            f"b={data['b']}: primes={data['factors_b']}",
            f"c={data['c']}: primes={data['factors_c']}",
            f"rad(abc) = {'*'.join(str(p) for p in sorted(set(data['factors_a'] + data['factors_b'] + data['factors_c'])))} = {data['radical']}",
            f"quality = log({data['c']})/log({data['radical']}) = {data['quality']:.4f}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return radical and quality.

        Args:
            data: Solution data.

        Returns:
            String with radical and quality.
        """
        hit = "abc hit" if data["quality"] > 1 else "not abc hit"
        return f"rad={data['radical']}, q={data['quality']:.4f}, {hit}"


@register
class BealCheckGenerator(StepGenerator):
    """Check if A^x + B^y is a perfect power, verify Beal's conjecture.

    Beal's conjecture (1993, $1M prize): if A^x + B^y = C^z where
    A, B, C, x, y, z are positive integers with x, y, z > 2,
    then A, B, C share a common prime factor.

    The generator computes A^x + B^y and checks if the result
    is a perfect power.

    Difficulty scaling:
        Difficulty 1-3: A, B in 1-5, x, y in 3-4.
        Difficulty 4-6: A, B in 2-10, x, y in 3-5.
        Difficulty 7-8: A, B in 2-15, x, y in 3-6.

    Prerequisites:
        exponentiation, gcd.
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "beal_check"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["exponentiation", "gcd"]

    def task_description(self, difficulty: int) -> str:
        """Generate a task description.

        Args:
            difficulty: Problem difficulty level.

        Returns:
            Natural language description.
        """
        return "compute A^x + B^y and check if result is a perfect power"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Beal check problem.

        Args:
            difficulty: Controls value ranges.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            a = self._rng.randint(1, 5)
            b = self._rng.randint(1, 5)
            x = self._rng.randint(3, 4)
            y = self._rng.randint(3, 4)
        elif difficulty <= 6:
            a = self._rng.randint(2, 10)
            b = self._rng.randint(2, 10)
            x = self._rng.randint(3, 5)
            y = self._rng.randint(3, 5)
        else:
            a = self._rng.randint(2, 15)
            b = self._rng.randint(2, 15)
            x = self._rng.randint(3, 6)
            y = self._rng.randint(3, 6)

        ax = a ** x
        by = b ** y
        total = ax + by
        is_power, base, exp = self._check_perfect_power(total)
        g = math.gcd(a, b)

        problem = f"{a}^{{{x}}} + {b}^{{{y}}}"
        return problem, {
            "a": a, "b": b, "x": x, "y": y,
            "ax": ax, "by": by, "total": total,
            "is_power": is_power, "base": base, "exp": exp,
            "gcd_ab": g,
        }

    def _check_perfect_power(self, n: int) -> tuple[bool, int, int]:
        """Check if n is a perfect power c^z with z > 2.

        Args:
            n: Number to check.

        Returns:
            Tuple (is_perfect_power, base, exponent).
        """
        if n <= 1:
            return False, 0, 0
        for z in range(3, int(math.log2(n)) + 2):
            c = round(n ** (1.0 / z))
            for candidate in [c - 1, c, c + 1]:
                if candidate > 0 and candidate ** z == n:
                    return True, candidate, z
        return False, 0, 0

    def _create_steps(self, data: dict) -> list[str]:
        """Generate computation and check steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing power computation and perfect power check.
        """
        steps = [
            f"{data['a']}^{data['x']} = {data['ax']}",
            f"{data['b']}^{data['y']} = {data['by']}",
            f"sum = {data['total']}",
        ]
        if data["is_power"]:
            steps.append(
                f"{data['total']} = {data['base']}^{data['exp']} (perfect power)"
            )
            steps.append(f"gcd({data['a']}, {data['b']}) = {data['gcd_ab']}")
        else:
            steps.append(f"{data['total']} is not a perfect power")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the result of the Beal check.

        Args:
            data: Solution data.

        Returns:
            String describing the result.
        """
        if data["is_power"]:
            return (
                f"{data['total']} = {data['base']}^{data['exp']}, "
                f"gcd={data['gcd_ab']}"
            )
        return f"{data['total']}, not a perfect power"


@register
class BrocardCheckGenerator(StepGenerator):
    """Check if n! + 1 is a perfect square (Brocard's problem).

    Brocard's problem (1876): find all n where n! + 1 = m^2.
    Only three solutions known: (4,5), (5,11), (7,71).
    Conjectured that no others exist.

    Difficulty scaling:
        Difficulty 1-3: n = 1-7 (includes the 3 known solutions).
        Difficulty 4-6: n = 1-12.
        Difficulty 7-8: n = 1-15.

    Prerequisites:
        multiplication, exponentiation.
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "brocard_check"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["multiplication", "exponentiation"]

    def task_description(self, difficulty: int) -> str:
        """Generate a task description.

        Args:
            difficulty: Problem difficulty level.

        Returns:
            Natural language description.
        """
        return "check if n! + 1 is a perfect square"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Brocard check problem.

        Args:
            difficulty: Controls n range.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            n = self._rng.randint(1, 7)
        elif difficulty <= 6:
            n = self._rng.randint(1, 12)
        else:
            n = self._rng.randint(1, 15)

        factorial = math.factorial(n)
        value = factorial + 1
        sqrt_val = math.isqrt(value)
        is_square = sqrt_val * sqrt_val == value

        problem = f"{n}! + 1 = m^2?"
        return problem, {
            "n": n, "factorial": factorial, "value": value,
            "is_square": is_square, "sqrt": sqrt_val if is_square else None,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate computation steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing factorial and square check.
        """
        steps = [
            f"{data['n']}! = {data['factorial']}",
            f"{data['n']}! + 1 = {data['value']}",
        ]
        if data["is_square"]:
            steps.append(f"{data['value']} = {data['sqrt']}^2 (perfect square!)")
        else:
            sqrt_approx = math.isqrt(data["value"])
            steps.append(
                f"sqrt({data['value']}) ~ {sqrt_approx}, "
                f"{sqrt_approx}^2={sqrt_approx**2} != {data['value']}"
            )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the Brocard check result.

        Args:
            data: Solution data.

        Returns:
            Result string.
        """
        if data["is_square"]:
            return f"yes, {data['n']}! + 1 = {data['sqrt']}^2"
        return f"no, {data['value']} is not a perfect square"


@register
class SATVerifyGenerator(StepGenerator):
    """Verify if a variable assignment satisfies a CNF formula.

    Connected to P vs NP: SAT is NP-complete. Verification is
    polynomial (the model checks assignments), but finding a
    satisfying assignment is believed to be exponential.

    Difficulty scaling:
        Difficulty 1-3: 2-3 variables, 2-4 clauses.
        Difficulty 4-6: 3-4 variables, 4-6 clauses.
        Difficulty 7-8: 4-5 variables, 6-8 clauses.

    Prerequisites:
        boolean_eval.
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "sat_verify"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["boolean_eval"]

    def task_description(self, difficulty: int) -> str:
        """Generate a task description.

        Args:
            difficulty: Problem difficulty level.

        Returns:
            Natural language description.
        """
        return "verify if assignment satisfies CNF formula"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a SAT verification problem.

        Creates a random CNF formula and a random assignment,
        balanced 50/50 between satisfying and non-satisfying.

        Args:
            difficulty: Controls variable and clause count.

        Returns:
            Tuple of (problem_string, solution_data).
        """
        if difficulty <= 3:
            n_vars = self._rng.randint(2, 3)
            n_clauses = self._rng.randint(2, 4)
        elif difficulty <= 6:
            n_vars = self._rng.randint(3, 4)
            n_clauses = self._rng.randint(4, 6)
        else:
            n_vars = self._rng.randint(4, 5)
            n_clauses = self._rng.randint(6, 8)

        variables = [chr(ord('a') + i) for i in range(n_vars)]
        clauses = []
        for _ in range(n_clauses):
            clause_size = self._rng.randint(2, min(3, n_vars))
            clause_vars = self._rng.sample(variables, clause_size)
            clause = []
            for v in clause_vars:
                negated = self._rng.random() < 0.5
                clause.append(("~" + v if negated else v))
            clauses.append(clause)

        assignment = {v: self._rng.choice([True, False]) for v in variables}

        clause_results = []
        for clause in clauses:
            result = False
            for lit in clause:
                if lit.startswith("~"):
                    result = result or not assignment[lit[1:]]
                else:
                    result = result or assignment[lit]
            clause_results.append(result)

        satisfies = all(clause_results)
        first_fail = None
        if not satisfies:
            for i, r in enumerate(clause_results):
                if not r:
                    first_fail = i
                    break

        clause_strs = [
            "(" + " v ".join(clause) + ")" for clause in clauses
        ]
        formula = " ^ ".join(clause_strs)
        assign_str = ", ".join(
            f"{v}={'T' if val else 'F'}" for v, val in assignment.items()
        )
        problem = f"{formula}; {assign_str}"

        return problem, {
            "clauses": clauses, "assignment": assignment,
            "clause_results": clause_results,
            "satisfies": satisfies, "first_fail": first_fail,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate clause-by-clause evaluation steps.

        Args:
            data: Solution data with clause results.

        Returns:
            Steps showing each clause evaluation.
        """
        steps = []
        for i, (clause, result) in enumerate(
            zip(data["clauses"], data["clause_results"])
        ):
            status = "T" if result else "F"
            steps.append(f"clause {i+1}: ({' v '.join(clause)}) = {status}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return verification result.

        Args:
            data: Solution data.

        Returns:
            'satisfies' or 'fails clause N'.
        """
        if data["satisfies"]:
            return "satisfies"
        return f"fails clause {data['first_fail'] + 1}"
