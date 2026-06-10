"""Extended differential equations generators.

6 generators covering variation of parameters, Laplace transform
solutions, matrix ODE systems, boundary value problems, stability
analysis, and exact ODEs across tiers 5-6.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


# ===================================================================
# 1. VARIATION OF PARAMETERS (tier 6)
# ===================================================================

@register
class VariationOfParametersGenerator(StepGenerator):
    """Solve y'' + p*y' + q*y = g(x) by variation of parameters.

    Computes the Wronskian of the homogeneous solutions, then finds
    particular solution integrals u1 and u2. Uses constant-coefficient
    equations with simple forcing functions.

    Difficulty scaling:
        Difficulty 1-3: y'' + y = g(x) with simple g (e^x, sin).
        Difficulty 4-6: y'' + a*y' + b*y = g(x), exponential g.
        Difficulty 7-8: non-trivial coefficients, product forcing.

    Prerequisites:
        diff_equation (tier 6).
    """

    _PROBLEMS_EASY = [
        # (description, y1, y2, g, wronskian, u1_integrand, u2_integrand, particular)
        ("y'' + y = sec(x)", "cos(x)", "sin(x)", "sec(x)",
         "1", "-tan(x)", "1",
         "x*sin(x) + cos(x)*ln|cos(x)|"),
        ("y'' + y = e^x", "cos(x)", "sin(x)", "e^x",
         "1", "-e^x*sin(x)", "e^x*cos(x)",
         "e^x/2"),
        ("y'' - y = e^x", "e^x", "e^{-x}", "e^x",
         "-2", "-1/2", "e^{2x}/2",
         "x*e^x/2"),
    ]

    _PROBLEMS_MED = [
        ("y'' + 4y = sin(2x)", "cos(2x)", "sin(2x)", "sin(2x)",
         "2", "-sin^2(2x)/2", "sin(2x)*cos(2x)/2",
         "-x*cos(2x)/4"),
        ("y'' - 3y' + 2y = e^{3x}", "e^x", "e^{2x}", "e^{3x}",
         "e^{3x}", "-e^{2x}", "e^x",
         "e^{3x}/2"),
        ("y'' + y = tan(x)", "cos(x)", "sin(x)", "tan(x)",
         "1", "-sin^2(x)/cos(x)", "sin(x)",
         "-cos(x)*ln|sec(x)+tan(x)|"),
    ]

    _PROBLEMS_HARD = [
        ("y'' - 2y' + y = e^x/x", "e^x", "x*e^x", "e^x/x",
         "e^{2x}", "-1/x", "1/x^2",
         "x*e^x*ln|x|"),
        ("y'' + y = csc(x)", "cos(x)", "sin(x)", "csc(x)",
         "1", "-1", "cos(x)/sin(x)",
         "-x*cos(x) + sin(x)*ln|sin(x)|"),
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "variation_of_parameters"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["diff_equation"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls equation complexity.

        Returns:
            Task description string.
        """
        return "solve ODE by variation of parameters"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a variation of parameters problem.

        Args:
            difficulty: Controls equation complexity.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            pool = self._PROBLEMS_EASY
        elif difficulty <= 6:
            pool = self._PROBLEMS_EASY + self._PROBLEMS_MED
        else:
            pool = self._PROBLEMS_EASY + self._PROBLEMS_MED + self._PROBLEMS_HARD

        desc, y1, y2, g, W, u1_int, u2_int, yp = self._rng.choice(pool)
        problem = f"{desc}. Solve by variation of parameters."
        return problem, {
            "desc": desc, "y1": y1, "y2": y2, "g": g,
            "wronskian": W, "u1_integrand": u1_int,
            "u2_integrand": u2_int, "particular": yp,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate variation of parameters steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing the method.
        """
        return [
            f"homogeneous solutions: y1={data['y1']}, y2={data['y2']}",
            f"W(y1,y2) = {data['wronskian']}",
            f"u1' = -y2*g/W = {data['u1_integrand']}",
            f"u2' = y1*g/W = {data['u2_integrand']}",
            f"y_p = {data['particular']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the final answer.

        Args:
            data: Solution data.

        Returns:
            General solution string.
        """
        return (
            f"y = c1*{data['y1']} + c2*{data['y2']} + {data['particular']}"
        )


# ===================================================================
# 2. LAPLACE SOLVE ODE (tier 6)
# ===================================================================

@register
class LaplaceSolveOdeGenerator(StepGenerator):
    """Solve an initial value problem using Laplace transforms.

    Transforms the ODE into an algebraic equation in s-domain,
    solves for Y(s), then applies inverse Laplace to get y(t).

    Difficulty scaling:
        Difficulty 1-3: y' + a*y = b with y(0) given.
        Difficulty 4-6: y'' + a*y = 0 with y(0), y'(0) given.
        Difficulty 7-8: y'' + a*y' + b*y = f(t) with forcing.

    Prerequisites:
        diff_equation (tier 6).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "laplace_solve_ode"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["diff_equation"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls ODE complexity.

        Returns:
            Task description string.
        """
        return "solve IVP using Laplace transform"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Laplace transform IVP problem.

        Args:
            difficulty: Controls ODE complexity.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            a = self._rng.randint(1, 4)
            y0 = self._rng.randint(1, 5)
            problem = f"y' + {a}y = 0, y(0) = {y0}. Solve using Laplace."
            ys = f"{y0}/(s+{a})"
            sol = f"{y0}*e^(-{a}t)"
            return problem, {
                "ode": f"y' + {a}y = 0", "y0": y0, "yp0": None,
                "Ys": ys, "solution": sol,
                "transform_step": f"sY - {y0} + {a}Y = 0",
                "solve_step": f"Y(s+{a}) = {y0}",
            }
        elif difficulty <= 6:
            omega = self._rng.randint(1, 4)
            y0 = self._rng.randint(0, 3)
            yp0 = self._rng.randint(0, 3)
            omega2 = omega * omega
            problem = (
                f"y'' + {omega2}y = 0, y(0) = {y0}, y'(0) = {yp0}. "
                f"Solve using Laplace."
            )
            ys = f"({y0}*s + {yp0})/(s^2+{omega2})"
            parts = []
            if y0 != 0:
                parts.append(f"{y0}*cos({omega}t)")
            if yp0 != 0:
                parts.append(f"{yp0}/{omega}*sin({omega}t)")
            sol = " + ".join(parts) if parts else "0"
            return problem, {
                "ode": f"y'' + {omega2}y = 0",
                "y0": y0, "yp0": yp0,
                "Ys": ys, "solution": sol,
                "transform_step": f"s^2*Y - {y0}*s - {yp0} + {omega2}*Y = 0",
                "solve_step": f"Y(s^2+{omega2}) = {y0}*s + {yp0}",
            }
        else:
            a = self._rng.randint(1, 3)
            b = self._rng.randint(1, 4)
            y0 = self._rng.randint(1, 3)
            yp0 = 0
            problem = (
                f"y'' + {a}y' + {b}y = 0, y(0) = {y0}, y'(0) = {yp0}. "
                f"Solve using Laplace."
            )
            disc = a * a - 4 * b
            ys = f"{y0}*(s+{a})/(s^2+{a}s+{b})"
            if disc > 0:
                r1 = round((-a + math.sqrt(disc)) / 2, 4)
                r2 = round((-a - math.sqrt(disc)) / 2, 4)
                sol = f"c1*e^({r1}t) + c2*e^({r2}t)"
            elif disc == 0:
                r = round(-a / 2, 4)
                sol = f"{y0}*e^({r}t)*(1 + {round(-r * y0, 4)}t)"
            else:
                alpha = round(-a / 2, 4)
                beta = round(math.sqrt(-disc) / 2, 4)
                sol = f"e^({alpha}t)*({y0}*cos({beta}t) + c*sin({beta}t))"
            return problem, {
                "ode": f"y'' + {a}y' + {b}y = 0",
                "y0": y0, "yp0": yp0,
                "Ys": ys, "solution": sol,
                "transform_step": (
                    f"s^2*Y - {y0}*s - {yp0} + {a}*(sY - {y0}) + {b}*Y = 0"
                ),
                "solve_step": f"Y(s^2+{a}s+{b}) = {y0}*s + {y0 * a}",
            }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Laplace transform solution steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing the transform method.
        """
        steps = [
            f"take Laplace: {data['transform_step']}",
            f"solve for Y: {data['solve_step']}",
            f"Y(s) = {data['Ys']}",
            f"inverse Laplace: y(t) = {data['solution']}",
        ]
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the final answer.

        Args:
            data: Solution data.

        Returns:
            Solution y(t).
        """
        return f"y(t) = {data['solution']}"


# ===================================================================
# 3. SYSTEM ODE MATRIX (tier 6)
# ===================================================================

@register
class SystemOdeMatrixGenerator(StepGenerator):
    """Solve x' = Ax for 2x2 matrix A using eigenvalues and eigenvectors.

    Finds eigenvalues of A, computes eigenvectors, and writes the
    general solution as a linear combination of eigenvector-exponential
    terms.

    Difficulty scaling:
        Difficulty 1-3: diagonal or triangular A, integer eigenvalues.
        Difficulty 4-6: distinct real eigenvalues.
        Difficulty 7-8: complex eigenvalues, repeated eigenvalues.

    Prerequisites:
        eigenvalue (tier 4).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "system_ode_matrix"

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
            difficulty: Controls matrix complexity.

        Returns:
            Task description string.
        """
        return "solve x' = Ax for 2x2 matrix using eigenvalues"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a matrix ODE system problem.

        Args:
            difficulty: Controls matrix complexity.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            lam1 = self._rng.randint(-3, 3)
            lam2 = self._rng.randint(-3, 3)
            while lam2 == lam1:
                lam2 = self._rng.randint(-3, 3)
            a = [[lam1, 0], [0, lam2]]
            v1 = [1, 0]
            v2 = [0, 1]
            case = "real_distinct"
        elif difficulty <= 6:
            lam1 = self._rng.randint(-3, 3)
            lam2 = self._rng.randint(-3, 3)
            while lam2 == lam1:
                lam2 = self._rng.randint(-3, 3)
            k = self._rng.randint(1, 3)
            a = [[lam1, k], [0, lam2]]
            v1 = [1, 0]
            v2_y = 1
            v2_x = k / (lam2 - lam1) if lam2 != lam1 else 0
            v2 = [round(v2_x, 4), v2_y]
            case = "real_distinct"
        else:
            alpha = self._rng.randint(-2, 2)
            beta = self._rng.randint(1, 3)
            a = [[alpha, -beta], [beta, alpha]]
            lam1 = complex(alpha, beta)
            lam2 = complex(alpha, -beta)
            v1 = [1, round(-beta, 4)]
            v2 = [1, round(beta, 4)]
            case = "complex"

        a_str = f"[[{a[0][0]},{a[0][1]}],[{a[1][0]},{a[1][1]}]]"
        problem = f"x' = Ax, A = {a_str}. Find general solution."

        if case == "real_distinct":
            sol = (
                f"c1*{v1}*e^({lam1}t) + c2*{v2}*e^({lam2}t)"
            )
            eigenvalues = f"{lam1}, {lam2}"
        else:
            sol = (
                f"e^({alpha}t)*(c1*cos({beta}t) + c2*sin({beta}t)) [vector form]"
            )
            eigenvalues = f"{alpha}+{beta}i, {alpha}-{beta}i"

        return problem, {
            "matrix": a, "a_str": a_str, "case": case,
            "eigenvalues": eigenvalues,
            "v1": v1, "v2": v2,
            "lam1": str(lam1), "lam2": str(lam2),
            "solution": sol,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate matrix ODE solution steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing eigenvalue method.
        """
        steps = [
            f"A = {data['a_str']}",
            f"eigenvalues: {data['eigenvalues']}",
            f"eigenvector for lam1: {data['v1']}",
            f"eigenvector for lam2: {data['v2']}",
        ]
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the final answer.

        Args:
            data: Solution data.

        Returns:
            General solution.
        """
        return f"x(t) = {data['solution']}"


# ===================================================================
# 4. BOUNDARY VALUE (tier 6)
# ===================================================================

@register
class BoundaryValueGenerator(StepGenerator):
    """Solve a boundary value problem y'' = f with y(0)=a, y(L)=b.

    Uses direct integration for simple forcing functions f(x) = c
    (constant) or f(x) = k*x (linear). Integrates twice and applies
    boundary conditions to determine constants.

    Difficulty scaling:
        Difficulty 1-3: y'' = 0 (linear solution).
        Difficulty 4-6: y'' = c (constant, quadratic solution).
        Difficulty 7-8: y'' = k*x (cubic solution).

    Prerequisites:
        second_derivative (tier 3).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "boundary_value"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["second_derivative"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls forcing function complexity.

        Returns:
            Task description string.
        """
        return "solve boundary value problem by direct integration"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a boundary value problem.

        Args:
            difficulty: Controls forcing function complexity.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        big_l = self._rng.randint(1, 4)
        ya = self._rng.randint(0, 5)
        yb = self._rng.randint(0, 5)

        if difficulty <= 3:
            f_str = "0"
            # y'' = 0 => y = c1*x + c2
            # y(0)=ya => c2 = ya
            # y(L)=yb => c1*L + ya = yb => c1 = (yb-ya)/L
            c1 = round((yb - ya) / big_l, 4)
            c2 = ya
            sol = f"{c1}*x + {c2}"
            int_steps = [
                "y' = c1",
                f"y = c1*x + c2",
                f"y(0) = {ya} => c2 = {c2}",
                f"y({big_l}) = {yb} => c1 = {c1}",
            ]
        elif difficulty <= 6:
            c = self._rng.randint(1, 4)
            f_str = str(c)
            # y'' = c => y = c*x^2/2 + c1*x + c2
            # y(0)=ya => c2 = ya
            # y(L)=yb => c*L^2/2 + c1*L + ya = yb
            c2 = ya
            c1 = round((yb - ya - c * big_l ** 2 / 2) / big_l, 4)
            sol = f"{round(c / 2, 4)}*x^2 + {c1}*x + {c2}"
            int_steps = [
                f"y' = {c}*x + c1",
                f"y = {round(c / 2, 4)}*x^2 + c1*x + c2",
                f"y(0) = {ya} => c2 = {c2}",
                f"y({big_l}) = {yb} => c1 = {c1}",
            ]
        else:
            k = self._rng.randint(1, 3)
            f_str = f"{k}*x"
            # y'' = k*x => y = k*x^3/6 + c1*x + c2
            # y(0)=ya => c2 = ya
            # y(L)=yb => k*L^3/6 + c1*L + ya = yb
            c2 = ya
            c1 = round((yb - ya - k * big_l ** 3 / 6) / big_l, 4)
            coeff3 = round(k / 6, 4)
            sol = f"{coeff3}*x^3 + {c1}*x + {c2}"
            int_steps = [
                f"y' = {round(k / 2, 4)}*x^2 + c1",
                f"y = {coeff3}*x^3 + c1*x + c2",
                f"y(0) = {ya} => c2 = {c2}",
                f"y({big_l}) = {yb} => c1 = {c1}",
            ]

        problem = (
            f"y'' = {f_str}, y(0) = {ya}, y({big_l}) = {yb}. "
            f"Solve the BVP."
        )
        return problem, {
            "f_str": f_str, "L": big_l, "ya": ya, "yb": yb,
            "solution": sol, "int_steps": int_steps,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate boundary value problem steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing direct integration.
        """
        return data["int_steps"]

    def _create_answer(self, data: dict) -> str:
        """Return the final answer.

        Args:
            data: Solution data.

        Returns:
            Solution y(x).
        """
        return f"y(x) = {data['solution']}"


# ===================================================================
# 5. STABILITY ODE (tier 6)
# ===================================================================

@register
class StabilityOdeGenerator(StepGenerator):
    """Classify equilibrium stability of a linear ODE system.

    For x' = Ax with 2x2 A, classifies the origin as stable node,
    unstable node, saddle, stable spiral, unstable spiral, or center
    based on eigenvalues of A.

    Difficulty scaling:
        Difficulty 1-3: diagonal A, real eigenvalues.
        Difficulty 4-6: general real eigenvalues.
        Difficulty 7-8: complex eigenvalues, degenerate cases.

    Prerequisites:
        eigenvalue (tier 4).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "stability_ode"

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
            difficulty: Controls matrix complexity.

        Returns:
            Task description string.
        """
        return "classify equilibrium stability of x' = Ax"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a stability classification problem.

        Args:
            difficulty: Controls matrix complexity.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            lam1 = self._rng.choice([-3, -2, -1, 1, 2, 3])
            lam2 = self._rng.choice([-3, -2, -1, 1, 2, 3])
            a = [[lam1, 0], [0, lam2]]
            eigenvalues = f"{lam1}, {lam2}"
            case = "real"
        elif difficulty <= 6:
            lam1 = self._rng.randint(-4, 4)
            lam2 = self._rng.randint(-4, 4)
            while lam1 == 0 and lam2 == 0:
                lam1 = self._rng.randint(-4, 4)
            k = self._rng.randint(1, 3)
            a = [[lam1, k], [0, lam2]]
            eigenvalues = f"{lam1}, {lam2}"
            case = "real"
        else:
            alpha = self._rng.choice([-2, -1, 0, 1, 2])
            beta = self._rng.randint(1, 3)
            a = [[alpha, -beta], [beta, alpha]]
            eigenvalues = f"{alpha}+{beta}i, {alpha}-{beta}i"
            case = "complex"
            lam1 = alpha
            lam2 = alpha

        a_str = f"[[{a[0][0]},{a[0][1]}],[{a[1][0]},{a[1][1]}]]"

        if case == "real":
            if lam1 < 0 and lam2 < 0:
                classification = "stable node"
            elif lam1 > 0 and lam2 > 0:
                classification = "unstable node"
            elif (lam1 > 0 and lam2 < 0) or (lam1 < 0 and lam2 > 0):
                classification = "saddle (unstable)"
            elif lam1 == 0 or lam2 == 0:
                if lam1 + lam2 < 0:
                    classification = "stable (degenerate)"
                elif lam1 + lam2 > 0:
                    classification = "unstable (degenerate)"
                else:
                    classification = "center (marginally stable)"
            else:
                classification = "stable node"
        else:
            if alpha < 0:
                classification = "stable spiral"
            elif alpha > 0:
                classification = "unstable spiral"
            else:
                classification = "center (marginally stable)"

        problem = f"x' = Ax, A = {a_str}. Classify the equilibrium."
        return problem, {
            "a_str": a_str, "eigenvalues": eigenvalues,
            "case": case, "classification": classification,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate stability classification steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing eigenvalue analysis.
        """
        steps = [
            f"A = {data['a_str']}",
            f"eigenvalues: {data['eigenvalues']}",
        ]
        if data["case"] == "real":
            steps.append("both eigenvalues real")
        else:
            steps.append("complex conjugate eigenvalues")
        steps.append(f"classification: {data['classification']}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the final answer.

        Args:
            data: Solution data.

        Returns:
            Stability classification.
        """
        return data["classification"]


# ===================================================================
# 6. EXACT ODE (tier 5)
# ===================================================================

@register
class ExactOdeGenerator(StepGenerator):
    """Check if M*dx + N*dy = 0 is exact and solve if so.

    Verifies the exactness condition dM/dy = dN/dx. If exact, finds
    the potential function F(x,y) such that dF = M*dx + N*dy.

    Difficulty scaling:
        Difficulty 1-3: polynomial M and N of degree 1.
        Difficulty 4-6: polynomial M and N of degree 2.
        Difficulty 7-8: mixed polynomial/trig terms.

    Prerequisites:
        diff_equation (tier 6).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "exact_ode"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["diff_equation"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls coefficient complexity.

        Returns:
            Task description string.
        """
        return "check exactness and solve M*dx + N*dy = 0"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an exact ODE problem.

        Args:
            difficulty: Controls coefficient complexity.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            # F(x,y) = a*x*y + b*x + c*y => M = a*y + b, N = a*x + c
            a = self._rng.randint(1, 4)
            b = self._rng.randint(0, 3)
            c = self._rng.randint(0, 3)
            m_str = f"{a}y + {b}" if b else f"{a}y"
            n_str = f"{a}x + {c}" if c else f"{a}x"
            dm_dy = str(a)
            dn_dx = str(a)
            is_exact = True
            f_str = f"{a}xy + {b}x + {c}y"
        elif difficulty <= 6:
            # F(x,y) = a*x^2*y + b*x*y^2 => M = 2a*x*y + b*y^2, N = a*x^2 + 2b*x*y
            a = self._rng.randint(1, 3)
            b = self._rng.randint(1, 3)
            m_str = f"{2 * a}xy + {b}y^2"
            n_str = f"{a}x^2 + {2 * b}xy"
            dm_dy = f"{2 * a}x + {2 * b}y"
            dn_dx = f"{2 * a}x + {2 * b}y"
            is_exact = True
            f_str = f"{a}x^2*y + {b}x*y^2"
        else:
            choice = self._rng.choice(["exact_cubic", "non_exact"])
            if choice == "exact_cubic":
                a = self._rng.randint(1, 2)
                # F = a*x^2*y + a*y^3/3
                m_str = f"{2 * a}xy"
                n_str = f"{a}x^2 + {a}y^2"
                dm_dy = f"{2 * a}x"
                dn_dx = f"{2 * a}x"
                is_exact = True
                f_str = f"{a}x^2*y + {a}y^3/3"
            else:
                p = self._rng.randint(1, 3)
                q = self._rng.randint(1, 3)
                m_str = f"{p}y"
                n_str = f"{q}x"
                dm_dy = str(p)
                dn_dx = str(q)
                is_exact = (p == q)
                f_str = f"{p}xy" if is_exact else "N/A"

        problem = f"({m_str})dx + ({n_str})dy = 0. Check exactness and solve."
        return problem, {
            "M": m_str, "N": n_str,
            "dM_dy": dm_dy, "dN_dx": dn_dx,
            "is_exact": is_exact, "F": f_str,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate exact ODE steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing exactness check and solution.
        """
        steps = [
            f"M = {data['M']}, N = {data['N']}",
            f"dM/dy = {data['dM_dy']}",
            f"dN/dx = {data['dN_dx']}",
        ]
        if data["is_exact"]:
            steps.append("dM/dy = dN/dx => exact")
            steps.append(f"F(x,y) = {data['F']}")
        else:
            steps.append("dM/dy != dN/dx => not exact")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the final answer.

        Args:
            data: Solution data.

        Returns:
            Potential function or not-exact indication.
        """
        if data["is_exact"]:
            return f"exact: F(x,y) = {data['F']} = C"
        return "not exact"
