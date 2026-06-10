"""Deep PDE generators for tiers 5-7.

8 generators covering the Schrodinger PDE, diffusion equation,
Laplace equation in cylindrical coordinates, damped wave equation,
nonlinear Burgers equation, 1D finite element method, CFL stability
condition, and spectral methods for PDEs.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


# -- Formatting helpers -----------------------------------------------


def _fmt(val: float) -> str:
    """Format a float to 4 decimal places, stripping trailing zeros.

    Args:
        val: Value to format.

    Returns:
        Formatted string.
    """
    return f"{round(val, 4):.4f}".rstrip("0").rstrip(".")


# =====================================================================
# 1. SCHRODINGER PDE (tier 6)
# =====================================================================

@register
class SchrodingerPDEGenerator(StepGenerator):
    """Solve the free-particle Schrodinger equation.

    i*hbar*du/dt = -hbar^2/(2m)*d^2u/dx^2 + V*u. For the free
    particle (V=0), plane wave solution u = exp(i(kx - wt)) with
    dispersion relation w = hbar*k^2/(2m).

    Difficulty scaling:
        Difficulty 1-3: free particle, compute dispersion.
        Difficulty 4-6: free particle, evaluate u at (x, t).
        Difficulty 7-8: particle in box, energy levels.

    Prerequisites:
        wave_equation_1d (tier 6).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "schrodinger_pde"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["wave_equation_1d"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls problem variant.

        Returns:
            Task description string.
        """
        return "solve Schrodinger equation for free particle"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Schrodinger equation problem.

        Args:
            difficulty: Controls problem variant.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 5:
            return self._free_particle(difficulty)
        return self._particle_in_box(difficulty)

    def _free_particle(self, difficulty: int) -> tuple[str, dict]:
        """Generate free particle dispersion problem.

        Args:
            difficulty: Controls parameter values.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        hbar = 1.0
        m = self._rng.choice([0.5, 1.0, 2.0])
        k = float(self._rng.randint(1, 4))
        omega = hbar * k ** 2 / (2 * m)

        x0 = round(self._rng.choice([0.0, 1.0, 2.0]), 4)
        t0 = round(self._rng.choice([0.5, 1.0]), 4)
        phase = k * x0 - omega * t0
        re_part = round(math.cos(phase), 4)
        im_part = round(math.sin(phase), 4)

        problem = (
            f"free particle: hbar={_fmt(hbar)}, m={_fmt(m)}, k={_fmt(k)}. "
            f"Compute dispersion w and u({_fmt(x0)},{_fmt(t0)})."
        )
        return problem, {
            "hbar": hbar, "m": m, "k": k, "omega": omega,
            "x0": x0, "t0": t0, "phase": phase,
            "re_part": re_part, "im_part": im_part,
        }

    def _particle_in_box(self, difficulty: int) -> tuple[str, dict]:
        """Generate particle in a box energy levels.

        Args:
            difficulty: Controls box size and quantum number.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        hbar = 1.0
        m = 1.0
        big_l = float(self._rng.randint(1, 3))
        n = self._rng.randint(1, 4)
        energy = (n ** 2 * math.pi ** 2 * hbar ** 2) / (2 * m * big_l ** 2)

        problem = (
            f"particle in box [0,{_fmt(big_l)}], hbar={_fmt(hbar)}, "
            f"m={_fmt(m)}. Energy level E_{n}?"
        )
        return problem, {
            "hbar": hbar, "m": m, "L": big_l, "n": n,
            "energy": energy, "omega": 0.0,
            "x0": 0.0, "t0": 0.0, "phase": 0.0,
            "re_part": 0.0, "im_part": 0.0,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Schrodinger equation solution steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing dispersion or energy levels.
        """
        steps = [
            f"i*hbar*du/dt = -hbar^2/(2m)*d^2u/dx^2",
        ]
        if data.get("energy") and data.get("n"):
            steps.append(
                f"E_n = n^2*pi^2*hbar^2/(2mL^2), n={data['n']}"
            )
            steps.append(f"E_{data['n']} = {_fmt(data['energy'])}")
        else:
            steps.append(
                f"w = hbar*k^2/(2m) = {_fmt(data['hbar'])}*"
                f"{_fmt(data['k'])}^2/(2*{_fmt(data['m'])}) = "
                f"{_fmt(data['omega'])}"
            )
            steps.append(
                f"u = exp(i({_fmt(data['k'])}x - {_fmt(data['omega'])}t))"
            )
            steps.append(
                f"Re(u) = {_fmt(data['re_part'])}, "
                f"Im(u) = {_fmt(data['im_part'])}"
            )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the final answer.

        Args:
            data: Solution data.

        Returns:
            Dispersion or energy value.
        """
        if data.get("energy") and data.get("n"):
            return f"E_{data['n']} = {_fmt(data['energy'])}"
        return f"w = {_fmt(data['omega'])}"


# =====================================================================
# 2. DIFFUSION EQUATION (tier 5)
# =====================================================================

@register
class DiffusionEquationGenerator(StepGenerator):
    """Solve the diffusion equation du/dt = D*d^2u/dx^2.

    For delta function initial condition, the solution is
    u(x,t) = 1/sqrt(4*pi*D*t) * exp(-x^2/(4*D*t)).
    Evaluates at a given (x, t).

    Difficulty scaling:
        Difficulty 1-3: D=1, simple (x, t) values.
        Difficulty 4-6: general D, moderate values.
        Difficulty 7-8: compute peak width (standard deviation).

    Prerequisites:
        exponentiation (tier 2).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "diffusion_equation"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["exponentiation"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls D and evaluation point.

        Returns:
            Task description string.
        """
        return "solve diffusion equation with delta IC"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a diffusion equation problem.

        Args:
            difficulty: Controls D and evaluation point.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            d_coeff = 1.0
        elif difficulty <= 6:
            d_coeff = self._rng.choice([0.5, 1.0, 2.0])
        else:
            d_coeff = round(self._rng.choice([0.25, 0.5, 1.0, 2.0, 4.0]), 4)

        t0 = round(self._rng.choice([0.5, 1.0, 2.0]), 4)
        x0 = round(self._rng.choice([0.0, 0.5, 1.0, 2.0]), 4)

        prefactor = 1.0 / math.sqrt(4 * math.pi * d_coeff * t0)
        exponent = -x0 ** 2 / (4 * d_coeff * t0)
        u_val = prefactor * math.exp(exponent)
        sigma = math.sqrt(2 * d_coeff * t0)

        problem = (
            f"du/dt = {_fmt(d_coeff)}*d^2u/dx^2, u(x,0) = delta(x). "
            f"Evaluate u({_fmt(x0)},{_fmt(t0)})."
        )
        return problem, {
            "D": d_coeff, "x0": x0, "t0": t0,
            "prefactor": prefactor, "exponent": exponent,
            "u_val": u_val, "sigma": sigma,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate diffusion equation solution steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing the Gaussian solution and evaluation.
        """
        return [
            f"u(x,t) = 1/sqrt(4*pi*D*t) * exp(-x^2/(4Dt))",
            f"D={_fmt(data['D'])}, t={_fmt(data['t0'])}, x={_fmt(data['x0'])}",
            f"prefactor = {_fmt(data['prefactor'])}",
            f"exponent = {_fmt(data['exponent'])}",
            f"u = {_fmt(data['u_val'])}, sigma = sqrt(2Dt) = {_fmt(data['sigma'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the solution value.

        Args:
            data: Solution data.

        Returns:
            Evaluated solution.
        """
        return f"u({_fmt(data['x0'])},{_fmt(data['t0'])}) = {_fmt(data['u_val'])}"


# =====================================================================
# 3. LAPLACE CYLINDRICAL (tier 7)
# =====================================================================

@register
class LaplaceCylindricalGenerator(StepGenerator):
    """Solve Laplace equation in cylindrical coordinates.

    (1/r)*d/dr(r*du/dr) + (1/r^2)*d^2u/dtheta^2 = 0.
    Separable solution u = R(r)*Theta(theta). R(r) = r^n or r^{-n},
    Theta = cos(n*theta) or sin(n*theta).

    Difficulty scaling:
        Difficulty 1-3: n=0, n=1 modes.
        Difficulty 4-6: n=2, evaluate at (r, theta).
        Difficulty 7-8: general n, boundary value problems.

    Prerequisites:
        heat_equation (tier 6).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "laplace_cylindrical"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["heat_equation"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls mode number.

        Returns:
            Task description string.
        """
        return "solve Laplace equation in cylindrical coordinates"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a cylindrical Laplace equation problem.

        Args:
            difficulty: Controls mode number.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            n = self._rng.choice([0, 1])
        elif difficulty <= 6:
            n = self._rng.choice([1, 2])
        else:
            n = self._rng.randint(2, 4)

        use_cos = self._rng.random() < 0.5
        trig = "cos" if use_cos else "sin"
        a_coeff = float(self._rng.randint(1, 4))

        r0 = round(self._rng.choice([0.5, 1.0, 2.0]), 4)
        theta0 = round(self._rng.choice(
            [0.0, math.pi / 6, math.pi / 4, math.pi / 3, math.pi / 2]
        ), 4)

        if n == 0:
            r_part = a_coeff
            theta_part = 1.0
            solution_form = f"u = {_fmt(a_coeff)} (constant)"
        else:
            r_part = a_coeff * r0 ** n
            trig_val = math.cos(n * theta0) if use_cos else math.sin(n * theta0)
            theta_part = trig_val
            solution_form = f"u = {_fmt(a_coeff)}*r^{n}*{trig}({n}*theta)"

        u_val = r_part * theta_part

        problem = (
            f"Laplace in cylindrical, mode n={n}. "
            f"u({_fmt(r0)},{_fmt(theta0)}) = ?"
        )
        return problem, {
            "n": n, "trig": trig, "a": a_coeff,
            "r0": r0, "theta0": theta0,
            "u_val": u_val, "solution_form": solution_form,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate cylindrical Laplace solution steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing separation and evaluation.
        """
        steps = [
            "(1/r)d/dr(r*du/dr) + (1/r^2)*d^2u/dtheta^2 = 0",
            f"separation: u = R(r)*Theta(theta), mode n={data['n']}",
            f"R(r) = r^{data['n']}, Theta = {data['trig']}({data['n']}*theta)",
            f"{data['solution_form']}",
            f"u({_fmt(data['r0'])},{_fmt(data['theta0'])}) = {_fmt(data['u_val'])}",
        ]
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the solution value.

        Args:
            data: Solution data.

        Returns:
            Evaluated solution.
        """
        return f"u = {_fmt(data['u_val'])}"


# =====================================================================
# 4. WAVE DAMPED (tier 6)
# =====================================================================

@register
class WaveDampedGenerator(StepGenerator):
    """Classify damped wave equation behaviour.

    u_tt + 2*gamma*u_t = c^2*u_xx. For mode with wavenumber k,
    characteristic equation: s^2 + 2*gamma*s + c^2*k^2 = 0.
    Classify: underdamped (gamma < c*k), critically damped
    (gamma = c*k), overdamped (gamma > c*k).

    Difficulty scaling:
        Difficulty 1-3: integer gamma, c, k=1.
        Difficulty 4-6: general k, classify regime.
        Difficulty 7-8: compute complex frequency.

    Prerequisites:
        wave_equation_1d (tier 6).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "wave_damped"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["wave_equation_1d"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls parameter complexity.

        Returns:
            Task description string.
        """
        return "classify damped wave equation behaviour"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a damped wave classification problem.

        Args:
            difficulty: Controls parameters.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        c = float(self._rng.randint(1, 4))
        if difficulty <= 3:
            k = 1.0
        else:
            k = float(self._rng.randint(1, 3))

        ck = c * k
        regime_choice = self._rng.choice(["under", "critical", "over"])
        if regime_choice == "under":
            gamma = round(ck * self._rng.choice([0.25, 0.5, 0.75]), 4)
        elif regime_choice == "critical":
            gamma = ck
        else:
            gamma = round(ck * self._rng.choice([1.5, 2.0, 3.0]), 4)

        discriminant = gamma ** 2 - ck ** 2
        if abs(discriminant) < 1e-10:
            regime = "critically damped"
            s1 = -gamma
            s2 = -gamma
        elif discriminant < 0:
            regime = "underdamped"
            real_part = -gamma
            imag_part = math.sqrt(-discriminant)
            s1 = round(real_part, 4)
            s2 = round(imag_part, 4)
        else:
            regime = "overdamped"
            s1 = round(-gamma + math.sqrt(discriminant), 4)
            s2 = round(-gamma - math.sqrt(discriminant), 4)

        problem = (
            f"u_tt + {_fmt(2 * gamma)}*u_t = {_fmt(c)}^2*u_xx, "
            f"k={_fmt(k)}. Classify."
        )
        return problem, {
            "c": c, "k": k, "gamma": gamma, "ck": ck,
            "discriminant": discriminant, "regime": regime,
            "s1": s1, "s2": s2,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate classification steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing classification.
        """
        steps = [
            f"gamma={_fmt(data['gamma'])}, c*k={_fmt(data['ck'])}",
            f"discriminant = gamma^2 - (ck)^2 = {_fmt(data['discriminant'])}",
        ]
        if data["regime"] == "underdamped":
            steps.append(
                f"underdamped: s = {_fmt(data['s1'])} +/- {_fmt(data['s2'])}i"
            )
        elif data["regime"] == "critically damped":
            steps.append(f"critically damped: s = {_fmt(data['s1'])} (repeated)")
        else:
            steps.append(
                f"overdamped: s1={_fmt(data['s1'])}, s2={_fmt(data['s2'])}"
            )
        steps.append(f"regime: {data['regime']}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the regime classification.

        Args:
            data: Solution data.

        Returns:
            Damping regime.
        """
        return data["regime"]


# =====================================================================
# 5. NONLINEAR PDE BURGER (tier 7)
# =====================================================================

@register
class NonlinearPDEBurgerGenerator(StepGenerator):
    """Analyse the inviscid Burgers equation via method of characteristics.

    u_t + u*u_x = 0. Characteristics: dx/dt = u, u constant along
    characteristics. Shock formation time t_s = -1/min(u_0'(x)).

    Difficulty scaling:
        Difficulty 1-3: u_0(x) = -ax, compute t_s = 1/a.
        Difficulty 4-6: u_0(x) = 1 - x on [0,1], general linear IC.
        Difficulty 7-8: u_0(x) = sin(pi*x), piecewise IC.

    Prerequisites:
        partial_derivative (tier 4).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "nonlinear_pde_burger"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["partial_derivative"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls IC complexity.

        Returns:
            Task description string.
        """
        return "find shock formation time for Burgers equation"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Burgers shock formation problem.

        Args:
            difficulty: Controls IC type.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            return self._linear_ic(difficulty)
        if difficulty <= 6:
            return self._affine_ic(difficulty)
        return self._sinusoidal_ic(difficulty)

    def _linear_ic(self, difficulty: int) -> tuple[str, dict]:
        """Generate with u_0(x) = -a*x (decreasing).

        min(u_0') = -a, so t_s = 1/a.

        Args:
            difficulty: Controls a.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        a = float(self._rng.randint(1, 4))
        t_s = 1.0 / a
        problem = f"u_t + u*u_x = 0, u_0(x) = -{_fmt(a)}x. Shock time?"
        return problem, {
            "ic": f"-{_fmt(a)}x", "min_deriv": -a, "t_s": t_s,
        }

    def _affine_ic(self, difficulty: int) -> tuple[str, dict]:
        """Generate with u_0(x) = b - a*x.

        min(u_0') = -a, so t_s = 1/a.

        Args:
            difficulty: Controls a, b.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        a = float(self._rng.randint(1, 4))
        b = float(self._rng.randint(0, 3))
        t_s = 1.0 / a
        problem = (
            f"u_t + u*u_x = 0, u_0(x) = {_fmt(b)} - {_fmt(a)}x. "
            f"Shock time?"
        )
        return problem, {
            "ic": f"{_fmt(b)} - {_fmt(a)}x", "min_deriv": -a, "t_s": t_s,
        }

    def _sinusoidal_ic(self, difficulty: int) -> tuple[str, dict]:
        """Generate with u_0(x) = -sin(pi*x).

        u_0'(x) = -pi*cos(pi*x), min = -pi at x=0, t_s = 1/pi.

        Args:
            difficulty: Controls variant.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        t_s = 1.0 / math.pi
        problem = (
            "u_t + u*u_x = 0, u_0(x) = -sin(pi*x). Shock time?"
        )
        return problem, {
            "ic": "-sin(pi*x)", "min_deriv": -math.pi, "t_s": t_s,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate shock formation analysis steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing characteristic analysis.
        """
        return [
            "characteristics: dx/dt = u, u constant along chars",
            f"u_0(x) = {data['ic']}",
            f"min(u_0'(x)) = {_fmt(data['min_deriv'])}",
            f"t_s = -1/min(u_0') = {_fmt(data['t_s'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the shock formation time.

        Args:
            data: Solution data.

        Returns:
            Shock time value.
        """
        return f"t_s = {_fmt(data['t_s'])}"


# =====================================================================
# 6. FEM 1D (tier 6)
# =====================================================================

@register
class FEM1DGenerator(StepGenerator):
    """Assemble the 1D finite element stiffness matrix for -u'' = f.

    Uses linear hat functions on [0,1] with uniform mesh of n elements.
    Stiffness matrix entries: K_{ii} = 2/h, K_{i,i+1} = K_{i+1,i} = -1/h.

    Difficulty scaling:
        Difficulty 1-3: 2-3 elements.
        Difficulty 4-6: 3-4 elements, compute load vector for f=1.
        Difficulty 7-8: 4-5 elements, solve the system.

    Prerequisites:
        finite_difference (tier 6).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "fem_1d"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["finite_difference"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls mesh size.

        Returns:
            Task description string.
        """
        return "assemble 1D FEM stiffness matrix for -u'' = f"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a 1D FEM assembly problem.

        Args:
            difficulty: Controls number of elements.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            n_elem = self._rng.choice([2, 3])
        elif difficulty <= 6:
            n_elem = self._rng.choice([3, 4])
        else:
            n_elem = self._rng.choice([4, 5])

        h = 1.0 / n_elem
        n_interior = n_elem - 1

        diag = round(2.0 / h, 4)
        off = round(-1.0 / h, 4)

        load = [round(h, 4)] * n_interior

        problem = (
            f"-u'' = 1 on [0,1], u(0)=u(1)=0, {n_elem} elements. "
            f"Assemble K."
        )
        return problem, {
            "n_elem": n_elem, "h": h, "n_interior": n_interior,
            "diag": diag, "off": off, "load": load,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate FEM assembly steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing stiffness matrix assembly.
        """
        steps = [
            f"mesh: {data['n_elem']} elements, h = {_fmt(data['h'])}",
            f"hat functions: phi_i linear, support [x_{{i-1}}, x_{{i+1}}]",
            f"K_{{ii}} = 2/h = {_fmt(data['diag'])}",
            f"K_{{i,i+1}} = -1/h = {_fmt(data['off'])}",
            f"interior nodes: {data['n_interior']}",
        ]
        if data["load"]:
            load_str = ", ".join(_fmt(v) for v in data["load"])
            steps.append(f"load vector (f=1): [{load_str}]")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the stiffness matrix parameters.

        Args:
            data: Solution data.

        Returns:
            Matrix diagonal and off-diagonal values.
        """
        return (
            f"K: {data['n_interior']}x{data['n_interior']}, "
            f"diag={_fmt(data['diag'])}, off={_fmt(data['off'])}"
        )


# =====================================================================
# 7. STABILITY CFL (tier 6)
# =====================================================================

@register
class StabilityCFLGenerator(StepGenerator):
    """Determine the maximum stable time step from the CFL condition.

    For explicit schemes: c*dt/dx <= C_max (usually C_max = 1).
    Given wave speed c and spatial step dx, find max dt.

    Difficulty scaling:
        Difficulty 1-3: simple integer c, dx.
        Difficulty 4-6: fractional dx, verify stability.
        Difficulty 7-8: 2D CFL condition.

    Prerequisites:
        division (tier 1).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "stability_cfl"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["division"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls parameter complexity.

        Returns:
            Task description string.
        """
        return "find maximum stable time step from CFL condition"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a CFL stability problem.

        Args:
            difficulty: Controls parameters.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 5:
            return self._cfl_1d(difficulty)
        return self._cfl_2d(difficulty)

    def _cfl_1d(self, difficulty: int) -> tuple[str, dict]:
        """Generate 1D CFL condition problem.

        Args:
            difficulty: Controls c and dx.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        c = float(self._rng.randint(1, 5))
        if difficulty <= 3:
            dx = round(1.0 / self._rng.randint(2, 5), 4)
        else:
            dx = round(1.0 / self._rng.randint(4, 10), 4)

        dt_max = dx / c
        given_dt = round(dt_max * self._rng.choice([0.5, 0.8, 1.0, 1.2]), 4)
        cfl_number = c * given_dt / dx
        stable = cfl_number <= 1.0 + 1e-10

        problem = (
            f"explicit scheme, c={_fmt(c)}, dx={_fmt(dx)}. "
            f"Max dt for CFL <= 1?"
        )
        return problem, {
            "c": c, "dx": dx, "dt_max": dt_max,
            "given_dt": given_dt, "cfl_number": cfl_number,
            "stable": stable, "dim": 1,
        }

    def _cfl_2d(self, difficulty: int) -> tuple[str, dict]:
        """Generate 2D CFL condition problem.

        CFL in 2D: c*dt*(1/dx + 1/dy) <= 1.

        Args:
            difficulty: Controls parameters.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        c = float(self._rng.randint(1, 3))
        dx = round(1.0 / self._rng.randint(4, 8), 4)
        dy = round(1.0 / self._rng.randint(4, 8), 4)
        dt_max = 1.0 / (c * (1.0 / dx + 1.0 / dy))

        problem = (
            f"2D explicit scheme, c={_fmt(c)}, dx={_fmt(dx)}, "
            f"dy={_fmt(dy)}. Max dt?"
        )
        return problem, {
            "c": c, "dx": dx, "dy": dy, "dt_max": dt_max,
            "given_dt": 0.0, "cfl_number": 1.0,
            "stable": True, "dim": 2,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate CFL analysis steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing CFL computation.
        """
        if data["dim"] == 1:
            return [
                f"CFL: c*dt/dx <= 1",
                f"c={_fmt(data['c'])}, dx={_fmt(data['dx'])}",
                f"dt_max = dx/c = {_fmt(data['dt_max'])}",
            ]
        return [
            "2D CFL: c*dt*(1/dx + 1/dy) <= 1",
            f"c={_fmt(data['c'])}, dx={_fmt(data['dx'])}, dy={_fmt(data.get('dy', 0))}",
            f"dt_max = 1/(c*(1/dx+1/dy)) = {_fmt(data['dt_max'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the maximum time step.

        Args:
            data: Solution data.

        Returns:
            Maximum stable dt.
        """
        return f"dt_max = {_fmt(data['dt_max'])}"


# =====================================================================
# 8. SPECTRAL METHOD (tier 7)
# =====================================================================

@register
class SpectralMethodGenerator(StepGenerator):
    """Solve a PDE using Fourier spectral methods.

    Expand u in Fourier modes: u = sum u_hat_k * e^{ikx}. The PDE
    becomes an ODE for each mode u_hat_k. Demonstrates for the heat
    equation and wave equation.

    Difficulty scaling:
        Difficulty 1-3: heat equation, first 2 modes.
        Difficulty 4-6: heat equation, 3-4 modes with decay.
        Difficulty 7-8: wave equation in spectral form.

    Prerequisites:
        heat_equation (tier 6).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "spectral_method"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["heat_equation"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls number of modes.

        Returns:
            Task description string.
        """
        return "solve PDE using Fourier spectral method"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a spectral method problem.

        Args:
            difficulty: Controls number of modes and PDE type.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 6:
            return self._heat_spectral(difficulty)
        return self._wave_spectral(difficulty)

    def _heat_spectral(self, difficulty: int) -> tuple[str, dict]:
        """Generate spectral method for heat equation.

        u_t = kappa * u_xx => du_hat_k/dt = -kappa*k^2*u_hat_k.
        Solution: u_hat_k(t) = u_hat_k(0)*exp(-kappa*k^2*t).

        Args:
            difficulty: Controls number of modes.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        kappa = float(self._rng.randint(1, 3))
        if difficulty <= 3:
            n_modes = 2
        else:
            n_modes = self._rng.randint(3, 4)

        t0 = round(self._rng.choice([0.1, 0.5, 1.0]), 4)
        modes = []
        for k in range(1, n_modes + 1):
            u0_k = round(float(self._rng.randint(1, 4)) / k, 4)
            decay = round(math.exp(-kappa * k ** 2 * t0), 4)
            u_t_k = round(u0_k * decay, 4)
            modes.append({
                "k": k, "u0_k": u0_k, "decay": decay, "u_t_k": u_t_k,
            })

        problem = (
            f"u_t = {_fmt(kappa)}*u_xx, spectral. "
            f"Mode amplitudes at t={_fmt(t0)}?"
        )
        return problem, {
            "pde": "heat", "kappa": kappa, "t0": t0, "modes": modes,
        }

    def _wave_spectral(self, difficulty: int) -> tuple[str, dict]:
        """Generate spectral method for wave equation.

        u_tt = c^2*u_xx => d^2u_hat_k/dt^2 = -c^2*k^2*u_hat_k.
        Solution: u_hat_k(t) = A_k*cos(ckt) + B_k*sin(ckt).

        Args:
            difficulty: Controls number of modes.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        c = float(self._rng.randint(1, 3))
        n_modes = self._rng.randint(2, 3)
        t0 = round(self._rng.choice([0.25, 0.5, 1.0]), 4)

        modes = []
        for k in range(1, n_modes + 1):
            a_k = round(float(self._rng.randint(0, 3)), 4)
            b_k = round(float(self._rng.randint(0, 2)), 4)
            omega_k = c * k
            u_t_k = round(
                a_k * math.cos(omega_k * t0) + b_k * math.sin(omega_k * t0),
                4,
            )
            modes.append({
                "k": k, "a_k": a_k, "b_k": b_k,
                "omega_k": omega_k, "u_t_k": u_t_k,
                "u0_k": a_k, "decay": 0.0,
            })

        problem = (
            f"u_tt = {_fmt(c)}^2*u_xx, spectral. "
            f"Mode amplitudes at t={_fmt(t0)}?"
        )
        return problem, {
            "pde": "wave", "c": c, "t0": t0, "modes": modes,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate spectral method solution steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing mode-by-mode solution.
        """
        steps = []
        if data["pde"] == "heat":
            steps.append("u_t = kappa*u_xx => du_hat_k/dt = -kappa*k^2*u_hat_k")
            for mode in data["modes"]:
                steps.append(
                    f"k={mode['k']}: u_hat(0)={_fmt(mode['u0_k'])}, "
                    f"decay={_fmt(mode['decay'])}, "
                    f"u_hat(t)={_fmt(mode['u_t_k'])}"
                )
        else:
            steps.append("u_tt = c^2*u_xx => d^2u_hat/dt^2 = -c^2*k^2*u_hat")
            for mode in data["modes"]:
                steps.append(
                    f"k={mode['k']}: w_k={_fmt(mode['omega_k'])}, "
                    f"u_hat(t)={_fmt(mode['u_t_k'])}"
                )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the mode amplitudes at time t.

        Args:
            data: Solution data.

        Returns:
            Mode amplitudes.
        """
        parts = [
            f"u_hat_{m['k']}={_fmt(m['u_t_k'])}" for m in data["modes"]
        ]
        return ", ".join(parts)
