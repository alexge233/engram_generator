"""Tier 8 generators — creative mathematics and abstraction.

Unlocks when Tier 0-7 tasks are mastered. These tasks test whether
the model understands mathematical STRUCTURE, not just procedures.
Solutions are verified by property checking: isomorphism detection,
cross-domain transfer, conjecture generation, complexity reduction,
problem transformation, analogy completion, equation construction,
and self-evaluation with trap detection.
"""
from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


class PolynomialFormatter:
    """Formats polynomial coefficient lists into LaTeX strings.

    Provides conversion from a list of coefficients (highest degree first)
    to a human-readable polynomial string with proper sign handling.

    Example:
        >>> f = PolynomialFormatter()
        >>> f.format([1, -2, 1])
        'x^2-2x+1'
        >>> f.format([2, 0, -12])
        '2x^2-12'
    """

    def format(self, coeffs: list[int]) -> str:
        """Format a coefficient list as a polynomial string.

        Args:
            coeffs: Coefficients from highest degree to constant.

        Returns:
            Formatted polynomial string.
        """
        degree = len(coeffs) - 1
        parts: list[str] = []
        for i, c in enumerate(coeffs):
            if c == 0:
                continue
            power = degree - i
            parts.append(self._format_term(c, power, is_first=(len(parts) == 0)))
        return "".join(parts) if parts else "0"

    def _format_term(self, coeff: int, power: int, is_first: bool) -> str:
        """Format a single polynomial term.

        Args:
            coeff: Coefficient value.
            power: Exponent of x.
            is_first: Whether this is the leading term.

        Returns:
            Formatted term string.
        """
        sign = self._sign_prefix(coeff, is_first)
        body = self._term_body(abs(coeff), power)
        return f"{sign}{body}"

    def _sign_prefix(self, coeff: int, is_first: bool) -> str:
        """Determine the sign prefix for a term.

        Args:
            coeff: Coefficient value.
            is_first: Whether this is the leading term.

        Returns:
            Sign string.
        """
        if is_first:
            return "-" if coeff < 0 else ""
        return "-" if coeff < 0 else "+"

    def _term_body(self, abs_coeff: int, power: int) -> str:
        """Format the body of a polynomial term.

        Args:
            abs_coeff: Absolute coefficient value.
            power: Exponent.

        Returns:
            Term body string.
        """
        if power == 0:
            return str(abs_coeff)
        if power == 1:
            return "x" if abs_coeff == 1 else f"{abs_coeff}x"
        if abs_coeff == 1:
            return f"x^{power}"
        return f"{abs_coeff}x^{power}"


class MappingVerifier:
    """Verifies structural mappings between mathematical expressions.

    Given a mapping of variable/operator substitutions, checks whether
    applying the mapping to one expression yields the other.

    Example:
        >>> v = MappingVerifier()
        >>> v.apply_mapping("2*x+3=7", {"x": "a", "*": "XOR"})
        '2 XOR a+3=7'
    """

    def apply_mapping(self, expression: str,
                      mapping: dict[str, str]) -> str:
        """Apply a symbol mapping to an expression string.

        Args:
            expression: Source expression.
            mapping: Dict of symbol replacements.

        Returns:
            Transformed expression.
        """
        result = expression
        for old, new in mapping.items():
            result = result.replace(old, new)
        return result

    def format_mapping(self, mapping: dict[str, str]) -> str:
        """Format a mapping as a readable string.

        Args:
            mapping: Dict of symbol replacements.

        Returns:
            Formatted mapping like 'x->a, *->XOR'.
        """
        parts = [f"{k}->{v}" for k, v in mapping.items()]
        return ", ".join(parts)


class FormulaEvaluator:
    """Evaluates simple formulas at integer points.

    Supports polynomial-like formulas defined by coefficient lists
    and provides batch evaluation for conjecture verification.

    Example:
        >>> e = FormulaEvaluator()
        >>> e.evaluate_polynomial([1, 0, -1], 3)
        8
    """

    def evaluate_polynomial(self, coeffs: list[int], x: int) -> int:
        """Evaluate a polynomial at a given x value.

        Args:
            coeffs: Coefficients from highest degree to constant.
            x: Point to evaluate at.

        Returns:
            Integer result of the evaluation.
        """
        result = 0
        for c in coeffs:
            result = result * x + c
        return result

    def evaluate_batch(self, coeffs: list[int],
                       points: list[int]) -> list[int]:
        """Evaluate a polynomial at multiple points.

        Args:
            coeffs: Coefficients from highest degree to constant.
            points: List of x values.

        Returns:
            List of evaluated results.
        """
        return [self.evaluate_polynomial(coeffs, x) for x in points]


@register
class IsomorphismDetectionGenerator(StepGenerator):
    """Identify shared structure between problems in different domains.

    Generates two problems that are structurally identical but use
    different operations or variable names. The model must identify
    the structural mapping between them. Verification: applying the
    mapping to one expression yields the other.

    Input format:
        ``identify the structural mapping between these problems``

    Target format:
        ``A: 2*x+3=7, B: 2*a+3=7 <step> identify variables: x->a
        <step> identify operations: same <step> mapping: x->a
        <step> verify: 2*a+3=7 matches B <step> x->a``

    Difficulty scaling:
        Difficulty 1-2: single variable rename.
        Difficulty 3-4: variable rename + constant shift.
        Difficulty 5-6: operator change (add<->multiply).
        Difficulty 7-8: multi-variable with operator change.

    Prerequisites:
        method_selection, generalise_sequence.

    Example:
        >>> gen = IsomorphismDetectionGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'isomorphism_detection'
    """

    _VARIABLE_PAIRS = [
        ("x", "a"), ("x", "t"), ("n", "k"), ("y", "m"), ("x", "p"),
    ]

    _OPERATOR_MAPS = [
        ("+", "XOR"), ("*", "AND"), ("+", "OR"), ("*", "shift"),
    ]

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "isomorphism_detection"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 8

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["method_selection", "generalise_sequence"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls mapping complexity.

        Returns:
            Natural language description.
        """
        return "identify the structural mapping between these problems"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate two structurally isomorphic problems.

        Args:
            difficulty: Controls mapping complexity.

        Returns:
            Tuple of (problem_pair_string, solution_data).
        """
        a_coeff = self._rng.randint(2, 5 + difficulty)
        b_const = self._rng.randint(1, 4 + difficulty)
        c_result = self._rng.randint(b_const + 1, b_const + 10 * difficulty)
        mapping = self._build_mapping(difficulty)
        expr_a = self._build_expression_a(a_coeff, b_const, c_result)
        expr_b = self._apply_mapping_to_expr(expr_a, mapping)
        problem = f"A: {expr_a}, B: {expr_b}"
        return problem, {
            "expr_a": expr_a, "expr_b": expr_b,
            "mapping": mapping, "a_coeff": a_coeff,
            "b_const": b_const, "c_result": c_result,
        }

    def _build_mapping(self, difficulty: int) -> dict[str, str]:
        """Build a structural mapping based on difficulty.

        Args:
            difficulty: Controls mapping complexity.

        Returns:
            Dict of symbol replacements.
        """
        var_pair = self._rng.choice(self._VARIABLE_PAIRS)
        mapping: dict[str, str] = {var_pair[0]: var_pair[1]}
        if difficulty >= 5:
            op_pair = self._rng.choice(self._OPERATOR_MAPS)
            mapping[op_pair[0]] = op_pair[1]
        return mapping

    def _build_expression_a(self, a: int, b: int, c: int) -> str:
        """Build the first expression in the pair.

        Args:
            a: Leading coefficient.
            b: Additive constant.
            c: Result value.

        Returns:
            Expression string like '2*x+3=7'.
        """
        return f"{a}*x+{b}={c}"

    def _apply_mapping_to_expr(self, expr: str,
                               mapping: dict[str, str]) -> str:
        """Apply a structural mapping to transform an expression.

        Args:
            expr: Source expression.
            mapping: Symbol replacements.

        Returns:
            Transformed expression.
        """
        verifier = MappingVerifier()
        return verifier.apply_mapping(expr, mapping)

    def _create_steps(self, data: dict) -> list[str]:
        """Generate mapping identification steps.

        Args:
            data: Solution data with expressions and mapping.

        Returns:
            Steps showing variable/operator identification and verification.
        """
        mapping = data["mapping"]
        verifier = MappingVerifier()
        steps: list[str] = []
        var_maps = {k: v for k, v in mapping.items() if k.isalpha()}
        op_maps = {k: v for k, v in mapping.items() if not k.isalpha()}
        steps.append(f"identify variables: {verifier.format_mapping(var_maps)}")
        if op_maps:
            steps.append(f"identify operations: {verifier.format_mapping(op_maps)}")
        else:
            steps.append("identify operations: same")
        steps.append(f"mapping: {verifier.format_mapping(mapping)}")
        verified = self._apply_mapping_to_expr(data["expr_a"], mapping)
        steps.append(f"verify: {verified} matches B")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the structural mapping.

        Args:
            data: Solution data.

        Returns:
            Mapping string like 'x->a'.
        """
        verifier = MappingVerifier()
        return verifier.format_mapping(data["mapping"])


@register
class CrossDomainTransferGenerator(StepGenerator):
    """Solve by mapping a problem to a different mathematical domain.

    Uses well-known equivalences between algebraic and geometric
    interpretations. E.g. sum 1+2+...+n maps to a triangle area
    yielding n(n+1)/2.

    Input format:
        ``solve by mapping to a different domain``

    Target format:
        ``\\text{sum}(1+2+...+n), n=10 <step> map to geometry:
        triangle with base n and height n+1 <step> area =
        n(n+1)/2 <step> 10*11/2=55 <step> 55``

    Difficulty scaling:
        Difficulty 1-2: arithmetic series (sum 1..n).
        Difficulty 3-4: sum of squares via geometry.
        Difficulty 5-6: sum of odd numbers via square area.
        Difficulty 7-8: combinatorial sums via paths.

    Prerequisites:
        generalise_sequence, derive_formula.

    Example:
        >>> gen = CrossDomainTransferGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'cross_domain_transfer'
    """

    _PROBLEM_TYPES = {
        1: "arithmetic_series", 2: "arithmetic_series",
        3: "sum_squares", 4: "sum_squares",
        5: "sum_odds", 6: "sum_odds",
        7: "triangular_paths", 8: "triangular_paths",
    }

    _N_RANGES = {
        1: (5, 10), 2: (8, 15), 3: (3, 7), 4: (4, 8),
        5: (3, 8), 6: (5, 10), 7: (3, 6), 8: (4, 8),
    }

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "cross_domain_transfer"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 8

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["generalise_sequence", "derive_formula"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls problem type.

        Returns:
            Natural language description.
        """
        return "solve by mapping to a different domain"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a problem solvable via domain transfer with randomised type.

        Args:
            difficulty: Controls problem type and parameter range.

        Returns:
            Tuple of (problem_string, solution_data).
        """
        # Allow any problem type (not just fixed per difficulty) for variety
        available_types = list(self._PROBLEM_TYPES.values())
        if difficulty <= 3:
            available_types = available_types[:4]
        problem_type = self._rng.choice(available_types)
        lo, hi = self._N_RANGES.get(difficulty, (5, 10))
        n = self._rng.randint(lo, hi + difficulty)
        builder = self._get_builder(problem_type)
        return builder(n)

    def _get_builder(self, problem_type: str):
        """Return the builder method for the given problem type.

        Args:
            problem_type: Type identifier string.

        Returns:
            Builder method.
        """
        builders = {
            "arithmetic_series": self._build_arithmetic_series,
            "sum_squares": self._build_sum_squares,
            "sum_odds": self._build_sum_odds,
            "triangular_paths": self._build_triangular_paths,
        }
        return builders[problem_type]

    def _build_arithmetic_series(self, n: int) -> tuple[str, dict]:
        """Build an arithmetic series problem.

        Args:
            n: Upper limit of the sum.

        Returns:
            Tuple of (problem_string, solution_data).
        """
        result = n * (n + 1) // 2
        return f"\\text{{sum}}(1+2+...+{n})", {
            "type": "arithmetic_series", "n": n, "result": result,
            "domain": "geometry", "formula": "n(n+1)/2",
            "interpretation": f"triangle with base {n} and height {n + 1}",
        }

    def _build_sum_squares(self, n: int) -> tuple[str, dict]:
        """Build a sum-of-squares problem.

        Args:
            n: Upper limit of the sum.

        Returns:
            Tuple of (problem_string, solution_data).
        """
        result = n * (n + 1) * (2 * n + 1) // 6
        return f"\\text{{sum}}(1^2+2^2+...+{n}^2)", {
            "type": "sum_squares", "n": n, "result": result,
            "domain": "geometry", "formula": "n(n+1)(2n+1)/6",
            "interpretation": f"stacked squares forming pyramid of height {n}",
        }

    def _build_sum_odds(self, n: int) -> tuple[str, dict]:
        """Build a sum-of-odds problem.

        Args:
            n: Number of odd terms.

        Returns:
            Tuple of (problem_string, solution_data).
        """
        result = n * n
        return f"\\text{{sum}}(1+3+5+...+{2 * n - 1})", {
            "type": "sum_odds", "n": n, "result": result,
            "domain": "geometry", "formula": "n^2",
            "interpretation": f"square of side {n} built from L-shaped strips",
        }

    def _build_triangular_paths(self, n: int) -> tuple[str, dict]:
        """Build a triangular path counting problem.

        Args:
            n: Grid size parameter.

        Returns:
            Tuple of (problem_string, solution_data).
        """
        result = 1
        for i in range(1, n + 1):
            result = result * (n + i) // i
        return f"\\text{{paths}}({n} \\times {n} \\text{{ grid}})", {
            "type": "triangular_paths", "n": n, "result": result,
            "domain": "combinatorics", "formula": "C(2n,n)",
            "interpretation": f"choosing {n} right-moves from {2 * n} total moves",
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate domain mapping and evaluation steps.

        Args:
            data: Solution data with domain and formula info.

        Returns:
            Steps showing the domain mapping and computation.
        """
        n = data["n"]
        return [
            f"map to {data['domain']}: {data['interpretation']}",
            f"formula = {data['formula']}",
            f"evaluate at n={n}: {data['result']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the computed result.

        Args:
            data: Solution data.

        Returns:
            String representation of the result.
        """
        return str(data["result"])


@register
class ConjectureGenerationGenerator(StepGenerator):
    """Observe data pairs and propose a formula that fits.

    Generates input-output pairs from a hidden polynomial formula.
    The model must guess the formula. Verification is done at unseen
    test points.

    Input format:
        ``propose a formula from observations``

    Target format:
        ``f(1)=3, f(2)=7, f(3)=13, f(4)=21 <step> differences:
        4,6,8 <step> second differences: 2,2 (constant) <step>
        degree 2 polynomial <step> f(x)=x^2+x+1 <step> verify:
        f(5)=31, f(6)=43 <step> x^2+x+1``

    Difficulty scaling:
        Difficulty 1-2: linear formulas (degree 1).
        Difficulty 3-4: quadratic formulas (degree 2).
        Difficulty 5-6: cubic formulas (degree 3).
        Difficulty 7-8: degree 3 with larger coefficients.

    Prerequisites:
        generalise_sequence.

    Example:
        >>> gen = ConjectureGenerationGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'conjecture_generation'
    """

    _DEGREE_MAP = {
        1: 1, 2: 1, 3: 2, 4: 2, 5: 3, 6: 3, 7: 3, 8: 3,
    }

    _COEFF_RANGES = {
        1: (1, 3), 2: (1, 4), 3: (1, 3), 4: (1, 4),
        5: (1, 3), 6: (1, 4), 7: (1, 5), 8: (2, 6),
    }

    _NUM_EXAMPLES = {
        1: 3, 2: 4, 3: 4, 4: 5, 5: 5, 6: 5, 7: 5, 8: 6,
    }

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "conjecture_generation"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 8

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["generalise_sequence"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls formula complexity.

        Returns:
            Natural language description.
        """
        return "propose a formula from observations"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate observed data pairs from a hidden formula.

        Args:
            difficulty: Controls polynomial degree and coefficient range.

        Returns:
            Tuple of (observations_string, solution_data).
        """
        degree = self._DEGREE_MAP.get(difficulty, 2)
        coeffs = self._generate_coefficients(difficulty, degree)
        evaluator = FormulaEvaluator()
        num_examples = self._NUM_EXAMPLES.get(difficulty, 4)
        inputs = list(range(1, num_examples + 1))
        outputs = evaluator.evaluate_batch(coeffs, inputs)
        test_inputs = list(range(num_examples + 1, num_examples + 3))
        test_outputs = evaluator.evaluate_batch(coeffs, test_inputs)
        observations = ", ".join(
            f"f({x})={y}" for x, y in zip(inputs, outputs)
        )
        return observations, {
            "coeffs": coeffs, "degree": degree,
            "inputs": inputs, "outputs": outputs,
            "test_inputs": test_inputs, "test_outputs": test_outputs,
        }

    def _generate_coefficients(self, difficulty: int,
                               degree: int) -> list[int]:
        """Generate random polynomial coefficients.

        Args:
            difficulty: Controls coefficient magnitude.
            degree: Polynomial degree.

        Returns:
            Coefficient list from highest degree to constant.
        """
        lo, hi = self._COEFF_RANGES.get(difficulty, (1, 4))
        coeffs: list[int] = []
        for i in range(degree + 1):
            c = self._rng.randint(lo, hi)
            if i > 0 and self._rng.random() < 0.3:
                c = -c
            coeffs.append(c)
        return coeffs

    def _create_steps(self, data: dict) -> list[str]:
        """Generate conjecture derivation steps.

        Args:
            data: Solution data with coefficients and test data.

        Returns:
            Steps showing difference analysis, degree, formula, verification.
        """
        steps: list[str] = []
        steps.append(self._differences_step(data["outputs"]))
        steps.append(f"degree {data['degree']} polynomial")
        formatter = PolynomialFormatter()
        formula = formatter.format(data["coeffs"])
        steps.append(f"f(x)={formula}")
        verifications = ", ".join(
            f"f({x})={y}"
            for x, y in zip(data["test_inputs"], data["test_outputs"])
        )
        steps.append(f"verify: {verifications}")
        return steps

    def _differences_step(self, outputs: list[int]) -> str:
        """Compute first differences from output values.

        Args:
            outputs: List of observed output values.

        Returns:
            Step string showing the differences.
        """
        diffs = [outputs[i + 1] - outputs[i] for i in range(len(outputs) - 1)]
        diffs_str = ",".join(str(d) for d in diffs)
        return f"differences: {diffs_str}"

    def _create_answer(self, data: dict) -> str:
        """Return the conjectured formula.

        Args:
            data: Solution data.

        Returns:
            Polynomial formula string.
        """
        formatter = PolynomialFormatter()
        return formatter.format(data["coeffs"])


@register
class ComplexityReductionGenerator(StepGenerator):
    """Simplify a verbose solution to fewer steps.

    Presents a correct but long-form expansion (e.g. expanding (x+a)^n
    term by term) and the model must find a shorter computational path
    to the same answer.

    Input format:
        ``simplify this solution to fewer steps``

    Target format:
        ``verbose: (x+1)^2 = x*x + x*1 + 1*x + 1*1 = x^2+2x+1
        (4 multiplications) <step> identify pattern: perfect square
        <step> short: a^2+2ab+b^2 with a=x, b=1 <step>
        x^2+2(1)x+1=x^2+2x+1 <step> 2 steps vs 4 <step> x^2+2x+1``

    Difficulty scaling:
        Difficulty 1-2: (x+a)^2 expansion.
        Difficulty 3-4: (x+a)^3 expansion.
        Difficulty 5-6: difference of squares a^2-b^2.
        Difficulty 7-8: sum/difference of cubes.

    Prerequisites:
        method_selection, derive_formula.

    Example:
        >>> gen = ComplexityReductionGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'complexity_reduction'
    """

    _PATTERN_TYPES = {
        1: "perfect_square", 2: "perfect_square",
        3: "perfect_cube", 4: "perfect_cube",
        5: "difference_of_squares", 6: "difference_of_squares",
        7: "sum_of_cubes", 8: "difference_of_cubes",
    }

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "complexity_reduction"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 8

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["method_selection", "derive_formula"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls pattern complexity.

        Returns:
            Natural language description.
        """
        return "simplify this solution to fewer steps"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a verbose solution and its shorter alternative.

        Args:
            difficulty: Controls which algebraic pattern is used.

        Returns:
            Tuple of (verbose_solution_string, solution_data).
        """
        pattern = self._PATTERN_TYPES.get(difficulty, "perfect_square")
        a = self._rng.randint(1, 3 + difficulty)
        b = self._rng.randint(1, 2 + difficulty // 2)
        builder = self._get_pattern_builder(pattern)
        return builder(a, b)

    def _get_pattern_builder(self, pattern: str):
        """Return the builder method for the given pattern type.

        Args:
            pattern: Pattern identifier string.

        Returns:
            Builder method.
        """
        builders = {
            "perfect_square": self._build_perfect_square,
            "perfect_cube": self._build_perfect_cube,
            "difference_of_squares": self._build_diff_squares,
            "sum_of_cubes": self._build_sum_cubes,
            "difference_of_cubes": self._build_diff_cubes,
        }
        return builders[pattern]

    def _build_perfect_square(self, a: int, b: int) -> tuple[str, dict]:
        """Build a perfect square expansion problem.

        Args:
            a: Coefficient of x.
            b: Constant term.

        Returns:
            Tuple of (verbose_string, solution_data).
        """
        result = f"{a * a}x^2+{2 * a * b}x+{b * b}"
        verbose_steps = 4
        short_steps = 2
        verbose = (
            f"({a}x+{b})^2 expanded term by term: "
            f"{a}x*{a}x + {a}x*{b} + {b}*{a}x + {b}*{b} "
            f"({verbose_steps} multiplications)"
        )
        return verbose, {
            "pattern": "perfect_square", "a": a, "b": b,
            "identity": "a^2+2ab+b^2",
            "result": result, "verbose_steps": verbose_steps,
            "short_steps": short_steps,
        }

    def _build_perfect_cube(self, a: int, b: int) -> tuple[str, dict]:
        """Build a perfect cube expansion problem.

        Args:
            a: Coefficient of x.
            b: Constant term.

        Returns:
            Tuple of (verbose_string, solution_data).
        """
        a3 = a ** 3
        a2b = 3 * a * a * b
        ab2 = 3 * a * b * b
        b3 = b ** 3
        result = f"{a3}x^3+{a2b}x^2+{ab2}x+{b3}"
        verbose = (
            f"({a}x+{b})^3 expanded fully: "
            f"({a}x+{b})*({a}x+{b})*({a}x+{b}) (9 multiplications)"
        )
        return verbose, {
            "pattern": "perfect_cube", "a": a, "b": b,
            "identity": "a^3+3a^2b+3ab^2+b^3",
            "result": result, "verbose_steps": 9, "short_steps": 3,
        }

    def _build_diff_squares(self, a: int, b: int) -> tuple[str, dict]:
        """Build a difference of squares problem.

        Args:
            a: First value.
            b: Second value.

        Returns:
            Tuple of (verbose_string, solution_data).
        """
        result_val = a * a - b * b
        verbose = (
            f"{a}^2-{b}^2 computed as {a}*{a}-{b}*{b}={a*a}-{b*b} "
            f"(2 multiplications + 1 subtraction)"
        )
        return verbose, {
            "pattern": "difference_of_squares", "a": a, "b": b,
            "identity": "(a+b)(a-b)",
            "result": str(result_val), "verbose_steps": 3, "short_steps": 2,
            "factored": f"({a}+{b})({a}-{b})={a + b}*{a - b}={result_val}",
        }

    def _build_sum_cubes(self, a: int, b: int) -> tuple[str, dict]:
        """Build a sum of cubes problem.

        Args:
            a: First value.
            b: Second value.

        Returns:
            Tuple of (verbose_string, solution_data).
        """
        result_val = a ** 3 + b ** 3
        verbose = (
            f"{a}^3+{b}^3 computed as {a}*{a}*{a}+{b}*{b}*{b} "
            f"(4 multiplications + 1 addition)"
        )
        return verbose, {
            "pattern": "sum_of_cubes", "a": a, "b": b,
            "identity": "(a+b)(a^2-ab+b^2)",
            "result": str(result_val), "verbose_steps": 5, "short_steps": 3,
        }

    def _build_diff_cubes(self, a: int, b: int) -> tuple[str, dict]:
        """Build a difference of cubes problem.

        Args:
            a: First value.
            b: Second value.

        Returns:
            Tuple of (verbose_string, solution_data).
        """
        result_val = a ** 3 - b ** 3
        verbose = (
            f"{a}^3-{b}^3 computed as {a}*{a}*{a}-{b}*{b}*{b} "
            f"(4 multiplications + 1 subtraction)"
        )
        return verbose, {
            "pattern": "difference_of_cubes", "a": a, "b": b,
            "identity": "(a-b)(a^2+ab+b^2)",
            "result": str(result_val), "verbose_steps": 5, "short_steps": 3,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate complexity reduction steps.

        Args:
            data: Solution data with pattern and identity info.

        Returns:
            Steps showing pattern identification and shorter path.
        """
        steps: list[str] = [
            f"identify pattern: {data['pattern']}",
            f"apply identity: {data['identity']}",
            f"with a={data['a']}, b={data['b']}",
            f"{data['short_steps']} steps vs {data['verbose_steps']}",
        ]
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the simplified result.

        Args:
            data: Solution data.

        Returns:
            Result string.
        """
        return data["result"]


@register
class ProblemTransformationGenerator(StepGenerator):
    """Rewrite a problem into an easier-to-solve form.

    Presents a problem that can be simplified via substitution
    (e.g. u=x^2 reduces a quartic to a quadratic). Shows the
    transformation and solves the easier version.

    Input format:
        ``transform this problem into an easier form``

    Target format:
        ``x^4-5x^2+4=0 <step> substitute u=x^2 <step>
        u^2-5u+4=0 <step> (u-4)(u-1)=0, u=4 or u=1 <step>
        x^2=4: x=2,-2 <step> x^2=1: x=1,-1 <step> 2,-2,1,-1``

    Difficulty scaling:
        Difficulty 1-2: biquadratic (x^4 -> u=x^2).
        Difficulty 3-4: exponential substitution (4^x -> u=2^x).
        Difficulty 5-6: trigonometric identity substitution.
        Difficulty 7-8: nested radical via squaring.

    Prerequisites:
        quadratic, method_selection.

    Example:
        >>> gen = ProblemTransformationGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'problem_transformation'
    """

    _TRANSFORM_TYPES = {
        1: "biquadratic", 2: "biquadratic",
        3: "exponential", 4: "exponential",
        5: "reciprocal", 6: "reciprocal",
        7: "nested_square", 8: "nested_square",
    }

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "problem_transformation"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 8

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["quadratic", "method_selection"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls transformation type.

        Returns:
            Natural language description.
        """
        return "transform this problem into an easier form"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a problem requiring substitution to solve.

        Args:
            difficulty: Controls transformation type.

        Returns:
            Tuple of (original_problem_string, solution_data).
        """
        transform_type = self._TRANSFORM_TYPES.get(difficulty, "biquadratic")
        builder = self._get_transform_builder(transform_type)
        return builder(difficulty)

    def _get_transform_builder(self, transform_type: str):
        """Return the builder method for the given transformation type.

        Args:
            transform_type: Transformation identifier.

        Returns:
            Builder method.
        """
        builders = {
            "biquadratic": self._build_biquadratic,
            "exponential": self._build_exponential,
            "reciprocal": self._build_reciprocal,
            "nested_square": self._build_nested_square,
        }
        return builders[transform_type]

    def _build_biquadratic(self, difficulty: int) -> tuple[str, dict]:
        """Build a biquadratic equation solvable via u=x^2.

        Args:
            difficulty: Controls root magnitudes.

        Returns:
            Tuple of (problem_string, solution_data).
        """
        u1 = self._rng.randint(1, 2 + difficulty)
        u2 = self._rng.randint(u1 + 1, u1 + 2 + difficulty)
        b = -(u1 + u2)
        c = u1 * u2
        problem = f"x^4+{b}x^2+{c}=0"
        solutions = sorted(set(
            [int(u1 ** 0.5), -int(u1 ** 0.5),
             int(u2 ** 0.5), -int(u2 ** 0.5)]
        ))
        return problem, {
            "type": "biquadratic", "substitution": "u=x^2",
            "reduced": f"u^2+{b}u+{c}=0",
            "u_solutions": [u1, u2], "solutions": solutions,
            "b": b, "c": c,
        }

    def _build_exponential(self, difficulty: int) -> tuple[str, dict]:
        """Build an exponential equation solvable via u=2^x.

        Args:
            difficulty: Controls coefficient magnitudes.

        Returns:
            Tuple of (problem_string, solution_data).
        """
        x1 = self._rng.randint(1, 2 + difficulty // 2)
        x2 = self._rng.randint(x1 + 1, x1 + 2)
        u1 = 2 ** x1
        u2 = 2 ** x2
        b = -(u1 + u2)
        c = u1 * u2
        problem = f"4^x+{b}*2^x+{c}=0"
        return problem, {
            "type": "exponential", "substitution": "u=2^x",
            "reduced": f"u^2+{b}u+{c}=0",
            "u_solutions": [u1, u2], "solutions": [x1, x2],
            "b": b, "c": c,
        }

    def _build_reciprocal(self, difficulty: int) -> tuple[str, dict]:
        """Build a reciprocal equation solvable via u=x+1/x.

        Args:
            difficulty: Controls parameter values.

        Returns:
            Tuple of (problem_string, solution_data).
        """
        target_sum = self._rng.randint(2, 3 + difficulty)
        problem = f"x+\\frac{{1}}{{x}}={target_sum}"
        discriminant = target_sum * target_sum - 4
        return problem, {
            "type": "reciprocal", "substitution": "multiply by x",
            "reduced": f"x^2-{target_sum}x+1=0",
            "target_sum": target_sum, "discriminant": discriminant,
            "solutions": [f"({target_sum}+sqrt({discriminant}))/2",
                          f"({target_sum}-sqrt({discriminant}))/2"],
        }

    def _build_nested_square(self, difficulty: int) -> tuple[str, dict]:
        """Build a nested square root equation solvable by squaring.

        Args:
            difficulty: Controls coefficient values.

        Returns:
            Tuple of (problem_string, solution_data).
        """
        x_val = self._rng.randint(2, 4 + difficulty)
        inner = x_val * x_val
        a = self._rng.randint(1, 3)
        radicand = inner + a
        problem = f"\\sqrt{{{radicand}-x^2}}={a}"
        return problem, {
            "type": "nested_square", "substitution": "square both sides",
            "reduced": f"{radicand}-x^2={a * a}",
            "solutions": [x_val, -x_val] if x_val != 0 else [0],
            "radicand": radicand, "a": a,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate transformation and solution steps.

        Args:
            data: Solution data with substitution info.

        Returns:
            Steps showing substitution, reduced form, and back-substitution.
        """
        steps: list[str] = [
            f"substitute: {data['substitution']}",
            f"reduced form: {data['reduced']}",
        ]
        if "u_solutions" in data:
            u_str = ", ".join(str(u) for u in data["u_solutions"])
            steps.append(f"solve reduced: u={u_str}")
        sol_str = ", ".join(str(s) for s in data["solutions"])
        steps.append(f"back-substitute: {sol_str}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the solutions to the original problem.

        Args:
            data: Solution data.

        Returns:
            Comma-separated solution values.
        """
        return ",".join(str(s) for s in data["solutions"])


@register
class AnalogCompletionGenerator(StepGenerator):
    """Complete mathematical analogies of the form A:B :: C:?.

    Generates analogies where the relationship between A and B must be
    identified and applied to C to produce the answer. Covers numerical,
    algebraic, and structural analogies.

    Input format:
        ``complete the mathematical analogy``

    Target format:
        ``2:4 :: 3:? <step> identify relationship: squaring (2^2=4)
        <step> apply to 3: 3^2=9 <step> 9``

    Difficulty scaling:
        Difficulty 1-2: squaring/cubing relationships.
        Difficulty 3-4: factorial or doubling relationships.
        Difficulty 5-6: polynomial evaluation relationships.
        Difficulty 7-8: inverse operation relationships.

    Prerequisites:
        generalise_sequence.

    Example:
        >>> gen = AnalogCompletionGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'analogy_completion'
    """

    _RELATION_TYPES = {
        1: "squaring", 2: "squaring",
        3: "cubing", 4: "factorial",
        5: "polynomial", 6: "polynomial",
        7: "inverse", 8: "inverse",
    }

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "analogy_completion"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 8

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["generalise_sequence"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls relationship complexity.

        Returns:
            Natural language description.
        """
        return "complete the mathematical analogy"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a mathematical analogy problem.

        Args:
            difficulty: Controls the type of relationship.

        Returns:
            Tuple of (analogy_string, solution_data).
        """
        relation = self._RELATION_TYPES.get(difficulty, "squaring")
        builder = self._get_relation_builder(relation)
        return builder(difficulty)

    def _get_relation_builder(self, relation: str):
        """Return the builder method for the given relation type.

        Args:
            relation: Relationship identifier string.

        Returns:
            Builder method.
        """
        builders = {
            "squaring": self._build_squaring,
            "cubing": self._build_cubing,
            "factorial": self._build_factorial,
            "polynomial": self._build_polynomial,
            "inverse": self._build_inverse,
        }
        return builders[relation]

    def _build_squaring(self, difficulty: int) -> tuple[str, dict]:
        """Build a squaring analogy: a:a^2 :: c:c^2.

        Args:
            difficulty: Controls operand size.

        Returns:
            Tuple of (analogy_string, solution_data).
        """
        a = self._rng.randint(2, 5 + difficulty)
        c = self._rng.randint(a + 1, a + 5)
        return f"{a}:{a**2} :: {c}:?", {
            "relation": "squaring", "description": f"x^2",
            "a": a, "b": a ** 2, "c": c, "answer": c ** 2,
        }

    def _build_cubing(self, difficulty: int) -> tuple[str, dict]:
        """Build a cubing analogy: a:a^3 :: c:c^3.

        Args:
            difficulty: Controls operand size.

        Returns:
            Tuple of (analogy_string, solution_data).
        """
        a = self._rng.randint(2, 4)
        c = self._rng.randint(a + 1, a + 3)
        return f"{a}:{a**3} :: {c}:?", {
            "relation": "cubing", "description": f"x^3",
            "a": a, "b": a ** 3, "c": c, "answer": c ** 3,
        }

    def _build_factorial(self, difficulty: int) -> tuple[str, dict]:
        """Build a factorial analogy: a:a! :: c:c!.

        Args:
            difficulty: Controls operand size.

        Returns:
            Tuple of (analogy_string, solution_data).
        """
        a = self._rng.randint(3, 5)
        c = self._rng.randint(a + 1, a + 2)
        a_fact = self._factorial(a)
        c_fact = self._factorial(c)
        return f"{a}:{a_fact} :: {c}:?", {
            "relation": "factorial", "description": "x!",
            "a": a, "b": a_fact, "c": c, "answer": c_fact,
        }

    def _build_polynomial(self, difficulty: int) -> tuple[str, dict]:
        """Build a polynomial evaluation analogy.

        Args:
            difficulty: Controls polynomial complexity.

        Returns:
            Tuple of (analogy_string, solution_data).
        """
        coeff = self._rng.randint(2, 4)
        const = self._rng.randint(1, 5)
        a = self._rng.randint(2, 5)
        c = self._rng.randint(a + 1, a + 4)
        b_val = coeff * a + const
        answer = coeff * c + const
        return f"{a}:{b_val} :: {c}:?", {
            "relation": "polynomial",
            "description": f"{coeff}x+{const}",
            "a": a, "b": b_val, "c": c, "answer": answer,
        }

    def _build_inverse(self, difficulty: int) -> tuple[str, dict]:
        """Build an inverse operation analogy.

        Args:
            difficulty: Controls operand complexity.

        Returns:
            Tuple of (analogy_string, solution_data).
        """
        a = self._rng.randint(2, 6 + difficulty)
        b = a * a
        c = self._rng.randint(a + 1, a + 5)
        d = c * c
        return f"{b}:{a} :: {d}:?", {
            "relation": "inverse", "description": "sqrt(x)",
            "a": b, "b": a, "c": d, "answer": c,
        }

    def _factorial(self, n: int) -> int:
        """Compute n factorial.

        Args:
            n: Non-negative integer.

        Returns:
            n! value.
        """
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result

    def _create_steps(self, data: dict) -> list[str]:
        """Generate analogy reasoning steps.

        Args:
            data: Solution data with relationship info.

        Returns:
            Steps showing relationship identification and application.
        """
        return [
            f"identify relationship: {data['relation']} ({data['description']})",
            f"verify: {data['a']} -> {data['b']}",
            f"apply to {data['c']}: {data['answer']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the analogy completion.

        Args:
            data: Solution data.

        Returns:
            String representation of the answer.
        """
        return str(data["answer"])


@register
class EquationConstructionGenerator(StepGenerator):
    """Build an equation from specified roots and properties.

    Given roots and a leading coefficient, constructs the polynomial
    equation by multiplying factors. Verification: evaluate at stated
    roots (should yield zero) and check leading coefficient.

    Input format:
        ``construct equation with these properties``

    Target format:
        ``roots: 3,-2; leading coefficient: 2 <step>
        factors: (x-3)(x+2) <step> expand: x^2-x-6 <step>
        multiply by 2: 2x^2-2x-12 <step> verify: 2(3)^2-2(3)-12=0
        <step> 2x^2-2x-12``

    Difficulty scaling:
        Difficulty 1-2: 2 integer roots, leading coeff 1.
        Difficulty 3-4: 2 integer roots, leading coeff 2-3.
        Difficulty 5-6: 3 integer roots, leading coeff 1-2.
        Difficulty 7-8: 3 integer roots, leading coeff 2-4.

    Prerequisites:
        polynomial_multiply, quadratic.

    Example:
        >>> gen = EquationConstructionGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'equation_construction'
    """

    _NUM_ROOTS = {
        1: 2, 2: 2, 3: 2, 4: 2, 5: 3, 6: 3, 7: 3, 8: 3,
    }

    _LEAD_COEFF_RANGES = {
        1: (1, 1), 2: (1, 1), 3: (2, 3), 4: (2, 3),
        5: (1, 2), 6: (1, 2), 7: (2, 4), 8: (2, 4),
    }

    _ROOT_RANGES = {
        1: (-3, 3), 2: (-4, 4), 3: (-5, 5), 4: (-5, 5),
        5: (-4, 4), 6: (-5, 5), 7: (-6, 6), 8: (-7, 7),
    }

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "equation_construction"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 8

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["polynomial_multiply", "quadratic"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls root count and coefficient range.

        Returns:
            Natural language description.
        """
        return "construct equation with these properties"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate equation construction specifications.

        Args:
            difficulty: Controls number of roots and leading coefficient.

        Returns:
            Tuple of (specification_string, solution_data).
        """
        num_roots = self._NUM_ROOTS.get(difficulty, 2)
        roots = self._generate_roots(difficulty, num_roots)
        lead_lo, lead_hi = self._LEAD_COEFF_RANGES.get(difficulty, (1, 2))
        lead_coeff = self._rng.randint(lead_lo, lead_hi)
        coeffs = self._compute_polynomial(roots, lead_coeff)
        roots_str = ",".join(str(r) for r in roots)
        problem = f"roots: {roots_str}; leading coefficient: {lead_coeff}"
        return problem, {
            "roots": roots, "lead_coeff": lead_coeff,
            "coeffs": coeffs, "num_roots": num_roots,
        }

    def _generate_roots(self, difficulty: int, num_roots: int) -> list[int]:
        """Generate distinct integer roots.

        Args:
            difficulty: Controls root magnitude range.
            num_roots: Number of roots to generate.

        Returns:
            List of distinct integer roots.
        """
        lo, hi = self._ROOT_RANGES.get(difficulty, (-4, 4))
        roots: list[int] = []
        attempts = 0
        while len(roots) < num_roots and attempts < 100:
            r = self._rng.randint(lo, hi)
            if r != 0 and r not in roots:
                roots.append(r)
            attempts += 1
        return sorted(roots)

    def _compute_polynomial(self, roots: list[int],
                            lead_coeff: int) -> list[int]:
        """Compute polynomial coefficients from roots and leading coefficient.

        Args:
            roots: List of roots.
            lead_coeff: Leading coefficient.

        Returns:
            Coefficient list from highest degree to constant.
        """
        poly = [1, -roots[0]]
        for r in roots[1:]:
            poly = self._multiply_by_factor(poly, r)
        return [c * lead_coeff for c in poly]

    def _multiply_by_factor(self, poly: list[int], root: int) -> list[int]:
        """Multiply a polynomial by (x - root).

        Args:
            poly: Current polynomial coefficients.
            root: Root of the new factor.

        Returns:
            New polynomial coefficients.
        """
        new_poly = [0] * (len(poly) + 1)
        for i, c in enumerate(poly):
            new_poly[i] += c
            new_poly[i + 1] += c * (-root)
        return new_poly

    def _create_steps(self, data: dict) -> list[str]:
        """Generate construction and verification steps.

        Args:
            data: Solution data with roots and coefficients.

        Returns:
            Steps showing factor construction, expansion, and verification.
        """
        roots = data["roots"]
        lead_coeff = data["lead_coeff"]
        coeffs = data["coeffs"]
        factors = self._format_factors(roots)
        steps: list[str] = [f"factors: {factors}"]
        formatter = PolynomialFormatter()
        monic = self._compute_polynomial(roots, 1)
        monic_str = formatter.format(monic)
        steps.append(f"expand: {monic_str}")
        if lead_coeff != 1:
            poly_str = formatter.format(coeffs)
            steps.append(f"multiply by {lead_coeff}: {poly_str}")
        verification = self._verify_at_root(coeffs, roots[0])
        steps.append(f"verify at x={roots[0]}: {verification}=0")
        return steps

    def _format_factors(self, roots: list[int]) -> str:
        """Format roots as linear factors.

        Args:
            roots: List of roots.

        Returns:
            Factor string like '(x-3)(x+2)'.
        """
        parts: list[str] = []
        for r in roots:
            if r >= 0:
                parts.append(f"(x-{r})")
            else:
                parts.append(f"(x+{-r})")
        return "".join(parts)

    def _verify_at_root(self, coeffs: list[int], root: int) -> str:
        """Format the verification of the polynomial at a root.

        Args:
            coeffs: Polynomial coefficients.
            root: Root to verify.

        Returns:
            Verification string showing the computation.
        """
        evaluator = FormulaEvaluator()
        result = evaluator.evaluate_polynomial(coeffs, root)
        formatter = PolynomialFormatter()
        poly_str = formatter.format(coeffs)
        return f"{poly_str} at x={root} = {result}"

    def _create_answer(self, data: dict) -> str:
        """Return the constructed polynomial.

        Args:
            data: Solution data.

        Returns:
            Polynomial string.
        """
        formatter = PolynomialFormatter()
        return formatter.format(data["coeffs"])


@register
class SelfEvaluationGenerator(StepGenerator):
    """Solve a problem and assess confidence in the solution.

    Presents problems that are either straightforward (high confidence
    warranted) or contain subtle traps (division by zero, extraneous
    solutions). The model must solve AND correctly identify whether
    the problem has a trap.

    Input format:
        ``solve and rate your confidence``

    Target format:
        ``\\frac{x^2-4}{x-2}=x+2 <step> simplify: x+2=x+2 <step>
        identity: true for all x <step> TRAP: x=2 makes
        denominator 0 <step> solution: all x except x=2 <step>
        confidence: low (trap detected) <step> x != 2``

    Difficulty scaling:
        Difficulty 1-2: linear equations (clean or with 0-division trap).
        Difficulty 3-4: quadratics (clean or extraneous root).
        Difficulty 5-6: rational equations (clean or domain restriction).
        Difficulty 7-8: radical equations (clean or sign error trap).

    Prerequisites:
        error_detection, estimate_magnitude.

    Example:
        >>> gen = SelfEvaluationGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'self_evaluation'
    """

    _PROBLEM_LEVELS = {
        1: "linear", 2: "linear",
        3: "quadratic", 4: "quadratic",
        5: "rational", 6: "rational",
        7: "radical", 8: "radical",
    }

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "self_evaluation"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 8

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["error_detection", "estimate_magnitude"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls problem type and trap likelihood.

        Returns:
            Natural language description.
        """
        return "solve and rate your confidence"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a problem that may or may not contain a trap.

        Args:
            difficulty: Controls problem type.

        Returns:
            Tuple of (problem_string, solution_data).
        """
        has_trap = self._rng.random() < 0.5
        level = self._PROBLEM_LEVELS.get(difficulty, "linear")
        builder = self._get_level_builder(level)
        return builder(has_trap, difficulty)

    def _get_level_builder(self, level: str):
        """Return the builder method for the given problem level.

        Args:
            level: Problem level identifier.

        Returns:
            Builder method.
        """
        builders = {
            "linear": self._build_linear,
            "quadratic": self._build_quadratic,
            "rational": self._build_rational,
            "radical": self._build_radical,
        }
        return builders[level]

    def _build_linear(self, has_trap: bool,
                      difficulty: int) -> tuple[str, dict]:
        """Build a linear problem, optionally with a division-by-zero trap.

        Args:
            has_trap: Whether to include a trap.
            difficulty: Controls coefficient magnitudes.

        Returns:
            Tuple of (problem_string, solution_data).
        """
        a = self._rng.randint(2, 5 + difficulty)
        b = self._rng.randint(1, 4 + difficulty)
        if has_trap:
            problem = f"\\frac{{{a}x}}{{{a}x-{a * b}}}=1"
            return problem, {
                "has_trap": True, "trap_type": "division by zero",
                "trap_value": b, "solution": f"no solution (x={b} excluded)",
                "confidence": "low",
            }
        c = a * b + self._rng.randint(1, 10)
        problem = f"{a}x+{b}={c}"
        x_val = (c - b) // a if (c - b) % a == 0 else c - b
        if (c - b) % a != 0:
            problem = f"{a}x+{b}={a * self._rng.randint(1, 5) + b}"
            x_val = self._rng.randint(1, 5)
            c = a * x_val + b
            problem = f"{a}x+{b}={c}"
        return problem, {
            "has_trap": False, "trap_type": "none",
            "solution": str(x_val), "confidence": "high",
        }

    def _build_quadratic(self, has_trap: bool,
                         difficulty: int) -> tuple[str, dict]:
        """Build a quadratic problem, optionally with an extraneous root.

        Args:
            has_trap: Whether to include a trap.
            difficulty: Controls root magnitudes.

        Returns:
            Tuple of (problem_string, solution_data).
        """
        r1 = self._rng.randint(1, 3 + difficulty)
        r2 = self._rng.randint(-3 - difficulty, -1)
        if has_trap:
            problem = f"|x^2-{r1*r1}|=-1"
            return problem, {
                "has_trap": True, "trap_type": "absolute value never negative",
                "solution": "no solution",
                "confidence": "low",
            }
        b = -(r1 + r2)
        c = r1 * r2
        problem = f"x^2+{b}x+{c}=0"
        return problem, {
            "has_trap": False, "trap_type": "none",
            "solution": f"x={r1} or x={r2}",
            "confidence": "high", "roots": [r1, r2],
        }

    def _build_rational(self, has_trap: bool,
                        difficulty: int) -> tuple[str, dict]:
        """Build a rational equation, optionally with domain restriction.

        Args:
            has_trap: Whether to include a trap.
            difficulty: Controls equation complexity.

        Returns:
            Tuple of (problem_string, solution_data).
        """
        a = self._rng.randint(2, 4 + difficulty)
        if has_trap:
            problem = f"\\frac{{x^2-{a*a}}}{{x-{a}}}=x+{a}"
            return problem, {
                "has_trap": True, "trap_type": f"x={a} excluded from domain",
                "solution": f"all x except x={a}",
                "confidence": "low",
            }
        b = self._rng.randint(1, 5)
        c = a + b
        problem = f"\\frac{{{a}}}{{x}}+{b}={c}"
        x_val = a // (c - b) if (c - b) != 0 else 1
        x_val = 1
        c = a + b
        return problem, {
            "has_trap": False, "trap_type": "none",
            "solution": f"x={x_val}",
            "confidence": "high",
        }

    def _build_radical(self, has_trap: bool,
                       difficulty: int) -> tuple[str, dict]:
        """Build a radical equation, optionally with sign constraint trap.

        Args:
            has_trap: Whether to include a trap.
            difficulty: Controls equation complexity.

        Returns:
            Tuple of (problem_string, solution_data).
        """
        a = self._rng.randint(2, 4 + difficulty)
        if has_trap:
            problem = f"\\sqrt{{x}}=-{a}"
            return problem, {
                "has_trap": True, "trap_type": "square root cannot be negative",
                "solution": "no solution",
                "confidence": "low",
            }
        x_val = a * a
        problem = f"\\sqrt{{x}}={a}"
        return problem, {
            "has_trap": False, "trap_type": "none",
            "solution": f"x={x_val}",
            "confidence": "high",
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution and confidence assessment steps.

        Args:
            data: Solution data with trap info.

        Returns:
            Steps showing solution process and confidence rating.
        """
        steps: list[str] = [f"solve: {data['solution']}"]
        if data["has_trap"]:
            steps.append(f"TRAP detected: {data['trap_type']}")
            steps.append(f"confidence: {data['confidence']} (trap present)")
        else:
            steps.append("no traps detected")
            steps.append(f"confidence: {data['confidence']}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the solution with confidence assessment.

        Args:
            data: Solution data.

        Returns:
            Solution string with trap indication.
        """
        if data["has_trap"]:
            return f"{data['solution']} [trap: {data['trap_type']}]"
        return data["solution"]
