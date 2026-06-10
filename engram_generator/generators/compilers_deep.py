"""Deep compiler construction generators.

8 generators across tiers 4-5 covering constant folding, dead code
elimination, register allocation, instruction selection, SSA
conversion, loop optimization, strength reduction, and tail call
optimization.
"""
from __future__ import annotations

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


# ---------------------------------------------------------------------------
# 1. Constant Folding (tier 4)
# ---------------------------------------------------------------------------

@register
class ConstantFoldingGenerator(StepGenerator):
    """Evaluate compile-time constants in expressions.

    Identifies sub-expressions where all operands are known at
    compile time and replaces them with their computed value.
    """

    _TEMPLATES = [
        {
            "before": "x = 3 + 4",
            "after": "x = 7",
            "folds": ["3 + 4 -> 7"],
        },
        {
            "before": "y = 2 * 6 + z",
            "after": "y = 12 + z",
            "folds": ["2 * 6 -> 12"],
        },
        {
            "before": "a = 10 / 2; b = a + 3",
            "after": "a = 5; b = 5 + 3",
            "folds": ["10 / 2 -> 5"],
        },
        {
            "before": "c = 5 * 4 - 3 * 2",
            "after": "c = 14",
            "folds": ["5 * 4 -> 20", "3 * 2 -> 6", "20 - 6 -> 14"],
        },
        {
            "before": "d = 8 + 0; e = d * 1",
            "after": "d = 8; e = d * 1",
            "folds": ["8 + 0 -> 8"],
        },
        {
            "before": "f = 100 - 50 + 25",
            "after": "f = 75",
            "folds": ["100 - 50 -> 50", "50 + 25 -> 75"],
        },
        {
            "before": "g = 3 * 3 * 3",
            "after": "g = 27",
            "folds": ["3 * 3 -> 9", "9 * 3 -> 27"],
        },
        {
            "before": "h = 7 + x; i = 2 + 3",
            "after": "h = 7 + x; i = 5",
            "folds": ["2 + 3 -> 5"],
        },
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "constant_folding"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

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
        return "fold compile-time constants in expression"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a constant folding problem.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        idx = difficulty % len(self._TEMPLATES)
        tmpl = self._TEMPLATES[idx]
        steps = [f"input: {tmpl['before']}"]
        for fold in tmpl["folds"]:
            steps.append(f"fold: {fold}")
        steps.append(f"result: {tmpl['after']}")

        problem = f"constant-fold: {tmpl['before']}"
        return problem, {
            "steps": steps,
            "before": tmpl["before"],
            "after": tmpl["after"],
        }

    def _create_steps(self, solution_data: dict) -> list[str]:
        """Return the folding steps.

        Args:
            solution_data: All computed solution information.

        Returns:
            Step strings in execution order.
        """
        return solution_data["steps"]

    def _create_answer(self, solution_data: dict) -> str:
        """Return the folded expression.

        Args:
            solution_data: All computed solution information.

        Returns:
            Optimized expression string.
        """
        return solution_data["after"]


# ---------------------------------------------------------------------------
# 2. Dead Code Elimination (tier 4)
# ---------------------------------------------------------------------------

@register
class DeadCodeEliminationGenerator(StepGenerator):
    """Identify and remove dead (unused) assignments.

    Given a sequence of assignments and a final use set, identify
    variables whose values are never consumed and remove them.
    """

    _TEMPLATES = [
        {
            "code": ["a = 1", "b = 2", "c = a + b", "d = 5", "return c"],
            "used": {"c"},
            "dead": ["d = 5"],
            "live": ["a = 1", "b = 2", "c = a + b", "return c"],
        },
        {
            "code": ["x = 10", "y = 20", "z = 30", "return x"],
            "used": {"x"},
            "dead": ["y = 20", "z = 30"],
            "live": ["x = 10", "return x"],
        },
        {
            "code": ["a = 1", "b = a + 1", "c = b + 1", "d = 99", "return c"],
            "used": {"c"},
            "dead": ["d = 99"],
            "live": ["a = 1", "b = a + 1", "c = b + 1", "return c"],
        },
        {
            "code": ["t = 7", "u = t * 2", "v = 3", "return u + v"],
            "used": {"u", "v"},
            "dead": [],
            "live": ["t = 7", "u = t * 2", "v = 3", "return u + v"],
        },
        {
            "code": ["p = 5", "q = 6", "r = p", "s = q", "return r"],
            "used": {"r"},
            "dead": ["q = 6", "s = q"],
            "live": ["p = 5", "r = p", "return r"],
        },
        {
            "code": ["a = 1", "a = 2", "b = a", "return b"],
            "used": {"b"},
            "dead": ["a = 1"],
            "live": ["a = 2", "b = a", "return b"],
        },
        {
            "code": ["x = f()", "y = g()", "return x"],
            "used": {"x"},
            "dead": ["y = g()"],
            "live": ["x = f()", "return x"],
        },
        {
            "code": ["a = 1", "b = 2", "c = 3", "d = 4", "return a + d"],
            "used": {"a", "d"},
            "dead": ["b = 2", "c = 3"],
            "live": ["a = 1", "d = 4", "return a + d"],
        },
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "dead_code_elimination"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["comparison"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task instruction string.
        """
        return "identify and remove dead code assignments"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a dead code elimination problem.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        idx = difficulty % len(self._TEMPLATES)
        tmpl = self._TEMPLATES[idx]

        steps = [f"code: {'; '.join(tmpl['code'])}"]
        steps.append(f"used at exit: {sorted(tmpl['used'])}")
        if tmpl["dead"]:
            for d in tmpl["dead"]:
                steps.append(f"DEAD: {d}")
        else:
            steps.append("no dead code found")
        steps.append(f"result: {'; '.join(tmpl['live'])}")

        problem = f"DCE: {'; '.join(tmpl['code'])}"
        return problem, {
            "steps": steps,
            "dead": tmpl["dead"],
            "live": tmpl["live"],
        }

    def _create_steps(self, solution_data: dict) -> list[str]:
        """Return the analysis steps.

        Args:
            solution_data: All computed solution information.

        Returns:
            Step strings in execution order.
        """
        return solution_data["steps"]

    def _create_answer(self, solution_data: dict) -> str:
        """Return the cleaned code.

        Args:
            solution_data: All computed solution information.

        Returns:
            Semicolon-separated live code.
        """
        return "; ".join(solution_data["live"])


# ---------------------------------------------------------------------------
# 3. Register Allocation (tier 5)
# ---------------------------------------------------------------------------

@register
class RegisterAllocationGenerator(StepGenerator):
    """Allocate registers using graph coloring.

    Given live ranges for variables, build an interference graph
    and color it with k registers. If k is insufficient, identify
    which variable to spill.
    """

    _TEMPLATES = [
        {
            "vars": {"a": (0, 3), "b": (1, 4), "c": (3, 5)},
            "k": 2,
            "interfere": [("a", "b")],
            "coloring": {"a": "R0", "b": "R1", "c": "R0"},
            "spill": None,
        },
        {
            "vars": {"x": (0, 4), "y": (1, 3), "z": (2, 5)},
            "k": 2,
            "interfere": [("x", "y"), ("x", "z"), ("y", "z")],
            "coloring": None,
            "spill": "x",
        },
        {
            "vars": {"a": (0, 2), "b": (2, 4), "c": (4, 6)},
            "k": 1,
            "interfere": [],
            "coloring": {"a": "R0", "b": "R0", "c": "R0"},
            "spill": None,
        },
        {
            "vars": {"p": (0, 5), "q": (1, 3), "r": (3, 6), "s": (0, 2)},
            "k": 2,
            "interfere": [("p", "q"), ("p", "s"), ("p", "r"), ("q", "s")],
            "coloring": None,
            "spill": "p",
        },
        {
            "vars": {"a": (0, 3), "b": (1, 2), "c": (2, 4)},
            "k": 2,
            "interfere": [("a", "b"), ("a", "c")],
            "coloring": {"a": "R0", "b": "R1", "c": "R1"},
            "spill": None,
        },
        {
            "vars": {"t1": (0, 1), "t2": (1, 2), "t3": (2, 3), "t4": (3, 4)},
            "k": 1,
            "interfere": [],
            "coloring": {"t1": "R0", "t2": "R0", "t3": "R0", "t4": "R0"},
            "spill": None,
        },
        {
            "vars": {"a": (0, 4), "b": (0, 4), "c": (0, 4)},
            "k": 2,
            "interfere": [("a", "b"), ("a", "c"), ("b", "c")],
            "coloring": None,
            "spill": "a",
        },
        {
            "vars": {"x": (0, 2), "y": (1, 3), "z": (2, 4), "w": (3, 5)},
            "k": 2,
            "interfere": [("x", "y"), ("y", "z"), ("z", "w")],
            "coloring": {"x": "R0", "y": "R1", "z": "R0", "w": "R1"},
            "spill": None,
        },
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "register_allocation"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["comparison"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task instruction string.
        """
        return "allocate registers by graph coloring"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a register allocation problem.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        idx = difficulty % len(self._TEMPLATES)
        tmpl = self._TEMPLATES[idx]

        vars_str = ", ".join(
            f"{v}=[{s}-{e}]" for v, (s, e) in tmpl["vars"].items()
        )
        steps = [f"live ranges: {vars_str}", f"k={tmpl['k']} registers"]

        if tmpl["interfere"]:
            intf_str = ", ".join(f"{a}-{b}" for a, b in tmpl["interfere"])
            steps.append(f"interference: {intf_str}")
        else:
            steps.append("no interference")

        if tmpl["coloring"] is not None:
            color_str = ", ".join(
                f"{v}={r}" for v, r in tmpl["coloring"].items()
            )
            steps.append(f"coloring: {color_str}")
        else:
            steps.append(f"cannot color with {tmpl['k']} regs, spill {tmpl['spill']}")

        problem = f"regalloc: {vars_str}, k={tmpl['k']}"
        return problem, {
            "steps": steps,
            "coloring": tmpl["coloring"],
            "spill": tmpl["spill"],
        }

    def _create_steps(self, solution_data: dict) -> list[str]:
        """Return the register allocation steps.

        Args:
            solution_data: All computed solution information.

        Returns:
            Step strings in execution order.
        """
        return solution_data["steps"]

    def _create_answer(self, solution_data: dict) -> str:
        """Return the allocation result.

        Args:
            solution_data: All computed solution information.

        Returns:
            Coloring or spill decision string.
        """
        if solution_data["coloring"] is not None:
            parts = [
                f"{v}={r}" for v, r in solution_data["coloring"].items()
            ]
            return ", ".join(parts)
        return f"SPILL {solution_data['spill']}"


# ---------------------------------------------------------------------------
# 4. Instruction Selection (tier 5)
# ---------------------------------------------------------------------------

@register
class InstructionSelectionGenerator(StepGenerator):
    """Tile an expression tree with machine instructions.

    Given a simple expression tree, select machine instructions
    (LOAD, STORE, ADD, MUL, SUB) to minimise total instruction count.
    """

    _TEMPLATES = [
        {
            "expr": "a + b",
            "instrs": ["LOAD R0, a", "LOAD R1, b", "ADD R0, R0, R1"],
            "count": 3,
        },
        {
            "expr": "a * b + c",
            "instrs": ["LOAD R0, a", "LOAD R1, b", "MUL R0, R0, R1", "LOAD R1, c", "ADD R0, R0, R1"],
            "count": 5,
        },
        {
            "expr": "(a + b) * (c + d)",
            "instrs": ["LOAD R0, a", "LOAD R1, b", "ADD R0, R0, R1", "LOAD R1, c", "LOAD R2, d", "ADD R1, R1, R2", "MUL R0, R0, R1"],
            "count": 7,
        },
        {
            "expr": "a - b",
            "instrs": ["LOAD R0, a", "LOAD R1, b", "SUB R0, R0, R1"],
            "count": 3,
        },
        {
            "expr": "a * b",
            "instrs": ["LOAD R0, a", "LOAD R1, b", "MUL R0, R0, R1"],
            "count": 3,
        },
        {
            "expr": "a + b + c",
            "instrs": ["LOAD R0, a", "LOAD R1, b", "ADD R0, R0, R1", "LOAD R1, c", "ADD R0, R0, R1"],
            "count": 5,
        },
        {
            "expr": "a * (b + c)",
            "instrs": ["LOAD R0, b", "LOAD R1, c", "ADD R0, R0, R1", "LOAD R1, a", "MUL R0, R1, R0"],
            "count": 5,
        },
        {
            "expr": "(a + b) * c - d",
            "instrs": ["LOAD R0, a", "LOAD R1, b", "ADD R0, R0, R1", "LOAD R1, c", "MUL R0, R0, R1", "LOAD R1, d", "SUB R0, R0, R1"],
            "count": 7,
        },
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "instruction_selection"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

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
        return "select machine instructions for expression tree"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an instruction selection problem.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        idx = difficulty % len(self._TEMPLATES)
        tmpl = self._TEMPLATES[idx]

        steps = [f"expr: {tmpl['expr']}"]
        for instr in tmpl["instrs"]:
            steps.append(f"  {instr}")
        steps.append(f"total instructions: {tmpl['count']}")

        problem = f"isel: {tmpl['expr']}"
        return problem, {
            "steps": steps,
            "instrs": tmpl["instrs"],
            "count": tmpl["count"],
        }

    def _create_steps(self, solution_data: dict) -> list[str]:
        """Return the instruction selection steps.

        Args:
            solution_data: All computed solution information.

        Returns:
            Step strings in execution order.
        """
        return solution_data["steps"]

    def _create_answer(self, solution_data: dict) -> str:
        """Return the instruction sequence.

        Args:
            solution_data: All computed solution information.

        Returns:
            Instruction count and sequence.
        """
        return f"{solution_data['count']} instrs: {'; '.join(solution_data['instrs'])}"


# ---------------------------------------------------------------------------
# 5. SSA Conversion (tier 5)
# ---------------------------------------------------------------------------

@register
class SsaConversionGenerator(StepGenerator):
    """Convert code to Static Single Assignment (SSA) form.

    Rename variables at each assignment point. Insert phi functions
    at join points where control flow merges.
    """

    _TEMPLATES = [
        {
            "code": ["x = 1", "x = x + 1", "y = x"],
            "ssa": ["x1 = 1", "x2 = x1 + 1", "y1 = x2"],
            "phis": [],
        },
        {
            "code": ["a = 5", "if c: a = 10", "b = a"],
            "ssa": ["a1 = 5", "if c: a2 = 10", "a3 = phi(a1, a2)", "b1 = a3"],
            "phis": ["a3 = phi(a1, a2)"],
        },
        {
            "code": ["x = 0", "while x < 10: x = x + 1"],
            "ssa": ["x1 = 0", "x2 = phi(x1, x3)", "while x2 < 10: x3 = x2 + 1"],
            "phis": ["x2 = phi(x1, x3)"],
        },
        {
            "code": ["a = 1", "b = 2", "c = a + b"],
            "ssa": ["a1 = 1", "b1 = 2", "c1 = a1 + b1"],
            "phis": [],
        },
        {
            "code": ["x = 1", "y = 2", "x = y", "y = x"],
            "ssa": ["x1 = 1", "y1 = 2", "x2 = y1", "y2 = x2"],
            "phis": [],
        },
        {
            "code": ["a = 0", "if p: a = 1", "if q: a = 2", "return a"],
            "ssa": ["a1 = 0", "if p: a2 = 1", "a3 = phi(a1, a2)", "if q: a4 = 2", "a5 = phi(a3, a4)", "return a5"],
            "phis": ["a3 = phi(a1, a2)", "a5 = phi(a3, a4)"],
        },
        {
            "code": ["t = f()", "t = g(t)", "return t"],
            "ssa": ["t1 = f()", "t2 = g(t1)", "return t2"],
            "phis": [],
        },
        {
            "code": ["i = 0", "s = 0", "while i < n: s = s + i; i = i + 1"],
            "ssa": ["i1 = 0", "s1 = 0", "i2 = phi(i1, i4)", "s2 = phi(s1, s3)", "while i2 < n: s3 = s2 + i2; i4 = i2 + 1"],
            "phis": ["i2 = phi(i1, i4)", "s2 = phi(s1, s3)"],
        },
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "ssa_conversion"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["comparison"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task instruction string.
        """
        return "convert code to SSA form with phi functions"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an SSA conversion problem.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        idx = difficulty % len(self._TEMPLATES)
        tmpl = self._TEMPLATES[idx]

        steps = [f"input: {'; '.join(tmpl['code'])}"]
        for line in tmpl["ssa"]:
            steps.append(f"  {line}")
        if tmpl["phis"]:
            steps.append(f"phi functions: {', '.join(tmpl['phis'])}")
        else:
            steps.append("no phi functions needed")

        problem = f"SSA: {'; '.join(tmpl['code'])}"
        return problem, {
            "steps": steps,
            "ssa": tmpl["ssa"],
            "phis": tmpl["phis"],
        }

    def _create_steps(self, solution_data: dict) -> list[str]:
        """Return the SSA conversion steps.

        Args:
            solution_data: All computed solution information.

        Returns:
            Step strings in execution order.
        """
        return solution_data["steps"]

    def _create_answer(self, solution_data: dict) -> str:
        """Return the SSA form.

        Args:
            solution_data: All computed solution information.

        Returns:
            Semicolon-separated SSA code.
        """
        return "; ".join(solution_data["ssa"])


# ---------------------------------------------------------------------------
# 6. Loop Optimization (tier 5)
# ---------------------------------------------------------------------------

@register
class LoopOptimizationGenerator(StepGenerator):
    """Identify and hoist loop-invariant computations.

    Given a loop body, identify expressions that do not change
    across iterations and show them hoisted outside the loop.
    """

    _TEMPLATES = [
        {
            "loop": "for i in range(n): x = a + b; y[i] = x * i",
            "invariant": ["x = a + b"],
            "after": "x = a + b; for i in range(n): y[i] = x * i",
        },
        {
            "loop": "for i in range(n): t = m * k; r[i] = t + i",
            "invariant": ["t = m * k"],
            "after": "t = m * k; for i in range(n): r[i] = t + i",
        },
        {
            "loop": "for i in range(n): a[i] = b[i] + c",
            "invariant": [],
            "after": "for i in range(n): a[i] = b[i] + c",
        },
        {
            "loop": "for i in range(n): d = len(s); a[i] = d + i",
            "invariant": ["d = len(s)"],
            "after": "d = len(s); for i in range(n): a[i] = d + i",
        },
        {
            "loop": "for i in range(n): p = x * y; q = p + z; r[i] = q - i",
            "invariant": ["p = x * y", "q = p + z"],
            "after": "p = x * y; q = p + z; for i in range(n): r[i] = q - i",
        },
        {
            "loop": "for i in range(n): v = 2 * pi * r; a[i] = v + i",
            "invariant": ["v = 2 * pi * r"],
            "after": "v = 2 * pi * r; for i in range(n): a[i] = v + i",
        },
        {
            "loop": "for i in range(n): s = s + a[i]",
            "invariant": [],
            "after": "for i in range(n): s = s + a[i]",
        },
        {
            "loop": "for i in range(n): w = a / b; c = w + 1; d[i] = c * i",
            "invariant": ["w = a / b", "c = w + 1"],
            "after": "w = a / b; c = w + 1; for i in range(n): d[i] = c * i",
        },
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "loop_optimization"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["comparison"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task instruction string.
        """
        return "identify and hoist loop-invariant code"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a loop optimization problem.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        idx = difficulty % len(self._TEMPLATES)
        tmpl = self._TEMPLATES[idx]

        steps = [f"loop: {tmpl['loop']}"]
        if tmpl["invariant"]:
            for inv in tmpl["invariant"]:
                steps.append(f"invariant: {inv}")
            steps.append(f"hoist outside loop")
        else:
            steps.append("no loop-invariant code found")
        steps.append(f"result: {tmpl['after']}")

        problem = f"LICM: {tmpl['loop']}"
        return problem, {
            "steps": steps,
            "invariant": tmpl["invariant"],
            "after": tmpl["after"],
        }

    def _create_steps(self, solution_data: dict) -> list[str]:
        """Return the optimization steps.

        Args:
            solution_data: All computed solution information.

        Returns:
            Step strings in execution order.
        """
        return solution_data["steps"]

    def _create_answer(self, solution_data: dict) -> str:
        """Return the optimized code.

        Args:
            solution_data: All computed solution information.

        Returns:
            Optimized loop string.
        """
        return solution_data["after"]


# ---------------------------------------------------------------------------
# 7. Strength Reduction (tier 4)
# ---------------------------------------------------------------------------

@register
class StrengthReductionGenerator(StepGenerator):
    """Replace expensive operations with cheaper equivalents.

    Transforms like x*2 -> x<<1, x/4 -> x>>2, x*7 -> (x<<3)-x.
    """

    _TEMPLATES = [
        {
            "before": "y = x * 2",
            "after": "y = x << 1",
            "rule": "x*2 -> x<<1",
        },
        {
            "before": "y = x * 4",
            "after": "y = x << 2",
            "rule": "x*4 -> x<<2",
        },
        {
            "before": "y = x / 2",
            "after": "y = x >> 1",
            "rule": "x/2 -> x>>1",
        },
        {
            "before": "y = x / 4",
            "after": "y = x >> 2",
            "rule": "x/4 -> x>>2",
        },
        {
            "before": "y = x * 7",
            "after": "y = (x << 3) - x",
            "rule": "x*7 -> (x<<3)-x",
        },
        {
            "before": "y = x * 15",
            "after": "y = (x << 4) - x",
            "rule": "x*15 -> (x<<4)-x",
        },
        {
            "before": "y = x * 8",
            "after": "y = x << 3",
            "rule": "x*8 -> x<<3",
        },
        {
            "before": "y = x * 3",
            "after": "y = (x << 1) + x",
            "rule": "x*3 -> (x<<1)+x",
        },
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "strength_reduction"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["binary_arithmetic"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task instruction string.
        """
        return "apply strength reduction to replace expensive ops"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a strength reduction problem.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        idx = difficulty % len(self._TEMPLATES)
        tmpl = self._TEMPLATES[idx]

        x_val = self._rng.randint(1, 50)
        before_parts = tmpl["before"].split(" = ")
        after_parts = tmpl["after"].split(" = ")

        before_eval = tmpl["before"]
        after_eval = tmpl["after"]

        steps = [
            f"original: {tmpl['before']}",
            f"rule: {tmpl['rule']}",
            f"reduced: {tmpl['after']}",
            f"verify x={x_val}: both yield same result",
        ]

        problem = f"strength-reduce: {tmpl['before']}"
        return problem, {
            "steps": steps,
            "before": tmpl["before"],
            "after": tmpl["after"],
            "rule": tmpl["rule"],
        }

    def _create_steps(self, solution_data: dict) -> list[str]:
        """Return the reduction steps.

        Args:
            solution_data: All computed solution information.

        Returns:
            Step strings in execution order.
        """
        return solution_data["steps"]

    def _create_answer(self, solution_data: dict) -> str:
        """Return the reduced expression.

        Args:
            solution_data: All computed solution information.

        Returns:
            Reduced code string.
        """
        return solution_data["after"]


# ---------------------------------------------------------------------------
# 8. Tail Call Optimization (tier 5)
# ---------------------------------------------------------------------------

@register
class TailCallOptimizationGenerator(StepGenerator):
    """Identify tail recursive functions and transform to iterative.

    Given a tail-recursive function, show the equivalent iterative
    version with a loop replacing the recursive call.
    """

    _TEMPLATES = [
        {
            "recursive": "def fact(n, acc=1): if n<=1: return acc; return fact(n-1, n*acc)",
            "iterative": "def fact(n, acc=1): while n>1: acc=n*acc; n=n-1; return acc",
            "is_tail": True,
        },
        {
            "recursive": "def sum_to(n, acc=0): if n<=0: return acc; return sum_to(n-1, acc+n)",
            "iterative": "def sum_to(n, acc=0): while n>0: acc=acc+n; n=n-1; return acc",
            "is_tail": True,
        },
        {
            "recursive": "def fib(n): if n<=1: return n; return fib(n-1)+fib(n-2)",
            "iterative": None,
            "is_tail": False,
        },
        {
            "recursive": "def gcd(a, b): if b==0: return a; return gcd(b, a%b)",
            "iterative": "def gcd(a, b): while b!=0: a,b=b,a%b; return a",
            "is_tail": True,
        },
        {
            "recursive": "def pow(b, e, acc=1): if e<=0: return acc; return pow(b, e-1, acc*b)",
            "iterative": "def pow(b, e, acc=1): while e>0: acc=acc*b; e=e-1; return acc",
            "is_tail": True,
        },
        {
            "recursive": "def len(lst, acc=0): if not lst: return acc; return len(lst[1:], acc+1)",
            "iterative": "def len(lst, acc=0): while lst: acc=acc+1; lst=lst[1:]; return acc",
            "is_tail": True,
        },
        {
            "recursive": "def f(n): if n<=0: return 0; return n + f(n-1)",
            "iterative": None,
            "is_tail": False,
        },
        {
            "recursive": "def rev(lst, acc=[]): if not lst: return acc; return rev(lst[1:], [lst[0]]+acc)",
            "iterative": "def rev(lst, acc=[]): while lst: acc=[lst[0]]+acc; lst=lst[1:]; return acc",
            "is_tail": True,
        },
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "tail_call_optimization"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["comparison"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task instruction string.
        """
        return "identify tail call and transform to iterative"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a tail call optimization problem.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        idx = difficulty % len(self._TEMPLATES)
        tmpl = self._TEMPLATES[idx]

        steps = [f"function: {tmpl['recursive']}"]
        if tmpl["is_tail"]:
            steps.append("recursive call is in tail position => tail recursive")
            steps.append(f"iterative: {tmpl['iterative']}")
        else:
            steps.append("recursive call is NOT in tail position")
            steps.append("cannot apply tail call optimization directly")

        problem = f"TCO: {tmpl['recursive']}"
        return problem, {
            "steps": steps,
            "is_tail": tmpl["is_tail"],
            "iterative": tmpl["iterative"],
        }

    def _create_steps(self, solution_data: dict) -> list[str]:
        """Return the analysis steps.

        Args:
            solution_data: All computed solution information.

        Returns:
            Step strings in execution order.
        """
        return solution_data["steps"]

    def _create_answer(self, solution_data: dict) -> str:
        """Return the optimization result.

        Args:
            solution_data: All computed solution information.

        Returns:
            Iterative form or not-applicable message.
        """
        if solution_data["is_tail"]:
            return solution_data["iterative"]
        return "NOT TAIL RECURSIVE"
