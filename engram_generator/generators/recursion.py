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
        return "recursive_trace"

    @property
    def tier(self) -> int:
        return 2

    @property
    def prerequisites(self) -> list[str]:
        return ["multiplication"]

    def task_description(self, difficulty: int) -> str:
        return "trace recursive function"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        fn = self._rng.choice(["factorial", "sum_to_n", "power"])
        n = self._rng.randint(2, min(6, 2 + difficulty))
        if fn == "factorial":
            calls = [f"f({i})" for i in range(n, -1, -1)]
            result = 1
            for i in range(1, n + 1):
                result *= i
            desc = f"f(n) = n * f(n-1), f(0) = 1"
        elif fn == "sum_to_n":
            calls = [f"f({i})" for i in range(n, -1, -1)]
            result = n * (n + 1) // 2
            desc = f"f(n) = n + f(n-1), f(0) = 0"
        else:
            base = self._rng.randint(2, 4)
            calls = [f"f({base},{i})" for i in range(n, -1, -1)]
            result = base ** n
            desc = f"f(b,n) = b * f(b,n-1), f(b,0) = 1"
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
        return "base_case_identify"

    @property
    def tier(self) -> int:
        return 2

    @property
    def prerequisites(self) -> list[str]:
        return ["recursive_trace"]

    def task_description(self, difficulty: int) -> str:
        return "identify base case"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        defs = [
            ("f(n) = n * f(n-1)", "f(0) = 1", "factorial"),
            ("f(n) = f(n-1) + f(n-2)", "f(0) = 0, f(1) = 1", "fibonacci"),
            ("f(n) = 2 * f(n-1)", "f(0) = 1", "powers of 2"),
            ("f(lst) = f(lst[1:]) + [lst[0]]", "f([]) = []", "reverse list"),
            ("f(n) = 1 + f(n//2)", "f(1) = 0", "log base 2"),
            ("f(a,b) = f(b, a%b)", "f(a, 0) = a", "GCD"),
        ]
        recursive, base, name = self._rng.choice(defs[:min(len(defs), 2 + difficulty)])
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
        return "call_stack_depth"

    @property
    def tier(self) -> int:
        return 3

    @property
    def prerequisites(self) -> list[str]:
        return ["recursive_trace"]

    def task_description(self, difficulty: int) -> str:
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
        return "memoisation"

    @property
    def tier(self) -> int:
        return 3

    @property
    def prerequisites(self) -> list[str]:
        return ["recursive_trace", "fibonacci"]

    def task_description(self, difficulty: int) -> str:
        return "count calls with memoisation"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        n = self._rng.randint(5, min(15, 5 + 3 * difficulty))
        without_memo = [0]
        def fib_count(k):
            without_memo[0] += 1
            if k <= 1: return k
            return fib_count(k - 1) + fib_count(k - 2)
        fib_count(n)
        naive_calls = without_memo[0]
        memo_calls = n + 1
        return (
            f"fibonacci({n}): calls without vs with memo",
            {"n": n, "naive": naive_calls, "memo": memo_calls},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        return [
            f"without memo: ~O(2^n) calls = {sd['naive']}",
            f"with memo: O(n) calls = {sd['memo']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        return f"naive={sd['naive']}, memo={sd['memo']}"
