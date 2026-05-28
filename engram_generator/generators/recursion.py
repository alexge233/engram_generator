"""Recursion generators.

4 generators across tiers 2-3.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register

@register
class RecursiveTraceGenerator(StepGenerator):
    """Trace the execution of a recursive function."""

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "recursive_trace"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 2

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["multiplication"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description."""
        return "trace recursive function"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a recursive function tracing problem.

        Args:
            difficulty: Controls input size and function variety.

        Returns:
            Tuple of (problem_string, solution_data).
        """
        fn = self._rng.choice(["factorial", "sum_to_n", "power", "double", "triangular"])
        n = self._rng.randint(2, min(10, 2 + difficulty * 2))
        if fn == "factorial":
            calls = [f"f({i})" for i in range(n, -1, -1)]
            result = 1
            for i in range(1, n + 1):
                result *= i
            desc = "f(n) = n * f(n-1), f(0) = 1"
        elif fn == "sum_to_n":
            calls = [f"f({i})" for i in range(n, -1, -1)]
            result = n * (n + 1) // 2
            desc = "f(n) = n + f(n-1), f(0) = 0"
        elif fn == "double":
            calls = [f"f({i})" for i in range(n, -1, -1)]
            result = 2 ** n
            desc = "f(n) = 2 * f(n-1), f(0) = 1"
        elif fn == "triangular":
            # f(n) = n^2 + f(n-1), f(0) = 0 -> sum of squares
            calls = [f"f({i})" for i in range(n, -1, -1)]
            result = sum(i * i for i in range(n + 1))
            desc = "f(n) = n^2 + f(n-1), f(0) = 0"
        else:
            base = self._rng.randint(2, 6)
            calls = [f"f({base},{i})" for i in range(n, -1, -1)]
            result = base ** n
            desc = "f(b,n) = b * f(b,n-1), f(b,0) = 1"
        return f"{desc}, compute f({n})", {"fn": fn, "n": n, "calls": calls, "result": result}

    def _create_steps(self, sd: dict) -> list[str]:
        return sd["calls"]

    def _create_answer(self, sd: dict) -> str:
        return str(sd["result"])


@register
class BaseCaseIdentifyGenerator(StepGenerator):
    """Identify the base case of a recursive definition."""

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "base_case_identify"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 2

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["recursive_trace"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description."""
        return "identify base case"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a base case identification problem.

        Args:
            difficulty: Controls the variety and complexity of recursive functions.

        Returns:
            Tuple of (problem_string, solution_data).
        """
        # Parametric templates: (recursive_template, base_template, name_template)
        templates = [
            ("f(n) = n * f(n-{step})", "f({bc}) = {bc_val}", "factorial_variant"),
            ("f(n) = f(n-1) + f(n-2)", "f(0) = {a}, f(1) = {b}", "fib_variant"),
            ("f(n) = {k} * f(n-1)", "f(0) = {a}", "geometric"),
            ("f(n) = n + f(n-1)", "f({bc}) = {bc_val}", "sum_variant"),
            ("f(n) = f(n-1) + {c}", "f(0) = {a}", "arithmetic_rec"),
            ("f(n) = n * n + f(n-1)", "f(0) = {a}", "sum_of_squares"),
            ("f(lst) = f(lst[1:]) + [lst[0]]", "f([]) = []", "reverse list"),
            ("f(n) = 1 + f(n//{d})", "f(1) = 0", "log_base"),
            ("f(a,b) = f(b, a%b)", "f(a, 0) = a", "GCD"),
            ("f(n) = f(n-1) * f(n-2)", "f(0) = {a}, f(1) = {b}", "mult_recurrence"),
        ]
        idx = self._rng.randint(0, min(len(templates) - 1, 3 + difficulty))
        rec_tmpl, base_tmpl, name_tmpl = templates[idx]

        # Randomise parameters for each template
        step = self._rng.randint(1, 3)
        bc = self._rng.choice([0, 1])
        bc_val = self._rng.randint(0, 5)
        k = self._rng.randint(2, 7)
        c = self._rng.randint(1, 10)
        a = self._rng.randint(0, 5)
        b = self._rng.randint(1, 5)
        d = self._rng.randint(2, 5)

        params = {"step": step, "bc": bc, "bc_val": bc_val, "k": k,
                  "c": c, "a": a, "b": b, "d": d}
        recursive = rec_tmpl.format(**params)
        base = base_tmpl.format(**params)
        name = name_tmpl

        return (
            f"recursive: {recursive}. What is the base case?",
            {"recursive": recursive, "base": base, "name": name},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        return [f"function: {sd['name']}", f"recursion: {sd['recursive']}"]

    def _create_answer(self, sd: dict) -> str:
        return sd["base"]


@register
class CallStackDepthGenerator(StepGenerator):
    """Compute the maximum call stack depth for a recursive call."""

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "call_stack_depth"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 3

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["recursive_trace"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description."""
        return "find call stack depth"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        fn = self._rng.choice(["factorial", "binary_search", "fibonacci"])
        n = self._rng.randint(4, min(20, 4 + 4 * difficulty))
        if fn == "factorial":
            depth = n
            desc = f"factorial({n})"
        elif fn == "binary_search":
            import math
            depth = math.ceil(math.log2(n + 1))
            desc = f"binary_search(array of {n})"
        else:
            depth = n
            desc = f"fibonacci({n}) naive"
        return desc, {"fn": fn, "n": n, "depth": depth}

    def _create_steps(self, sd: dict) -> list[str]:
        if sd["fn"] == "factorial":
            return [f"each call reduces n by 1, depth = n = {sd['n']}"]
        elif sd["fn"] == "binary_search":
            return [f"halves search space each call, depth = ceil(log2({sd['n']}+1))"]
        return [f"linear chain of calls, depth = n = {sd['n']}"]

    def _create_answer(self, sd: dict) -> str:
        return str(sd["depth"])


@register
class MemoisationGenerator(StepGenerator):
    """Compare call counts with and without memoisation."""

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "memoisation"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 3

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["recursive_trace", "fibonacci"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description."""
        return "count calls with memoisation"

    @staticmethod
    def _count_fibonacci(n: int) -> int:
        """Count naive recursive calls for fibonacci(n).

        Args:
            n: Input to fibonacci.

        Returns:
            Total number of recursive calls without memoisation.
        """
        counter = [0]
        def fib(k: int) -> int:
            counter[0] += 1
            if k <= 1:
                return k
            return fib(k - 1) + fib(k - 2)
        fib(n)
        return counter[0]

    @staticmethod
    def _count_tribonacci(n: int) -> int:
        """Count naive recursive calls for tribonacci(n).

        Args:
            n: Input to tribonacci.

        Returns:
            Total number of recursive calls without memoisation.
        """
        counter = [0]
        def trib(k: int) -> int:
            counter[0] += 1
            if k <= 0:
                return 0
            if k <= 2:
                return 1
            return trib(k - 1) + trib(k - 2) + trib(k - 3)
        trib(n)
        return counter[0]

    @staticmethod
    def _count_staircase(n: int) -> int:
        """Count naive recursive calls for staircase(n).

        Args:
            n: Input to staircase.

        Returns:
            Total number of recursive calls without memoisation.
        """
        counter = [0]
        def stair(k: int) -> int:
            counter[0] += 1
            if k <= 1:
                return 1
            return stair(k - 1) + stair(k - 2)
        stair(n)
        return counter[0]

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a memoisation comparison problem.

        Args:
            difficulty: Controls the input size n.

        Returns:
            Tuple of (problem_string, solution_data).
        """
        fn_type = self._rng.choice(["fibonacci", "tribonacci", "staircase"])
        n = self._rng.randint(5, min(18, 5 + 3 * difficulty))

        if fn_type == "fibonacci":
            naive_calls = self._count_fibonacci(n)
            desc = f"fibonacci({n})"
        elif fn_type == "tribonacci":
            n = min(n, 14)
            naive_calls = self._count_tribonacci(n)
            desc = f"tribonacci({n})"
        else:
            steps = self._rng.randint(1, 3)
            naive_calls = self._count_staircase(n)
            desc = f"staircase({n}, steps={steps})"

        return (
            f"{desc}: calls without vs with memo",
            {"n": n, "naive": naive_calls, "memo": n + 1, "fn_type": fn_type},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        return [
            f"without memo: ~O(2^n) calls = {sd['naive']}",
            f"with memo: O(n) calls = {sd['memo']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        return f"naive={sd['naive']}, memo={sd['memo']}"
