"""Tier 0 generators — foundational arithmetic and pattern recognition.

These are the entry-point tasks that unlock all subsequent tiers.
Every model begins here regardless of architecture or capacity.
"""
from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


class DigitDecomposer:
    """Decomposes integers into right-to-left digit arrays for column arithmetic.

    Provides zero-padded digit access at each position, enabling
    step-by-step carry/borrow propagation in addition and subtraction.

    Attributes:
        length: Number of digit positions (padded to the longer operand).

    Example:
        >>> d = DigitDecomposer(123, 45)
        >>> d.length
        3
        >>> d.a_digit(0), d.b_digit(0)
        (3, 5)
        >>> d.a_digit(2), d.b_digit(2)
        (1, 0)
    """

    def __init__(self, a: int, b: int) -> None:
        """Initialise with two non-negative integers.

        Args:
            a: First operand.
            b: Second operand.
        """
        self._a_digits = [int(d) for d in str(a)][::-1]
        self._b_digits = [int(d) for d in str(b)][::-1]
        self._length = max(len(self._a_digits), len(self._b_digits))
        self._pad()

    def _pad(self) -> None:
        """Zero-pad both digit arrays to equal length."""
        self._a_digits += [0] * (self._length - len(self._a_digits))
        self._b_digits += [0] * (self._length - len(self._b_digits))

    @property
    def length(self) -> int:
        """Return the padded digit count."""
        return self._length

    def a_digit(self, position: int) -> int:
        """Return digit of first operand at given position.

        Args:
            position: Zero-indexed from the right (ones=0, tens=1, ...).

        Returns:
            Digit value (0-9).
        """
        return self._a_digits[position]

    def b_digit(self, position: int) -> int:
        """Return digit of second operand at given position.

        Args:
            position: Zero-indexed from the right (ones=0, tens=1, ...).

        Returns:
            Digit value (0-9).
        """
        return self._b_digits[position]


@register
class AdditionGenerator(StepGenerator):
    """Multi-digit addition with carry propagation.

    Generates addition problems where the model must show the
    carry chain from right to left, one digit position per step.
    This is the most fundamental multi-step arithmetic operation
    and serves as a prerequisite for multiplication, polynomial
    evaluation, and most of the curriculum.

    Input format:
        ``add two 5 digit numbers``

    Target format:
        ``13278 + 46048 <step> 8+8=16 <step> 7+4+1=12 <step>
        2+0+1=3 <step> 3+6=9 <step> 1+4=5 <step> 59326``

    Difficulty scaling:
        Difficulty N produces N-digit operands. Difficulty 1 is single-digit
        (0-9), difficulty 8 produces 8-digit numbers (10000000-99999999).
        The number of steps equals the digit count plus one if there is
        a final carry.

    Prerequisites:
        None (Tier 0 foundation task).

    Example:
        >>> gen = AdditionGenerator(min_difficulty=2, max_difficulty=2, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.input_text
        'add two 2 digit numbers'
        >>> sample.answer
        '58'
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "addition"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 0

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Number of digits per operand.

        Returns:
            Natural language description.
        """
        return f"add two {difficulty} digit numbers"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate two operands and compute their sum.

        Args:
            difficulty: Number of digits per operand.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        lower, upper = self._operand_range(difficulty)
        a = self._rng.randint(lower, upper)
        b = self._rng.randint(lower, upper)
        return f"{a} + {b}", {"a": a, "b": b, "result": a + b}

    def _create_steps(self, data: dict) -> list[str]:
        """Generate carry chain steps from right to left.

        Args:
            data: Solution data containing operands and result.

        Returns:
            Step strings showing each digit addition with carries.
        """
        digits = DigitDecomposer(data["a"], data["b"])
        steps: list[str] = []
        carry = 0

        for i in range(digits.length):
            step, carry = self._digit_step(
                digits.a_digit(i), digits.b_digit(i), carry,
            )
            steps.append(step)

        if carry > 0:
            steps.append(f"carry={carry}")
        return steps

    def _digit_step(self, a: int, b: int, carry: int) -> tuple[str, int]:
        """Compute one digit addition with optional carry.

        Args:
            a: Digit from first operand.
            b: Digit from second operand.
            carry: Incoming carry from previous position.

        Returns:
            Tuple of (step_string, outgoing_carry).
        """
        total = a + b + carry
        if carry > 0:
            return f"{a}+{b}+{carry}={total}", total // 10
        return f"{a}+{b}={total}", total // 10

    def _create_answer(self, data: dict) -> str:
        """Return the sum as a string.

        Args:
            data: Solution data.

        Returns:
            String representation of the result.
        """
        return str(data["result"])


@register
class SubtractionGenerator(StepGenerator):
    """Multi-digit subtraction with borrow propagation.

    Generates subtraction problems where the model must show the
    borrow chain from right to left. The larger operand is always
    placed first to ensure non-negative results.

    Input format:
        ``subtract two 5 digit numbers``

    Target format:
        ``46048 - 13278 <step> 8-8=0 <step> 4-7: borrow, 14-7=7 <step>
        ... <step> 32770``

    Difficulty scaling:
        Difficulty N produces N-digit operands. Borrow frequency increases
        naturally with digit count, making higher difficulties require
        more careful tracking.

    Prerequisites:
        None (Tier 0 foundation task).

    Example:
        >>> gen = SubtractionGenerator(min_difficulty=2, max_difficulty=2, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.answer
        '32'
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "subtraction"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 0

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Number of digits per operand.

        Returns:
            Natural language description.
        """
        return f"subtract two {difficulty} digit numbers"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate two operands with the larger first.

        Args:
            difficulty: Number of digits per operand.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        lower, upper = self._operand_range(difficulty)
        a = self._rng.randint(lower, upper)
        b = self._rng.randint(lower, upper)
        if b > a:
            a, b = b, a
        return f"{a} - {b}", {"a": a, "b": b, "result": a - b}

    def _create_steps(self, data: dict) -> list[str]:
        """Generate borrow chain steps from right to left.

        Args:
            data: Solution data containing operands.

        Returns:
            Step strings showing each digit subtraction with borrows.
        """
        digits = DigitDecomposer(data["a"], data["b"])
        steps: list[str] = []
        borrow = 0

        for i in range(digits.length):
            step, borrow = self._digit_step(
                digits.a_digit(i), digits.b_digit(i), borrow,
            )
            steps.append(step)

        return steps

    def _digit_step(self, a: int, b: int, borrow: int) -> tuple[str, int]:
        """Compute one digit subtraction with optional borrow.

        Args:
            a: Digit from first operand.
            b: Digit from second operand.
            borrow: Incoming borrow from previous position.

        Returns:
            Tuple of (step_string, outgoing_borrow).
        """
        top = a - borrow
        new_borrow = 0
        if top < b:
            top += 10
            new_borrow = 1

        diff = top - b
        if borrow > 0:
            return f"{a}-{borrow}-{b}={diff}", new_borrow
        return f"{a}-{b}={diff}", new_borrow

    def _create_answer(self, data: dict) -> str:
        """Return the difference as a string.

        Args:
            data: Solution data.

        Returns:
            String representation of the result.
        """
        return str(data["result"])


@register
class SortingGenerator(StepGenerator):
    """Selection sort with step-by-step swap operations.

    Generates a list of random integers and shows each selection
    and swap operation to produce an ascending sorted list. This
    task tests iterative state tracking and comparison logic.

    Input format:
        ``sort 5 numbers in ascending order``

    Target format:
        ``4,95,36,32,29 <step> 4 in place <step> swap 95 and 29 <step>
        swap 36 and 32 <step> 36 in place <step> 95 in place <step>
        4,29,32,36,95``

    Difficulty scaling:
        List length is difficulty + 2. Difficulty 1 gives 3 elements,
        difficulty 8 gives 10. Selection sort produces O(n) steps,
        making higher difficulties proportionally longer.

    Prerequisites:
        None (Tier 0 foundation task).

    Example:
        >>> gen = SortingGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.input_text
        'sort 3 numbers in ascending order'
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "sorting"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 0

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls list length (difficulty + 2).

        Returns:
            Natural language description.
        """
        return f"sort {difficulty + 2} numbers in ascending order"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a list of random numbers to sort.

        Args:
            difficulty: Controls list length.

        Returns:
            Tuple of (comma-separated numbers, solution_data).
        """
        n = difficulty + 2
        nums = [self._rng.randint(1, 100) for _ in range(n)]
        return ",".join(str(x) for x in nums), {"nums": nums}

    def _create_steps(self, data: dict) -> list[str]:
        """Generate selection sort operations.

        Args:
            data: Solution data with the number list.

        Returns:
            Step strings describing each swap or in-place decision.
        """
        nums = data["nums"][:]
        steps: list[str] = []

        for i in range(len(nums)):
            min_idx = self._find_min_index(nums, i)
            steps.append(self._apply_swap(nums, i, min_idx))

        return steps

    def _find_min_index(self, nums: list[int], start: int) -> int:
        """Find the index of the minimum element from a start position.

        Args:
            nums: Current list state.
            start: Index to begin searching from.

        Returns:
            Index of the minimum element in nums[start:].
        """
        min_idx = start
        for j in range(start + 1, len(nums)):
            if nums[j] < nums[min_idx]:
                min_idx = j
        return min_idx

    def _apply_swap(self, nums: list[int], i: int, min_idx: int) -> str:
        """Perform a swap if needed and return the step description.

        Modifies the nums list in place.

        Args:
            nums: Current list state.
            i: Current sort position.
            min_idx: Index of the minimum element.

        Returns:
            Step string describing the swap or in-place decision.
        """
        if min_idx != i:
            step = f"swap {nums[i]} and {nums[min_idx]}"
            nums[i], nums[min_idx] = nums[min_idx], nums[i]
            return step
        return f"{nums[i]} in place"

    def _create_answer(self, data: dict) -> str:
        """Return the sorted list as a comma-separated string.

        Args:
            data: Solution data.

        Returns:
            Sorted numbers joined by commas.
        """
        return ",".join(str(x) for x in sorted(data["nums"]))


@register
class DigitRootGenerator(StepGenerator):
    """Repeated digit summation until a single digit remains.

    Generates a multi-digit number and repeatedly sums its digits
    until a single digit is reached. Each summation round is one step.
    This task tests iterative convergence with a simple termination
    condition (result < 10).

    Input format:
        ``find the digit root``

    Target format:
        ``\\text{digroot}(9876) <step> 9+8+7+6=30 <step> 3+0=3 <step> 3``

    Difficulty scaling:
        Input number has difficulty + 1 digits. More digits means a
        larger initial sum, but convergence is always fast (2-3 rounds
        regardless of input size).

    Prerequisites:
        None (Tier 0 foundation task).

    Example:
        >>> gen = DigitRootGenerator(min_difficulty=3, max_difficulty=3, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> len(sample.steps)  # Always 2-3 rounds
        2
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "digit_root"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 0

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls the number of digits in the input.

        Returns:
            Natural language description.
        """
        return "find the digit root"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a multi-digit number for digit root computation.

        Args:
            difficulty: Number of digits is difficulty + 1.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        num_digits = difficulty + 1
        lower = 10 ** (num_digits - 1)
        upper = 10 ** num_digits - 1
        n = self._rng.randint(lower, upper)
        return f"\\text{{digroot}}({n})", {"n": n}

    def _create_steps(self, data: dict) -> list[str]:
        """Generate digit summation steps until convergence.

        Args:
            data: Solution data with the input number.

        Returns:
            Step strings showing each summation round.
        """
        current = data["n"]
        steps: list[str] = []

        while current >= 10:
            digits = [int(d) for d in str(current)]
            total = sum(digits)
            steps.append(f"{'+'.join(str(d) for d in digits)}={total}")
            current = total

        return steps

    def _create_answer(self, data: dict) -> str:
        """Compute the digit root by repeated summation.

        Args:
            data: Solution data with the input number.

        Returns:
            Single-digit result as a string.
        """
        n = data["n"]
        while n >= 10:
            n = sum(int(d) for d in str(n))
        return str(n)
