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
        """Return the unique task identifier."""
        return "bayes_chain"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["bayes_theorem", "conditional_prob"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description."""
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
        """Return the unique task identifier."""
        return "conditional_independence"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["conditional_prob", "independence_test"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description."""
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
        """Return the unique task identifier."""
        return "joint_distribution"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["conditional_independence", "expected_value"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description."""
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
        """Return the unique task identifier."""
        return "separation_of_variables"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["integral", "derivative"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description."""
        return "solve separable ODE"

    def _build_templates(self, a: int, b: int, n: int) -> list[tuple[str, str, str]]:
        """Build all separable ODE templates from randomised coefficients.

        Args:
            a: Primary coefficient.
            b: Secondary coefficient.
            n: Exponent choice (2 or 3).

        Returns:
            List of (ode, solution, name) tuples.
        """
        return [
            (f"dy/dx = {a}y", f"y = Ce^{{{a}x}}", "exponential growth"),
            (f"dy/dx = -{a}y", f"y = Ce^{{-{a}x}}", "exponential decay"),
            (f"dy/dx = {a}y/x", f"y = Cx^{{{a}}}", "power law"),
            (f"dy/dx = {a}x/y", f"y^2 = {a}x^2 + C", "implicit quadratic"),
            (f"dy/dx = {a}x^{n}", f"y = {a}x^{{{n + 1}}}/{n + 1} + C", "polynomial"),
            (f"dy/dx = {a}y^2", f"y = -1/({a}x + C)", "reciprocal"),
            (f"dy/dx = {a}*sqrt(y)", f"2*sqrt(y) = {a}x + C", "square root"),
            (f"dy/dx = {a}e^{{-{b}x}}", f"y = -{a}/{b}*e^{{-{b}x}} + C", "exponential RHS"),
            (f"dy/dx = {a}/(1 + x^2)", f"y = {a}*arctan(x) + C", "arctangent"),
            (f"dy/dx = {a}*y*x", f"y = Ce^{{{a}x^2/2}}", "Gaussian growth"),
        ]

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a separable ODE with randomised coefficients.

        Args:
            difficulty: Controls ODE form variety and coefficient range.

        Returns:
            Tuple of (ode_string, solution_data).
        """
        a = self._rng.randint(1, max(1, difficulty + 2))
        b = self._rng.randint(1, max(1, difficulty + 1))
        n = self._rng.choice([2, 3])
        cases = self._build_templates(a, b, n)
        ode, solution, name = self._rng.choice(
            cases[:min(len(cases), 3 + difficulty)]
        )
        return (
            f"solve: {ode}",
            {"ode": ode, "solution": solution,
             "method": "separation", "name": name},
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
        """Return the unique task identifier."""
        return "integrating_factor"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["separation_of_variables", "chain_rule"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description."""
        return "solve ODE with integrating factor"

    def _build_templates(self, a: int, b: int) -> list[dict]:
        """Build all integrating factor ODE templates from coefficients.

        Args:
            a: Primary coefficient for P(x).
            b: Secondary coefficient for Q(x).

        Returns:
            List of dicts with keys ode, mu, solution, name.
        """
        return [
            {"ode": f"dy/dx + {a}y = e^{{{b}x}}", "mu": f"e^{{{a}x}}",
             "solution": (f"y = (e^{{{a + b}x}}/{a + b} + C)/e^{{{a}x}}"
                          if a + b != 0 else f"y = (x + C)/e^{{{a}x}}"),
             "name": "exponential RHS"},
            {"ode": f"dy/dx - {a}y = {b}", "mu": f"e^{{-{a}x}}",
             "solution": f"y = -{b}/{a} + Ce^{{{a}x}}", "name": "constant RHS"},
            {"ode": f"dy/dx + {a}y = {b}x", "mu": f"e^{{{a}x}}",
             "solution": f"y = ({b}x/{a} - {b}/{a**2}) + Ce^{{-{a}x}}",
             "name": "polynomial RHS"},
            {"ode": f"dy/dx + {a}y = {b}*sin(x)", "mu": f"e^{{{a}x}}",
             "solution": (f"y = {b}*({a}*sin(x) - cos(x))/({a**2}+1) "
                          f"+ Ce^{{-{a}x}}"),
             "name": "trig RHS"},
            {"ode": f"dy/dx + ({a}/x)y = {b}*x^2", "mu": f"x^{{{a}}}",
             "solution": f"y = {b}*x^3/({a}+3) + C/x^{{{a}}}",
             "name": "variable coeff"},
            {"ode": f"dy/dx - {a}y = e^{{{a}x}}", "mu": f"e^{{-{a}x}}",
             "solution": f"y = x*e^{{{a}x}} + Ce^{{{a}x}}",
             "name": "resonance"},
            {"ode": f"dy/dx + {a}y = {b}*e^{{-{a}x}}", "mu": f"e^{{{a}x}}",
             "solution": f"y = {b}*x*e^{{-{a}x}} + Ce^{{-{a}x}}",
             "name": "matching exponential"},
            {"ode": f"dy/dx + {a}y = {b}*x^2", "mu": f"e^{{{a}x}}",
             "solution": (f"y = {b}*(x^2/{a} - 2x/{a**2} + 2/{a**3}) "
                          f"+ Ce^{{-{a}x}}"),
             "name": "quadratic RHS"},
        ]

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an integrating factor ODE with randomised coefficients.

        Args:
            difficulty: Controls variety of ODE forms.

        Returns:
            Tuple of (ode_string, solution_data).
        """
        a = self._rng.randint(1, 6)
        b = self._rng.randint(1, 6)
        templates = self._build_templates(a, b)
        case = self._rng.choice(templates[:min(len(templates), 2 + difficulty)])
        return (
            f"solve: {case['ode']}",
            {"ode": case["ode"], "mu": case["mu"],
             "solution": case["solution"], "name": case["name"]},
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
        """Return the unique task identifier."""
        return "characteristic_equation"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["quadratic", "separation_of_variables"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description."""
        return "solve via characteristic equation"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a characteristic equation ODE with randomised roots.

        Args:
            difficulty: Controls coefficient ranges.

        Returns:
            Tuple of (ode_string, solution_data).
        """
        root_type = self._rng.choice(["distinct", "repeated", "complex"])
        max_coeff = min(3 + difficulty, 8)
        if root_type == "distinct":
            r1 = self._rng.randint(-max_coeff, max_coeff)
            offset = self._rng.randint(1, max(1, max_coeff))
            r2 = r1 + offset
            a, b, c = 1, -(r1 + r2), r1 * r2
            solution = f"y = C1*e^{{{r1}x}} + C2*e^{{{r2}x}}"
        elif root_type == "repeated":
            r = self._rng.randint(-max_coeff, max_coeff)
            a, b, c = 1, -2 * r, r * r
            solution = f"y = (C1 + C2*x)*e^{{{r}x}}"
        else:
            alpha = self._rng.randint(-max_coeff, max_coeff)
            beta = self._rng.randint(1, max(1, max_coeff))
            a, b, c = 1, -2 * alpha, alpha * alpha + beta * beta
            solution = f"y = e^{{{alpha}x}}(C1*cos({beta}x) + C2*sin({beta}x))"

        ode = f"{a}y'' + {b}y' + {c}y = 0"
        char_eq = f"{a}r^2 + {b}r + {c} = 0"
        return ode, {"ode": ode, "char_eq": char_eq,
                     "root_type": root_type, "solution": solution}

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
        """Return the unique task identifier."""
        return "group_table"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["modular"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description."""
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
        """Return the unique task identifier."""
        return "ring_arithmetic"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["group_table", "mod_inv"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description."""
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
        """Return the unique task identifier."""
        return "group_homomorphism"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["group_table", "group_order"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description."""
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
        """Return the unique task identifier."""
        return "direct_proof"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 3

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["deduction_chain", "implication"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description."""
        return "construct direct proof"

    def _select_variables(self) -> tuple[str, str, str]:
        """Choose three distinct variable names for proof templates.

        Returns:
            Tuple of (primary_var, secondary_var, tertiary_var).
        """
        var = self._rng.choice(["n", "m", "k", "x", "j"])
        v2 = self._rng.choice(["a", "b", "p", "q", "u", "v"])
        v3 = self._rng.choice(["c", "d", "r", "s", "w", "t"])
        while v3 == v2:
            v3 = self._rng.choice(["c", "d", "r", "s", "w", "t"])
        return var, v2, v3

    def _parity_templates(self, var: str, v2: str, v3: str,
                          exp: int) -> list[dict]:
        """Build parity-based direct proof templates.

        Args:
            var: Primary variable name.
            v2: Secondary variable name.
            v3: Tertiary variable name.
            exp: Exponent (2 or 3).

        Returns:
            List of dicts with keys claim and steps.
        """
        return [
            {"claim": f"if {var} is even, {var}^{exp} is even",
             "steps": [f"assume {var} = 2k",
                       f"{var}^{exp} = (2k)^{exp} = {2**exp}*k^{exp} = 2*({2**(exp-1)}*k^{exp})",
                       f"{2**(exp-1)}*k^{exp} is integer, so {var}^{exp} is even"]},
            {"claim": f"sum of two even numbers is even",
             "steps": [f"let {v2} = 2m, {v3} = 2n",
                       f"{v2} + {v3} = 2m + 2n = 2(m+n)",
                       f"m+n is integer, so sum is even"]},
            {"claim": f"product of two odd numbers is odd",
             "steps": [f"let {v2} = 2m+1, {v3} = 2n+1",
                       f"{v2}*{v3} = 4mn + 2m + 2n + 1 = 2(2mn+m+n) + 1",
                       f"this is odd"]},
            {"claim": f"if {var}^{exp} is odd, {var} is odd",
             "steps": [f"contrapositive: if {var} is even, {var}^{exp} is even",
                       f"{var} = 2k implies {var}^{exp} = {2**exp}*k^{exp} = 2*({2**(exp-1)}*k^{exp})",
                       f"done by contrapositive"]},
        ]

    def _arithmetic_templates(self, var: str, v2: str, v3: str,
                              c: int) -> list[dict]:
        """Build arithmetic-based direct proof templates.

        Args:
            var: Primary variable name.
            v2: Secondary variable name.
            v3: Tertiary variable name.
            c: Small integer constant.

        Returns:
            List of dicts with keys claim and steps.
        """
        return [
            {"claim": f"if {var} is divisible by {c}, then {var}^2 is divisible by {c**2}",
             "steps": [f"assume {var} = {c}*k",
                       f"{var}^2 = ({c}*k)^2 = {c**2}*k^2",
                       f"so {var}^2 is divisible by {c**2}"]},
            {"claim": (f"sum of {c} consecutive integers starting at {var} "
                       f"is divisible by {c} when {c} is odd"),
             "steps": [f"sum = {c}*{var} + (0+1+...+{c - 1}) = {c}*{var} + {c * (c - 1) // 2}",
                       f"= {c}*({var} + {(c - 1) // 2})",
                       f"divisible by {c}"]},
            {"claim": f"for any integer {var}, {c}*{var} + {c + 1} is odd iff {var} is even",
             "steps": [f"if {var} even: {var}=2k, {c}*2k + {c + 1} = {2 * c}k + {c + 1}",
                       (f"{2 * c}k is even, {c + 1} is {'even' if (c + 1) % 2 == 0 else 'odd'}, "
                        f"sum is {'even' if (c + 1) % 2 == 0 else 'odd'}"),
                       f"verified for even case"]},
            {"claim": (f"the square of any integer {var} "
                       f"leaves remainder 0 or 1 when divided by 4"),
             "steps": [f"if {var} is even: {var}=2k, {var}^2=4k^2, remainder 0",
                       f"if {var} is odd: {var}=2k+1, {var}^2=4k^2+4k+1=4(k^2+k)+1, remainder 1",
                       f"only remainders 0 and 1 are possible"]},
            {"claim": f"({v2}+{v3})^2 = {v2}^2 + 2*{v2}*{v3} + {v3}^2",
             "steps": [f"({v2}+{v3})^2 = ({v2}+{v3})*({v2}+{v3})",
                       f"= {v2}^2 + {v2}*{v3} + {v3}*{v2} + {v3}^2",
                       f"= {v2}^2 + 2*{v2}*{v3} + {v3}^2"]},
        ]

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a direct proof with randomised variables and constants.

        Args:
            difficulty: Controls which proof templates are accessible.

        Returns:
            Tuple of (claim_string, proof_data).
        """
        var, v2, v3 = self._select_variables()
        exp = self._rng.choice([2, 3])
        c = self._rng.randint(2, 7)
        proofs = (self._parity_templates(var, v2, v3, exp)
                  + self._arithmetic_templates(var, v2, v3, c))
        proof = self._rng.choice(proofs[:min(len(proofs), 3 + difficulty)])
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
        """Return the unique task identifier."""
        return "proof_by_contradiction"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["direct_proof", "negation"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description."""
        return "proof by contradiction"

    def _random_params(self) -> dict:
        """Generate randomised parameters for contradiction templates.

        Returns:
            Dict with keys p, n_val, k_val, m_val, exp, var.
        """
        return {
            "p": self._rng.choice([2, 3, 5, 7, 11, 13, 17, 19, 23]),
            "n_val": self._rng.randint(3, 30),
            "k_val": self._rng.randint(2, 12),
            "m_val": self._rng.randint(2, 15),
            "exp": self._rng.choice([2, 3, 4]),
            "var": self._rng.choice(["a", "b", "c", "m", "n", "x", "y"]),
        }

    def _irrationality_templates(self, pm: dict) -> list[dict]:
        """Build irrationality and divisibility contradiction templates.

        Args:
            pm: Parameter dict from _random_params().

        Returns:
            List of dicts with keys claim, assumption, steps, contradiction.
        """
        p, k, m = pm["p"], pm["k_val"], pm["m_val"]
        exp, v = pm["exp"], pm["var"]
        return [
            {"claim": f"sqrt({p}) is irrational",
             "assumption": f"assume sqrt({p}) = {v}/b in lowest terms",
             "steps": [f"{p}*b^2 = {v}^2, so {p} divides {v}",
                       f"let {v} = {p}*k, then {p}*b^2 = {p}^2*k^2, so {p} divides b"],
             "contradiction": (f"both {v} and b are divisible by {p}, "
                               f"contradicting 'lowest terms'")},
            {"claim": f"there is no largest multiple of {k}",
             "assumption": f"assume M = {k}*{m} is the largest multiple of {k}",
             "steps": [f"consider M + {k} = {k}*{m} + {k} = {k}*{m + 1}",
                       f"M + {k} > M and is a multiple of {k}"],
             "contradiction": (f"M + {k} = {k * (m + 1)} is a larger multiple "
                               f"of {k}, contradicting 'M is largest'")},
            {"claim": f"log_{p}({p ** exp + 1}) is irrational",
             "assumption": f"assume log_{p}({p ** exp + 1}) = {v}/b for integers {v},b",
             "steps": [f"{p}^({v}/b) = {p ** exp + 1}",
                       f"{p}^{v} = {p ** exp + 1}^b, but {p}^{v} is a power of {p}"],
             "contradiction": f"{p ** exp + 1}^b is not a power of {p}, contradiction"},
            {"claim": (f"if {v}^{exp} is divisible by {p} then {v} "
                       f"is divisible by {p}"),
             "assumption": f"assume {v}^{exp} is divisible by {p} but {v} is not",
             "steps": [f"since {p} is prime, {p} | {v}^{exp} implies {p} | {v}",
                       f"by Euclid's lemma on prime factorisation"],
             "contradiction": f"we assumed {v} is not divisible by {p}, contradiction"},
            {"claim": f"{k}*irrational is irrational",
             "assumption": (f"assume {k}*x = {v}/b where x is irrational, "
                            f"{v}/b is rational"),
             "steps": [f"x = {v}/({k}*b)", f"ratio of integers is rational"],
             "contradiction": (f"x = {v}/({k}*b) is rational, contradicting "
                               f"x being irrational")},
        ]

    def _counting_templates(self, pm: dict) -> list[dict]:
        """Build counting and pigeonhole contradiction templates.

        Args:
            pm: Parameter dict from _random_params().

        Returns:
            List of dicts with keys claim, assumption, steps, contradiction.
        """
        p, n, k, m = pm["p"], pm["n_val"], pm["k_val"], pm["m_val"]
        v = pm["var"]
        return [
            {"claim": (f"in a set of {n} integers, not all can have "
                       f"distinct remainders mod {n - 1}"),
             "assumption": (f"assume all {n} integers have distinct "
                            f"remainders mod {n - 1}"),
             "steps": [f"there are only {n - 1} possible remainders: 0..{n - 2}",
                       f"but we have {n} integers"],
             "contradiction": "by pigeonhole, two must share a remainder, contradiction"},
            {"claim": f"there is no smallest positive rational greater than 1/{m}",
             "assumption": f"assume r > 1/{m} is the smallest such rational",
             "steps": [f"consider (r + 1/{m})/2", f"1/{m} < (r + 1/{m})/2 < r"],
             "contradiction": (f"(r + 1/{m})/2 is a smaller rational above 1/{m}, "
                               f"contradiction")},
            {"claim": (f"in a group of {n} people, not everyone can have "
                       f"a different number of friends (within the group)"),
             "assumption": f"assume all {n} people have different friend counts",
             "steps": [f"friend counts range 0..{n - 1}",
                       f"if someone has 0 friends, no one can have {n - 1}"],
             "contradiction": f"cannot use both 0 and {n - 1}, pigeonhole violation"},
            {"claim": (f"there is no integer {v} such that "
                       f"{v}^2 - {v} = {p * k + 1}"),
             "assumption": f"assume {v}^2 - {v} = {p * k + 1}",
             "steps": [f"{v}({v}-1) = {p * k + 1}",
                       (f"consecutive integers {v} and {v}-1 multiply to "
                        f"{p * k + 1}")],
             "contradiction": (f"product of consecutive integers is even, but "
                               f"{p * k + 1} is odd, contradiction")},
            {"claim": (f"no integer {v} satisfies "
                       f"{v} mod {k} = 0 and {v} mod {k} = {k - 1} "
                       f"simultaneously"),
             "assumption": (f"assume {v} mod {k} = 0 and "
                            f"{v} mod {k} = {k - 1}"),
             "steps": [f"from first: {v} = {k}*q for some integer q",
                       f"from second: {v} = {k}*q' + {k - 1}"],
             "contradiction": (f"0 != {k - 1}, so {v} cannot have two distinct "
                               f"remainders mod {k}")},
        ]

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a proof by contradiction with randomised parameters.

        Args:
            difficulty: Controls which proof templates are accessible.

        Returns:
            Tuple of (claim_string, proof_data).
        """
        pm = self._random_params()
        proofs = self._irrationality_templates(pm) + self._counting_templates(pm)
        proof = self._rng.choice(proofs[:min(len(proofs), 3 + difficulty)])
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
        """Return the unique task identifier."""
        return "proof_by_cases"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["direct_proof"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description."""
        return "proof by cases"

    def _build_templates(self, var: str, d: int, exp: int,
                         c: int) -> list[dict]:
        """Build all proof-by-cases templates from randomised parameters.

        Args:
            var: Variable name used in claims.
            d: Divisor for modular residue cases.
            exp: Exponent (2 or 3).
            c: Small integer constant.

        Returns:
            List of dicts with keys claim and cases.
        """
        return [
            {"claim": f"|{var}| >= 0 for all integers {var}",
             "cases": [(f"{var} >= 0", f"|{var}| = {var} >= 0"),
                       (f"{var} < 0", f"|{var}| = -{var} > 0 >= 0")]},
            {"claim": f"{var}^2 - {var} is even for all integers {var}",
             "cases": [(f"{var} even: {var} = 2k",
                        f"{var}^2 - {var} = 4k^2 - 2k = 2(2k^2 - k), even"),
                       (f"{var} odd: {var} = 2k+1",
                        f"{var}^2 - {var} = (2k+1)^2 - (2k+1) = 4k^2+2k = 2(2k^2+k), even")]},
            {"claim": f"max(a,b) + min(a,b) = a + b",
             "cases": [("a >= b", "max=a, min=b, a+b=a+b"),
                       ("a < b", "max=b, min=a, b+a=a+b")]},
            {"claim": f"{var}^{exp} mod {d} has at most {d} distinct residues",
             "cases": [(f"{var} mod {d} = {r}", f"{var}^{exp} mod {d} = {r**exp % d}")
                       for r in range(d)]},
            {"claim": f"|{var} * {c}| = |{var}| * {c} for all integers {var}",
             "cases": [(f"{var} >= 0", f"|{var}*{c}| = {var}*{c} = |{var}|*{c}"),
                       (f"{var} < 0", f"|{var}*{c}| = -{var}*{c} = |{var}|*{c}")]},
            {"claim": f"for all integers {var}, {var}^2 + {var} is even",
             "cases": [(f"{var} even: {var} = 2k",
                        f"{var}^2 + {var} = 4k^2 + 2k = 2(2k^2 + k), even"),
                       (f"{var} odd: {var} = 2k+1",
                        f"{var}^2 + {var} = 4k^2 + 4k + 2 = 2(2k^2 + 2k + 1), even")]},
            {"claim": (f"{var}({var}+1)({var}+2) is divisible "
                       f"by 6 for all integers {var}"),
             "cases": [(f"{var} mod 3 = 0", f"{var} divisible by 3, product divisible by 6"),
                       (f"{var} mod 3 = 1", f"{var}+2 divisible by 3, product divisible by 6"),
                       (f"{var} mod 3 = 2", f"{var}+1 divisible by 3, product divisible by 6")]},
            {"claim": f"floor({var}/{d}) + ceil({var}/{d}) >= 2*{var}/{d} for integer {var}",
             "cases": [(f"{var} mod {d} = 0",
                        f"floor = ceil = {var}/{d}, sum = 2*{var}/{d}"),
                       (f"{var} mod {d} != 0",
                        f"ceil > {var}/{d} > floor, sum > 2*floor >= 2*{var}/{d} - 1")]},
        ]

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a proof by cases with randomised parameters.

        Args:
            difficulty: Controls which proof templates are accessible.

        Returns:
            Tuple of (claim_string, proof_data).
        """
        var = self._rng.choice(["n", "m", "k", "x", "j"])
        d = self._rng.choice([2, 3, 5])
        exp = self._rng.choice([2, 3])
        c = self._rng.randint(2, 10)
        proofs = self._build_templates(var, d, exp, c)
        proof = self._rng.choice(proofs[:min(len(proofs), 2 + difficulty)])
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
        """Return the unique task identifier."""
        return "strong_induction"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["proof_by_induction"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description."""
        return "proof by strong induction"

    def _random_params(self) -> dict:
        """Generate randomised parameters for strong induction templates.

        Returns:
            Dict with keys stamp_a, stamp_b, min_amount, fib_start_a,
            fib_start_b, exp_base, bound, divisor.
        """
        stamp_a = self._rng.choice([3, 5, 7])
        stamp_b = stamp_a + self._rng.choice([2, 4])
        fib_a = self._rng.randint(1, 5)
        return {
            "stamp_a": stamp_a, "stamp_b": stamp_b,
            "min_amount": stamp_a + stamp_b,
            "fib_a": fib_a, "fib_b": fib_a + self._rng.randint(1, 5),
            "exp_base": self._rng.choice([2, 3, 5]),
            "bound": self._rng.choice([3, 4, 5, 6]),
            "divisor": self._rng.choice([2, 3, 6]),
        }

    def _number_theory_templates(self, pm: dict) -> list[dict]:
        """Build number theory strong induction templates.

        Args:
            pm: Parameter dict from _random_params().

        Returns:
            List of dicts with keys claim, base, inductive, step.
        """
        sa, sb, mi = pm["stamp_a"], pm["stamp_b"], pm["min_amount"]
        fa, fb = pm["fib_a"], pm["fib_b"]
        eb = pm["exp_base"]
        bd, dv = pm["bound"], pm["divisor"]
        return [
            {"claim": "every integer >= 2 has a prime factorisation",
             "base": "2 is prime, so 2 = 2 (trivial factorisation)",
             "inductive": "assume all integers 2..n-1 have prime factorisations",
             "step": ("if n is prime, done. If n = ab where 2 <= a,b < n, "
                      "by hypothesis a and b have factorisations, so n does too.")},
            {"claim": (f"every amount >= {mi} cents can be made "
                       f"with {sa}c and {sb}c stamps"),
             "base": f"{mi}={sa}+{sb}, {mi+1} verified, {mi+2} verified",
             "inductive": f"assume all amounts {mi}..n-1 can be made",
             "step": (f"for n >= {mi + sa}: n-{sa} >= {mi}, so n-{sa} "
                      f"can be made, add one {sa}c stamp.")},
            {"claim": (f"F(n) < {eb}^n for all n >= 1 "
                       f"(Fibonacci with F(1)={fa}, F(2)={fb})"),
             "base": (f"F(1)={fa} < {eb}^1={eb}, "
                      f"F(2)={fb} < {eb}^2={eb**2}"),
             "inductive": f"assume F(k) < {eb}^k for all k < n",
             "step": (f"F(n) = F(n-1) + F(n-2) < {eb}^(n-1) + "
                      f"{eb}^(n-2) = {eb}^(n-2)*({eb}+1) <= {eb}^n")},
            {"claim": (f"every integer >= {bd} can be written as "
                       f"sum of {dv}s and {dv + 1}s"),
             "base": (f"{bd}={dv}*{bd // dv} + "
                      f"{bd % dv}*({dv + 1}) verified for "
                      f"{bd}..{bd + dv}"),
             "inductive": f"assume all integers {bd}..n-1 decompose",
             "step": (f"for n >= {bd + dv}: n-{dv} >= {bd}, "
                      f"by hypothesis n-{dv} decomposes, add one {dv}.")},
        ]

    def _structural_templates(self, pm: dict) -> list[dict]:
        """Build structural and combinatorial strong induction templates.

        Args:
            pm: Parameter dict from _random_params().

        Returns:
            List of dicts with keys claim, base, inductive, step.
        """
        eb, dv = pm["exp_base"], pm["divisor"]
        return [
            {"claim": "every n >= 2 can be expressed as product of at most n primes",
             "base": "2 = 2 (one prime factor)",
             "inductive": "assume true for all 2 <= k < n",
             "step": ("if n is prime, done (1 factor <= n). "
                      "If n = ab with 2 <= a,b < n, a uses <= a factors, "
                      "b uses <= b factors, total <= a+b <= n.")},
            {"claim": "a binary tree with n internal nodes has n+1 leaves",
             "base": "n=0: tree is a single leaf, 0+1=1 leaf",
             "inductive": "assume true for all trees with < n internal nodes",
             "step": ("remove root: left subtree has k internal nodes, "
                      "right has n-1-k. By hypothesis: k+1 + (n-1-k)+1 = n+1 leaves.")},
            {"claim": (f"every {dv}-regular graph on n >= {dv + 1} "
                       f"vertices has a Hamiltonian cycle"),
             "base": f"K_{dv+1} has a Hamiltonian cycle",
             "inductive": "assume true for all such graphs with < n vertices",
             "step": "by Dirac's theorem (degree >= n/2), Hamiltonian cycle exists."},
            {"claim": f"2^n > n^{eb} for all n >= {eb * 4}",
             "base": (f"2^{eb * 4} = {2**(eb * 4)} > "
                      f"{(eb * 4)**eb} = ({eb * 4})^{eb}"),
             "inductive": f"assume 2^k > k^{eb} for all {eb * 4} <= k < n",
             "step": (f"2^n = 2 * 2^(n-1) > 2 * (n-1)^{eb} "
                      f"> n^{eb} for large n")},
        ]

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a strong induction proof with randomised parameters.

        Args:
            difficulty: Controls which proof templates are accessible.

        Returns:
            Tuple of (claim_string, proof_data).
        """
        pm = self._random_params()
        proofs = (self._number_theory_templates(pm)
                  + self._structural_templates(pm))
        proof = self._rng.choice(proofs[:min(len(proofs), 2 + difficulty)])
        return f"prove by strong induction: {proof['claim']}", proof

    def _create_steps(self, sd: dict) -> list[str]:
        return [f"base: {sd['base']}", f"hypothesis: {sd['inductive']}", f"step: {sd['step']}"]

    def _create_answer(self, sd: dict) -> str:
        return "QED"
