"""Compiler construction generators.

6 generators across tiers 4-6 covering tokenisation, recursive descent
parsing, FIRST/FOLLOW set computation, LL(1) parse table construction,
type checking, and lambda calculus beta reduction.
"""
from __future__ import annotations

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


# ---------------------------------------------------------------------------
# Helper classes
# ---------------------------------------------------------------------------

class _Token:
    """A single token produced by lexical analysis.

    Attributes:
        kind: Token category (NUM, ID, PLUS, STAR, LPAREN, RPAREN).
        value: Lexeme string.
    """

    def __init__(self, kind: str, value: str) -> None:
        """Initialise the token.

        Args:
            kind: Token type name.
            value: Literal text of the token.
        """
        self.kind = kind
        self.value = value

    def __repr__(self) -> str:
        """Return compact token representation."""
        if self.kind in ("NUM", "ID"):
            return f"({self.kind},{self.value})"
        return f"({self.kind})"


class _Lexer:
    """A simple lexer for arithmetic expressions with identifiers.

    Recognises integers, single-letter identifiers, and the operators
    +, *, (, ).

    Attributes:
        text: Source expression string.
    """

    _OP_MAP: dict[str, str] = {
        "+": "PLUS", "-": "MINUS", "*": "STAR", "/": "SLASH",
        "(": "LPAREN", ")": "RPAREN",
    }

    def __init__(self, text: str) -> None:
        """Initialise with a source string.

        Args:
            text: Expression to tokenise.
        """
        self.text = text

    def tokenise(self) -> list[_Token]:
        """Tokenise the expression.

        Returns:
            List of Token objects.
        """
        tokens: list[_Token] = []
        i = 0
        while i < len(self.text):
            ch = self.text[i]
            if ch.isspace():
                i += 1
            elif ch.isdigit():
                start = i
                while i < len(self.text) and self.text[i].isdigit():
                    i += 1
                tokens.append(_Token("NUM", self.text[start:i]))
            elif ch.isalpha():
                start = i
                while i < len(self.text) and self.text[i].isalpha():
                    i += 1
                tokens.append(_Token("ID", self.text[start:i]))
            elif ch in self._OP_MAP:
                tokens.append(_Token(self._OP_MAP[ch], ch))
                i += 1
            else:
                i += 1
        return tokens


class _RecursiveDescentParser:
    """A recursive descent parser for the grammar:

        E -> T + E | T
        T -> F * T | F
        F -> num | id | ( E )

    Produces a parse tree as nested parenthesised strings.

    Attributes:
        tokens: Token stream from the lexer.
        pos: Current position in token stream.
    """

    def __init__(self, tokens: list[_Token]) -> None:
        """Initialise with a token stream.

        Args:
            tokens: List of Token objects.
        """
        self.tokens = tokens
        self.pos = 0
        self.steps: list[str] = []

    def _peek(self) -> _Token | None:
        """Return current token without consuming it.

        Returns:
            Current token or None if exhausted.
        """
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def _consume(self, kind: str) -> _Token:
        """Consume and return a token of the expected kind.

        Args:
            kind: Expected token type.

        Returns:
            The consumed token.

        Raises:
            ValueError: If the current token does not match.
        """
        tok = self._peek()
        if tok is None or tok.kind != kind:
            raise ValueError(f"expected {kind}, got {tok}")
        self.pos += 1
        return tok

    def parse(self) -> str:
        """Parse the token stream and return a parse tree string.

        Returns:
            Nested parenthesised parse tree.
        """
        result = self._parse_e()
        self.steps.append(f"parse tree: {result}")
        return result

    def _parse_e(self) -> str:
        """Parse E -> T + E | T.

        Returns:
            Parse tree string for E.
        """
        left = self._parse_t()
        tok = self._peek()
        if tok and tok.kind == "PLUS":
            self._consume("PLUS")
            self.steps.append(f"E -> T + E")
            right = self._parse_e()
            return f"(+ {left} {right})"
        self.steps.append(f"E -> T")
        return left

    def _parse_t(self) -> str:
        """Parse T -> F * T | F.

        Returns:
            Parse tree string for T.
        """
        left = self._parse_f()
        tok = self._peek()
        if tok and tok.kind == "STAR":
            self._consume("STAR")
            self.steps.append(f"T -> F * T")
            right = self._parse_t()
            return f"(* {left} {right})"
        self.steps.append(f"T -> F")
        return left

    def _parse_f(self) -> str:
        """Parse F -> num | id | ( E ).

        Returns:
            Parse tree string for F.
        """
        tok = self._peek()
        if tok is None:
            raise ValueError("unexpected end of input")
        if tok.kind == "NUM":
            self._consume("NUM")
            self.steps.append(f"F -> {tok.value}")
            return tok.value
        if tok.kind == "ID":
            self._consume("ID")
            self.steps.append(f"F -> {tok.value}")
            return tok.value
        if tok.kind == "LPAREN":
            self._consume("LPAREN")
            self.steps.append("F -> ( E )")
            inner = self._parse_e()
            self._consume("RPAREN")
            return inner
        raise ValueError(f"unexpected token {tok}")


# ---------------------------------------------------------------------------
# 1. Tokenize (tier 4)
# ---------------------------------------------------------------------------

@register
class TokenizeGenerator(StepGenerator):
    """Tokenize a simple arithmetic expression into a token stream.

    Generates expressions like '3 + x * 2' and produces a sequence
    of (TYPE, value) tokens.
    """

    _TEMPLATES: list[dict] = [
        {"expr": "3 + x * 2", "desc": "addition and multiplication"},
        {"expr": "a + b", "desc": "two identifiers"},
        {"expr": "10 * y + 5", "desc": "multiply then add"},
        {"expr": "(x + 1) * 2", "desc": "parenthesised addition"},
        {"expr": "a * (b + c)", "desc": "multiply by sum"},
        {"expr": "42", "desc": "single number"},
        {"expr": "x + y + z", "desc": "chained addition"},
        {"expr": "(1 + 2) * (3 + 4)", "desc": "two parenthesised groups"},
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "tokenize"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["regex_match"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task instruction string.
        """
        return "tokenize expression into token stream"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a tokenisation problem.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        idx = difficulty % len(self._TEMPLATES)
        tmpl = self._TEMPLATES[idx]
        lexer = _Lexer(tmpl["expr"])
        tokens = lexer.tokenise()
        steps = [f"scan '{tmpl['expr']}'"]
        for tok in tokens:
            steps.append(f"emit {tok}")
        problem = f"tokenize: {tmpl['expr']}"
        return problem, {"steps": steps, "tokens": tokens}

    def _create_steps(self, solution_data: dict) -> list[str]:
        """Return the scanning steps.

        Args:
            solution_data: All computed solution information.

        Returns:
            Step strings for each token emitted.
        """
        return solution_data["steps"]

    def _create_answer(self, solution_data: dict) -> str:
        """Return the token stream.

        Args:
            solution_data: All computed solution information.

        Returns:
            Comma-separated token representations.
        """
        return ", ".join(str(t) for t in solution_data["tokens"])


# ---------------------------------------------------------------------------
# 2. Recursive Descent Parse (tier 5)
# ---------------------------------------------------------------------------

@register
class RecursiveDescentGenerator(StepGenerator):
    """Parse an expression using recursive descent and show the parse tree.

    Uses the grammar E->T+E|T, T->F*T|F, F->num|id|(E). Shows
    the parse tree as nested parenthesised notation.
    """

    _EXPRESSIONS: list[str] = [
        "3 + 2",
        "x * 2",
        "1 + x * 2",
        "a + b + c",
        "x * y + z",
        "(x + 1) * 2",
        "a * b * c",
        "1 + 2 + 3",
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "recursive_descent"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["tokenize"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task instruction string.
        """
        return "parse expression with recursive descent"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a recursive descent parsing problem.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        idx = difficulty % len(self._EXPRESSIONS)
        expr = self._EXPRESSIONS[idx]
        lexer = _Lexer(expr)
        tokens = lexer.tokenise()
        parser = _RecursiveDescentParser(tokens)
        tree = parser.parse()
        problem = f"parse: {expr} using E->T+E|T, T->F*T|F, F->num|id|(E)"
        return problem, {"steps": parser.steps, "tree": tree}

    def _create_steps(self, solution_data: dict) -> list[str]:
        """Return the parsing steps.

        Args:
            solution_data: All computed solution information.

        Returns:
            Step strings showing production choices.
        """
        return solution_data["steps"]

    def _create_answer(self, solution_data: dict) -> str:
        """Return the parse tree.

        Args:
            solution_data: All computed solution information.

        Returns:
            Nested parenthesised parse tree string.
        """
        return solution_data["tree"]


# ---------------------------------------------------------------------------
# 3. FIRST and FOLLOW Sets (tier 5)
# ---------------------------------------------------------------------------

@register
class FirstFollowSetGenerator(StepGenerator):
    """Compute FIRST and FOLLOW sets for a simple grammar.

    Given a grammar with 3-4 productions, compute FIRST(X) and
    FOLLOW(X) for each nonterminal.
    """

    _GRAMMARS: list[dict] = [
        {
            "rules": "E -> T E'; E' -> + T E' | eps; T -> id | ( E )",
            "first": {"E": {"id", "("}, "E'": {"+", "eps"}, "T": {"id", "("}},
            "follow": {"E": {"$", ")"}, "E'": {"$", ")"}, "T": {"+", "$", ")"}},
        },
        {
            "rules": "S -> A B; A -> a | eps; B -> b | eps",
            "first": {"S": {"a", "b", "eps"}, "A": {"a", "eps"}, "B": {"b", "eps"}},
            "follow": {"S": {"$"}, "A": {"b", "$"}, "B": {"$"}},
        },
        {
            "rules": "S -> a B | b A; A -> a | a S | b A A; B -> b | b S | a B B",
            "first": {"S": {"a", "b"}, "A": {"a", "b"}, "B": {"a", "b"}},
            "follow": {"S": {"$"}, "A": {"$"}, "B": {"$"}},
        },
        {
            "rules": "S -> A a; A -> B d | eps; B -> b | eps",
            "first": {"S": {"b", "d", "a"}, "A": {"b", "d", "eps"}, "B": {"b", "eps"}},
            "follow": {"S": {"$"}, "A": {"a"}, "B": {"d"}},
        },
        {
            "rules": "E -> T X; X -> + T X | eps; T -> ( E ) | id",
            "first": {"E": {"(", "id"}, "X": {"+", "eps"}, "T": {"(", "id"}},
            "follow": {"E": {"$", ")"}, "X": {"$", ")"}, "T": {"+", "$", ")"}},
        },
        {
            "rules": "S -> A B c; A -> a | eps; B -> b | eps",
            "first": {"S": {"a", "b", "c"}, "A": {"a", "eps"}, "B": {"b", "eps"}},
            "follow": {"S": {"$"}, "A": {"b", "c"}, "B": {"c"}},
        },
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "first_follow_set"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["cfg_derivation"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task instruction string.
        """
        return "compute FIRST and FOLLOW sets for grammar"

    def _format_set(self, s: set[str]) -> str:
        """Format a set as a sorted brace-enclosed string.

        Args:
            s: Set of symbols.

        Returns:
            Formatted set string like {a, b}.
        """
        return "{" + ", ".join(sorted(s)) + "}"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a FIRST/FOLLOW set computation problem.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        idx = difficulty % len(self._GRAMMARS)
        grammar = self._GRAMMARS[idx]
        problem = f"grammar: {grammar['rules']}"

        steps = []
        for nt in sorted(grammar["first"]):
            steps.append(
                f"FIRST({nt}) = {self._format_set(grammar['first'][nt])}"
            )
        for nt in sorted(grammar["follow"]):
            steps.append(
                f"FOLLOW({nt}) = {self._format_set(grammar['follow'][nt])}"
            )

        return problem, {
            "steps": steps,
            "first": grammar["first"],
            "follow": grammar["follow"],
        }

    def _create_steps(self, solution_data: dict) -> list[str]:
        """Return the FIRST/FOLLOW computation steps.

        Args:
            solution_data: All computed solution information.

        Returns:
            Step strings for each set.
        """
        return solution_data["steps"]

    def _create_answer(self, solution_data: dict) -> str:
        """Return a compact summary of FIRST and FOLLOW sets.

        Args:
            solution_data: All computed solution information.

        Returns:
            Summary string.
        """
        parts = []
        for nt in sorted(solution_data["first"]):
            parts.append(
                f"FIRST({nt})={self._format_set(solution_data['first'][nt])}"
            )
        for nt in sorted(solution_data["follow"]):
            parts.append(
                f"FOLLOW({nt})={self._format_set(solution_data['follow'][nt])}"
            )
        return "; ".join(parts)

    def _format_set(self, s: set[str]) -> str:
        """Format a set as a sorted brace-enclosed string.

        Args:
            s: Set of symbols.

        Returns:
            Formatted set string.
        """
        return "{" + ",".join(sorted(s)) + "}"


# ---------------------------------------------------------------------------
# 4. LL(1) Parse Table (tier 6)
# ---------------------------------------------------------------------------

@register
class LL1ParseTableGenerator(StepGenerator):
    """Build an LL(1) parse table from FIRST/FOLLOW sets.

    Given a grammar and its FIRST/FOLLOW sets, construct the LL(1)
    parse table and identify any conflicts.
    """

    _TEMPLATES: list[dict] = [
        {
            "rules": "E -> T E'; E' -> + T E' | eps; T -> id | ( E )",
            "table": {
                ("E", "id"): "E -> T E'",
                ("E", "("): "E -> T E'",
                ("E'", "+"): "E' -> + T E'",
                ("E'", ")"): "E' -> eps",
                ("E'", "$"): "E' -> eps",
                ("T", "id"): "T -> id",
                ("T", "("): "T -> ( E )",
            },
            "conflict": False,
        },
        {
            "rules": "S -> A B; A -> a | eps; B -> b | eps",
            "table": {
                ("S", "a"): "S -> A B",
                ("S", "b"): "S -> A B",
                ("S", "$"): "S -> A B",
                ("A", "a"): "A -> a",
                ("A", "b"): "A -> eps",
                ("A", "$"): "A -> eps",
                ("B", "b"): "B -> b",
                ("B", "$"): "B -> eps",
            },
            "conflict": False,
        },
        {
            "rules": "S -> a S | a",
            "table": {
                ("S", "a"): "CONFLICT: S->aS / S->a",
            },
            "conflict": True,
        },
        {
            "rules": "S -> A B c; A -> a | eps; B -> b | eps",
            "table": {
                ("S", "a"): "S -> A B c",
                ("S", "b"): "S -> A B c",
                ("S", "c"): "S -> A B c",
                ("A", "a"): "A -> a",
                ("A", "b"): "A -> eps",
                ("A", "c"): "A -> eps",
                ("B", "b"): "B -> b",
                ("B", "c"): "B -> eps",
            },
            "conflict": False,
        },
        {
            "rules": "E -> T X; X -> + T X | eps; T -> ( E ) | id",
            "table": {
                ("E", "("): "E -> T X",
                ("E", "id"): "E -> T X",
                ("X", "+"): "X -> + T X",
                ("X", ")"): "X -> eps",
                ("X", "$"): "X -> eps",
                ("T", "("): "T -> ( E )",
                ("T", "id"): "T -> id",
            },
            "conflict": False,
        },
        {
            "rules": "S -> i E t S S' | a; S' -> e S | eps; E -> b",
            "table": {
                ("S", "i"): "S -> i E t S S'",
                ("S", "a"): "S -> a",
                ("S'", "e"): "CONFLICT: S'->eS / S'->eps",
                ("S'", "$"): "S' -> eps",
                ("E", "b"): "E -> b",
            },
            "conflict": True,
        },
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "ll1_parse_table"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["first_follow_set"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task instruction string.
        """
        return "build LL(1) parse table from grammar"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an LL(1) parse table construction problem.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        idx = difficulty % len(self._TEMPLATES)
        tmpl = self._TEMPLATES[idx]
        problem = f"grammar: {tmpl['rules']}; build LL(1) table"

        steps = []
        for (nt, terminal), entry in sorted(tmpl["table"].items()):
            steps.append(f"M[{nt},{terminal}] = {entry}")

        if tmpl["conflict"]:
            steps.append("grammar is NOT LL(1)")
        else:
            steps.append("no conflicts, grammar is LL(1)")

        return problem, {
            "steps": steps,
            "table": tmpl["table"],
            "conflict": tmpl["conflict"],
        }

    def _create_steps(self, solution_data: dict) -> list[str]:
        """Return the parse table construction steps.

        Args:
            solution_data: All computed solution information.

        Returns:
            Step strings for each table entry.
        """
        return solution_data["steps"]

    def _create_answer(self, solution_data: dict) -> str:
        """Return the LL(1) verdict.

        Args:
            solution_data: All computed solution information.

        Returns:
            LL(1) status and conflict info if applicable.
        """
        if solution_data["conflict"]:
            conflicts = [
                f"M[{nt},{t}]={v}"
                for (nt, t), v in sorted(solution_data["table"].items())
                if "CONFLICT" in v
            ]
            return f"NOT LL(1): {'; '.join(conflicts)}"
        return "LL(1): no conflicts"


# ---------------------------------------------------------------------------
# 5. Type Check (tier 5)
# ---------------------------------------------------------------------------

@register
class TypeCheckGenerator(StepGenerator):
    """Type-check a simple expression with int, float, and bool types.

    Rules: int+int=int, int+float=float, float+float=float,
    bool&&bool=bool, bool||bool=bool. Reports the result type or error.
    """

    _RULES: dict[tuple[str, str, str], str] = {
        ("int", "+", "int"): "int",
        ("int", "+", "float"): "float",
        ("float", "+", "int"): "float",
        ("float", "+", "float"): "float",
        ("int", "*", "int"): "int",
        ("int", "*", "float"): "float",
        ("float", "*", "int"): "float",
        ("float", "*", "float"): "float",
        ("int", "-", "int"): "int",
        ("int", "-", "float"): "float",
        ("float", "-", "int"): "float",
        ("float", "-", "float"): "float",
        ("bool", "&&", "bool"): "bool",
        ("bool", "||", "bool"): "bool",
    }

    _EXPRESSIONS: list[dict] = [
        {"expr": "3 + 2", "types": ["int", "int"], "op": "+"},
        {"expr": "3 + 2.0", "types": ["int", "float"], "op": "+"},
        {"expr": "1.5 * 2", "types": ["float", "int"], "op": "*"},
        {"expr": "true && false", "types": ["bool", "bool"], "op": "&&"},
        {"expr": "true || true", "types": ["bool", "bool"], "op": "||"},
        {"expr": "3 + true", "types": ["int", "bool"], "op": "+"},
        {"expr": "1.0 - 0.5", "types": ["float", "float"], "op": "-"},
        {"expr": "true && 1", "types": ["bool", "int"], "op": "&&"},
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "type_check"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["recursive_descent"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task instruction string.
        """
        return "type-check expression"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a type-checking problem.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        idx = difficulty % len(self._EXPRESSIONS)
        tmpl = self._EXPRESSIONS[idx]
        lhs_type = tmpl["types"][0]
        rhs_type = tmpl["types"][1]
        op = tmpl["op"]

        key = (lhs_type, op, rhs_type)
        result_type = self._RULES.get(key)

        steps = [
            f"lhs: {lhs_type}",
            f"op: {op}",
            f"rhs: {rhs_type}",
        ]

        if result_type is not None:
            steps.append(f"rule: {lhs_type} {op} {rhs_type} -> {result_type}")
            answer = f"type={result_type}"
        else:
            steps.append(
                f"no rule for {lhs_type} {op} {rhs_type}"
            )
            answer = f"TYPE ERROR: {lhs_type} {op} {rhs_type}"

        problem = f"type-check: {tmpl['expr']}"
        return problem, {"steps": steps, "answer": answer}

    def _create_steps(self, solution_data: dict) -> list[str]:
        """Return the type-checking analysis steps.

        Args:
            solution_data: All computed solution information.

        Returns:
            Step strings showing type inference.
        """
        return solution_data["steps"]

    def _create_answer(self, solution_data: dict) -> str:
        """Return the type or error.

        Args:
            solution_data: All computed solution information.

        Returns:
            Result type or type error.
        """
        return solution_data["answer"]


# ---------------------------------------------------------------------------
# 6. Lambda Calculus Beta Reduction (tier 6)
# ---------------------------------------------------------------------------

@register
class LambdaReduceGenerator(StepGenerator):
    """Perform one step of beta reduction on a lambda calculus term.

    Given (lambda x. M) N, compute M[x:=N] using simple substitution
    with no variable capture (terms are chosen to be capture-free).
    """

    _TEMPLATES: list[dict] = [
        {
            "term": "(lam x. x) a",
            "var": "x", "body": "x", "arg": "a",
            "result": "a",
            "sub_steps": ["x[x:=a] = a"],
        },
        {
            "term": "(lam x. x x) y",
            "var": "x", "body": "x x", "arg": "y",
            "result": "y y",
            "sub_steps": ["x[x:=y] = y", "x[x:=y] = y"],
        },
        {
            "term": "(lam x. y) z",
            "var": "x", "body": "y", "arg": "z",
            "result": "y",
            "sub_steps": ["y[x:=z] = y (x not free in y)"],
        },
        {
            "term": "(lam f. f a) (lam x. x)",
            "var": "f", "body": "f a", "arg": "(lam x. x)",
            "result": "(lam x. x) a",
            "sub_steps": ["f[f:=(lam x. x)] = (lam x. x)"],
        },
        {
            "term": "(lam x. x y x) a",
            "var": "x", "body": "x y x", "arg": "a",
            "result": "a y a",
            "sub_steps": ["x[x:=a] = a", "y unchanged", "x[x:=a] = a"],
        },
        {
            "term": "(lam x. (lam y. x)) a",
            "var": "x", "body": "(lam y. x)", "arg": "a",
            "result": "(lam y. a)",
            "sub_steps": ["x[x:=a] inside (lam y. x) = (lam y. a)"],
        },
        {
            "term": "(lam x. x) (lam y. y)",
            "var": "x", "body": "x", "arg": "(lam y. y)",
            "result": "(lam y. y)",
            "sub_steps": ["x[x:=(lam y. y)] = (lam y. y)"],
        },
        {
            "term": "(lam f. f (f a)) (lam x. x)",
            "var": "f", "body": "f (f a)", "arg": "(lam x. x)",
            "result": "(lam x. x) ((lam x. x) a)",
            "sub_steps": [
                "f[f:=(lam x. x)] = (lam x. x)",
                "f[f:=(lam x. x)] in (f a) = (lam x. x) a",
            ],
        },
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "lambda_reduce"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["expression_simplify"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task instruction string.
        """
        return "perform one beta reduction step"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a beta reduction problem.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        idx = difficulty % len(self._TEMPLATES)
        tmpl = self._TEMPLATES[idx]
        problem = f"beta-reduce: {tmpl['term']}"
        return problem, {
            "var": tmpl["var"],
            "body": tmpl["body"],
            "arg": tmpl["arg"],
            "sub_steps": tmpl["sub_steps"],
            "result": tmpl["result"],
        }

    def _create_steps(self, solution_data: dict) -> list[str]:
        """Return the substitution steps.

        Args:
            solution_data: All computed solution information.

        Returns:
            Step strings showing the substitution process.
        """
        steps = [
            f"redex: (lam {solution_data['var']}. "
            f"{solution_data['body']}) {solution_data['arg']}",
            f"substitute {solution_data['var']} := {solution_data['arg']}",
        ]
        steps.extend(solution_data["sub_steps"])
        return steps

    def _create_answer(self, solution_data: dict) -> str:
        """Return the reduced term.

        Args:
            solution_data: All computed solution information.

        Returns:
            Result of beta reduction.
        """
        return solution_data["result"]
