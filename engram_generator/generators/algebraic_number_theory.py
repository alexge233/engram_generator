"""Algebraic number theory generators.

6 generators at tiers 6-7 covering norm and trace in quadratic fields,
ring of integers, ideal factorisation, class numbers, p-adic
valuations, and Hensel lifting. All produce step-by-step solutions
with LaTeX formatting.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

def _fmt(value: float, decimals: int = 4) -> str:
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


def _legendre_symbol(a: int, p: int) -> int:
    """Compute Legendre symbol (a/p) via Euler's criterion.

    Args:
        a: Integer.
        p: Odd prime.

    Returns:
        1 if a is a quadratic residue mod p, -1 if not, 0 if p | a.
    """
    a = a % p
    if a == 0:
        return 0
    result = pow(a, (p - 1) // 2, p)
    return 1 if result == 1 else -1


def _mod_inverse(a: int, m: int) -> int:
    """Compute modular inverse of a modulo m using extended Euclidean.

    Args:
        a: Integer with gcd(a, m) = 1.
        m: Modulus.

    Returns:
        Integer x such that a*x = 1 (mod m).

    Raises:
        ValueError: If inverse does not exist.
    """
    g, x, _ = _extended_gcd(a, m)
    if g != 1:
        raise ValueError(f"No inverse: gcd({a}, {m}) = {g}")
    return x % m


def _extended_gcd(a: int, b: int) -> tuple[int, int, int]:
    """Extended Euclidean algorithm.

    Args:
        a: First integer.
        b: Second integer.

    Returns:
        Tuple (gcd, x, y) such that a*x + b*y = gcd.
    """
    if a == 0:
        return b, 0, 1
    g, x1, y1 = _extended_gcd(b % a, a)
    return g, y1 - (b // a) * x1, x1


# ---------------------------------------------------------------------------
# Small primes for sampling
# ---------------------------------------------------------------------------

_SMALL_PRIMES = [
    2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47,
]


# ===================================================================
# 1. Norm and Trace in Quadratic Field  (tier 6)
# ===================================================================

@register
class NormTraceFieldGenerator(StepGenerator):
    """Compute norm and trace of elements in Q(sqrt(d)).

    For alpha = a + b*sqrt(d) in Q(sqrt(d)), the field norm is
    N(alpha) = a^2 - d*b^2 and the trace is T(alpha) = 2a.
    These are fundamental invariants of the quadratic extension.

    Difficulty scaling:
        Difficulty 1-3: small integer a, b, positive d.
        Difficulty 4-6: larger coefficients, negative d.
        Difficulty 7-8: verify multiplicativity N(alpha*beta).

    Prerequisites:
        quadratic.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "norm_trace_field"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["quadratic"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute norm and trace in quadratic field"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a norm/trace computation problem.

        Args:
            difficulty: Controls coefficient size and sign of d.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            a = self._rng.randint(1, 5)
            b = self._rng.randint(1, 4)
            d = self._rng.choice([2, 3, 5, 7])
        elif difficulty <= 6:
            a = self._rng.randint(-8, 8)
            b = self._rng.randint(1, 6)
            d = self._rng.choice([-3, -2, -1, 2, 3, 5, -5, -7])
        else:
            a = self._rng.randint(-10, 10)
            b = self._rng.randint(1, 8)
            d = self._rng.choice([-3, -2, 2, 3, 5, -5, -7, -11])

        norm = a * a - d * b * b
        trace = 2 * a

        # For high difficulty, also compute product norm
        verify_mult = difficulty >= 7
        a2 = self._rng.randint(1, 4)
        b2 = self._rng.randint(1, 3)
        norm2 = a2 * a2 - d * b2 * b2
        product_norm = norm * norm2

        sign_str = "+" if b >= 0 else "-"
        b_abs = abs(b)
        if d < 0:
            d_str = f"\\sqrt{{{d}}}"
        else:
            d_str = f"\\sqrt{{{d}}}"

        problem = (
            f"\\alpha = {a} {sign_str} {b_abs}{d_str}"
            f" \\in \\mathbb{{Q}}({d_str})"
        )

        return problem, {
            "a": a, "b": b, "d": d,
            "norm": norm, "trace": trace,
            "verify_mult": verify_mult,
            "a2": a2, "b2": b2, "norm2": norm2,
            "product_norm": product_norm,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate norm and trace computation steps.

        Args:
            data: Solution data with field element.

        Returns:
            List of step strings.
        """
        a, b, d = data["a"], data["b"], data["d"]
        steps = [
            f"alpha = {a} + {b}*sqrt({d})",
            f"N(alpha) = {a}^2 - ({d})*{b}^2"
            f" = {a * a} - {d * b * b} = {data['norm']}",
            f"T(alpha) = 2*{a} = {data['trace']}",
        ]
        if data["verify_mult"]:
            steps.append(
                f"beta = {data['a2']} + {data['b2']}*sqrt({d}), "
                f"N(beta) = {data['norm2']}"
            )
            steps.append(
                f"N(alpha*beta) = N(alpha)*N(beta)"
                f" = {data['norm']}*{data['norm2']}"
                f" = {data['product_norm']}"
            )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return norm and trace values.

        Args:
            data: Solution data.

        Returns:
            String with N and T values.
        """
        ans = f"N = {data['norm']}, T = {data['trace']}"
        if data["verify_mult"]:
            ans += f", N(alpha*beta) = {data['product_norm']}"
        return ans


# ===================================================================
# 2. Ring of Integers  (tier 6)
# ===================================================================

@register
class RingOfIntegersGenerator(StepGenerator):
    """Determine the ring of integers of Q(sqrt(d)).

    The ring of integers O_K of Q(sqrt(d)) depends on d mod 4:
    - If d = 2, 3 (mod 4): O_K = Z[sqrt(d)]
    - If d = 1 (mod 4): O_K = Z[(1 + sqrt(d))/2]

    Difficulty scaling:
        Difficulty 1-3: positive squarefree d, simple cases.
        Difficulty 4-6: negative d (imaginary quadratic fields).
        Difficulty 7-8: verify an element is/is not in O_K.

    Prerequisites:
        modular.
    """

    _SQUAREFREE_POS = [2, 3, 5, 6, 7, 10, 11, 13, 14, 15, 17, 19]
    _SQUAREFREE_NEG = [-1, -2, -3, -5, -7, -11, -13, -15, -19, -23]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "ring_of_integers"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["modular"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "determine ring of integers of quadratic field"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a ring of integers determination problem.

        Args:
            difficulty: Controls field type and membership test.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            d = self._rng.choice(self._SQUAREFREE_POS)
        elif difficulty <= 6:
            d = self._rng.choice(
                self._SQUAREFREE_NEG + self._SQUAREFREE_POS[:6]
            )
        else:
            d = self._rng.choice(
                self._SQUAREFREE_NEG + self._SQUAREFREE_POS
            )

        d_mod4 = d % 4
        if d_mod4 < 0:
            d_mod4 += 4

        if d_mod4 == 1:
            ring_str = f"Z[(1 + sqrt({d}))/2]"
            basis = f"1, (1 + sqrt({d}))/2"
            discriminant = d
        else:
            ring_str = f"Z[sqrt({d})]"
            basis = f"1, sqrt({d})"
            discriminant = 4 * d

        # For high difficulty, test membership
        test_membership = difficulty >= 7
        test_a = self._rng.randint(1, 5)
        test_b = self._rng.randint(1, 5)
        if d_mod4 == 1:
            # (test_a + test_b*(1+sqrt(d))/2) is in O_K
            is_in_ring = True
            test_elem = f"{test_a} + {test_b}*(1+sqrt({d}))/2"
        else:
            # test_a + test_b*sqrt(d) is in O_K
            is_in_ring = True
            test_elem = f"{test_a} + {test_b}*sqrt({d})"

        # Also test one that might not be in O_K
        bad_b_num = 2 * self._rng.randint(1, 3) + 1  # odd numerator
        bad_b_den = 2
        if d_mod4 == 1:
            # (1+sqrt(d))/2 basis, so half-integer coeffs are OK
            is_bad_in_ring = True
        else:
            # Z[sqrt(d)] basis, so half-integer coeff is NOT in O_K
            is_bad_in_ring = False

        problem = f"\\mathcal{{O}}_{{\\mathbb{{Q}}(\\sqrt{{{d}}})}}"

        return problem, {
            "d": d, "d_mod4": d_mod4,
            "ring_str": ring_str, "basis": basis,
            "discriminant": discriminant,
            "test_membership": test_membership,
            "test_elem": test_elem, "is_in_ring": is_in_ring,
            "bad_elem": f"{bad_b_num}/{bad_b_den}*sqrt({d})",
            "is_bad_in_ring": is_bad_in_ring,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate ring of integers determination steps.

        Args:
            data: Solution data with field discriminant.

        Returns:
            List of step strings.
        """
        d = data["d"]
        steps = [
            f"d = {d}, d mod 4 = {data['d_mod4']}",
        ]
        if data["d_mod4"] == 1:
            steps.append(f"d = 1 mod 4: O_K = {data['ring_str']}")
        else:
            steps.append(f"d != 1 mod 4: O_K = {data['ring_str']}")
        steps.append(f"basis: {data['basis']}")
        steps.append(f"discriminant = {data['discriminant']}")

        if data["test_membership"]:
            steps.append(
                f"{data['test_elem']}: "
                f"{'in' if data['is_in_ring'] else 'not in'} O_K"
            )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the ring of integers.

        Args:
            data: Solution data.

        Returns:
            String with O_K description.
        """
        return f"O_K = {data['ring_str']}, disc = {data['discriminant']}"


# ===================================================================
# 3. Ideal Factorisation  (tier 7)
# ===================================================================

@register
class IdealFactorisationGenerator(StepGenerator):
    """Factor an ideal (p) in the ring of integers of Q(sqrt(d)).

    A rational prime p in Z[sqrt(d)] either splits (p) = P*P',
    ramifies (p) = P^2, or remains inert. The behaviour is
    determined by the Legendre symbol (d/p).

    Difficulty scaling:
        Difficulty 1-3: small primes, positive d.
        Difficulty 4-6: larger primes, mixed sign d.
        Difficulty 7-8: explicit ideal generators given.

    Prerequisites:
        factorisation.
    """

    _FIELDS = [
        {"d": -1, "label": "Gaussian integers"},
        {"d": -3, "label": "Eisenstein integers"},
        {"d": 2, "label": "Q(sqrt(2))"},
        {"d": -5, "label": "Q(sqrt(-5))"},
        {"d": 3, "label": "Q(sqrt(3))"},
        {"d": 5, "label": "Q(sqrt(5))"},
        {"d": -7, "label": "Q(sqrt(-7))"},
        {"d": -2, "label": "Q(sqrt(-2))"},
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "ideal_factorisation"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["factorisation"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "factor rational prime in ring of integers"

    def _classify_prime(self, p: int, d: int) -> str:
        """Classify how prime p behaves in Z[sqrt(d)].

        Args:
            p: A rational prime.
            d: Squarefree integer defining the field.

        Returns:
            One of 'split', 'ramified', 'inert'.
        """
        if p == 2:
            d_mod8 = d % 8
            if d_mod8 < 0:
                d_mod8 += 8
            if d_mod8 == 1 or d_mod8 == 7:
                return "split"
            if d_mod8 == 3 or d_mod8 == 5:
                return "inert"
            return "ramified"

        leg = _legendre_symbol(d, p)
        if leg == 1:
            return "split"
        if leg == -1:
            return "inert"
        return "ramified"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an ideal factorisation problem.

        Args:
            difficulty: Controls prime size and field choice.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            pool = self._FIELDS[:3]
            primes = [2, 3, 5, 7]
        elif difficulty <= 6:
            pool = self._FIELDS[:6]
            primes = [2, 3, 5, 7, 11, 13]
        else:
            pool = self._FIELDS
            primes = [2, 3, 5, 7, 11, 13, 17, 19]

        field = self._rng.choice(pool)
        d = field["d"]
        p = self._rng.choice(primes)

        behaviour = self._classify_prime(p, d)

        if p == 2:
            leg_str = f"d mod 8 = {d % 8}"
        else:
            leg = _legendre_symbol(d, p)
            leg_str = f"({d}/{p}) = {leg}"

        problem = f"({p}) \\text{{ in }} \\mathbb{{Z}}[\\sqrt{{{d}}}]"

        return problem, {
            "p": p, "d": d, "label": field["label"],
            "behaviour": behaviour,
            "leg_str": leg_str,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate ideal factorisation steps.

        Args:
            data: Solution data with prime and field.

        Returns:
            List of step strings.
        """
        p, d = data["p"], data["d"]
        steps = [
            f"field: {data['label']}, d = {d}",
            f"prime p = {p}",
            f"test: {data['leg_str']}",
        ]
        if data["behaviour"] == "split":
            steps.append(f"({p}) = P * P' (splits)")
        elif data["behaviour"] == "ramified":
            steps.append(f"({p}) = P^2 (ramifies)")
        else:
            steps.append(f"({p}) remains inert")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the factorisation type.

        Args:
            data: Solution data.

        Returns:
            String describing the behaviour.
        """
        return f"({data['p']}): {data['behaviour']}"


# ===================================================================
# 4. Class Number  (tier 7)
# ===================================================================

@register
class ClassNumberGenerator(StepGenerator):
    """Compute the class number h(d) for small discriminants.

    The class number measures the failure of unique factorisation
    in the ring of integers. Uses the Minkowski bound to limit the
    search for ideal classes.

    Difficulty scaling:
        Difficulty 1-3: known h=1 fields (d=-1,-2,-3,-7).
        Difficulty 4-6: h=1 or h=2 fields.
        Difficulty 7-8: h=2 or h=3 fields with Minkowski bound.

    Prerequisites:
        factorisation.
    """

    # (d, class_number, minkowski_bound, is_ufd)
    _CLASS_DATA = [
        (-1, 1, 1.27, True),
        (-2, 1, 1.80, True),
        (-3, 1, 1.10, True),
        (-7, 1, 1.68, True),
        (-11, 1, 2.11, True),
        (-5, 2, 2.84, False),
        (-6, 2, 3.11, False),
        (-10, 2, 4.02, False),
        (-14, 4, 4.76, False),
        (-15, 2, 4.92, False),
        (-23, 3, 6.09, False),
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "class_number"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["factorisation"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute class number of imaginary quadratic field"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a class number computation problem.

        Args:
            difficulty: Controls discriminant complexity.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            pool = [e for e in self._CLASS_DATA if e[1] == 1]
        elif difficulty <= 6:
            pool = [e for e in self._CLASS_DATA if e[1] <= 2]
        else:
            pool = [e for e in self._CLASS_DATA if e[1] >= 2]

        d, h, mink, is_ufd = self._rng.choice(pool)

        # Compute discriminant
        d_mod4 = d % 4
        if d_mod4 < 0:
            d_mod4 += 4
        disc = d if d_mod4 == 1 else 4 * d

        problem = f"h(\\mathbb{{Q}}(\\sqrt{{{d}}}))"

        return problem, {
            "d": d, "h": h,
            "minkowski": round(mink, 4),
            "is_ufd": is_ufd,
            "disc": disc,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate class number computation steps.

        Args:
            data: Solution data with discriminant and bound.

        Returns:
            List of step strings.
        """
        d = data["d"]
        steps = [
            f"Q(sqrt({d})), disc = {data['disc']}",
            f"Minkowski bound = {_fmt(data['minkowski'])}",
            f"check primes p <= {math.floor(data['minkowski'])}",
        ]
        if data["is_ufd"]:
            steps.append("all ideals principal -> h = 1 (UFD)")
        else:
            steps.append(f"non-trivial ideal classes -> h = {data['h']}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the class number.

        Args:
            data: Solution data.

        Returns:
            String with class number and UFD status.
        """
        ufd = "UFD" if data["is_ufd"] else "not UFD"
        return f"h = {data['h']} ({ufd})"


# ===================================================================
# 5. p-adic Valuation  (tier 6)
# ===================================================================

@register
class PAdicValuationGenerator(StepGenerator):
    """Compute the p-adic valuation v_p(n).

    The p-adic valuation v_p(n) is the exponent of p in the prime
    factorisation of n. Key properties: v_p(a*b) = v_p(a) + v_p(b),
    v_p(a+b) >= min(v_p(a), v_p(b)).

    Difficulty scaling:
        Difficulty 1-3: small n, small prime p.
        Difficulty 4-6: compute v_p for a product a*b.
        Difficulty 7-8: verify ultrametric inequality for a sum.

    Prerequisites:
        factorisation.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "p_adic_valuation"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["factorisation"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute p-adic valuation"

    def _valuation(self, n: int, p: int) -> int:
        """Compute v_p(n) for positive n.

        Args:
            n: Positive integer.
            p: Prime.

        Returns:
            Exponent of p in factorisation of n.
        """
        if n == 0:
            return float("inf")
        v = 0
        while n % p == 0:
            v += 1
            n //= p
        return v

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a p-adic valuation problem.

        Args:
            difficulty: Controls number size and problem type.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            p = self._rng.choice([2, 3, 5])
            n = self._rng.randint(2, 100)
            v = self._valuation(n, p)
            problem = f"v_{{{p}}}({n})"
            return problem, {
                "mode": "single", "p": p, "n": n, "v": v,
            }

        if difficulty <= 6:
            p = self._rng.choice([2, 3, 5, 7])
            a = self._rng.randint(2, 50)
            b = self._rng.randint(2, 50)
            va = self._valuation(a, p)
            vb = self._valuation(b, p)
            product = a * b
            vp = va + vb
            problem = f"v_{{{p}}}({a} \\cdot {b})"
            return problem, {
                "mode": "product", "p": p,
                "a": a, "b": b, "va": va, "vb": vb,
                "product": product, "vp": vp,
            }

        # Ultrametric inequality
        p = self._rng.choice([2, 3, 5])
        a = self._rng.randint(2, 80)
        b = self._rng.randint(2, 80)
        va = self._valuation(a, p)
        vb = self._valuation(b, p)
        s = a + b
        vs = self._valuation(s, p)
        min_vab = min(va, vb)
        problem = f"v_{{{p}}}({a} + {b})"
        return problem, {
            "mode": "sum", "p": p,
            "a": a, "b": b, "va": va, "vb": vb,
            "sum": s, "vs": vs, "min_vab": min_vab,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate p-adic valuation steps.

        Args:
            data: Solution data with valuation details.

        Returns:
            List of step strings.
        """
        p = data["p"]

        if data["mode"] == "single":
            n = data["n"]
            factors = _factorise(n)
            fac_str = " * ".join(
                f"{pr}^{e}" if e > 1 else str(pr) for pr, e in factors
            )
            return [
                f"{n} = {fac_str}",
                f"v_{p}({n}) = {data['v']}",
            ]

        if data["mode"] == "product":
            return [
                f"v_{p}({data['a']}) = {data['va']}",
                f"v_{p}({data['b']}) = {data['vb']}",
                f"v_{p}({data['a']}*{data['b']})"
                f" = {data['va']} + {data['vb']} = {data['vp']}",
            ]

        # sum mode
        return [
            f"v_{p}({data['a']}) = {data['va']}",
            f"v_{p}({data['b']}) = {data['vb']}",
            f"min(v_{p}(a), v_{p}(b)) = {data['min_vab']}",
            f"v_{p}({data['a']} + {data['b']})"
            f" = v_{p}({data['sum']}) = {data['vs']}",
            f"{data['vs']} >= {data['min_vab']}: "
            f"{'holds' if data['vs'] >= data['min_vab'] else 'violated'}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the p-adic valuation.

        Args:
            data: Solution data.

        Returns:
            String with valuation value.
        """
        if data["mode"] == "single":
            return f"v_{data['p']}({data['n']}) = {data['v']}"
        if data["mode"] == "product":
            return f"v_{data['p']}({data['product']}) = {data['vp']}"
        return f"v_{data['p']}({data['sum']}) = {data['vs']}"


# ===================================================================
# 6. Hensel Lift  (tier 7)
# ===================================================================

@register
class HenselLiftGenerator(StepGenerator):
    """Lift a root of f(x) = 0 mod p to mod p^2 using Hensel's lemma.

    Given f(x) with a simple root x_0 mod p (i.e. f'(x_0) != 0 mod p),
    lift to x_1 = x_0 - f(x_0) * f'(x_0)^{-1} mod p^2.

    Difficulty scaling:
        Difficulty 1-3: f(x) = x^2 - a, small p.
        Difficulty 4-6: f(x) = x^2 + bx + c, medium p.
        Difficulty 7-8: f(x) = x^3 + ax + b, lift to mod p^3.

    Prerequisites:
        mod_inv.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "hensel_lift"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["mod_inv"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "lift root mod p to mod p^2 via Hensel's lemma"

    def _find_root_mod_p(self, coeffs: list[int], p: int) -> int:
        """Find a simple root of polynomial mod p by brute force.

        Args:
            coeffs: Polynomial coefficients [a_n, ..., a_1, a_0]
                     for a_n*x^n + ... + a_1*x + a_0.
            p: Prime modulus.

        Returns:
            A root x_0 with f'(x_0) != 0 mod p, or -1 if none.
        """
        n = len(coeffs) - 1
        for x in range(p):
            val = 0
            for c in coeffs:
                val = (val * x + c) % p
            if val == 0:
                # Check derivative is non-zero
                deriv_coeffs = [
                    (n - i) * coeffs[i] for i in range(n)
                ]
                dval = 0
                for c in deriv_coeffs:
                    dval = (dval * x + c) % p
                if dval % p != 0:
                    return x
        return -1

    def _eval_poly(self, coeffs: list[int], x: int, mod: int) -> int:
        """Evaluate polynomial at x modulo mod.

        Args:
            coeffs: Polynomial coefficients [a_n, ..., a_1, a_0].
            x: Point to evaluate at.
            mod: Modulus.

        Returns:
            f(x) mod mod.
        """
        val = 0
        for c in coeffs:
            val = (val * x + c) % mod
        return val

    def _eval_deriv(self, coeffs: list[int], x: int, mod: int) -> int:
        """Evaluate derivative of polynomial at x modulo mod.

        Args:
            coeffs: Polynomial coefficients [a_n, ..., a_1, a_0].
            x: Point to evaluate at.
            mod: Modulus.

        Returns:
            f'(x) mod mod.
        """
        n = len(coeffs) - 1
        deriv_coeffs = [(n - i) * coeffs[i] for i in range(n)]
        val = 0
        for c in deriv_coeffs:
            val = (val * x + c) % mod
        return val

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Hensel lifting problem.

        Args:
            difficulty: Controls polynomial degree and lift level.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            p = self._rng.choice([3, 5, 7])
            # f(x) = x^2 - a
            a = self._rng.randint(2, p * p - 1)
            coeffs = [1, 0, -a]
            poly_str = f"x^2 - {a}"
        elif difficulty <= 6:
            p = self._rng.choice([3, 5, 7, 11])
            b = self._rng.randint(1, p - 1)
            c = self._rng.randint(1, p - 1)
            coeffs = [1, b, c]
            poly_str = f"x^2 + {b}x + {c}"
        else:
            p = self._rng.choice([3, 5, 7])
            a_coeff = self._rng.randint(1, p - 1)
            b_coeff = self._rng.randint(1, p - 1)
            coeffs = [1, 0, a_coeff, b_coeff]
            poly_str = f"x^3 + {a_coeff}x + {b_coeff}"

        x0 = self._find_root_mod_p(coeffs, p)

        # If no simple root found, fall back to x^2 - 1 which
        # always has x=1 as a root for p >= 3
        if x0 == -1:
            coeffs = [1, 0, -1]
            poly_str = "x^2 - 1"
            x0 = 1

        p_sq = p * p
        f_x0 = self._eval_poly(coeffs, x0, p_sq)
        fp_x0 = self._eval_deriv(coeffs, x0, p)
        fp_inv = _mod_inverse(fp_x0, p)

        # Hensel lift: x1 = x0 - f(x0) * f'(x0)^{-1} mod p^2
        x1 = (x0 - f_x0 * fp_inv) % p_sq

        # Verify
        f_x1 = self._eval_poly(coeffs, x1, p_sq)

        # For high difficulty, also lift to p^3
        lift_to_p3 = difficulty >= 7
        x2 = 0
        p_cube = p * p * p
        if lift_to_p3:
            f_x1_p3 = self._eval_poly(coeffs, x1, p_cube)
            fp_x1 = self._eval_deriv(coeffs, x1, p)
            fp_inv2 = _mod_inverse(fp_x1, p)
            x2 = (x1 - f_x1_p3 * fp_inv2) % p_cube

        problem = (
            f"f(x) = {poly_str}, \\; f(x) \\equiv 0 \\pmod{{{p}}}"
        )

        return problem, {
            "poly_str": poly_str, "coeffs": coeffs,
            "p": p, "p_sq": p_sq,
            "x0": x0, "f_x0": f_x0,
            "fp_x0": fp_x0, "fp_inv": fp_inv,
            "x1": x1, "f_x1": f_x1,
            "lift_to_p3": lift_to_p3,
            "x2": x2, "p_cube": p_cube,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Hensel lifting steps.

        Args:
            data: Solution data with root and lift details.

        Returns:
            List of step strings.
        """
        p = data["p"]
        steps = [
            f"f(x) = {data['poly_str']}",
            f"x_0 = {data['x0']} (root mod {p})",
            f"f({data['x0']}) mod {data['p_sq']} = {data['f_x0']}",
            f"f'({data['x0']}) mod {p} = {data['fp_x0']}",
            f"f'(x_0)^{{-1}} mod {p} = {data['fp_inv']}",
            f"x_1 = {data['x0']} - {data['f_x0']}*{data['fp_inv']}"
            f" mod {data['p_sq']} = {data['x1']}",
        ]
        if data["lift_to_p3"]:
            steps.append(
                f"lift to mod {data['p_cube']}: x_2 = {data['x2']}"
            )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the lifted root.

        Args:
            data: Solution data.

        Returns:
            String with x_1 (and x_2 if applicable).
        """
        ans = f"x_1 = {data['x1']} mod {data['p_sq']}"
        if data["lift_to_p3"]:
            ans += f", x_2 = {data['x2']} mod {data['p_cube']}"
        return ans
