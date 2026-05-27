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
        """Generate a negation problem with randomised variable names.

        Args:
            difficulty: Controls expression complexity.

        Returns:
            Tuple of (expression_string, solution_data).
        """
        var_pool = ["P", "Q", "R", "S", "T", "U", "V", "W"]
        chosen = self._rng.sample(var_pool, min(2 + difficulty, len(var_pool)))
        v1, v2 = chosen[0], chosen[1]
        a = self._rng.choice([True, False])
        b = self._rng.choice([True, False])

        modes = ["simple", "demorgan_and", "demorgan_or", "double",
                 "triple", "nested_demorgan", "demorgan_chain"]
        mode = self._rng.choice(modes[:min(len(modes), 3 + difficulty)])

        if mode == "simple":
            expr = f"NOT {v1} (where {v1}={a})"
            result = not a
            steps = [f"NOT {a} = {result}"]
        elif mode == "demorgan_and":
            expr = f"NOT ({v1} AND {v2}) (where {v1}={a}, {v2}={b})"
            result = (not a) or (not b)
            steps = [
                f"De Morgan: NOT ({v1} AND {v2}) = (NOT {v1}) OR (NOT {v2})",
                f"(NOT {a}) OR (NOT {b}) = {not a} OR {not b} = {result}",
            ]
        elif mode == "demorgan_or":
            expr = f"NOT ({v1} OR {v2}) (where {v1}={a}, {v2}={b})"
            result = (not a) and (not b)
            steps = [
                f"De Morgan: NOT ({v1} OR {v2}) = (NOT {v1}) AND (NOT {v2})",
                f"(NOT {a}) AND (NOT {b}) = {not a} AND {not b} = {result}",
            ]
        elif mode == "double":
            expr = f"NOT (NOT {v1}) (where {v1}={a})"
            result = a
            steps = [f"double negation: NOT (NOT {a}) = {a}"]
        elif mode == "triple":
            expr = f"NOT (NOT (NOT {v1})) (where {v1}={a})"
            result = not a
            steps = [
                f"inner: NOT {a} = {not a}",
                f"middle: NOT {not a} = {a}",
                f"outer: NOT {a} = {not a}",
            ]
        elif mode == "nested_demorgan":
            c = self._rng.choice([True, False])
            v3 = chosen[2] if len(chosen) > 2 else "R"
            expr = (f"NOT (NOT {v1} AND {v2} OR {v3}) "
                    f"(where {v1}={a}, {v2}={b}, {v3}={c})")
            inner = ((not a) and b) or c
            result = not inner
            steps = [
                f"NOT {v1} = {not a}",
                f"({not a} AND {b}) = {(not a) and b}",
                f"({(not a) and b} OR {c}) = {inner}",
                f"NOT {inner} = {result}",
            ]
        else:  # demorgan_chain
            c = self._rng.choice([True, False])
            v3 = chosen[2] if len(chosen) > 2 else "R"
            expr = (f"NOT ({v1} AND {v2}) OR NOT {v3} "
                    f"(where {v1}={a}, {v2}={b}, {v3}={c})")
            left = (not a) or (not b)
            right = not c
            result = left or right
            steps = [
                f"De Morgan: NOT ({a} AND {b}) = {not a} OR {not b} = {left}",
                f"NOT {c} = {right}",
                f"{left} OR {right} = {result}",
            ]

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
        """Generate an implication evaluation with randomised variable names.

        Args:
            difficulty: Controls expression complexity.

        Returns:
            Tuple of (expression_string, solution_data).
        """
        var_pool = ["P", "Q", "R", "S", "T", "U", "V", "W"]
        chosen = self._rng.sample(var_pool, min(3 + difficulty, len(var_pool)))
        vp, vq = chosen[0], chosen[1]
        p = self._rng.choice([True, False])
        q = self._rng.choice([True, False])
        imp_result = (not p) or q

        mode = self._rng.choice(["simple", "and", "or", "chain", "nested"])
        mode_idx = ["simple", "and", "or", "chain", "nested"]
        mode = self._rng.choice(mode_idx[:min(len(mode_idx), 2 + difficulty)])

        if mode == "simple":
            expr = f"{vp} -> {vq} (where {vp}={p}, {vq}={q})"
            result = imp_result
            return expr, {"steps": [
                f"{vp} -> {vq} = (NOT {vp}) OR {vq}",
                f"(NOT {p}) OR {q} = {not p} OR {q} = {result}",
            ], "result": result}
        elif mode == "and":
            vr = chosen[2]
            r = self._rng.choice([True, False])
            result = imp_result and r
            expr = f"({vp} -> {vq}) AND {vr} (where {vp}={p}, {vq}={q}, {vr}={r})"
            return expr, {"steps": [
                f"{vp} -> {vq} = (NOT {p}) OR {q} = {imp_result}",
                f"{imp_result} AND {r} = {result}",
            ], "result": result}
        elif mode == "or":
            vr = chosen[2]
            r = self._rng.choice([True, False])
            result = imp_result or r
            expr = f"({vp} -> {vq}) OR {vr} (where {vp}={p}, {vq}={q}, {vr}={r})"
            return expr, {"steps": [
                f"{vp} -> {vq} = (NOT {p}) OR {q} = {imp_result}",
                f"{imp_result} OR {r} = {result}",
            ], "result": result}
        elif mode == "chain":
            vr = chosen[2]
            r = self._rng.choice([True, False])
            imp2 = (not q) or r
            result = (not imp_result) or imp2
            expr = (f"({vp} -> {vq}) -> ({vq} -> {vr}) "
                    f"(where {vp}={p}, {vq}={q}, {vr}={r})")
            return expr, {"steps": [
                f"{vp} -> {vq} = {imp_result}",
                f"{vq} -> {vr} = (NOT {q}) OR {r} = {imp2}",
                f"{imp_result} -> {imp2} = (NOT {imp_result}) OR {imp2} = {result}",
            ], "result": result}
        else:  # nested
            vr = chosen[2]
            r = self._rng.choice([True, False])
            inner = (not q) or r
            result = (not p) or inner
            expr = (f"{vp} -> ({vq} -> {vr}) "
                    f"(where {vp}={p}, {vq}={q}, {vr}={r})")
            return expr, {"steps": [
                f"{vq} -> {vr} = (NOT {q}) OR {r} = {inner}",
                f"{vp} -> {inner} = (NOT {p}) OR {inner} = {result}",
            ], "result": result}

    def _create_steps(self, sd: dict) -> list[str]:
        return sd["steps"]

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
        """Generate a biconditional evaluation with randomised variables.

        Args:
            difficulty: Controls expression complexity.

        Returns:
            Tuple of (expression_string, solution_data).
        """
        var_pool = ["P", "Q", "R", "S", "T", "U", "V", "W"]
        chosen = self._rng.sample(var_pool, min(3 + difficulty, len(var_pool)))
        vp, vq = chosen[0], chosen[1]
        p = self._rng.choice([True, False])
        q = self._rng.choice([True, False])
        bic = (p == q)

        modes = ["simple", "and", "or", "chain", "nested", "xor_equiv"]
        mode = self._rng.choice(modes[:min(len(modes), 2 + difficulty)])

        if mode == "simple":
            expr = f"{vp} <-> {vq} (where {vp}={p}, {vq}={q})"
            result = bic
            pq = (not p) or q
            qp = (not q) or p
            steps = [
                f"{vp} <-> {vq} = ({vp} -> {vq}) AND ({vq} -> {vp})",
                f"{vp} -> {vq} = {pq}",
                f"{vq} -> {vp} = {qp}",
                f"{pq} AND {qp} = {result}",
            ]
        elif mode == "and":
            vr = chosen[2]
            r = self._rng.choice([True, False])
            result = bic and r
            expr = f"({vp} <-> {vq}) AND {vr} (where {vp}={p}, {vq}={q}, {vr}={r})"
            steps = [
                f"{vp} <-> {vq} = {bic}",
                f"{bic} AND {r} = {result}",
            ]
        elif mode == "or":
            vr = chosen[2]
            r = self._rng.choice([True, False])
            result = bic or r
            expr = f"({vp} <-> {vq}) OR {vr} (where {vp}={p}, {vq}={q}, {vr}={r})"
            steps = [
                f"{vp} <-> {vq} = {bic}",
                f"{bic} OR {r} = {result}",
            ]
        elif mode == "chain":
            vr = chosen[2]
            r = self._rng.choice([True, False])
            bic2 = (q == r)
            result = bic and bic2
            expr = (f"({vp} <-> {vq}) AND ({vq} <-> {vr}) "
                    f"(where {vp}={p}, {vq}={q}, {vr}={r})")
            steps = [
                f"{vp} <-> {vq} = {bic}",
                f"{vq} <-> {vr} = {bic2}",
                f"{bic} AND {bic2} = {result}",
            ]
        elif mode == "nested":
            vr = chosen[2]
            r = self._rng.choice([True, False])
            inner = (q == r)
            result = (p == inner)
            expr = (f"{vp} <-> ({vq} <-> {vr}) "
                    f"(where {vp}={p}, {vq}={q}, {vr}={r})")
            steps = [
                f"{vq} <-> {vr} = {inner}",
                f"{vp} <-> {inner} = {result}",
            ]
        else:  # xor_equiv
            result = not bic  # XOR is NOT biconditional
            expr = f"NOT ({vp} <-> {vq}) (where {vp}={p}, {vq}={q})"
            steps = [
                f"{vp} <-> {vq} = {bic}",
                f"NOT {bic} = {result} (XOR)",
            ]

        return expr, {"result": result, "steps": steps}

    def _create_steps(self, sd: dict) -> list[str]:
        return sd["steps"]

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
        """Generate a syllogism with randomised category triples.

        Args:
            difficulty: Controls the pool size and form variety.

        Returns:
            Tuple of (premise_string, solution_data).
        """
        # Large pools for random category construction
        supers = [
            "animals", "vertebrates", "organisms", "creatures", "beings",
            "celestial bodies", "shapes", "numbers", "structures",
            "vehicles", "instruments", "compounds", "elements",
            "languages", "beverages", "materials", "devices",
        ]
        mids = [
            "mammals", "birds", "reptiles", "fish", "insects",
            "planets", "polygons", "integers", "primes",
            "cars", "guitars", "metals", "gases",
            "scripts", "teas", "alloys", "sensors",
        ]
        subs = [
            "dogs", "eagles", "cobras", "salmon", "ants",
            "gas giants", "squares", "twin primes", "Mersenne primes",
            "sedans", "bass guitars", "iron", "helium",
            "kanji", "oolongs", "steel", "thermometers",
        ]

        idx_a = self._rng.randint(0, len(mids) - 1)
        idx_b = self._rng.randint(0, len(supers) - 1)
        idx_c = self._rng.randint(0, len(subs) - 1)
        A, B, C = mids[idx_a], supers[idx_b], subs[idx_c]

        forms = ["barbara", "invalid_middle", "celarent", "invalid_neg"]
        form = self._rng.choice(forms[:min(len(forms), 2 + difficulty)])

        if form == "barbara":
            p1 = f"all {A} are {B}"
            p2 = f"all {C} are {A}"
            conclusion = f"all {C} are {B}"
            valid = True
            reason = "follows by transitivity (Barbara)"
        elif form == "celarent":
            p1 = f"no {A} are {B}"
            p2 = f"all {C} are {A}"
            conclusion = f"no {C} are {B}"
            valid = True
            reason = "follows by Celarent"
        elif form == "invalid_middle":
            p1 = f"all {A} are {B}"
            p2 = f"all {C} are {B}"
            conclusion = f"all {C} are {A}"
            valid = False
            reason = "undistributed middle"
        else:  # invalid_neg
            p1 = f"no {A} are {B}"
            p2 = f"some {C} are {A}"
            conclusion = f"all {C} are {B}"
            valid = False
            reason = "illicit negative"

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
        """Generate a compound propositional formula with randomised variables.

        Args:
            difficulty: Controls formula complexity.

        Returns:
            Tuple of (formula_string, solution_data).
        """
        var_pool = ["p", "q", "r", "s", "t", "u"]
        n_vars = min(3 + difficulty // 2, len(var_pool))
        chosen = self._rng.sample(var_pool, n_vars)
        vals = {v: self._rng.choice([True, False]) for v in chosen}
        v = chosen  # shorthand

        # Build formulas dynamically based on chosen variables
        formulas = [
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

        if n_vars >= 4:
            formulas.extend([
                (f"({v[0]} -> {v[1]}) AND ({v[2]} -> {v[3]})",
                 (not vals[v[0]] or vals[v[1]]) and (not vals[v[2]] or vals[v[3]])),
                (f"({v[0]} AND {v[1]}) -> ({v[2]} OR {v[3]})",
                 not (vals[v[0]] and vals[v[1]]) or (vals[v[2]] or vals[v[3]])),
                (f"({v[0]} <-> {v[1]}) AND ({v[2]} <-> {v[3]})",
                 (vals[v[0]] == vals[v[1]]) and (vals[v[2]] == vals[v[3]])),
            ])

        formula, result = self._rng.choice(formulas[:min(len(formulas), difficulty + 4)])
        assign = ", ".join(f"{k}={vals[k]}" for k in chosen)
        return (
            f"{formula} where {assign}",
            {"formula": formula, "vals": vals, "vars": chosen, "result": result},
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
        """Generate a logical equivalence check with randomised variable names.

        Args:
            difficulty: Controls pool of equivalence patterns.

        Returns:
            Tuple of (question_string, solution_data).
        """
        var_pool = ["p", "q", "r", "s", "t", "u"]
        chosen = self._rng.sample(var_pool, min(3 + difficulty // 2, len(var_pool)))
        a, b = chosen[0], chosen[1]

        # Template pairs use placeholders A, B, C
        templates = [
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

        if len(chosen) >= 3:
            c = chosen[2]
            templates.extend([
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
            ])

        f1, f2, equiv, law = self._rng.choice(
            templates[:min(len(templates), difficulty + 5)]
        )
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
