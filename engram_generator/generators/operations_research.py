"""Operations research generators -- queues, inventory, scheduling, and more.

Covers M/M/1 and M/M/c queues, EOQ inventory, newsvendor,
project scheduling (CPM), Markov decision processes,
linear congruential generators, and system reliability.
Tiers range from 4 (introductory OR) to 6 (advanced).
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


class _ORFormatter:
    """Formats numeric values for operations research problems.

    Provides consistent rounding and clean string representations
    to keep target text compact.
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


_f = _ORFormatter.fmt


# ===================================================================
# 1. M/M/1 queue  (tier 5)
# ===================================================================

@register
class MM1QueueGenerator(StepGenerator):
    """M/M/1 queue metrics: rho, L, W.

    Computes server utilisation rho = lambda/mu, expected number
    in system L = rho/(1-rho), and expected time in system
    W = 1/(mu-lambda).

    Difficulty scaling:
        Difficulty 1-3: integer rates, low utilisation.
        Difficulty 4-6: decimal rates, moderate utilisation.
        Difficulty 7-8: high utilisation (rho > 0.9).

    Prerequisites:
        division.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "mm1_queue"

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
        return "compute M/M/1 queue metrics"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate arrival and service rates and compute queue metrics.

        Args:
            difficulty: Controls utilisation range.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            mu = self._rng.randint(5, 15)
            lam = self._rng.randint(1, mu - 1)
        elif difficulty <= 6:
            mu = round(self._rng.uniform(5, 20), 1)
            lam = round(self._rng.uniform(1, mu - 0.5), 1)
        else:
            mu = round(self._rng.uniform(10, 30), 1)
            lam = round(mu * self._rng.uniform(0.9, 0.98), 1)
            if lam >= mu:
                lam = round(mu - 0.1, 1)

        rho = round(lam / mu, 4)
        l_sys = round(rho / (1 - rho), 4)
        w_sys = round(1 / (mu - lam), 4)
        l_q = round(rho ** 2 / (1 - rho), 4)
        w_q = round(lam / (mu * (mu - lam)), 4)

        return "\\rho = \\lambda/\\mu,\\; L = \\rho/(1-\\rho)", {
            "lam": lam, "mu": mu, "rho": rho,
            "L": l_sys, "W": w_sys,
            "Lq": l_q, "Wq": w_q,
            "full": difficulty >= 4,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate queue computation steps.

        Args:
            data: Solution data with rates and metrics.

        Returns:
            List of step strings.
        """
        steps = [
            f"lambda={_f(data['lam'])}, mu={_f(data['mu'])}",
            f"rho = lambda/mu = {_f(data['rho'])}",
            f"L = rho/(1-rho) = {_f(data['L'])}",
            f"W = 1/(mu-lambda) = {_f(data['W'])}",
        ]
        if data["full"]:
            steps.append(f"Lq = {_f(data['Lq'])}, Wq = {_f(data['Wq'])}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the queue metrics.

        Args:
            data: Solution data.

        Returns:
            String with rho, L, and W.
        """
        if data["full"]:
            return (
                f"rho={_f(data['rho'])}, L={_f(data['L'])}, "
                f"W={_f(data['W'])}, Lq={_f(data['Lq'])}"
            )
        return f"rho={_f(data['rho'])}, L={_f(data['L'])}, W={_f(data['W'])}"


# ===================================================================
# 2. M/M/c queue  (tier 6)
# ===================================================================

@register
class MMCQueueGenerator(StepGenerator):
    """M/M/c queue: compute P_0 using the Erlang-C formula for c=2 or 3.

    Builds the Erlang-C summation for small server counts and
    computes the probability of zero customers in the system.

    Difficulty scaling:
        Difficulty 1-3: c=2, integer rates.
        Difficulty 4-6: c=2 or 3, decimal rates.
        Difficulty 7-8: c=3, also compute P(wait) and Lq.

    Prerequisites:
        mm1_queue.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "mmc_queue"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["mm1_queue"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute M/M/c queue probability P_0"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate M/M/c parameters and compute P_0 via Erlang-C.

        Args:
            difficulty: Controls server count and rate ranges.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            c = 2
            mu = self._rng.randint(4, 10)
            lam = self._rng.randint(2, 2 * mu - 1)
        elif difficulty <= 6:
            c = self._rng.choice([2, 3])
            mu = round(self._rng.uniform(3, 10), 1)
            lam = round(self._rng.uniform(1, c * mu - 0.5), 1)
        else:
            c = 3
            mu = round(self._rng.uniform(5, 12), 1)
            lam = round(self._rng.uniform(c * mu * 0.7, c * mu - 0.5), 1)

        a = round(lam / mu, 4)  # offered load
        rho = round(a / c, 4)

        # P_0 = [sum_{n=0}^{c-1} a^n/n! + a^c/c! * 1/(1-rho)]^{-1}
        sum_part = 0.0
        for n in range(c):
            sum_part += a ** n / math.factorial(n)
        tail = (a ** c / math.factorial(c)) * (1 / (1 - rho))
        p0 = round(1.0 / (sum_part + tail), 4)

        # P(wait) = Erlang-C
        p_wait = round((a ** c / math.factorial(c)) * p0 / (1 - rho), 4)
        lq = round(p_wait * rho / (1 - rho), 4)

        return "P_0 = \\left[\\sum_{n=0}^{c-1}\\frac{a^n}{n!} + \\frac{a^c}{c!}\\frac{1}{1-\\rho}\\right]^{-1}", {
            "lam": lam, "mu": mu, "c": c, "a": a, "rho": rho,
            "sum_part": round(sum_part, 4),
            "tail": round(tail, 4),
            "P0": p0, "P_wait": p_wait, "Lq": lq,
            "full": difficulty >= 7,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Erlang-C computation steps.

        Args:
            data: Solution data with rates, c, and P_0.

        Returns:
            List of step strings.
        """
        steps = [
            f"lambda={_f(data['lam'])}, mu={_f(data['mu'])}, c={data['c']}",
            f"a = lambda/mu = {_f(data['a'])}, rho = a/c = {_f(data['rho'])}",
            f"sum = {_f(data['sum_part'])}, tail = {_f(data['tail'])}",
            f"P_0 = 1/(sum+tail) = {_f(data['P0'])}",
        ]
        if data["full"]:
            steps.append(
                f"P(wait)={_f(data['P_wait'])}, Lq={_f(data['Lq'])}"
            )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return P_0 and optionally P(wait) and Lq.

        Args:
            data: Solution data.

        Returns:
            String with queue probabilities.
        """
        if data["full"]:
            return (
                f"P_0={_f(data['P0'])}, P(wait)={_f(data['P_wait'])}, "
                f"Lq={_f(data['Lq'])}"
            )
        return f"P_0 = {_f(data['P0'])}"


# ===================================================================
# 3. Inventory EOQ  (tier 4)
# ===================================================================

@register
class InventoryEOQGenerator(StepGenerator):
    """Economic order quantity: EOQ = sqrt(2*D*S/H).

    Given annual demand D, setup cost S, and holding cost H,
    computes the optimal order quantity and total cost.

    Difficulty scaling:
        Difficulty 1-3: small integer demand and costs.
        Difficulty 4-6: larger values, also compute total cost.
        Difficulty 7-8: compute reorder point with lead time.

    Prerequisites:
        multiplication.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "inventory_eoq"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["multiplication"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute economic order quantity"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate demand, setup, and holding costs, then compute EOQ.

        Args:
            difficulty: Controls value ranges and problem variant.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            d = self._rng.randint(100, 1000)
            s = self._rng.randint(10, 50)
            h = self._rng.randint(1, 10)
        else:
            d = self._rng.randint(500, 5000 + difficulty * 1000)
            s = round(self._rng.uniform(20, 200), 1)
            h = round(self._rng.uniform(1, 20 + difficulty * 2), 1)

        eoq = round(math.sqrt(2 * d * s / h), 4)
        n_orders = round(d / eoq, 4)
        tc = round(d * s / eoq + eoq * h / 2, 4)

        data = {
            "D": d, "S": s, "H": h,
            "EOQ": eoq, "N_orders": n_orders, "TC": tc,
            "full": difficulty >= 4,
        }

        if difficulty >= 7:
            lead = self._rng.randint(1, 14)
            daily_d = round(d / 365, 4)
            rop = round(daily_d * lead, 4)
            data["lead"] = lead
            data["daily_D"] = daily_d
            data["ROP"] = rop

        return "EOQ = \\sqrt{\\frac{2DS}{H}}", data

    def _create_steps(self, data: dict) -> list[str]:
        """Generate EOQ computation steps.

        Args:
            data: Solution data with D, S, H, and EOQ.

        Returns:
            List of step strings.
        """
        inside = round(2 * data["D"] * data["S"] / data["H"], 4)
        steps = [
            f"D={_f(data['D'])}, S={_f(data['S'])}, H={_f(data['H'])}",
            f"2DS/H = {_f(inside)}",
            f"EOQ = sqrt({_f(inside)}) = {_f(data['EOQ'])}",
        ]
        if data["full"]:
            steps.append(f"TC = DS/EOQ + EOQ*H/2 = {_f(data['TC'])}")
        if "ROP" in data:
            steps.append(
                f"daily_D={_f(data['daily_D'])}, lead={data['lead']}d, "
                f"ROP={_f(data['ROP'])}"
            )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the EOQ and optionally total cost.

        Args:
            data: Solution data.

        Returns:
            String with EOQ result.
        """
        result = f"EOQ = {_f(data['EOQ'])}"
        if data["full"]:
            result += f", TC = {_f(data['TC'])}"
        if "ROP" in data:
            result += f", ROP = {_f(data['ROP'])}"
        return result


# ===================================================================
# 4. Newsvendor  (tier 5)
# ===================================================================

@register
class NewsvendorGenerator(StepGenerator):
    """Newsvendor problem: optimal order Q* where F(Q*) = (p-c)/(p-s).

    Computes the critical ratio and optimal order quantity assuming
    a uniform demand distribution.

    Difficulty scaling:
        Difficulty 1-3: small integer prices, uniform demand.
        Difficulty 4-6: wider price ranges, compute expected profit.
        Difficulty 7-8: also compute expected leftover and shortage.

    Prerequisites:
        division.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "newsvendor"

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
        return "solve newsvendor optimal order quantity"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate price, cost, salvage, and demand range for newsvendor.

        Args:
            difficulty: Controls price ranges and extra computations.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            p = self._rng.randint(8, 20)
            c = self._rng.randint(3, p - 2)
            s = self._rng.randint(0, c - 1)
        else:
            p = self._rng.randint(10, 50 + difficulty * 10)
            c = self._rng.randint(max(3, p // 3), p - 2)
            s = self._rng.randint(0, max(0, c - 2))

        cr = round((p - c) / (p - s), 4)

        # Uniform demand U[a, b]
        a = self._rng.randint(10, 50)
        b = a + self._rng.randint(20, 100 + difficulty * 20)

        q_star = round(a + cr * (b - a), 4)

        data = {
            "p": p, "c": c, "s": s,
            "CR": cr, "a": a, "b": b, "Q_star": q_star,
            "full": difficulty >= 4,
        }

        if difficulty >= 7:
            # Expected leftover and shortage
            e_left = round((b - q_star) ** 2 / (2 * (b - a)), 4) if q_star < b else 0.0
            e_short = round((q_star - a) ** 2 / (2 * (b - a)), 4) if q_star > a else 0.0
            data["E_left"] = round(e_left, 4)
            data["E_short"] = round(e_short, 4)

        return "F(Q^*) = \\frac{p-c}{p-s}", data

    def _create_steps(self, data: dict) -> list[str]:
        """Generate newsvendor computation steps.

        Args:
            data: Solution data with prices and critical ratio.

        Returns:
            List of step strings.
        """
        steps = [
            f"p={data['p']}, c={data['c']}, s={data['s']}",
            f"CR = (p-c)/(p-s) = ({data['p']}-{data['c']})/({data['p']}-{data['s']}) = {_f(data['CR'])}",
            f"demand ~ U[{data['a']},{data['b']}]",
            f"Q* = {data['a']} + {_f(data['CR'])}*({data['b']}-{data['a']}) = {_f(data['Q_star'])}",
        ]
        if "E_left" in data:
            steps.append(
                f"E[leftover]={_f(data['E_left'])}, "
                f"E[shortage]={_f(data['E_short'])}"
            )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the optimal order quantity.

        Args:
            data: Solution data.

        Returns:
            String with Q* and critical ratio.
        """
        result = f"Q* = {_f(data['Q_star'])}, CR = {_f(data['CR'])}"
        if "E_left" in data:
            result += f", E[left]={_f(data['E_left'])}"
        return result


# ===================================================================
# 5. Project scheduling (CPM)  (tier 5)
# ===================================================================

@register
class ProjectSchedulingGenerator(StepGenerator):
    """CPM critical path: find the critical path in an activity network.

    Builds a small DAG of 4-6 activities with durations, computes
    earliest start, latest start, and identifies the critical path.

    Difficulty scaling:
        Difficulty 1-3: 4 activities, simple linear chains.
        Difficulty 4-6: 5 activities with parallel branches.
        Difficulty 7-8: 6 activities, compute float for each.

    Prerequisites:
        sorting.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "project_scheduling"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["sorting"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "find critical path in project network"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an activity network and compute CPM metrics.

        Args:
            difficulty: Controls number of activities.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            # A -> B -> D, A -> C -> D
            durations = {
                "A": self._rng.randint(2, 6),
                "B": self._rng.randint(3, 8),
                "C": self._rng.randint(2, 7),
                "D": self._rng.randint(2, 5),
            }
            preds = {"A": [], "B": ["A"], "C": ["A"], "D": ["B", "C"]}
        elif difficulty <= 6:
            durations = {
                "A": self._rng.randint(2, 6),
                "B": self._rng.randint(3, 8),
                "C": self._rng.randint(2, 7),
                "D": self._rng.randint(2, 6),
                "E": self._rng.randint(3, 7),
            }
            preds = {
                "A": [], "B": ["A"], "C": ["A"],
                "D": ["B"], "E": ["C", "D"],
            }
        else:
            durations = {
                "A": self._rng.randint(2, 6),
                "B": self._rng.randint(3, 8),
                "C": self._rng.randint(2, 7),
                "D": self._rng.randint(2, 6),
                "E": self._rng.randint(3, 7),
                "F": self._rng.randint(2, 5),
            }
            preds = {
                "A": [], "B": ["A"], "C": ["A"],
                "D": ["B"], "E": ["C"], "F": ["D", "E"],
            }

        # Forward pass
        es: dict[str, int] = {}
        topo = list(durations.keys())
        for act in topo:
            if not preds[act]:
                es[act] = 0
            else:
                es[act] = max(es[p] + durations[p] for p in preds[act])
        ef = {act: es[act] + durations[act] for act in topo}

        project_duration = max(ef.values())

        # Backward pass
        ls: dict[str, int] = {}
        lf: dict[str, int] = {}
        for act in reversed(topo):
            successors = [s for s in topo if act in preds[s]]
            if not successors:
                lf[act] = project_duration
            else:
                lf[act] = min(ls[s] for s in successors)
            ls[act] = lf[act] - durations[act]

        slack = {act: ls[act] - es[act] for act in topo}
        critical = [act for act in topo if slack[act] == 0]

        return "ES_j = \\max_{i \\in pred(j)}(ES_i + d_i)", {
            "durations": durations, "preds": preds,
            "ES": es, "EF": ef, "LS": ls, "LF": lf,
            "slack": slack, "critical": critical,
            "T": project_duration,
            "show_float": difficulty >= 7,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate CPM computation steps.

        Args:
            data: Solution data with ES, LS, slack, and critical path.

        Returns:
            List of step strings.
        """
        dur_str = ", ".join(
            f"{a}={d}" for a, d in data["durations"].items()
        )
        steps = [
            f"durations: {dur_str}",
        ]
        es_str = ", ".join(f"{a}={data['ES'][a]}" for a in data["ES"])
        steps.append(f"ES: {es_str}")
        steps.append(f"project duration T={data['T']}")
        steps.append(f"critical path: {'-'.join(data['critical'])}")
        if data["show_float"]:
            fl_str = ", ".join(
                f"{a}={data['slack'][a]}" for a in data["slack"]
            )
            steps.append(f"float: {fl_str}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the critical path and project duration.

        Args:
            data: Solution data.

        Returns:
            String with critical path and T.
        """
        return (
            f"critical path: {'-'.join(data['critical'])}, "
            f"T = {data['T']}"
        )


# ===================================================================
# 6. Markov decision process (one iteration)  (tier 6)
# ===================================================================

@register
class MarkovDecisionGenerator(StepGenerator):
    """Policy iteration: evaluate V = R + gamma*P*V, then improve.

    Builds a 2-state MDP with 2 actions per state. Performs one
    round of policy evaluation and one improvement step.

    Difficulty scaling:
        Difficulty 1-3: gamma=0.9, simple transitions.
        Difficulty 4-6: varied gamma, verify improvement.
        Difficulty 7-8: 3 states, compute full policy iteration.

    Prerequisites:
        expected_value.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "markov_decision"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["expected_value"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "perform one policy iteration step in MDP"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a small MDP and perform one policy iteration round.

        Args:
            difficulty: Controls number of states and gamma.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 6:
            n = 2
        else:
            n = 3

        if difficulty <= 3:
            gamma = 0.9
        else:
            gamma = round(self._rng.uniform(0.8, 0.99), 2)

        # Rewards for current policy (one action per state)
        r = [self._rng.randint(1, 10) for _ in range(n)]

        # Transition probs under current policy (row i -> state j)
        p_mat: list[list[float]] = []
        for i in range(n):
            row = [round(self._rng.uniform(0.1, 0.9), 2) for _ in range(n)]
            total = sum(row)
            row = [round(x / total, 4) for x in row]
            p_mat.append(row)

        # Solve V = R + gamma * P * V via direct solve for 2-state
        # (I - gamma*P) V = R
        if n == 2:
            a11 = 1 - gamma * p_mat[0][0]
            a12 = -gamma * p_mat[0][1]
            a21 = -gamma * p_mat[1][0]
            a22 = 1 - gamma * p_mat[1][1]
            det = a11 * a22 - a12 * a21
            v0 = round((a22 * r[0] - a12 * r[1]) / det, 4)
            v1 = round((-a21 * r[0] + a11 * r[1]) / det, 4)
            v = [v0, v1]
        else:
            # 3-state: iterative for simplicity (20 iterations)
            v = [0.0] * n
            for _ in range(50):
                v_new = []
                for i in range(n):
                    val = r[i] + gamma * sum(
                        p_mat[i][j] * v[j] for j in range(n)
                    )
                    v_new.append(val)
                v = v_new
            v = [round(x, 4) for x in v]

        # Alternative action rewards for improvement check
        r_alt = [self._rng.randint(1, 10) for _ in range(n)]
        p_alt: list[list[float]] = []
        for i in range(n):
            row = [round(self._rng.uniform(0.1, 0.9), 2) for _ in range(n)]
            total = sum(row)
            row = [round(x / total, 4) for x in row]
            p_alt.append(row)

        # Q-values for alternative action
        q_alt = [
            round(r_alt[i] + gamma * sum(
                p_alt[i][j] * v[j] for j in range(n)
            ), 4) for i in range(n)
        ]
        # Q-values for current policy
        q_cur = [
            round(r[i] + gamma * sum(
                p_mat[i][j] * v[j] for j in range(n)
            ), 4) for i in range(n)
        ]
        improved = [
            "alt" if q_alt[i] > q_cur[i] else "cur"
            for i in range(n)
        ]

        return "V = R + \\gamma P V", {
            "n": n, "gamma": gamma, "R": r, "P": p_mat,
            "V": v, "R_alt": r_alt, "P_alt": p_alt,
            "Q_cur": q_cur, "Q_alt": q_alt,
            "improved": improved,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate policy iteration steps.

        Args:
            data: Solution data with MDP parameters and values.

        Returns:
            List of step strings.
        """
        v_str = ", ".join(f"V{i}={_f(data['V'][i])}" for i in range(data["n"]))
        steps = [
            f"gamma={data['gamma']}, states={data['n']}",
            f"R={data['R']}",
            f"evaluate: {v_str}",
        ]
        for i in range(data["n"]):
            steps.append(
                f"s{i}: Q_cur={_f(data['Q_cur'][i])}, "
                f"Q_alt={_f(data['Q_alt'][i])} -> {data['improved'][i]}"
            )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the value function and improved policy.

        Args:
            data: Solution data.

        Returns:
            String with V and policy.
        """
        v_str = ", ".join(f"V{i}={_f(data['V'][i])}" for i in range(data["n"]))
        pi_str = ", ".join(
            f"s{i}={data['improved'][i]}" for i in range(data["n"])
        )
        return f"{v_str}; policy: {pi_str}"


# ===================================================================
# 7. Simulation LCG  (tier 4)
# ===================================================================

@register
class SimulationLCGGenerator(StepGenerator):
    """Linear congruential generator: X_{n+1} = (a*X_n + c) mod m.

    Generates 5 pseudo-random numbers and normalises to [0,1].

    Difficulty scaling:
        Difficulty 1-3: small modulus (m <= 64), simple params.
        Difficulty 4-6: larger modulus, compute U_i = X_i/m.
        Difficulty 7-8: test period length of the sequence.

    Prerequisites:
        multiplication.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "simulation_lcg"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["multiplication"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "generate pseudo-random numbers with LCG"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate LCG parameters and compute 5 values.

        Args:
            difficulty: Controls modulus size.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            m = self._rng.choice([16, 32, 64])
            a = self._rng.choice([5, 7, 11, 13])
            c = self._rng.choice([1, 3, 7])
        else:
            m = self._rng.choice([128, 256, 512])
            a = self._rng.randint(5, 31)
            c = self._rng.randint(1, 15)

        x0 = self._rng.randint(1, m - 1)

        xs = [x0]
        for _ in range(5):
            xs.append((a * xs[-1] + c) % m)

        us = [round(x / m, 4) for x in xs[1:]]

        # Check period (up to m steps)
        if difficulty >= 7:
            seen = {x0}
            xn = x0
            period = 0
            for _ in range(m):
                xn = (a * xn + c) % m
                period += 1
                if xn in seen:
                    break
                seen.add(xn)
        else:
            period = None

        return "X_{n+1} = (aX_n + c) \\bmod m", {
            "a": a, "c": c, "m": m, "X0": x0,
            "Xs": xs[1:], "Us": us,
            "period": period,
            "full": difficulty >= 4,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate LCG computation steps.

        Args:
            data: Solution data with parameters and sequence.

        Returns:
            List of step strings.
        """
        steps = [
            f"a={data['a']}, c={data['c']}, m={data['m']}, X0={data['X0']}",
        ]
        prev = data["X0"]
        for i, x in enumerate(data["Xs"][:3]):
            steps.append(
                f"X{i+1} = ({data['a']}*{prev}+{data['c']}) mod {data['m']} = {x}"
            )
            prev = x
        x_str = ", ".join(str(x) for x in data["Xs"])
        steps.append(f"sequence: [{x_str}]")
        if data["full"]:
            u_str = ", ".join(_f(u) for u in data["Us"])
            steps.append(f"U = [{u_str}]")
        if data["period"] is not None:
            steps.append(f"period = {data['period']}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the generated sequence.

        Args:
            data: Solution data.

        Returns:
            String with the pseudo-random sequence.
        """
        x_str = ", ".join(str(x) for x in data["Xs"])
        result = f"X = [{x_str}]"
        if data["period"] is not None:
            result += f", period = {data['period']}"
        return result


# ===================================================================
# 8. Reliability  (tier 5)
# ===================================================================

@register
class ReliabilityGenerator(StepGenerator):
    """System reliability: series R_s = prod R_i, parallel R_p = 1 - prod(1-R_i).

    Computes overall reliability for series, parallel, or
    series-parallel configurations.

    Difficulty scaling:
        Difficulty 1-3: pure series or parallel (2-3 components).
        Difficulty 4-6: series-parallel combination (4 components).
        Difficulty 7-8: complex configuration (5+ components).

    Prerequisites:
        multiplication.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "reliability"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["multiplication"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute system reliability"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate component reliabilities and compute system reliability.

        Args:
            difficulty: Controls configuration complexity.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            config = self._rng.choice(["series", "parallel"])
            n = self._rng.randint(2, 3)
            rs = [round(self._rng.uniform(0.8, 0.99), 4) for _ in range(n)]
            if config == "series":
                r_sys = round(math.prod(rs), 4)
            else:
                r_sys = round(1 - math.prod(1 - r for r in rs), 4)
            return "R_s = \\prod R_i", {
                "config": config, "components": rs, "R_sys": r_sys,
            }

        # Series-parallel: two parallel subsystems in series
        n1 = self._rng.randint(2, 3)
        n2 = self._rng.randint(2, 3)
        rs1 = [round(self._rng.uniform(0.7, 0.98), 4) for _ in range(n1)]
        rs2 = [round(self._rng.uniform(0.7, 0.98), 4) for _ in range(n2)]
        r_par1 = round(1 - math.prod(1 - r for r in rs1), 4)
        r_par2 = round(1 - math.prod(1 - r for r in rs2), 4)
        r_sys = round(r_par1 * r_par2, 4)

        return "R_s = \\prod R_{par,i}", {
            "config": "series-parallel",
            "sub1": rs1, "sub2": rs2,
            "R_par1": r_par1, "R_par2": r_par2,
            "R_sys": r_sys,
            "components": rs1 + rs2,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate reliability computation steps.

        Args:
            data: Solution data with component reliabilities.

        Returns:
            List of step strings.
        """
        config = data["config"]
        if config == "series":
            r_str = ", ".join(_f(r) for r in data["components"])
            prod_val = _f(data["R_sys"])
            return [
                f"series: R = [{r_str}]",
                f"R_sys = prod = {prod_val}",
            ]
        if config == "parallel":
            r_str = ", ".join(_f(r) for r in data["components"])
            q_str = ", ".join(
                _f(1 - r) for r in data["components"]
            )
            return [
                f"parallel: R = [{r_str}]",
                f"1-R = [{q_str}]",
                f"R_sys = 1 - prod(1-R_i) = {_f(data['R_sys'])}",
            ]
        # series-parallel
        s1_str = ", ".join(_f(r) for r in data["sub1"])
        s2_str = ", ".join(_f(r) for r in data["sub2"])
        return [
            f"subsystem1 (par): [{s1_str}] -> R1={_f(data['R_par1'])}",
            f"subsystem2 (par): [{s2_str}] -> R2={_f(data['R_par2'])}",
            f"R_sys = R1*R2 = {_f(data['R_sys'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the system reliability.

        Args:
            data: Solution data.

        Returns:
            String with R_sys.
        """
        return f"R_sys = {_f(data['R_sys'])}"
