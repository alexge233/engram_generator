"""Computer science generators — boolean logic through neural network forward pass.

Introduces boolean algebra and binary arithmetic (tier 3), two's complement
(tier 4), softmax/attention/backpropagation (tier 5), and neural network
forward pass (tier 6). These tasks build a path from foundational digital
logic to modern deep learning primitives, using small integer weights and
inputs for clean, verifiable outputs.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


class BooleanExpression:
    """Represents a boolean expression for simplification.

    Stores an expression tree as a string with its simplified form,
    the law used for simplification, and the intermediate steps.
    Supports De Morgan's law, distribution, and absorption.

    Example:
        >>> expr = BooleanExpression("NOT(A AND B)", "NOT(A) OR NOT(B)", "De Morgan")
        >>> expr.original
        'NOT(A AND B)'
    """

    def __init__(self, original: str, simplified: str, law: str) -> None:
        """Initialise a boolean expression with its simplification.

        Args:
            original: The unsimplified expression.
            simplified: The simplified result.
            law: Name of the simplification law applied.
        """
        self._original = original
        self._simplified = simplified
        self._law = law

    @property
    def original(self) -> str:
        """Return the original expression."""
        return self._original

    @property
    def simplified(self) -> str:
        """Return the simplified expression."""
        return self._simplified

    @property
    def law(self) -> str:
        """Return the name of the law used."""
        return self._law


class BooleanExpressionPool:
    """Pool of pre-built boolean expressions for simplification tasks.

    Organises expressions by difficulty level, with simpler De Morgan
    and identity law applications at lower difficulties and multi-step
    simplifications at higher difficulties.

    Example:
        >>> import random
        >>> pool = BooleanExpressionPool(random.Random(42))
        >>> expr = pool.sample(1)
        >>> expr.law
        'De Morgan'
    """

    _EASY_EXPRESSIONS: list[tuple[str, str, str]] = [
        ("NOT(A AND B)", "NOT(A) OR NOT(B)", "De Morgan"),
        ("NOT(A OR B)", "NOT(A) AND NOT(B)", "De Morgan"),
        ("A AND 1", "A", "Identity"),
        ("A OR 0", "A", "Identity"),
        ("A AND 0", "0", "Annihilation"),
        ("A OR 1", "1", "Annihilation"),
        ("A AND NOT(A)", "0", "Complement"),
        ("A OR NOT(A)", "1", "Complement"),
    ]

    _MEDIUM_EXPRESSIONS: list[tuple[str, str, str]] = [
        ("A AND (A OR B)", "A", "Absorption"),
        ("A OR (A AND B)", "A", "Absorption"),
        ("NOT(NOT(A))", "A", "Double Negation"),
        ("(A AND B) OR (A AND NOT(B))", "A", "Distribution"),
        ("NOT(A AND B) AND A", "A AND NOT(B)", "De Morgan + Simplify"),
    ]

    _HARD_EXPRESSIONS: list[tuple[str, str, str]] = [
        (
            "NOT(NOT(A) AND NOT(B))",
            "A OR B",
            "De Morgan + Double Negation",
        ),
        (
            "(A OR B) AND (A OR NOT(B))",
            "A",
            "Distribution + Complement",
        ),
        (
            "NOT(A OR B) OR A",
            "A OR NOT(B)",
            "De Morgan + Absorption",
        ),
    ]

    def __init__(self, rng: "random.Random") -> None:
        """Initialise with a random number generator.

        Args:
            rng: Seeded Random instance.
        """
        self._rng = rng

    def sample(self, difficulty: int) -> BooleanExpression:
        """Sample a boolean expression appropriate for the difficulty.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            A BooleanExpression instance.
        """
        pool = self._select_pool(difficulty)
        original, simplified, law = self._rng.choice(pool)
        return BooleanExpression(original, simplified, law)

    def _select_pool(self, difficulty: int) -> list[tuple[str, str, str]]:
        """Select the expression pool based on difficulty.

        Args:
            difficulty: Difficulty level.

        Returns:
            List of (original, simplified, law) tuples.
        """
        if difficulty <= 3:
            return self._EASY_EXPRESSIONS
        if difficulty <= 6:
            return self._EASY_EXPRESSIONS + self._MEDIUM_EXPRESSIONS
        return (
            self._EASY_EXPRESSIONS
            + self._MEDIUM_EXPRESSIONS
            + self._HARD_EXPRESSIONS
        )


class BinaryAdder:
    """Performs binary addition with carry propagation.

    Adds two binary strings bit by bit from right to left,
    recording each step with the carry chain.

    Example:
        >>> adder = BinaryAdder("1010", "0111")
        >>> adder.result
        '10001'
    """

    def __init__(self, a_bin: str, b_bin: str) -> None:
        """Initialise with two binary strings.

        Args:
            a_bin: First binary number as a string.
            b_bin: Second binary number as a string.
        """
        self._a = a_bin
        self._b = b_bin
        self._steps: list[str] = []
        self._result = self._add()

    @property
    def result(self) -> str:
        """Return the binary sum."""
        return self._result

    @property
    def steps(self) -> list[str]:
        """Return the addition steps."""
        return list(self._steps)

    def _add(self) -> str:
        """Perform binary addition with step recording.

        Returns:
            Binary sum as a string.
        """
        max_len = max(len(self._a), len(self._b))
        a_padded = self._a.zfill(max_len)
        b_padded = self._b.zfill(max_len)
        carry = 0
        result_bits: list[str] = []

        for i in range(max_len - 1, -1, -1):
            total, carry = self._add_bit(
                int(a_padded[i]), int(b_padded[i]), carry, i,
            )
            result_bits.append(str(total))

        if carry:
            result_bits.append("1")
            self._steps.append("final carry=1")
        return "".join(reversed(result_bits))

    def _add_bit(self, a: int, b: int, carry: int,
                 pos: int) -> tuple[int, int]:
        """Add one bit position with carry.

        Args:
            a: Bit from first number.
            b: Bit from second number.
            carry: Incoming carry.
            pos: Bit position index.

        Returns:
            Tuple of (result_bit, outgoing_carry).
        """
        total = a + b + carry
        bit = total % 2
        new_carry = total // 2
        if carry > 0:
            self._steps.append(
                f"pos{pos}: {a}+{b}+{carry}={total}, bit={bit}, carry={new_carry}"
            )
        else:
            self._steps.append(
                f"pos{pos}: {a}+{b}={total}, bit={bit}, carry={new_carry}"
            )
        return bit, new_carry


class LogicGateEvaluator:
    """Evaluates nested logic gate expressions on binary inputs.

    Supports AND, OR, NOT, NAND, NOR, and XOR gates with
    step-by-step evaluation from innermost to outermost.

    Example:
        >>> evaluator = LogicGateEvaluator()
        >>> evaluator.evaluate_gate("AND", 1, 0)
        0
    """

    def evaluate_gate(self, gate: str, a: int, b: int = 0) -> int:
        """Evaluate a single logic gate.

        Args:
            gate: Gate name (AND, OR, NOT, NAND, NOR, XOR).
            a: First input (0 or 1).
            b: Second input (0 or 1), unused for NOT.

        Returns:
            Gate output (0 or 1).
        """
        if gate == "AND":
            return a & b
        if gate == "OR":
            return a | b
        if gate == "NOT":
            return 1 - a
        if gate == "NAND":
            return 1 - (a & b)
        if gate == "NOR":
            return 1 - (a | b)
        return a ^ b

    def format_gate(self, gate: str, a: int, b: int = 0) -> str:
        """Format a gate evaluation as a step string.

        Args:
            gate: Gate name.
            a: First input.
            b: Second input, unused for NOT.

        Returns:
            Step string like 'AND(1,0)=0'.
        """
        result = self.evaluate_gate(gate, a, b)
        if gate == "NOT":
            return f"NOT({a})={result}"
        return f"{gate}({a},{b})={result}"


class VectorMath:
    """Provides dot product and vector operations for small vectors.

    Supports integer and float vectors, with step-by-step dot
    product computation and LaTeX formatting.

    Example:
        >>> VectorMath.dot([1, 2], [3, 4])
        11
    """

    @staticmethod
    def dot(a: list[int], b: list[int]) -> int:
        """Compute the dot product of two integer vectors.

        Args:
            a: First vector.
            b: Second vector.

        Returns:
            Integer dot product.
        """
        return sum(x * y for x, y in zip(a, b))

    @staticmethod
    def dot_step(a: list[int], b: list[int]) -> str:
        """Format a dot product computation as a step string.

        Args:
            a: First vector.
            b: Second vector.

        Returns:
            Step string showing each term and the sum.
        """
        terms = [f"{x}({y})" for x, y in zip(a, b)]
        result = sum(x * y for x, y in zip(a, b))
        return f"{'+'.join(terms)}={result}"

    @staticmethod
    def format_vector(vec: list[int]) -> str:
        """Format a vector in LaTeX notation.

        Args:
            vec: List of integer values.

        Returns:
            LaTeX vector string like '[1, 2, 3]'.
        """
        return f"[{', '.join(str(v) for v in vec)}]"


class SigmoidActivation:
    """Computes the sigmoid function for neural network forward passes.

    Provides step-by-step evaluation of sigma(x) = 1/(1 + e^{-x})
    with controlled precision.

    Example:
        >>> sig = SigmoidActivation()
        >>> sig.evaluate(0.0)
        0.5
    """

    def evaluate(self, x: float) -> float:
        """Compute sigmoid(x) with 4 decimal places.

        Args:
            x: Input value.

        Returns:
            Sigmoid value rounded to 4 decimals.
        """
        return round(1.0 / (1.0 + math.exp(-x)), 4)

    def step_detail(self, x: float) -> str:
        """Format a sigmoid evaluation as a step string.

        Args:
            x: Input value.

        Returns:
            Step string showing intermediate computation.
        """
        exp_neg = round(math.exp(-x), 4)
        denom = round(1.0 + exp_neg, 4)
        result = round(1.0 / denom, 4)
        return f"\\sigma({x})=1/(1+e^{{{-x:.4f}}})=1/{denom}={result}"


@register
class BooleanAlgebraGenerator(StepGenerator):
    """Simplify boolean expressions using standard boolean laws.

    Generates boolean expressions and shows their simplification
    using De Morgan's law, distribution, absorption, identity,
    annihilation, complement, and double negation laws.

    Input format:
        ``simplify boolean expression``

    Target format:
        ``NOT(A AND B) <step> apply De Morgan <step> NOT(A) OR NOT(B)``

    Difficulty scaling:
        Difficulty 1-3: single-law applications (De Morgan, identity).
        Difficulty 4-6: absorption and distribution laws.
        Difficulty 7-8: multi-law simplifications.

    Prerequisites:
        logic.

    Example:
        >>> gen = BooleanAlgebraGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'boolean_algebra'
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "boolean_algebra"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 3

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["logic"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls expression complexity.

        Returns:
            Natural language description.
        """
        return "simplify boolean expression"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a boolean expression to simplify.

        Args:
            difficulty: Controls expression complexity.

        Returns:
            Tuple of (expression_string, solution_data).
        """
        pool = BooleanExpressionPool(self._rng)
        expr = pool.sample(difficulty)
        return expr.original, {
            "expression": expr,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate simplification steps showing the law applied.

        Args:
            data: Solution data with the boolean expression.

        Returns:
            Steps showing the law name and result.
        """
        expr = data["expression"]
        return [
            f"apply {expr.law}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the simplified expression.

        Args:
            data: Solution data.

        Returns:
            Simplified boolean expression string.
        """
        return data["expression"].simplified


@register
class BinaryArithmeticGenerator(StepGenerator):
    """Add two binary numbers with carry propagation.

    Generates two binary numbers of varying bit width and shows
    the addition process bit by bit from least significant to
    most significant, tracking carries at each position.

    Input format:
        ``add two binary numbers``

    Target format:
        ``1010 + 0111 <step> pos3: 0+1=1, bit=1, carry=0
        <step> pos2: 1+1=2, bit=0, carry=1
        <step> pos1: 0+1+1=2, bit=0, carry=1
        <step> pos0: 1+0+1=2, bit=0, carry=1
        <step> final carry=1 <step> 10001``

    Difficulty scaling:
        Difficulty 1-2: 4-bit numbers.
        Difficulty 3-4: 6-bit numbers.
        Difficulty 5-6: 8-bit numbers.
        Difficulty 7-8: 10-bit numbers.

    Prerequisites:
        addition, base_conversion.

    Example:
        >>> gen = BinaryArithmeticGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'binary_arithmetic'
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "binary_arithmetic"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 3

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["addition", "base_conversion"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls bit width.

        Returns:
            Natural language description.
        """
        return "add two binary numbers"

    def _bit_width(self, difficulty: int) -> int:
        """Map difficulty to bit width.

        Args:
            difficulty: Difficulty level.

        Returns:
            Number of bits per operand.
        """
        if difficulty <= 2:
            return 4
        if difficulty <= 4:
            return 6
        if difficulty <= 6:
            return 8
        return 10

    def _random_binary(self, bits: int) -> str:
        """Generate a random binary string of given width.

        Args:
            bits: Number of bits.

        Returns:
            Binary string with leading bit always 1.
        """
        result = "1"
        for _ in range(bits - 1):
            result += str(self._rng.randint(0, 1))
        return result

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate two binary numbers and compute their sum.

        Args:
            difficulty: Controls bit width.

        Returns:
            Tuple of (problem_string, solution_data).
        """
        bits = self._bit_width(difficulty)
        a_bin = self._random_binary(bits)
        b_bin = self._random_binary(bits)
        adder = BinaryAdder(a_bin, b_bin)

        problem = f"{a_bin} + {b_bin}"
        return problem, {
            "a_bin": a_bin, "b_bin": b_bin, "adder": adder,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate bit-by-bit addition steps.

        Args:
            data: Solution data with the binary adder.

        Returns:
            Steps showing each bit addition with carries.
        """
        return data["adder"].steps

    def _create_answer(self, data: dict) -> str:
        """Return the binary sum.

        Args:
            data: Solution data.

        Returns:
            Binary result string.
        """
        return data["adder"].result


@register
class TwosComplementGenerator(StepGenerator):
    """Represent negative numbers in N-bit two's complement.

    Generates a negative integer and an N-bit representation,
    showing the conversion process: write the positive binary,
    invert all bits, and add one. Verifies the result by checking
    the sign bit and decimal value.

    Input format:
        ``convert to twos complement``

    Target format:
        ``-5 in 8-bit <step> |5| = 00000101 <step>
        invert: 11111010 <step> add 1: 11111011 <step> 11111011``

    Difficulty scaling:
        Difficulty 1-2: 4-bit, values in [-7, -1].
        Difficulty 3-4: 6-bit, values in [-31, -1].
        Difficulty 5-6: 8-bit, values in [-127, -1].
        Difficulty 7-8: 10-bit, values in [-511, -1].

    Prerequisites:
        binary_arithmetic.

    Example:
        >>> gen = TwosComplementGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'twos_complement'
    """

    _BIT_WIDTHS: dict[int, int] = {
        1: 4, 2: 4, 3: 6, 4: 6,
        5: 8, 6: 8, 7: 10, 8: 10,
    }

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "twos_complement"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["binary_arithmetic"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls bit width.

        Returns:
            Natural language description.
        """
        return "convert to twos complement"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a negative number and its two's complement.

        Args:
            difficulty: Controls bit width and value range.

        Returns:
            Tuple of (problem_string, solution_data).
        """
        bits = self._BIT_WIDTHS.get(difficulty, 8)
        max_neg = -(2 ** (bits - 1) - 1)
        value = self._rng.randint(max_neg, -1)
        positive_bin = self._to_binary(abs(value), bits)
        inverted = self._invert_bits(positive_bin)
        twos_comp = self._add_one(inverted)

        problem = f"{value} in {bits}-bit"
        return problem, {
            "value": value, "bits": bits,
            "positive_bin": positive_bin, "inverted": inverted,
            "twos_comp": twos_comp,
        }

    def _to_binary(self, value: int, bits: int) -> str:
        """Convert a positive integer to a zero-padded binary string.

        Args:
            value: Non-negative integer.
            bits: Desired bit width.

        Returns:
            Binary string padded to the specified width.
        """
        return bin(value)[2:].zfill(bits)

    def _invert_bits(self, binary: str) -> str:
        """Invert all bits in a binary string.

        Args:
            binary: Binary string of 0s and 1s.

        Returns:
            Inverted binary string.
        """
        return "".join("1" if b == "0" else "0" for b in binary)

    def _add_one(self, binary: str) -> str:
        """Add one to a binary string.

        Args:
            binary: Binary string.

        Returns:
            Result of binary + 1, same width.
        """
        bits = len(binary)
        value = int(binary, 2) + 1
        return bin(value)[2:].zfill(bits)[-bits:]

    def _create_steps(self, data: dict) -> list[str]:
        """Generate two's complement conversion steps.

        Args:
            data: Solution data with intermediate binary strings.

        Returns:
            Steps showing positive binary, inversion, and addition.
        """
        abs_val = abs(data["value"])
        return [
            f"|{data['value']}| = {data['positive_bin']}",
            f"invert: {data['inverted']}",
            f"add 1: {data['twos_comp']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the two's complement representation.

        Args:
            data: Solution data.

        Returns:
            Binary string in two's complement.
        """
        return data["twos_comp"]


@register
class LogicGateEvalGenerator(StepGenerator):
    """Evaluate nested logic gate expressions.

    Generates expressions with 2-3 nested logic gates (AND, OR,
    NAND, NOR, XOR, NOT) applied to binary inputs, showing
    evaluation from innermost gate to outermost.

    Input format:
        ``evaluate logic gate expression``

    Target format:
        ``NAND(AND(1,0),OR(1,1)) <step> AND(1,0)=0
        <step> OR(1,1)=1 <step> NAND(0,1)=1 <step> 1``

    Difficulty scaling:
        Difficulty 1-3: 2 nested gates (AND, OR only).
        Difficulty 4-6: 2-3 nested gates (adds NAND, NOR).
        Difficulty 7-8: 3 nested gates (adds XOR, NOT).

    Prerequisites:
        logic.

    Example:
        >>> gen = LogicGateEvalGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'logic_gate_eval'
    """

    _EASY_GATES: list[str] = ["AND", "OR"]
    _MEDIUM_GATES: list[str] = ["AND", "OR", "NAND", "NOR"]
    _HARD_GATES: list[str] = ["AND", "OR", "NAND", "NOR", "XOR"]

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "logic_gate_eval"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 3

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["logic"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls nesting depth and gate types.

        Returns:
            Natural language description.
        """
        return "evaluate logic gate expression"

    def _gate_pool(self, difficulty: int) -> list[str]:
        """Select available gate types based on difficulty.

        Args:
            difficulty: Difficulty level.

        Returns:
            List of gate name strings.
        """
        if difficulty <= 3:
            return self._EASY_GATES
        if difficulty <= 6:
            return self._MEDIUM_GATES
        return self._HARD_GATES

    def _nesting_depth(self, difficulty: int) -> int:
        """Map difficulty to nesting depth.

        Args:
            difficulty: Difficulty level.

        Returns:
            Number of nesting levels (2 or 3).
        """
        if difficulty <= 6:
            return 2
        return 3

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a nested logic gate expression and evaluate it.

        Args:
            difficulty: Controls gate types and nesting.

        Returns:
            Tuple of (expression_string, solution_data).
        """
        pool = self._gate_pool(difficulty)
        evaluator = LogicGateEvaluator()
        depth = self._nesting_depth(difficulty)

        if depth == 2:
            return self._build_depth_2(pool, evaluator)
        return self._build_depth_3(pool, evaluator)

    def _build_depth_2(self, pool: list[str],
                       evaluator: LogicGateEvaluator) -> tuple[str, dict]:
        """Build a 2-level nested gate expression.

        Args:
            pool: Available gate types.
            evaluator: Logic gate evaluator instance.

        Returns:
            Tuple of (expression, solution_data).
        """
        inner1_gate = self._rng.choice(pool)
        inner2_gate = self._rng.choice(pool)
        outer_gate = self._rng.choice(pool)
        a, b = self._rng.randint(0, 1), self._rng.randint(0, 1)
        c, d = self._rng.randint(0, 1), self._rng.randint(0, 1)

        r1 = evaluator.evaluate_gate(inner1_gate, a, b)
        r2 = evaluator.evaluate_gate(inner2_gate, c, d)
        final = evaluator.evaluate_gate(outer_gate, r1, r2)

        expr = (
            f"{outer_gate}("
            f"{inner1_gate}({a},{b}),"
            f"{inner2_gate}({c},{d}))"
        )
        steps = [
            evaluator.format_gate(inner1_gate, a, b),
            evaluator.format_gate(inner2_gate, c, d),
            evaluator.format_gate(outer_gate, r1, r2),
        ]
        return expr, {"steps": steps, "result": final}

    def _build_depth_3(self, pool: list[str],
                       evaluator: LogicGateEvaluator) -> tuple[str, dict]:
        """Build a 3-level nested gate expression.

        Args:
            pool: Available gate types.
            evaluator: Logic gate evaluator instance.

        Returns:
            Tuple of (expression, solution_data).
        """
        g1 = self._rng.choice(pool)
        g2 = self._rng.choice(pool)
        g3 = self._rng.choice(pool)
        g4 = self._rng.choice(pool)
        a, b = self._rng.randint(0, 1), self._rng.randint(0, 1)
        c, d = self._rng.randint(0, 1), self._rng.randint(0, 1)

        r1 = evaluator.evaluate_gate(g1, a, b)
        r2 = evaluator.evaluate_gate(g2, c, d)
        r3 = evaluator.evaluate_gate(g3, r1, r2)
        final = evaluator.evaluate_gate(g4, r3, self._rng.randint(0, 1))

        inner_input = self._rng.randint(0, 1)
        final = evaluator.evaluate_gate(g4, r3, inner_input)

        expr = (
            f"{g4}("
            f"{g3}("
            f"{g1}({a},{b}),{g2}({c},{d})),"
            f"{inner_input})"
        )
        steps = [
            evaluator.format_gate(g1, a, b),
            evaluator.format_gate(g2, c, d),
            evaluator.format_gate(g3, r1, r2),
            evaluator.format_gate(g4, r3, inner_input),
        ]
        return expr, {"steps": steps, "result": final}

    def _create_steps(self, data: dict) -> list[str]:
        """Return the pre-computed evaluation steps.

        Args:
            data: Solution data with evaluation steps.

        Returns:
            Steps showing each gate evaluation.
        """
        return data["steps"]

    def _create_answer(self, data: dict) -> str:
        """Return the final gate output.

        Args:
            data: Solution data.

        Returns:
            String '0' or '1'.
        """
        return str(data["result"])


@register
class SoftmaxEvalGenerator(StepGenerator):
    """Compute the softmax of a small integer vector.

    Generates a vector of 3-5 small integers, computes e^{x_i}
    for each element, sums the exponentials, and divides each
    by the sum to produce the softmax probability distribution.

    Input format:
        ``compute softmax of vector``

    Target format:
        ``softmax([2, 1, 0]) <step> e^2=7.3891 <step> e^1=2.7183
        <step> e^0=1.0 <step> sum=11.1074
        <step> p_0=7.3891/11.1074=0.6652
        <step> p_1=2.7183/11.1074=0.2447
        <step> p_2=1.0/11.1074=0.0900
        <step> [0.6652, 0.2447, 0.0900]``

    Difficulty scaling:
        Difficulty 1-3: 3 elements, values in [-2, 3].
        Difficulty 4-6: 4 elements, values in [-3, 5].
        Difficulty 7-8: 5 elements, values in [-5, 8].

    Prerequisites:
        exponentiation, division, addition.

    Example:
        >>> gen = SoftmaxEvalGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'softmax_eval'
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "softmax_eval"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["exponentiation", "division", "addition"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls vector size and value range.

        Returns:
            Natural language description.
        """
        return "compute softmax of vector"

    def _vector_params(self, difficulty: int) -> tuple[int, int, int]:
        """Map difficulty to vector size and value range.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (vector_size, min_value, max_value).
        """
        if difficulty <= 3:
            return 3, -2, 3
        if difficulty <= 6:
            return 4, -3, 5
        return 5, -5, 8

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an integer vector and compute its softmax.

        Args:
            difficulty: Controls vector size and range.

        Returns:
            Tuple of (problem_string, solution_data).
        """
        size, lo, hi = self._vector_params(difficulty)
        vec = [self._rng.randint(lo, hi) for _ in range(size)]
        exp_vals = [round(math.exp(x), 4) for x in vec]
        exp_sum = round(sum(exp_vals), 4)
        probs = [round(e / exp_sum, 4) for e in exp_vals]

        vec_str = ", ".join(str(x) for x in vec)
        problem = f"softmax([{vec_str}])"
        return problem, {
            "vec": vec, "exp_vals": exp_vals,
            "exp_sum": exp_sum, "probs": probs,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate exponentiation, sum, and division steps.

        Args:
            data: Solution data with intermediate values.

        Returns:
            Steps showing each e^{x_i}, the sum, and each probability.
        """
        vec = data["vec"]
        exp_vals = data["exp_vals"]
        exp_sum = data["exp_sum"]
        probs = data["probs"]
        steps: list[str] = []

        for i, (x, e) in enumerate(zip(vec, exp_vals)):
            steps.append(f"e^{{{x}}}={e}")

        steps.append(f"sum={exp_sum}")

        for i, (e, p) in enumerate(zip(exp_vals, probs)):
            steps.append(f"p_{{{i}}}={e}/{exp_sum}={p}")

        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the softmax probability vector.

        Args:
            data: Solution data.

        Returns:
            String representation of the probability vector.
        """
        probs = data["probs"]
        return f"[{', '.join(str(p) for p in probs)}]"


@register
class AttentionScoreGenerator(StepGenerator):
    """Compute scaled attention score QK^T/sqrt(d_k) for small vectors.

    Generates a query vector Q and a key vector K of dimension d_k,
    computes their dot product, and divides by sqrt(d_k). Uses small
    integer values for clean computation.

    Input format:
        ``compute attention score``

    Target format:
        ``Q=[1,2,3], K=[4,5,6], d_k=3 <step>
        QK^T=1(4)+2(5)+3(6)=32 <step>
        \\sqrt{d_k}=\\sqrt{3}=1.7321 <step>
        32/1.7321=18.4752 <step> 18.4752``

    Difficulty scaling:
        Difficulty 1-3: d_k=2, values in [-3, 3].
        Difficulty 4-6: d_k=3, values in [-5, 5].
        Difficulty 7-8: d_k=4, values in [-8, 8].

    Prerequisites:
        matrix_multiply, division.

    Example:
        >>> gen = AttentionScoreGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'attention_score'
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "attention_score"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["matrix_multiply", "division"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls vector dimension.

        Returns:
            Natural language description.
        """
        return "compute attention score"

    def _vector_params(self, difficulty: int) -> tuple[int, int, int]:
        """Map difficulty to dimension and value range.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (d_k, min_value, max_value).
        """
        if difficulty <= 3:
            return 2, -3, 3
        if difficulty <= 6:
            return 3, -5, 5
        return 4, -8, 8

    def _random_vector(self, size: int, lo: int, hi: int) -> list[int]:
        """Generate a random integer vector.

        Args:
            size: Vector dimension.
            lo: Minimum element value.
            hi: Maximum element value.

        Returns:
            List of random integers.
        """
        return [self._rng.randint(lo, hi) for _ in range(size)]

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate Q, K vectors and compute the attention score.

        Args:
            difficulty: Controls dimension and value range.

        Returns:
            Tuple of (problem_string, solution_data).
        """
        dk, lo, hi = self._vector_params(difficulty)
        q = self._random_vector(dk, lo, hi)
        k = self._random_vector(dk, lo, hi)
        dot = VectorMath.dot(q, k)
        sqrt_dk = round(math.sqrt(dk), 4)
        score = round(dot / sqrt_dk, 4)

        q_str = VectorMath.format_vector(q)
        k_str = VectorMath.format_vector(k)
        problem = f"Q={q_str}, K={k_str}, d_k={dk}"
        return problem, {
            "q": q, "k": k, "dk": dk, "dot": dot,
            "sqrt_dk": sqrt_dk, "score": score,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate dot product and scaling steps.

        Args:
            data: Solution data with Q, K, and score.

        Returns:
            Steps showing dot product, sqrt(d_k), and division.
        """
        q, k = data["q"], data["k"]
        dot = data["dot"]
        dk = data["dk"]
        sqrt_dk = data["sqrt_dk"]
        score = data["score"]

        dot_step = VectorMath.dot_step(q, k)
        return [
            f"QK^T={dot_step}",
            f"\\sqrt{{d_k}}=\\sqrt{{{dk}}}={sqrt_dk}",
            f"{dot}/{sqrt_dk}={score}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the attention score.

        Args:
            data: Solution data.

        Returns:
            String representation of the scaled score.
        """
        return str(data["score"])


@register
class BackpropSimpleGenerator(StepGenerator):
    """Compute the gradient of f(x) = ax^2 + bx + c at a point.

    Generates a simple quadratic function with integer coefficients,
    differentiates symbolically using the power rule, and evaluates
    the derivative at an integer point.

    Input format:
        ``compute gradient of quadratic at point``

    Target format:
        ``f(x)=3x^2+2x+1, x=4 <step> f'(x)=6x+2
        <step> f'(4)=6(4)+2=26 <step> 26``

    Difficulty scaling:
        Difficulty 1-3: a in [1, 3], b in [-3, 3], c in [-5, 5], x in [1, 3].
        Difficulty 4-6: a in [1, 5], b in [-5, 5], c in [-8, 8], x in [1, 5].
        Difficulty 7-8: a in [1, 8], b in [-8, 8], c in [-10, 10], x in [1, 8].

    Prerequisites:
        derivative_eval.

    Example:
        >>> gen = BackpropSimpleGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'backprop_simple'
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "backprop_simple"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["derivative_eval"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls coefficient and point magnitude.

        Returns:
            Natural language description.
        """
        return "compute gradient of quadratic at point"

    def _param_ranges(self, difficulty: int) -> dict[str, tuple[int, int]]:
        """Map difficulty to coefficient and point ranges.

        Args:
            difficulty: Difficulty level.

        Returns:
            Dict of parameter ranges.
        """
        if difficulty <= 3:
            return {"a": (1, 3), "b": (-3, 3), "c": (-5, 5), "x": (1, 3)}
        if difficulty <= 6:
            return {"a": (1, 5), "b": (-5, 5), "c": (-8, 8), "x": (1, 5)}
        return {"a": (1, 8), "b": (-8, 8), "c": (-10, 10), "x": (1, 8)}

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a quadratic, differentiate, and evaluate.

        Args:
            difficulty: Controls coefficient magnitude.

        Returns:
            Tuple of (problem_string, solution_data).
        """
        ranges = self._param_ranges(difficulty)
        a = self._rng.randint(*ranges["a"])
        b = self._rng.randint(*ranges["b"])
        c = self._rng.randint(*ranges["c"])
        x = self._rng.randint(*ranges["x"])
        deriv_a = 2 * a
        gradient = deriv_a * x + b

        func_str = self._format_quadratic(a, b, c)
        problem = f"f(x)={func_str}, x={x}"
        return problem, {
            "a": a, "b": b, "c": c, "x": x,
            "deriv_a": deriv_a, "gradient": gradient,
        }

    def _format_quadratic(self, a: int, b: int, c: int) -> str:
        """Format ax^2 + bx + c as a string.

        Args:
            a: Coefficient of x^2.
            b: Coefficient of x.
            c: Constant term.

        Returns:
            Formatted quadratic string.
        """
        parts = [f"{a}x^2"]
        if b > 0:
            parts.append(f"+{b}x")
        elif b < 0:
            parts.append(f"{b}x")
        if c > 0:
            parts.append(f"+{c}")
        elif c < 0:
            parts.append(f"{c}")
        return "".join(parts)

    def _format_derivative(self, deriv_a: int, b: int) -> str:
        """Format the derivative 2ax + b as a string.

        Args:
            deriv_a: Coefficient 2a.
            b: Constant term of derivative.

        Returns:
            Formatted derivative string.
        """
        parts = [f"{deriv_a}x"]
        if b > 0:
            parts.append(f"+{b}")
        elif b < 0:
            parts.append(f"{b}")
        return "".join(parts)

    def _create_steps(self, data: dict) -> list[str]:
        """Generate differentiation and evaluation steps.

        Args:
            data: Solution data with coefficients and point.

        Returns:
            Steps showing the derivative and its evaluation.
        """
        deriv_a = data["deriv_a"]
        b = data["b"]
        x = data["x"]
        gradient = data["gradient"]
        deriv_str = self._format_derivative(deriv_a, b)
        product = deriv_a * x

        if b >= 0:
            eval_str = f"{deriv_a}({x})+{b}={product}+{b}={gradient}"
        else:
            eval_str = f"{deriv_a}({x}){b}={product}{b}={gradient}"

        return [
            f"f'(x)={deriv_str}",
            f"f'({x})={eval_str}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the gradient value.

        Args:
            data: Solution data.

        Returns:
            String representation of the gradient.
        """
        return str(data["gradient"])


@register
class NeuralForwardGenerator(StepGenerator):
    """Compute a 2-layer MLP forward pass with sigmoid activation.

    Generates a 2-layer multi-layer perceptron with small integer
    weights and biases. Computes z1 = W1*x + b1, a1 = sigmoid(z1),
    z2 = W2*a1 + b2, output = sigmoid(z2). Uses 2-dimensional
    input, 2-dimensional hidden layer, and 1-dimensional output.

    Input format:
        ``compute neural network forward pass``

    Target format:
        ``x=[1,2], W1=[[1,2],[3,4]], b1=[0,1],
        W2=[[1,1]], b2=[0] <step>
        z1_0=1(1)+2(2)+0=5 <step> z1_1=3(1)+4(2)+1=12
        <step> a1_0=sigmoid(5)=0.9933 <step> a1_1=sigmoid(12)=0.9999
        <step> z2=1(0.9933)+1(0.9999)+0=1.9932
        <step> output=sigmoid(1.9932)=0.8802 <step> 0.8802``

    Difficulty scaling:
        Difficulty 1-3: weights in [-2, 2], biases in [-1, 1].
        Difficulty 4-6: weights in [-3, 3], biases in [-2, 2].
        Difficulty 7-8: weights in [-5, 5], biases in [-3, 3].

    Prerequisites:
        matrix_multiply, sigmoid_eval.

    Example:
        >>> gen = NeuralForwardGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'neural_forward'
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "neural_forward"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["matrix_multiply", "sigmoid_eval"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls weight magnitude.

        Returns:
            Natural language description.
        """
        return "compute neural network forward pass"

    def _weight_range(self, difficulty: int) -> tuple[int, int]:
        """Map difficulty to weight range.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (min_weight, max_weight).
        """
        if difficulty <= 3:
            return -2, 2
        if difficulty <= 6:
            return -3, 3
        return -5, 5

    def _bias_range(self, difficulty: int) -> tuple[int, int]:
        """Map difficulty to bias range.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (min_bias, max_bias).
        """
        if difficulty <= 3:
            return -1, 1
        if difficulty <= 6:
            return -2, 2
        return -3, 3

    def _random_matrix(self, rows: int, cols: int,
                       lo: int, hi: int) -> list[list[int]]:
        """Generate a random integer matrix.

        Args:
            rows: Number of rows.
            cols: Number of columns.
            lo: Minimum entry value.
            hi: Maximum entry value.

        Returns:
            2D list of integer entries.
        """
        return [
            [self._rng.randint(lo, hi) for _ in range(cols)]
            for _ in range(rows)
        ]

    def _random_bias(self, size: int, lo: int, hi: int) -> list[int]:
        """Generate a random integer bias vector.

        Args:
            size: Vector dimension.
            lo: Minimum value.
            hi: Maximum value.

        Returns:
            List of integer biases.
        """
        return [self._rng.randint(lo, hi) for _ in range(size)]

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a 2-layer MLP and compute the forward pass.

        Args:
            difficulty: Controls weight and bias magnitude.

        Returns:
            Tuple of (problem_string, solution_data).
        """
        w_lo, w_hi = self._weight_range(difficulty)
        b_lo, b_hi = self._bias_range(difficulty)
        x = [self._rng.randint(-3, 3) for _ in range(2)]
        w1 = self._random_matrix(2, 2, w_lo, w_hi)
        b1 = self._random_bias(2, b_lo, b_hi)
        w2 = self._random_matrix(1, 2, w_lo, w_hi)
        b2 = self._random_bias(1, b_lo, b_hi)

        z1, a1, z2, output = self._forward(x, w1, b1, w2, b2)

        problem = self._format_problem(x, w1, b1, w2, b2)
        return problem, {
            "x": x, "w1": w1, "b1": b1, "w2": w2, "b2": b2,
            "z1": z1, "a1": a1, "z2": z2, "output": output,
        }

    def _forward(self, x: list[int], w1: list[list[int]],
                 b1: list[int], w2: list[list[int]],
                 b2: list[int]) -> tuple[list[int], list[float], float, float]:
        """Compute the full forward pass.

        Args:
            x: Input vector.
            w1: First layer weights (2x2).
            b1: First layer biases (2).
            w2: Second layer weights (1x2).
            b2: Second layer biases (1).

        Returns:
            Tuple of (z1, a1, z2, output).
        """
        sigmoid = SigmoidActivation()
        z1 = [
            w1[i][0] * x[0] + w1[i][1] * x[1] + b1[i]
            for i in range(2)
        ]
        a1 = [sigmoid.evaluate(float(z)) for z in z1]
        z2_val = w2[0][0] * a1[0] + w2[0][1] * a1[1] + b2[0]
        z2_rounded = round(z2_val, 4)
        output = sigmoid.evaluate(z2_rounded)
        return z1, a1, z2_rounded, output

    def _format_problem(self, x: list[int], w1: list[list[int]],
                        b1: list[int], w2: list[list[int]],
                        b2: list[int]) -> str:
        """Format the MLP specification as a problem string.

        Args:
            x: Input vector.
            w1: First layer weights.
            b1: First layer biases.
            w2: Second layer weights.
            b2: Second layer biases.

        Returns:
            Formatted problem description.
        """
        x_str = VectorMath.format_vector(x)
        w1_str = f"[{VectorMath.format_vector(w1[0])}, {VectorMath.format_vector(w1[1])}]"
        b1_str = VectorMath.format_vector(b1)
        w2_str = f"[{VectorMath.format_vector(w2[0])}]"
        b2_str = VectorMath.format_vector(b2)
        return f"x={x_str}, W1={w1_str}, b1={b1_str}, W2={w2_str}, b2={b2_str}"

    def _create_steps(self, data: dict) -> list[str]:
        """Generate layer-by-layer forward pass steps.

        Args:
            data: Solution data with all intermediate values.

        Returns:
            Steps showing z1, a1, z2, and output computation.
        """
        x = data["x"]
        w1, b1 = data["w1"], data["b1"]
        w2, b2 = data["w2"], data["b2"]
        z1, a1 = data["z1"], data["a1"]
        z2, output = data["z2"], data["output"]
        steps: list[str] = []

        for i in range(2):
            dot = w1[i][0] * x[0] + w1[i][1] * x[1]
            steps.append(
                f"z1_{i}={w1[i][0]}({x[0]})+{w1[i][1]}({x[1]})+{b1[i]}={z1[i]}"
            )

        for i in range(2):
            steps.append(f"a1_{i}=sigmoid({z1[i]})={a1[i]}")

        z2_dot = round(w2[0][0] * a1[0] + w2[0][1] * a1[1], 4)
        steps.append(
            f"z2={w2[0][0]}({a1[0]})+{w2[0][1]}({a1[1]})+{b2[0]}={z2}"
        )
        steps.append(f"output=sigmoid({z2})={output}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the network output.

        Args:
            data: Solution data.

        Returns:
            String representation of the output.
        """
        return str(data["output"])
