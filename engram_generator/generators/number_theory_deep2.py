"""Deeper number theory generators -- quadratic forms, p-adic, analytic.

10 generators at tiers 3-6 covering sum of four squares, Legendre symbol,
Hensel lifting, Dirichlet characters, Mobius inversion, continued fraction
convergents, Fibonacci mod, digit sum divisibility, modular equations, and
prime counting.
"""
from __future__ import annotations

import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_SMALL_PRIMES = [
    2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47,
    53, 59, 61, 67, 71, 73, 79, 83, 89, 97,
]


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


def _euler_totient(n: int) -> int:
    """Compute Euler's totient function phi(n).

    Args:
        n: Positive integer.

    Returns:
        phi(n).
    """
    result = n
    temp = n
    d = 2
    while d * d <= temp:
        if temp % d == 0:
            while temp % d == 0:
                temp //= d
            result -= result // d
        d += 1
    if temp > 1:
        result -= result // temp
    return result


def _mobius(n: int) -> int:
    """Compute the Mobius function mu(n).

    Args:
        n: Positive integer.

    Returns:
        mu(n): 0 if n has squared factor, (-1)^k if k distinct primes.
    """
    factors = _factorise(n)
    for _, exp in factors:
        if exp > 1:
            return 0
    return 1 if len(factors) % 2 == 0 else -1


def _divisors(n: int) -> list[int]:
    """Return sorted list of positive divisors of n.

    Args:
        n: Positive integer.

    Returns:
        Sorted list of divisors.
    """
    divs = []
    for i in range(1, int(math.isqrt(n)) + 1):
        if n % i == 0:
            divs.append(i)
            if i != n // i:
                divs.append(n // i)
    return sorted(divs)


def _extended_gcd(a: int, b: int) -> tuple[int, int, int]:
    """Compute extended GCD: returns (g, x, y) such that a*x + b*y = g.

    Args:
        a: First integer.
        b: Second integer.

    Returns:
        Tuple (gcd, x, y).
    """
    if a == 0:
        return b, 0, 1
    g, x, y = _extended_gcd(b % a, a)
    return g, y - (b // a) * x, x


def _mod_inverse(a: int, m: int) -> int:
    """Compute modular inverse of a modulo m.

    Args:
        a: Integer.
        m: Modulus.

    Returns:
        a^{-1} mod m.

    Raises:
        ValueError: If inverse does not exist.
    """
    g, x, _ = _extended_gcd(a % m, m)
    if g != 1:
        raise ValueError(f"No inverse: gcd({a},{m})={g}")
    return x % m


def _fmt(value: float, places: int = 4) -> str:
    """Round a float and return its string representation.

    Args:
        value: Number to format.
        places: Decimal places.

    Returns:
        Rounded string.
    """
    return str(round(value, places))


def _sieve(limit: int) -> list[int]:
    """Return all primes up to limit using Sieve of Eratosthenes.

    Args:
        limit: Upper bound (inclusive).

    Returns:
        List of primes <= limit.
    """
    if limit < 2:
        return []
    is_prime_arr = [True] * (limit + 1)
    is_prime_arr[0] = is_prime_arr[1] = False
    for i in range(2, int(math.isqrt(limit)) + 1):
        if is_prime_arr[i]:
            for j in range(i * i, limit + 1, i):
                is_prime_arr[j] = False
    return [i for i, v in enumerate(is_prime_arr) if v]


# ---------------------------------------------------------------------------
# 1. Sum of Four Squares (Lagrange)
# ---------------------------------------------------------------------------

@register
class SumOfFourSquaresGenerator(StepGenerator):
    """Express n as a sum of four squares using greedy decomposition.

    Lagrange's theorem guarantees every natural number is a sum of four
    squares. Uses greedy approach: find largest square <= remainder, repeat.

    Difficulty scaling:
        d1-2: n in [1, 20].
        d3-4: n in [10, 50].
        d5-6: n in [30, 100].
        d7-8: n in [50, 200].

    Prerequisites:
        exponentiation.
    """

    _RANGES = {
        1: (1, 20), 2: (1, 20), 3: (10, 50), 4: (10, 50),
        5: (30, 100), 6: (30, 100), 7: (50, 200), 8: (50, 200),
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "sum_of_four_squares"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["exponentiation"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "express n as sum of four squares"

    def _decompose(self, n: int) -> list[int]:
        """Decompose n into exactly 4 squares.

        Uses greedy with backtracking: if the greedy approach leaves
        a non-zero remainder after 3 squares, the last square absorbs
        whatever is left (if it's a perfect square), otherwise tries
        a smaller first square.

        Args:
            n: Non-negative integer.

        Returns:
            List of exactly 4 non-negative integers whose squares sum to n.
        """
        for a in range(int(math.isqrt(n)), -1, -1):
            rem_a = n - a * a
            for b in range(int(math.isqrt(rem_a)), -1, -1):
                rem_b = rem_a - b * b
                for c in range(int(math.isqrt(rem_b)), -1, -1):
                    rem_c = rem_b - c * c
                    d = int(math.isqrt(rem_c))
                    if d * d == rem_c:
                        return [a, b, c, d]
        return [0, 0, 0, 0]

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a sum of four squares problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        lo, hi = self._RANGES.get(difficulty, self._RANGES[1])
        n = self._rng.randint(lo, hi)
        parts = self._decompose(n)
        verify = sum(x * x for x in parts)
        problem = f"express {n} as sum of 4 squares"
        return problem, {"n": n, "parts": parts, "verify": verify}

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing greedy decomposition.
        """
        n = data["n"]
        parts = data["parts"]
        steps = []
        remainder = n
        for i, p in enumerate(parts):
            steps.append(f"step {i + 1}: floor(sqrt({remainder}))={p}, "
                         f"remainder={remainder}-{p}^2={remainder - p * p}")
            remainder -= p * p
        sq_str = "+".join(f"{p}^2" for p in parts)
        steps.append(f"{n}={sq_str}={data['verify']}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the decomposition.

        Args:
            data: Solution data dict.

        Returns:
            Decomposition as string.
        """
        return "+".join(f"{p}^2" for p in data["parts"])


# ---------------------------------------------------------------------------
# 2. Legendre Symbol Computation
# ---------------------------------------------------------------------------

@register
class LegendreSymbolComputeGenerator(StepGenerator):
    """Compute (a/p) via Euler criterion or multiplicativity.

    For compound values, uses (ab/p) = (a/p)(b/p). Falls back to
    Euler criterion a^{(p-1)/2} mod p.

    Difficulty scaling:
        d1-2: p from {5, 7, 11}, a=2-5.
        d3-4: p from {11, 13, 17}, a=2-10.
        d5-6: p from {17, 19, 23}, a as product of two small ints.
        d7-8: p from {23, 29, 31, 37}, a as product.

    Prerequisites:
        quadratic_residue.
    """

    _POOLS = {
        1: [5, 7, 11], 2: [5, 7, 11],
        3: [11, 13, 17], 4: [11, 13, 17],
        5: [17, 19, 23], 6: [17, 19, 23],
        7: [23, 29, 31, 37], 8: [23, 29, 31, 37],
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "legendre_symbol_compute"

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
        return "compute Legendre symbol"

    def _legendre(self, a: int, p: int) -> int:
        """Compute the Legendre symbol (a/p).

        Args:
            a: Integer.
            p: Odd prime.

        Returns:
            1, -1, or 0.
        """
        a = a % p
        if a == 0:
            return 0
        result = pow(a, (p - 1) // 2, p)
        return 1 if result == 1 else -1

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Legendre symbol problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        pool = self._POOLS.get(difficulty, self._POOLS[1])
        p = self._rng.choice(pool)
        if difficulty <= 4:
            a = self._rng.randint(2, min(p - 1, 3 + difficulty * 2))
            compound = False
            a1, a2 = a, 1
        else:
            a1 = self._rng.randint(2, min(p - 1, 6))
            a2 = self._rng.randint(2, min(p - 1, 6))
            a = a1 * a2
            compound = True
        ls = self._legendre(a, p)
        ls1 = self._legendre(a1, p)
        ls2 = self._legendre(a2, p)
        euler_val = pow(a % p, (p - 1) // 2, p)
        problem = f"\\left(\\frac{{{a}}}{{{p}}}\\right)"
        return problem, {
            "a": a, "p": p, "a1": a1, "a2": a2,
            "compound": compound, "ls": ls,
            "ls1": ls1, "ls2": ls2, "euler_val": euler_val,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing Legendre symbol computation.
        """
        a, p = data["a"], data["p"]
        steps = [f"compute ({a}/{p})"]
        if data["compound"]:
            a1, a2 = data["a1"], data["a2"]
            steps.append(f"({a}/{p})=({a1}/{p})*({a2}/{p})")
            steps.append(f"({a1}/{p})={data['ls1']}, ({a2}/{p})={data['ls2']}")
            steps.append(f"product={data['ls1']}*{data['ls2']}={data['ls']}")
        else:
            steps.append(f"Euler: {a}^{{{(p - 1) // 2}}} mod {p}={data['euler_val']}")
            tag = "QR" if data["ls"] == 1 else "NR"
            steps.append(f"({a}/{p})={data['ls']} ({tag})")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the Legendre symbol value.

        Args:
            data: Solution data dict.

        Returns:
            1, -1, or 0 as string.
        """
        return str(data["ls"])


# ---------------------------------------------------------------------------
# 3. Hensel Lift (Extended)
# ---------------------------------------------------------------------------

@register
class HenselLiftExtGenerator(StepGenerator):
    """Lift root of f(x) = x^2 - a mod p to mod p^k via Newton iteration.

    Uses x_{k+1} = x_k - f(x_k) * (f'(x_k))^{-1} mod p^{k+1}.

    Difficulty scaling:
        d1-2: lift from p to p^2, p in {3, 5, 7}.
        d3-4: lift to p^3, p in {5, 7, 11}.
        d5-6: lift to p^3, p in {7, 11, 13}.
        d7-8: lift to p^4, p in {11, 13}.

    Prerequisites:
        mod_pow.
    """

    _CONFIGS = {
        1: ([3, 5, 7], 2), 2: ([3, 5, 7], 2),
        3: ([5, 7, 11], 3), 4: ([5, 7, 11], 3),
        5: ([7, 11, 13], 3), 6: ([7, 11, 13], 3),
        7: ([11, 13], 4), 8: ([11, 13], 4),
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "hensel_lift_ext"

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
        return "Hensel-lift a root mod p to mod p^k"

    def _find_root_mod_p(self, a: int, p: int) -> int | None:
        """Find x such that x^2 = a mod p.

        Args:
            a: Integer.
            p: Odd prime.

        Returns:
            Root modulo p, or None if no root.
        """
        for x in range(p):
            if (x * x) % p == a % p:
                return x
        return None

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Hensel lifting problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        primes, target_k = self._CONFIGS.get(difficulty, self._CONFIGS[1])
        p = self._rng.choice(primes)
        # Pick a quadratic residue mod p
        for _ in range(50):
            a = self._rng.randint(2, p * p)
            root = self._find_root_mod_p(a, p)
            if root is not None and root != 0:
                break
        else:
            a, root = 4, 2  # fallback

        # Hensel lift from mod p to mod p^k
        lifts: list[tuple[int, int]] = [(root, p)]
        x_cur = root
        for k in range(2, target_k + 1):
            pk = p ** k
            f_val = (x_cur * x_cur - a) % pk
            f_prime = (2 * x_cur) % pk
            inv_fp = _mod_inverse(f_prime, pk)
            x_cur = (x_cur - f_val * inv_fp) % pk
            lifts.append((x_cur, pk))

        problem = f"lift x^2\\equiv {a}\\pmod{{{p}}} to mod {p}^{{{target_k}}}"
        return problem, {
            "a": a, "p": p, "target_k": target_k,
            "lifts": lifts, "final_root": x_cur,
            "final_mod": p ** target_k,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing each lift iteration.
        """
        a = data["a"]
        steps = [f"f(x)=x^2-{a}"]
        for x_k, pk in data["lifts"]:
            verify = (x_k * x_k - a) % pk
            steps.append(f"x={x_k} mod {pk}, f({x_k})\\equiv {verify}")
        steps.append(f"root: {data['final_root']} mod {data['final_mod']}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the lifted root.

        Args:
            data: Solution data dict.

        Returns:
            Root mod p^k as string.
        """
        return f"{data['final_root']} mod {data['final_mod']}"


# ---------------------------------------------------------------------------
# 4. Dirichlet Character
# ---------------------------------------------------------------------------

@register
class DirichletCharacterGenerator(StepGenerator):
    """Evaluate a Dirichlet character chi mod q.

    Chi is completely multiplicative: chi(ab) = chi(a)*chi(b).
    Chi(n) = 0 if gcd(n, q) > 1. Evaluates the principal character
    or a real character for small moduli.

    Difficulty scaling:
        d1-2: q in {3, 4, 5}, principal character.
        d3-4: q in {5, 7, 8}, principal character.
        d5-6: q in {5, 7, 8}, Legendre-based character.
        d7-8: q in {7, 11, 12}, Legendre-based character.

    Prerequisites:
        totient.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "dirichlet_character"

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
        return "evaluate Dirichlet character"

    def _principal_char(self, n: int, q: int) -> int:
        """Evaluate the principal character mod q.

        Args:
            n: Integer to evaluate.
            q: Modulus.

        Returns:
            1 if gcd(n,q)=1, else 0.
        """
        return 1 if math.gcd(n, q) == 1 else 0

    def _real_char(self, n: int, q: int) -> int:
        """Evaluate a real non-principal character mod q.

        Uses Jacobi/Kronecker symbol structure for small q.

        Args:
            n: Integer to evaluate.
            q: Modulus.

        Returns:
            0, 1, or -1.
        """
        if math.gcd(n, q) > 1:
            return 0
        # For prime q, use Legendre symbol
        if _is_prime(q):
            r = pow(n % q, (q - 1) // 2, q)
            return 1 if r == 1 else -1
        # For composite q, use principal as fallback
        return 1 if math.gcd(n, q) == 1 else 0

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Dirichlet character evaluation problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 2:
            q = self._rng.choice([3, 4, 5])
            use_principal = True
        elif difficulty <= 4:
            q = self._rng.choice([5, 7, 8])
            use_principal = True
        elif difficulty <= 6:
            q = self._rng.choice([5, 7, 8])
            use_principal = False
        else:
            q = self._rng.choice([7, 11, 12])
            use_principal = False

        # Evaluate character for n = 1 to q
        values: list[tuple[int, int]] = []
        for n in range(1, q + 1):
            if use_principal:
                val = self._principal_char(n, q)
            else:
                val = self._real_char(n, q)
            values.append((n, val))

        phi_q = _euler_totient(q)
        char_type = "principal" if use_principal else "real"
        problem = f"\\chi mod {q} ({char_type}), n=1..{q}"
        return problem, {
            "q": q, "phi_q": phi_q, "char_type": char_type,
            "values": values, "use_principal": use_principal,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing character evaluation.
        """
        q = data["q"]
        steps = [
            f"chi mod {q} ({data['char_type']}), phi({q})={data['phi_q']}",
        ]
        for n, val in data["values"]:
            g = math.gcd(n, q)
            if g > 1:
                steps.append(f"chi({n})=0 (gcd={g})")
            else:
                steps.append(f"chi({n})={val}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the character table as a compact string.

        Args:
            data: Solution data dict.

        Returns:
            Character values as string.
        """
        vals = ",".join(str(v) for _, v in data["values"])
        return f"[{vals}]"


# ---------------------------------------------------------------------------
# 5. Mobius Inversion
# ---------------------------------------------------------------------------

@register
class MobiusInversionGenerator(StepGenerator):
    """Apply Mobius inversion to recover f from g.

    If g(n) = sum_{d|n} f(d), then f(n) = sum_{d|n} mu(n/d)*g(d).
    Computes f(n) from given g values.

    Difficulty scaling:
        d1-2: n in [6, 12].
        d3-4: n in [10, 20].
        d5-6: n in [15, 30].
        d7-8: n in [20, 50].

    Prerequisites:
        factorisation.
    """

    _RANGES = {
        1: (6, 12), 2: (6, 12), 3: (10, 20), 4: (10, 20),
        5: (15, 30), 6: (15, 30), 7: (20, 50), 8: (20, 50),
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "mobius_inversion"

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
        return "apply Mobius inversion to recover f from g"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Mobius inversion problem.

        Uses g(n) = sum_{d|n} d (i.e., f(d) = d, so g = sigma).
        Recovers f(n) = sum_{d|n} mu(n/d)*g(d).

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        lo, hi = self._RANGES.get(difficulty, self._RANGES[1])
        n = self._rng.randint(lo, hi)
        if n < 2:
            n = 6

        divs = _divisors(n)
        # g(d) = sigma(d) = sum of divisors of d
        g_vals = {d: sum(_divisors(d)) for d in divs}
        # f(n) = sum_{d|n} mu(n/d) * g(d)
        terms: list[tuple[int, int, int, int]] = []
        f_n = 0
        for d in divs:
            mu_val = _mobius(n // d)
            gd = g_vals[d]
            contrib = mu_val * gd
            terms.append((d, n // d, mu_val, gd))
            f_n += contrib

        problem = f"Mobius inversion: f({n}) from g(d)=\\sigma(d)"
        return problem, {
            "n": n, "divs": divs, "g_vals": g_vals,
            "terms": terms, "f_n": f_n,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing the inversion computation.
        """
        n = data["n"]
        steps = [f"divisors of {n}: {data['divs']}"]
        for d, nd, mu_val, gd in data["terms"][:5]:
            steps.append(f"d={d}: mu({nd})={mu_val}, g({d})={gd}")
        total_str = "+".join(
            f"{mu_val}*{gd}" for _, _, mu_val, gd in data["terms"][:5]
        )
        steps.append(f"f({n})={total_str}={data['f_n']}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return f(n).

        Args:
            data: Solution data dict.

        Returns:
            f(n) as string.
        """
        return str(data["f_n"])


# ---------------------------------------------------------------------------
# 6. Continued Fraction Convergent
# ---------------------------------------------------------------------------

@register
class ContinuedFractionConvergentGenerator(StepGenerator):
    """Compute convergents p_k/q_k from a continued fraction [a0; a1, ...].

    Uses recurrence: p_k = a_k*p_{k-1} + p_{k-2},
    q_k = a_k*q_{k-1} + q_{k-2}.

    Difficulty scaling:
        d1-2: CF with 3 terms.
        d3-4: CF with 4 terms.
        d5-6: CF with 5 terms.
        d7-8: CF with 6 terms.

    Prerequisites:
        continued_fraction.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "continued_fraction_convergent"

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
        return "compute continued fraction convergents"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a convergent computation problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 2:
            length = 3
        elif difficulty <= 4:
            length = 4
        elif difficulty <= 6:
            length = 5
        else:
            length = 6

        cf = [self._rng.randint(1, 5)]
        for _ in range(length - 1):
            cf.append(self._rng.randint(1, 4))

        # Compute convergents
        p_prev2, p_prev1 = 0, 1
        q_prev2, q_prev1 = 1, 0
        convergents: list[tuple[int, int]] = []
        for a_k in cf:
            p_k = a_k * p_prev1 + p_prev2
            q_k = a_k * q_prev1 + q_prev2
            convergents.append((p_k, q_k))
            p_prev2, p_prev1 = p_prev1, p_k
            q_prev2, q_prev1 = q_prev1, q_k

        cf_str = f"[{cf[0]}; " + ", ".join(str(a) for a in cf[1:]) + "]"
        final_p, final_q = convergents[-1]
        value = round(final_p / final_q, 4)
        problem = f"convergents of {cf_str}"
        return problem, {
            "cf": cf, "convergents": convergents,
            "value": value, "cf_str": cf_str,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing convergent recurrence.
        """
        steps = [f"CF = {data['cf_str']}"]
        for i, ((p, q), a) in enumerate(
            zip(data["convergents"], data["cf"])
        ):
            steps.append(f"k={i}: a_{i}={a}, p_{i}/q_{i}={p}/{q}")
        final_p, final_q = data["convergents"][-1]
        steps.append(f"value={_fmt(data['value'])}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the final convergent.

        Args:
            data: Solution data dict.

        Returns:
            p/q as string.
        """
        p, q = data["convergents"][-1]
        return f"{p}/{q}"


# ---------------------------------------------------------------------------
# 7. Fibonacci mod (Pisano Period)
# ---------------------------------------------------------------------------

@register
class FibonacciModGenerator(StepGenerator):
    """Compute F_n mod m using the Pisano period.

    The Fibonacci sequence mod m is periodic with period pi(m).
    Computes pi(m) for small m, then F_n mod m = F_{n mod pi(m)} mod m.

    Difficulty scaling:
        d1-2: m in [2, 5], n in [10, 30].
        d3-4: m in [3, 8], n in [20, 60].
        d5-6: m in [5, 12], n in [40, 100].
        d7-8: m in [7, 15], n in [60, 200].

    Prerequisites:
        modular.
    """

    _CONFIGS = {
        1: ((2, 5), (10, 30)), 2: ((2, 5), (10, 30)),
        3: ((3, 8), (20, 60)), 4: ((3, 8), (20, 60)),
        5: ((5, 12), (40, 100)), 6: ((5, 12), (40, 100)),
        7: ((7, 15), (60, 200)), 8: ((7, 15), (60, 200)),
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "fibonacci_mod"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["modular"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute Fibonacci number mod m via Pisano period"

    def _pisano_period(self, m: int) -> int:
        """Compute the Pisano period pi(m).

        Args:
            m: Modulus >= 2.

        Returns:
            Period of Fibonacci sequence mod m.
        """
        a, b = 0, 1
        for i in range(1, 6 * m + 1):
            a, b = b, (a + b) % m
            if a == 0 and b == 1:
                return i
        return 6 * m  # upper bound fallback

    def _fib_mod(self, n: int, m: int) -> int:
        """Compute F_n mod m directly.

        Args:
            n: Fibonacci index.
            m: Modulus.

        Returns:
            F_n mod m.
        """
        if n == 0:
            return 0
        a, b = 0, 1
        for _ in range(n - 1):
            a, b = b, (a + b) % m
        return b

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Fibonacci mod problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        (mlo, mhi), (nlo, nhi) = self._CONFIGS.get(
            difficulty, self._CONFIGS[1]
        )
        m = self._rng.randint(mlo, mhi)
        n = self._rng.randint(nlo, nhi)
        pi_m = self._pisano_period(m)
        reduced_n = n % pi_m
        result = self._fib_mod(reduced_n, m)
        problem = f"F_{{{n}}} \\mod {m}"
        return problem, {
            "n": n, "m": m, "pi_m": pi_m,
            "reduced_n": reduced_n, "result": result,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing Pisano period computation.
        """
        n, m = data["n"], data["m"]
        return [
            f"Pisano period pi({m})={data['pi_m']}",
            f"{n} mod {data['pi_m']}={data['reduced_n']}",
            f"F_{{{data['reduced_n']}}} mod {m}={data['result']}",
            f"F_{{{n}}} mod {m}={data['result']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return F_n mod m.

        Args:
            data: Solution data dict.

        Returns:
            Result as string.
        """
        return str(data["result"])


# ---------------------------------------------------------------------------
# 8. Digit Sum Divisibility
# ---------------------------------------------------------------------------

@register
class DigitSumDivisibilityGenerator(StepGenerator):
    """Test divisibility via digit sum rules.

    By 3: n divisible by 3 iff digit sum divisible by 3.
    By 9: n divisible by 9 iff digit sum divisible by 9.
    By 11: n divisible by 11 iff alternating digit sum divisible by 11.

    Difficulty scaling:
        d1-2: 2-3 digit numbers, test div by 3.
        d3-4: 3-4 digit numbers, test div by 3 and 9.
        d5-6: 4-5 digit numbers, test div by 3, 9, 11.
        d7-8: 5-6 digit numbers, all three tests.

    Prerequisites:
        modular.
    """

    _CONFIGS = {
        1: (10, 999, [3]), 2: (10, 999, [3]),
        3: (100, 9999, [3, 9]), 4: (100, 9999, [3, 9]),
        5: (1000, 99999, [3, 9, 11]), 6: (1000, 99999, [3, 9, 11]),
        7: (10000, 999999, [3, 9, 11]), 8: (10000, 999999, [3, 9, 11]),
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "digit_sum_divisibility"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 3

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["modular"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "test divisibility via digit sum rules"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a digit sum divisibility problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        lo, hi, tests = self._CONFIGS.get(difficulty, self._CONFIGS[1])
        n = self._rng.randint(lo, hi)
        digits = [int(c) for c in str(n)]
        digit_sum = sum(digits)
        alt_sum = sum(
            d * (1 if i % 2 == 0 else -1)
            for i, d in enumerate(digits)
        )
        results: list[tuple[int, bool, str]] = []
        for d in tests:
            if d == 11:
                divisible = n % 11 == 0
                reason = f"alt_sum={alt_sum}, {alt_sum}%11={alt_sum % 11}"
            else:
                divisible = n % d == 0
                reason = f"digit_sum={digit_sum}, {digit_sum}%{d}={digit_sum % d}"
            results.append((d, divisible, reason))

        problem = f"divisibility of {n} by {tests}"
        return problem, {
            "n": n, "digits": digits, "digit_sum": digit_sum,
            "alt_sum": alt_sum, "results": results,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing digit sum rules.
        """
        n = data["n"]
        digits_str = "+".join(str(d) for d in data["digits"])
        steps = [f"digits of {n}: {digits_str}={data['digit_sum']}"]
        if data["alt_sum"] != data["digit_sum"]:
            alt_str = "+".join(
                f"{'+'if i%2==0 else '-'}{d}"
                for i, d in enumerate(data["digits"])
            )
            steps.append(f"alt sum: {alt_str}={data['alt_sum']}")
        for d, div, reason in data["results"]:
            verdict = "yes" if div else "no"
            steps.append(f"div by {d}: {reason} -> {verdict}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return divisibility results.

        Args:
            data: Solution data dict.

        Returns:
            Results as string.
        """
        parts = [f"{d}:{'yes' if div else 'no'}" for d, div, _ in data["results"]]
        return ", ".join(parts)


# ---------------------------------------------------------------------------
# 9. Modular Equation
# ---------------------------------------------------------------------------

@register
class ModularEquationGenerator(StepGenerator):
    """Solve ax = b (mod m).

    Solution exists iff gcd(a, m) | b. If g = gcd(a, m) divides b,
    there are g solutions: x = (b/g) * (a/g)^{-1} mod (m/g) + k*(m/g).

    Difficulty scaling:
        d1-2: a, b in [2, 10], m in [5, 15].
        d3-4: a, b in [3, 20], m in [7, 25].
        d5-6: a, b in [5, 30], m in [11, 40].
        d7-8: a, b in [5, 50], m in [13, 60].

    Prerequisites:
        mod_pow.
    """

    _RANGES = {
        1: (2, 10, 5, 15), 2: (2, 10, 5, 15),
        3: (3, 20, 7, 25), 4: (3, 20, 7, 25),
        5: (5, 30, 11, 40), 6: (5, 30, 11, 40),
        7: (5, 50, 13, 60), 8: (5, 50, 13, 60),
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "modular_equation"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

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
        return "solve modular linear equation"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a modular equation problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        alo, ahi, mlo, mhi = self._RANGES.get(difficulty, self._RANGES[1])
        a = self._rng.randint(alo, ahi)
        m = self._rng.randint(mlo, mhi)
        b = self._rng.randint(1, m - 1)
        g = math.gcd(a, m)
        solvable = b % g == 0
        solutions: list[int] = []
        if solvable:
            a_r, b_r, m_r = a // g, b // g, m // g
            inv = _mod_inverse(a_r, m_r)
            x0 = (b_r * inv) % m_r
            for k in range(g):
                solutions.append((x0 + k * m_r) % m)
            solutions.sort()

        problem = f"{a}x \\equiv {b} \\pmod{{{m}}}"
        return problem, {
            "a": a, "b": b, "m": m, "g": g,
            "solvable": solvable, "solutions": solutions,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing solution procedure.
        """
        a, b, m, g = data["a"], data["b"], data["m"], data["g"]
        steps = [
            f"gcd({a},{m})={g}",
            f"{g}|{b}? {'yes' if data['solvable'] else 'no'}",
        ]
        if data["solvable"]:
            steps.append(f"reduce: {a // g}x={b // g} mod {m // g}")
            steps.append(f"solutions: {data['solutions']}")
            for x in data["solutions"][:3]:
                steps.append(f"verify: {a}*{x} mod {m}={a * x % m}")
        else:
            steps.append("no solution")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the solutions.

        Args:
            data: Solution data dict.

        Returns:
            Solutions as string, or 'no solution'.
        """
        if data["solvable"]:
            return ",".join(str(x) for x in data["solutions"])
        return "no solution"


# ---------------------------------------------------------------------------
# 10. Prime Counting Function
# ---------------------------------------------------------------------------

@register
class PrimeCountingGenerator(StepGenerator):
    """Compute pi(n) = number of primes <= n.

    Uses sieve of Eratosthenes for small n. Compares result with
    the prime number theorem estimate n/ln(n).

    Difficulty scaling:
        d1-2: n in [10, 20].
        d3-4: n in [15, 40].
        d5-6: n in [30, 70].
        d7-8: n in [50, 100].

    Prerequisites:
        primality.
    """

    _RANGES = {
        1: (10, 20), 2: (10, 20), 3: (15, 40), 4: (15, 40),
        5: (30, 70), 6: (30, 70), 7: (50, 100), 8: (50, 100),
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "prime_counting"

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
        return "compute prime counting function pi(n)"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a prime counting problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        lo, hi = self._RANGES.get(difficulty, self._RANGES[1])
        n = self._rng.randint(lo, hi)
        primes = _sieve(n)
        pi_n = len(primes)
        estimate = n / math.log(n) if n > 1 else 0.0
        error = abs(pi_n - estimate)
        problem = f"\\pi({n})"
        return problem, {
            "n": n, "primes": primes, "pi_n": pi_n,
            "estimate": round(estimate, 4),
            "error": round(error, 4),
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing sieve and comparison.
        """
        n = data["n"]
        primes = data["primes"]
        primes_str = str(primes[:10])
        if len(primes) > 10:
            primes_str = primes_str[:-1] + ", ...]"
        steps = [
            f"sieve up to {n}",
            f"primes: {primes_str}",
            f"pi({n})={data['pi_n']}",
            f"PNT estimate: {n}/ln({n})={_fmt(data['estimate'])}",
            f"error: |{data['pi_n']}-{_fmt(data['estimate'])}|={_fmt(data['error'])}",
        ]
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return pi(n).

        Args:
            data: Solution data dict.

        Returns:
            Prime count as string.
        """
        return str(data["pi_n"])
