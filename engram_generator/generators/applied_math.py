"""Tier 4 generators — applied science, linear algebra, and expert algorithms.

Unlocks when Tier 3 tasks are mastered. Introduces physics formulae,
matrix operations, dynamic programming, graph algorithms, and calculus
evaluation. These tasks require multi-step reasoning over structured
mathematical and algorithmic domains.
"""
from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


class PhysicsParameterSampler:
    """Samples physical quantities with difficulty-scaled magnitude.

    Provides a uniform interface for generating random values in
    physics problems, scaling the magnitude of operands with
    difficulty level.

    Example:
        >>> import random
        >>> rng = random.Random(42)
        >>> s = PhysicsParameterSampler(rng)
        >>> s.sample(3, 1, 5)  # doctest: +SKIP
        3
    """

    def __init__(self, rng: 'random.Random') -> None:
        """Initialise with a random number generator.

        Args:
            rng: Seeded Random instance.
        """
        self._rng = rng

    def sample(self, difficulty: int, low: int = 1, high: int = 10) -> int:
        """Sample an integer scaled by difficulty.

        Args:
            difficulty: Difficulty level (1-8).
            low: Base lower bound.
            high: Base upper bound.

        Returns:
            Random integer in [low * scale, high * scale].
        """
        scale = max(1, difficulty)
        return self._rng.randint(low * scale, high * scale)

    def sample_float(self, low: float, high: float,
                     decimals: int = 1) -> float:
        """Sample a float rounded to given decimal places.

        Args:
            low: Lower bound.
            high: Upper bound.
            decimals: Number of decimal places.

        Returns:
            Rounded random float.
        """
        return round(self._rng.uniform(low, high), decimals)


class MatrixHelper:
    """Utility methods for matrix formatting, multiplication, and inversion.

    Provides LaTeX formatting for matrices, standard 2x2 and 3x3
    multiplication, determinant computation, and 2x2 inversion.

    Example:
        >>> MatrixHelper.format_matrix([[1, 2], [3, 4]])
        '\\\\begin{pmatrix} 1 & 2 \\\\\\\\ 3 & 4 \\\\end{pmatrix}'
    """

    @staticmethod
    def format_matrix(matrix: list[list[int]]) -> str:
        """Format a matrix in LaTeX pmatrix notation.

        Args:
            matrix: 2D list of integers.

        Returns:
            LaTeX pmatrix string.
        """
        rows = [" & ".join(str(v) for v in row) for row in matrix]
        body = " \\\\ ".join(rows)
        return f"\\begin{{pmatrix}} {body} \\end{{pmatrix}}"

    @staticmethod
    def multiply(a: list[list[int]], b: list[list[int]]) -> list[list[int]]:
        """Multiply two square matrices.

        Args:
            a: First matrix (n x n).
            b: Second matrix (n x n).

        Returns:
            Product matrix (n x n).
        """
        n = len(a)
        result = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    result[i][j] += a[i][k] * b[k][j]
        return result

    @staticmethod
    def det_2x2(m: list[list[int]]) -> int:
        """Compute the determinant of a 2x2 matrix.

        Args:
            m: A 2x2 matrix.

        Returns:
            Integer determinant.
        """
        return m[0][0] * m[1][1] - m[0][1] * m[1][0]

    @staticmethod
    def inverse_2x2(m: list[list[int]], det: int) -> list[list[int]]:
        """Compute the inverse of a 2x2 matrix with known determinant.

        Args:
            m: A 2x2 matrix with integer entries.
            det: The determinant (must be +-1 for integer result).

        Returns:
            Inverse matrix with integer entries.
        """
        sign = det
        return [
            [sign * m[1][1], -sign * m[0][1]],
            [-sign * m[1][0], sign * m[0][0]],
        ]


class DPTableBuilder:
    """Builds dynamic programming tables with step-by-step traces.

    Provides utilities for constructing DP tables used in
    edit distance and coin change problems, recording each
    significant cell update as a step.

    Example:
        >>> builder = DPTableBuilder()
        >>> builder.format_row(0, [0, 1, 2, 3])
        'row0: 0,1,2,3'
    """

    def format_row(self, row_idx: int, row: list[int]) -> str:
        """Format a DP table row as a step string.

        Args:
            row_idx: Row index.
            row: List of cell values.

        Returns:
            Formatted row string.
        """
        values = ",".join(str(v) for v in row)
        return f"row{row_idx}: {values}"


class GraphBuilder:
    """Builds small weighted directed graphs with guaranteed connectivity.

    Generates adjacency representations suitable for Dijkstra's
    algorithm, ensuring a path exists from source to target.

    Example:
        >>> import random
        >>> rng = random.Random(42)
        >>> g = GraphBuilder(rng)
        >>> adj = g.build(4, 2)  # doctest: +SKIP
    """

    def __init__(self, rng: 'random.Random') -> None:
        """Initialise with a random number generator.

        Args:
            rng: Seeded Random instance.
        """
        self._rng = rng

    def build(self, num_nodes: int, difficulty: int) -> dict[str, list[tuple[str, int]]]:
        """Build a weighted directed graph with guaranteed path from first to last node.

        Args:
            num_nodes: Number of nodes.
            difficulty: Controls edge weight magnitude.

        Returns:
            Adjacency dict mapping node labels to (neighbour, weight) lists.
        """
        labels = [chr(97 + i) for i in range(num_nodes)]
        adj: dict[str, list[tuple[str, int]]] = {label: [] for label in labels}
        self._add_spine(adj, labels, difficulty)
        self._add_extra_edges(adj, labels, difficulty)
        return adj

    def _add_spine(self, adj: dict[str, list[tuple[str, int]]],
                   labels: list[str], difficulty: int) -> None:
        """Add a guaranteed path through all nodes in order.

        Args:
            adj: Adjacency dict to modify.
            labels: Node labels.
            difficulty: Controls weight magnitude.
        """
        for i in range(len(labels) - 1):
            weight = self._rng.randint(1, 5 * max(1, difficulty))
            adj[labels[i]].append((labels[i + 1], weight))

    def _add_extra_edges(self, adj: dict[str, list[tuple[str, int]]],
                         labels: list[str], difficulty: int) -> None:
        """Add random forward edges for alternative paths.

        Args:
            adj: Adjacency dict to modify.
            labels: Node labels.
            difficulty: Controls weight magnitude.
        """
        num_extra = self._rng.randint(1, max(1, len(labels) - 1))
        for _ in range(num_extra):
            i = self._rng.randint(0, len(labels) - 2)
            j = self._rng.randint(i + 1, len(labels) - 1)
            weight = self._rng.randint(1, 10 * max(1, difficulty))
            adj[labels[i]].append((labels[j], weight))

    def format_adjacency(self, adj: dict[str, list[tuple[str, int]]]) -> str:
        """Format adjacency dict as a compact string.

        Args:
            adj: Adjacency dict.

        Returns:
            String like 'a:b3,c1;b:d2;c:b1,d5;d:'.
        """
        parts: list[str] = []
        for node in sorted(adj.keys()):
            edges = ",".join(f"{n}{w}" for n, w in adj[node])
            parts.append(f"{node}:{edges}")
        return ";".join(parts)


class PolynomialTerm:
    """Represents a single term in a polynomial for differentiation.

    Stores coefficient and exponent, and provides derivative
    computation and LaTeX formatting.

    Example:
        >>> t = PolynomialTerm(3, 2)
        >>> t.to_latex("x")
        '3x^{2}'
        >>> d = t.derivative()
        >>> d.coefficient, d.exponent
        (6, 1)
    """

    def __init__(self, coefficient: int, exponent: int) -> None:
        """Initialise a polynomial term.

        Args:
            coefficient: Numeric coefficient.
            exponent: Power of the variable.
        """
        self.coefficient = coefficient
        self.exponent = exponent

    def derivative(self) -> 'PolynomialTerm':
        """Compute the derivative of this term.

        Returns:
            New PolynomialTerm with power rule applied.
        """
        return PolynomialTerm(
            self.coefficient * self.exponent,
            max(0, self.exponent - 1),
        )

    def evaluate(self, value: int) -> int:
        """Evaluate this term at a given value.

        Args:
            value: Variable value.

        Returns:
            Coefficient * value^exponent.
        """
        return self.coefficient * (value ** self.exponent)

    def to_latex(self, var: str) -> str:
        """Format this term in LaTeX notation.

        Args:
            var: Variable name (e.g., 'x').

        Returns:
            LaTeX string for this term.
        """
        if self.exponent == 0:
            return str(self.coefficient)
        if self.exponent == 1:
            return f"{self.coefficient}{var}"
        return f"{self.coefficient}{var}^{{{self.exponent}}}"


class BivariateTermFormatter:
    """Formats bivariate polynomial terms and computes partial derivatives.

    Represents terms of the form c * x^a * y^b and provides
    partial differentiation with respect to either variable.

    Example:
        >>> t = BivariateTermFormatter(3, 2, 1)
        >>> t.to_latex()
        '3x^{2}y'
    """

    def __init__(self, coefficient: int, x_exp: int, y_exp: int) -> None:
        """Initialise a bivariate term.

        Args:
            coefficient: Numeric coefficient.
            x_exp: Exponent of x.
            y_exp: Exponent of y.
        """
        self.coefficient = coefficient
        self.x_exp = x_exp
        self.y_exp = y_exp

    def partial_x(self) -> 'BivariateTermFormatter':
        """Compute the partial derivative with respect to x.

        Returns:
            New BivariateTermFormatter with d/dx applied, or None if zero.
        """
        if self.x_exp == 0:
            return BivariateTermFormatter(0, 0, 0)
        return BivariateTermFormatter(
            self.coefficient * self.x_exp,
            self.x_exp - 1,
            self.y_exp,
        )

    def partial_y(self) -> 'BivariateTermFormatter':
        """Compute the partial derivative with respect to y.

        Returns:
            New BivariateTermFormatter with d/dy applied, or None if zero.
        """
        if self.y_exp == 0:
            return BivariateTermFormatter(0, 0, 0)
        return BivariateTermFormatter(
            self.coefficient * self.y_exp,
            self.x_exp,
            self.y_exp - 1,
        )

    def to_latex(self) -> str:
        """Format this term in LaTeX notation.

        Returns:
            LaTeX string for this bivariate term.
        """
        if self.coefficient == 0:
            return "0"
        parts = self._format_coefficient()
        parts += self._format_variable("x", self.x_exp)
        parts += self._format_variable("y", self.y_exp)
        return parts if parts else str(self.coefficient)

    def _format_coefficient(self) -> str:
        """Format the coefficient portion.

        Returns:
            Coefficient string, omitting 1 when variables are present.
        """
        has_vars = self.x_exp > 0 or self.y_exp > 0
        if self.coefficient == 1 and has_vars:
            return ""
        if self.coefficient == -1 and has_vars:
            return "-"
        return str(self.coefficient)

    def _format_variable(self, var: str, exp: int) -> str:
        """Format a single variable with its exponent.

        Args:
            var: Variable name.
            exp: Exponent value.

        Returns:
            LaTeX variable string.
        """
        if exp == 0:
            return ""
        if exp == 1:
            return var
        return f"{var}^{{{exp}}}"


@register
class KinematicsVelocityGenerator(StepGenerator):
    """Kinematics velocity computation using v = v_0 + at.

    Generates problems where the model must apply the first
    kinematic equation to find the final velocity given initial
    velocity, acceleration, and time.

    Input format:
        ``find final velocity using kinematics``

    Target format:
        ``v = v_0 + at <step> v = 10 + 3(4) <step> v = 10 + 12 <step> v = 22``

    Difficulty scaling:
        Difficulty 1: v0 in [1,10], a in [1,10], t in [1,10].
        Difficulty 8: v0 in [8,80], a in [8,80], t in [8,80].
        Magnitudes scale linearly with difficulty.

    Prerequisites:
        multiplication, addition.

    Example:
        >>> gen = KinematicsVelocityGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'kinematics_velocity'
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "kinematics_velocity"

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
            difficulty: Controls parameter magnitude.

        Returns:
            Natural language description.
        """
        return "find final velocity using kinematics"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate kinematics parameters and compute final velocity.

        Args:
            difficulty: Controls parameter magnitude.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        sampler = PhysicsParameterSampler(self._rng)
        v0 = sampler.sample(difficulty)
        a = sampler.sample(difficulty)
        t = sampler.sample(difficulty)
        v = v0 + a * t
        return "v = v_0 + at", {"v0": v0, "a": a, "t": t, "v": v}

    def _create_steps(self, data: dict) -> list[str]:
        """Generate substitution and arithmetic steps.

        Args:
            data: Solution data with v0, a, t, v.

        Returns:
            Steps showing substitution, multiplication, and addition.
        """
        v0, a, t = data["v0"], data["a"], data["t"]
        product = a * t
        return [
            f"v = {v0} + {a}({t})",
            f"v = {v0} + {product}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the final velocity.

        Args:
            data: Solution data.

        Returns:
            String representation of v.
        """
        return f"v = {data['v']}"


@register
class KineticEnergyGenerator(StepGenerator):
    """Kinetic energy computation using KE = (1/2)mv^2.

    Generates problems where the model must compute kinetic
    energy by squaring velocity, multiplying by mass, and
    halving the result.

    Input format:
        ``compute kinetic energy``

    Target format:
        ``KE = \\frac{1}{2}mv^2 <step> KE = \\frac{1}{2}(5)(3^2)
        <step> \\frac{1}{2}(5)(9) <step> \\frac{45}{2} <step> 22.5``

    Difficulty scaling:
        Difficulty 1: m in [1,10], v in [1,10].
        Difficulty 8: m in [8,80], v in [8,80].
        Magnitudes scale linearly with difficulty.

    Prerequisites:
        multiplication, exponentiation.

    Example:
        >>> gen = KineticEnergyGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'kinetic_energy'
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "kinetic_energy"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["multiplication", "exponentiation"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls parameter magnitude.

        Returns:
            Natural language description.
        """
        return "compute kinetic energy"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate mass and velocity, then compute kinetic energy.

        Args:
            difficulty: Controls parameter magnitude.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        sampler = PhysicsParameterSampler(self._rng)
        m = sampler.sample(difficulty)
        v = sampler.sample(difficulty)
        v_sq = v * v
        numerator = m * v_sq
        ke = numerator / 2
        return (
            "KE = \\frac{1}{2}mv^2",
            {"m": m, "v": v, "v_sq": v_sq, "numerator": numerator, "ke": ke},
        )

    def _create_steps(self, data: dict) -> list[str]:
        """Generate squaring, multiplication, and halving steps.

        Args:
            data: Solution data with m, v, v_sq, numerator, ke.

        Returns:
            Steps showing each arithmetic operation.
        """
        m, v = data["m"], data["v"]
        v_sq, numerator = data["v_sq"], data["numerator"]
        return [
            f"KE = \\frac{{1}}{{2}}({m})({v}^2)",
            f"\\frac{{1}}{{2}}({m})({v_sq})",
            f"\\frac{{{numerator}}}{{2}}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the kinetic energy value.

        Args:
            data: Solution data.

        Returns:
            String representation of KE.
        """
        ke = data["ke"]
        if ke == int(ke):
            return str(int(ke))
        return str(ke)


@register
class OhmsLawGenerator(StepGenerator):
    """Ohm's law application solving V = IR for any variable.

    Generates problems where the model must rearrange V = IR
    to solve for voltage, current, or resistance, then substitute
    and compute.

    Input format:
        ``apply ohms law to find current``

    Target format:
        ``V = IR <step> I = \\frac{V}{R} <step> I = \\frac{12}{4} <step> 3``

    Difficulty scaling:
        Difficulty 1: values in [1,10].
        Difficulty 8: values in [8,80].
        Randomly chooses which variable to solve for.

    Prerequisites:
        linear_equation.

    Example:
        >>> gen = OhmsLawGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'ohms_law'
    """

    _SOLVE_TARGETS = ["V", "I", "R"]

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "ohms_law"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["linear_equation"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls parameter magnitude.

        Returns:
            Natural language description.
        """
        return "apply ohms law"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate Ohm's law parameters and choose solve target.

        Constructs values so the solution is always an integer.

        Args:
            difficulty: Controls parameter magnitude.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        sampler = PhysicsParameterSampler(self._rng)
        target = self._rng.choice(self._SOLVE_TARGETS)
        i = sampler.sample(difficulty)
        r = sampler.sample(difficulty)
        v = i * r
        return "V = IR", {"V": v, "I": i, "R": r, "target": target}

    def _create_steps(self, data: dict) -> list[str]:
        """Generate rearrangement and substitution steps.

        Args:
            data: Solution data with V, I, R, and target variable.

        Returns:
            Steps showing formula rearrangement and computation.
        """
        target = data["target"]
        if target == "V":
            return self._steps_for_voltage(data)
        if target == "I":
            return self._steps_for_current(data)
        return self._steps_for_resistance(data)

    def _steps_for_voltage(self, data: dict) -> list[str]:
        """Generate steps for solving for voltage.

        Args:
            data: Solution data.

        Returns:
            Steps for V = IR.
        """
        return [
            f"V = ({data['I']})({data['R']})",
        ]

    def _steps_for_current(self, data: dict) -> list[str]:
        """Generate steps for solving for current.

        Args:
            data: Solution data.

        Returns:
            Steps for I = V/R.
        """
        return [
            f"I = \\frac{{V}}{{R}}",
            f"I = \\frac{{{data['V']}}}{{{data['R']}}}",
        ]

    def _steps_for_resistance(self, data: dict) -> list[str]:
        """Generate steps for solving for resistance.

        Args:
            data: Solution data.

        Returns:
            Steps for R = V/I.
        """
        return [
            f"R = \\frac{{V}}{{I}}",
            f"R = \\frac{{{data['V']}}}{{{data['I']}}}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the solved variable value.

        Args:
            data: Solution data.

        Returns:
            String representation of the target variable.
        """
        return str(data[data["target"]])


@register
class IdealGasGenerator(StepGenerator):
    """Ideal gas law application solving PV = nRT for any variable.

    Generates problems using the ideal gas law with R = 8.314
    J/(mol*K), randomly choosing which variable to solve for.
    Values are constructed to produce clean decimal results.

    Input format:
        ``apply ideal gas law``

    Target format:
        ``PV = nRT <step> P = \\frac{nRT}{V} <step>
        P = \\frac{(2)(8.314)(300)}{5} <step> 997.7``

    Difficulty scaling:
        Difficulty 1: n in [1,3], T in [200,400], V in [1,5].
        Difficulty 8: n in [1,10], T in [200,600], V in [1,20].

    Prerequisites:
        multiplication, division.

    Example:
        >>> gen = IdealGasGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'ideal_gas'
    """

    _R = 8.314
    _SOLVE_TARGETS = ["P", "V", "n", "T"]

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "ideal_gas"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["multiplication", "division"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls parameter ranges.

        Returns:
            Natural language description.
        """
        return "apply ideal gas law"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate ideal gas parameters and choose solve target.

        Args:
            difficulty: Controls parameter ranges.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        n = self._rng.randint(1, max(3, difficulty))
        temp = self._rng.randint(200, 200 + 50 * difficulty)
        vol = self._rng.randint(1, max(5, difficulty * 2))
        nrt = round(n * self._R * temp, 1)
        pressure = round(nrt / vol, 1)
        target = self._rng.choice(self._SOLVE_TARGETS)

        return "PV = nRT", {
            "P": pressure, "V": vol, "n": n, "T": temp,
            "nRT": nrt, "target": target,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate rearrangement and substitution steps.

        Args:
            data: Solution data with P, V, n, T, and target.

        Returns:
            Steps showing formula manipulation and computation.
        """
        target = data["target"]
        if target == "P":
            return self._steps_solve_p(data)
        if target == "V":
            return self._steps_solve_v(data)
        if target == "n":
            return self._steps_solve_n(data)
        return self._steps_solve_t(data)

    def _steps_solve_p(self, data: dict) -> list[str]:
        """Generate steps for solving for pressure.

        Args:
            data: Solution data.

        Returns:
            Steps for P = nRT/V.
        """
        return [
            f"P = \\frac{{nRT}}{{V}}",
            f"P = \\frac{{({data['n']})({self._R})({data['T']})}}{{{data['V']}}}",
            f"P = \\frac{{{data['nRT']}}}{{{data['V']}}}",
        ]

    def _steps_solve_v(self, data: dict) -> list[str]:
        """Generate steps for solving for volume.

        Args:
            data: Solution data.

        Returns:
            Steps for V = nRT/P.
        """
        return [
            f"V = \\frac{{nRT}}{{P}}",
            f"V = \\frac{{({data['n']})({self._R})({data['T']})}}{{{data['P']}}}",
            f"V = \\frac{{{data['nRT']}}}{{{data['P']}}}",
        ]

    def _steps_solve_n(self, data: dict) -> list[str]:
        """Generate steps for solving for moles.

        Args:
            data: Solution data.

        Returns:
            Steps for n = PV/RT.
        """
        rt = round(self._R * data["T"], 1)
        return [
            f"n = \\frac{{PV}}{{RT}}",
            f"n = \\frac{{({data['P']})({data['V']})}}{{{rt}}}",
        ]

    def _steps_solve_t(self, data: dict) -> list[str]:
        """Generate steps for solving for temperature.

        Args:
            data: Solution data.

        Returns:
            Steps for T = PV/nR.
        """
        nr = round(data["n"] * self._R, 3)
        return [
            f"T = \\frac{{PV}}{{nR}}",
            f"T = \\frac{{({data['P']})({data['V']})}}{{{nr}}}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the solved variable value.

        Args:
            data: Solution data.

        Returns:
            String representation of the target variable.
        """
        val = data[data["target"]]
        if isinstance(val, float) and val == int(val):
            return str(int(val))
        return str(val)


@register
class MatrixMultiplyGenerator(StepGenerator):
    """Matrix multiplication for 2x2 and 3x3 matrices.

    Generates two square matrices and shows the dot-product
    computation for each cell of the result matrix, followed
    by the assembled product matrix.

    Input format:
        ``multiply two matrices``

    Target format:
        ``A \\times B <step> c_{11}=1(5)+2(7)=19 <step>
        c_{12}=1(6)+2(8)=22 <step> ... <step>
        \\begin{pmatrix} 19 & 22 \\\\ 43 & 50 \\end{pmatrix}``

    Difficulty scaling:
        Difficulty 1-4: 2x2 matrices with entries in [-5, 10].
        Difficulty 5-8: 3x3 matrices with entries in [-10, 15].

    Prerequisites:
        multiplication, addition.

    Example:
        >>> gen = MatrixMultiplyGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'matrix_multiply'
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "matrix_multiply"

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
            difficulty: Controls matrix size.

        Returns:
            Natural language description.
        """
        return "multiply two matrices"

    def _matrix_size(self, difficulty: int) -> int:
        """Determine matrix dimension from difficulty.

        Args:
            difficulty: Difficulty level.

        Returns:
            Matrix dimension (2 or 3).
        """
        return 3 if difficulty >= 5 else 2

    def _random_matrix(self, size: int, difficulty: int) -> list[list[int]]:
        """Generate a random square matrix.

        Args:
            size: Matrix dimension.
            difficulty: Controls entry magnitude.

        Returns:
            2D list of integer entries.
        """
        lo = -5 if size == 2 else -10
        hi = 10 if size == 2 else 15
        return [
            [self._rng.randint(lo, hi) for _ in range(size)]
            for _ in range(size)
        ]

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate two matrices and compute their product.

        Args:
            difficulty: Controls matrix size and entry magnitude.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        size = self._matrix_size(difficulty)
        a = self._random_matrix(size, difficulty)
        b = self._random_matrix(size, difficulty)
        result = MatrixHelper.multiply(a, b)

        problem = (
            f"{MatrixHelper.format_matrix(a)} \\times "
            f"{MatrixHelper.format_matrix(b)}"
        )
        return problem, {"a": a, "b": b, "result": result, "size": size}

    def _create_steps(self, data: dict) -> list[str]:
        """Generate dot-product steps for each cell.

        Args:
            data: Solution data with matrices and product.

        Returns:
            Steps showing the computation of each result cell.
        """
        a, b, result = data["a"], data["b"], data["result"]
        size = data["size"]
        steps: list[str] = []

        for i in range(size):
            for j in range(size):
                steps.append(self._cell_step(a, b, result, i, j, size))

        return steps

    def _cell_step(self, a: list[list[int]], b: list[list[int]],
                   result: list[list[int]], i: int, j: int,
                   size: int) -> str:
        """Format a single cell dot-product computation.

        Args:
            a: First matrix.
            b: Second matrix.
            result: Product matrix.
            i: Row index.
            j: Column index.
            size: Matrix dimension.

        Returns:
            Step string showing the dot product.
        """
        terms = [f"{a[i][k]}({b[k][j]})" for k in range(size)]
        return f"c_{{{i+1}{j+1}}}={'+'.join(terms)}={result[i][j]}"

    def _create_answer(self, data: dict) -> str:
        """Return the product matrix in LaTeX.

        Args:
            data: Solution data.

        Returns:
            LaTeX pmatrix string.
        """
        return MatrixHelper.format_matrix(data["result"])


@register
class MatrixInverseGenerator(StepGenerator):
    """2x2 matrix inverse with determinant +-1 for integer results.

    Constructs 2x2 matrices with det = +-1 so the inverse has
    integer entries. Shows the determinant computation and
    adjugate formula application.

    Input format:
        ``find matrix inverse``

    Target format:
        ``A^{-1} <step> det=ad-bc=1 <step>
        \\frac{1}{1}\\begin{pmatrix} d & -b \\\\ -c & a \\end{pmatrix}
        <step> \\begin{pmatrix} ... \\end{pmatrix}``

    Difficulty scaling:
        Difficulty 1: entries in [-3, 3].
        Difficulty 8: entries in [-10, 10].
        Matrices always have det = +-1.

    Prerequisites:
        determinant.

    Example:
        >>> gen = MatrixInverseGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'matrix_inverse'
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "matrix_inverse"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["determinant"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls entry magnitude.

        Returns:
            Natural language description.
        """
        return "find matrix inverse"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a 2x2 matrix with det = +-1.

        Constructs the matrix by picking a, b, c and computing d
        so that ad - bc = +-1.

        Args:
            difficulty: Controls entry magnitude.

        Returns:
            Tuple of (latex_matrix, solution_data).
        """
        matrix, det = self._build_unit_det_matrix(difficulty)
        inverse = MatrixHelper.inverse_2x2(matrix, det)

        problem = f"{MatrixHelper.format_matrix(matrix)}^{{-1}}"
        return problem, {"matrix": matrix, "det": det, "inverse": inverse}

    def _build_unit_det_matrix(self, difficulty: int) -> tuple[list[list[int]], int]:
        """Build a 2x2 matrix with determinant +-1.

        Args:
            difficulty: Controls entry magnitude.

        Returns:
            Tuple of (matrix, determinant).
        """
        bound = min(3 + difficulty, 10)
        det = self._rng.choice([-1, 1])
        for _ in range(200):
            a = self._nonzero_randint(bound)
            b = self._rng.randint(-bound, bound)
            c = self._rng.randint(-bound, bound)
            if (det + b * c) % a == 0:
                d = (det + b * c) // a
                return [[a, b], [c, d]], det
        return [[1, 0], [0, det]], det

    def _nonzero_randint(self, bound: int) -> int:
        """Generate a nonzero random integer in [-bound, bound].

        Args:
            bound: Absolute maximum value.

        Returns:
            Nonzero integer.
        """
        val = 0
        while val == 0:
            val = self._rng.randint(-bound, bound)
        return val

    def _fix_d(self, a: int, b: int, c: int, det: int) -> int:
        """Adjust d when (det + bc) is not divisible by a.

        Resamples c until ad - bc = det has an integer solution for d.

        Args:
            a: Top-left entry.
            b: Top-right entry.
            c: Bottom-left entry.
            det: Target determinant (+-1).

        Returns:
            Valid value for d.
        """
        for _ in range(100):
            c_new = self._rng.randint(-abs(a) * 3, abs(a) * 3)
            if (det + b * c_new) % a == 0:
                return (det + b * c_new) // a
        return (det + b * 0) // a

    def _create_steps(self, data: dict) -> list[str]:
        """Generate determinant and adjugate steps.

        Args:
            data: Solution data with matrix, det, and inverse.

        Returns:
            Steps showing det computation and adjugate formula.
        """
        m = data["matrix"]
        det = data["det"]
        a, b, c, d = m[0][0], m[0][1], m[1][0], m[1][1]

        adjugate = MatrixHelper.format_matrix([[d, -b], [-c, a]])
        return [
            f"\\det = ({a})({d})-({b})({c})={det}",
            f"\\frac{{1}}{{{det}}}{adjugate}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the inverse matrix in LaTeX.

        Args:
            data: Solution data.

        Returns:
            LaTeX pmatrix string for the inverse.
        """
        return MatrixHelper.format_matrix(data["inverse"])


@register
class EigenvalueGenerator(StepGenerator):
    """Eigenvalue computation for 2x2 matrices.

    Constructs a 2x2 matrix from chosen integer eigenvalues
    using a similarity transform P*D*P^{-1}, then shows the
    characteristic polynomial and its roots.

    Input format:
        ``find eigenvalues of matrix``

    Target format:
        ``\\det(A-\\lambda I)=0 <step>
        (a-\\lambda)(d-\\lambda)-bc=0 <step>
        \\lambda^2-5\\lambda+6=0 <step> \\lambda=2,3``

    Difficulty scaling:
        Difficulty 1: eigenvalues in [1, 5].
        Difficulty 8: eigenvalues in [-10, 10].

    Prerequisites:
        quadratic, determinant.

    Example:
        >>> gen = EigenvalueGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'eigenvalue'
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "eigenvalue"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["quadratic", "determinant"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls eigenvalue magnitude.

        Returns:
            Natural language description.
        """
        return "find eigenvalues of matrix"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a 2x2 matrix with known integer eigenvalues.

        Constructs the matrix as P*D*P^{-1} where D is diagonal
        with the chosen eigenvalues and P has det = 1.

        Args:
            difficulty: Controls eigenvalue magnitude.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        bound = min(2 + difficulty, 10)
        lam1 = self._rng.randint(-bound, bound)
        lam2 = self._rng.randint(-bound, bound)
        matrix = self._build_matrix(lam1, lam2)
        trace = lam1 + lam2
        det = lam1 * lam2

        problem = f"\\det(A-\\lambda I)=0 \\text{{ where }} A={MatrixHelper.format_matrix(matrix)}"
        return problem, {
            "matrix": matrix, "lam1": lam1, "lam2": lam2,
            "trace": trace, "det": det,
        }

    def _build_matrix(self, lam1: int, lam2: int) -> list[list[int]]:
        """Construct a matrix with given eigenvalues via similarity.

        Uses P = [[1,1],[0,1]] with det=1, so P^{-1} = [[1,-1],[0,1]].
        Result is [[lam1, lam2-lam1], [0, lam2]].

        Args:
            lam1: First eigenvalue.
            lam2: Second eigenvalue.

        Returns:
            2x2 integer matrix.
        """
        return [
            [lam1, lam2 - lam1],
            [0, lam2],
        ]

    def _create_steps(self, data: dict) -> list[str]:
        """Generate characteristic polynomial and factoring steps.

        Args:
            data: Solution data with matrix, eigenvalues, trace, det.

        Returns:
            Steps showing polynomial derivation and roots.
        """
        m = data["matrix"]
        trace, det = data["trace"], data["det"]
        a, b, c, d = m[0][0], m[0][1], m[1][0], m[1][1]

        return [
            f"({a}-\\lambda)({d}-\\lambda)-({b})({c})=0",
            f"\\lambda^2-{trace}\\lambda+{det}=0",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the eigenvalues.

        Args:
            data: Solution data.

        Returns:
            Eigenvalues as a comma-separated string.
        """
        lam1, lam2 = sorted([data["lam1"], data["lam2"]])
        return f"\\lambda={lam1},{lam2}"


@register
class EditDistanceGenerator(StepGenerator):
    """Levenshtein edit distance between two strings with DP table.

    Generates two short strings and computes the edit distance
    using dynamic programming, showing each row of the DP table
    as a step.

    Input format:
        ``compute edit distance between two words``

    Target format:
        ``edist(kitten,sitting) <step> row0: 0,1,2,3,4,5,6,7
        <step> row1: 1,1,2,3,4,5,6,7 <step> ... <step> 3``

    Difficulty scaling:
        Difficulty 1: words of length 3-4.
        Difficulty 8: words of length 8-10.
        Uses random lowercase strings.

    Prerequisites:
        addition.

    Example:
        >>> gen = EditDistanceGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'edit_distance'
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "edit_distance"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["addition"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls word length.

        Returns:
            Natural language description.
        """
        return "compute edit distance between two words"

    def _word_length(self, difficulty: int) -> int:
        """Map difficulty to word length.

        Args:
            difficulty: Difficulty level.

        Returns:
            Word length.
        """
        return min(2 + difficulty, 10)

    def _random_word(self, length: int) -> str:
        """Generate a random lowercase word.

        Args:
            length: Number of characters.

        Returns:
            Random lowercase string.
        """
        return "".join(chr(self._rng.randint(97, 122)) for _ in range(length))

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate two words and compute their edit distance.

        Args:
            difficulty: Controls word length.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        length = self._word_length(difficulty)
        word_a = self._random_word(length)
        word_b = self._random_word(length)
        dp = self._compute_dp(word_a, word_b)

        return (
            f"edist({word_a},{word_b})",
            {"word_a": word_a, "word_b": word_b, "dp": dp},
        )

    def _compute_dp(self, a: str, b: str) -> list[list[int]]:
        """Compute the full DP table for edit distance.

        Args:
            a: First string.
            b: Second string.

        Returns:
            2D list representing the DP table.
        """
        m, n = len(a), len(b)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        self._init_base_cases(dp, m, n)
        self._fill_table(dp, a, b, m, n)
        return dp

    def _init_base_cases(self, dp: list[list[int]], m: int, n: int) -> None:
        """Fill base cases of the DP table.

        Args:
            dp: DP table to modify.
            m: Length of first string.
            n: Length of second string.
        """
        for i in range(m + 1):
            dp[i][0] = i
        for j in range(n + 1):
            dp[0][j] = j

    def _fill_table(self, dp: list[list[int]], a: str, b: str,
                    m: int, n: int) -> None:
        """Fill the DP table using the recurrence relation.

        Args:
            dp: DP table to modify.
            a: First string.
            b: Second string.
            m: Length of first string.
            n: Length of second string.
        """
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                cost = 0 if a[i - 1] == b[j - 1] else 1
                dp[i][j] = min(
                    dp[i - 1][j] + 1,
                    dp[i][j - 1] + 1,
                    dp[i - 1][j - 1] + cost,
                )

    def _create_steps(self, data: dict) -> list[str]:
        """Generate row-by-row DP table steps.

        Args:
            data: Solution data with the DP table.

        Returns:
            Steps showing each row of the table.
        """
        dp = data["dp"]
        builder = DPTableBuilder()
        return [builder.format_row(i, row) for i, row in enumerate(dp)]

    def _create_answer(self, data: dict) -> str:
        """Return the edit distance.

        Args:
            data: Solution data.

        Returns:
            String representation of the edit distance.
        """
        return str(data["dp"][-1][-1])


@register
class CoinChangeGenerator(StepGenerator):
    """Minimum coin change using dynamic programming.

    Generates a target amount and a set of coin denominations
    (always including 1 to guarantee a solution), then shows
    the DP table construction for the minimum number of coins.

    Input format:
        ``find minimum coins for amount``

    Target format:
        ``coins(11;1,5,6) <step> dp[0]=0 <step> dp[1]=1
        <step> ... <step> dp[11]=2 <step> 2``

    Difficulty scaling:
        Difficulty 1: amount in [5, 10], 2 coin types.
        Difficulty 8: amount in [20, 50], 4-5 coin types.

    Prerequisites:
        addition.

    Example:
        >>> gen = CoinChangeGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'coin_change'
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "coin_change"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["addition"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls amount and coin count.

        Returns:
            Natural language description.
        """
        return "find minimum coins for amount"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate coin denominations and target amount.

        Args:
            difficulty: Controls amount range and number of coins.

        Returns:
            Tuple of (problem_string, solution_data).
        """
        coins = self._generate_coins(difficulty)
        amount = self._rng.randint(5 + difficulty * 2, 10 + difficulty * 5)
        dp = self._compute_dp(amount, coins)

        coins_str = ",".join(str(c) for c in sorted(coins))
        return f"coins({amount};{coins_str})", {
            "amount": amount, "coins": coins, "dp": dp,
        }

    def _generate_coins(self, difficulty: int) -> list[int]:
        """Generate a set of coin denominations including 1.

        Args:
            difficulty: Controls number of denominations.

        Returns:
            Sorted list of coin values.
        """
        num_coins = min(2 + difficulty // 2, 5)
        coins = {1}
        while len(coins) < num_coins:
            coins.add(self._rng.randint(2, 10 + difficulty))
        return sorted(coins)

    def _compute_dp(self, amount: int, coins: list[int]) -> list[int]:
        """Compute the minimum coins DP table.

        Args:
            amount: Target amount.
            coins: Available denominations.

        Returns:
            DP table where dp[i] is minimum coins for amount i.
        """
        dp = [float("inf")] * (amount + 1)
        dp[0] = 0

        for i in range(1, amount + 1):
            for c in coins:
                if c <= i and dp[i - c] + 1 < dp[i]:
                    dp[i] = dp[i - c] + 1

        return [int(v) for v in dp]

    def _create_steps(self, data: dict) -> list[str]:
        """Generate DP table fill steps.

        Args:
            data: Solution data with the DP table.

        Returns:
            Steps showing each dp[i] value.
        """
        dp = data["dp"]
        return [f"dp[{i}]={dp[i]}" for i in range(len(dp))]

    def _create_answer(self, data: dict) -> str:
        """Return the minimum number of coins.

        Args:
            data: Solution data.

        Returns:
            String representation of the answer.
        """
        return str(data["dp"][data["amount"]])


@register
class ShortestPathGenerator(StepGenerator):
    """Dijkstra's algorithm on small weighted directed graphs.

    Generates a small weighted graph with guaranteed path from
    source to target, then shows Dijkstra's relaxation steps
    in order of node settlement.

    Input format:
        ``find shortest path in weighted graph``

    Target format:
        ``a:b3,c1;b:d2;c:b1,d5;d: from a to d <step>
        a=0 <step> c=1 <step> b=2 <step> d=4 <step> 4``

    Difficulty scaling:
        Difficulty 1: 4 nodes.
        Difficulty 8: 8 nodes.
        Edge weights scale with difficulty.

    Prerequisites:
        graph_reach, addition.

    Example:
        >>> gen = ShortestPathGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'shortest_path'
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "shortest_path"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["graph_reach", "addition"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls graph size.

        Returns:
            Natural language description.
        """
        return "find shortest path in weighted graph"

    def _num_nodes(self, difficulty: int) -> int:
        """Map difficulty to graph size.

        Args:
            difficulty: Difficulty level.

        Returns:
            Number of nodes.
        """
        return min(3 + difficulty, 8)

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a weighted graph and compute shortest paths.

        Args:
            difficulty: Controls graph size and edge weights.

        Returns:
            Tuple of (graph_description, solution_data).
        """
        num_nodes = self._num_nodes(difficulty)
        builder = GraphBuilder(self._rng)
        adj = builder.build(num_nodes, difficulty)
        source = "a"
        target = chr(97 + num_nodes - 1)
        dist, order = self._dijkstra(adj, source)

        graph_str = builder.format_adjacency(adj)
        problem = f"{graph_str} from {source} to {target}"
        return problem, {
            "adj": adj, "source": source, "target": target,
            "dist": dist, "order": order,
        }

    def _dijkstra(self, adj: dict[str, list[tuple[str, int]]],
                  source: str) -> tuple[dict[str, int], list[str]]:
        """Run Dijkstra's algorithm from the source node.

        Args:
            adj: Adjacency dict with (neighbour, weight) pairs.
            source: Starting node label.

        Returns:
            Tuple of (distance_dict, settlement_order).
        """
        dist: dict[str, float] = {node: float("inf") for node in adj}
        dist[source] = 0
        visited: set[str] = set()
        order: list[str] = []

        for _ in range(len(adj)):
            u = self._nearest_unvisited(dist, visited)
            if u is None:
                break
            visited.add(u)
            order.append(u)
            self._relax_edges(adj, dist, u)

        return {k: int(v) for k, v in dist.items() if v < float("inf")}, order

    def _nearest_unvisited(self, dist: dict[str, float],
                           visited: set[str]) -> str | None:
        """Find the unvisited node with smallest distance.

        Args:
            dist: Current distance estimates.
            visited: Set of already-settled nodes.

        Returns:
            Node label or None if all visited.
        """
        best = None
        best_dist = float("inf")
        for node, d in dist.items():
            if node not in visited and d < best_dist:
                best = node
                best_dist = d
        return best

    def _relax_edges(self, adj: dict[str, list[tuple[str, int]]],
                     dist: dict[str, float], u: str) -> None:
        """Relax all edges from node u.

        Args:
            adj: Adjacency dict.
            dist: Distance dict to update.
            u: Current node being settled.
        """
        for v, w in adj[u]:
            new_dist = dist[u] + w
            if new_dist < dist[v]:
                dist[v] = new_dist

    def _create_steps(self, data: dict) -> list[str]:
        """Generate node settlement steps in Dijkstra order.

        Args:
            data: Solution data with distances and order.

        Returns:
            Steps showing each node's shortest distance.
        """
        dist = data["dist"]
        order = data["order"]
        return [f"{node}={dist[node]}" for node in order if node in dist]

    def _create_answer(self, data: dict) -> str:
        """Return the shortest distance to the target.

        Args:
            data: Solution data.

        Returns:
            String representation of the shortest path length.
        """
        return str(data["dist"].get(data["target"], "no path"))


@register
class DerivativeEvalGenerator(StepGenerator):
    """Differentiate a polynomial and evaluate at a point.

    Generates a polynomial with 2-4 terms, differentiates using
    the power rule, then evaluates the derivative at a random
    integer point.

    Input format:
        ``evaluate derivative at point``

    Target format:
        ``\\frac{d}{dx}(3x^2+2x+1) \\text{ at } x=4 <step>
        f'(x)=6x+2 <step> f'(4)=6(4)+2 <step> 26``

    Difficulty scaling:
        Difficulty 1: 2 terms, coefficients in [1, 5], exponents 1-2.
        Difficulty 8: 4 terms, coefficients in [1, 15], exponents 1-5.

    Prerequisites:
        derivative, polynomial_eval.

    Example:
        >>> gen = DerivativeEvalGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'derivative_eval'
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "derivative_eval"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["derivative", "polynomial_eval"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls polynomial complexity.

        Returns:
            Natural language description.
        """
        return "evaluate derivative at point"

    def _num_terms(self, difficulty: int) -> int:
        """Map difficulty to number of polynomial terms.

        Args:
            difficulty: Difficulty level.

        Returns:
            Number of terms (2-4).
        """
        return min(2 + difficulty // 3, 4)

    def _generate_terms(self, difficulty: int) -> list[PolynomialTerm]:
        """Generate polynomial terms with distinct exponents.

        Args:
            difficulty: Controls coefficient and exponent ranges.

        Returns:
            List of PolynomialTerm instances.
        """
        n = self._num_terms(difficulty)
        max_exp = min(2 + difficulty // 2, 5)
        max_coeff = min(5 + difficulty, 15)
        exponents = list(range(1, max_exp + 1))
        self._rng.shuffle(exponents)
        chosen = sorted(exponents[:n], reverse=True)

        return [
            PolynomialTerm(self._rng.randint(1, max_coeff), e)
            for e in chosen
        ]

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a polynomial, its derivative, and evaluation point.

        Args:
            difficulty: Controls polynomial complexity.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        terms = self._generate_terms(difficulty)
        point = self._rng.randint(1, min(5 + difficulty, 10))
        derivs = [t.derivative() for t in terms]
        result = sum(d.evaluate(point) for d in derivs)

        poly_latex = "+".join(t.to_latex("x") for t in terms)
        problem = f"\\frac{{d}}{{dx}}({poly_latex}) \\text{{ at }} x={point}"
        return problem, {
            "terms": terms, "derivs": derivs,
            "point": point, "result": result,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate differentiation and evaluation steps.

        Args:
            data: Solution data with terms, derivatives, and point.

        Returns:
            Steps showing the derivative and its evaluation.
        """
        derivs = data["derivs"]
        point = data["point"]

        deriv_latex = "+".join(d.to_latex("x") for d in derivs if d.coefficient != 0)
        eval_parts = "+".join(
            f"{d.coefficient}({point})" if d.exponent == 0
            else f"{d.coefficient}({point}^{{{d.exponent}}})"
            for d in derivs if d.coefficient != 0
        )
        return [
            f"f'(x)={deriv_latex}",
            f"f'({point})={eval_parts}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the evaluated derivative.

        Args:
            data: Solution data.

        Returns:
            String representation of the result.
        """
        return str(data["result"])


@register
class PartialDerivativeGenerator(StepGenerator):
    """Partial derivative of a bivariate polynomial.

    Generates a polynomial in x and y with 2-4 terms, then
    differentiates with respect to a randomly chosen variable,
    showing each term's derivative.

    Input format:
        ``find partial derivative with respect to x``

    Target format:
        ``\\frac{\\partial}{\\partial x}(3x^{2}y+2xy^{3})
        <step> 6xy <step> 2y^{3} <step> 6xy+2y^{3}``

    Difficulty scaling:
        Difficulty 1: 2 terms, exponents 1-2.
        Difficulty 8: 4 terms, exponents 1-4.

    Prerequisites:
        derivative.

    Example:
        >>> gen = PartialDerivativeGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'partial_derivative'
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "partial_derivative"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["derivative"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls polynomial complexity.

        Returns:
            Natural language description.
        """
        return "find partial derivative"

    def _num_terms(self, difficulty: int) -> int:
        """Map difficulty to number of polynomial terms.

        Args:
            difficulty: Difficulty level.

        Returns:
            Number of terms (2-4).
        """
        return min(2 + difficulty // 3, 4)

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a bivariate polynomial and choose differentiation variable.

        Args:
            difficulty: Controls term count and exponent range.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        var = self._rng.choice(["x", "y"])
        terms = self._generate_bivariate_terms(difficulty)
        derivs = self._differentiate(terms, var)

        poly_latex = "+".join(t.to_latex() for t in terms)
        problem = f"\\frac{{\\partial}}{{\\partial {var}}}({poly_latex})"
        return problem, {"terms": terms, "derivs": derivs, "var": var}

    def _generate_bivariate_terms(self, difficulty: int) -> list[BivariateTermFormatter]:
        """Generate bivariate polynomial terms.

        Ensures each term has a nonzero exponent for both variables
        so that partial derivatives are nontrivial.

        Args:
            difficulty: Controls exponent range and term count.

        Returns:
            List of BivariateTermFormatter instances.
        """
        n = self._num_terms(difficulty)
        max_exp = min(2 + difficulty // 2, 4)
        terms: list[BivariateTermFormatter] = []

        for _ in range(n):
            coeff = self._rng.randint(1, 5 + difficulty)
            x_exp = self._rng.randint(1, max_exp)
            y_exp = self._rng.randint(1, max_exp)
            terms.append(BivariateTermFormatter(coeff, x_exp, y_exp))

        return terms

    def _differentiate(self, terms: list[BivariateTermFormatter],
                       var: str) -> list[BivariateTermFormatter]:
        """Differentiate each term with respect to the chosen variable.

        Args:
            terms: Bivariate terms.
            var: Variable to differentiate with respect to.

        Returns:
            List of differentiated terms (excluding zero terms).
        """
        if var == "x":
            return [t.partial_x() for t in terms if t.x_exp > 0]
        return [t.partial_y() for t in terms if t.y_exp > 0]

    def _create_steps(self, data: dict) -> list[str]:
        """Generate per-term differentiation steps.

        Args:
            data: Solution data with terms and derivatives.

        Returns:
            Steps showing each term's partial derivative.
        """
        derivs = data["derivs"]
        return [d.to_latex() for d in derivs if d.coefficient != 0]

    def _create_answer(self, data: dict) -> str:
        """Return the full partial derivative expression.

        Args:
            data: Solution data.

        Returns:
            LaTeX expression for the combined partial derivative.
        """
        derivs = data["derivs"]
        nonzero = [d for d in derivs if d.coefficient != 0]
        if not nonzero:
            return "0"
        return "+".join(d.to_latex() for d in nonzero)
