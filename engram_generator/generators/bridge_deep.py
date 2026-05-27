"""Bridge and deep-topic generators connecting lower tiers to 7-10.

Adds 16 generators: probability (3), differential equations (3),
abstract algebra (3), formal proofs (4), prerequisite bridges (3).
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


# ═══════════════════════════════════════════════════════════════════
# DEEPER PROBABILITY (3 generators, tiers 4-5)
# ═══════════════════════════════════════════════════════════════════

@register
class BayesChainGenerator(StepGenerator):
    """Apply Bayes' theorem with sequential evidence updates."""

    @property
    def task_name(self) -> str:
        return "bayes_chain"

    @property
    def tier(self) -> int:
        return 4

    @property
    def prerequisites(self) -> list[str]:
        return ["bayes_theorem", "conditional_prob"]

    def task_description(self, difficulty: int) -> str:
        return "Bayesian update chain"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        prior = round(self._rng.uniform(0.1, 0.5), 2)
        n_updates = min(1 + difficulty, 4)
        likelihoods = [round(self._rng.uniform(0.6, 0.95), 2) for _ in range(n_updates)]
        false_pos = [round(self._rng.uniform(0.05, 0.3), 2) for _ in range(n_updates)]

        p = prior
        steps = [f"prior P(H) = {p}"]
        for i in range(n_updates):
            p_e_h = likelihoods[i]
            p_e_nh = false_pos[i]
            p_e = p * p_e_h + (1 - p) * p_e_nh
            p = round(p * p_e_h / p_e, 4)
            steps.append(f"evidence {i+1}: P(H|E) = {p}")

        return (
            f"prior={prior}, {n_updates} positive tests (sensitivity={likelihoods}, FPR={false_pos})",
            {"prior": prior, "posterior": p, "steps": steps},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        return sd["steps"]

    def _create_answer(self, sd: dict) -> str:
        return f"{sd['posterior']}"


@register
class ConditionalIndependenceGenerator(StepGenerator):
    """Check conditional independence from a joint distribution table."""

    @property
    def task_name(self) -> str:
        return "conditional_independence"

    @property
    def tier(self) -> int:
        return 4

    @property
    def prerequisites(self) -> list[str]:
        return ["conditional_prob", "independence_test"]

    def task_description(self, difficulty: int) -> str:
        return "check conditional independence"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        p_c = round(self._rng.uniform(0.3, 0.7), 2)
        p_a_c = round(self._rng.uniform(0.2, 0.8), 2)
        p_b_c = round(self._rng.uniform(0.2, 0.8), 2)

        if self._rng.random() < 0.5:
            p_ab_c = round(p_a_c * p_b_c, 4)
            indep = True
        else:
            p_ab_c = round(self._rng.uniform(0.1, 0.6), 4)
            indep = abs(p_ab_c - p_a_c * p_b_c) < 0.001

        return (
            f"P(C)={p_c}, P(A|C)={p_a_c}, P(B|C)={p_b_c}, P(A∩B|C)={p_ab_c}",
            {"p_a_c": p_a_c, "p_b_c": p_b_c, "p_ab_c": p_ab_c,
             "product": round(p_a_c * p_b_c, 4), "indep": indep},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        return [
            f"P(A|C) * P(B|C) = {sd['p_a_c']} * {sd['p_b_c']} = {sd['product']}",
            f"P(A∩B|C) = {sd['p_ab_c']}",
            f"{'equal' if sd['indep'] else 'not equal'} → {'independent' if sd['indep'] else 'dependent'}",
        ]

    def _create_answer(self, sd: dict) -> str:
        return "INDEPENDENT" if sd["indep"] else "DEPENDENT"


@register
class JointDistributionGenerator(StepGenerator):
    """Compute marginals and expectations from a joint distribution."""

    @property
    def task_name(self) -> str:
        return "joint_distribution"

    @property
    def tier(self) -> int:
        return 5

    @property
    def prerequisites(self) -> list[str]:
        return ["conditional_independence", "expected_value"]

    def task_description(self, difficulty: int) -> str:
        return "joint distribution computation"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        nx = min(2 + difficulty // 2, 4)
        ny = min(2 + difficulty // 2, 4)
        raw = [[self._rng.randint(1, 10) for _ in range(ny)] for _ in range(nx)]
        total = sum(sum(row) for row in raw)
        joint = [[round(v / total, 4) for v in row] for row in raw]

        marginal_x = [round(sum(row), 4) for row in joint]
        marginal_y = [round(sum(joint[i][j] for i in range(nx)), 4) for j in range(ny)]
        e_x = round(sum(i * marginal_x[i] for i in range(nx)), 4)

        table = "; ".join(
            "[" + ", ".join(f"{joint[i][j]}" for j in range(ny)) + "]"
            for i in range(nx)
        )
        return (
            f"P(X,Y): {table}",
            {"joint": joint, "marginal_x": marginal_x, "marginal_y": marginal_y, "e_x": e_x},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        return [
            f"P(X): {sd['marginal_x']}",
            f"P(Y): {sd['marginal_y']}",
            f"E[X] = {sd['e_x']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        return f"E[X]={sd['e_x']}"


# ═══════════════════════════════════════════════════════════════════
# DIFFERENTIAL EQUATIONS (3 generators, tiers 4-5)
# ═══════════════════════════════════════════════════════════════════

@register
class SeparationOfVariablesGenerator(StepGenerator):
    """Solve a separable ODE."""

    @property
    def task_name(self) -> str:
        return "separation_of_variables"

    @property
    def tier(self) -> int:
        return 4

    @property
    def prerequisites(self) -> list[str]:
        return ["integral", "derivative"]

    def task_description(self, difficulty: int) -> str:
        return "solve separable ODE"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        cases = [
            ("dy/dx = ky", "y = Ce^{kx}", "exponential growth"),
            ("dy/dx = -ky", "y = Ce^{-kx}", "exponential decay"),
            ("dy/dx = y/x", "y = Cx", "proportional"),
            ("dy/dx = x/y", "y^2 = x^2 + C", "implicit"),
        ]
        ode, solution, name = self._rng.choice(cases[:min(len(cases), 2 + difficulty)])
        k = self._rng.randint(1, max(1, difficulty))
        ode_sub = ode.replace("k", str(k))
        sol_sub = solution.replace("k", str(k))
        return (
            f"solve: {ode_sub}",
            {"ode": ode_sub, "solution": sol_sub, "method": "separation", "name": name},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        return [f"separate variables", f"integrate both sides", f"general solution"]

    def _create_answer(self, sd: dict) -> str:
        return sd["solution"]


@register
class IntegratingFactorGenerator(StepGenerator):
    """Solve a first-order linear ODE using an integrating factor."""

    @property
    def task_name(self) -> str:
        return "integrating_factor"

    @property
    def tier(self) -> int:
        return 5

    @property
    def prerequisites(self) -> list[str]:
        return ["separation_of_variables", "chain_rule"]

    def task_description(self, difficulty: int) -> str:
        return "solve ODE with integrating factor"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        cases = [
            ("dy/dx + y = e^x", "e^x", "y = (e^{2x}/2 + C)/e^x", "simple"),
            ("dy/dx + 2y = x", "e^{2x}", "y = (x/2 - 1/4) + Ce^{-2x}", "polynomial RHS"),
            ("dy/dx - y = 1", "e^{-x}", "y = -1 + Ce^x", "constant RHS"),
        ]
        ode, mu, solution, name = self._rng.choice(cases[:min(len(cases), 1 + difficulty)])
        return (
            f"solve: {ode}",
            {"ode": ode, "mu": mu, "solution": solution, "name": name},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        return [
            f"identify P(x) from dy/dx + P(x)*y = Q(x)",
            f"integrating factor mu = {sd['mu']}",
            f"multiply through and integrate",
        ]

    def _create_answer(self, sd: dict) -> str:
        return sd["solution"]


@register
class CharacteristicEquationGenerator(StepGenerator):
    """Solve a second-order constant-coefficient ODE."""

    @property
    def task_name(self) -> str:
        return "characteristic_equation"

    @property
    def tier(self) -> int:
        return 5

    @property
    def prerequisites(self) -> list[str]:
        return ["quadratic", "separation_of_variables"]

    def task_description(self, difficulty: int) -> str:
        return "solve via characteristic equation"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        root_type = self._rng.choice(["distinct", "repeated", "complex"])
        if root_type == "distinct":
            r1 = self._rng.randint(-3, 3)
            r2 = r1 + self._rng.randint(1, 3)
            a, b, c = 1, -(r1 + r2), r1 * r2
            solution = f"y = C1*e^{{{r1}x}} + C2*e^{{{r2}x}}"
        elif root_type == "repeated":
            r = self._rng.randint(-3, 3)
            a, b, c = 1, -2 * r, r * r
            solution = f"y = (C1 + C2*x)*e^{{{r}x}}"
        else:
            alpha = self._rng.randint(-2, 2)
            beta = self._rng.randint(1, 3)
            a, b, c = 1, -2 * alpha, alpha * alpha + beta * beta
            solution = f"y = e^{{{alpha}x}}(C1*cos({beta}x) + C2*sin({beta}x))"

        ode = f"{a}y'' + {b}y' + {c}y = 0"
        char_eq = f"{a}r^2 + {b}r + {c} = 0"
        return ode, {"ode": ode, "char_eq": char_eq, "root_type": root_type, "solution": solution}

    def _create_steps(self, sd: dict) -> list[str]:
        return [
            f"characteristic: {sd['char_eq']}",
            f"roots: {sd['root_type']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        return sd["solution"]


# ═══════════════════════════════════════════════════════════════════
# ABSTRACT ALGEBRA (3 generators, tiers 4-6)
# ═══════════════════════════════════════════════════════════════════

@register
class GroupTableGenerator(StepGenerator):
    """Compute a Cayley table for Z_n under addition mod n."""

    @property
    def task_name(self) -> str:
        return "group_table"

    @property
    def tier(self) -> int:
        return 4

    @property
    def prerequisites(self) -> list[str]:
        return ["modular"]

    def task_description(self, difficulty: int) -> str:
        return "compute group operation table"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        n = min(3 + difficulty, 8)
        a = self._rng.randint(0, n - 1)
        b = self._rng.randint(0, n - 1)
        result = (a + b) % n
        inverse_a = (n - a) % n
        return (
            f"Z_{n}: compute {a} + {b}, and find inverse of {a}",
            {"n": n, "a": a, "b": b, "sum": result, "inv_a": inverse_a},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        return [
            f"{sd['a']} + {sd['b']} mod {sd['n']} = {sd['sum']}",
            f"inverse of {sd['a']}: {sd['n']} - {sd['a']} = {sd['inv_a']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        return f"sum={sd['sum']}, inv={sd['inv_a']}"


@register
class RingArithmeticGenerator(StepGenerator):
    """Perform arithmetic in Z_n (addition and multiplication mod n)."""

    @property
    def task_name(self) -> str:
        return "ring_arithmetic"

    @property
    def tier(self) -> int:
        return 5

    @property
    def prerequisites(self) -> list[str]:
        return ["group_table", "mod_inv"]

    def task_description(self, difficulty: int) -> str:
        return "ring arithmetic in Z_n"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        n = self._rng.choice([5, 6, 7, 8, 10, 11, 12])
        a = self._rng.randint(1, n - 1)
        b = self._rng.randint(1, n - 1)
        add = (a + b) % n
        mul = (a * b) % n
        return (
            f"Z_{n}: {a} + {b} and {a} * {b}",
            {"n": n, "a": a, "b": b, "add": add, "mul": mul},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        return [
            f"{sd['a']} + {sd['b']} = {sd['a'] + sd['b']} mod {sd['n']} = {sd['add']}",
            f"{sd['a']} * {sd['b']} = {sd['a'] * sd['b']} mod {sd['n']} = {sd['mul']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        return f"add={sd['add']}, mul={sd['mul']}"


@register
class GroupHomomorphismGenerator(StepGenerator):
    """Check if a map between groups is a homomorphism."""

    @property
    def task_name(self) -> str:
        return "group_homomorphism"

    @property
    def tier(self) -> int:
        return 6

    @property
    def prerequisites(self) -> list[str]:
        return ["group_table", "group_order"]

    def task_description(self, difficulty: int) -> str:
        return "verify group homomorphism"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        n = self._rng.choice([4, 6, 8])
        m = self._rng.choice([2, 3, 4])
        k = n // m if n % m == 0 else 1

        is_homo = (n % m == 0) and self._rng.random() < 0.6
        if is_homo:
            f_desc = f"f(x) = x mod {m}"
            test_a = self._rng.randint(0, n - 1)
            test_b = self._rng.randint(0, n - 1)
            f_apb = (test_a + test_b) % n % m
            fa_fb = ((test_a % m) + (test_b % m)) % m
            valid = f_apb == fa_fb
        else:
            f_desc = f"f(x) = x + 1 mod {m}"
            test_a = self._rng.randint(0, n - 1)
            test_b = self._rng.randint(0, n - 1)
            f_apb = ((test_a + test_b) % n + 1) % m
            fa_fb = (((test_a + 1) % m) + ((test_b + 1) % m)) % m
            valid = f_apb == fa_fb

        return (
            f"f: Z_{n} -> Z_{m}, {f_desc}. Is it a homomorphism?",
            {"n": n, "m": m, "f_desc": f_desc, "test_a": test_a, "test_b": test_b,
             "f_apb": f_apb, "fa_fb": fa_fb, "valid": valid},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        return [
            f"test: f({sd['test_a']} + {sd['test_b']}) = {sd['f_apb']}",
            f"f({sd['test_a']}) + f({sd['test_b']}) = {sd['fa_fb']}",
            f"{'equal' if sd['valid'] else 'not equal'}",
        ]

    def _create_answer(self, sd: dict) -> str:
        return "YES" if sd["valid"] else "NO"


# ═══════════════════════════════════════════════════════════════════
# FORMAL PROOFS (4 generators, tiers 3-5)
# ═══════════════════════════════════════════════════════════════════

@register
class DirectProofGenerator(StepGenerator):
    """Construct a direct proof for a simple statement."""

    @property
    def task_name(self) -> str:
        return "direct_proof"

    @property
    def tier(self) -> int:
        return 3

    @property
    def prerequisites(self) -> list[str]:
        return ["deduction_chain", "implication"]

    def task_description(self, difficulty: int) -> str:
        return "construct direct proof"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        proofs = [
            {
                "claim": "if n is even, n^2 is even",
                "steps": ["assume n = 2k", "n^2 = (2k)^2 = 4k^2 = 2(2k^2)", "2k^2 is integer, so n^2 is even"],
            },
            {
                "claim": "sum of two even numbers is even",
                "steps": ["let a = 2m, b = 2n", "a + b = 2m + 2n = 2(m+n)", "m+n is integer, so sum is even"],
            },
            {
                "claim": "product of two odd numbers is odd",
                "steps": ["let a = 2m+1, b = 2n+1", "ab = 4mn + 2m + 2n + 1 = 2(2mn+m+n) + 1", "this is odd"],
            },
            {
                "claim": "if n^2 is odd, n is odd",
                "steps": ["contrapositive: if n is even, n^2 is even", "n = 2k implies n^2 = 4k^2 = 2(2k^2)", "done by contrapositive"],
            },
        ]
        proof = self._rng.choice(proofs[:min(len(proofs), 2 + difficulty)])
        return f"prove: {proof['claim']}", proof

    def _create_steps(self, sd: dict) -> list[str]:
        return sd["steps"]

    def _create_answer(self, sd: dict) -> str:
        return "QED"


@register
class ProofByContradictionGenerator(StepGenerator):
    """Identify the contradiction in a proof by contradiction."""

    @property
    def task_name(self) -> str:
        return "proof_by_contradiction"

    @property
    def tier(self) -> int:
        return 4

    @property
    def prerequisites(self) -> list[str]:
        return ["direct_proof", "negation"]

    def task_description(self, difficulty: int) -> str:
        return "proof by contradiction"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        proofs = [
            {
                "claim": "sqrt(2) is irrational",
                "assumption": "assume sqrt(2) = a/b in lowest terms",
                "steps": ["2b^2 = a^2, so a is even", "let a = 2k, then 2b^2 = 4k^2, so b is even"],
                "contradiction": "both a and b are even, contradicting 'lowest terms'",
            },
            {
                "claim": "there are infinitely many primes",
                "assumption": "assume finitely many primes: p1, p2, ..., pn",
                "steps": ["let N = p1*p2*...*pn + 1", "N is not divisible by any pi"],
                "contradiction": "N is either prime or has a prime factor not in the list",
            },
            {
                "claim": "there is no largest integer",
                "assumption": "assume M is the largest integer",
                "steps": ["consider M + 1", "M + 1 > M"],
                "contradiction": "M + 1 is larger than M, contradicting 'M is largest'",
            },
        ]
        proof = self._rng.choice(proofs[:min(len(proofs), 1 + difficulty)])
        return f"prove: {proof['claim']}", proof

    def _create_steps(self, sd: dict) -> list[str]:
        return [sd["assumption"]] + sd["steps"] + [sd["contradiction"]]

    def _create_answer(self, sd: dict) -> str:
        return sd["contradiction"]


@register
class ProofByCasesGenerator(StepGenerator):
    """Prove a statement by exhaustive case analysis."""

    @property
    def task_name(self) -> str:
        return "proof_by_cases"

    @property
    def tier(self) -> int:
        return 4

    @property
    def prerequisites(self) -> list[str]:
        return ["direct_proof"]

    def task_description(self, difficulty: int) -> str:
        return "proof by cases"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        proofs = [
            {
                "claim": "|n| >= 0 for all integers n",
                "cases": [
                    ("n >= 0", "|n| = n >= 0"),
                    ("n < 0", "|n| = -n > 0 >= 0"),
                ],
            },
            {
                "claim": "n^2 - n is even for all integers n",
                "cases": [
                    ("n even: n = 2k", "n^2 - n = 4k^2 - 2k = 2(2k^2 - k), even"),
                    ("n odd: n = 2k+1", "n^2 - n = (2k+1)^2 - (2k+1) = 4k^2+2k = 2(2k^2+k), even"),
                ],
            },
            {
                "claim": "max(a,b) + min(a,b) = a + b",
                "cases": [
                    ("a >= b", "max=a, min=b, a+b=a+b"),
                    ("a < b", "max=b, min=a, b+a=a+b"),
                ],
            },
        ]
        proof = self._rng.choice(proofs[:min(len(proofs), 1 + difficulty)])
        return f"prove: {proof['claim']}", proof

    def _create_steps(self, sd: dict) -> list[str]:
        steps = []
        for condition, result in sd["cases"]:
            steps.append(f"case {condition}: {result}")
        steps.append("all cases covered")
        return steps

    def _create_answer(self, sd: dict) -> str:
        return "QED"


@register
class StrongInductionGenerator(StepGenerator):
    """Apply strong induction to prove a statement."""

    @property
    def task_name(self) -> str:
        return "strong_induction"

    @property
    def tier(self) -> int:
        return 5

    @property
    def prerequisites(self) -> list[str]:
        return ["proof_by_induction"]

    def task_description(self, difficulty: int) -> str:
        return "proof by strong induction"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        proofs = [
            {
                "claim": "every integer >= 2 has a prime factorisation",
                "base": "2 is prime, so 2 = 2 (trivial factorisation)",
                "inductive": "assume all integers 2..n-1 have prime factorisations",
                "step": "if n is prime, done. If n = ab where 2 <= a,b < n, by hypothesis a and b have factorisations, so n does too.",
            },
            {
                "claim": "every amount >= 8 cents can be made with 3c and 5c stamps",
                "base": "8=3+5, 9=3+3+3, 10=5+5",
                "inductive": "assume all amounts 8..n-1 can be made",
                "step": "for n >= 11: n-3 >= 8, so n-3 can be made, add one 3c stamp.",
            },
        ]
        proof = self._rng.choice(proofs[:min(len(proofs), 1 + difficulty)])
        return f"prove by strong induction: {proof['claim']}", proof

    def _create_steps(self, sd: dict) -> list[str]:
        return [f"base: {sd['base']}", f"hypothesis: {sd['inductive']}", f"step: {sd['step']}"]

    def _create_answer(self, sd: dict) -> str:
        return "QED"
