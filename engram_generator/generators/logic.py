"""Logic and formal reasoning generators.

Adds 13 generators across tiers 0-4 covering boolean algebra,
propositional logic, deduction, and constraint puzzles.
"""
from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


# ── TIER 0 ─────────────────────────────────────────────────────────

@register
class BooleanEvalGenerator(StepGenerator):
    """Evaluate boolean expressions with AND, OR, NOT."""

    @property
    def task_name(self) -> str:
        return "boolean_eval"

    @property
    def tier(self) -> int:
        return 0

    def task_description(self, difficulty: int) -> str:
        return "evaluate boolean expression"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        n_ops = min(1 + difficulty, 6)
        vals = [self._rng.choice([True, False]) for _ in range(n_ops + 1)]
        ops = [self._rng.choice(["AND", "OR"]) for _ in range(n_ops)]

        expr_parts = [str(vals[0])]
        for i in range(n_ops):
            expr_parts.append(ops[i])
            expr_parts.append(str(vals[i + 1]))

        if difficulty >= 3 and self._rng.random() < 0.5:
            idx = self._rng.randint(0, len(vals) - 1)
            vals[idx] = not vals[idx]
            expr_parts = [str(vals[0])]
            for i in range(n_ops):
                expr_parts.append(ops[i])
                expr_parts.append(str(vals[i + 1]))
            expr_parts.insert(self._rng.randint(0, len(expr_parts)), "NOT")

        result = vals[0]
        steps = [f"start: {vals[0]}"]
        for i in range(n_ops):
            if ops[i] == "AND":
                result = result and vals[i + 1]
            else:
                result = result or vals[i + 1]
            steps.append(f"{ops[i]} {vals[i + 1]} = {result}")

        expr = " ".join(expr_parts)
        return expr, {"result": result, "eval_steps": steps}

    def _create_steps(self, sd: dict) -> list[str]:
        return sd["eval_steps"]

    def _create_answer(self, sd: dict) -> str:
        return str(sd["result"])


@register
class TruthTableGenerator(StepGenerator):
    """Evaluate a logic formula for given variable assignments."""

    @property
    def task_name(self) -> str:
        return "truth_table"

    @property
    def tier(self) -> int:
        return 0

    def task_description(self, difficulty: int) -> str:
        return "evaluate truth table row"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        n_vars = min(2 + difficulty // 2, 4)
        var_names = ["p", "q", "r", "s"][:n_vars]
        vals = {v: self._rng.choice([True, False]) for v in var_names}

        formulas = [
            ("p AND q", lambda v: v["p"] and v["q"]),
            ("p OR q", lambda v: v["p"] or v["q"]),
            ("NOT p AND q", lambda v: (not v["p"]) and v["q"]),
            ("p AND (q OR r)", lambda v: v["p"] and (v.get("q", False) or v.get("r", False))),
            ("(p OR q) AND (NOT r)", lambda v: (v["p"] or v["q"]) and not v.get("r", False)),
            ("p AND q AND r", lambda v: v["p"] and v.get("q", False) and v.get("r", False)),
            ("(NOT p) OR (q AND r)", lambda v: (not v["p"]) or (v.get("q", False) and v.get("r", False))),
        ]

        valid = [(f, fn) for f, fn in formulas if all(
            c not in f for c in var_names[n_vars:]
        )]
        formula, fn = self._rng.choice(valid[:min(len(valid), difficulty + 2)])
        result = fn(vals)

        assign_str = ", ".join(f"{k}={v}" for k, v in vals.items())
        return (
            f"{formula} where {assign_str}",
            {"formula": formula, "vals": vals, "result": result},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        steps = [f"{k} = {v}" for k, v in sd["vals"].items()]
        steps.append(f"{sd['formula']} = {sd['result']}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        return str(sd["result"])


@register
class NegationGenerator(StepGenerator):
    """Apply NOT and De Morgan's laws."""

    @property
    def task_name(self) -> str:
        return "negation"

    @property
    def tier(self) -> int:
        return 0

    def task_description(self, difficulty: int) -> str:
        return "negate expression"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        mode = self._rng.choice(["simple", "demorgan_and", "demorgan_or", "double"])

        a = self._rng.choice([True, False])
        b = self._rng.choice([True, False])

        if mode == "simple":
            expr = f"NOT {a}"
            result = not a
            steps = [f"NOT {a} = {result}"]
        elif mode == "demorgan_and":
            expr = f"NOT ({a} AND {b})"
            result = (not a) or (not b)
            steps = [
                f"De Morgan: NOT (A AND B) = (NOT A) OR (NOT B)",
                f"(NOT {a}) OR (NOT {b}) = {not a} OR {not b} = {result}",
            ]
        elif mode == "demorgan_or":
            expr = f"NOT ({a} OR {b})"
            result = (not a) and (not b)
            steps = [
                f"De Morgan: NOT (A OR B) = (NOT A) AND (NOT B)",
                f"(NOT {a}) AND (NOT {b}) = {not a} AND {not b} = {result}",
            ]
        else:
            expr = f"NOT (NOT {a})"
            result = a
            steps = [f"double negation: NOT (NOT {a}) = {a}"]

        return expr, {"result": result, "steps": steps}

    def _create_steps(self, sd: dict) -> list[str]:
        return sd["steps"]

    def _create_answer(self, sd: dict) -> str:
        return str(sd["result"])


# ── TIER 1 ─────────────────────────────────────────────────────────

@register
class ImplicationGenerator(StepGenerator):
    """Evaluate material implication p -> q."""

    @property
    def task_name(self) -> str:
        return "implication"

    @property
    def tier(self) -> int:
        return 1

    @property
    def prerequisites(self) -> list[str]:
        return ["boolean_eval"]

    def task_description(self, difficulty: int) -> str:
        return "evaluate implication"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        p = self._rng.choice([True, False])
        q = self._rng.choice([True, False])
        result = (not p) or q

        if difficulty >= 3:
            r = self._rng.choice([True, False])
            expr = f"({p} -> {q}) AND {r}"
            result = result and r
            return expr, {"p": p, "q": q, "r": r, "result": result, "compound": True}

        return f"{p} -> {q}", {"p": p, "q": q, "result": result, "compound": False}

    def _create_steps(self, sd: dict) -> list[str]:
        imp = (not sd["p"]) or sd["q"]
        steps = [
            f"p -> q = (NOT p) OR q",
            f"(NOT {sd['p']}) OR {sd['q']} = {not sd['p']} OR {sd['q']} = {imp}",
        ]
        if sd.get("compound"):
            steps.append(f"{imp} AND {sd['r']} = {sd['result']}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        return str(sd["result"])


@register
class BiconditionalGenerator(StepGenerator):
    """Evaluate biconditional p <-> q."""

    @property
    def task_name(self) -> str:
        return "biconditional"

    @property
    def tier(self) -> int:
        return 1

    @property
    def prerequisites(self) -> list[str]:
        return ["implication"]

    def task_description(self, difficulty: int) -> str:
        return "evaluate biconditional"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        p = self._rng.choice([True, False])
        q = self._rng.choice([True, False])
        result = p == q
        return f"{p} <-> {q}", {"p": p, "q": q, "result": result}

    def _create_steps(self, sd: dict) -> list[str]:
        pq = (not sd["p"]) or sd["q"]
        qp = (not sd["q"]) or sd["p"]
        return [
            f"p <-> q = (p -> q) AND (q -> p)",
            f"p -> q = {pq}",
            f"q -> p = {qp}",
            f"{pq} AND {qp} = {sd['result']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        return str(sd["result"])


@register
class SyllogismGenerator(StepGenerator):
    """Determine if a syllogism is valid and state the conclusion."""

    @property
    def task_name(self) -> str:
        return "syllogism"

    @property
    def tier(self) -> int:
        return 1

    @property
    def prerequisites(self) -> list[str]:
        return ["implication"]

    def task_description(self, difficulty: int) -> str:
        return "evaluate syllogism"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        categories = [
            ("mammals", "animals", "dogs"),
            ("birds", "vertebrates", "eagles"),
            ("roses", "flowers", "red roses"),
            ("squares", "rectangles", "unit squares"),
            ("primes", "integers", "twin primes"),
            ("planets", "celestial bodies", "gas giants"),
        ]
        A, B, C = self._rng.choice(categories[:min(len(categories), difficulty + 2)])

        valid = self._rng.choice([True, True, True, False])
        if valid:
            p1 = f"all {A} are {B}"
            p2 = f"all {C} are {A}"
            conclusion = f"all {C} are {B}"
        else:
            p1 = f"all {A} are {B}"
            p2 = f"all {C} are {B}"
            conclusion = f"all {C} are {A}"

        return (
            f"premise 1: {p1}; premise 2: {p2}; conclusion: {conclusion}",
            {"p1": p1, "p2": p2, "conclusion": conclusion, "valid": valid},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        return [
            f"premise 1: {sd['p1']}",
            f"premise 2: {sd['p2']}",
            f"conclusion: {sd['conclusion']}",
            f"valid: {'yes — follows by transitivity' if sd['valid'] else 'no — undistributed middle'}",
        ]

    def _create_answer(self, sd: dict) -> str:
        return "VALID" if sd["valid"] else "INVALID"


# ── TIER 2 ─────────────────────────────────────────────────────────

@register
class PropositionalEvalGenerator(StepGenerator):
    """Evaluate compound propositional formulas."""

    @property
    def task_name(self) -> str:
        return "propositional_eval"

    @property
    def tier(self) -> int:
        return 2

    @property
    def prerequisites(self) -> list[str]:
        return ["boolean_eval", "implication"]

    def task_description(self, difficulty: int) -> str:
        return "evaluate propositional formula"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        p = self._rng.choice([True, False])
        q = self._rng.choice([True, False])
        r = self._rng.choice([True, False])

        formulas = [
            (f"(p -> q) AND r", (not p or q) and r),
            (f"p OR (q -> r)", p or (not q or r)),
            (f"(NOT p) -> (q AND r)", p or (q and r)),
            (f"(p AND q) -> r", not (p and q) or r),
            (f"(p -> q) -> r", not (not p or q) or r),
            (f"(p <-> q) OR r", (p == q) or r),
        ]

        formula, result = self._rng.choice(formulas[:min(len(formulas), difficulty + 2)])
        assign = f"p={p}, q={q}, r={r}"
        return (
            f"{formula} where {assign}",
            {"formula": formula, "p": p, "q": q, "r": r, "result": result},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        return [
            f"p={sd['p']}, q={sd['q']}, r={sd['r']}",
            f"substitute into {sd['formula']}",
            f"result = {sd['result']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        return str(sd["result"])


@register
class LogicalEquivalenceGenerator(StepGenerator):
    """Determine if two formulas are logically equivalent."""

    @property
    def task_name(self) -> str:
        return "logical_equivalence"

    @property
    def tier(self) -> int:
        return 2

    @property
    def prerequisites(self) -> list[str]:
        return ["propositional_eval"]

    def task_description(self, difficulty: int) -> str:
        return "check logical equivalence"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        pairs = [
            ("p -> q", "NOT p OR q", True),
            ("NOT (p AND q)", "NOT p OR NOT q", True),
            ("NOT (p OR q)", "NOT p AND NOT q", True),
            ("p -> q", "q -> p", False),
            ("p -> q", "NOT q -> NOT p", True),
            ("p AND q", "p OR q", False),
            ("p <-> q", "(p -> q) AND (q -> p)", True),
        ]
        f1, f2, equiv = self._rng.choice(pairs[:min(len(pairs), difficulty + 3)])
        return (
            f"is '{f1}' equivalent to '{f2}'?",
            {"f1": f1, "f2": f2, "equiv": equiv},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        return [
            f"formula 1: {sd['f1']}",
            f"formula 2: {sd['f2']}",
            f"equivalent: {sd['equiv']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        return "YES" if sd["equiv"] else "NO"


@register
class ContrapositiveGenerator(StepGenerator):
    """State the contrapositive of a conditional."""

    @property
    def task_name(self) -> str:
        return "contrapositive"

    @property
    def tier(self) -> int:
        return 2

    @property
    def prerequisites(self) -> list[str]:
        return ["implication", "negation"]

    def task_description(self, difficulty: int) -> str:
        return "find the contrapositive"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        statements = [
            ("it rains", "the ground is wet"),
            ("x > 5", "x > 3"),
            ("n is even", "n^2 is even"),
            ("f is differentiable", "f is continuous"),
            ("AB is parallel to CD", "angles are equal"),
            ("the function is bounded", "the integral converges"),
        ]
        p, q = self._rng.choice(statements[:min(len(statements), difficulty + 2)])
        return (
            f"if {p} then {q}",
            {"p": p, "q": q, "not_p": f"NOT ({p})", "not_q": f"NOT ({q})"},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        return [
            f"original: if {sd['p']} then {sd['q']}",
            f"contrapositive: if {sd['not_q']} then {sd['not_p']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        return f"if {sd['not_q']} then {sd['not_p']}"


# ── TIER 3 ─────────────────────────────────────────────────────────

@register
class DeductionChainGenerator(StepGenerator):
    """Derive a conclusion through a chain of implications."""

    @property
    def task_name(self) -> str:
        return "deduction_chain"

    @property
    def tier(self) -> int:
        return 3

    @property
    def prerequisites(self) -> list[str]:
        return ["propositional_eval", "contrapositive"]

    def task_description(self, difficulty: int) -> str:
        return "follow deduction chain"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        n = min(2 + difficulty, 6)
        props = [chr(ord("A") + i) for i in range(n + 1)]
        chain = [f"{props[i]} -> {props[i + 1]}" for i in range(n)]
        given = props[0]
        conclusion = props[-1]
        return (
            f"given: {given} is True; {'; '.join(chain)}. what is {conclusion}?",
            {"chain": chain, "props": props, "given": given, "conclusion": conclusion},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        steps = [f"{sd['given']} is True"]
        for i in range(len(sd["chain"])):
            steps.append(
                f"by {sd['chain'][i]}: {sd['props'][i + 1]} is True"
            )
        return steps

    def _create_answer(self, sd: dict) -> str:
        return f"{sd['conclusion']} is True"


@register
class QuantifierEvalGenerator(StepGenerator):
    """Evaluate universal/existential quantifiers over finite domains."""

    @property
    def task_name(self) -> str:
        return "quantifier_eval"

    @property
    def tier(self) -> int:
        return 3

    @property
    def prerequisites(self) -> list[str]:
        return ["boolean_eval"]

    def task_description(self, difficulty: int) -> str:
        return "evaluate quantified statement"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        size = min(3 + difficulty, 10)
        domain = list(range(1, size + 1))

        predicates = [
            ("x > 0", lambda x: x > 0),
            ("x is even", lambda x: x % 2 == 0),
            ("x < 10", lambda x: x < 10),
            ("x^2 > x", lambda x: x * x > x),
            ("x is prime", lambda x: x > 1 and all(x % d != 0 for d in range(2, x))),
        ]

        quantifier = self._rng.choice(["forall", "exists"])
        pred_str, pred_fn = self._rng.choice(predicates[:min(len(predicates), difficulty + 2)])
        checks = [(x, pred_fn(x)) for x in domain]

        if quantifier == "forall":
            result = all(v for _, v in checks)
        else:
            result = any(v for _, v in checks)

        domain_str = "{" + ", ".join(str(x) for x in domain) + "}"
        return (
            f"{quantifier} x in {domain_str}: {pred_str}",
            {"quantifier": quantifier, "pred": pred_str,
             "domain": domain, "checks": checks, "result": result},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        steps = []
        for x, v in sd["checks"]:
            steps.append(f"x={x}: {sd['pred']} = {v}")
        steps.append(f"{sd['quantifier']}: {sd['result']}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        return str(sd["result"])


# ── TIER 4 ─────────────────────────────────────────────────────────

@register
class KnightsKnavesGenerator(StepGenerator):
    """Solve knights and knaves puzzles."""

    @property
    def task_name(self) -> str:
        return "knights_knaves"

    @property
    def tier(self) -> int:
        return 4

    @property
    def prerequisites(self) -> list[str]:
        return ["deduction_chain"]

    def task_description(self, difficulty: int) -> str:
        return "solve knights and knaves"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        n = min(2 + difficulty // 2, 4)
        names = ["A", "B", "C", "D"][:n]
        types = {name: self._rng.choice(["knight", "knave"]) for name in names}

        statements = []
        for name in names:
            target = self._rng.choice([n for n in names if n != name])
            claim_type = self._rng.choice(["knight", "knave"])
            statement = f"{name} says: '{target} is a {claim_type}'"

            if types[name] == "knight":
                consistent = (types[target] == claim_type)
            else:
                consistent = (types[target] != claim_type)

            if not consistent:
                claim_type = "knave" if claim_type == "knight" else "knight"
                statement = f"{name} says: '{target} is a {claim_type}'"

            statements.append(statement)

        problem = "; ".join(statements)
        return problem, {"types": types, "statements": statements}

    def _create_steps(self, sd: dict) -> list[str]:
        steps = []
        for name, t in sd["types"].items():
            steps.append(f"assume {name} is {t}")
        steps.append("check consistency with all statements")
        return steps

    def _create_answer(self, sd: dict) -> str:
        parts = [f"{n}={t}" for n, t in sorted(sd["types"].items())]
        return ", ".join(parts)


@register
class LogicalPuzzleGenerator(StepGenerator):
    """Solve constraint satisfaction puzzles."""

    @property
    def task_name(self) -> str:
        return "logical_puzzle"

    @property
    def tier(self) -> int:
        return 4

    @property
    def prerequisites(self) -> list[str]:
        return ["deduction_chain"]

    def task_description(self, difficulty: int) -> str:
        return "solve logic puzzle"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        n = min(2 + difficulty // 2, 4)
        names = ["Alice", "Bob", "Carol", "Dave"][:n]
        colors = ["red", "blue", "green", "yellow"][:n]
        self._rng.shuffle(colors)
        assignment = dict(zip(names, colors))

        clues = []
        for i, name in enumerate(names):
            c = assignment[name]
            other = self._rng.choice([n for n in names if n != name])
            oc = assignment[other]
            wrong = self._rng.choice([col for col in colors if col != oc])
            clues.append(f"{name} has {c}")
            clues.append(f"{other} does not have {wrong}")

        self._rng.shuffle(clues)
        clues = clues[:n + 1]
        problem = "; ".join(clues)
        return problem, {"assignment": assignment, "clues": clues}

    def _create_steps(self, sd: dict) -> list[str]:
        steps = [f"clue: {c}" for c in sd["clues"]]
        steps.append("eliminate and assign")
        return steps

    def _create_answer(self, sd: dict) -> str:
        parts = [f"{n}={c}" for n, c in sorted(sd["assignment"].items())]
        return ", ".join(parts)
