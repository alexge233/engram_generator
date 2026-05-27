"""Tier 1 generators — basic operations and equations.

Unlocks when Tier 0 foundation tasks are mastered. Introduces
multiplication, division, Fibonacci sequences, Caesar cipher,
run-length encoding, and expression simplification.
"""
from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register
from engram_generator.generators.arithmetic_core import DigitDecomposer


@register
class MultiplicationGenerator(StepGenerator):
    """Multi-digit multiplication with partial product steps.

    Generates multiplication problems decomposed into single-digit
    multiplications. Each digit of the second operand multiplies the
    entire first operand, producing partial products that are summed.

    Input format:
        ``multiply two 3 digit numbers``

    Target format:
        ``345 * 67 <step> 345*7=2415 <step> 345*6=2070 <step>
        2415+20700=23115 <step> 23115``

    Difficulty scaling:
        Difficulty N produces N-digit operands. Difficulty 1 is
        single-digit, difficulty 8 produces 8-digit numbers.
        Step count grows quadratically with digit count.

    Prerequisites:
        addition (carry propagation needed for summing partial products).

    Example:
        >>> gen = MultiplicationGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'multiplication'
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "multiplication"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 1

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["addition"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Number of digits per operand.

        Returns:
            Natural language description.
        """
        return f"multiply two {difficulty} digit numbers"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate two operands and compute their product.

        Args:
            difficulty: Number of digits per operand.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        lower, upper = self._operand_range(difficulty)
        a = self._rng.randint(lower, upper)
        b = self._rng.randint(lower, upper)
        return f"{a} \\times {b}", {"a": a, "b": b, "result": a * b}

    def _create_steps(self, data: dict) -> list[str]:
        """Generate partial product steps.

        Args:
            data: Solution data with operands.

        Returns:
            Steps showing each partial product and final sum.
        """
        a, b = data["a"], data["b"]
        b_digits = [int(d) for d in str(b)][::-1]
        partials = self._compute_partials(a, b_digits)
        return self._format_partial_steps(a, b_digits, partials)

    def _compute_partials(self, a: int, b_digits: list[int]) -> list[int]:
        """Compute partial products for each digit of b.

        Args:
            a: First operand.
            b_digits: Digits of second operand, right-to-left.

        Returns:
            Partial products shifted by position.
        """
        partials: list[int] = []
        for i, d in enumerate(b_digits):
            partials.append(a * d * (10 ** i))
        return partials

    def _format_partial_steps(self, a: int, b_digits: list[int],
                              partials: list[int]) -> list[str]:
        """Format partial products and summation as step strings.

        Args:
            a: First operand.
            b_digits: Digits of second operand, right-to-left.
            partials: Computed partial products.

        Returns:
            Formatted step strings.
        """
        steps: list[str] = []
        for i, d in enumerate(b_digits):
            steps.append(f"{a}*{d}={a * d}")

        if len(partials) > 1:
            running = partials[0]
            for i in range(1, len(partials)):
                total = running + partials[i]
                steps.append(f"{running}+{partials[i]}={total}")
                running = total

        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the product as a string.

        Args:
            data: Solution data.

        Returns:
            String representation of the product.
        """
        return str(data["result"])


@register
class DivisionGenerator(StepGenerator):
    """Long division with quotient digit steps.

    Generates division problems where the divisor evenly divides the
    dividend (no remainder), showing the long division process
    digit by digit from left to right.

    Input format:
        ``divide a 5 digit number``

    Target format:
        ``46050 \\div 15 <step> 46/15=3r1 <step> 10/15=0r10 <step>
        105/15=7r0 <step> 0/15=0r0 <step> 3070``

    Difficulty scaling:
        Difficulty N produces a dividend with N digits and a divisor
        with ceil(N/2) digits. The dividend is constructed as
        divisor * quotient to ensure clean division.

    Prerequisites:
        subtraction (needed for remainder computation).

    Example:
        >>> gen = DivisionGenerator(min_difficulty=2, max_difficulty=2, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'division'
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "division"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 1

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["subtraction"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls dividend digit count.

        Returns:
            Natural language description.
        """
        return f"divide a {difficulty} digit number"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a clean division problem (no remainder).

        Args:
            difficulty: Dividend digit count.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        divisor = self._random_divisor(difficulty)
        quotient = self._random_quotient(difficulty)
        dividend = divisor * quotient

        return (
            f"{dividend} \\div {divisor}",
            {"dividend": dividend, "divisor": divisor, "quotient": quotient},
        )

    def _random_divisor(self, difficulty: int) -> int:
        """Generate a divisor appropriate for the difficulty.

        Args:
            difficulty: Controls divisor size (ceil(difficulty/2) digits).

        Returns:
            A positive integer divisor.
        """
        div_digits = max(1, (difficulty + 1) // 2)
        lower, upper = self._operand_range(div_digits)
        return max(2, self._rng.randint(lower, upper))

    def _random_quotient(self, difficulty: int) -> int:
        """Generate a quotient that produces the desired dividend size.

        Args:
            difficulty: Target dividend digit count.

        Returns:
            A positive integer quotient.
        """
        quot_digits = max(1, difficulty // 2)
        lower, upper = self._operand_range(quot_digits)
        return max(1, self._rng.randint(lower, upper))

    def _create_steps(self, data: dict) -> list[str]:
        """Generate long division steps left-to-right.

        Args:
            data: Solution data with dividend, divisor, quotient.

        Returns:
            Steps showing each digit of the quotient.
        """
        dividend = data["dividend"]
        divisor = data["divisor"]
        return self._long_division_steps(dividend, divisor)

    def _long_division_steps(self, dividend: int, divisor: int) -> list[str]:
        """Perform long division and record each step.

        Args:
            dividend: The number being divided.
            divisor: The number dividing.

        Returns:
            Step strings for each quotient digit.
        """
        digits = [int(d) for d in str(dividend)]
        steps: list[str] = []
        remainder = 0

        for d in digits:
            current = remainder * 10 + d
            q = current // divisor
            remainder = current % divisor
            steps.append(f"{current}/{divisor}={q}r{remainder}")

        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the quotient as a string.

        Args:
            data: Solution data.

        Returns:
            String representation of the quotient.
        """
        return str(data["quotient"])


@register
class FibonacciGenerator(StepGenerator):
    """Fibonacci sequence computation with recurrence steps.

    Generates a request for the nth Fibonacci number and shows
    each addition step of the recurrence f(n) = f(n-1) + f(n-2).
    Directly exercises the engram's two-slot memory pattern.

    Input format:
        ``compute fibonacci number 10``

    Target format:
        ``\\text{fib}(10) <step> f(2)=1 <step> f(3)=1+1=2 <step>
        f(4)=2+1=3 <step> ... <step> 55``

    Difficulty scaling:
        Difficulty 1: n in [5,8] (4-7 steps).
        Difficulty 8: n in [35,45] (34-44 steps).
        Steps equal n-1, scaling linearly.

    Prerequisites:
        addition (each step is one addition).

    Example:
        >>> gen = FibonacciGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'fibonacci'
    """

    _N_RANGES = {
        1: (5, 8), 2: (8, 12), 3: (12, 16), 4: (16, 20),
        5: (20, 25), 6: (25, 30), 7: (30, 35), 8: (35, 45),
    }

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "fibonacci"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 1

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["addition"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls the value of n.

        Returns:
            Natural language description.
        """
        return "compute fibonacci number"

    def _n_for_difficulty(self, difficulty: int) -> int:
        """Map difficulty to a Fibonacci index n.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Fibonacci index to compute.
        """
        lo, hi = self._N_RANGES.get(difficulty, (5, 8))
        return self._rng.randint(lo, hi)

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Fibonacci problem.

        Args:
            difficulty: Controls the index n.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        n = self._n_for_difficulty(difficulty)
        sequence = self._compute_sequence(n)
        return f"\\text{{fib}}({n})", {"n": n, "sequence": sequence}

    def _compute_sequence(self, n: int) -> list[int]:
        """Compute the Fibonacci sequence up to index n.

        Args:
            n: Target index (0-indexed: fib(0)=0, fib(1)=1).

        Returns:
            Full sequence from fib(0) to fib(n).
        """
        if n <= 0:
            return [0]
        if n == 1:
            return [0, 1]

        seq = [0, 1]
        for _ in range(2, n + 1):
            seq.append(seq[-1] + seq[-2])
        return seq

    def _create_steps(self, data: dict) -> list[str]:
        """Generate recurrence steps showing each addition.

        Args:
            data: Solution data with the full sequence.

        Returns:
            Steps showing f(i) = f(i-1) + f(i-2) = result.
        """
        seq = data["sequence"]
        steps: list[str] = []

        for i in range(2, len(seq)):
            steps.append(f"f({i})={seq[i-1]}+{seq[i-2]}={seq[i]}")

        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the nth Fibonacci number.

        Args:
            data: Solution data.

        Returns:
            String representation of fib(n).
        """
        return str(data["sequence"][-1])


@register
class CaesarGenerator(StepGenerator):
    """Caesar cipher decryption with per-character shift steps.

    Generates an encrypted word and shift value, then shows the
    decryption of each character by shifting backwards in the
    alphabet. Tests per-element modular arithmetic.

    Input format:
        ``decrypt caesar cipher with shift 3``

    Target format:
        ``khoor,3 <step> k-3=h <step> h-3=e <step> o-3=l <step>
        o-3=l <step> r-3=o <step> hello``

    Difficulty scaling:
        Difficulty 1: 3-5 character words.
        Difficulty 8: 15-20 character words.
        Shift is random 1-25.

    Prerequisites:
        None (basic modular arithmetic on letters).

    Example:
        >>> gen = CaesarGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'caesar'
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "caesar"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 1

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["addition"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls plaintext length.

        Returns:
            Natural language description.
        """
        return "decrypt caesar cipher"

    def _word_length(self, difficulty: int) -> int:
        """Map difficulty to plaintext length.

        Args:
            difficulty: Difficulty level.

        Returns:
            Number of characters in the plaintext.
        """
        return min(3 + difficulty * 2, 20)

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Caesar cipher problem.

        Args:
            difficulty: Controls word length.

        Returns:
            Tuple of (ciphertext_with_shift, solution_data).
        """
        length = self._word_length(difficulty)
        plaintext = self._random_word(length)
        shift = self._rng.randint(1, 25)
        ciphertext = self._encrypt(plaintext, shift)

        return (
            f"{ciphertext},{shift}",
            {"plaintext": plaintext, "ciphertext": ciphertext, "shift": shift},
        )

    def _random_word(self, length: int) -> str:
        """Generate a random lowercase word.

        Args:
            length: Number of characters.

        Returns:
            Random string of lowercase letters.
        """
        return "".join(chr(self._rng.randint(97, 122)) for _ in range(length))

    def _encrypt(self, plaintext: str, shift: int) -> str:
        """Encrypt plaintext with Caesar cipher.

        Args:
            plaintext: Lowercase string to encrypt.
            shift: Number of positions to shift forward.

        Returns:
            Encrypted string.
        """
        return "".join(
            chr((ord(c) - 97 + shift) % 26 + 97) for c in plaintext
        )

    def _create_steps(self, data: dict) -> list[str]:
        """Generate per-character decryption steps.

        Args:
            data: Solution data with ciphertext and shift.

        Returns:
            Steps showing each character shift.
        """
        ciphertext = data["ciphertext"]
        shift = data["shift"]
        plaintext = data["plaintext"]

        return [
            f"{c}-{shift}={p}" for c, p in zip(ciphertext, plaintext)
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the decrypted plaintext.

        Args:
            data: Solution data.

        Returns:
            Original plaintext string.
        """
        return data["plaintext"]


@register
class RunLengthGenerator(StepGenerator):
    """Run-length encoding with stateful counting steps.

    Generates a string with repeated character runs and shows the
    encoding process: scan left-to-right, count consecutive identical
    characters, emit count+character pairs.

    Input format:
        ``run length encode string``

    Target format:
        ``aaabbccccc <step> a:3 <step> b:2 <step> c:5 <step> 3a2b5c``

    Difficulty scaling:
        Difficulty 1: ~5 character strings.
        Difficulty 8: ~25 character strings.
        Adjacent runs always use different characters.

    Prerequisites:
        None (basic string processing).

    Example:
        >>> gen = RunLengthGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'run_length'
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "run_length"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 1

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["counting"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls string length.

        Returns:
            Natural language description.
        """
        return "run length encode string"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a string with character runs.

        Args:
            difficulty: Controls total string length.

        Returns:
            Tuple of (input_string, solution_data).
        """
        runs = self._generate_runs(difficulty)
        text = "".join(c * n for c, n in runs)
        return text, {"runs": runs, "text": text}

    def _generate_runs(self, difficulty: int) -> list[tuple[str, int]]:
        """Generate a list of (character, count) run pairs.

        Ensures adjacent runs use different characters.

        Args:
            difficulty: Controls total length.

        Returns:
            List of (character, run_length) tuples.
        """
        target_len = 3 + difficulty * 3
        runs: list[tuple[str, int]] = []
        current_len = 0
        last_char = ""

        while current_len < target_len:
            char = self._random_char_except(last_char)
            run_len = min(self._rng.randint(1, 5), target_len - current_len)
            runs.append((char, run_len))
            current_len += run_len
            last_char = char

        return runs

    def _random_char_except(self, exclude: str) -> str:
        """Generate a random lowercase character different from exclude.

        Args:
            exclude: Character to avoid (empty string to allow any).

        Returns:
            A lowercase letter different from exclude.
        """
        while True:
            c = chr(self._rng.randint(97, 122))
            if c != exclude:
                return c

    def _create_steps(self, data: dict) -> list[str]:
        """Generate encoding steps for each run.

        Args:
            data: Solution data with run pairs.

        Returns:
            Steps showing each character:count identification.
        """
        return [f"{char}:{count}" for char, count in data["runs"]]

    def _create_answer(self, data: dict) -> str:
        """Return the run-length encoded string.

        Args:
            data: Solution data.

        Returns:
            Encoded string like '3a2b5c'.
        """
        return "".join(f"{count}{char}" for char, count in data["runs"])


@register
class LinearEquationGenerator(StepGenerator):
    """Solve linear equations of the form ax + b = c.

    Generates equations with guaranteed integer solutions by
    constructing the equation backwards from a chosen solution.
    Shows the algebraic isolation steps.

    Input format:
        ``solve linear equation``

    Target format:
        ``3x + 5 = 20 <step> 3x = 20 - 5 <step> 3x = 15 <step>
        x = \\frac{15}{3} <step> 5``

    Difficulty scaling:
        Difficulty 1: coefficients 1-5, small solutions.
        Difficulty 5: coefficients 10-50.
        Difficulty 8: coefficients 50-200.
        Negative solutions appear ~30% of the time.

    Prerequisites:
        addition, subtraction.

    Example:
        >>> gen = LinearEquationGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'linear_equation'
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "linear_equation"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 1

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["addition", "subtraction"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls coefficient magnitude.

        Returns:
            Natural language description.
        """
        return "solve linear equation"

    def _coeff_range(self, difficulty: int) -> tuple[int, int]:
        """Map difficulty to coefficient magnitude range.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (min_coeff, max_coeff).
        """
        base = max(1, difficulty * 5)
        return base, base * 10

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a linear equation with integer solution.

        Constructs backwards: choose x, a, b, then compute c = ax + b.

        Args:
            difficulty: Controls coefficient magnitude.

        Returns:
            Tuple of (latex_equation, solution_data).
        """
        lo, hi = self._coeff_range(difficulty)
        a = self._rng.randint(lo, hi)
        x = self._rng.randint(-hi, hi)
        b = self._rng.randint(-hi, hi)
        c = a * x + b

        equation = f"{a}x + {b} = {c}"
        return equation, {"a": a, "b": b, "c": c, "x": x}

    def _create_steps(self, data: dict) -> list[str]:
        """Generate algebraic isolation steps.

        Args:
            data: Solution data with coefficients and solution.

        Returns:
            Steps showing subtraction then division.
        """
        a, b, c, x = data["a"], data["b"], data["c"], data["x"]
        rhs = c - b

        return [
            f"{a}x = {c} - {b}",
            f"{a}x = {rhs}",
            f"x = \\frac{{{rhs}}}{{{a}}}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the solution x.

        Args:
            data: Solution data.

        Returns:
            String representation of x.
        """
        return str(data["x"])


@register
class ExpressionSimplifyGenerator(StepGenerator):
    """Collect like terms in algebraic expressions.

    Generates expressions with mixed x-terms and constants, then
    shows the collection process: group x-coefficients, group
    constants, produce simplified form.

    Input format:
        ``simplify algebraic expression``

    Target format:
        ``2x + 3 - x + 5 - 4x <step> x: 2-1-4=-3 <step>
        const: 3+5=8 <step> -3x + 8``

    Difficulty scaling:
        Difficulty 1: 3 terms.
        Difficulty 8: 12+ terms.
        Coefficients range from -10 to 10.

    Prerequisites:
        addition, subtraction.

    Example:
        >>> gen = ExpressionSimplifyGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'expression_simplify'
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "expression_simplify"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 1

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["addition", "subtraction"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls number of terms.

        Returns:
            Natural language description.
        """
        return "simplify algebraic expression"

    def _term_count(self, difficulty: int) -> int:
        """Map difficulty to number of terms.

        Args:
            difficulty: Difficulty level.

        Returns:
            Number of terms in the expression.
        """
        return difficulty + 2

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an expression with mixed terms.

        Args:
            difficulty: Controls term count.

        Returns:
            Tuple of (expression_string, solution_data).
        """
        n = self._term_count(difficulty)
        x_coeffs, constants = self._generate_terms(n)
        expression = self._format_expression(x_coeffs, constants)
        return expression, {"x_coeffs": x_coeffs, "constants": constants}

    def _generate_terms(self, n: int) -> tuple[list[int], list[int]]:
        """Generate random x-coefficients and constant terms.

        Roughly half are x-terms, half are constants.

        Args:
            n: Total number of terms.

        Returns:
            Tuple of (x_coefficient_list, constant_list).
        """
        x_coeffs: list[int] = []
        constants: list[int] = []

        for i in range(n):
            val = self._rng.randint(-10, 10)
            if val == 0:
                val = 1
            if i % 2 == 0:
                x_coeffs.append(val)
            else:
                constants.append(val)

        return x_coeffs, constants

    def _format_expression(self, x_coeffs: list[int],
                           constants: list[int]) -> str:
        """Format coefficients and constants into an expression string.

        Args:
            x_coeffs: List of x-term coefficients.
            constants: List of constant values.

        Returns:
            Expression string like '2x + 3 - x + 5'.
        """
        terms: list[str] = []
        for c in x_coeffs:
            terms.append(self._format_x_term(c))
        for c in constants:
            terms.append(str(c))

        self._rng.shuffle(terms)
        return " + ".join(terms).replace("+ -", "- ")

    def _format_x_term(self, coeff: int) -> str:
        """Format a coefficient with x.

        Args:
            coeff: The coefficient value.

        Returns:
            Formatted term like '3x', '-x', or 'x'.
        """
        if coeff == 1:
            return "x"
        if coeff == -1:
            return "-x"
        return f"{coeff}x"

    def _create_steps(self, data: dict) -> list[str]:
        """Generate collection steps for x-terms and constants.

        Args:
            data: Solution data with coefficient lists.

        Returns:
            Steps showing grouping and summation.
        """
        x_sum = sum(data["x_coeffs"])
        const_sum = sum(data["constants"])

        x_parts = "+".join(str(c) for c in data["x_coeffs"]).replace("+-", "-")
        const_parts = "+".join(str(c) for c in data["constants"]).replace("+-", "-")

        return [
            f"x: {x_parts}={x_sum}",
            f"const: {const_parts}={const_sum}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the simplified expression.

        Args:
            data: Solution data.

        Returns:
            Simplified expression string.
        """
        x_sum = sum(data["x_coeffs"])
        const_sum = sum(data["constants"])
        return self._format_simplified(x_sum, const_sum)

    def _format_simplified(self, x_coeff: int, constant: int) -> str:
        """Format the simplified expression from totals.

        Args:
            x_coeff: Total x coefficient.
            constant: Total constant.

        Returns:
            Clean simplified expression.
        """
        parts: list[str] = []

        if x_coeff != 0:
            parts.append(self._format_x_term(x_coeff))

        if constant != 0 or not parts:
            if parts and constant > 0:
                parts.append(f"+ {constant}")
            else:
                parts.append(str(constant))

        return " ".join(parts)
