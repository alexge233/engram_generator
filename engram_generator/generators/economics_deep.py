"""Deep economics generators -- macro, micro, and econometrics.

8 generators across tiers 4-6 covering IS-LM model, Solow growth,
Phillips curve, option Greeks, present value of annuities,
Bertrand oligopoly, adverse selection, and moral hazard.
"""
from __future__ import annotations

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
    if isinstance(rounded, float) and rounded == int(rounded):
        return str(int(rounded))
    return str(rounded)


# ===================================================================
# 1. IS-LM Model  (tier 5)
# ===================================================================

@register
class ISLMModelGenerator(StepGenerator):
    """Solve for equilibrium output and interest rate in the IS-LM model.

    IS curve: Y = C_0 + c*(Y - T) + I_0 - b*r + G.
    LM curve: M/P = d*Y - e*r.
    Solve the 2-equation system for Y* and r*.

    Difficulty scaling:
        Difficulty 1-3: simple parameters, no taxes.
        Difficulty 4-6: taxes included.
        Difficulty 7-8: fiscal/monetary policy shifts.

    Prerequisites:
        system_equations.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "is_lm_model"

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
            Short task description string.
        """
        return "solve IS-LM model for equilibrium Y and r"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an IS-LM equilibrium problem.

        IS: Y = C_0 + c*(Y-T) + I_0 - b*r + G => (1-c)*Y + b*r = C_0 - c*T + I_0 + G
        LM: M/P = d*Y - e*r => d*Y - e*r = M/P

        Args:
            difficulty: Controls parameter complexity.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            c_mpc = 0.8
            c_0 = self._rng.randint(50, 150)
            i_0 = self._rng.randint(50, 200)
            g = self._rng.randint(50, 200)
            t = 0
            b = self._rng.randint(10, 50)
        elif difficulty <= 6:
            c_mpc = round(self._rng.uniform(0.6, 0.9), 2)
            c_0 = self._rng.randint(50, 200)
            i_0 = self._rng.randint(50, 200)
            g = self._rng.randint(50, 300)
            t = self._rng.randint(50, 150)
            b = self._rng.randint(10, 60)
        else:
            c_mpc = round(self._rng.uniform(0.5, 0.9), 2)
            c_0 = self._rng.randint(100, 300)
            i_0 = self._rng.randint(100, 300)
            g = self._rng.randint(100, 400)
            t = self._rng.randint(50, 200)
            b = self._rng.randint(20, 80)

        d = round(self._rng.uniform(0.1, 0.5), 2)
        e = self._rng.randint(10, 50)
        m_p = self._rng.randint(100, 500)

        # IS: (1-c)*Y + b*r = C_0 - c*T + I_0 + G
        a11 = round(1 - c_mpc, 4)
        a12 = b
        rhs1 = round(c_0 - c_mpc * t + i_0 + g, 4)

        # LM: d*Y - e*r = M/P
        a21 = d
        a22 = -e
        rhs2 = m_p

        # Cramer's rule
        det_val = round(a11 * a22 - a12 * a21, 4)
        if abs(det_val) < 1e-6:
            det_val = 1.0  # Safety fallback
        y_star = round((rhs1 * a22 - a12 * rhs2) / det_val, 4)
        r_star = round((a11 * rhs2 - rhs1 * a21) / det_val, 4)

        problem = (
            f"C={c_0}+{_fmt(c_mpc)}(Y-{t}), "
            f"I={i_0}-{b}r, G={g}, "
            f"M/P={m_p}, L={_fmt(d)}Y-{e}r"
        )
        return problem, {
            "c_mpc": c_mpc, "c_0": c_0, "i_0": i_0,
            "g": g, "t": t, "b": b, "d": d, "e": e, "m_p": m_p,
            "a11": a11, "det": det_val,
            "y_star": y_star, "r_star": r_star,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate IS-LM solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return [
            f"IS: (1-{_fmt(sd['c_mpc'])})*Y + {sd['b']}*r = "
            f"{sd['c_0']}-{_fmt(sd['c_mpc'])}*{sd['t']}+{sd['i_0']}+{sd['g']}",
            f"LM: {_fmt(sd['d'])}*Y - {sd['e']}*r = {sd['m_p']}",
            f"det = {_fmt(sd['det'])}",
            f"Y* = {_fmt(sd['y_star'])}",
            f"r* = {_fmt(sd['r_star'])}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the equilibrium output and interest rate.

        Args:
            sd: Solution data.

        Returns:
            Y* and r* values.
        """
        return f"Y*={_fmt(sd['y_star'])}, r*={_fmt(sd['r_star'])}"


# ===================================================================
# 2. Solow Growth Model  (tier 5)
# ===================================================================

@register
class SolowGrowthGenerator(StepGenerator):
    """Compute steady-state capital per worker in the Solow model.

    k_dot = s*f(k) - (n+d)*k.  Steady state: s*f(k*) = (n+d)*k*.
    For Cobb-Douglas f(k) = k^alpha:
    k* = (s/(n+d))^{1/(1-alpha)}.
    y* = (k*)^alpha.

    Difficulty scaling:
        Difficulty 1-3: simple alpha=1/3, integer rates.
        Difficulty 4-6: varied alpha, decimal rates.
        Difficulty 7-8: compute golden rule and transition.

    Prerequisites:
        exponentiation.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "solow_growth"

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
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "compute Solow model steady-state capital per worker"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Solow growth model problem.

        Args:
            difficulty: Controls parameter complexity.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            alpha = round(1 / 3, 4)
            s = 0.2
            n = 0.02
            d = 0.05
        elif difficulty <= 6:
            alpha = round(self._rng.choice([0.25, 0.3, 1 / 3, 0.4]), 4)
            s = round(self._rng.uniform(0.1, 0.4), 2)
            n = round(self._rng.uniform(0.01, 0.05), 3)
            d = round(self._rng.uniform(0.03, 0.1), 3)
        else:
            alpha = round(self._rng.uniform(0.2, 0.5), 4)
            s = round(self._rng.uniform(0.05, 0.5), 2)
            n = round(self._rng.uniform(0.005, 0.05), 4)
            d = round(self._rng.uniform(0.02, 0.15), 4)

        exponent = round(1 / (1 - alpha), 4)
        base = round(s / (n + d), 4)
        k_star = round(base ** exponent, 4)
        y_star = round(k_star ** alpha, 4)

        # Golden rule: s_gold = alpha
        c_star = round((1 - s) * y_star, 4)

        problem = (
            f"f(k)=k^{_fmt(alpha)}, "
            f"s={_fmt(s)}, n={_fmt(n)}, d={_fmt(d)}"
        )
        return problem, {
            "alpha": alpha, "s": s, "n": n, "d": d,
            "exponent": exponent, "base": base,
            "k_star": k_star, "y_star": y_star,
            "c_star": c_star,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate Solow model computation steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return [
            f"steady state: s*k^alpha = (n+d)*k",
            f"k* = (s/(n+d))^{{1/(1-alpha)}} = ({_fmt(sd['s'])}/{_fmt(round(sd['n'] + sd['d'], 4))})^{_fmt(sd['exponent'])}",
            f"base = {_fmt(sd['base'])}, exponent = {_fmt(sd['exponent'])}",
            f"k* = {_fmt(sd['k_star'])}",
            f"y* = k*^alpha = {_fmt(sd['y_star'])}",
            f"c* = (1-s)*y* = {_fmt(sd['c_star'])}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the steady-state values.

        Args:
            sd: Solution data.

        Returns:
            k*, y*, and c* values.
        """
        return (
            f"k*={_fmt(sd['k_star'])}, "
            f"y*={_fmt(sd['y_star'])}, "
            f"c*={_fmt(sd['c_star'])}"
        )


# ===================================================================
# 3. Phillips Curve  (tier 4)
# ===================================================================

@register
class PhillipsCurveGenerator(StepGenerator):
    """Compute inflation from the expectations-augmented Phillips curve.

    pi = pi_e - beta*(u - u_n) where pi_e is expected inflation,
    u is actual unemployment, u_n is the natural rate, and beta is
    the slope parameter.

    Difficulty scaling:
        Difficulty 1-3: integer rates, beta=1.
        Difficulty 4-6: decimal rates.
        Difficulty 7-8: solve for u given target inflation.

    Prerequisites:
        multiplication.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "phillips_curve"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["multiplication"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "compute inflation via Phillips curve"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Phillips curve problem.

        Args:
            difficulty: Controls parameter precision.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            pi_e = float(self._rng.randint(1, 5))
            u_n = float(self._rng.randint(4, 7))
            u = float(self._rng.randint(3, 9))
            beta = 1.0
        elif difficulty <= 6:
            pi_e = round(self._rng.uniform(1.0, 6.0), 1)
            u_n = round(self._rng.uniform(3.0, 7.0), 1)
            u = round(self._rng.uniform(2.0, 10.0), 1)
            beta = round(self._rng.uniform(0.5, 2.0), 2)
        else:
            pi_e = round(self._rng.uniform(0.5, 8.0), 2)
            u_n = round(self._rng.uniform(3.0, 8.0), 2)
            u = round(self._rng.uniform(1.0, 12.0), 2)
            beta = round(self._rng.uniform(0.3, 2.5), 2)

        gap = round(u - u_n, 4)
        pi_actual = round(pi_e - beta * gap, 4)

        problem = (
            f"pi_e={_fmt(pi_e)}%, u={_fmt(u)}%, "
            f"u_n={_fmt(u_n)}%, beta={_fmt(beta)}"
        )
        return problem, {
            "pi_e": pi_e, "u": u, "u_n": u_n, "beta": beta,
            "gap": gap, "pi_actual": pi_actual,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate Phillips curve computation steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return [
            f"pi = pi_e - beta*(u - u_n)",
            f"unemployment gap: u - u_n = {_fmt(sd['u'])} - {_fmt(sd['u_n'])} = {_fmt(sd['gap'])}",
            f"pi = {_fmt(sd['pi_e'])} - {_fmt(sd['beta'])}*{_fmt(sd['gap'])} = {_fmt(sd['pi_actual'])}%",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the inflation rate.

        Args:
            sd: Solution data.

        Returns:
            Inflation value.
        """
        return f"pi={_fmt(sd['pi_actual'])}%"


# ===================================================================
# 4. Option Greeks  (tier 6)
# ===================================================================

@register
class OptionGreeksGenerator(StepGenerator):
    """Compute option Greeks from simplified Black-Scholes parameters.

    Delta = N(d1) for call.  Gamma = N'(d1) / (S*sigma*sqrt(T)).
    Theta (simplified) = -(S*N'(d1)*sigma)/(2*sqrt(T)).
    Vega = S*N'(d1)*sqrt(T).
    d1 = (ln(S/K) + (r + sigma^2/2)*T) / (sigma*sqrt(T)).

    Difficulty scaling:
        Difficulty 1-3: compute d1 and Delta only.
        Difficulty 4-6: Delta and Gamma.
        Difficulty 7-8: all four Greeks.

    Prerequisites:
        derivative.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "option_greeks"

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
            Short task description string.
        """
        return "compute option Greeks from Black-Scholes"

    @staticmethod
    def _norm_cdf(x: float) -> float:
        """Approximate the standard normal CDF.

        Args:
            x: Input value.

        Returns:
            Approximate Phi(x).
        """
        return 0.5 * (1 + math.erf(x / math.sqrt(2)))

    @staticmethod
    def _norm_pdf(x: float) -> float:
        """Compute the standard normal PDF.

        Args:
            x: Input value.

        Returns:
            phi(x) value.
        """
        return math.exp(-x * x / 2) / math.sqrt(2 * math.pi)

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an option Greeks problem.

        Args:
            difficulty: Controls which Greeks to compute.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        s = self._rng.randint(80, 120)
        k = self._rng.randint(80, 120)
        r = round(self._rng.uniform(0.01, 0.1), 3)
        sigma = round(self._rng.uniform(0.1, 0.5), 2)
        t = round(self._rng.uniform(0.1, 2.0), 2)

        sqrt_t = math.sqrt(t)
        d1 = round(
            (math.log(s / k) + (r + sigma ** 2 / 2) * t)
            / (sigma * sqrt_t), 4
        )
        delta = round(self._norm_cdf(d1), 4)
        n_prime_d1 = round(self._norm_pdf(d1), 4)
        gamma = round(n_prime_d1 / (s * sigma * sqrt_t), 4)
        theta = round(-(s * n_prime_d1 * sigma) / (2 * sqrt_t), 4)
        vega = round(s * n_prime_d1 * sqrt_t, 4)

        problem = (
            f"S={s}, K={k}, r={_fmt(r)}, "
            f"sigma={_fmt(sigma)}, T={_fmt(t)}"
        )
        return problem, {
            "s": s, "k": k, "r": r, "sigma": sigma, "t": t,
            "d1": d1, "delta": delta, "n_prime_d1": n_prime_d1,
            "gamma": gamma, "theta": theta, "vega": vega,
            "difficulty": difficulty,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate option Greeks computation steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        steps = [
            f"d1 = (ln({sd['s']}/{sd['k']}) + ({_fmt(sd['r'])} + {_fmt(sd['sigma'])}^2/2)*{_fmt(sd['t'])}) / ({_fmt(sd['sigma'])}*sqrt({_fmt(sd['t'])})) = {_fmt(sd['d1'])}",
            f"Delta = N(d1) = {_fmt(sd['delta'])}",
        ]
        if sd["difficulty"] >= 4:
            steps.append(
                f"N'(d1) = {_fmt(sd['n_prime_d1'])}"
            )
            steps.append(
                f"Gamma = N'(d1)/(S*sigma*sqrt(T)) = {_fmt(sd['gamma'])}"
            )
        if sd["difficulty"] >= 7:
            steps.append(f"Theta = -(S*N'(d1)*sigma)/(2*sqrt(T)) = {_fmt(sd['theta'])}")
            steps.append(f"Vega = S*N'(d1)*sqrt(T) = {_fmt(sd['vega'])}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the computed Greeks.

        Args:
            sd: Solution data.

        Returns:
            Greek values as comma-separated string.
        """
        parts = [f"Delta={_fmt(sd['delta'])}"]
        if sd["difficulty"] >= 4:
            parts.append(f"Gamma={_fmt(sd['gamma'])}")
        if sd["difficulty"] >= 7:
            parts.append(f"Theta={_fmt(sd['theta'])}")
            parts.append(f"Vega={_fmt(sd['vega'])}")
        return ", ".join(parts)


# ===================================================================
# 5. Present Value of Annuity  (tier 4)
# ===================================================================

@register
class PresentValueAnnuityGenerator(StepGenerator):
    """Compute the present value of an annuity or growing annuity.

    PV = C/r * (1 - 1/(1+r)^n).
    Growing annuity: PV = C/(r-g) * (1 - ((1+g)/(1+r))^n).

    Difficulty scaling:
        Difficulty 1-3: ordinary annuity, small n.
        Difficulty 4-6: ordinary annuity, medium n.
        Difficulty 7-8: growing annuity.

    Prerequisites:
        exponentiation.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "present_value_annuity"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["exponentiation"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "compute present value of annuity"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a present value annuity problem.

        Args:
            difficulty: Controls annuity type.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        c = self._rng.randint(100, 5000)
        r = round(self._rng.uniform(0.02, 0.12), 3)

        if difficulty <= 3:
            n = self._rng.randint(3, 10)
            g = 0.0
        elif difficulty <= 6:
            n = self._rng.randint(5, 30)
            g = 0.0
        else:
            n = self._rng.randint(5, 25)
            g = round(self._rng.uniform(0.01, min(r - 0.005, 0.08)), 3)

        if g == 0.0:
            discount_factor = round(1 / (1 + r) ** n, 4)
            pv = round(c / r * (1 - discount_factor), 4)
            problem = f"C={c}, r={_fmt(r)}, n={n}"
        else:
            ratio = round(((1 + g) / (1 + r)) ** n, 4)
            pv = round(c / (r - g) * (1 - ratio), 4)
            problem = f"C={c}, r={_fmt(r)}, g={_fmt(g)}, n={n}"
            discount_factor = ratio

        return problem, {
            "c": c, "r": r, "n": n, "g": g,
            "discount_factor": discount_factor, "pv": pv,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate present value computation steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        if sd["g"] == 0.0:
            return [
                f"PV = C/r * (1 - 1/(1+r)^n)",
                f"(1+r)^n = (1+{_fmt(sd['r'])})^{sd['n']}",
                f"discount factor = {_fmt(sd['discount_factor'])}",
                f"PV = {sd['c']}/{_fmt(sd['r'])} * (1 - {_fmt(sd['discount_factor'])}) = {_fmt(sd['pv'])}",
            ]
        return [
            f"PV = C/(r-g) * (1 - ((1+g)/(1+r))^n)",
            f"r-g = {_fmt(round(sd['r'] - sd['g'], 4))}",
            f"((1+g)/(1+r))^n = {_fmt(sd['discount_factor'])}",
            f"PV = {sd['c']}/{_fmt(round(sd['r'] - sd['g'], 4))} * (1 - {_fmt(sd['discount_factor'])}) = {_fmt(sd['pv'])}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the present value.

        Args:
            sd: Solution data.

        Returns:
            Present value.
        """
        return f"PV={_fmt(sd['pv'])}"


# ===================================================================
# 6. Oligopoly Bertrand Competition  (tier 5)
# ===================================================================

@register
class OligopolyBertrandGenerator(StepGenerator):
    """Solve Bertrand competition equilibrium.

    Identical products: P = MC (zero profit).
    Differentiated products: P_i = (a + c_i)/2 (given linear demand
    q_i = a - b*p_i + d*p_j).  Solve the system for equilibrium prices.

    Difficulty scaling:
        Difficulty 1-3: identical products, P = MC.
        Difficulty 4-6: symmetric differentiated products.
        Difficulty 7-8: asymmetric costs.

    Prerequisites:
        system_equations.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "oligopoly_bertrand"

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
            Short task description string.
        """
        return "solve Bertrand oligopoly equilibrium"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Bertrand competition problem.

        Args:
            difficulty: Controls product differentiation.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            mc = self._rng.randint(5, 50)
            p_star = mc
            profit = 0
            problem = f"identical products, MC={mc}"
            return problem, {
                "mode": "identical", "mc": mc,
                "p_star": p_star, "profit": profit,
            }
        else:
            # Differentiated: q_i = a - b*p_i + d*p_j
            a = self._rng.randint(50, 200)
            b = self._rng.randint(2, 8)
            d_val = self._rng.randint(1, b - 1) if b > 1 else 1

            if difficulty <= 6:
                c1 = self._rng.randint(5, 30)
                c2 = c1  # Symmetric
            else:
                c1 = self._rng.randint(5, 30)
                c2 = self._rng.randint(5, 30)

            # FOC: q_i - b*(p_i - c_i) = 0
            # a - b*p_i + d*p_j - b*p_i + b*c_i = 0
            # 2b*p_i - d*p_j = a + b*c_i
            # Solve: [[2b, -d], [-d, 2b]] [p1, p2] = [a+b*c1, a+b*c2]
            det_val = 4 * b * b - d_val * d_val
            rhs1 = a + b * c1
            rhs2 = a + b * c2
            p1 = round((2 * b * rhs1 + d_val * rhs2) / det_val, 4)
            p2 = round((d_val * rhs1 + 2 * b * rhs2) / det_val, 4)
            q1 = round(a - b * p1 + d_val * p2, 4)
            q2 = round(a - b * p2 + d_val * p1, 4)
            pi1 = round((p1 - c1) * q1, 4)
            pi2 = round((p2 - c2) * q2, 4)

            problem = (
                f"q_i={a}-{b}p_i+{d_val}p_j, "
                f"c1={c1}, c2={c2}"
            )
            return problem, {
                "mode": "differentiated",
                "a": a, "b": b, "d": d_val,
                "c1": c1, "c2": c2, "det": det_val,
                "p1": p1, "p2": p2,
                "q1": q1, "q2": q2,
                "pi1": pi1, "pi2": pi2,
            }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate Bertrand competition solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        if sd["mode"] == "identical":
            return [
                f"identical products: Bertrand paradox",
                f"P = MC = {sd['mc']}",
                f"profit = 0",
            ]
        return [
            f"FOC: 2*{sd['b']}*p_i - {sd['d']}*p_j = a + b*c_i",
            f"det = 4*{sd['b']}^2 - {sd['d']}^2 = {sd['det']}",
            f"p1 = {_fmt(sd['p1'])}, p2 = {_fmt(sd['p2'])}",
            f"q1 = {_fmt(sd['q1'])}, q2 = {_fmt(sd['q2'])}",
            f"pi1 = {_fmt(sd['pi1'])}, pi2 = {_fmt(sd['pi2'])}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the equilibrium prices and profits.

        Args:
            sd: Solution data.

        Returns:
            Price and profit values.
        """
        if sd["mode"] == "identical":
            return f"P={sd['mc']}, profit=0"
        return (
            f"p1={_fmt(sd['p1'])}, p2={_fmt(sd['p2'])}, "
            f"pi1={_fmt(sd['pi1'])}, pi2={_fmt(sd['pi2'])}"
        )


# ===================================================================
# 7. Adverse Selection (Akerlof Lemons)  (tier 5)
# ===================================================================

@register
class AdverseSelectionGenerator(StepGenerator):
    """Analyse market unravelling under adverse selection.

    Seller has quality q uniformly distributed in [q_lo, q_hi].
    Seller's reservation price: v_s(q) = q.
    Buyer's valuation: v_b(q) = alpha*q (alpha > 1).
    Buyer offers price P; only sellers with q <= P remain.
    Average quality in market = (q_lo + P)/2.
    Buyer's expected value = alpha * (q_lo + P)/2.
    Equilibrium: P = alpha * (q_lo + P)/2.

    Difficulty scaling:
        Difficulty 1-3: simple alpha, binary quality.
        Difficulty 4-6: uniform quality distribution.
        Difficulty 7-8: check if market unravels.

    Prerequisites:
        expected_value.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "adverse_selection"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["expected_value"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "analyse adverse selection market equilibrium"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an adverse selection problem.

        Equilibrium: P = alpha*(q_lo + P)/2
        => P*(1 - alpha/2) = alpha*q_lo/2
        => P = alpha*q_lo / (2 - alpha)
        Market exists only if alpha < 2 (otherwise P diverges).

        Args:
            difficulty: Controls quality distribution complexity.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            q_lo = 0
            q_hi = self._rng.choice([100, 200])
            alpha = 1.5
        elif difficulty <= 6:
            q_lo = self._rng.randint(0, 50)
            q_hi = self._rng.randint(q_lo + 50, 300)
            alpha = round(self._rng.uniform(1.1, 1.8), 2)
        else:
            q_lo = self._rng.randint(0, 100)
            q_hi = self._rng.randint(q_lo + 50, 500)
            alpha = round(self._rng.uniform(1.0, 2.5), 2)

        # P_eq = alpha*q_lo / (2 - alpha) if alpha < 2
        if alpha < 2:
            p_eq = round(alpha * q_lo / (2 - alpha), 4)
            # Check if P_eq <= q_hi (market exists)
            market_exists = p_eq <= q_hi and p_eq >= q_lo
            avg_q = round((q_lo + min(p_eq, q_hi)) / 2, 4)
            buyer_value = round(alpha * avg_q, 4)
            unravels = not market_exists
        else:
            # alpha >= 2: buyer always values more, full market
            p_eq = round(float(q_hi), 4)
            avg_q = round((q_lo + q_hi) / 2, 4)
            buyer_value = round(alpha * avg_q, 4)
            market_exists = True
            unravels = False

        problem = (
            f"q in [{q_lo},{q_hi}], alpha={_fmt(alpha)}"
        )
        return problem, {
            "q_lo": q_lo, "q_hi": q_hi, "alpha": alpha,
            "p_eq": p_eq, "avg_q": avg_q,
            "buyer_value": buyer_value,
            "market_exists": market_exists, "unravels": unravels,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate adverse selection analysis steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        steps = [
            f"quality in [{sd['q_lo']}, {sd['q_hi']}], buyer premium alpha={_fmt(sd['alpha'])}",
            f"equilibrium: P = alpha*(q_lo+P)/2",
        ]
        if sd["alpha"] < 2:
            steps.append(
                f"P = alpha*q_lo/(2-alpha) = "
                f"{_fmt(sd['alpha'])}*{sd['q_lo']}/{_fmt(round(2 - sd['alpha'], 4))} = "
                f"{_fmt(sd['p_eq'])}"
            )
        else:
            steps.append(f"alpha >= 2: buyer always values more, P = q_hi = {_fmt(sd['p_eq'])}")
        steps.append(f"avg quality = {_fmt(sd['avg_q'])}")
        steps.append(f"market {'unravels' if sd['unravels'] else 'exists'}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the equilibrium price and market status.

        Args:
            sd: Solution data.

        Returns:
            Equilibrium price and market verdict.
        """
        status = "unravels" if sd["unravels"] else "exists"
        return f"P={_fmt(sd['p_eq'])}, market {status}"


# ===================================================================
# 8. Moral Hazard (Principal-Agent)  (tier 5)
# ===================================================================

@register
class MoralHazardGenerator(StepGenerator):
    """Analyse a principal-agent moral hazard problem.

    Agent chooses effort e in {e_L, e_H}.  Output is high (y_H) with
    probability p(e) and low (y_L) otherwise.  Cost of effort: c(e).
    First-best: choose e that maximises E[y] - c(e).
    Second-best: agent's IC constraint binds.

    Difficulty scaling:
        Difficulty 1-3: binary effort, compute first-best.
        Difficulty 4-6: compute both first-best and second-best.
        Difficulty 7-8: compute minimum wage premium.

    Prerequisites:
        expected_value.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "moral_hazard"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["expected_value"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "analyse principal-agent moral hazard problem"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a moral hazard problem.

        Args:
            difficulty: Controls whether to compute second-best.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        y_h = self._rng.randint(100, 500)
        y_l = self._rng.randint(10, y_h - 20)
        p_h = round(self._rng.uniform(0.6, 0.95), 2)  # prob high output with high effort
        p_l = round(self._rng.uniform(0.1, p_h - 0.1), 2)  # with low effort
        c_h = self._rng.randint(10, 80)
        c_l = self._rng.randint(0, max(1, c_h - 10))

        # Expected output
        ey_h = round(p_h * y_h + (1 - p_h) * y_l, 4)
        ey_l = round(p_l * y_h + (1 - p_l) * y_l, 4)

        # First-best surplus
        surplus_h = round(ey_h - c_h, 4)
        surplus_l = round(ey_l - c_l, 4)
        first_best = "high" if surplus_h >= surplus_l else "low"
        first_best_surplus = max(surplus_h, surplus_l)

        # Second-best: IC constraint => w_H - w_L >= c_h - c_l / (p_h - p_l)
        delta_c = c_h - c_l
        delta_p = round(p_h - p_l, 4)
        if delta_p > 0:
            wage_spread = round(delta_c / delta_p, 4)
        else:
            wage_spread = 0.0

        problem = (
            f"y_H={y_h}, y_L={y_l}, "
            f"p_H={_fmt(p_h)}, p_L={_fmt(p_l)}, "
            f"c_H={c_h}, c_L={c_l}"
        )
        return problem, {
            "y_h": y_h, "y_l": y_l,
            "p_h": p_h, "p_l": p_l,
            "c_h": c_h, "c_l": c_l,
            "ey_h": ey_h, "ey_l": ey_l,
            "surplus_h": surplus_h, "surplus_l": surplus_l,
            "first_best": first_best,
            "first_best_surplus": first_best_surplus,
            "delta_c": delta_c, "delta_p": delta_p,
            "wage_spread": wage_spread,
            "difficulty": difficulty,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate moral hazard analysis steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        steps = [
            f"E[y|high] = {_fmt(sd['p_h'])}*{sd['y_h']} + {_fmt(round(1 - sd['p_h'], 4))}*{sd['y_l']} = {_fmt(sd['ey_h'])}",
            f"E[y|low] = {_fmt(sd['p_l'])}*{sd['y_h']} + {_fmt(round(1 - sd['p_l'], 4))}*{sd['y_l']} = {_fmt(sd['ey_l'])}",
            f"surplus(high) = {_fmt(sd['ey_h'])} - {sd['c_h']} = {_fmt(sd['surplus_h'])}",
            f"surplus(low) = {_fmt(sd['ey_l'])} - {sd['c_l']} = {_fmt(sd['surplus_l'])}",
            f"first-best: {sd['first_best']} effort",
        ]
        if sd["difficulty"] >= 4:
            steps.append(
                f"IC: delta_c/(p_H-p_L) = {sd['delta_c']}/{_fmt(sd['delta_p'])} = {_fmt(sd['wage_spread'])}"
            )
            steps.append(f"min wage spread to induce high effort: {_fmt(sd['wage_spread'])}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the first-best effort and wage spread.

        Args:
            sd: Solution data.

        Returns:
            Effort choice and, if applicable, wage spread.
        """
        result = f"first-best={sd['first_best']}"
        if sd["difficulty"] >= 4:
            result += f", wage_spread={_fmt(sd['wage_spread'])}"
        return result
