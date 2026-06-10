"""Extended queuing theory generators -- Erlang, Little's law, M/G/1, Jackson, priority.

Covers Erlang-B and Erlang-C blocking/waiting probabilities, Little's law,
Pollaczek-Khinchine M/G/1 formula, open Jackson networks, and
non-preemptive priority queuing. Tiers range from 4 to 6.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


class _QFmt:
    """Formats numeric values for queuing theory problems.

    Provides consistent rounding and clean string representations
    to keep target text compact.
    """

    @staticmethod
    def f(value: float, decimals: int = 4) -> str:
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


_f = _QFmt.f


# ===================================================================
# 1. Erlang-B  (tier 5)
# ===================================================================

@register
class ErlangBGenerator(StepGenerator):
    """Erlang-B blocking probability: B(N,A) = (A^N/N!) / sum_{k=0}^{N} (A^k/k!).

    Computes the probability that all N servers are busy given
    traffic intensity A (in Erlangs). Used for loss systems where
    blocked calls are cleared.

    Difficulty scaling:
        Difficulty 1-3: N=2-3 servers, integer traffic intensity.
        Difficulty 4-6: N=3-5 servers, decimal traffic intensity.
        Difficulty 7-8: N=5-8 servers, high traffic.

    Prerequisites:
        exponentiation.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "erlang_b"

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
        return "compute Erlang-B blocking probability"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate server count and traffic intensity, compute B(N,A).

        Args:
            difficulty: Controls server count and traffic range.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            n = self._rng.randint(2, 3)
            a = float(self._rng.randint(1, n + 1))
        elif difficulty <= 6:
            n = self._rng.randint(3, 5)
            a = round(self._rng.uniform(1.0, n + 2), 1)
        else:
            n = self._rng.randint(5, 8)
            a = round(self._rng.uniform(n * 0.6, n + 3), 1)

        # Compute B(N,A) using iterative Erlang-B recursion for stability
        b = 1.0
        for k in range(1, n + 1):
            b = (a * b) / (k + a * b)
        b = round(b, 4)

        # Also compute via direct formula for steps
        numerator = round(a ** n / math.factorial(n), 4)
        denom_sum = sum(a ** k / math.factorial(k) for k in range(n + 1))
        denom_sum = round(denom_sum, 4)

        return "B(N,A) = \\frac{A^N/N!}{\\sum_{k=0}^{N} A^k/k!}", {
            "N": n, "A": a, "numerator": numerator,
            "denom_sum": denom_sum, "B": b,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Erlang-B computation steps.

        Args:
            data: Solution data with N, A, and blocking probability.

        Returns:
            List of step strings.
        """
        return [
            f"N={data['N']}, A={_f(data['A'])}",
            f"A^N/N! = {_f(data['A'])}^{data['N']}/{data['N']}! = {_f(data['numerator'])}",
            f"sum_{{k=0}}^{{{data['N']}}} A^k/k! = {_f(data['denom_sum'])}",
            f"B({data['N']},{_f(data['A'])}) = {_f(data['numerator'])}/{_f(data['denom_sum'])} = {_f(data['B'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the Erlang-B blocking probability.

        Args:
            data: Solution data.

        Returns:
            String with B(N,A).
        """
        return f"B({data['N']},{_f(data['A'])}) = {_f(data['B'])}"


# ===================================================================
# 2. Erlang-C  (tier 5)
# ===================================================================

@register
class ErlangCGenerator(StepGenerator):
    """Erlang-C waiting probability: C(N,A) = (A^N/N! * N/(N-A)) / (sum + A^N/N! * N/(N-A)).

    Computes the probability that an arriving customer must wait
    (all servers busy) in an M/M/N queue with no losses.

    Difficulty scaling:
        Difficulty 1-3: N=2 servers, integer traffic.
        Difficulty 4-6: N=2-3 servers, decimal traffic, compute Wq.
        Difficulty 7-8: N=3-4 servers, high utilisation.

    Prerequisites:
        erlang_b.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "erlang_c"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["erlang_b"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute Erlang-C waiting probability"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate server count and traffic, compute C(N,A) and optional Wq.

        Args:
            difficulty: Controls server count and traffic range.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            n = 2
            a = float(self._rng.randint(1, n))
            if a >= n:
                a = n - 0.5
        elif difficulty <= 6:
            n = self._rng.choice([2, 3])
            a = round(self._rng.uniform(0.5, n - 0.2), 1)
        else:
            n = self._rng.choice([3, 4])
            a = round(self._rng.uniform(n * 0.7, n - 0.1), 1)

        if a >= n:
            a = round(n - 0.1, 1)

        # sum_{k=0}^{N-1} A^k/k!
        sum_part = sum(a ** k / math.factorial(k) for k in range(n))
        sum_part = round(sum_part, 4)

        # A^N/N! * N/(N-A)
        tail = (a ** n / math.factorial(n)) * (n / (n - a))
        tail = round(tail, 4)

        c_val = round(tail / (sum_part + tail), 4)

        # Optional: average waiting time Wq = C(N,A) / (N*mu - lambda)
        # Use mu=1 so A = lambda/mu = lambda
        mu = round(self._rng.uniform(2.0, 8.0), 1)
        lam = round(a * mu, 4)
        wq = round(c_val / (n * mu - lam), 4) if difficulty >= 4 else None

        return "C(N,A) = \\frac{A^N/N! \\cdot N/(N-A)}{\\sum_{k=0}^{N-1} A^k/k! + A^N/N! \\cdot N/(N-A)}", {
            "N": n, "A": a, "sum_part": sum_part,
            "tail": tail, "C": c_val,
            "mu": mu, "lam": lam, "Wq": wq,
            "full": difficulty >= 4,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Erlang-C computation steps.

        Args:
            data: Solution data with N, A, and waiting probability.

        Returns:
            List of step strings.
        """
        steps = [
            f"N={data['N']}, A={_f(data['A'])}",
            f"sum = {_f(data['sum_part'])}",
            f"tail = A^N/N! * N/(N-A) = {_f(data['tail'])}",
            f"C({data['N']},{_f(data['A'])}) = {_f(data['tail'])}/({_f(data['sum_part'])}+{_f(data['tail'])}) = {_f(data['C'])}",
        ]
        if data["full"] and data["Wq"] is not None:
            steps.append(
                f"mu={_f(data['mu'])}, Wq = C/(N*mu-lambda) = {_f(data['Wq'])}"
            )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the Erlang-C probability and optional Wq.

        Args:
            data: Solution data.

        Returns:
            String with C(N,A).
        """
        result = f"C({data['N']},{_f(data['A'])}) = {_f(data['C'])}"
        if data["full"] and data["Wq"] is not None:
            result += f", Wq = {_f(data['Wq'])}"
        return result


# ===================================================================
# 3. Little's law  (tier 4)
# ===================================================================

@register
class LittlesLawGenerator(StepGenerator):
    """Little's law: L = lambda * W, Lq = lambda * Wq.

    Given any two of {L, lambda, W}, computes the third.
    Higher difficulties also use the queue variant Lq = lambda * Wq.

    Difficulty scaling:
        Difficulty 1-3: integer values, compute L from lambda and W.
        Difficulty 4-6: decimal values, random unknown quantity.
        Difficulty 7-8: also compute Lq = lambda * Wq.

    Prerequisites:
        multiplication.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "littles_law"

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
        return "apply Little's law to compute queue metric"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate queue parameters and apply L = lambda * W.

        Args:
            difficulty: Controls value ranges and variant.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            lam = float(self._rng.randint(2, 10))
            w = float(self._rng.randint(1, 5))
            unknown = "L"
        elif difficulty <= 6:
            lam = round(self._rng.uniform(1.0, 20.0), 2)
            w = round(self._rng.uniform(0.5, 10.0), 2)
            unknown = self._rng.choice(["L", "lambda", "W"])
        else:
            lam = round(self._rng.uniform(2.0, 30.0), 2)
            w = round(self._rng.uniform(0.5, 8.0), 2)
            unknown = self._rng.choice(["L", "lambda", "W"])

        l_val = round(lam * w, 4)

        data = {
            "lambda": lam, "W": w, "L": l_val, "unknown": unknown,
        }

        if difficulty >= 7:
            wq = round(self._rng.uniform(0.1, w * 0.8), 2)
            lq = round(lam * wq, 4)
            data["Wq"] = wq
            data["Lq"] = lq
            data["has_queue"] = True
        else:
            data["has_queue"] = False

        return "L = \\lambda W", data

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Little's law computation steps.

        Args:
            data: Solution data with queue parameters.

        Returns:
            List of step strings.
        """
        unknown = data["unknown"]
        if unknown == "L":
            steps = [
                f"lambda={_f(data['lambda'])}, W={_f(data['W'])}",
                f"L = lambda * W = {_f(data['lambda'])} * {_f(data['W'])} = {_f(data['L'])}",
            ]
        elif unknown == "lambda":
            steps = [
                f"L={_f(data['L'])}, W={_f(data['W'])}",
                f"lambda = L / W = {_f(data['L'])} / {_f(data['W'])} = {_f(data['lambda'])}",
            ]
        else:
            steps = [
                f"L={_f(data['L'])}, lambda={_f(data['lambda'])}",
                f"W = L / lambda = {_f(data['L'])} / {_f(data['lambda'])} = {_f(data['W'])}",
            ]

        if data["has_queue"]:
            steps.append(
                f"Lq = lambda * Wq = {_f(data['lambda'])} * {_f(data['Wq'])} = {_f(data['Lq'])}"
            )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the computed unknown.

        Args:
            data: Solution data.

        Returns:
            String with the solved quantity.
        """
        unknown = data["unknown"]
        if unknown == "L":
            result = f"L = {_f(data['L'])}"
        elif unknown == "lambda":
            result = f"lambda = {_f(data['lambda'])}"
        else:
            result = f"W = {_f(data['W'])}"

        if data["has_queue"]:
            result += f", Lq = {_f(data['Lq'])}"
        return result


# ===================================================================
# 4. M/G/1 queue  (tier 6)
# ===================================================================

@register
class MG1QueueGenerator(StepGenerator):
    """M/G/1 queue via Pollaczek-Khinchine: Lq = lambda^2 * E[S^2] / (2*(1-rho)).

    Computes queue length for an M/G/1 queue given arrival rate and
    first two moments of the service time distribution.

    Difficulty scaling:
        Difficulty 1-3: deterministic service (E[S^2] = E[S]^2).
        Difficulty 4-6: general service with given E[S] and E[S^2].
        Difficulty 7-8: also compute Wq, W, and L.

    Prerequisites:
        mm1_queue.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "mg1_queue"

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
        return "compute M/G/1 queue length via Pollaczek-Khinchine"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate arrival rate and service moments, compute Lq.

        Args:
            difficulty: Controls service distribution complexity.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            lam = float(self._rng.randint(1, 5))
            es = round(1.0 / self._rng.randint(2, 8), 4)
            es2 = round(es ** 2, 4)  # deterministic
        elif difficulty <= 6:
            lam = round(self._rng.uniform(1.0, 8.0), 1)
            es = round(self._rng.uniform(0.05, 0.4), 4)
            cv = round(self._rng.uniform(0.5, 2.0), 2)  # coefficient of variation
            var_s = round((cv * es) ** 2, 4)
            es2 = round(var_s + es ** 2, 4)
        else:
            lam = round(self._rng.uniform(2.0, 12.0), 1)
            es = round(self._rng.uniform(0.02, 0.3), 4)
            cv = round(self._rng.uniform(1.0, 3.0), 2)
            var_s = round((cv * es) ** 2, 4)
            es2 = round(var_s + es ** 2, 4)

        rho = round(lam * es, 4)
        if rho >= 1.0:
            lam = round(0.8 / es, 4)
            rho = round(lam * es, 4)

        lq = round(lam ** 2 * es2 / (2 * (1 - rho)), 4)

        data = {
            "lambda": lam, "ES": es, "ES2": es2, "rho": rho, "Lq": lq,
            "full": difficulty >= 7,
        }

        if difficulty >= 7:
            wq = round(lq / lam, 4)
            w = round(wq + es, 4)
            l_sys = round(lam * w, 4)
            data["Wq"] = wq
            data["W"] = w
            data["L"] = l_sys

        return "L_q = \\frac{\\lambda^2 E[S^2]}{2(1-\\rho)}", data

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Pollaczek-Khinchine computation steps.

        Args:
            data: Solution data with arrival rate and service moments.

        Returns:
            List of step strings.
        """
        steps = [
            f"lambda={_f(data['lambda'])}, E[S]={_f(data['ES'])}, E[S^2]={_f(data['ES2'])}",
            f"rho = lambda*E[S] = {_f(data['rho'])}",
            f"Lq = lambda^2*E[S^2]/(2*(1-rho)) = {_f(data['Lq'])}",
        ]
        if data["full"]:
            steps.append(f"Wq = Lq/lambda = {_f(data['Wq'])}")
            steps.append(f"W = Wq + E[S] = {_f(data['W'])}, L = lambda*W = {_f(data['L'])}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the M/G/1 queue metrics.

        Args:
            data: Solution data.

        Returns:
            String with Lq and optional full metrics.
        """
        result = f"Lq = {_f(data['Lq'])}, rho = {_f(data['rho'])}"
        if data["full"]:
            result += f", W = {_f(data['W'])}, L = {_f(data['L'])}"
        return result


# ===================================================================
# 5. Jackson network  (tier 6)
# ===================================================================

@register
class JacksonNetworkGenerator(StepGenerator):
    """Open Jackson network: solve lambda_i = gamma_i + sum r_ji * lambda_j.

    Solves traffic equations for a 2-3 node open network. Each node
    behaves as an independent M/M/1 queue once the effective arrival
    rates are found.

    Difficulty scaling:
        Difficulty 1-3: 2 nodes, simple routing.
        Difficulty 4-6: 3 nodes, split routing.
        Difficulty 7-8: 3 nodes, compute per-node L and total L.

    Prerequisites:
        mm1_queue.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "jackson_network"

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
        return "solve traffic equations in open Jackson network"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a small Jackson network and solve traffic equations.

        Args:
            difficulty: Controls number of nodes and complexity.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            # 2-node: gamma -> node1 -> node2 -> exit
            gamma = [float(self._rng.randint(2, 8)), 0.0]
            r = [[0.0, 1.0], [0.0, 0.0]]  # node1 -> node2
            mu = [float(self._rng.randint(5, 15)),
                  float(self._rng.randint(5, 15))]
            # lambda_1 = gamma_1, lambda_2 = lambda_1
            lam = [gamma[0], gamma[0]]
        elif difficulty <= 6:
            # 3-node: external arrivals, routing with splits
            gamma = [round(self._rng.uniform(2, 8), 1), 0.0, 0.0]
            p12 = round(self._rng.uniform(0.3, 0.7), 2)
            p13 = round(1 - p12, 2)
            r = [
                [0.0, p12, p13],
                [0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0],
            ]
            mu = [round(self._rng.uniform(5, 15), 1) for _ in range(3)]
            # lambda_1 = gamma_1, lambda_2 = p12*lambda_1, lambda_3 = p13*lambda_1
            lam = [
                gamma[0],
                round(p12 * gamma[0], 4),
                round(p13 * gamma[0], 4),
            ]
        else:
            # 3-node: with feedback
            gamma = [round(self._rng.uniform(3, 10), 1), 0.0, 0.0]
            p12 = round(self._rng.uniform(0.4, 0.6), 2)
            p13 = round(1 - p12, 2)
            p21 = round(self._rng.uniform(0.1, 0.3), 2)
            r = [
                [0.0, p12, p13],
                [p21, 0.0, 0.0],
                [0.0, 0.0, 0.0],
            ]
            mu = [round(self._rng.uniform(8, 20), 1) for _ in range(3)]
            # Solve: lambda_1 = gamma_1 + p21*lambda_2
            #        lambda_2 = p12*lambda_1
            #        lambda_3 = p13*lambda_1
            # lambda_1 = gamma_1 + p21*p12*lambda_1
            # lambda_1*(1 - p21*p12) = gamma_1
            lam_1 = round(gamma[0] / (1 - p21 * p12), 4)
            lam_2 = round(p12 * lam_1, 4)
            lam_3 = round(p13 * lam_1, 4)
            lam = [lam_1, lam_2, lam_3]

        n = len(gamma)

        # Ensure stability: lambda_i < mu_i
        for i in range(n):
            if lam[i] >= mu[i]:
                mu[i] = round(lam[i] + self._rng.uniform(1, 5), 1)

        rho = [round(lam[i] / mu[i], 4) for i in range(n)]
        l_node = [round(rho[i] / (1 - rho[i]), 4) for i in range(n)]
        l_total = round(sum(l_node), 4)

        return "\\lambda_i = \\gamma_i + \\sum_j r_{ji} \\lambda_j", {
            "n": n, "gamma": gamma, "r": r, "mu": mu,
            "lambda": lam, "rho": rho,
            "L_node": l_node, "L_total": l_total,
            "full": difficulty >= 7,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Jackson network computation steps.

        Args:
            data: Solution data with traffic equations and metrics.

        Returns:
            List of step strings.
        """
        n = data["n"]
        gamma_str = ", ".join(_f(g) for g in data["gamma"])
        steps = [f"nodes={n}, gamma=[{gamma_str}]"]

        lam_str = ", ".join(
            f"lambda_{i+1}={_f(data['lambda'][i])}" for i in range(n)
        )
        steps.append(f"traffic: {lam_str}")

        mu_str = ", ".join(f"mu_{i+1}={_f(data['mu'][i])}" for i in range(n))
        rho_str = ", ".join(
            f"rho_{i+1}={_f(data['rho'][i])}" for i in range(n)
        )
        steps.append(f"{mu_str}")
        steps.append(f"{rho_str}")

        if data["full"]:
            l_str = ", ".join(
                f"L_{i+1}={_f(data['L_node'][i])}" for i in range(n)
            )
            steps.append(f"{l_str}, L_total={_f(data['L_total'])}")

        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the effective arrival rates and optional metrics.

        Args:
            data: Solution data.

        Returns:
            String with lambda values.
        """
        n = data["n"]
        lam_str = ", ".join(
            f"lambda_{i+1}={_f(data['lambda'][i])}" for i in range(n)
        )
        result = lam_str
        if data["full"]:
            result += f", L_total={_f(data['L_total'])}"
        return result


# ===================================================================
# 6. Priority queue  (tier 5)
# ===================================================================

@register
class PriorityQueueGenerator(StepGenerator):
    """Non-preemptive priority queue: W_k = W_0 / ((1-sigma_{k-1})(1-sigma_k)).

    Computes waiting time per priority class where sigma_k is the
    cumulative utilisation up to class k, and W_0 is the base
    waiting time (average residual service).

    Difficulty scaling:
        Difficulty 1-3: 2 priority classes, integer rates.
        Difficulty 4-6: 3 classes, decimal rates.
        Difficulty 7-8: 3 classes, compute Lq per class.

    Prerequisites:
        division.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "priority_queue"

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
        return "compute waiting time per priority class"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate arrival and service rates per class, compute W_k.

        Args:
            difficulty: Controls number of classes and rate ranges.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            n_classes = 2
            lam = [float(self._rng.randint(1, 5)) for _ in range(n_classes)]
            mu = float(self._rng.randint(8, 15))
        elif difficulty <= 6:
            n_classes = 3
            lam = [round(self._rng.uniform(0.5, 4.0), 1) for _ in range(n_classes)]
            mu = round(self._rng.uniform(8, 20), 1)
        else:
            n_classes = 3
            lam = [round(self._rng.uniform(1.0, 5.0), 1) for _ in range(n_classes)]
            mu = round(self._rng.uniform(10, 25), 1)

        # Ensure stability: total rho < 1
        rho = [round(l / mu, 4) for l in lam]
        total_rho = sum(rho)
        if total_rho >= 0.95:
            mu = round(sum(lam) / 0.8, 1)
            rho = [round(l / mu, 4) for l in lam]

        # sigma_k = sum of rho_0..rho_k
        sigma = []
        cumul = 0.0
        for r in rho:
            cumul += r
            sigma.append(round(cumul, 4))

        # W_0 = base waiting = sum(rho_k / mu) / ... simplified as
        # W_0 = sum(lambda_k / mu^2) = sum(rho_k / mu)
        w0 = round(sum(r / mu for r in lam) / 1.0, 4)  # sum(lambda_k * E[S^2]/2)
        # For M/M/1 per class: E[S^2] = 2/mu^2, so W_0 = sum(lambda_k/mu^2)
        w0 = round(sum(l / (mu ** 2) for l in lam), 4)

        # W_k = W_0 / ((1-sigma_{k-1})(1-sigma_k))
        # sigma_{-1} = 0
        w_class = []
        for k in range(n_classes):
            s_prev = 0.0 if k == 0 else sigma[k - 1]
            s_curr = sigma[k]
            denom = (1 - s_prev) * (1 - s_curr)
            if denom <= 0:
                denom = 0.001
            w_k = round(w0 / denom, 4)
            w_class.append(w_k)

        data = {
            "n_classes": n_classes, "lambda": lam, "mu": mu,
            "rho": rho, "sigma": sigma, "W0": w0,
            "W_class": w_class,
            "full": difficulty >= 7,
        }

        if difficulty >= 7:
            lq_class = [round(lam[k] * w_class[k], 4) for k in range(n_classes)]
            data["Lq_class"] = lq_class

        return "W_k = \\frac{W_0}{(1-\\sigma_{k-1})(1-\\sigma_k)}", data

    def _create_steps(self, data: dict) -> list[str]:
        """Generate priority queue computation steps.

        Args:
            data: Solution data with per-class waiting times.

        Returns:
            List of step strings.
        """
        n = data["n_classes"]
        lam_str = ", ".join(
            f"lambda_{k+1}={_f(data['lambda'][k])}" for k in range(n)
        )
        rho_str = ", ".join(
            f"rho_{k+1}={_f(data['rho'][k])}" for k in range(n)
        )
        steps = [
            f"mu={_f(data['mu'])}, {lam_str}",
            f"{rho_str}",
            f"W_0 = {_f(data['W0'])}",
        ]
        for k in range(n):
            steps.append(f"W_{k+1} = {_f(data['W_class'][k])}")

        if data["full"] and "Lq_class" in data:
            lq_str = ", ".join(
                f"Lq_{k+1}={_f(data['Lq_class'][k])}" for k in range(n)
            )
            steps.append(lq_str)
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the per-class waiting times.

        Args:
            data: Solution data.

        Returns:
            String with W_k for each class.
        """
        n = data["n_classes"]
        w_str = ", ".join(
            f"W_{k+1}={_f(data['W_class'][k])}" for k in range(n)
        )
        return w_str
