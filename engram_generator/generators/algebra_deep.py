"""Deep algebra generators -- ring theory, field theory, advanced groups.

10 generators across tiers 5-7 covering Sylow theorems, direct products,
quotient rings, polynomial irreducibility, splitting fields, group
presentations, Smith normal form, exterior algebra, tensor products of
modules, and Galois groups.
"""
from __future__ import annotations

import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


# ===================================================================
# HELPER UTILITIES
# ===================================================================

def _gcd(a: int, b: int) -> int:
    """Compute greatest common divisor.

    Args:
        a: First integer.
        b: Second integer.

    Returns:
        GCD of a and b.
    """
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a


def _is_prime(n: int) -> bool:
    """Test if n is prime.

    Args:
        n: Positive integer.

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


def _factorise(n: int) -> dict[int, int]:
    """Return prime factorisation as {prime: exponent}.

    Args:
        n: Positive integer >= 2.

    Returns:
        Dictionary mapping primes to their exponents.
    """
    factors: dict[int, int] = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors[d] = factors.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        factors[n] = factors.get(n, 0) + 1
    return factors


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


def _format_poly(coeffs: list[int], var: str = "x",
                 mod: int | None = None) -> str:
    """Format polynomial from coefficients (highest degree first).

    Args:
        coeffs: Coefficients from highest to lowest degree.
        var: Variable name.
        mod: If set, show coefficients modulo this value.

    Returns:
        Polynomial string.
    """
    deg = len(coeffs) - 1
    parts: list[str] = []
    for i, c in enumerate(coeffs):
        if mod is not None:
            c = c % mod
        power = deg - i
        if c == 0:
            continue
        if power == 0:
            parts.append(str(c))
        elif power == 1:
            parts.append(f"{c}{var}" if c != 1 else var)
        else:
            parts.append(f"{c}{var}^{power}" if c != 1 else f"{var}^{power}")
    return " + ".join(parts) if parts else "0"


# ===================================================================
# 1. SYLOW THEOREM (tier 6)
# ===================================================================

@register
class SylowTheoremGenerator(StepGenerator):
    """Compute the number of Sylow p-subgroups of a finite group.

    For |G| = p^a * m with gcd(p, m) = 1, the number n_p of Sylow
    p-subgroups satisfies: n_p divides m and n_p = 1 (mod p).

    Difficulty scaling:
        Difficulty 1-3: |G| = 12, 18, 20.
        Difficulty 4-6: |G| = 24, 36, 45.
        Difficulty 7-8: |G| = 48, 60, 72.

    Prerequisites:
        factorisation (tier 6).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "sylow_theorem"

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
            Short task description string.
        """
        return "find the number of Sylow p-subgroups"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Sylow theorem problem.

        Args:
            difficulty: Controls group order range.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        pool_low = [12, 18, 20]
        pool_mid = [24, 36, 45]
        pool_high = [48, 60, 72]
        if difficulty <= 3:
            pool = pool_low
        elif difficulty <= 6:
            pool = pool_mid
        else:
            pool = pool_high
        order = self._rng.choice(pool)
        factors = _factorise(order)
        p = self._rng.choice(list(factors.keys()))
        a = factors[p]
        m = order // (p ** a)

        divs_m = _divisors(m)
        candidates = [d for d in divs_m if d % p == 1]

        problem = f"|G| = {order}; find n_{p} (Sylow {p}-subgroups)"
        return problem, {
            "order": order, "p": p, "a": a, "m": m,
            "divs_m": divs_m, "candidates": candidates,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        steps = [
            f"|G| = {sd['order']} = {sd['p']}^{sd['a']} * {sd['m']}",
            f"n_{sd['p']} divides m = {sd['m']}: divisors = {sd['divs_m']}",
            f"n_{sd['p']} = 1 (mod {sd['p']})",
            f"candidates: {sd['candidates']}",
        ]
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return possible values of n_p.

        Args:
            sd: Solution data.

        Returns:
            Comma-separated candidate values.
        """
        vals = ", ".join(str(c) for c in sd["candidates"])
        return f"n_{sd['p']} in {{{vals}}}"


# ===================================================================
# 2. DIRECT PRODUCT GROUP (tier 5)
# ===================================================================

@register
class DirectProductGroupGenerator(StepGenerator):
    """Compute element orders in a direct product G x H.

    For groups Z/mZ x Z/nZ, order of (a, b) = lcm(ord(a), ord(b)).
    |G x H| = |G| * |H|.

    Difficulty scaling:
        Difficulty 1-3: m, n in [2, 4].
        Difficulty 4-6: m, n in [3, 6].
        Difficulty 7-8: m, n in [4, 8].

    Prerequisites:
        group_table (tier 4).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "direct_product_group"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["group_table"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "compute element order in a direct product group"

    def _element_order(self, a: int, n: int) -> int:
        """Compute the order of element a in Z/nZ.

        Args:
            a: Element value.
            n: Group modulus.

        Returns:
            Smallest positive k such that k*a = 0 mod n.
        """
        if a % n == 0:
            return 1
        return n // _gcd(a, n)

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a direct product order problem.

        Args:
            difficulty: Controls group sizes.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            m = self._rng.randint(2, 4)
            n = self._rng.randint(2, 4)
        elif difficulty <= 6:
            m = self._rng.randint(3, 6)
            n = self._rng.randint(3, 6)
        else:
            m = self._rng.randint(4, 8)
            n = self._rng.randint(4, 8)

        a = self._rng.randint(0, m - 1)
        b = self._rng.randint(0, n - 1)
        ord_a = self._element_order(a, m)
        ord_b = self._element_order(b, n)
        g = _gcd(ord_a, ord_b)
        lcm_ab = (ord_a * ord_b) // g if g else 1
        prod_order = m * n

        problem = (f"Z/{m}Z x Z/{n}Z; "
                   f"find order of ({a}, {b}) and |G x H|")
        return problem, {
            "m": m, "n": n, "a": a, "b": b,
            "ord_a": ord_a, "ord_b": ord_b,
            "lcm": lcm_ab, "prod_order": prod_order,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return [
            f"ord({sd['a']}) in Z/{sd['m']}Z = {sd['ord_a']}",
            f"ord({sd['b']}) in Z/{sd['n']}Z = {sd['ord_b']}",
            f"ord(({sd['a']},{sd['b']})) = lcm({sd['ord_a']},{sd['ord_b']}) = {sd['lcm']}",
            f"|Z/{sd['m']}Z x Z/{sd['n']}Z| = {sd['m']}*{sd['n']} = {sd['prod_order']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return element order and group order.

        Args:
            sd: Solution data.

        Returns:
            Answer string.
        """
        return f"ord(({sd['a']},{sd['b']})) = {sd['lcm']}; |GxH| = {sd['prod_order']}"


# ===================================================================
# 3. QUOTIENT RING (tier 6)
# ===================================================================

@register
class QuotientRingGenerator(StepGenerator):
    """Compute multiplication in quotient rings Z/nZ.

    Elements are cosets a + nZ. Multiplication: (a+nZ)(b+nZ) = ab + nZ.
    Compute products and verify ring axioms on small examples.

    Difficulty scaling:
        Difficulty 1-3: n in [3, 5].
        Difficulty 4-6: n in [4, 7].
        Difficulty 7-8: n in [6, 10].

    Prerequisites:
        ring_arithmetic (tier 5).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "quotient_ring"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["ring_arithmetic"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "compute products in a quotient ring Z/nZ"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a quotient ring multiplication problem.

        Args:
            difficulty: Controls ring size.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            n = self._rng.randint(3, 5)
        elif difficulty <= 6:
            n = self._rng.randint(4, 7)
        else:
            n = self._rng.randint(6, 10)

        a = self._rng.randint(1, n - 1)
        b = self._rng.randint(1, n - 1)
        c = self._rng.randint(1, n - 1)

        ab = (a * b) % n
        bc = (b * c) % n
        abc_left = (ab * c) % n
        abc_right = (a * bc) % n

        problem = (f"in Z/{n}Z: compute ({a}+{n}Z)({b}+{n}Z), "
                   f"then ({a}+{n}Z)({b}+{n}Z)({c}+{n}Z)")
        return problem, {
            "n": n, "a": a, "b": b, "c": c,
            "ab": ab, "bc": bc,
            "abc_left": abc_left, "abc_right": abc_right,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return [
            f"({sd['a']}+{sd['n']}Z)({sd['b']}+{sd['n']}Z) = "
            f"{sd['a']}*{sd['b']}+{sd['n']}Z = "
            f"{sd['a']*sd['b']}+{sd['n']}Z = {sd['ab']}+{sd['n']}Z",
            f"({sd['ab']}+{sd['n']}Z)({sd['c']}+{sd['n']}Z) = "
            f"{sd['ab']}*{sd['c']}+{sd['n']}Z = "
            f"{sd['ab']*sd['c']}+{sd['n']}Z = {sd['abc_left']}+{sd['n']}Z",
            f"associativity check: {sd['abc_left']} == {sd['abc_right']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return computed coset products.

        Args:
            sd: Solution data.

        Returns:
            Answer string.
        """
        return (f"({sd['a']})({sd['b']}) = {sd['ab']} mod {sd['n']}; "
                f"({sd['a']})({sd['b']})({sd['c']}) = {sd['abc_left']} mod {sd['n']}")


# ===================================================================
# 4. POLYNOMIAL IRREDUCIBILITY (tier 6)
# ===================================================================

@register
class PolynomialIrreducibilityGenerator(StepGenerator):
    """Test if a polynomial is irreducible over Z/pZ.

    For degree 2-3: f(x) is irreducible iff it has no roots in Z/pZ.
    For higher degrees: uses Eisenstein criterion when applicable.

    Difficulty scaling:
        Difficulty 1-3: degree 2 over Z/2Z or Z/3Z.
        Difficulty 4-6: degree 2-3 over Z/3Z or Z/5Z.
        Difficulty 7-8: degree 3 over Z/5Z or Z/7Z.

    Prerequisites:
        polynomial_division (tier 5).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "polynomial_irreducibility"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["polynomial_division"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "test polynomial irreducibility over Z/pZ"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an irreducibility test problem.

        Args:
            difficulty: Controls degree and field size.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            p = self._rng.choice([2, 3])
            deg = 2
        elif difficulty <= 6:
            p = self._rng.choice([3, 5])
            deg = self._rng.choice([2, 3])
        else:
            p = self._rng.choice([5, 7])
            deg = 3

        # Generate random polynomial with leading coeff 1
        coeffs = [1] + [self._rng.randint(0, p - 1) for _ in range(deg)]

        # Evaluate at all elements of Z/pZ to find roots
        roots = []
        evaluations: list[tuple[int, int]] = []
        for x in range(p):
            val = 0
            for c in coeffs:
                val = (val * x + c) % p
            evaluations.append((x, val))
            if val == 0:
                roots.append(x)

        irreducible = len(roots) == 0
        poly_str = _format_poly(coeffs, mod=p)
        problem = f"is {poly_str} irreducible over Z/{p}Z?"
        return problem, {
            "coeffs": coeffs, "p": p, "deg": deg,
            "poly_str": poly_str, "evaluations": evaluations,
            "roots": roots, "irreducible": irreducible,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        steps = [f"f(x) = {sd['poly_str']} over Z/{sd['p']}Z (degree {sd['deg']})"]
        for x, val in sd["evaluations"]:
            steps.append(f"f({x}) = {val} mod {sd['p']}")
        if sd["roots"]:
            steps.append(f"roots found: {sd['roots']} -> reducible")
        else:
            steps.append("no roots -> irreducible (degree <= 3)")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return irreducibility result.

        Args:
            sd: Solution data.

        Returns:
            Answer string.
        """
        label = "irreducible" if sd["irreducible"] else "reducible"
        root_str = str(sd["roots"]) if sd["roots"] else "none"
        return f"{sd['poly_str']} is {label} over Z/{sd['p']}Z; roots: {root_str}"


# ===================================================================
# 5. SPLITTING FIELD (tier 6)
# ===================================================================

@register
class SplittingFieldGenerator(StepGenerator):
    """Find the splitting field of x^2 - d over Q.

    Adjoins sqrt(d) to Q. The degree [Q(sqrt(d)):Q] = 2 when d is
    not a perfect square.

    Difficulty scaling:
        Difficulty 1-3: d in [2, 3, 5].
        Difficulty 4-6: d in [2, 3, 5, 6, 7].
        Difficulty 7-8: d in [2, 3, 5, 6, 7, 10, 11, 13].

    Prerequisites:
        polynomial_division (tier 5).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "splitting_field"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["polynomial_division"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "find the splitting field of a quadratic polynomial"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a splitting field problem.

        Args:
            difficulty: Controls radicand range.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            pool = [2, 3, 5]
        elif difficulty <= 6:
            pool = [2, 3, 5, 6, 7]
        else:
            pool = [2, 3, 5, 6, 7, 10, 11, 13]

        d = self._rng.choice(pool)
        a = self._rng.choice([1, -1])
        # f(x) = x^2 - a*d (always non-perfect-square d)
        constant = a * d
        poly_str = f"x^2 - {constant}" if constant > 0 else f"x^2 + {-constant}"
        degree = 2
        roots = [f"sqrt({constant})", f"-sqrt({constant})"]
        field = f"Q(sqrt({constant}))"

        problem = f"find splitting field of {poly_str} over Q"
        return problem, {
            "d": d, "constant": constant,
            "poly_str": poly_str, "roots": roots,
            "field": field, "degree": degree,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return [
            f"f(x) = {sd['poly_str']}",
            f"roots: {sd['roots'][0]}, {sd['roots'][1]}",
            f"adjoin {sd['roots'][0]} to Q",
            f"splitting field = {sd['field']}",
            f"[{sd['field']}:Q] = {sd['degree']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the splitting field and extension degree.

        Args:
            sd: Solution data.

        Returns:
            Answer string.
        """
        return f"splitting field = {sd['field']}; [{sd['field']}:Q] = {sd['degree']}"


# ===================================================================
# 6. GROUP PRESENTATION (tier 5)
# ===================================================================

@register
class GroupPresentationGenerator(StepGenerator):
    """Compute group order from a finite presentation.

    Handles dihedral groups D_n = <a,b | a^n=1, b^2=1, bab=a^{-1}>
    with |D_n| = 2n, and cyclic groups Z/nZ = <a | a^n=1> with |Z/nZ| = n.

    Difficulty scaling:
        Difficulty 1-3: cyclic groups, n in [3, 6].
        Difficulty 4-6: dihedral groups, n in [3, 5].
        Difficulty 7-8: dihedral groups, n in [5, 8].

    Prerequisites:
        group_order (tier 6).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "group_presentation"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["group_order"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "compute group order from a presentation"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a group presentation problem.

        Args:
            difficulty: Controls group type and size.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            group_type = "cyclic"
            n = self._rng.randint(3, 6)
            pres = f"<a | a^{n}=1>"
            order = n
            explanation = f"cyclic group of order {n}"
        else:
            group_type = "dihedral"
            if difficulty <= 6:
                n = self._rng.randint(3, 5)
            else:
                n = self._rng.randint(5, 8)
            pres = f"<a,b | a^{n}=1, b^2=1, bab=a^{{-1}}>"
            order = 2 * n
            explanation = f"dihedral group D_{n}"

        problem = f"G = {pres}; find |G|"
        return problem, {
            "group_type": group_type, "n": n,
            "pres": pres, "order": order,
            "explanation": explanation,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        if sd["group_type"] == "cyclic":
            return [
                f"presentation: {sd['pres']}",
                f"one generator a with a^{sd['n']}=1",
                f"|G| = {sd['n']}",
            ]
        return [
            f"presentation: {sd['pres']}",
            f"identify as D_{sd['n']}",
            f"rotations: {sd['n']}, reflections: {sd['n']}",
            f"|D_{sd['n']}| = 2*{sd['n']} = {sd['order']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the group order.

        Args:
            sd: Solution data.

        Returns:
            Answer string.
        """
        return f"|G| = {sd['order']} ({sd['explanation']})"


# ===================================================================
# 7. SMITH NORMAL FORM (tier 6)
# ===================================================================

@register
class SmithNormalFormGenerator(StepGenerator):
    """Reduce an integer matrix to Smith normal form.

    Uses elementary row and column operations to diagonalise a 2x2
    integer matrix. Diagonal entries satisfy d1 | d2.

    Difficulty scaling:
        Difficulty 1-3: entries in [-3, 3].
        Difficulty 4-6: entries in [-5, 5].
        Difficulty 7-8: entries in [-8, 8].

    Prerequisites:
        gcd (tier 2).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "smith_normal_form"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["gcd"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "compute the Smith normal form of an integer matrix"

    def _smith_2x2(self, a: int, b: int, c: int, d: int) -> tuple[int, int, list[str]]:
        """Compute Smith normal form of [[a,b],[c,d]].

        Args:
            a: Entry (0,0).
            b: Entry (0,1).
            c: Entry (1,0).
            d: Entry (1,1).

        Returns:
            Tuple of (d1, d2, steps) where diag = [d1, d2].
        """
        steps: list[str] = [f"input: [[{a},{b}],[{c},{d}]]"]
        det = abs(a * d - b * c)
        if det == 0:
            # Rank <= 1
            g = _gcd(_gcd(abs(a), abs(b)), _gcd(abs(c), abs(d)))
            if g == 0:
                steps.append("zero matrix -> SNF = [[0,0],[0,0]]")
                return 0, 0, steps
            steps.append(f"gcd of all entries = {g}")
            steps.append(f"SNF = [[{g},0],[0,0]]")
            return g, 0, steps
        g = _gcd(_gcd(abs(a), abs(b)), _gcd(abs(c), abs(d)))
        d2 = det // g if g else 0
        steps.append(f"gcd of all entries = {g}")
        steps.append(f"|det| = {det}")
        steps.append(f"d1 = {g}, d2 = {det}//{g} = {d2}")
        steps.append(f"SNF = [[{g},0],[0,{d2}]]")
        return g, d2, steps

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Smith normal form problem.

        Args:
            difficulty: Controls entry magnitude.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            mag = 3
        elif difficulty <= 6:
            mag = 5
        else:
            mag = 8

        # Ensure non-zero matrix
        while True:
            a = self._rng.randint(-mag, mag)
            b = self._rng.randint(-mag, mag)
            c = self._rng.randint(-mag, mag)
            d = self._rng.randint(-mag, mag)
            if any(x != 0 for x in [a, b, c, d]):
                break

        d1, d2, steps = self._smith_2x2(a, b, c, d)
        problem = f"Smith normal form of [[{a},{b}],[{c},{d}]]"
        return problem, {
            "matrix": [[a, b], [c, d]],
            "d1": d1, "d2": d2, "steps": steps,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return sd["steps"]

    def _create_answer(self, sd: dict) -> str:
        """Return the Smith normal form diagonal.

        Args:
            sd: Solution data.

        Returns:
            Answer string.
        """
        return f"SNF = diag({sd['d1']}, {sd['d2']})"


# ===================================================================
# 8. EXTERIOR ALGEBRA (tier 6)
# ===================================================================

@register
class ExteriorAlgebraGenerator(StepGenerator):
    """Compute wedge products in exterior algebra.

    Rules: e_i ^ e_j = -e_j ^ e_i, e_i ^ e_i = 0.
    Computes wedge products of linear combinations of basis vectors.

    Difficulty scaling:
        Difficulty 1-3: 2 basis vectors, 2-term combinations.
        Difficulty 4-6: 3 basis vectors, 2-term combinations.
        Difficulty 7-8: 3 basis vectors, 3-term combinations.

    Prerequisites:
        set_operations (tier 3).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "exterior_algebra"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["set_operations"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "compute a wedge product of vectors"

    def _format_vector(self, coeffs: list[int], dim: int) -> str:
        """Format a vector as a linear combination of basis vectors.

        Args:
            coeffs: Coefficients for e1, e2, etc.
            dim: Dimension (number of basis vectors).

        Returns:
            Formatted string like ``2e1 + 3e2``.
        """
        parts: list[str] = []
        for i in range(dim):
            c = coeffs[i]
            if c == 0:
                continue
            if c == 1:
                parts.append(f"e{i+1}")
            elif c == -1:
                parts.append(f"-e{i+1}")
            else:
                parts.append(f"{c}e{i+1}")
        return " + ".join(parts).replace("+ -", "- ") if parts else "0"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a wedge product problem.

        Args:
            difficulty: Controls dimension and vector size.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            dim = 2
        else:
            dim = 3

        mag = min(2 + difficulty, 5)
        u = [self._rng.randint(-mag, mag) for _ in range(dim)]
        v = [self._rng.randint(-mag, mag) for _ in range(dim)]

        # Ensure non-zero
        if all(c == 0 for c in u):
            u[0] = 1
        if all(c == 0 for c in v):
            v[0] = 1

        # Compute u ^ v: coefficient of e_i ^ e_j = u_i*v_j - u_j*v_i
        wedge_terms: list[tuple[str, int]] = []
        steps: list[str] = [
            f"u = {self._format_vector(u, dim)}",
            f"v = {self._format_vector(v, dim)}",
        ]

        for i in range(dim):
            for j in range(i + 1, dim):
                coeff = u[i] * v[j] - u[j] * v[i]
                basis = f"e{i+1}^e{j+1}"
                wedge_terms.append((basis, coeff))
                steps.append(
                    f"{basis}: {u[i]}*{v[j]} - {u[j]}*{v[i]} = {coeff}"
                )

        result_parts = []
        for basis, coeff in wedge_terms:
            if coeff != 0:
                if coeff == 1:
                    result_parts.append(basis)
                elif coeff == -1:
                    result_parts.append(f"-{basis}")
                else:
                    result_parts.append(f"{coeff}{basis}")
        result = " + ".join(result_parts).replace("+ -", "- ") if result_parts else "0"

        problem = (f"compute ({self._format_vector(u, dim)}) ^ "
                   f"({self._format_vector(v, dim)})")
        return problem, {
            "u": u, "v": v, "dim": dim,
            "wedge_terms": wedge_terms, "result": result,
            "steps": steps,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return sd["steps"]

    def _create_answer(self, sd: dict) -> str:
        """Return the wedge product result.

        Args:
            sd: Solution data.

        Returns:
            Answer string.
        """
        return f"u ^ v = {sd['result']}"


# ===================================================================
# 9. TENSOR PRODUCT MODULES (tier 6)
# ===================================================================

@register
class TensorProductModulesGenerator(StepGenerator):
    """Compute tensor products of cyclic Z-modules.

    Z/mZ tensor_Z Z/nZ = Z/gcd(m,n)Z.

    Difficulty scaling:
        Difficulty 1-3: m, n in [2, 6].
        Difficulty 4-6: m, n in [3, 12].
        Difficulty 7-8: m, n in [4, 20].

    Prerequisites:
        gcd (tier 2).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "tensor_product_modules"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["gcd"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "compute the tensor product of cyclic modules"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a tensor product of modules problem.

        Args:
            difficulty: Controls moduli range.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            m = self._rng.randint(2, 6)
            n = self._rng.randint(2, 6)
        elif difficulty <= 6:
            m = self._rng.randint(3, 12)
            n = self._rng.randint(3, 12)
        else:
            m = self._rng.randint(4, 20)
            n = self._rng.randint(4, 20)

        g = _gcd(m, n)

        problem = f"Z/{m}Z tensor_Z Z/{n}Z = ?"
        return problem, {"m": m, "n": n, "gcd": g}

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return [
            f"Z/{sd['m']}Z tensor_Z Z/{sd['n']}Z",
            f"gcd({sd['m']}, {sd['n']}) = {sd['gcd']}",
            f"result = Z/{sd['gcd']}Z",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the tensor product result.

        Args:
            sd: Solution data.

        Returns:
            Answer string.
        """
        if sd["gcd"] == 1:
            return f"Z/{sd['m']}Z tensor Z/{sd['n']}Z = 0"
        return f"Z/{sd['m']}Z tensor Z/{sd['n']}Z = Z/{sd['gcd']}Z"


# ===================================================================
# 10. GALOIS GROUP (tier 7)
# ===================================================================

@register
class GaloisGroupGenerator(StepGenerator):
    """Determine the Galois group of a small field extension.

    Template-based for well-known extensions:
    - x^2 - d: Gal(Q(sqrt(d))/Q) = Z/2Z.
    - x^3 - 2: Gal(Q(2^{1/3}, omega)/Q) = S_3.
    - x^4 - 1 (cyclotomic): Gal(Q(i)/Q) = Z/2Z.

    Difficulty scaling:
        Difficulty 1-3: quadratic extensions (Z/2Z).
        Difficulty 4-6: mix of quadratic and cubic.
        Difficulty 7-8: cubic extensions (S_3).

    Prerequisites:
        polynomial_division (tier 5).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "galois_group"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["polynomial_division"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "determine the Galois group of a field extension"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Galois group problem.

        Args:
            difficulty: Controls extension complexity.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        templates = []
        if difficulty <= 3:
            # Quadratic only
            d = self._rng.choice([2, 3, 5, 7])
            templates = [("quadratic", d)]
        elif difficulty <= 6:
            d = self._rng.choice([2, 3, 5, 7, 11])
            templates = [("quadratic", d), ("cubic", 2)]
        else:
            templates = [("cubic", 2), ("cubic", 3)]

        ttype, param = self._rng.choice(templates)

        if ttype == "quadratic":
            poly = f"x^2 - {param}"
            field = f"Q(sqrt({param}))"
            galois = "Z/2Z"
            degree = 2
            order = 2
            auts = [
                "identity: sqrt({0}) -> sqrt({0})".format(param),
                "conjugation: sqrt({0}) -> -sqrt({0})".format(param),
            ]
        else:
            poly = f"x^3 - {param}"
            field = f"Q({param}^{{1/3}}, omega)"
            galois = "S_3"
            degree = 6
            order = 6
            auts = [
                f"identity",
                f"{param}^{{1/3}} -> omega*{param}^{{1/3}}",
                f"{param}^{{1/3}} -> omega^2*{param}^{{1/3}}",
                f"+ conjugation of omega (3 more)",
            ]

        problem = f"find Gal(splitting field of {poly} over Q)"
        return problem, {
            "poly": poly, "field": field,
            "galois": galois, "degree": degree,
            "order": order, "auts": auts,
            "ttype": ttype,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        steps = [
            f"f(x) = {sd['poly']}",
            f"splitting field = {sd['field']}",
            f"[{sd['field']}:Q] = {sd['degree']}",
        ]
        for a in sd["auts"]:
            steps.append(f"automorphism: {a}")
        steps.append(f"Gal = {sd['galois']} (order {sd['order']})")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the Galois group.

        Args:
            sd: Solution data.

        Returns:
            Answer string.
        """
        return f"Gal({sd['field']}/Q) = {sd['galois']}, |Gal| = {sd['order']}"
