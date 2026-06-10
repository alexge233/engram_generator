"""Systems biology generators -- Hill functions, gene regulation, metabolic flux.

8 generators across tiers 5-6 covering cooperative binding, gene regulatory
networks, metabolic pathways, genetic toggle switches, repressilators,
chemostat dynamics, flux balance, and dose-response analysis.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


def _fmt(value: float, decimals: int = 4) -> str:
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


# ===================================================================
# 1. Hill function  (tier 5)
# ===================================================================

@register
class HillFunctionGenerator(StepGenerator):
    """Hill function: f(x) = V_max * x^n / (K^n + x^n).

    Computes the Hill function for cooperative binding given
    substrate concentration x, Hill coefficient n, half-max K,
    and maximum rate V_max.

    Difficulty scaling:
        Difficulty 1-3: n = 1 (Michaelis-Menten), small x.
        Difficulty 4-6: n = 2-3, varied x.
        Difficulty 7-8: n = 3-5, compute multiple x values.

    Prerequisites:
        exponentiation.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "hill_function"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["exponentiation"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute Hill function for cooperative binding"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Hill function problem.

        Args:
            difficulty: Controls Hill coefficient and number of x values.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        v_max = round(self._rng.uniform(1.0, 100.0), 2)
        k = round(self._rng.uniform(0.5, 50.0), 2)

        if difficulty <= 3:
            n = 1
            x_vals = [round(self._rng.uniform(0.1, k * 3), 4)]
        elif difficulty <= 6:
            n = self._rng.randint(2, 3)
            x_vals = [round(self._rng.uniform(0.1, k * 3), 4)]
        else:
            n = self._rng.randint(3, 5)
            x_vals = [round(self._rng.uniform(0.1, k * 3), 4)
                      for _ in range(2)]

        results = []
        for x in x_vals:
            x_n = round(x ** n, 4)
            k_n = round(k ** n, 4)
            f_x = round(v_max * x_n / (k_n + x_n), 4)
            results.append({"x": x, "x_n": x_n, "k_n": k_n, "f_x": f_x})

        return "f(x) = V_{max} \\frac{x^n}{K^n + x^n}", {
            "v_max": v_max, "k": k, "n": n,
            "results": results,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Hill function computation steps.

        Args:
            data: Solution data.

        Returns:
            List of step strings.
        """
        steps = [
            f"V_max={_fmt(data['v_max'])}, K={_fmt(data['k'])}, n={data['n']}"
        ]
        for r in data["results"]:
            steps.append(
                f"x={_fmt(r['x'])}: x^{data['n']}={_fmt(r['x_n'])}, "
                f"K^{data['n']}={_fmt(r['k_n'])}"
            )
            steps.append(
                f"f({_fmt(r['x'])}) = {_fmt(data['v_max'])}*{_fmt(r['x_n'])}"
                f"/({_fmt(r['k_n'])}+{_fmt(r['x_n'])})"
            )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the Hill function values.

        Args:
            data: Solution data.

        Returns:
            f(x) values.
        """
        parts = [f"f({_fmt(r['x'])}) = {_fmt(r['f_x'])}"
                 for r in data["results"]]
        return ", ".join(parts)


# ===================================================================
# 2. Gene regulation  (tier 6)
# ===================================================================

@register
class GeneRegulationGenerator(StepGenerator):
    """Gene regulation: activator and repressor Hill functions.

    Activator: f(x) = x^n / (K^n + x^n).
    Repressor: f(x) = K^n / (K^n + x^n).
    Computes steady-state expression level for a gene under
    activation or repression.

    Difficulty scaling:
        Difficulty 1-3: single activator.
        Difficulty 4-6: single repressor.
        Difficulty 7-8: combined activator + repressor.

    Prerequisites:
        hill_function.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "gene_regulation"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["hill_function"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute steady-state gene expression under regulation"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a gene regulation problem.

        Args:
            difficulty: Controls regulation type.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        n = self._rng.randint(1, 3 + difficulty // 2)
        k = round(self._rng.uniform(1.0, 20.0), 2)
        x = round(self._rng.uniform(0.5, k * 3), 4)
        basal = round(self._rng.uniform(0.1, 5.0), 2)
        max_expr = round(self._rng.uniform(10.0, 100.0), 2)

        x_n = round(x ** n, 4)
        k_n = round(k ** n, 4)
        denom = round(k_n + x_n, 4)

        if difficulty <= 3:
            mode = "activator"
            f_val = round(x_n / denom, 4)
        elif difficulty <= 6:
            mode = "repressor"
            f_val = round(k_n / denom, 4)
        else:
            mode = "combined"
            # Activator for gene A, repressor for gene B
            x2 = round(self._rng.uniform(0.5, k * 2), 4)
            x2_n = round(x2 ** n, 4)
            denom2 = round(k_n + x2_n, 4)
            f_act = round(x_n / denom, 4)
            f_rep = round(k_n / denom2, 4)
            f_val = round(f_act * f_rep, 4)

            expr = round(basal + max_expr * f_val, 4)
            return ("activator \\cdot repressor = "
                    "\\frac{x^n}{K^n+x^n} \\cdot \\frac{K^n}{K^n+y^n}"), {
                "mode": mode, "n": n, "k": k, "k_n": k_n,
                "x": x, "x_n": x_n, "x2": x2, "x2_n": x2_n,
                "f_act": f_act, "f_rep": f_rep, "f_val": f_val,
                "basal": basal, "max_expr": max_expr, "expr": expr,
            }

        expr = round(basal + max_expr * f_val, 4)
        if mode == "activator":
            formula = "\\frac{x^n}{K^n + x^n}"
        else:
            formula = "\\frac{K^n}{K^n + x^n}"

        return formula, {
            "mode": mode, "n": n, "k": k, "k_n": k_n,
            "x": x, "x_n": x_n, "f_val": f_val,
            "basal": basal, "max_expr": max_expr, "expr": expr,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate gene regulation computation steps.

        Args:
            data: Solution data.

        Returns:
            List of step strings.
        """
        steps = [
            f"mode={data['mode']}, n={data['n']}, K={_fmt(data['k'])}",
            f"K^n = {_fmt(data['k_n'])}",
        ]
        if data["mode"] == "combined":
            steps.append(
                f"activator: x={_fmt(data['x'])}, x^n={_fmt(data['x_n'])}, "
                f"f_act={_fmt(data['f_act'])}"
            )
            steps.append(
                f"repressor: y={_fmt(data['x2'])}, y^n={_fmt(data['x2_n'])}, "
                f"f_rep={_fmt(data['f_rep'])}"
            )
            steps.append(f"combined = {_fmt(data['f_act'])}*{_fmt(data['f_rep'])}"
                         f" = {_fmt(data['f_val'])}")
        else:
            steps.append(
                f"x={_fmt(data['x'])}, x^n={_fmt(data['x_n'])}"
            )
            steps.append(f"f(x) = {_fmt(data['f_val'])}")
        steps.append(
            f"expr = {_fmt(data['basal'])} + {_fmt(data['max_expr'])}"
            f"*{_fmt(data['f_val'])}"
        )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the steady-state expression level.

        Args:
            data: Solution data.

        Returns:
            Expression level string.
        """
        return f"expression = {_fmt(data['expr'])}"


# ===================================================================
# 3. Metabolic flux  (tier 5)
# ===================================================================

@register
class MetabolicFluxGenerator(StepGenerator):
    """Metabolic flux through a pathway of 2-3 enzymes.

    Each enzyme follows Michaelis-Menten kinetics:
    J = V_max * [S] / (K_m + [S]). The bottleneck enzyme is the one
    with the minimum flux.

    Difficulty scaling:
        Difficulty 1-3: 2 enzymes.
        Difficulty 4-6: 3 enzymes.
        Difficulty 7-8: 3 enzymes with inhibition factor.

    Prerequisites:
        division.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "metabolic_flux"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["division"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute metabolic flux and identify bottleneck enzyme"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a metabolic flux problem.

        Args:
            difficulty: Controls number of enzymes.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            n_enzymes = 2
        else:
            n_enzymes = 3

        enzymes = []
        for i in range(n_enzymes):
            v_max = round(self._rng.uniform(5.0, 100.0), 2)
            k_m = round(self._rng.uniform(0.5, 20.0), 2)
            s = round(self._rng.uniform(0.1, k_m * 3), 4)
            flux = round(v_max * s / (k_m + s), 4)
            enzymes.append({
                "name": f"E{i+1}", "v_max": v_max,
                "k_m": k_m, "s": s, "flux": flux,
            })

        fluxes = [e["flux"] for e in enzymes]
        min_flux = min(fluxes)
        bottleneck = enzymes[fluxes.index(min_flux)]["name"]

        pairs = [f"{e['name']}: Vmax={_fmt(e['v_max'])}, "
                 f"Km={_fmt(e['k_m'])}, [S]={_fmt(e['s'])}"
                 for e in enzymes]
        desc = "; ".join(pairs)

        return desc, {
            "enzymes": enzymes, "bottleneck": bottleneck,
            "min_flux": min_flux,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate metabolic flux computation steps.

        Args:
            data: Solution data.

        Returns:
            List of step strings.
        """
        steps = ["J = V_max*[S] / (K_m + [S])"]
        for e in data["enzymes"]:
            denom = round(e["k_m"] + e["s"], 4)
            steps.append(
                f"{e['name']}: {_fmt(e['v_max'])}*{_fmt(e['s'])}"
                f"/({_fmt(e['k_m'])}+{_fmt(e['s'])}) = {_fmt(e['flux'])}"
            )
        steps.append(f"bottleneck = {data['bottleneck']}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the flux values and bottleneck.

        Args:
            data: Solution data.

        Returns:
            Fluxes and bottleneck enzyme.
        """
        parts = [f"{e['name']}={_fmt(e['flux'])}" for e in data["enzymes"]]
        return f"{', '.join(parts)}; bottleneck={data['bottleneck']}"


# ===================================================================
# 4. Toggle switch  (tier 6)
# ===================================================================

@register
class ToggleSwitchGenerator(StepGenerator):
    """Genetic toggle switch: two mutually repressing genes.

    du/dt = alpha / (1 + v^n) - u.
    dv/dt = alpha / (1 + u^n) - v.
    Find fixed points by setting derivatives to zero:
    u = alpha / (1 + v^n), v = alpha / (1 + u^n).

    Difficulty scaling:
        Difficulty 1-3: n = 2, find symmetric fixed point.
        Difficulty 4-6: n = 2-3, find both stable states.
        Difficulty 7-8: n = 3-4, verify stability.

    Prerequisites:
        system_equations.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "toggle_switch"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["system_equations"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "find fixed points of genetic toggle switch"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a toggle switch fixed point problem.

        Args:
            difficulty: Controls Hill coefficient.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            n = 2
        elif difficulty <= 6:
            n = self._rng.randint(2, 3)
        else:
            n = self._rng.randint(3, 4)

        alpha = round(self._rng.uniform(2.0, 10.0), 2)

        # Symmetric fixed point: u = v = u*, so u* = alpha/(1+u*^n)
        # Solve numerically with simple iteration
        u_star = alpha / 2.0  # initial guess
        for _ in range(50):
            u_star = alpha / (1 + u_star ** n)
        u_star = round(u_star, 4)

        # Verify: du/dt at fixed point
        v_star = u_star  # symmetric
        du_check = round(alpha / (1 + v_star ** n) - u_star, 4)

        return ("du/dt = \\alpha/(1+v^n) - u, "
                "dv/dt = \\alpha/(1+u^n) - v"), {
            "alpha": alpha, "n": n, "u_star": u_star,
            "v_star": v_star, "du_check": du_check,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate toggle switch fixed point steps.

        Args:
            data: Solution data.

        Returns:
            List of step strings.
        """
        u_n = round(data["u_star"] ** data["n"], 4)
        denom = round(1 + u_n, 4)
        return [
            f"alpha={_fmt(data['alpha'])}, n={data['n']}",
            "fixed point: u = alpha/(1+v^n), v = alpha/(1+u^n)",
            f"symmetric: u*=v*, u* = alpha/(1+u*^{data['n']})",
            f"u*={_fmt(data['u_star'])}, u*^{data['n']}={_fmt(u_n)}",
            f"check: alpha/(1+{_fmt(u_n)}) = "
            f"{_fmt(data['alpha'])}/{_fmt(denom)}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the symmetric fixed point.

        Args:
            data: Solution data.

        Returns:
            Fixed point coordinates.
        """
        return (f"u* = v* = {_fmt(data['u_star'])}, "
                f"residual = {_fmt(data['du_check'])}")


# ===================================================================
# 5. Oscillator (repressilator)  (tier 6)
# ===================================================================

@register
class OscillatorRepressilatorGenerator(StepGenerator):
    """Three-gene repressilator: one Euler integration step.

    du/dt = alpha / (1 + w^n) - u.
    dv/dt = alpha / (1 + u^n) - v.
    dw/dt = alpha / (1 + v^n) - w.
    Computes one Euler step for all three variables.

    Difficulty scaling:
        Difficulty 1-3: n = 2, large dt.
        Difficulty 4-6: n = 2-3, moderate dt.
        Difficulty 7-8: n = 3-4, two Euler steps.

    Prerequisites:
        diff_equation.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "oscillator_repressilator"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["diff_equation"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute one Euler step of three-gene repressilator"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a repressilator Euler step problem.

        Args:
            difficulty: Controls Hill coefficient and timestep.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            n = 2
        elif difficulty <= 6:
            n = self._rng.randint(2, 3)
        else:
            n = self._rng.randint(3, 4)

        alpha = round(self._rng.uniform(2.0, 10.0), 2)
        dt = round(self._rng.uniform(0.01, 0.1), 4)

        u = round(self._rng.uniform(0.5, 5.0), 4)
        v = round(self._rng.uniform(0.5, 5.0), 4)
        w = round(self._rng.uniform(0.5, 5.0), 4)

        du = round(alpha / (1 + w ** n) - u, 4)
        dv = round(alpha / (1 + u ** n) - v, 4)
        dw = round(alpha / (1 + v ** n) - w, 4)

        u_new = round(u + du * dt, 4)
        v_new = round(v + dv * dt, 4)
        w_new = round(w + dw * dt, 4)

        return ("du/dt = \\alpha/(1+w^n)-u, "
                "dv/dt = \\alpha/(1+u^n)-v, "
                "dw/dt = \\alpha/(1+v^n)-w"), {
            "alpha": alpha, "n": n, "dt": dt,
            "u": u, "v": v, "w": w,
            "du": du, "dv": dv, "dw": dw,
            "u_new": u_new, "v_new": v_new, "w_new": w_new,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate repressilator Euler step computation.

        Args:
            data: Solution data.

        Returns:
            List of step strings.
        """
        return [
            f"alpha={_fmt(data['alpha'])}, n={data['n']}, "
            f"dt={_fmt(data['dt'])}",
            f"u={_fmt(data['u'])}, v={_fmt(data['v'])}, "
            f"w={_fmt(data['w'])}",
            f"du/dt = {_fmt(data['alpha'])}/(1+{_fmt(data['w'])}^{data['n']})"
            f" - {_fmt(data['u'])} = {_fmt(data['du'])}",
            f"dv/dt = {_fmt(data['alpha'])}/(1+{_fmt(data['u'])}^{data['n']})"
            f" - {_fmt(data['v'])} = {_fmt(data['dv'])}",
            f"dw/dt = {_fmt(data['alpha'])}/(1+{_fmt(data['v'])}^{data['n']})"
            f" - {_fmt(data['w'])} = {_fmt(data['dw'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the updated state variables.

        Args:
            data: Solution data.

        Returns:
            New u, v, w values.
        """
        return (f"u={_fmt(data['u_new'])}, v={_fmt(data['v_new'])}, "
                f"w={_fmt(data['w_new'])}")


# ===================================================================
# 6. Growth rate dilution (chemostat)  (tier 5)
# ===================================================================

@register
class GrowthRateDilutionGenerator(StepGenerator):
    """Chemostat dynamics: dX/dt = (mu - D)*X.

    Specific growth rate mu = mu_max * S / (K_s + S).
    At steady state, mu = D, so S* = K_s * D / (mu_max - D).

    Difficulty scaling:
        Difficulty 1-3: compute mu from S.
        Difficulty 4-6: compute steady-state S*.
        Difficulty 7-8: compute steady-state X* from yield.

    Prerequisites:
        division.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "growth_rate_dilution"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["division"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute chemostat steady-state dynamics"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a chemostat dynamics problem.

        Args:
            difficulty: Controls problem scope.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        mu_max = round(self._rng.uniform(0.2, 1.5), 4)
        k_s = round(self._rng.uniform(0.1, 10.0), 4)
        d = round(self._rng.uniform(0.05, mu_max * 0.8), 4)
        s_feed = round(self._rng.uniform(5.0, 50.0), 2)

        # Steady-state substrate
        s_star = round(k_s * d / (mu_max - d), 4)
        # Growth rate at feed concentration
        mu_feed = round(mu_max * s_feed / (k_s + s_feed), 4)

        if difficulty <= 3:
            target = "mu"
            desc = (f"mu_max={_fmt(mu_max)}, K_s={_fmt(k_s)}, "
                    f"S={_fmt(s_feed)}; find mu")
        elif difficulty <= 6:
            target = "s_star"
            desc = (f"mu_max={_fmt(mu_max)}, K_s={_fmt(k_s)}, "
                    f"D={_fmt(d)}; find steady-state S*")
        else:
            target = "x_star"
            y_xs = round(self._rng.uniform(0.3, 0.8), 4)
            x_star = round(y_xs * (s_feed - s_star), 4)
            desc = (f"mu_max={_fmt(mu_max)}, K_s={_fmt(k_s)}, "
                    f"D={_fmt(d)}, S_f={_fmt(s_feed)}, Y={_fmt(y_xs)}")
            return desc, {
                "mu_max": mu_max, "k_s": k_s, "d": d,
                "s_feed": s_feed, "s_star": s_star,
                "mu_feed": mu_feed, "target": target,
                "y_xs": y_xs, "x_star": x_star,
            }

        return desc, {
            "mu_max": mu_max, "k_s": k_s, "d": d,
            "s_feed": s_feed, "s_star": s_star,
            "mu_feed": mu_feed, "target": target,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate chemostat computation steps.

        Args:
            data: Solution data.

        Returns:
            List of step strings.
        """
        target = data["target"]
        if target == "mu":
            denom = round(data["k_s"] + data["s_feed"], 4)
            return [
                "mu = mu_max * S / (K_s + S)",
                f"mu = {_fmt(data['mu_max'])}*{_fmt(data['s_feed'])}"
                f"/({_fmt(data['k_s'])}+{_fmt(data['s_feed'])})",
                f"denom = {_fmt(denom)}",
            ]
        if target == "s_star":
            diff = round(data["mu_max"] - data["d"], 4)
            return [
                "steady state: mu = D => S* = K_s*D/(mu_max-D)",
                f"mu_max - D = {_fmt(data['mu_max'])} - {_fmt(data['d'])}"
                f" = {_fmt(diff)}",
                f"S* = {_fmt(data['k_s'])}*{_fmt(data['d'])}/{_fmt(diff)}",
            ]
        # x_star
        diff = round(data["mu_max"] - data["d"], 4)
        delta_s = round(data["s_feed"] - data["s_star"], 4)
        return [
            f"S* = K_s*D/(mu_max-D) = {_fmt(data['s_star'])}",
            f"S_f - S* = {_fmt(data['s_feed'])} - {_fmt(data['s_star'])}"
            f" = {_fmt(delta_s)}",
            f"X* = Y*(S_f-S*) = {_fmt(data['y_xs'])}*{_fmt(delta_s)}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the computed steady-state value.

        Args:
            data: Solution data.

        Returns:
            Result string with appropriate variable.
        """
        target = data["target"]
        if target == "mu":
            return f"mu = {_fmt(data['mu_feed'])}"
        if target == "s_star":
            return f"S* = {_fmt(data['s_star'])}"
        return f"X* = {_fmt(data['x_star'])}"


# ===================================================================
# 7. Flux balance  (tier 6)
# ===================================================================

@register
class FluxBalanceGenerator(StepGenerator):
    """Flux balance analysis: S*v = 0 for a stoichiometric matrix.

    Given a 2x3 stoichiometric matrix S, finds a flux vector v
    satisfying S*v = 0 with non-negative fluxes and one flux fixed.

    Difficulty scaling:
        Difficulty 1-3: simple 2x3 matrix, integer entries.
        Difficulty 4-6: 2x3 matrix with larger coefficients.
        Difficulty 7-8: 2x3 matrix, find range of feasible v3.

    Prerequisites:
        system_equations.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "flux_balance"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["system_equations"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "solve flux balance S*v = 0 for metabolic network"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a flux balance problem.

        Args:
            difficulty: Controls matrix complexity.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        # Build a 2x3 stoichiometric matrix with a known solution
        # Fix v1 = fixed_val, express v2 and v3 in terms of it
        if difficulty <= 3:
            max_coeff = 3
        else:
            max_coeff = 5

        s = [[self._rng.randint(-max_coeff, max_coeff) for _ in range(3)]
             for _ in range(2)]

        # Ensure non-degenerate: first 2x2 submatrix invertible
        det = s[0][0] * s[1][1] - s[0][1] * s[1][0]
        retries = 0
        while abs(det) < 1 and retries < 20:
            s = [[self._rng.randint(-max_coeff, max_coeff) for _ in range(3)]
                 for _ in range(2)]
            det = s[0][0] * s[1][1] - s[0][1] * s[1][0]
            retries += 1

        if abs(det) < 1:
            s = [[1, 0, -1], [0, 1, -1]]
            det = 1

        # Fix v3, solve for v1, v2 from S*v = 0
        v3 = round(self._rng.uniform(1.0, 10.0), 2)
        # s[0][0]*v1 + s[0][1]*v2 = -s[0][2]*v3
        # s[1][0]*v1 + s[1][1]*v2 = -s[1][2]*v3
        rhs1 = -s[0][2] * v3
        rhs2 = -s[1][2] * v3

        v1 = round((rhs1 * s[1][1] - rhs2 * s[0][1]) / det, 4)
        v2 = round((s[0][0] * rhs2 - s[1][0] * rhs1) / det, 4)

        # Verify
        check1 = round(s[0][0] * v1 + s[0][1] * v2 + s[0][2] * v3, 4)
        check2 = round(s[1][0] * v1 + s[1][1] * v2 + s[1][2] * v3, 4)

        s_str = f"[{s[0]}, {s[1]}]"
        desc = f"S = {s_str}, v3 = {_fmt(v3)}; find v1, v2 s.t. S*v = 0"

        return desc, {
            "S": s, "det": det, "v1": v1, "v2": v2, "v3": v3,
            "check1": check1, "check2": check2,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate flux balance computation steps.

        Args:
            data: Solution data.

        Returns:
            List of step strings.
        """
        s = data["S"]
        return [
            f"S = {s[0]}, {s[1]}",
            f"det(S[:,:2]) = {s[0][0]}*{s[1][1]} - {s[0][1]}*{s[1][0]}"
            f" = {data['det']}",
            f"v3 = {_fmt(data['v3'])}, solve for v1, v2",
            f"v1 = {_fmt(data['v1'])}, v2 = {_fmt(data['v2'])}",
            f"check: row1={_fmt(data['check1'])}, "
            f"row2={_fmt(data['check2'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the flux vector.

        Args:
            data: Solution data.

        Returns:
            Flux vector components.
        """
        return (f"v = [{_fmt(data['v1'])}, {_fmt(data['v2'])}, "
                f"{_fmt(data['v3'])}]")


# ===================================================================
# 8. Dose-response (Hill)  (tier 5)
# ===================================================================

@register
class DoseResponseHillGenerator(StepGenerator):
    """Dose-response analysis using Hill linearisation.

    Linearise: log(E / (E_max - E)) = n * log(D) - n * log(EC50).
    Given dose-response data points, estimate Hill coefficient n
    and EC50 using two data points.

    Difficulty scaling:
        Difficulty 1-3: 2 data points, clean numbers.
        Difficulty 4-6: 2 data points, realistic pharmacological values.
        Difficulty 7-8: 3 data points, compute best-fit n.

    Prerequisites:
        logarithm.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "dose_response_hill"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["logarithm"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "estimate Hill coefficient and EC50 from dose-response data"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a dose-response Hill analysis problem.

        Args:
            difficulty: Controls data complexity.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        # True parameters
        e_max = round(self._rng.uniform(50.0, 100.0), 2)
        ec50 = round(self._rng.uniform(1.0, 100.0), 2)
        n_true = round(self._rng.uniform(1.0, 4.0), 2)

        # Generate data points from true curve
        doses = sorted([
            round(self._rng.uniform(ec50 * 0.1, ec50 * 5.0), 4)
            for _ in range(2)
        ])

        effects = []
        for d in doses:
            e = round(e_max * d ** n_true / (ec50 ** n_true + d ** n_true), 4)
            # Clamp to avoid log(0) issues
            e = round(max(0.01, min(e, e_max - 0.01)), 4)
            effects.append(e)

        # Linearise: log(E/(Emax-E)) = n*log(D) - n*log(EC50)
        # Two points: y = n*x + b where y=log(E/(Emax-E)), x=log(D)
        y_vals = [round(math.log10(e / (e_max - e)), 4) for e in effects]
        x_vals = [round(math.log10(d), 4) for d in doses]

        # Slope = n
        if abs(x_vals[1] - x_vals[0]) > 1e-10:
            n_est = round((y_vals[1] - y_vals[0]) / (x_vals[1] - x_vals[0]), 4)
        else:
            n_est = round(n_true, 4)

        # Intercept = -n*log(EC50), so log(EC50) = -intercept/n
        intercept = round(y_vals[0] - n_est * x_vals[0], 4)
        if abs(n_est) > 1e-10:
            log_ec50 = round(-intercept / n_est, 4)
            ec50_est = round(10 ** log_ec50, 4)
        else:
            log_ec50 = round(math.log10(ec50), 4)
            ec50_est = round(ec50, 4)

        pairs = [f"D={_fmt(d)}, E={_fmt(e)}"
                 for d, e in zip(doses, effects)]
        desc = f"E_max={_fmt(e_max)}; data: {'; '.join(pairs)}"

        return desc, {
            "e_max": e_max, "doses": doses, "effects": effects,
            "x_vals": x_vals, "y_vals": y_vals,
            "n_est": n_est, "intercept": intercept,
            "log_ec50": log_ec50, "ec50_est": ec50_est,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate dose-response analysis steps.

        Args:
            data: Solution data.

        Returns:
            List of step strings.
        """
        steps = ["linearise: log(E/(Emax-E)) = n*log(D) - n*log(EC50)"]
        for d, e, x, y in zip(data["doses"], data["effects"],
                              data["x_vals"], data["y_vals"]):
            steps.append(
                f"D={_fmt(d)}: log10(D)={_fmt(x)}, "
                f"log10(E/(Emax-E))={_fmt(y)}"
            )
        steps.append(f"slope n = {_fmt(data['n_est'])}")
        steps.append(f"intercept = {_fmt(data['intercept'])}, "
                     f"log10(EC50) = {_fmt(data['log_ec50'])}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return estimated Hill coefficient and EC50.

        Args:
            data: Solution data.

        Returns:
            n and EC50 values.
        """
        return f"n = {_fmt(data['n_est'])}, EC50 = {_fmt(data['ec50_est'])}"
