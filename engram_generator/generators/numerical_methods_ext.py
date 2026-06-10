"""Extended numerical methods generators.

8 generators across tiers 5-6 covering root-finding, integration,
ODE solvers, interpolation, matrix factorisation, and eigenvalue methods.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


@register
class SecantMethodGenerator(StepGenerator):
    """Find a root using the secant method.

    Applies x_{n+1} = x_n - f(x_n) * (x_n - x_{n-1}) / (f(x_n) - f(x_{n-1}))
    for 3-5 iterations on a polynomial f(x).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "secant_method"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["newton_raphson"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "secant method root finding"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a root-finding problem using the secant method.

        Args:
            difficulty: Controls polynomial complexity and iteration count.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        root = self._rng.randint(1, 3 + difficulty)
        a = self._rng.randint(1, 2 + difficulty // 2)
        # f(x) = a*(x - root) = a*x - a*root
        c = a * root
        n_iter = min(3 + difficulty // 3, 5)

        x_prev = root + self._rng.uniform(1.0, 3.0)
        x_curr = root - self._rng.uniform(0.5, 2.0)
        x_prev = round(x_prev, 4)
        x_curr = round(x_curr, 4)

        trace = []
        for _ in range(n_iter):
            f_prev = a * x_prev - c
            f_curr = a * x_curr - c
            denom = f_curr - f_prev
            if abs(denom) < 1e-12:
                break
            x_next = x_curr - f_curr * (x_curr - x_prev) / denom
            x_next = round(x_next, 4)
            trace.append(
                f"x_prev={x_prev}, x_curr={x_curr}, "
                f"f(x_prev)={round(f_prev, 4)}, f(x_curr)={round(f_curr, 4)}, "
                f"x_next={x_next}"
            )
            x_prev = x_curr
            x_curr = x_next

        problem = (
            f"f(x)={a}x-{c}, x0={round(x_prev, 4)}, "
            f"x1={round(x_curr, 4)}, {n_iter} iterations"
        )
        return problem, {
            "trace": trace,
            "final": x_curr,
            "root": root,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data from _create_problem.

        Returns:
            List of step strings.
        """
        return sd["trace"]

    def _create_answer(self, sd: dict) -> str:
        """Extract the final approximation.

        Args:
            sd: Solution data.

        Returns:
            Final root approximation.
        """
        return f"x={sd['final']} (root={sd['root']})"


@register
class FixedPointIterationGenerator(StepGenerator):
    """Find a fixed point via x_{n+1} = g(x_n).

    Generates an iteration function g with |g'(x)| < 1 near the
    fixed point and iterates 3-5 times to demonstrate convergence.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "fixed_point_iteration"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["derivative"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "fixed point iteration"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a fixed-point iteration problem.

        Uses g(x) = x/k + c/k where kx - c = 0 has root x* = c/k,
        and g'(x) = 1/k which satisfies |g'| < 1 for k >= 2.

        Args:
            difficulty: Controls constant magnitudes and iteration count.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        k = self._rng.randint(2, 3 + difficulty // 2)
        c = self._rng.randint(1, 4 + difficulty)
        fixed_pt = round(c / k, 4)
        g_prime = round(1 / k, 4)
        n_iter = min(3 + difficulty // 3, 5)

        x = round(self._rng.uniform(fixed_pt + 0.5, fixed_pt + 3.0), 4)
        trace = [f"x0={x}"]
        for i in range(n_iter):
            x_new = round(x / k + c / k, 4)
            trace.append(f"x{i + 1}=x/{k}+{c}/{k}={x_new}")
            x = x_new

        problem = (
            f"g(x)=x/{k}+{c}/{k}, x0={trace[0].split('=')[1]}, "
            f"{n_iter} iterations, g'(x)=1/{k}={g_prime}"
        )
        return problem, {
            "trace": trace,
            "final": x,
            "fixed_pt": fixed_pt,
            "g_prime": g_prime,
            "converges": abs(g_prime) < 1,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        steps = [f"|g'|={sd['g_prime']}<1, converges"]
        steps.extend(sd["trace"])
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Extract the final fixed-point approximation.

        Args:
            sd: Solution data.

        Returns:
            Final approximation and true fixed point.
        """
        return f"x={sd['final']} (fixed_pt={sd['fixed_pt']})"


@register
class SimpsonRuleGenerator(StepGenerator):
    """Approximate a definite integral using Simpson's rule.

    Applies (h/3) * (f(a) + 4*f(a+h) + 2*f(a+2h) + ... + f(b))
    with an even number of subintervals.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "simpson_rule"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["definite_integral"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "Simpson's rule integration"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Simpson's rule integration problem.

        Args:
            difficulty: Controls interval width and subinterval count.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        a_val = self._rng.randint(0, 2)
        b_val = a_val + self._rng.randint(1, 2 + difficulty)
        n = 2 * min(1 + difficulty // 2, 4)  # must be even
        h = (b_val - a_val) / n
        fn_type = self._rng.choice(["x^2", "x^3", "x"])

        xs = [a_val + i * h for i in range(n + 1)]
        if fn_type == "x^2":
            fxs = [x ** 2 for x in xs]
        elif fn_type == "x^3":
            fxs = [x ** 3 for x in xs]
        else:
            fxs = list(xs)

        # Simpson's 1/3 rule
        total = fxs[0] + fxs[-1]
        for i in range(1, n):
            total += 4 * fxs[i] if i % 2 == 1 else 2 * fxs[i]
        integral = round(h / 3 * total, 4)

        problem = (
            f"Simpson's rule: integral of {fn_type} from "
            f"{a_val} to {b_val}, n={n}"
        )
        return problem, {
            "fn": fn_type, "a": a_val, "b": b_val,
            "n": n, "h": round(h, 4), "xs": xs,
            "fxs": [round(f, 4) for f in fxs],
            "integral": integral,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        steps = [
            f"h=({sd['b']}-{sd['a']})/{sd['n']}={sd['h']}",
            f"f values: {sd['fxs']}",
        ]
        coeffs = []
        for i in range(sd["n"] + 1):
            if i == 0 or i == sd["n"]:
                coeffs.append("1")
            elif i % 2 == 1:
                coeffs.append("4")
            else:
                coeffs.append("2")
        steps.append(f"coefficients: {coeffs}")
        steps.append(f"integral=(h/3)*sum={sd['integral']}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Extract the integral approximation.

        Args:
            sd: Solution data.

        Returns:
            Integral value.
        """
        return f"{sd['integral']}"


@register
class RungeKuttaGenerator(StepGenerator):
    """Solve an ODE using the 4th-order Runge-Kutta method.

    Computes k1, k2, k3, k4 and applies
    y_{n+1} = y_n + (h/6)*(k1 + 2*k2 + 2*k3 + k4).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "runge_kutta"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["derivative"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "RK4 ODE step"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an RK4 ODE problem.

        Args:
            difficulty: Controls step count and ODE type.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        y0 = round(self._rng.uniform(0.5, 2.0), 2)
        h = round(self._rng.choice([0.1, 0.2, 0.25, 0.5]), 2)
        n_steps = min(1 + difficulty // 2, 3)
        ode = self._rng.choice(["y", "-y", "t+y"])

        def f(t: float, y: float) -> float:
            """Evaluate the ODE right-hand side."""
            if ode == "y":
                return y
            if ode == "-y":
                return -y
            return t + y

        t, y = 0.0, y0
        trace = []
        for _ in range(n_steps):
            k1 = f(t, y)
            k2 = f(t + h / 2, y + h * k1 / 2)
            k3 = f(t + h / 2, y + h * k2 / 2)
            k4 = f(t + h, y + h * k3)
            y_new = y + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
            trace.append({
                "t": round(t, 4), "y": round(y, 4),
                "k1": round(k1, 4), "k2": round(k2, 4),
                "k3": round(k3, 4), "k4": round(k4, 4),
                "y_new": round(y_new, 4),
            })
            t = round(t + h, 4)
            y = round(y_new, 4)

        problem = f"dy/dt={ode}, y(0)={y0}, h={h}, {n_steps} RK4 steps"
        return problem, {"ode": ode, "trace": trace, "final_t": t, "final_y": y}

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps showing each RK4 iteration.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        steps = []
        for s in sd["trace"]:
            steps.append(
                f"t={s['t']}: k1={s['k1']},k2={s['k2']},"
                f"k3={s['k3']},k4={s['k4']},y_new={s['y_new']}"
            )
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Extract the final ODE solution value.

        Args:
            sd: Solution data.

        Returns:
            Final y value.
        """
        return f"y({sd['final_t']})={sd['final_y']}"


@register
class LagrangeInterpolationGenerator(StepGenerator):
    """Interpolate a value using Lagrange's formula.

    Computes L(x) = sum_i y_i * prod_{j!=i} (x - x_j) / (x_i - x_j)
    for 3-4 data points.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "interpolation_lagrange"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["polynomial_eval"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "Lagrange interpolation"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Lagrange interpolation problem.

        Args:
            difficulty: Controls number of points and value range.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        n_pts = 3 if difficulty <= 4 else 4
        x_pts = sorted(self._rng.sample(range(-5, 6), n_pts))
        y_pts = [self._rng.randint(-5, 5 + difficulty) for _ in range(n_pts)]

        # Evaluate at a point not in x_pts
        x_eval = self._rng.choice(
            [v for v in range(-4, 5) if v not in x_pts]
        )

        # Compute Lagrange basis values
        basis_vals = []
        result = 0.0
        for i in range(n_pts):
            numer = 1.0
            denom = 1.0
            for j in range(n_pts):
                if j != i:
                    numer *= (x_eval - x_pts[j])
                    denom *= (x_pts[i] - x_pts[j])
            li = numer / denom
            basis_vals.append(round(li, 4))
            result += y_pts[i] * li

        result = round(result, 4)
        pts_str = ", ".join(
            f"({x_pts[i]},{y_pts[i]})" for i in range(n_pts)
        )
        problem = f"points: {pts_str}. Evaluate L({x_eval})"
        return problem, {
            "x_pts": x_pts, "y_pts": y_pts,
            "x_eval": x_eval, "basis": basis_vals,
            "result": result,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        steps = []
        for i, li in enumerate(sd["basis"]):
            steps.append(
                f"L_{i}({sd['x_eval']})={li}, "
                f"y_{i}={sd['y_pts'][i]}"
            )
        steps.append(
            f"L({sd['x_eval']})=sum(y_i*L_i)={sd['result']}"
        )
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Extract the interpolated value.

        Args:
            sd: Solution data.

        Returns:
            Interpolated value at x_eval.
        """
        return f"L({sd['x_eval']})={sd['result']}"


@register
class LUDecompositionGenerator(StepGenerator):
    """Factor a matrix A into L and U (A = LU).

    Decomposes a 2x2 or 3x3 matrix into lower and upper triangular
    factors using Gaussian elimination without pivoting.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "lu_decomposition"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["gaussian_elimination"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "LU decomposition"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an LU decomposition problem.

        Args:
            difficulty: Controls matrix size (2x2 vs 3x3).

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 4:
            return self._create_2x2()
        return self._create_3x3()

    def _create_2x2(self) -> tuple[str, dict]:
        """Generate a 2x2 LU decomposition problem.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        a11 = self._rng.randint(1, 5)
        a12 = self._rng.randint(-4, 4)
        a21 = self._rng.randint(-4, 4)
        a22 = self._rng.randint(-4, 5)
        A = [[a11, a12], [a21, a22]]

        # L = [[1, 0], [m, 1]], U = [[a11, a12], [0, a22 - m*a12]]
        m = round(a21 / a11, 4)
        u22 = round(a22 - m * a12, 4)
        L = [[1, 0], [m, 1]]
        U = [[a11, a12], [0, u22]]

        a_str = f"[[{a11},{a12}],[{a21},{a22}]]"
        return (
            f"A={a_str}. Find L, U such that A=LU.",
            {"A": A, "L": L, "U": U, "size": 2},
        )

    def _create_3x3(self) -> tuple[str, dict]:
        """Generate a 3x3 LU decomposition problem.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        A = [[self._rng.randint(-3, 4) for _ in range(3)] for _ in range(3)]
        # Ensure diagonal dominance for non-zero pivots
        for i in range(3):
            A[i][i] = max(abs(A[i][i]), 2) * (1 if A[i][i] >= 0 else -1)
            if A[i][i] == 0:
                A[i][i] = 2

        L = [[0.0] * 3 for _ in range(3)]
        U = [[0.0] * 3 for _ in range(3)]
        for i in range(3):
            L[i][i] = 1.0

        # Doolittle algorithm
        for j in range(3):
            for i in range(j + 1):
                s = sum(L[i][k] * U[k][j] for k in range(i))
                U[i][j] = round(A[i][j] - s, 4)
            for i in range(j + 1, 3):
                s = sum(L[i][k] * U[k][j] for k in range(j))
                if abs(U[j][j]) < 1e-12:
                    L[i][j] = 0.0
                else:
                    L[i][j] = round((A[i][j] - s) / U[j][j], 4)

        def fmt(M: list[list[float]]) -> str:
            """Format a matrix as a string."""
            rows = [",".join(str(v) for v in r) for r in M]
            return "[" + "],[".join(rows) + "]"

        return (
            f"A=[{fmt(A)}]. Find L, U.",
            {"A": A, "L": L, "U": U, "size": 3},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        def fmt(M: list[list[float]]) -> str:
            """Format a matrix as a string."""
            rows = [",".join(str(v) for v in r) for r in M]
            return "[" + "],[".join(rows) + "]"

        return [
            f"L=[{fmt(sd['L'])}]",
            f"U=[{fmt(sd['U'])}]",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Extract L and U matrices.

        Args:
            sd: Solution data.

        Returns:
            L and U in string form.
        """
        def fmt(M: list[list[float]]) -> str:
            """Format a matrix as a string."""
            rows = [",".join(str(v) for v in r) for r in M]
            return "[" + "],[".join(rows) + "]"

        return f"L=[{fmt(sd['L'])}], U=[{fmt(sd['U'])}]"


@register
class PowerMethodGenerator(StepGenerator):
    """Find the dominant eigenvalue using the power method.

    Iterates x_{k+1} = A * x_k / ||A * x_k|| for 3-5 iterations
    on a 2x2 matrix to approximate the largest eigenvalue.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "power_method"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["matrix_multiply"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "power method eigenvalue"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a power method problem on a 2x2 matrix.

        Args:
            difficulty: Controls iteration count and value range.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        # Build a 2x2 matrix with known dominant eigenvalue
        lam1 = self._rng.randint(3, 4 + difficulty)
        lam2 = self._rng.randint(1, lam1 - 1)
        A = [[lam1, 0], [0, lam2]]

        # Optionally rotate for harder problems
        if difficulty >= 4:
            off = self._rng.randint(1, 2)
            A = [[lam1 + off, off], [off, lam2 + off]]

        n_iter = min(3 + difficulty // 3, 5)
        x = [1.0, 1.0]

        trace = []
        eigenvalue_approx = 0.0
        for _ in range(n_iter):
            # Ax
            ax = [
                A[0][0] * x[0] + A[0][1] * x[1],
                A[1][0] * x[0] + A[1][1] * x[1],
            ]
            norm = math.sqrt(ax[0] ** 2 + ax[1] ** 2)
            if norm < 1e-12:
                break
            eigenvalue_approx = round(norm, 4)
            x_new = [round(ax[0] / norm, 4), round(ax[1] / norm, 4)]
            trace.append(
                f"Ax=[{round(ax[0], 4)},{round(ax[1], 4)}], "
                f"||Ax||={eigenvalue_approx}, "
                f"x=[{x_new[0]},{x_new[1]}]"
            )
            x = x_new

        a_str = f"[[{A[0][0]},{A[0][1]}],[{A[1][0]},{A[1][1]}]]"
        problem = f"A={a_str}, x0=[1,1], {n_iter} iterations"
        return problem, {
            "A": A, "trace": trace,
            "eigenvalue": eigenvalue_approx,
            "eigenvector": x,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return sd["trace"]

    def _create_answer(self, sd: dict) -> str:
        """Extract the dominant eigenvalue approximation.

        Args:
            sd: Solution data.

        Returns:
            Eigenvalue and eigenvector approximation.
        """
        return (
            f"lambda={sd['eigenvalue']}, "
            f"x=[{sd['eigenvector'][0]},{sd['eigenvector'][1]}]"
        )


@register
class ConditionNumberGenerator(StepGenerator):
    """Compute the condition number of a 2x2 matrix.

    Calculates cond(A) = ||A|| * ||A^{-1}|| using the Frobenius norm
    and determines whether the matrix is well- or ill-conditioned.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "condition_number"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["matrix_multiply"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "matrix condition number"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a condition number problem for a 2x2 matrix.

        Args:
            difficulty: Controls whether well- or ill-conditioned.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 4:
            # Well-conditioned
            a, b = self._rng.randint(2, 5), self._rng.randint(0, 2)
            c, d = self._rng.randint(0, 2), self._rng.randint(2, 5)
        else:
            # Potentially ill-conditioned
            a = self._rng.randint(5, 10 + difficulty)
            b = a - self._rng.randint(0, 1)
            c = self._rng.randint(1, 3)
            d = c + self._rng.randint(0, 1)

        A = [[a, b], [c, d]]
        det = a * d - b * c
        if det == 0:
            d += 1
            A[1][1] = d
            det = a * d - b * c

        # Inverse: (1/det) * [[d, -b], [-c, a]]
        inv = [
            [round(d / det, 4), round(-b / det, 4)],
            [round(-c / det, 4), round(a / det, 4)],
        ]

        # Frobenius norms
        norm_a = round(math.sqrt(a ** 2 + b ** 2 + c ** 2 + d ** 2), 4)
        norm_inv = round(
            math.sqrt(inv[0][0] ** 2 + inv[0][1] ** 2 +
                       inv[1][0] ** 2 + inv[1][1] ** 2),
            4,
        )
        cond = round(norm_a * norm_inv, 4)
        status = "well-conditioned" if cond < 100 else "ill-conditioned"

        a_str = f"[[{a},{b}],[{c},{d}]]"
        problem = f"A={a_str}. Compute cond(A) (Frobenius norm)."
        return problem, {
            "A": A, "inv": inv, "det": det,
            "norm_a": norm_a, "norm_inv": norm_inv,
            "cond": cond, "status": status,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        inv = sd["inv"]
        return [
            f"det(A)={sd['det']}",
            f"A^-1=[[{inv[0][0]},{inv[0][1]}],[{inv[1][0]},{inv[1][1]}]]",
            f"||A||_F={sd['norm_a']}",
            f"||A^-1||_F={sd['norm_inv']}",
            f"cond(A)={sd['norm_a']}*{sd['norm_inv']}={sd['cond']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Extract the condition number and classification.

        Args:
            sd: Solution data.

        Returns:
            Condition number and well/ill classification.
        """
        return f"cond(A)={sd['cond']}, {sd['status']}"
