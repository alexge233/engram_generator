"""Deep logic generators -- set theory, forcing, ordinals, large cardinals.

8 generators at tiers 5-7 covering ordinal arithmetic, cardinal arithmetic,
axiom of choice applications, transfinite induction, set cardinality proofs,
well-ordering, Boolean algebra lattices, and ZFC axiom application.
"""
from __future__ import annotations

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

# Ordinal representation as strings for template-based generation
_ORDINAL_EXPRESSIONS = {
    "basic": [
        ("omega+1", "omega+1"),
        ("omega+2", "omega+2"),
        ("omega+omega", "omega*2"),
        ("omega*2+1", "omega*2+1"),
        ("omega*3", "omega*3"),
    ],
    "intermediate": [
        ("omega^2", "omega^2"),
        ("omega^2+omega", "omega^2+omega"),
        ("omega^2+1", "omega^2+1"),
        ("omega^omega", "omega^omega"),
    ],
    "advanced": [
        ("omega^(omega^omega)", "omega^(omega^omega)"),
        ("epsilon_0", "epsilon_0"),
    ],
}

# Cardinal expressions for template-based generation
_CARDINAL_FACTS = [
    ("aleph_0+aleph_0", "aleph_0", "countable union of countable = countable"),
    ("aleph_0*aleph_0", "aleph_0", "N x N is countable (Cantor pairing)"),
    ("aleph_0+n", "aleph_0", "finite + countable = countable"),
    ("n*aleph_0", "aleph_0", "finite copies of countable = countable"),
    ("2^aleph_0", "c", "Cantor's theorem: |P(N)| = |R| = c"),
    ("aleph_0^aleph_0", "c", "N^N has cardinality c"),
    ("c+c", "c", "continuum + continuum = continuum"),
    ("c*c", "c", "R x R has cardinality c"),
    ("c+aleph_0", "c", "continuum absorbs countable"),
]

# Zorn's lemma applications
_ZORNS_APPLICATIONS = [
    (
        "every vector space has a basis",
        "chains of linearly independent sets have upper bounds (their union)",
        "maximal linearly independent set = basis",
    ),
    (
        "every proper ideal is contained in a maximal ideal",
        "chains of proper ideals have upper bounds (their union is proper)",
        "maximal element = maximal ideal",
    ),
    (
        "every filter extends to an ultrafilter",
        "chains of filters have upper bounds (their union is a filter)",
        "maximal element = ultrafilter",
    ),
]

# ZFC axiom templates
_ZFC_AXIOMS = [
    ("pairing", "For any a, b: {a, b} exists",
     "given a={a}, b={b}: construct {{{a}, {b}}}"),
    ("union", "For any set A: union(A) exists",
     "given A={{{inner}}}: union(A)={union_result}"),
    ("power_set", "For any set A: P(A) exists",
     "given A={a_set}: P(A)={power_result}"),
    ("separation", "For any set A and property P: {x in A : P(x)} exists",
     "given A={a_set}, P(x): {filtered}"),
]


def _power_set(s: frozenset) -> list[frozenset]:
    """Compute the power set of a frozenset.

    Args:
        s: Input set.

    Returns:
        List of all subsets as frozensets.
    """
    elements = list(s)
    result = []
    for i in range(1 << len(elements)):
        subset = frozenset(elements[j] for j in range(len(elements)) if i & (1 << j))
        result.append(subset)
    return sorted(result, key=lambda x: (len(x), sorted(x)))


def _format_set(s: frozenset | set) -> str:
    """Format a set as a readable string.

    Args:
        s: Set to format.

    Returns:
        String representation.
    """
    if not s:
        return "{}"
    return "{" + ", ".join(str(x) for x in sorted(s)) + "}"


# ---------------------------------------------------------------------------
# 1. Ordinal Arithmetic (tier 6)
# ---------------------------------------------------------------------------

@register
class OrdinalArithmeticGenerator(StepGenerator):
    """Compute ordinal arithmetic expressions.

    Demonstrates non-commutativity: omega+1 != 1+omega.
    omega*2 = omega+omega. Template-based with known results.

    Difficulty scaling:
        d1-2: basic ordinal addition (omega+finite).
        d3-4: ordinal multiplication (omega*finite).
        d5-6: ordinal exponentiation and non-commutativity.
        d7-8: compound expressions with omega^2.

    Prerequisites:
        comparison.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "ordinal_arithmetic"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["comparison"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute ordinal arithmetic expression"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an ordinal arithmetic problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 2:
            n = self._rng.randint(1, 5)
            templates = [
                (f"\\omega+{n}", f"omega+{n}",
                 f"omega+{n}: adjoin {n} after omega",
                 f"omega+{n} (limit ordinal + finite)"),
                (f"{n}+\\omega", "omega",
                 f"{n}+omega = omega: finite absorbed on left",
                 "omega (left absorption)"),
            ]
        elif difficulty <= 4:
            n = self._rng.randint(2, 4)
            templates = [
                (f"\\omega \\cdot {n}", f"omega*{n}",
                 f"omega*{n} = {'omega+' * (n - 1)}omega",
                 f"omega*{n} ({n} copies of omega)"),
                (f"{n} \\cdot \\omega", "omega",
                 f"{n}*omega = omega: left multiplication by finite",
                 "omega (left multiplication absorbed)"),
            ]
        elif difficulty <= 6:
            templates = [
                ("\\omega+1 \\neq 1+\\omega", "omega+1 != omega",
                 "omega+1 has a max element; 1+omega=omega does not",
                 "omega+1 != 1+omega (non-commutative)"),
                ("\\omega \\cdot 2", "omega*2",
                 "omega*2 = omega+omega: two copies of omega",
                 "omega*2 = omega+omega"),
                ("\\omega^2", "omega^2",
                 "omega^2 = omega*omega: omega copies of omega",
                 "omega^2 = sup{omega*n : n < omega}"),
            ]
        else:
            n = self._rng.randint(1, 3)
            templates = [
                (f"\\omega^2+\\omega+{n}", f"omega^2+omega+{n}",
                 "Cantor normal form: omega^2 + omega + finite",
                 f"omega^2+omega+{n} (Cantor NF)"),
                ("\\omega^\\omega", "omega^omega",
                 "omega^omega = sup{omega^n : n < omega}",
                 "omega^omega (tower)"),
            ]

        expr, result, explanation, summary = self._rng.choice(templates)
        problem = f"compute: {expr}"
        return problem, {
            "expr": expr, "result": result,
            "explanation": explanation, "summary": summary,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing ordinal computation.
        """
        return [
            f"expression: {data['expr']}",
            data["explanation"],
            f"result: {data['result']}",
            data["summary"],
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the ordinal result.

        Args:
            data: Solution data dict.

        Returns:
            Result as string.
        """
        return data["result"]


# ---------------------------------------------------------------------------
# 2. Cardinal Arithmetic (tier 6)
# ---------------------------------------------------------------------------

@register
class CardinalArithmeticGenerator(StepGenerator):
    """Compute cardinal arithmetic expressions.

    aleph_0 + aleph_0 = aleph_0, aleph_0 * aleph_0 = aleph_0,
    2^aleph_0 = c (continuum). Template-based with justifications.

    Difficulty scaling:
        d1-2: basic countable operations.
        d3-4: products and powers.
        d5-6: continuum operations.
        d7-8: mixed expressions.

    Prerequisites:
        comparison.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "cardinal_arithmetic"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["comparison"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute cardinal arithmetic expression"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a cardinal arithmetic problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 2:
            pool = _CARDINAL_FACTS[:4]
        elif difficulty <= 4:
            pool = _CARDINAL_FACTS[:6]
        elif difficulty <= 6:
            pool = _CARDINAL_FACTS[4:8]
        else:
            pool = _CARDINAL_FACTS

        expr, result, reason = self._rng.choice(pool)
        # For expressions with 'n', substitute a concrete finite value
        n = self._rng.randint(2, 10)
        expr_concrete = expr.replace("n", str(n))
        reason_concrete = reason

        problem = f"compute: {expr_concrete}"
        return problem, {
            "expr": expr_concrete, "result": result,
            "reason": reason_concrete, "n": n,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing cardinal computation.
        """
        return [
            f"expression: {data['expr']}",
            f"reason: {data['reason']}",
            f"result: {data['result']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the cardinal result.

        Args:
            data: Solution data dict.

        Returns:
            Cardinal as string.
        """
        return data["result"]


# ---------------------------------------------------------------------------
# 3. Axiom of Choice Application (tier 7)
# ---------------------------------------------------------------------------

@register
class AxiomOfChoiceAppGenerator(StepGenerator):
    """Apply Zorn's lemma to prove existence of maximal elements.

    Template-based: every vector space has a basis, every proper ideal
    is contained in a maximal ideal, every filter extends to an ultrafilter.

    Difficulty scaling:
        d1-3: vector space basis (most concrete).
        d4-6: maximal ideal existence.
        d7-8: ultrafilter extension.

    Prerequisites:
        proof_by_contradiction.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "axiom_of_choice_app"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["proof_by_contradiction"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "apply Zorn's lemma"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an axiom of choice application problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            idx = 0
        elif difficulty <= 6:
            idx = 1
        else:
            idx = 2

        statement, chain_arg, conclusion = _ZORNS_APPLICATIONS[idx]
        problem = f"prove: {statement}"
        return problem, {
            "statement": statement,
            "chain_arg": chain_arg,
            "conclusion": conclusion,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing Zorn's lemma application.
        """
        return [
            f"goal: {data['statement']}",
            "apply Zorn's lemma: need every chain has upper bound",
            f"chain argument: {data['chain_arg']}",
            f"Zorn gives maximal element",
            f"conclusion: {data['conclusion']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the conclusion.

        Args:
            data: Solution data dict.

        Returns:
            Conclusion as string.
        """
        return data["conclusion"]


# ---------------------------------------------------------------------------
# 4. Transfinite Induction (tier 7)
# ---------------------------------------------------------------------------

@register
class TransfiniteInductionGenerator(StepGenerator):
    """Prove properties for all ordinals via transfinite induction.

    Three cases: base (0), successor (alpha+1), limit (sup).
    Template-based proofs for standard properties.

    Difficulty scaling:
        d1-3: "every ordinal has a Cantor normal form" (sketch).
        d4-6: "cumulative hierarchy V_alpha is well-defined".
        d7-8: "every well-ordered set is isomorphic to a unique ordinal".

    Prerequisites:
        natural_deduction.
    """

    _TEMPLATES = [
        {
            "statement": "every ordinal has a Cantor normal form",
            "base": "P(0): 0 = omega^0 * 0 (trivially in CNF)",
            "successor": "P(alpha+1): if alpha has CNF, alpha+1 = CNF(alpha)+1",
            "limit": "P(lambda): lambda = sup{alpha < lambda}, each has CNF",
            "conclusion": "all ordinals have Cantor normal form by TI",
        },
        {
            "statement": "cumulative hierarchy V_alpha is well-defined for all alpha",
            "base": "V_0 = empty set (well-defined)",
            "successor": "V_{alpha+1} = P(V_alpha): power set of well-defined set",
            "limit": "V_lambda = union_{alpha<lambda} V_alpha: union of well-defined sets",
            "conclusion": "V_alpha well-defined for all ordinals by TI",
        },
        {
            "statement": "every well-ordered set is order-isomorphic to a unique ordinal",
            "base": "empty set is isomorphic to 0",
            "successor": "if W\\{max}~alpha then W~alpha+1",
            "limit": "if all initial segments have ordinals, take their sup",
            "conclusion": "every well-order ~ unique ordinal by TI",
        },
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "transfinite_induction"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["natural_deduction"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "prove property by transfinite induction"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a transfinite induction problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            template = self._TEMPLATES[0]
        elif difficulty <= 6:
            template = self._TEMPLATES[1]
        else:
            template = self._TEMPLATES[2]

        problem = f"prove by TI: {template['statement']}"
        return problem, dict(template)

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing the three cases.
        """
        return [
            f"claim: {data['statement']}",
            f"base case: {data['base']}",
            f"successor case: {data['successor']}",
            f"limit case: {data['limit']}",
            f"QED: {data['conclusion']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the conclusion.

        Args:
            data: Solution data dict.

        Returns:
            Conclusion as string.
        """
        return data["conclusion"]


# ---------------------------------------------------------------------------
# 5. Set Cardinality (tier 5)
# ---------------------------------------------------------------------------

@register
class SetCardinalityGenerator(StepGenerator):
    """Prove cardinality equalities between infinite sets.

    |N| = |Z| = |Q| = aleph_0 < |R| = c. Shows bijections for
    countable sets and diagonal argument for uncountability.

    Difficulty scaling:
        d1-2: |N| = |Z| via explicit bijection.
        d3-4: |N| = |Q| via Cantor pairing.
        d5-6: |R| > |N| via diagonal argument.
        d7-8: |P(N)| = |R| = c.

    Prerequisites:
        set_operations.
    """

    _PROBLEMS = [
        {
            "statement": "|N| = |Z|",
            "bijection": "f(n) = (-1)^n * floor(n/2)",
            "examples": [(0, 0), (1, -1), (2, 1), (3, -2), (4, 2)],
            "result": "aleph_0",
            "justification": "bijection N->Z: 0->0, 1->-1, 2->1, 3->-2, ...",
        },
        {
            "statement": "|N| = |Q|",
            "bijection": "Cantor zigzag on p/q grid",
            "examples": [(1, "1/1"), (2, "1/2"), (3, "2/1"), (4, "1/3"), (5, "3/1")],
            "result": "aleph_0",
            "justification": "Cantor pairing enumerates Q: zigzag through p/q",
        },
        {
            "statement": "|R| > |N| (uncountable)",
            "bijection": "Cantor diagonal: assume f:N->R bijection, construct r not in range",
            "examples": [],
            "result": "c > aleph_0",
            "justification": "diagonal r differs from f(n) at n-th digit -> r not in range",
        },
        {
            "statement": "|P(N)| = |R| = c",
            "bijection": "S subset N <-> 0.b_1 b_2 b_3... in [0,1] (binary)",
            "examples": [],
            "result": "c = 2^aleph_0",
            "justification": "characteristic function of S gives binary expansion in [0,1]",
        },
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "set_cardinality_infinite"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["set_operations"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "prove set cardinality equality"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a set cardinality problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 2:
            data = self._PROBLEMS[0]
        elif difficulty <= 4:
            data = self._PROBLEMS[1]
        elif difficulty <= 6:
            data = self._PROBLEMS[2]
        else:
            data = self._PROBLEMS[3]

        problem = f"prove: {data['statement']}"
        return problem, dict(data)

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing the cardinality proof.
        """
        steps = [
            f"claim: {data['statement']}",
            f"method: {data['bijection']}",
        ]
        if data["examples"]:
            ex_str = ", ".join(f"{a}->{b}" for a, b in data["examples"][:4])
            steps.append(f"examples: {ex_str}")
        steps.append(data["justification"])
        steps.append(f"result: {data['result']}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the cardinality result.

        Args:
            data: Solution data dict.

        Returns:
            Cardinality as string.
        """
        return data["result"]


# ---------------------------------------------------------------------------
# 6. Well-Ordering (tier 6)
# ---------------------------------------------------------------------------

@register
class WellOrderingGenerator(StepGenerator):
    """Prove properties of well-ordered sets.

    Every non-empty subset of N has a minimum (by contradiction).
    Every well-ordered set is totally ordered. Template-based.

    Difficulty scaling:
        d1-2: verify minimum in small subsets of N.
        d3-4: prove N is well-ordered by contradiction.
        d5-6: prove every well-ordered set is totally ordered.
        d7-8: well-ordering theorem (AC implies WO).

    Prerequisites:
        proof_by_contradiction.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "well_ordering"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["proof_by_contradiction"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "prove well-ordering property"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a well-ordering problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 2:
            # Verify minimum in concrete subset
            size = self._rng.randint(3, 6)
            subset = sorted(self._rng.sample(range(1, 30), size))
            minimum = subset[0]
            problem = f"find minimum of S={{{', '.join(str(x) for x in subset)}}}"
            return problem, {
                "type": "concrete",
                "subset": subset, "minimum": minimum,
                "statement": f"min(S) = {minimum}",
            }
        elif difficulty <= 4:
            problem = "prove: every non-empty subset of N has a minimum"
            return problem, {
                "type": "contradiction",
                "statement": "N is well-ordered",
                "assume": "assume S subset N has no minimum",
                "derive": "then for all n in S, exists m in S with m < n",
                "contradiction": "infinite descent contradicts N being bounded below by 0",
                "conclusion": "every non-empty S subset N has a minimum",
            }
        elif difficulty <= 6:
            problem = "prove: every well-ordered set is totally ordered"
            return problem, {
                "type": "total_order",
                "statement": "well-ordered => totally ordered",
                "assume": "let (W, <=) be well-ordered",
                "derive": "for any a,b in W: {a,b} has minimum, so a<=b or b<=a",
                "contradiction": "",
                "conclusion": "W is totally ordered (trichotomy holds)",
            }
        else:
            problem = "well-ordering theorem: AC implies every set can be well-ordered"
            return problem, {
                "type": "wo_theorem",
                "statement": "AC <=> every set can be well-ordered",
                "assume": "given AC, define choice function on P(X)\\{empty}",
                "derive": "construct well-ordering by transfinite recursion using choice",
                "contradiction": "",
                "conclusion": "AC implies WO (Zermelo 1904)",
            }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing well-ordering proof.
        """
        if data["type"] == "concrete":
            subset = data["subset"]
            return [
                f"S={{{', '.join(str(x) for x in subset)}}}",
                f"S is non-empty subset of N",
                f"minimum element: {data['minimum']}",
                f"verify: {data['minimum']} <= all elements of S",
            ]
        steps = [f"claim: {data['statement']}"]
        if data["assume"]:
            steps.append(f"proof: {data['assume']}")
        if data["derive"]:
            steps.append(data["derive"])
        if data["contradiction"]:
            steps.append(f"contradiction: {data['contradiction']}")
        steps.append(f"QED: {data['conclusion']}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the conclusion.

        Args:
            data: Solution data dict.

        Returns:
            Conclusion or minimum as string.
        """
        if data["type"] == "concrete":
            return str(data["minimum"])
        return data["conclusion"]


# ---------------------------------------------------------------------------
# 7. Boolean Algebra Lattice (tier 5)
# ---------------------------------------------------------------------------

@register
class BooleanAlgebraLatticeGenerator(StepGenerator):
    """Verify Boolean algebra axioms in the power set lattice.

    Checks complement, distributivity, De Morgan's laws, and
    identity elements in P(S) for small finite sets S.

    Difficulty scaling:
        d1-2: |S|=2, verify complement.
        d3-4: |S|=2, verify distributivity.
        d5-6: |S|=3, verify De Morgan.
        d7-8: |S|=3, full axiom check.

    Prerequisites:
        boolean_eval.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "boolean_algebra_lattice"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["boolean_eval"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "verify Boolean algebra axioms in power set lattice"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Boolean algebra lattice problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 4:
            s = frozenset({1, 2})
        else:
            s = frozenset({1, 2, 3})

        # Pick two subsets
        ps = _power_set(s)
        a = frozenset(self._rng.sample(sorted(s), self._rng.randint(0, len(s))))
        b = frozenset(self._rng.sample(sorted(s), self._rng.randint(0, len(s))))
        c = frozenset(self._rng.sample(sorted(s), self._rng.randint(0, len(s))))

        # Complement
        a_comp = s - a
        # Distributivity: A & (B | C) = (A & B) | (A & C)
        dist_lhs = a & (b | c)
        dist_rhs = (a & b) | (a & c)
        dist_ok = dist_lhs == dist_rhs
        # De Morgan: complement(A | B) = complement(A) & complement(B)
        dm_lhs = s - (a | b)
        dm_rhs = (s - a) & (s - b)
        dm_ok = dm_lhs == dm_rhs

        if difficulty <= 2:
            check_type = "complement"
        elif difficulty <= 4:
            check_type = "distributivity"
        elif difficulty <= 6:
            check_type = "de_morgan"
        else:
            check_type = "full"

        problem = (f"P({_format_set(s)}): "
                   f"A={_format_set(a)}, B={_format_set(b)}")
        return problem, {
            "s": s, "a": a, "b": b, "c": c,
            "a_comp": a_comp,
            "dist_lhs": dist_lhs, "dist_rhs": dist_rhs, "dist_ok": dist_ok,
            "dm_lhs": dm_lhs, "dm_rhs": dm_rhs, "dm_ok": dm_ok,
            "check_type": check_type,
            "ps_size": len(ps),
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing axiom verification.
        """
        a, b = data["a"], data["b"]
        s = data["s"]
        steps = [f"S={_format_set(s)}, |P(S)|={data['ps_size']}"]

        ct = data["check_type"]
        if ct in ("complement", "full"):
            steps.append(
                f"complement: A={_format_set(a)}, A'={_format_set(data['a_comp'])}"
            )
            steps.append(
                f"A union A'={_format_set(a | data['a_comp'])}=S, "
                f"A inter A'={_format_set(a & data['a_comp'])}=empty"
            )

        if ct in ("distributivity", "full"):
            steps.append(
                f"dist: A&(B|C)={_format_set(data['dist_lhs'])}, "
                f"(A&B)|(A&C)={_format_set(data['dist_rhs'])} "
                f"{'ok' if data['dist_ok'] else 'fail'}"
            )

        if ct in ("de_morgan", "full"):
            steps.append(
                f"DM: (A|B)'={_format_set(data['dm_lhs'])}, "
                f"A'&B'={_format_set(data['dm_rhs'])} "
                f"{'ok' if data['dm_ok'] else 'fail'}"
            )

        return steps

    def _create_answer(self, data: dict) -> str:
        """Return verification result.

        Args:
            data: Solution data dict.

        Returns:
            Verification status.
        """
        results = []
        ct = data["check_type"]
        if ct in ("complement", "full"):
            results.append("complement:ok")
        if ct in ("distributivity", "full"):
            results.append(f"dist:{'ok' if data['dist_ok'] else 'fail'}")
        if ct in ("de_morgan", "full"):
            results.append(f"DM:{'ok' if data['dm_ok'] else 'fail'}")
        return ", ".join(results)


# ---------------------------------------------------------------------------
# 8. ZFC Axiom Application (tier 7)
# ---------------------------------------------------------------------------

@register
class ZFCAxiomApplyGenerator(StepGenerator):
    """Apply ZFC axioms to construct specific sets.

    Uses pairing, union, power set, and separation (comprehension)
    axioms to build sets from given inputs. Template-based.

    Difficulty scaling:
        d1-2: pairing axiom {a, b}.
        d3-4: union axiom.
        d5-6: power set axiom.
        d7-8: separation (comprehension) axiom.

    Prerequisites:
        set_operations.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "zfc_axiom_apply"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["set_operations"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "apply ZFC axiom to construct a set"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a ZFC axiom application problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 2:
            # Pairing
            a = self._rng.randint(1, 5)
            b = self._rng.randint(1, 5)
            result_set = _format_set(frozenset({a, b}))
            problem = f"pairing axiom: construct {{{a}, {b}}}"
            return problem, {
                "axiom": "pairing",
                "statement": f"for any a, b: {{a, b}} exists",
                "construction": f"given a={a}, b={b}",
                "result": result_set,
                "verify": f"{{{a}, {b}}} is a set by pairing",
            }
        elif difficulty <= 4:
            # Union
            s1 = frozenset(self._rng.sample(range(1, 6), 2))
            s2 = frozenset(self._rng.sample(range(1, 6), 2))
            a_set = frozenset({s1, s2})
            union_result = s1 | s2
            problem = f"union axiom: union({{{_format_set(s1)}, {_format_set(s2)}}})"
            return problem, {
                "axiom": "union",
                "statement": "for any set A: union(A) exists",
                "construction": f"A = {{{_format_set(s1)}, {_format_set(s2)}}}",
                "result": _format_set(union_result),
                "verify": f"union = {_format_set(union_result)}",
            }
        elif difficulty <= 6:
            # Power set
            size = self._rng.randint(1, 3)
            base = frozenset(self._rng.sample(range(1, 6), size))
            ps = _power_set(base)
            ps_strs = [_format_set(s) for s in ps]
            ps_display = ", ".join(ps_strs[:6])
            if len(ps_strs) > 6:
                ps_display += ", ..."
            problem = f"power set axiom: P({_format_set(base)})"
            return problem, {
                "axiom": "power_set",
                "statement": "for any set A: P(A) exists",
                "construction": f"A = {_format_set(base)}",
                "result": f"|P(A)| = {len(ps)}",
                "verify": f"P(A) = {{{ps_display}}}",
            }
        else:
            # Separation
            base = frozenset(self._rng.sample(range(1, 10), 5))
            threshold = self._rng.randint(3, 7)
            filtered = frozenset(x for x in base if x > threshold)
            problem = (f"separation: {{x in {_format_set(base)} : x > {threshold}}}")
            return problem, {
                "axiom": "separation",
                "statement": "for any set A and property P: {x in A : P(x)} exists",
                "construction": f"A = {_format_set(base)}, P(x) = (x > {threshold})",
                "result": _format_set(filtered),
                "verify": f"{{x in A : x > {threshold}}} = {_format_set(filtered)}",
            }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing axiom application.
        """
        return [
            f"axiom: {data['axiom']} -- {data['statement']}",
            f"input: {data['construction']}",
            data["verify"],
            f"result: {data['result']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the constructed set.

        Args:
            data: Solution data dict.

        Returns:
            Result as string.
        """
        return data["result"]
