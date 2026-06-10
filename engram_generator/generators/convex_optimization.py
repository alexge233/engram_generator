"""Convex optimization generators.

6 generators at tier 6 covering Fenchel conjugates, proximal operators,
dual problems, strong duality, subgradients, and the log barrier method.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


@register
class ConvexConjugateGenerator(StepGenerator):
    """Compute the Fenchel conjugate f*(y) = sup_x(xy - f(x)).

    For canonical convex functions (x^2/2, |x|, e^x), computes the
    conjugate by finding the supremum analytically. The student must
    set the derivative of xy - f(x) to zero, solve for x, and
    substitute back.

    Difficulty scaling:
        Difficulty 1-3: f(x) = a*x^2/2 (conjugate is y^2/(2a)).
        Difficulty 4-6: f(x) = a*|x| (conjugate is 0 if |y|<=a, else inf).
        Difficulty 7-8: f(x) = e^(ax) (conjugate involves y*ln(y/a)-y).

    Prerequisites:
        lagrange_multiplier (tier 6).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "convex_conjugate"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["lagrange_multiplier"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute Fenchel conjugate f*(y)"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Fenchel conjugate problem.

        Args:
            difficulty: Controls function type.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            return self._quadratic_case(difficulty)
        if difficulty <= 6:
            return self._abs_case(difficulty)
        return self._exp_case(difficulty)

    def _quadratic_case(self, difficulty: int) -> tuple[str, dict]:
        """Generate conjugate of f(x) = a*x^2/2.

        Args:
            difficulty: Controls coefficient a.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        a = self._rng.randint(1, 2 + difficulty)
        y = round(self._rng.uniform(0.5, 4.0), 4)
        # f*(y) = sup_x(xy - a*x^2/2). d/dx: y - a*x = 0 => x = y/a
        x_opt = round(y / a, 4)
        conj = round(y * x_opt - a * x_opt ** 2 / 2, 4)
        problem = f"f(x) = {a}x^2/2, y={y}. Compute f*(y)."
        return problem, {
            "kind": "quadratic", "a": a, "y": y,
            "x_opt": x_opt, "conjugate": conj,
            "formula": f"y^2/(2*{a})",
        }

    def _abs_case(self, difficulty: int) -> tuple[str, dict]:
        """Generate conjugate of f(x) = a*|x|.

        Args:
            difficulty: Controls coefficient a.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        a = self._rng.randint(1, 2 + difficulty)
        y = round(self._rng.uniform(-3.0, 3.0), 4)
        # f*(y) = 0 if |y| <= a, else +inf
        in_domain = abs(y) <= a
        conj = 0.0 if in_domain else float("inf")
        problem = f"f(x) = {a}|x|, y={y}. Compute f*(y)."
        return problem, {
            "kind": "abs", "a": a, "y": y,
            "in_domain": in_domain,
            "conjugate": conj,
            "formula": f"0 if |y|<={a}, +inf otherwise",
        }

    def _exp_case(self, difficulty: int) -> tuple[str, dict]:
        """Generate conjugate of f(x) = e^(ax).

        Args:
            difficulty: Controls coefficient a.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        a = self._rng.randint(1, difficulty)
        y = round(self._rng.uniform(0.5, 3.0), 4)
        # f*(y) = y*ln(y/a) - y for y > 0
        if y > 0:
            conj = round(y * math.log(y / a) - y, 4)
        else:
            conj = 0.0
        problem = f"f(x) = e^({a}x), y={y}. Compute f*(y)."
        return problem, {
            "kind": "exp", "a": a, "y": y,
            "conjugate": conj,
            "formula": f"y*ln(y/{a}) - y for y>0",
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data from _create_problem.

        Returns:
            List of step strings.
        """
        kind = sd["kind"]
        if kind == "quadratic":
            return [
                f"f*(y) = sup_x(xy - {sd['a']}x^2/2)",
                f"d/dx: y - {sd['a']}x = 0 => x = y/{sd['a']}",
                f"x_opt = {sd['x_opt']}",
                f"f*({sd['y']}) = {sd['conjugate']}",
            ]
        if kind == "abs":
            return [
                f"f*(y) = sup_x(xy - {sd['a']}|x|)",
                f"|y| = {round(abs(sd['y']), 4)}, a = {sd['a']}",
                f"|y| <= a: {sd['in_domain']}",
                f"f*({sd['y']}) = {sd['conjugate']}",
            ]
        return [
            f"f*(y) = sup_x(xy - e^({sd['a']}x))",
            f"d/dx: y - {sd['a']}e^({sd['a']}x) = 0",
            f"x = ln(y/{sd['a']})/{sd['a']}",
            f"f*({sd['y']}) = {sd['conjugate']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Extract the final answer.

        Args:
            sd: Solution data.

        Returns:
            Conjugate value string.
        """
        return f"f*({sd['y']}) = {sd['conjugate']}"


@register
class ProximalOperatorGenerator(StepGenerator):
    """Compute the proximal operator prox_f(v) = argmin(f(x) + ||x-v||^2/2).

    For f = lambda*|x|, the proximal operator is the soft-thresholding
    operator. The student must evaluate the closed-form solution
    sign(v)*max(|v| - lambda, 0).

    Difficulty scaling:
        Difficulty 1-3: small lambda and integer v.
        Difficulty 4-6: larger lambda, real-valued v.
        Difficulty 7-8: vector case (2D soft-thresholding).

    Prerequisites:
        gradient_descent (tier 4).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "proximal_operator"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["gradient_descent"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute proximal operator (soft threshold)"

    def _soft_threshold(self, v: float, lam: float) -> float:
        """Compute the scalar soft-thresholding operator.

        Args:
            v: Input value.
            lam: Threshold parameter.

        Returns:
            Soft-thresholded value.
        """
        if v > lam:
            return round(v - lam, 4)
        if v < -lam:
            return round(v + lam, 4)
        return 0.0

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a proximal operator problem.

        Args:
            difficulty: Controls parameter complexity.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            lam = round(self._rng.randint(1, 3) * 0.5, 4)
            v = self._rng.randint(-5, 5)
            result = self._soft_threshold(float(v), lam)
            problem = f"f(x)={lam}|x|, v={v}. Compute prox_f(v)."
            return problem, {
                "dim": 1, "lam": lam, "v": v,
                "result": result,
            }
        if difficulty <= 6:
            lam = round(self._rng.uniform(0.5, 3.0), 4)
            v = round(self._rng.uniform(-5.0, 5.0), 4)
            result = self._soft_threshold(v, lam)
            problem = f"f(x)={lam}|x|, v={v}. Compute prox_f(v)."
            return problem, {
                "dim": 1, "lam": lam, "v": v,
                "result": result,
            }
        # 2D case
        lam = round(self._rng.uniform(0.5, 2.0), 4)
        v1 = round(self._rng.uniform(-4.0, 4.0), 4)
        v2 = round(self._rng.uniform(-4.0, 4.0), 4)
        r1 = self._soft_threshold(v1, lam)
        r2 = self._soft_threshold(v2, lam)
        problem = (
            f"f(x)={lam}||x||_1, v=({v1},{v2}). "
            f"Compute prox_f(v)."
        )
        return problem, {
            "dim": 2, "lam": lam, "v": (v1, v2),
            "result": (r1, r2),
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        lam = sd["lam"]
        if sd["dim"] == 1:
            v = sd["v"]
            return [
                f"prox_f(v) = sign(v)*max(|v|-{lam}, 0)",
                f"|v| = {round(abs(v), 4)}",
                f"max(|v|-{lam}, 0) = {round(max(abs(v) - lam, 0), 4)}",
                f"prox_f({v}) = {sd['result']}",
            ]
        v1, v2 = sd["v"]
        r1, r2 = sd["result"]
        return [
            f"apply soft-threshold component-wise",
            f"prox_1: sign({v1})*max({round(abs(v1), 4)}-{lam},0) = {r1}",
            f"prox_2: sign({v2})*max({round(abs(v2), 4)}-{lam},0) = {r2}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Extract the final answer.

        Args:
            sd: Solution data.

        Returns:
            Proximal operator result.
        """
        if sd["dim"] == 1:
            return f"prox_f(v) = {sd['result']}"
        r1, r2 = sd["result"]
        return f"prox_f(v) = ({r1}, {r2})"


@register
class DualProblemGenerator(StepGenerator):
    """Write the dual of a primal linear program.

    Given primal min c^T x s.t. Ax <= b, x >= 0, constructs the
    dual max b^T y s.t. A^T y + s = c, y >= 0. Uses small 2-3
    constraint, 2-variable LPs.

    Difficulty scaling:
        Difficulty 1-3: 2 constraints, 2 variables.
        Difficulty 4-6: 3 constraints, 2 variables.
        Difficulty 7-8: 3 constraints, 3 variables.

    Prerequisites:
        linear_program (tier 5).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "dual_problem"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["linear_program"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "write the dual of a primal LP"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a primal LP and derive its dual.

        Args:
            difficulty: Controls constraint/variable count.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            m, n = 2, 2
        elif difficulty <= 6:
            m, n = 3, 2
        else:
            m, n = 3, 3

        c = [self._rng.randint(1, 3 + difficulty) for _ in range(n)]
        A = [[self._rng.randint(1, 3 + difficulty) for _ in range(n)]
             for _ in range(m)]
        b = [self._rng.randint(2, 8 + difficulty) for _ in range(m)]

        # Dual: max b^T y s.t. A^T y <= c, y >= 0
        AT = [[A[i][j] for i in range(m)] for j in range(n)]

        A_str = "; ".join(
            "[" + ",".join(str(v) for v in row) + "]" for row in A
        )
        problem = (
            f"min [{','.join(str(v) for v in c)}]^T x "
            f"s.t. A=[{A_str}]x <= [{','.join(str(v) for v in b)}], "
            f"x>=0. Write the dual."
        )
        return problem, {
            "c": c, "A": A, "b": b, "AT": AT, "m": m, "n": n,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        steps = [
            "primal min -> dual max",
            "swap roles of c and b",
            f"A^T = {sd['AT']}",
        ]
        for j in range(sd["n"]):
            row = sd["AT"][j]
            con = (
                "+".join(f"{row[i]}y{i + 1}" for i in range(sd["m"]))
                + f"<={sd['c'][j]}"
            )
            steps.append(f"dual constraint {j + 1}: {con}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Extract the dual formulation.

        Args:
            sd: Solution data.

        Returns:
            Dual objective and constraint summary.
        """
        obj = "+".join(f"{sd['b'][i]}y{i + 1}" for i in range(sd["m"]))
        return f"max {obj}, {sd['n']} constraints, y>=0"


@register
class StrongDualityGenerator(StepGenerator):
    """Check Slater's condition for strong duality.

    Given a convex program min f(x) s.t. Ax < b, verifies that there
    exists a strictly feasible point x such that all inequality
    constraints hold strictly. If Slater's condition is satisfied,
    strong duality holds.

    Difficulty scaling:
        Difficulty 1-3: 2 constraints, easy feasibility.
        Difficulty 4-6: 3 constraints.
        Difficulty 7-8: 4 constraints, tighter feasible region.

    Prerequisites:
        dual_problem (tier 6).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "strong_duality"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["dual_problem"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "check Slater's condition for strong duality"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Slater's condition check problem.

        Args:
            difficulty: Controls constraint count.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        m = min(2 + difficulty // 3, 4)
        A = [[self._rng.randint(1, 3 + difficulty) for _ in range(2)]
             for _ in range(m)]
        b = [self._rng.randint(4, 10 + difficulty * 2) for _ in range(m)]

        # Try x = (1, 1) as a candidate strictly feasible point
        x_cand = [1.0, 1.0]
        slacks = []
        all_strict = True
        for i in range(m):
            val = A[i][0] * x_cand[0] + A[i][1] * x_cand[1]
            slack = round(b[i] - val, 4)
            slacks.append(slack)
            if slack <= 0:
                all_strict = False

        # If candidate fails, try x = (0.5, 0.5)
        if not all_strict:
            x_cand = [0.5, 0.5]
            slacks = []
            all_strict = True
            for i in range(m):
                val = A[i][0] * x_cand[0] + A[i][1] * x_cand[1]
                slack = round(b[i] - val, 4)
                slacks.append(slack)
                if slack <= 0:
                    all_strict = False

        A_str = "; ".join(
            f"{A[i][0]}x1+{A[i][1]}x2<={b[i]}" for i in range(m)
        )
        problem = f"min f(x) s.t. {A_str}. Check Slater's condition."
        return problem, {
            "A": A, "b": b, "m": m,
            "x_cand": x_cand, "slacks": slacks,
            "slater_holds": all_strict,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        x = sd["x_cand"]
        steps = [
            f"try x = ({x[0]}, {x[1]})",
        ]
        for i in range(sd["m"]):
            a_row = sd["A"][i]
            val = round(a_row[0] * x[0] + a_row[1] * x[1], 4)
            steps.append(
                f"g{i + 1}(x) = {val}, b{i + 1} = {sd['b'][i]}, "
                f"slack = {sd['slacks'][i]}"
            )
        if sd["slater_holds"]:
            steps.append("all slacks > 0: Slater's holds")
        else:
            steps.append("some slack <= 0: Slater's fails")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Extract the final answer.

        Args:
            sd: Solution data.

        Returns:
            Slater's condition result.
        """
        if sd["slater_holds"]:
            return "Slater's holds, strong duality guaranteed"
        return "Slater's fails for tested point"


@register
class SubgradientGenerator(StepGenerator):
    """Compute a subgradient of a non-smooth convex function.

    For f(x) = |x|: subgradient is sign(x) when x != 0, any g in [-1,1]
    at x = 0. For f(x) = max(0, 1-x): g = 0 if x > 1, g = -1 if x < 1,
    g in [-1, 0] at x = 1.

    Difficulty scaling:
        Difficulty 1-3: f(x) = a*|x| at integer points.
        Difficulty 4-6: f(x) = max(0, c - ax) (hinge loss).
        Difficulty 7-8: f(x) = max(f1(x), f2(x)) at kink.

    Prerequisites:
        gradient_descent (tier 4).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "subgradient"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["gradient_descent"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute subgradient of non-smooth function"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a subgradient computation problem.

        Args:
            difficulty: Controls function type.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            return self._abs_case(difficulty)
        if difficulty <= 6:
            return self._hinge_case(difficulty)
        return self._max_case(difficulty)

    def _abs_case(self, difficulty: int) -> tuple[str, dict]:
        """Generate subgradient of a*|x|.

        Args:
            difficulty: Controls coefficient and point.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        a = self._rng.randint(1, 2 + difficulty)
        x = self._rng.choice([-3, -2, -1, 0, 1, 2, 3])
        if x > 0:
            g = a
            subdiff = f"{{{a}}}"
        elif x < 0:
            g = -a
            subdiff = f"{{{-a}}}"
        else:
            g = 0
            subdiff = f"[{-a}, {a}]"
        problem = f"f(x) = {a}|x|, x={x}. Compute a subgradient."
        return problem, {
            "kind": "abs", "a": a, "x": x,
            "g": g, "subdiff": subdiff,
        }

    def _hinge_case(self, difficulty: int) -> tuple[str, dict]:
        """Generate subgradient of max(0, c - ax) (hinge loss).

        Args:
            difficulty: Controls parameters.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        a = self._rng.randint(1, 2 + difficulty)
        c = self._rng.randint(1, 3 + difficulty)
        x = round(self._rng.uniform(-2.0, 4.0), 4)
        threshold = round(c / a, 4)
        if x < threshold:
            g = -a
            subdiff = f"{{{-a}}}"
        elif x > threshold:
            g = 0
            subdiff = "{0}"
        else:
            g = round(-a / 2, 4)
            subdiff = f"[{-a}, 0]"
        problem = (
            f"f(x) = max(0, {c}-{a}x), x={x}. "
            f"Compute a subgradient."
        )
        return problem, {
            "kind": "hinge", "a": a, "c": c, "x": x,
            "threshold": threshold, "g": g, "subdiff": subdiff,
        }

    def _max_case(self, difficulty: int) -> tuple[str, dict]:
        """Generate subgradient of max(f1, f2) at a kink point.

        Args:
            difficulty: Controls function complexity.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        # f(x) = max(a1*x + b1, a2*x + b2)
        a1 = self._rng.randint(1, difficulty)
        b1 = self._rng.randint(-3, 3)
        a2 = self._rng.randint(-difficulty, -1)
        b2 = self._rng.randint(-3, 3)
        # Kink at a1*x + b1 = a2*x + b2 => x = (b2 - b1) / (a1 - a2)
        denom = a1 - a2
        x_kink = round((b2 - b1) / denom, 4)
        # At the kink, subdifferential is [min(a1,a2), max(a1,a2)]
        g_lo = min(a1, a2)
        g_hi = max(a1, a2)
        g = round((g_lo + g_hi) / 2, 4)
        subdiff = f"[{g_lo}, {g_hi}]"
        problem = (
            f"f(x) = max({a1}x+{b1}, {a2}x+{b2}), "
            f"x={x_kink}. Compute a subgradient."
        )
        return problem, {
            "kind": "max", "a1": a1, "b1": b1, "a2": a2, "b2": b2,
            "x": x_kink, "g": g, "subdiff": subdiff,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        kind = sd["kind"]
        if kind == "abs":
            return [
                f"f(x) = {sd['a']}|x|, x = {sd['x']}",
                f"subdifferential at x={sd['x']}: {sd['subdiff']}",
                f"choose g = {sd['g']}",
            ]
        if kind == "hinge":
            return [
                f"kink at x = {sd['c']}/{sd['a']} = {sd['threshold']}",
                f"x = {sd['x']}, threshold = {sd['threshold']}",
                f"subdifferential: {sd['subdiff']}",
                f"choose g = {sd['g']}",
            ]
        return [
            f"f1 = {sd['a1']}x+{sd['b1']}, f2 = {sd['a2']}x+{sd['b2']}",
            f"kink at x = {sd['x']} where f1 = f2",
            f"subdifferential: {sd['subdiff']}",
            f"choose g = {sd['g']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Extract the final answer.

        Args:
            sd: Solution data.

        Returns:
            Subgradient value and subdifferential.
        """
        return f"g = {sd['g']}, subdiff = {sd['subdiff']}"


@register
class BarrierMethodGenerator(StepGenerator):
    """Perform one Newton step of the log barrier method.

    Minimises f(x) - (1/t)*sum(log(-g_i(x))) where g_i are inequality
    constraints. Computes the barrier gradient and Hessian, then takes
    a Newton step.

    Difficulty scaling:
        Difficulty 1-3: f(x) = ax^2, one constraint.
        Difficulty 4-6: f(x) = ax^2 + bx, two constraints.
        Difficulty 7-8: quadratic with three constraints.

    Prerequisites:
        gradient_descent (tier 4).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "barrier_method"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["gradient_descent"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "one Newton step of log barrier method"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a log barrier Newton step problem.

        Args:
            difficulty: Controls constraint count and coefficients.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        a = self._rng.randint(1, 2 + difficulty)
        b = self._rng.randint(-3, 3)
        t = self._rng.choice([1, 2, 5, 10])

        if difficulty <= 3:
            constraints = [("x", self._rng.randint(2, 5 + difficulty))]
        elif difficulty <= 6:
            ub = self._rng.randint(2, 5 + difficulty)
            lb = self._rng.randint(-5, 0)
            constraints = [("x", ub), ("-x", -lb)]
        else:
            ub = self._rng.randint(3, 6 + difficulty)
            lb = self._rng.randint(-4, 0)
            c3 = self._rng.randint(1, 3)
            constraints = [("x", ub), ("-x", -lb), (f"{c3}x", ub + c3)]

        # Start at x0 strictly feasible
        x0 = round(self._rng.uniform(0.5, min(c[1] for c in constraints) - 0.5), 4)

        # Compute barrier value: f(x) - (1/t)*sum(log(b_i - a_i*x))
        # For simplicity, constraint g_i: a_i*x <= b_i => b_i - a_i*x > 0
        barrier_grad = 2 * a * x0 + b
        barrier_hess = 2.0 * a
        for coeff_str, bound in constraints:
            if coeff_str == "x":
                ci = 1.0
            elif coeff_str == "-x":
                ci = -1.0
            else:
                ci = float(coeff_str.replace("x", ""))
            slack = bound - ci * x0
            if slack <= 0:
                slack = 0.1
            barrier_grad += (1.0 / t) * (ci / slack)
            barrier_hess += (1.0 / t) * (ci * ci / (slack * slack))

        barrier_grad = round(barrier_grad, 4)
        barrier_hess = round(barrier_hess, 4)

        # Newton step: x1 = x0 - grad / hess
        if abs(barrier_hess) > 1e-9:
            step = round(-barrier_grad / barrier_hess, 4)
        else:
            step = 0.0
        x1 = round(x0 + step, 4)

        con_str = ", ".join(f"{c[0]}<={c[1]}" for c in constraints)
        problem = (
            f"min {a}x^2+{b}x s.t. {con_str}, "
            f"t={t}, x0={x0}. One Newton step."
        )
        return problem, {
            "a": a, "b": b, "t": t,
            "constraints": constraints,
            "x0": x0, "barrier_grad": barrier_grad,
            "barrier_hess": barrier_hess,
            "step": step, "x1": x1,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return [
            f"phi(x) = {sd['a']}x^2+{sd['b']}x - (1/{sd['t']})*sum(log(slack))",
            f"x0 = {sd['x0']}",
            f"barrier grad = {sd['barrier_grad']}",
            f"barrier hess = {sd['barrier_hess']}",
            f"Newton step = {sd['step']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Extract the final answer.

        Args:
            sd: Solution data.

        Returns:
            New iterate after Newton step.
        """
        return f"x1 = {sd['x1']}"
