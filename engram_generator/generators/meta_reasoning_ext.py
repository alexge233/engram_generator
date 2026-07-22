"""Extended tier 7-10 generators — constraint optimisation through emergent capability.

Completes the reasoning curriculum with 18 generators spanning:
- Tier 7 (meta-reasoning): constraint optimisation, problem construction,
  complexity analysis, error correction, identity derivation.
- Tier 8 (creative): minimal axioms, novel problem design, solution elegance.
- Tier 9 (research): reduction proofs, learning bounds, hypothesis design,
  meta-pattern recognition, representation choice.
- Tier 10 (self-architecture): training diagnosis, failure mode classification,
  data prescription, efficiency analysis, emergent capability prediction.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


class ConstraintPool:
    """Encapsulates a constrained optimisation problem.

    Stores an objective function and a set of linear constraints,
    providing evaluation and feasibility checking on integer points.

    Attributes:
        objective_name: Description of the objective.
        constraint_descriptions: Human-readable constraint list.

    Example:
        >>> pool = ConstraintPool("maximise 3x+2y", [(3, 2, 18)], [(1, 1, 8)])
        >>> pool.evaluate_objective(2, 3)
        12
        >>> pool.is_feasible(2, 3)
        True
    """

    def __init__(self, objective_name: str,
                 le_constraints: list[tuple[int, int, int]],
                 eq_constraints: list[tuple[int, int, int]] | None = None) -> None:
        """Initialise the constraint pool.

        Args:
            objective_name: Human-readable objective description.
            le_constraints: List of (a, b, c) for ax + by <= c.
            eq_constraints: Optional list of (a, b, c) for ax + by = c.
        """
        self._objective_name = objective_name
        self._le_constraints = le_constraints
        self._eq_constraints = eq_constraints or []

    @property
    def objective_name(self) -> str:
        """Return the objective description."""
        return self._objective_name

    @property
    def constraint_descriptions(self) -> list[str]:
        """Return human-readable constraint descriptions.

        Returns:
            List of constraint strings.
        """
        parts: list[str] = []
        for a, b, c in self._le_constraints:
            parts.append(f"{a}x+{b}y <= {c}")
        for a, b, c in self._eq_constraints:
            parts.append(f"{a}x+{b}y = {c}")
        return parts

    def evaluate_objective(self, x: int, y: int) -> int:
        """Evaluate the objective placeholder at (x, y).

        Args:
            x: First variable value.
            y: Second variable value.

        Returns:
            Objective value (caller provides coefficients).
        """
        return x + y

    def is_feasible(self, x: int, y: int) -> bool:
        """Check whether a point satisfies all constraints.

        Args:
            x: First variable value.
            y: Second variable value.

        Returns:
            True if all constraints are satisfied.
        """
        for a, b, c in self._le_constraints:
            if a * x + b * y > c:
                return False
        for a, b, c in self._eq_constraints:
            if a * x + b * y != c:
                return False
        return True


class IdentityVerifier:
    """Verifies algebraic and trigonometric identities at test points.

    Evaluates both sides of an identity at multiple points and
    checks whether they agree within a tolerance.

    Example:
        >>> v = IdentityVerifier()
        >>> v.check_polynomial_identity([1, 0, -1], [1, -1, 1, 1], [0, 1, -1, 2])
        True
    """

    def check_polynomial_identity(self, lhs_coeffs: list[int],
                                  rhs_coeffs: list[int],
                                  test_points: list[int]) -> bool:
        """Check if two polynomials agree at all test points.

        Args:
            lhs_coeffs: Coefficients of the left-hand side.
            rhs_coeffs: Coefficients of the right-hand side.
            test_points: Points at which to evaluate.

        Returns:
            True if both sides agree at every test point.
        """
        for x in test_points:
            if self._eval_poly(lhs_coeffs, x) != self._eval_poly(rhs_coeffs, x):
                return False
        return True

    def _eval_poly(self, coeffs: list[int], x: int) -> int:
        """Evaluate a polynomial via Horner's method.

        Args:
            coeffs: Coefficients from highest degree to constant.
            x: Point to evaluate at.

        Returns:
            Polynomial value at x.
        """
        result = 0
        for c in coeffs:
            result = result * x + c
        return result


class TrainingCurveAnalyser:
    """Analyses training curves to diagnose common pathologies.

    Provides pattern matching on loss sequences to identify
    plateaus, oscillations, divergence, and overfitting.

    Example:
        >>> a = TrainingCurveAnalyser()
        >>> a.detect_pattern([5.0, 4.0, 3.5, 3.4, 3.39, 3.38])
        'plateau'
    """

    def detect_pattern(self, losses: list[float]) -> str:
        """Detect the dominant pattern in a loss curve.

        Args:
            losses: Sequence of loss values over epochs.

        Returns:
            Pattern name: 'plateau', 'divergence', 'oscillation', or 'normal'.
        """
        if self._is_diverging(losses):
            return "divergence"
        if self._is_oscillating(losses):
            return "oscillation"
        if self._is_plateau(losses):
            return "plateau"
        return "normal"

    def _is_plateau(self, losses: list[float]) -> bool:
        """Check if the loss curve has plateaued.

        Args:
            losses: Sequence of loss values.

        Returns:
            True if recent improvements are negligible.
        """
        if len(losses) < 4:
            return False
        recent = losses[-4:]
        spread = max(recent) - min(recent)
        return spread < 0.05 * abs(recent[0]) if recent[0] != 0 else spread < 0.01

    def _is_diverging(self, losses: list[float]) -> bool:
        """Check if the loss is increasing.

        Args:
            losses: Sequence of loss values.

        Returns:
            True if loss is trending upward.
        """
        if len(losses) < 3:
            return False
        return losses[-1] > losses[-2] > losses[-3]

    def _is_oscillating(self, losses: list[float]) -> bool:
        """Check if the loss is oscillating.

        Args:
            losses: Sequence of loss values.

        Returns:
            True if loss alternates between increasing and decreasing.
        """
        if len(losses) < 5:
            return False
        direction_changes = 0
        for i in range(2, len(losses)):
            prev_dir = losses[i - 1] - losses[i - 2]
            curr_dir = losses[i] - losses[i - 1]
            if prev_dir * curr_dir < 0:
                direction_changes += 1
        return direction_changes >= 3


class FlopCounter:
    """Counts floating-point operations for common neural network layers.

    Provides FLOP estimates for linear layers, attention, convolution,
    and normalization operations.

    Example:
        >>> c = FlopCounter()
        >>> c.linear_flops(512, 2048, 128)
        268435456
    """

    def linear_flops(self, d_in: int, d_out: int, seq_len: int) -> int:
        """Count FLOPs for a linear layer.

        Args:
            d_in: Input dimension.
            d_out: Output dimension.
            seq_len: Sequence length (batch dimension).

        Returns:
            Total FLOPs (multiply-add counted as 2 ops).
        """
        return 2 * seq_len * d_in * d_out

    def attention_flops(self, seq_len: int, d_model: int, n_heads: int) -> int:
        """Count FLOPs for multi-head self-attention.

        Args:
            seq_len: Sequence length.
            d_model: Model dimension.
            n_heads: Number of attention heads.

        Returns:
            Total FLOPs for Q, K, V projections and attention.
        """
        qkv = 3 * self.linear_flops(d_model, d_model, seq_len)
        attn = 2 * n_heads * seq_len * seq_len * (d_model // n_heads)
        output = self.linear_flops(d_model, d_model, seq_len)
        return qkv + attn + output

    def ffn_flops(self, d_model: int, d_ff: int, seq_len: int) -> int:
        """Count FLOPs for a feed-forward network block.

        Args:
            d_model: Model dimension.
            d_ff: Feed-forward hidden dimension.
            seq_len: Sequence length.

        Returns:
            Total FLOPs for two linear layers.
        """
        return self.linear_flops(d_model, d_ff, seq_len) + self.linear_flops(d_ff, d_model, seq_len)


@register
class ConstraintOptimisationGenerator(StepGenerator):
    """Minimise or maximise an objective subject to linear constraints.

    Generates a 2-variable linear programming problem with integer
    vertex solutions. The model must identify the feasible region,
    evaluate the objective at each vertex, and select the optimum.

    Input format:
        ``optimise objective subject to constraints``

    Target format:
        ``maximise 3x+2y subject to x+y<=8, 2x+y<=12, x>=0, y>=0
        <step> vertices: (0,0),(0,8),(4,4),(6,0) <step> evaluate:
        f(0,0)=0, f(0,8)=16, f(4,4)=20, f(6,0)=18 <step>
        optimal: (4,4), value=20 <step> 20``

    Difficulty scaling:
        Difficulty 1-2: 2 constraints, small coefficients.
        Difficulty 3-4: 3 constraints.
        Difficulty 5-6: 3 constraints with larger coefficients.
        Difficulty 7-8: 4 constraints.

    Prerequisites:
        lagrange_multiplier.

    Example:
        >>> gen = ConstraintOptimisationGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'constraint_optimisation'
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "constraint_optimisation"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["lagrange_multiplier"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls number of constraints.

        Returns:
            Natural language description.
        """
        return "optimise objective subject to constraints"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a linear programming problem with known vertex solution.

        Args:
            difficulty: Controls constraint count and coefficient magnitude.

        Returns:
            Tuple of (problem_string, solution_data).
        """
        obj_a = self._rng.randint(1, 3 + difficulty)
        obj_b = self._rng.randint(1, 3 + difficulty)
        x_max = self._rng.randint(4, 6 + difficulty)
        y_max = self._rng.randint(4, 6 + difficulty)
        c1_a = self._rng.randint(1, 3)
        c1_b = self._rng.randint(1, 3)
        c1_rhs = c1_a * x_max + c1_b * self._rng.randint(1, y_max)
        constraints = [(c1_a, c1_b, c1_rhs)]
        if difficulty >= 3:
            c2_a = self._rng.randint(1, 2)
            c2_b = self._rng.randint(1, 3)
            c2_rhs = c2_a * self._rng.randint(2, x_max) + c2_b * y_max
            constraints.append((c2_a, c2_b, c2_rhs))
        vertices = self._find_integer_vertices(constraints, x_max, y_max)
        if not vertices:
            vertices = [(0, 0), (x_max, 0), (0, y_max)]
        best_vertex = max(vertices, key=lambda p: obj_a * p[0] + obj_b * p[1])
        best_value = obj_a * best_vertex[0] + obj_b * best_vertex[1]
        evaluations = {v: obj_a * v[0] + obj_b * v[1] for v in vertices}
        constraint_strs = [f"{a}x+{b}y<={c}" for a, b, c in constraints]
        constraint_strs.extend(["x>=0", "y>=0"])
        problem = f"maximise {obj_a}x+{obj_b}y subject to {', '.join(constraint_strs)}"
        return problem, {
            "obj_a": obj_a, "obj_b": obj_b,
            "constraints": constraints,
            "vertices": vertices,
            "evaluations": evaluations,
            "best_vertex": best_vertex,
            "best_value": best_value,
        }

    def _find_integer_vertices(self, constraints: list[tuple[int, int, int]],
                               x_max: int, y_max: int) -> list[tuple[int, int]]:
        """Find feasible integer vertices of the constraint polytope.

        Args:
            constraints: List of (a, b, rhs) for ax+by<=rhs.
            x_max: Maximum x bound.
            y_max: Maximum y bound.

        Returns:
            List of feasible (x, y) vertex points.
        """
        candidates: list[tuple[int, int]] = [(0, 0)]
        for a, b, c in constraints:
            if a > 0:
                candidates.append((c // a, 0))
            if b > 0:
                candidates.append((0, c // b))
        for i in range(len(constraints)):
            for j in range(i + 1, len(constraints)):
                pt = self._intersect(constraints[i], constraints[j])
                if pt is not None:
                    candidates.append(pt)
        pool = ConstraintPool("", constraints)
        feasible: list[tuple[int, int]] = []
        for x, y in candidates:
            if x >= 0 and y >= 0 and pool.is_feasible(x, y):
                if (x, y) not in feasible:
                    feasible.append((x, y))
        return sorted(feasible)

    def _intersect(self, c1: tuple[int, int, int],
                   c2: tuple[int, int, int]) -> tuple[int, int] | None:
        """Find the integer intersection of two constraint boundaries.

        Args:
            c1: First constraint (a1, b1, rhs1).
            c2: Second constraint (a2, b2, rhs2).

        Returns:
            Integer (x, y) if the intersection is integral, else None.
        """
        a1, b1, r1 = c1
        a2, b2, r2 = c2
        det = a1 * b2 - a2 * b1
        if det == 0:
            return None
        x_num = r1 * b2 - r2 * b1
        y_num = a1 * r2 - a2 * r1
        if x_num % det != 0 or y_num % det != 0:
            return None
        return (x_num // det, y_num // det)

    def _create_steps(self, data: dict) -> list[str]:
        """Generate optimisation steps.

        Args:
            data: Solution data with vertices and evaluations.

        Returns:
            Steps showing vertex enumeration, evaluation, and selection.
        """
        vert_str = ", ".join(f"({x},{y})" for x, y in data["vertices"])
        eval_parts = [
            f"f({x},{y})={v}" for (x, y), v in data["evaluations"].items()
        ]
        bx, by = data["best_vertex"]
        return [
            f"vertices: {vert_str}",
            f"evaluate: {', '.join(eval_parts)}",
            f"optimal: ({bx},{by}), value={data['best_value']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the optimal objective value.

        Args:
            data: Solution data.

        Returns:
            String of the optimal value.
        """
        return str(data["best_value"])


@register
class ProblemConstructionGenerator(StepGenerator):
    """Create a valid mathematical problem from specifications and solve it.

    Generates a polynomial from random roots and coefficients, then
    presents the construction task. Verification evaluates the
    polynomial at the roots to confirm they yield zero.

    Input format:
        ``construct a problem and solve it``

    Target format:
        ``construct degree-2 polynomial with roots 3,-2 <step>
        factors: (x-3)(x+2) <step> expand: x^2-x-6 <step>
        verify: p(3)=9-3-6=0, p(-2)=4+2-6=0 <step> x^2-x-6``

    Difficulty scaling:
        Difficulty 1-2: quadratic with 2 small roots.
        Difficulty 3-4: quadratic with larger roots.
        Difficulty 5-6: cubic with 3 roots.
        Difficulty 7-8: cubic with scaling coefficient.

    Prerequisites:
        construct_polynomial.

    Example:
        >>> gen = ProblemConstructionGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'problem_construction'
    """

    _DEGREE_MAP = {
        1: 2, 2: 2, 3: 2, 4: 2, 5: 3, 6: 3, 7: 3, 8: 3,
    }

    _ROOT_RANGE = {
        1: (-3, 3), 2: (-4, 4), 3: (-5, 5), 4: (-6, 6),
        5: (-4, 4), 6: (-5, 5), 7: (-6, 6), 8: (-8, 8),
    }

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "problem_construction"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["construct_polynomial"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls degree and root magnitude.

        Returns:
            Natural language description.
        """
        return "construct a problem and solve it"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a polynomial construction problem.

        Args:
            difficulty: Controls polynomial degree and root range.

        Returns:
            Tuple of (specification, solution_data).
        """
        degree = self._DEGREE_MAP.get(difficulty, 2)
        lo, hi = self._ROOT_RANGE.get(difficulty, (-4, 4))
        roots = self._sample_roots(degree, lo, hi)
        lead = self._rng.randint(1, 1 + difficulty // 6)
        coeffs = self._expand_roots(roots, lead)
        verifications = {r: self._eval_poly(coeffs, r) for r in roots}
        problem = f"construct degree-{degree} polynomial with roots {','.join(str(r) for r in roots)}"
        return problem, {
            "degree": degree, "roots": roots, "lead": lead,
            "coeffs": coeffs, "verifications": verifications,
        }

    def _sample_roots(self, count: int, lo: int, hi: int) -> list[int]:
        """Sample distinct non-zero integer roots.

        Args:
            count: Number of roots.
            lo: Minimum root value.
            hi: Maximum root value.

        Returns:
            Sorted list of distinct roots.
        """
        pool = [x for x in range(lo, hi + 1) if x != 0]
        return sorted(self._rng.sample(pool, min(count, len(pool))))

    def _expand_roots(self, roots: list[int], lead: int) -> list[int]:
        """Expand roots into polynomial coefficients.

        Args:
            roots: List of integer roots.
            lead: Leading coefficient multiplier.

        Returns:
            Coefficients from highest degree to constant.
        """
        coeffs = [1]
        for r in roots:
            new = [0] * (len(coeffs) + 1)
            for i, c in enumerate(coeffs):
                new[i] += c
                new[i + 1] -= c * r
            coeffs = new
        return [c * lead for c in coeffs]

    def _eval_poly(self, coeffs: list[int], x: int) -> int:
        """Evaluate polynomial at x via Horner's method.

        Args:
            coeffs: Coefficients from highest degree to constant.
            x: Evaluation point.

        Returns:
            Polynomial value at x.
        """
        result = 0
        for c in coeffs:
            result = result * x + c
        return result

    def _format_factors(self, roots: list[int]) -> str:
        """Format polynomial as product of linear factors.

        Args:
            roots: List of roots.

        Returns:
            String like '(x-3)(x+2)'.
        """
        parts: list[str] = []
        for r in roots:
            if r >= 0:
                parts.append(f"(x-{r})")
            else:
                parts.append(f"(x+{abs(r)})")
        return "".join(parts)

    def _format_poly(self, coeffs: list[int]) -> str:
        """Format coefficients as a polynomial string.

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
            is_first = len(parts) == 0
            sign = "-" if c < 0 else ("" if is_first else "+")
            ac = abs(c)
            if power == 0:
                parts.append(f"{sign}{ac}")
            elif power == 1:
                body = "x" if ac == 1 else f"{ac}x"
                parts.append(f"{sign}{body}")
            else:
                body = f"x^{power}" if ac == 1 else f"{ac}x^{power}"
                parts.append(f"{sign}{body}")
        return "".join(parts) if parts else "0"

    def _create_steps(self, data: dict) -> list[str]:
        """Generate construction and verification steps.

        Args:
            data: Solution data with roots and coefficients.

        Returns:
            Steps showing factors, expansion, and root verification.
        """
        roots = data["roots"]
        coeffs = data["coeffs"]
        factors_str = self._format_factors(roots)
        poly_str = self._format_poly(coeffs)
        verify_parts = [f"p({r})={data['verifications'][r]}" for r in roots]
        return [
            f"factors: {factors_str}",
            f"expand: {poly_str}",
            f"verify: {', '.join(verify_parts)}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the constructed polynomial.

        Args:
            data: Solution data.

        Returns:
            Polynomial string.
        """
        return self._format_poly(data["coeffs"])


@register
class ComplexityAnalysisGenerator(StepGenerator):
    """Analyse and compare the step counts of two algorithmic approaches.

    Presents a problem solvable by two approaches with different
    complexity classes, computes concrete step counts for a given
    input size, and identifies which is faster.

    Input format:
        ``analyse complexity of two approaches``

    Target format:
        ``problem: find element in sorted list of 128 elements <step>
        approach A: linear scan -> 128 comparisons <step>
        approach B: binary search -> 8 comparisons <step>
        ratio: 128/8 = 16x faster <step> binary search (8 steps)``

    Difficulty scaling:
        Difficulty 1-2: linear vs binary search (n=32..64).
        Difficulty 3-4: quadratic vs n*log(n) sort (n=16..32).
        Difficulty 5-6: exponential vs polynomial (n=10..15).
        Difficulty 7-8: cubic vs quadratic (n=20..50).

    Prerequisites:
        algorithm_design (tier 9).

    Example:
        >>> gen = ComplexityAnalysisGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'complexity_analysis'
    """

    _PROBLEM_TYPES = {
        1: "linear_vs_binary", 2: "linear_vs_binary",
        3: "quadratic_vs_nlogn", 4: "quadratic_vs_nlogn",
        5: "exp_vs_poly", 6: "exp_vs_poly",
        7: "cubic_vs_quadratic", 8: "cubic_vs_quadratic",
    }

    _N_RANGES = {
        1: (32, 64), 2: (64, 128), 3: (16, 32), 4: (32, 64),
        5: (10, 15), 6: (12, 18), 7: (20, 30), 8: (30, 50),
    }

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "complexity_analysis"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 9

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["algorithm_design"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls problem type and input size.

        Returns:
            Natural language description.
        """
        return "analyse complexity of two approaches"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a complexity analysis problem.

        Args:
            difficulty: Controls problem type and size.

        Returns:
            Tuple of (problem_description, solution_data).
        """
        ptype = self._rng.choice(list(self._PROBLEM_TYPES.values()))
        lo, hi = self._N_RANGES.get(difficulty, (32, 64))
        n = self._rng.randint(lo, hi)
        builder = self._get_builder(ptype)
        return builder(n)

    def _get_builder(self, ptype: str):
        """Return the builder for the given problem type.

        Args:
            ptype: Problem type string.

        Returns:
            Builder method.
        """
        return {
            "linear_vs_binary": self._build_linear_vs_binary,
            "quadratic_vs_nlogn": self._build_quadratic_vs_nlogn,
            "exp_vs_poly": self._build_exp_vs_poly,
            "cubic_vs_quadratic": self._build_cubic_vs_quadratic,
        }[ptype]

    def _build_linear_vs_binary(self, n: int) -> tuple[str, dict]:
        """Build a linear vs binary search comparison.

        Args:
            n: Input size.

        Returns:
            Tuple of (problem_string, solution_data).
        """
        steps_a = n
        steps_b = int(math.log2(n)) + 1
        return f"find element in sorted list of {n} elements", {
            "n": n, "algo_a": "linear scan", "algo_b": "binary search",
            "steps_a": steps_a, "steps_b": steps_b,
            "complexity_a": "O(n)", "complexity_b": "O(log n)",
            "winner": "binary search", "ratio": steps_a / max(steps_b, 1),
        }

    def _build_quadratic_vs_nlogn(self, n: int) -> tuple[str, dict]:
        """Build a quadratic vs n*log(n) sort comparison.

        Args:
            n: Input size.

        Returns:
            Tuple of (problem_string, solution_data).
        """
        steps_a = n * n
        steps_b = int(n * math.log2(n))
        return f"sort {n} elements", {
            "n": n, "algo_a": "selection sort", "algo_b": "merge sort",
            "steps_a": steps_a, "steps_b": steps_b,
            "complexity_a": "O(n^2)", "complexity_b": "O(n log n)",
            "winner": "merge sort", "ratio": steps_a / max(steps_b, 1),
        }

    def _build_exp_vs_poly(self, n: int) -> tuple[str, dict]:
        """Build an exponential vs polynomial comparison.

        Args:
            n: Input size.

        Returns:
            Tuple of (problem_string, solution_data).
        """
        steps_a = 2 ** n
        steps_b = n * n
        return f"solve problem of size {n}", {
            "n": n, "algo_a": "brute force", "algo_b": "dynamic programming",
            "steps_a": steps_a, "steps_b": steps_b,
            "complexity_a": "O(2^n)", "complexity_b": "O(n^2)",
            "winner": "dynamic programming", "ratio": steps_a / max(steps_b, 1),
        }

    def _build_cubic_vs_quadratic(self, n: int) -> tuple[str, dict]:
        """Build a cubic vs quadratic comparison.

        Args:
            n: Input size.

        Returns:
            Tuple of (problem_string, solution_data).
        """
        steps_a = n * n * n
        steps_b = n * n
        return f"process {n} items", {
            "n": n, "algo_a": "triple nested loop", "algo_b": "optimised quadratic",
            "steps_a": steps_a, "steps_b": steps_b,
            "complexity_a": "O(n^3)", "complexity_b": "O(n^2)",
            "winner": "optimised quadratic", "ratio": steps_a / max(steps_b, 1),
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate analysis steps.

        Args:
            data: Solution data with both approaches.

        Returns:
            Steps showing each approach's cost and ratio.
        """
        ratio = data["ratio"]
        return [
            f"approach A: {data['algo_a']} {data['complexity_a']} -> {data['steps_a']} steps",
            f"approach B: {data['algo_b']} {data['complexity_b']} -> {data['steps_b']} steps",
            f"ratio: {data['steps_a']}/{data['steps_b']} = {ratio:.1f}x faster",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the winning approach.

        Args:
            data: Solution data.

        Returns:
            Winner with step count.
        """
        return f"{data['winner']} ({data['steps_b']} steps)"


@register
class ErrorCorrectionGenerator(StepGenerator):
    """Fix a flawed arithmetic proof by identifying and correcting the error.

    Generates a correct computation, corrupts one step, and asks the
    model to both identify the error AND produce the corrected chain.

    Input format:
        ``fix the error in this computation``

    Target format:
        ``5+3+7+2=17; shown steps: 5,9,16,17 <step> step 2 wrong:
        shows 9, should be 8 <step> correct chain: 5,8,15,17 <step>
        corrected answer: 17 <step> 17``

    Difficulty scaling:
        Difficulty 1-2: 3-step addition chain.
        Difficulty 3-4: 4-step chain.
        Difficulty 5-6: 5-step chain.
        Difficulty 7-8: 6-step chain with larger numbers.

    Prerequisites:
        error_detection.

    Example:
        >>> gen = ErrorCorrectionGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'error_correction'
    """

    _CHAIN_LENGTHS = {
        1: 3, 2: 3, 3: 4, 4: 4, 5: 5, 6: 5, 7: 6, 8: 6,
    }

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "error_correction"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["error_detection"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls chain length.

        Returns:
            Natural language description.
        """
        return "fix the error in this computation"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a computation with one planted error and its correction.

        Args:
            difficulty: Controls chain length and number magnitude.

        Returns:
            Tuple of (corrupted_chain, solution_data).
        """
        length = self._CHAIN_LENGTHS.get(difficulty, 4)
        upper = 10 ** min(difficulty, 3)
        operands = [self._rng.randint(1, upper) for _ in range(length)]
        correct_running = self._running_sums(operands)
        error_idx = self._rng.randint(0, len(correct_running) - 1)
        corrupted = correct_running[:]
        offset = self._rng.choice([-3, -2, -1, 1, 2, 3])
        for i in range(error_idx, len(corrupted)):
            corrupted[i] = correct_running[i] + offset
        ops_str = "+".join(str(x) for x in operands)
        shown_str = ",".join(str(s) for s in corrupted)
        problem = f"{ops_str}; shown steps: {shown_str}"
        return problem, {
            "operands": operands,
            "correct_running": correct_running,
            "corrupted": corrupted,
            "error_idx": error_idx,
            "correct_answer": sum(operands),
        }

    def _running_sums(self, operands: list[int]) -> list[int]:
        """Compute running cumulative sums.

        Args:
            operands: List of numbers to accumulate.

        Returns:
            List of running totals after each addition.
        """
        totals: list[int] = []
        running = operands[0]
        for i in range(1, len(operands)):
            running += operands[i]
            totals.append(running)
        return totals

    def _create_steps(self, data: dict) -> list[str]:
        """Generate error identification and correction steps.

        Args:
            data: Solution data with error location and correct values.

        Returns:
            Steps showing detection, correction, and verified answer.
        """
        idx = data["error_idx"]
        wrong = data["corrupted"][idx]
        correct = data["correct_running"][idx]
        correct_str = ",".join(str(s) for s in data["correct_running"])
        return [
            f"step {idx + 1} wrong: shows {wrong}, should be {correct}",
            f"correct chain: {correct_str}",
            f"corrected answer: {data['correct_answer']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the correct final answer.

        Args:
            data: Solution data.

        Returns:
            Correct answer string.
        """
        return str(data["correct_answer"])


@register
class DeriveIdentityGenerator(StepGenerator):
    """Prove a trigonometric or algebraic identity by manipulation.

    Presents a known identity and requires step-by-step algebraic
    manipulation to prove it. Verification checks both sides at
    test points.

    Input format:
        ``prove this identity``

    Target format:
        ``prove: (a+b)^2 - (a-b)^2 = 4ab <step> expand LHS:
        a^2+2ab+b^2 - (a^2-2ab+b^2) <step> = a^2+2ab+b^2-a^2+2ab-b^2
        <step> = 4ab = RHS <step> verify: a=3,b=2: LHS=25-1=24,
        RHS=4*6=24 <step> proven``

    Difficulty scaling:
        Difficulty 1-2: difference of squares identity.
        Difficulty 3-4: perfect square difference identity.
        Difficulty 5-6: sum/difference of cubes.
        Difficulty 7-8: binomial identity or mixed.

    Prerequisites:
        derive_formula.

    Example:
        >>> gen = DeriveIdentityGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'derive_identity'
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "derive_identity"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["derive_formula"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls identity complexity.

        Returns:
            Natural language description.
        """
        return "prove this identity"

    _IDENTITIES: list[dict] = [
        {"name": "difference of squares", "statement": "(a+b)(a-b) = a^2 - b^2",
         "proof_steps": ["expand LHS: a*a - a*b + b*a - b*b",
                         "= a^2 - ab + ab - b^2", "= a^2 - b^2 = RHS"],
         "test_a": 5, "test_b": 3, "lhs_val": 16, "rhs_val": 16},
        {"name": "square difference", "statement": "(a+b)^2 - (a-b)^2 = 4ab",
         "proof_steps": ["expand (a+b)^2 = a^2+2ab+b^2",
                         "expand (a-b)^2 = a^2-2ab+b^2",
                         "subtract: 2ab - (-2ab) = 4ab = RHS"],
         "test_a": 3, "test_b": 2, "lhs_val": 24, "rhs_val": 24},
        {"name": "sum of cubes",
         "statement": "a^3 + b^3 = (a+b)(a^2-ab+b^2)",
         "proof_steps": [
             "expand RHS: a*a^2 - a*ab + a*b^2 + b*a^2 - b*ab + b*b^2",
             "= a^3 - a^2b + ab^2 + a^2b - ab^2 + b^3",
             "cancel: = a^3 + b^3 = LHS"],
         "test_a": 2, "test_b": 3, "lhs_val": 35, "rhs_val": 35},
        {"name": "difference of cubes",
         "statement": "a^3 - b^3 = (a-b)(a^2+ab+b^2)",
         "proof_steps": [
             "expand RHS: a*a^2 + a*ab + a*b^2 - b*a^2 - b*ab - b*b^2",
             "= a^3 + a^2b + ab^2 - a^2b - ab^2 - b^3",
             "cancel: = a^3 - b^3 = LHS"],
         "test_a": 4, "test_b": 2, "lhs_val": 56, "rhs_val": 56},
        {"name": "perfect square trinomial",
         "statement": "(a+b)^2 = a^2 + 2ab + b^2",
         "proof_steps": ["expand: (a+b)(a+b) = a*a + a*b + b*a + b*b",
                         "= a^2 + 2ab + b^2"],
         "test_a": 3, "test_b": 4, "lhs_val": 49, "rhs_val": 49},
        {"name": "sum of arithmetic series", "statement": "1+2+...+n = n(n+1)/2",
         "proof_steps": ["S = 1 + 2 + ... + n", "S = n + (n-1) + ... + 1",
                         "2S = (n+1) + (n+1) + ... = n(n+1)", "S = n(n+1)/2"],
         "test_a": 10, "test_b": 0, "lhs_val": 55, "rhs_val": 55},
        {"name": "geometric sum",
         "statement": "1 + r + r^2 + ... + r^n = (r^{n+1}-1)/(r-1)",
         "proof_steps": ["S = 1 + r + ... + r^n", "rS = r + r^2 + ... + r^{n+1}",
                         "rS - S = r^{n+1} - 1", "S = (r^{n+1}-1)/(r-1)"],
         "test_a": 2, "test_b": 4, "lhs_val": 31, "rhs_val": 31},
        {"name": "binomial square difference",
         "statement": "(a+b)(a-b) = a^2 - b^2 (conjugate pair)",
         "proof_steps": ["LHS = a^2 - ab + ab - b^2 = a^2 - b^2"],
         "test_a": 7, "test_b": 3, "lhs_val": 40, "rhs_val": 40},
        {"name": "Cauchy-Schwarz for two terms",
         "statement": "(a1*b1 + a2*b2)^2 <= (a1^2+a2^2)(b1^2+b2^2)",
         "proof_steps": ["expand RHS - LHS", "= (a1*b2 - a2*b1)^2 >= 0",
                         "therefore LHS <= RHS always"],
         "test_a": 1, "test_b": 2, "lhs_val": 25, "rhs_val": 25},
        {"name": "AM-GM for two numbers",
         "statement": "(a+b)/2 >= sqrt(ab) for a,b >= 0",
         "proof_steps": ["equivalent to (a+b)^2 >= 4ab",
                         "a^2 + 2ab + b^2 >= 4ab", "a^2 - 2ab + b^2 >= 0",
                         "(a-b)^2 >= 0, always true"],
         "test_a": 3, "test_b": 12, "lhs_val": 8, "rhs_val": 6},
    ]

    def _get_identities(self, difficulty: int) -> list[dict]:
        """Return identities appropriate for the difficulty.

        Args:
            difficulty: Difficulty level.

        Returns:
            List of identity dictionaries.
        """
        n = len(self._IDENTITIES)
        if difficulty <= 2:
            return self._IDENTITIES[:max(3, n // 3)]
        if difficulty <= 5:
            return self._IDENTITIES[:max(5, 2 * n // 3)]
        return list(self._IDENTITIES)

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Select an identity and generate randomised test values.

        Args:
            difficulty: Controls which identities are available.

        Returns:
            Tuple of (identity_statement, solution_data).
        """
        pool = self._get_identities(difficulty)
        identity = dict(self._rng.choice(pool))
        # Randomise test values for variety
        test_a = self._rng.randint(2, 8 + difficulty)
        test_b = self._rng.randint(1, 6 + difficulty)
        identity["test_a"] = test_a
        identity["test_b"] = test_b
        # Recompute verification values based on identity name
        identity["lhs_val"], identity["rhs_val"] = self._compute_identity_values(
            identity["name"], test_a, test_b
        )
        problem = f"prove: {identity['statement']} (verify at a={test_a},b={test_b})"
        return problem, {"identity": identity}

    def _compute_identity_values(self, name: str, a: int, b: int) -> tuple:
        """Compute LHS and RHS values for an identity at given test points.

        Args:
            name: Identity name.
            a: First test value.
            b: Second test value.

        Returns:
            Tuple of (lhs_value, rhs_value).
        """
        if name == "difference of squares":
            return (a + b) * (a - b), a * a - b * b
        if name == "square difference":
            return (a + b) ** 2 - (a - b) ** 2, 4 * a * b
        if name == "sum of cubes":
            return a ** 3 + b ** 3, (a + b) * (a * a - a * b + b * b)
        if name == "difference of cubes":
            return a ** 3 - b ** 3, (a - b) * (a * a + a * b + b * b)
        if name == "perfect square trinomial":
            return (a + b) ** 2, a * a + 2 * a * b + b * b
        if name == "sum of arithmetic series":
            return a * (a + 1) // 2, a * (a + 1) // 2
        if name == "geometric sum":
            s = sum(a ** i for i in range(b + 1))
            return s, (a ** (b + 1) - 1) // (a - 1) if a != 1 else b + 1
        if name == "binomial square difference":
            return (a + b) * (a - b), a * a - b * b
        if name == "Cauchy-Schwarz for two terms":
            return (a * 1 + b * 2) ** 2, (a * a + b * b) * (1 + 4)
        if name == "AM-GM for two numbers":
            return (a + b) // 2, int((a * b) ** 0.5)
        return a, a

    def _create_steps(self, data: dict) -> list[str]:
        """Generate proof manipulation steps.

        Args:
            data: Solution data with identity info.

        Returns:
            Steps showing algebraic manipulation and verification.
        """
        identity = data["identity"]
        steps = list(identity["proof_steps"])
        a, b = identity["test_a"], identity["test_b"]
        steps.append(
            f"verify: a={a},b={b}: LHS={identity['lhs_val']}, "
            f"RHS={identity['rhs_val']}"
        )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the proven identity statement.

        Args:
            data: Solution data.

        Returns:
            Proof completion string.
        """
        return "proven"


@register
class MinimalAxiomsGenerator(StepGenerator):
    """Remove an unnecessary axiom from a derivation.

    Presents a derivation that uses N axioms, one of which is redundant
    (derivable from the others). The model must identify and remove it,
    producing a shorter derivation.

    Input format:
        ``identify the unnecessary axiom``

    Target format:
        ``axioms: A1: a+b=b+a, A2: a+0=a, A3: 0+a=a <step>
        A3 is redundant: by A1, 0+a = a+0 = a (by A2) <step>
        minimal set: {A1, A2} <step> A3 removed``

    Difficulty scaling:
        Difficulty 1-2: 3 axioms, one clearly redundant.
        Difficulty 3-4: 4 axioms, one redundant.
        Difficulty 5-6: 4 axioms, less obvious redundancy.
        Difficulty 7-8: 5 axioms, subtle redundancy.

    Prerequisites:
        derive_formula.

    Example:
        >>> gen = MinimalAxiomsGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'minimal_axioms'
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "minimal_axioms"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 8

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["derive_formula"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls axiom count.

        Returns:
            Natural language description.
        """
        return "identify the unnecessary axiom"

    def _get_axiom_sets(self, difficulty: int) -> list[dict]:
        """Return axiom sets appropriate for the difficulty.

        Args:
            difficulty: Difficulty level.

        Returns:
            List of axiom set dictionaries.
        """
        sets = [
            {
                "axioms": ["a+b=b+a", "a+0=a", "0+a=a"],
                "redundant_idx": 2,
                "redundant_name": "A3",
                "derivation": "by A1, 0+a = a+0 = a (by A2)",
                "minimal": ["a+b=b+a", "a+0=a"],
            },
            {
                "axioms": ["a*1=a", "1*a=a", "a*b=b*a", "a*0=0"],
                "redundant_idx": 1,
                "redundant_name": "A2",
                "derivation": "by A3, 1*a = a*1 = a (by A1)",
                "minimal": ["a*1=a", "a*b=b*a", "a*0=0"],
            },
            {
                "axioms": ["a+b=b+a", "(a+b)+c=a+(b+c)", "a+0=a", "a+(-a)=0", "0+a=a"],
                "redundant_idx": 4,
                "redundant_name": "A5",
                "derivation": "by A1, 0+a = a+0 = a (by A3)",
                "minimal": ["a+b=b+a", "(a+b)+c=a+(b+c)", "a+0=a", "a+(-a)=0"],
            },
            {
                "axioms": ["a*b=b*a", "(a*b)*c=a*(b*c)", "a*1=a", "a*(b+c)=a*b+a*c", "(b+c)*a=b*a+c*a"],
                "redundant_idx": 4,
                "redundant_name": "A5",
                "derivation": "by A1, (b+c)*a = a*(b+c) = a*b+a*c (by A4) = b*a+c*a (by A1 twice)",
                "minimal": ["a*b=b*a", "(a*b)*c=a*(b*c)", "a*1=a", "a*(b+c)=a*b+a*c"],
            },
        ]
        if difficulty <= 2:
            return sets[:1]
        if difficulty <= 4:
            return sets[:2]
        if difficulty <= 6:
            return sets[:3]
        return sets

    _VAR_SETS = [
        ("a", "b", "c"), ("x", "y", "z"), ("p", "q", "r"),
        ("u", "v", "w"), ("m", "n", "k"), ("s", "t", "r"),
    ]

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an axiom minimisation problem with randomised variable names.

        Args:
            difficulty: Controls axiom set complexity.

        Returns:
            Tuple of (axiom_list, solution_data).
        """
        pool = self._get_axiom_sets(difficulty)
        axiom_set = self._rng.choice(pool)
        # Randomise variable names for variety
        var_set = self._rng.choice(self._VAR_SETS)
        v1, v2, v3 = var_set
        axioms = [
            ax.replace("a", v1).replace("b", v2).replace("c", v3)
            for ax in axiom_set["axioms"]
        ]
        derivation = axiom_set["derivation"].replace("a", v1).replace("b", v2).replace("c", v3)
        label_offset = self._rng.randint(0, 3)
        labels = [f"A{i + 1 + label_offset}" for i in range(len(axioms))]
        axiom_strs = [f"{labels[i]}: {ax}" for i, ax in enumerate(axioms)]
        redundant_name = labels[axiom_set["redundant_idx"]]
        problem = f"axioms: {', '.join(axiom_strs)}"
        return problem, {
            "axioms": axioms,
            "redundant_idx": axiom_set["redundant_idx"],
            "redundant_name": redundant_name,
            "derivation": derivation,
            "minimal": [ax for i, ax in enumerate(axioms) if i != axiom_set["redundant_idx"]],
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate redundancy identification steps.

        Args:
            data: Solution data with redundant axiom info.

        Returns:
            Steps showing which axiom is redundant and why.
        """
        minimal_strs = [f"A{i + 1}" for i in range(len(data["axioms"])) if i != data["redundant_idx"]]
        return [
            f"{data['redundant_name']} is redundant: {data['derivation']}",
            f"minimal set: {{{', '.join(minimal_strs)}}}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return which axiom was removed.

        Args:
            data: Solution data.

        Returns:
            Removal statement.
        """
        return f"{data['redundant_name']} removed"


@register
class NovelProblemGenerator(StepGenerator):
    """Create a problem that requires a specific combination of skills.

    Constructs a multi-step problem where the solution requires
    applying two specified skills in sequence.

    Input format:
        ``create problem requiring factoring and evaluation``

    Target format:
        ``problem: find p(5) where p(x)=x^2-4x+3 <step> step 1:
        factor: (x-1)(x-3) <step> step 2: evaluate: (5-1)(5-3)=4*2=8
        <step> verify: 25-20+3=8 <step> 8``

    Difficulty scaling:
        Difficulty 1-2: factor then evaluate.
        Difficulty 3-4: derive then verify.
        Difficulty 5-6: construct then analyse.
        Difficulty 7-8: transform then optimise.

    Prerequisites:
        problem_construction.

    Example:
        >>> gen = NovelProblemGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'novel_problem'
    """

    _SKILL_COMBOS = {
        1: ("factor", "evaluate"),
        2: ("factor", "evaluate"),
        3: ("derive", "verify"),
        4: ("derive", "verify"),
        5: ("construct", "analyse"),
        6: ("construct", "analyse"),
        7: ("transform", "optimise"),
        8: ("transform", "optimise"),
    }

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "novel_problem"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 8

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["problem_construction"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls which skill pair is required.

        Returns:
            Natural language description.
        """
        s1, s2 = self._SKILL_COMBOS.get(difficulty, ("factor", "evaluate"))
        return f"create problem requiring {s1} and {s2}"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a multi-skill problem.

        Args:
            difficulty: Controls skill combination and magnitude.

        Returns:
            Tuple of (problem_string, solution_data).
        """
        s1, s2 = self._SKILL_COMBOS.get(difficulty, ("factor", "evaluate"))
        r1 = self._rng.randint(1, 3 + difficulty)
        r2 = self._rng.randint(-3 - difficulty, -1)
        b = -(r1 + r2)
        c = r1 * r2
        eval_x = self._rng.randint(r1 + 1, r1 + 5)
        eval_result = eval_x * eval_x + b * eval_x + c
        problem = f"find p({eval_x}) where p(x)=x^2+{b}x+{c}"
        return problem, {
            "skills": (s1, s2), "r1": r1, "r2": r2,
            "b": b, "c": c, "eval_x": eval_x,
            "eval_result": eval_result,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate multi-skill solution steps.

        Args:
            data: Solution data with skills and polynomial info.

        Returns:
            Steps showing each skill application.
        """
        r1, r2 = data["r1"], data["r2"]
        ex = data["eval_x"]
        s1, s2 = data["skills"]
        factor_str = f"(x-{r1})(x-{r2})" if r2 >= 0 else f"(x-{r1})(x+{abs(r2)})"
        val1 = ex - r1
        val2 = ex - r2
        return [
            f"step 1 ({s1}): {factor_str}",
            f"step 2 ({s2}): ({ex}-{r1})({ex}-{r2})={val1}*{val2}={val1 * val2}",
            f"verify: {ex}^2+{data['b']}*{ex}+{data['c']}={data['eval_result']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the evaluation result.

        Args:
            data: Solution data.

        Returns:
            Result string.
        """
        return str(data["eval_result"])


@register
class SolutionEleganceGenerator(StepGenerator):
    """Find a shorter proof than the given verbose solution.

    Presents a correct but long computation path and asks for a
    shorter algebraic shortcut that reaches the same answer.

    Input format:
        ``find a shorter solution``

    Target format:
        ``verbose: 97*103 = 97*100 + 97*3 = 9700+291 = 9991 (3 steps)
        <step> insight: (100-3)(100+3) = 100^2-9 <step>
        short: 10000-9=9991 (1 step) <step> 9991``

    Difficulty scaling:
        Difficulty 1-2: multiplication via difference of squares.
        Difficulty 3-4: addition via grouping.
        Difficulty 5-6: exponentiation via binomial shortcut.
        Difficulty 7-8: series summation via closed form.

    Prerequisites:
        complexity_reduction.

    Example:
        >>> gen = SolutionEleganceGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'solution_elegance'
    """

    _PATTERN_TYPES = {
        1: "diff_squares", 2: "diff_squares",
        3: "grouping", 4: "grouping",
        5: "binomial", 6: "binomial",
        7: "series_closed", 8: "series_closed",
    }

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "solution_elegance"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 8

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["complexity_reduction"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls shortcut type.

        Returns:
            Natural language description.
        """
        return "find a shorter solution"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a verbose computation with a known shortcut.

        Args:
            difficulty: Controls shortcut type.

        Returns:
            Tuple of (verbose_solution, solution_data).
        """
        pattern = self._rng.choice(list(self._PATTERN_TYPES.values()))
        builder = self._get_builder(pattern)
        return builder(difficulty)

    def _get_builder(self, pattern: str):
        """Return builder for the given pattern.

        Args:
            pattern: Pattern type string.

        Returns:
            Builder method.
        """
        return {
            "diff_squares": self._build_diff_squares,
            "grouping": self._build_grouping,
            "binomial": self._build_binomial,
            "series_closed": self._build_series,
        }[pattern]

    def _build_diff_squares(self, difficulty: int) -> tuple[str, dict]:
        """Build a difference-of-squares shortcut problem.

        Args:
            difficulty: Controls base value.

        Returns:
            Tuple of (verbose_string, solution_data).
        """
        base = self._rng.choice([10, 20, 50, 100]) * (1 + difficulty // 3)
        d = self._rng.randint(1, 5)
        a = base - d
        b = base + d
        result = a * b
        verbose_steps = 3
        verbose = f"{a}*{b} via {a}*{base} + {a}*{d} ({verbose_steps} steps)"
        shortcut = f"({base}-{d})({base}+{d}) = {base}^2-{d}^2 = {base * base}-{d * d} = {result}"
        return verbose, {
            "result": result, "verbose_steps": verbose_steps,
            "short_steps": 1, "insight": f"difference of squares: {base}^2-{d}^2",
            "shortcut": shortcut, "verbose": verbose,
        }

    def _build_grouping(self, difficulty: int) -> tuple[str, dict]:
        """Build a grouping shortcut problem.

        Args:
            difficulty: Controls number of terms.

        Returns:
            Tuple of (verbose_string, solution_data).
        """
        n = self._rng.randint(3, 4 + difficulty // 2)
        terms = [self._rng.randint(10, 50) for _ in range(n)]
        complement = 100 - terms[-1]
        terms[0] = complement
        result = sum(terms)
        verbose_parts = "+".join(str(t) for t in terms)
        verbose = f"{verbose_parts} computed left-to-right ({n - 1} additions)"
        shortcut = f"group {terms[0]}+{terms[-1]}=100, then add rest"
        return verbose, {
            "result": result, "verbose_steps": n - 1,
            "short_steps": max(1, n - 2),
            "insight": f"group complementary pair: {terms[0]}+{terms[-1]}=100",
            "shortcut": shortcut,
        }

    def _build_binomial(self, difficulty: int) -> tuple[str, dict]:
        """Build a binomial shortcut problem.

        Args:
            difficulty: Controls exponent.

        Returns:
            Tuple of (verbose_string, solution_data).
        """
        base = self._rng.randint(10, 20)
        result = base * base
        verbose = f"compute {base}^2 via long multiply (4+ digit operations)"
        d = base - 10 * (base // 10)
        tens = 10 * (base // 10)
        shortcut = f"({tens}+{d})^2 = {tens}^2+2*{tens}*{d}+{d}^2 = {tens * tens}+{2 * tens * d}+{d * d} = {result}"
        return verbose, {
            "result": result, "verbose_steps": 4,
            "short_steps": 2,
            "insight": f"binomial expansion of ({tens}+{d})^2",
            "shortcut": shortcut,
        }

    def _build_series(self, difficulty: int) -> tuple[str, dict]:
        """Build a series closed-form shortcut problem.

        Args:
            difficulty: Controls series length.

        Returns:
            Tuple of (verbose_string, solution_data).
        """
        n = self._rng.randint(5, 10 + difficulty)
        result = n * (n + 1) // 2
        verbose = f"1+2+3+...+{n} computed one-by-one ({n - 1} additions)"
        shortcut = f"n(n+1)/2 = {n}*{n + 1}/2 = {result}"
        return verbose, {
            "result": result, "verbose_steps": n - 1,
            "short_steps": 1,
            "insight": f"Gauss formula: n(n+1)/2",
            "shortcut": shortcut,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate elegance comparison steps.

        Args:
            data: Solution data with verbose and short paths.

        Returns:
            Steps showing insight and comparison.
        """
        return [
            f"insight: {data['insight']}",
            f"short: {data['shortcut']}",
            f"{data['short_steps']} steps vs {data['verbose_steps']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the computed result.

        Args:
            data: Solution data.

        Returns:
            Result string.
        """
        return str(data["result"])


@register
class ReductionGenerator(StepGenerator):
    """Show that problem A is at least as hard as problem B.

    Demonstrates a polynomial-time reduction from one well-known
    problem to another, proving a lower bound on hardness.

    Input format:
        ``show this problem is at least as hard as sorting``

    Target format:
        ``reduce sorting to element_uniqueness <step> given sorting
        oracle, check if adjacent elements equal in O(n) <step>
        sorting is Omega(n log n) so element_uniqueness is too
        <step> element_uniqueness >= Omega(n log n) <step>
        Omega(n log n)``

    Difficulty scaling:
        Difficulty 1-2: sorting reduces to uniqueness.
        Difficulty 3-4: 3SAT reduces to vertex cover.
        Difficulty 5-6: sorting reduces to closest pair.
        Difficulty 7-8: matrix multiply reduces to graph reachability.

    Prerequisites:
        algorithm_design, impossibility_proof.

    Example:
        >>> gen = ReductionGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'reduction'
    """

    _REDUCTION_TYPES = {
        1: "sort_to_uniqueness", 2: "sort_to_uniqueness",
        3: "sat_to_cover", 4: "sat_to_cover",
        5: "sort_to_closest", 6: "sort_to_closest",
        7: "matmul_to_reach", 8: "matmul_to_reach",
    }

    _REDUCTIONS: dict[str, dict] = {
        "sort_to_uniqueness": {
            "from": "sorting", "to": "element uniqueness",
            "steps": [
                "given sorting oracle, sort the array in O(n log n)",
                "scan adjacent elements for duplicates in O(n)",
                "sorting lower bound Omega(n log n) transfers",
            ],
            "bound": "Omega(n log n)",
            "test_input": "[4,1,3,1,2]",
            "test_result": "sort->[1,1,2,3,4]->duplicate found at index 0,1",
        },
        "sat_to_cover": {
            "from": "3-SAT", "to": "vertex cover",
            "steps": [
                "for each clause, create a triangle gadget of 3 vertices",
                "for each variable, create a pair of vertices (true/false)",
                "connect clause vertices to variable vertices matching literals",
                "3-SAT satisfiable iff vertex cover of size k exists",
            ],
            "bound": "NP-hard",
            "test_input": "(x1 OR x2) AND (NOT x1 OR x3)",
            "test_result": "2 triangles + 3 variable pairs -> 9 vertices, k=5",
        },
        "sort_to_closest": {
            "from": "sorting", "to": "closest pair",
            "steps": [
                "if we can find closest pair in f(n) time",
                "sorting can be done by repeated closest-pair extraction",
                "but sorting needs Omega(n log n)",
                "so closest pair needs Omega(n log n)",
            ],
            "bound": "Omega(n log n)",
            "test_input": "[7,1,4,9,2]",
            "test_result": "closest pair: (1,2), distance=1",
        },
        "matmul_to_reach": {
            "from": "matrix multiply", "to": "transitive closure",
            "steps": [
                "represent graph as adjacency matrix A",
                "A^n gives reachability in n steps",
                "matrix multiply lower bound transfers to graph reachability",
                "transitive closure is at least as hard as matrix multiply",
            ],
            "bound": "O(n^2.37) lower bound from matrix multiply",
            "test_input": "3x3 adjacency matrix",
            "test_result": "A^2 gives 2-hop reachability",
        },
    }

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "reduction"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 9

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["algorithm_design", "impossibility_proof"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls which reduction is presented.

        Returns:
            Natural language description.
        """
        rtype = self._rng.choice(list(self._REDUCTIONS.keys()))
        red = self._REDUCTIONS[rtype]
        return f"show {red['to']} is at least as hard as {red['from']}"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a reduction proof problem with randomised test inputs.

        Args:
            difficulty: Controls reduction type.

        Returns:
            Tuple of (problem_statement, solution_data).
        """
        rtype = self._rng.choice(list(self._REDUCTIONS.keys()))
        red = self._REDUCTIONS[rtype]
        # Generate randomised test inputs based on reduction type
        n = self._rng.randint(4, 10 + difficulty * 2)
        test_input, test_result = self._randomise_test(rtype, n)
        problem = f"reduce {red['from']} to {red['to']} (n={n})"
        return problem, {
            "from_problem": red["from"], "to_problem": red["to"],
            "proof_steps": red["steps"], "bound": red["bound"],
            "test_input": test_input, "test_result": test_result,
        }

    def _randomise_test(self, rtype: str, n: int) -> tuple[str, str]:
        """Generate randomised test input/result for a reduction type.

        Args:
            rtype: Reduction type key.
            n: Problem size parameter.

        Returns:
            Tuple of (test_input, test_result) strings.
        """
        if rtype == "sort_to_uniqueness":
            arr = [self._rng.randint(1, n * 2) for _ in range(n)]
            dup_idx = self._rng.randint(0, n - 2)
            arr[dup_idx + 1] = arr[dup_idx]
            s = sorted(arr)
            return f"{arr}", f"sort->{s}->duplicate found"
        if rtype == "sat_to_cover":
            clauses = self._rng.randint(2, 4 + n // 2)
            verts = clauses * 3 + n
            return (f"({clauses} clauses, {n} variables)",
                    f"{clauses} triangles + {n} variable pairs -> {verts} vertices")
        if rtype == "sort_to_closest":
            arr = sorted(self._rng.sample(range(1, n * 5), n))
            diffs = [arr[i + 1] - arr[i] for i in range(len(arr) - 1)]
            min_d = min(diffs)
            idx = diffs.index(min_d)
            return f"{arr}", f"closest pair: ({arr[idx]},{arr[idx+1]}), distance={min_d}"
        # matmul_to_reach
        return f"{n}x{n} adjacency matrix", f"A^2 gives 2-hop reachability for {n} nodes"

    def _create_steps(self, data: dict) -> list[str]:
        """Generate reduction proof steps.

        Args:
            data: Solution data with proof steps.

        Returns:
            Steps showing the reduction and test.
        """
        steps = list(data["proof_steps"])
        steps.append(f"test: {data['test_input']} -> {data['test_result']}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the proven bound.

        Args:
            data: Solution data.

        Returns:
            Bound string.
        """
        return data["bound"]


@register
class LearningBoundGenerator(StepGenerator):
    """Estimate sample complexity for a learning problem.

    Computes the number of samples needed to achieve a target
    accuracy with a given confidence, using VC-dimension or
    Hoeffding-style bounds.

    Input format:
        ``estimate samples needed for 95% accuracy``

    Target format:
        ``hypothesis class: linear classifiers in d=10 <step>
        VC dimension = d+1 = 11 <step> by VC bound:
        n >= (4/eps^2)(d*ln(2/eps) + ln(2/delta)) <step>
        with eps=0.05, delta=0.05: n >= 8802 <step> ~8802 samples``

    Difficulty scaling:
        Difficulty 1-2: simple Hoeffding bound.
        Difficulty 3-4: VC-dimension for linear classifiers.
        Difficulty 5-6: tighter PAC bound.
        Difficulty 7-8: information-theoretic lower bound.

    Prerequisites:
        binomial_dist, info_entropy.

    Example:
        >>> gen = LearningBoundGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'learning_bound'
    """

    _BOUND_TYPES = {
        1: "hoeffding", 2: "hoeffding",
        3: "vc_linear", 4: "vc_linear",
        5: "pac_tight", 6: "pac_tight",
        7: "info_lower", 8: "info_lower",
    }

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "learning_bound"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 9

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["binomial_dist", "info_entropy"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls bound type.

        Returns:
            Natural language description.
        """
        return "estimate samples needed for target accuracy"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a sample complexity estimation problem.

        Args:
            difficulty: Controls bound type.

        Returns:
            Tuple of (problem_spec, solution_data).
        """
        btype = self._rng.choice(list(self._BOUND_TYPES.values()))
        builder = self._get_builder(btype)
        return builder(difficulty)

    def _get_builder(self, btype: str):
        """Return builder for the given bound type.

        Args:
            btype: Bound type string.

        Returns:
            Builder method.
        """
        return {
            "hoeffding": self._build_hoeffding,
            "vc_linear": self._build_vc_linear,
            "pac_tight": self._build_pac_tight,
            "info_lower": self._build_info_lower,
        }[btype]

    def _build_hoeffding(self, difficulty: int) -> tuple[str, dict]:
        """Build a Hoeffding bound problem.

        Args:
            difficulty: Controls epsilon and delta.

        Returns:
            Tuple of (problem_string, solution_data).
        """
        eps = round(self._rng.uniform(0.01, 0.1), 2)
        delta = round(self._rng.uniform(0.01, 0.1), 2)
        n = int(math.ceil(math.log(2.0 / delta) / (2 * eps * eps)))
        problem = f"estimate n for |mean - E[X]| < {eps} with probability {1 - delta}"
        return problem, {
            "bound_type": "Hoeffding",
            "formula": "n >= ln(2/delta) / (2*eps^2)",
            "eps": eps, "delta": delta, "n_samples": n,
            "explanation": f"ln(2/{delta}) / (2*{eps}^2) = {n}",
        }

    def _build_vc_linear(self, difficulty: int) -> tuple[str, dict]:
        """Build a VC-dimension bound for linear classifiers.

        Args:
            difficulty: Controls dimension.

        Returns:
            Tuple of (problem_string, solution_data).
        """
        d = self._rng.randint(2, 5) * difficulty
        eps = round(self._rng.uniform(0.02, 0.1), 2)
        delta = 0.05
        vc_dim = d + 1
        n = int(math.ceil((4 / (eps * eps)) * (vc_dim * math.log(2 / eps) + math.log(2 / delta))))
        problem = f"linear classifiers in d={d}, target error < {eps}"
        return problem, {
            "bound_type": "VC bound",
            "formula": "n >= (4/eps^2)(VC*ln(2/eps) + ln(2/delta))",
            "d": d, "vc_dim": vc_dim, "eps": eps, "delta": delta,
            "n_samples": n,
            "explanation": f"VC dim = {vc_dim}, n >= {n}",
        }

    def _build_pac_tight(self, difficulty: int) -> tuple[str, dict]:
        """Build a tighter PAC bound problem.

        Args:
            difficulty: Controls dimension and target.

        Returns:
            Tuple of (problem_string, solution_data).
        """
        d = self._rng.randint(3, 8) * difficulty
        eps = round(self._rng.uniform(0.01, 0.05), 2)
        delta = 0.05
        n = int(math.ceil((d + math.log(1 / delta)) / eps))
        problem = f"PAC learning in d={d}, error < {eps}, confidence {1 - delta}"
        return problem, {
            "bound_type": "PAC tight",
            "formula": "n >= (d + ln(1/delta)) / eps",
            "d": d, "eps": eps, "delta": delta, "n_samples": n,
            "explanation": f"({d} + ln(1/{delta})) / {eps} = {n}",
        }

    def _build_info_lower(self, difficulty: int) -> tuple[str, dict]:
        """Build an information-theoretic lower bound problem.

        Args:
            difficulty: Controls hypothesis class size.

        Returns:
            Tuple of (problem_string, solution_data).
        """
        k = self._rng.randint(2, 5) * difficulty
        bits_needed = k
        n = int(math.ceil(bits_needed / math.log2(3)))
        problem = f"distinguish among 2^{k} hypotheses"
        return problem, {
            "bound_type": "information-theoretic",
            "formula": "n >= k / log2(3) (Fano inequality)",
            "k": k, "n_samples": n,
            "explanation": f"need {bits_needed} bits, each sample gives log2(3) bits -> n >= {n}",
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate bound derivation steps.

        Args:
            data: Solution data with bound info.

        Returns:
            Steps showing the bound formula and computation.
        """
        return [
            f"bound type: {data['bound_type']}",
            f"formula: {data['formula']}",
            data["explanation"],
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the estimated sample count.

        Args:
            data: Solution data.

        Returns:
            Sample count string.
        """
        return f"~{data['n_samples']} samples"


@register
class HypothesisDesignGenerator(StepGenerator):
    """Design an experiment to test a given hypothesis.

    Presents a hypothesis about a system and asks the model to
    design an experiment with controlled variables, measurements,
    and success criteria.

    Input format:
        ``design experiment to test this hypothesis``

    Target format:
        ``hypothesis: learning rate 0.01 gives lower loss than 0.1
        <step> control: fix all other hyperparameters <step>
        measure: validation loss after 100 epochs <step>
        run: train with lr=0.01 and lr=0.1 <step>
        criterion: lr=0.01 wins if val_loss is lower by > 0.5%
        <step> controlled experiment with 2 conditions``

    Difficulty scaling:
        Difficulty 1-2: single hyperparameter comparison.
        Difficulty 3-4: architecture comparison.
        Difficulty 5-6: data augmentation effect.
        Difficulty 7-8: multi-factor experiment.

    Prerequisites:
        method_selection.

    Example:
        >>> gen = HypothesisDesignGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'hypothesis_design'
    """

    _EXPERIMENT_TYPES = {
        1: "learning_rate", 2: "learning_rate",
        3: "architecture", 4: "architecture",
        5: "augmentation", 6: "augmentation",
        7: "multi_factor", 8: "multi_factor",
    }

    _EXPERIMENTS: dict[str, dict] = {
        "learning_rate": {
            "hypothesis": "learning rate 0.01 gives lower final loss than 0.1",
            "control": "fix architecture, data, batch size, epochs",
            "variable": "learning rate: {0.01, 0.1}",
            "measure": "validation loss after 100 epochs",
            "criterion": "lr=0.01 wins if val_loss lower by > 0.5%",
            "conditions": 2,
        },
        "architecture": {
            "hypothesis": "deeper network (6 layers) outperforms shallow (3 layers)",
            "control": "fix total parameter count, learning rate, data",
            "variable": "depth: {3 layers, 6 layers}",
            "measure": "test accuracy after convergence",
            "criterion": "deep wins if accuracy > 1% higher",
            "conditions": 2,
        },
        "augmentation": {
            "hypothesis": "data augmentation improves generalisation",
            "control": "fix model, learning rate, training epochs",
            "variable": "augmentation: {none, random crop + flip}",
            "measure": "gap between train and test accuracy",
            "criterion": "augmentation helps if gap shrinks by > 2%",
            "conditions": 2,
        },
        "multi_factor": {
            "hypothesis": "batch size and learning rate interact",
            "control": "fix architecture, data, epochs",
            "variable": "batch_size x lr: {32, 128} x {0.01, 0.001}",
            "measure": "final validation loss for each combination",
            "criterion": "interaction if best lr differs between batch sizes",
            "conditions": 4,
        },
    }

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "hypothesis_design"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 9

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["method_selection"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls experiment complexity.

        Returns:
            Natural language description.
        """
        return "design experiment to test this hypothesis"

    _HYPOTHESIS_TEMPLATES = {
        "learning_rate": {
            "hyp_tpl": "learning rate {lr1} gives lower final loss than {lr2} on {task}",
            "control": "fix architecture, data, batch size, epochs",
            "variable_tpl": "learning rate: {{{lr1}, {lr2}}}",
            "measure_tpl": "validation loss after {epochs} epochs",
            "criterion_tpl": "lr={lr1} wins if val_loss lower by > {margin}%",
            "conditions": 2,
        },
        "architecture": {
            "hyp_tpl": "deeper network ({deep} layers) outperforms shallow ({shallow} layers) on {task}",
            "control": "fix total parameter count, learning rate, data",
            "variable_tpl": "depth: {{{shallow} layers, {deep} layers}}",
            "measure": "test accuracy after convergence",
            "criterion_tpl": "deep wins if accuracy > {margin}% higher",
            "conditions": 2,
        },
        "augmentation": {
            "hyp_tpl": "data augmentation improves generalisation on {task} with {n} samples",
            "control": "fix model, learning rate, training epochs",
            "variable": "augmentation: {none, random crop + flip}",
            "measure_tpl": "gap between train and test accuracy after {epochs} epochs",
            "criterion_tpl": "augmentation helps if gap shrinks by > {margin}%",
            "conditions": 2,
        },
        "multi_factor": {
            "hyp_tpl": "batch size and learning rate interact for {task} training",
            "control": "fix architecture, data, epochs",
            "variable_tpl": "batch_size x lr: {{{bs1}, {bs2}}} x {{{lr1}, {lr2}}}",
            "measure": "final validation loss for each combination",
            "criterion": "interaction if best lr differs between batch sizes",
            "conditions": 4,
        },
    }

    _TASK_NAMES = [
        "image classification", "text generation", "machine translation",
        "sentiment analysis", "object detection", "speech recognition",
        "question answering", "summarisation",
    ]

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an experiment design problem with randomised parameters.

        Args:
            difficulty: Controls experiment type.

        Returns:
            Tuple of (hypothesis_string, solution_data).
        """
        etype = self._rng.choice(list(self._HYPOTHESIS_TEMPLATES.keys()))
        tpl = self._HYPOTHESIS_TEMPLATES[etype]
        task = self._rng.choice(self._TASK_NAMES)
        lr1 = round(self._rng.choice([0.0001, 0.0005, 0.001, 0.005, 0.01]), 4)
        lr2 = round(lr1 * self._rng.choice([5, 10, 20]), 4)
        epochs = self._rng.choice([50, 100, 200, 500])
        margin = round(self._rng.uniform(0.3, 3.0), 1)
        deep = self._rng.randint(4, 12 + difficulty)
        shallow = self._rng.randint(2, max(3, deep // 2))
        n = self._rng.choice([1000, 5000, 10000, 50000])
        bs1 = self._rng.choice([16, 32, 64])
        bs2 = self._rng.choice([128, 256, 512])
        fmt = dict(task=task, lr1=lr1, lr2=lr2, epochs=epochs,
                   margin=margin, deep=deep, shallow=shallow, n=n,
                   bs1=bs1, bs2=bs2)
        hypothesis = tpl["hyp_tpl"].format(**fmt)
        variable = tpl.get("variable_tpl", tpl.get("variable", "")).format(**fmt)
        measure = tpl.get("measure_tpl", tpl.get("measure", "")).format(**fmt)
        criterion = tpl.get("criterion_tpl", tpl.get("criterion", "")).format(**fmt)
        exp = {
            "hypothesis": hypothesis,
            "control": tpl["control"],
            "variable": variable,
            "measure": measure,
            "criterion": criterion,
            "conditions": tpl["conditions"],
        }
        problem = f"hypothesis: {exp['hypothesis']}"
        return problem, exp

    def _create_steps(self, data: dict) -> list[str]:
        """Generate experiment design steps.

        Args:
            data: Solution data with experiment specification.

        Returns:
            Steps showing controls, measurements, and criteria.
        """
        return [
            f"control: {data['control']}",
            f"variable: {data['variable']}",
            f"measure: {data['measure']}",
            f"criterion: {data['criterion']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the experiment summary.

        Args:
            data: Solution data.

        Returns:
            Experiment description string.
        """
        return f"controlled experiment with {data['conditions']} conditions"


@register
class MetaPatternGenerator(StepGenerator):
    """Identify a common pattern across multiple error instances.

    Presents several error examples and asks the model to identify
    the shared underlying pattern or systematic bias.

    Input format:
        ``identify the common pattern across these errors``

    Target format:
        ``error 1: 23+19=41 (off by -1) <step> error 2: 45+17=61
        (off by -1) <step> error 3: 67+15=81 (off by -1) <step>
        pattern: consistently underestimates carry propagation
        <step> systematic: -1 bias in addition with carry``

    Difficulty scaling:
        Difficulty 1-2: constant offset error.
        Difficulty 3-4: sign error pattern.
        Difficulty 5-6: order-of-magnitude error.
        Difficulty 7-8: conditional error (only when carry occurs).

    Prerequisites:
        error_detection, generalise_sequence.

    Example:
        >>> gen = MetaPatternGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'meta_pattern'
    """

    _PATTERN_TYPES = {
        1: "constant_offset", 2: "constant_offset",
        3: "sign_error", 4: "sign_error",
        5: "magnitude_error", 6: "magnitude_error",
        7: "carry_error", 8: "carry_error",
    }

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "meta_pattern"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 9

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["error_detection", "generalise_sequence"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls pattern type.

        Returns:
            Natural language description.
        """
        return "identify the common pattern across these errors"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate multiple error instances sharing a pattern.

        Args:
            difficulty: Controls error type.

        Returns:
            Tuple of (error_list, solution_data).
        """
        ptype = self._rng.choice(list(self._PATTERN_TYPES.values()))
        builder = self._get_builder(ptype)
        return builder(difficulty)

    def _get_builder(self, ptype: str):
        """Return builder for the given pattern type.

        Args:
            ptype: Pattern type string.

        Returns:
            Builder method.
        """
        return {
            "constant_offset": self._build_constant_offset,
            "sign_error": self._build_sign_error,
            "magnitude_error": self._build_magnitude_error,
            "carry_error": self._build_carry_error,
        }[ptype]

    def _build_constant_offset(self, difficulty: int) -> tuple[str, dict]:
        """Build a constant offset error pattern.

        Args:
            difficulty: Controls operand size.

        Returns:
            Tuple of (problem_string, solution_data).
        """
        offset = self._rng.choice([-2, -1, 1, 2])
        examples: list[dict] = []
        for _ in range(3):
            a = self._rng.randint(10, 50 + 10 * difficulty)
            b = self._rng.randint(10, 50 + 10 * difficulty)
            correct = a + b
            wrong = correct + offset
            examples.append({"expr": f"{a}+{b}", "wrong": wrong, "correct": correct, "diff": offset})
        parts = [f"{e['expr']}={e['wrong']} (off by {e['diff']:+d})" for e in examples]
        return "; ".join(parts), {
            "examples": examples, "offset": offset,
            "pattern": f"constant offset of {offset:+d}",
            "classification": f"systematic: {offset:+d} bias in addition",
        }

    def _build_sign_error(self, difficulty: int) -> tuple[str, dict]:
        """Build a sign error pattern.

        Args:
            difficulty: Controls operand size.

        Returns:
            Tuple of (problem_string, solution_data).
        """
        examples: list[dict] = []
        for _ in range(3):
            a = self._rng.randint(10, 40 + 10 * difficulty)
            b = self._rng.randint(1, 20)
            correct = a - b
            wrong = a + b
            examples.append({"expr": f"{a}-{b}", "wrong": wrong, "correct": correct})
        parts = [f"{e['expr']}={e['wrong']} (should be {e['correct']})" for e in examples]
        return "; ".join(parts), {
            "examples": examples,
            "pattern": "subtraction computed as addition",
            "classification": "systematic: sign of second operand flipped",
        }

    def _build_magnitude_error(self, difficulty: int) -> tuple[str, dict]:
        """Build an order-of-magnitude error pattern.

        Args:
            difficulty: Controls operand size.

        Returns:
            Tuple of (problem_string, solution_data).
        """
        examples: list[dict] = []
        for _ in range(3):
            a = self._rng.randint(2, 9)
            b = self._rng.randint(2, 9)
            correct = a * b * 10
            wrong = a * b
            examples.append({"expr": f"{a}*{b}*10", "wrong": wrong, "correct": correct})
        parts = [f"{e['expr']}={e['wrong']} (should be {e['correct']})" for e in examples]
        return "; ".join(parts), {
            "examples": examples,
            "pattern": "factor of 10 dropped",
            "classification": "systematic: multiplication by 10 omitted",
        }

    def _build_carry_error(self, difficulty: int) -> tuple[str, dict]:
        """Build a carry propagation error pattern.

        Args:
            difficulty: Controls operand size.

        Returns:
            Tuple of (problem_string, solution_data).
        """
        examples: list[dict] = []
        for _ in range(3):
            a = self._rng.randint(5, 9) * 10 + self._rng.randint(5, 9)
            b = self._rng.randint(5, 9) * 10 + self._rng.randint(5, 9)
            correct = a + b
            wrong = correct - 10
            examples.append({"expr": f"{a}+{b}", "wrong": wrong, "correct": correct, "diff": -10})
        parts = [f"{e['expr']}={e['wrong']} (should be {e['correct']})" for e in examples]
        return "; ".join(parts), {
            "examples": examples,
            "pattern": "carry not propagated to hundreds digit",
            "classification": "systematic: missed carry propagation",
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate pattern identification steps.

        Args:
            data: Solution data with examples and pattern.

        Returns:
            Steps showing each error and the identified pattern.
        """
        steps: list[str] = []
        for i, ex in enumerate(data["examples"]):
            steps.append(f"error {i + 1}: {ex['expr']}={ex['wrong']} (correct: {ex['correct']})")
        steps.append(f"pattern: {data['pattern']}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the error classification.

        Args:
            data: Solution data.

        Returns:
            Classification string.
        """
        return data["classification"]


@register
class RepresentationChoiceGenerator(StepGenerator):
    """Choose the best representation for a given problem.

    Presents a problem and several representation options, then
    analyses which representation makes the problem easiest.

    Input format:
        ``choose best representation for this problem``

    Target format:
        ``problem: find shortest path in weighted graph <step>
        option A: adjacency matrix -> O(V^2) space, O(1) edge lookup
        <step> option B: adjacency list -> O(V+E) space, O(degree)
        lookup <step> for sparse graphs (E << V^2), B is better
        <step> adjacency list``

    Difficulty scaling:
        Difficulty 1-2: array vs linked list for search.
        Difficulty 3-4: matrix vs list for graphs.
        Difficulty 5-6: sorted array vs hash table.
        Difficulty 7-8: tree vs hash table vs sorted array.

    Prerequisites:
        method_selection, complexity_comparison.

    Example:
        >>> gen = RepresentationChoiceGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'representation_choice'
    """

    _CHOICE_TYPES = {
        1: "array_vs_list", 2: "array_vs_list",
        3: "matrix_vs_adjlist", 4: "matrix_vs_adjlist",
        5: "sorted_vs_hash", 6: "sorted_vs_hash",
        7: "tree_vs_hash", 8: "tree_vs_hash",
    }

    _CHOICES: dict[str, dict] = {
        "array_vs_list": {
            "problem": "frequent random access to elements by index",
            "options": [
                {"name": "array", "space": "O(n)", "access": "O(1)", "insert": "O(n)"},
                {"name": "linked list", "space": "O(n)", "access": "O(n)", "insert": "O(1)"},
            ],
            "winner": "array",
            "reason": "O(1) random access dominates for index-based retrieval",
        },
        "matrix_vs_adjlist": {
            "problem": "shortest path in sparse weighted graph",
            "options": [
                {"name": "adjacency matrix", "space": "O(V^2)", "access": "O(1)", "insert": "O(1)"},
                {"name": "adjacency list", "space": "O(V+E)", "access": "O(degree)", "insert": "O(1)"},
            ],
            "winner": "adjacency list",
            "reason": "O(V+E) space is much smaller than O(V^2) for sparse graphs",
        },
        "sorted_vs_hash": {
            "problem": "frequent membership queries with no ordering needed",
            "options": [
                {"name": "sorted array", "space": "O(n)", "access": "O(log n)", "insert": "O(n)"},
                {"name": "hash table", "space": "O(n)", "access": "O(1) amortised", "insert": "O(1) amortised"},
            ],
            "winner": "hash table",
            "reason": "O(1) amortised lookup beats O(log n) when ordering is not needed",
        },
        "tree_vs_hash": {
            "problem": "maintain sorted order with frequent insertions and range queries",
            "options": [
                {"name": "balanced BST", "space": "O(n)", "access": "O(log n)", "insert": "O(log n)"},
                {"name": "hash table", "space": "O(n)", "access": "O(1) amortised", "insert": "O(1) amortised"},
            ],
            "winner": "balanced BST",
            "reason": "BST supports range queries and sorted traversal; hash table does not",
        },
    }

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "representation_choice"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 9

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["method_selection", "complexity_comparison"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls which comparison is used.

        Returns:
            Natural language description.
        """
        return "choose best representation for this problem"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a representation choice problem with randomised size params.

        Args:
            difficulty: Controls comparison type.

        Returns:
            Tuple of (problem_description, solution_data).
        """
        ctype = self._rng.choice(list(self._CHOICES.keys()))
        choice = dict(self._CHOICES[ctype])
        n = self._rng.randint(100, 10000 + difficulty * 5000)
        e = self._rng.randint(n, n * 3)
        ops = self._rng.randint(1000, 100000)
        # Add context with random parameters to the problem description
        context = self._rng.choice([
            f" (n={n} elements, {ops} operations)",
            f" ({n} items, {e} relationships)",
            f" (dataset of {n} entries)",
            f" (n={n}, expected {ops} queries)",
        ])
        problem = f"problem: {choice['problem']}{context}"
        choice["problem"] = choice["problem"] + context
        return problem, choice

    def _create_steps(self, data: dict) -> list[str]:
        """Generate representation analysis steps.

        Args:
            data: Solution data with options and winner.

        Returns:
            Steps showing each option's properties and the verdict.
        """
        steps: list[str] = []
        for opt in data["options"]:
            steps.append(
                f"option {opt['name']}: space={opt['space']}, "
                f"access={opt['access']}, insert={opt['insert']}"
            )
        steps.append(f"verdict: {data['winner']} ({data['reason']})")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the recommended representation.

        Args:
            data: Solution data.

        Returns:
            Winner name.
        """
        return data["winner"]


@register
class TrainingDiagnosisGenerator(StepGenerator):
    """Diagnose a training plateau from loss curve data.

    Presents a sequence of training losses and asks the model to
    identify the pathology and suggest a remedy.

    Input format:
        ``diagnose this training curve``

    Target format:
        ``losses: [5.0, 3.2, 2.1, 2.05, 2.04, 2.04, 2.04] <step>
        pattern: plateau after epoch 3 <step> diagnosis: learning
        rate too low to escape local minimum <step> remedy: increase
        learning rate or use learning rate warmup <step> plateau``

    Difficulty scaling:
        Difficulty 1-2: simple plateau.
        Difficulty 3-4: oscillation (lr too high).
        Difficulty 5-6: divergence (exploding gradients).
        Difficulty 7-8: overfitting (train drops, val rises).

    Prerequisites:
        scaling_prediction.

    Example:
        >>> gen = TrainingDiagnosisGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'training_diagnosis'
    """

    _PATHOLOGY_TYPES = {
        1: "plateau", 2: "plateau",
        3: "oscillation", 4: "oscillation",
        5: "divergence", 6: "divergence",
        7: "overfitting", 8: "overfitting",
    }

    _REMEDIES: dict[str, str] = {
        "plateau": "increase learning rate or use warmup/cosine schedule",
        "oscillation": "reduce learning rate or increase batch size",
        "divergence": "reduce learning rate, add gradient clipping, check for NaN",
        "overfitting": "add regularisation (dropout, weight decay) or increase data",
    }

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "training_diagnosis"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 10

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["scaling_prediction"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls pathology type.

        Returns:
            Natural language description.
        """
        return "diagnose this training curve"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a training curve with a specific pathology.

        Args:
            difficulty: Controls pathology type.

        Returns:
            Tuple of (loss_curve, solution_data).
        """
        pathology = self._rng.choice(list(self._PATHOLOGY_TYPES.values()))
        builder = self._get_builder(pathology)
        return builder()

    def _get_builder(self, pathology: str):
        """Return builder for the given pathology.

        Args:
            pathology: Pathology type string.

        Returns:
            Builder method.
        """
        return {
            "plateau": self._build_plateau,
            "oscillation": self._build_oscillation,
            "divergence": self._build_divergence,
            "overfitting": self._build_overfitting,
        }[pathology]

    def _build_plateau(self) -> tuple[str, dict]:
        """Build a plateau loss curve.

        Returns:
            Tuple of (loss_string, solution_data).
        """
        start = round(self._rng.uniform(4.0, 6.0), 1)
        plateau_val = round(self._rng.uniform(1.5, 2.5), 2)
        losses = [start]
        val = start
        for _ in range(3):
            val = round(val * 0.7, 2)
            losses.append(val)
        for _ in range(4):
            losses.append(round(plateau_val + self._rng.uniform(-0.01, 0.01), 2))
        return f"losses: {losses}", {
            "losses": losses, "pathology": "plateau",
            "diagnosis": "learning rate too low to escape local minimum",
            "remedy": self._REMEDIES["plateau"],
        }

    def _build_oscillation(self) -> tuple[str, dict]:
        """Build an oscillating loss curve.

        Returns:
            Tuple of (loss_string, solution_data).
        """
        base = round(self._rng.uniform(2.0, 3.0), 1)
        amp = round(self._rng.uniform(0.3, 0.8), 2)
        losses: list[float] = []
        for i in range(8):
            val = base + amp * ((-1) ** i)
            losses.append(round(val, 2))
        return f"losses: {losses}", {
            "losses": losses, "pathology": "oscillation",
            "diagnosis": "learning rate too high, overshooting minima",
            "remedy": self._REMEDIES["oscillation"],
        }

    def _build_divergence(self) -> tuple[str, dict]:
        """Build a diverging loss curve.

        Returns:
            Tuple of (loss_string, solution_data).
        """
        start = round(self._rng.uniform(3.0, 5.0), 1)
        losses = [start]
        val = start
        for _ in range(3):
            val = round(val * 0.8, 2)
            losses.append(val)
        for _ in range(4):
            val = round(val * 1.3, 2)
            losses.append(val)
        return f"losses: {losses}", {
            "losses": losses, "pathology": "divergence",
            "diagnosis": "exploding gradients or numerical instability",
            "remedy": self._REMEDIES["divergence"],
        }

    def _build_overfitting(self) -> tuple[str, dict]:
        """Build an overfitting loss curve.

        Returns:
            Tuple of (loss_string, solution_data).
        """
        train_losses: list[float] = []
        val_losses: list[float] = []
        t_val = round(self._rng.uniform(4.0, 5.0), 1)
        v_val = t_val
        for i in range(8):
            t_val = round(t_val * 0.85, 2)
            train_losses.append(t_val)
            if i < 4:
                v_val = round(v_val * 0.88, 2)
            else:
                v_val = round(v_val * 1.05, 2)
            val_losses.append(v_val)
        return f"train: {train_losses}, val: {val_losses}", {
            "losses": train_losses, "val_losses": val_losses,
            "pathology": "overfitting",
            "diagnosis": "train loss decreasing but validation loss increasing",
            "remedy": self._REMEDIES["overfitting"],
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate diagnosis steps.

        Args:
            data: Solution data with pathology info.

        Returns:
            Steps showing pattern detection, diagnosis, and remedy.
        """
        analyser = TrainingCurveAnalyser()
        detected = analyser.detect_pattern(data["losses"])
        return [
            f"pattern: {detected}",
            f"diagnosis: {data['diagnosis']}",
            f"remedy: {data['remedy']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the identified pathology.

        Args:
            data: Solution data.

        Returns:
            Pathology name.
        """
        return data["pathology"]


@register
class FailureModeClassificationGenerator(StepGenerator):
    """Classify errors as systematic or random from multiple observations.

    Presents a set of predictions and true values, and asks the model
    to determine whether the errors are systematic (biased) or random.

    Input format:
        ``classify these errors as systematic or random``

    Target format:
        ``predictions: [12,23,35], true: [10,20,32] <step>
        errors: [+2,+3,+3] <step> mean error: +2.67
        (positive bias) <step> systematic: consistent positive offset
        <step> systematic``

    Difficulty scaling:
        Difficulty 1-2: clearly systematic (constant offset).
        Difficulty 3-4: clearly random (mixed signs, no pattern).
        Difficulty 5-6: subtle systematic (proportional error).
        Difficulty 7-8: mixed (systematic + random noise).

    Prerequisites:
        error_detection.

    Example:
        >>> gen = FailureModeClassificationGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'failure_mode_classification'
    """

    _ERROR_TYPES = {
        1: "systematic_constant", 2: "systematic_constant",
        3: "random", 4: "random",
        5: "systematic_proportional", 6: "systematic_proportional",
        7: "mixed", 8: "mixed",
    }

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "failure_mode_classification"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 10

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["error_detection"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls error type.

        Returns:
            Natural language description.
        """
        return "classify these errors as systematic or random"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an error classification problem.

        Args:
            difficulty: Controls error type.

        Returns:
            Tuple of (predictions_and_truth, solution_data).
        """
        etype = self._rng.choice(list(self._ERROR_TYPES.values()))
        builder = self._get_builder(etype)
        return builder()

    def _get_builder(self, etype: str):
        """Return builder for the given error type.

        Args:
            etype: Error type string.

        Returns:
            Builder method.
        """
        return {
            "systematic_constant": self._build_systematic_constant,
            "random": self._build_random,
            "systematic_proportional": self._build_systematic_proportional,
            "mixed": self._build_mixed,
        }[etype]

    def _build_systematic_constant(self) -> tuple[str, dict]:
        """Build a constant systematic error.

        Returns:
            Tuple of (problem_string, solution_data).
        """
        offset = self._rng.choice([2, 3, 5, -2, -3])
        true_vals = [self._rng.randint(10, 50) for _ in range(5)]
        preds = [t + offset for t in true_vals]
        errors = [p - t for p, t in zip(preds, true_vals)]
        mean_err = sum(errors) / len(errors)
        return f"predictions: {preds}, true: {true_vals}", {
            "predictions": preds, "true_values": true_vals,
            "errors": errors, "mean_error": mean_err,
            "classification": "systematic",
            "explanation": f"constant offset of {offset:+d}",
        }

    def _build_random(self) -> tuple[str, dict]:
        """Build a random error pattern.

        Returns:
            Tuple of (problem_string, solution_data).
        """
        true_vals = [self._rng.randint(10, 50) for _ in range(5)]
        errors = [self._rng.randint(-5, 5) for _ in range(5)]
        preds = [t + e for t, e in zip(true_vals, errors)]
        mean_err = sum(errors) / len(errors)
        return f"predictions: {preds}, true: {true_vals}", {
            "predictions": preds, "true_values": true_vals,
            "errors": errors, "mean_error": mean_err,
            "classification": "random",
            "explanation": "errors have mixed signs and no consistent pattern",
        }

    def _build_systematic_proportional(self) -> tuple[str, dict]:
        """Build a proportional systematic error.

        Returns:
            Tuple of (problem_string, solution_data).
        """
        scale = round(self._rng.uniform(1.05, 1.15), 2)
        true_vals = [self._rng.randint(10, 50) for _ in range(5)]
        preds = [int(t * scale) for t in true_vals]
        errors = [p - t for p, t in zip(preds, true_vals)]
        mean_err = sum(errors) / len(errors)
        return f"predictions: {preds}, true: {true_vals}", {
            "predictions": preds, "true_values": true_vals,
            "errors": errors, "mean_error": mean_err,
            "classification": "systematic",
            "explanation": f"proportional overestimate by factor ~{scale}",
        }

    def _build_mixed(self) -> tuple[str, dict]:
        """Build a mixed systematic + random error pattern.

        Returns:
            Tuple of (problem_string, solution_data).
        """
        offset = self._rng.choice([2, 3])
        true_vals = [self._rng.randint(10, 50) for _ in range(5)]
        errors = [offset + self._rng.randint(-1, 1) for _ in range(5)]
        preds = [t + e for t, e in zip(true_vals, errors)]
        mean_err = sum(errors) / len(errors)
        return f"predictions: {preds}, true: {true_vals}", {
            "predictions": preds, "true_values": true_vals,
            "errors": errors, "mean_error": mean_err,
            "classification": "systematic",
            "explanation": f"systematic offset ~{offset:+d} with small random noise",
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate classification steps.

        Args:
            data: Solution data with errors and classification.

        Returns:
            Steps showing error analysis and verdict.
        """
        err_str = ", ".join(f"{e:+d}" for e in data["errors"])
        return [
            f"errors: [{err_str}]",
            f"mean error: {data['mean_error']:+.1f}",
            f"analysis: {data['explanation']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the classification verdict.

        Args:
            data: Solution data.

        Returns:
            Classification string.
        """
        return data["classification"]


@register
class DataPrescriptionGenerator(StepGenerator):
    """Prescribe training data to fix a diagnosed weakness.

    Given a model weakness (e.g. fails on carry arithmetic), prescribes
    the type and quantity of training data that would address it.

    Input format:
        ``prescribe training data to fix this weakness``

    Target format:
        ``weakness: model fails on multi-digit addition with carries
        <step> root cause: insufficient carry propagation examples
        <step> prescription: 1000 addition problems with 3+ carries
        <step> data spec: a+b where a,b in [100,999], sum > 1000
        <step> 1000 samples of multi-carry addition``

    Difficulty scaling:
        Difficulty 1-2: simple skill gap (single operation).
        Difficulty 3-4: compositional weakness.
        Difficulty 5-6: distribution shift.
        Difficulty 7-8: adversarial edge cases.

    Prerequisites:
        training_diagnosis.

    Example:
        >>> gen = DataPrescriptionGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'data_prescription'
    """

    _WEAKNESS_TYPES = {
        1: "carry_arithmetic", 2: "carry_arithmetic",
        3: "multi_step", 4: "multi_step",
        5: "distribution_shift", 6: "distribution_shift",
        7: "edge_cases", 8: "edge_cases",
    }

    _PRESCRIPTIONS: dict[str, dict] = {
        "carry_arithmetic": {
            "weakness": "model fails on multi-digit addition with carries",
            "root_cause": "insufficient carry propagation examples in training",
            "data_type": "addition problems where sum digits require carrying",
            "quantity": 1000,
            "spec": "a+b where a,b in [100,999] and digit sum >= 10 in each column",
        },
        "multi_step": {
            "weakness": "model fails when solution requires > 3 reasoning steps",
            "root_cause": "training data biased toward 1-2 step solutions",
            "data_type": "problems requiring 4-6 explicit reasoning steps",
            "quantity": 2000,
            "spec": "chain computations: a op b op c op d with intermediate verification",
        },
        "distribution_shift": {
            "weakness": "model accuracy drops on inputs larger than training range",
            "root_cause": "training data concentrated on small inputs",
            "data_type": "problems with operands 10x-100x larger than current training max",
            "quantity": 5000,
            "spec": "same task types but with operands in [1000, 100000]",
        },
        "edge_cases": {
            "weakness": "model fails on boundary conditions (zero, negative, overflow)",
            "root_cause": "edge cases underrepresented in training data",
            "data_type": "problems involving 0, -1, MAX_INT, and boundary values",
            "quantity": 3000,
            "spec": "targeted examples: x*0, x+(-x), operations near integer limits",
        },
    }

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "data_prescription"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 10

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["training_diagnosis"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls weakness type.

        Returns:
            Natural language description.
        """
        return "prescribe training data to fix this weakness"

    _PRESCRIPTION_TEMPLATES = {
        "carry_arithmetic": {
            "weakness_tpl": "model fails on {n}-digit addition with carries (accuracy {acc}%)",
            "root_cause": "insufficient carry propagation examples in training",
            "data_type": "addition problems where sum digits require carrying",
            "spec_tpl": "a+b where a,b in [{lo},{hi}] and digit sum >= 10 in each column",
        },
        "multi_step": {
            "weakness_tpl": "model fails when solution requires > {n} reasoning steps (accuracy {acc}%)",
            "root_cause": "training data biased toward 1-2 step solutions",
            "data_type_tpl": "problems requiring {min_s}-{max_s} explicit reasoning steps",
            "spec": "chain computations: a op b op c op d with intermediate verification",
        },
        "distribution_shift": {
            "weakness_tpl": "model accuracy drops to {acc}% on inputs {scale}x larger than training range",
            "root_cause": "training data concentrated on small inputs",
            "data_type_tpl": "problems with operands {scale}x-{scale2}x larger than current training max",
            "spec_tpl": "same task types but with operands in [{lo}, {hi}]",
        },
        "edge_cases": {
            "weakness_tpl": "model fails on {n} of {total} boundary conditions (zero, negative, overflow)",
            "root_cause": "edge cases underrepresented in training data",
            "data_type": "problems involving 0, -1, MAX_INT, and boundary values",
            "spec": "targeted examples: x*0, x+(-x), operations near integer limits",
        },
    }

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a data prescription problem with randomised parameters.

        Args:
            difficulty: Controls weakness type.

        Returns:
            Tuple of (weakness_description, solution_data).
        """
        wtype = self._rng.choice(list(self._PRESCRIPTION_TEMPLATES.keys()))
        tpl = self._PRESCRIPTION_TEMPLATES[wtype]
        n = self._rng.randint(2, 6 + difficulty)
        acc = self._rng.randint(5, 40)
        lo = self._rng.choice([100, 1000, 10000])
        hi = lo * self._rng.randint(5, 20)
        scale = self._rng.choice([10, 50, 100])
        scale2 = scale * self._rng.randint(2, 10)
        total = self._rng.randint(10, 50)
        min_s = n + 1
        max_s = min_s + self._rng.randint(1, 4)
        quantity = self._rng.choice([500, 1000, 2000, 3000, 5000, 10000])
        fmt = dict(n=n, acc=acc, lo=lo, hi=hi, scale=scale, scale2=scale2,
                   total=total, min_s=min_s, max_s=max_s)
        weakness = tpl["weakness_tpl"].format(**fmt)
        data_type = tpl.get("data_type_tpl", tpl.get("data_type", "")).format(**fmt)
        spec = tpl.get("spec_tpl", tpl.get("spec", "")).format(**fmt)
        prescription = {
            "weakness": weakness,
            "root_cause": tpl["root_cause"],
            "data_type": data_type,
            "quantity": quantity,
            "spec": spec,
        }
        problem = f"weakness: {prescription['weakness']}"
        return problem, prescription

    def _create_steps(self, data: dict) -> list[str]:
        """Generate prescription steps.

        Args:
            data: Solution data with weakness and prescription.

        Returns:
            Steps showing diagnosis and data specification.
        """
        return [
            f"root cause: {data['root_cause']}",
            f"prescription: {data['quantity']} samples of {data['data_type']}",
            f"data spec: {data['spec']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the prescription summary.

        Args:
            data: Solution data.

        Returns:
            Prescription string.
        """
        return f"{data['quantity']} samples of {data['data_type']}"


@register
class EfficiencyAnalysisGenerator(StepGenerator):
    """Identify the FLOP bottleneck in a transformer block.

    Analyses the FLOP distribution across attention, feed-forward,
    and normalization layers to identify the dominant cost.

    Input format:
        ``identify the FLOP bottleneck``

    Target format:
        ``config: d_model=512, d_ff=2048, seq_len=128, heads=8 <step>
        attention FLOPs: 134M <step> FFN FLOPs: 268M <step>
        ratio: FFN/attention = 2.0 <step> bottleneck: FFN (67%)
        <step> FFN``

    Difficulty scaling:
        Each difficulty level defines ranges for d_model, d_ff multiplier,
        seq_len, and n_heads. Parameters are sampled randomly within
        those ranges, producing combinatorial variety per difficulty.
        Difficulty 1-2: small models (d_model 128-256).
        Difficulty 3-4: medium models (d_model 256-512).
        Difficulty 5-6: large models (d_model 512-1024).
        Difficulty 7-8: very large with long sequences (d_model 1024-4096).

    Prerequisites:
        architecture_analysis.

    Example:
        >>> gen = EfficiencyAnalysisGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'efficiency_analysis'
    """

    _CONFIG_RANGES = {
        1: {"d_model": [128, 256], "d_ff_mult": [2, 4], "seq_len": [32, 64, 128], "n_heads": [2, 4]},
        2: {"d_model": [128, 256], "d_ff_mult": [2, 4, 8], "seq_len": [64, 128, 256], "n_heads": [2, 4, 8]},
        3: {"d_model": [256, 512], "d_ff_mult": [2, 4], "seq_len": [64, 128, 256], "n_heads": [4, 8]},
        4: {"d_model": [256, 512], "d_ff_mult": [2, 4, 8], "seq_len": [128, 256, 512], "n_heads": [4, 8, 16]},
        5: {"d_model": [512, 1024], "d_ff_mult": [2, 4], "seq_len": [128, 256, 512], "n_heads": [8, 16]},
        6: {"d_model": [512, 1024], "d_ff_mult": [2, 4, 8], "seq_len": [256, 512, 1024], "n_heads": [8, 16, 32]},
        7: {"d_model": [1024, 2048], "d_ff_mult": [2, 4], "seq_len": [256, 512, 1024], "n_heads": [16, 32]},
        8: {"d_model": [1024, 2048, 4096], "d_ff_mult": [2, 4, 8], "seq_len": [512, 1024, 2048], "n_heads": [16, 32, 64]},
    }

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "efficiency_analysis"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 10

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["architecture_analysis"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls model size.

        Returns:
            Natural language description.
        """
        return "identify the FLOP bottleneck"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a FLOP analysis problem.

        Randomly samples d_model, d_ff multiplier, seq_len, and n_heads
        from the ranges defined for the given difficulty level, producing
        combinatorial variety instead of a single fixed config.

        Args:
            difficulty: Controls the parameter ranges to sample from.

        Returns:
            Tuple of (config_string, solution_data).
        """
        ranges = self._CONFIG_RANGES.get(difficulty, self._CONFIG_RANGES[3])
        d = self._rng.choice(ranges["d_model"])
        d_ff = d * self._rng.choice(ranges["d_ff_mult"])
        seq = self._rng.choice(ranges["seq_len"])
        heads = self._rng.choice(ranges["n_heads"])
        # Ensure heads divides d_model
        while d % heads != 0:
            heads = self._rng.choice(ranges["n_heads"])
        counter = FlopCounter()
        attn_flops = counter.attention_flops(seq, d, heads)
        ffn_flops = counter.ffn_flops(d, d_ff, seq)
        total = attn_flops + ffn_flops
        attn_pct = round(100 * attn_flops / total, 1) if total > 0 else 0
        ffn_pct = round(100 * ffn_flops / total, 1) if total > 0 else 0
        bottleneck = "attention" if attn_flops > ffn_flops else "FFN"
        bottleneck_pct = max(attn_pct, ffn_pct)
        problem = (
            f"config: d_model={d}, d_ff={d_ff}, "
            f"seq_len={seq}, heads={heads}"
        )
        return problem, {
            "config": {"d_model": d, "d_ff": d_ff, "seq_len": seq, "n_heads": heads},
            "attn_flops": attn_flops, "ffn_flops": ffn_flops,
            "total": total, "attn_pct": attn_pct, "ffn_pct": ffn_pct,
            "bottleneck": bottleneck, "bottleneck_pct": bottleneck_pct,
        }

    def _format_flops(self, flops: int) -> str:
        """Format a FLOP count as a human-readable string.

        Args:
            flops: Number of FLOPs.

        Returns:
            Formatted string with M/B suffix.
        """
        if flops >= 1_000_000_000:
            return f"{flops / 1_000_000_000:.1f}B"
        if flops >= 1_000_000:
            return f"{flops / 1_000_000:.1f}M"
        return str(flops)

    def _create_steps(self, data: dict) -> list[str]:
        """Generate FLOP analysis steps.

        Args:
            data: Solution data with FLOP counts.

        Returns:
            Steps showing each component's cost and the bottleneck.
        """
        return [
            f"attention FLOPs: {self._format_flops(data['attn_flops'])} ({data['attn_pct']}%)",
            f"FFN FLOPs: {self._format_flops(data['ffn_flops'])} ({data['ffn_pct']}%)",
            f"bottleneck: {data['bottleneck']} ({data['bottleneck_pct']}%)",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the identified bottleneck.

        Args:
            data: Solution data.

        Returns:
            Bottleneck component name.
        """
        return data["bottleneck"]


@register
class EmergentCapabilityGenerator(StepGenerator):
    """Predict at what model scale a capability will emerge.

    Uses scaling law extrapolation to predict the parameter count at
    which a capability (measured by a proxy metric) will cross a
    threshold.

    Input format:
        ``predict when this capability will emerge``

    Target format:
        ``capability: multi-step reasoning <step> observed: N=10M ->
        5%, N=100M -> 12%, N=1B -> 35% <step> fit power law:
        acc = 0.5 * N^0.25 <step> threshold: 50% accuracy <step>
        predict: N = 6.25B parameters <step> ~6.25B``

    Difficulty scaling:
        Difficulty 1-2: linear extrapolation (2 data points).
        Difficulty 3-4: power law with 3 data points.
        Difficulty 5-6: log-linear scaling.
        Difficulty 7-8: sigmoid emergence (sharp threshold).

    Prerequisites:
        scaling_prediction.

    Example:
        >>> gen = EmergentCapabilityGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'emergent_capability'
    """

    _CAPABILITIES = [
        "multi-step arithmetic",
        "chain-of-thought reasoning",
        "in-context learning",
        "compositional generalisation",
    ]

    _SCALE_TYPES = {
        1: "linear", 2: "linear",
        3: "power_law", 4: "power_law",
        5: "log_linear", 6: "log_linear",
        7: "sigmoid", 8: "sigmoid",
    }

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "emergent_capability"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 10

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["scaling_prediction"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls scaling model.

        Returns:
            Natural language description.
        """
        return "predict when this capability will emerge"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a capability emergence prediction problem.

        Args:
            difficulty: Controls scaling model type.

        Returns:
            Tuple of (observations, solution_data).
        """
        stype = self._rng.choice(list(self._SCALE_TYPES.values()))
        capability = self._rng.choice(self._CAPABILITIES)
        builder = self._get_builder(stype)
        return builder(capability)

    def _get_builder(self, stype: str):
        """Return builder for the given scale type.

        Args:
            stype: Scale type string.

        Returns:
            Builder method.
        """
        return {
            "linear": self._build_linear,
            "power_law": self._build_power_law,
            "log_linear": self._build_log_linear,
            "sigmoid": self._build_sigmoid,
        }[stype]

    def _build_linear(self, capability: str) -> tuple[str, dict]:
        """Build a linear extrapolation problem.

        Args:
            capability: Capability name.

        Returns:
            Tuple of (problem_string, solution_data).
        """
        n1 = 10_000_000
        n2 = 100_000_000
        acc1 = round(self._rng.uniform(5, 15), 1)
        acc2 = round(self._rng.uniform(20, 35), 1)
        threshold = 50.0
        slope = (acc2 - acc1) / (n2 - n1)
        target_n = int(n1 + (threshold - acc1) / slope) if slope > 0 else n2 * 10
        problem = f"capability: {capability}; N={self._fmt_n(n1)}->{acc1}%, N={self._fmt_n(n2)}->{acc2}%"
        return problem, {
            "capability": capability,
            "data_points": [(n1, acc1), (n2, acc2)],
            "scaling": "linear", "threshold": threshold,
            "target_n": target_n,
            "formula": f"acc = {slope:.2e} * N + {acc1 - slope * n1:.1f}",
        }

    def _build_power_law(self, capability: str) -> tuple[str, dict]:
        """Build a power law extrapolation problem.

        Args:
            capability: Capability name.

        Returns:
            Tuple of (problem_string, solution_data).
        """
        alpha = round(self._rng.uniform(0.15, 0.3), 2)
        c = round(self._rng.uniform(0.3, 1.0), 2)
        n_points = [(10_000_000, round(c * (10_000_000 ** alpha), 1)),
                     (100_000_000, round(c * (100_000_000 ** alpha), 1)),
                     (1_000_000_000, round(c * (1_000_000_000 ** alpha), 1))]
        threshold = 50.0
        target_n = int((threshold / c) ** (1 / alpha)) if c > 0 else 10_000_000_000
        obs_parts = [f"N={self._fmt_n(n)}->{a}%" for n, a in n_points]
        problem = f"capability: {capability}; {', '.join(obs_parts)}"
        return problem, {
            "capability": capability,
            "data_points": n_points,
            "scaling": "power law", "threshold": threshold,
            "target_n": target_n,
            "formula": f"acc = {c} * N^{alpha}",
        }

    def _build_log_linear(self, capability: str) -> tuple[str, dict]:
        """Build a log-linear extrapolation problem.

        Args:
            capability: Capability name.

        Returns:
            Tuple of (problem_string, solution_data).
        """
        a = round(self._rng.uniform(3.0, 8.0), 1)
        b = round(self._rng.uniform(-40, -10), 1)
        n_points = [(10_000_000, round(a * math.log10(10_000_000) + b, 1)),
                     (100_000_000, round(a * math.log10(100_000_000) + b, 1)),
                     (1_000_000_000, round(a * math.log10(1_000_000_000) + b, 1))]
        threshold = 50.0
        target_n = int(10 ** ((threshold - b) / a)) if a > 0 else 10_000_000_000
        obs_parts = [f"N={self._fmt_n(n)}->{acc}%" for n, acc in n_points]
        problem = f"capability: {capability}; {', '.join(obs_parts)}"
        return problem, {
            "capability": capability,
            "data_points": n_points,
            "scaling": "log-linear", "threshold": threshold,
            "target_n": target_n,
            "formula": f"acc = {a} * log10(N) + {b}",
        }

    def _build_sigmoid(self, capability: str) -> tuple[str, dict]:
        """Build a sigmoid emergence problem.

        Args:
            capability: Capability name.

        Returns:
            Tuple of (problem_string, solution_data).
        """
        midpoint_log = round(self._rng.uniform(8.5, 10.0), 1)
        midpoint = int(10 ** midpoint_log)
        n_points = [(10_000_000, 2), (100_000_000, 5), (1_000_000_000, 15)]
        threshold = 50.0
        target_n = midpoint
        obs_parts = [f"N={self._fmt_n(n)}->{a}%" for n, a in n_points]
        problem = f"capability: {capability}; {', '.join(obs_parts)}"
        return problem, {
            "capability": capability,
            "data_points": n_points,
            "scaling": "sigmoid (sharp emergence)", "threshold": threshold,
            "target_n": target_n,
            "formula": f"acc = 100 / (1 + exp(-k*(log10(N)-{midpoint_log})))",
        }

    def _fmt_n(self, n: int) -> str:
        """Format a parameter count with M/B suffix.

        Args:
            n: Parameter count.

        Returns:
            Formatted string.
        """
        if n >= 1_000_000_000:
            return f"{n / 1_000_000_000:.1f}B"
        if n >= 1_000_000:
            return f"{n / 1_000_000:.0f}M"
        return str(n)

    def _create_steps(self, data: dict) -> list[str]:
        """Generate emergence prediction steps.

        Args:
            data: Solution data with scaling info.

        Returns:
            Steps showing data, fitted model, and prediction.
        """
        obs = [f"N={self._fmt_n(n)}->{a}%" for n, a in data["data_points"]]
        return [
            f"observed: {', '.join(obs)}",
            f"fit {data['scaling']}: {data['formula']}",
            f"threshold: {data['threshold']}% accuracy",
            f"predict emergence: N = {self._fmt_n(data['target_n'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the predicted scale for emergence.

        Args:
            data: Solution data.

        Returns:
            Parameter count string.
        """
        return f"~{self._fmt_n(data['target_n'])}"
