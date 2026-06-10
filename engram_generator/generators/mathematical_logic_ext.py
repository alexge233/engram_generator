"""Mathematical logic extension generators.

10 generators across tiers 6-8 covering first-order satisfaction,
prenex normal form, Skolemisation, Herbrand universe, tableau proofs,
Craig interpolation, temporal logic, satisfiability check, clause
resolution, and Godel incompleteness.
"""
from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


# ═══════════════════════════════════════════════════════════════════
# HELPER UTILITIES
# ═══════════════════════════════════════════════════════════════════

def _format_clause(literals: list[str]) -> str:
    """Format a list of literals as a clause string.

    Args:
        literals: List of literal strings (e.g. ``['p', '~q']``).

    Returns:
        String like ``{p, ~q}``.
    """
    if not literals:
        return "{} (empty)"
    return "{" + ", ".join(literals) + "}"


def _negate(lit: str) -> str:
    """Negate a propositional literal.

    Args:
        lit: Literal string, e.g. ``'p'`` or ``'~p'``.

    Returns:
        Negated literal.
    """
    if lit.startswith("~"):
        return lit[1:]
    return f"~{lit}"


def _eval_prop(formula: str, assignment: dict[str, bool]) -> bool:
    """Evaluate a simple propositional formula under an assignment.

    Supports: variables (single letters), ~ (not), & (and), | (or),
    -> (implies), parentheses. Evaluated left-to-right with standard
    precedence: ~ > & > | > ->.

    Args:
        formula: Propositional formula string.
        assignment: Mapping from variable names to truth values.

    Returns:
        Truth value of the formula.
    """
    tokens = _tokenise_prop(formula)
    return _parse_implies(tokens, [0], assignment)


def _tokenise_prop(formula: str) -> list[str]:
    """Tokenise a propositional formula.

    Args:
        formula: Formula string.

    Returns:
        List of tokens.
    """
    tokens = []
    i = 0
    while i < len(formula):
        ch = formula[i]
        if ch in " \t":
            i += 1
            continue
        if ch in "()~&|":
            tokens.append(ch)
            i += 1
        elif ch == "-" and i + 1 < len(formula) and formula[i + 1] == ">":
            tokens.append("->")
            i += 2
        elif ch.isalpha():
            var = ch
            i += 1
            while i < len(formula) and (formula[i].isalnum() or formula[i] == "_"):
                var += formula[i]
                i += 1
            tokens.append(var)
        else:
            i += 1
    return tokens


def _parse_implies(tokens: list[str], pos: list[int],
                   asgn: dict[str, bool]) -> bool:
    """Parse implication (lowest precedence, right-associative).

    Args:
        tokens: Token list.
        pos: Mutable position pointer.
        asgn: Variable assignment.

    Returns:
        Evaluated truth value.
    """
    left = _parse_or(tokens, pos, asgn)
    if pos[0] < len(tokens) and tokens[pos[0]] == "->":
        pos[0] += 1
        right = _parse_implies(tokens, pos, asgn)
        return (not left) or right
    return left


def _parse_or(tokens: list[str], pos: list[int],
              asgn: dict[str, bool]) -> bool:
    """Parse disjunction.

    Args:
        tokens: Token list.
        pos: Mutable position pointer.
        asgn: Variable assignment.

    Returns:
        Evaluated truth value.
    """
    left = _parse_and(tokens, pos, asgn)
    while pos[0] < len(tokens) and tokens[pos[0]] == "|":
        pos[0] += 1
        right = _parse_and(tokens, pos, asgn)
        left = left or right
    return left


def _parse_and(tokens: list[str], pos: list[int],
               asgn: dict[str, bool]) -> bool:
    """Parse conjunction.

    Args:
        tokens: Token list.
        pos: Mutable position pointer.
        asgn: Variable assignment.

    Returns:
        Evaluated truth value.
    """
    left = _parse_not(tokens, pos, asgn)
    while pos[0] < len(tokens) and tokens[pos[0]] == "&":
        pos[0] += 1
        right = _parse_not(tokens, pos, asgn)
        left = left and right
    return left


def _parse_not(tokens: list[str], pos: list[int],
               asgn: dict[str, bool]) -> bool:
    """Parse negation.

    Args:
        tokens: Token list.
        pos: Mutable position pointer.
        asgn: Variable assignment.

    Returns:
        Evaluated truth value.
    """
    if pos[0] < len(tokens) and tokens[pos[0]] == "~":
        pos[0] += 1
        return not _parse_not(tokens, pos, asgn)
    return _parse_atom(tokens, pos, asgn)


def _parse_atom(tokens: list[str], pos: list[int],
                asgn: dict[str, bool]) -> bool:
    """Parse atomic variable or parenthesised expression.

    Args:
        tokens: Token list.
        pos: Mutable position pointer.
        asgn: Variable assignment.

    Returns:
        Evaluated truth value.
    """
    if pos[0] < len(tokens) and tokens[pos[0]] == "(":
        pos[0] += 1
        val = _parse_implies(tokens, pos, asgn)
        if pos[0] < len(tokens) and tokens[pos[0]] == ")":
            pos[0] += 1
        return val
    if pos[0] < len(tokens):
        var = tokens[pos[0]]
        pos[0] += 1
        return asgn.get(var, False)
    return False


# ═══════════════════════════════════════════════════════════════════
# 1. FIRST-ORDER SATISFACTION (tier 6)
# ═══════════════════════════════════════════════════════════════════

@register
class FirstOrderSatisfactionGenerator(StepGenerator):
    """Evaluate a first-order formula in a finite model.

    Given a finite domain and a relation, evaluate formulas of the
    form (forall x, P(x)), (exists x, P(x)), or
    (forall x, exists y, R(x,y)).

    Difficulty scaling:
        Difficulty 1-3: domain size 3, single quantifier.
        Difficulty 4-6: domain size 4, nested quantifiers.
        Difficulty 7-8: domain size 5, nested quantifiers with negation.

    Prerequisites:
        quantifier_eval (tier 3).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "first_order_satisfaction"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["quantifier_eval"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls model size and formula complexity.

        Returns:
            Task description string.
        """
        return "evaluate first-order formula in finite model"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a first-order satisfaction problem.

        Args:
            difficulty: Controls domain size and quantifier depth.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            n = 3
            domain = list(range(n))
            # Unary predicate P
            p_set = set(self._rng.sample(domain, self._rng.randint(1, n)))
            formula = self._rng.choice(["forall x: P(x)", "exists x: P(x)"])
            if "forall" in formula:
                result = all(x in p_set for x in domain)
            else:
                result = any(x in p_set for x in domain)
            p_str = "{" + ", ".join(str(x) for x in sorted(p_set)) + "}"
            problem = f"Domain = {{{', '.join(str(x) for x in domain)}}}. P = {p_str}. {formula}?"
            return problem, {
                "domain": domain, "formula": formula, "result": result,
                "p_set": sorted(p_set), "detail": f"P = {p_str}",
            }
        else:
            n = 4 if difficulty <= 6 else 5
            domain = list(range(n))
            # Binary relation R: for each x, randomly choose which y's are related
            rel = {}
            for x in domain:
                rel[x] = set(self._rng.sample(domain, self._rng.randint(0, n)))
            # forall x, exists y: R(x,y)
            formula = "forall x, exists y: R(x,y)"
            result = all(len(rel[x]) > 0 for x in domain)
            rel_str = "; ".join(f"{x}->{{{', '.join(str(y) for y in sorted(rel[x]))}}}"
                                for x in domain)
            problem = (
                f"Domain = {{{', '.join(str(x) for x in domain)}}}. "
                f"R: {rel_str}. {formula}?"
            )
            return problem, {
                "domain": domain, "formula": formula, "result": result,
                "rel": {x: sorted(v) for x, v in rel.items()},
                "detail": rel_str,
            }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate evaluation steps.

        Args:
            data: Solution data.

        Returns:
            Steps checking the formula at each domain element.
        """
        steps = [f"formula: {data['formula']}"]
        if "forall x, exists y" in data["formula"]:
            for x in data["domain"]:
                ys = data["rel"].get(x, [])
                has = len(ys) > 0
                steps.append(f"x={x}: R({x},y) for y in {ys}, exists? {has}")
        else:
            for x in data["domain"]:
                in_p = x in data.get("p_set", [])
                steps.append(f"x={x}: P({x}) = {in_p}")
        steps.append(f"result: {data['result']}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the truth value.

        Args:
            data: Solution data.

        Returns:
            True or False.
        """
        return str(data["result"])


# ═══════════════════════════════════════════════════════════════════
# 2. PRENEX NORMAL FORM (tier 6)
# ═══════════════════════════════════════════════════════════════════

@register
class PrenexNormalFormGenerator(StepGenerator):
    """Convert a first-order formula to prenex normal form.

    Moves all quantifiers to the front. Template-based with known
    input/output pairs for common patterns.

    Difficulty scaling:
        Difficulty 1-3: single quantifier swap with negation.
        Difficulty 4-6: two quantifiers, one negation.
        Difficulty 7-8: three quantifiers, nested negation.

    Prerequisites:
        quantifier_eval (tier 3).
    """

    TEMPLATES: list[dict] = [
        {"input": "~(forall x: P(x))", "output": "exists x: ~P(x)",
         "steps": ["push ~ inside forall", "forall x becomes exists x, negate body"]},
        {"input": "~(exists x: P(x))", "output": "forall x: ~P(x)",
         "steps": ["push ~ inside exists", "exists x becomes forall x, negate body"]},
        {"input": "(forall x: P(x)) & (exists y: Q(y))",
         "output": "forall x: exists y: (P(x) & Q(y))",
         "steps": ["x not free in Q(y), y not free in P(x)", "merge quantifiers to front"]},
        {"input": "~(forall x: exists y: R(x,y))",
         "output": "exists x: forall y: ~R(x,y)",
         "steps": ["push ~ past forall x -> exists x", "push ~ past exists y -> forall y",
                    "negate body R(x,y) -> ~R(x,y)"]},
        {"input": "(exists x: P(x)) -> (forall y: Q(y))",
         "output": "forall x: forall y: (P(x) -> Q(y))",
         "steps": ["rewrite A->B as ~A|B", "~(exists x: P(x)) = forall x: ~P(x)",
                    "merge: forall x: forall y: (~P(x)|Q(y)) = forall x: forall y: (P(x)->Q(y))"]},
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "prenex_normal_form"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["quantifier_eval"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls formula complexity.

        Returns:
            Task description string.
        """
        return "convert first-order formula to prenex normal form"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a prenex normal form problem.

        Args:
            difficulty: Controls template selection.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            tmpl = self._rng.choice(self.TEMPLATES[:2])
        elif difficulty <= 6:
            tmpl = self._rng.choice(self.TEMPLATES[2:4])
        else:
            tmpl = self.TEMPLATES[4]

        problem = f"Convert to prenex normal form: {tmpl['input']}"
        return problem, {
            "input": tmpl["input"],
            "output": tmpl["output"],
            "conversion_steps": tmpl["steps"],
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate conversion steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing quantifier movement.
        """
        steps = [f"input: {data['input']}"]
        for s in data["conversion_steps"]:
            steps.append(s)
        steps.append(f"prenex form: {data['output']}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the prenex form.

        Args:
            data: Solution data.

        Returns:
            Formula in prenex normal form.
        """
        return data["output"]


# ═══════════════════════════════════════════════════════════════════
# 3. SKOLEMISATION (tier 7)
# ═══════════════════════════════════════════════════════════════════

@register
class SkolemisationGenerator(StepGenerator):
    """Eliminate existential quantifiers by Skolem functions.

    Given a prenex formula, replaces each existential variable with
    a Skolem function of the preceding universal variables.

    Difficulty scaling:
        Difficulty 1-3: exists x: P(x) -> P(c).
        Difficulty 4-6: forall x, exists y: R(x,y) -> R(x, f(x)).
        Difficulty 7-8: forall x, forall y, exists z: S(x,y,z) -> S(x,y,g(x,y)).

    Prerequisites:
        prenex_normal_form (tier 6).
    """

    TEMPLATES: list[dict] = [
        {"input": "exists x: P(x)", "output": "P(c)",
         "explanation": "no universal quantifiers, replace x with constant c"},
        {"input": "forall x: exists y: R(x,y)", "output": "forall x: R(x, f(x))",
         "explanation": "y depends on x, replace with Skolem function f(x)"},
        {"input": "forall x: forall y: exists z: S(x,y,z)",
         "output": "forall x: forall y: S(x, y, g(x,y))",
         "explanation": "z depends on x and y, replace with g(x,y)"},
        {"input": "exists x: forall y: exists z: T(x,y,z)",
         "output": "forall y: T(c, y, h(y))",
         "explanation": "x has no preceding universals -> constant c; z depends on y -> h(y)"},
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "skolemisation"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["prenex_normal_form"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls formula complexity.

        Returns:
            Task description string.
        """
        return "Skolemise prenex formula by eliminating existential quantifiers"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Skolemisation problem.

        Args:
            difficulty: Controls template.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            tmpl = self.TEMPLATES[0]
        elif difficulty <= 6:
            tmpl = self.TEMPLATES[1]
        else:
            tmpl = self._rng.choice(self.TEMPLATES[2:])

        problem = f"Skolemise: {tmpl['input']}"
        return problem, {
            "input": tmpl["input"],
            "output": tmpl["output"],
            "explanation": tmpl["explanation"],
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Skolemisation steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing each replacement.
        """
        return [
            f"input: {data['input']}",
            f"identify existential variables and their preceding universals",
            data["explanation"],
            f"result: {data['output']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the Skolemised formula.

        Args:
            data: Solution data.

        Returns:
            Formula with Skolem functions.
        """
        return data["output"]


# ═══════════════════════════════════════════════════════════════════
# 4. HERBRAND UNIVERSE (tier 7)
# ═══════════════════════════════════════════════════════════════════

@register
class HerbrandUniverseGenerator(StepGenerator):
    """Enumerate terms of the Herbrand universe.

    Given constants and function symbols, lists terms up to a given
    depth. H_0 = constants, H_{k+1} = H_k union {f(t) | t in H_k}.

    Difficulty scaling:
        Difficulty 1-3: 2 constants, no function symbols. H = {a, b}.
        Difficulty 4-6: 1 constant, 1 unary function, depth 1.
        Difficulty 7-8: 1 constant, 1 unary function, depth 2.

    Prerequisites:
        skolemisation (tier 7).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "herbrand_universe"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["skolemisation"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls universe depth.

        Returns:
            Task description string.
        """
        return "enumerate Herbrand universe terms"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Herbrand universe problem.

        Args:
            difficulty: Controls constants, functions, and depth.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            constants = self._rng.sample(["a", "b", "c"], 2)
            functions = []
            depth = 0
            terms = sorted(constants)
        elif difficulty <= 6:
            constants = [self._rng.choice(["a", "b"])]
            functions = ["f"]
            depth = 1
            h0 = sorted(constants)
            h1 = h0[:]
            for t in h0:
                ft = f"f({t})"
                if ft not in h1:
                    h1.append(ft)
            terms = sorted(h1)
        else:
            constants = [self._rng.choice(["a", "b"])]
            functions = ["f"]
            depth = 2
            h0 = sorted(constants)
            h1 = h0[:]
            for t in h0:
                ft = f"f({t})"
                if ft not in h1:
                    h1.append(ft)
            h2 = h1[:]
            for t in h1:
                ft = f"f({t})"
                if ft not in h2:
                    h2.append(ft)
            terms = sorted(h2)

        const_str = ", ".join(constants)
        func_str = ", ".join(functions) if functions else "(none)"
        problem = (
            f"Constants: {{{const_str}}}. Functions: {{{func_str}}}. "
            f"Enumerate Herbrand universe to depth {depth}."
        )
        return problem, {
            "constants": constants, "functions": functions,
            "depth": depth, "terms": terms,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate enumeration steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing each level of the universe.
        """
        steps = [f"H_0 = {{{', '.join(data['constants'])}}}"]
        if data["functions"]:
            current = sorted(data["constants"])
            for d in range(1, data["depth"] + 1):
                new_terms = []
                for t in current:
                    for f in data["functions"]:
                        ft = f"{f}({t})"
                        if ft not in current and ft not in new_terms:
                            new_terms.append(ft)
                current = current + new_terms
                steps.append(f"H_{d} = {{{', '.join(sorted(current))}}}")
        steps.append(f"Herbrand universe = {{{', '.join(data['terms'])}}}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the Herbrand universe.

        Args:
            data: Solution data.

        Returns:
            Set of terms.
        """
        return "{" + ", ".join(data["terms"]) + "}"


# ═══════════════════════════════════════════════════════════════════
# 5. TABLEAU PROOF (tier 7)
# ═══════════════════════════════════════════════════════════════════

@register
class TableauProofGenerator(StepGenerator):
    """Prove a tautology using semantic tableaux.

    Starts with the negation of the formula, branches on disjunctions,
    and closes branches on contradictions.

    Difficulty scaling:
        Difficulty 1-3: p | ~p (simple tautology).
        Difficulty 4-6: (p -> q) -> (~q -> ~p) (contrapositive).
        Difficulty 7-8: ((p -> q) & (q -> r)) -> (p -> r) (transitivity).

    Prerequisites:
        propositional_eval (tier 2).
    """

    TAUTOLOGIES: list[dict] = [
        {
            "formula": "p | ~p",
            "neg": "~p & p",
            "steps": ["assume ~(p | ~p)", "= ~p & ~~p", "= ~p & p", "contradiction: p and ~p"],
        },
        {
            "formula": "(p -> q) -> (~q -> ~p)",
            "neg": "(p -> q) & ~(~q -> ~p)",
            "steps": [
                "assume ~((p->q)->(~q->~p))",
                "= (p->q) & ~(~q->~p)",
                "= (p->q) & (~q & p)",
                "from p->q and p: q",
                "but ~q. contradiction.",
            ],
        },
        {
            "formula": "((p -> q) & (q -> r)) -> (p -> r)",
            "neg": "(p -> q) & (q -> r) & p & ~r",
            "steps": [
                "assume ~(((p->q)&(q->r))->(p->r))",
                "= (p->q) & (q->r) & ~(p->r)",
                "= (p->q) & (q->r) & p & ~r",
                "from p->q and p: q",
                "from q->r and q: r",
                "but ~r. contradiction.",
            ],
        },
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "tableau_proof"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["propositional_eval"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls tautology complexity.

        Returns:
            Task description string.
        """
        return "prove tautology using semantic tableau"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a tableau proof problem.

        Args:
            difficulty: Controls which tautology.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            tmpl = self.TAUTOLOGIES[0]
        elif difficulty <= 6:
            tmpl = self.TAUTOLOGIES[1]
        else:
            tmpl = self.TAUTOLOGIES[2]

        problem = f"Prove by semantic tableau: {tmpl['formula']}"
        return problem, {
            "formula": tmpl["formula"],
            "neg": tmpl["neg"],
            "proof_steps": tmpl["steps"],
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate tableau proof steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing tableau construction and closure.
        """
        return data["proof_steps"]

    def _create_answer(self, data: dict) -> str:
        """Return the proof result.

        Args:
            data: Solution data.

        Returns:
            Confirmation that the formula is a tautology.
        """
        return f"{data['formula']} is a tautology (all branches closed)"


# ═══════════════════════════════════════════════════════════════════
# 6. CRAIG INTERPOLATION (tier 8)
# ═══════════════════════════════════════════════════════════════════

@register
class CraigInterpolationGenerator(StepGenerator):
    """Find a Craig interpolant between two formulas.

    Given A |= C, find B such that A |= B and B |= C, where
    Var(B) is a subset of Var(A) intersect Var(C). Template-based.

    Difficulty scaling:
        Difficulty 1-4: simple implication chain A = p&q, C = p|r, B = p.
        Difficulty 5-6: longer chain with shared variables.
        Difficulty 7-8: three shared variables.

    Prerequisites:
        natural_deduction (tier 7).
    """

    TEMPLATES: list[dict] = [
        {
            "a": "p & q", "c": "p | r", "b": "p",
            "shared": ["p"],
            "check_a_b": "p & q |= p (trivially)",
            "check_b_c": "p |= p | r (trivially)",
        },
        {
            "a": "p & (q | r)", "c": "p & (s | r)", "b": "p & r",
            "shared": ["p", "r"],
            "check_a_b": "need r in (q|r); only works if r holds. Interpolant: p",
            "check_b_c": "p |= p & (s | r) when r holds",
        },
        {
            "a": "(p -> q) & p", "c": "q | r", "b": "q",
            "shared": ["q"],
            "check_a_b": "(p->q) & p |= q (modus ponens)",
            "check_b_c": "q |= q | r (trivially)",
        },
        {
            "a": "p & q & r", "c": "(p | s) & (r | t)", "b": "p & r",
            "shared": ["p", "r"],
            "check_a_b": "p & q & r |= p & r (trivially)",
            "check_b_c": "p & r |= (p|s) & (r|t) (trivially)",
        },
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "craig_interpolation"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 8

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["natural_deduction"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls formula complexity.

        Returns:
            Task description string.
        """
        return "find Craig interpolant between two formulas"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Craig interpolation problem.

        Args:
            difficulty: Controls template complexity.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 4:
            tmpl = self._rng.choice(self.TEMPLATES[:2])
        elif difficulty <= 6:
            tmpl = self.TEMPLATES[2]
        else:
            tmpl = self.TEMPLATES[3]

        problem = (
            f"A = {tmpl['a']}, C = {tmpl['c']}. "
            f"A |= C. Find interpolant B with Var(B) subset Var(A) cap Var(C)."
        )
        return problem, {
            "a": tmpl["a"], "c": tmpl["c"], "b": tmpl["b"],
            "shared": tmpl["shared"],
            "check_a_b": tmpl["check_a_b"],
            "check_b_c": tmpl["check_b_c"],
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate interpolation steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing shared variables and verification.
        """
        return [
            f"A = {data['a']}, C = {data['c']}",
            f"shared variables: {{{', '.join(data['shared'])}}}",
            f"candidate B = {data['b']}",
            f"check A |= B: {data['check_a_b']}",
            f"check B |= C: {data['check_b_c']}",
            f"Var(B) = {{{', '.join(data['shared'])}}} subset Var(A) cap Var(C). valid.",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the interpolant.

        Args:
            data: Solution data.

        Returns:
            The Craig interpolant formula.
        """
        return f"B = {data['b']}"


# ═══════════════════════════════════════════════════════════════════
# 7. TEMPORAL LOGIC (tier 7)
# ═══════════════════════════════════════════════════════════════════

@register
class TemporalLogicGenerator(StepGenerator):
    """Evaluate LTL formulas on finite traces.

    Evaluates G (globally), F (finally), and U (until) operators
    on finite state traces.

    Difficulty scaling:
        Difficulty 1-3: G p or F p on 4-step trace.
        Difficulty 4-6: p U q on 4-step trace.
        Difficulty 7-8: nested: G(p -> F q) on 5-step trace.

    Prerequisites:
        propositional_eval (tier 2).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "temporal_logic"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["propositional_eval"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls formula complexity.

        Returns:
            Task description string.
        """
        return "evaluate LTL formula on finite trace"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a temporal logic problem.

        Args:
            difficulty: Controls formula and trace complexity.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            trace_len = 4
            p_vals = [self._rng.choice([True, False]) for _ in range(trace_len)]
            op = self._rng.choice(["G", "F"])
            if op == "G":
                result = all(p_vals)
                formula = "G p"
            else:
                result = any(p_vals)
                formula = "F p"
            trace_str = ", ".join(str(v) for v in p_vals)
            problem = f"Trace p = [{trace_str}]. Evaluate {formula}."
            return problem, {
                "formula": formula, "op": op, "trace_p": p_vals,
                "result": result, "trace_len": trace_len,
            }
        elif difficulty <= 6:
            trace_len = 4
            p_vals = [self._rng.choice([True, False]) for _ in range(trace_len)]
            q_vals = [self._rng.choice([True, False]) for _ in range(trace_len)]
            # p U q: p holds until q becomes true
            result = False
            for i in range(trace_len):
                if q_vals[i]:
                    result = all(p_vals[j] for j in range(i))
                    break
            formula = "p U q"
            p_str = ", ".join(str(v) for v in p_vals)
            q_str = ", ".join(str(v) for v in q_vals)
            problem = f"Trace p=[{p_str}], q=[{q_str}]. Evaluate {formula}."
            return problem, {
                "formula": formula, "op": "U",
                "trace_p": p_vals, "trace_q": q_vals,
                "result": result, "trace_len": trace_len,
            }
        else:
            trace_len = 5
            p_vals = [self._rng.choice([True, False]) for _ in range(trace_len)]
            q_vals = [self._rng.choice([True, False]) for _ in range(trace_len)]
            # G(p -> F q): at every step, if p then eventually q
            result = True
            for i in range(trace_len):
                if p_vals[i]:
                    if not any(q_vals[j] for j in range(i, trace_len)):
                        result = False
                        break
            formula = "G(p -> F q)"
            p_str = ", ".join(str(v) for v in p_vals)
            q_str = ", ".join(str(v) for v in q_vals)
            problem = f"Trace p=[{p_str}], q=[{q_str}]. Evaluate {formula}."
            return problem, {
                "formula": formula, "op": "G_implies_F",
                "trace_p": p_vals, "trace_q": q_vals,
                "result": result, "trace_len": trace_len,
            }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate evaluation steps.

        Args:
            data: Solution data.

        Returns:
            Steps checking the formula at each time step.
        """
        steps = [f"formula: {data['formula']}"]
        op = data["op"]
        if op in ("G", "F"):
            for i in range(data["trace_len"]):
                steps.append(f"t={i}: p={data['trace_p'][i]}")
            if op == "G":
                steps.append(f"G p: all true? {data['result']}")
            else:
                steps.append(f"F p: any true? {data['result']}")
        elif op == "U":
            for i in range(data["trace_len"]):
                steps.append(f"t={i}: p={data['trace_p'][i]}, q={data['trace_q'][i]}")
            steps.append(f"p U q: p holds until q? {data['result']}")
        else:
            for i in range(data["trace_len"]):
                steps.append(f"t={i}: p={data['trace_p'][i]}, q={data['trace_q'][i]}")
            steps.append(f"G(p -> F q): {data['result']}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the evaluation result.

        Args:
            data: Solution data.

        Returns:
            True or False.
        """
        return str(data["result"])


# ═══════════════════════════════════════════════════════════════════
# 8. SATISFIABILITY CHECK (tier 6)
# ═══════════════════════════════════════════════════════════════════

@register
class SatisfiabilityCheckGenerator(StepGenerator):
    """Check satisfiability by truth table enumeration.

    Generates a propositional formula, enumerates all assignments,
    and reports the first satisfying assignment or UNSAT.

    Difficulty scaling:
        Difficulty 1-3: 2 variables, simple formula.
        Difficulty 4-6: 3 variables.
        Difficulty 7-8: 4 variables.

    Prerequisites:
        boolean_eval (tier 0).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "satisfiability_check"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["boolean_eval"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls variable count.

        Returns:
            Task description string.
        """
        return "check propositional satisfiability by truth table"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a satisfiability problem.

        Args:
            difficulty: Controls number of variables.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            var_names = ["p", "q"]
            # Generate a random 2-variable formula
            op = self._rng.choice(["&", "|", "->"])
            neg_p = self._rng.choice(["", "~"])
            neg_q = self._rng.choice(["", "~"])
            formula = f"{neg_p}p {op} {neg_q}q"
        elif difficulty <= 6:
            var_names = ["p", "q", "r"]
            op1 = self._rng.choice(["&", "|"])
            op2 = self._rng.choice(["&", "|", "->"])
            neg = [self._rng.choice(["", "~"]) for _ in range(3)]
            formula = f"({neg[0]}p {op1} {neg[1]}q) {op2} {neg[2]}r"
        else:
            var_names = ["p", "q", "r", "s"]
            op1 = self._rng.choice(["&", "|"])
            op2 = self._rng.choice(["&", "|"])
            op3 = self._rng.choice(["&", "|", "->"])
            neg = [self._rng.choice(["", "~"]) for _ in range(4)]
            formula = f"({neg[0]}p {op1} {neg[1]}q) {op2} ({neg[2]}r {op3} {neg[3]}s)"

        n_vars = len(var_names)
        sat_assignment = None
        all_results = []
        for bits in range(2 ** n_vars):
            asgn = {}
            for i, v in enumerate(var_names):
                asgn[v] = bool((bits >> (n_vars - 1 - i)) & 1)
            val = _eval_prop(formula, asgn)
            all_results.append((dict(asgn), val))
            if val and sat_assignment is None:
                sat_assignment = dict(asgn)

        is_sat = sat_assignment is not None
        problem = f"Is {formula} satisfiable? Find assignment or prove UNSAT."
        return problem, {
            "formula": formula, "vars": var_names,
            "is_sat": is_sat, "sat_assignment": sat_assignment,
            "n_assignments": 2 ** n_vars,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate satisfiability check steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing enumeration result.
        """
        steps = [f"formula: {data['formula']}", f"variables: {', '.join(data['vars'])}"]
        steps.append(f"total assignments to check: {data['n_assignments']}")
        if data["is_sat"]:
            asgn_str = ", ".join(f"{k}={v}" for k, v in data["sat_assignment"].items())
            steps.append(f"satisfying assignment found: {asgn_str}")
        else:
            steps.append("no satisfying assignment exists")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return SAT or UNSAT.

        Args:
            data: Solution data.

        Returns:
            Satisfiability result.
        """
        if data["is_sat"]:
            asgn_str = ", ".join(f"{k}={v}" for k, v in data["sat_assignment"].items())
            return f"SAT: {asgn_str}"
        return "UNSAT"


# ═══════════════════════════════════════════════════════════════════
# 9. CLAUSE RESOLUTION (tier 6)
# ═══════════════════════════════════════════════════════════════════

@register
class ClauseResolutionGenerator(StepGenerator):
    """Resolve clauses to derive the empty clause or a resolvent.

    Given two clauses, finds a complementary literal and produces the
    resolvent. Chains resolutions to derive the empty clause.

    Difficulty scaling:
        Difficulty 1-3: 2 clauses, single resolution step.
        Difficulty 4-6: 3 clauses, two resolution steps.
        Difficulty 7-8: 4 clauses, chain to empty clause.

    Prerequisites:
        sat_verify (tier 5).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "clause_resolution"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["sat_verify"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls clause count.

        Returns:
            Task description string.
        """
        return "derive resolvent by clause resolution"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a clause resolution problem.

        Args:
            difficulty: Controls number of clauses and steps.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        vars_pool = ["p", "q", "r", "s"]

        if difficulty <= 3:
            a, b = self._rng.sample(vars_pool, 2)
            c1 = [a, b]
            c2 = [_negate(a)]
            resolvent = [b]
            steps_data = [
                {"c1": c1, "c2": c2, "on": a, "result": resolvent}
            ]
            clauses = [c1, c2]
        elif difficulty <= 6:
            a, b, c = self._rng.sample(vars_pool, 3)
            c1 = [a, b]
            c2 = [_negate(a), c]
            c3 = [_negate(c)]
            r1 = [b, c]  # resolve c1, c2 on a
            r2 = [b]  # resolve r1, c3 on c
            steps_data = [
                {"c1": c1, "c2": c2, "on": a, "result": r1},
                {"c1": r1, "c2": c3, "on": c, "result": r2},
            ]
            clauses = [c1, c2, c3]
        else:
            a, b = self._rng.sample(vars_pool, 2)
            c1 = [a]
            c2 = [_negate(a), b]
            c3 = [_negate(b)]
            r1 = [b]
            r2 = []  # empty clause
            steps_data = [
                {"c1": c1, "c2": c2, "on": a, "result": r1},
                {"c1": r1, "c2": c3, "on": b, "result": r2},
            ]
            clauses = [c1, c2, c3]

        clause_strs = [_format_clause(c) for c in clauses]
        problem = f"Clauses: {', '.join(clause_strs)}. Resolve to derive conclusion."
        return problem, {
            "clauses": clauses, "steps_data": steps_data,
            "final": steps_data[-1]["result"],
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate resolution steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing each resolution.
        """
        steps = []
        for i, s in enumerate(data["steps_data"]):
            c1_str = _format_clause(s["c1"])
            c2_str = _format_clause(s["c2"])
            r_str = _format_clause(s["result"])
            steps.append(f"resolve {c1_str} and {c2_str} on {s['on']}: {r_str}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the final resolvent.

        Args:
            data: Solution data.

        Returns:
            Final clause or indication of empty clause.
        """
        return _format_clause(data["final"])


# ═══════════════════════════════════════════════════════════════════
# 10. GODEL INCOMPLETENESS (tier 8)
# ═══════════════════════════════════════════════════════════════════

@register
class GodelIncompletenessGenerator(StepGenerator):
    """State Godel's first incompleteness theorem for a formal system.

    Template-based: identifies the self-referential sentence G that
    asserts its own unprovability in a given consistent, sufficiently
    strong formal system.

    Difficulty scaling:
        Difficulty 1-3: Peano Arithmetic.
        Difficulty 4-6: ZFC set theory.
        Difficulty 7-8: arbitrary recursively axiomatisable extension of PA.

    Prerequisites:
        natural_deduction (tier 7).
    """

    SYSTEMS: list[dict] = [
        {
            "name": "Peano Arithmetic (PA)",
            "axioms": "Peano axioms for natural numbers",
            "g_sentence": "G_PA: 'this sentence is not provable in PA'",
            "consequence": "if PA is consistent, then G_PA is true but unprovable in PA",
        },
        {
            "name": "ZFC set theory",
            "axioms": "Zermelo-Fraenkel axioms with choice",
            "g_sentence": "G_ZFC: 'this sentence is not provable in ZFC'",
            "consequence": "if ZFC is consistent, then G_ZFC is true but unprovable in ZFC",
        },
        {
            "name": "T (extension of PA)",
            "axioms": "recursively axiomatisable extension of PA",
            "g_sentence": "G_T: 'this sentence is not provable in T'",
            "consequence": "if T is consistent and contains PA, then G_T is true but unprovable in T",
        },
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "godel_incompleteness"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 8

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["natural_deduction"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls formal system.

        Returns:
            Task description string.
        """
        return "state Godel's first incompleteness theorem"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Godel incompleteness problem.

        Args:
            difficulty: Controls which formal system.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            sys = self.SYSTEMS[0]
        elif difficulty <= 6:
            sys = self.SYSTEMS[1]
        else:
            sys = self.SYSTEMS[2]

        problem = (
            f"Formal system: {sys['name']}. "
            f"State Godel's first incompleteness theorem. "
            f"Identify the self-referential sentence."
        )
        return problem, {
            "system": sys["name"],
            "axioms": sys["axioms"],
            "g_sentence": sys["g_sentence"],
            "consequence": sys["consequence"],
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate theorem statement steps.

        Args:
            data: Solution data.

        Returns:
            Steps stating the theorem and its consequences.
        """
        return [
            f"{data['system']}: consistent + recursive",
            f"G: {data['g_sentence']}",
            f"{data['consequence']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the theorem statement.

        Args:
            data: Solution data.

        Returns:
            The incompleteness result.
        """
        return data["consequence"]
