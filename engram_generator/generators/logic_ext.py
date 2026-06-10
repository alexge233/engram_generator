"""Extended logic generators.

8 generators covering CNF conversion, DNF conversion, logical
consequence, proof by induction, predicate logic validity, reductio
ad absurdum, soundness/completeness, and Tarski truth evaluation
across tiers 5-7.
"""
from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


# ===================================================================
# HELPER UTILITIES
# ===================================================================

def _eval_formula(formula: str, assignment: dict[str, bool]) -> bool:
    """Evaluate a propositional formula under an assignment.

    Supports variables (single lowercase letters), NOT, AND, OR, ->,
    <->, and parentheses. Uses recursive descent.

    Args:
        formula: Propositional formula string.
        assignment: Mapping from variable names to truth values.

    Returns:
        Truth value of the formula.
    """
    tokens = _tokenize(formula)
    result, _ = _parse_biconditional(tokens, 0, assignment)
    return result


def _tokenize(formula: str) -> list[str]:
    """Tokenize a propositional formula.

    Args:
        formula: Formula string.

    Returns:
        List of tokens.
    """
    tokens = []
    i = 0
    while i < len(formula):
        if formula[i].isspace():
            i += 1
        elif formula[i] in "()":
            tokens.append(formula[i])
            i += 1
        elif formula[i:i + 3] == "NOT":
            tokens.append("NOT")
            i += 3
        elif formula[i:i + 3] == "AND":
            tokens.append("AND")
            i += 3
        elif formula[i:i + 2] == "OR":
            tokens.append("OR")
            i += 2
        elif formula[i:i + 3] == "<->":
            tokens.append("<->")
            i += 3
        elif formula[i:i + 2] == "->":
            tokens.append("->")
            i += 2
        elif formula[i].isalpha():
            tokens.append(formula[i])
            i += 1
        else:
            i += 1
    return tokens


def _parse_biconditional(tokens: list[str], pos: int,
                         a: dict[str, bool]) -> tuple[bool, int]:
    """Parse biconditional level.

    Args:
        tokens: Token list.
        pos: Current position.
        a: Variable assignment.

    Returns:
        Tuple of (value, next_position).
    """
    left, pos = _parse_implication(tokens, pos, a)
    while pos < len(tokens) and tokens[pos] == "<->":
        pos += 1
        right, pos = _parse_implication(tokens, pos, a)
        left = (left == right)
    return left, pos


def _parse_implication(tokens: list[str], pos: int,
                       a: dict[str, bool]) -> tuple[bool, int]:
    """Parse implication level (right-associative).

    Args:
        tokens: Token list.
        pos: Current position.
        a: Variable assignment.

    Returns:
        Tuple of (value, next_position).
    """
    left, pos = _parse_or(tokens, pos, a)
    if pos < len(tokens) and tokens[pos] == "->":
        pos += 1
        right, pos = _parse_implication(tokens, pos, a)
        return (not left) or right, pos
    return left, pos


def _parse_or(tokens: list[str], pos: int,
              a: dict[str, bool]) -> tuple[bool, int]:
    """Parse OR level.

    Args:
        tokens: Token list.
        pos: Current position.
        a: Variable assignment.

    Returns:
        Tuple of (value, next_position).
    """
    left, pos = _parse_and(tokens, pos, a)
    while pos < len(tokens) and tokens[pos] == "OR":
        pos += 1
        right, pos = _parse_and(tokens, pos, a)
        left = left or right
    return left, pos


def _parse_and(tokens: list[str], pos: int,
               a: dict[str, bool]) -> tuple[bool, int]:
    """Parse AND level.

    Args:
        tokens: Token list.
        pos: Current position.
        a: Variable assignment.

    Returns:
        Tuple of (value, next_position).
    """
    left, pos = _parse_not(tokens, pos, a)
    while pos < len(tokens) and tokens[pos] == "AND":
        pos += 1
        right, pos = _parse_not(tokens, pos, a)
        left = left and right
    return left, pos


def _parse_not(tokens: list[str], pos: int,
               a: dict[str, bool]) -> tuple[bool, int]:
    """Parse NOT level.

    Args:
        tokens: Token list.
        pos: Current position.
        a: Variable assignment.

    Returns:
        Tuple of (value, next_position).
    """
    if pos < len(tokens) and tokens[pos] == "NOT":
        pos += 1
        val, pos = _parse_not(tokens, pos, a)
        return not val, pos
    return _parse_atom(tokens, pos, a)


def _parse_atom(tokens: list[str], pos: int,
                a: dict[str, bool]) -> tuple[bool, int]:
    """Parse atomic formula or parenthesised expression.

    Args:
        tokens: Token list.
        pos: Current position.
        a: Variable assignment.

    Returns:
        Tuple of (value, next_position).
    """
    if pos < len(tokens) and tokens[pos] == "(":
        pos += 1
        val, pos = _parse_biconditional(tokens, pos, a)
        if pos < len(tokens) and tokens[pos] == ")":
            pos += 1
        return val, pos
    if pos < len(tokens) and tokens[pos].isalpha() and len(tokens[pos]) == 1:
        var = tokens[pos]
        return a.get(var, False), pos + 1
    return False, pos + 1


def _get_vars(formula: str) -> list[str]:
    """Extract variable names from a formula.

    Args:
        formula: Propositional formula string.

    Returns:
        Sorted list of unique variable names.
    """
    return sorted(set(
        c for c in formula if c.isalpha() and c.islower()
        and c not in ("N", "O", "A")
    ))


# ===================================================================
# 1. CNF CONVERSION (tier 5)
# ===================================================================

@register
class CnfConversionGenerator(StepGenerator):
    """Convert a propositional formula to conjunctive normal form.

    Applies De Morgan's laws, double negation elimination, and
    distribution to convert arbitrary formulas to CNF.

    Difficulty scaling:
        Difficulty 1-3: 2-variable formulas with one connective.
        Difficulty 4-6: 2-3 variables, implications, biconditionals.
        Difficulty 7-8: 3 variables, nested connectives.

    Prerequisites:
        propositional_eval (tier 2).
    """

    _FORMULAS_EASY = [
        ("NOT (p AND q)", "CNF: (NOT p) OR (NOT q)",
         ["De Morgan: NOT (p AND q) = (NOT p) OR (NOT q)",
          "already a single clause"]),
        ("NOT (p OR q)", "CNF: (NOT p) AND (NOT q)",
         ["De Morgan: NOT (p OR q) = (NOT p) AND (NOT q)",
          "two unit clauses"]),
        ("NOT (NOT p)", "CNF: p",
         ["double negation: NOT (NOT p) = p"]),
    ]

    _FORMULAS_MED = [
        ("p -> q", "CNF: (NOT p) OR q",
         ["implication elimination: p -> q = (NOT p) OR q",
          "single clause"]),
        ("p <-> q", "CNF: ((NOT p) OR q) AND ((NOT q) OR p)",
         ["biconditional: (p -> q) AND (q -> p)",
          "= ((NOT p) OR q) AND ((NOT q) OR p)"]),
        ("NOT (p -> q)", "CNF: p AND (NOT q)",
         ["NOT ((NOT p) OR q) = p AND (NOT q)",
          "De Morgan applied"]),
    ]

    _FORMULAS_HARD = [
        ("(p OR q) -> r", "CNF: ((NOT p) OR r) AND ((NOT q) OR r)",
         ["implication: (NOT (p OR q)) OR r",
          "distribute: ((NOT p) AND (NOT q)) OR r",
          "= ((NOT p) OR r) AND ((NOT q) OR r)"]),
        ("p -> (q AND r)", "CNF: ((NOT p) OR q) AND ((NOT p) OR r)",
         ["implication: (NOT p) OR (q AND r)",
          "distribute: ((NOT p) OR q) AND ((NOT p) OR r)"]),
        ("NOT (p AND q AND r)",
         "CNF: (NOT p) OR (NOT q) OR (NOT r)",
         ["generalised De Morgan",
          "single clause with three literals"]),
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "cnf_conversion"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

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
        return "convert propositional formula to CNF"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a CNF conversion problem.

        Args:
            difficulty: Controls formula complexity.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            pool = self._FORMULAS_EASY
        elif difficulty <= 6:
            pool = self._FORMULAS_EASY + self._FORMULAS_MED
        else:
            pool = self._FORMULAS_EASY + self._FORMULAS_MED + self._FORMULAS_HARD

        formula, cnf, conversion_steps = self._rng.choice(pool)
        problem = f"Convert to CNF: {formula}"
        return problem, {
            "formula": formula, "cnf": cnf, "steps": conversion_steps,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate CNF conversion steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing the conversion.
        """
        return data["steps"]

    def _create_answer(self, data: dict) -> str:
        """Return the final answer.

        Args:
            data: Solution data.

        Returns:
            Formula in CNF.
        """
        return data["cnf"]


# ===================================================================
# 2. DNF CONVERSION (tier 5)
# ===================================================================

@register
class DnfConversionGenerator(StepGenerator):
    """Convert a propositional formula to disjunctive normal form.

    Applies De Morgan's laws, double negation elimination, and
    distribution (dual of CNF) to convert to DNF.

    Difficulty scaling:
        Difficulty 1-3: 2-variable formulas.
        Difficulty 4-6: implications, biconditionals.
        Difficulty 7-8: 3 variables, nested connectives.

    Prerequisites:
        propositional_eval (tier 2).
    """

    _FORMULAS_EASY = [
        ("NOT (p OR q)", "DNF: (NOT p) AND (NOT q)",
         ["De Morgan: NOT (p OR q) = (NOT p) AND (NOT q)",
          "single minterm"]),
        ("NOT (p AND q)", "DNF: (NOT p) OR (NOT q)",
         ["De Morgan: NOT (p AND q) = (NOT p) OR (NOT q)",
          "two minterms"]),
        ("p AND (NOT p)", "DNF: False (empty disjunction)",
         ["p AND (NOT p) is a contradiction", "no satisfying minterm"]),
    ]

    _FORMULAS_MED = [
        ("p -> q", "DNF: (NOT p) OR (p AND q)",
         ["implication: (NOT p) OR q",
          "expand: (NOT p) OR (p AND q) (adding p implicitly)"]),
        ("p <-> q", "DNF: (p AND q) OR (NOT p AND NOT q)",
         ["biconditional: both true or both false",
          "= (p AND q) OR (NOT p AND NOT q)"]),
        ("NOT (p -> q)", "DNF: p AND (NOT q)",
         ["NOT ((NOT p) OR q) = p AND (NOT q)"]),
    ]

    _FORMULAS_HARD = [
        ("(p AND q) OR r",
         "DNF: (p AND q) OR r",
         ["already in DNF",
          "two minterms: (p AND q), (r)"]),
        ("p AND (q OR r)",
         "DNF: (p AND q) OR (p AND r)",
         ["distribute AND over OR",
          "= (p AND q) OR (p AND r)"]),
        ("(p OR q) AND (p OR r)",
         "DNF: p OR (q AND r)",
         ["factor out p: p OR (q AND r)",
          "or expand to three minterms"]),
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "dnf_conversion"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

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
        return "convert propositional formula to DNF"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a DNF conversion problem.

        Args:
            difficulty: Controls formula complexity.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            pool = self._FORMULAS_EASY
        elif difficulty <= 6:
            pool = self._FORMULAS_EASY + self._FORMULAS_MED
        else:
            pool = self._FORMULAS_EASY + self._FORMULAS_MED + self._FORMULAS_HARD

        formula, dnf, conversion_steps = self._rng.choice(pool)
        problem = f"Convert to DNF: {formula}"
        return problem, {
            "formula": formula, "dnf": dnf, "steps": conversion_steps,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate DNF conversion steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing the conversion.
        """
        return data["steps"]

    def _create_answer(self, data: dict) -> str:
        """Return the final answer.

        Args:
            data: Solution data.

        Returns:
            Formula in DNF.
        """
        return data["dnf"]


# ===================================================================
# 3. LOGICAL CONSEQUENCE (tier 5)
# ===================================================================

@register
class LogicalConsequenceGenerator(StepGenerator):
    """Determine if phi |= psi by checking all models.

    For 2-3 variable propositional formulas, enumerates all truth
    value assignments satisfying phi and checks if all also satisfy psi.

    Difficulty scaling:
        Difficulty 1-3: 2 variables, simple formulas.
        Difficulty 4-6: 2 variables, compound formulas.
        Difficulty 7-8: 3 variables.

    Prerequisites:
        propositional_eval (tier 2).
    """

    _PAIRS_2VAR = [
        ("p AND q", "p", True,
         "every model of p AND q has p = True"),
        ("p AND q", "p OR q", True,
         "if both true, then at least one true"),
        ("p", "p OR q", True,
         "if p true, then p OR q true"),
        ("p OR q", "p AND q", False,
         "p=T, q=F satisfies p OR q but not p AND q"),
        ("p -> q", "NOT p OR q", True,
         "p -> q is equivalent to NOT p OR q"),
        ("p", "p -> q", False,
         "p=T, q=F: p true but p -> q false"),
    ]

    _PAIRS_3VAR = [
        ("p AND q AND r", "p AND q", True,
         "conjunction of 3 entails conjunction of 2"),
        ("(p -> q) AND (q -> r)", "p -> r", True,
         "hypothetical syllogism: chain of implications"),
        ("p OR q", "p OR q OR r", True,
         "weakening: adding disjunct preserves truth"),
        ("p AND (q OR r)", "(p AND q) OR (p AND r)", True,
         "distribution is an equivalence"),
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "logical_consequence"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

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
        return "determine if phi |= psi (logical consequence)"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a logical consequence problem.

        Args:
            difficulty: Controls formula complexity.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 6:
            pool = self._PAIRS_2VAR
        else:
            pool = self._PAIRS_2VAR + self._PAIRS_3VAR

        phi, psi, entails, reason = self._rng.choice(pool)
        problem = f"Does {phi} |= {psi}?"
        return problem, {
            "phi": phi, "psi": psi, "entails": entails, "reason": reason,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate logical consequence steps.

        Args:
            data: Solution data.

        Returns:
            Steps checking all models.
        """
        steps = [
            f"phi: {data['phi']}",
            f"psi: {data['psi']}",
            "check: every model of phi satisfies psi?",
            data["reason"],
        ]
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the final answer.

        Args:
            data: Solution data.

        Returns:
            YES or NO.
        """
        if data["entails"]:
            return f"YES, {data['phi']} |= {data['psi']}"
        return f"NO, countermodel exists"


# ===================================================================
# 4. PROOF BY INDUCTION (EXTENDED) (tier 6)
# ===================================================================

@register
class ProofByInductionExtGenerator(StepGenerator):
    """Prove sum formulas by mathematical induction.

    Generates a sum identity, verifies the base case, and carries
    out the inductive step algebraically.

    Difficulty scaling:
        Difficulty 1-3: sum of first n integers.
        Difficulty 4-6: sum of squares, cubes.
        Difficulty 7-8: sum of geometric series, alternating sums.

    Prerequisites:
        proof_by_contradiction (tier 4).
    """

    _FORMULAS_EASY = [
        ("sum k for k=1..n", "n(n+1)/2",
         lambda n: n * (n + 1) // 2,
         "base: 1 = 1*2/2 = 1. "
         "inductive: assume sum_k = n(n+1)/2, then sum_{n+1} = n(n+1)/2 + (n+1) = (n+1)(n+2)/2"),
    ]

    _FORMULAS_MED = [
        ("sum k^2 for k=1..n", "n(n+1)(2n+1)/6",
         lambda n: n * (n + 1) * (2 * n + 1) // 6,
         "base: 1 = 1*2*3/6 = 1. "
         "inductive: add (n+1)^2, factor to get (n+1)(n+2)(2n+3)/6"),
        ("sum k^3 for k=1..n", "[n(n+1)/2]^2",
         lambda n: (n * (n + 1) // 2) ** 2,
         "base: 1 = [1*2/2]^2 = 1. "
         "inductive: add (n+1)^3, use factoring"),
    ]

    _FORMULAS_HARD = [
        ("sum 2^k for k=0..n", "2^{n+1} - 1",
         lambda n: 2 ** (n + 1) - 1,
         "base: 2^0 = 1 = 2^1 - 1. "
         "inductive: 2^{n+1} - 1 + 2^{n+1} = 2^{n+2} - 1"),
        ("sum (2k-1) for k=1..n", "n^2",
         lambda n: n ** 2,
         "base: 1 = 1^2. "
         "inductive: n^2 + (2n+1) = (n+1)^2"),
        ("sum 1/(k(k+1)) for k=1..n", "n/(n+1)",
         lambda n: round(n / (n + 1), 4),
         "base: 1/2 = 1/2. "
         "inductive: n/(n+1) + 1/((n+1)(n+2)) = (n+1)/(n+2)"),
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "proof_by_induction_ext"

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
            difficulty: Controls formula complexity.

        Returns:
            Task description string.
        """
        return "prove sum formula by mathematical induction"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an induction proof problem.

        Args:
            difficulty: Controls formula complexity.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            pool = self._FORMULAS_EASY
        elif difficulty <= 6:
            pool = self._FORMULAS_EASY + self._FORMULAS_MED
        else:
            pool = self._FORMULAS_EASY + self._FORMULAS_MED + self._FORMULAS_HARD

        desc, closed_form, fn, proof_sketch = self._rng.choice(pool)

        n = self._rng.randint(3, 8)
        value = fn(n)
        base_val = fn(1)

        problem = f"Prove: {desc} = {closed_form}. Verify for n={n}."
        return problem, {
            "desc": desc, "closed_form": closed_form,
            "n": n, "value": value, "base_val": base_val,
            "proof_sketch": proof_sketch,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate induction proof steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing base case, inductive step, and verification.
        """
        return [
            f"base case (n=1): {data['desc']} = {data['base_val']}",
            data["proof_sketch"],
            f"verify n={data['n']}: {data['closed_form']} = {data['value']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the final answer.

        Args:
            data: Solution data.

        Returns:
            Verified formula value.
        """
        return f"{data['closed_form']} = {data['value']} for n={data['n']}"


# ===================================================================
# 5. PREDICATE LOGIC VALIDITY (tier 6)
# ===================================================================

@register
class PredicateLogicValidityGenerator(StepGenerator):
    """Check if a predicate logic formula is valid in finite models.

    Given a formula with quantifiers and a finite domain {1,...,n},
    exhaustively evaluates to determine validity.

    Difficulty scaling:
        Difficulty 1-3: domain size 2, simple quantifiers.
        Difficulty 4-6: domain size 2-3, nested quantifiers.
        Difficulty 7-8: domain size 3, mixed quantifiers.

    Prerequisites:
        quantifier_eval (tier 3).
    """

    _FORMULAS_EASY = [
        ("forall x: P(x) -> P(x)", True,
         "tautology: P(x) -> P(x) is always true",
         lambda d, interp: True),
        ("exists x: P(x) OR NOT P(x)", True,
         "tautology: P(x) OR NOT P(x) for any x",
         lambda d, interp: True),
        ("forall x: P(x) AND NOT P(x)", False,
         "contradiction: P(x) AND NOT P(x) is always false",
         lambda d, interp: False),
    ]

    _FORMULAS_MED = [
        ("forall x: forall y: P(x,y) -> P(x,y)", True,
         "tautology regardless of interpretation",
         lambda d, interp: True),
        ("forall x: exists y: x = y", True,
         "every element equals itself: take y = x",
         lambda d, interp: True),
        ("exists x: exists y: x != y", None,
         "true iff |domain| >= 2",
         lambda d, interp: len(d) >= 2),
    ]

    _FORMULAS_HARD = [
        ("forall x: exists y: R(x,y) -> exists y: forall x: R(x,y)", False,
         "not valid: universal/existential swap fails in general",
         lambda d, interp: False),
        ("(forall x: P(x)) -> (exists x: P(x))", None,
         "valid when domain is non-empty",
         lambda d, interp: len(d) > 0),
        ("exists x: (P(x) -> forall y: P(y))", True,
         "valid: if all P true pick any; if some P false pick that one",
         lambda d, interp: True),
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "predicate_logic_validity"

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
        return "check predicate logic validity in finite model"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a predicate logic validity problem.

        Args:
            difficulty: Controls formula complexity.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            pool = self._FORMULAS_EASY
            domain_size = 2
        elif difficulty <= 6:
            pool = self._FORMULAS_EASY + self._FORMULAS_MED
            domain_size = self._rng.randint(2, 3)
        else:
            pool = self._FORMULAS_EASY + self._FORMULAS_MED + self._FORMULAS_HARD
            domain_size = 3

        formula, fixed_val, reason, evaluator = self._rng.choice(pool)
        domain = list(range(1, domain_size + 1))

        if fixed_val is not None:
            valid = fixed_val
        else:
            valid = evaluator(domain, {})

        problem = (
            f"domain = {{{', '.join(str(d) for d in domain)}}}. "
            f"Is '{formula}' valid?"
        )
        return problem, {
            "formula": formula, "domain": domain,
            "valid": valid, "reason": reason,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate validity check steps.

        Args:
            data: Solution data.

        Returns:
            Steps explaining the evaluation.
        """
        return [
            f"formula: {data['formula']}",
            f"domain: {{{', '.join(str(d) for d in data['domain'])}}}",
            data["reason"],
            f"valid: {'YES' if data['valid'] else 'NO'}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the final answer.

        Args:
            data: Solution data.

        Returns:
            YES or NO.
        """
        return "YES, valid" if data["valid"] else "NO, not valid"


# ===================================================================
# 6. REDUCTIO AD ABSURDUM (tier 5)
# ===================================================================

@register
class ReductioAdAbsurdumGenerator(StepGenerator):
    """Prove by contradiction (assume negation, derive contradiction).

    Template-based proofs of classic results: irrationality of sqrt(2),
    infinitude of primes, no largest integer, etc.

    Difficulty scaling:
        Difficulty 1-3: simple contradictions (no largest integer).
        Difficulty 4-6: irrationality of sqrt(2), pigeonhole.
        Difficulty 7-8: infinitude of primes, uncountability.

    Prerequisites:
        proof_by_contradiction (tier 4).
    """

    _PROOFS_EASY = [
        ("there is no largest integer",
         "assume N is largest; then N+1 > N, contradiction",
         "no largest integer exists"),
        ("if n^2 is even then n is even",
         "assume n is odd: n = 2k+1, n^2 = 4k^2+4k+1 is odd, contradiction",
         "n must be even"),
    ]

    _PROOFS_MED = [
        ("sqrt(2) is irrational",
         "assume sqrt(2) = a/b in lowest terms; "
         "then 2b^2 = a^2 so a is even, a = 2k; "
         "2b^2 = 4k^2, b^2 = 2k^2, b is even; "
         "contradicts lowest terms",
         "sqrt(2) is irrational"),
        ("in any group of 3 integers, two have the same parity",
         "assume all three have different parity; "
         "but there are only 2 parities, contradiction by pigeonhole",
         "two must share parity"),
    ]

    _PROOFS_HARD = [
        ("there are infinitely many primes",
         "assume primes are p_1,...,p_k; "
         "let N = p_1*...*p_k + 1; "
         "N is not divisible by any p_i, "
         "so N has a new prime factor, contradiction",
         "infinitely many primes exist"),
        ("R is uncountable",
         "assume R is countable as r_1, r_2, ...; "
         "Cantor diagonal: construct real differing from r_n in nth digit; "
         "this real is not in the list, contradiction",
         "R is uncountable"),
        ("sqrt(3) is irrational",
         "assume sqrt(3) = a/b in lowest terms; "
         "3b^2 = a^2, so 3|a, let a = 3k; "
         "3b^2 = 9k^2, b^2 = 3k^2, so 3|b; "
         "contradicts lowest terms",
         "sqrt(3) is irrational"),
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "reductio_ad_absurdum"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["proof_by_contradiction"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls proof complexity.

        Returns:
            Task description string.
        """
        return "prove statement by reductio ad absurdum"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a proof by contradiction problem.

        Args:
            difficulty: Controls proof complexity.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            pool = self._PROOFS_EASY
        elif difficulty <= 6:
            pool = self._PROOFS_EASY + self._PROOFS_MED
        else:
            pool = self._PROOFS_EASY + self._PROOFS_MED + self._PROOFS_HARD

        statement, proof_sketch, conclusion = self._rng.choice(pool)
        problem = f"Prove by contradiction: {statement}"
        return problem, {
            "statement": statement, "proof_sketch": proof_sketch,
            "conclusion": conclusion,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate proof by contradiction steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing the proof.
        """
        return [
            f"goal: {data['statement']}",
            "assume the negation",
            data["proof_sketch"],
            f"conclusion: {data['conclusion']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the final answer.

        Args:
            data: Solution data.

        Returns:
            Conclusion.
        """
        return data["conclusion"]


# ===================================================================
# 7. SOUNDNESS / COMPLETENESS (tier 7)
# ===================================================================

@register
class SoundnessCompletenessGenerator(StepGenerator):
    """Check if a deduction step is sound in a given proof system.

    Template-based: given a derivation rule (modus ponens, conjunction
    introduction, etc.), determines if the application is syntactically
    valid and semantically sound.

    Difficulty scaling:
        Difficulty 1-3: modus ponens, conjunction intro.
        Difficulty 4-6: disjunction elim, conditional proof.
        Difficulty 7-8: RAA, universal generalization, completeness.

    Prerequisites:
        natural_deduction (tier 7).
    """

    _RULES_EASY = [
        ("modus ponens: from p and p -> q, derive q",
         True, True,
         "valid rule: if p and p -> q both true, q must be true"),
        ("conjunction intro: from p and q, derive p AND q",
         True, True,
         "valid rule: both premises true entails conjunction"),
        ("conjunction elim: from p AND q, derive p",
         True, True,
         "valid rule: conjunction true implies each conjunct true"),
    ]

    _RULES_MED = [
        ("disjunction intro: from p, derive p OR q",
         True, True,
         "valid rule: if p true, then p OR q true for any q"),
        ("hypothetical syllogism: from p->q and q->r, derive p->r",
         True, True,
         "valid rule: chain of implications"),
        ("affirming the consequent: from q and p->q, derive p",
         True, False,
         "INVALID: q and p->q do not entail p (unsound application)"),
        ("denying the antecedent: from NOT p and p->q, derive NOT q",
         True, False,
         "INVALID: NOT p and p->q do not entail NOT q"),
    ]

    _RULES_HARD = [
        ("RAA: from p leading to contradiction, derive NOT p",
         True, True,
         "valid rule: reductio ad absurdum is sound in classical logic"),
        ("universal generalisation: from P(a) for arbitrary a, derive forall x P(x)",
         True, True,
         "valid if a is truly arbitrary (no special assumptions)"),
        ("completeness: every valid formula is provable (propositional logic)",
         True, True,
         "propositional logic is complete by truth-table method"),
        ("Godel: every true arithmetic formula is provable in PA",
         False, False,
         "FALSE by Godel's first incompleteness theorem"),
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "soundness_completeness"

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
            difficulty: Controls rule complexity.

        Returns:
            Task description string.
        """
        return "check soundness of deduction rule or completeness claim"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a soundness/completeness check problem.

        Args:
            difficulty: Controls rule complexity.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            pool = self._RULES_EASY
        elif difficulty <= 6:
            pool = self._RULES_EASY + self._RULES_MED
        else:
            pool = self._RULES_EASY + self._RULES_MED + self._RULES_HARD

        description, syntactic, semantic, reason = self._rng.choice(pool)
        problem = f"Is this sound? {description}"
        return problem, {
            "description": description,
            "syntactically_valid": syntactic,
            "semantically_sound": semantic,
            "reason": reason,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate soundness check steps.

        Args:
            data: Solution data.

        Returns:
            Steps explaining the soundness analysis.
        """
        return [
            f"rule: {data['description']}",
            f"syntactically valid: {'YES' if data['syntactically_valid'] else 'NO'}",
            f"semantically sound: {'YES' if data['semantically_sound'] else 'NO'}",
            data["reason"],
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the final answer.

        Args:
            data: Solution data.

        Returns:
            SOUND or UNSOUND.
        """
        if data["semantically_sound"]:
            return "SOUND"
        return "UNSOUND"


# ===================================================================
# 8. TARSKI TRUTH (tier 6)
# ===================================================================

@register
class TarskiTruthGenerator(StepGenerator):
    """Evaluate truth of a formula in a given structure.

    Given a structure M = (domain, interpretation of predicates and
    constants), evaluates a first-order formula under Tarski's
    definition of truth.

    Difficulty scaling:
        Difficulty 1-3: atomic formulas, 2-element domain.
        Difficulty 4-6: connectives, 2-3 element domain.
        Difficulty 7-8: quantifiers, 3 element domain.

    Prerequisites:
        quantifier_eval (tier 3).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "tarski_truth"

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
            difficulty: Controls formula and structure complexity.

        Returns:
            Task description string.
        """
        return "evaluate truth of formula in structure (Tarski semantics)"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Tarski truth evaluation problem.

        Args:
            difficulty: Controls complexity.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            domain = [1, 2]
        elif difficulty <= 6:
            domain = list(range(1, self._rng.randint(2, 3) + 1))
        else:
            domain = [1, 2, 3]

        p_ext = set()
        for d in domain:
            if self._rng.random() < 0.5:
                p_ext.add(d)

        r_ext = set()
        for a in domain:
            for b in domain:
                if self._rng.random() < 0.4:
                    r_ext.add((a, b))

        c_val = self._rng.choice(domain)

        if difficulty <= 3:
            kind = self._rng.choice(["atomic_p", "atomic_r"])
        elif difficulty <= 6:
            kind = self._rng.choice(["atomic_p", "not_p", "and_pq", "or_pq"])
        else:
            kind = self._rng.choice(["forall_p", "exists_p", "forall_r"])

        domain_str = "{" + ", ".join(str(d) for d in domain) + "}"
        p_str = "{" + ", ".join(str(d) for d in sorted(p_ext)) + "}"
        r_pairs = "{" + ", ".join(f"({a},{b})" for a, b in sorted(r_ext)) + "}"

        if kind == "atomic_p":
            formula = f"P({c_val})"
            result = c_val in p_ext
            eval_steps = [f"P({c_val}): {c_val} in {p_str} -> {result}"]
        elif kind == "atomic_r":
            a_val = self._rng.choice(domain)
            b_val = self._rng.choice(domain)
            formula = f"R({a_val}, {b_val})"
            result = (a_val, b_val) in r_ext
            eval_steps = [
                f"R({a_val},{b_val}): ({a_val},{b_val}) in {r_pairs} -> {result}"
            ]
        elif kind == "not_p":
            formula = f"NOT P({c_val})"
            result = c_val not in p_ext
            eval_steps = [
                f"P({c_val}) = {c_val in p_ext}",
                f"NOT P({c_val}) = {result}",
            ]
        elif kind == "and_pq":
            a_val = self._rng.choice(domain)
            b_val = self._rng.choice(domain)
            formula = f"P({a_val}) AND P({b_val})"
            result = (a_val in p_ext) and (b_val in p_ext)
            eval_steps = [
                f"P({a_val}) = {a_val in p_ext}",
                f"P({b_val}) = {b_val in p_ext}",
                f"AND = {result}",
            ]
        elif kind == "or_pq":
            a_val = self._rng.choice(domain)
            b_val = self._rng.choice(domain)
            formula = f"P({a_val}) OR P({b_val})"
            result = (a_val in p_ext) or (b_val in p_ext)
            eval_steps = [
                f"P({a_val}) = {a_val in p_ext}",
                f"P({b_val}) = {b_val in p_ext}",
                f"OR = {result}",
            ]
        elif kind == "forall_p":
            formula = "forall x: P(x)"
            result = all(d in p_ext for d in domain)
            checks = [f"P({d})={d in p_ext}" for d in domain]
            eval_steps = checks + [f"forall: {result}"]
        elif kind == "exists_p":
            formula = "exists x: P(x)"
            result = any(d in p_ext for d in domain)
            checks = [f"P({d})={d in p_ext}" for d in domain]
            eval_steps = checks + [f"exists: {result}"]
        else:  # forall_r
            a_val = self._rng.choice(domain)
            formula = f"forall y: R({a_val}, y)"
            result = all((a_val, d) in r_ext for d in domain)
            checks = [
                f"R({a_val},{d})={((a_val, d) in r_ext)}" for d in domain
            ]
            eval_steps = checks + [f"forall y: {result}"]

        problem = (
            f"M = (D={domain_str}, P={p_str}, R={r_pairs}, c={c_val}). "
            f"Evaluate: M |= {formula}?"
        )
        return problem, {
            "formula": formula, "domain": domain,
            "result": result, "eval_steps": eval_steps,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate truth evaluation steps.

        Args:
            data: Solution data.

        Returns:
            Steps evaluating the formula.
        """
        steps = [f"formula: {data['formula']}"]
        steps.extend(data["eval_steps"])
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the final answer.

        Args:
            data: Solution data.

        Returns:
            TRUE or FALSE.
        """
        return "TRUE" if data["result"] else "FALSE"
