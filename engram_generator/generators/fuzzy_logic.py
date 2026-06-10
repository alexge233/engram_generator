"""Fuzzy logic generators.

4 generators across tiers 4-5 covering membership functions,
fuzzy operations, fuzzy inference (Mamdani), and defuzzification.
"""
from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


@register
class MembershipFunctionGenerator(StepGenerator):
    """Evaluate triangular and trapezoidal membership functions.

    Triangular: mu(x; a, b, c) = max(0, min((x-a)/(b-a), (c-x)/(c-b))).
    Trapezoidal: mu(x; a, b, c, d) with a flat top between b and c.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "membership_function"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["division"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "evaluate fuzzy membership function"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a membership function evaluation problem.

        Args:
            difficulty: Controls function type and parameter range.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        use_trap = difficulty >= 5
        mag = min(2 + difficulty, 8)

        a = self._rng.randint(0, mag)
        b = a + self._rng.randint(1, mag)

        if use_trap:
            c = b + self._rng.randint(1, mag)
            d = c + self._rng.randint(1, mag)
            x = round(self._rng.uniform(a - 1, d + 1), 4)

            # Trapezoidal membership
            if x <= a or x >= d:
                mu = 0.0
            elif x <= b:
                mu = (x - a) / (b - a)
            elif x <= c:
                mu = 1.0
            else:
                mu = (d - x) / (d - c)
            mu = round(max(0.0, mu), 4)

            steps = [
                f"trapezoidal(x={x}; a={a}, b={b}, c={c}, d={d})",
                f"left ramp: (x-a)/(b-a) = {round((x - a) / (b - a), 4) if b != a else 0}",
                f"right ramp: (d-x)/(d-c) = {round((d - x) / (d - c), 4) if d != c else 0}",
                f"mu = {mu}",
            ]
            problem = f"mu_trap(x={x}; a={a},b={b},c={c},d={d})"
        else:
            c = b + self._rng.randint(1, mag)
            x = round(self._rng.uniform(a - 1, c + 1), 4)

            # Triangular membership
            left = (x - a) / (b - a) if b != a else 0.0
            right = (c - x) / (c - b) if c != b else 0.0
            mu = round(max(0.0, min(left, right)), 4)

            steps = [
                f"triangular(x={x}; a={a}, b={b}, c={c})",
                f"left = (x-a)/(b-a) = {round(left, 4)}",
                f"right = (c-x)/(c-b) = {round(right, 4)}",
                f"mu = max(0, min(left, right)) = {mu}",
            ]
            problem = f"mu_tri(x={x}; a={a},b={b},c={c})"

        return problem, {"mu": mu, "steps_log": steps}

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data from _create_problem.

        Returns:
            List of step strings.
        """
        return sd["steps_log"]

    def _create_answer(self, sd: dict) -> str:
        """Extract the final answer.

        Args:
            sd: Solution data from _create_problem.

        Returns:
            Membership value.
        """
        return f"mu = {sd['mu']}"


@register
class FuzzyOperationsGenerator(StepGenerator):
    """Compute basic fuzzy set operations.

    AND = min(mu_A, mu_B), OR = max(mu_A, mu_B), NOT = 1 - mu_A.
    Evaluates multiple operations on given membership values.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "fuzzy_operations"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["comparison"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "fuzzy AND, OR, NOT operations"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a fuzzy operations problem.

        Args:
            difficulty: Controls number of sets and operations.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        n_sets = min(2 + difficulty // 3, 4)
        mus = [round(self._rng.uniform(0.0, 1.0), 4) for _ in range(n_sets)]

        results = {}
        steps = []

        # AND (pairwise min of first two)
        f_and = round(min(mus[0], mus[1]), 4)
        steps.append(f"AND(A,B) = min({mus[0]},{mus[1]}) = {f_and}")
        results["and"] = f_and

        # OR (pairwise max of first two)
        f_or = round(max(mus[0], mus[1]), 4)
        steps.append(f"OR(A,B) = max({mus[0]},{mus[1]}) = {f_or}")
        results["or"] = f_or

        # NOT of first
        f_not = round(1.0 - mus[0], 4)
        steps.append(f"NOT(A) = 1 - {mus[0]} = {f_not}")
        results["not_a"] = f_not

        # For higher difficulty, chain operations
        if n_sets >= 3:
            f_and3 = round(min(f_and, mus[2]), 4)
            steps.append(
                f"AND(A,B,C) = min({f_and},{mus[2]}) = {f_and3}"
            )
            results["and3"] = f_and3

        if n_sets >= 4:
            f_or4 = round(max(f_or, max(mus[2], mus[3])), 4)
            steps.append(
                f"OR(A,B,C,D) = max({f_or},{mus[2]},{mus[3]}) = {f_or4}"
            )
            results["or4"] = f_or4

        problem = f"Fuzzy ops on mu = {mus}"
        return problem, {
            "mus": mus, "results": results, "steps_log": steps,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data from _create_problem.

        Returns:
            List of step strings.
        """
        return sd["steps_log"]

    def _create_answer(self, sd: dict) -> str:
        """Extract the final answer.

        Args:
            sd: Solution data from _create_problem.

        Returns:
            All computed operation results.
        """
        r = sd["results"]
        return f"AND={r['and']}, OR={r['or']}, NOT_A={r['not_a']}"


@register
class FuzzyInferenceGenerator(StepGenerator):
    """Apply Mamdani fuzzy inference rules.

    Evaluates IF x is A AND y is B THEN z is C rules, applies
    rule strength truncation to output fuzzy sets, and aggregates
    the results.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "fuzzy_inference"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["fuzzy_operations"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "Mamdani fuzzy inference"

    def _triangular_mu(self, x: float, a: float, b: float,
                       c: float) -> float:
        """Evaluate a triangular membership function.

        Args:
            x: Input value.
            a: Left foot.
            b: Peak.
            c: Right foot.

        Returns:
            Membership degree in [0, 1].
        """
        if b == a:
            left = 0.0
        else:
            left = (x - a) / (b - a)
        if c == b:
            right = 0.0
        else:
            right = (c - x) / (c - b)
        return max(0.0, min(left, right))

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Mamdani fuzzy inference problem.

        Args:
            difficulty: Controls number of rules.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        n_rules = min(2 + difficulty // 3, 3)

        # Input values
        x_val = round(self._rng.uniform(0, 10), 4)
        y_val = round(self._rng.uniform(0, 10), 4)

        rules = []
        steps = []
        agg_strengths = []

        for i in range(n_rules):
            # Random triangular params for input sets
            ax = self._rng.randint(0, 4)
            bx = ax + self._rng.randint(1, 4)
            cx = bx + self._rng.randint(1, 4)
            ay = self._rng.randint(0, 4)
            by = ay + self._rng.randint(1, 4)
            cy = by + self._rng.randint(1, 4)

            mu_x = round(self._triangular_mu(x_val, ax, bx, cx), 4)
            mu_y = round(self._triangular_mu(y_val, ay, by, cy), 4)
            strength = round(min(mu_x, mu_y), 4)

            rules.append({
                "x_set": (ax, bx, cx),
                "y_set": (ay, by, cy),
                "mu_x": mu_x, "mu_y": mu_y,
                "strength": strength,
            })
            agg_strengths.append(strength)

            steps.append(
                f"R{i + 1}: mu_A(x)={mu_x}, mu_B(y)={mu_y}, "
                f"strength=min={strength}"
            )

        # Aggregate: max of rule strengths
        agg = round(max(agg_strengths), 4)
        steps.append(f"Aggregate: max strengths = {agg}")

        problem = f"Mamdani: x={x_val}, y={y_val}, {n_rules} rules"
        return problem, {
            "rules": rules, "aggregate": agg, "steps_log": steps,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data from _create_problem.

        Returns:
            List of step strings.
        """
        return sd["steps_log"]

    def _create_answer(self, sd: dict) -> str:
        """Extract the final answer.

        Args:
            sd: Solution data from _create_problem.

        Returns:
            Aggregated rule strengths.
        """
        strengths = [r["strength"] for r in sd["rules"]]
        return f"strengths={strengths}, agg={sd['aggregate']}"


@register
class DefuzzificationGenerator(StepGenerator):
    """Defuzzify a fuzzy set using the centroid method.

    Computes z* = sum(mu(z_i) * z_i) / sum(mu(z_i)) for a discrete
    set of points, converting a fuzzy output back to a crisp value.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "defuzzification"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["arithmetic_mean"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "centroid defuzzification"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a defuzzification problem.

        Args:
            difficulty: Controls number of discrete points.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        n_points = min(4 + difficulty, 8)

        # Generate discrete points with membership values
        z_vals = sorted([round(self._rng.uniform(0, 10), 4)
                         for _ in range(n_points)])
        mu_vals = [round(self._rng.uniform(0.0, 1.0), 4)
                   for _ in range(n_points)]

        # Ensure at least one non-zero membership
        if all(m < 0.01 for m in mu_vals):
            mu_vals[n_points // 2] = round(self._rng.uniform(0.3, 1.0), 4)

        numerator = sum(mu_vals[i] * z_vals[i] for i in range(n_points))
        denominator = sum(mu_vals)
        if abs(denominator) < 1e-12:
            denominator = 1.0

        centroid = round(numerator / denominator, 4)

        steps = [
            f"z = {z_vals}",
            f"mu = {mu_vals}",
            f"sum(mu*z) = {round(numerator, 4)}",
            f"sum(mu) = {round(denominator, 4)}",
            f"centroid = {round(numerator, 4)} / {round(denominator, 4)}",
        ]

        problem = (
            f"Centroid defuzzify: z={z_vals}, mu={mu_vals}"
        )
        return problem, {
            "centroid": centroid, "steps_log": steps,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data from _create_problem.

        Returns:
            List of step strings.
        """
        return sd["steps_log"]

    def _create_answer(self, sd: dict) -> str:
        """Extract the final answer.

        Args:
            sd: Solution data from _create_problem.

        Returns:
            Centroid value.
        """
        return f"z* = {sd['centroid']}"
