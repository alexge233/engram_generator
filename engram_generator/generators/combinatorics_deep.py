"""Deep combinatorics generators -- generating functions, species, Polya.

10 generators at tiers 3-6 covering Fibonacci identities, Pascal's triangle,
Vandermonde identity, exponential generating functions, Polya enumeration,
recurrence characteristic equations, Catalan applications, double counting,
pigeonhole applications, and compositions.
"""
from __future__ import annotations

import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _fib(n: int) -> int:
    """Compute the n-th Fibonacci number.

    Args:
        n: Non-negative index.

    Returns:
        F_n.
    """
    if n <= 0:
        return 0
    a, b = 0, 1
    for _ in range(n - 1):
        a, b = b, a + b
    return b


def _comb(n: int, k: int) -> int:
    """Compute binomial coefficient C(n, k).

    Args:
        n: Total items.
        k: Items to choose.

    Returns:
        C(n, k).
    """
    if k < 0 or k > n:
        return 0
    return math.comb(n, k)


def _catalan(n: int) -> int:
    """Compute the n-th Catalan number.

    Args:
        n: Non-negative index.

    Returns:
        C_n = C(2n, n) / (n + 1).
    """
    return math.comb(2 * n, n) // (n + 1)


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
# 1. Fibonacci Identity (tier 4)
# ---------------------------------------------------------------------------

@register
class FibonacciIdentityGenerator(StepGenerator):
    """Verify Fibonacci identities for given m, n.

    Checks F_{m+n} = F_m * F_{n+1} + F_{m-1} * F_n and
    Cassini's identity F_{n-1}*F_{n+1} - F_n^2 = (-1)^n.

    Difficulty scaling:
        d1-2: m, n in [2, 5].
        d3-4: m, n in [3, 8].
        d5-6: m, n in [5, 12].
        d7-8: m, n in [7, 15].

    Prerequisites:
        multiplication.
    """

    _RANGES = {
        1: (2, 5), 2: (2, 5), 3: (3, 8), 4: (3, 8),
        5: (5, 12), 6: (5, 12), 7: (7, 15), 8: (7, 15),
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "fibonacci_identity"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["multiplication"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "verify Fibonacci identities"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Fibonacci identity verification problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        lo, hi = self._RANGES.get(difficulty, self._RANGES[1])
        m = self._rng.randint(lo, hi)
        n = self._rng.randint(lo, hi)
        # Addition identity: F_{m+n} = F_m * F_{n+1} + F_{m-1} * F_n
        f_mn = _fib(m + n)
        f_m = _fib(m)
        f_n1 = _fib(n + 1)
        f_m1 = _fib(m - 1)
        f_n = _fib(n)
        lhs_add = f_mn
        rhs_add = f_m * f_n1 + f_m1 * f_n
        # Cassini: F_{n-1}*F_{n+1} - F_n^2 = (-1)^n
        f_n_minus1 = _fib(n - 1)
        cassini_lhs = f_n_minus1 * f_n1 - f_n * f_n
        cassini_rhs = (-1) ** n
        problem = f"Fibonacci: m={m}, n={n}"
        return problem, {
            "m": m, "n": n,
            "f_m": f_m, "f_n": f_n, "f_mn": f_mn,
            "f_n1": f_n1, "f_m1": f_m1,
            "lhs_add": lhs_add, "rhs_add": rhs_add,
            "add_ok": lhs_add == rhs_add,
            "cassini_lhs": cassini_lhs, "cassini_rhs": cassini_rhs,
            "cassini_ok": cassini_lhs == cassini_rhs,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing identity verification.
        """
        m, n = data["m"], data["n"]
        return [
            f"F_{{{m}}}={data['f_m']}, F_{{{n}}}={data['f_n']}, "
            f"F_{{{m + n}}}={data['f_mn']}",
            f"F_{{{m}}}*F_{{{n + 1}}}+F_{{{m - 1}}}*F_{{{n}}}"
            f"={data['f_m']}*{data['f_n1']}+{data['f_m1']}*{data['f_n']}"
            f"={data['rhs_add']}",
            f"addition identity: {'verified' if data['add_ok'] else 'failed'}",
            f"Cassini: F_{{{n - 1}}}*F_{{{n + 1}}}-F_{{{n}}}^2"
            f"={data['cassini_lhs']}=(-1)^{n}={data['cassini_rhs']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return verification results.

        Args:
            data: Solution data dict.

        Returns:
            Identity verification status.
        """
        a = "add:verified" if data["add_ok"] else "add:failed"
        c = "cassini:verified" if data["cassini_ok"] else "cassini:failed"
        return f"{a}, {c}"


# ---------------------------------------------------------------------------
# 2. Pascal's Triangle (tier 3)
# ---------------------------------------------------------------------------

@register
class PascalTriangleGenerator(StepGenerator):
    """Generate row n of Pascal's triangle and verify the recurrence.

    Verifies C(n,k) = C(n-1,k-1) + C(n-1,k) for each entry.

    Difficulty scaling:
        d1-2: n in [3, 5].
        d3-4: n in [5, 7].
        d5-6: n in [6, 9].
        d7-8: n in [8, 12].

    Prerequisites:
        addition.
    """

    _RANGES = {
        1: (3, 5), 2: (3, 5), 3: (5, 7), 4: (5, 7),
        5: (6, 9), 6: (6, 9), 7: (8, 12), 8: (8, 12),
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "pascal_triangle"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 3

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["addition"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "generate Pascal's triangle row"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Pascal's triangle problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        lo, hi = self._RANGES.get(difficulty, self._RANGES[1])
        n = self._rng.randint(lo, hi)
        row = [_comb(n, k) for k in range(n + 1)]
        # Verify recurrence for a few k
        checks: list[tuple[int, int, int, int]] = []
        for k in range(1, min(n, 4)):
            left = _comb(n - 1, k - 1)
            right = _comb(n - 1, k)
            checks.append((k, left, right, left + right))
        problem = f"Pascal row {n}"
        return problem, {
            "n": n, "row": row, "checks": checks,
            "row_sum": sum(row),
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing row generation and verification.
        """
        n = data["n"]
        row_str = " ".join(str(x) for x in data["row"])
        steps = [f"row {n}: {row_str}"]
        for k, left, right, total in data["checks"]:
            steps.append(
                f"C({n},{k})=C({n - 1},{k - 1})+C({n - 1},{k})"
                f"={left}+{right}={total}"
            )
        steps.append(f"row sum=2^{n}={data['row_sum']}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the row.

        Args:
            data: Solution data dict.

        Returns:
            Row as space-separated string.
        """
        return " ".join(str(x) for x in data["row"])


# ---------------------------------------------------------------------------
# 3. Vandermonde Identity (tier 4)
# ---------------------------------------------------------------------------

@register
class VandermondeIdentityGenerator(StepGenerator):
    """Verify Vandermonde's identity: C(m+n,r) = sum C(m,k)*C(n,r-k).

    Computes both sides for given m, n, r and verifies equality.

    Difficulty scaling:
        d1-2: m,n in [2, 4], r in [1, 3].
        d3-4: m,n in [3, 6], r in [2, 5].
        d5-6: m,n in [4, 8], r in [3, 7].
        d7-8: m,n in [5, 10], r in [4, 9].

    Prerequisites:
        binomial.
    """

    _RANGES = {
        1: (2, 4, 1, 3), 2: (2, 4, 1, 3),
        3: (3, 6, 2, 5), 4: (3, 6, 2, 5),
        5: (4, 8, 3, 7), 6: (4, 8, 3, 7),
        7: (5, 10, 4, 9), 8: (5, 10, 4, 9),
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "vandermonde_identity"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["binomial"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "verify Vandermonde's identity"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Vandermonde identity problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        mnlo, mnhi, rlo, rhi = self._RANGES.get(difficulty, self._RANGES[1])
        m = self._rng.randint(mnlo, mnhi)
        n = self._rng.randint(mnlo, mnhi)
        r = self._rng.randint(rlo, min(rhi, m + n))
        lhs = _comb(m + n, r)
        terms: list[tuple[int, int, int, int]] = []
        rhs = 0
        for k in range(r + 1):
            ck_m = _comb(m, k)
            ck_n = _comb(n, r - k)
            product = ck_m * ck_n
            if product > 0:
                terms.append((k, ck_m, ck_n, product))
            rhs += product

        problem = f"C({m + n},{r})=sum C({m},k)*C({n},{r}-k)"
        return problem, {
            "m": m, "n": n, "r": r,
            "lhs": lhs, "rhs": rhs,
            "terms": terms, "verified": lhs == rhs,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing the summation.
        """
        m, n, r = data["m"], data["n"], data["r"]
        steps = [f"LHS: C({m + n},{r})={data['lhs']}"]
        for k, cm, cn, prod in data["terms"][:5]:
            steps.append(f"k={k}: C({m},{k})*C({n},{r - k})={cm}*{cn}={prod}")
        steps.append(f"RHS sum={data['rhs']}")
        steps.append(f"{'verified' if data['verified'] else 'failed'}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the verification result.

        Args:
            data: Solution data dict.

        Returns:
            LHS value and status.
        """
        return f"{data['lhs']} ({'verified' if data['verified'] else 'failed'})"


# ---------------------------------------------------------------------------
# 4. Exponential Generating Function (tier 6)
# ---------------------------------------------------------------------------

@register
class ExponentialGFGenerator(StepGenerator):
    """Extract coefficients from exponential generating functions.

    EGF for labeled structures: e^x for sets (coeff of x^n/n! = 1),
    1/(1-x) for permutations (coeff of x^n/n! = n!). Computes
    [x^n/n!] of given EGF.

    Difficulty scaling:
        d1-2: e^x, n in [2, 4].
        d3-4: e^{cx}, n in [2, 5].
        d5-6: e^x * (1+x), n in [3, 6].
        d7-8: e^{2x} - e^x, n in [3, 7].

    Prerequisites:
        exponentiation.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "exponential_gf"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

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
        return "extract coefficient from exponential generating function"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an EGF coefficient extraction problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 2:
            n = self._rng.randint(2, 4)
            egf_name = "e^x"
            # [x^n/n!] of e^x is 1, so a_n = n! * 1 = 1 (labeled count)
            coeff = 1
            a_n = coeff * math.factorial(n)
            explanation = f"[x^{n}] e^x = 1/{n}!, a_{n} = {n}!*1/{n}! = 1"
        elif difficulty <= 4:
            c = self._rng.randint(2, 3)
            n = self._rng.randint(2, 5)
            egf_name = f"e^{{{c}x}}"
            # [x^n/n!] of e^{cx} is c^n/n!, so a_n = c^n
            coeff = c ** n
            a_n = coeff
            explanation = f"[x^{n}/{n}!] e^{{{c}x}} = {c}^{n}/{n}! -> a_{n}={c}^{n}={coeff}"
        elif difficulty <= 6:
            n = self._rng.randint(3, 6)
            egf_name = "e^x(1+x)"
            # e^x(1+x) = e^x + x*e^x
            # [x^n/n!] = 1/n! + 1/(n-1)! = (1 + n)/n!
            # a_n = 1 + n
            a_n = 1 + n
            coeff = a_n
            explanation = f"[x^{n}/{n}!] = 1/{n}! + 1/{n - 1}! = (1+{n})/{n}!"
        else:
            n = self._rng.randint(3, 7)
            egf_name = "e^{2x}-e^x"
            # [x^n/n!] of e^{2x}-e^x = (2^n - 1)/n!
            # a_n = 2^n - 1
            a_n = 2 ** n - 1
            coeff = a_n
            explanation = f"[x^{n}/{n}!] = (2^{n}-1)/{n}! -> a_{n}=2^{n}-1={a_n}"

        problem = f"[x^{n}/{n}!] of {egf_name}"
        return problem, {
            "n": n, "egf_name": egf_name,
            "a_n": a_n, "coeff": coeff,
            "explanation": explanation,
            "n_factorial": math.factorial(n),
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing coefficient extraction.
        """
        return [
            f"EGF: {data['egf_name']}",
            f"n={data['n']}, {data['n']}!={data['n_factorial']}",
            data["explanation"],
            f"a_{{{data['n']}}}={data['a_n']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the coefficient.

        Args:
            data: Solution data dict.

        Returns:
            a_n as string.
        """
        return str(data["a_n"])


# ---------------------------------------------------------------------------
# 5. Polya Enumeration (tier 6)
# ---------------------------------------------------------------------------

@register
class PolyaEnumerationGenerator(StepGenerator):
    """Count distinct necklaces using Burnside/Polya enumeration.

    For n beads with k colors under cyclic group:
    Z(C_n) = (1/n) * sum_{d|n} phi(d) * k^{n/d}.

    Difficulty scaling:
        d1-2: n in [3, 4], k=2.
        d3-4: n in [4, 6], k=2.
        d5-6: n in [4, 6], k=3.
        d7-8: n in [5, 8], k=3.

    Prerequisites:
        catalan.
    """

    _CONFIGS = {
        1: (3, 4, 2), 2: (3, 4, 2), 3: (4, 6, 2), 4: (4, 6, 2),
        5: (4, 6, 3), 6: (4, 6, 3), 7: (5, 8, 3), 8: (5, 8, 3),
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "polya_enumeration"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["catalan"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "count necklaces via Polya enumeration"

    def _divisors(self, n: int) -> list[int]:
        """Return sorted divisors of n.

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

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Polya enumeration problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        nlo, nhi, k = self._CONFIGS.get(difficulty, self._CONFIGS[1])
        n = self._rng.randint(nlo, nhi)
        divs = self._divisors(n)
        terms: list[tuple[int, int, int]] = []
        total = 0
        for d in divs:
            phi_d = _euler_totient(d)
            power = k ** (n // d)
            contrib = phi_d * power
            terms.append((d, phi_d, power))
            total += contrib
        necklaces = total // n

        problem = f"necklaces: {n} beads, {k} colors"
        return problem, {
            "n": n, "k": k, "divs": divs,
            "terms": terms, "total": total,
            "necklaces": necklaces,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing the Polya formula.
        """
        n, k = data["n"], data["k"]
        steps = [f"Z(C_{n}): divisors of {n}={data['divs']}"]
        for d, phi_d, power in data["terms"]:
            steps.append(f"d={d}: phi({d})={phi_d}, {k}^{{{n // d}}}={power}")
        steps.append(f"sum={data['total']}, necklaces={data['total']}/{n}={data['necklaces']}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the number of necklaces.

        Args:
            data: Solution data dict.

        Returns:
            Count as string.
        """
        return str(data["necklaces"])


# ---------------------------------------------------------------------------
# 6. Recurrence Characteristic Equation (tier 5)
# ---------------------------------------------------------------------------

@register
class RecurrenceCharacteristicGenerator(StepGenerator):
    """Solve linear recurrence via characteristic equation.

    For a_n = c1*a_{n-1} + c2*a_{n-2}, the characteristic equation
    is r^2 - c1*r - c2 = 0. General solution a_n = A*r1^n + B*r2^n.

    Difficulty scaling:
        d1-2: c1,c2 in [1,2], integer roots.
        d3-4: c1,c2 in [1,3], integer roots.
        d5-6: c1,c2 in [1,4], may have repeated roots.
        d7-8: c1,c2 in [1,5], may have irrational roots.

    Prerequisites:
        binomial.
    """

    _NICE_PAIRS = [
        (3, -2, 1, 2), (5, -6, 2, 3), (4, -3, 1, 3),
        (7, -10, 2, 5), (6, -8, 2, 4), (5, -4, 1, 4),
        (7, -12, 3, 4), (8, -15, 3, 5), (9, -20, 4, 5),
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "recurrence_characteristic"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["binomial"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "solve recurrence via characteristic equation"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a characteristic equation problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 4:
            pool = self._NICE_PAIRS[:4]
        elif difficulty <= 6:
            pool = self._NICE_PAIRS[:7]
        else:
            pool = self._NICE_PAIRS

        c1, c2, r1, r2 = self._rng.choice(pool)
        # a_0 = 1, a_1 = 1
        a0, a1 = 1, 1
        disc = c1 * c1 + 4 * c2
        # For distinct integer roots: A*r1^0 + B*r2^0 = a0, A*r1 + B*r2 = a1
        if r1 != r2:
            # A + B = a0, A*r1 + B*r2 = a1
            # B = (a1 - a0*r1)/(r2 - r1), A = a0 - B
            b_num = a1 - a0 * r1
            b_den = r2 - r1
        else:
            b_num, b_den = 0, 1

        # Compute first few terms
        terms = [a0, a1]
        for i in range(2, 7):
            terms.append(c1 * terms[-1] + c2 * terms[-2])

        problem = f"a_n={c1}*a_{{n-1}}+({c2})*a_{{n-2}}, a_0={a0}, a_1={a1}"
        return problem, {
            "c1": c1, "c2": c2, "r1": r1, "r2": r2,
            "a0": a0, "a1": a1, "disc": disc,
            "terms": terms,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing characteristic equation solution.
        """
        c1, c2 = data["c1"], data["c2"]
        r1, r2 = data["r1"], data["r2"]
        steps = [
            f"char eq: r^2-{c1}r-({c2})=0",
            f"disc={c1}^2+4*{c2}={data['disc']}",
            f"roots: r1={r1}, r2={r2}",
        ]
        if r1 != r2:
            steps.append(f"general: a_n = A*{r1}^n + B*{r2}^n")
        else:
            steps.append(f"repeated: a_n = (A+Bn)*{r1}^n")
        terms_str = ", ".join(str(t) for t in data["terms"])
        steps.append(f"first terms: {terms_str}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the roots.

        Args:
            data: Solution data dict.

        Returns:
            Roots as string.
        """
        return f"r1={data['r1']}, r2={data['r2']}"


# ---------------------------------------------------------------------------
# 7. Catalan Application (tier 5)
# ---------------------------------------------------------------------------

@register
class CatalanApplicationGenerator(StepGenerator):
    """Count structures equal to the n-th Catalan number.

    Covers balanced parentheses, full binary trees, triangulations
    of (n+2)-gon, and monotone paths. All equal C_n = C(2n,n)/(n+1).

    Difficulty scaling:
        d1-2: n in [2, 3].
        d3-4: n in [3, 5].
        d5-6: n in [4, 6].
        d7-8: n in [5, 8].

    Prerequisites:
        catalan.
    """

    _RANGES = {
        1: (2, 3), 2: (2, 3), 3: (3, 5), 4: (3, 5),
        5: (4, 6), 6: (4, 6), 7: (5, 8), 8: (5, 8),
    }

    _APPLICATIONS = [
        ("balanced parentheses with {n} pairs", "parentheses"),
        ("full binary trees with {n} internal nodes", "binary_trees"),
        ("triangulations of a {np2}-gon", "triangulations"),
        ("monotone paths on {n}x{n} grid above diagonal", "paths"),
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "catalan_application"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["catalan"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "count Catalan structures"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Catalan application problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        lo, hi = self._RANGES.get(difficulty, self._RANGES[1])
        n = self._rng.randint(lo, hi)
        template, app_type = self._rng.choice(self._APPLICATIONS)
        c_n = _catalan(n)
        c2n_n = math.comb(2 * n, n)
        description = template.format(n=n, np2=n + 2)
        problem = f"count: {description}"
        return problem, {
            "n": n, "app_type": app_type,
            "description": description,
            "c_n": c_n, "c2n_n": c2n_n,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing Catalan number computation.
        """
        n = data["n"]
        return [
            f"{data['description']}",
            f"count = C_{n} = C(2*{n},{n})/({n}+1)",
            f"C({2 * n},{n})={data['c2n_n']}",
            f"C_{n}={data['c2n_n']}/{n + 1}={data['c_n']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the Catalan number.

        Args:
            data: Solution data dict.

        Returns:
            C_n as string.
        """
        return str(data["c_n"])


# ---------------------------------------------------------------------------
# 8. Double Counting (tier 4)
# ---------------------------------------------------------------------------

@register
class DoubleCountingGenerator(StepGenerator):
    """Prove identity by counting the same set two ways.

    Uses the handshake lemma: sum of degrees = 2|E| in a graph.
    Generates small graphs and verifies both sides.

    Difficulty scaling:
        d1-2: 3-4 vertices, sparse.
        d3-4: 4-5 vertices.
        d5-6: 5-6 vertices.
        d7-8: 6-7 vertices.

    Prerequisites:
        addition.
    """

    _RANGES = {
        1: (3, 4), 2: (3, 4), 3: (4, 5), 4: (4, 5),
        5: (5, 6), 6: (5, 6), 7: (6, 7), 8: (6, 7),
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "double_counting"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["addition"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "verify handshake lemma via double counting"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a double counting (handshake lemma) problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        lo, hi = self._RANGES.get(difficulty, self._RANGES[1])
        v = self._rng.randint(lo, hi)
        # Generate random edges
        max_edges = v * (v - 1) // 2
        num_edges = self._rng.randint(v - 1, min(max_edges, v + difficulty))
        all_possible = [(i, j) for i in range(v) for j in range(i + 1, v)]
        self._rng.shuffle(all_possible)
        edges = all_possible[:num_edges]
        # Compute degrees
        degrees = [0] * v
        for i, j in edges:
            degrees[i] += 1
            degrees[j] += 1
        deg_sum = sum(degrees)
        two_e = 2 * len(edges)

        problem = f"G: V={v}, E={len(edges)}, handshake lemma"
        return problem, {
            "v": v, "num_edges": len(edges),
            "degrees": degrees, "deg_sum": deg_sum,
            "two_e": two_e, "verified": deg_sum == two_e,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing double counting.
        """
        deg_str = ", ".join(str(d) for d in data["degrees"])
        return [
            f"|V|={data['v']}, |E|={data['num_edges']}",
            f"degrees: [{deg_str}]",
            f"sum(deg)={data['deg_sum']}",
            f"2*|E|={data['two_e']}",
            f"handshake lemma: {'verified' if data['verified'] else 'failed'}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return verification result.

        Args:
            data: Solution data dict.

        Returns:
            Sum of degrees and 2|E|.
        """
        return f"sum_deg={data['deg_sum']}, 2|E|={data['two_e']}"


# ---------------------------------------------------------------------------
# 9. Pigeonhole Application (tier 4)
# ---------------------------------------------------------------------------

@register
class PigeonholeApplicationGenerator(StepGenerator):
    """Apply the pigeonhole principle to structured problems.

    Template-based: birthday-style problems, divisibility arguments,
    and subset sum existence. Generates problem and solution.

    Difficulty scaling:
        d1-2: n+1 items in n boxes, small n.
        d3-4: modular arithmetic pigeonhole.
        d5-6: birthday problem variant.
        d7-8: subset sum pigeonhole.

    Prerequisites:
        division.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "pigeonhole_application"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["division"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "apply pigeonhole principle"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a pigeonhole problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 2:
            # Basic: n+1 items in n boxes
            n = self._rng.randint(3, 8)
            items = n + 1
            problem = f"{items} items in {n} boxes"
            min_in_box = 2
            explanation = f"{items} items, {n} boxes -> some box has >= {min_in_box}"
            answer_val = min_in_box
        elif difficulty <= 4:
            # Mod pigeonhole: among n+1 integers, two have same remainder mod n
            n = self._rng.randint(3, 7)
            items = n + 1
            problem = f"among {items} integers, two with same remainder mod {n}"
            min_in_box = 2
            explanation = (f"{items} integers, {n} possible remainders "
                           f"-> two share remainder")
            answer_val = min_in_box
        elif difficulty <= 6:
            # Birthday: n people, k=365 days -> need 366 for guaranteed match
            n = self._rng.randint(20, 50)
            k = 12  # months for small version
            items = k + 1
            problem = f"{items} people, {k} birth months"
            min_in_box = 2
            explanation = (f"{items} people, {k} months -> "
                           f"guaranteed shared month")
            answer_val = min_in_box
        else:
            # Generalized: kn+1 items in n boxes -> some box has >= k+1
            n = self._rng.randint(3, 6)
            k = self._rng.randint(2, 4)
            items = k * n + 1
            problem = f"{items} items in {n} boxes"
            min_in_box = k + 1
            explanation = (f"{items}={k}*{n}+1 items, {n} boxes "
                           f"-> some box has >= {min_in_box}")
            answer_val = min_in_box

        return problem, {
            "items": items, "boxes": n if difficulty <= 6 else n,
            "min_in_box": answer_val,
            "explanation": explanation,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing pigeonhole reasoning.
        """
        return [
            f"items={data['items']}, boxes={data['boxes']}",
            f"ceil({data['items']}/{data['boxes']})={math.ceil(data['items'] / data['boxes'])}",
            data["explanation"],
            f"min in some box >= {data['min_in_box']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the minimum occupancy guarantee.

        Args:
            data: Solution data dict.

        Returns:
            Minimum as string.
        """
        return str(data["min_in_box"])


# ---------------------------------------------------------------------------
# 10. Compositions (tier 4)
# ---------------------------------------------------------------------------

@register
class CompositionsGenerator(StepGenerator):
    """Count compositions of n (ordered partitions).

    Compositions of n into k parts = C(n-1, k-1).
    Total compositions of n = 2^{n-1}.

    Difficulty scaling:
        d1-2: n in [3, 5], count total.
        d3-4: n in [4, 7], count into k parts.
        d5-6: n in [5, 9], both.
        d7-8: n in [6, 12], both.

    Prerequisites:
        binomial.
    """

    _RANGES = {
        1: (3, 5), 2: (3, 5), 3: (4, 7), 4: (4, 7),
        5: (5, 9), 6: (5, 9), 7: (6, 12), 8: (6, 12),
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "compositions"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["binomial"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "count compositions of n"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a compositions counting problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        lo, hi = self._RANGES.get(difficulty, self._RANGES[1])
        n = self._rng.randint(lo, hi)
        total = 2 ** (n - 1)
        k = self._rng.randint(2, min(n, 4))
        into_k = _comb(n - 1, k - 1)
        problem = f"compositions of {n}"
        return problem, {
            "n": n, "k": k, "total": total,
            "into_k": into_k,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing composition counting.
        """
        n, k = data["n"], data["k"]
        return [
            f"total compositions of {n} = 2^{{{n - 1}}}={data['total']}",
            f"compositions into {k} parts = C({n - 1},{k - 1})"
            f"={data['into_k']}",
            f"verify: sum_{{k=1}}^{{{n}}} C({n - 1},k-1)=2^{{{n - 1}}}={data['total']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the composition counts.

        Args:
            data: Solution data dict.

        Returns:
            Total and k-part counts.
        """
        return f"total={data['total']}, into_{data['k']}={data['into_k']}"
