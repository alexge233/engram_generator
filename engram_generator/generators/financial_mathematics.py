"""Financial mathematics generators.

8 generators across tiers 4-6 covering portfolio theory, option pricing,
risk measures, and fixed-income analytics.
"""
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


# ===================================================================
# Z-score lookup for VaR
# ===================================================================

_Z_TABLE = {
    0.90: 1.2816,
    0.95: 1.6449,
    0.99: 2.3263,
}


# ===================================================================
# 1. PORTFOLIO RETURN (tier 4)
# ===================================================================

@register
class PortfolioReturnGenerator(StepGenerator):
    """Compute weighted portfolio return from asset weights and returns.

    R_p = sum(w_i * R_i) for a set of assets with given weights
    and individual returns.

    Difficulty scaling:
        Difficulty 1-3: 2 assets.
        Difficulty 4-6: 3 assets.
        Difficulty 7-8: 4 assets.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "portfolio_return"

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
            difficulty: Controls number of assets.

        Returns:
            Task description string.
        """
        return "compute weighted portfolio return"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a portfolio return problem.

        Args:
            difficulty: Controls number of assets and return range.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            n = 2
        elif difficulty <= 6:
            n = 3
        else:
            n = 4

        # Generate weights that sum to 1
        raw = [self._rng.randint(1, 10) for _ in range(n)]
        total = sum(raw)
        weights = [_round4(w / total) for w in raw]
        # Fix rounding so weights sum exactly to 1
        weights[-1] = _round4(1.0 - sum(weights[:-1]))

        returns = [_round4(self._rng.uniform(-0.15, 0.35)) for _ in range(n)]

        products = [_round4(weights[i] * returns[i]) for i in range(n)]
        rp = _round4(sum(products))

        asset_labels = [f"A{i+1}" for i in range(n)]
        parts = [f"{asset_labels[i]}: w={weights[i]}, R={returns[i]}"
                 for i in range(n)]
        problem = "Portfolio: " + "; ".join(parts)

        return problem, {
            "weights": weights,
            "returns": returns,
            "products": products,
            "rp": rp,
            "labels": asset_labels,
            "n": n,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data from _create_problem.

        Returns:
            List of step strings.
        """
        steps = []
        for i in range(sd["n"]):
            steps.append(
                f"w_{i+1}*R_{i+1} = {sd['weights'][i]}*{sd['returns'][i]}"
                f" = {sd['products'][i]}"
            )
        steps.append(
            f"R_p = sum = {sd['rp']}"
        )
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the final answer.

        Args:
            sd: Solution data.

        Returns:
            Portfolio return as a string.
        """
        return str(sd["rp"])


# ===================================================================
# 2. PORTFOLIO VARIANCE (tier 5)
# ===================================================================

@register
class PortfolioVarianceGenerator(StepGenerator):
    """Compute portfolio variance for 2-3 assets.

    sigma_p^2 = sum_i sum_j w_i * w_j * sigma_i * sigma_j * rho_ij.

    Difficulty scaling:
        Difficulty 1-4: 2 assets.
        Difficulty 5-8: 3 assets.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "portfolio_variance"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["std_dev"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls number of assets.

        Returns:
            Task description string.
        """
        return "compute portfolio variance"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a portfolio variance problem.

        Args:
            difficulty: Controls number of assets.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        n = 2 if difficulty <= 4 else 3

        raw = [self._rng.randint(1, 10) for _ in range(n)]
        total = sum(raw)
        weights = [_round4(w / total) for w in raw]
        weights[-1] = _round4(1.0 - sum(weights[:-1]))

        sigmas = [_round4(self._rng.uniform(0.05, 0.30)) for _ in range(n)]

        # Build correlation matrix (symmetric, 1 on diagonal)
        rho = [[0.0] * n for _ in range(n)]
        for i in range(n):
            rho[i][i] = 1.0
            for j in range(i + 1, n):
                val = _round4(self._rng.uniform(-0.5, 0.9))
                rho[i][j] = val
                rho[j][i] = val

        # Compute variance
        variance = 0.0
        terms = []
        for i in range(n):
            for j in range(n):
                term = weights[i] * weights[j] * sigmas[i] * sigmas[j] * rho[i][j]
                variance += term
                if i <= j:
                    terms.append(
                        f"w{i+1}*w{j+1}*s{i+1}*s{j+1}*rho{i+1}{j+1}"
                        f" = {_round4(term)}"
                    )
        variance = _round4(variance)

        parts = []
        for i in range(n):
            parts.append(f"w{i+1}={weights[i]}, sigma{i+1}={sigmas[i]}")
        rho_parts = []
        for i in range(n):
            for j in range(i + 1, n):
                rho_parts.append(f"rho{i+1}{j+1}={rho[i][j]}")
        problem = "; ".join(parts) + "; " + "; ".join(rho_parts)

        return problem, {
            "weights": weights,
            "sigmas": sigmas,
            "rho": rho,
            "terms": terms,
            "variance": variance,
            "n": n,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        steps = ["sigma_p^2 = sum_i sum_j w_i*w_j*s_i*s_j*rho_ij"]
        steps.extend(sd["terms"])
        steps.append(f"sigma_p^2 = {sd['variance']}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the final answer.

        Args:
            sd: Solution data.

        Returns:
            Portfolio variance as a string.
        """
        return str(sd["variance"])


# ===================================================================
# 3. SHARPE RATIO (tier 5)
# ===================================================================

@register
class SharpeRatioGenerator(StepGenerator):
    """Compute Sharpe ratio from portfolio return, risk-free rate, and volatility.

    S = (R_p - R_f) / sigma_p.

    Difficulty scaling:
        Difficulty 1-4: simple values.
        Difficulty 5-8: wider ranges.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "sharpe_ratio"

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
            Task description string.
        """
        return "compute the Sharpe ratio"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Sharpe ratio problem.

        Args:
            difficulty: Controls value ranges.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        rp = _round4(self._rng.uniform(0.05, 0.25 + 0.02 * difficulty))
        rf = _round4(self._rng.uniform(0.01, 0.05))
        sigma_p = _round4(self._rng.uniform(0.08, 0.30))

        excess = _round4(rp - rf)
        sharpe = _round4(excess / sigma_p)

        problem = f"R_p={rp}, R_f={rf}, sigma_p={sigma_p}"
        return problem, {
            "rp": rp,
            "rf": rf,
            "sigma_p": sigma_p,
            "excess": excess,
            "sharpe": sharpe,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return [
            f"excess return = R_p - R_f = {sd['rp']} - {sd['rf']}"
            f" = {sd['excess']}",
            f"S = {sd['excess']} / {sd['sigma_p']} = {sd['sharpe']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the final answer.

        Args:
            sd: Solution data.

        Returns:
            Sharpe ratio as a string.
        """
        return str(sd["sharpe"])


# ===================================================================
# 4. OPTION PAYOFF (tier 4)
# ===================================================================

@register
class OptionPayoffGenerator(StepGenerator):
    """Compute call or put option payoff at expiry.

    Call payoff = max(S - K, 0).
    Put payoff = max(K - S, 0).

    Difficulty scaling:
        Difficulty 1-4: single option.
        Difficulty 5-8: compute net profit with premium.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "option_payoff"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["subtraction"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task description string.
        """
        return "compute option payoff at expiry"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an option payoff problem.

        Args:
            difficulty: Controls complexity and premium inclusion.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        opt_type = self._rng.choice(["call", "put"])
        s = _round4(self._rng.uniform(80, 120 + 10 * difficulty))
        k = _round4(self._rng.uniform(80, 120 + 10 * difficulty))

        if opt_type == "call":
            payoff = _round4(max(s - k, 0))
        else:
            payoff = _round4(max(k - s, 0))

        problem = f"{opt_type} option: S={s}, K={k}"
        sd = {"opt_type": opt_type, "s": s, "k": k, "payoff": payoff}

        if difficulty >= 5:
            premium = _round4(self._rng.uniform(1.0, 10.0))
            profit = _round4(payoff - premium)
            problem += f", premium={premium}"
            sd["premium"] = premium
            sd["profit"] = profit
        else:
            sd["premium"] = None
            sd["profit"] = None

        return problem, sd

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        if sd["opt_type"] == "call":
            steps = [f"payoff = max(S-K, 0) = max({sd['s']}-{sd['k']}, 0)"
                     f" = {sd['payoff']}"]
        else:
            steps = [f"payoff = max(K-S, 0) = max({sd['k']}-{sd['s']}, 0)"
                     f" = {sd['payoff']}"]

        if sd["premium"] is not None:
            steps.append(
                f"profit = payoff - premium = {sd['payoff']}-{sd['premium']}"
                f" = {sd['profit']}"
            )
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the final answer.

        Args:
            sd: Solution data.

        Returns:
            Payoff (and profit if applicable) as a string.
        """
        if sd["profit"] is not None:
            return f"payoff={sd['payoff']}, profit={sd['profit']}"
        return f"payoff={sd['payoff']}"


# ===================================================================
# 5. BINOMIAL OPTION PRICING (tier 6)
# ===================================================================

@register
class BinomialOptionGenerator(StepGenerator):
    """Price an option using the one-step binomial model.

    C = (p*C_u + (1-p)*C_d) / (1+r) where p = (1+r-d) / (u-d).

    Difficulty scaling:
        Difficulty 1-4: call option only.
        Difficulty 5-8: call or put with varying parameters.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "binomial_option"

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
            difficulty: Current difficulty level.

        Returns:
            Task description string.
        """
        return "price option using one-step binomial model"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a binomial option pricing problem.

        Args:
            difficulty: Controls parameter ranges.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        s0 = self._rng.randint(50, 100 + 10 * difficulty)
        u = _round4(1.0 + self._rng.uniform(0.05, 0.25))
        d = _round4(1.0 - self._rng.uniform(0.05, 0.20))
        r = _round4(self._rng.uniform(0.02, 0.08))
        k = self._rng.randint(int(s0 * 0.85), int(s0 * 1.15))

        opt_type = "call" if difficulty <= 4 else self._rng.choice(["call", "put"])

        su = _round4(s0 * u)
        sd_val = _round4(s0 * d)

        if opt_type == "call":
            cu = _round4(max(su - k, 0))
            cd = _round4(max(sd_val - k, 0))
        else:
            cu = _round4(max(k - su, 0))
            cd = _round4(max(k - sd_val, 0))

        p = _round4((1 + r - d) / (u - d))
        price = _round4((p * cu + (1 - p) * cd) / (1 + r))

        problem = (f"{opt_type}: S0={s0}, K={k}, u={u}, d={d}, r={r}")
        return problem, {
            "opt_type": opt_type,
            "s0": s0, "k": k, "u": u, "d": d, "r": r,
            "su": su, "sd": sd_val, "cu": cu, "cd": cd,
            "p": p, "price": price,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return [
            f"S_u = {sd['s0']}*{sd['u']} = {sd['su']}",
            f"S_d = {sd['s0']}*{sd['d']} = {sd['sd']}",
            f"C_u = max({sd['opt_type']} payoff at S_u) = {sd['cu']}",
            f"C_d = max({sd['opt_type']} payoff at S_d) = {sd['cd']}",
            f"p = (1+{sd['r']}-{sd['d']})/({sd['u']}-{sd['d']}) = {sd['p']}",
            f"C = ({sd['p']}*{sd['cu']}+{_round4(1-sd['p'])}*{sd['cd']})"
            f"/(1+{sd['r']}) = {sd['price']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the final answer.

        Args:
            sd: Solution data.

        Returns:
            Option price as a string.
        """
        return str(sd["price"])


# ===================================================================
# 6. VALUE AT RISK (tier 5)
# ===================================================================

@register
class VaRComputationGenerator(StepGenerator):
    """Compute parametric Value at Risk.

    VaR = mu - z_alpha * sigma for a given confidence level.

    Difficulty scaling:
        Difficulty 1-3: 90% confidence.
        Difficulty 4-6: 95% confidence.
        Difficulty 7-8: 99% confidence.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "var_computation"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["std_dev"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task description string.
        """
        return "compute parametric Value at Risk"

    def _select_confidence(self, difficulty: int) -> float:
        """Select confidence level based on difficulty.

        Args:
            difficulty: Difficulty level 1-8.

        Returns:
            Confidence level.
        """
        if difficulty <= 3:
            return 0.90
        if difficulty <= 6:
            return 0.95
        return 0.99

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a VaR computation problem.

        Args:
            difficulty: Controls confidence level and value ranges.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        confidence = self._select_confidence(difficulty)
        z = _Z_TABLE[confidence]

        mu = _round4(self._rng.uniform(0.01, 0.15))
        sigma = _round4(self._rng.uniform(0.05, 0.25))
        portfolio_value = self._rng.randint(100000, 1000000)

        var_pct = _round4(mu - z * sigma)
        var_dollar = _round4(abs(var_pct) * portfolio_value)

        problem = (f"mu={mu}, sigma={sigma}, confidence={confidence}, "
                   f"portfolio=${portfolio_value}")
        return problem, {
            "mu": mu, "sigma": sigma, "confidence": confidence,
            "z": z, "var_pct": var_pct, "var_dollar": var_dollar,
            "portfolio_value": portfolio_value,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return [
            f"z_{sd['confidence']} = {sd['z']}",
            f"VaR% = mu - z*sigma = {sd['mu']} - {sd['z']}*{sd['sigma']}"
            f" = {sd['var_pct']}",
            f"VaR$ = |{sd['var_pct']}|*{sd['portfolio_value']}"
            f" = {sd['var_dollar']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the final answer.

        Args:
            sd: Solution data.

        Returns:
            VaR as a string.
        """
        return f"VaR={sd['var_pct']} (${sd['var_dollar']})"


# ===================================================================
# 7. BOND PRICING (tier 5)
# ===================================================================

@register
class BondPricingGenerator(StepGenerator):
    """Compute bond price from coupon payments and face value.

    P = sum_{t=1}^{T} C/(1+r)^t + F/(1+r)^T.

    Difficulty scaling:
        Difficulty 1-3: 2-3 periods.
        Difficulty 4-6: 4-5 periods.
        Difficulty 7-8: 6-8 periods.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "bond_pricing"

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
            Task description string.
        """
        return "compute bond price from coupon rate and yield"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a bond pricing problem.

        Args:
            difficulty: Controls number of periods.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            periods = self._rng.randint(2, 3)
        elif difficulty <= 6:
            periods = self._rng.randint(4, 5)
        else:
            periods = self._rng.randint(6, 8)

        face = self._rng.choice([100, 1000])
        coupon_rate = _round4(self._rng.uniform(0.03, 0.10))
        ytm = _round4(self._rng.uniform(0.02, 0.12))
        coupon = _round4(face * coupon_rate)

        pv_coupons = 0.0
        coupon_pvs = []
        for t in range(1, periods + 1):
            pv = _round4(coupon / (1 + ytm) ** t)
            pv_coupons += pv
            coupon_pvs.append(pv)
        pv_coupons = _round4(pv_coupons)

        pv_face = _round4(face / (1 + ytm) ** periods)
        price = _round4(pv_coupons + pv_face)

        problem = (f"F={face}, coupon_rate={coupon_rate}, "
                   f"YTM={ytm}, T={periods}")
        return problem, {
            "face": face, "coupon_rate": coupon_rate, "ytm": ytm,
            "periods": periods, "coupon": coupon,
            "coupon_pvs": coupon_pvs, "pv_coupons": pv_coupons,
            "pv_face": pv_face, "price": price,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        steps = [f"C = {sd['face']}*{sd['coupon_rate']} = {sd['coupon']}"]
        for t, pv in enumerate(sd["coupon_pvs"], 1):
            steps.append(f"PV(C_{t}) = {sd['coupon']}/(1+{sd['ytm']})^{t}"
                         f" = {pv}")
        steps.append(f"PV(F) = {sd['face']}/(1+{sd['ytm']})^{sd['periods']}"
                     f" = {sd['pv_face']}")
        steps.append(f"P = {sd['pv_coupons']} + {sd['pv_face']}"
                     f" = {sd['price']}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the final answer.

        Args:
            sd: Solution data.

        Returns:
            Bond price as a string.
        """
        return str(sd["price"])


# ===================================================================
# 8. MACAULAY DURATION (tier 5)
# ===================================================================

@register
class DurationBondGenerator(StepGenerator):
    """Compute Macaulay duration of a bond.

    D = (1/P) * sum_{t=1}^{T} t * CF_t / (1+r)^t.

    Difficulty scaling:
        Difficulty 1-3: 2-3 periods.
        Difficulty 4-6: 4-5 periods.
        Difficulty 7-8: 6-8 periods.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "duration_bond"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["bond_pricing"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task description string.
        """
        return "compute Macaulay duration of a bond"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Macaulay duration problem.

        Args:
            difficulty: Controls number of periods.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            periods = self._rng.randint(2, 3)
        elif difficulty <= 6:
            periods = self._rng.randint(4, 5)
        else:
            periods = self._rng.randint(6, 8)

        face = self._rng.choice([100, 1000])
        coupon_rate = _round4(self._rng.uniform(0.03, 0.10))
        ytm = _round4(self._rng.uniform(0.02, 0.12))
        coupon = _round4(face * coupon_rate)

        # Compute price first
        price = 0.0
        for t in range(1, periods + 1):
            cf = coupon if t < periods else coupon + face
            price += cf / (1 + ytm) ** t
        price = _round4(price)

        # Compute weighted sum for duration
        weighted_sum = 0.0
        weighted_terms = []
        for t in range(1, periods + 1):
            cf = coupon if t < periods else coupon + face
            pv_cf = _round4(cf / (1 + ytm) ** t)
            term = _round4(t * pv_cf)
            weighted_sum += term
            weighted_terms.append((t, cf, pv_cf, term))
        weighted_sum = _round4(weighted_sum)

        duration = _round4(weighted_sum / price)

        problem = (f"F={face}, coupon_rate={coupon_rate}, "
                   f"YTM={ytm}, T={periods}")
        return problem, {
            "face": face, "coupon_rate": coupon_rate, "ytm": ytm,
            "periods": periods, "coupon": coupon, "price": price,
            "weighted_terms": weighted_terms,
            "weighted_sum": weighted_sum, "duration": duration,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        steps = [f"P = {sd['price']}"]
        for t, cf, pv_cf, term in sd["weighted_terms"]:
            steps.append(f"t={t}: CF={cf}, PV={pv_cf}, t*PV={term}")
        steps.append(f"sum(t*PV) = {sd['weighted_sum']}")
        steps.append(f"D = {sd['weighted_sum']}/{sd['price']}"
                     f" = {sd['duration']}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the final answer.

        Args:
            sd: Solution data.

        Returns:
            Duration in years as a string.
        """
        return f"{sd['duration']} years"
