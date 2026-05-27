"""Tier 3 generators — intermediate algorithms and mathematical operations.

Unlocks when Tier 0-2 foundation tasks are mastered. Introduces
LCM, modular exponentiation, modular inverse, integration,
second derivatives, systems of equations, determinants, Collatz
sequences, base conversion, permutations, prefix scans, RPN
evaluation, and cycle detection.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


class GCDHelper:
    """Computes greatest common divisor and records Euclidean steps.

    Provides a reusable GCD computation with step-by-step recording
    of the Euclidean algorithm, used by LCM and modular inverse generators.

    Example:
        >>> h = GCDHelper()
        >>> h.compute(12, 18)
        6
        >>> h.steps
        ['18=12*1+6', '12=6*2+0']
    """

    def __init__(self) -> None:
        """Initialise with empty step list."""
        self._steps: list[str] = []

    @property
    def steps(self) -> list[str]:
        """Return the recorded Euclidean algorithm steps."""
        return self._steps

    def compute(self, a: int, b: int) -> int:
        """Compute GCD using the Euclidean algorithm with step recording.

        Args:
            a: First positive integer.
            b: Second positive integer.

        Returns:
            Greatest common divisor of a and b.
        """
        self._steps = []
        if a < b:
            a, b = b, a
        return self._euclidean(a, b)

    def _euclidean(self, a: int, b: int) -> int:
        """Recursively apply Euclidean division and record each step.

        Args:
            a: Larger operand.
            b: Smaller operand.

        Returns:
            GCD of a and b.
        """
        if b == 0:
            return a
        q, r = divmod(a, b)
        self._steps.append(f"{a}={b}*{q}+{r}")
        return self._euclidean(b, r)


class PolynomialHelper:
    """Represents and differentiates polynomials with integer coefficients.

    Stores a polynomial as a list of (coefficient, power) pairs sorted
    by descending power. Supports differentiation and LaTeX formatting.

    Example:
        >>> p = PolynomialHelper([(3, 3), (2, 1), (1, 0)])
        >>> p.to_latex()
        '3x^3+2x+1'
        >>> d = p.differentiate()
        >>> d.to_latex()
        '9x^2+2'
    """

    def __init__(self, terms: list[tuple[int, int]]) -> None:
        """Initialise with a list of (coefficient, power) pairs.

        Args:
            terms: List of (coefficient, power) tuples, highest power first.
        """
        self._terms = sorted(terms, key=lambda t: -t[1])

    @property
    def terms(self) -> list[tuple[int, int]]:
        """Return the polynomial terms as (coefficient, power) pairs."""
        return list(self._terms)

    def differentiate(self) -> "PolynomialHelper":
        """Compute the derivative of this polynomial.

        Returns:
            New PolynomialHelper representing the derivative.
        """
        derived = [(c * p, p - 1) for c, p in self._terms if p > 0]
        if not derived:
            return PolynomialHelper([(0, 0)])
        return PolynomialHelper(derived)

    def to_latex(self) -> str:
        """Format the polynomial as a LaTeX string.

        Returns:
            LaTeX representation of the polynomial.
        """
        if not self._terms:
            return "0"
        parts: list[str] = []
        for i, (c, p) in enumerate(self._terms):
            parts.append(self._format_term(c, p, is_first=(i == 0)))
        return "".join(parts)

    def _format_term(self, coeff: int, power: int,
                     is_first: bool) -> str:
        """Format a single term as LaTeX.

        Args:
            coeff: Coefficient value.
            power: Power of x.
            is_first: Whether this is the leading term.

        Returns:
            Formatted term string.
        """
        if power == 0:
            return self._format_constant(coeff, is_first)
        return self._format_variable_term(coeff, power, is_first)

    def _format_constant(self, coeff: int, is_first: bool) -> str:
        """Format a constant term.

        Args:
            coeff: Constant value.
            is_first: Whether this is the leading term.

        Returns:
            Formatted constant string with sign handling.
        """
        if is_first:
            return str(coeff)
        if coeff >= 0:
            return f"+{coeff}"
        return str(coeff)

    def _format_variable_term(self, coeff: int, power: int,
                              is_first: bool) -> str:
        """Format a term containing x.

        Args:
            coeff: Coefficient value.
            power: Power of x (must be > 0).
            is_first: Whether this is the leading term.

        Returns:
            Formatted variable term like '3x^2' or '-x'.
        """
        sign = "" if is_first else ("+" if coeff > 0 else "")
        coeff_str = self._coeff_string(coeff)
        x_part = "x" if power == 1 else f"x^{power}"
        return f"{sign}{coeff_str}{x_part}"

    def _coeff_string(self, coeff: int) -> str:
        """Format a coefficient, hiding 1/-1.

        Args:
            coeff: Coefficient value.

        Returns:
            String representation, empty for 1, '-' for -1.
        """
        if coeff == 1:
            return ""
        if coeff == -1:
            return "-"
        return str(coeff)


class MatrixHelper:
    """Represents a square matrix and computes determinants with steps.

    Supports 2x2 and 3x3 determinant computation using the standard
    formula (2x2) or cofactor expansion along the first row (3x3).

    Example:
        >>> m = MatrixHelper([[3, 1], [5, 2]])
        >>> m.determinant()
        1
    """

    def __init__(self, matrix: list[list[int]]) -> None:
        """Initialise with a 2D integer matrix.

        Args:
            matrix: Square matrix as list of rows.
        """
        self._matrix = matrix
        self._size = len(matrix)

    @property
    def size(self) -> int:
        """Return the dimension of the square matrix."""
        return self._size

    @property
    def matrix(self) -> list[list[int]]:
        """Return the matrix data."""
        return self._matrix

    def determinant(self) -> int:
        """Compute the determinant.

        Returns:
            Integer determinant value.
        """
        if self._size == 2:
            return self._det_2x2()
        return self._det_3x3()

    def _det_2x2(self) -> int:
        """Compute 2x2 determinant: ad - bc.

        Returns:
            Determinant value.
        """
        m = self._matrix
        return m[0][0] * m[1][1] - m[0][1] * m[1][0]

    def _det_3x3(self) -> int:
        """Compute 3x3 determinant via cofactor expansion along row 0.

        Returns:
            Determinant value.
        """
        m = self._matrix
        result = 0
        for j in range(3):
            sign = (-1) ** j
            minor = self._minor(0, j)
            result += sign * m[0][j] * minor.determinant()
        return result

    def _minor(self, row: int, col: int) -> "MatrixHelper":
        """Compute the minor matrix by removing a row and column.

        Args:
            row: Row index to remove.
            col: Column index to remove.

        Returns:
            New MatrixHelper for the minor.
        """
        rows = [r for i, r in enumerate(self._matrix) if i != row]
        minor = [[val for j, val in enumerate(r) if j != col] for r in rows]
        return MatrixHelper(minor)

    def to_latex(self) -> str:
        """Format the matrix in LaTeX pmatrix notation.

        Returns:
            LaTeX string like '\\begin{pmatrix} 3 & 1 \\\\ 5 & 2 \\end{pmatrix}'.
        """
        rows = [" & ".join(str(v) for v in row) for row in self._matrix]
        body = " \\\\ ".join(rows)
        return f"\\begin{{pmatrix}} {body} \\end{{pmatrix}}"


class GraphHelper:
    """Represents a directed graph and detects cycles via DFS.

    Stores the graph as an adjacency list and provides cycle detection
    with path recording for step-by-step output.

    Example:
        >>> g = GraphHelper({"a": ["b"], "b": ["c"], "c": ["a"]})
        >>> g.has_cycle()
        True
    """

    def __init__(self, adj: dict[str, list[str]]) -> None:
        """Initialise with an adjacency list.

        Args:
            adj: Mapping from node name to list of successor names.
        """
        self._adj = adj

    @property
    def adjacency(self) -> dict[str, list[str]]:
        """Return the adjacency list."""
        return dict(self._adj)

    def has_cycle(self) -> bool:
        """Check whether the graph contains a cycle.

        Returns:
            True if a cycle exists, False otherwise.
        """
        visited: set[str] = set()
        rec_stack: set[str] = set()
        for node in self._adj:
            if self._dfs_cycle(node, visited, rec_stack):
                return True
        return False

    def find_cycle_path(self) -> list[str]:
        """Find a cycle path if one exists.

        Returns:
            List of node names forming the cycle, or empty list.
        """
        visited: set[str] = set()
        rec_stack: set[str] = set()
        path: list[str] = []
        for node in self._adj:
            if self._dfs_path(node, visited, rec_stack, path):
                return self._extract_cycle(path)
        return []

    def _dfs_cycle(self, node: str, visited: set[str],
                   rec_stack: set[str]) -> bool:
        """DFS helper for cycle detection.

        Args:
            node: Current node.
            visited: Globally visited nodes.
            rec_stack: Nodes on the current recursion stack.

        Returns:
            True if a cycle is found from this node.
        """
        if node in rec_stack:
            return True
        if node in visited:
            return False
        visited.add(node)
        rec_stack.add(node)
        for neighbour in self._adj.get(node, []):
            if self._dfs_cycle(neighbour, visited, rec_stack):
                return True
        rec_stack.discard(node)
        return False

    def _dfs_path(self, node: str, visited: set[str],
                  rec_stack: set[str], path: list[str]) -> bool:
        """DFS helper that records the path for cycle extraction.

        Args:
            node: Current node.
            visited: Globally visited nodes.
            rec_stack: Nodes on the current recursion stack.
            path: Current DFS path being built.

        Returns:
            True if a cycle is found.
        """
        if node in rec_stack:
            path.append(node)
            return True
        if node in visited:
            return False
        visited.add(node)
        rec_stack.add(node)
        path.append(node)
        for neighbour in self._adj.get(node, []):
            if self._dfs_path(neighbour, visited, rec_stack, path):
                return True
        path.pop()
        rec_stack.discard(node)
        return False

    def _extract_cycle(self, path: list[str]) -> list[str]:
        """Extract the cycle from a DFS path ending with repeated node.

        Args:
            path: DFS path where last node repeats an earlier node.

        Returns:
            Cycle nodes from the repeated node back to itself.
        """
        cycle_node = path[-1]
        start = path.index(cycle_node)
        return path[start:]

    def to_edge_string(self) -> str:
        """Format the graph as a semicolon-separated edge list.

        Returns:
            String like 'a:b,c;b:d;c:;d:'.
        """
        parts: list[str] = []
        for node in sorted(self._adj):
            targets = ",".join(self._adj[node])
            parts.append(f"{node}:{targets}")
        return ";".join(parts)


@register
class LCMGenerator(StepGenerator):
    """Least common multiple via GCD computation.

    Generates LCM problems using the identity lcm(a,b) = a*b/gcd(a,b).
    Shows the GCD step followed by the multiplication and division.

    Input format:
        ``find least common multiple``

    Target format:
        ``\\text{lcm}(12,18) <step> \\gcd(12,18)=6 <step> 12*18/6=36 <step> 36``

    Difficulty scaling:
        Difficulty 1-2: two operands, 2-9 range.
        Difficulty 3-4: two operands, 10-99.
        Difficulty 5-6: three operands chained pairwise, 10-99.
        Difficulty 7-8: three operands chained pairwise, 100-999.

    Prerequisites:
        gcd, multiplication.

    Example:
        >>> gen = LCMGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'lcm'
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "lcm"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 3

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["gcd", "multiplication"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls operand count and magnitude.

        Returns:
            Natural language description.
        """
        return "find least common multiple"

    def _operand_count(self, difficulty: int) -> int:
        """Determine how many operands based on difficulty.

        Args:
            difficulty: Difficulty level.

        Returns:
            Number of operands (2 or 3).
        """
        if difficulty >= 5:
            return 3
        return 2

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate operands and compute the LCM.

        Args:
            difficulty: Controls operand count and range.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        lower, upper = self._operand_range(min((difficulty + 1) // 2, 3))
        lower = max(2, lower)
        count = self._operand_count(difficulty)
        operands = [self._rng.randint(lower, upper) for _ in range(count)]
        result = self._chain_lcm(operands)
        label = ",".join(str(x) for x in operands)
        return f"\\text{{lcm}}({label})", {"operands": operands, "result": result}

    def _chain_lcm(self, operands: list[int]) -> int:
        """Compute LCM of a list by chaining pairwise.

        Args:
            operands: List of positive integers.

        Returns:
            LCM of all operands.
        """
        result = operands[0]
        for op in operands[1:]:
            result = (result * op) // math.gcd(result, op)
        return result

    def _create_steps(self, data: dict) -> list[str]:
        """Generate GCD and LCM computation steps.

        Args:
            data: Solution data with operands.

        Returns:
            Steps showing each pairwise GCD and LCM computation.
        """
        operands = data["operands"]
        steps: list[str] = []
        current = operands[0]
        for op in operands[1:]:
            g = math.gcd(current, op)
            lcm_val = (current * op) // g
            steps.append(f"\\gcd({current},{op})={g}")
            steps.append(f"{current}*{op}/{g}={lcm_val}")
            current = lcm_val
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the LCM as a string.

        Args:
            data: Solution data.

        Returns:
            String representation of the LCM.
        """
        return str(data["result"])


@register
class ModPowGenerator(StepGenerator):
    """Modular exponentiation by repeated squaring.

    Generates problems computing a^e mod m using binary exponentiation.
    Shows each squaring step with modular reduction.

    Input format:
        ``compute modular power``

    Target format:
        ``3^{13} \\mod 7 <step> 3^1=3 <step> 3^2=9\\equiv 2 <step>
        3^4=4 <step> 3^8=16\\equiv 2 <step> 3^{13}=3*4*2=24\\equiv 3
        <step> 3``

    Difficulty scaling:
        Difficulty 1-2: base 2-9, exponent 2-10, modulus 3-11.
        Difficulty 3-4: base 2-20, exponent 10-30, modulus 5-23.
        Difficulty 5-6: base 2-50, exponent 20-60, modulus 7-47.
        Difficulty 7-8: base 2-99, exponent 50-120, modulus 11-97.

    Prerequisites:
        exponentiation, modular.

    Example:
        >>> gen = ModPowGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'mod_pow'
    """

    _PARAM_RANGES: dict[int, dict[str, tuple[int, int]]] = {
        1: {"base": (2, 9), "exp": (2, 10), "mod": (3, 11)},
        2: {"base": (2, 9), "exp": (2, 10), "mod": (3, 11)},
        3: {"base": (2, 20), "exp": (10, 30), "mod": (5, 23)},
        4: {"base": (2, 20), "exp": (10, 30), "mod": (5, 23)},
        5: {"base": (2, 50), "exp": (20, 60), "mod": (7, 47)},
        6: {"base": (2, 50), "exp": (20, 60), "mod": (7, 47)},
        7: {"base": (2, 99), "exp": (50, 120), "mod": (11, 97)},
        8: {"base": (2, 99), "exp": (50, 120), "mod": (11, 97)},
    }

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "mod_pow"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 3

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["exponentiation", "modular"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls parameter ranges.

        Returns:
            Natural language description.
        """
        return "compute modular power"

    def _params(self, difficulty: int) -> dict[str, tuple[int, int]]:
        """Return parameter ranges for the given difficulty.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Dict mapping parameter name to (min, max) range.
        """
        return self._PARAM_RANGES.get(difficulty, self._PARAM_RANGES[8])

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a modular exponentiation problem.

        Args:
            difficulty: Controls parameter ranges.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        ranges = self._params(difficulty)
        base = self._rng.randint(*ranges["base"])
        exp = self._rng.randint(*ranges["exp"])
        mod = self._rng.randint(*ranges["mod"])
        result = pow(base, exp, mod)
        squares = self._compute_squares(base, exp, mod)
        return (
            f"{base}^{{{exp}}} \\mod {mod}",
            {"base": base, "exp": exp, "mod": mod,
             "result": result, "squares": squares},
        )

    def _compute_squares(self, base: int, exp: int,
                         mod: int) -> list[tuple[int, int, int]]:
        """Compute the repeated squaring table.

        Args:
            base: Base value.
            exp: Exponent value.
            mod: Modulus value.

        Returns:
            List of (power_of_2, raw_value, reduced_value) tuples.
        """
        squares: list[tuple[int, int, int]] = []
        current = base % mod
        power = 1
        while power <= exp:
            raw = current
            reduced = current % mod
            squares.append((power, raw, reduced))
            current = (reduced * reduced) % mod
            power *= 2
        return squares

    def _create_steps(self, data: dict) -> list[str]:
        """Generate repeated squaring steps.

        Args:
            data: Solution data with squaring table.

        Returns:
            Steps showing each squaring and the final combination.
        """
        steps: list[str] = []
        base = data["base"]
        squares = data["squares"]
        for power, raw, reduced in squares:
            steps.append(self._format_square_step(base, power, raw, reduced))
        steps.append(self._format_combination(data))
        return steps

    def _format_square_step(self, base: int, power: int,
                            raw: int, reduced: int) -> str:
        """Format one squaring step.

        Args:
            base: Original base.
            power: Current power of 2.
            raw: Raw squared value.
            reduced: Value after modular reduction.

        Returns:
            Formatted step string.
        """
        if raw == reduced:
            return f"{base}^{{{power}}}={reduced}"
        return f"{base}^{{{power}}}={raw}\\equiv {reduced}"

    def _format_combination(self, data: dict) -> str:
        """Format the final combination of relevant squares.

        Args:
            data: Solution data.

        Returns:
            Step string showing the product of selected squares.
        """
        exp = data["exp"]
        mod = data["mod"]
        base = data["base"]
        squares = data["squares"]
        used = [(p, r) for p, _, r in squares if exp & p]
        factors = "*".join(str(r) for _, r in used)
        product = 1
        for _, r in used:
            product = (product * r) % mod
        return f"{base}^{{{exp}}}={factors}\\equiv {product} \\mod {mod}"

    def _create_answer(self, data: dict) -> str:
        """Return the modular power result.

        Args:
            data: Solution data.

        Returns:
            String representation of the result.
        """
        return str(data["result"])


@register
class ModInvGenerator(StepGenerator):
    """Modular inverse via the extended Euclidean algorithm.

    Generates problems finding a^{-1} mod m where gcd(a,m)=1.
    Shows the extended Euclidean algorithm steps and back-substitution.

    Input format:
        ``find modular inverse``

    Target format:
        ``3^{-1} \\mod 11 <step> 11=3*3+2 <step> 3=2*1+1 <step>
        back: 1=3-2*1 <step> 1=3-(11-3*3) <step> 4``

    Difficulty scaling:
        Difficulty 1-2: a in [2,9], m in [3,13].
        Difficulty 3-4: a in [2,20], m in [11,47].
        Difficulty 5-6: a in [2,50], m in [23,97].
        Difficulty 7-8: a in [2,99], m in [53,197].

    Prerequisites:
        gcd.

    Example:
        >>> gen = ModInvGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'mod_inv'
    """

    _PARAM_RANGES: dict[int, dict[str, tuple[int, int]]] = {
        1: {"a": (2, 9), "m": (3, 13)},
        2: {"a": (2, 9), "m": (3, 13)},
        3: {"a": (2, 20), "m": (11, 47)},
        4: {"a": (2, 20), "m": (11, 47)},
        5: {"a": (2, 50), "m": (23, 97)},
        6: {"a": (2, 50), "m": (23, 97)},
        7: {"a": (2, 99), "m": (53, 197)},
        8: {"a": (2, 99), "m": (53, 197)},
    }

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "mod_inv"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 3

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["gcd"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls parameter ranges.

        Returns:
            Natural language description.
        """
        return "find modular inverse"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a modular inverse problem with coprime a and m.

        Uses rejection sampling to ensure gcd(a,m)=1.

        Args:
            difficulty: Controls parameter ranges.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        ranges = self._PARAM_RANGES.get(difficulty, self._PARAM_RANGES[8])
        a, m = self._sample_coprime(ranges)
        inv = pow(a, -1, m)
        euc_steps, back_steps = self._extended_euclidean(m, a)
        return (
            f"{a}^{{-1}} \\mod {m}",
            {"a": a, "m": m, "inv": inv,
             "euc_steps": euc_steps, "back_steps": back_steps},
        )

    def _sample_coprime(self, ranges: dict[str, tuple[int, int]]
                        ) -> tuple[int, int]:
        """Sample a and m such that gcd(a,m)=1 by rejection.

        Args:
            ranges: Parameter ranges for a and m.

        Returns:
            Tuple of (a, m) with gcd(a,m)=1.
        """
        while True:
            a = self._rng.randint(*ranges["a"])
            m = self._rng.randint(*ranges["m"])
            if m > a and math.gcd(a, m) == 1:
                return a, m

    def _extended_euclidean(self, m: int, a: int
                           ) -> tuple[list[str], list[str]]:
        """Run extended Euclidean algorithm and back-substitution.

        Args:
            m: Modulus.
            a: Value to invert.

        Returns:
            Tuple of (forward_steps, back_substitution_steps).
        """
        forward: list[str] = []
        equations: list[tuple[int, int, int, int]] = []
        r0, r1 = m, a
        while r1 > 0:
            q, r = divmod(r0, r1)
            forward.append(f"{r0}={r1}*{q}+{r}")
            equations.append((r0, r1, q, r))
            r0, r1 = r1, r
        back_steps = self._back_substitute(equations)
        return forward, back_steps

    def _back_substitute(self, equations: list[tuple[int, int, int, int]]
                         ) -> list[str]:
        """Perform back-substitution on Euclidean equations.

        Args:
            equations: List of (dividend, divisor, quotient, remainder) tuples.

        Returns:
            Back-substitution step strings.
        """
        if len(equations) < 2:
            return ["back: 1=1"]
        steps: list[str] = []
        r0, r1, q, _ = equations[-2]
        steps.append(f"back: 1={r0}-{r1}*{q}")
        return steps

    def _create_steps(self, data: dict) -> list[str]:
        """Generate extended Euclidean steps.

        Args:
            data: Solution data with forward and back steps.

        Returns:
            Combined forward and backward steps.
        """
        return data["euc_steps"] + data["back_steps"]

    def _create_answer(self, data: dict) -> str:
        """Return the modular inverse.

        Args:
            data: Solution data.

        Returns:
            String representation of the modular inverse.
        """
        return str(data["inv"])


@register
class IntegralGenerator(StepGenerator):
    """Polynomial integration using the reverse power rule.

    Generates antiderivative problems by first constructing a polynomial
    with integer coefficients (the antiderivative), then differentiating
    to get the integrand. The model must reverse the process.

    Input format:
        ``integrate polynomial``

    Target format:
        ``\\int 6x+2 dx <step> \\frac{6}{2}x^2=3x^2 <step>
        \\frac{2}{1}x=2x <step> 3x^2+2x+c``

    Difficulty scaling:
        Difficulty 1-2: 2 terms, coefficients 1-5.
        Difficulty 3-4: 3 terms, coefficients 1-10.
        Difficulty 5-6: 4 terms, coefficients 1-15.
        Difficulty 7-8: 5 terms, coefficients 1-20.

    Prerequisites:
        derivative.

    Example:
        >>> gen = IntegralGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'integral'
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "integral"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 3

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["derivative"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls term count and coefficient range.

        Returns:
            Natural language description.
        """
        return "integrate polynomial"

    def _term_count(self, difficulty: int) -> int:
        """Map difficulty to number of terms in the antiderivative.

        Args:
            difficulty: Difficulty level.

        Returns:
            Number of terms.
        """
        return min(2 + (difficulty - 1) // 2, 5)

    def _coeff_range(self, difficulty: int) -> tuple[int, int]:
        """Map difficulty to coefficient magnitude range.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (min_coeff, max_coeff).
        """
        return 1, 5 + difficulty * 2

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an integration problem from an antiderivative.

        Constructs an antiderivative with integer coefficients, then
        differentiates to produce the integrand.

        Args:
            difficulty: Controls complexity.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        antiderivative = self._build_antiderivative(difficulty)
        integrand = antiderivative.differentiate()
        return (
            f"\\int {integrand.to_latex()} dx",
            {"integrand": integrand, "antiderivative": antiderivative},
        )

    def _build_antiderivative(self, difficulty: int) -> PolynomialHelper:
        """Build a polynomial to serve as the antiderivative.

        Each term has integer coefficient and power from n_terms down to 1.

        Args:
            difficulty: Controls term count and coefficient range.

        Returns:
            PolynomialHelper representing the antiderivative.
        """
        n = self._term_count(difficulty)
        lo, hi = self._coeff_range(difficulty)
        terms: list[tuple[int, int]] = []
        for power in range(n, 0, -1):
            coeff = self._rng.randint(lo, hi)
            terms.append((coeff, power))
        return PolynomialHelper(terms)

    def _create_steps(self, data: dict) -> list[str]:
        """Generate reverse power rule steps for each term.

        Args:
            data: Solution data with integrand and antiderivative.

        Returns:
            Steps showing each term's integration.
        """
        integrand = data["integrand"]
        antiderivative = data["antiderivative"]
        steps: list[str] = []
        for (ic, ip), (ac, ap) in zip(integrand.terms, antiderivative.terms):
            steps.append(self._format_integration_step(ic, ip, ac, ap))
        return steps

    def _format_integration_step(self, int_coeff: int, int_power: int,
                                 anti_coeff: int, anti_power: int) -> str:
        """Format one term's integration step.

        Args:
            int_coeff: Integrand term coefficient.
            int_power: Integrand term power.
            anti_coeff: Antiderivative term coefficient.
            anti_power: Antiderivative term power.

        Returns:
            Step string showing the reverse power rule application.
        """
        new_power = int_power + 1
        x_part = "x" if anti_power == 1 else f"x^{anti_power}"
        return f"\\frac{{{int_coeff}}}{{{new_power}}}{x_part}={anti_coeff}{x_part}"

    def _create_answer(self, data: dict) -> str:
        """Return the antiderivative with constant of integration.

        Args:
            data: Solution data.

        Returns:
            Antiderivative in LaTeX plus '+c'.
        """
        return f"{data['antiderivative'].to_latex()}+c"


@register
class SecondDerivativeGenerator(StepGenerator):
    """Second derivative computation by applying the power rule twice.

    Generates a polynomial of degree >= 2, computes f', then f'',
    showing each differentiation as a separate step.

    Input format:
        ``find second derivative``

    Target format:
        ``\\frac{d^2}{dx^2}(x^3+2x^2) <step> f'=3x^2+4x <step>
        f''=6x+4 <step> 6x+4``

    Difficulty scaling:
        Difficulty 1-2: degree 2, coefficients 1-5.
        Difficulty 3-4: degree 3, coefficients 1-10.
        Difficulty 5-6: degree 4, coefficients 1-15.
        Difficulty 7-8: degree 5, coefficients 1-20.

    Prerequisites:
        derivative.

    Example:
        >>> gen = SecondDerivativeGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'second_derivative'
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "second_derivative"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 3

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["derivative"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls polynomial degree.

        Returns:
            Natural language description.
        """
        return "find second derivative"

    def _degree(self, difficulty: int) -> int:
        """Map difficulty to polynomial degree (minimum 2).

        Args:
            difficulty: Difficulty level.

        Returns:
            Polynomial degree.
        """
        return min(2 + (difficulty - 1) // 2, 5)

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a polynomial and compute its second derivative.

        Args:
            difficulty: Controls degree and coefficient range.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        poly = self._build_polynomial(difficulty)
        first = poly.differentiate()
        second = first.differentiate()
        return (
            f"\\frac{{d^2}}{{dx^2}}({poly.to_latex()})",
            {"poly": poly, "first": first, "second": second},
        )

    def _build_polynomial(self, difficulty: int) -> PolynomialHelper:
        """Build a polynomial with the target degree.

        Args:
            difficulty: Controls degree and coefficient range.

        Returns:
            PolynomialHelper instance.
        """
        deg = self._degree(difficulty)
        hi = 5 + difficulty * 2
        terms: list[tuple[int, int]] = []
        for power in range(deg, 0, -1):
            coeff = self._rng.randint(1, hi)
            terms.append((coeff, power))
        return PolynomialHelper(terms)

    def _create_steps(self, data: dict) -> list[str]:
        """Generate two differentiation steps.

        Args:
            data: Solution data with polynomial and derivatives.

        Returns:
            Steps showing f' and f''.
        """
        return [
            f"f'={data['first'].to_latex()}",
            f"f''={data['second'].to_latex()}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the second derivative.

        Args:
            data: Solution data.

        Returns:
            LaTeX string of the second derivative.
        """
        return data["second"].to_latex()


@register
class SystemEquationsGenerator(StepGenerator):
    """Solve 2x2 linear systems with integer solutions.

    Generates a system of two equations in two unknowns by first
    choosing integer solutions x and y, then constructing a
    non-singular coefficient matrix. Uses elimination to solve.

    Input format:
        ``solve system of two equations``

    Target format:
        ``2x+y=7; x-y=1 <step> add: 3x=8 <step> x=\\frac{8}{3}...``

    Difficulty scaling:
        Difficulty 1-2: coefficients 1-5, solutions -5 to 5.
        Difficulty 3-4: coefficients 1-10, solutions -10 to 10.
        Difficulty 5-6: coefficients 1-15, solutions -15 to 15.
        Difficulty 7-8: coefficients 1-20, solutions -20 to 20.

    Prerequisites:
        linear_equation, multiplication.

    Example:
        >>> gen = SystemEquationsGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'system_equations'
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "system_equations"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 3

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["linear_equation", "multiplication"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls coefficient and solution ranges.

        Returns:
            Natural language description.
        """
        return "solve system of two equations"

    def _range_for_difficulty(self, difficulty: int) -> int:
        """Map difficulty to coefficient/solution magnitude.

        Args:
            difficulty: Difficulty level.

        Returns:
            Maximum absolute value for coefficients and solutions.
        """
        return 5 + (difficulty - 1) * 2

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a 2x2 linear system with integer solutions.

        Constructs the system backwards from chosen solutions to
        guarantee integer answers and a non-singular matrix.

        Args:
            difficulty: Controls coefficient magnitude.

        Returns:
            Tuple of (system_string, solution_data).
        """
        bound = self._range_for_difficulty(difficulty)
        x_val = self._rng.randint(-bound, bound)
        y_val = self._rng.randint(-bound, bound)
        a1, b1, a2, b2 = self._non_singular_coeffs(bound)
        c1 = a1 * x_val + b1 * y_val
        c2 = a2 * x_val + b2 * y_val
        eq1 = self._format_equation(a1, b1, c1)
        eq2 = self._format_equation(a2, b2, c2)
        return (
            f"{eq1}; {eq2}",
            {"a1": a1, "b1": b1, "c1": c1,
             "a2": a2, "b2": b2, "c2": c2,
             "x": x_val, "y": y_val},
        )

    def _non_singular_coeffs(self, bound: int) -> tuple[int, int, int, int]:
        """Generate non-singular coefficient matrix by rejection.

        Args:
            bound: Maximum absolute coefficient value.

        Returns:
            Tuple (a1, b1, a2, b2) with a1*b2 - a2*b1 != 0.
        """
        while True:
            a1 = self._rng.randint(1, bound)
            b1 = self._rng.randint(-bound, bound)
            a2 = self._rng.randint(1, bound)
            b2 = self._rng.randint(-bound, bound)
            if a1 * b2 - a2 * b1 != 0:
                return a1, b1, a2, b2

    def _format_equation(self, a: int, b: int, c: int) -> str:
        """Format one equation as ax+by=c.

        Args:
            a: Coefficient of x.
            b: Coefficient of y.
            c: Right-hand side constant.

        Returns:
            Formatted equation string.
        """
        b_sign = "+" if b >= 0 else ""
        return f"{a}x{b_sign}{b}y={c}"

    def _create_steps(self, data: dict) -> list[str]:
        """Generate elimination steps to solve the system.

        Uses the first equation to eliminate x from the second.

        Args:
            data: Solution data with coefficients and solutions.

        Returns:
            Steps showing elimination, substitution, and solution.
        """
        a1, b1, c1 = data["a1"], data["b1"], data["c1"]
        a2, b2, c2 = data["a2"], data["b2"], data["c2"]
        x_val, y_val = data["x"], data["y"]
        return self._elimination_steps(a1, b1, c1, a2, b2, c2, x_val, y_val)

    def _elimination_steps(self, a1: int, b1: int, c1: int,
                           a2: int, b2: int, c2: int,
                           x_val: int, y_val: int) -> list[str]:
        """Perform variable elimination and record steps.

        Args:
            a1: Eq1 x-coefficient.
            b1: Eq1 y-coefficient.
            c1: Eq1 constant.
            a2: Eq2 x-coefficient.
            b2: Eq2 y-coefficient.
            c2: Eq2 constant.
            x_val: Solution for x.
            y_val: Solution for y.

        Returns:
            Step strings for the elimination process.
        """
        new_b = b2 * a1 - b1 * a2
        new_c = c2 * a1 - c1 * a2
        steps: list[str] = []
        steps.append(f"eliminate x: {new_b}y={new_c}")
        steps.append(f"y={y_val}")
        steps.append(f"substitute: {a1}x+{b1}*{y_val}={c1}")
        steps.append(f"x={x_val}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the solution pair.

        Args:
            data: Solution data.

        Returns:
            String like 'x=3, y=-2'.
        """
        return f"x={data['x']}, y={data['y']}"


@register
class DeterminantGenerator(StepGenerator):
    """Matrix determinant computation for 2x2 and 3x3 matrices.

    Generates random integer matrices and shows the determinant
    calculation. Uses ad-bc for 2x2 and cofactor expansion along
    the first row for 3x3.

    Input format:
        ``compute matrix determinant``

    Target format:
        ``\\det\\begin{pmatrix} 3 & 1 \\\\ 5 & 2 \\end{pmatrix} <step>
        3*2-1*5=1 <step> 1``

    Difficulty scaling:
        Difficulty 1-4: 2x2 matrices, entries in [-5*d, 5*d].
        Difficulty 5-8: 3x3 matrices with cofactor expansion.

    Prerequisites:
        multiplication, subtraction.

    Example:
        >>> gen = DeterminantGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'determinant'
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "determinant"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 3

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["multiplication", "subtraction"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls matrix size.

        Returns:
            Natural language description.
        """
        return "compute matrix determinant"

    def _matrix_size(self, difficulty: int) -> int:
        """Determine matrix dimension from difficulty.

        Args:
            difficulty: Difficulty level.

        Returns:
            Matrix size (2 or 3).
        """
        if difficulty >= 5:
            return 3
        return 2

    def _entry_bound(self, difficulty: int) -> int:
        """Determine matrix entry magnitude bound.

        Args:
            difficulty: Difficulty level.

        Returns:
            Maximum absolute entry value.
        """
        return 5 * difficulty

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a matrix and compute its determinant.

        Args:
            difficulty: Controls matrix size and entry range.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        size = self._matrix_size(difficulty)
        bound = self._entry_bound(difficulty)
        matrix = self._random_matrix(size, bound)
        helper = MatrixHelper(matrix)
        det = helper.determinant()
        return (
            f"\\det{helper.to_latex()}",
            {"matrix": matrix, "size": size, "det": det},
        )

    def _random_matrix(self, size: int, bound: int) -> list[list[int]]:
        """Generate a random square integer matrix.

        Args:
            size: Matrix dimension.
            bound: Maximum absolute entry value.

        Returns:
            2D list of integers.
        """
        return [
            [self._rng.randint(-bound, bound) for _ in range(size)]
            for _ in range(size)
        ]

    def _create_steps(self, data: dict) -> list[str]:
        """Generate determinant computation steps.

        Args:
            data: Solution data with matrix and size.

        Returns:
            Steps showing the computation.
        """
        if data["size"] == 2:
            return self._steps_2x2(data["matrix"])
        return self._steps_3x3(data["matrix"])

    def _steps_2x2(self, m: list[list[int]]) -> list[str]:
        """Generate steps for a 2x2 determinant.

        Args:
            m: 2x2 matrix.

        Returns:
            Single step showing ad-bc=result.
        """
        det = m[0][0] * m[1][1] - m[0][1] * m[1][0]
        return [f"{m[0][0]}*{m[1][1]}-{m[0][1]}*{m[1][0]}={det}"]

    def _steps_3x3(self, m: list[list[int]]) -> list[str]:
        """Generate cofactor expansion steps for a 3x3 determinant.

        Args:
            m: 3x3 matrix.

        Returns:
            Steps showing each cofactor and the final sum.
        """
        steps: list[str] = []
        cofactors: list[int] = []
        for j in range(3):
            sign = (-1) ** j
            minor = MatrixHelper(m)._minor(0, j)
            minor_det = minor.determinant()
            cofactor = sign * m[0][j] * minor_det
            cofactors.append(cofactor)
            sign_str = "+" if sign > 0 else "-"
            steps.append(
                f"C_{{{j}}}={sign_str}{m[0][j]}*{minor_det}={cofactor}"
            )
        det = sum(cofactors)
        terms = "+".join(str(c) for c in cofactors).replace("+-", "-")
        steps.append(f"det={terms}={det}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the determinant value.

        Args:
            data: Solution data.

        Returns:
            String representation of the determinant.
        """
        return str(data["det"])


@register
class CollatzGenerator(StepGenerator):
    """Collatz sequence step counting to reach 1.

    Generates a starting number and shows each step of the Collatz
    sequence: if even divide by 2, if odd multiply by 3 and add 1.
    Counts total steps to reach 1.

    Input format:
        ``count collatz steps to reach 1``

    Target format:
        ``\\text{collatz}(7) <step> 7*3+1=22 <step> 22/2=11 <step>
        11*3+1=34 <step> ... <step> 16``

    Difficulty scaling:
        Difficulty 1-2: start in [3, 15].
        Difficulty 3-4: start in [10, 50].
        Difficulty 5-6: start in [30, 150].
        Difficulty 7-8: start in [100, 500].

    Prerequisites:
        division, multiplication.

    Example:
        >>> gen = CollatzGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'collatz'
    """

    _START_RANGES: dict[int, tuple[int, int]] = {
        1: (3, 15), 2: (3, 15),
        3: (10, 50), 4: (10, 50),
        5: (30, 150), 6: (30, 150),
        7: (100, 500), 8: (100, 500),
    }

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "collatz"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 3

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["division", "multiplication"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls starting number range.

        Returns:
            Natural language description.
        """
        return "count collatz steps to reach 1"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Collatz problem with a starting number.

        Args:
            difficulty: Controls starting number range.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        lo, hi = self._START_RANGES.get(difficulty, self._START_RANGES[8])
        start = self._rng.randint(lo, hi)
        sequence = self._compute_sequence(start)
        return (
            f"\\text{{collatz}}({start})",
            {"start": start, "sequence": sequence},
        )

    def _compute_sequence(self, n: int) -> list[int]:
        """Compute the full Collatz sequence from n to 1.

        Args:
            n: Starting value.

        Returns:
            List of values in the sequence including n and 1.
        """
        seq = [n]
        while n != 1:
            n = self._next_collatz(n)
            seq.append(n)
        return seq

    def _next_collatz(self, n: int) -> int:
        """Compute the next value in the Collatz sequence.

        Args:
            n: Current value.

        Returns:
            Next value (n/2 if even, 3n+1 if odd).
        """
        if n % 2 == 0:
            return n // 2
        return 3 * n + 1

    def _create_steps(self, data: dict) -> list[str]:
        """Generate step descriptions for each Collatz transition.

        Args:
            data: Solution data with the full sequence.

        Returns:
            Steps showing each odd/even operation.
        """
        seq = data["sequence"]
        steps: list[str] = []
        for i in range(len(seq) - 1):
            steps.append(self._format_collatz_step(seq[i], seq[i + 1]))
        return steps

    def _format_collatz_step(self, current: int, next_val: int) -> str:
        """Format one Collatz step.

        Args:
            current: Current sequence value.
            next_val: Next sequence value.

        Returns:
            Step string showing the operation.
        """
        if current % 2 == 0:
            return f"{current}/2={next_val}"
        return f"{current}*3+1={next_val}"

    def _create_answer(self, data: dict) -> str:
        """Return the step count to reach 1.

        Args:
            data: Solution data.

        Returns:
            Number of steps as a string.
        """
        return str(len(data["sequence"]) - 1)


@register
class BaseConversionGenerator(StepGenerator):
    """Decimal to base-N conversion with repeated division.

    Converts a decimal number to a target base by repeated division,
    showing each quotient and remainder. Uses a-f for hex digits.

    Input format:
        ``convert decimal to base``

    Target format:
        ``255 \\to base 16 <step> 255/16=15r15 <step> 15/16=0r15
        <step> ff``

    Difficulty scaling:
        Difficulty 1-2: number 2-99, bases 2-8.
        Difficulty 3-4: number 10-999, bases 2-16.
        Difficulty 5-6: number 100-9999, bases 2-16.
        Difficulty 7-8: number 1000-65535, bases 2-16.

    Prerequisites:
        division, modular.

    Example:
        >>> gen = BaseConversionGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'base_conversion'
    """

    _DIGITS = "0123456789abcdef"

    _PARAM_RANGES: dict[int, dict[str, tuple[int, int]]] = {
        1: {"num": (2, 99), "base": (2, 8)},
        2: {"num": (2, 99), "base": (2, 8)},
        3: {"num": (10, 999), "base": (2, 16)},
        4: {"num": (10, 999), "base": (2, 16)},
        5: {"num": (100, 9999), "base": (2, 16)},
        6: {"num": (100, 9999), "base": (2, 16)},
        7: {"num": (1000, 65535), "base": (2, 16)},
        8: {"num": (1000, 65535), "base": (2, 16)},
    }

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "base_conversion"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 3

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["division", "modular"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls number and base ranges.

        Returns:
            Natural language description.
        """
        return "convert decimal to base"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a base conversion problem.

        Args:
            difficulty: Controls number and base ranges.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        ranges = self._PARAM_RANGES.get(difficulty, self._PARAM_RANGES[8])
        num = self._rng.randint(*ranges["num"])
        base = self._rng.randint(*ranges["base"])
        digits, div_steps = self._convert(num, base)
        return (
            f"{num} \\to base {base}",
            {"num": num, "base": base, "digits": digits,
             "div_steps": div_steps},
        )

    def _convert(self, num: int, base: int
                 ) -> tuple[list[int], list[tuple[int, int, int]]]:
        """Convert a number to the target base by repeated division.

        Args:
            num: Decimal number to convert.
            base: Target base.

        Returns:
            Tuple of (digit_list_msd_first, division_step_tuples).
        """
        digits: list[int] = []
        steps: list[tuple[int, int, int]] = []
        current = num
        while current > 0:
            q, r = divmod(current, base)
            steps.append((current, q, r))
            digits.append(r)
            current = q
        digits.reverse()
        return digits, steps

    def _create_steps(self, data: dict) -> list[str]:
        """Generate division steps for base conversion.

        Args:
            data: Solution data with division steps.

        Returns:
            Steps showing each division.
        """
        base = data["base"]
        return [
            f"{n}/{base}={q}r{r}"
            for n, q, r in data["div_steps"]
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the number in the target base.

        Args:
            data: Solution data.

        Returns:
            String representation in the target base using a-f for hex.
        """
        return "".join(self._DIGITS[d] for d in data["digits"])


@register
class PermutationGenerator(StepGenerator):
    """Permutation count P(n,r) = n!/(n-r)!.

    Computes the number of r-permutations from n elements by
    multiplying n * (n-1) * ... * (n-r+1).

    Input format:
        ``compute permutation count``

    Target format:
        ``P(7,3) <step> 7*6*5 <step> 210``

    Difficulty scaling:
        Difficulty 1-2: n in [4,7], r in [2,3].
        Difficulty 3-4: n in [6,10], r in [3,5].
        Difficulty 5-6: n in [8,15], r in [4,6].
        Difficulty 7-8: n in [10,20], r in [5,8].

    Prerequisites:
        multiplication.

    Example:
        >>> gen = PermutationGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'permutation'
    """

    _PARAM_RANGES: dict[int, dict[str, tuple[int, int]]] = {
        1: {"n": (4, 7), "r": (2, 3)},
        2: {"n": (4, 7), "r": (2, 3)},
        3: {"n": (6, 10), "r": (3, 5)},
        4: {"n": (6, 10), "r": (3, 5)},
        5: {"n": (8, 15), "r": (4, 6)},
        6: {"n": (8, 15), "r": (4, 6)},
        7: {"n": (10, 20), "r": (5, 8)},
        8: {"n": (10, 20), "r": (5, 8)},
    }

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "permutation"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 3

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["multiplication"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls n and r ranges.

        Returns:
            Natural language description.
        """
        return "compute permutation count"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a permutation count problem.

        Args:
            difficulty: Controls n and r ranges.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        ranges = self._PARAM_RANGES.get(difficulty, self._PARAM_RANGES[8])
        n = self._rng.randint(*ranges["n"])
        r = self._rng.randint(*ranges["r"])
        r = min(r, n)
        factors = list(range(n, n - r, -1))
        result = 1
        for f in factors:
            result *= f
        return f"P({n},{r})", {"n": n, "r": r, "factors": factors, "result": result}

    def _create_steps(self, data: dict) -> list[str]:
        """Generate the multiplication chain step.

        Args:
            data: Solution data with factors.

        Returns:
            Step showing the factor product.
        """
        factors = data["factors"]
        return ["*".join(str(f) for f in factors)]

    def _create_answer(self, data: dict) -> str:
        """Return the permutation count.

        Args:
            data: Solution data.

        Returns:
            String representation of P(n,r).
        """
        return str(data["result"])


@register
class PrefixScanGenerator(StepGenerator):
    """Inclusive prefix scan with addition or multiplication.

    Generates a list of integers and computes the inclusive prefix scan
    (cumulative fold), showing each accumulation step.

    Input format:
        ``compute prefix scan``

    Target format:
        ``scan(5,3,8,2,+) <step> 5 <step> 5+3=8 <step> 8+8=16
        <step> 16+2=18 <step> 5,8,16,18``

    Difficulty scaling:
        Difficulty 1-2: 3-4 elements, addition only.
        Difficulty 3-4: 4-6 elements, addition or multiplication.
        Difficulty 5-6: 5-8 elements, addition or multiplication.
        Difficulty 7-8: 7-10 elements, addition or multiplication.

    Prerequisites:
        addition, multiplication.

    Example:
        >>> gen = PrefixScanGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'prefix_scan'
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "prefix_scan"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 3

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["addition", "multiplication"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls list length and operation.

        Returns:
            Natural language description.
        """
        return "compute prefix scan"

    def _list_length(self, difficulty: int) -> int:
        """Map difficulty to input list length.

        Args:
            difficulty: Difficulty level.

        Returns:
            Number of elements in the input list.
        """
        return min(3 + difficulty, 10)

    def _choose_op(self, difficulty: int) -> str:
        """Choose the scan operation based on difficulty.

        Args:
            difficulty: Difficulty level.

        Returns:
            Operation symbol ('+' or '*').
        """
        if difficulty <= 2:
            return "+"
        return self._rng.choice(["+", "*"])

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a prefix scan problem.

        Args:
            difficulty: Controls list length and operation.

        Returns:
            Tuple of (problem_string, solution_data).
        """
        length = self._list_length(difficulty)
        op = self._choose_op(difficulty)
        nums = self._generate_values(length, op)
        scan_result = self._compute_scan(nums, op)
        label = ",".join(str(x) for x in nums)
        return (
            f"scan({label},{op})",
            {"nums": nums, "op": op, "scan": scan_result},
        )

    def _generate_values(self, length: int, op: str) -> list[int]:
        """Generate input values appropriate for the operation.

        Args:
            length: Number of elements.
            op: Operation ('+' or '*').

        Returns:
            List of random integers.
        """
        if op == "*":
            return [self._rng.randint(1, 5) for _ in range(length)]
        return [self._rng.randint(1, 20) for _ in range(length)]

    def _compute_scan(self, nums: list[int], op: str) -> list[int]:
        """Compute the inclusive prefix scan.

        Args:
            nums: Input values.
            op: Operation to apply.

        Returns:
            List of cumulative results.
        """
        result: list[int] = [nums[0]]
        for i in range(1, len(nums)):
            result.append(self._apply_op(result[-1], nums[i], op))
        return result

    def _apply_op(self, a: int, b: int, op: str) -> int:
        """Apply the binary operation.

        Args:
            a: Left operand.
            b: Right operand.
            op: Operation symbol.

        Returns:
            Result of a op b.
        """
        if op == "*":
            return a * b
        return a + b

    def _create_steps(self, data: dict) -> list[str]:
        """Generate accumulation steps.

        Args:
            data: Solution data with values and scan results.

        Returns:
            Steps showing each accumulation.
        """
        nums = data["nums"]
        scan = data["scan"]
        op = data["op"]
        steps: list[str] = [str(nums[0])]
        for i in range(1, len(nums)):
            steps.append(f"{scan[i-1]}{op}{nums[i]}={scan[i]}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the prefix scan result as comma-separated values.

        Args:
            data: Solution data.

        Returns:
            Comma-separated scan result.
        """
        return ",".join(str(x) for x in data["scan"])


@register
class RPNGenerator(StepGenerator):
    """Reverse Polish Notation stack evaluation.

    Generates RPN expressions using +, -, * and shows the stack-based
    evaluation step by step: push operands, pop and apply operators.

    Input format:
        ``evaluate reverse polish notation``

    Target format:
        ``3 4 + 2 * <step> push 3 <step> push 4 <step> 3+4=7
        <step> push 2 <step> 7*2=14 <step> 14``

    Difficulty scaling:
        Difficulty 1-2: 2 operators (3 operands).
        Difficulty 3-4: 3-4 operators.
        Difficulty 5-6: 4-5 operators.
        Difficulty 7-8: 5-6 operators.

    Prerequisites:
        addition, subtraction, multiplication.

    Example:
        >>> gen = RPNGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'rpn'
    """

    _OPS = ["+", "-", "*"]

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "rpn"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 3

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["addition", "subtraction", "multiplication"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls expression complexity.

        Returns:
            Natural language description.
        """
        return "evaluate reverse polish notation"

    def _op_count(self, difficulty: int) -> int:
        """Map difficulty to number of operators.

        Args:
            difficulty: Difficulty level.

        Returns:
            Number of binary operators in the expression.
        """
        return min(2 + (difficulty - 1) // 2, 6)

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an RPN expression and evaluate it.

        Builds a valid RPN expression by interleaving operands and
        operators such that the stack depth never goes below 2 before
        an operator is applied.

        Args:
            difficulty: Controls expression complexity.

        Returns:
            Tuple of (rpn_string, solution_data).
        """
        n_ops = self._op_count(difficulty)
        tokens, eval_steps, result = self._build_expression(n_ops)
        expr_str = " ".join(str(t) for t in tokens)
        return expr_str, {"tokens": tokens, "eval_steps": eval_steps, "result": result}

    def _build_expression(self, n_ops: int
                          ) -> tuple[list, list[str], int]:
        """Build a valid RPN expression with evaluation trace.

        Args:
            n_ops: Number of operators to include.

        Returns:
            Tuple of (token_list, evaluation_steps, final_result).
        """
        tokens: list = []
        stack: list[int] = []
        steps: list[str] = []
        ops_remaining = n_ops

        for _ in range(n_ops + 1):
            val = self._rng.randint(1, 9)
            tokens.append(val)
            stack.append(val)
            steps.append(f"push {val}")

            while ops_remaining > 0 and len(stack) >= 2 and self._should_apply_op(stack, ops_remaining):
                op = self._rng.choice(self._OPS)
                tokens.append(op)
                b = stack.pop()
                a = stack.pop()
                result = self._eval_op(a, b, op)
                steps.append(f"{a}{op}{b}={result}")
                stack.append(result)
                ops_remaining -= 1

        while ops_remaining > 0 and len(stack) >= 2:
            op = self._rng.choice(self._OPS)
            tokens.append(op)
            b = stack.pop()
            a = stack.pop()
            result = self._eval_op(a, b, op)
            steps.append(f"{a}{op}{b}={result}")
            stack.append(result)
            ops_remaining -= 1

        return tokens, steps, stack[0]

    def _should_apply_op(self, stack: list[int],
                         ops_remaining: int) -> bool:
        """Decide whether to apply an operator now.

        Args:
            stack: Current evaluation stack.
            ops_remaining: Number of operators still to place.

        Returns:
            True if an operator should be applied.
        """
        if len(stack) > ops_remaining + 1:
            return True
        return self._rng.random() < 0.4

    def _eval_op(self, a: int, b: int, op: str) -> int:
        """Evaluate a binary operation.

        Args:
            a: Left operand.
            b: Right operand.
            op: Operator symbol.

        Returns:
            Result of the operation.
        """
        if op == "+":
            return a + b
        if op == "-":
            return a - b
        return a * b

    def _create_steps(self, data: dict) -> list[str]:
        """Return the pre-computed evaluation steps.

        Args:
            data: Solution data with evaluation trace.

        Returns:
            Steps showing pushes and operations.
        """
        return data["eval_steps"]

    def _create_answer(self, data: dict) -> str:
        """Return the final stack value.

        Args:
            data: Solution data.

        Returns:
            String representation of the result.
        """
        return str(data["result"])


@register
class CycleDetectGenerator(StepGenerator):
    """Directed graph cycle detection via DFS.

    Generates directed graphs with a 50/50 chance of containing
    a cycle. Shows the DFS traversal path and reports whether
    a cycle was found.

    Input format:
        ``detect cycle in directed graph``

    Target format:
        ``a:b;b:c;c:a;d:e;e: <step> visit a->b->c->a: cycle found <step> yes``

    Difficulty scaling:
        Difficulty 1-2: 3-4 nodes.
        Difficulty 3-4: 4-6 nodes.
        Difficulty 5-6: 5-8 nodes.
        Difficulty 7-8: 7-10 nodes.

    Prerequisites:
        graph_reach.

    Example:
        >>> gen = CycleDetectGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'cycle_detect'
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "cycle_detect"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 3

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["graph_reach"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls graph size.

        Returns:
            Natural language description.
        """
        return "detect cycle in directed graph"

    def _node_count(self, difficulty: int) -> int:
        """Map difficulty to number of graph nodes.

        Args:
            difficulty: Difficulty level.

        Returns:
            Number of nodes.
        """
        return min(3 + difficulty, 10)

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a directed graph with or without a cycle.

        Uses a 50/50 split between cyclic and acyclic graphs.

        Args:
            difficulty: Controls graph size.

        Returns:
            Tuple of (edge_list_string, solution_data).
        """
        n = self._node_count(difficulty)
        has_cycle = self._rng.random() < 0.5
        if has_cycle:
            adj = self._build_cyclic_graph(n)
        else:
            adj = self._build_acyclic_graph(n)
        graph = GraphHelper(adj)
        return graph.to_edge_string(), {"graph": graph, "has_cycle": graph.has_cycle()}

    def _node_names(self, n: int) -> list[str]:
        """Generate single-letter node names.

        Args:
            n: Number of nodes.

        Returns:
            List of node name strings.
        """
        return [chr(97 + i) for i in range(n)]

    def _build_cyclic_graph(self, n: int) -> dict[str, list[str]]:
        """Build a directed graph guaranteed to contain a cycle.

        Creates a cycle among a subset of nodes, plus random extra edges.

        Args:
            n: Number of nodes.

        Returns:
            Adjacency list with at least one cycle.
        """
        names = self._node_names(n)
        adj: dict[str, list[str]] = {name: [] for name in names}
        cycle_len = self._rng.randint(2, min(n, 4))
        cycle_nodes = self._rng.sample(names, cycle_len)
        for i in range(cycle_len):
            adj[cycle_nodes[i]].append(cycle_nodes[(i + 1) % cycle_len])
        self._add_random_edges(adj, names, n // 2)
        return adj

    def _build_acyclic_graph(self, n: int) -> dict[str, list[str]]:
        """Build a directed acyclic graph.

        Edges only go from lower-index to higher-index nodes.

        Args:
            n: Number of nodes.

        Returns:
            Adjacency list guaranteed to be acyclic.
        """
        names = self._node_names(n)
        adj: dict[str, list[str]] = {name: [] for name in names}
        for i in range(n - 1):
            for j in range(i + 1, n):
                if self._rng.random() < 0.4:
                    adj[names[i]].append(names[j])
        return adj

    def _add_random_edges(self, adj: dict[str, list[str]],
                          names: list[str], count: int) -> None:
        """Add random edges to a graph (may create additional cycles).

        Args:
            adj: Adjacency list to modify in place.
            names: Node names.
            count: Number of edges to attempt to add.
        """
        for _ in range(count):
            src = self._rng.choice(names)
            dst = self._rng.choice(names)
            if src != dst and dst not in adj[src]:
                adj[src].append(dst)

    def _create_steps(self, data: dict) -> list[str]:
        """Generate DFS traversal steps.

        Args:
            data: Solution data with graph and cycle status.

        Returns:
            Steps showing DFS path and cycle detection result.
        """
        graph = data["graph"]
        if data["has_cycle"]:
            cycle = graph.find_cycle_path()
            path_str = "->".join(cycle)
            return [f"visit {path_str}: cycle found"]
        return [self._format_acyclic_traversal(graph)]

    def _format_acyclic_traversal(self, graph: GraphHelper) -> str:
        """Format a DFS traversal showing no cycle.

        Args:
            graph: The graph to traverse.

        Returns:
            Step string showing visited nodes and no-cycle result.
        """
        visited: list[str] = []
        seen: set[str] = set()
        for node in sorted(graph.adjacency):
            if node not in seen:
                self._dfs_order(graph, node, seen, visited)
        path_str = "->".join(visited)
        return f"visit {path_str}: no cycle"

    def _dfs_order(self, graph: GraphHelper, node: str,
                   seen: set[str], visited: list[str]) -> None:
        """Record DFS traversal order.

        Args:
            graph: The graph.
            node: Current node.
            seen: Set of already-visited nodes.
            visited: Ordered list of visited nodes.
        """
        if node in seen:
            return
        seen.add(node)
        visited.append(node)
        for neighbour in graph.adjacency.get(node, []):
            self._dfs_order(graph, neighbour, seen, visited)

    def _create_answer(self, data: dict) -> str:
        """Return whether a cycle exists.

        Args:
            data: Solution data with cycle status.

        Returns:
            'yes' if cycle exists, 'no' otherwise.
        """
        return "yes" if data["has_cycle"] else "no"
