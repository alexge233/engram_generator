"""Extended recursion generators.

6 generators across tiers 2-4.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


@register
class TowerOfHanoiGenerator(StepGenerator):
    """Solve the Tower of Hanoi problem with n disks.

    Lists all moves to transfer n disks from peg A to peg C
    using peg B as auxiliary. Total moves = 2^n - 1.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "tower_of_hanoi"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 3

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["recursive_trace"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "solve Tower of Hanoi"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Tower of Hanoi problem.

        Args:
            difficulty: Controls number of disks (2-5).

        Returns:
            Tuple of (problem_text, solution_data).
        """
        n = min(2 + difficulty // 2, 5)
        moves: list[str] = []

        def hanoi(k: int, src: str, dst: str, aux: str) -> None:
            """Recursively solve Tower of Hanoi.

            Args:
                k: Number of disks.
                src: Source peg.
                dst: Destination peg.
                aux: Auxiliary peg.
            """
            if k == 0:
                return
            hanoi(k - 1, src, aux, dst)
            moves.append(f"disk {k}: {src}->{dst}")
            hanoi(k - 1, aux, dst, src)

        hanoi(n, "A", "C", "B")
        total = 2 ** n - 1
        return (
            f"Tower of Hanoi: {n} disks, A->C using B",
            {"n": n, "moves": moves, "total": total},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Show the sequence of moves.

        Args:
            sd: Solution data dict.

        Returns:
            Step strings listing each move.
        """
        return sd["moves"]

    def _create_answer(self, sd: dict) -> str:
        """Return the total number of moves.

        Args:
            sd: Solution data dict.

        Returns:
            Total move count.
        """
        return f"{sd['total']} moves"


@register
class RecursivePowerGenerator(StepGenerator):
    """Compute a^n by repeated squaring (fast exponentiation).

    Traces recursive calls showing how exponent is halved at each step.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "recursive_power"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 3

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["multiplication"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute power by repeated squaring"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a repeated squaring problem.

        Args:
            difficulty: Controls base and exponent range.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        base = self._rng.randint(2, min(5, 2 + difficulty))
        exp = self._rng.randint(2, min(12, 2 + difficulty * 2))
        calls: list[str] = []

        def power(a: int, n: int) -> int:
            """Compute a^n by repeated squaring.

            Args:
                a: Base.
                n: Exponent.

            Returns:
                a raised to the power n.
            """
            if n == 0:
                calls.append(f"pow({a},{n})=1")
                return 1
            if n == 1:
                calls.append(f"pow({a},{n})={a}")
                return a
            if n % 2 == 0:
                half = power(a, n // 2)
                result = half * half
                calls.append(f"pow({a},{n})=pow({a},{n // 2})^2={result}")
                return result
            sub = power(a, n - 1)
            result = a * sub
            calls.append(f"pow({a},{n})={a}*pow({a},{n - 1})={result}")
            return result

        result = power(base, exp)
        return (
            f"compute {base}^{exp} by repeated squaring",
            {"base": base, "exp": exp, "calls": calls, "result": result},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Show the recursive call trace.

        Args:
            sd: Solution data dict.

        Returns:
            Step strings showing each recursive call.
        """
        return sd["calls"]

    def _create_answer(self, sd: dict) -> str:
        """Return the computed power.

        Args:
            sd: Solution data dict.

        Returns:
            The result of a^n.
        """
        return str(sd["result"])


@register
class RecursiveGCDGenerator(StepGenerator):
    """Trace the Euclidean algorithm recursively.

    Computes gcd(a, b) = gcd(b, a mod b), tracing each call until
    the base case gcd(a, 0) = a is reached.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "recursive_gcd"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 3

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["recursive_trace"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "trace Euclidean GCD"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a recursive GCD problem.

        Args:
            difficulty: Controls operand range.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        upper = 10 * difficulty + 10
        a = self._rng.randint(10, upper)
        b = self._rng.randint(2, upper)
        if a < b:
            a, b = b, a
        calls: list[str] = []
        x, y = a, b
        while y != 0:
            calls.append(f"gcd({x},{y}): {x} mod {y} = {x % y}")
            x, y = y, x % y
        calls.append(f"gcd({x},0) = {x}")
        return (
            f"gcd({a},{b}) using Euclidean algorithm",
            {"a": a, "b": b, "calls": calls, "result": x},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Show each recursive call of the Euclidean algorithm.

        Args:
            sd: Solution data dict.

        Returns:
            Step strings.
        """
        return sd["calls"]

    def _create_answer(self, sd: dict) -> str:
        """Return the GCD.

        Args:
            sd: Solution data dict.

        Returns:
            The greatest common divisor.
        """
        return str(sd["result"])


@register
class RecursiveBinarySearchGenerator(StepGenerator):
    """Trace recursive binary search on a sorted array.

    Shows recursive calls with lo, hi, and mid indices at each step.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "recursive_binary_search"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["recursive_trace"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "trace recursive binary search"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a binary search tracing problem.

        Args:
            difficulty: Controls array size.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        size = min(5 + difficulty * 2, 16)
        arr = sorted(self._rng.sample(range(1, size * 3), size))
        target = self._rng.choice(arr)
        calls: list[str] = []
        lo, hi = 0, len(arr) - 1
        found_idx = -1
        while lo <= hi:
            mid = (lo + hi) // 2
            calls.append(f"search(lo={lo},hi={hi},mid={mid},arr[mid]={arr[mid]})")
            if arr[mid] == target:
                found_idx = mid
                break
            elif arr[mid] < target:
                lo = mid + 1
            else:
                hi = mid - 1
        return (
            f"binary search for {target} in {arr}",
            {"arr": arr, "target": target, "calls": calls,
             "found_idx": found_idx},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Show recursive binary search calls.

        Args:
            sd: Solution data dict.

        Returns:
            Step strings.
        """
        return sd["calls"]

    def _create_answer(self, sd: dict) -> str:
        """Return the index where the target was found.

        Args:
            sd: Solution data dict.

        Returns:
            Found index or NOT FOUND.
        """
        if sd["found_idx"] >= 0:
            return f"found at index {sd['found_idx']}"
        return "NOT FOUND"


@register
class RecursiveSumGenerator(StepGenerator):
    """Compute sum of an array recursively.

    sum(arr) = arr[0] + sum(arr[1:]). Traces calls for an array
    of 4-6 elements.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "recursive_sum"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 2

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["addition"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute recursive array sum"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a recursive sum problem.

        Args:
            difficulty: Controls array size and element range.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        size = self._rng.randint(4, min(6, 4 + difficulty))
        r = 5 * difficulty
        arr = [self._rng.randint(1, r) for _ in range(size)]
        calls: list[str] = []
        for i in range(size):
            remaining = arr[i:]
            calls.append(f"sum({remaining}) = {arr[i]} + sum({arr[i + 1:]})")
        calls.append("sum([]) = 0")
        total = sum(arr)
        return (
            f"sum({arr}) recursively: sum(a) = a[0] + sum(a[1:])",
            {"arr": arr, "calls": calls, "total": total},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Show recursive sum calls.

        Args:
            sd: Solution data dict.

        Returns:
            Step strings.
        """
        return sd["calls"]

    def _create_answer(self, sd: dict) -> str:
        """Return the total sum.

        Args:
            sd: Solution data dict.

        Returns:
            Sum of the array.
        """
        return str(sd["total"])


@register
class RecursivePermutationsGenerator(StepGenerator):
    """Generate permutations of n elements recursively.

    Counts total permutations (n!) and shows the first few
    generated by the recursive algorithm.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "recursive_permutations"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["memoisation"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "generate recursive permutations"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a recursive permutations problem.

        Args:
            difficulty: Controls the number of elements (3-5).

        Returns:
            Tuple of (problem_text, solution_data).
        """
        n = min(3 + difficulty // 3, 5)
        elements = list(range(1, n + 1))
        perms: list[list[int]] = []

        def permute(arr: list[int], start: int) -> None:
            """Generate permutations by swapping.

            Args:
                arr: Current array state.
                start: Index from which to permute.
            """
            if start == len(arr) - 1:
                perms.append(list(arr))
                return
            for i in range(start, len(arr)):
                arr[start], arr[i] = arr[i], arr[start]
                permute(arr, start + 1)
                arr[start], arr[i] = arr[i], arr[start]

        permute(elements, 0)
        total = math.factorial(n)
        shown = perms[:min(6, len(perms))]
        steps = [f"fix position 0 with {elements[i]}" for i in range(min(n, 4))]
        return (
            f"permutations of {elements}",
            {"elements": elements, "total": total,
             "shown": shown, "steps": steps},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Show how permutations are generated.

        Args:
            sd: Solution data dict.

        Returns:
            Step strings.
        """
        steps = list(sd["steps"])
        for p in sd["shown"]:
            steps.append(f"perm: {p}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the total permutation count.

        Args:
            sd: Solution data dict.

        Returns:
            n! total permutations.
        """
        return f"{sd['total']} permutations"
