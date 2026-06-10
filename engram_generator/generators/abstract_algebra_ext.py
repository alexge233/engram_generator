"""Extended abstract algebra generators.

10 generators covering dihedral groups, group centres, conjugacy classes,
group actions, polynomial rings, Chinese remainder for rings, Euclidean
domains, free groups, permutation cycles, and automorphism groups across
tiers 4-6.
"""
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


def _lcm(a: int, b: int) -> int:
    """Compute least common multiple.

    Args:
        a: First integer.
        b: Second integer.

    Returns:
        LCM of a and b.
    """
    if a == 0 or b == 0:
        return 0
    return abs(a * b) // _gcd(a, b)


def _format_set(elements: list) -> str:
    """Format a list as a set string.

    Args:
        elements: Sorted list of elements.

    Returns:
        String like ``{0, 1, 2}``.
    """
    return "{" + ", ".join(str(e) for e in elements) + "}"


def _format_poly(coeffs: list[int], var: str = "x") -> str:
    """Format polynomial coefficients as a string.

    Args:
        coeffs: Coefficients from highest to lowest degree.
        var: Variable name.

    Returns:
        Polynomial string.
    """
    deg = len(coeffs) - 1
    parts = []
    for i, c in enumerate(coeffs):
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
# 1. DIHEDRAL GROUP (tier 5)
# ===================================================================

@register
class DihedralGroupGenerator(StepGenerator):
    """Compute products in the dihedral group D_n.

    Elements are rotations r^k (k=0..n-1) and reflections s*r^k.
    Uses relations: r^n = 1, s^2 = 1, s*r = r^{-1}*s.

    Difficulty scaling:
        Difficulty 1-3: n in [3, 4].
        Difficulty 4-6: n in [4, 5].
        Difficulty 7-8: n in [5, 6].

    Prerequisites:
        group_table (tier 4).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "dihedral_group"

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
            difficulty: Controls group size.

        Returns:
            Task description string.
        """
        return "compute product in dihedral group D_n"

    def _select_n(self, difficulty: int) -> int:
        """Choose n for D_n based on difficulty.

        Args:
            difficulty: Difficulty level 1-8.

        Returns:
            Integer n.
        """
        if difficulty <= 3:
            return self._rng.choice([3, 4])
        if difficulty <= 6:
            return self._rng.choice([4, 5])
        return self._rng.choice([5, 6])

    def _multiply(self, n: int, a_s: bool, a_r: int,
                  b_s: bool, b_r: int) -> tuple[bool, int]:
        """Multiply two D_n elements.

        Each element is (has_s, rotation_power). The product uses
        s*r^k = r^{-k}*s and s^2 = 1.

        Args:
            n: Order of the rotation subgroup.
            a_s: Whether first element has reflection.
            a_r: Rotation power of first element.
            b_s: Whether second element has reflection.
            b_r: Rotation power of second element.

        Returns:
            Tuple of (result_has_s, result_rotation).
        """
        if not a_s and not b_s:
            return False, (a_r + b_r) % n
        if not a_s and b_s:
            return True, (a_r + b_r) % n
        if a_s and not b_s:
            return True, (a_r - b_r) % n
        return False, (a_r - b_r) % n

    def _elem_str(self, has_s: bool, rot: int) -> str:
        """Format a D_n element as a string.

        Args:
            has_s: Whether the element has a reflection.
            rot: Rotation power.

        Returns:
            String like ``sr^2`` or ``r^3``.
        """
        if not has_s and rot == 0:
            return "e"
        if not has_s:
            return f"r^{rot}" if rot > 1 else "r"
        if rot == 0:
            return "s"
        return f"sr^{rot}" if rot > 1 else "sr"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a dihedral group product problem.

        Args:
            difficulty: Controls group size.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        n = self._select_n(difficulty)
        a_s = self._rng.choice([True, False])
        a_r = self._rng.randint(0, n - 1)
        b_s = self._rng.choice([True, False])
        b_r = self._rng.randint(0, n - 1)

        res_s, res_r = self._multiply(n, a_s, a_r, b_s, b_r)

        a_str = self._elem_str(a_s, a_r)
        b_str = self._elem_str(b_s, b_r)
        res_str = self._elem_str(res_s, res_r)

        problem = f"D_{n}: compute {a_str} * {b_str}"
        return problem, {
            "n": n, "a_str": a_str, "b_str": b_str,
            "a_s": a_s, "a_r": a_r, "b_s": b_s, "b_r": b_r,
            "res_s": res_s, "res_r": res_r, "res_str": res_str,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate product computation steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing the computation.
        """
        n = data["n"]
        steps = [
            f"D_{n}: r^{n}=e, s^2=e, sr=r^{{-1}}s",
            f"({data['a_str']}) * ({data['b_str']})",
        ]
        if data["a_s"] and not data["b_s"]:
            steps.append(
                f"s*r^{data['a_r']} * r^{data['b_r']} = "
                f"s*r^{(data['a_r'] - data['b_r']) % n} "
                f"(using sr^k * r^j = sr^{{k-j}})"
            )
        elif data["a_s"] and data["b_s"]:
            steps.append(
                f"sr^{data['a_r']} * sr^{data['b_r']} = "
                f"r^{(data['a_r'] - data['b_r']) % n} "
                f"(using s^2=e)"
            )
        else:
            steps.append(f"combine rotations mod {n}")
        steps.append(f"= {data['res_str']}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the final answer.

        Args:
            data: Solution data.

        Returns:
            Product element.
        """
        return data["res_str"]


# ===================================================================
# 2. GROUP CENTER (tier 5)
# ===================================================================

@register
class GroupCenterGenerator(StepGenerator):
    """Find the center Z(G) of a small group.

    For Z_n (abelian), Z(G) = G. For D_n, Z(G) depends on parity of n.
    Checks commutativity of each element with all others.

    Difficulty scaling:
        Difficulty 1-3: Z_n groups (n in [3, 5]).
        Difficulty 4-6: D_3 or D_4.
        Difficulty 7-8: D_5 or D_6.

    Prerequisites:
        group_table (tier 4).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "group_center"

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
            difficulty: Controls group type and size.

        Returns:
            Task description string.
        """
        return "find the center Z(G) of a group"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a group center problem.

        Args:
            difficulty: Controls group type and size.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            n = self._rng.randint(3, 5)
            group_type = "Z_n"
            center = list(range(n))
            center_str = _format_set(center)
            reason = f"Z_{n} is abelian, so Z(G) = G"
            problem = f"G = Z_{n} under addition. Find Z(G)."
            return problem, {
                "group": f"Z_{n}", "center": center,
                "center_str": center_str, "reason": reason,
            }

        if difficulty <= 6:
            n = self._rng.choice([3, 4])
        else:
            n = self._rng.choice([5, 6])

        if n % 2 == 0:
            center_elems = ["e", f"r^{n // 2}"]
            reason = f"D_{n} (n even): center = {{e, r^{n // 2}}}"
        else:
            center_elems = ["e"]
            reason = f"D_{n} (n odd): center = {{e}}"

        problem = f"G = D_{n}. Find Z(G)."
        return problem, {
            "group": f"D_{n}", "center": center_elems,
            "center_str": "{" + ", ".join(center_elems) + "}",
            "reason": reason,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate center computation steps.

        Args:
            data: Solution data.

        Returns:
            Steps explaining the center.
        """
        return [
            f"G = {data['group']}",
            "Z(G) = {{g in G : gx = xg for all x in G}}",
            data["reason"],
            f"Z(G) = {data['center_str']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the final answer.

        Args:
            data: Solution data.

        Returns:
            Center as a set string.
        """
        return f"Z(G) = {data['center_str']}"


# ===================================================================
# 3. CONJUGACY CLASS (tier 6)
# ===================================================================

@register
class ConjugacyClassGenerator(StepGenerator):
    """Compute the conjugacy class of an element in S_3.

    The conjugacy class of a in G is {g*a*g^{-1} : g in G}.
    In S_3, conjugacy classes correspond to cycle types.

    Difficulty scaling:
        Difficulty 1-3: identity and transpositions in S_3.
        Difficulty 4-6: 3-cycles in S_3.
        Difficulty 7-8: elements in S_4 (by cycle type).

    Prerequisites:
        group_table (tier 4).
    """

    _S3_ELEMENTS = [
        (0, "e", [1, 2, 3]),
        (1, "(1 2)", [2, 1, 3]),
        (2, "(1 3)", [3, 2, 1]),
        (3, "(2 3)", [1, 3, 2]),
        (4, "(1 2 3)", [2, 3, 1]),
        (5, "(1 3 2)", [3, 1, 2]),
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "conjugacy_class"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["group_table"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls group complexity.

        Returns:
            Task description string.
        """
        return "compute conjugacy class of element in symmetric group"

    def _compose(self, sigma: list[int], tau: list[int]) -> list[int]:
        """Compose two permutations (sigma after tau).

        Args:
            sigma: First permutation (applied second), 1-indexed images.
            tau: Second permutation (applied first), 1-indexed images.

        Returns:
            Composed permutation.
        """
        return [sigma[tau[i] - 1] for i in range(len(sigma))]

    def _inverse(self, perm: list[int]) -> list[int]:
        """Compute inverse permutation.

        Args:
            perm: Permutation as 1-indexed images.

        Returns:
            Inverse permutation.
        """
        inv = [0] * len(perm)
        for i, p in enumerate(perm):
            inv[p - 1] = i + 1
        return inv

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a conjugacy class problem.

        Args:
            difficulty: Controls group complexity.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        idx, name, perm = self._rng.choice(self._S3_ELEMENTS)

        conj_class = set()
        for _, _, g in self._S3_ELEMENTS:
            g_inv = self._inverse(g)
            result = self._compose(g, self._compose(perm, g_inv))
            conj_class.add(tuple(result))

        conj_names = []
        for c in sorted(conj_class):
            for _, n, p in self._S3_ELEMENTS:
                if list(c) == p:
                    conj_names.append(n)
                    break

        problem = f"S_3: conjugacy class of a = {name}"
        return problem, {
            "element": name, "perm": perm,
            "conj_class": conj_names,
            "size": len(conj_names),
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate conjugacy class computation steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing the conjugation.
        """
        return [
            f"a = {data['element']}",
            "conjugacy class = {{g*a*g^{{-1}} : g in S_3}}",
            f"elements: {', '.join(data['conj_class'])}",
            f"|class| = {data['size']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the final answer.

        Args:
            data: Solution data.

        Returns:
            Conjugacy class elements.
        """
        return "{" + ", ".join(data["conj_class"]) + "}"


# ===================================================================
# 4. GROUP ACTION (tier 6)
# ===================================================================

@register
class GroupActionGenerator(StepGenerator):
    """Compute orbit and stabiliser of a group action.

    Z_n acts on Z_n by addition. Computes Orb(x) and Stab(x) and
    verifies the orbit-stabiliser theorem: |Orb(x)|*|Stab(x)| = |G|.

    Difficulty scaling:
        Difficulty 1-3: Z_n acting on itself, n in [3, 5].
        Difficulty 4-6: n in [5, 7].
        Difficulty 7-8: n in [6, 8].

    Prerequisites:
        group_table (tier 4).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "group_action"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["group_table"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls group size.

        Returns:
            Task description string.
        """
        return "compute orbit and stabiliser of group action"

    def _select_n(self, difficulty: int) -> int:
        """Choose group order based on difficulty.

        Args:
            difficulty: Difficulty level 1-8.

        Returns:
            Integer n.
        """
        if difficulty <= 3:
            return self._rng.randint(3, 5)
        if difficulty <= 6:
            return self._rng.randint(5, 7)
        return self._rng.randint(6, 8)

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a group action problem.

        Args:
            difficulty: Controls group size.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        n = self._select_n(difficulty)
        x = self._rng.randint(0, n - 1)

        orbit = sorted(set((g + x) % n for g in range(n)))
        stabiliser = sorted(g for g in range(n) if (g + x) % n == x)

        orbit_size = len(orbit)
        stab_size = len(stabiliser)
        verify = orbit_size * stab_size == n

        problem = (
            f"Z_{n} acts on Z_{n} by addition. "
            f"Find Orb({x}) and Stab({x})."
        )
        return problem, {
            "n": n, "x": x,
            "orbit": orbit, "stabiliser": stabiliser,
            "orbit_size": orbit_size, "stab_size": stab_size,
            "verify": verify,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate orbit-stabiliser computation steps.

        Args:
            data: Solution data.

        Returns:
            Steps computing orbit and stabiliser.
        """
        return [
            f"action: g.x = (g + {data['x']}) mod {data['n']}",
            f"Orb({data['x']}) = {_format_set(data['orbit'])}",
            f"Stab({data['x']}) = {_format_set(data['stabiliser'])}",
            f"|Orb|*|Stab| = {data['orbit_size']}*{data['stab_size']} = "
            f"{data['orbit_size'] * data['stab_size']} = |G| = {data['n']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the final answer.

        Args:
            data: Solution data.

        Returns:
            Orbit and stabiliser.
        """
        return (
            f"Orb = {_format_set(data['orbit'])}, "
            f"Stab = {_format_set(data['stabiliser'])}"
        )


# ===================================================================
# 5. POLYNOMIAL RING (tier 5)
# ===================================================================

@register
class PolynomialRingGenerator(StepGenerator):
    """Perform arithmetic in Z_p[x].

    Adds or multiplies two polynomials over a prime field Z_p,
    reducing coefficients modulo p.

    Difficulty scaling:
        Difficulty 1-3: p in [2, 3], degree 1-2.
        Difficulty 4-6: p in [3, 5], degree 2-3.
        Difficulty 7-8: p in [5, 7], degree 2-3.

    Prerequisites:
        polynomial_division (tier 5).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "polynomial_ring"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["polynomial_division"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls field size and degree.

        Returns:
            Task description string.
        """
        return "perform polynomial arithmetic in Z_p[x]"

    def _select_params(self, difficulty: int) -> tuple[int, int]:
        """Choose prime p and max degree.

        Args:
            difficulty: Difficulty level 1-8.

        Returns:
            Tuple of (prime, max_degree).
        """
        if difficulty <= 3:
            return self._rng.choice([2, 3]), self._rng.randint(1, 2)
        if difficulty <= 6:
            return self._rng.choice([3, 5]), self._rng.randint(2, 3)
        return self._rng.choice([5, 7]), self._rng.randint(2, 3)

    def _random_poly(self, p: int, deg: int) -> list[int]:
        """Generate a random polynomial with given degree over Z_p.

        Args:
            p: Prime modulus.
            deg: Degree of the polynomial.

        Returns:
            Coefficients from highest to lowest degree.
        """
        coeffs = [self._rng.randint(1, p - 1)]
        for _ in range(deg):
            coeffs.append(self._rng.randint(0, p - 1))
        return coeffs

    def _add_poly(self, a: list[int], b: list[int], p: int) -> list[int]:
        """Add two polynomials mod p.

        Args:
            a: First polynomial coefficients (high to low).
            b: Second polynomial coefficients (high to low).
            p: Prime modulus.

        Returns:
            Sum polynomial coefficients.
        """
        max_len = max(len(a), len(b))
        pa = [0] * (max_len - len(a)) + a
        pb = [0] * (max_len - len(b)) + b
        result = [(pa[i] + pb[i]) % p for i in range(max_len)]
        while len(result) > 1 and result[0] == 0:
            result.pop(0)
        return result

    def _mul_poly(self, a: list[int], b: list[int], p: int) -> list[int]:
        """Multiply two polynomials mod p.

        Args:
            a: First polynomial coefficients (high to low).
            b: Second polynomial coefficients (high to low).
            p: Prime modulus.

        Returns:
            Product polynomial coefficients.
        """
        result = [0] * (len(a) + len(b) - 1)
        for i, ca in enumerate(a):
            for j, cb in enumerate(b):
                result[i + j] = (result[i + j] + ca * cb) % p
        while len(result) > 1 and result[0] == 0:
            result.pop(0)
        return result

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a polynomial ring arithmetic problem.

        Args:
            difficulty: Controls field size and degree.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        p, deg = self._select_params(difficulty)
        a = self._random_poly(p, deg)
        b_deg = self._rng.randint(1, deg)
        b = self._random_poly(p, b_deg)

        op = self._rng.choice(["add", "multiply"])
        if op == "add":
            result = self._add_poly(a, b, p)
        else:
            result = self._mul_poly(a, b, p)

        a_str = _format_poly(a)
        b_str = _format_poly(b)
        r_str = _format_poly(result)
        op_sym = "+" if op == "add" else "*"

        problem = f"Z_{p}[x]: ({a_str}) {op_sym} ({b_str})"
        return problem, {
            "p": p, "a": a, "b": b, "op": op,
            "a_str": a_str, "b_str": b_str,
            "result": result, "r_str": r_str,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate polynomial arithmetic steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing the computation.
        """
        steps = [
            f"f(x) = {data['a_str']}",
            f"g(x) = {data['b_str']}",
            f"operation: {data['op']} in Z_{data['p']}[x]",
            f"reduce coefficients mod {data['p']}",
            f"result = {data['r_str']}",
        ]
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the final answer.

        Args:
            data: Solution data.

        Returns:
            Result polynomial.
        """
        return data["r_str"]


# ===================================================================
# 6. CHINESE REMAINDER (RINGS) (tier 6)
# ===================================================================

@register
class ChineseRemainderRingsGenerator(StepGenerator):
    """Apply the Chinese Remainder Theorem for rings.

    Z/mnZ is isomorphic to Z/mZ x Z/nZ when gcd(m,n)=1. Maps an
    element of Z/mnZ to its pair in the product and back.

    Difficulty scaling:
        Difficulty 1-3: m, n in {2, 3, 5}.
        Difficulty 4-6: m, n in {3, 5, 7}.
        Difficulty 7-8: m, n in {5, 7, 11}.

    Prerequisites:
        modular (tier 2).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "chinese_remainder_rings"

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
            difficulty: Controls moduli size.

        Returns:
            Task description string.
        """
        return "apply CRT isomorphism Z/mnZ -> Z/mZ x Z/nZ"

    def _select_coprime_pair(self, difficulty: int) -> tuple[int, int]:
        """Select coprime m, n based on difficulty.

        Args:
            difficulty: Difficulty level 1-8.

        Returns:
            Tuple of coprime integers (m, n).
        """
        if difficulty <= 3:
            pool = [2, 3, 5]
        elif difficulty <= 6:
            pool = [3, 5, 7]
        else:
            pool = [5, 7, 11]

        m = self._rng.choice(pool)
        candidates = [p for p in pool if _gcd(m, p) == 1 and p != m]
        if not candidates:
            candidates = [p for p in [2, 3, 5, 7, 11] if _gcd(m, p) == 1 and p != m]
        n = self._rng.choice(candidates)
        return m, n

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a CRT ring isomorphism problem.

        Args:
            difficulty: Controls moduli size.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        m, n = self._select_coprime_pair(difficulty)
        mn = m * n
        a = self._rng.randint(0, mn - 1)

        a_mod_m = a % m
        a_mod_n = a % n

        problem = (
            f"CRT: Z/{mn}Z -> Z/{m}Z x Z/{n}Z. "
            f"Map {a} to its pair."
        )
        return problem, {
            "m": m, "n": n, "mn": mn, "a": a,
            "a_mod_m": a_mod_m, "a_mod_n": a_mod_n,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate CRT mapping steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing the mapping.
        """
        return [
            f"gcd({data['m']}, {data['n']}) = 1, so CRT applies",
            f"{data['a']} mod {data['m']} = {data['a_mod_m']}",
            f"{data['a']} mod {data['n']} = {data['a_mod_n']}",
            f"phi({data['a']}) = ({data['a_mod_m']}, {data['a_mod_n']})",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the final answer.

        Args:
            data: Solution data.

        Returns:
            Mapped pair.
        """
        return f"({data['a_mod_m']}, {data['a_mod_n']})"


# ===================================================================
# 7. EUCLIDEAN DOMAIN (tier 6)
# ===================================================================

@register
class EuclideanDomainGenerator(StepGenerator):
    """Perform division in the Gaussian integers Z[i].

    Given a, b in Z[i], computes q, r such that a = bq + r with
    N(r) < N(b), where N(a+bi) = a^2 + b^2.

    Difficulty scaling:
        Difficulty 1-3: small Gaussian integers with |re|, |im| <= 3.
        Difficulty 4-6: |re|, |im| <= 5.
        Difficulty 7-8: |re|, |im| <= 7.

    Prerequisites:
        gcd (tier 2).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "euclidean_domain"

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
            difficulty: Controls operand size.

        Returns:
            Task description string.
        """
        return "perform division in Gaussian integers Z[i]"

    def _norm(self, re: int, im: int) -> int:
        """Compute the norm N(a+bi) = a^2 + b^2.

        Args:
            re: Real part.
            im: Imaginary part.

        Returns:
            Norm value.
        """
        return re * re + im * im

    def _gauss_str(self, re: int, im: int) -> str:
        """Format a Gaussian integer as a string.

        Args:
            re: Real part.
            im: Imaginary part.

        Returns:
            String like ``3 + 2i``.
        """
        if im == 0:
            return str(re)
        if re == 0:
            if im == 1:
                return "i"
            if im == -1:
                return "-i"
            return f"{im}i"
        sign = "+" if im > 0 else "-"
        aim = abs(im)
        im_part = "i" if aim == 1 else f"{aim}i"
        return f"{re} {sign} {im_part}"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Gaussian integer division problem.

        Args:
            difficulty: Controls operand size.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            bound = 3
        elif difficulty <= 6:
            bound = 5
        else:
            bound = 7

        b_re = self._rng.randint(1, bound)
        b_im = self._rng.randint(0, bound)
        while self._norm(b_re, b_im) == 0:
            b_re = self._rng.randint(1, bound)

        a_re = self._rng.randint(-bound, bound)
        a_im = self._rng.randint(-bound, bound)

        nb = self._norm(b_re, b_im)
        num_re = a_re * b_re + a_im * b_im
        num_im = a_im * b_re - a_re * b_im

        q_re = round(num_re / nb)
        q_im = round(num_im / nb)

        r_re = a_re - (q_re * b_re - q_im * b_im)
        r_im = a_im - (q_re * b_im + q_im * b_re)
        nr = self._norm(r_re, r_im)

        problem = (
            f"Z[i]: divide a = {self._gauss_str(a_re, a_im)} "
            f"by b = {self._gauss_str(b_re, b_im)}"
        )
        return problem, {
            "a_re": a_re, "a_im": a_im, "b_re": b_re, "b_im": b_im,
            "q_re": q_re, "q_im": q_im, "r_re": r_re, "r_im": r_im,
            "nb": nb, "nr": nr,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Gaussian integer division steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing the division.
        """
        return [
            f"N(b) = {data['b_re']}^2 + {data['b_im']}^2 = {data['nb']}",
            f"a/b = compute and round to nearest Gaussian integer",
            f"q = {self._gauss_str(data['q_re'], data['q_im'])}",
            f"r = a - b*q = {self._gauss_str(data['r_re'], data['r_im'])}",
            f"N(r) = {data['nr']} < N(b) = {data['nb']}: "
            f"{'YES' if data['nr'] < data['nb'] else 'CHECK'}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the final answer.

        Args:
            data: Solution data.

        Returns:
            Quotient and remainder.
        """
        return (
            f"q = {self._gauss_str(data['q_re'], data['q_im'])}, "
            f"r = {self._gauss_str(data['r_re'], data['r_im'])}"
        )


# ===================================================================
# 8. FREE GROUP (tier 6)
# ===================================================================

@register
class FreeGroupGenerator(StepGenerator):
    """Reduce and multiply words in the free group F_2 = <a, b>.

    Generates two words, concatenates them, and reduces by cancelling
    adjacent inverse pairs (a*a^{-1}, b*b^{-1}, etc.).

    Difficulty scaling:
        Difficulty 1-3: words of length 2-3.
        Difficulty 4-6: words of length 3-5.
        Difficulty 7-8: words of length 5-7.

    Prerequisites:
        set_operations (tier 3).
    """

    _GENERATORS = ["a", "A", "b", "B"]  # A = a^{-1}, B = b^{-1}

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "free_group"

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
            difficulty: Controls word length.

        Returns:
            Task description string.
        """
        return "reduce word product in free group F_2 = <a, b>"

    def _inverse_letter(self, c: str) -> str:
        """Return the inverse of a generator letter.

        Args:
            c: Generator letter (a, A, b, or B).

        Returns:
            Inverse letter.
        """
        return c.swapcase()

    def _reduce(self, word: list[str]) -> list[str]:
        """Reduce a word by cancelling adjacent inverse pairs.

        Args:
            word: List of generator letters.

        Returns:
            Reduced word.
        """
        stack: list[str] = []
        for letter in word:
            if stack and stack[-1] == self._inverse_letter(letter):
                stack.pop()
            else:
                stack.append(letter)
        return stack

    def _word_str(self, word: list[str]) -> str:
        """Format a word as a readable string.

        Args:
            word: List of generator letters.

        Returns:
            String like ``a*b^{-1}*a``.
        """
        if not word:
            return "e"
        parts = []
        for c in word:
            if c == "A":
                parts.append("a^{-1}")
            elif c == "B":
                parts.append("b^{-1}")
            else:
                parts.append(c)
        return "*".join(parts)

    def _random_word(self, length: int) -> list[str]:
        """Generate a random word of given length.

        Args:
            length: Number of letters.

        Returns:
            List of generator letters.
        """
        return [self._rng.choice(self._GENERATORS) for _ in range(length)]

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a free group word reduction problem.

        Args:
            difficulty: Controls word lengths.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            len1 = self._rng.randint(2, 3)
            len2 = self._rng.randint(2, 3)
        elif difficulty <= 6:
            len1 = self._rng.randint(3, 5)
            len2 = self._rng.randint(3, 5)
        else:
            len1 = self._rng.randint(5, 7)
            len2 = self._rng.randint(5, 7)

        w1 = self._random_word(len1)
        w2 = self._random_word(len2)
        product = w1 + w2
        reduced = self._reduce(product)

        w1_str = self._word_str(w1)
        w2_str = self._word_str(w2)
        prod_str = self._word_str(product)
        red_str = self._word_str(reduced)

        problem = f"F_2: ({w1_str}) * ({w2_str}). Reduce."
        return problem, {
            "w1_str": w1_str, "w2_str": w2_str,
            "prod_str": prod_str, "red_str": red_str,
            "reduced_len": len(reduced),
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate word reduction steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing concatenation and cancellation.
        """
        return [
            f"concatenate: {data['prod_str']}",
            "cancel adjacent inverse pairs",
            f"reduced: {data['red_str']}",
            f"length: {data['reduced_len']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the final answer.

        Args:
            data: Solution data.

        Returns:
            Reduced word.
        """
        return data["red_str"]


# ===================================================================
# 9. PERMUTATION CYCLE (tier 4)
# ===================================================================

@register
class PermutationCycleGenerator(StepGenerator):
    """Convert between two-line and cycle notation for permutations.

    Given a permutation, converts to cycle notation and computes the
    order as the LCM of cycle lengths.

    Difficulty scaling:
        Difficulty 1-3: n in [3, 4].
        Difficulty 4-6: n in [4, 5].
        Difficulty 7-8: n in [5, 6].

    Prerequisites:
        permutation (tier 3).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "permutation_cycle"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["permutation"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls permutation size.

        Returns:
            Task description string.
        """
        return "convert permutation to cycle notation and compute order"

    def _select_n(self, difficulty: int) -> int:
        """Choose permutation degree.

        Args:
            difficulty: Difficulty level 1-8.

        Returns:
            Integer n.
        """
        if difficulty <= 3:
            return self._rng.choice([3, 4])
        if difficulty <= 6:
            return self._rng.choice([4, 5])
        return self._rng.choice([5, 6])

    def _to_cycles(self, perm: list[int]) -> list[list[int]]:
        """Convert permutation to cycle notation.

        Args:
            perm: Permutation where perm[i] is the image of i+1.

        Returns:
            List of cycles (each a list of 1-indexed elements).
        """
        n = len(perm)
        visited = [False] * n
        cycles = []
        for i in range(n):
            if visited[i]:
                continue
            cycle = []
            j = i
            while not visited[j]:
                visited[j] = True
                cycle.append(j + 1)
                j = perm[j] - 1
            if len(cycle) > 1:
                cycles.append(cycle)
        return cycles

    def _cycles_str(self, cycles: list[list[int]]) -> str:
        """Format cycles as a string.

        Args:
            cycles: List of cycles.

        Returns:
            String like ``(1 2 3)(4 5)`` or ``e``.
        """
        if not cycles:
            return "e"
        parts = []
        for cycle in cycles:
            parts.append("(" + " ".join(str(x) for x in cycle) + ")")
        return "".join(parts)

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a permutation cycle conversion problem.

        Args:
            difficulty: Controls permutation degree.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        n = self._select_n(difficulty)
        perm = list(range(1, n + 1))
        self._rng.shuffle(perm)

        cycles = self._to_cycles(perm)
        cycle_lengths = [len(c) for c in cycles]
        if not cycle_lengths:
            cycle_lengths = [1]

        order = cycle_lengths[0]
        for cl in cycle_lengths[1:]:
            order = _lcm(order, cl)

        two_line = " ".join(str(x) for x in range(1, n + 1))
        images = " ".join(str(x) for x in perm)
        cycle_str = self._cycles_str(cycles)

        problem = f"sigma = [{two_line} | {images}]. Write in cycles, find order."
        return problem, {
            "n": n, "perm": perm, "cycles": cycles,
            "cycle_str": cycle_str,
            "cycle_lengths": cycle_lengths, "order": order,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate cycle conversion steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing the conversion.
        """
        steps = [
            f"two-line: {' '.join(str(i) for i in range(1, data['n'] + 1))} "
            f"-> {' '.join(str(x) for x in data['perm'])}",
            f"cycle notation: {data['cycle_str']}",
            f"cycle lengths: {data['cycle_lengths']}",
            f"order = lcm({', '.join(str(cl) for cl in data['cycle_lengths'])}) "
            f"= {data['order']}",
        ]
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the final answer.

        Args:
            data: Solution data.

        Returns:
            Cycle notation and order.
        """
        return f"{data['cycle_str']}, order = {data['order']}"


# ===================================================================
# 10. AUTOMORPHISM GROUP (tier 6)
# ===================================================================

@register
class AutomorphismGroupGenerator(StepGenerator):
    """Compute Aut(Z_n) = (Z/nZ)*.

    The automorphism group of Z_n is the group of units modulo n,
    consisting of elements coprime to n under multiplication mod n.

    Difficulty scaling:
        Difficulty 1-3: n in [3, 6].
        Difficulty 4-6: n in [5, 10].
        Difficulty 7-8: n in [8, 12].

    Prerequisites:
        group_order (tier 6).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "automorphism_group"

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
            difficulty: Controls group size.

        Returns:
            Task description string.
        """
        return "compute Aut(Z_n) = (Z/nZ)* and verify group structure"

    def _select_n(self, difficulty: int) -> int:
        """Choose n based on difficulty.

        Args:
            difficulty: Difficulty level 1-8.

        Returns:
            Integer n >= 3.
        """
        if difficulty <= 3:
            return self._rng.randint(3, 6)
        if difficulty <= 6:
            return self._rng.randint(5, 10)
        return self._rng.randint(8, 12)

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an automorphism group problem.

        Args:
            difficulty: Controls n.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        n = self._select_n(difficulty)
        units = sorted([k for k in range(1, n) if _gcd(k, n) == 1])
        phi_n = len(units)

        a = self._rng.choice(units)
        b = self._rng.choice(units)
        product = (a * b) % n
        in_units = product in units

        problem = (
            f"Aut(Z_{n}): list (Z/{n}Z)*, "
            f"verify {a}*{b} mod {n} in group."
        )
        return problem, {
            "n": n, "units": units, "phi_n": phi_n,
            "a": a, "b": b, "product": product, "in_units": in_units,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate automorphism group steps.

        Args:
            data: Solution data.

        Returns:
            Steps listing units and verifying closure.
        """
        return [
            f"(Z/{data['n']}Z)* = elements coprime to {data['n']}",
            f"units = {_format_set(data['units'])}",
            f"|Aut(Z_{data['n']})| = phi({data['n']}) = {data['phi_n']}",
            f"{data['a']} * {data['b']} mod {data['n']} = {data['product']}",
            f"in group: {'YES' if data['in_units'] else 'NO'}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the final answer.

        Args:
            data: Solution data.

        Returns:
            Units and order.
        """
        return (
            f"Aut(Z_{data['n']}) = {_format_set(data['units'])}, "
            f"order = {data['phi_n']}"
        )
