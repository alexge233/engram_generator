"""Quantum mechanics generators — complex arithmetic through quantum gates.

Introduces complex number operations (tier 4), Euler's formula and
qubit measurement (tier 5), and quantum gate application (tier 6).
These tasks build a path from foundational complex arithmetic to
quantum computing concepts, using simple fractions and exact
trigonometric values for clean, verifiable outputs.
"""
import math
from fractions import Fraction

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


class ComplexNumber:
    """Represents a complex number a + bi with integer or fractional parts.

    Provides arithmetic operations, modulus computation, and LaTeX
    formatting for complex number manipulation in quantum mechanics
    generators.

    Example:
        >>> c = ComplexNumber(3, -2)
        >>> c.to_latex()
        '3-2i'
        >>> c.modulus_squared()
        13
    """

    def __init__(self, real: int, imag: int) -> None:
        """Initialise with integer real and imaginary parts.

        Args:
            real: Real component.
            imag: Imaginary component.
        """
        self._real = real
        self._imag = imag

    @property
    def real(self) -> int:
        """Return the real part."""
        return self._real

    @property
    def imag(self) -> int:
        """Return the imaginary part."""
        return self._imag

    def multiply(self, other: "ComplexNumber") -> "ComplexNumber":
        """Multiply this complex number by another using FOIL.

        Args:
            other: The complex number to multiply by.

        Returns:
            Product as a new ComplexNumber.
        """
        real = self._real * other.real - self._imag * other.imag
        imag = self._real * other.imag + self._imag * other.real
        return ComplexNumber(real, imag)

    def modulus_squared(self) -> int:
        """Compute |z|^2 = a^2 + b^2.

        Returns:
            The squared modulus as an integer.
        """
        return self._real * self._real + self._imag * self._imag

    def to_latex(self) -> str:
        """Format as a LaTeX string.

        Returns:
            LaTeX representation like '3-2i' or '5+4i'.
        """
        if self._imag == 0:
            return str(self._real)
        if self._real == 0:
            return self._format_imag_only()
        sign = "+" if self._imag > 0 else "-"
        abs_imag = abs(self._imag)
        imag_str = "i" if abs_imag == 1 else f"{abs_imag}i"
        return f"{self._real}{sign}{imag_str}"

    def _format_imag_only(self) -> str:
        """Format when the real part is zero.

        Returns:
            LaTeX string for the imaginary-only case.
        """
        if self._imag == 1:
            return "i"
        if self._imag == -1:
            return "-i"
        return f"{self._imag}i"


class AngleTable:
    """Provides exact trigonometric values for standard angles.

    Stores known sin/cos values as string representations for
    angles commonly used in quantum mechanics: 0, pi/6, pi/4,
    pi/3, pi/2, and pi. Avoids floating-point approximation
    by using symbolic exact values.

    Example:
        >>> table = AngleTable()
        >>> table.cos_str("pi/4")
        '\\\\frac{\\\\sqrt{2}}{2}'
    """

    _ANGLES: list[str] = ["0", "\\pi/6", "\\pi/4", "\\pi/3", "\\pi/2", "\\pi"]

    _COS_VALUES: dict[str, str] = {
        "0": "1",
        "\\pi/6": "\\frac{\\sqrt{3}}{2}",
        "\\pi/4": "\\frac{\\sqrt{2}}{2}",
        "\\pi/3": "\\frac{1}{2}",
        "\\pi/2": "0",
        "\\pi": "-1",
    }

    _SIN_VALUES: dict[str, str] = {
        "0": "0",
        "\\pi/6": "\\frac{1}{2}",
        "\\pi/4": "\\frac{\\sqrt{2}}{2}",
        "\\pi/3": "\\frac{\\sqrt{3}}{2}",
        "\\pi/2": "1",
        "\\pi": "0",
    }

    _NUMERIC_ANGLES: dict[str, float] = {
        "0": 0.0,
        "\\pi/6": math.pi / 6,
        "\\pi/4": math.pi / 4,
        "\\pi/3": math.pi / 3,
        "\\pi/2": math.pi / 2,
        "\\pi": math.pi,
    }

    @property
    def angles(self) -> list[str]:
        """Return the list of available angle labels."""
        return list(self._ANGLES)

    def cos_str(self, angle: str) -> str:
        """Return the exact cosine value as a LaTeX string.

        Args:
            angle: Angle label from the standard set.

        Returns:
            LaTeX string for cos(angle).
        """
        return self._COS_VALUES[angle]

    def sin_str(self, angle: str) -> str:
        """Return the exact sine value as a LaTeX string.

        Args:
            angle: Angle label from the standard set.

        Returns:
            LaTeX string for sin(angle).
        """
        return self._SIN_VALUES[angle]

    def cos_numeric(self, angle: str) -> float:
        """Return the numeric cosine value.

        Args:
            angle: Angle label from the standard set.

        Returns:
            Float cosine value.
        """
        return round(math.cos(self._NUMERIC_ANGLES[angle]), 4)

    def sin_numeric(self, angle: str) -> float:
        """Return the numeric sine value.

        Args:
            angle: Angle label from the standard set.

        Returns:
            Float sine value.
        """
        return round(math.sin(self._NUMERIC_ANGLES[angle]), 4)


class QubitState:
    """Represents a single-qubit state a|0> + b|1> with fractional amplitudes.

    Stores amplitudes as string labels and their squared magnitudes
    as Fractions, providing measurement probability computation and
    LaTeX formatting in Dirac notation.

    Example:
        >>> qs = QubitState("\\\\frac{1}{\\\\sqrt{2}}", "\\\\frac{1}{\\\\sqrt{2}}", Fraction(1, 2), Fraction(1, 2))
        >>> qs.prob_zero()
        Fraction(1, 2)
    """

    _AMPLITUDE_POOL: list[tuple[str, Fraction]] = [
        ("1", Fraction(1, 1)),
        ("\\frac{1}{\\sqrt{2}}", Fraction(1, 2)),
        ("\\frac{1}{2}", Fraction(1, 4)),
        ("\\frac{\\sqrt{3}}{2}", Fraction(3, 4)),
    ]

    def __init__(self, alpha_label: str, beta_label: str,
                 alpha_sq: Fraction, beta_sq: Fraction) -> None:
        """Initialise a qubit state with labelled amplitudes.

        Args:
            alpha_label: LaTeX string for amplitude of |0>.
            beta_label: LaTeX string for amplitude of |1>.
            alpha_sq: |alpha|^2 as a Fraction.
            beta_sq: |beta|^2 as a Fraction.
        """
        self._alpha_label = alpha_label
        self._beta_label = beta_label
        self._alpha_sq = alpha_sq
        self._beta_sq = beta_sq

    @property
    def alpha_label(self) -> str:
        """Return the LaTeX label for the |0> amplitude."""
        return self._alpha_label

    @property
    def beta_label(self) -> str:
        """Return the LaTeX label for the |1> amplitude."""
        return self._beta_label

    def prob_zero(self) -> Fraction:
        """Return the measurement probability P(0) = |alpha|^2.

        Returns:
            Probability as a Fraction.
        """
        return self._alpha_sq

    def prob_one(self) -> Fraction:
        """Return the measurement probability P(1) = |beta|^2.

        Returns:
            Probability as a Fraction.
        """
        return self._beta_sq

    def to_latex(self) -> str:
        """Format the qubit state in Dirac bra-ket notation.

        Returns:
            LaTeX string like 'alpha|0> + beta|1>'.
        """
        return (
            f"{self._alpha_label}|0\\rangle + "
            f"{self._beta_label}|1\\rangle"
        )

    @classmethod
    def valid_pairs(cls) -> list[tuple[tuple[str, Fraction], tuple[str, Fraction]]]:
        """Return all valid (alpha, beta) pairs that normalise to 1.

        Returns:
            List of ((alpha_label, alpha_sq), (beta_label, beta_sq)) tuples.
        """
        pairs: list[tuple[tuple[str, Fraction], tuple[str, Fraction]]] = []
        for a_label, a_sq in cls._AMPLITUDE_POOL:
            for b_label, b_sq in cls._AMPLITUDE_POOL:
                if a_sq + b_sq == Fraction(1, 1):
                    pairs.append(((a_label, a_sq), (b_label, b_sq)))
        return pairs


class QuantumGate:
    """Represents a 2x2 quantum gate matrix with known name.

    Provides matrix-vector multiplication for single-qubit gates
    and LaTeX formatting for both the gate matrix and the result.

    Example:
        >>> h = QuantumGate("H", [[1, 1], [1, -1]], "\\\\frac{1}{\\\\sqrt{2}}")
        >>> h.name
        'H'
    """

    def __init__(self, name: str, matrix: list[list[int]],
                 scale_label: str = "1") -> None:
        """Initialise a quantum gate.

        Args:
            name: Gate name (e.g. 'H', 'X', 'Z').
            matrix: 2x2 integer matrix (before scaling).
            scale_label: LaTeX string for the overall scale factor.
        """
        self._name = name
        self._matrix = matrix
        self._scale_label = scale_label

    @property
    def name(self) -> str:
        """Return the gate name."""
        return self._name

    @property
    def scale_label(self) -> str:
        """Return the LaTeX scale factor."""
        return self._scale_label

    def matrix_latex(self) -> str:
        """Format the gate matrix in LaTeX pmatrix notation.

        Returns:
            LaTeX string for the gate matrix.
        """
        rows = [" & ".join(str(v) for v in row) for row in self._matrix]
        body = " \\\\ ".join(rows)
        if self._scale_label == "1":
            return f"\\begin{{pmatrix}} {body} \\end{{pmatrix}}"
        return (
            f"{self._scale_label}"
            f"\\begin{{pmatrix}} {body} \\end{{pmatrix}}"
        )

    def apply_to(self, vector: list[int]) -> list[int]:
        """Apply the gate matrix to a 2-element state vector.

        Args:
            vector: Two-element integer vector [a, b].

        Returns:
            Result vector [c, d] after matrix multiplication.
        """
        c = self._matrix[0][0] * vector[0] + self._matrix[0][1] * vector[1]
        d = self._matrix[1][0] * vector[0] + self._matrix[1][1] * vector[1]
        return [c, d]

    def step_row(self, row_idx: int, vector: list[int]) -> str:
        """Format one row of the matrix-vector multiplication.

        Args:
            row_idx: Row index (0 or 1).
            vector: Input state vector.

        Returns:
            Step string showing the dot product computation.
        """
        r = self._matrix[row_idx]
        result = r[0] * vector[0] + r[1] * vector[1]
        return (
            f"c_{{{row_idx}}}="
            f"{r[0]}({vector[0]})+{r[1]}({vector[1]})="
            f"{result}"
        )


@register
class ComplexArithmeticGenerator(StepGenerator):
    """Complex number multiplication using FOIL and i^2 = -1.

    Generates two complex numbers (a+bi) and (c+di) with small
    integer components and shows the FOIL expansion step by step:
    first, outer, inner, last, followed by the i^2 = -1 substitution
    and combination of real and imaginary parts.

    Input format:
        ``multiply two complex numbers``

    Target format:
        ``(3+2i)(1-4i) <step> first: 3*1=3 <step> outer: 3*(-4i)=-12i
        <step> inner: 2i*1=2i <step> last: 2i*(-4i)=-8i^2=8
        <step> real: 3+8=11 <step> imag: -12i+2i=-10i <step> 11-10i``

    Difficulty scaling:
        Difficulty 1-3: components in [-3, 3].
        Difficulty 4-6: components in [-6, 6].
        Difficulty 7-8: components in [-10, 10].

    Prerequisites:
        multiplication, addition.

    Example:
        >>> gen = ComplexArithmeticGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'complex_arithmetic'
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "complex_arithmetic"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["multiplication", "addition"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls component magnitude.

        Returns:
            Natural language description.
        """
        return "multiply two complex numbers"

    def _component_range(self, difficulty: int) -> tuple[int, int]:
        """Map difficulty to component range.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (min_component, max_component).
        """
        if difficulty <= 3:
            return -3, 3
        if difficulty <= 6:
            return -6, 6
        return -10, 10

    def _sample_nonzero(self, lo: int, hi: int) -> int:
        """Sample a nonzero integer in [lo, hi].

        Args:
            lo: Lower bound.
            hi: Upper bound.

        Returns:
            Nonzero integer.
        """
        val = 0
        while val == 0:
            val = self._rng.randint(lo, hi)
        return val

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate two complex numbers and compute their product.

        Args:
            difficulty: Controls component magnitude.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        lo, hi = self._component_range(difficulty)
        z1 = ComplexNumber(self._sample_nonzero(lo, hi), self._sample_nonzero(lo, hi))
        z2 = ComplexNumber(self._sample_nonzero(lo, hi), self._sample_nonzero(lo, hi))
        product = z1.multiply(z2)

        problem = f"({z1.to_latex()})({z2.to_latex()})"
        return problem, {"z1": z1, "z2": z2, "product": product}

    def _create_steps(self, data: dict) -> list[str]:
        """Generate FOIL expansion steps.

        Args:
            data: Solution data with z1, z2, and product.

        Returns:
            Steps showing first, outer, inner, last, and combination.
        """
        z1, z2 = data["z1"], data["z2"]
        first = z1.real * z2.real
        outer = z1.real * z2.imag
        inner = z1.imag * z2.real
        last_i2 = z1.imag * z2.imag
        real_sum = first + (-last_i2)
        imag_sum = outer + inner

        return [
            f"first: {z1.real}*{z2.real}={first}",
            f"outer: {z1.real}*{z2.imag}i={outer}i",
            f"inner: {z1.imag}i*{z2.real}={inner}i",
            f"last: {z1.imag}i*{z2.imag}i={last_i2}i^2={-last_i2}",
            f"real: {first}+{-last_i2}={real_sum}",
            f"imag: {outer}i+{inner}i={imag_sum}i",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the product as a complex number string.

        Args:
            data: Solution data.

        Returns:
            LaTeX string for the product.
        """
        return data["product"].to_latex()


@register
class ComplexModulusGenerator(StepGenerator):
    """Compute the modulus |a+bi| = sqrt(a^2 + b^2).

    Generates a complex number with small integer components and
    shows the step-by-step computation: square real part, square
    imaginary part, sum them, and take the square root.

    Input format:
        ``compute complex modulus``

    Target format:
        ``|3+4i| <step> a^2=3^2=9 <step> b^2=4^2=16
        <step> a^2+b^2=9+16=25 <step> \\sqrt{25}=5 <step> 5``

    Difficulty scaling:
        Difficulty 1-3: components in [-4, 4].
        Difficulty 4-6: components in [-8, 8].
        Difficulty 7-8: components in [-12, 12].

    Prerequisites:
        complex_arithmetic, exponentiation.

    Example:
        >>> gen = ComplexModulusGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'complex_modulus'
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "complex_modulus"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["complex_arithmetic", "exponentiation"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls component magnitude.

        Returns:
            Natural language description.
        """
        return "compute complex modulus"

    def _component_range(self, difficulty: int) -> tuple[int, int]:
        """Map difficulty to component range.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (min_component, max_component).
        """
        if difficulty <= 3:
            return -4, 4
        if difficulty <= 6:
            return -8, 8
        return -12, 12

    def _sample_nonzero(self, lo: int, hi: int) -> int:
        """Sample a nonzero integer in [lo, hi].

        Args:
            lo: Lower bound.
            hi: Upper bound.

        Returns:
            Nonzero integer.
        """
        val = 0
        while val == 0:
            val = self._rng.randint(lo, hi)
        return val

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a complex number and compute its modulus.

        Args:
            difficulty: Controls component magnitude.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        lo, hi = self._component_range(difficulty)
        a = self._sample_nonzero(lo, hi)
        b = self._sample_nonzero(lo, hi)
        z = ComplexNumber(a, b)
        a_sq = a * a
        b_sq = b * b
        sum_sq = a_sq + b_sq
        modulus = math.sqrt(sum_sq)

        return f"|{z.to_latex()}|", {
            "a": a, "b": b, "a_sq": a_sq, "b_sq": b_sq,
            "sum_sq": sum_sq, "modulus": modulus,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate squaring, summing, and square root steps.

        Args:
            data: Solution data with intermediate values.

        Returns:
            Steps showing each computation phase.
        """
        a, b = data["a"], data["b"]
        a_sq, b_sq = data["a_sq"], data["b_sq"]
        sum_sq = data["sum_sq"]
        modulus = data["modulus"]

        return [
            f"a^2={a}^2={a_sq}",
            f"b^2={b}^2={b_sq}",
            f"a^2+b^2={a_sq}+{b_sq}={sum_sq}",
            f"\\sqrt{{{sum_sq}}}={self._format_modulus(modulus)}",
        ]

    def _format_modulus(self, modulus: float) -> str:
        """Format the modulus value cleanly.

        Args:
            modulus: The computed modulus.

        Returns:
            String representation, integer if exact.
        """
        if modulus == int(modulus):
            return str(int(modulus))
        return f"{modulus:.4f}".rstrip("0").rstrip(".")

    def _create_answer(self, data: dict) -> str:
        """Return the modulus value.

        Args:
            data: Solution data.

        Returns:
            String representation of the modulus.
        """
        return self._format_modulus(data["modulus"])


@register
class EulerFormulaGenerator(StepGenerator):
    """Evaluate Euler's formula e^{i*theta} = cos(theta) + i*sin(theta).

    Uses standard angles (0, pi/6, pi/4, pi/3, pi/2, pi) with known
    exact trigonometric values. Shows the formula substitution and
    evaluation of both cosine and sine components.

    Input format:
        ``evaluate euler formula``

    Target format:
        ``e^{i\\pi/4} <step> \\cos(\\pi/4)=\\frac{\\sqrt{2}}{2}
        <step> \\sin(\\pi/4)=\\frac{\\sqrt{2}}{2}
        <step> \\frac{\\sqrt{2}}{2}+\\frac{\\sqrt{2}}{2}i``

    Difficulty scaling:
        Difficulty 1-3: angles 0, pi/2, pi (simplest exact values).
        Difficulty 4-6: adds pi/4, pi/3.
        Difficulty 7-8: adds pi/6 (all six angles).

    Prerequisites:
        complex_arithmetic, exponentiation.

    Example:
        >>> gen = EulerFormulaGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'euler_formula'
    """

    _EASY_ANGLES: list[str] = ["0", "\\pi/2", "\\pi"]
    _MEDIUM_ANGLES: list[str] = ["0", "\\pi/4", "\\pi/3", "\\pi/2", "\\pi"]
    _HARD_ANGLES: list[str] = [
        "0", "\\pi/6", "\\pi/4", "\\pi/3", "\\pi/2", "\\pi",
    ]

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "euler_formula"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["complex_arithmetic", "exponentiation"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls angle selection.

        Returns:
            Natural language description.
        """
        return "evaluate euler formula"

    def _angle_pool(self, difficulty: int) -> list[str]:
        """Select the angle pool based on difficulty.

        Args:
            difficulty: Difficulty level.

        Returns:
            List of available angle labels.
        """
        if difficulty <= 3:
            return self._EASY_ANGLES
        if difficulty <= 6:
            return self._MEDIUM_ANGLES
        return self._HARD_ANGLES

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an Euler formula evaluation problem.

        Args:
            difficulty: Controls angle selection.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        table = AngleTable()
        pool = self._angle_pool(difficulty)
        angle = self._rng.choice(pool)
        cos_str = table.cos_str(angle)
        sin_str = table.sin_str(angle)

        problem = f"e^{{i{angle}}}"
        return problem, {
            "angle": angle, "cos_str": cos_str, "sin_str": sin_str,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate formula substitution steps.

        Args:
            data: Solution data with angle and trig values.

        Returns:
            Steps showing cos and sin evaluation.
        """
        angle = data["angle"]
        cos_str = data["cos_str"]
        sin_str = data["sin_str"]
        return [
            f"e^{{i\\theta}} = \\cos(\\theta) + i\\sin(\\theta)",
            f"\\cos({angle})={cos_str}",
            f"\\sin({angle})={sin_str}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the complex number result.

        Args:
            data: Solution data.

        Returns:
            LaTeX string for cos(theta) + i*sin(theta).
        """
        cos_str = data["cos_str"]
        sin_str = data["sin_str"]
        if sin_str == "0":
            return cos_str
        if cos_str == "0":
            return f"{sin_str}i"
        return f"{cos_str}+{sin_str}i"


@register
class QubitMeasureGenerator(StepGenerator):
    """Compute measurement probabilities for a single-qubit state.

    Generates a normalised qubit state a|0> + b|1> using simple
    fractional amplitudes (1/sqrt(2), 1/2, sqrt(3)/2) and computes
    P(0) = |a|^2 and P(1) = |b|^2. Shows the squaring of each
    amplitude and verifies normalisation.

    Input format:
        ``compute qubit measurement probabilities``

    Target format:
        ``|\\psi\\rangle = \\frac{1}{\\sqrt{2}}|0\\rangle +
        \\frac{1}{\\sqrt{2}}|1\\rangle <step>
        P(0) = |\\frac{1}{\\sqrt{2}}|^2 = \\frac{1}{2} <step>
        P(1) = |\\frac{1}{\\sqrt{2}}|^2 = \\frac{1}{2} <step>
        P(0)+P(1)=1 <step> P(0)=1/2, P(1)=1/2``

    Difficulty scaling:
        Difficulty 1-4: equal superposition (1/sqrt(2), 1/sqrt(2)).
        Difficulty 5-6: adds (1/2, sqrt(3)/2) pair.
        Difficulty 7-8: all valid amplitude pairs from the pool.

    Prerequisites:
        complex_modulus.

    Example:
        >>> gen = QubitMeasureGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'qubit_measure'
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "qubit_measure"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["complex_modulus"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls amplitude complexity.

        Returns:
            Natural language description.
        """
        return "compute qubit measurement probabilities"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a normalised qubit state and compute probabilities.

        Args:
            difficulty: Controls amplitude pair selection.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        qubit = self._sample_qubit(difficulty)
        problem = f"|\\psi\\rangle = {qubit.to_latex()}"
        return problem, {"qubit": qubit}

    def _sample_qubit(self, difficulty: int) -> QubitState:
        """Sample a valid normalised qubit state.

        Args:
            difficulty: Controls amplitude complexity.

        Returns:
            A QubitState instance with normalised amplitudes.
        """
        pairs = QubitState.valid_pairs()
        if difficulty <= 4:
            pairs = [p for p in pairs if p[0][1] == Fraction(1, 2)]
        elif difficulty <= 6:
            pairs = [
                p for p in pairs
                if p[0][1] in (Fraction(1, 2), Fraction(1, 4), Fraction(3, 4))
            ]
        chosen = self._rng.choice(pairs)
        return QubitState(
            chosen[0][0], chosen[1][0], chosen[0][1], chosen[1][1],
        )

    def _format_fraction(self, f: Fraction) -> str:
        """Format a Fraction as LaTeX.

        Args:
            f: Fraction to format.

        Returns:
            LaTeX string for the fraction.
        """
        if f.denominator == 1:
            return str(f.numerator)
        return f"\\frac{{{f.numerator}}}{{{f.denominator}}}"

    def _create_steps(self, data: dict) -> list[str]:
        """Generate amplitude squaring and normalisation steps.

        Args:
            data: Solution data with the qubit state.

        Returns:
            Steps showing P(0), P(1), and normalisation check.
        """
        qubit = data["qubit"]
        p0 = qubit.prob_zero()
        p1 = qubit.prob_one()
        total = p0 + p1

        return [
            f"P(0) = |{qubit.alpha_label}|^2 = {self._format_fraction(p0)}",
            f"P(1) = |{qubit.beta_label}|^2 = {self._format_fraction(p1)}",
            f"P(0)+P(1)={self._format_fraction(total)}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the measurement probabilities.

        Args:
            data: Solution data.

        Returns:
            String showing P(0) and P(1).
        """
        qubit = data["qubit"]
        p0_str = self._format_fraction(qubit.prob_zero())
        p1_str = self._format_fraction(qubit.prob_one())
        return f"P(0)={p0_str}, P(1)={p1_str}"


@register
class QuantumGateGenerator(StepGenerator):
    """Apply a quantum gate (Hadamard, Pauli-X, Pauli-Z) to a qubit.

    Generates a single-qubit state vector and a 2x2 quantum gate,
    then shows the matrix-vector multiplication step by step.
    Uses integer state vectors |0> = [1,0] and |1> = [0,1] for
    clean computation.

    Input format:
        ``apply quantum gate to qubit``

    Target format:
        ``H|0\\rangle <step> \\frac{1}{\\sqrt{2}}\\begin{pmatrix}
        1 & 1 \\\\ 1 & -1 \\end{pmatrix}\\begin{pmatrix}
        1 \\\\ 0 \\end{pmatrix} <step> c_{0}=1(1)+1(0)=1
        <step> c_{1}=1(1)+(-1)(0)=1 <step>
        \\frac{1}{\\sqrt{2}}\\begin{pmatrix} 1 \\\\ 1 \\end{pmatrix}``

    Difficulty scaling:
        Difficulty 1-3: Pauli-X gate (bit flip) on |0> or |1>.
        Difficulty 4-5: Pauli-Z gate (phase flip).
        Difficulty 6-8: Hadamard gate (superposition).

    Prerequisites:
        qubit_measure, matrix_multiply.

    Example:
        >>> gen = QuantumGateGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'quantum_gate'
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "quantum_gate"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["qubit_measure", "matrix_multiply"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls gate complexity.

        Returns:
            Natural language description.
        """
        return "apply quantum gate to qubit"

    def _select_gate(self, difficulty: int) -> QuantumGate:
        """Select a quantum gate based on difficulty.

        Args:
            difficulty: Difficulty level.

        Returns:
            A QuantumGate instance.
        """
        if difficulty <= 3:
            return QuantumGate("X", [[0, 1], [1, 0]])
        if difficulty <= 5:
            return QuantumGate("Z", [[1, 0], [0, -1]])
        return QuantumGate(
            "H", [[1, 1], [1, -1]], "\\frac{1}{\\sqrt{2}}",
        )

    def _select_input(self) -> tuple[list[int], str]:
        """Select an input basis state |0> or |1>.

        Returns:
            Tuple of (vector, ket_label).
        """
        if self._rng.random() < 0.5:
            return [1, 0], "|0\\rangle"
        return [0, 1], "|1\\rangle"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a gate application problem.

        Args:
            difficulty: Controls gate selection.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        gate = self._select_gate(difficulty)
        vector, ket = self._select_input()
        result = gate.apply_to(vector)

        problem = f"{gate.name}{ket}"
        return problem, {
            "gate": gate, "vector": vector, "ket": ket, "result": result,
        }

    def _format_vector(self, vec: list[int]) -> str:
        """Format a 2-element vector in LaTeX pmatrix notation.

        Args:
            vec: Two-element integer vector.

        Returns:
            LaTeX pmatrix string.
        """
        return f"\\begin{{pmatrix}} {vec[0]} \\\\ {vec[1]} \\end{{pmatrix}}"

    def _create_steps(self, data: dict) -> list[str]:
        """Generate matrix-vector multiplication steps.

        Args:
            data: Solution data with gate, vector, and result.

        Returns:
            Steps showing the gate matrix, each row computation, and result.
        """
        gate = data["gate"]
        vector = data["vector"]
        result = data["result"]

        steps = [
            f"{gate.matrix_latex()}{self._format_vector(vector)}",
            gate.step_row(0, vector),
            gate.step_row(1, vector),
        ]
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the resulting state vector.

        Args:
            data: Solution data.

        Returns:
            LaTeX string for the output state with scale factor.
        """
        gate = data["gate"]
        result = data["result"]
        vec_str = self._format_vector(result)
        if gate.scale_label == "1":
            return vec_str
        return f"{gate.scale_label}{vec_str}"
