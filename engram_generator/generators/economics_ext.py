"""Extended economics generators -- marginal analysis, consumer surplus,
multiplier effect, exchange rates, inflation/real rates, production
functions, game theory (Cournot), time value of money.

8 generators across tiers 4-5, deepening the economics domain.
"""
from __future__ import annotations

import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


# ===================================================================
# 1. Marginal analysis  (tier 4)
# ===================================================================

@register
class MarginalAnalysisGenerator(StepGenerator):
    """Find profit-maximising quantity via marginal analysis.

    Given total cost TC(Q) = aQ^2 + bQ + c and total revenue
    TR(Q) = pQ, compute MC = dTC/dQ, MR = dTR/dQ, and find Q*
    where MC = MR.

    Difficulty scaling:
        Difficulty 1-3: linear TC, simple MR.
        Difficulty 4-6: quadratic TC.
        Difficulty 7-8: quadratic TC and quadratic TR.

    Prerequisites:
        derivative.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "marginal_analysis"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

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
        return "find profit-maximising quantity via MC = MR"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a marginal analysis problem.

        Creates cost and revenue functions, differentiates to find
        MC and MR, then solves MC = MR for optimal Q.

        Args:
            difficulty: Controls complexity of cost/revenue functions.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            # TC = bQ + c (linear), TR = pQ
            b = self._rng.randint(2, 10)
            c = self._rng.randint(10, 100)
            p = self._rng.randint(b + 1, b + 20)
            # MC = b, MR = p; MC = MR only if b = p (never profitable to stop)
            # Use quadratic instead for meaningful result
            a = self._rng.randint(1, 3)
            # TC = aQ^2 + bQ + c, TR = pQ
            # MC = 2aQ + b, MR = p
            # 2aQ + b = p => Q = (p - b) / (2a)
            q_star = round((p - b) / (2 * a), 4)
            profit = round(p * q_star - (a * q_star ** 2 + b * q_star + c), 4)
            desc = f"TC = {a}Q^2 + {b}Q + {c}, TR = {p}Q; find Q*"
            return desc, {
                "mode": "quad_linear",
                "a": a, "b": b, "c": c, "p": p,
                "mc_expr": f"2*{a}*Q + {b}", "mr_expr": str(p),
                "q_star": q_star, "profit": profit,
            }
        elif difficulty <= 6:
            a = self._rng.randint(1, 5)
            b = self._rng.randint(1, 15)
            c = self._rng.randint(10, 200)
            p = self._rng.randint(b + 5, b + 50)
            q_star = round((p - b) / (2 * a), 4)
            profit = round(p * q_star - (a * q_star ** 2 + b * q_star + c), 4)
            desc = f"TC = {a}Q^2 + {b}Q + {c}, TR = {p}Q; find Q*"
            return desc, {
                "mode": "quad_linear",
                "a": a, "b": b, "c": c, "p": p,
                "mc_expr": f"2*{a}*Q + {b}", "mr_expr": str(p),
                "q_star": q_star, "profit": profit,
            }
        else:
            # TR = dQ - eQ^2 (downward-sloping demand)
            a = self._rng.randint(1, 4)
            b = self._rng.randint(1, 10)
            c = self._rng.randint(10, 100)
            d = self._rng.randint(20, 80)
            e = self._rng.randint(1, 5)
            # MC = 2aQ + b, MR = d - 2eQ
            # 2aQ + b = d - 2eQ => Q = (d - b) / (2a + 2e)
            q_star = round((d - b) / (2 * a + 2 * e), 4)
            tr = round(d * q_star - e * q_star ** 2, 4)
            tc = round(a * q_star ** 2 + b * q_star + c, 4)
            profit = round(tr - tc, 4)
            desc = (
                f"TC = {a}Q^2+{b}Q+{c}, TR = {d}Q-{e}Q^2; find Q*"
            )
            return desc, {
                "mode": "quad_quad",
                "a": a, "b": b, "c": c, "d": d, "e": e,
                "mc_expr": f"2*{a}*Q + {b}",
                "mr_expr": f"{d} - 2*{e}*Q",
                "q_star": q_star, "profit": profit,
            }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return [
            f"MC = d(TC)/dQ = {sd['mc_expr']}",
            f"MR = d(TR)/dQ = {sd['mr_expr']}",
            f"set MC = MR, solve for Q",
            f"Q* = {sd['q_star']}",
            f"profit = TR - TC at Q* = {sd['profit']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the optimal quantity and profit.

        Args:
            sd: Solution data.

        Returns:
            Q* and profit.
        """
        return f"Q* = {sd['q_star']}, profit = {sd['profit']}"


# ===================================================================
# 2. Consumer surplus  (tier 5)
# ===================================================================

@register
class ConsumerSurplusGenerator(StepGenerator):
    """Compute consumer surplus from a linear demand curve.

    CS = integral from 0 to Q* of (D(Q) - P*) dQ. For linear demand
    D(Q) = a - bQ with equilibrium price P* and quantity Q*, this
    simplifies to CS = 0.5 * (a - P*) * Q*.

    Difficulty scaling:
        Difficulty 1-3: given P* and Q* directly.
        Difficulty 4-6: compute Q* from D(Q*) = P*.
        Difficulty 7-8: compute both CS and producer surplus.

    Prerequisites:
        multiplication.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "consumer_surplus"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

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
        return "compute consumer surplus from linear demand"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a consumer surplus problem.

        Creates a linear demand curve and equilibrium price/quantity,
        then computes the consumer surplus as a triangle area.

        Args:
            difficulty: Controls what is given vs computed.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        a = self._rng.randint(20, 100 + 20 * difficulty)
        b_coeff = self._rng.randint(1, min(5, 1 + difficulty))
        p_star = self._rng.randint(5, a // 2)
        q_star = round((a - p_star) / b_coeff, 4)
        cs = round(0.5 * (a - p_star) * q_star, 4)

        if difficulty <= 3:
            desc = (
                f"D(Q) = {a} - {b_coeff}Q, P* = {p_star}, "
                f"Q* = {q_star}; consumer surplus?"
            )
        elif difficulty <= 6:
            desc = (
                f"D(Q) = {a} - {b_coeff}Q, P* = {p_star}; "
                f"find Q* and consumer surplus"
            )
        else:
            # Also compute producer surplus with supply S(Q) = cQ
            c_coeff = self._rng.randint(1, min(5, 1 + difficulty))
            # PS = 0.5 * P* * Q* (triangle under supply)
            ps = round(0.5 * p_star * q_star, 4)
            desc = (
                f"D(Q) = {a} - {b_coeff}Q, S(Q) = {c_coeff}Q, "
                f"P* = {p_star}; CS and PS?"
            )
            return desc, {
                "mode": "both", "a": a, "b": b_coeff, "p_star": p_star,
                "q_star": q_star, "cs": cs, "ps": ps,
            }

        return desc, {
            "mode": "cs_only", "a": a, "b": b_coeff,
            "p_star": p_star, "q_star": q_star, "cs": cs,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        steps = [
            f"D(Q) = {sd['a']} - {sd['b']}Q",
            f"Q* = ({sd['a']} - {sd['p_star']})/{sd['b']} = {sd['q_star']}",
            f"CS = 0.5 * ({sd['a']} - {sd['p_star']}) * {sd['q_star']} = {sd['cs']}",
        ]
        if sd["mode"] == "both":
            steps.append(
                f"PS = 0.5 * {sd['p_star']} * {sd['q_star']} = {sd['ps']}"
            )
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the consumer surplus (and optionally producer surplus).

        Args:
            sd: Solution data.

        Returns:
            Result string.
        """
        if sd["mode"] == "both":
            return f"CS = {sd['cs']}, PS = {sd['ps']}"
        return f"CS = {sd['cs']}"


# ===================================================================
# 3. Multiplier effect  (tier 4)
# ===================================================================

@register
class MultiplierEffectGenerator(StepGenerator):
    """Compute fiscal multiplier and total GDP change.

    Fiscal multiplier = 1 / (1 - MPC). Total GDP change = multiplier
    * initial spending change. With taxation: multiplier = 1/(1-MPC*(1-t)).

    Difficulty scaling:
        Difficulty 1-3: simple multiplier, no tax.
        Difficulty 4-6: with proportional tax rate.
        Difficulty 7-8: balanced budget multiplier (spending = tax increase).

    Prerequisites:
        division.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "multiplier_effect"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["division"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "compute fiscal multiplier and GDP change"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a multiplier effect problem.

        Creates an MPC, optional tax rate, and spending change,
        then computes the multiplier and total GDP impact.

        Args:
            difficulty: Controls whether taxation is included.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        mpc = round(self._rng.uniform(0.5, 0.95), 2)
        spending = self._rng.randint(10, 100) * 10  # billions

        if difficulty <= 3:
            multiplier = round(1.0 / (1.0 - mpc), 4)
            gdp_change = round(multiplier * spending, 4)
            desc = f"MPC = {mpc}, spending increase = {spending}B; GDP change?"
            return desc, {
                "mode": "simple", "mpc": mpc, "spending": spending,
                "multiplier": multiplier, "gdp_change": gdp_change,
            }
        elif difficulty <= 6:
            t = round(self._rng.uniform(0.1, 0.35), 2)
            multiplier = round(1.0 / (1.0 - mpc * (1 - t)), 4)
            gdp_change = round(multiplier * spending, 4)
            desc = (
                f"MPC = {mpc}, tax rate t = {t}, "
                f"spending increase = {spending}B; GDP change?"
            )
            return desc, {
                "mode": "tax", "mpc": mpc, "t": t, "spending": spending,
                "multiplier": multiplier, "gdp_change": gdp_change,
            }
        else:
            # Balanced budget: spending = tax increase, multiplier = 1
            multiplier = 1.0
            gdp_change = round(multiplier * spending, 4)
            desc = (
                f"MPC = {mpc}, balanced budget (spending = tax "
                f"increase = {spending}B); GDP change?"
            )
            return desc, {
                "mode": "balanced", "mpc": mpc, "spending": spending,
                "multiplier": multiplier, "gdp_change": gdp_change,
            }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        if sd["mode"] == "simple":
            return [
                f"multiplier = 1/(1 - MPC) = 1/(1 - {sd['mpc']})",
                f"multiplier = {sd['multiplier']}",
                f"GDP change = {sd['multiplier']} * {sd['spending']} = {sd['gdp_change']}B",
            ]
        elif sd["mode"] == "tax":
            return [
                f"multiplier = 1/(1 - MPC*(1-t)) = 1/(1 - {sd['mpc']}*(1-{sd['t']}))",
                f"multiplier = {sd['multiplier']}",
                f"GDP change = {sd['multiplier']} * {sd['spending']} = {sd['gdp_change']}B",
            ]
        else:
            return [
                "balanced budget multiplier = 1",
                f"GDP change = 1 * {sd['spending']} = {sd['gdp_change']}B",
            ]

    def _create_answer(self, sd: dict) -> str:
        """Return the multiplier and GDP change.

        Args:
            sd: Solution data.

        Returns:
            Result string.
        """
        return f"multiplier = {sd['multiplier']}, GDP change = {sd['gdp_change']}B"


# ===================================================================
# 4. Exchange rate  (tier 4)
# ===================================================================

@register
class ExchangeRateGenerator(StepGenerator):
    """Convert currencies and check for triangular arbitrage.

    Given direct/indirect exchange rate quotes, convert between
    currencies. For triangular arbitrage: check if A/B * B/C * C/A = 1.

    Difficulty scaling:
        Difficulty 1-3: simple two-currency conversion.
        Difficulty 4-6: indirect quote conversion.
        Difficulty 7-8: triangular arbitrage check with three currencies.

    Prerequisites:
        multiplication.
    """

    _CURRENCIES: list[str] = ["USD", "EUR", "GBP", "JPY", "CHF", "CAD"]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "exchange_rate"

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
        return "convert currencies or check triangular arbitrage"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an exchange rate problem.

        Creates exchange rates and asks for conversion or arbitrage
        detection.

        Args:
            difficulty: Controls problem complexity.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 6:
            c1, c2 = self._rng.sample(self._CURRENCIES, 2)
            rate = round(self._rng.uniform(0.5, 150.0), 4)
            amount = round(self._rng.uniform(100.0, 10000.0), 2)
            converted = round(amount * rate, 4)
            desc = f"rate {c1}/{c2} = {rate}; convert {amount} {c1} to {c2}"
            return desc, {
                "mode": "convert", "c1": c1, "c2": c2,
                "rate": rate, "amount": amount, "converted": converted,
            }
        else:
            c1, c2, c3 = self._rng.sample(self._CURRENCIES, 3)
            r_ab = round(self._rng.uniform(0.5, 2.0), 4)
            r_bc = round(self._rng.uniform(0.5, 2.0), 4)
            # Introduce slight deviation for arbitrage opportunity
            fair_r_ca = round(1.0 / (r_ab * r_bc), 4)
            deviation = round(self._rng.uniform(-0.05, 0.05), 4)
            r_ca = round(fair_r_ca + deviation, 4)
            product = round(r_ab * r_bc * r_ca, 4)
            arbitrage = product != 1.0
            desc = (
                f"{c1}/{c2} = {r_ab}, {c2}/{c3} = {r_bc}, "
                f"{c3}/{c1} = {r_ca}; arbitrage possible?"
            )
            return desc, {
                "mode": "arbitrage", "c1": c1, "c2": c2, "c3": c3,
                "r_ab": r_ab, "r_bc": r_bc, "r_ca": r_ca,
                "product": product, "arbitrage": arbitrage,
            }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        if sd["mode"] == "convert":
            return [
                f"rate {sd['c1']}/{sd['c2']} = {sd['rate']}",
                f"{sd['amount']} * {sd['rate']} = {sd['converted']}",
            ]
        return [
            f"{sd['c1']}/{sd['c2']} * {sd['c2']}/{sd['c3']} * {sd['c3']}/{sd['c1']}",
            f"= {sd['r_ab']} * {sd['r_bc']} * {sd['r_ca']} = {sd['product']}",
            f"if product != 1 -> arbitrage exists",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the conversion result or arbitrage verdict.

        Args:
            sd: Solution data.

        Returns:
            Result string.
        """
        if sd["mode"] == "convert":
            return f"{sd['converted']} {sd['c2']}"
        verdict = "yes" if sd["arbitrage"] else "no"
        return f"product = {sd['product']}, arbitrage = {verdict}"


# ===================================================================
# 5. Inflation / real rate (Fisher equation)  (tier 4)
# ===================================================================

@register
class InflationRealRateGenerator(StepGenerator):
    """Convert between nominal and real interest rates.

    Fisher equation: (1+r) = (1+i)/(1+pi), or approximately r = i - pi.
    Given nominal rate i and inflation pi, compute real rate r.

    Difficulty scaling:
        Difficulty 1-3: approximate formula r = i - pi.
        Difficulty 4-6: exact Fisher equation.
        Difficulty 7-8: solve for i or pi given the other two.

    Prerequisites:
        division.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "inflation_real_rate"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["division"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "compute real rate using Fisher equation"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Fisher equation problem.

        Creates nominal rate and inflation rate, then computes the
        real rate using either the approximate or exact formula.

        Args:
            difficulty: Controls which formula and direction.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        i_rate = round(self._rng.uniform(0.02, 0.15), 4)
        pi_rate = round(self._rng.uniform(0.01, 0.10), 4)

        if difficulty <= 3:
            r_approx = round(i_rate - pi_rate, 4)
            desc = (
                f"nominal rate i = {round(i_rate * 100, 2)}%, "
                f"inflation pi = {round(pi_rate * 100, 2)}%; "
                f"real rate (approx)?"
            )
            return desc, {
                "mode": "approx", "i": i_rate, "pi": pi_rate,
                "r": r_approx,
            }
        elif difficulty <= 6:
            r_exact = round((1 + i_rate) / (1 + pi_rate) - 1, 4)
            desc = (
                f"nominal rate i = {round(i_rate * 100, 2)}%, "
                f"inflation pi = {round(pi_rate * 100, 2)}%; "
                f"exact real rate?"
            )
            return desc, {
                "mode": "exact", "i": i_rate, "pi": pi_rate,
                "r": r_exact,
            }
        else:
            # Given r and pi, find i
            r_rate = round(self._rng.uniform(0.01, 0.08), 4)
            i_calc = round((1 + r_rate) * (1 + pi_rate) - 1, 4)
            desc = (
                f"real rate r = {round(r_rate * 100, 2)}%, "
                f"inflation pi = {round(pi_rate * 100, 2)}%; "
                f"find nominal rate i"
            )
            return desc, {
                "mode": "find_i", "r": r_rate, "pi": pi_rate,
                "i": i_calc,
            }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        if sd["mode"] == "approx":
            return [
                "r ~ i - pi (approximation)",
                f"r = {sd['i']} - {sd['pi']} = {sd['r']}",
                f"r = {round(sd['r'] * 100, 4)}%",
            ]
        elif sd["mode"] == "exact":
            return [
                "(1+r) = (1+i)/(1+pi)",
                f"(1+r) = (1+{sd['i']})/(1+{sd['pi']})",
                f"r = {sd['r']} = {round(sd['r'] * 100, 4)}%",
            ]
        else:
            return [
                "(1+i) = (1+r)*(1+pi)",
                f"(1+i) = (1+{sd['r']})*(1+{sd['pi']})",
                f"i = {sd['i']} = {round(sd['i'] * 100, 4)}%",
            ]

    def _create_answer(self, sd: dict) -> str:
        """Return the computed rate.

        Args:
            sd: Solution data.

        Returns:
            Rate as a string.
        """
        if sd["mode"] in ("approx", "exact"):
            return f"r = {round(sd['r'] * 100, 4)}%"
        return f"i = {round(sd['i'] * 100, 4)}%"


# ===================================================================
# 6. Production function  (tier 5)
# ===================================================================

@register
class ProductionFunctionGenerator(StepGenerator):
    """Analyse a production function for marginal products and returns to scale.

    Given Q = A * L^alpha * K^beta, compute MPL = dQ/dL, MPK = dQ/dK,
    and determine returns to scale: if alpha + beta > 1 (increasing),
    = 1 (constant), or < 1 (decreasing).

    Difficulty scaling:
        Difficulty 1-3: compute Q only.
        Difficulty 4-6: compute MPL and MPK.
        Difficulty 7-8: determine returns to scale.

    Prerequisites:
        derivative.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "production_function"

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
            Short task description string.
        """
        return "analyse production function: MPL, MPK, returns to scale"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a production function analysis problem.

        Creates a Cobb-Douglas-style production function and asks for
        output, marginal products, and/or returns to scale.

        Args:
            difficulty: Controls what is asked.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        a_coeff = round(self._rng.uniform(1.0, 5.0), 2)
        alpha = round(self._rng.uniform(0.2, 0.8), 2)
        beta = round(self._rng.uniform(0.2, 0.8), 2)
        l_val = self._rng.randint(10, 100)
        k_val = self._rng.randint(10, 100)

        q = round(a_coeff * l_val ** alpha * k_val ** beta, 4)
        mpl = round(alpha * a_coeff * l_val ** (alpha - 1) * k_val ** beta, 4)
        mpk = round(beta * a_coeff * l_val ** alpha * k_val ** (beta - 1), 4)

        sum_exp = round(alpha + beta, 4)
        if sum_exp > 1.0:
            rts = "increasing"
        elif sum_exp < 1.0:
            rts = "decreasing"
        else:
            rts = "constant"

        desc = (
            f"Q = {a_coeff}*L^{alpha}*K^{beta}, "
            f"L = {l_val}, K = {k_val}"
        )
        if difficulty <= 3:
            desc += "; compute Q"
        elif difficulty <= 6:
            desc += "; compute Q, MPL, MPK"
        else:
            desc += "; compute Q, MPL, MPK, returns to scale"

        return desc, {
            "a": a_coeff, "alpha": alpha, "beta": beta,
            "l": l_val, "k": k_val,
            "q": q, "mpl": mpl, "mpk": mpk,
            "sum_exp": sum_exp, "rts": rts,
            "difficulty": difficulty,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        steps = [
            f"Q = {sd['a']}*{sd['l']}^{sd['alpha']}*{sd['k']}^{sd['beta']} = {sd['q']}",
        ]
        if sd["difficulty"] > 3:
            steps.extend([
                f"MPL = alpha*Q/L = {sd['alpha']}*{sd['q']}/{sd['l']} = {sd['mpl']}",
                f"MPK = beta*Q/K = {sd['beta']}*{sd['q']}/{sd['k']} = {sd['mpk']}",
            ])
        if sd["difficulty"] > 6:
            steps.append(
                f"alpha+beta = {sd['sum_exp']} -> {sd['rts']} returns to scale"
            )
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the production function analysis results.

        Args:
            sd: Solution data.

        Returns:
            Result string.
        """
        if sd["difficulty"] <= 3:
            return f"Q = {sd['q']}"
        elif sd["difficulty"] <= 6:
            return f"Q = {sd['q']}, MPL = {sd['mpl']}, MPK = {sd['mpk']}"
        return (
            f"Q = {sd['q']}, MPL = {sd['mpl']}, MPK = {sd['mpk']}, "
            f"RTS = {sd['rts']}"
        )


# ===================================================================
# 7. Game theory: Cournot duopoly  (tier 5)
# ===================================================================

@register
class GameTheoryMarketGenerator(StepGenerator):
    """Solve a Cournot duopoly for Nash equilibrium.

    Market demand: P = a - (q1 + q2). Firms have constant marginal
    cost c. Best response: q1 = (a - c - q2) / 2. Symmetric Nash
    equilibrium: q* = (a - c) / 3, P* = (a + 2c) / 3.

    Difficulty scaling:
        Difficulty 1-3: symmetric costs, compute q* and P*.
        Difficulty 4-6: asymmetric costs c1 != c2.
        Difficulty 7-8: compute profits and total surplus.

    Prerequisites:
        system_equations.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "game_theory_market"

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
        return "solve Cournot duopoly for Nash equilibrium"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Cournot duopoly problem.

        Creates demand and cost parameters, then solves for the
        Nash equilibrium quantities and market price.

        Args:
            difficulty: Controls symmetry and what is computed.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        a = self._rng.randint(50, 200)

        if difficulty <= 3:
            c = self._rng.randint(5, a // 3)
            q_star = round((a - c) / 3, 4)
            q_total = round(2 * q_star, 4)
            p_star = round(a - q_total, 4)
            desc = f"P = {a} - Q, c = {c} (symmetric); Nash eq?"
            return desc, {
                "mode": "symmetric", "a": a, "c": c,
                "q_star": q_star, "q_total": q_total, "p_star": p_star,
            }
        else:
            c1 = self._rng.randint(5, a // 4)
            c2 = self._rng.randint(5, a // 4)
            # q1 = (a - 2c1 + c2) / 3, q2 = (a - 2c2 + c1) / 3
            q1 = round((a - 2 * c1 + c2) / 3, 4)
            q2 = round((a - 2 * c2 + c1) / 3, 4)
            q_total = round(q1 + q2, 4)
            p_star = round(a - q_total, 4)
            profit1 = round((p_star - c1) * q1, 4)
            profit2 = round((p_star - c2) * q2, 4)
            desc = f"P = {a} - Q, c1 = {c1}, c2 = {c2}; Nash eq?"
            return desc, {
                "mode": "asymmetric", "a": a, "c1": c1, "c2": c2,
                "q1": q1, "q2": q2, "q_total": q_total, "p_star": p_star,
                "profit1": profit1, "profit2": profit2,
                "difficulty": difficulty,
            }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        if sd["mode"] == "symmetric":
            return [
                f"BR: q_i = ({sd['a']} - {sd['c']} - q_j)/2",
                f"symmetric: q* = ({sd['a']} - {sd['c']})/3 = {sd['q_star']}",
                f"Q = 2*{sd['q_star']} = {sd['q_total']}",
                f"P* = {sd['a']} - {sd['q_total']} = {sd['p_star']}",
            ]
        steps = [
            f"BR1: q1 = ({sd['a']} - 2*{sd['c1']} + {sd['c2']})/3 = {sd['q1']}",
            f"BR2: q2 = ({sd['a']} - 2*{sd['c2']} + {sd['c1']})/3 = {sd['q2']}",
            f"Q = {sd['q1']} + {sd['q2']} = {sd['q_total']}",
            f"P* = {sd['a']} - {sd['q_total']} = {sd['p_star']}",
        ]
        if sd.get("difficulty", 0) > 6:
            steps.append(
                f"pi1 = ({sd['p_star']}-{sd['c1']})*{sd['q1']} = {sd['profit1']}"
            )
            steps.append(
                f"pi2 = ({sd['p_star']}-{sd['c2']})*{sd['q2']} = {sd['profit2']}"
            )
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the Nash equilibrium quantities and price.

        Args:
            sd: Solution data.

        Returns:
            Result string.
        """
        if sd["mode"] == "symmetric":
            return f"q* = {sd['q_star']}, P* = {sd['p_star']}"
        ans = f"q1 = {sd['q1']}, q2 = {sd['q2']}, P* = {sd['p_star']}"
        if sd.get("difficulty", 0) > 6:
            ans += f", pi1 = {sd['profit1']}, pi2 = {sd['profit2']}"
        return ans


# ===================================================================
# 8. Time value of money  (tier 4)
# ===================================================================

@register
class TimeValueMoneyGenerator(StepGenerator):
    """Compute future value, present value, or annuity present value.

    FV = PV * (1+r)^n. Annuity PV = PMT * (1 - (1+r)^{-n}) / r.

    Difficulty scaling:
        Difficulty 1-3: simple FV from PV.
        Difficulty 4-6: PV from FV (discounting).
        Difficulty 7-8: annuity present value.

    Prerequisites:
        exponentiation.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "time_value_money"

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
        return "compute time value of money (FV, PV, or annuity)"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a time value of money problem.

        Creates principal, rate, and time parameters, then computes
        future value, present value, or annuity present value.

        Args:
            difficulty: Controls problem variant.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        r = round(self._rng.uniform(0.02, 0.12), 3)
        n = self._rng.randint(1, min(15, 3 + difficulty * 2))

        if difficulty <= 3:
            pv = self._rng.randint(100, 5000) * 10
            fv = round(pv * (1 + r) ** n, 4)
            desc = f"PV = {pv}, r = {round(r * 100, 1)}%, n = {n}; find FV"
            return desc, {
                "mode": "fv", "pv": pv, "r": r, "n": n, "fv": fv,
            }
        elif difficulty <= 6:
            fv = self._rng.randint(100, 5000) * 10
            pv = round(fv / (1 + r) ** n, 4)
            desc = f"FV = {fv}, r = {round(r * 100, 1)}%, n = {n}; find PV"
            return desc, {
                "mode": "pv", "fv": fv, "r": r, "n": n, "pv": pv,
            }
        else:
            pmt = self._rng.randint(50, 500) * 10
            annuity_pv = round(pmt * (1 - (1 + r) ** (-n)) / r, 4)
            desc = (
                f"PMT = {pmt}, r = {round(r * 100, 1)}%, "
                f"n = {n}; annuity PV?"
            )
            return desc, {
                "mode": "annuity", "pmt": pmt, "r": r, "n": n,
                "annuity_pv": annuity_pv,
            }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        if sd["mode"] == "fv":
            factor = round((1 + sd["r"]) ** sd["n"], 4)
            return [
                f"FV = PV * (1+r)^n",
                f"(1+{sd['r']})^{sd['n']} = {factor}",
                f"FV = {sd['pv']} * {factor} = {sd['fv']}",
            ]
        elif sd["mode"] == "pv":
            factor = round((1 + sd["r"]) ** sd["n"], 4)
            return [
                f"PV = FV / (1+r)^n",
                f"(1+{sd['r']})^{sd['n']} = {factor}",
                f"PV = {sd['fv']} / {factor} = {sd['pv']}",
            ]
        else:
            discount = round((1 + sd["r"]) ** (-sd["n"]), 4)
            factor = round((1 - discount) / sd["r"], 4)
            return [
                "PV_annuity = PMT * (1 - (1+r)^{-n}) / r",
                f"(1+{sd['r']})^(-{sd['n']}) = {discount}",
                f"factor = (1 - {discount})/{sd['r']} = {factor}",
                f"PV = {sd['pmt']} * {factor} = {sd['annuity_pv']}",
            ]

    def _create_answer(self, sd: dict) -> str:
        """Return the computed value.

        Args:
            sd: Solution data.

        Returns:
            Result string.
        """
        if sd["mode"] == "fv":
            return f"FV = {sd['fv']}"
        elif sd["mode"] == "pv":
            return f"PV = {sd['pv']}"
        else:
            return f"PV_annuity = {sd['annuity_pv']}"
