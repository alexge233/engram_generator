"""Expanded generators to fill gaps across tiers 0-6.

Adds 38 new generators targeting tiers with low coverage,
bringing the total from 209 to 247.
"""
import math
import random
from fractions import Fraction

from engram_generator.base import StepGenerator, STEP_TOKEN
from engram_generator.curriculum.registry import register


# ── TIER 0 (4 → 7) ─────────────────────────────────────────────────

@register
class CountingGenerator(StepGenerator):
    """Count items matching a criterion in a list."""

    @property
    def task_name(self) -> str:
        return "counting"

    @property
    def tier(self) -> int:
        return 0

    def task_description(self, difficulty: int) -> str:
        return f"count items in list"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        length = min(4 + difficulty * 2, 20)
        items = [self._rng.randint(1, 9) for _ in range(length)]
        target = self._rng.choice(items)
        count = items.count(target)
        problem = f"count({target} in [{','.join(str(x) for x in items)}])"
        return problem, {"items": items, "target": target, "count": count}

    def _create_steps(self, sd: dict) -> list[str]:
        positions = [i for i, x in enumerate(sd["items"]) if x == sd["target"]]
        return [f"position {p}: {sd['target']}" for p in positions]

    def _create_answer(self, sd: dict) -> str:
        return str(sd["count"])


@register
class ComparisonGenerator(StepGenerator):
    """Compare two numbers and return the larger/smaller."""

    @property
    def task_name(self) -> str:
        return "comparison"

    @property
    def tier(self) -> int:
        return 0

    def task_description(self, difficulty: int) -> str:
        return "compare two numbers"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        digits = min(1 + difficulty, 6)
        lo = 10 ** (digits - 1)
        hi = 10 ** digits - 1
        a = self._rng.randint(lo, hi)
        b = self._rng.randint(lo, hi)
        while b == a:
            b = self._rng.randint(lo, hi)
        op = self._rng.choice(["max", "min"])
        result = max(a, b) if op == "max" else min(a, b)
        problem = f"{op}({a},{b})"
        return problem, {"a": a, "b": b, "op": op, "result": result}

    def _create_steps(self, sd: dict) -> list[str]:
        cmp = ">" if sd["a"] > sd["b"] else "<"
        return [f"{sd['a']} {cmp} {sd['b']}"]

    def _create_answer(self, sd: dict) -> str:
        return str(sd["result"])


@register
class RoundingGenerator(StepGenerator):
    """Round a number to a given number of decimal places."""

    @property
    def task_name(self) -> str:
        return "rounding"

    @property
    def tier(self) -> int:
        return 0

    def task_description(self, difficulty: int) -> str:
        return "round number"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        places = self._rng.randint(0, min(difficulty, 4))
        value = round(self._rng.uniform(0.01, 100 * difficulty), places + 3)
        result = round(value, places)
        problem = f"round({value},{places})"
        return problem, {"value": value, "places": places, "result": result}

    def _create_steps(self, sd: dict) -> list[str]:
        return [f"round to {sd['places']} decimal places"]

    def _create_answer(self, sd: dict) -> str:
        return str(sd["result"])


# ── TIER 1 (7 → 12) ────────────────────────────────────────────────

@register
class AbsoluteValueGenerator(StepGenerator):
    """Compute absolute value of an expression."""

    @property
    def task_name(self) -> str:
        return "absolute_value"

    @property
    def tier(self) -> int:
        return 1

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["subtraction"]

    def task_description(self, difficulty: int) -> str:
        return "compute absolute value"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        a = self._rng.randint(-50 * difficulty, 50 * difficulty)
        b = self._rng.randint(-50 * difficulty, 50 * difficulty)
        expr_val = a - b
        result = abs(expr_val)
        problem = f"|{a}-{b}|"
        return problem, {"a": a, "b": b, "expr_val": expr_val, "result": result}

    def _create_steps(self, sd: dict) -> list[str]:
        return [
            f"{sd['a']}-{sd['b']}={sd['expr_val']}",
            f"|{sd['expr_val']}|={sd['result']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        return str(sd["result"])


@register
class FloorCeilGenerator(StepGenerator):
    """Compute floor or ceiling of a value."""

    @property
    def task_name(self) -> str:
        return "floor_ceil"

    @property
    def tier(self) -> int:
        return 1

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["division"]

    def task_description(self, difficulty: int) -> str:
        return "compute floor or ceiling"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        a = self._rng.randint(1, 100 * difficulty)
        b = self._rng.randint(2, 10 + difficulty)
        op = self._rng.choice(["floor", "ceil"])
        value = a / b
        result = math.floor(value) if op == "floor" else math.ceil(value)
        problem = f"{op}({a}/{b})"
        return problem, {"a": a, "b": b, "op": op, "value": value, "result": result}

    def _create_steps(self, sd: dict) -> list[str]:
        return [
            f"{sd['a']}/{sd['b']}={sd['value']:.4f}",
            f"{sd['op']}={sd['result']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        return str(sd["result"])


@register
class PercentageGenerator(StepGenerator):
    """Compute percentage of a number."""

    @property
    def task_name(self) -> str:
        return "percentage"

    @property
    def tier(self) -> int:
        return 1

    @property
    def prerequisites(self) -> list[str]:
        return ["multiplication", "division"]

    def task_description(self, difficulty: int) -> str:
        return "compute percentage"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        pct = self._rng.choice([5, 10, 15, 20, 25, 30, 40, 50, 60, 75, 80])
        base = self._rng.randint(10, 100 * difficulty)
        result = base * pct / 100
        problem = f"{pct}% of {base}"
        return problem, {"pct": pct, "base": base, "result": result}

    def _create_steps(self, sd: dict) -> list[str]:
        return [
            f"{sd['pct']}/100={sd['pct']/100}",
            f"{sd['pct']/100}*{sd['base']}={sd['result']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        r = sd["result"]
        return str(int(r)) if r == int(r) else str(r)


@register
class SequenceNextGenerator(StepGenerator):
    """Find the next term in an arithmetic or geometric sequence."""

    @property
    def task_name(self) -> str:
        return "sequence_next"

    @property
    def tier(self) -> int:
        return 1

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["addition"]

    def task_description(self, difficulty: int) -> str:
        return "find next in sequence"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        seq_type = self._rng.choice(["arithmetic", "geometric"])
        length = min(3 + difficulty // 2, 7)

        if seq_type == "arithmetic":
            start = self._rng.randint(-10, 10)
            diff = self._rng.randint(1, 5 + difficulty)
            terms = [start + i * diff for i in range(length)]
            next_term = start + length * diff
            rule = f"d={diff}"
        else:
            start = self._rng.randint(1, 5)
            ratio = self._rng.choice([2, 3, -2])
            terms = [start * ratio ** i for i in range(length)]
            next_term = start * ratio ** length
            rule = f"r={ratio}"

        problem = ",".join(str(t) for t in terms) + ",?"
        return problem, {"terms": terms, "next": next_term,
                         "type": seq_type, "rule": rule}

    def _create_steps(self, sd: dict) -> list[str]:
        return [
            f"type: {sd['type']}",
            f"rule: {sd['rule']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        return str(sd["next"])


@register
class FractionArithmeticGenerator(StepGenerator):
    """Add, subtract, multiply or divide fractions."""

    @property
    def task_name(self) -> str:
        return "fraction_arithmetic"

    @property
    def tier(self) -> int:
        return 1

    @property
    def prerequisites(self) -> list[str]:
        return ["multiplication", "addition"]

    def task_description(self, difficulty: int) -> str:
        return "compute fraction arithmetic"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        max_den = 5 + difficulty * 2
        a = Fraction(self._rng.randint(1, max_den), self._rng.randint(2, max_den))
        b = Fraction(self._rng.randint(1, max_den), self._rng.randint(2, max_den))
        op = self._rng.choice(["+", "-", "*"])
        if op == "+":
            result = a + b
        elif op == "-":
            result = a - b
        else:
            result = a * b
        problem = f"{a} {op} {b}"
        return problem, {"a": a, "b": b, "op": op, "result": result}

    def _create_steps(self, sd: dict) -> list[str]:
        a, b, result = sd["a"], sd["b"], sd["result"]
        steps = []
        if sd["op"] in ["+", "-"]:
            lcm = a.denominator * b.denominator // math.gcd(a.denominator, b.denominator)
            steps.append(f"LCD={lcm}")
            steps.append(f"{a.numerator*lcm//a.denominator}/{lcm} {sd['op']} {b.numerator*lcm//b.denominator}/{lcm}")
        steps.append(f"={result}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        return str(sd["result"])


# ── TIER 2 (12 → 16) ───────────────────────────────────────────────

@register
class SquareRootGenerator(StepGenerator):
    """Compute integer square roots."""

    @property
    def task_name(self) -> str:
        return "square_root"

    @property
    def tier(self) -> int:
        return 2

    @property
    def prerequisites(self) -> list[str]:
        return ["multiplication"]

    def task_description(self, difficulty: int) -> str:
        return "compute square root"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a square root problem with wider randomised range.

        Args:
            difficulty: Controls the root range.

        Returns:
            Tuple of (problem_string, solution_data).
        """
        root = self._rng.randint(2, 20 + difficulty * 5)
        n = root * root
        problem = f"\\sqrt{{{n}}}"
        return problem, {"n": n, "root": root}

    def _create_steps(self, sd: dict) -> list[str]:
        return [f"{sd['root']}*{sd['root']}={sd['n']}"]

    def _create_answer(self, sd: dict) -> str:
        return str(sd["root"])


@register
class PrimeFactorisationGenerator(StepGenerator):
    """Find the complete prime factorisation of a number."""

    @property
    def task_name(self) -> str:
        return "prime_factorisation"

    @property
    def tier(self) -> int:
        return 2

    @property
    def prerequisites(self) -> list[str]:
        return ["division"]

    def task_description(self, difficulty: int) -> str:
        return "find prime factorisation"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        primes = [2, 3, 5, 7, 11, 13]
        num_factors = min(2 + difficulty // 2, 5)
        factors = sorted(self._rng.choices(primes[:min(difficulty + 2, 6)],
                                            k=num_factors))
        n = 1
        for f in factors:
            n *= f
        problem = f"factorise({n})"
        return problem, {"n": n, "factors": factors}

    def _create_steps(self, sd: dict) -> list[str]:
        steps = []
        remaining = sd["n"]
        for f in sd["factors"]:
            steps.append(f"{remaining}/{f}={remaining // f}")
            remaining //= f
        return steps

    def _create_answer(self, sd: dict) -> str:
        return "*".join(str(f) for f in sd["factors"])


@register
class ArithmeticMeanGenerator(StepGenerator):
    """Compute the arithmetic mean of a list of numbers."""

    @property
    def task_name(self) -> str:
        return "arithmetic_mean"

    @property
    def tier(self) -> int:
        return 2

    @property
    def prerequisites(self) -> list[str]:
        return ["addition", "division"]

    def task_description(self, difficulty: int) -> str:
        return "compute arithmetic mean"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        length = min(3 + difficulty, 10)
        values = [self._rng.randint(1, 50 + difficulty * 10) for _ in range(length)]
        total = sum(values)
        mean = total / length
        problem = f"mean([{','.join(str(v) for v in values)}])"
        return problem, {"values": values, "total": total,
                         "length": length, "mean": mean}

    def _create_steps(self, sd: dict) -> list[str]:
        return [
            f"sum={sd['total']}",
            f"n={sd['length']}",
            f"{sd['total']}/{sd['length']}={sd['mean']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        m = sd["mean"]
        return str(int(m)) if m == int(m) else f"{m:.2f}"


@register
class WeightedSumGenerator(StepGenerator):
    """Compute weighted sum of values."""

    @property
    def task_name(self) -> str:
        return "weighted_sum"

    @property
    def tier(self) -> int:
        return 2

    @property
    def prerequisites(self) -> list[str]:
        return ["multiplication", "addition"]

    def task_description(self, difficulty: int) -> str:
        return "compute weighted sum"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        length = min(2 + difficulty // 2, 5)
        values = [self._rng.randint(1, 20) for _ in range(length)]
        weights = [self._rng.randint(1, 5) for _ in range(length)]
        products = [v * w for v, w in zip(values, weights)]
        result = sum(products)
        pairs = [f"{v}*{w}" for v, w in zip(values, weights)]
        problem = " + ".join(pairs)
        return problem, {"values": values, "weights": weights,
                         "products": products, "result": result}

    def _create_steps(self, sd: dict) -> list[str]:
        steps = [f"{v}*{w}={p}" for v, w, p in
                 zip(sd["values"], sd["weights"], sd["products"])]
        steps.append(f"sum={sd['result']}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        return str(sd["result"])


# ── TIER 3 (23 → 28) ───────────────────────────────────────────────

@register
class SummationGenerator(StepGenerator):
    """Compute summation \\sum_{i=a}^{b} f(i) for simple f."""

    @property
    def task_name(self) -> str:
        return "summation"

    @property
    def tier(self) -> int:
        return 3

    @property
    def prerequisites(self) -> list[str]:
        return ["addition", "exponentiation"]

    def task_description(self, difficulty: int) -> str:
        return "compute summation"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        a = self._rng.randint(0, 2)
        b = a + min(2 + difficulty, 8)
        func_type = self._rng.choice(["linear", "square", "constant"])

        if func_type == "linear":
            coeff = self._rng.randint(1, 5)
            terms = [coeff * i for i in range(a, b + 1)]
            problem = f"\\sum_{{i={a}}}^{{{b}}} {coeff}i"
        elif func_type == "square":
            terms = [i * i for i in range(a, b + 1)]
            problem = f"\\sum_{{i={a}}}^{{{b}}} i^2"
        else:
            c = self._rng.randint(1, 10)
            terms = [c for _ in range(a, b + 1)]
            problem = f"\\sum_{{i={a}}}^{{{b}}} {c}"

        result = sum(terms)
        return problem, {"a": a, "b": b, "terms": terms, "result": result}

    def _create_steps(self, sd: dict) -> list[str]:
        steps = [f"i={i}: {t}" for i, t in enumerate(sd["terms"], sd["a"])]
        return steps

    def _create_answer(self, sd: dict) -> str:
        return str(sd["result"])


@register
class ProductNotationGenerator(StepGenerator):
    """Compute product \\prod_{i=a}^{b} f(i)."""

    @property
    def task_name(self) -> str:
        return "product_notation"

    @property
    def tier(self) -> int:
        return 3

    @property
    def prerequisites(self) -> list[str]:
        return ["multiplication"]

    def task_description(self, difficulty: int) -> str:
        return "compute product"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a product notation problem with randomised ranges and expressions.

        Args:
            difficulty: Controls the range and expression type.

        Returns:
            Tuple of (problem_string, solution_data).
        """
        a = self._rng.randint(1, 5)
        b = a + self._rng.randint(1, min(2 + difficulty, 6))
        expr_type = self._rng.choice(["i", "i+c", "c*i", "i^2"])

        if expr_type == "i":
            terms = list(range(a, b + 1))
            problem = f"\\prod_{{i={a}}}^{{{b}}} i"
        elif expr_type == "i+c":
            c = self._rng.randint(1, 5)
            terms = [i + c for i in range(a, b + 1)]
            problem = f"\\prod_{{i={a}}}^{{{b}}} (i+{c})"
        elif expr_type == "c*i":
            c = self._rng.randint(2, 4)
            terms = [c * i for i in range(a, b + 1)]
            problem = f"\\prod_{{i={a}}}^{{{b}}} {c}i"
        else:
            terms = [i * i for i in range(a, b + 1)]
            problem = f"\\prod_{{i={a}}}^{{{b}}} i^2"

        result = 1
        for t in terms:
            result *= t
        return problem, {"a": a, "b": b, "terms": terms, "result": result}

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate step-by-step product computation.

        Args:
            sd: Solution data with terms.

        Returns:
            Steps showing running product.
        """
        running = 1
        steps = []
        for t in sd["terms"]:
            running *= t
            steps.append(f"*{t}={running}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the product result.

        Args:
            sd: Solution data.

        Returns:
            String representation of the product.
        """
        return str(sd["result"])


@register
class MatrixAddGenerator(StepGenerator):
    """Add two matrices element-wise."""

    @property
    def task_name(self) -> str:
        return "matrix_add"

    @property
    def tier(self) -> int:
        return 3

    @property
    def prerequisites(self) -> list[str]:
        return ["addition"]

    def task_description(self, difficulty: int) -> str:
        return "add two matrices"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        size = 2 if difficulty < 5 else 3
        mag = 5 + difficulty * 3
        a = [[self._rng.randint(-mag, mag) for _ in range(size)] for _ in range(size)]
        b = [[self._rng.randint(-mag, mag) for _ in range(size)] for _ in range(size)]
        result = [[a[i][j] + b[i][j] for j in range(size)] for i in range(size)]

        def fmt(m):
            rows = [" & ".join(str(x) for x in row) for row in m]
            return "\\begin{pmatrix}" + " \\\\ ".join(rows) + "\\end{pmatrix}"

        problem = f"{fmt(a)} + {fmt(b)}"
        return problem, {"a": a, "b": b, "result": result, "size": size}

    def _create_steps(self, sd: dict) -> list[str]:
        steps = []
        for i in range(sd["size"]):
            for j in range(sd["size"]):
                steps.append(f"c_{{{i+1}{j+1}}}={sd['a'][i][j]}+{sd['b'][i][j]}={sd['result'][i][j]}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        rows = [",".join(str(x) for x in row) for row in sd["result"]]
        return "[" + ";".join(rows) + "]"


@register
class MatrixScalarGenerator(StepGenerator):
    """Multiply a matrix by a scalar."""

    @property
    def task_name(self) -> str:
        return "matrix_scalar"

    @property
    def tier(self) -> int:
        return 3

    @property
    def prerequisites(self) -> list[str]:
        return ["multiplication"]

    def task_description(self, difficulty: int) -> str:
        return "multiply matrix by scalar"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        size = 2 if difficulty < 5 else 3
        scalar = self._rng.randint(2, 5 + difficulty)
        m = [[self._rng.randint(-10, 10) for _ in range(size)] for _ in range(size)]
        result = [[scalar * m[i][j] for j in range(size)] for i in range(size)]

        rows = [" & ".join(str(x) for x in row) for row in m]
        mat_str = "\\begin{pmatrix}" + " \\\\ ".join(rows) + "\\end{pmatrix}"
        problem = f"{scalar} \\cdot {mat_str}"
        return problem, {"scalar": scalar, "m": m, "result": result, "size": size}

    def _create_steps(self, sd: dict) -> list[str]:
        steps = []
        for i in range(sd["size"]):
            for j in range(sd["size"]):
                steps.append(f"{sd['scalar']}*{sd['m'][i][j]}={sd['result'][i][j]}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        rows = [",".join(str(x) for x in row) for row in sd["result"]]
        return "[" + ";".join(rows) + "]"


@register
class DotProductGenerator(StepGenerator):
    """Compute dot product of two vectors."""

    @property
    def task_name(self) -> str:
        return "dot_product"

    @property
    def tier(self) -> int:
        return 3

    @property
    def prerequisites(self) -> list[str]:
        return ["multiplication", "addition"]

    def task_description(self, difficulty: int) -> str:
        return "compute dot product"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        length = min(2 + difficulty, 6)
        a = [self._rng.randint(-10, 10) for _ in range(length)]
        b = [self._rng.randint(-10, 10) for _ in range(length)]
        products = [x * y for x, y in zip(a, b)]
        result = sum(products)
        problem = f"[{','.join(str(x) for x in a)}] \\cdot [{','.join(str(x) for x in b)}]"
        return problem, {"a": a, "b": b, "products": products, "result": result}

    def _create_steps(self, sd: dict) -> list[str]:
        steps = [f"{a}*{b}={p}" for a, b, p in
                 zip(sd["a"], sd["b"], sd["products"])]
        steps.append(f"sum={sd['result']}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        return str(sd["result"])


# ── TIER 4 (33 → 37) ───────────────────────────────────────────────

@register
class MatrixTransposeGenerator(StepGenerator):
    """Compute the transpose of a matrix."""

    @property
    def task_name(self) -> str:
        return "matrix_transpose"

    @property
    def tier(self) -> int:
        return 4

    @property
    def prerequisites(self) -> list[str]:
        return ["matrix_add"]

    def task_description(self, difficulty: int) -> str:
        return "transpose matrix"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        rows = self._rng.choice([2, 3]) if difficulty < 5 else 3
        cols = self._rng.choice([2, 3])
        m = [[self._rng.randint(-10, 10) for _ in range(cols)] for _ in range(rows)]
        result = [[m[i][j] for i in range(rows)] for j in range(cols)]

        row_strs = [" & ".join(str(x) for x in row) for row in m]
        mat_str = "\\begin{pmatrix}" + " \\\\ ".join(row_strs) + "\\end{pmatrix}"
        problem = f"{mat_str}^T"
        return problem, {"m": m, "result": result, "rows": rows, "cols": cols}

    def _create_steps(self, sd: dict) -> list[str]:
        return [f"row {j+1} -> col {j+1}" for j in range(sd["cols"])]

    def _create_answer(self, sd: dict) -> str:
        rows = [",".join(str(x) for x in row) for row in sd["result"]]
        return "[" + ";".join(rows) + "]"


@register
class TraceGenerator(StepGenerator):
    """Compute the trace of a square matrix."""

    @property
    def task_name(self) -> str:
        return "matrix_trace"

    @property
    def tier(self) -> int:
        return 4

    @property
    def prerequisites(self) -> list[str]:
        return ["addition"]

    def task_description(self, difficulty: int) -> str:
        return "compute matrix trace"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        size = 2 if difficulty < 4 else 3 if difficulty < 7 else 4
        m = [[self._rng.randint(-20, 20) for _ in range(size)] for _ in range(size)]
        diag = [m[i][i] for i in range(size)]
        result = sum(diag)

        row_strs = [" & ".join(str(x) for x in row) for row in m]
        mat_str = "\\begin{pmatrix}" + " \\\\ ".join(row_strs) + "\\end{pmatrix}"
        problem = f"tr({mat_str})"
        return problem, {"m": m, "diag": diag, "result": result}

    def _create_steps(self, sd: dict) -> list[str]:
        return [f"diag=[{','.join(str(d) for d in sd['diag'])}]",
                f"sum={sd['result']}"]

    def _create_answer(self, sd: dict) -> str:
        return str(sd["result"])


@register
class NormGenerator(StepGenerator):
    """Compute L1 or L2 norm of a vector."""

    @property
    def task_name(self) -> str:
        return "vector_norm"

    @property
    def tier(self) -> int:
        return 4

    @property
    def prerequisites(self) -> list[str]:
        return ["exponentiation", "addition"]

    def task_description(self, difficulty: int) -> str:
        return "compute vector norm"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        length = min(2 + difficulty // 2, 5)
        values = [self._rng.randint(-10, 10) for _ in range(length)]
        norm_type = self._rng.choice(["L1", "L2"])

        if norm_type == "L1":
            result = sum(abs(v) for v in values)
            problem = f"||[{','.join(str(v) for v in values)}]||_1"
        else:
            sq_sum = sum(v * v for v in values)
            result = round(math.sqrt(sq_sum), 4)
            problem = f"||[{','.join(str(v) for v in values)}]||_2"

        return problem, {"values": values, "norm_type": norm_type,
                         "result": result}

    def _create_steps(self, sd: dict) -> list[str]:
        if sd["norm_type"] == "L1":
            abs_vals = [abs(v) for v in sd["values"]]
            return [f"|{v}|={a}" for v, a in zip(sd["values"], abs_vals)] + \
                   [f"sum={sum(abs_vals)}"]
        else:
            squares = [v * v for v in sd["values"]]
            return [f"{v}^2={s}" for v, s in zip(sd["values"], squares)] + \
                   [f"sum={sum(squares)}", f"sqrt={sd['result']}"]

    def _create_answer(self, sd: dict) -> str:
        r = sd["result"]
        return str(int(r)) if r == int(r) else str(r)


@register
class CrossProductGenerator(StepGenerator):
    """Compute cross product of two 3D vectors."""

    @property
    def task_name(self) -> str:
        return "cross_product"

    @property
    def tier(self) -> int:
        return 4

    @property
    def prerequisites(self) -> list[str]:
        return ["multiplication", "subtraction"]

    def task_description(self, difficulty: int) -> str:
        return "compute cross product"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        mag = 3 + difficulty * 2
        a = [self._rng.randint(-mag, mag) for _ in range(3)]
        b = [self._rng.randint(-mag, mag) for _ in range(3)]
        result = [
            a[1] * b[2] - a[2] * b[1],
            a[2] * b[0] - a[0] * b[2],
            a[0] * b[1] - a[1] * b[0],
        ]
        problem = f"[{a[0]},{a[1]},{a[2]}] x [{b[0]},{b[1]},{b[2]}]"
        return problem, {"a": a, "b": b, "result": result}

    def _create_steps(self, sd: dict) -> list[str]:
        a, b = sd["a"], sd["b"]
        return [
            f"i: {a[1]}*{b[2]}-{a[2]}*{b[1]}={sd['result'][0]}",
            f"j: {a[2]}*{b[0]}-{a[0]}*{b[2]}={sd['result'][1]}",
            f"k: {a[0]}*{b[1]}-{a[1]}*{b[0]}={sd['result'][2]}",
        ]

    def _create_answer(self, sd: dict) -> str:
        return f"[{sd['result'][0]},{sd['result'][1]},{sd['result'][2]}]"


# ── TIER 5 (46 → 50) ───────────────────────────────────────────────

@register
class ImplicitDiffGenerator(StepGenerator):
    """Implicit differentiation of x^2 + y^2 = r^2 style equations."""

    @property
    def task_name(self) -> str:
        return "implicit_diff"

    @property
    def tier(self) -> int:
        return 5

    @property
    def prerequisites(self) -> list[str]:
        return ["derivative", "chain_rule"]

    def task_description(self, difficulty: int) -> str:
        return "implicit differentiation"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        a = self._rng.randint(1, 5)
        b = self._rng.randint(1, 5)
        c = self._rng.randint(1, 20)
        problem = f"d/dx({a}x^2 + {b}y^2 = {c})"
        dy_dx = f"-{a}x/({b}y)"
        return problem, {"a": a, "b": b, "c": c, "dy_dx": dy_dx}

    def _create_steps(self, sd: dict) -> list[str]:
        return [
            f"{2*sd['a']}x + {2*sd['b']}y*dy/dx = 0",
            f"{2*sd['b']}y*dy/dx = -{2*sd['a']}x",
            f"dy/dx = -{2*sd['a']}x/({2*sd['b']}y)",
        ]

    def _create_answer(self, sd: dict) -> str:
        return sd["dy_dx"]


@register
class AreaUnderCurveGenerator(StepGenerator):
    """Compute area under a polynomial curve between bounds."""

    @property
    def task_name(self) -> str:
        return "area_under_curve"

    @property
    def tier(self) -> int:
        return 5

    @property
    def prerequisites(self) -> list[str]:
        return ["definite_integral"]

    def task_description(self, difficulty: int) -> str:
        return "compute area under curve"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        a = self._rng.randint(0, 3)
        b = a + self._rng.randint(1, 3 + difficulty)
        coeff = self._rng.randint(1, 5)
        power = self._rng.randint(1, min(difficulty, 3))

        antideriv_b = coeff * b ** (power + 1) / (power + 1)
        antideriv_a = coeff * a ** (power + 1) / (power + 1)
        area = abs(antideriv_b - antideriv_a)

        problem = f"\\int_{{{a}}}^{{{b}}} {coeff}x^{power} dx"
        return problem, {"a": a, "b": b, "coeff": coeff, "power": power,
                         "area": area, "F_b": antideriv_b, "F_a": antideriv_a}

    def _create_steps(self, sd: dict) -> list[str]:
        p1 = sd["power"] + 1
        return [
            f"F(x) = {sd['coeff']}/{p1} x^{p1}",
            f"F({sd['b']}) = {sd['F_b']}",
            f"F({sd['a']}) = {sd['F_a']}",
            f"|F(b)-F(a)| = {sd['area']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        a = sd["area"]
        return str(int(a)) if a == int(a) else f"{a:.4f}"


@register
class RelatedRatesGenerator(StepGenerator):
    """Related rates problem: given dr/dt, find dA/dt for circle."""

    @property
    def task_name(self) -> str:
        return "related_rates"

    @property
    def tier(self) -> int:
        return 5

    @property
    def prerequisites(self) -> list[str]:
        return ["chain_rule", "derivative"]

    def task_description(self, difficulty: int) -> str:
        return "solve related rates"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        r = self._rng.randint(2, 10 + difficulty)
        dr_dt = self._rng.randint(1, 5)
        dA_dt = 2 * math.pi * r * dr_dt
        problem = f"A=\\pi r^2, r={r}, dr/dt={dr_dt}, find dA/dt"
        return problem, {"r": r, "dr_dt": dr_dt, "dA_dt": round(dA_dt, 4)}

    def _create_steps(self, sd: dict) -> list[str]:
        return [
            "dA/dt = 2*pi*r*dr/dt",
            f"= 2*pi*{sd['r']}*{sd['dr_dt']}",
            f"= {sd['dA_dt']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        return str(sd["dA_dt"])


@register
class LogarithmGenerator(StepGenerator):
    """Evaluate logarithms base 2, 10, or e."""

    @property
    def task_name(self) -> str:
        return "logarithm"

    @property
    def tier(self) -> int:
        return 5

    @property
    def prerequisites(self) -> list[str]:
        return ["exponentiation"]

    def task_description(self, difficulty: int) -> str:
        return "evaluate logarithm"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a logarithm evaluation problem with randomised base and exponent.

        Args:
            difficulty: Controls exponent range and base variety.

        Returns:
            Tuple of (problem_string, solution_data).
        """
        base = self._rng.choice([2, 3, 4, 5, 7, 8, 10])
        exp = self._rng.randint(1, min(4 + difficulty, 10))
        value = base ** exp
        problem = f"\\log_{{{base}}}({value})"
        return problem, {"base": base, "value": value, "exp": exp}

    def _create_steps(self, sd: dict) -> list[str]:
        return [f"{sd['base']}^{sd['exp']}={sd['value']}"]

    def _create_answer(self, sd: dict) -> str:
        return str(sd["exp"])


# ── TIER 6 (36 → 40) ───────────────────────────────────────────────

@register
class PartialDerivativeMultiGenerator(StepGenerator):
    """Compute multiple partial derivatives of a multivariate function."""

    @property
    def task_name(self) -> str:
        return "partial_deriv_multi"

    @property
    def tier(self) -> int:
        return 6

    @property
    def prerequisites(self) -> list[str]:
        return ["partial_derivative", "product_rule"]

    def task_description(self, difficulty: int) -> str:
        return "compute partial derivatives"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        a = self._rng.randint(1, 5)
        b = self._rng.randint(1, 5)
        c = self._rng.randint(1, 5)
        problem = f"f(x,y) = {a}x^2y + {b}xy^2 + {c}x"
        df_dx = f"{2*a}xy + {b}y^2 + {c}"
        df_dy = f"{a}x^2 + {2*b}xy"
        return problem, {"a": a, "b": b, "c": c, "df_dx": df_dx, "df_dy": df_dy}

    def _create_steps(self, sd: dict) -> list[str]:
        return [
            f"df/dx: {2*sd['a']}xy + {sd['b']}y^2 + {sd['c']}",
            f"df/dy: {sd['a']}x^2 + {2*sd['b']}xy",
        ]

    def _create_answer(self, sd: dict) -> str:
        return f"dx={sd['df_dx']}; dy={sd['df_dy']}"


@register
class MatrixPowerGenerator(StepGenerator):
    """Compute A^n for a 2x2 matrix by repeated multiplication."""

    @property
    def task_name(self) -> str:
        return "matrix_power"

    @property
    def tier(self) -> int:
        return 6

    @property
    def prerequisites(self) -> list[str]:
        return ["matrix_multiply"]

    def task_description(self, difficulty: int) -> str:
        return "compute matrix power"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        m = [[self._rng.randint(-3, 3) for _ in range(2)] for _ in range(2)]
        power = min(2 + difficulty // 3, 4)

        def mat_mul(a, b):
            return [
                [a[0][0]*b[0][0] + a[0][1]*b[1][0], a[0][0]*b[0][1] + a[0][1]*b[1][1]],
                [a[1][0]*b[0][0] + a[1][1]*b[1][0], a[1][0]*b[0][1] + a[1][1]*b[1][1]],
            ]

        result = [[1, 0], [0, 1]]
        steps = []
        for p in range(power):
            result = mat_mul(result, m)
            steps.append(f"A^{p+1}=[{result[0][0]},{result[0][1]};{result[1][0]},{result[1][1]}]")

        rows = [" & ".join(str(x) for x in row) for row in m]
        mat_str = "\\begin{pmatrix}" + " \\\\ ".join(rows) + "\\end{pmatrix}"
        problem = f"{mat_str}^{power}"
        return problem, {"m": m, "power": power, "result": result, "steps_data": steps}

    def _create_steps(self, sd: dict) -> list[str]:
        return sd["steps_data"]

    def _create_answer(self, sd: dict) -> str:
        r = sd["result"]
        return f"[{r[0][0]},{r[0][1]};{r[1][0]},{r[1][1]}]"


@register
class SystemODEGenerator(StepGenerator):
    """Solve a simple system of first-order ODEs by substitution."""

    @property
    def task_name(self) -> str:
        return "system_ode"

    @property
    def tier(self) -> int:
        return 6

    @property
    def prerequisites(self) -> list[str]:
        return ["diff_equation", "system_equations"]

    def task_description(self, difficulty: int) -> str:
        return "solve ODE system"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a first-order ODE problem with randomised coefficients.

        Args:
            difficulty: Controls coefficient range.

        Returns:
            Tuple of (problem_string, solution_data).
        """
        max_coeff = min(2 + difficulty, 8)
        a = self._rng.randint(-max_coeff, max_coeff)
        if a == 0:
            a = self._rng.choice([-1, 1])
        b = self._rng.randint(1, max(3, 2 * difficulty))
        problem = f"dx/dt = {a}x, x(0) = {b}"
        solution = f"{b}e^{{{a}t}}"
        return problem, {"a": a, "b": b, "solution": solution}

    def _create_steps(self, sd: dict) -> list[str]:
        return [
            "dx/x = a*dt",
            f"ln|x| = {sd['a']}t + C",
            f"x(0) = {sd['b']} => C = ln({sd['b']})",
            f"x(t) = {sd['solution']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        return sd["solution"]


@register
class ConvolutionMatrixGenerator(StepGenerator):
    """Apply a 3x3 convolution kernel to a small matrix."""

    @property
    def task_name(self) -> str:
        return "conv_2d"

    @property
    def tier(self) -> int:
        return 6

    @property
    def prerequisites(self) -> list[str]:
        return ["matrix_multiply", "convolution"]

    def task_description(self, difficulty: int) -> str:
        return "apply 2D convolution"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        in_size = min(3 + difficulty // 2, 5)
        inp = [[self._rng.randint(0, 9) for _ in range(in_size)] for _ in range(in_size)]
        kernels = [
            [[1, 0, -1], [1, 0, -1], [1, 0, -1]],
            [[0, -1, 0], [-1, 4, -1], [0, -1, 0]],
            [[1, 1, 1], [1, 1, 1], [1, 1, 1]],
        ]
        kernel = self._rng.choice(kernels)
        out_size = in_size - 2

        output = []
        steps = []
        for i in range(out_size):
            row = []
            for j in range(out_size):
                val = 0
                for ki in range(3):
                    for kj in range(3):
                        val += inp[i + ki][j + kj] * kernel[ki][kj]
                row.append(val)
                steps.append(f"out[{i},{j}]={val}")
            output.append(row)

        problem = f"conv({in_size}x{in_size}, 3x3 kernel)"
        return problem, {"input": inp, "kernel": kernel, "output": output,
                         "steps_data": steps}

    def _create_steps(self, sd: dict) -> list[str]:
        return sd["steps_data"]

    def _create_answer(self, sd: dict) -> str:
        rows = [",".join(str(x) for x in row) for row in sd["output"]]
        return "[" + ";".join(rows) + "]"
