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
        """Return the unique task identifier."""
        return "boolean_eval"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 0

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description."""
        return "evaluate boolean expression"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        n_ops = min(1 + difficulty, 6)
        vals = [self._rng.choice([True, False]) for _ in range(n_ops + 1)]
        ops = [self._rng.choice(["AND", "OR"]) for _ in range(n_ops)]
        not_positions: set[int] = set()

        if difficulty >= 3 and self._rng.random() < 0.5:
            n_nots = 1 + (difficulty >= 5)
            for _ in range(n_nots):
                pos = self._rng.randint(0, n_ops)
                not_positions.add(pos)

        effective_vals = list(vals)
        for pos in not_positions:
            effective_vals[pos] = not effective_vals[pos]

        expr_parts = []
        for i, val in enumerate(vals):
            if i in not_positions:
                expr_parts.append(f"NOT {val}")
            else:
                expr_parts.append(str(val))
            if i < n_ops:
                expr_parts.append(ops[i])

        result = effective_vals[0]
        steps = []
        if not_positions and 0 in not_positions:
            steps.append(f"NOT {vals[0]} = {effective_vals[0]}")
        steps.append(f"start: {effective_vals[0]}")
        for i in range(n_ops):
            operand = effective_vals[i + 1]
            if (i + 1) in not_positions:
                steps.append(f"NOT {vals[i + 1]} = {operand}")
            if ops[i] == "AND":
                result = result and operand
            else:
                result = result or operand
            steps.append(f"{ops[i]} {operand} = {result}")

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
        """Return the unique task identifier."""
        return "truth_table"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 0

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description."""
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

    _MODES = ["simple", "demorgan_and", "demorgan_or", "double",
              "triple", "nested_demorgan", "demorgan_chain"]
    _VAR_POOL = ["P", "Q", "R", "S", "T", "U", "V", "W"]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "negation"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 0

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description."""
        return "negate expression"

    def _select_mode(self, difficulty: int) -> tuple[str, list[str], bool, bool]:
        """Select negation mode and randomise variables/values.

        Args:
            difficulty: Controls expression complexity.

        Returns:
            Tuple of (mode, chosen_vars, a_value, b_value).
        """
        chosen = self._rng.sample(
            self._VAR_POOL, min(2 + difficulty, len(self._VAR_POOL)))
        a = self._rng.choice([True, False])
        b = self._rng.choice([True, False])
        mode = self._rng.choice(
            self._MODES[:min(len(self._MODES), 3 + difficulty)])
        return mode, chosen, a, b

    def _evaluate_simple(self, v1: str, a: bool) -> tuple[str, bool, list[str]]:
        """Evaluate simple NOT and double/triple negation modes.

        Args:
            v1: Variable name.
            a: Truth value of the variable.

        Returns:
            Tuple of (expression, result, steps).
        """
        result = not a
        return f"NOT {v1} (where {v1}={a})", result, [f"NOT {a} = {result}"]

    def _evaluate_demorgan(self, mode: str, v1: str, v2: str,
                           a: bool, b: bool) -> tuple[str, bool, list[str]]:
        """Evaluate De Morgan's law modes (AND/OR).

        Args:
            mode: Either 'demorgan_and' or 'demorgan_or'.
            v1: First variable name.
            v2: Second variable name.
            a: Truth value of v1.
            b: Truth value of v2.

        Returns:
            Tuple of (expression, result, steps).
        """
        if mode == "demorgan_and":
            op, neg_op = "AND", "OR"
            result = (not a) or (not b)
        else:
            op, neg_op = "OR", "AND"
            result = (not a) and (not b)
        expr = f"NOT ({v1} {op} {v2}) (where {v1}={a}, {v2}={b})"
        steps = [
            f"De Morgan: NOT ({v1} {op} {v2}) = (NOT {v1}) {neg_op} (NOT {v2})",
            f"(NOT {a}) {neg_op} (NOT {b}) = {not a} {neg_op} {not b} = {result}",
        ]
        return expr, result, steps

    def _evaluate_multi_negation(self, mode: str, v1: str,
                                 a: bool) -> tuple[str, bool, list[str]]:
        """Evaluate double or triple negation.

        Args:
            mode: Either 'double' or 'triple'.
            v1: Variable name.
            a: Truth value.

        Returns:
            Tuple of (expression, result, steps).
        """
        if mode == "double":
            return (f"NOT (NOT {v1}) (where {v1}={a})", a,
                    [f"double negation: NOT (NOT {a}) = {a}"])
        result = not a
        return (f"NOT (NOT (NOT {v1})) (where {v1}={a})", result, [
            f"inner: NOT {a} = {not a}",
            f"middle: NOT {not a} = {a}",
            f"outer: NOT {a} = {not a}",
        ])

    def _evaluate_nested(self, mode: str, chosen: list[str],
                         a: bool, b: bool) -> tuple[str, bool, list[str]]:
        """Evaluate nested De Morgan or De Morgan chain modes.

        Args:
            mode: Either 'nested_demorgan' or 'demorgan_chain'.
            chosen: List of chosen variable names.
            a: Truth value of first variable.
            b: Truth value of second variable.

        Returns:
            Tuple of (expression, result, steps).
        """
        v1, v2 = chosen[0], chosen[1]
        c = self._rng.choice([True, False])
        v3 = chosen[2] if len(chosen) > 2 else "R"
        if mode == "nested_demorgan":
            inner = ((not a) and b) or c
            result = not inner
            expr = (f"NOT (NOT {v1} AND {v2} OR {v3}) "
                    f"(where {v1}={a}, {v2}={b}, {v3}={c})")
            steps = [
                f"NOT {v1} = {not a}",
                f"({not a} AND {b}) = {(not a) and b}",
                f"({(not a) and b} OR {c}) = {inner}",
                f"NOT {inner} = {result}",
            ]
        else:  # demorgan_chain
            left = (not a) or (not b)
            right = not c
            result = left or right
            expr = (f"NOT ({v1} AND {v2}) OR NOT {v3} "
                    f"(where {v1}={a}, {v2}={b}, {v3}={c})")
            steps = [
                f"De Morgan: NOT ({a} AND {b}) = {not a} OR {not b} = {left}",
                f"NOT {c} = {right}",
                f"{left} OR {right} = {result}",
            ]
        return expr, result, steps

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a negation problem with randomised variable names.

        Args:
            difficulty: Controls expression complexity.

        Returns:
            Tuple of (expression_string, solution_data).
        """
        mode, chosen, a, b = self._select_mode(difficulty)
        v1, v2 = chosen[0], chosen[1]

        if mode == "simple":
            expr, result, steps = self._evaluate_simple(v1, a)
        elif mode in ("demorgan_and", "demorgan_or"):
            expr, result, steps = self._evaluate_demorgan(mode, v1, v2, a, b)
        elif mode in ("double", "triple"):
            expr, result, steps = self._evaluate_multi_negation(mode, v1, a)
        else:
            expr, result, steps = self._evaluate_nested(mode, chosen, a, b)

        return expr, {"result": result, "steps": steps}

    def _create_steps(self, sd: dict) -> list[str]:
        return sd["steps"]

    def _create_answer(self, sd: dict) -> str:
        return str(sd["result"])


# ── TIER 1 ─────────────────────────────────────────────────────────

@register
class ImplicationGenerator(StepGenerator):
    """Evaluate material implication p -> q."""

    _VAR_POOL = ["P", "Q", "R", "S", "T", "U", "V", "W"]
    _MODES = ["simple", "and", "or", "chain", "nested"]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "implication"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 1

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["boolean_eval"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description."""
        return "evaluate implication"

    def _select_mode(self, difficulty: int) -> tuple[str, list[str], bool, bool, bool]:
        """Select implication mode and randomise variables/values.

        Args:
            difficulty: Controls mode pool size.

        Returns:
            Tuple of (mode, chosen_vars, p, q, imp_result).
        """
        chosen = self._rng.sample(
            self._VAR_POOL, min(3 + difficulty, len(self._VAR_POOL)))
        p = self._rng.choice([True, False])
        q = self._rng.choice([True, False])
        # Consume one rng call to match original two-call pattern
        self._rng.choice(self._MODES)
        mode = self._rng.choice(
            self._MODES[:min(len(self._MODES), 2 + difficulty)])
        return mode, chosen, p, q, (not p) or q

    def _evaluate_simple(self, vp: str, vq: str, p: bool, q: bool,
                         imp: bool) -> tuple[str, dict]:
        """Evaluate simple p -> q implication.

        Args:
            vp: Name for variable p.
            vq: Name for variable q.
            p: Truth value of p.
            q: Truth value of q.
            imp: Pre-computed implication result.

        Returns:
            Tuple of (expression, solution_data).
        """
        expr = f"{vp} -> {vq} (where {vp}={p}, {vq}={q})"
        return expr, {"steps": [
            f"{vp} -> {vq} = (NOT {vp}) OR {vq}",
            f"(NOT {p}) OR {q} = {not p} OR {q} = {imp}",
        ], "result": imp}

    def _evaluate_binary(self, mode: str, vp: str, vq: str, vr: str,
                         p: bool, q: bool, imp: bool) -> tuple[str, dict]:
        """Evaluate (p -> q) AND/OR r implication.

        Args:
            mode: Either 'and' or 'or'.
            vp: Name for variable p.
            vq: Name for variable q.
            vr: Name for variable r.
            p: Truth value of p.
            q: Truth value of q.
            imp: Pre-computed p -> q result.

        Returns:
            Tuple of (expression, solution_data).
        """
        r = self._rng.choice([True, False])
        op = "AND" if mode == "and" else "OR"
        result = (imp and r) if mode == "and" else (imp or r)
        expr = f"({vp} -> {vq}) {op} {vr} (where {vp}={p}, {vq}={q}, {vr}={r})"
        return expr, {"steps": [
            f"{vp} -> {vq} = (NOT {p}) OR {q} = {imp}",
            f"{imp} {op} {r} = {result}",
        ], "result": result}

    def _evaluate_compound(self, mode: str, vp: str, vq: str, vr: str,
                           p: bool, q: bool,
                           imp: bool) -> tuple[str, dict]:
        """Evaluate chain or nested implication.

        Args:
            mode: Either 'chain' or 'nested'.
            vp: Name for variable p.
            vq: Name for variable q.
            vr: Name for variable r.
            p: Truth value of p.
            q: Truth value of q.
            imp: Pre-computed p -> q result.

        Returns:
            Tuple of (expression, solution_data).
        """
        r = self._rng.choice([True, False])
        imp2 = (not q) or r
        if mode == "chain":
            result = (not imp) or imp2
            expr = (f"({vp} -> {vq}) -> ({vq} -> {vr}) "
                    f"(where {vp}={p}, {vq}={q}, {vr}={r})")
            steps = [
                f"{vp} -> {vq} = {imp}",
                f"{vq} -> {vr} = (NOT {q}) OR {r} = {imp2}",
                f"{imp} -> {imp2} = (NOT {imp}) OR {imp2} = {result}",
            ]
        else:  # nested
            inner = imp2
            result = (not p) or inner
            expr = (f"{vp} -> ({vq} -> {vr}) "
                    f"(where {vp}={p}, {vq}={q}, {vr}={r})")
            steps = [
                f"{vq} -> {vr} = (NOT {q}) OR {r} = {inner}",
                f"{vp} -> {inner} = (NOT {p}) OR {inner} = {result}",
            ]
        return expr, {"steps": steps, "result": result}

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an implication evaluation with randomised variable names.

        Args:
            difficulty: Controls expression complexity.

        Returns:
            Tuple of (expression_string, solution_data).
        """
        mode, chosen, p, q, imp = self._select_mode(difficulty)
        vp, vq = chosen[0], chosen[1]

        if mode == "simple":
            return self._evaluate_simple(vp, vq, p, q, imp)
        if mode in ("and", "or"):
            return self._evaluate_binary(mode, vp, vq, chosen[2], p, q, imp)
        return self._evaluate_compound(mode, vp, vq, chosen[2], p, q, imp)

    def _create_steps(self, sd: dict) -> list[str]:
        return sd["steps"]

    def _create_answer(self, sd: dict) -> str:
        return str(sd["result"])


@register
class BiconditionalGenerator(StepGenerator):
    """Evaluate biconditional p <-> q."""

    _VAR_POOL = ["P", "Q", "R", "S", "T", "U", "V", "W"]
    _MODES = ["simple", "and", "or", "chain", "nested", "xor_equiv"]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "biconditional"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 1

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["implication"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description."""
        return "evaluate biconditional"

    def _select_mode(self, difficulty: int) -> tuple[str, list[str], bool, bool, bool]:
        """Select biconditional mode and randomise variables/values.

        Args:
            difficulty: Controls mode pool size.

        Returns:
            Tuple of (mode, chosen_vars, p, q, biconditional_result).
        """
        chosen = self._rng.sample(
            self._VAR_POOL, min(3 + difficulty, len(self._VAR_POOL)))
        p = self._rng.choice([True, False])
        q = self._rng.choice([True, False])
        mode = self._rng.choice(
            self._MODES[:min(len(self._MODES), 2 + difficulty)])
        return mode, chosen, p, q, (p == q)

    def _evaluate_simple(self, vp: str, vq: str, p: bool, q: bool,
                         bic: bool) -> tuple[str, bool, list[str]]:
        """Evaluate simple biconditional p <-> q.

        Args:
            vp: Name for variable p.
            vq: Name for variable q.
            p: Truth value of p.
            q: Truth value of q.
            bic: Pre-computed biconditional result.

        Returns:
            Tuple of (expression, result, steps).
        """
        pq, qp = (not p) or q, (not q) or p
        return (f"{vp} <-> {vq} (where {vp}={p}, {vq}={q})", bic, [
            f"{vp} <-> {vq} = ({vp} -> {vq}) AND ({vq} -> {vp})",
            f"{vp} -> {vq} = {pq}",
            f"{vq} -> {vp} = {qp}",
            f"{pq} AND {qp} = {bic}",
        ])

    def _evaluate_binary(self, mode: str, vp: str, vq: str, vr: str,
                         p: bool, q: bool,
                         bic: bool) -> tuple[str, bool, list[str]]:
        """Evaluate (p <-> q) AND/OR r.

        Args:
            mode: Either 'and' or 'or'.
            vp: Name for variable p.
            vq: Name for variable q.
            vr: Name for variable r.
            p: Truth value of p.
            q: Truth value of q.
            bic: Pre-computed biconditional result.

        Returns:
            Tuple of (expression, result, steps).
        """
        r = self._rng.choice([True, False])
        op = "AND" if mode == "and" else "OR"
        result = (bic and r) if mode == "and" else (bic or r)
        expr = f"({vp} <-> {vq}) {op} {vr} (where {vp}={p}, {vq}={q}, {vr}={r})"
        return expr, result, [
            f"{vp} <-> {vq} = {bic}",
            f"{bic} {op} {r} = {result}",
        ]

    def _evaluate_compound(self, mode: str, vp: str, vq: str, vr: str,
                           p: bool, q: bool,
                           bic: bool) -> tuple[str, bool, list[str]]:
        """Evaluate chain, nested, or xor_equiv biconditional.

        Args:
            mode: One of 'chain', 'nested', or 'xor_equiv'.
            vp: Name for variable p.
            vq: Name for variable q.
            vr: Name for variable r.
            p: Truth value of p.
            q: Truth value of q.
            bic: Pre-computed biconditional result.

        Returns:
            Tuple of (expression, result, steps).
        """
        if mode == "xor_equiv":
            result = not bic
            return (f"NOT ({vp} <-> {vq}) (where {vp}={p}, {vq}={q})", result,
                    [f"{vp} <-> {vq} = {bic}", f"NOT {bic} = {result} (XOR)"])
        r = self._rng.choice([True, False])
        if mode == "chain":
            bic2 = (q == r)
            result = bic and bic2
            expr = (f"({vp} <-> {vq}) AND ({vq} <-> {vr}) "
                    f"(where {vp}={p}, {vq}={q}, {vr}={r})")
            return expr, result, [
                f"{vp} <-> {vq} = {bic}", f"{vq} <-> {vr} = {bic2}",
                f"{bic} AND {bic2} = {result}",
            ]
        # nested
        inner = (q == r)
        result = (p == inner)
        expr = (f"{vp} <-> ({vq} <-> {vr}) "
                f"(where {vp}={p}, {vq}={q}, {vr}={r})")
        return expr, result, [
            f"{vq} <-> {vr} = {inner}", f"{vp} <-> {inner} = {result}",
        ]

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a biconditional evaluation with randomised variables.

        Args:
            difficulty: Controls expression complexity.

        Returns:
            Tuple of (expression_string, solution_data).
        """
        mode, chosen, p, q, bic = self._select_mode(difficulty)
        vp, vq = chosen[0], chosen[1]

        if mode == "simple":
            expr, result, steps = self._evaluate_simple(vp, vq, p, q, bic)
        elif mode in ("and", "or"):
            expr, result, steps = self._evaluate_binary(
                mode, vp, vq, chosen[2], p, q, bic)
        else:
            expr, result, steps = self._evaluate_compound(
                mode, vp, vq, chosen[2] if len(chosen) > 2 else "R",
                p, q, bic)

        return expr, {"result": result, "steps": steps}

    def _create_steps(self, sd: dict) -> list[str]:
        return sd["steps"]

    def _create_answer(self, sd: dict) -> str:
        return str(sd["result"])


@register
class SyllogismGenerator(StepGenerator):
    """Determine if a syllogism is valid and state the conclusion."""

    _SUPERS = [
        "animals", "vertebrates", "organisms", "creatures", "beings",
        "celestial bodies", "shapes", "numbers", "structures",
        "vehicles", "instruments", "compounds", "elements",
        "languages", "beverages", "materials", "devices",
    ]
    _MIDS = [
        "mammals", "birds", "reptiles", "fish", "insects",
        "planets", "polygons", "integers", "primes",
        "cars", "guitars", "metals", "gases",
        "scripts", "teas", "alloys", "sensors",
    ]
    _SUBS = [
        "dogs", "eagles", "cobras", "salmon", "ants",
        "gas giants", "squares", "twin primes", "Mersenne primes",
        "sedans", "bass guitars", "iron", "helium",
        "kanji", "oolongs", "steel", "thermometers",
    ]
    _FORMS = ["barbara", "invalid_middle", "celarent", "invalid_neg"]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "syllogism"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 1

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["implication"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description."""
        return "evaluate syllogism"

    def _build_syllogism(self, form: str, A: str, B: str,
                         C: str) -> tuple[str, str, str, bool, str]:
        """Build premise pair, conclusion, and validity for a given form.

        Args:
            form: Syllogism form name.
            A: Middle term category.
            B: Super term category.
            C: Sub term category.

        Returns:
            Tuple of (premise1, premise2, conclusion, valid, reason).
        """
        if form == "barbara":
            return (f"all {A} are {B}", f"all {C} are {A}",
                    f"all {C} are {B}", True,
                    "follows by transitivity (Barbara)")
        if form == "celarent":
            return (f"no {A} are {B}", f"all {C} are {A}",
                    f"no {C} are {B}", True, "follows by Celarent")
        if form == "invalid_middle":
            return (f"all {A} are {B}", f"all {C} are {B}",
                    f"all {C} are {A}", False, "undistributed middle")
        # invalid_neg
        return (f"no {A} are {B}", f"some {C} are {A}",
                f"all {C} are {B}", False, "illicit negative")

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a syllogism with randomised category triples.

        Args:
            difficulty: Controls the pool size and form variety.

        Returns:
            Tuple of (premise_string, solution_data).
        """
        idx_a = self._rng.randint(0, len(self._MIDS) - 1)
        idx_b = self._rng.randint(0, len(self._SUPERS) - 1)
        idx_c = self._rng.randint(0, len(self._SUBS) - 1)
        A, B, C = self._MIDS[idx_a], self._SUPERS[idx_b], self._SUBS[idx_c]

        form = self._rng.choice(
            self._FORMS[:min(len(self._FORMS), 2 + difficulty)])
        p1, p2, conclusion, valid, reason = self._build_syllogism(
            form, A, B, C)

        return (
            f"premise 1: {p1}; premise 2: {p2}; conclusion: {conclusion}",
            {"p1": p1, "p2": p2, "conclusion": conclusion,
             "valid": valid, "reason": reason},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        return [
            f"premise 1: {sd['p1']}",
            f"premise 2: {sd['p2']}",
            f"conclusion: {sd['conclusion']}",
            f"valid: {'yes — ' + sd['reason'] if sd['valid'] else 'no — ' + sd['reason']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        return "VALID" if sd["valid"] else "INVALID"


# ── TIER 2 ─────────────────────────────────────────────────────────

@register
class PropositionalEvalGenerator(StepGenerator):
    """Evaluate compound propositional formulas."""

    _VAR_POOL = ["p", "q", "r", "s", "t", "u"]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "propositional_eval"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 2

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["boolean_eval", "implication"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description."""
        return "evaluate propositional formula"

    def _build_formulas(self, v: list[str],
                        vals: dict[str, bool]) -> list[tuple[str, bool]]:
        """Build the 3-variable formula pool.

        Args:
            v: List of chosen variable names (at least 3).
            vals: Mapping from variable name to truth value.

        Returns:
            List of (formula_string, result) tuples.
        """
        return [
            (f"({v[0]} -> {v[1]}) AND {v[2]}",
             (not vals[v[0]] or vals[v[1]]) and vals[v[2]]),
            (f"{v[0]} OR ({v[1]} -> {v[2]})",
             vals[v[0]] or (not vals[v[1]] or vals[v[2]])),
            (f"(NOT {v[0]}) -> ({v[1]} AND {v[2]})",
             vals[v[0]] or (vals[v[1]] and vals[v[2]])),
            (f"({v[0]} AND {v[1]}) -> {v[2]}",
             not (vals[v[0]] and vals[v[1]]) or vals[v[2]]),
            (f"({v[0]} -> {v[1]}) -> {v[2]}",
             not (not vals[v[0]] or vals[v[1]]) or vals[v[2]]),
            (f"({v[0]} <-> {v[1]}) OR {v[2]}",
             (vals[v[0]] == vals[v[1]]) or vals[v[2]]),
            (f"NOT ({v[0]} -> {v[1]}) AND {v[2]}",
             (vals[v[0]] and not vals[v[1]]) and vals[v[2]]),
            (f"({v[0]} OR {v[1]}) <-> {v[2]}",
             (vals[v[0]] or vals[v[1]]) == vals[v[2]]),
            (f"({v[0]} AND {v[1]}) OR (NOT {v[2]})",
             (vals[v[0]] and vals[v[1]]) or (not vals[v[2]])),
            (f"NOT {v[0]} AND (NOT {v[1]} OR {v[2]})",
             (not vals[v[0]]) and ((not vals[v[1]]) or vals[v[2]])),
        ]

    def _build_4var_formulas(self, v: list[str],
                             vals: dict[str, bool]) -> list[tuple[str, bool]]:
        """Build the 4-variable formula extensions.

        Args:
            v: List of chosen variable names (at least 4).
            vals: Mapping from variable name to truth value.

        Returns:
            List of (formula_string, result) tuples.
        """
        return [
            (f"({v[0]} -> {v[1]}) AND ({v[2]} -> {v[3]})",
             (not vals[v[0]] or vals[v[1]]) and (not vals[v[2]] or vals[v[3]])),
            (f"({v[0]} AND {v[1]}) -> ({v[2]} OR {v[3]})",
             not (vals[v[0]] and vals[v[1]]) or (vals[v[2]] or vals[v[3]])),
            (f"({v[0]} <-> {v[1]}) AND ({v[2]} <-> {v[3]})",
             (vals[v[0]] == vals[v[1]]) and (vals[v[2]] == vals[v[3]])),
        ]

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a compound propositional formula with randomised variables.

        Args:
            difficulty: Controls formula complexity.

        Returns:
            Tuple of (formula_string, solution_data).
        """
        n_vars = min(3 + difficulty // 2, len(self._VAR_POOL))
        chosen = self._rng.sample(self._VAR_POOL, n_vars)
        vals = {v: self._rng.choice([True, False]) for v in chosen}

        formulas = self._build_formulas(chosen, vals)
        if n_vars >= 4:
            formulas.extend(self._build_4var_formulas(chosen, vals))

        formula, result = self._rng.choice(
            formulas[:min(len(formulas), difficulty + 4)])
        assign = ", ".join(f"{k}={vals[k]}" for k in chosen)
        return (
            f"{formula} where {assign}",
            {"formula": formula, "vals": vals, "vars": chosen,
             "result": result},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        assign = ", ".join(f"{k}={sd['vals'][k]}" for k in sd["vars"])
        return [
            assign,
            f"substitute into {sd['formula']}",
            f"result = {sd['result']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        return str(sd["result"])


@register
class LogicalEquivalenceGenerator(StepGenerator):
    """Determine if two formulas are logically equivalent."""

    _VAR_POOL = ["p", "q", "r", "s", "t", "u"]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "logical_equivalence"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 2

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["propositional_eval"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description."""
        return "check logical equivalence"

    def _build_2var_templates(self, a: str,
                              b: str) -> list[tuple[str, str, bool, str]]:
        """Build equivalence templates using two variables.

        Args:
            a: First variable name.
            b: Second variable name.

        Returns:
            List of (formula1, formula2, equivalent, law_name) tuples.
        """
        return [
            (f"{a} -> {b}", f"NOT {a} OR {b}", True, "material implication"),
            (f"NOT ({a} AND {b})", f"NOT {a} OR NOT {b}", True, "De Morgan"),
            (f"NOT ({a} OR {b})", f"NOT {a} AND NOT {b}", True, "De Morgan"),
            (f"{a} -> {b}", f"{b} -> {a}", False, "converse fallacy"),
            (f"{a} -> {b}", f"NOT {b} -> NOT {a}", True, "contrapositive"),
            (f"{a} AND {b}", f"{a} OR {b}", False, "conjunction vs disjunction"),
            (f"{a} <-> {b}", f"({a} -> {b}) AND ({b} -> {a})", True, "biconditional"),
            (f"{a} AND ({a} OR {b})", f"{a}", True, "absorption"),
            (f"{a} OR ({a} AND {b})", f"{a}", True, "absorption"),
            (f"NOT (NOT {a})", f"{a}", True, "double negation"),
            (f"{a} AND {b}", f"{b} AND {a}", True, "commutativity"),
            (f"{a} OR {b}", f"{b} OR {a}", True, "commutativity"),
            (f"{a} -> {b}", f"{a} AND NOT {b}", False, "negation of conditional"),
        ]

    def _build_3var_templates(self, a: str, b: str,
                              c: str) -> list[tuple[str, str, bool, str]]:
        """Build equivalence templates using three variables.

        Args:
            a: First variable name.
            b: Second variable name.
            c: Third variable name.

        Returns:
            List of (formula1, formula2, equivalent, law_name) tuples.
        """
        return [
            (f"{a} AND ({b} OR {c})", f"({a} AND {b}) OR ({a} AND {c})",
             True, "distribution"),
            (f"{a} OR ({b} AND {c})", f"({a} OR {b}) AND ({a} OR {c})",
             True, "distribution"),
            (f"({a} -> {b}) AND ({a} -> {c})", f"{a} -> ({b} AND {c})",
             True, "conjunction of consequents"),
            (f"({a} -> {c}) AND ({b} -> {c})", f"({a} OR {b}) -> {c}",
             True, "combination of antecedents"),
            (f"NOT ({a} AND {b} AND {c})",
             f"NOT {a} OR NOT {b} OR NOT {c}",
             True, "generalised De Morgan"),
        ]

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a logical equivalence check with randomised variable names.

        Args:
            difficulty: Controls pool of equivalence patterns.

        Returns:
            Tuple of (question_string, solution_data).
        """
        chosen = self._rng.sample(
            self._VAR_POOL, min(3 + difficulty // 2, len(self._VAR_POOL)))
        a, b = chosen[0], chosen[1]

        templates = self._build_2var_templates(a, b)
        if len(chosen) >= 3:
            templates.extend(self._build_3var_templates(a, b, chosen[2]))

        f1, f2, equiv, law = self._rng.choice(
            templates[:min(len(templates), difficulty + 5)])
        return (
            f"is '{f1}' equivalent to '{f2}'?",
            {"f1": f1, "f2": f2, "equiv": equiv, "law": law},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        return [
            f"formula 1: {sd['f1']}",
            f"formula 2: {sd['f2']}",
            f"law: {sd['law']}",
            f"equivalent: {sd['equiv']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        return "YES" if sd["equiv"] else "NO"


@register
class ContrapositiveGenerator(StepGenerator):
    """State the contrapositive of a conditional."""

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "contrapositive"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 2

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["implication", "negation"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description."""
        return "find the contrapositive"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a contrapositive problem with randomised parameters.

        Args:
            difficulty: Controls statement pool and complexity.

        Returns:
            Tuple of (conditional_string, solution_data).
        """
        # Randomised numeric/variable components
        var_names = ["x", "y", "z", "w", "a", "b", "n", "m", "k"]
        var = self._rng.choice(var_names)
        threshold_a = self._rng.randint(1, 20)
        threshold_b = self._rng.randint(1, threshold_a) if threshold_a > 1 else 1
        exp = self._rng.choice([2, 3])
        divisor = self._rng.choice([2, 3, 4, 5, 6, 7])

        statements = [
            (f"it rains on day {self._rng.randint(1,30)}",
             f"the ground is wet"),
            (f"{var} > {threshold_a}", f"{var} > {threshold_b}"),
            (f"{var} is even", f"{var}^{exp} is even"),
            (f"f is differentiable at {var}={threshold_a}",
             f"f is continuous at {var}={threshold_a}"),
            (f"line {var.upper()} is parallel to line {self._rng.choice('LMNPQ')}",
             f"alternate angles are equal"),
            (f"the function g({var}) is bounded on [0,{threshold_a}]",
             f"the integral of g({var}) converges on [0,{threshold_a}]"),
            (f"{var} is divisible by {divisor * 2}",
             f"{var} is divisible by {divisor}"),
            (f"{var}^{exp} < {threshold_a}",
             f"{var} < {threshold_a}"),
            (f"triangle has all sides equal",
             f"triangle has all angles equal"),
            (f"sequence a_{var} converges",
             f"sequence a_{var} is bounded"),
            (f"matrix A_{threshold_a}x{threshold_a} is invertible",
             f"det(A) != 0"),
            (f"graph G has {threshold_a} vertices and is connected",
             f"graph G has at least {threshold_a - 1} edges"),
        ]
        p, q = self._rng.choice(statements[:min(len(statements), 4 + difficulty)])
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
        """Return the unique task identifier."""
        return "deduction_chain"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 3

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["propositional_eval", "contrapositive"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description."""
        return "follow deduction chain"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a deduction chain with randomised proposition names.

        Args:
            difficulty: Controls chain length.

        Returns:
            Tuple of (chain_string, solution_data).
        """
        n = min(2 + difficulty, 6)
        # Draw from a larger shuffled pool to avoid always using A,B,C...
        pool = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        self._rng.shuffle(pool)
        props = pool[:n + 1]
        chain = [f"{props[i]} -> {props[i + 1]}" for i in range(n)]
        given = props[0]
        conclusion = props[-1]

        # Randomise the truth value of the given proposition
        given_val = self._rng.choice([True, False])
        if given_val:
            conclusion_val = True  # chain of implications from True
            prompt = (f"given: {given} is True; {'; '.join(chain)}. "
                      f"what is {conclusion}?")
        else:
            conclusion_val = False  # can't derive True from False given
            # Reverse: use contrapositive chain
            prompt = (f"given: {given} is False; {'; '.join(chain)}. "
                      f"can we determine {conclusion}?")

        return (
            prompt,
            {"chain": chain, "props": props, "given": given,
             "conclusion": conclusion, "given_val": given_val,
             "conclusion_val": conclusion_val},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        if sd["given_val"]:
            steps = [f"{sd['given']} is True"]
            for i in range(len(sd["chain"])):
                steps.append(
                    f"by {sd['chain'][i]}: {sd['props'][i + 1]} is True"
                )
        else:
            steps = [f"{sd['given']} is False"]
            steps.append(
                f"{sd['given']} -> {sd['props'][1]} does not let us "
                f"conclude {sd['props'][1]} is False (fallacy of denying "
                f"the antecedent)"
            )
            steps.append(f"{sd['conclusion']} cannot be determined")
        return steps

    def _create_answer(self, sd: dict) -> str:
        if sd["given_val"]:
            return f"{sd['conclusion']} is True"
        return f"{sd['conclusion']} is undetermined"


@register
class QuantifierEvalGenerator(StepGenerator):
    """Evaluate universal/existential quantifiers over finite domains."""

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "quantifier_eval"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 3

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["boolean_eval"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description."""
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
        """Return the unique task identifier."""
        return "knights_knaves"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["deduction_chain"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description."""
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
        types = sd["types"]
        statements = sd["statements"]
        for stmt in statements:
            steps.append(f"given: {stmt}")
        for name in types:
            other_type = "knight" if types[name] == "knave" else "knave"
            steps.append(
                f"test {name}=knight vs {name}=knave"
            )
            for stmt in statements:
                if stmt.startswith(f"{name} says:"):
                    steps.append(f"if {name}=knight then claim is true")
                    steps.append(f"if {name}=knave then claim is false")
                    break
        steps.append(f"consistent assignment found")
        return steps

    def _create_answer(self, sd: dict) -> str:
        parts = [f"{n}={t}" for n, t in sorted(sd["types"].items())]
        return ", ".join(parts)


@register
class LogicalPuzzleGenerator(StepGenerator):
    """Solve constraint satisfaction puzzles."""

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "logical_puzzle"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["deduction_chain"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description."""
        return "solve logic puzzle"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        from itertools import permutations

        n = min(2 + difficulty // 2, 4)
        names = ["Alice", "Bob", "Carol", "Dave"][:n]
        colors = ["red", "blue", "green", "yellow"][:n]
        self._rng.shuffle(colors)
        assignment = dict(zip(names, colors))

        one_reveal = self._rng.choice(names)
        revealed = {one_reveal}
        clues = [f"{one_reveal} has {assignment[one_reveal]}"]

        for _ in range(20):
            name = self._rng.choice(names)
            wrong = self._rng.choice(
                [c for c in colors if c != assignment[name]]
            )
            clue = f"{name} does not have {wrong}"
            if clue not in clues:
                clues.append(clue)
            if self._is_unique(names, colors, clues, assignment):
                break

        self._rng.shuffle(clues)
        problem = "; ".join(clues)
        return problem, {
            "assignment": assignment,
            "clues": clues,
            "revealed": revealed,
        }

    @staticmethod
    def _is_unique(names, colors, clues, expected):
        """Check if clues uniquely determine the assignment."""
        from itertools import permutations

        count = 0
        for perm in permutations(colors):
            candidate = dict(zip(names, perm))
            ok = True
            for clue in clues:
                if " has " in clue and "does not" not in clue:
                    parts = clue.split(" has ")
                    if candidate.get(parts[0]) != parts[1]:
                        ok = False
                        break
                elif "does not have" in clue:
                    parts = clue.split(" does not have ")
                    if candidate.get(parts[0]) == parts[1]:
                        ok = False
                        break
            if ok:
                count += 1
                if count > 1:
                    return False
        return count == 1

    def _create_steps(self, sd: dict) -> list[str]:
        steps = []
        assignment = sd["assignment"]
        revealed = sd["revealed"]
        remaining = [n for n in assignment if n not in revealed]
        for name in revealed:
            steps.append(f"given: {name} = {assignment[name]}")
        all_colors = set(assignment.values())
        used = {assignment[n] for n in revealed}
        for name in remaining:
            avail = all_colors - used
            steps.append(f"eliminate for {name}: options = {sorted(avail)}")
            steps.append(f"assign {name} = {assignment[name]}")
            used.add(assignment[name])
        return steps

    def _create_answer(self, sd: dict) -> str:
        parts = [f"{n}={c}" for n, c in sorted(sd["assignment"].items())]
        return ", ".join(parts)
