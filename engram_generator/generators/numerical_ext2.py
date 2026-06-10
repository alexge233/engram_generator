"""Extended numerical methods generators (set 2).

6 generators across tiers 5-6.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


@register
class GaussianQuadratureGenerator(StepGenerator):
    """Approximate an integral using 2-point Gauss-Legendre quadrature.

    Transforms [a, b] to [-1, 1] and applies
    integral ~ (b-a)/2 * [f(x1) + f(x2)] where x1, x2 are the
    Gauss points at -1/sqrt(3) and 1/sqrt(3).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "gaussian_quadrature"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

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
        return "2-point Gauss-Legendre quadrature"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Gaussian quadrature problem.

        Args:
            difficulty: Controls interval and function.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        a_val = self._rng.randint(0, 2)
        b_val = a_val + self._rng.randint(1, 2 + difficulty)
        fn_type = self._rng.choice(["x^2", "x^3", "x"])

        gp = 1.0 / math.sqrt(3.0)
        mid = (a_val + b_val) / 2.0
        half = (b_val - a_val) / 2.0
        t1 = mid - half * gp
        t2 = mid + half * gp

        if fn_type == "x^2":
            f1 = t1 ** 2
            f2 = t2 ** 2
        elif fn_type == "x^3":
            f1 = t1 ** 3
            f2 = t2 ** 3
        else:
            f1 = t1
            f2 = t2

        integral = round(half * (f1 + f2), 4)
        t1 = round(t1, 4)
        t2 = round(t2, 4)
        f1 = round(f1, 4)
        f2 = round(f2, 4)

        problem = (
            f"Gauss-Legendre 2pt: integral of {fn_type} "
            f"from {a_val} to {b_val}"
        )
        return problem, {
            "fn": fn_type, "a": a_val, "b": b_val,
            "t1": t1, "t2": t2, "f1": f1, "f2": f2,
            "half": round(half, 4), "integral": integral,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Show quadrature computation.

        Args:
            sd: Solution data dict.

        Returns:
            Step strings.
        """
        return [
            f"transform [{sd['a']},{sd['b']}] to [-1,1]",
            f"Gauss points: t1={sd['t1']}, t2={sd['t2']}",
            f"f(t1)={sd['f1']}, f(t2)={sd['f2']}",
            f"integral = {sd['half']} * ({sd['f1']}+{sd['f2']}) = {sd['integral']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the quadrature result.

        Args:
            sd: Solution data dict.

        Returns:
            Integral approximation.
        """
        return f"{sd['integral']}"


@register
class AdamsBashforthGenerator(StepGenerator):
    """Solve an ODE using the 2-step Adams-Bashforth method.

    Applies y_{n+1} = y_n + h/2 * (3*f_n - f_{n-1}) for 2-3 steps
    after bootstrapping with Euler's method for the first step.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "adams_bashforth"

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
        return "Adams-Bashforth 2-step method"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an Adams-Bashforth problem.

        Args:
            difficulty: Controls step count.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        y0 = round(self._rng.uniform(0.5, 2.0), 2)
        h = round(self._rng.choice([0.1, 0.2, 0.25]), 2)
        ode = self._rng.choice(["y", "-y", "2*y"])
        n_steps = min(2 + difficulty // 3, 3)

        def f(y_val: float) -> float:
            """Evaluate the ODE right-hand side.

            Args:
                y_val: Current y value.

            Returns:
                f(y) value.
            """
            if ode == "y":
                return y_val
            if ode == "-y":
                return -y_val
            return 2.0 * y_val

        t = 0.0
        y = y0
        f_prev = f(y)
        y1 = y + h * f_prev
        t += h
        trace = [f"Euler bootstrap: y1={round(y1, 4)}"]

        f_curr = f(y1)
        y_prev = y
        y = y1
        for i in range(n_steps):
            y_new = y + h / 2.0 * (3 * f_curr - f_prev)
            y_new = round(y_new, 4)
            t_new = round(t + h, 4)
            trace.append(
                f"AB2 step {i + 1}: f_n={round(f_curr, 4)}, "
                f"f_{{n-1}}={round(f_prev, 4)}, y={y_new}"
            )
            f_prev = f_curr
            y = y_new
            f_curr = f(y)
            t = t_new

        problem = (
            f"dy/dt={ode}, y(0)={y0}, h={h}, "
            f"AB2 {n_steps} steps"
        )
        return problem, {
            "ode": ode, "y0": y0, "h": h,
            "trace": trace, "final_t": round(t, 4),
            "final_y": round(y, 4),
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Show Adams-Bashforth steps.

        Args:
            sd: Solution data dict.

        Returns:
            Step strings.
        """
        return sd["trace"]

    def _create_answer(self, sd: dict) -> str:
        """Return the final solution value.

        Args:
            sd: Solution data dict.

        Returns:
            Final y value at final t.
        """
        return f"y({sd['final_t']}) = {sd['final_y']}"


@register
class NewtonInterpolationGenerator(StepGenerator):
    """Interpolate using Newton's divided differences.

    Computes the divided difference table and evaluates
    P(x) = f[x0] + f[x0,x1]*(x-x0) + f[x0,x1,x2]*(x-x0)*(x-x1) + ...
    for 3-4 data points.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "newton_interpolation"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

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
        return "Newton divided difference interpolation"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Newton interpolation problem.

        Args:
            difficulty: Controls number of points.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        n_pts = 3 if difficulty <= 4 else 4
        x_pts = sorted(self._rng.sample(range(-4, 5), n_pts))
        y_pts = [self._rng.randint(-5, 5 + difficulty) for _ in range(n_pts)]

        table: list[list[float]] = [list(map(float, y_pts))]
        for order in range(1, n_pts):
            row: list[float] = []
            prev = table[order - 1]
            for i in range(len(prev) - 1):
                dd = (prev[i + 1] - prev[i]) / (x_pts[i + order] - x_pts[i])
                row.append(round(dd, 4))
            table.append(row)

        coeffs = [table[k][0] for k in range(n_pts)]

        x_eval = self._rng.choice(
            [v for v in range(-3, 4) if v not in x_pts]
        )
        result = 0.0
        product = 1.0
        for k in range(n_pts):
            result += coeffs[k] * product
            if k < n_pts - 1:
                product *= (x_eval - x_pts[k])
        result = round(result, 4)

        pts_str = ", ".join(
            f"({x_pts[i]},{y_pts[i]})" for i in range(n_pts)
        )
        problem = f"Newton interp: {pts_str}. P({x_eval})?"
        return problem, {
            "x_pts": x_pts, "y_pts": y_pts,
            "coeffs": [round(c, 4) for c in coeffs],
            "x_eval": x_eval, "result": result,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Show divided difference table and evaluation.

        Args:
            sd: Solution data dict.

        Returns:
            Step strings.
        """
        steps = [f"divided diff coefficients: {sd['coeffs']}"]
        terms = [f"f[x0]={sd['coeffs'][0]}"]
        for k in range(1, len(sd["coeffs"])):
            factors = "*".join(
                f"({sd['x_eval']}-{sd['x_pts'][j]})"
                for j in range(k)
            )
            terms.append(f"f[x0..x{k}]*{factors}")
        steps.append(f"P({sd['x_eval']}) = " + " + ".join(terms))
        steps.append(f"= {sd['result']}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the interpolated value.

        Args:
            sd: Solution data dict.

        Returns:
            P(x_eval).
        """
        return f"P({sd['x_eval']}) = {sd['result']}"


@register
class NumericalIntegrationErrorGenerator(StepGenerator):
    """Compare error bounds for trapezoidal and Simpson's rules.

    Trapezoidal error is O(h^2) and Simpson's error is O(h^4).
    Given step size h and second/fourth derivatives, estimates errors.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "numerical_integration_error"

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
        return "compare numerical integration errors"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an error comparison problem.

        Args:
            difficulty: Controls interval and h.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        a_val = 0
        b_val = self._rng.randint(1, 2 + difficulty)
        fn_type = self._rng.choice(["x^2", "x^3", "x^4"])
        n = self._rng.randint(2, min(8, 2 + difficulty * 2))
        h = round((b_val - a_val) / n, 4)

        if fn_type == "x^2":
            max_f2 = 2.0
            max_f4 = 0.0
        elif fn_type == "x^3":
            max_f2 = round(6.0 * b_val, 4)
            max_f4 = 0.0
        else:
            max_f2 = round(12.0 * b_val ** 2, 4)
            max_f4 = 24.0

        trap_bound = round(
            (b_val - a_val) * h ** 2 * max_f2 / 12.0, 4
        )
        if max_f4 > 0:
            simp_bound = round(
                (b_val - a_val) * h ** 4 * max_f4 / 180.0, 4
            )
        else:
            simp_bound = 0.0

        problem = (
            f"f(x)={fn_type}, [{a_val},{b_val}], n={n}, h={h}. "
            f"compare trap vs Simpson error bounds"
        )
        return problem, {
            "fn": fn_type, "a": a_val, "b": b_val,
            "n": n, "h": h,
            "max_f2": max_f2, "max_f4": max_f4,
            "trap_bound": trap_bound, "simp_bound": simp_bound,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Show error bound computations.

        Args:
            sd: Solution data dict.

        Returns:
            Step strings.
        """
        return [
            f"h = {sd['h']}",
            f"max|f''| = {sd['max_f2']}, max|f''''| = {sd['max_f4']}",
            f"trap error <= (b-a)*h^2*M2/12 = {sd['trap_bound']}",
            f"Simpson error <= (b-a)*h^4*M4/180 = {sd['simp_bound']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the error bounds.

        Args:
            sd: Solution data dict.

        Returns:
            Trapezoidal and Simpson error bounds.
        """
        return f"trap<={sd['trap_bound']}, Simpson<={sd['simp_bound']}"


@register
class EigenvaluePowerIterationGenerator(StepGenerator):
    """Find the dominant eigenvalue using power iteration.

    Iterates v_{k+1} = A*v_k, then eigenvalue ~ (A*v_k dot v_k)/(v_k dot v_k).
    Shows 3-5 iterations on a 2x2 matrix.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "eigenvalue_power_iteration"

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
        return "power iteration for eigenvalue"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a power iteration problem.

        Args:
            difficulty: Controls iteration count and matrix values.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        lam1 = self._rng.randint(3, 4 + difficulty)
        lam2 = self._rng.randint(1, lam1 - 1)
        off = self._rng.randint(0, min(2, difficulty // 2))
        a_mat = [[lam1 + off, off], [off, lam2 + off]]
        n_iter = min(3 + difficulty // 3, 5)

        v = [1.0, 1.0]
        trace: list[str] = []
        eigenvalue = 0.0
        for k in range(n_iter):
            av = [
                a_mat[0][0] * v[0] + a_mat[0][1] * v[1],
                a_mat[1][0] * v[0] + a_mat[1][1] * v[1],
            ]
            dot_av_v = av[0] * v[0] + av[1] * v[1]
            dot_v_v = v[0] * v[0] + v[1] * v[1]
            eigenvalue = round(dot_av_v / dot_v_v, 4)
            norm = math.sqrt(av[0] ** 2 + av[1] ** 2)
            if norm < 1e-12:
                break
            v = [round(av[0] / norm, 4), round(av[1] / norm, 4)]
            trace.append(
                f"iter {k + 1}: Av=[{round(av[0], 4)},{round(av[1], 4)}], "
                f"lambda={eigenvalue}, v=[{v[0]},{v[1]}]"
            )

        a_str = f"[[{a_mat[0][0]},{a_mat[0][1]}],[{a_mat[1][0]},{a_mat[1][1]}]]"
        problem = f"A={a_str}, v0=[1,1], {n_iter} power iterations"
        return problem, {
            "A": a_mat, "trace": trace,
            "eigenvalue": eigenvalue, "eigenvector": v,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Show power iteration steps.

        Args:
            sd: Solution data dict.

        Returns:
            Step strings.
        """
        return sd["trace"]

    def _create_answer(self, sd: dict) -> str:
        """Return the dominant eigenvalue approximation.

        Args:
            sd: Solution data dict.

        Returns:
            Eigenvalue and eigenvector.
        """
        return (
            f"lambda={sd['eigenvalue']}, "
            f"v=[{sd['eigenvector'][0]},{sd['eigenvector'][1]}]"
        )


@register
class NonlinearSystemGenerator(StepGenerator):
    """Solve a 2x2 nonlinear system using Newton's method.

    Computes the Jacobian, solves J*delta = -F, and updates the
    solution for 2-3 iterations.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "nonlinear_system"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

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
        return "Newton's method for nonlinear system"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a 2x2 nonlinear system problem.

        Uses f1(x,y) = x^2 + y^2 - r^2, f2(x,y) = x - a*y
        so the system has a clean solution.

        Args:
            difficulty: Controls iteration count and parameters.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        a_coeff = self._rng.randint(1, 2 + difficulty // 2)
        r_val = self._rng.randint(2, 4 + difficulty)
        n_iter = min(2 + difficulty // 3, 3)

        x = round(self._rng.uniform(r_val * 0.3, r_val * 0.9), 4)
        y = round(self._rng.uniform(r_val * 0.1, r_val * 0.5), 4)

        trace: list[str] = []
        for i in range(n_iter):
            f1 = x ** 2 + y ** 2 - r_val ** 2
            f2 = x - a_coeff * y
            j11 = 2 * x
            j12 = 2 * y
            j21 = 1.0
            j22 = -float(a_coeff)
            det = j11 * j22 - j12 * j21
            if abs(det) < 1e-12:
                break
            dx = round(-(j22 * f1 - j12 * f2) / det, 4)
            dy = round(-(-j21 * f1 + j11 * f2) / det, 4)
            x = round(x + dx, 4)
            y = round(y + dy, 4)
            trace.append(
                f"iter {i + 1}: F=[{round(f1, 4)},{round(f2, 4)}], "
                f"delta=[{dx},{dy}], x={x}, y={y}"
            )

        problem = (
            f"f1=x^2+y^2-{r_val ** 2}, f2=x-{a_coeff}y. "
            f"x0={trace[0].split('x=')[1].split(',')[0] if trace else x}, "
            f"Newton {n_iter} iterations"
        )
        return problem, {
            "r": r_val, "a": a_coeff,
            "trace": trace, "final_x": x, "final_y": y,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Show Newton iteration steps.

        Args:
            sd: Solution data dict.

        Returns:
            Step strings.
        """
        return sd["trace"]

    def _create_answer(self, sd: dict) -> str:
        """Return the solution approximation.

        Args:
            sd: Solution data dict.

        Returns:
            Final (x, y) values.
        """
        return f"x={sd['final_x']}, y={sd['final_y']}"
