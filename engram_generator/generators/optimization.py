"""Optimization generators.

6 generators across tiers 5-6 covering linear programming,
simplex method, duality, convexity, KKT conditions, and
gradient descent convergence.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


@register
class LinearProgramGenerator(StepGenerator):
    """Solve a 2-variable linear program by vertex enumeration.

    Generates a maximisation LP with random objective coefficients and
    inequality constraints. The student must list feasible vertices,
    evaluate the objective at each, and identify the maximum.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "linear_program"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["system_equations"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "solve LP by vertex enumeration"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a 2-variable LP with constraints and solve it.

        Args:
            difficulty: Controls coefficient magnitudes and constraint count.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        c1 = self._rng.randint(1, 3 + difficulty)
        c2 = self._rng.randint(1, 3 + difficulty)
        n_cons = min(2 + difficulty // 2, 4)
        constraints = []
        for _ in range(n_cons):
            a1 = self._rng.randint(1, 4)
            a2 = self._rng.randint(1, 4)
            b = self._rng.randint(4, 8 + difficulty * 2)
            constraints.append((a1, a2, b))

        # Collect vertices from all pairs of constraint boundaries + axes
        vertices = []
        lines = list(constraints) + [(1, 0, 0), (0, 1, 0)]
        for i in range(len(lines)):
            for j in range(i + 1, len(lines)):
                a1, a2, b1 = lines[i]
                c1_, c2_, b2 = lines[j]
                det = a1 * c2_ - a2 * c1_
                if det == 0:
                    continue
                x = (b1 * c2_ - a2 * b2) / det
                y = (a1 * b2 - b1 * c1_) / det
                if x < -1e-9 or y < -1e-9:
                    continue
                feasible = True
                for ca1, ca2, cb in constraints:
                    if ca1 * x + ca2 * y > cb + 1e-9:
                        feasible = False
                        break
                if feasible:
                    vertices.append((round(x, 4), round(y, 4)))

        # Deduplicate
        seen = set()
        unique = []
        for v in vertices:
            key = (round(v[0], 3), round(v[1], 3))
            if key not in seen:
                seen.add(key)
                unique.append(v)
        vertices = unique

        if not vertices:
            vertices = [(0, 0)]

        obj_vals = [(c1 * x + c2 * y, x, y) for x, y in vertices]
        best = max(obj_vals, key=lambda t: t[0])

        con_str = "; ".join(
            f"{a1}x1+{a2}x2<={b}" for a1, a2, b in constraints
        )
        problem = (
            f"max {c1}x1+{c2}x2 s.t. {con_str}, x1>=0, x2>=0"
        )
        return problem, {
            "c": (c1, c2),
            "constraints": constraints,
            "vertices": vertices,
            "obj_vals": [(round(v, 4), x, y) for v, x, y in obj_vals],
            "best": (round(best[0], 4), best[1], best[2]),
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data from _create_problem.

        Returns:
            List of step strings.
        """
        steps = []
        verts_str = ", ".join(
            f"({x},{y})" for x, y in sd["vertices"]
        )
        steps.append(f"vertices: {verts_str}")
        c1, c2 = sd["c"]
        for val, x, y in sd["obj_vals"]:
            steps.append(f"z({x},{y})={val}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Extract the optimal solution.

        Args:
            sd: Solution data.

        Returns:
            Optimal value and point.
        """
        val, x, y = sd["best"]
        return f"max={val} at ({x},{y})"


@register
class SimplexStepGenerator(StepGenerator):
    """Perform one simplex pivot on a tableau.

    Given a small simplex tableau, identify the entering and leaving
    variables via minimum ratio test, then perform the pivot operation.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "simplex_step"

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
        return "perform one simplex pivot"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a simplex tableau and perform one pivot.

        Args:
            difficulty: Controls tableau coefficient range.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        # 2-variable, 2-slack tableau: [x1, x2, s1, s2 | rhs]
        a = [[self._rng.randint(1, 3 + difficulty) for _ in range(2)]
             for _ in range(2)]
        rhs = [self._rng.randint(4, 10 + difficulty * 2) for _ in range(2)]
        obj = [self._rng.randint(1, 4 + difficulty),
               self._rng.randint(1, 4 + difficulty)]

        # Build tableau rows: [a_i1, a_i2, s1_col, s2_col, rhs]
        tableau = []
        for i in range(2):
            row = list(a[i]) + [0, 0, rhs[i]]
            row[2 + i] = 1
            tableau.append(row)
        # Objective row (negated for max): [-c1, -c2, 0, 0, 0]
        obj_row = [-obj[0], -obj[1], 0, 0, 0]
        tableau.append(obj_row)

        # Entering: most negative in obj row
        entering = 0 if obj_row[0] <= obj_row[1] else 1

        # Leaving: minimum ratio test
        ratios = []
        for i in range(2):
            if tableau[i][entering] > 0:
                ratios.append((tableau[i][4] / tableau[i][entering], i))
        if not ratios:
            # Force a valid tableau
            a[0][entering] = 2
            tableau[0][entering] = 2
            ratios = [(rhs[0] / 2, 0)]

        leaving = min(ratios, key=lambda t: t[0])[1]
        pivot_val = tableau[leaving][entering]

        # Pivot
        new_tab = [row[:] for row in tableau]
        for j in range(5):
            new_tab[leaving][j] = round(
                tableau[leaving][j] / pivot_val, 4
            )
        for i in range(3):
            if i == leaving:
                continue
            factor = tableau[i][entering]
            for j in range(5):
                new_tab[i][j] = round(
                    tableau[i][j] - factor * new_tab[leaving][j], 4
                )

        tab_str = " ; ".join(
            "[" + ",".join(str(v) for v in row) + "]"
            for row in tableau
        )
        labels = ["x1", "x2", "s1", "s2"]
        return (
            f"tableau: {tab_str}. Pivot once.",
            {
                "tableau": tableau,
                "entering": entering,
                "leaving": leaving,
                "pivot_val": pivot_val,
                "new_tableau": new_tab,
                "labels": labels,
            },
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        lbl = sd["labels"]
        return [
            f"entering: {lbl[sd['entering']]} (most negative)",
            f"leaving: {lbl[2 + sd['leaving']]} (min ratio)",
            f"pivot element: {sd['pivot_val']}",
            "new row: ["
            + ",".join(str(v) for v in sd["new_tableau"][sd["leaving"]])
            + "]",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Extract the pivoted tableau objective row.

        Args:
            sd: Solution data.

        Returns:
            New objective row after pivot.
        """
        obj = sd["new_tableau"][2]
        return "obj=[" + ",".join(str(v) for v in obj) + "]"


@register
class DualLPGenerator(StepGenerator):
    """Write the dual of a given linear program.

    Given a primal LP (max c^T x s.t. Ax <= b, x >= 0), produce
    the dual (min b^T y s.t. A^T y >= c, y >= 0) by transposing
    the constraint matrix.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "dual_lp"

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
        return "write the dual LP"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a primal LP and compute its dual.

        Args:
            difficulty: Controls matrix size and coefficient range.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        m = min(2 + difficulty // 3, 3)  # constraints
        n = 2  # variables
        c = [self._rng.randint(1, 4 + difficulty) for _ in range(n)]
        A = [[self._rng.randint(1, 3 + difficulty) for _ in range(n)]
             for _ in range(m)]
        b = [self._rng.randint(3, 10 + difficulty) for _ in range(m)]

        # Dual: min b^T y s.t. A^T y >= c, y >= 0
        AT = [[A[i][j] for i in range(m)] for j in range(n)]

        A_str = "; ".join(
            "[" + ",".join(str(v) for v in row) + "]" for row in A
        )
        problem = (
            f"max [{','.join(str(v) for v in c)}]^T x "
            f"s.t. A=[{A_str}], b=[{','.join(str(v) for v in b)}], x>=0. "
            f"Write the dual."
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
            f"primal: max -> dual: min",
            f"swap b and c roles",
            f"A^T = {sd['AT']}",
        ]
        for j in range(sd["n"]):
            row = sd["AT"][j]
            con = (
                "+".join(f"{row[i]}y{i + 1}" for i in range(sd["m"]))
                + f">={sd['c'][j]}"
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
        return f"min {obj}, {sd['n']} constraints, y>=0"


@register
class ConvexCheckGenerator(StepGenerator):
    """Check convexity of a function.

    For 1D functions, compute the second derivative and check sign.
    For 2D functions, compute Hessian eigenvalues and verify
    positive semi-definiteness.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "convex_check"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["eigenvalue"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "check convexity"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a function and check its convexity.

        Args:
            difficulty: Controls whether 1D or 2D, and coefficient range.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 4:
            return self._create_1d(difficulty)
        return self._create_2d(difficulty)

    def _create_1d(self, difficulty: int) -> tuple[str, dict]:
        """Generate a 1D convexity check problem.

        Args:
            difficulty: Controls coefficient magnitude.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        a = self._rng.randint(1, 3 + difficulty)
        b = self._rng.randint(-5, 5)
        c = self._rng.randint(-5, 5)
        sign = self._rng.choice([1, -1])
        a = a * sign
        # f(x) = a*x^2 + b*x + c
        f_str = f"{a}x^2+{b}x+{c}"
        second_deriv = 2 * a
        convex = second_deriv > 0
        concave = second_deriv < 0
        if second_deriv == 0:
            result = "linear (both convex and concave)"
        elif convex:
            result = "convex"
        else:
            result = "concave"
        return (
            f"f(x) = {f_str}. Is f convex?",
            {
                "fn": f_str, "dim": 1,
                "second_deriv": second_deriv,
                "result": result,
            },
        )

    def _create_2d(self, difficulty: int) -> tuple[str, dict]:
        """Generate a 2D convexity check via Hessian eigenvalues.

        Args:
            difficulty: Controls coefficient magnitude.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        # f(x,y) = a*x^2 + b*y^2 + c*x*y
        a = self._rng.randint(1, 2 + difficulty)
        b = self._rng.randint(1, 2 + difficulty)
        c = self._rng.randint(-3, 3)
        if self._rng.random() < 0.3:
            a = -a  # make some non-convex
        f_str = f"{a}x^2+{b}y^2+{c}xy"
        # Hessian: [[2a, c], [c, 2b]]
        h11, h12, h22 = 2 * a, c, 2 * b
        trace = h11 + h22
        det = h11 * h22 - h12 * h12
        disc = math.sqrt(max(trace * trace - 4 * det, 0))
        e1 = round((trace + disc) / 2, 4)
        e2 = round((trace - disc) / 2, 4)
        if e1 >= 0 and e2 >= 0:
            result = "convex"
        elif e1 <= 0 and e2 <= 0:
            result = "concave"
        else:
            result = "neither"
        return (
            f"f(x,y) = {f_str}. Check convexity.",
            {
                "fn": f_str, "dim": 2,
                "hessian": [[h11, h12], [h12, h22]],
                "eigenvalues": (e1, e2),
                "result": result,
            },
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        if sd["dim"] == 1:
            return [
                f"f''(x) = {sd['second_deriv']}",
                f"{'>=0 -> convex' if sd['second_deriv'] >= 0 else '<0 -> concave'}",
            ]
        h = sd["hessian"]
        e1, e2 = sd["eigenvalues"]
        return [
            f"H = [[{h[0][0]},{h[0][1]}],[{h[1][0]},{h[1][1]}]]",
            f"eigenvalues: {e1}, {e2}",
            f"both>=0 -> convex" if e1 >= 0 and e2 >= 0
            else f"sign check: {sd['result']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the convexity result.

        Args:
            sd: Solution data.

        Returns:
            Convexity classification.
        """
        return sd["result"]


@register
class KKTConditionsGenerator(StepGenerator):
    """Write KKT conditions for a constrained optimisation problem.

    Given min f(x) subject to g(x) <= 0, write out the stationarity,
    complementary slackness, and dual feasibility conditions.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "kkt_conditions"

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
        return "write KKT conditions"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a constrained optimisation and derive KKT conditions.

        Args:
            difficulty: Controls coefficient range and constraint count.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        # f(x) = a*x^2 + b*x, g(x) = c*x - d <= 0
        a = self._rng.randint(1, 3 + difficulty)
        b = self._rng.randint(-5, 5)
        c = self._rng.randint(1, 3 + difficulty)
        d = self._rng.randint(1, 5 + difficulty)

        # grad f = 2*a*x + b, grad g = c
        # KKT: 2*a*x + b + lambda*c = 0
        # Complementary slackness: lambda*(c*x - d) = 0
        # Primal feasibility: c*x - d <= 0
        # Dual feasibility: lambda >= 0

        # Unconstrained minimum: x* = -b / (2*a)
        x_unc = round(-b / (2 * a), 4)
        g_at_unc = round(c * x_unc - d, 4)

        if g_at_unc <= 0:
            # Constraint inactive: lambda = 0, x* = x_unc
            lam = 0.0
            x_star = x_unc
        else:
            # Constraint active: c*x = d -> x = d/c
            x_star = round(d / c, 4)
            # lambda from stationarity: 2*a*(d/c) + b + lambda*c = 0
            lam = round(-(2 * a * x_star + b) / c, 4)
            if lam < 0:
                # Infeasible KKT; use unconstrained and note
                lam = 0.0
                x_star = x_unc

        f_star = round(a * x_star ** 2 + b * x_star, 4)

        problem = (
            f"min {a}x^2+{b}x s.t. {c}x-{d}<=0. "
            f"Write KKT conditions."
        )
        return problem, {
            "a": a, "b": b, "c": c, "d": d,
            "x_star": x_star, "lambda": lam, "f_star": f_star,
            "grad_f": f"2*{a}*x+{b}",
            "grad_g": str(c),
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return [
            f"stationarity: {sd['grad_f']}+lambda*{sd['grad_g']}=0",
            f"comp. slackness: lambda*({sd['c']}x-{sd['d']})=0",
            f"primal: {sd['c']}x-{sd['d']}<=0",
            f"dual: lambda>=0",
            f"x*={sd['x_star']}, lambda={sd['lambda']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Extract the KKT solution.

        Args:
            sd: Solution data.

        Returns:
            Optimal point and multiplier.
        """
        return (
            f"x*={sd['x_star']}, lambda={sd['lambda']}, "
            f"f*={sd['f_star']}"
        )


@register
class GradientDescentConvergenceGenerator(StepGenerator):
    """Compute gradient descent steps and show convergence.

    Applies the update rule x_{k+1} = x_k - alpha * grad f(x_k)
    for n steps and shows convergence towards the minimum.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "gradient_descent_convergence"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

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
        return "gradient descent convergence"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a GD convergence problem on a quadratic.

        Args:
            difficulty: Controls step count and coefficient range.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        # f(x) = a*x^2 + b*x + c  ->  grad = 2*a*x + b
        a = self._rng.randint(1, 2 + difficulty)
        b = self._rng.randint(-5, 5)
        c_val = self._rng.randint(0, 5)
        x0 = round(self._rng.uniform(-5.0, 5.0), 2)
        alpha = round(self._rng.choice([0.01, 0.05, 0.1, 0.2]), 2)
        n_steps = min(3 + difficulty, 8)

        x = x0
        trace = [round(x, 4)]
        for _ in range(n_steps):
            grad = 2 * a * x + b
            x = x - alpha * grad
            x = round(x, 4)
            trace.append(x)

        x_min = round(-b / (2 * a), 4)
        f_min = round(a * x_min ** 2 + b * x_min + c_val, 4)
        f_final = round(a * trace[-1] ** 2 + b * trace[-1] + c_val, 4)

        problem = (
            f"f(x)={a}x^2+{b}x+{c_val}, x0={x0}, "
            f"alpha={alpha}, {n_steps} steps"
        )
        return problem, {
            "a": a, "b": b, "c": c_val, "x0": x0,
            "alpha": alpha, "n_steps": n_steps,
            "trace": trace, "x_min": x_min,
            "f_min": f_min, "f_final": f_final,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps showing each GD iteration.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        steps = []
        for k in range(sd["n_steps"]):
            xk = sd["trace"][k]
            xk1 = sd["trace"][k + 1]
            grad = round(2 * sd["a"] * xk + sd["b"], 4)
            steps.append(
                f"k={k}: x={xk}, grad={grad}, x_new={xk1}"
            )
        steps.append(f"x_min={sd['x_min']}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Extract the final GD state.

        Args:
            sd: Solution data.

        Returns:
            Final x value and function value.
        """
        return (
            f"x_final={sd['trace'][-1]}, f={sd['f_final']}, "
            f"x_min={sd['x_min']}"
        )
