"""Extended partial differential equation generators for tiers 6-7.

Provides 8 generators covering the Poisson equation, Helmholtz equation,
advection equation, Burgers equation, boundary condition classification,
eigenfunction expansion, Crank-Nicolson scheme, and variational PDE
formulation (Euler-Lagrange).
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


# ── Formatting helpers ────────────────────────────────────────────────


def _fmt(val: float) -> str:
    """Format a float to 4 decimal places, stripping trailing zeros.

    Args:
        val: Value to format.

    Returns:
        Formatted string.
    """
    return f"{round(val, 4):.4f}".rstrip("0").rstrip(".")


# ── 1. Poisson equation (tier 6) ────────────────────────────────────


@register
class PoissonEquationGenerator(StepGenerator):
    """Solve the Poisson equation u_xx + u_yy = f for simple source terms.

    Finds a particular solution for polynomial or constant f, then
    adds the homogeneous solution. Evaluates at a given point.

    Input format:
        ``solve Poisson equation``

    Target format:
        ``u_xx + u_yy = -2, u(0,y)=u(1,y)=u(x,0)=u(x,1)=0 <step>
        particular: u_p = (x-x^2)/2 + (y-y^2)/2 ??? too complex
        <step> use separation approach on rectangle <step> ...``

    Difficulty scaling:
        Difficulty 1-3: f = constant, rectangle, separation.
        Difficulty 4-6: f = ax + b, superposition.
        Difficulty 7-8: f = polynomial in x and y.

    Prerequisites:
        partial_derivative (tier 4).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "poisson_equation"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["partial_derivative"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls source term complexity.

        Returns:
            Natural language description.
        """
        return "solve Poisson equation"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Poisson equation problem.

        For u_xx + u_yy = c on [0,L]x[0,L] with zero BCs, the
        particular solution u_p = c*(x^2+y^2)/4 doesn't satisfy BCs.
        Instead we use a known particular + Fourier correction, but
        for training we focus on the template: identify f, find u_p
        satisfying u_p_xx + u_p_yy = f, then note correction needed.

        Args:
            difficulty: Controls source term type.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            return self._const_source(difficulty)
        if difficulty <= 6:
            return self._linear_source(difficulty)
        return self._quadratic_source(difficulty)

    def _const_source(self, difficulty: int) -> tuple[str, dict]:
        """Generate Poisson with constant source.

        u_xx + u_yy = c. Particular: u_p = c*x*(1-x)/2 satisfies
        u_p_xx = -c. Then u_yy part needs correction (homogeneous).

        Args:
            difficulty: Controls c.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        c = self._rng.randint(-4, -1)
        big_l = self._rng.randint(1, 2)
        x0 = round(big_l * 0.5, 4)
        y0 = round(big_l * 0.5, 4)
        # Particular solution u_p = c*x*(L-x)/(2L^2) + c*y*(L-y)/(2L^2)
        # Then u_p_xx + u_p_yy = c/L^2 + c/L^2 => need to adjust
        # Simpler: u_p = (c/4)*(x^2 + y^2) satisfies nabla^2 u_p = c
        up_val = (c / 4.0) * (x0 ** 2 + y0 ** 2)
        problem = (f"\\nabla^2 u = {c} on [0,{big_l}]^2, "
                   f"zero boundary conditions")
        return problem, {
            "source": f"{c}", "L": big_l,
            "particular": f"u_p = ({c}/4)(x^2+y^2)",
            "up_check": f"u_p_xx + u_p_yy = {c/2}+{c/2} = {c}",
            "x0": x0, "y0": y0,
            "up_val": up_val,
            "note": "homogeneous correction needed for BCs",
        }

    def _linear_source(self, difficulty: int) -> tuple[str, dict]:
        """Generate Poisson with f = ax.

        Particular: u_p = a*x^3/6 satisfies u_p_xx = ax. u_p_yy = 0.

        Args:
            difficulty: Controls a.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        a = self._rng.randint(1, 4)
        big_l = 1
        x0 = round(self._rng.choice([0.25, 0.5, 0.75]), 4)
        y0 = round(self._rng.choice([0.25, 0.5, 0.75]), 4)
        up_val = a * x0 ** 3 / 6.0
        problem = (f"\\nabla^2 u = {a}x on [0,{big_l}]^2, "
                   f"zero boundary conditions")
        return problem, {
            "source": f"{a}x", "L": big_l,
            "particular": f"u_p = {a}x^3/6",
            "up_check": f"u_p_xx = {a}x, u_p_yy = 0, sum = {a}x",
            "x0": x0, "y0": y0,
            "up_val": up_val,
            "note": "homogeneous correction for boundary conditions",
        }

    def _quadratic_source(self, difficulty: int) -> tuple[str, dict]:
        """Generate Poisson with f = a(x^2 + y^2).

        Particular: u_p = a(x^4 + y^4)/12.
        u_p_xx = a*x^2, u_p_yy = a*y^2, sum = a(x^2+y^2).

        Args:
            difficulty: Controls a.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        a = self._rng.randint(1, 3)
        big_l = 1
        x0 = round(self._rng.choice([0.25, 0.5, 0.75]), 4)
        y0 = round(self._rng.choice([0.25, 0.5, 0.75]), 4)
        up_val = a * (x0 ** 4 + y0 ** 4) / 12.0
        problem = (f"\\nabla^2 u = {a}(x^2+y^2) on [0,{big_l}]^2, "
                   f"zero BCs")
        return problem, {
            "source": f"{a}(x^2+y^2)", "L": big_l,
            "particular": f"u_p = {a}(x^4+y^4)/12",
            "up_check": (f"u_p_xx = {a}x^2, u_p_yy = {a}y^2, "
                         f"sum = {a}(x^2+y^2)"),
            "x0": x0, "y0": y0,
            "up_val": up_val,
            "note": "homogeneous correction for boundary conditions",
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Poisson equation solution steps.

        Args:
            data: Solution data with particular solution.

        Returns:
            Steps showing source, particular, and verification.
        """
        return [
            f"source: f = {data['source']}",
            f"particular: {data['particular']}",
            f"verify: {data['up_check']}",
            f"u_p({_fmt(data['x0'])},{_fmt(data['y0'])}) = {_fmt(data['up_val'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the particular solution evaluation.

        Args:
            data: Solution data.

        Returns:
            Particular solution value and note.
        """
        return (f"u_p = {_fmt(data['up_val'])} "
                f"({data['note']})")


# ── 2. Helmholtz equation (tier 6) ──────────────────────────────────


@register
class HelmholtzEquationGenerator(StepGenerator):
    """Solve the Helmholtz equation by separation of variables.

    Solves (nabla^2 + k^2)*u = 0 on a rectangle [0,a]x[0,b] with
    zero boundary conditions. Finds eigenvalues k_{mn}.

    Input format:
        ``solve Helmholtz equation on rectangle``

    Target format:
        ``(nabla^2 + k^2)u = 0 on [0,2]x[0,3] <step>
        u = sin(m*pi*x/2)*sin(n*pi*y/3) <step>
        k_{mn}^2 = (m*pi/2)^2 + (n*pi/3)^2 <step>
        k_{11}^2 = (pi/2)^2 + (pi/3)^2 = 3.5586``

    Difficulty scaling:
        Difficulty 1-3: small a, b, first few modes.
        Difficulty 4-6: moderate a, b, more modes.
        Difficulty 7-8: larger domain, higher modes.

    Prerequisites:
        heat_equation (tier 6).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "helmholtz_equation"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["heat_equation"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls domain and mode count.

        Returns:
            Natural language description.
        """
        return "solve Helmholtz equation on rectangle"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Helmholtz equation problem.

        Args:
            difficulty: Controls domain size and number of modes.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            a = self._rng.choice([1, 2])
            b = self._rng.choice([1, 2])
            n_modes = 2
        elif difficulty <= 6:
            a = self._rng.choice([1, 2, 3])
            b = self._rng.choice([1, 2, 3])
            n_modes = 3
        else:
            a = self._rng.choice([2, 3, 4])
            b = self._rng.choice([2, 3, 4])
            n_modes = 4

        modes = []
        for m in range(1, n_modes + 1):
            for n in range(1, n_modes + 1):
                k_sq = (m * math.pi / a) ** 2 + (n * math.pi / b) ** 2
                modes.append({"m": m, "n": n, "k_sq": k_sq})
                if len(modes) >= n_modes:
                    break
            if len(modes) >= n_modes:
                break

        problem = (f"(\\nabla^2 + k^2)u = 0 on "
                   f"[0,{a}]\\times[0,{b}], u=0 on boundary")
        return problem, {
            "a": a, "b": b, "modes": modes,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Helmholtz equation solution steps.

        Args:
            data: Solution data with eigenvalues.

        Returns:
            Steps showing eigenfunctions and eigenvalues.
        """
        steps = [
            f"u_{{mn}} = \\sin(m\\pi x/{data['a']})\\sin(n\\pi y/{data['b']})",
        ]
        for mode in data["modes"]:
            m, n = mode["m"], mode["n"]
            steps.append(
                f"k_{{{m}{n}}}^2 = "
                f"({m}pi/{data['a']})^2 + ({n}pi/{data['b']})^2 "
                f"= {_fmt(mode['k_sq'])}"
            )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the first eigenvalue.

        Args:
            data: Solution data.

        Returns:
            First eigenvalue k_11^2.
        """
        return f"k_11^2 = {_fmt(data['modes'][0]['k_sq'])}"


# ── 3. Advection equation (tier 6) ──────────────────────────────────


@register
class AdvectionEquationGenerator(StepGenerator):
    """Solve the advection equation u_t + c*u_x = 0.

    The solution is u(x,t) = f(x - c*t) where f is the initial
    condition. Evaluates at a given (x, t).

    Input format:
        ``solve advection equation``

    Target format:
        ``u_t + 2*u_x = 0, u(x,0) = sin(pi*x) <step>
        solution: u(x,t) = sin(pi*(x-2t)) <step>
        u(1, 0.5) = sin(pi*(1-1)) = 0``

    Difficulty scaling:
        Difficulty 1-3: f(x) = ax, small c.
        Difficulty 4-6: f(x) = sin(pi*x), moderate c.
        Difficulty 7-8: f(x) = exp(-x^2), larger c.

    Prerequisites:
        partial_derivative (tier 4).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "advection_equation"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["partial_derivative"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls IC and wave speed.

        Returns:
            Natural language description.
        """
        return "solve advection equation"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an advection equation problem.

        Args:
            difficulty: Controls IC type and wave speed.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            return self._linear_ic(difficulty)
        if difficulty <= 6:
            return self._sin_ic(difficulty)
        return self._gaussian_ic(difficulty)

    def _linear_ic(self, difficulty: int) -> tuple[str, dict]:
        """Generate advection with f(x) = ax.

        Args:
            difficulty: Controls parameters.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        a = self._rng.randint(1, 4)
        c = self._rng.randint(1, 3)
        x0 = round(self._rng.choice([1.0, 2.0, 3.0]), 2)
        t0 = round(self._rng.choice([0.5, 1.0]), 2)
        xi = x0 - c * t0
        u_val = a * xi
        problem = f"u_t + {c}u_x = 0, u(x,0) = {a}x"
        return problem, {
            "c": c, "ic": f"{a}x", "x0": x0, "t0": t0,
            "xi": xi, "u_val": u_val,
        }

    def _sin_ic(self, difficulty: int) -> tuple[str, dict]:
        """Generate advection with f(x) = sin(pi*x).

        Args:
            difficulty: Controls wave speed.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        c = self._rng.randint(1, 4)
        x0 = round(self._rng.choice([0.5, 1.0, 1.5]), 2)
        t0 = round(self._rng.choice([0.25, 0.5, 1.0]), 2)
        xi = x0 - c * t0
        u_val = math.sin(math.pi * xi)
        problem = f"u_t + {c}u_x = 0, u(x,0) = \\sin(\\pi x)"
        return problem, {
            "c": c, "ic": "sin(pi*x)", "x0": x0, "t0": t0,
            "xi": xi, "u_val": u_val,
        }

    def _gaussian_ic(self, difficulty: int) -> tuple[str, dict]:
        """Generate advection with f(x) = exp(-x^2).

        Args:
            difficulty: Controls wave speed.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        c = self._rng.randint(2, 5)
        x0 = round(self._rng.choice([1.0, 2.0, 3.0]), 2)
        t0 = round(self._rng.choice([0.5, 1.0]), 2)
        xi = x0 - c * t0
        u_val = math.exp(-xi * xi)
        problem = f"u_t + {c}u_x = 0, u(x,0) = e^{{-x^2}}"
        return problem, {
            "c": c, "ic": "exp(-x^2)", "x0": x0, "t0": t0,
            "xi": xi, "u_val": u_val,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate advection equation solution steps.

        Args:
            data: Solution data with characteristic and evaluation.

        Returns:
            Steps showing characteristic and evaluation.
        """
        return [
            f"u(x,t) = f(x - {data['c']}t)",
            f"xi = {_fmt(data['x0'])} - {data['c']}*{_fmt(data['t0'])} = {_fmt(data['xi'])}",
            f"u = f({_fmt(data['xi'])}) = {_fmt(data['u_val'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the solution value.

        Args:
            data: Solution data.

        Returns:
            Formatted u(x, t).
        """
        return f"u({_fmt(data['x0'])},{_fmt(data['t0'])}) = {_fmt(data['u_val'])}"


# ── 4. Burgers equation (tier 7) ────────────────────────────────────


@register
class BurgersEquationGenerator(StepGenerator):
    """Analyse the inviscid Burgers equation u_t + u*u_x = 0.

    For a shock wave with left state u_L and right state u_R, the
    Rankine-Hugoniot shock speed is s = (u_L + u_R) / 2.

    Input format:
        ``find shock speed for Burgers equation``

    Target format:
        ``u_t + u*u_x = 0, u_L = 3, u_R = 1 <step>
        Rankine-Hugoniot: s = (u_L + u_R)/2
        <step> s = (3+1)/2 = 2 <step> shock at x = 2*t``

    Difficulty scaling:
        Difficulty 1-3: integer u_L > u_R.
        Difficulty 4-6: u_L, u_R with fractions.
        Difficulty 7-8: evaluate u at given (x,t) relative to shock.

    Prerequisites:
        wave_equation_1d (tier 6).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "burgers_equation"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["wave_equation_1d"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls parameter complexity.

        Returns:
            Natural language description.
        """
        return "find shock speed for Burgers equation"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Burgers equation shock problem.

        Args:
            difficulty: Controls u_L, u_R values.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            u_l = self._rng.randint(2, 6)
            u_r = self._rng.randint(0, u_l - 1)
        elif difficulty <= 6:
            u_l = self._rng.randint(1, 5)
            u_r = round(self._rng.choice([0.5, 1.0, 1.5]), 1)
            if u_r >= u_l:
                u_r = round(u_l / 2.0, 1)
        else:
            u_l = self._rng.randint(3, 8)
            u_r = self._rng.randint(0, u_l - 1)

        shock_speed = (u_l + u_r) / 2.0

        # For higher difficulty, evaluate at a point
        t0 = round(self._rng.choice([0.5, 1.0, 2.0]), 1)
        x0 = round(self._rng.choice([1.0, 2.0, 3.0, 4.0]), 1)
        shock_pos = shock_speed * t0
        if x0 < shock_pos:
            u_at_point = u_l
        else:
            u_at_point = u_r

        problem = (f"u_t + u \\cdot u_x = 0, "
                   f"u_L = {_fmt(u_l)}, u_R = {_fmt(u_r)}")
        return problem, {
            "u_l": u_l, "u_r": u_r,
            "shock_speed": shock_speed,
            "t0": t0, "x0": x0,
            "shock_pos": shock_pos,
            "u_at_point": u_at_point,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Burgers equation solution steps.

        Args:
            data: Solution data with shock speed.

        Returns:
            Steps showing Rankine-Hugoniot and evaluation.
        """
        return [
            "Rankine-Hugoniot: s = (u_L + u_R)/2",
            (f"s = ({_fmt(data['u_l'])} + {_fmt(data['u_r'])})/2 "
             f"= {_fmt(data['shock_speed'])}"),
            (f"at t={_fmt(data['t0'])}: shock at "
             f"x = {_fmt(data['shock_pos'])}"),
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the shock speed.

        Args:
            data: Solution data.

        Returns:
            Shock speed value.
        """
        return f"s = {_fmt(data['shock_speed'])}"


# ── 5. Boundary conditions classification (tier 6) ──────────────────


@register
class BoundaryConditionsPDEGenerator(StepGenerator):
    """Classify and apply PDE boundary conditions.

    Identifies boundary conditions as Dirichlet (u = g), Neumann
    (du/dn = g), or Robin (au + b*du/dn = g), and sets up the
    corresponding problem for the heat or wave equation.

    Input format:
        ``classify and apply PDE boundary conditions``

    Target format:
        ``u_t = k*u_xx, u(0,t) = 0, u_x(L,t) = 0 <step>
        x=0: Dirichlet (u=0) <step> x=L: Neumann (u_x=0)
        <step> eigenfunctions: sin((2n-1)*pi*x/(2L))``

    Difficulty scaling:
        Difficulty 1-3: both Dirichlet, heat equation.
        Difficulty 4-6: mixed Dirichlet/Neumann.
        Difficulty 7-8: Robin boundary condition.

    Prerequisites:
        heat_equation (tier 6).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "boundary_conditions_pde"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["heat_equation"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls BC type.

        Returns:
            Natural language description.
        """
        return "classify and apply PDE boundary conditions"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a boundary condition classification problem.

        Args:
            difficulty: Controls BC type.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            return self._dirichlet_both(difficulty)
        if difficulty <= 6:
            return self._mixed_dn(difficulty)
        return self._robin_bc(difficulty)

    def _dirichlet_both(self, difficulty: int) -> tuple[str, dict]:
        """Generate both-Dirichlet BCs for heat equation.

        u(0,t) = 0, u(L,t) = 0 => sin(n*pi*x/L) eigenfunctions.

        Args:
            difficulty: Controls L.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        k = self._rng.randint(1, 3)
        big_l = self._rng.randint(1, 3)
        lam1 = k * (math.pi / big_l) ** 2
        problem = (f"u_t = {k}u_{{xx}} on [0,{big_l}], "
                   f"u(0,t) = 0, u({big_l},t) = 0")
        return problem, {
            "pde": "heat", "k": k, "L": big_l,
            "bc_left": "Dirichlet: u(0,t) = 0",
            "bc_right": f"Dirichlet: u({big_l},t) = 0",
            "eigenfunc": f"sin(n*pi*x/{big_l})",
            "lambda_1": lam1,
        }

    def _mixed_dn(self, difficulty: int) -> tuple[str, dict]:
        """Generate mixed Dirichlet-Neumann BCs.

        u(0,t) = 0, u_x(L,t) = 0 => sin((2n-1)*pi*x/(2L)).

        Args:
            difficulty: Controls L and k.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        k = self._rng.randint(1, 3)
        big_l = self._rng.randint(1, 2)
        lam1 = k * (math.pi / (2 * big_l)) ** 2
        problem = (f"u_t = {k}u_{{xx}} on [0,{big_l}], "
                   f"u(0,t) = 0, u_x({big_l},t) = 0")
        return problem, {
            "pde": "heat", "k": k, "L": big_l,
            "bc_left": "Dirichlet: u(0,t) = 0",
            "bc_right": f"Neumann: u_x({big_l},t) = 0",
            "eigenfunc": f"sin((2n-1)*pi*x/(2*{big_l}))",
            "lambda_1": lam1,
        }

    def _robin_bc(self, difficulty: int) -> tuple[str, dict]:
        """Generate Robin boundary condition.

        u(0,t) = 0, a*u(L,t) + u_x(L,t) = 0.

        Args:
            difficulty: Controls parameters.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        k = self._rng.randint(1, 3)
        big_l = self._rng.randint(1, 2)
        h = self._rng.randint(1, 3)
        problem = (f"u_t = {k}u_{{xx}} on [0,{big_l}], "
                   f"u(0,t) = 0, {h}u({big_l},t) + u_x({big_l},t) = 0")
        return problem, {
            "pde": "heat", "k": k, "L": big_l, "h": h,
            "bc_left": "Dirichlet: u(0,t) = 0",
            "bc_right": f"Robin: {h}u + u_x = 0 at x={big_l}",
            "eigenfunc": "sin(mu_n*x) where mu_n*cos(mu_n*L)+h*sin(mu_n*L)=0",
            "lambda_1": 0.0,  # transcendental
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate BC classification steps.

        Args:
            data: Solution data with BC types and eigenfunctions.

        Returns:
            Steps showing classification and eigenfunctions.
        """
        steps = [
            f"left: {data['bc_left']}",
            f"right: {data['bc_right']}",
            f"eigenfunctions: {data['eigenfunc']}",
        ]
        if data["lambda_1"] > 0:
            steps.append(f"lambda_1 = {_fmt(data['lambda_1'])}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the BC classification and eigenfunction form.

        Args:
            data: Solution data.

        Returns:
            Classification summary.
        """
        return f"phi_n(x) = {data['eigenfunc']}"


# ── 6. Eigenfunction expansion (tier 6) ─────────────────────────────


@register
class EigenfunctionExpansionGenerator(StepGenerator):
    """Expand a solution in eigenfunctions and find Fourier coefficients.

    For u(x,t) = sum c_n * phi_n(x) * T_n(t), finds the first
    few c_n from the initial condition by computing inner products.

    Input format:
        ``find eigenfunction expansion coefficients``

    Target format:
        ``u(x,0) = x(1-x) on [0,1], phi_n = sin(n*pi*x) <step>
        c_n = 2*int_0^1 x(1-x)*sin(n*pi*x) dx <step>
        c_1 = 8/(pi^3) = 0.2580
        <step> c_2 = 0, c_3 = 8/(27*pi^3)``

    Difficulty scaling:
        Difficulty 1-3: u(x,0) = constant, 2 terms.
        Difficulty 4-6: u(x,0) = x(L-x), 3 terms.
        Difficulty 7-8: u(x,0) = piecewise linear, 3 terms.

    Prerequisites:
        fourier_coefficient (tier 6).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "eigenfunction_expansion"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["fourier_coefficient"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls IC and number of terms.

        Returns:
            Natural language description.
        """
        return "find eigenfunction expansion coefficients"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an eigenfunction expansion problem.

        Args:
            difficulty: Controls IC type and number of coefficients.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            return self._const_ic(difficulty)
        if difficulty <= 6:
            return self._parabolic_ic(difficulty)
        return self._linear_ic(difficulty)

    def _const_ic(self, difficulty: int) -> tuple[str, dict]:
        """Generate expansion of constant IC.

        u(x,0) = A on [0,L]. c_n = (2A/L)*int_0^L sin(n*pi*x/L) dx
        = 2A*(1-cos(n*pi))/(n*pi) = 4A/(n*pi) for odd n, 0 for even.

        Args:
            difficulty: Controls A and L.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        a_val = self._rng.randint(1, 4)
        big_l = self._rng.randint(1, 2)
        n_terms = 2
        coeffs = []
        for n in range(1, n_terms + 1):
            if n % 2 == 1:
                c_n = 4.0 * a_val / (n * math.pi)
            else:
                c_n = 0.0
            coeffs.append({"n": n, "c_n": c_n})
        problem = f"u(x,0) = {a_val} on [0,{big_l}], phi_n = \\sin(n\\pi x/{big_l})"
        return problem, {
            "ic": f"{a_val}", "L": big_l,
            "coeffs": coeffs,
        }

    def _parabolic_ic(self, difficulty: int) -> tuple[str, dict]:
        """Generate expansion of u(x,0) = x(1-x) on [0,1].

        c_n = 2*int_0^1 x(1-x)*sin(n*pi*x) dx.
        = 8/(n^3*pi^3) for odd n, 0 for even n.

        Args:
            difficulty: Unused but required.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        n_terms = 3
        coeffs = []
        for n in range(1, n_terms + 1):
            if n % 2 == 1:
                c_n = 8.0 / (n ** 3 * math.pi ** 3)
            else:
                c_n = 0.0
            coeffs.append({"n": n, "c_n": c_n})
        problem = "u(x,0) = x(1-x) on [0,1], phi_n = \\sin(n\\pi x)"
        return problem, {
            "ic": "x(1-x)", "L": 1,
            "coeffs": coeffs,
        }

    def _linear_ic(self, difficulty: int) -> tuple[str, dict]:
        """Generate expansion of u(x,0) = x on [0,1].

        c_n = 2*int_0^1 x*sin(n*pi*x) dx = -2*cos(n*pi)/(n*pi)
        = 2*(-1)^{n+1}/(n*pi).

        Args:
            difficulty: Unused but required.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        n_terms = 3
        coeffs = []
        for n in range(1, n_terms + 1):
            c_n = 2.0 * ((-1) ** (n + 1)) / (n * math.pi)
            coeffs.append({"n": n, "c_n": c_n})
        problem = "u(x,0) = x on [0,1], phi_n = \\sin(n\\pi x)"
        return problem, {
            "ic": "x", "L": 1,
            "coeffs": coeffs,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate eigenfunction expansion steps.

        Args:
            data: Solution data with coefficients.

        Returns:
            Steps showing coefficient computation.
        """
        steps = [f"u(x,0) = {data['ic']} on [0,{data['L']}]"]
        for coeff in data["coeffs"]:
            steps.append(
                f"c_{coeff['n']} = {_fmt(coeff['c_n'])}"
            )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the Fourier coefficients.

        Args:
            data: Solution data.

        Returns:
            Formatted coefficients.
        """
        parts = [f"c_{c['n']}={_fmt(c['c_n'])}" for c in data["coeffs"]]
        return ", ".join(parts)


# ── 7. Crank-Nicolson scheme (tier 6) ───────────────────────────────


@register
class CrankNicolsonGenerator(StepGenerator):
    """Set up the Crank-Nicolson semi-implicit scheme for the heat equation.

    The scheme averages the explicit and implicit discretisations:
    (u^{n+1}_j - u^n_j)/dt = (D(u^{n+1}) + D(u^n))/2, where
    D is the second-order central difference operator.

    Input format:
        ``set up Crank-Nicolson scheme``

    Target format:
        ``u_t = k*u_xx, dx=0.25, dt=0.1, k=1 <step>
        r = k*dt/dx^2 = 1.6 <step>
        -r/2*u^{n+1}_{j-1} + (1+r)*u^{n+1}_j - r/2*u^{n+1}_{j+1}
        = r/2*u^n_{j-1} + (1-r)*u^n_j + r/2*u^n_{j+1} <step>
        tridiagonal system with diag = 1+r, off-diag = -r/2``

    Difficulty scaling:
        Difficulty 1-3: small grid (2-3 interior points).
        Difficulty 4-6: medium grid (3-4 points), compute RHS.
        Difficulty 7-8: larger grid, one time step evaluation.

    Prerequisites:
        finite_difference (tier 6).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "crank_nicolson"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["finite_difference"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls grid size.

        Returns:
            Natural language description.
        """
        return "set up Crank-Nicolson scheme"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Crank-Nicolson scheme problem.

        Args:
            difficulty: Controls grid size and parameters.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            n = self._rng.choice([2, 3])
            k = self._rng.choice([1, 2])
        elif difficulty <= 6:
            n = self._rng.choice([3, 4])
            k = self._rng.choice([1, 2, 3])
        else:
            n = self._rng.choice([4, 5])
            k = self._rng.choice([1, 2])

        dx = 1.0 / (n + 1)
        dt = round(self._rng.choice([0.01, 0.05, 0.1]), 4)
        r = k * dt / (dx * dx)

        # Set up initial condition u^0_j = sin(pi*x_j)
        grid = [round((j + 1) * dx, 4) for j in range(n)]
        u0 = [round(math.sin(math.pi * x), 4) for x in grid]

        # Compute RHS for one step: r/2*u_{j-1} + (1-r)*u_j + r/2*u_{j+1}
        rhs = []
        for j in range(n):
            left = u0[j - 1] if j > 0 else 0.0
            right = u0[j + 1] if j < n - 1 else 0.0
            val = (r / 2.0) * left + (1 - r) * u0[j] + (r / 2.0) * right
            rhs.append(round(val, 4))

        # Solve tridiagonal: (-r/2, 1+r, -r/2) * u^{n+1} = rhs
        diag = 1 + r
        off = -r / 2.0
        u1 = self._solve_tridiag(n, diag, off, rhs)

        problem = f"u_t = {k}u_{{xx}}, dx={_fmt(dx)}, dt={_fmt(dt)}"
        return problem, {
            "k": k, "n": n, "dx": dx, "dt": dt, "r": r,
            "diag": diag, "off": off,
            "grid": grid, "u0": u0, "rhs": rhs, "u1": u1,
        }

    def _solve_tridiag(self, n: int, diag: float, off: float,
                       rhs: list[float]) -> list[float]:
        """Solve tridiagonal system with constant coefficients.

        Args:
            n: System size.
            diag: Main diagonal value.
            off: Off-diagonal value.
            rhs: Right-hand side vector.

        Returns:
            Solution vector.
        """
        b = [diag] * n
        d = list(rhs)
        for i in range(1, n):
            m = off / b[i - 1]
            b[i] -= m * off
            d[i] -= m * d[i - 1]
        x = [0.0] * n
        x[n - 1] = d[n - 1] / b[n - 1]
        for i in range(n - 2, -1, -1):
            x[i] = (d[i] - off * x[i + 1]) / b[i]
        return [round(v, 4) for v in x]

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Crank-Nicolson scheme setup steps.

        Args:
            data: Solution data with grid and system.

        Returns:
            Steps showing r, stencil, and system.
        """
        u0_str = ", ".join(_fmt(v) for v in data["u0"])
        u1_str = ", ".join(_fmt(v) for v in data["u1"])
        return [
            f"r = k*dt/dx^2 = {_fmt(data['r'])}",
            f"LHS diag = {_fmt(data['diag'])}, off = {_fmt(data['off'])}",
            f"u^0 = [{u0_str}]",
            f"u^1 = [{u1_str}]",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the solution after one time step.

        Args:
            data: Solution data.

        Returns:
            Solution at time step 1.
        """
        parts = [f"u^1_{j+1}={_fmt(v)}" for j, v in enumerate(data["u1"])]
        return ", ".join(parts)


# ── 8. Variational PDE / Euler-Lagrange (tier 7) ────────────────────


@register
class VariationalPDEGenerator(StepGenerator):
    """Derive the Euler-Lagrange equation from a variational principle.

    Given a functional J[u] = integral L(x, u, u') dx, derives the
    Euler-Lagrange equation d/dx(dL/du') - dL/du = 0 and identifies
    the resulting PDE.

    Input format:
        ``derive Euler-Lagrange equation from variational principle``

    Target format:
        ``J[u] = int_0^1 (u'^2 + u^2 - 2fu) dx <step>
        L = u'^2 + u^2 - 2fu <step>
        dL/du' = 2u', dL/du = 2u - 2f <step>
        EL: -2u'' + 2u - 2f = 0 => -u'' + u = f``

    Difficulty scaling:
        Difficulty 1-3: J = int (u'^2) dx => u'' = 0.
        Difficulty 4-6: J = int (u'^2 + u^2 - 2fu) dx.
        Difficulty 7-8: J = int (u'^2/2 + V(x)*u^2/2 - f*u) dx.

    Prerequisites:
        heat_equation (tier 6).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "variational_pde"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["heat_equation"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls Lagrangian complexity.

        Returns:
            Natural language description.
        """
        return "derive Euler-Lagrange equation from variational principle"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a variational PDE problem.

        Args:
            difficulty: Controls Lagrangian complexity.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            return self._simple_var(difficulty)
        if difficulty <= 6:
            return self._standard_var(difficulty)
        return self._potential_var(difficulty)

    def _simple_var(self, difficulty: int) -> tuple[str, dict]:
        """Generate J = int a*u'^2 dx, EL: u'' = 0.

        Args:
            difficulty: Controls coefficient.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        a = self._rng.randint(1, 3)
        problem = f"J[u] = \\int_0^1 {a}(u')^2 dx, u(0)=0, u(1)=1"
        return problem, {
            "var_type": "simple", "a": a,
            "lagrangian": f"{a}(u')^2",
            "dLdu_prime": f"{2*a}u'",
            "dLdu": "0",
            "el_equation": f"-{2*a}u'' = 0, i.e. u'' = 0",
            "solution": "u(x) = x",
        }

    def _standard_var(self, difficulty: int) -> tuple[str, dict]:
        """Generate J = int (u'^2 + u^2 - 2fu) dx.

        EL: -u'' + u = f.

        Args:
            difficulty: Controls f.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        f_type = self._rng.choice(["const", "x"])
        if f_type == "const":
            c = self._rng.randint(1, 4)
            f_str = str(c)
            sol_note = f"particular: u_p = {c}"
        else:
            f_str = "x"
            sol_note = "particular: u_p = x"
        problem = f"J[u] = \\int_0^1 ((u')^2 + u^2 - 2 \\cdot {f_str} \\cdot u) dx"
        return problem, {
            "var_type": "standard",
            "lagrangian": f"(u')^2 + u^2 - 2*{f_str}*u",
            "dLdu_prime": "2u'",
            "dLdu": f"2u - 2*{f_str}",
            "el_equation": f"-u'' + u = {f_str}",
            "solution": sol_note,
        }

    def _potential_var(self, difficulty: int) -> tuple[str, dict]:
        """Generate J = int (u'^2/2 + V*u^2/2 - f*u) dx.

        EL: -u'' + V*u = f.

        Args:
            difficulty: Controls V.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        v = self._rng.randint(1, 4)
        c = self._rng.randint(1, 3)
        problem = (f"J[u] = \\int_0^1 ((u')^2/2 + "
                   f"{v}u^2/2 - {c}u) dx")
        return problem, {
            "var_type": "potential", "v": v, "c": c,
            "lagrangian": f"(u')^2/2 + {v}u^2/2 - {c}u",
            "dLdu_prime": "u'",
            "dLdu": f"{v}u - {c}",
            "el_equation": f"-u'' + {v}u = {c}",
            "solution": f"particular: u_p = {c}/{v} = {_fmt(c/v)}",
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Euler-Lagrange derivation steps.

        Args:
            data: Solution data with Lagrangian and derivatives.

        Returns:
            Steps showing L, partial derivatives, and EL equation.
        """
        return [
            f"L = {data['lagrangian']}",
            f"dL/du' = {data['dLdu_prime']}, dL/du = {data['dLdu']}",
            f"EL: d/dx(dL/du') - dL/du = 0",
            f"=> {data['el_equation']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the Euler-Lagrange equation.

        Args:
            data: Solution data.

        Returns:
            EL equation and solution note.
        """
        return data["el_equation"]
