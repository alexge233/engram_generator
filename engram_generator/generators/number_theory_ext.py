"""Extended number theory generators.

8 generators at tier 6 covering quadratic reciprocity, primitive roots,
sum of two squares, Moebius function, divisor function, Jacobi symbol,
Pell equation, and multiplicative order. Each produces step-by-step
solutions with LaTeX formatting.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

_SMALL_PRIMES = [
    2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47,
    53, 59, 61, 67, 71, 73, 79, 83, 89, 97,
]

_ODD_PRIMES = [p for p in _SMALL_PRIMES if p > 2]


def _is_prime(n: int) -> bool:
    """Check primality by trial division.

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


def _factorise(n: int) -> list[tuple[int, int]]:
    """Return the prime factorisation of n as (prime, exponent) pairs.

    Args:
        n: Positive integer to factorise.

    Returns:
        Sorted list of (prime, exponent) tuples.
    """
    factors: list[tuple[int, int]] = []
    d = 2
    while d * d <= n:
        exp = 0
        while n % d == 0:
            exp += 1
            n //= d
        if exp:
            factors.append((d, exp))
        d += 1
    if n > 1:
        factors.append((n, 1))
    return factors


def _euler_criterion(a: int, p: int) -> int:
    """Compute Legendre symbol (a/p) via Euler's criterion.

    Args:
        a: Integer.
        p: Odd prime.

    Returns:
        1 if a is a quadratic residue mod p, -1 if not, 0 if p divides a.
    """
    a = a % p
    if a == 0:
        return 0
    result = pow(a, (p - 1) // 2, p)
    return 1 if result == 1 else -1


def _cf_sqrt(d: int) -> list[int]:
    """Compute the periodic continued fraction of sqrt(d).

    Args:
        d: Non-square positive integer.

    Returns:
        List [a0, a1, a2, ...] where a1..an is the repeating period.
    """
    a0 = math.isqrt(d)
    coeffs = [a0]
    m, denom, a = 0, 1, a0
    seen: dict[tuple[int, int, int], int] = {}
    for _ in range(200):
        m = denom * a - m
        denom = (d - m * m) // denom
        if denom == 0:
            break
        a = (a0 + m) // denom
        state = (m, denom, a)
        if state in seen:
            break
        seen[state] = len(coeffs)
        coeffs.append(a)
    return coeffs


# ---------------------------------------------------------------------------
# 1. Quadratic Reciprocity
# ---------------------------------------------------------------------------

@register
class QuadraticReciprocityGenerator(StepGenerator):
    """Apply quadratic reciprocity to compute Legendre symbols.

    Given distinct odd primes p and q, uses the law:
    (p/q)(q/p) = (-1)^((p-1)/2 * (q-1)/2) and Euler's criterion
    to compute both Legendre symbols.

    Difficulty scaling:
        Difficulty 1-3: primes from [3, 5, 7, 11, 13].
        Difficulty 4-6: primes from [7, 11, 13, 17, 19, 23].
        Difficulty 7-8: primes from [13, 17, 19, 23, 29, 31, 37].

    Prerequisites:
        quadratic_residue.
    """

    _POOLS = {
        "low": [3, 5, 7, 11, 13],
        "mid": [7, 11, 13, 17, 19, 23],
        "high": [13, 17, 19, 23, 29, 31, 37],
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "quadratic_reciprocity"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["quadratic_residue"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "apply quadratic reciprocity"

    def _pool(self, difficulty: int) -> list[int]:
        """Select prime pool by difficulty.

        Args:
            difficulty: Difficulty level.

        Returns:
            List of odd primes.
        """
        if difficulty <= 3:
            return self._POOLS["low"]
        if difficulty <= 6:
            return self._POOLS["mid"]
        return self._POOLS["high"]

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a quadratic reciprocity problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        pool = self._pool(difficulty)
        p = self._rng.choice(pool)
        q = self._rng.choice([x for x in pool if x != p])
        pq = _euler_criterion(p, q)
        qp = _euler_criterion(q, p)
        sign_exp = ((p - 1) // 2) * ((q - 1) // 2)
        rhs = (-1) ** sign_exp
        problem = f"\\left(\\frac{{{p}}}{{{q}}}\\right)"
        return problem, {
            "p": p, "q": q, "pq": pq, "qp": qp,
            "sign_exp": sign_exp, "rhs": rhs,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps.

        Args:
            data: Solution data dict.

        Returns:
            Steps applying the reciprocity law.
        """
        p, q = data["p"], data["q"]
        return [
            f"(p-1)/2 = {(p - 1) // 2}, (q-1)/2 = {(q - 1) // 2}",
            f"(-1)^{{{data['sign_exp']}}} = {data['rhs']}",
            f"({q}/{p}) = {data['qp']} by Euler",
            f"({p}/{q}) = {data['rhs']} * {data['qp']} = {data['pq']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the Legendre symbol value.

        Args:
            data: Solution data dict.

        Returns:
            The Legendre symbol (p/q) as a string.
        """
        return str(data["pq"])


# ---------------------------------------------------------------------------
# 2. Primitive Root
# ---------------------------------------------------------------------------

@register
class PrimitiveRootGenerator(StepGenerator):
    """Find the smallest primitive root modulo a prime p.

    A primitive root g has multiplicative order p-1, meaning g^k mod p
    cycles through all non-zero residues.

    Difficulty scaling:
        Difficulty 1-3: p from [3, 5, 7, 11].
        Difficulty 4-6: p from [11, 13, 17, 19, 23].
        Difficulty 7-8: p from [23, 29, 31, 37, 41].

    Prerequisites:
        totient.
    """

    _POOLS = {
        "low": [3, 5, 7, 11],
        "mid": [11, 13, 17, 19, 23],
        "high": [23, 29, 31, 37, 41],
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "primitive_root"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["totient"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "find smallest primitive root"

    def _pool(self, difficulty: int) -> list[int]:
        """Select prime pool by difficulty.

        Args:
            difficulty: Difficulty level.

        Returns:
            List of primes.
        """
        if difficulty <= 3:
            return self._POOLS["low"]
        if difficulty <= 6:
            return self._POOLS["mid"]
        return self._POOLS["high"]

    def _find_primitive_root(self, p: int) -> tuple[int, list[str]]:
        """Find the smallest primitive root mod p.

        Args:
            p: An odd prime.

        Returns:
            Tuple of (root, trace_steps).
        """
        phi = p - 1
        factors = _factorise(phi)
        divisors = [phi // f for f, _ in factors]
        steps: list[str] = []
        for g in range(2, p):
            is_root = True
            for d in divisors:
                if pow(g, d, p) == 1:
                    is_root = False
                    break
            if is_root:
                steps.append(f"g={g}: order divides {phi}")
                steps.append(f"check {g}^d != 1 for d in {divisors}")
                return g, steps
        return 2, steps  # pragma: no cover

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a primitive root problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        pool = self._pool(difficulty)
        p = self._rng.choice(pool)
        root, trace = self._find_primitive_root(p)
        problem = f"\\text{{prim\\_root}}({p})"
        return problem, {"p": p, "root": root, "trace": trace}

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing the root search.
        """
        return data["trace"]

    def _create_answer(self, data: dict) -> str:
        """Return the smallest primitive root.

        Args:
            data: Solution data dict.

        Returns:
            The primitive root as a string.
        """
        return str(data["root"])


# ---------------------------------------------------------------------------
# 3. Sum of Two Squares
# ---------------------------------------------------------------------------

@register
class SumOfSquaresGenerator(StepGenerator):
    """Express a prime p = 1 mod 4 as a sum of two squares.

    Fermat's theorem guarantees every prime p = 1 (mod 4) can be
    written as p = a^2 + b^2. Uses a descent algorithm to find a, b.

    Difficulty scaling:
        Difficulty 1-3: p from [5, 13, 17, 29].
        Difficulty 4-6: p from [37, 41, 53, 61].
        Difficulty 7-8: p from [73, 89, 97].

    Prerequisites:
        primality.
    """

    _POOLS = {
        "low": [5, 13, 17, 29],
        "mid": [37, 41, 53, 61],
        "high": [73, 89, 97],
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "sum_of_squares"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["primality"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "express prime as sum of two squares"

    def _pool(self, difficulty: int) -> list[int]:
        """Select prime pool by difficulty.

        Args:
            difficulty: Difficulty level.

        Returns:
            List of primes congruent to 1 mod 4.
        """
        if difficulty <= 3:
            return self._POOLS["low"]
        if difficulty <= 6:
            return self._POOLS["mid"]
        return self._POOLS["high"]

    def _decompose(self, p: int) -> tuple[int, int]:
        """Find a, b such that a^2 + b^2 = p.

        Args:
            p: Prime with p = 1 (mod 4).

        Returns:
            Tuple (a, b) with a <= b.
        """
        for a in range(1, math.isqrt(p) + 1):
            remainder = p - a * a
            b = math.isqrt(remainder)
            if b * b == remainder:
                return (min(a, b), max(a, b))
        raise ValueError(f"No decomposition for {p}")  # pragma: no cover

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a sum of squares problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        pool = self._pool(difficulty)
        p = self._rng.choice(pool)
        a, b = self._decompose(p)
        problem = f"{p} = a^2 + b^2"
        return problem, {"p": p, "a": a, "b": b}

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing the decomposition.
        """
        p, a, b = data["p"], data["a"], data["b"]
        return [
            f"{p} \\equiv 1 \\pmod{{4}}",
            f"try a={a}: {p} - {a}^2 = {p - a * a}",
            f"\\sqrt{{{p - a * a}}} = {b}",
            f"{p} = {a}^2 + {b}^2",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the two squares.

        Args:
            data: Solution data dict.

        Returns:
            String 'a^2 + b^2'.
        """
        return f"{data['a']}^2 + {data['b']}^2"


# ---------------------------------------------------------------------------
# 4. Moebius Function
# ---------------------------------------------------------------------------

@register
class MoebiusFunctionGenerator(StepGenerator):
    """Compute the Moebius function mu(n).

    mu(n) = 0 if n has a squared prime factor, (-1)^k if n is a
    product of k distinct primes, and mu(1) = 1.

    Difficulty scaling:
        Difficulty 1-3: n in [2, 30].
        Difficulty 4-6: n in [20, 80].
        Difficulty 7-8: n in [50, 150].

    Prerequisites:
        factorisation.
    """

    _RANGES = {
        "low": (2, 30),
        "mid": (20, 80),
        "high": (50, 150),
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "mobius_function"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["factorisation"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute Moebius function"

    def _range(self, difficulty: int) -> tuple[int, int]:
        """Select n range by difficulty.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple (lo, hi).
        """
        if difficulty <= 3:
            return self._RANGES["low"]
        if difficulty <= 6:
            return self._RANGES["mid"]
        return self._RANGES["high"]

    def _mobius(self, n: int) -> tuple[int, list[tuple[int, int]]]:
        """Compute mu(n) and its factorisation.

        Args:
            n: Positive integer.

        Returns:
            Tuple of (mu_value, factorisation).
        """
        factors = _factorise(n)
        for _, exp in factors:
            if exp >= 2:
                return 0, factors
        k = len(factors)
        return (-1) ** k, factors

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Moebius function problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        lo, hi = self._range(difficulty)
        n = self._rng.randint(lo, hi)
        mu, factors = self._mobius(n)
        problem = f"\\mu({n})"
        return problem, {"n": n, "mu": mu, "factors": factors}

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing factorisation and mu computation.
        """
        n = data["n"]
        factors = data["factors"]
        fac_str = " \\cdot ".join(
            f"{p}^{{{e}}}" if e > 1 else str(p) for p, e in factors
        )
        steps = [f"{n} = {fac_str}"]
        for p, e in factors:
            if e >= 2:
                steps.append(f"{p}^{{{e}}} is squared")
                steps.append("\\mu = 0")
                return steps
        k = len(factors)
        steps.append(f"k = {k} distinct primes")
        steps.append(f"\\mu = (-1)^{{{k}}} = {data['mu']}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return mu(n).

        Args:
            data: Solution data dict.

        Returns:
            The Moebius function value as a string.
        """
        return str(data["mu"])


# ---------------------------------------------------------------------------
# 5. Divisor Function
# ---------------------------------------------------------------------------

@register
class DivisorFunctionGenerator(StepGenerator):
    """Compute sigma_0(n) and sigma_1(n) from prime factorisation.

    sigma_0(n) is the number of divisors and sigma_1(n) is the sum
    of divisors, both computed multiplicatively from the factorisation.

    Difficulty scaling:
        Difficulty 1-3: n in [2, 30].
        Difficulty 4-6: n in [20, 80].
        Difficulty 7-8: n in [50, 150].

    Prerequisites:
        factorisation.
    """

    _RANGES = {
        "low": (2, 30),
        "mid": (20, 80),
        "high": (50, 150),
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "divisor_function"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["factorisation"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute divisor functions"

    def _range(self, difficulty: int) -> tuple[int, int]:
        """Select n range by difficulty.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple (lo, hi).
        """
        if difficulty <= 3:
            return self._RANGES["low"]
        if difficulty <= 6:
            return self._RANGES["mid"]
        return self._RANGES["high"]

    def _divisor_sums(self, n: int) -> tuple[int, int, list[tuple[int, int]]]:
        """Compute sigma_0 and sigma_1 of n.

        Args:
            n: Positive integer.

        Returns:
            Tuple of (sigma_0, sigma_1, factorisation).
        """
        factors = _factorise(n)
        sigma0 = 1
        sigma1 = 1
        for p, e in factors:
            sigma0 *= (e + 1)
            sigma1 *= (p ** (e + 1) - 1) // (p - 1)
        return sigma0, sigma1, factors

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a divisor function problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        lo, hi = self._range(difficulty)
        n = self._rng.randint(lo, hi)
        if n < 2:
            n = 2
        sigma0, sigma1, factors = self._divisor_sums(n)
        problem = f"\\sigma_0({n}), \\sigma_1({n})"
        return problem, {
            "n": n, "sigma0": sigma0, "sigma1": sigma1,
            "factors": factors,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing multiplicative computation.
        """
        n = data["n"]
        factors = data["factors"]
        fac_str = " \\cdot ".join(
            f"{p}^{{{e}}}" if e > 1 else str(p) for p, e in factors
        )
        steps = [f"{n} = {fac_str}"]
        s0_parts = [f"({e}+1)" for _, e in factors]
        steps.append(f"\\sigma_0 = {'*'.join(s0_parts)} = {data['sigma0']}")
        s1_parts = []
        for p, e in factors:
            geo = (p ** (e + 1) - 1) // (p - 1)
            s1_parts.append(str(geo))
        steps.append(f"\\sigma_1 = {'*'.join(s1_parts)} = {data['sigma1']}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return sigma_0 and sigma_1.

        Args:
            data: Solution data dict.

        Returns:
            Both divisor function values.
        """
        return f"sigma_0={data['sigma0']}, sigma_1={data['sigma1']}"


# ---------------------------------------------------------------------------
# 6. Jacobi Symbol
# ---------------------------------------------------------------------------

@register
class JacobiSymbolGenerator(StepGenerator):
    """Compute the Jacobi symbol (a/n) for composite odd n.

    Uses reciprocity and reduction rules to evaluate the symbol
    without full factorisation of n.

    Difficulty scaling:
        Difficulty 1-3: n in [9, 15, 21, 25].
        Difficulty 4-6: n in [21, 25, 33, 35, 45].
        Difficulty 7-8: n in [45, 51, 55, 63, 75, 77].

    Prerequisites:
        quadratic_reciprocity.
    """

    _POOLS = {
        "low": [9, 15, 21, 25],
        "mid": [21, 25, 33, 35, 45],
        "high": [45, 51, 55, 63, 75, 77],
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "jacobi_symbol"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["quadratic_reciprocity"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute Jacobi symbol"

    def _pool(self, difficulty: int) -> list[int]:
        """Select modulus pool by difficulty.

        Args:
            difficulty: Difficulty level.

        Returns:
            List of composite odd moduli.
        """
        if difficulty <= 3:
            return self._POOLS["low"]
        if difficulty <= 6:
            return self._POOLS["mid"]
        return self._POOLS["high"]

    def _jacobi(self, a: int, n: int) -> int:
        """Compute the Jacobi symbol (a/n).

        Args:
            a: Numerator.
            n: Odd positive denominator.

        Returns:
            The Jacobi symbol value: -1, 0, or 1.
        """
        if n == 1:
            return 1
        a = a % n
        result = 1
        while a != 0:
            while a % 2 == 0:
                a //= 2
                if n % 8 in (3, 5):
                    result = -result
            a, n = n, a
            if a % 4 == 3 and n % 4 == 3:
                result = -result
            a = a % n
        return result if n == 1 else 0

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Jacobi symbol problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        pool = self._pool(difficulty)
        n = self._rng.choice(pool)
        a = self._rng.randint(2, n - 1)
        while math.gcd(a, n) != 1:
            a = self._rng.randint(2, n - 1)
        val = self._jacobi(a, n)
        problem = f"\\left(\\frac{{{a}}}{{{n}}}\\right)_J"
        return problem, {"a": a, "n": n, "val": val}

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing reciprocity and reduction.
        """
        a, n = data["a"], data["n"]
        factors = _factorise(n)
        fac_str = " \\cdot ".join(
            f"{p}^{{{e}}}" if e > 1 else str(p) for p, e in factors
        )
        steps = [
            f"n = {n} = {fac_str}",
            f"\\gcd({a}, {n}) = 1",
        ]
        for p, e in factors:
            ls = _euler_criterion(a, p) if _is_prime(p) else self._jacobi(a, p)
            steps.append(f"({a}/{p}) = {ls}")
        steps.append(f"product = {data['val']}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the Jacobi symbol value.

        Args:
            data: Solution data dict.

        Returns:
            The symbol value as a string.
        """
        return str(data["val"])


# ---------------------------------------------------------------------------
# 7. Pell Equation
# ---------------------------------------------------------------------------

@register
class PellEquationGenerator(StepGenerator):
    """Find the fundamental solution to x^2 - D*y^2 = 1.

    Uses the continued fraction expansion of sqrt(D) to find the
    smallest positive solution via convergents.

    Difficulty scaling:
        Difficulty 1-3: D from [2, 3, 5, 6, 7].
        Difficulty 4-6: D from [7, 8, 10, 11, 12, 13].
        Difficulty 7-8: D from [13, 14, 15, 17, 19, 21].

    Prerequisites:
        continued_fraction.
    """

    _POOLS = {
        "low": [2, 3, 5, 6, 7],
        "mid": [7, 8, 10, 11, 12, 13],
        "high": [13, 14, 15, 17, 19, 21],
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "pell_equation"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["continued_fraction"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "solve Pell equation"

    def _pool(self, difficulty: int) -> list[int]:
        """Select D pool by difficulty.

        Args:
            difficulty: Difficulty level.

        Returns:
            List of non-square D values.
        """
        if difficulty <= 3:
            return self._POOLS["low"]
        if difficulty <= 6:
            return self._POOLS["mid"]
        return self._POOLS["high"]

    def _solve_pell(self, d: int) -> tuple[int, int, list[int]]:
        """Find fundamental solution to x^2 - d*y^2 = 1.

        Args:
            d: Non-square positive integer.

        Returns:
            Tuple of (x, y, cf_coefficients).
        """
        coeffs = _cf_sqrt(d)
        # Iterate convergents until x^2 - d*y^2 = 1
        h_prev, h_curr = 0, 1
        k_prev, k_curr = 1, 0
        for i, a in enumerate(coeffs):
            h_prev, h_curr = h_curr, a * h_curr + h_prev
            k_prev, k_curr = k_curr, a * k_curr + k_prev
            if i > 0 and h_curr * h_curr - d * k_curr * k_curr == 1:
                return h_curr, k_curr, coeffs
        # Extend with periodic part
        period = coeffs[1:]
        if not period:
            return h_curr, k_curr, coeffs
        for _ in range(200):
            for a in period:
                h_prev, h_curr = h_curr, a * h_curr + h_prev
                k_prev, k_curr = k_curr, a * k_curr + k_prev
                if h_curr * h_curr - d * k_curr * k_curr == 1:
                    return h_curr, k_curr, coeffs
        return h_curr, k_curr, coeffs  # pragma: no cover

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Pell equation problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        pool = self._pool(difficulty)
        d = self._rng.choice(pool)
        x, y, coeffs = self._solve_pell(d)
        problem = f"x^2 - {d}y^2 = 1"
        return problem, {"d": d, "x": x, "y": y, "coeffs": coeffs}

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing CF expansion and convergent.
        """
        d = data["d"]
        coeffs = data["coeffs"]
        cf_str = f"[{coeffs[0]}; {', '.join(str(c) for c in coeffs[1:])}]"
        x, y = data["x"], data["y"]
        return [
            f"\\sqrt{{{d}}} = {cf_str}",
            f"convergent: x={x}, y={y}",
            f"{x}^2 - {d}*{y}^2 = {x * x - d * y * y}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the fundamental solution.

        Args:
            data: Solution data dict.

        Returns:
            The (x, y) pair as a string.
        """
        return f"x={data['x']}, y={data['y']}"


# ---------------------------------------------------------------------------
# 8. Multiplicative Order
# ---------------------------------------------------------------------------

@register
class OrderElementGenerator(StepGenerator):
    """Find the multiplicative order of a mod n.

    The order is the smallest positive k such that a^k = 1 (mod n),
    which exists when gcd(a, n) = 1.

    Difficulty scaling:
        Difficulty 1-3: n from [5, 7, 8, 9, 11].
        Difficulty 4-6: n from [11, 13, 16, 17, 19].
        Difficulty 7-8: n from [19, 23, 25, 27, 29].

    Prerequisites:
        mod_pow.
    """

    _POOLS = {
        "low": [5, 7, 8, 9, 11],
        "mid": [11, 13, 16, 17, 19],
        "high": [19, 23, 25, 27, 29],
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "order_element"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["mod_pow"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "find multiplicative order"

    def _pool(self, difficulty: int) -> list[int]:
        """Select modulus pool by difficulty.

        Args:
            difficulty: Difficulty level.

        Returns:
            List of moduli.
        """
        if difficulty <= 3:
            return self._POOLS["low"]
        if difficulty <= 6:
            return self._POOLS["mid"]
        return self._POOLS["high"]

    def _find_order(self, a: int, n: int) -> tuple[int, list[str]]:
        """Find the multiplicative order of a modulo n.

        Args:
            a: Base element with gcd(a, n) = 1.
            n: Modulus.

        Returns:
            Tuple of (order, trace_steps).
        """
        steps: list[str] = []
        val = 1
        for k in range(1, n + 1):
            val = (val * a) % n
            steps.append(f"{a}^{{{k}}} \\equiv {val} \\pmod{{{n}}}")
            if val == 1:
                return k, steps
        return n, steps  # pragma: no cover

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a multiplicative order problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        pool = self._pool(difficulty)
        n = self._rng.choice(pool)
        # Pick a coprime to n
        candidates = [a for a in range(2, n) if math.gcd(a, n) == 1]
        a = self._rng.choice(candidates)
        order, trace = self._find_order(a, n)
        # Trim trace to keep output short
        if len(trace) > 4:
            trace = trace[:2] + ["\\ldots"] + trace[-1:]
        problem = f"\\text{{ord}}_{{{n}}}({a})"
        return problem, {"a": a, "n": n, "order": order, "trace": trace}

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing successive powers.
        """
        return data["trace"]

    def _create_answer(self, data: dict) -> str:
        """Return the multiplicative order.

        Args:
            data: Solution data dict.

        Returns:
            The order as a string.
        """
        return str(data["order"])
