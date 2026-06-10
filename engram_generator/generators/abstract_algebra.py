"""Abstract algebra generators.

12 generators covering group theory, ring theory, and field extensions
across tiers 5-6. Includes group axiom verification, subgroup tests,
coset enumeration, Lagrange's theorem, cyclic group generators, normal
subgroups, quotient groups, kernel computation, isomorphism checking,
ring ideals, field extensions, and symmetric group permutation composition.
"""
from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


# ═══════════════════════════════════════════════════════════════════
# HELPER UTILITIES
# ═══════════════════════════════════════════════════════════════════

def _format_set(elements: list[int]) -> str:
    """Format a list of integers as a set string.

    Args:
        elements: Sorted list of integers.

    Returns:
        String like ``{0, 1, 2}``.
    """
    return "{" + ", ".join(str(e) for e in elements) + "}"


def _gcd(a: int, b: int) -> int:
    """Compute greatest common divisor.

    Args:
        a: First integer.
        b: Second integer.

    Returns:
        GCD of a and b.
    """
    while b:
        a, b = b, a % b
    return a


def _is_prime(n: int) -> bool:
    """Check if n is prime.

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


def _divisors(n: int) -> list[int]:
    """Return sorted list of divisors of n.

    Args:
        n: Positive integer.

    Returns:
        Sorted list of all positive divisors.
    """
    divs = []
    for i in range(1, n + 1):
        if n % i == 0:
            divs.append(i)
    return divs


# ═══════════════════════════════════════════════════════════════════
# 1. GROUP AXIOM CHECK (tier 5)
# ═══════════════════════════════════════════════════════════════════

@register
class GroupAxiomCheckGenerator(StepGenerator):
    """Verify group axioms on a small Cayley table.

    Given Z_n under addition mod n, verifies closure, associativity,
    identity element existence, and inverse existence for randomly
    chosen test elements. Produces step-by-step verification of each
    axiom.

    Difficulty scaling:
        Difficulty 1-3: n in [3, 5].
        Difficulty 4-6: n in [4, 6].
        Difficulty 7-8: n in [5, 7].

    Prerequisites:
        group_table (tier 4).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "group_axiom_check"

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
        return "verify group axioms on Cayley table"

    def _select_n(self, difficulty: int) -> int:
        """Choose group order based on difficulty.

        Args:
            difficulty: Difficulty level 1-8.

        Returns:
            Integer n for Z_n.
        """
        if difficulty <= 3:
            return self._rng.randint(3, 5)
        if difficulty <= 6:
            return self._rng.randint(4, 6)
        return self._rng.randint(5, 7)

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a group axiom verification problem.

        Args:
            difficulty: Controls group size.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        n = self._select_n(difficulty)
        a = self._rng.randint(0, n - 1)
        b = self._rng.randint(0, n - 1)
        c = self._rng.randint(0, n - 1)

        closure = (a + b) % n
        assoc_left = ((a + b) % n + c) % n
        assoc_right = (a + (b + c) % n) % n
        identity = 0
        inv_a = (n - a) % n

        problem = f"Z_{n} under +: verify axioms for a={a}, b={b}, c={c}"
        return problem, {
            "n": n, "a": a, "b": b, "c": c,
            "closure": closure,
            "assoc_left": assoc_left, "assoc_right": assoc_right,
            "identity": identity, "inv_a": inv_a,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate axiom verification steps.

        Args:
            data: Solution data.

        Returns:
            Steps checking each axiom.
        """
        n = data["n"]
        a, b, c = data["a"], data["b"], data["c"]
        return [
            f"closure: ({a}+{b}) mod {n} = {data['closure']} in Z_{n}",
            f"assoc: (({a}+{b})+{c}) mod {n} = {data['assoc_left']}, "
            f"({a}+({b}+{c})) mod {n} = {data['assoc_right']}",
            f"identity: 0, since {a}+0 mod {n} = {a}",
            f"inverse of {a}: {data['inv_a']}, "
            f"since ({a}+{data['inv_a']}) mod {n} = 0",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the final answer.

        Args:
            data: Solution data.

        Returns:
            Confirmation that all axioms hold.
        """
        return "all axioms verified"


# ═══════════════════════════════════════════════════════════════════
# 2. SUBGROUP TEST (tier 5)
# ═══════════════════════════════════════════════════════════════════

@register
class SubgroupTestGenerator(StepGenerator):
    """Test whether a subset of Z_n forms a subgroup under addition.

    Generates a subset of Z_n and checks closure under the group
    operation and existence of inverses. The subset is chosen to be
    a valid subgroup roughly half the time.

    Difficulty scaling:
        Difficulty 1-3: n in [4, 6].
        Difficulty 4-6: n in [6, 8].
        Difficulty 7-8: n in [8, 12].

    Prerequisites:
        group_axiom_check (tier 5).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "subgroup_test"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["group_axiom_check"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls group size.

        Returns:
            Task description string.
        """
        return "test if subset is a subgroup of Z_n"

    def _select_n(self, difficulty: int) -> int:
        """Choose group order based on difficulty.

        Args:
            difficulty: Difficulty level 1-8.

        Returns:
            A composite integer n with non-trivial divisors.
        """
        if difficulty <= 3:
            return self._rng.choice([4, 6])
        if difficulty <= 6:
            return self._rng.choice([6, 8])
        return self._rng.choice([8, 10, 12])

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a subgroup test problem.

        Args:
            difficulty: Controls group size.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        n = self._select_n(difficulty)
        divs = _divisors(n)
        make_subgroup = self._rng.random() < 0.5

        if make_subgroup and len(divs) > 2:
            d = self._rng.choice([d for d in divs if 1 < d < n])
            subset = sorted([i * d % n for i in range(n // d)])
        else:
            size = self._rng.randint(2, max(2, n // 2))
            subset = sorted(self._rng.sample(range(n), size))
            if 0 not in subset:
                subset[0] = 0
                subset.sort()

        closed = True
        has_inverses = True
        for x in subset:
            inv = (n - x) % n
            if inv not in subset:
                has_inverses = False
                break
        if has_inverses:
            for x in subset:
                for y in subset:
                    if (x + y) % n not in subset:
                        closed = False
                        break
                if not closed:
                    break
        is_subgroup = closed and has_inverses

        s_str = _format_set(subset)
        problem = f"H={s_str} subset of Z_{n} under +. Is H a subgroup?"
        return problem, {
            "n": n, "subset": subset, "is_subgroup": is_subgroup,
            "closed": closed, "has_inverses": has_inverses,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate subgroup test steps.

        Args:
            data: Solution data.

        Returns:
            Steps checking identity, closure, and inverses.
        """
        n = data["n"]
        subset = data["subset"]
        steps = [f"identity: 0 {'in' if 0 in subset else 'not in'} H"]
        if data["has_inverses"]:
            steps.append("all inverses present in H")
        else:
            for x in subset:
                if (n - x) % n not in subset:
                    steps.append(f"inv({x})={(n - x) % n} not in H")
                    break
        if data["closed"]:
            steps.append("closed under + mod " + str(n))
        else:
            steps.append("not closed under + mod " + str(n))
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the final answer.

        Args:
            data: Solution data.

        Returns:
            YES or NO.
        """
        return "YES" if data["is_subgroup"] else "NO"


# ═══════════════════════════════════════════════════════════════════
# 3. COSET ENUMERATE (tier 5)
# ═══════════════════════════════════════════════════════════════════

@register
class CosetEnumerateGenerator(StepGenerator):
    """Enumerate all left cosets of a subgroup H in Z_n.

    Given a proper subgroup H of Z_n under addition, computes all
    distinct left cosets a + H = {(a + h) mod n : h in H}.

    Difficulty scaling:
        Difficulty 1-3: n in [4, 6], small subgroups.
        Difficulty 4-6: n in [6, 9].
        Difficulty 7-8: n in [8, 12].

    Prerequisites:
        subgroup_test (tier 5).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "coset_enumerate"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["subgroup_test"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls group size.

        Returns:
            Task description string.
        """
        return "enumerate left cosets of subgroup"

    def _select_n(self, difficulty: int) -> int:
        """Choose group order with a non-trivial proper subgroup.

        Args:
            difficulty: Difficulty level 1-8.

        Returns:
            Composite integer n.
        """
        if difficulty <= 3:
            return self._rng.choice([4, 6])
        if difficulty <= 6:
            return self._rng.choice([6, 8, 9])
        return self._rng.choice([8, 10, 12])

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a coset enumeration problem.

        Args:
            difficulty: Controls group size.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        n = self._select_n(difficulty)
        proper_divs = [d for d in _divisors(n) if 1 < d < n]
        d = self._rng.choice(proper_divs)
        h = sorted([(i * d) % n for i in range(n // d)])

        cosets = []
        seen = set()
        for a in range(n):
            coset = tuple(sorted([(a + hh) % n for hh in h]))
            if coset not in seen:
                seen.add(coset)
                cosets.append((a, list(coset)))

        h_str = _format_set(h)
        problem = f"Z_{n}, H={h_str}. List all left cosets a+H."
        return problem, {
            "n": n, "h": h, "cosets": cosets, "num_cosets": len(cosets),
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate coset enumeration steps.

        Args:
            data: Solution data.

        Returns:
            Steps listing each distinct coset.
        """
        steps = []
        for rep, coset in data["cosets"]:
            steps.append(f"{rep}+H = {_format_set(coset)}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the final answer.

        Args:
            data: Solution data.

        Returns:
            Number of distinct cosets.
        """
        parts = []
        for _, coset in data["cosets"]:
            parts.append(_format_set(coset))
        return "; ".join(parts)


# ═══════════════════════════════════════════════════════════════════
# 4. LAGRANGE VERIFY (tier 5)
# ═══════════════════════════════════════════════════════════════════

@register
class LagrangeVerifyGenerator(StepGenerator):
    """Verify Lagrange's theorem for a subgroup of Z_n.

    Given G = Z_n and a subgroup H, verifies that |H| divides |G|
    and computes the index [G:H] = |G|/|H|.

    Difficulty scaling:
        Difficulty 1-3: n in [4, 6].
        Difficulty 4-6: n in [6, 10].
        Difficulty 7-8: n in [8, 12].

    Prerequisites:
        coset_enumerate (tier 5).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "lagrange_verify"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["coset_enumerate"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls group size.

        Returns:
            Task description string.
        """
        return "verify Lagrange's theorem for subgroup"

    def _select_n(self, difficulty: int) -> int:
        """Choose group order based on difficulty.

        Args:
            difficulty: Difficulty level 1-8.

        Returns:
            Composite integer n.
        """
        if difficulty <= 3:
            return self._rng.choice([4, 6])
        if difficulty <= 6:
            return self._rng.choice([6, 8, 10])
        return self._rng.choice([8, 10, 12])

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Lagrange's theorem verification problem.

        Args:
            difficulty: Controls group size.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        n = self._select_n(difficulty)
        proper_divs = [d for d in _divisors(n) if 1 < d < n]
        d = self._rng.choice(proper_divs)
        h_size = n // d
        h = sorted([(i * d) % n for i in range(h_size)])

        divides = (n % h_size == 0)
        index = n // h_size

        h_str = _format_set(h)
        problem = (
            f"G=Z_{n}, H={h_str}. "
            f"Verify |H| divides |G| and find [G:H]."
        )
        return problem, {
            "n": n, "h": h, "h_size": h_size,
            "divides": divides, "index": index,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Lagrange verification steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing |G|, |H|, divisibility, and index.
        """
        return [
            f"|G| = {data['n']}",
            f"|H| = {data['h_size']}",
            f"{data['n']} / {data['h_size']} = {data['index']} "
            f"({'divides' if data['divides'] else 'does not divide'})",
            f"[G:H] = {data['index']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the final answer.

        Args:
            data: Solution data.

        Returns:
            Index value.
        """
        return f"|H|={data['h_size']} divides |G|={data['n']}, [G:H]={data['index']}"


# ═══════════════════════════════════════════════════════════════════
# 5. CYCLIC GROUP GENERATOR (tier 6)
# ═══════════════════════════════════════════════════════════════════

@register
class CyclicGroupGenGenerator(StepGenerator):
    """Find a generator of the cyclic group Z_n.

    Given Z_n under addition, finds an element g whose multiples
    produce all elements of the group. An element g generates Z_n
    if and only if gcd(g, n) = 1.

    Difficulty scaling:
        Difficulty 1-3: n in [3, 7].
        Difficulty 4-6: n in [5, 10].
        Difficulty 7-8: n in [7, 12].

    Prerequisites:
        group_order (tier 6).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "cyclic_group_gen"

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
        return "find generator of cyclic group Z_n"

    def _select_n(self, difficulty: int) -> int:
        """Choose group order based on difficulty.

        Args:
            difficulty: Difficulty level 1-8.

        Returns:
            Integer n >= 3.
        """
        if difficulty <= 3:
            return self._rng.randint(3, 7)
        if difficulty <= 6:
            return self._rng.randint(5, 10)
        return self._rng.randint(7, 12)

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a cyclic group generator problem.

        Args:
            difficulty: Controls group size.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        n = self._select_n(difficulty)
        g = self._rng.randint(1, n - 1)
        multiples = [(i, (i * g) % n) for i in range(1, n + 1)]
        generated = sorted(set(m for _, m in multiples))
        is_generator = (len(generated) == n)
        all_generators = sorted([x for x in range(1, n) if _gcd(x, n) == 1])

        problem = f"Z_{n} under +: is g={g} a generator? List all generators."
        return problem, {
            "n": n, "g": g, "multiples": multiples,
            "generated": generated, "is_generator": is_generator,
            "all_generators": all_generators,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate cyclic group steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing multiples and generator status.
        """
        n = data["n"]
        g = data["g"]
        mult_strs = []
        for i, val in data["multiples"][:n]:
            mult_strs.append(f"{i}*{g}={val}")
        steps = [
            "multiples: " + ", ".join(mult_strs[:min(6, len(mult_strs))]),
            f"generated set: {_format_set(data['generated'])}",
            f"gcd({g},{n})={_gcd(g, n)}, "
            f"{'is' if data['is_generator'] else 'not'} a generator",
        ]
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the final answer.

        Args:
            data: Solution data.

        Returns:
            Whether g is a generator and list of all generators.
        """
        status = "YES" if data["is_generator"] else "NO"
        gens = _format_set(data["all_generators"])
        return f"{status}, generators={gens}"


# ═══════════════════════════════════════════════════════════════════
# 6. NORMAL SUBGROUP (tier 6)
# ═══════════════════════════════════════════════════════════════════

@register
class NormalSubgroupGenerator(StepGenerator):
    """Check if a subgroup is normal in Z_n.

    In an abelian group like Z_n every subgroup is normal. This
    generator verifies normality by showing that left cosets equal
    right cosets for all elements.

    Difficulty scaling:
        Difficulty 1-3: n in [4, 6].
        Difficulty 4-6: n in [6, 9].
        Difficulty 7-8: n in [8, 12].

    Prerequisites:
        coset_enumerate (tier 5).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "normal_subgroup"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["coset_enumerate"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls group size.

        Returns:
            Task description string.
        """
        return "check if subgroup is normal"

    def _select_n(self, difficulty: int) -> int:
        """Choose group order based on difficulty.

        Args:
            difficulty: Difficulty level 1-8.

        Returns:
            Composite integer n.
        """
        if difficulty <= 3:
            return self._rng.choice([4, 6])
        if difficulty <= 6:
            return self._rng.choice([6, 8, 9])
        return self._rng.choice([8, 10, 12])

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a normal subgroup check problem.

        Args:
            difficulty: Controls group size.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        n = self._select_n(difficulty)
        proper_divs = [d for d in _divisors(n) if 1 < d < n]
        d = self._rng.choice(proper_divs)
        h = sorted([(i * d) % n for i in range(n // d)])

        test_a = self._rng.randint(1, n - 1)
        left_coset = sorted([(test_a + hh) % n for hh in h])
        right_coset = sorted([(hh + test_a) % n for hh in h])
        is_normal = (left_coset == right_coset)

        h_str = _format_set(h)
        problem = (
            f"Z_{n}, H={h_str}. "
            f"Is H normal? Check a={test_a}."
        )
        return problem, {
            "n": n, "h": h, "test_a": test_a,
            "left_coset": left_coset, "right_coset": right_coset,
            "is_normal": is_normal,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate normal subgroup check steps.

        Args:
            data: Solution data.

        Returns:
            Steps comparing left and right cosets.
        """
        a = data["test_a"]
        return [
            f"left coset {a}+H = {_format_set(data['left_coset'])}",
            f"right coset H+{a} = {_format_set(data['right_coset'])}",
            f"Z_{data['n']} is abelian, so all subgroups are normal",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the final answer.

        Args:
            data: Solution data.

        Returns:
            YES (always, since Z_n is abelian).
        """
        return "YES (abelian group, all subgroups normal)"


# ═══════════════════════════════════════════════════════════════════
# 7. QUOTIENT GROUP (tier 6)
# ═══════════════════════════════════════════════════════════════════

@register
class QuotientGroupGenerator(StepGenerator):
    """Compute the multiplication table of G/N for a normal subgroup.

    Given Z_n and a normal subgroup N, computes the cosets of N and
    builds the Cayley table of the quotient group Z_n / N, which is
    isomorphic to Z_{n/|N|}.

    Difficulty scaling:
        Difficulty 1-3: n in [4, 6].
        Difficulty 4-6: n in [6, 8].
        Difficulty 7-8: n in [8, 12].

    Prerequisites:
        normal_subgroup (tier 6).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "quotient_group"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["normal_subgroup"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls group size.

        Returns:
            Task description string.
        """
        return "compute quotient group table"

    def _select_n(self, difficulty: int) -> int:
        """Choose group order based on difficulty.

        Args:
            difficulty: Difficulty level 1-8.

        Returns:
            Composite integer n.
        """
        if difficulty <= 3:
            return self._rng.choice([4, 6])
        if difficulty <= 6:
            return self._rng.choice([6, 8])
        return self._rng.choice([8, 10, 12])

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a quotient group table problem.

        Args:
            difficulty: Controls group size.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        n = self._select_n(difficulty)
        proper_divs = [d for d in _divisors(n) if 1 < d < n]
        d = self._rng.choice(proper_divs)
        h_size = n // d
        h = sorted([(i * d) % n for i in range(h_size)])

        cosets = []
        seen = set()
        reps = []
        for a in range(n):
            coset = tuple(sorted([(a + hh) % n for hh in h]))
            if coset not in seen:
                seen.add(coset)
                cosets.append(list(coset))
                reps.append(a)

        num_cosets = len(cosets)
        table = []
        for i in range(num_cosets):
            row = []
            for j in range(num_cosets):
                sum_rep = (reps[i] + reps[j]) % n
                for k in range(num_cosets):
                    if sum_rep in cosets[k]:
                        row.append(k)
                        break
            table.append(row)

        h_str = _format_set(h)
        problem = f"Z_{n}/N where N={h_str}. Compute the Cayley table."
        return problem, {
            "n": n, "h": h, "reps": reps, "cosets": cosets,
            "table": table, "num_cosets": num_cosets,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate quotient group table steps.

        Args:
            data: Solution data.

        Returns:
            Steps listing cosets and table entries.
        """
        steps = []
        for i, (rep, coset) in enumerate(zip(data["reps"], data["cosets"])):
            steps.append(f"C{i}={_format_set(coset)} (rep {rep})")
        table_rows = []
        for i, row in enumerate(data["table"]):
            table_rows.append(
                f"C{i}: " + " ".join(f"C{v}" for v in row)
            )
        steps.append("table: " + "; ".join(table_rows))
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the final answer.

        Args:
            data: Solution data.

        Returns:
            Quotient group isomorphism type.
        """
        k = data["num_cosets"]
        return f"Z_{data['n']}/N ~ Z_{k}, order {k}"


# ═══════════════════════════════════════════════════════════════════
# 8. KERNEL COMPUTE (tier 6)
# ═══════════════════════════════════════════════════════════════════

@register
class KernelComputeGenerator(StepGenerator):
    """Compute the kernel of a group homomorphism phi: Z_n -> Z_m.

    Given phi(x) = (k*x) mod m for a valid multiplier k, finds all
    elements x in Z_n that map to 0 in Z_m.

    Difficulty scaling:
        Difficulty 1-3: n in [4, 6], m in [2, 3].
        Difficulty 4-6: n in [6, 10], m in [2, 5].
        Difficulty 7-8: n in [8, 12], m in [3, 6].

    Prerequisites:
        group_homomorphism (tier 6).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "kernel_compute"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["group_homomorphism"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls group sizes.

        Returns:
            Task description string.
        """
        return "compute kernel of group homomorphism"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a kernel computation problem.

        Args:
            difficulty: Controls domain and codomain sizes.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            n = self._rng.randint(4, 6)
            m = self._rng.choice([2, 3])
        elif difficulty <= 6:
            n = self._rng.randint(6, 10)
            m = self._rng.choice([2, 3, 4, 5])
        else:
            n = self._rng.randint(8, 12)
            m = self._rng.choice([3, 4, 5, 6])

        k = self._rng.randint(1, m - 1)

        image = [(k * x) % m for x in range(n)]
        kernel = sorted([x for x in range(n) if image[x] == 0])

        problem = (
            f"phi: Z_{n} -> Z_{m}, phi(x) = {k}x mod {m}. "
            f"Find ker(phi)."
        )
        return problem, {
            "n": n, "m": m, "k": k, "image": image, "kernel": kernel,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate kernel computation steps.

        Args:
            data: Solution data.

        Returns:
            Steps evaluating phi at each element.
        """
        k, m = data["k"], data["m"]
        eval_strs = []
        for x in range(data["n"]):
            val = data["image"][x]
            eval_strs.append(f"phi({x})={val}")
        steps = [
            "evaluate: " + ", ".join(eval_strs[:8]),
            f"ker = elements mapping to 0",
        ]
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the final answer.

        Args:
            data: Solution data.

        Returns:
            The kernel as a set.
        """
        return f"ker(phi) = {_format_set(data['kernel'])}"


# ═══════════════════════════════════════════════════════════════════
# 9. ISOMORPHISM CHECK (tier 6)
# ═══════════════════════════════════════════════════════════════════

@register
class IsomorphismCheckGenerator(StepGenerator):
    """Determine if two small groups are isomorphic.

    Constructs two groups of the same order (both Z_n under addition
    mod n but with relabelled elements) and checks whether a
    bijection preserving the operation exists.

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
        return "isomorphism_check"

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
        return "check if two groups are isomorphic"

    def _select_n(self, difficulty: int) -> int:
        """Choose group order based on difficulty.

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

    def _build_table(self, n: int, perm: list[int]) -> list[list[int]]:
        """Build a Cayley table with relabelled elements.

        Args:
            n: Group order.
            perm: Permutation mapping original labels to new labels.

        Returns:
            n x n table where entry [i][j] = perm[(inv_perm[i]+inv_perm[j]) mod n].
        """
        inv_perm = [0] * n
        for i, p in enumerate(perm):
            inv_perm[p] = i
        table = []
        for i in range(n):
            row = []
            for j in range(n):
                row.append(perm[(inv_perm[i] + inv_perm[j]) % n])
            table.append(row)
        return table

    def _table_str(self, table: list[list[int]]) -> str:
        """Format a Cayley table compactly.

        Args:
            table: 2D list of integers.

        Returns:
            Compact string representation.
        """
        rows = []
        for row in table:
            rows.append(" ".join(str(x) for x in row))
        return " | ".join(rows)

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an isomorphism check problem.

        Args:
            difficulty: Controls group size.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        n = self._select_n(difficulty)
        identity_perm = list(range(n))
        table_a = self._build_table(n, identity_perm)

        perm_b = list(range(n))
        self._rng.shuffle(perm_b)
        table_b = self._build_table(n, perm_b)

        is_iso = True
        bijection = perm_b

        ta_str = self._table_str(table_a)
        tb_str = self._table_str(table_b)
        problem = f"G1 table: [{ta_str}], G2 table: [{tb_str}]. Isomorphic?"
        return problem, {
            "n": n, "table_a": table_a, "table_b": table_b,
            "is_iso": is_iso, "bijection": bijection,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate isomorphism check steps.

        Args:
            data: Solution data.

        Returns:
            Steps comparing orders and structure.
        """
        n = data["n"]
        bij = data["bijection"]
        mapping = ", ".join(f"{i}->{bij[i]}" for i in range(n))
        steps = [
            f"|G1| = |G2| = {n}",
            f"both cyclic of order {n}",
            f"bijection: {mapping}",
        ]
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the final answer.

        Args:
            data: Solution data.

        Returns:
            YES or NO with bijection.
        """
        bij = data["bijection"]
        mapping = ", ".join(f"{i}->{bij[i]}" for i in range(data["n"]))
        return f"YES, map: {mapping}"


# ═══════════════════════════════════════════════════════════════════
# 10. RING IDEAL CHECK (tier 6)
# ═══════════════════════════════════════════════════════════════════

@register
class RingIdealCheckGenerator(StepGenerator):
    """Verify if a subset of Z_n forms an ideal.

    An ideal I of Z_n must be closed under addition mod n, contain
    additive inverses, and satisfy the absorption property: for all
    r in Z_n and a in I, r*a mod n is in I.

    Difficulty scaling:
        Difficulty 1-3: n in [4, 6].
        Difficulty 4-6: n in [6, 9].
        Difficulty 7-8: n in [8, 12].

    Prerequisites:
        ring_arithmetic (tier 5).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "ring_ideal_check"

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
            difficulty: Controls ring size.

        Returns:
            Task description string.
        """
        return "check if subset is an ideal of Z_n"

    def _select_n(self, difficulty: int) -> int:
        """Choose ring order based on difficulty.

        Args:
            difficulty: Difficulty level 1-8.

        Returns:
            Composite integer n.
        """
        if difficulty <= 3:
            return self._rng.choice([4, 6])
        if difficulty <= 6:
            return self._rng.choice([6, 8, 9])
        return self._rng.choice([8, 10, 12])

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a ring ideal check problem.

        Args:
            difficulty: Controls ring size.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        n = self._select_n(difficulty)
        make_ideal = self._rng.random() < 0.5

        if make_ideal:
            proper_divs = [d for d in _divisors(n) if 1 < d < n]
            if proper_divs:
                d = self._rng.choice(proper_divs)
                subset = sorted([i * d for i in range(n // d)])
            else:
                subset = [0]
        else:
            size = self._rng.randint(2, max(2, n // 2))
            subset = sorted(self._rng.sample(range(n), size))
            if 0 not in subset:
                subset[0] = 0
                subset.sort()

        add_closed = True
        for a in subset:
            for b in subset:
                if (a + b) % n not in subset:
                    add_closed = False
                    break
            if not add_closed:
                break

        absorbs = True
        for r in range(n):
            for a in subset:
                if (r * a) % n not in subset:
                    absorbs = False
                    break
            if not absorbs:
                break

        is_ideal = add_closed and absorbs

        s_str = _format_set(subset)
        problem = f"Z_{n}: is I={s_str} an ideal?"
        return problem, {
            "n": n, "subset": subset, "is_ideal": is_ideal,
            "add_closed": add_closed, "absorbs": absorbs,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate ideal check steps.

        Args:
            data: Solution data.

        Returns:
            Steps checking closure and absorption.
        """
        steps = [
            f"additive closure: {'YES' if data['add_closed'] else 'NO'}",
            f"absorption (r*a in I for all r): "
            f"{'YES' if data['absorbs'] else 'NO'}",
        ]
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the final answer.

        Args:
            data: Solution data.

        Returns:
            YES or NO.
        """
        return "YES" if data["is_ideal"] else "NO"


# ═══════════════════════════════════════════════════════════════════
# 11. FIELD EXTENSION (tier 6)
# ═══════════════════════════════════════════════════════════════════

@register
class FieldExtensionGenerator(StepGenerator):
    """Determine if a polynomial over Z_p is irreducible.

    Tests a polynomial f(x) over a prime field Z_p by evaluating
    f(a) for all a in Z_p. If f has no roots, it is irreducible
    (for degree <= 3).

    Difficulty scaling:
        Difficulty 1-3: degree 2, p in [2, 3, 5].
        Difficulty 4-6: degree 2-3, p in [3, 5, 7].
        Difficulty 7-8: degree 2-3, p in [5, 7, 11].

    Prerequisites:
        polynomial_division (tier 5).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "field_extension"

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
            difficulty: Controls polynomial complexity.

        Returns:
            Task description string.
        """
        return "check if polynomial is irreducible over Z_p"

    def _select_params(self, difficulty: int) -> tuple[int, int]:
        """Choose polynomial degree and field characteristic.

        Args:
            difficulty: Difficulty level 1-8.

        Returns:
            Tuple of (degree, prime p).
        """
        if difficulty <= 3:
            deg = 2
            p = self._rng.choice([2, 3, 5])
        elif difficulty <= 6:
            deg = self._rng.choice([2, 3])
            p = self._rng.choice([3, 5, 7])
        else:
            deg = self._rng.choice([2, 3])
            p = self._rng.choice([5, 7, 11])
        return deg, p

    def _poly_str(self, coeffs: list[int]) -> str:
        """Format polynomial coefficients as a LaTeX string.

        Args:
            coeffs: Coefficients from highest to lowest degree.

        Returns:
            LaTeX polynomial string.
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
                if c == 1:
                    parts.append("x")
                else:
                    parts.append(f"{c}x")
            else:
                if c == 1:
                    parts.append(f"x^{power}")
                else:
                    parts.append(f"{c}x^{power}")
        return " + ".join(parts) if parts else "0"

    def _eval_poly(self, coeffs: list[int], x: int, p: int) -> int:
        """Evaluate polynomial at x modulo p using Horner's method.

        Args:
            coeffs: Coefficients from highest to lowest degree.
            x: Point of evaluation.
            p: Prime modulus.

        Returns:
            f(x) mod p.
        """
        result = 0
        for c in coeffs:
            result = (result * x + c) % p
        return result

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an irreducibility test problem.

        Args:
            difficulty: Controls degree and field size.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        deg, p = self._select_params(difficulty)
        coeffs = [1]
        for _ in range(deg):
            coeffs.append(self._rng.randint(0, p - 1))
        if coeffs[-1] == 0:
            coeffs[-1] = self._rng.randint(1, p - 1)

        evals = {}
        roots = []
        for a in range(p):
            val = self._eval_poly(coeffs, a, p)
            evals[a] = val
            if val == 0:
                roots.append(a)

        irreducible = len(roots) == 0

        poly = self._poly_str(coeffs)
        problem = f"f(x) = {poly} over Z_{p}. Is f irreducible?"
        return problem, {
            "p": p, "deg": deg, "coeffs": coeffs, "poly": poly,
            "evals": evals, "roots": roots, "irreducible": irreducible,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate irreducibility test steps.

        Args:
            data: Solution data.

        Returns:
            Steps evaluating f at each element of Z_p.
        """
        p = data["p"]
        eval_strs = []
        for a in range(min(p, 8)):
            eval_strs.append(f"f({a})={data['evals'][a]}")
        steps = [
            "evaluate at all elements: " + ", ".join(eval_strs),
        ]
        if data["roots"]:
            steps.append(f"roots found: {_format_set(data['roots'])}")
        else:
            steps.append("no roots in Z_" + str(p))
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the final answer.

        Args:
            data: Solution data.

        Returns:
            YES (irreducible) or NO (reducible) with roots.
        """
        if data["irreducible"]:
            return "YES, irreducible over Z_" + str(data["p"])
        roots_str = _format_set(data["roots"])
        return f"NO, roots: {roots_str}"


# ═══════════════════════════════════════════════════════════════════
# 12. SYMMETRIC GROUP (tier 5)
# ═══════════════════════════════════════════════════════════════════

@register
class SymmetricGroupGenerator(StepGenerator):
    """Compose two permutations in S_n using cycle notation.

    Given two permutations of {1, ..., n} in cycle notation,
    computes their composition (right-to-left application) and
    expresses the result in cycle notation.

    Difficulty scaling:
        Difficulty 1-3: n = 3 or 4.
        Difficulty 4-6: n = 4 or 5.
        Difficulty 7-8: n = 5 or 6.

    Prerequisites:
        permutation (tier 3).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "symmetric_group"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

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
        return "compose permutations in cycle notation"

    def _select_n(self, difficulty: int) -> int:
        """Choose permutation degree based on difficulty.

        Args:
            difficulty: Difficulty level 1-8.

        Returns:
            Integer n in [3, 6].
        """
        if difficulty <= 3:
            return self._rng.choice([3, 4])
        if difficulty <= 6:
            return self._rng.choice([4, 5])
        return self._rng.choice([5, 6])

    def _random_permutation(self, n: int) -> list[int]:
        """Generate a random permutation of {1, ..., n}.

        Args:
            n: Degree of the symmetric group.

        Returns:
            List where result[i] is the image of i+1 (0-indexed storage).
        """
        perm = list(range(1, n + 1))
        self._rng.shuffle(perm)
        return perm

    def _to_cycles(self, perm: list[int]) -> list[list[int]]:
        """Convert a permutation (1-indexed images) to cycle notation.

        Args:
            perm: List where perm[i] is the image of i+1.

        Returns:
            List of cycles, each a list of elements. Fixed points omitted.
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
            String like ``(1 2 3)(4 5)`` or ``e`` for identity.
        """
        if not cycles:
            return "e"
        parts = []
        for cycle in cycles:
            parts.append("(" + " ".join(str(x) for x in cycle) + ")")
        return "".join(parts)

    def _compose(self, sigma: list[int], tau: list[int]) -> list[int]:
        """Compose two permutations: result = sigma . tau (apply tau first).

        Args:
            sigma: First permutation (applied second).
            tau: Second permutation (applied first).

        Returns:
            Composed permutation as a list.
        """
        n = len(sigma)
        return [sigma[tau[i] - 1] for i in range(n)]

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a permutation composition problem.

        Args:
            difficulty: Controls permutation degree.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        n = self._select_n(difficulty)
        sigma = self._random_permutation(n)
        tau = self._random_permutation(n)
        composed = self._compose(sigma, tau)

        sigma_cycles = self._to_cycles(sigma)
        tau_cycles = self._to_cycles(tau)
        result_cycles = self._to_cycles(composed)

        sigma_str = self._cycles_str(sigma_cycles)
        tau_str = self._cycles_str(tau_cycles)
        result_str = self._cycles_str(result_cycles)

        problem = (
            f"S_{n}: sigma={sigma_str}, tau={tau_str}. "
            f"Compute sigma . tau."
        )
        return problem, {
            "n": n, "sigma": sigma, "tau": tau, "composed": composed,
            "sigma_str": sigma_str, "tau_str": tau_str,
            "result_str": result_str, "result_cycles": result_cycles,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate permutation composition steps.

        Args:
            data: Solution data.

        Returns:
            Steps tracing each element through both permutations.
        """
        n = data["n"]
        tau = data["tau"]
        sigma = data["sigma"]
        trace_parts = []
        for i in range(1, n + 1):
            mid = tau[i - 1]
            final = sigma[mid - 1]
            trace_parts.append(f"{i}->{mid}->{final}")
        steps = [
            f"apply tau then sigma: " + ", ".join(trace_parts),
            f"result: {data['result_str']}",
        ]
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the final answer.

        Args:
            data: Solution data.

        Returns:
            Composed permutation in cycle notation.
        """
        return data["result_str"]
