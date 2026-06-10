"""Advanced economics generators.

6 generators across tiers 4-6 covering Cobb-Douglas production,
price elasticity, auction revenue, supply-demand equilibrium,
comparative advantage, and utility maximisation.
"""
from __future__ import annotations

import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


# ---------------------------------------------------------------------------
# 1. Cobb-Douglas (tier 5)
# ---------------------------------------------------------------------------

@register
class CobbDouglasGenerator(StepGenerator):
    """Compute output from a Cobb-Douglas production function.

    Given Y = A * K^alpha * L^(1-alpha) with parameters A (total factor
    productivity), K (capital), L (labour), and alpha, compute the
    output Y.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "cobb_douglas"

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
            Task instruction string.
        """
        return "compute Cobb-Douglas output Y = A * K^alpha * L^(1-alpha)"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Cobb-Douglas computation problem.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        a = round(self._rng.uniform(0.5, 3.0), 2)
        k = self._rng.randint(10, 50 * max(1, difficulty))
        l_val = self._rng.randint(10, 50 * max(1, difficulty))
        alpha = round(self._rng.uniform(0.2, 0.8), 2)
        k_part = round(k ** alpha, 4)
        l_part = round(l_val ** (1 - alpha), 4)
        y = round(a * k_part * l_part, 4)
        problem = f"Y = A*K^alpha*L^(1-alpha); A={a}, K={k}, L={l_val}, alpha={alpha}"
        return problem, {
            "a": a, "k": k, "l": l_val, "alpha": alpha,
            "k_part": k_part, "l_part": l_part, "y": y,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate computation steps.

        Args:
            sd: All computed solution information.

        Returns:
            Steps showing intermediate calculations.
        """
        return [
            f"K^alpha = {sd['k']}^{sd['alpha']} = {sd['k_part']}",
            f"L^(1-alpha) = {sd['l']}^{round(1 - sd['alpha'], 2)} = {sd['l_part']}",
            f"Y = {sd['a']} * {sd['k_part']} * {sd['l_part']} = {sd['y']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the computed output.

        Args:
            sd: All computed solution information.

        Returns:
            Output Y rounded to 4 decimal places.
        """
        return str(sd["y"])


# ---------------------------------------------------------------------------
# 2. Elasticity (tier 4)
# ---------------------------------------------------------------------------

@register
class ElasticityGenerator(StepGenerator):
    """Compute price elasticity of demand.

    Given a linear demand function Q(P) = a - bP, compute the price
    elasticity Ed = (dQ/dP) * (P/Q) at a specific price point.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "elasticity"

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
            Task instruction string.
        """
        return "compute price elasticity of demand"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an elasticity computation problem.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        a = self._rng.randint(50, 200)
        b = self._rng.randint(1, min(10, 2 + difficulty))
        # Ensure P gives positive Q
        max_p = (a - 1) // b
        p = self._rng.randint(1, max(1, max_p))
        q = a - b * p
        # dQ/dP = -b for linear demand
        dq_dp = -b
        ed = round(dq_dp * (p / q), 4)
        problem = f"Q(P) = {a} - {b}P; price elasticity at P={p}"
        return problem, {
            "a": a, "b": b, "p": p, "q": q,
            "dq_dp": dq_dp, "ed": ed,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate elasticity computation steps.

        Args:
            sd: All computed solution information.

        Returns:
            Steps showing derivative and ratio calculation.
        """
        return [
            f"Q({sd['p']}) = {sd['a']} - {sd['b']}*{sd['p']} = {sd['q']}",
            f"dQ/dP = -{sd['b']}",
            f"Ed = (dQ/dP)*(P/Q) = {sd['dq_dp']}*({sd['p']}/{sd['q']}) = {sd['ed']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the elasticity value.

        Args:
            sd: All computed solution information.

        Returns:
            Price elasticity rounded to 4 decimal places.
        """
        return str(sd["ed"])


# ---------------------------------------------------------------------------
# 3. Auction Revenue (tier 5)
# ---------------------------------------------------------------------------

@register
class AuctionRevenueGenerator(StepGenerator):
    """Compute expected revenue in a second-price auction.

    With n bidders drawing values uniformly from [0, 1], the expected
    revenue equals the expected second-highest bid: E[R] = (n-1)/(n+1).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "auction_revenue"

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
            Task instruction string.
        """
        return "compute expected revenue in second-price auction"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an auction revenue problem.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        n = self._rng.randint(2, min(10, 2 + difficulty * 2))
        revenue = round((n - 1) / (n + 1), 4)
        problem = (
            f"second-price auction, {n} bidders, values ~ Uniform[0,1]; "
            f"expected revenue?"
        )
        return problem, {"n": n, "revenue": revenue}

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate auction revenue derivation steps.

        Args:
            sd: All computed solution information.

        Returns:
            Steps showing the order statistic formula.
        """
        n = sd["n"]
        return [
            f"second-price: winner pays second-highest bid",
            f"E[2nd order stat of {n} Uniform[0,1]] = (n-1)/(n+1)",
            f"E[R] = ({n}-1)/({n}+1) = {n - 1}/{n + 1} = {sd['revenue']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the expected revenue.

        Args:
            sd: All computed solution information.

        Returns:
            Expected revenue rounded to 4 decimal places.
        """
        return str(sd["revenue"])


# ---------------------------------------------------------------------------
# 4. Supply-Demand Equilibrium (tier 4)
# ---------------------------------------------------------------------------

@register
class SupplyDemandEquilibriumGenerator(StepGenerator):
    """Find market equilibrium price and quantity.

    Given linear supply Qs = a + bP and demand Qd = c - dP, solve
    for the equilibrium price P* and quantity Q*.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "supply_demand_equilibrium"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["system_equations"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task instruction string.
        """
        return "find supply-demand equilibrium"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a supply-demand equilibrium problem.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        # Qs = a + b*P, Qd = c - d*P
        # Equilibrium: a + b*P = c - d*P => P* = (c - a) / (b + d)
        b = self._rng.randint(1, max(1, difficulty))
        d = self._rng.randint(1, max(1, difficulty))
        # Choose a, c so P* is positive and integer-friendly
        a = self._rng.randint(0, 20)
        # c must be > a for positive equilibrium price
        c = a + (b + d) * self._rng.randint(1, min(10, 2 + difficulty))
        p_star = round((c - a) / (b + d), 4)
        q_star = round(a + b * p_star, 4)
        problem = f"Qs = {a} + {b}P, Qd = {c} - {d}P; find equilibrium"
        return problem, {
            "a": a, "b": b, "c": c, "d": d,
            "p_star": p_star, "q_star": q_star,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate equilibrium solving steps.

        Args:
            sd: All computed solution information.

        Returns:
            Steps showing the algebra.
        """
        return [
            f"set Qs = Qd: {sd['a']} + {sd['b']}P = {sd['c']} - {sd['d']}P",
            f"({sd['b']}+{sd['d']})P = {sd['c']}-{sd['a']}",
            f"P* = {sd['c'] - sd['a']}/{sd['b'] + sd['d']} = {sd['p_star']}",
            f"Q* = {sd['a']} + {sd['b']}*{sd['p_star']} = {sd['q_star']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the equilibrium price and quantity.

        Args:
            sd: All computed solution information.

        Returns:
            P* and Q* values.
        """
        return f"P*={sd['p_star']}, Q*={sd['q_star']}"


# ---------------------------------------------------------------------------
# 5. Comparative Advantage (tier 4)
# ---------------------------------------------------------------------------

@register
class ComparativeAdvantageGenerator(StepGenerator):
    """Determine comparative advantage from production possibilities.

    Given two countries producing two goods, compute opportunity costs
    and identify which country has comparative advantage in each good.
    """

    _GOODS: list[tuple[str, str]] = [
        ("wheat", "cloth"),
        ("cars", "computers"),
        ("wine", "cheese"),
        ("steel", "textiles"),
    ]

    _COUNTRIES: list[tuple[str, str]] = [
        ("Alpha", "Beta"),
        ("North", "South"),
        ("Avalon", "Borealis"),
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "comparative_advantage"

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
            Task instruction string.
        """
        return "determine comparative advantage"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a comparative advantage problem.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        goods = self._GOODS[difficulty % len(self._GOODS)]
        countries = self._COUNTRIES[difficulty % len(self._COUNTRIES)]

        # Production per unit of labour
        scale = max(1, difficulty)
        a1 = self._rng.randint(2 * scale, 10 * scale)  # country A, good 1
        a2 = self._rng.randint(2 * scale, 10 * scale)  # country A, good 2
        b1 = self._rng.randint(2 * scale, 10 * scale)  # country B, good 1
        b2 = self._rng.randint(2 * scale, 10 * scale)  # country B, good 2

        # Opportunity costs
        oc_a1 = round(a2 / a1, 4)  # cost of good1 in terms of good2 for A
        oc_b1 = round(b2 / b1, 4)  # cost of good1 in terms of good2 for B

        # Comparative advantage: lower opportunity cost
        if oc_a1 < oc_b1:
            adv_good1 = countries[0]
            adv_good2 = countries[1]
        elif oc_a1 > oc_b1:
            adv_good1 = countries[1]
            adv_good2 = countries[0]
        else:
            adv_good1 = "neither (equal)"
            adv_good2 = "neither (equal)"

        problem = (
            f"{countries[0]}: {a1} {goods[0]}, {a2} {goods[1]}; "
            f"{countries[1]}: {b1} {goods[0]}, {b2} {goods[1]}; "
            f"who has comparative advantage?"
        )
        return problem, {
            "countries": countries, "goods": goods,
            "a1": a1, "a2": a2, "b1": b1, "b2": b2,
            "oc_a1": oc_a1, "oc_b1": oc_b1,
            "adv_good1": adv_good1, "adv_good2": adv_good2,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate comparative advantage analysis steps.

        Args:
            sd: All computed solution information.

        Returns:
            Steps showing opportunity cost calculations.
        """
        c = sd["countries"]
        g = sd["goods"]
        return [
            f"{c[0]} OC of 1 {g[0]} = {sd['a2']}/{sd['a1']} = {sd['oc_a1']} {g[1]}",
            f"{c[1]} OC of 1 {g[0]} = {sd['b2']}/{sd['b1']} = {sd['oc_b1']} {g[1]}",
            f"lower OC in {g[0]}: {sd['adv_good1']}",
            f"lower OC in {g[1]}: {sd['adv_good2']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return comparative advantage assignments.

        Args:
            sd: All computed solution information.

        Returns:
            Which country has advantage in which good.
        """
        g = sd["goods"]
        return f"{g[0]}: {sd['adv_good1']}; {g[1]}: {sd['adv_good2']}"


# ---------------------------------------------------------------------------
# 6. Utility Maximise (tier 6)
# ---------------------------------------------------------------------------

@register
class UtilityMaximiseGenerator(StepGenerator):
    """Maximise utility subject to a budget constraint using Lagrange.

    Given U(x,y) = x^a * y^b and budget p_x*x + p_y*y = M, solve
    for optimal x*, y* and maximum utility using the Lagrange method.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "utility_maximise"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["lagrange_multiplier"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task instruction string.
        """
        return "maximise utility with budget constraint (Lagrange)"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a utility maximisation problem.

        For Cobb-Douglas U = x^a * y^b with budget p_x*x + p_y*y = M,
        the optimal allocation is:
            x* = (a / (a+b)) * (M / p_x)
            y* = (b / (a+b)) * (M / p_y)

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        # Use simple integer exponents for cleaner arithmetic
        a_exp = self._rng.randint(1, min(4, 1 + difficulty))
        b_exp = self._rng.randint(1, min(4, 1 + difficulty))

        # Prices and income chosen to give clean results
        px = self._rng.randint(1, min(10, 2 + difficulty))
        py = self._rng.randint(1, min(10, 2 + difficulty))
        # Make M divisible by both prices to get nicer numbers
        m_base = self._rng.randint(5, 20 * max(1, difficulty))
        m = m_base * (a_exp + b_exp) * px * py // math.gcd(px, py)
        # Cap M to keep output short
        m = min(m, 10000)

        # Optimal allocation for Cobb-Douglas
        total_exp = a_exp + b_exp
        x_star = round((a_exp / total_exp) * (m / px), 4)
        y_star = round((b_exp / total_exp) * (m / py), 4)
        u_star = round(x_star ** a_exp * y_star ** b_exp, 4)

        problem = (
            f"max U(x,y) = x^{a_exp} * y^{b_exp} "
            f"s.t. {px}x + {py}y = {m}"
        )
        return problem, {
            "a_exp": a_exp, "b_exp": b_exp,
            "px": px, "py": py, "m": m,
            "x_star": x_star, "y_star": y_star, "u_star": u_star,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate Lagrange optimisation steps.

        Args:
            sd: All computed solution information.

        Returns:
            Steps showing the Lagrange conditions and solution.
        """
        a = sd["a_exp"]
        b = sd["b_exp"]
        return [
            f"L = x^{a}*y^{b} - lam*({sd['px']}x + {sd['py']}y - {sd['m']})",
            f"dL/dx = {a}*x^{a - 1}*y^{b} - lam*{sd['px']} = 0",
            f"dL/dy = {b}*x^{a}*y^{b - 1} - lam*{sd['py']} = 0",
            f"x* = ({a}/{a + b})*({sd['m']}/{sd['px']}) = {sd['x_star']}",
            f"y* = ({b}/{a + b})*({sd['m']}/{sd['py']}) = {sd['y_star']}",
            f"U* = {sd['x_star']}^{a} * {sd['y_star']}^{b} = {sd['u_star']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the optimal allocation and utility.

        Args:
            sd: All computed solution information.

        Returns:
            Optimal x*, y*, and U*.
        """
        return f"x*={sd['x_star']}, y*={sd['y_star']}, U*={sd['u_star']}"
