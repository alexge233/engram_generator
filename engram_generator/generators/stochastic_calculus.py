"""Stochastic calculus generators -- Ito calculus, SDEs, and martingale transforms.

6 generators covering Ito's lemma, geometric Brownian motion,
Black-Scholes option pricing, Euler-Maruyama SDE discretisation,
Ornstein-Uhlenbeck processes, and martingale transforms across tiers 6-7.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


# ===================================================================
# HELPER UTILITIES
# ===================================================================

def _round4(x: float) -> float:
    """Round a float to 4 decimal places.

    Args:
        x: Value to round.

    Returns:
        Rounded value.
    """
    return round(x, 4)


def _normal_cdf(x: float) -> float:
    """Approximate the standard normal CDF using the error function.

    Args:
        x: Quantile value.

    Returns:
        P(Z <= x) for standard normal Z.
    """
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


# ===================================================================
# 1. ITO LEMMA (tier 7)
# ===================================================================

@register
class ItoLemmaGenerator(StepGenerator):
    """Apply Ito's lemma to a function of Brownian motion.

    For f(B_t) where B_t is standard Brownian motion, Ito's lemma gives
    df = f'(B_t) dB_t + (1/2) f''(B_t) dt. Evaluates the drift and
    diffusion coefficients for f = B^2, f = e^B, and f = sin(B).

    Difficulty scaling:
        Difficulty 1-3: f(x) = x^2, small B_t values.
        Difficulty 4-6: f(x) = e^x, moderate B_t values.
        Difficulty 7-8: f(x) = sin(x), arbitrary B_t values.

    Prerequisites:
        brownian_motion (tier 6).
    """

    _FUNCTIONS = {
        "x^2": {
            "f_label": "B_t^2",
            "f": lambda b: b ** 2,
            "fp": lambda b: 2 * b,
            "fpp": lambda _b: 2.0,
            "fp_label": "2*B_t",
            "fpp_label": "2",
        },
        "e^x": {
            "f_label": "e^{B_t}",
            "f": lambda b: math.exp(b),
            "fp": lambda b: math.exp(b),
            "fpp": lambda b: math.exp(b),
            "fp_label": "e^{B_t}",
            "fpp_label": "e^{B_t}",
        },
        "sin(x)": {
            "f_label": "sin(B_t)",
            "f": lambda b: math.sin(b),
            "fp": lambda b: math.cos(b),
            "fpp": lambda b: -math.sin(b),
            "fp_label": "cos(B_t)",
            "fpp_label": "-sin(B_t)",
        },
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "ito_lemma"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["brownian_motion"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls function choice.

        Returns:
            Task description string.
        """
        return "apply Ito's lemma to f(B_t) and find drift and diffusion"

    def _select_function(self, difficulty: int) -> str:
        """Choose a function based on difficulty.

        Args:
            difficulty: Difficulty level 1-8.

        Returns:
            Function key string.
        """
        if difficulty <= 3:
            return "x^2"
        if difficulty <= 6:
            return "e^x"
        return "sin(x)"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an Ito's lemma problem.

        Args:
            difficulty: Controls function and B_t value.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        func_key = self._select_function(difficulty)
        spec = self._FUNCTIONS[func_key]

        if difficulty <= 3:
            b_t = _round4(self._rng.uniform(0.5, 2.0))
        elif difficulty <= 6:
            b_t = _round4(self._rng.uniform(0.1, 1.5))
        else:
            b_t = _round4(self._rng.uniform(0.5, 3.0))

        f_val = _round4(spec["f"](b_t))
        fp_val = _round4(spec["fp"](b_t))
        fpp_val = _round4(spec["fpp"](b_t))
        drift = _round4(0.5 * fpp_val)
        diffusion = fp_val

        problem = (
            f"f(x)={func_key}, B_t={b_t}. "
            f"Apply Ito: df = f'dB + (1/2)f''dt."
        )
        return problem, {
            "func_key": func_key, "b_t": b_t,
            "f_val": f_val, "fp_val": fp_val, "fpp_val": fpp_val,
            "drift": drift, "diffusion": diffusion,
            "fp_label": spec["fp_label"],
            "fpp_label": spec["fpp_label"],
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Ito's lemma application steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing derivative evaluation.
        """
        return [
            f"f'({data['b_t']}) = {data['fp_label']} = {data['fp_val']}",
            f"f''({data['b_t']}) = {data['fpp_label']} = {data['fpp_val']}",
            f"diffusion = f' = {data['diffusion']}",
            f"drift = (1/2)*f'' = 0.5*{data['fpp_val']} = {data['drift']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the drift and diffusion coefficients.

        Args:
            data: Solution data.

        Returns:
            Formatted drift and diffusion values.
        """
        return f"drift={data['drift']}, diffusion={data['diffusion']}"


# ===================================================================
# 2. GEOMETRIC BROWNIAN MOTION (tier 7)
# ===================================================================

@register
class GeometricBrownianGenerator(StepGenerator):
    """Compute the value of geometric Brownian motion at time t.

    For dS = mu*S*dt + sigma*S*dB, the analytic solution is
    S(t) = S_0 * exp((mu - sigma^2/2)*t + sigma*B_t).
    Given S_0, mu, sigma, t, and B_t, computes S(t).

    Difficulty scaling:
        Difficulty 1-3: integer mu and sigma, small t.
        Difficulty 4-6: decimal mu and sigma, moderate t.
        Difficulty 7-8: wider parameter ranges.

    Prerequisites:
        ito_lemma (tier 7).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "geometric_brownian"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["ito_lemma"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls parameter complexity.

        Returns:
            Task description string.
        """
        return "compute S(t) for geometric Brownian motion"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a geometric Brownian motion problem.

        Args:
            difficulty: Controls parameter ranges.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        s_0 = _round4(self._rng.uniform(50, 200))

        if difficulty <= 3:
            mu = _round4(self._rng.uniform(0.01, 0.1))
            sigma = _round4(self._rng.uniform(0.1, 0.3))
            t = self._rng.randint(1, 2)
            b_t = _round4(self._rng.uniform(-1.0, 1.0))
        elif difficulty <= 6:
            mu = _round4(self._rng.uniform(0.02, 0.15))
            sigma = _round4(self._rng.uniform(0.1, 0.4))
            t = self._rng.randint(1, 3)
            b_t = _round4(self._rng.uniform(-1.5, 1.5))
        else:
            mu = _round4(self._rng.uniform(0.05, 0.2))
            sigma = _round4(self._rng.uniform(0.15, 0.5))
            t = self._rng.randint(1, 5)
            b_t = _round4(self._rng.uniform(-2.0, 2.0))

        drift_adj = _round4(mu - sigma ** 2 / 2)
        exponent = _round4(drift_adj * t + sigma * b_t)
        s_t = _round4(s_0 * math.exp(exponent))

        problem = (
            f"GBM: S_0={s_0}, mu={mu}, sigma={sigma}, "
            f"t={t}, B_t={b_t}. Compute S(t)."
        )
        return problem, {
            "s_0": s_0, "mu": mu, "sigma": sigma,
            "t": t, "b_t": b_t,
            "drift_adj": drift_adj, "exponent": exponent, "s_t": s_t,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate GBM computation steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing the analytic solution evaluation.
        """
        return [
            f"mu - sigma^2/2 = {data['mu']} - {data['sigma']}^2/2 = {data['drift_adj']}",
            f"exponent = {data['drift_adj']}*{data['t']} + {data['sigma']}*{data['b_t']} = {data['exponent']}",
            f"S(t) = {data['s_0']} * exp({data['exponent']}) = {data['s_t']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the GBM value.

        Args:
            data: Solution data.

        Returns:
            S(t) as a string.
        """
        return f"S(t) = {data['s_t']}"


# ===================================================================
# 3. BLACK-SCHOLES (tier 7)
# ===================================================================

@register
class BlackScholesGenerator(StepGenerator):
    """Compute a European call option price using the Black-Scholes formula.

    C = S*N(d1) - K*e^(-rT)*N(d2) where
    d1 = (ln(S/K) + (r + sigma^2/2)*T) / (sigma*sqrt(T)),
    d2 = d1 - sigma*sqrt(T).

    Difficulty scaling:
        Difficulty 1-3: near at-the-money, short expiry.
        Difficulty 4-6: moderate moneyness, medium expiry.
        Difficulty 7-8: wider parameter ranges.

    Prerequisites:
        geometric_brownian (tier 7).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "black_scholes"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["geometric_brownian"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls parameter ranges.

        Returns:
            Task description string.
        """
        return "compute European call price using Black-Scholes"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Black-Scholes option pricing problem.

        Args:
            difficulty: Controls moneyness and expiry range.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        s = _round4(self._rng.uniform(80, 120))
        r = _round4(self._rng.uniform(0.01, 0.08))
        sigma = _round4(self._rng.uniform(0.15, 0.4))

        if difficulty <= 3:
            k = _round4(s * self._rng.uniform(0.95, 1.05))
            t = _round4(self._rng.uniform(0.1, 0.5))
        elif difficulty <= 6:
            k = _round4(s * self._rng.uniform(0.85, 1.15))
            t = _round4(self._rng.uniform(0.25, 1.0))
        else:
            k = _round4(s * self._rng.uniform(0.7, 1.3))
            t = _round4(self._rng.uniform(0.5, 2.0))

        sqrt_t = math.sqrt(t)
        d1 = _round4(
            (math.log(s / k) + (r + sigma ** 2 / 2) * t) / (sigma * sqrt_t)
        )
        d2 = _round4(d1 - sigma * sqrt_t)
        n_d1 = _round4(_normal_cdf(d1))
        n_d2 = _round4(_normal_cdf(d2))
        call = _round4(s * n_d1 - k * math.exp(-r * t) * n_d2)

        problem = (
            f"BS: S={s}, K={k}, r={r}, sigma={sigma}, T={t}. "
            f"Compute call price C."
        )
        return problem, {
            "s": s, "k": k, "r": r, "sigma": sigma, "t": t,
            "d1": d1, "d2": d2, "n_d1": n_d1, "n_d2": n_d2,
            "call": call,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Black-Scholes computation steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing d1, d2, N(d1), N(d2), and C.
        """
        return [
            f"d1 = (ln({data['s']}/{data['k']}) + ({data['r']}+{data['sigma']}^2/2)*{data['t']}) / ({data['sigma']}*sqrt({data['t']})) = {data['d1']}",
            f"d2 = {data['d1']} - {data['sigma']}*sqrt({data['t']}) = {data['d2']}",
            f"N(d1) = {data['n_d1']}, N(d2) = {data['n_d2']}",
            f"C = {data['s']}*{data['n_d1']} - {data['k']}*e^(-{data['r']}*{data['t']})*{data['n_d2']} = {data['call']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the call option price.

        Args:
            data: Solution data.

        Returns:
            Call price as a string.
        """
        return f"C = {data['call']}"


# ===================================================================
# 4. SDE EULER-MARUYAMA (tier 6)
# ===================================================================

@register
class SdeEulerGenerator(StepGenerator):
    """Compute one Euler-Maruyama step for a stochastic differential equation.

    Applies X_{n+1} = X_n + a(X_n)*dt + b(X_n)*sqrt(dt)*Z where
    a is the drift function, b is the diffusion function, dt is the
    time step, and Z is a given standard normal draw.

    Difficulty scaling:
        Difficulty 1-3: a(x) = mu*x, b(x) = sigma*x (GBM).
        Difficulty 4-6: a(x) = theta*(mu - x), b(x) = sigma (OU).
        Difficulty 7-8: a(x) = alpha - beta*x, b(x) = sigma*sqrt(x) (CIR).

    Prerequisites:
        multiplication (tier 1).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "sde_euler"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["multiplication"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls SDE type.

        Returns:
            Task description string.
        """
        return "compute one Euler-Maruyama step for an SDE"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an Euler-Maruyama step problem.

        Args:
            difficulty: Controls SDE type and parameters.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        dt = _round4(self._rng.choice([0.01, 0.05, 0.1, 0.25]))
        z = _round4(self._rng.uniform(-2.0, 2.0))
        sqrt_dt = _round4(math.sqrt(dt))

        if difficulty <= 3:
            return self._gbm_step(dt, z, sqrt_dt)
        if difficulty <= 6:
            return self._ou_step(dt, z, sqrt_dt)
        return self._cir_step(dt, z, sqrt_dt)

    def _gbm_step(self, dt: float, z: float,
                   sqrt_dt: float) -> tuple[str, dict]:
        """Generate a GBM Euler step.

        Args:
            dt: Time step.
            z: Standard normal draw.
            sqrt_dt: Square root of dt.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        x_n = _round4(self._rng.uniform(50, 150))
        mu = _round4(self._rng.uniform(0.02, 0.1))
        sigma = _round4(self._rng.uniform(0.1, 0.3))

        a_val = _round4(mu * x_n)
        b_val = _round4(sigma * x_n)
        x_next = _round4(x_n + a_val * dt + b_val * sqrt_dt * z)

        problem = (
            f"EM step: dX = {mu}*X*dt + {sigma}*X*dB, "
            f"X_n={x_n}, dt={dt}, Z={z}."
        )
        return problem, {
            "sde_type": "GBM", "x_n": x_n, "dt": dt, "z": z,
            "sqrt_dt": sqrt_dt, "a_val": a_val, "b_val": b_val,
            "x_next": x_next,
        }

    def _ou_step(self, dt: float, z: float,
                  sqrt_dt: float) -> tuple[str, dict]:
        """Generate an Ornstein-Uhlenbeck Euler step.

        Args:
            dt: Time step.
            z: Standard normal draw.
            sqrt_dt: Square root of dt.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        x_n = _round4(self._rng.uniform(0.5, 5.0))
        theta = _round4(self._rng.uniform(0.5, 2.0))
        mu = _round4(self._rng.uniform(1.0, 3.0))
        sigma = _round4(self._rng.uniform(0.1, 0.5))

        a_val = _round4(theta * (mu - x_n))
        b_val = sigma
        x_next = _round4(x_n + a_val * dt + b_val * sqrt_dt * z)

        problem = (
            f"EM step: dX = {theta}*({mu}-X)*dt + {sigma}*dB, "
            f"X_n={x_n}, dt={dt}, Z={z}."
        )
        return problem, {
            "sde_type": "OU", "x_n": x_n, "dt": dt, "z": z,
            "sqrt_dt": sqrt_dt, "a_val": a_val, "b_val": b_val,
            "x_next": x_next,
        }

    def _cir_step(self, dt: float, z: float,
                   sqrt_dt: float) -> tuple[str, dict]:
        """Generate a CIR process Euler step.

        Args:
            dt: Time step.
            z: Standard normal draw.
            sqrt_dt: Square root of dt.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        x_n = _round4(self._rng.uniform(1.0, 5.0))
        alpha = _round4(self._rng.uniform(0.5, 2.0))
        beta = _round4(self._rng.uniform(0.1, 1.0))
        sigma = _round4(self._rng.uniform(0.1, 0.5))

        a_val = _round4(alpha - beta * x_n)
        b_val = _round4(sigma * math.sqrt(max(x_n, 0)))
        x_next = _round4(x_n + a_val * dt + b_val * sqrt_dt * z)

        problem = (
            f"EM step: dX = ({alpha}-{beta}*X)*dt + {sigma}*sqrt(X)*dB, "
            f"X_n={x_n}, dt={dt}, Z={z}."
        )
        return problem, {
            "sde_type": "CIR", "x_n": x_n, "dt": dt, "z": z,
            "sqrt_dt": sqrt_dt, "a_val": a_val, "b_val": b_val,
            "x_next": x_next,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Euler-Maruyama computation steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing drift, diffusion, and update.
        """
        return [
            f"a(X_n) = {data['a_val']}",
            f"b(X_n) = {data['b_val']}",
            f"sqrt(dt) = {data['sqrt_dt']}",
            f"X_{{n+1}} = {data['x_n']} + {data['a_val']}*{data['dt']} + {data['b_val']}*{data['sqrt_dt']}*{data['z']} = {data['x_next']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the next state value.

        Args:
            data: Solution data.

        Returns:
            X_{n+1} as a string.
        """
        return f"X_{{n+1}} = {data['x_next']}"


# ===================================================================
# 5. ORNSTEIN-UHLENBECK (tier 7)
# ===================================================================

@register
class OrnsteinUhlenbeckGenerator(StepGenerator):
    """Compute the mean and variance of an Ornstein-Uhlenbeck process.

    For dX = theta*(mu - X)*dt + sigma*dB with X(0) = x_0, computes
    E[X(t)] = mu + (x_0 - mu)*exp(-theta*t) and
    Var(X(t)) = sigma^2/(2*theta) * (1 - exp(-2*theta*t)).

    Difficulty scaling:
        Difficulty 1-3: integer theta and mu, small t.
        Difficulty 4-6: decimal parameters, moderate t.
        Difficulty 7-8: wider ranges.

    Prerequisites:
        ito_lemma (tier 7).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "ornstein_uhlenbeck"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["ito_lemma"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls parameter complexity.

        Returns:
            Task description string.
        """
        return "compute E[X(t)] and Var(X(t)) for Ornstein-Uhlenbeck process"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an Ornstein-Uhlenbeck moments problem.

        Args:
            difficulty: Controls parameter ranges.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            theta = self._rng.randint(1, 3)
            mu = self._rng.randint(1, 5)
            sigma = _round4(self._rng.uniform(0.1, 0.5))
            x_0 = self._rng.randint(0, 10)
            t = self._rng.randint(1, 2)
        elif difficulty <= 6:
            theta = _round4(self._rng.uniform(0.5, 3.0))
            mu = _round4(self._rng.uniform(1.0, 5.0))
            sigma = _round4(self._rng.uniform(0.1, 1.0))
            x_0 = _round4(self._rng.uniform(0.0, 10.0))
            t = _round4(self._rng.uniform(0.5, 3.0))
        else:
            theta = _round4(self._rng.uniform(0.1, 5.0))
            mu = _round4(self._rng.uniform(0.0, 10.0))
            sigma = _round4(self._rng.uniform(0.1, 2.0))
            x_0 = _round4(self._rng.uniform(-5.0, 15.0))
            t = _round4(self._rng.uniform(0.5, 5.0))

        exp_neg_theta_t = _round4(math.exp(-theta * t))
        e_xt = _round4(mu + (x_0 - mu) * exp_neg_theta_t)
        exp_neg_2theta_t = _round4(math.exp(-2 * theta * t))
        var_xt = _round4(sigma ** 2 / (2 * theta) * (1 - exp_neg_2theta_t))

        problem = (
            f"OU: theta={theta}, mu={mu}, sigma={sigma}, "
            f"X(0)={x_0}, t={t}. E[X(t)]? Var(X(t))?"
        )
        return problem, {
            "theta": theta, "mu": mu, "sigma": sigma,
            "x_0": x_0, "t": t,
            "exp_neg_theta_t": exp_neg_theta_t,
            "exp_neg_2theta_t": exp_neg_2theta_t,
            "e_xt": e_xt, "var_xt": var_xt,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Ornstein-Uhlenbeck moment computation steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing the mean and variance formulae evaluation.
        """
        return [
            f"exp(-theta*t) = exp(-{data['theta']}*{data['t']}) = {data['exp_neg_theta_t']}",
            f"E[X(t)] = {data['mu']} + ({data['x_0']}-{data['mu']})*{data['exp_neg_theta_t']} = {data['e_xt']}",
            f"exp(-2*theta*t) = {data['exp_neg_2theta_t']}",
            f"Var(X(t)) = {data['sigma']}^2/(2*{data['theta']}) * (1-{data['exp_neg_2theta_t']}) = {data['var_xt']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the mean and variance.

        Args:
            data: Solution data.

        Returns:
            E[X(t)] and Var(X(t)) as a string.
        """
        return f"E[X(t)]={data['e_xt']}, Var(X(t))={data['var_xt']}"


# ===================================================================
# 6. MARTINGALE TRANSFORM (tier 7)
# ===================================================================

@register
class MartingaleTransformGenerator(StepGenerator):
    """Compute a discrete martingale transform (H . M)_n.

    If M is a martingale and H is predictable, the martingale transform
    (H . M)_n = sum_{k=1}^{n} H_k * (M_k - M_{k-1}) is also a
    martingale. Given small sequences H and M, computes the transform.

    Difficulty scaling:
        Difficulty 1-3: n = 3, constant H.
        Difficulty 4-6: n = 4, simple integer H.
        Difficulty 7-8: n = 5, varying H values.

    Prerequisites:
        brownian_motion (tier 6).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "martingale_transform"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["brownian_motion"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls sequence length.

        Returns:
            Task description string.
        """
        return "compute martingale transform (H.M)_n"

    def _select_length(self, difficulty: int) -> int:
        """Choose sequence length based on difficulty.

        Args:
            difficulty: Difficulty level 1-8.

        Returns:
            Number of time steps n.
        """
        if difficulty <= 3:
            return 3
        if difficulty <= 6:
            return 4
        return 5

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a martingale transform problem.

        Args:
            difficulty: Controls sequence length and H complexity.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        n = self._select_length(difficulty)

        # Generate martingale increments (symmetric random walk style)
        m_values = [0]
        for _ in range(n):
            increment = self._rng.choice([-2, -1, 1, 2])
            m_values.append(m_values[-1] + increment)

        # Generate predictable process H (H_k depends on info up to k-1)
        if difficulty <= 3:
            h_val = self._rng.randint(1, 3)
            h_values = [h_val] * n
        else:
            h_values = [self._rng.randint(1, 4) for _ in range(n)]

        # Compute transform increments and cumulative sum
        increments = []
        for k in range(n):
            delta_m = m_values[k + 1] - m_values[k]
            increments.append(_round4(h_values[k] * delta_m))

        partial_sums = []
        running = 0.0
        for inc in increments:
            running = _round4(running + inc)
            partial_sums.append(running)

        transform_n = partial_sums[-1]

        m_str = ", ".join(str(v) for v in m_values)
        h_str = ", ".join(str(v) for v in h_values)
        problem = (
            f"M = [{m_str}], H = [{h_str}]. "
            f"Compute (H.M)_{n}."
        )
        return problem, {
            "n": n, "m_values": m_values, "h_values": h_values,
            "increments": increments, "partial_sums": partial_sums,
            "transform_n": transform_n,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate martingale transform computation steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing each increment and the running sum.
        """
        steps = []
        for k in range(data["n"]):
            delta_m = data["m_values"][k + 1] - data["m_values"][k]
            steps.append(
                f"H_{k + 1}*(M_{k + 1}-M_{k}) = "
                f"{data['h_values'][k]}*{delta_m} = "
                f"{data['increments'][k]}"
            )
        inc_str = " + ".join(str(v) for v in data["increments"])
        steps.append(f"(H.M)_{data['n']} = {inc_str} = {data['transform_n']}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the martingale transform value.

        Args:
            data: Solution data.

        Returns:
            Transform value as a string.
        """
        return f"(H.M)_{data['n']} = {data['transform_n']}"
