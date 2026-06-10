"""Mathematical physics generators.

8 generators across tiers 6-7 covering action principle, variational
derivatives, Green's functions for ODEs, Sturm-Liouville eigenvalues,
Fourier heat kernel, symmetry generators, path integrals, and group
representations in physics.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


class _PhysFormatter:
    """Formats numeric values for mathematical physics problems.

    Provides consistent rounding and clean string representations
    to keep target text compact and under the 512-character limit.
    """

    @staticmethod
    def fmt(value: float, decimals: int = 4) -> str:
        """Format a numeric value, stripping unnecessary trailing zeros.

        Args:
            value: Number to format.
            decimals: Maximum decimal places.

        Returns:
            Clean string representation.
        """
        rounded = round(value, decimals)
        if rounded == int(rounded):
            return str(int(rounded))
        return str(rounded)


# ---------------------------------------------------------------------------
# 1. Action principle  (tier 6)
# ---------------------------------------------------------------------------


@register
class ActionPrincipleGenerator(StepGenerator):
    """Compute the action S = integral L dt for a simple trajectory.

    Generates a Lagrangian for a free particle or harmonic oscillator,
    defines a trajectory segment over [0, T], and computes the action
    integral. Shows that the classical path is stationary.

    Input format:
        ``compute the action integral``

    Target format:
        ``L = T - V <step> trajectory: q(t) = ... <step>
        S = integral_0^T L dt = ... <step> S = ...``

    Difficulty scaling:
        d1-3: free particle L = m*v^2/2, constant velocity.
        d4-6: harmonic oscillator L = m*v^2/2 - k*q^2/2, q(t)=A*sin(wt).
        d7-8: perturbed trajectory, compare actions.

    Prerequisites:
        lagrangian, definite_integral.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "action_principle"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["lagrangian", "definite_integral"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls system complexity.

        Returns:
            Natural language description.
        """
        return "compute the action integral"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a trajectory and compute the action.

        Args:
            difficulty: Controls system type.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            return self._free_particle(difficulty)
        if difficulty <= 6:
            return self._harmonic_oscillator(difficulty)
        return self._perturbed_path(difficulty)

    def _free_particle(self, difficulty: int) -> tuple[str, dict]:
        """Compute action for a free particle at constant velocity.

        Args:
            difficulty: Controls parameter magnitude.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        m = self._rng.randint(1, 3 + difficulty)
        v = round(self._rng.uniform(0.5, 3.0), 2)
        t_max = self._rng.randint(1, 3 + difficulty)
        lag = round(0.5 * m * v * v, 4)
        action = round(lag * t_max, 4)
        return "S = \\int_0^T L \\, dt", {
            "system": "free", "m": m, "v": v, "T": t_max,
            "L": lag, "S": action,
            "trajectory": f"q(t) = {v}t",
        }

    def _harmonic_oscillator(self, difficulty: int) -> tuple[str, dict]:
        """Compute action for a harmonic oscillator trajectory.

        Args:
            difficulty: Controls parameter magnitude.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        m = self._rng.randint(1, 2 + difficulty)
        k = self._rng.randint(1, 2 + difficulty)
        omega = round(math.sqrt(k / m), 4)
        amp = round(self._rng.uniform(0.5, 2.0), 2)
        t_max = round(math.pi / omega, 4) if omega > 0 else 1.0
        t_max = round(min(t_max, 5.0), 4)
        # S = integral of (m/2)(A*w*cos(wt))^2 - (k/2)(A*sin(wt))^2 dt
        # For full half-period, S = 0 for classical path
        # Numerically integrate with small steps
        n_steps = 100
        dt = t_max / n_steps
        action = 0.0
        for i in range(n_steps):
            t = (i + 0.5) * dt
            q = amp * math.sin(omega * t)
            v = amp * omega * math.cos(omega * t)
            lag = 0.5 * m * v * v - 0.5 * k * q * q
            action += lag * dt
        action = round(action, 4)
        return "S = \\int_0^T L \\, dt", {
            "system": "harmonic", "m": m, "k": k, "omega": omega,
            "A": amp, "T": t_max, "S": action,
            "trajectory": f"q(t) = {amp}\\sin({_PhysFormatter.fmt(omega)}t)",
        }

    def _perturbed_path(self, difficulty: int) -> tuple[str, dict]:
        """Compare actions of classical and perturbed paths.

        Args:
            difficulty: Controls perturbation magnitude.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        m = self._rng.randint(1, difficulty)
        v0 = round(self._rng.uniform(1.0, 3.0), 2)
        t_max = self._rng.randint(1, 3)
        eps = round(self._rng.uniform(0.1, 0.5), 2)
        # Classical: q(t) = v0*t, S_cl = m*v0^2*T/2
        s_cl = round(0.5 * m * v0 * v0 * t_max, 4)
        # Perturbed: q(t) = v0*t + eps*sin(pi*t/T)
        n_steps = 100
        dt = t_max / n_steps
        s_pert = 0.0
        for i in range(n_steps):
            t = (i + 0.5) * dt
            vel = v0 + eps * math.pi / t_max * math.cos(math.pi * t / t_max)
            lag = 0.5 * m * vel * vel
            s_pert += lag * dt
        s_pert = round(s_pert, 4)
        return "S = \\int_0^T L \\, dt", {
            "system": "perturbed", "m": m, "v0": v0, "T": t_max,
            "eps": eps, "S_cl": s_cl, "S_pert": s_pert,
            "S": s_cl,
            "trajectory": f"q(t) = {v0}t (classical)",
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate action computation steps.

        Args:
            data: Solution data with trajectory and action.

        Returns:
            Steps showing Lagrangian, trajectory, and integration.
        """
        system = data["system"]
        steps = [f"trajectory: {data['trajectory']}"]
        if system == "free":
            steps.append(f"L = \\frac{{1}}{{2}}({data['m']})({data['v']})^2 = {_PhysFormatter.fmt(data['L'])}")
            steps.append(f"S = L \\cdot T = {_PhysFormatter.fmt(data['L'])} \\cdot {data['T']}")
        elif system == "harmonic":
            steps.append(f"m={data['m']}, k={data['k']}, \\omega={_PhysFormatter.fmt(data['omega'])}")
            steps.append(f"S = \\int_0^{{{_PhysFormatter.fmt(data['T'])}}} L \\, dt")
        else:
            steps.append(f"S_{{cl}} = \\frac{{1}}{{2}}({data['m']})({data['v0']})^2({data['T']}) = {_PhysFormatter.fmt(data['S_cl'])}")
            steps.append(f"S_{{pert}} = {_PhysFormatter.fmt(data['S_pert'])} (eps={data['eps']})")
            steps.append(f"S_{{pert}} > S_{{cl}}: classical path is stationary")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the action value.

        Args:
            data: Solution data.

        Returns:
            String representation of S.
        """
        return f"S = {_PhysFormatter.fmt(data['S'])}"


# ---------------------------------------------------------------------------
# 2. Variational derivative  (tier 7)
# ---------------------------------------------------------------------------


@register
class VariationalDerivativeGenerator(StepGenerator):
    """Compute the variational derivative via Euler-Lagrange.

    Given a functional F[y] = integral f(y, y') dx, computes the
    Euler-Lagrange equation: delta F/delta y = df/dy - d/dx(df/dy').

    Input format:
        ``compute variational derivative``

    Target format:
        ``F[y] = \\int f(y,y') dx <step>
        df/dy = ... <step> df/dy' = ... <step>
        d/dx(df/dy') = ... <step>
        \\delta F/\\delta y = ...``

    Difficulty scaling:
        d1-3: f = a*y'^2 + b*y^2 (harmonic).
        d4-6: f = a*y'^2 + b*y^2 + c*y (shifted).
        d7-8: f = a*y'^2 + b*y^4 (nonlinear).

    Prerequisites:
        partial_derivative.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "variational_derivative"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["partial_derivative"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls integrand complexity.

        Returns:
            Natural language description.
        """
        return "compute variational derivative"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a functional and compute its Euler-Lagrange equation.

        Args:
            difficulty: Controls integrand complexity.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        a = self._rng.randint(1, 3 + difficulty)
        b = self._rng.randint(1, 3 + difficulty)
        c = 0
        if difficulty <= 3:
            ftype = "harmonic"
        elif difficulty <= 6:
            ftype = "shifted"
            c = self._rng.randint(1, difficulty)
        else:
            ftype = "nonlinear"

        if ftype == "harmonic":
            f_str = f"{a}y'^2 + {b}y^2"
            df_dy = f"{2 * b}y"
            df_dyp = f"{2 * a}y'"
            d_dx_dfyp = f"{2 * a}y''"
            el = f"{2 * b}y - {2 * a}y'' = 0"
        elif ftype == "shifted":
            f_str = f"{a}y'^2 + {b}y^2 + {c}y"
            df_dy = f"{2 * b}y + {c}"
            df_dyp = f"{2 * a}y'"
            d_dx_dfyp = f"{2 * a}y''"
            el = f"{2 * b}y + {c} - {2 * a}y'' = 0"
        else:
            f_str = f"{a}y'^2 + {b}y^4"
            df_dy = f"{4 * b}y^3"
            df_dyp = f"{2 * a}y'"
            d_dx_dfyp = f"{2 * a}y''"
            el = f"{4 * b}y^3 - {2 * a}y'' = 0"

        return "\\frac{\\delta F}{\\delta y} = \\frac{\\partial f}{\\partial y} - \\frac{d}{dx}\\frac{\\partial f}{\\partial y'}", {
            "ftype": ftype, "a": a, "b": b, "c": c,
            "f_str": f_str, "df_dy": df_dy, "df_dyp": df_dyp,
            "d_dx_dfyp": d_dx_dfyp, "el": el,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate variational derivative computation steps.

        Args:
            data: Solution data with partial derivatives and EL equation.

        Returns:
            Steps showing each partial derivative and the result.
        """
        return [
            f"f(y,y') = {data['f_str']}",
            f"\\partial f/\\partial y = {data['df_dy']}",
            f"\\partial f/\\partial y' = {data['df_dyp']}",
            f"d/dx(\\partial f/\\partial y') = {data['d_dx_dfyp']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the Euler-Lagrange equation.

        Args:
            data: Solution data.

        Returns:
            The EL equation as a string.
        """
        return data["el"]


# ---------------------------------------------------------------------------
# 3. Green's function ODE  (tier 7)
# ---------------------------------------------------------------------------


@register
class GreenFunctionODEGenerator(StepGenerator):
    """Compute Green's function for y'' + k^2*y = delta(x - s).

    For the equation y'' + k^2*y = delta(x - s), the Green's function
    is G(x, s) = sin(k|x - s|) / k. Evaluates at specific points.

    Input format:
        ``find Green's function``

    Target format:
        ``y'' + k^2 y = \\delta(x-s) <step>
        G(x,s) = \\sin(k|x-s|)/k <step>
        G(...) = ...``

    Difficulty scaling:
        d1-3: integer k, simple evaluation points.
        d4-6: non-integer k, multiple evaluation points.
        d7-8: boundary conditions, matching conditions at x=s.

    Prerequisites:
        diff_equation.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "green_function_ode"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["diff_equation"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls complexity of evaluation.

        Returns:
            Natural language description.
        """
        return "find Green's function"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Green's function problem and evaluate it.

        Args:
            difficulty: Controls parameter choices.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            k = self._rng.randint(1, 3)
        elif difficulty <= 6:
            k = round(self._rng.uniform(0.5, 4.0), 2)
        else:
            k = round(self._rng.uniform(1.0, 5.0), 2)

        s = round(self._rng.uniform(0.0, 2.0), 2)

        n_eval = min(2 + difficulty // 3, 4)
        evals = []
        for _ in range(n_eval):
            x = round(self._rng.uniform(0.0, 4.0), 2)
            g_val = round(math.sin(k * abs(x - s)) / k, 4) if k != 0 else 0.0
            evals.append((x, g_val))

        # Matching conditions for higher difficulty
        matching = []
        if difficulty >= 7:
            # G continuous at x=s: G(s-, s) = G(s+, s) = 0
            matching.append(f"G({_PhysFormatter.fmt(s)}^-, {_PhysFormatter.fmt(s)}) = 0 (continuous)")
            # Jump in derivative: G'(s+) - G'(s-) = 1
            matching.append("G'(s+) - G'(s-) = 1 (jump condition)")

        return f"y'' + {_PhysFormatter.fmt(k)}^2 y = \\delta(x - {_PhysFormatter.fmt(s)})", {
            "k": k, "s": s, "evals": evals, "matching": matching,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Green's function derivation steps.

        Args:
            data: Solution data with evaluations.

        Returns:
            Steps showing the formula and evaluations.
        """
        k_str = _PhysFormatter.fmt(data["k"])
        steps = [
            f"G(x,s) = \\sin({k_str}|x-s|) / {k_str}",
        ]
        for cond in data["matching"]:
            steps.append(cond)
        for x, g in data["evals"]:
            steps.append(f"G({_PhysFormatter.fmt(x)}, {_PhysFormatter.fmt(data['s'])}) = {_PhysFormatter.fmt(g)}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the Green's function evaluations.

        Args:
            data: Solution data.

        Returns:
            String with all evaluation results.
        """
        parts = [f"G({_PhysFormatter.fmt(x)},{_PhysFormatter.fmt(data['s'])})={_PhysFormatter.fmt(g)}"
                 for x, g in data["evals"]]
        return "; ".join(parts)


# ---------------------------------------------------------------------------
# 4. Sturm-Liouville  (tier 7)
# ---------------------------------------------------------------------------


@register
class SturmLiouvilleGenerator(StepGenerator):
    """Find eigenvalues of a Sturm-Liouville problem.

    Solves -(p*y')' + q*y = lambda*w*y on [0, L] with Dirichlet
    boundary conditions y(0) = y(L) = 0. For the simple case
    p=1, q=0, w=1, eigenvalues are (n*pi/L)^2 with eigenfunctions
    sin(n*pi*x/L).

    Input format:
        ``find Sturm-Liouville eigenvalues``

    Target format:
        ``-y'' = \\lambda y on [0, L] <step>
        y(0) = y(L) = 0 <step>
        \\lambda_n = (n\\pi/L)^2 <step>
        \\lambda_1 = ..., \\lambda_2 = ..., ...``

    Difficulty scaling:
        d1-3: p=1, q=0, w=1, integer L.
        d4-6: p=1, q=constant, w=1 (shifted eigenvalues).
        d7-8: p=1, q=0, w=constant (scaled eigenvalues).

    Prerequisites:
        eigenvalue.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "sturm_liouville"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["eigenvalue"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls problem complexity.

        Returns:
            Natural language description.
        """
        return "find Sturm-Liouville eigenvalues"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Sturm-Liouville problem and compute eigenvalues.

        Args:
            difficulty: Controls the form of the equation.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        big_l = self._rng.randint(1, 2 + difficulty)
        n_eigs = min(3, 1 + difficulty // 2)

        if difficulty <= 3:
            # -y'' = lambda*y, y(0)=y(L)=0
            q_val = 0
            w_val = 1
            eigenvalues = []
            for n in range(1, n_eigs + 1):
                lam = round((n * math.pi / big_l) ** 2, 4)
                eigenvalues.append((n, lam))
            eq_str = f"-y'' = \\lambda y \\text{{ on }} [0, {big_l}]"
            eig_formula = f"(n\\pi/{big_l})^2"
        elif difficulty <= 6:
            # -y'' + q*y = lambda*y
            q_val = self._rng.randint(1, difficulty)
            w_val = 1
            eigenvalues = []
            for n in range(1, n_eigs + 1):
                lam = round((n * math.pi / big_l) ** 2 + q_val, 4)
                eigenvalues.append((n, lam))
            eq_str = f"-y'' + {q_val}y = \\lambda y \\text{{ on }} [0, {big_l}]"
            eig_formula = f"(n\\pi/{big_l})^2 + {q_val}"
        else:
            # -y'' = lambda*w*y
            q_val = 0
            w_val = self._rng.randint(2, difficulty)
            eigenvalues = []
            for n in range(1, n_eigs + 1):
                lam = round((n * math.pi / big_l) ** 2 / w_val, 4)
                eigenvalues.append((n, lam))
            eq_str = f"-y'' = {w_val}\\lambda y \\text{{ on }} [0, {big_l}]"
            eig_formula = f"(n\\pi/{big_l})^2 / {w_val}"

        return eq_str, {
            "L": big_l, "q": q_val, "w": w_val,
            "eigenvalues": eigenvalues,
            "eig_formula": eig_formula,
            "eigenfunctions": f"\\sin(n\\pi x/{big_l})",
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Sturm-Liouville eigenvalue computation steps.

        Args:
            data: Solution data with eigenvalues.

        Returns:
            Steps showing boundary conditions, formula, and values.
        """
        steps = [
            f"y(0) = y({data['L']}) = 0",
            f"eigenfunctions: {data['eigenfunctions']}",
            f"\\lambda_n = {data['eig_formula']}",
        ]
        for n, lam in data["eigenvalues"]:
            steps.append(f"\\lambda_{n} = {_PhysFormatter.fmt(lam)}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the eigenvalues.

        Args:
            data: Solution data.

        Returns:
            String listing eigenvalues.
        """
        parts = [f"\\lambda_{n}={_PhysFormatter.fmt(lam)}"
                 for n, lam in data["eigenvalues"]]
        return ", ".join(parts)


# ---------------------------------------------------------------------------
# 5. Fourier heat kernel  (tier 6)
# ---------------------------------------------------------------------------


@register
class FourierHeatKernelGenerator(StepGenerator):
    """Solve the heat equation u_t = k*u_xx with Fourier series.

    Given initial condition u(x, 0) on [0, L], computes the first 3
    Fourier sine series coefficients and writes the time-dependent
    solution u(x, t) = sum B_n * sin(n*pi*x/L) * exp(-k*(n*pi/L)^2*t).

    Input format:
        ``solve heat equation with Fourier series``

    Target format:
        ``u_t = k u_{xx}, u(0,t)=u(L,t)=0 <step>
        B_1 = ..., B_2 = ..., B_3 = ... <step>
        u(x,t) = sum ...``

    Difficulty scaling:
        d1-3: u(x,0) = sin(pi*x/L) (single mode).
        d4-6: u(x,0) = x*(L-x) (requires integration).
        d7-8: u(x,0) = piecewise linear.

    Prerequisites:
        fourier_coefficient.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "fourier_heat_kernel"

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
            difficulty: Controls initial condition complexity.

        Returns:
            Natural language description.
        """
        return "solve heat equation with Fourier series"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a heat equation problem and compute Fourier solution.

        Args:
            difficulty: Controls initial condition type.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        big_l = self._rng.randint(1, 2 + difficulty)
        kappa = round(self._rng.uniform(0.1, 2.0), 2)

        if difficulty <= 3:
            return self._single_mode(big_l, kappa)
        if difficulty <= 6:
            return self._quadratic_ic(big_l, kappa)
        return self._piecewise_ic(big_l, kappa)

    def _single_mode(self, big_l: int, kappa: float) -> tuple[str, dict]:
        """Heat equation with single Fourier mode initial condition.

        Args:
            big_l: Domain length.
            kappa: Thermal diffusivity.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        amp = self._rng.randint(1, 5)
        coeffs = [(1, float(amp)), (2, 0.0), (3, 0.0)]
        decay_1 = round(kappa * (math.pi / big_l) ** 2, 4)
        return f"u_t = {_PhysFormatter.fmt(kappa)} u_{{xx}}", {
            "L": big_l, "k": kappa, "ic": f"{amp}\\sin(\\pi x/{big_l})",
            "coeffs": coeffs, "decay_rates": [decay_1],
        }

    def _quadratic_ic(self, big_l: int, kappa: float) -> tuple[str, dict]:
        """Heat equation with u(x,0) = x*(L-x).

        Args:
            big_l: Domain length.
            kappa: Thermal diffusivity.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        # B_n = (2/L) * integral_0^L x(L-x)*sin(n*pi*x/L) dx
        # = 4L^2/(n^3 * pi^3) for odd n, 0 for even n
        coeffs = []
        for n in range(1, 4):
            if n % 2 == 1:
                bn = round(4 * big_l ** 2 / (n ** 3 * math.pi ** 3), 4)
            else:
                bn = 0.0
            coeffs.append((n, bn))

        decay_rates = []
        for n in range(1, 4):
            rate = round(kappa * (n * math.pi / big_l) ** 2, 4)
            decay_rates.append(rate)

        return f"u_t = {_PhysFormatter.fmt(kappa)} u_{{xx}}", {
            "L": big_l, "k": kappa, "ic": f"x({big_l}-x)",
            "coeffs": coeffs, "decay_rates": decay_rates,
        }

    def _piecewise_ic(self, big_l: int, kappa: float) -> tuple[str, dict]:
        """Heat equation with piecewise linear initial condition.

        Args:
            big_l: Domain length.
            kappa: Thermal diffusivity.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        # Triangle: u(x,0) = 2x/L for x <= L/2, 2(L-x)/L for x > L/2
        # B_n = 8/(n^2*pi^2) * sin(n*pi/2) for triangle wave
        coeffs = []
        for n in range(1, 4):
            bn = round(8.0 / (n ** 2 * math.pi ** 2) * math.sin(n * math.pi / 2), 4)
            coeffs.append((n, bn))

        decay_rates = []
        for n in range(1, 4):
            rate = round(kappa * (n * math.pi / big_l) ** 2, 4)
            decay_rates.append(rate)

        return f"u_t = {_PhysFormatter.fmt(kappa)} u_{{xx}}", {
            "L": big_l, "k": kappa, "ic": "triangle on [0,L]",
            "coeffs": coeffs, "decay_rates": decay_rates,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Fourier heat kernel solution steps.

        Args:
            data: Solution data with coefficients and decay rates.

        Returns:
            Steps showing coefficients and solution form.
        """
        big_l = data["L"]
        steps = [
            f"u(x,0) = {data['ic']}, L={big_l}",
            f"u(0,t) = u({big_l},t) = 0",
        ]
        for n, bn in data["coeffs"]:
            steps.append(f"B_{n} = {_PhysFormatter.fmt(bn)}")
        terms = []
        for (n, bn), rate in zip(data["coeffs"], data["decay_rates"]):
            if bn != 0.0:
                terms.append(
                    f"{_PhysFormatter.fmt(bn)}\\sin({n}\\pi x/{big_l})"
                    f"e^{{-{_PhysFormatter.fmt(rate)}t}}"
                )
        if terms:
            steps.append("u(x,t) = " + " + ".join(terms[:3]))
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the Fourier coefficients.

        Args:
            data: Solution data.

        Returns:
            String listing B_1, B_2, B_3.
        """
        parts = [f"B_{n}={_PhysFormatter.fmt(bn)}" for n, bn in data["coeffs"]]
        return ", ".join(parts)


# ---------------------------------------------------------------------------
# 6. Symmetry generator  (tier 7)
# ---------------------------------------------------------------------------


@register
class SymmetryGeneratorPhysics(StepGenerator):
    """Identify infinitesimal generators of continuous symmetries.

    For rotation symmetry, the generator is L_z = x*d/dy - y*d/dx.
    For translation, it is d/dx. Applies the generator to a given
    function and verifies the symmetry.

    Input format:
        ``identify symmetry generator and apply``

    Target format:
        ``symmetry: rotation about z <step>
        generator: L_z = x \\partial/\\partial y - y \\partial/\\partial x <step>
        apply to f(x,y) = ... <step>
        L_z f = ...``

    Difficulty scaling:
        d1-3: translation d/dx on polynomials.
        d4-6: rotation L_z on polynomials in x, y.
        d7-8: scaling x*d/dx + y*d/dy on homogeneous functions.

    Prerequisites:
        partial_derivative.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "symmetry_generator"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["partial_derivative"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls symmetry type.

        Returns:
            Natural language description.
        """
        return "identify symmetry generator and apply"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a symmetry generator problem.

        Args:
            difficulty: Controls symmetry type.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            return self._translation(difficulty)
        if difficulty <= 6:
            return self._rotation(difficulty)
        return self._scaling(difficulty)

    def _translation(self, difficulty: int) -> tuple[str, dict]:
        """Apply translation generator d/dx to a polynomial.

        Args:
            difficulty: Controls polynomial degree.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        a = self._rng.randint(1, 3 + difficulty)
        b = self._rng.randint(1, 3 + difficulty)
        # f(x) = a*x^2 + b*x
        f_str = f"{a}x^2 + {b}x"
        # d/dx f = 2a*x + b
        result = f"{2 * a}x + {b}"
        return "\\partial/\\partial x", {
            "symmetry": "translation in x",
            "generator": "\\partial/\\partial x",
            "f": f_str, "result": result,
        }

    def _rotation(self, difficulty: int) -> tuple[str, dict]:
        """Apply rotation generator L_z to a polynomial in x, y.

        Args:
            difficulty: Controls polynomial complexity.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        a = self._rng.randint(1, difficulty)
        b = self._rng.randint(1, difficulty)
        # f(x,y) = a*x^2 + b*y^2
        f_str = f"{a}x^2 + {b}y^2"
        # L_z f = x*(df/dy) - y*(df/dx) = x*(2b*y) - y*(2a*x)
        #       = 2b*xy - 2a*xy = 2(b-a)*xy
        coeff = 2 * (b - a)
        if coeff == 0:
            result = "0"
        elif coeff == 1:
            result = "xy"
        elif coeff == -1:
            result = "-xy"
        else:
            result = f"{coeff}xy"

        return "L_z = x\\partial_y - y\\partial_x", {
            "symmetry": "rotation about z-axis",
            "generator": "L_z = x\\partial/\\partial y - y\\partial/\\partial x",
            "f": f_str, "result": result,
            "df_dx": f"{2 * a}x", "df_dy": f"{2 * b}y",
        }

    def _scaling(self, difficulty: int) -> tuple[str, dict]:
        """Apply scaling generator x*d/dx + y*d/dy to a homogeneous function.

        Args:
            difficulty: Controls function degree.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        a = self._rng.randint(1, difficulty)
        deg = self._rng.choice([2, 3])
        # f = a * x^deg (homogeneous of degree deg)
        f_str = f"{a}x^{deg}"
        # (x*d/dx) f = a*deg*x^deg = deg * f
        result = f"{a * deg}x^{deg}"

        return "D = x\\partial_x + y\\partial_y", {
            "symmetry": "scaling",
            "generator": "D = x\\partial/\\partial x + y\\partial/\\partial y",
            "f": f_str, "result": result,
            "degree": deg,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate symmetry generator application steps.

        Args:
            data: Solution data with generator and result.

        Returns:
            Steps showing the generator, function, and result.
        """
        steps = [
            f"symmetry: {data['symmetry']}",
            f"generator: {data['generator']}",
            f"f = {data['f']}",
        ]
        if "df_dx" in data:
            steps.append(f"\\partial f/\\partial x = {data['df_dx']}")
            steps.append(f"\\partial f/\\partial y = {data['df_dy']}")
        if "degree" in data:
            steps.append(f"f is homogeneous of degree {data['degree']}")
        steps.append(f"generator applied: {data['result']}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the result of applying the generator.

        Args:
            data: Solution data.

        Returns:
            String with the generator action result.
        """
        return data["result"]


# ---------------------------------------------------------------------------
# 7. Path integral (simple)  (tier 7)
# ---------------------------------------------------------------------------


@register
class PathIntegralSimpleGenerator(StepGenerator):
    """Compute Gaussian path integrals and partition functions.

    Uses the identity integral exp(-a*x^2) dx = sqrt(pi/a) to compute
    partition functions for the harmonic oscillator and related systems.

    Input format:
        ``compute Gaussian integral / partition function``

    Target format:
        ``\\int_{-\\infty}^{\\infty} e^{-ax^2} dx = \\sqrt{\\pi/a} <step>
        a = ... <step> result = ...``

    Difficulty scaling:
        d1-3: single Gaussian integral with integer a.
        d4-6: partition function Z = integral exp(-beta*H) dx for harmonic.
        d7-8: multi-dimensional Gaussian (product of 1D integrals).

    Prerequisites:
        definite_integral.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "path_integral_simple"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["definite_integral"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls integral complexity.

        Returns:
            Natural language description.
        """
        return "compute Gaussian integral / partition function"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Gaussian integral problem.

        Args:
            difficulty: Controls problem type.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            return self._single_gaussian(difficulty)
        if difficulty <= 6:
            return self._harmonic_partition(difficulty)
        return self._multi_dim_gaussian(difficulty)

    def _single_gaussian(self, difficulty: int) -> tuple[str, dict]:
        """Compute a single Gaussian integral.

        Args:
            difficulty: Controls parameter a.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        a = self._rng.randint(1, 3 + difficulty)
        result = round(math.sqrt(math.pi / a), 4)
        return "\\int_{-\\infty}^{\\infty} e^{-ax^2} dx", {
            "type": "single", "a": a,
            "result": result,
            "formula": f"\\sqrt{{\\pi/{a}}}",
        }

    def _harmonic_partition(self, difficulty: int) -> tuple[str, dict]:
        """Compute partition function for harmonic oscillator.

        Z = integral exp(-beta * k * x^2 / 2) dx = sqrt(2*pi/(beta*k))

        Args:
            difficulty: Controls parameters.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        beta = round(self._rng.uniform(0.5, 3.0), 2)
        k = self._rng.randint(1, 2 + difficulty)
        # a = beta*k/2
        a = round(beta * k / 2, 4)
        z = round(math.sqrt(2 * math.pi / (beta * k)), 4)
        return "Z = \\int e^{-\\beta k x^2/2} dx", {
            "type": "partition", "beta": beta, "k": k,
            "a_eff": a, "result": z,
            "formula": f"\\sqrt{{2\\pi/({_PhysFormatter.fmt(beta)} \\cdot {k})}}",
        }

    def _multi_dim_gaussian(self, difficulty: int) -> tuple[str, dict]:
        """Compute a multi-dimensional Gaussian as product of 1D integrals.

        Args:
            difficulty: Controls dimension.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        dim = self._rng.choice([2, 3])
        a_vals = [self._rng.randint(1, difficulty) for _ in range(dim)]
        individual = [round(math.sqrt(math.pi / a), 4) for a in a_vals]
        total = round(math.prod(individual), 4)
        return f"\\int e^{{-\\sum a_i x_i^2}} d^{dim}x", {
            "type": "multi", "dim": dim, "a_vals": a_vals,
            "individual": individual, "result": total,
            "formula": f"\\prod_{{i=1}}^{{{dim}}} \\sqrt{{\\pi/a_i}}",
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Gaussian integral computation steps.

        Args:
            data: Solution data with parameters and result.

        Returns:
            Steps showing the computation.
        """
        if data["type"] == "single":
            return [
                f"a = {data['a']}",
                f"\\int e^{{-{data['a']}x^2}} dx = {data['formula']}",
                f"= {_PhysFormatter.fmt(data['result'])}",
            ]
        if data["type"] == "partition":
            return [
                f"\\beta = {data['beta']}, k = {data['k']}",
                f"effective a = \\beta k/2 = {_PhysFormatter.fmt(data['a_eff'])}",
                f"Z = {data['formula']} = {_PhysFormatter.fmt(data['result'])}",
            ]
        # multi
        steps = [f"dimension = {data['dim']}"]
        for i, (a, val) in enumerate(zip(data["a_vals"], data["individual"])):
            steps.append(f"a_{i+1}={a}: \\sqrt{{\\pi/{a}}} = {_PhysFormatter.fmt(val)}")
        steps.append(f"product = {_PhysFormatter.fmt(data['result'])}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the integral result.

        Args:
            data: Solution data.

        Returns:
            String with the result.
        """
        return _PhysFormatter.fmt(data["result"])


# ---------------------------------------------------------------------------
# 8. Group representation in physics  (tier 7)
# ---------------------------------------------------------------------------


@register
class GroupRepresentationPhysicsGenerator(StepGenerator):
    """Represent rotation group SO(2) as 2x2 matrices and verify axioms.

    Constructs rotation matrices R(theta), composes two rotations,
    and verifies closure, identity, inverse, and associativity.

    Input format:
        ``SO(2) representation and group axioms``

    Target format:
        ``R(\\theta) = [[cos, -sin],[sin, cos]] <step>
        R(\\theta_1) = ... <step> R(\\theta_2) = ... <step>
        R(\\theta_1)R(\\theta_2) = R(\\theta_1+\\theta_2) <step>
        verify: ...``

    Difficulty scaling:
        d1-3: simple angles (0, pi/2, pi).
        d4-6: arbitrary angles, verify inverse.
        d7-8: compose 3 rotations, verify associativity.

    Prerequisites:
        complex_arithmetic.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "group_representation_physics"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["complex_arithmetic"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls verification complexity.

        Returns:
            Natural language description.
        """
        return "SO(2) representation and group axioms"

    @staticmethod
    def _rotation_matrix(theta: float) -> list[list[float]]:
        """Compute the 2x2 rotation matrix for angle theta.

        Args:
            theta: Rotation angle in radians.

        Returns:
            2x2 matrix as nested list.
        """
        c = round(math.cos(theta), 4)
        s = round(math.sin(theta), 4)
        return [[c, round(-s, 4)], [s, c]]

    @staticmethod
    def _mat_mul_2x2(a: list[list[float]], b: list[list[float]]) -> list[list[float]]:
        """Multiply two 2x2 matrices.

        Args:
            a: First 2x2 matrix.
            b: Second 2x2 matrix.

        Returns:
            Product matrix.
        """
        return [
            [round(a[0][0] * b[0][0] + a[0][1] * b[1][0], 4),
             round(a[0][0] * b[0][1] + a[0][1] * b[1][1], 4)],
            [round(a[1][0] * b[0][0] + a[1][1] * b[1][0], 4),
             round(a[1][0] * b[0][1] + a[1][1] * b[1][1], 4)],
        ]

    @staticmethod
    def _fmt_mat(m: list[list[float]]) -> str:
        """Format a 2x2 matrix as a compact string.

        Args:
            m: 2x2 matrix.

        Returns:
            Formatted string.
        """
        return (f"[[{_PhysFormatter.fmt(m[0][0])},{_PhysFormatter.fmt(m[0][1])}],"
                f"[{_PhysFormatter.fmt(m[1][0])},{_PhysFormatter.fmt(m[1][1])}]]")

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an SO(2) representation problem.

        Args:
            difficulty: Controls complexity of verification.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            return self._simple_angles(difficulty)
        if difficulty <= 6:
            return self._inverse_check(difficulty)
        return self._associativity_check(difficulty)

    def _simple_angles(self, difficulty: int) -> tuple[str, dict]:
        """Compose two rotations with simple angles.

        Args:
            difficulty: Controls angle choices.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        angles = [0, math.pi / 6, math.pi / 4, math.pi / 3, math.pi / 2, math.pi]
        t1 = self._rng.choice(angles)
        t2 = self._rng.choice(angles)
        r1 = self._rotation_matrix(t1)
        r2 = self._rotation_matrix(t2)
        product = self._mat_mul_2x2(r1, r2)
        r_sum = self._rotation_matrix(t1 + t2)
        return "R(\\theta) = [[\\cos\\theta, -\\sin\\theta],[\\sin\\theta, \\cos\\theta]]", {
            "type": "compose",
            "t1": round(t1, 4), "t2": round(t2, 4),
            "r1": r1, "r2": r2,
            "product": product, "r_sum": r_sum,
            "t_sum": round(t1 + t2, 4),
        }

    def _inverse_check(self, difficulty: int) -> tuple[str, dict]:
        """Verify R(theta) * R(-theta) = I.

        Args:
            difficulty: Controls angle.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        t = round(self._rng.uniform(0.1, math.pi), 4)
        r = self._rotation_matrix(t)
        r_inv = self._rotation_matrix(-t)
        product = self._mat_mul_2x2(r, r_inv)
        return "R(\\theta) = [[\\cos\\theta, -\\sin\\theta],[\\sin\\theta, \\cos\\theta]]", {
            "type": "inverse",
            "t": t, "r": r, "r_inv": r_inv,
            "product": product,
        }

    def _associativity_check(self, difficulty: int) -> tuple[str, dict]:
        """Verify (R1*R2)*R3 = R1*(R2*R3) for three rotations.

        Args:
            difficulty: Controls angles.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        t1 = round(self._rng.uniform(0.1, math.pi), 4)
        t2 = round(self._rng.uniform(0.1, math.pi), 4)
        t3 = round(self._rng.uniform(0.1, math.pi), 4)
        r1 = self._rotation_matrix(t1)
        r2 = self._rotation_matrix(t2)
        r3 = self._rotation_matrix(t3)
        left = self._mat_mul_2x2(self._mat_mul_2x2(r1, r2), r3)
        right = self._mat_mul_2x2(r1, self._mat_mul_2x2(r2, r3))
        return "R(\\theta) = [[\\cos\\theta, -\\sin\\theta],[\\sin\\theta, \\cos\\theta]]", {
            "type": "associativity",
            "t1": t1, "t2": t2, "t3": t3,
            "r1": r1, "r2": r2, "r3": r3,
            "left": left, "right": right,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate SO(2) verification steps.

        Args:
            data: Solution data with matrices and products.

        Returns:
            Steps showing matrix construction and verification.
        """
        if data["type"] == "compose":
            return [
                f"R({_PhysFormatter.fmt(data['t1'])}) = {self._fmt_mat(data['r1'])}",
                f"R({_PhysFormatter.fmt(data['t2'])}) = {self._fmt_mat(data['r2'])}",
                f"R1*R2 = {self._fmt_mat(data['product'])}",
                f"R({_PhysFormatter.fmt(data['t_sum'])}) = {self._fmt_mat(data['r_sum'])}",
                "closure verified: R1*R2 = R(t1+t2)",
            ]
        if data["type"] == "inverse":
            return [
                f"R({_PhysFormatter.fmt(data['t'])}) = {self._fmt_mat(data['r'])}",
                f"R(-{_PhysFormatter.fmt(data['t'])}) = {self._fmt_mat(data['r_inv'])}",
                f"R*R^{{-1}} = {self._fmt_mat(data['product'])}",
                "inverse verified: R*R^{-1} = I",
            ]
        # associativity
        return [
            f"R1={self._fmt_mat(data['r1'])}",
            f"R2={self._fmt_mat(data['r2'])}",
            f"R3={self._fmt_mat(data['r3'])}",
            f"(R1*R2)*R3 = {self._fmt_mat(data['left'])}",
            f"R1*(R2*R3) = {self._fmt_mat(data['right'])}",
            "associativity verified",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the verification result.

        Args:
            data: Solution data.

        Returns:
            String with the axiom verified.
        """
        if data["type"] == "compose":
            return f"R1*R2 = R({_PhysFormatter.fmt(data['t_sum'])})"
        if data["type"] == "inverse":
            return "R * R^{-1} = I"
        return "associativity holds"
