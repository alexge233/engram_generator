"""Deep number theory generators -- Fermat, Wilson, Euler criterion, Miller-Rabin.

10 generators at tiers 5-6 covering Fermat's little theorem, Wilson's theorem,
extended CRT, Euler criterion, Carmichael numbers, discrete logarithm,
Miller-Rabin, sum of divisors formula, multiplicative functions, and perfect
power testing.
"""
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


# ---------------------------------------------------------------------------
# 1. Fermat's Little Theorem
# ---------------------------------------------------------------------------

@register
class FermatLittleGenerator(StepGenerator):
    """Apply Fermat's little theorem: a^{p-1} = 1 mod p for prime p.

    Computes a^{p-1} mod p and uses it for modular inverse:
    a^{-1} = a^{p-2} mod p.

    Difficulty scaling:
        d1-2: p from {5, 7, 11}, a from {2, 3, 4}.
        d3-4: p from {11, 13, 17, 19}, a from {2,...,8}.
        d5-6: p from {17, 19, 23, 29}, a from {2,...,12}.
        d7-8: p from {29, 31, 37, 41}, a from {2,...,15}.

    Prerequisites:
        mod_pow.
    """

    _POOLS = {
        "low": [5, 7, 11],
        "mid": [11, 13, 17, 19],
        "high_mid": [17, 19, 23, 29],
        "high": [29, 31, 37, 41],
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "fermat_little"

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
        return "apply Fermat's little theorem"

    def _pool(self, difficulty: int) -> list[int]:
        """Select prime pool by difficulty.

        Args:
            difficulty: Difficulty level.

        Returns:
            List of primes.
        """
        if difficulty <= 2:
            return self._POOLS["low"]
        if difficulty <= 4:
            return self._POOLS["mid"]
        if difficulty <= 6:
            return self._POOLS["high_mid"]
        return self._POOLS["high"]

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Fermat's little theorem problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        pool = self._pool(difficulty)
        p = self._rng.choice(pool)
        a = self._rng.randint(2, min(p - 1, 3 + difficulty * 2))
        fermat_result = pow(a, p - 1, p)
        inverse = pow(a, p - 2, p)
        problem = f"a={a}, p={p}"
        return problem, {
            "a": a, "p": p,
            "fermat_result": fermat_result,
            "inverse": inverse,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing Fermat's theorem and modular inverse.
        """
        a, p = data["a"], data["p"]
        return [
            f"Fermat: {a}^{{{p - 1}}} \\equiv 1 \\pmod{{{p}}}",
            f"{a}^{{{p - 1}}} mod {p} = {data['fermat_result']}",
            f"inverse: {a}^{{-1}} = {a}^{{{p - 2}}} mod {p} = {data['inverse']}",
            f"verify: {a}*{data['inverse']} mod {p} = {(a * data['inverse']) % p}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the modular inverse.

        Args:
            data: Solution data dict.

        Returns:
            Inverse as a string.
        """
        return str(data["inverse"])


# ---------------------------------------------------------------------------
# 2. Wilson's Theorem
# ---------------------------------------------------------------------------

@register
class WilsonTheoremGenerator(StepGenerator):
    """Apply Wilson's theorem: (p-1)! = -1 mod p iff p is prime.

    Computes (p-1)! mod p for small primes and verifies the theorem.

    Difficulty scaling:
        d1-2: p from {3, 5, 7}.
        d3-4: p from {7, 11, 13}.
        d5-6: p from {11, 13, 17}.
        d7-8: p from {13, 17, 19, 23}.

    Prerequisites:
        modular.
    """

    _POOLS = {
        1: [3, 5, 7], 2: [3, 5, 7],
        3: [7, 11, 13], 4: [7, 11, 13],
        5: [11, 13, 17], 6: [11, 13, 17],
        7: [13, 17, 19, 23], 8: [13, 17, 19, 23],
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "wilson_theorem"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

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
        return "verify Wilson's theorem"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Wilson's theorem problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        pool = self._POOLS.get(difficulty, self._POOLS[1])
        p = self._rng.choice(pool)
        factorial_mod = 1
        trace_steps: list[str] = []
        for i in range(2, p):
            factorial_mod = (factorial_mod * i) % p
            if i <= 6 or i == p - 1:
                trace_steps.append(f"{i}!\\equiv {factorial_mod} \\pmod{{{p}}}")
        problem = f"({p}-1)! \\mod {p}"
        return problem, {
            "p": p, "result": factorial_mod,
            "expected": p - 1,
            "trace": trace_steps,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing factorial computation and verification.
        """
        p = data["p"]
        steps = data["trace"][:4]
        if len(data["trace"]) > 4:
            steps.append("\\ldots")
            steps.append(data["trace"][-1])
        steps.append(f"({p}-1)! \\equiv {data['result']} \\equiv -1 \\pmod{{{p}}}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return (p-1)! mod p.

        Args:
            data: Solution data dict.

        Returns:
            Result as a string.
        """
        return str(data["result"])


# ---------------------------------------------------------------------------
# 3. Chinese Remainder Theorem (Extended)
# ---------------------------------------------------------------------------

@register
class ChineseRemainderExtGenerator(StepGenerator):
    """Solve a system of 3-4 congruences using CRT step-by-step.

    Shows the CRT construction: N_i = N/n_i, y_i = N_i^{-1} mod n_i,
    x = sum a_i * N_i * y_i mod N.

    Difficulty scaling:
        d1-3: 3 congruences with small moduli.
        d4-6: 3 congruences with moderate moduli.
        d7-8: 4 congruences.

    Prerequisites:
        crt.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "chinese_remainder_ext"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["crt"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "solve system of congruences via CRT"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a CRT system problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            moduli = [3, 5, 7]
        elif difficulty <= 6:
            choices = [[3, 5, 7], [3, 7, 11], [5, 7, 11], [3, 5, 11]]
            moduli = self._rng.choice(choices)
        else:
            choices = [[3, 5, 7, 11], [3, 5, 7, 13], [3, 7, 11, 13]]
            moduli = self._rng.choice(choices)
        remainders = [self._rng.randint(0, m - 1) for m in moduli]
        big_n = 1
        for m in moduli:
            big_n *= m
        big_ns = [big_n // m for m in moduli]
        ys = [_mod_inverse(big_ns[i], moduli[i]) for i in range(len(moduli))]
        x = sum(remainders[i] * big_ns[i] * ys[i] for i in range(len(moduli))) % big_n
        congs = ", ".join(
            f"x\\equiv {remainders[i]} \\pmod{{{moduli[i]}}}"
            for i in range(len(moduli))
        )
        problem = congs
        return problem, {
            "moduli": moduli, "remainders": remainders,
            "big_n": big_n, "big_ns": big_ns, "ys": ys, "x": x,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing the CRT construction.
        """
        steps = [f"N={data['big_n']}"]
        for i, (m, a, ni, yi) in enumerate(zip(
            data["moduli"], data["remainders"], data["big_ns"], data["ys"]
        )):
            steps.append(f"N_{i + 1}={ni}, y_{i + 1}={ni}^{{-1}} mod {m}={yi}")
        terms = [f"{a}*{ni}*{yi}"
                 for a, ni, yi in zip(data["remainders"], data["big_ns"], data["ys"])]
        steps.append(f"x={'+'.join(terms)} mod {data['big_n']}={data['x']}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the CRT solution.

        Args:
            data: Solution data dict.

        Returns:
            Solution x as a string.
        """
        return str(data["x"])


# ---------------------------------------------------------------------------
# 4. Euler Criterion
# ---------------------------------------------------------------------------

@register
class EulerCriterionGenerator(StepGenerator):
    """Compute Legendre symbol via Euler criterion.

    a^((p-1)/2) = (a/p) mod p. Returns 1 if a is a quadratic residue,
    -1 (i.e. p-1) if not, 0 if p divides a.

    Difficulty scaling:
        d1-2: p from {5, 7, 11}, a=2-4.
        d3-4: p from {11, 13, 17}, a=2-8.
        d5-6: p from {17, 19, 23}, a=2-12.
        d7-8: p from {23, 29, 31, 37}, a=2-15.

    Prerequisites:
        mod_pow.
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
        return "euler_criterion"

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
        return "compute Legendre symbol via Euler criterion"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an Euler criterion problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        pool = self._POOLS.get(difficulty, self._POOLS[1])
        p = self._rng.choice(pool)
        a = self._rng.randint(2, min(p - 1, 3 + difficulty * 2))
        exp = (p - 1) // 2
        result = pow(a, exp, p)
        legendre = 1 if result == 1 else -1
        problem = f"\\left(\\frac{{{a}}}{{{p}}}\\right) via Euler"
        return problem, {
            "a": a, "p": p, "exp": exp,
            "result": result, "legendre": legendre,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing the Euler criterion computation.
        """
        a, p = data["a"], data["p"]
        return [
            f"Euler: a^{{(p-1)/2}} mod p",
            f"{a}^{{{data['exp']}}} mod {p} = {data['result']}",
            f"{data['result']} {'= 1 (QR)' if data['legendre'] == 1 else '= p-1 (NR)'}",
            f"({a}/{p}) = {data['legendre']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the Legendre symbol.

        Args:
            data: Solution data dict.

        Returns:
            Legendre symbol as a string.
        """
        return str(data["legendre"])


# ---------------------------------------------------------------------------
# 5. Carmichael Number Test
# ---------------------------------------------------------------------------

@register
class CarmichaelNumberGenerator(StepGenerator):
    """Test if n is a Carmichael number.

    A Carmichael number is composite but a^{n-1} = 1 mod n for all
    a with gcd(a,n)=1. Tests with witnesses a=2,3,5,7.

    Difficulty scaling:
        d1-3: test known Carmichaels (561, 1105).
        d4-6: test near-Carmichaels and composites.
        d7-8: larger Carmichaels (1729, 2465, 2821).

    Prerequisites:
        mod_pow.
    """

    _CARMICHAELS = [561, 1105, 1729, 2465, 2821]
    _NON_CARMICHAELS = [15, 21, 35, 45, 63, 91, 105, 231, 341, 645]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "carmichael_number"

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
        return "test if number is Carmichael"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Carmichael number test problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            pool = self._CARMICHAELS[:2] + self._NON_CARMICHAELS[:3]
        elif difficulty <= 6:
            pool = self._CARMICHAELS[:3] + self._NON_CARMICHAELS[3:7]
        else:
            pool = self._CARMICHAELS + self._NON_CARMICHAELS[5:]
        n = self._rng.choice(pool)
        witnesses = [a for a in [2, 3, 5, 7] if math.gcd(a, n) == 1]
        results = {}
        is_carmichael = True
        for a in witnesses:
            r = pow(a, n - 1, n)
            results[a] = r
            if r != 1:
                is_carmichael = False
        is_carmichael = is_carmichael and not _is_prime(n)
        problem = f"Carmichael test: n={n}"
        return problem, {
            "n": n, "witnesses": witnesses,
            "results": results, "is_carmichael": is_carmichael,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing the witness tests.
        """
        n = data["n"]
        steps = [f"n={n} is {'prime' if _is_prime(n) else 'composite'}"]
        for a in data["witnesses"]:
            r = data["results"][a]
            status = "pass" if r == 1 else f"FAIL ({r})"
            steps.append(f"{a}^{{{n - 1}}} mod {n} = {r} [{status}]")
        verdict = "Carmichael" if data["is_carmichael"] else "not Carmichael"
        steps.append(f"verdict: {verdict}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return whether n is Carmichael.

        Args:
            data: Solution data dict.

        Returns:
            'Carmichael' or 'not Carmichael'.
        """
        return "Carmichael" if data["is_carmichael"] else "not Carmichael"


# ---------------------------------------------------------------------------
# 6. Discrete Logarithm (Baby-Step Giant-Step)
# ---------------------------------------------------------------------------

@register
class DiscreteLogarithmGenerator(StepGenerator):
    """Find x such that g^x = h mod p using baby-step giant-step.

    For small primes, computes m = ceil(sqrt(p)), builds baby-step
    table {g^j mod p : j=0..m-1}, then checks giant steps.

    Difficulty scaling:
        d1-2: p from {7, 11, 13}.
        d3-4: p from {13, 17, 19}.
        d5-6: p from {19, 23, 29}.
        d7-8: p from {29, 31, 37}.

    Prerequisites:
        mod_pow.
    """

    _POOLS = {
        1: [7, 11, 13], 2: [7, 11, 13],
        3: [13, 17, 19], 4: [13, 17, 19],
        5: [19, 23, 29], 6: [19, 23, 29],
        7: [29, 31, 37], 8: [29, 31, 37],
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "discrete_logarithm"

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
        return "find discrete logarithm via baby-step giant-step"

    def _find_generator(self, p: int) -> int:
        """Find a primitive root modulo p.

        Args:
            p: An odd prime.

        Returns:
            A primitive root.
        """
        phi = p - 1
        factors = _factorise(phi)
        divisors = [phi // f for f, _ in factors]
        for g in range(2, p):
            if all(pow(g, d, p) != 1 for d in divisors):
                return g
        return 2  # pragma: no cover

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a discrete logarithm problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        pool = self._POOLS.get(difficulty, self._POOLS[1])
        p = self._rng.choice(pool)
        g = self._find_generator(p)
        x_true = self._rng.randint(1, p - 2)
        h = pow(g, x_true, p)
        m = math.isqrt(p - 1) + 1
        baby = {}
        val = 1
        for j in range(m):
            baby[val] = j
            val = (val * g) % p
        g_inv_m = pow(g, (p - 1) - m, p)
        gamma = h
        x_found = -1
        for i in range(m):
            if gamma in baby:
                x_found = i * m + baby[gamma]
                break
            gamma = (gamma * g_inv_m) % p
        problem = f"g={g}, h={h}, p={p}: find x s.t. g^x=h mod p"
        return problem, {
            "g": g, "h": h, "p": p,
            "m": m, "x": x_found if x_found >= 0 else x_true,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing baby-step giant-step algorithm.
        """
        g, h, p, m = data["g"], data["h"], data["p"], data["m"]
        return [
            f"m=ceil(sqrt({p - 1}))={m}",
            f"baby steps: g^j mod {p} for j=0..{m - 1}",
            f"giant steps: h*g^{{-m*i}} mod {p} for i=0..{m - 1}",
            f"match found: x={data['x']}",
            f"verify: {g}^{{{data['x']}}} mod {p}={pow(g, data['x'], p)}={h}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the discrete logarithm.

        Args:
            data: Solution data dict.

        Returns:
            x as a string.
        """
        return str(data["x"])


# ---------------------------------------------------------------------------
# 7. Miller-Rabin Primality Test
# ---------------------------------------------------------------------------

@register
class MillerRabinGenerator(StepGenerator):
    """Perform Miller-Rabin primality test.

    Write n-1 = 2^s*d. Check if a^d = 1 mod n or a^{2^r*d} = -1 mod n
    for some r in 0..s-1.

    Difficulty scaling:
        d1-2: small primes and composites (10-50).
        d3-4: range 20-100.
        d5-6: range 50-200.
        d7-8: range 100-500.

    Prerequisites:
        mod_pow.
    """

    _RANGES = {
        1: (10, 50), 2: (10, 50), 3: (20, 100), 4: (20, 100),
        5: (50, 200), 6: (50, 200), 7: (100, 500), 8: (100, 500),
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "miller_rabin"

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
        return "perform Miller-Rabin primality test"

    def _decompose(self, n: int) -> tuple[int, int]:
        """Write n-1 = 2^s * d with d odd.

        Args:
            n: Odd integer > 2.

        Returns:
            Tuple (s, d).
        """
        s = 0
        d = n - 1
        while d % 2 == 0:
            d //= 2
            s += 1
        return s, d

    def _test_witness(self, a: int, n: int, s: int, d: int) -> tuple[bool, list[str]]:
        """Test a single Miller-Rabin witness.

        Args:
            a: Witness base.
            n: Number to test.
            s: Exponent of 2 in n-1.
            d: Odd part of n-1.

        Returns:
            Tuple (probably_prime, trace_steps).
        """
        x = pow(a, d, n)
        trace = [f"a={a}: a^d={a}^{d} mod {n}={x}"]
        if x == 1 or x == n - 1:
            trace.append(f"  -> probably prime")
            return True, trace
        for r in range(1, s):
            x = pow(x, 2, n)
            trace.append(f"  a^{{2^{r}*d}} mod {n}={x}")
            if x == n - 1:
                trace.append(f"  -> probably prime")
                return True, trace
        trace.append(f"  -> composite witness")
        return False, trace

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Miller-Rabin test problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        lo, hi = self._RANGES.get(difficulty, self._RANGES[1])
        n = self._rng.randint(lo, hi)
        if n % 2 == 0:
            n += 1
        if n < 5:
            n = 5
        s, d = self._decompose(n)
        witnesses = [a for a in [2, 3, 5, 7] if a < n]
        all_trace: list[str] = [f"n-1={n - 1}=2^{s}*{d}"]
        final_verdict = True
        for a in witnesses[:2]:
            prob_prime, trace = self._test_witness(a, n, s, d)
            all_trace.extend(trace)
            if not prob_prime:
                final_verdict = False
                break
        actual = _is_prime(n)
        problem = f"Miller-Rabin: n={n}"
        return problem, {
            "n": n, "s": s, "d": d,
            "trace": all_trace,
            "verdict": "probably prime" if final_verdict else "composite",
            "actual": actual,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing the Miller-Rabin test.
        """
        steps = data["trace"][:6]
        if len(data["trace"]) > 6:
            steps.append("\\ldots")
        steps.append(f"verdict: {data['verdict']}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the primality verdict.

        Args:
            data: Solution data dict.

        Returns:
            'probably prime' or 'composite'.
        """
        return data["verdict"]


# ---------------------------------------------------------------------------
# 8. Sum of Divisors Formula
# ---------------------------------------------------------------------------

@register
class SumOfDivisorsFormulaGenerator(StepGenerator):
    """Compute sigma(n) using the prime factorisation formula.

    sigma(n) = prod (p^{a+1}-1)/(p-1) from prime factorisation n = prod p^a.

    Difficulty scaling:
        d1-2: n in [6, 30].
        d3-4: n in [20, 80].
        d5-6: n in [50, 150].
        d7-8: n in [100, 300].

    Prerequisites:
        factorisation.
    """

    _RANGES = {
        1: (6, 30), 2: (6, 30), 3: (20, 80), 4: (20, 80),
        5: (50, 150), 6: (50, 150), 7: (100, 300), 8: (100, 300),
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "sum_of_divisors_formula"

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
        return "compute sum of divisors via factorisation formula"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a sum of divisors problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        lo, hi = self._RANGES.get(difficulty, self._RANGES[1])
        n = self._rng.randint(lo, hi)
        if n < 2:
            n = 6
        factors = _factorise(n)
        sigma = 1
        parts = []
        for p, a in factors:
            term = (p ** (a + 1) - 1) // (p - 1)
            sigma *= term
            parts.append((p, a, term))
        brute = sum(d for d in range(1, n + 1) if n % d == 0)
        problem = f"\\sigma({n})"
        return problem, {
            "n": n, "factors": factors,
            "parts": parts, "sigma": sigma, "brute": brute,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing the formula application.
        """
        n = data["n"]
        fac_str = " \\cdot ".join(
            f"{p}^{{{a}}}" if a > 1 else str(p) for p, a in data["factors"]
        )
        steps = [f"{n} = {fac_str}"]
        for p, a, term in data["parts"]:
            steps.append(f"({p}^{{{a + 1}}}-1)/({p}-1)=({p ** (a + 1)}-1)/{p - 1}={term}")
        product_str = "*".join(str(t) for _, _, t in data["parts"])
        steps.append(f"\\sigma({n})={product_str}={data['sigma']}")
        steps.append(f"verify: brute force sum={data['brute']}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return sigma(n).

        Args:
            data: Solution data dict.

        Returns:
            Sum of divisors as a string.
        """
        return str(data["sigma"])


# ---------------------------------------------------------------------------
# 9. Multiplicative Function Verification
# ---------------------------------------------------------------------------

@register
class MultiplicativeFunctionGenerator(StepGenerator):
    """Verify multiplicativity of phi and tau.

    phi(mn) = phi(m)*phi(n) when gcd(m,n)=1.
    tau(mn) = tau(m)*tau(n) when gcd(m,n)=1.

    Difficulty scaling:
        d1-2: m,n from coprime pairs < 20.
        d3-4: m,n from coprime pairs < 50.
        d5-6: m,n from coprime pairs < 100.
        d7-8: m,n from coprime pairs < 200.

    Prerequisites:
        totient.
    """

    _RANGES = {
        1: (2, 20), 2: (2, 20), 3: (2, 50), 4: (2, 50),
        5: (2, 100), 6: (2, 100), 7: (2, 200), 8: (2, 200),
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "multiplicative_function"

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
        return "verify multiplicativity of phi and tau"

    def _count_divisors(self, n: int) -> int:
        """Count divisors of n from its factorisation.

        Args:
            n: Positive integer.

        Returns:
            Number of divisors.
        """
        factors = _factorise(n)
        result = 1
        for _, a in factors:
            result *= (a + 1)
        return result

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a multiplicative function verification problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        lo, hi = self._RANGES.get(difficulty, self._RANGES[1])
        for _ in range(50):
            m = self._rng.randint(lo, hi)
            n = self._rng.randint(lo, hi)
            if math.gcd(m, n) == 1 and m > 1 and n > 1:
                break
        phi_m = _euler_totient(m)
        phi_n = _euler_totient(n)
        phi_mn = _euler_totient(m * n)
        tau_m = self._count_divisors(m)
        tau_n = self._count_divisors(n)
        tau_mn = self._count_divisors(m * n)
        problem = f"verify \\phi({m}*{n})=\\phi({m})*\\phi({n})"
        return problem, {
            "m": m, "n": n, "mn": m * n,
            "phi_m": phi_m, "phi_n": phi_n, "phi_mn": phi_mn,
            "tau_m": tau_m, "tau_n": tau_n, "tau_mn": tau_mn,
            "phi_ok": phi_mn == phi_m * phi_n,
            "tau_ok": tau_mn == tau_m * tau_n,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing verification.
        """
        m, n = data["m"], data["n"]
        return [
            f"gcd({m},{n})=1",
            f"\\phi({m})={data['phi_m']}, \\phi({n})={data['phi_n']}, \\phi({m * n})={data['phi_mn']}",
            f"\\phi({m})*\\phi({n})={data['phi_m'] * data['phi_n']}={'=' if data['phi_ok'] else '!='}{data['phi_mn']}",
            f"\\tau({m})={data['tau_m']}, \\tau({n})={data['tau_n']}, \\tau({m * n})={data['tau_mn']}",
            f"\\tau({m})*\\tau({n})={data['tau_m'] * data['tau_n']}={'=' if data['tau_ok'] else '!='}{data['tau_mn']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the verification result.

        Args:
            data: Solution data dict.

        Returns:
            phi and tau verification results.
        """
        return f"phi:{'verified' if data['phi_ok'] else 'failed'}, tau:{'verified' if data['tau_ok'] else 'failed'}"


# ---------------------------------------------------------------------------
# 10. Perfect Power Test
# ---------------------------------------------------------------------------

@register
class PerfectPowerTestGenerator(StepGenerator):
    """Check if n = a^k for some integers a, k >= 2.

    Tests k=2, 3, ..., floor(log2(n)) and checks if the k-th root
    is an integer.

    Difficulty scaling:
        d1-2: n in [4, 50] (many perfect powers).
        d3-4: n in [10, 200].
        d5-6: n in [50, 500].
        d7-8: n in [100, 1000].

    Prerequisites:
        exponentiation.
    """

    _RANGES = {
        1: (4, 50), 2: (4, 50), 3: (10, 200), 4: (10, 200),
        5: (50, 500), 6: (50, 500), 7: (100, 1000), 8: (100, 1000),
    }

    _PERFECT_POWERS = [4, 8, 9, 16, 25, 27, 32, 36, 49, 64, 81, 100, 121,
                       125, 128, 144, 169, 196, 216, 225, 243, 256, 289,
                       324, 343, 361, 400, 441, 484, 512, 529, 625, 729, 1000]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "perfect_power_test"

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
        return "test if number is a perfect power"

    def _check_perfect_power(self, n: int) -> tuple[bool, int, int]:
        """Check if n is a perfect power.

        Args:
            n: Positive integer >= 2.

        Returns:
            Tuple (is_power, base, exponent). If not a power, base=exponent=0.
        """
        max_k = int(math.log2(n)) + 1
        for k in range(2, max_k + 1):
            a = round(n ** (1.0 / k))
            for candidate in [a - 1, a, a + 1]:
                if candidate >= 2 and candidate ** k == n:
                    return True, candidate, k
        return False, 0, 0

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a perfect power test problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        lo, hi = self._RANGES.get(difficulty, self._RANGES[1])
        if self._rng.random() < 0.5:
            candidates = [p for p in self._PERFECT_POWERS if lo <= p <= hi]
            if candidates:
                n = self._rng.choice(candidates)
            else:
                n = self._rng.randint(lo, hi)
        else:
            n = self._rng.randint(lo, hi)
        is_power, base, exp = self._check_perfect_power(n)
        max_k = int(math.log2(n)) + 1
        problem = f"is {n} = a^k for a,k >= 2?"
        return problem, {
            "n": n, "is_power": is_power,
            "base": base, "exp": exp, "max_k": max_k,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing the test for each k.
        """
        n = data["n"]
        steps = [f"test k=2,...,{data['max_k']}"]
        for k in range(2, min(data["max_k"] + 1, 6)):
            a = round(n ** (1.0 / k))
            if a >= 2 and a ** k == n:
                steps.append(f"k={k}: {a}^{k}={a ** k}={n} YES")
            else:
                steps.append(f"k={k}: {a}^{k}={a ** k}!={n}")
        if data["is_power"]:
            steps.append(f"{n}={data['base']}^{data['exp']}")
        else:
            steps.append(f"{n} is not a perfect power")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the perfect power verdict.

        Args:
            data: Solution data dict.

        Returns:
            Decomposition or 'not a perfect power'.
        """
        if data["is_power"]:
            return f"{data['base']}^{data['exp']}"
        return "not a perfect power"
