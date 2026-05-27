"""Tier 2 generators — intermediate mathematics and graph algorithms.

Unlocks when Tier 1 tasks are mastered. Introduces modular arithmetic,
exponentiation, GCD via Euclid, polynomial evaluation via Horner's method,
power rule differentiation, quadratic root finding, graph reachability
via BFS, and binomial coefficients.
"""
from collections import deque
from math import gcd

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


class PolynomialFormatter:
    """Formats polynomial coefficients into LaTeX strings.

    Converts a list of coefficients [a_n, a_{n-1}, ..., a_0] into
    a human-readable polynomial string with proper sign handling
    and exponent notation.

    Example:
        >>> f = PolynomialFormatter()
        >>> f.format([2, 0, 1, -4])
        '2x^3+x-4'
    """

    def format(self, coeffs: list[int]) -> str:
        """Format coefficients into a polynomial string.

        Args:
            coeffs: Coefficients from highest to lowest degree.

        Returns:
            Formatted polynomial string.
        """
        degree = len(coeffs) - 1
        parts: list[str] = []

        for i, c in enumerate(coeffs):
            if c == 0:
                continue
            power = degree - i
            parts.append(self._format_term(c, power, len(parts) == 0))

        return "".join(parts) if parts else "0"

    def _format_term(self, coeff: int, power: int,
                     is_first: bool) -> str:
        """Format a single polynomial term.

        Args:
            coeff: Coefficient value.
            power: Exponent of x.
            is_first: Whether this is the first non-zero term.

        Returns:
            Formatted term string with sign.
        """
        sign = self._sign_prefix(coeff, is_first)
        abs_coeff = abs(coeff)
        body = self._term_body(abs_coeff, power)
        return f"{sign}{body}"

    def _sign_prefix(self, coeff: int, is_first: bool) -> str:
        """Determine the sign prefix for a term.

        Args:
            coeff: Coefficient value.
            is_first: Whether this is the leading term.

        Returns:
            Sign string (empty, '-', '+', or '-').
        """
        if is_first:
            return "-" if coeff < 0 else ""
        return "-" if coeff < 0 else "+"

    def _term_body(self, abs_coeff: int, power: int) -> str:
        """Format the body of a term (coefficient and variable).

        Args:
            abs_coeff: Absolute value of the coefficient.
            power: Exponent of x.

        Returns:
            Term body like '3x^2', 'x', or '5'.
        """
        if power == 0:
            return str(abs_coeff)
        if power == 1:
            return "x" if abs_coeff == 1 else f"{abs_coeff}x"
        if abs_coeff == 1:
            return f"x^{power}"
        return f"{abs_coeff}x^{power}"


class GraphBuilder:
    """Builds random directed graphs with controllable reachability.

    Constructs a directed graph as an adjacency list and can ensure
    that a target node is either reachable or unreachable from a
    source node, enabling 50/50 yes/no generation.

    Example:
        >>> import random
        >>> gb = GraphBuilder(random.Random(42))
        >>> adj, nodes = gb.build(4, reachable=True)
    """

    def __init__(self, rng: "random.Random") -> None:
        """Initialise with a random number generator.

        Args:
            rng: Seeded random instance.
        """
        self._rng = rng

    def build(self, num_nodes: int,
              reachable: bool) -> tuple[dict[str, list[str]], list[str]]:
        """Build a directed graph with controlled reachability.

        Args:
            num_nodes: Number of nodes in the graph.
            reachable: Whether the last node should be reachable from the first.

        Returns:
            Tuple of (adjacency_dict, node_list).
        """
        nodes = [chr(97 + i) for i in range(num_nodes)]
        adj: dict[str, list[str]] = {n: [] for n in nodes}

        if reachable:
            self._add_reachable_path(adj, nodes)
        else:
            self._add_unreachable_edges(adj, nodes)

        self._add_random_edges(adj, nodes)
        return adj, nodes

    def _add_reachable_path(self, adj: dict[str, list[str]],
                            nodes: list[str]) -> None:
        """Ensure a path exists from first to last node.

        Args:
            adj: Adjacency dict to modify in place.
            nodes: Ordered node list.
        """
        path = self._rng.sample(nodes[1:-1], len(nodes) - 2)
        path = [nodes[0]] + path + [nodes[-1]]

        for i in range(len(path) - 1):
            if path[i + 1] not in adj[path[i]]:
                adj[path[i]].append(path[i + 1])

    def _add_unreachable_edges(self, adj: dict[str, list[str]],
                               nodes: list[str]) -> None:
        """Add edges that avoid connecting first to last node.

        Splits nodes into two disconnected groups to guarantee
        the last node is unreachable from the first.

        Args:
            adj: Adjacency dict to modify in place.
            nodes: Ordered node list.
        """
        mid = len(nodes) // 2
        group_a = nodes[:mid]
        group_b = nodes[mid:]

        for group in (group_a, group_b):
            for i in range(len(group) - 1):
                if self._rng.random() < 0.6:
                    adj[group[i]].append(group[i + 1])

    def _add_random_edges(self, adj: dict[str, list[str]],
                          nodes: list[str]) -> None:
        """Sprinkle random edges without self-loops or duplicates.

        Args:
            adj: Adjacency dict to modify in place.
            nodes: Node list.
        """
        num_extra = self._rng.randint(1, len(nodes))

        for _ in range(num_extra):
            src = self._rng.choice(nodes[:-1])
            dst = self._rng.choice(nodes)
            if dst != src and dst not in adj[src]:
                adj[src].append(dst)


@register
class ModularGenerator(StepGenerator):
    """Modular arithmetic — compute the remainder of integer division.

    Generates problems of the form 'a mod b' and shows the division
    step before extracting the remainder. Uses LaTeX \\mod notation.

    Input format:
        ``compute remainder``

    Target format:
        ``47 \\mod 7 <step> 47/7=6r5 <step> 5``

    Difficulty scaling:
        Difficulty N produces operands with N digits. The dividend
        is always larger than the divisor. Higher difficulties yield
        larger quotients and remainders.

    Prerequisites:
        division.

    Example:
        >>> gen = ModularGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'modular'
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "modular"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 2

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["division"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls operand size.

        Returns:
            Natural language description.
        """
        return "compute remainder"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a modular arithmetic problem.

        Args:
            difficulty: Number of digits for the dividend.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        lower, upper = self._operand_range(difficulty)
        a = self._rng.randint(max(2, lower), upper)
        b = self._rng.randint(2, max(2, upper // 2))
        if a < b:
            a, b = b, a

        quotient = a // b
        remainder = a % b
        return (
            f"{a} \\mod {b}",
            {"a": a, "b": b, "quotient": quotient, "remainder": remainder},
        )

    def _create_steps(self, data: dict) -> list[str]:
        """Generate the division step showing quotient and remainder.

        Args:
            data: Solution data with operands.

        Returns:
            Single step showing the division result.
        """
        return [
            f"{data['a']}/{data['b']}={data['quotient']}r{data['remainder']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the remainder as a string.

        Args:
            data: Solution data.

        Returns:
            String representation of the remainder.
        """
        return str(data["remainder"])


@register
class ExponentiationGenerator(StepGenerator):
    """Repeated multiplication to compute integer powers.

    Generates problems of the form 'base^exp' and shows each
    multiplication step building up to the final result.

    Input format:
        ``compute power``

    Target format:
        ``3^4 <step> 3*3=9 <step> 9*3=27 <step> 27*3=81 <step> 81``

    Difficulty scaling:
        d1: base 2-5, exp 2-3.
        d5: base 2-10, exp 4-6.
        d8: base 2-15, exp 5-8.
        Results are capped at 32 characters to avoid overflow.

    Prerequisites:
        multiplication.

    Example:
        >>> gen = ExponentiationGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'exponentiation'
    """

    _BASE_RANGES = {
        1: (2, 5), 2: (2, 6), 3: (2, 7), 4: (2, 8),
        5: (2, 10), 6: (2, 12), 7: (2, 13), 8: (2, 15),
    }

    _EXP_RANGES = {
        1: (2, 3), 2: (2, 3), 3: (3, 4), 4: (3, 5),
        5: (4, 6), 6: (4, 6), 7: (5, 7), 8: (5, 8),
    }

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "exponentiation"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 2

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["multiplication"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls base and exponent ranges.

        Returns:
            Natural language description.
        """
        return "compute power"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a power computation problem.

        Retries if the result exceeds 32 characters to keep
        targets within token budget.

        Args:
            difficulty: Controls base and exponent ranges.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        base_lo, base_hi = self._BASE_RANGES.get(difficulty, (2, 5))
        exp_lo, exp_hi = self._EXP_RANGES.get(difficulty, (2, 3))

        for _ in range(50):
            base = self._rng.randint(base_lo, base_hi)
            exp = self._rng.randint(exp_lo, exp_hi)
            result = base ** exp
            if len(str(result)) <= 32:
                break

        return (
            f"{base}^{exp}",
            {"base": base, "exp": exp, "result": result},
        )

    def _create_steps(self, data: dict) -> list[str]:
        """Generate repeated multiplication steps.

        Args:
            data: Solution data with base, exponent, and result.

        Returns:
            Steps showing each successive multiplication.
        """
        base = data["base"]
        exp = data["exp"]
        steps: list[str] = []
        current = base

        for _ in range(exp - 1):
            product = current * base
            steps.append(f"{current}*{base}={product}")
            current = product

        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the power result as a string.

        Args:
            data: Solution data.

        Returns:
            String representation of base^exp.
        """
        return str(data["result"])


@register
class GCDGenerator(StepGenerator):
    """Greatest common divisor via the Euclidean algorithm.

    Generates pairs of integers and shows repeated modular reduction
    until the remainder reaches zero. The last non-zero remainder
    is the GCD.

    Input format:
        ``find greatest common divisor``

    Target format:
        ``\\gcd(48,18) <step> 48 \\mod 18=12 <step> 18 \\mod 12=6 <step>
        12 \\mod 6=0 <step> 6``

    Difficulty scaling:
        Difficulty N produces operands with N digits. Larger operands
        tend to require more Euclidean steps.

    Prerequisites:
        modular.

    Example:
        >>> gen = GCDGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'gcd'
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "gcd"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 2

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["modular"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls operand size.

        Returns:
            Natural language description.
        """
        return "find greatest common divisor"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a GCD problem with two positive integers.

        Args:
            difficulty: Number of digits per operand.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        lower, upper = self._operand_range(difficulty)
        a = self._rng.randint(max(2, lower), upper)
        b = self._rng.randint(max(2, lower), upper)
        if a < b:
            a, b = b, a

        return (
            f"\\gcd({a},{b})",
            {"a": a, "b": b, "result": gcd(a, b)},
        )

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Euclidean algorithm steps.

        Args:
            data: Solution data with two operands.

        Returns:
            Steps showing each modular reduction.
        """
        a, b = data["a"], data["b"]
        steps: list[str] = []

        while b != 0:
            remainder = a % b
            steps.append(f"{a} \\mod {b}={remainder}")
            a, b = b, remainder

        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the GCD as a string.

        Args:
            data: Solution data.

        Returns:
            String representation of the GCD.
        """
        return str(data["result"])


@register
class PolynomialEvalGenerator(StepGenerator):
    """Evaluate a polynomial at a point using Horner's method.

    Generates a polynomial with integer coefficients and evaluates
    it at an integer point, showing the nested multiplication
    (Horner's scheme) step by step.

    Input format:
        ``evaluate polynomial at point``

    Target format:
        ``2x^3+x-4 at x=3 <step> ((2*3+0)*3+1)*3-4 <step>
        (6+0)*3+1=19 <step> 19*3-4=53 <step> 53``

    Difficulty scaling:
        d1: degree 1-2.
        d5: degree 3-4.
        d8: degree 5-6.
        Coefficients range from -9 to 9.

    Prerequisites:
        multiplication, exponentiation.

    Example:
        >>> gen = PolynomialEvalGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'polynomial_eval'
    """

    _DEGREE_RANGES = {
        1: (1, 2), 2: (2, 2), 3: (2, 3), 4: (3, 3),
        5: (3, 4), 6: (4, 4), 7: (4, 5), 8: (5, 6),
    }

    def __init__(self, **kwargs) -> None:
        """Initialise with a polynomial formatter.

        Args:
            **kwargs: Passed to parent constructor.
        """
        super().__init__(**kwargs)
        self._formatter = PolynomialFormatter()

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "polynomial_eval"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 2

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["multiplication", "exponentiation"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls polynomial degree.

        Returns:
            Natural language description.
        """
        return "evaluate polynomial at point"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a polynomial evaluation problem.

        Args:
            difficulty: Controls polynomial degree.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        deg_lo, deg_hi = self._DEGREE_RANGES.get(difficulty, (1, 2))
        degree = self._rng.randint(deg_lo, deg_hi)
        coeffs = self._random_coefficients(degree)
        x_val = self._rng.randint(1, 5)
        result = self._horner_eval(coeffs, x_val)
        poly_str = self._formatter.format(coeffs)

        return (
            f"{poly_str} at x={x_val}",
            {"coeffs": coeffs, "x": x_val, "result": result,
             "poly_str": poly_str},
        )

    def _random_coefficients(self, degree: int) -> list[int]:
        """Generate random non-zero leading coefficient and others.

        Args:
            degree: Polynomial degree.

        Returns:
            Coefficient list from highest to lowest degree.
        """
        coeffs: list[int] = []
        for i in range(degree + 1):
            c = self._rng.randint(-9, 9)
            if i == 0 and c == 0:
                c = 1
            coeffs.append(c)
        return coeffs

    def _horner_eval(self, coeffs: list[int], x: int) -> int:
        """Evaluate polynomial using Horner's method.

        Args:
            coeffs: Coefficients from highest to lowest degree.
            x: Point to evaluate at.

        Returns:
            Polynomial value at x.
        """
        result = coeffs[0]
        for c in coeffs[1:]:
            result = result * x + c
        return result

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Horner's method evaluation steps.

        Args:
            data: Solution data with coefficients and x value.

        Returns:
            Steps showing each multiply-and-add.
        """
        coeffs = data["coeffs"]
        x = data["x"]
        return self._horner_steps(coeffs, x)

    def _horner_steps(self, coeffs: list[int], x: int) -> list[str]:
        """Compute and format each Horner step.

        Args:
            coeffs: Polynomial coefficients (high to low).
            x: Evaluation point.

        Returns:
            Step strings showing the nested computation.
        """
        steps: list[str] = []
        acc = coeffs[0]

        for c in coeffs[1:]:
            product = acc * x
            new_acc = product + c
            steps.append(f"{acc}*{x}+{c}={new_acc}")
            acc = new_acc

        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the polynomial value as a string.

        Args:
            data: Solution data.

        Returns:
            String representation of the result.
        """
        return str(data["result"])


@register
class DerivativeGenerator(StepGenerator):
    """Power rule differentiation of polynomials.

    Generates a polynomial and differentiates each term using the
    power rule d/dx(ax^n) = n*a*x^(n-1). Uses LaTeX \\frac{d}{dx}
    notation for the problem statement.

    Input format:
        ``differentiate polynomial``

    Target format:
        ``\\frac{d}{dx}(3x^2+2x-5) <step> 3*2x=6x <step> 2*1=2 <step>
        0 <step> 6x+2``

    Difficulty scaling:
        d1: degree 1-2, 2-3 terms.
        d5: degree 3-4, 4-5 terms.
        d8: degree 5-7, 6-8 terms.

    Prerequisites:
        polynomial_eval.

    Example:
        >>> gen = DerivativeGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'derivative'
    """

    _DEGREE_RANGES = {
        1: (1, 2), 2: (2, 2), 3: (2, 3), 4: (3, 3),
        5: (3, 4), 6: (4, 5), 7: (5, 6), 8: (5, 7),
    }

    def __init__(self, **kwargs) -> None:
        """Initialise with a polynomial formatter.

        Args:
            **kwargs: Passed to parent constructor.
        """
        super().__init__(**kwargs)
        self._formatter = PolynomialFormatter()

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "derivative"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 2

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["polynomial_eval"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls degree and term count.

        Returns:
            Natural language description.
        """
        return "differentiate polynomial"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a polynomial differentiation problem.

        Args:
            difficulty: Controls polynomial degree.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        deg_lo, deg_hi = self._DEGREE_RANGES.get(difficulty, (1, 2))
        degree = self._rng.randint(deg_lo, deg_hi)
        coeffs = self._random_coefficients(degree)
        derivative = self._differentiate(coeffs)
        poly_str = self._formatter.format(coeffs)

        return (
            f"\\frac{{d}}{{dx}}({poly_str})",
            {"coeffs": coeffs, "derivative": derivative,
             "poly_str": poly_str},
        )

    def _random_coefficients(self, degree: int) -> list[int]:
        """Generate random polynomial coefficients.

        Args:
            degree: Polynomial degree.

        Returns:
            Coefficient list from highest to lowest degree.
        """
        coeffs: list[int] = []
        for i in range(degree + 1):
            c = self._rng.randint(-9, 9)
            if i == 0 and c == 0:
                c = 1
            coeffs.append(c)
        return coeffs

    def _differentiate(self, coeffs: list[int]) -> list[int]:
        """Apply power rule to all terms.

        Args:
            coeffs: Coefficients from highest to lowest degree.

        Returns:
            Derivative coefficients (one degree lower).
        """
        degree = len(coeffs) - 1
        result: list[int] = []

        for i, c in enumerate(coeffs[:-1]):
            power = degree - i
            result.append(c * power)

        return result if result else [0]

    def _create_steps(self, data: dict) -> list[str]:
        """Generate per-term differentiation steps.

        Args:
            data: Solution data with coefficients.

        Returns:
            Steps showing each term's power rule application.
        """
        coeffs = data["coeffs"]
        degree = len(coeffs) - 1
        steps: list[str] = []

        for i, c in enumerate(coeffs):
            power = degree - i
            steps.append(self._term_step(c, power))

        return steps

    def _term_step(self, coeff: int, power: int) -> str:
        """Format the power rule step for one term.

        Args:
            coeff: Original coefficient.
            power: Original exponent.

        Returns:
            Step string showing the differentiation.
        """
        if power == 0:
            return "0"

        new_coeff = coeff * power
        if power == 1:
            return f"{coeff}*{power}={new_coeff}"

        new_power = power - 1
        x_part = "x" if new_power == 1 else f"x^{new_power}"
        return f"{coeff}*{power}{x_part}={new_coeff}{x_part}"

    def _create_answer(self, data: dict) -> str:
        """Return the derivative polynomial as a string.

        Args:
            data: Solution data.

        Returns:
            Formatted derivative polynomial.
        """
        return self._formatter.format(data["derivative"])


@register
class QuadraticGenerator(StepGenerator):
    """Find integer roots of quadratic equations.

    Generates quadratics by choosing integer roots r1, r2 and
    expanding (x - r1)(x - r2). Shows the discriminant, square
    root, and quadratic formula steps using LaTeX notation.

    Input format:
        ``find roots of quadratic equation``

    Target format:
        ``x^2-5x+6=0 <step> \\delta=25-24=1 <step> \\sqrt{1}=1 <step>
        x=\\frac{5\\pm 1}{2} <step> 2,3``

    Difficulty scaling:
        Root magnitudes scale with difficulty.
        d1: roots in [-3, 3].
        d5: roots in [-15, 15].
        d8: roots in [-30, 30].

    Prerequisites:
        multiplication, subtraction.

    Example:
        >>> gen = QuadraticGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'quadratic'
    """

    _ROOT_RANGES = {
        1: (1, 3), 2: (1, 5), 3: (2, 8), 4: (3, 10),
        5: (5, 15), 6: (5, 20), 7: (8, 25), 8: (10, 30),
    }

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "quadratic"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 2

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["multiplication", "subtraction"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls root magnitude.

        Returns:
            Natural language description.
        """
        return "find roots of quadratic equation"

    def _random_root(self, lo: int, hi: int) -> int:
        """Generate a random root, negative ~30% of the time.

        Args:
            lo: Minimum absolute value of the root.
            hi: Maximum absolute value of the root.

        Returns:
            Integer root value.
        """
        if self._rng.random() < 0.3:
            return self._rng.randint(-hi, -lo)
        return self._rng.randint(lo, hi)

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a quadratic equation from integer roots.

        Constructs (x - r1)(x - r2) = x^2 - (r1+r2)x + r1*r2.

        Args:
            difficulty: Controls root magnitude.

        Returns:
            Tuple of (latex_equation, solution_data).
        """
        lo, hi = self._ROOT_RANGES.get(difficulty, (1, 3))
        r1 = self._random_root(lo, hi)
        r2 = self._random_root(lo, hi)
        b = -(r1 + r2)
        c = r1 * r2
        discriminant = b * b - 4 * c
        equation = self._format_quadratic(1, b, c)

        return (
            f"{equation}=0",
            {"a": 1, "b": b, "c": c, "r1": r1, "r2": r2,
             "discriminant": discriminant, "sqrt_disc": abs(r1 - r2)},
        )

    def _format_quadratic(self, a: int, b: int, c: int) -> str:
        """Format quadratic coefficients into equation string.

        Args:
            a: Leading coefficient (always 1).
            b: Linear coefficient.
            c: Constant term.

        Returns:
            Formatted quadratic like 'x^2-5x+6'.
        """
        formatter = PolynomialFormatter()
        return formatter.format([a, b, c])

    def _create_steps(self, data: dict) -> list[str]:
        """Generate quadratic formula solution steps.

        Args:
            data: Solution data with coefficients and roots.

        Returns:
            Steps showing discriminant, sqrt, and formula.
        """
        b = data["b"]
        disc = data["discriminant"]
        sqrt_d = data["sqrt_disc"]
        b_sq = b ** 2
        four_ac = 4 * data["a"] * data["c"]

        return [
            self._discriminant_step(b_sq, four_ac, disc),
            f"\\sqrt{{{disc}}}={sqrt_d}",
            f"x=\\frac{{{-b}\\pm {sqrt_d}}}{{{2 * data['a']}}}",
        ]

    def _discriminant_step(self, b_sq: int, four_ac: int,
                           disc: int) -> str:
        """Format the discriminant computation step.

        Args:
            b_sq: Value of b squared.
            four_ac: Value of 4ac.
            disc: Discriminant value.

        Returns:
            LaTeX step string for discriminant.
        """
        if four_ac >= 0:
            return f"\\delta={b_sq}-{four_ac}={disc}"
        return f"\\delta={b_sq}+{abs(four_ac)}={disc}"

    def _create_answer(self, data: dict) -> str:
        """Return the sorted roots as a comma-separated string.

        Args:
            data: Solution data.

        Returns:
            Roots in ascending order.
        """
        roots = sorted([data["r1"], data["r2"]])
        return ",".join(str(r) for r in roots)


@register
class GraphReachGenerator(StepGenerator):
    """BFS reachability in directed graphs.

    Generates a random directed graph and checks whether a target
    node is reachable from a source node using breadth-first search.
    Shows each BFS frontier expansion as a step.

    Input format:
        ``check if node is reachable in directed graph``

    Target format:
        ``a:b,c;b:d;c:e;d:;e: from a to e <step> visit a <step>
        visit b,c <step> visit d,e <step> yes``

    Difficulty scaling:
        d1: 3-4 nodes.
        d5: 6-8 nodes.
        d8: 10-12 nodes.
        50/50 split between reachable and unreachable targets.

    Prerequisites:
        logic.

    Example:
        >>> gen = GraphReachGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'graph_reach'
    """

    _NODE_RANGES = {
        1: (3, 4), 2: (4, 5), 3: (4, 5), 4: (5, 6),
        5: (6, 8), 6: (7, 9), 7: (8, 10), 8: (10, 12),
    }

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "graph_reach"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 2

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["boolean_eval"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls graph size.

        Returns:
            Natural language description.
        """
        return "check if node is reachable in directed graph"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a directed graph reachability problem.

        Args:
            difficulty: Controls number of nodes.

        Returns:
            Tuple of (graph_description, solution_data).
        """
        lo, hi = self._NODE_RANGES.get(difficulty, (3, 4))
        num_nodes = self._rng.randint(lo, hi)
        reachable = self._rng.random() < 0.5

        builder = GraphBuilder(self._rng)
        adj, nodes = builder.build(num_nodes, reachable)
        source, target = nodes[0], nodes[-1]
        bfs_result = self._bfs(adj, source, target)
        graph_str = self._format_graph(adj, nodes)

        return (
            f"{graph_str} from {source} to {target}",
            {"adj": adj, "source": source, "target": target,
             "frontiers": bfs_result["frontiers"],
             "reachable": bfs_result["reachable"]},
        )

    def _format_graph(self, adj: dict[str, list[str]],
                      nodes: list[str]) -> str:
        """Format adjacency list as a compact string.

        Args:
            adj: Adjacency dict.
            nodes: Ordered node list.

        Returns:
            String like 'a:b,c;b:d;c:;d:'.
        """
        parts: list[str] = []
        for n in nodes:
            neighbors = ",".join(sorted(adj[n]))
            parts.append(f"{n}:{neighbors}")
        return ";".join(parts)

    def _bfs(self, adj: dict[str, list[str]], source: str,
             target: str) -> dict:
        """Perform BFS and record frontier expansions.

        Args:
            adj: Adjacency dict.
            source: Starting node.
            target: Goal node.

        Returns:
            Dict with frontiers list and reachable boolean.
        """
        visited: set[str] = set()
        queue: deque[str] = deque([source])
        visited.add(source)
        frontiers: list[list[str]] = [[source]]

        while queue:
            frontier: list[str] = []
            for _ in range(len(queue)):
                node = queue.popleft()
                for neighbor in sorted(adj.get(node, [])):
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)
                        frontier.append(neighbor)

            if frontier:
                frontiers.append(sorted(frontier))

        return {"frontiers": frontiers, "reachable": target in visited}

    def _create_steps(self, data: dict) -> list[str]:
        """Generate BFS frontier visit steps.

        Args:
            data: Solution data with BFS frontiers.

        Returns:
            Steps showing each frontier expansion.
        """
        return [
            f"visit {','.join(frontier)}"
            for frontier in data["frontiers"]
        ]

    def _create_answer(self, data: dict) -> str:
        """Return 'yes' or 'no' for reachability.

        Args:
            data: Solution data.

        Returns:
            'yes' if target is reachable, 'no' otherwise.
        """
        return "yes" if data["reachable"] else "no"


@register
class BinomialGenerator(StepGenerator):
    """Compute binomial coefficients C(n, k).

    Generates binomial coefficient problems and shows the
    multiplicative formula: C(n,k) = n!/(k!(n-k)!) computed as
    (n * (n-1) * ... * (n-k+1)) / (k * (k-1) * ... * 1).

    Input format:
        ``compute binomial coefficient``

    Target format:
        ``\\binom{7}{3} <step> 7*6*5=210 <step> 3*2*1=6 <step>
        210/6=35 <step> 35``

    Difficulty scaling:
        d1: n=4-6, k chosen randomly.
        d5: n=10-15.
        d8: n=18-25.

    Prerequisites:
        multiplication, division.

    Example:
        >>> gen = BinomialGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'binomial'
    """

    _N_RANGES = {
        1: (4, 6), 2: (5, 7), 3: (6, 9), 4: (8, 11),
        5: (10, 15), 6: (12, 17), 7: (15, 20), 8: (18, 25),
    }

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "binomial"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 2

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["multiplication", "division"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls n range.

        Returns:
            Natural language description.
        """
        return "compute binomial coefficient"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a binomial coefficient problem.

        Args:
            difficulty: Controls n range.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        n_lo, n_hi = self._N_RANGES.get(difficulty, (4, 6))
        n = self._rng.randint(n_lo, n_hi)
        k = self._rng.randint(1, n - 1)

        if k > n - k:
            k = n - k

        numerator = self._falling_product(n, k)
        denominator = self._factorial(k)
        result = numerator // denominator

        return (
            f"\\binom{{{n}}}{{{k}}}",
            {"n": n, "k": k, "numerator": numerator,
             "denominator": denominator, "result": result},
        )

    def _falling_product(self, n: int, k: int) -> int:
        """Compute n * (n-1) * ... * (n-k+1).

        Args:
            n: Top of the binomial.
            k: Number of factors.

        Returns:
            Product of k falling terms from n.
        """
        product = 1
        for i in range(k):
            product *= (n - i)
        return product

    def _factorial(self, k: int) -> int:
        """Compute k factorial.

        Args:
            k: Non-negative integer.

        Returns:
            k! value.
        """
        product = 1
        for i in range(1, k + 1):
            product *= i
        return product

    def _create_steps(self, data: dict) -> list[str]:
        """Generate numerator, denominator, and division steps.

        Args:
            data: Solution data with n, k, products.

        Returns:
            Steps showing the multiplicative computation.
        """
        n, k = data["n"], data["k"]
        num_str = self._format_product_chain(n, k, descending=True)
        den_str = self._format_product_chain(k, k, descending=False)

        return [
            f"{num_str}={data['numerator']}",
            f"{den_str}={data['denominator']}",
            f"{data['numerator']}/{data['denominator']}={data['result']}",
        ]

    def _format_product_chain(self, start: int, count: int,
                              descending: bool) -> str:
        """Format a chain of multiplied integers.

        Args:
            start: Starting integer.
            count: Number of factors.
            descending: If True, count down; otherwise count up from 1.

        Returns:
            String like '7*6*5' or '3*2*1'.
        """
        if descending:
            factors = [str(start - i) for i in range(count)]
        else:
            factors = [str(i) for i in range(start, 0, -1)]

        return "*".join(factors)

    def _create_answer(self, data: dict) -> str:
        """Return the binomial coefficient as a string.

        Args:
            data: Solution data.

        Returns:
            String representation of C(n, k).
        """
        return str(data["result"])
