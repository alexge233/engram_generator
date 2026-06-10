"""Extended meta-reasoning generators -- proof strategy, dimensional checks,
approximation bounds, research methodology, and theorem dependencies.

Builds on existing meta-reasoning and proof-verification generators with
tier 7-9 tasks requiring strategic reasoning about mathematical arguments,
physics consistency, approximation theory, and dependency analysis.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


class ProofStrategyPool:
    """Encapsulates proof strategy selection for mathematical statements.

    Maps mathematical statement types to appropriate proof strategies
    and provides rationale for each selection.

    Attributes:
        _strategies: Mapping of statement types to strategy info.
    """

    _STRATEGIES = {
        "divisibility": {
            "best": "direct",
            "rationale": "direct computation from definition",
            "alternatives": ["induction"],
        },
        "irrationality": {
            "best": "contradiction",
            "rationale": "assume rational p/q, derive contradiction",
            "alternatives": ["construction"],
        },
        "sum_formula": {
            "best": "induction",
            "rationale": "base case then inductive step on n",
            "alternatives": ["direct"],
        },
        "inequality": {
            "best": "cases",
            "rationale": "split by sign of variable to handle absolute values",
            "alternatives": ["contradiction", "direct"],
        },
        "existence": {
            "best": "construction",
            "rationale": "explicitly construct the required object",
            "alternatives": ["contradiction"],
        },
        "uniqueness": {
            "best": "contradiction",
            "rationale": "assume two solutions exist, show they must be equal",
            "alternatives": ["direct"],
        },
        "equivalence": {
            "best": "direct",
            "rationale": "prove both directions by direct implication",
            "alternatives": ["contradiction"],
        },
        "pigeonhole": {
            "best": "contradiction",
            "rationale": "assume no box has 2+ items, count contradiction",
            "alternatives": ["direct"],
        },
    }

    def get_statement_types(self) -> list[str]:
        """Return all available statement types.

        Returns:
            List of statement type keys.
        """
        return list(self._STRATEGIES.keys())

    def get_strategy(self, statement_type: str) -> dict:
        """Return the strategy info for a statement type.

        Args:
            statement_type: Key into the strategy pool.

        Returns:
            Dict with best strategy, rationale, and alternatives.
        """
        return dict(self._STRATEGIES[statement_type])


class DimensionChecker:
    """Verifies dimensional consistency of physics equations.

    Assigns fundamental dimensions [M], [L], [T] to physical
    quantities and checks that both sides of an equation match.

    Attributes:
        _dimension_table: Mapping of quantity names to dimension tuples.
    """

    _DIMENSION_TABLE = {
        "force": (1, 1, -2),
        "mass": (1, 0, 0),
        "acceleration": (0, 1, -2),
        "velocity": (0, 1, -1),
        "distance": (0, 1, 0),
        "time": (0, 0, 1),
        "energy": (1, 2, -2),
        "power": (1, 2, -3),
        "pressure": (1, -1, -2),
        "area": (0, 2, 0),
        "momentum": (1, 1, -1),
        "density": (1, -3, 0),
        "volume": (0, 3, 0),
        "frequency": (0, 0, -1),
        "charge": (0, 0, 1),
    }

    def get_dimensions(self, quantity: str) -> tuple[int, int, int]:
        """Return (M, L, T) exponents for a quantity.

        Args:
            quantity: Name of the physical quantity.

        Returns:
            Tuple of dimension exponents (M, L, T).
        """
        return self._DIMENSION_TABLE.get(quantity, (0, 0, 0))

    def format_dimensions(self, dims: tuple[int, int, int]) -> str:
        """Format dimension tuple as human-readable string.

        Args:
            dims: Tuple of (M, L, T) exponents.

        Returns:
            Formatted dimension string like [M^1 L^1 T^-2].
        """
        labels = ["M", "L", "T"]
        parts = []
        for label, exp in zip(labels, dims):
            if exp != 0:
                parts.append(f"{label}^{exp}" if exp != 1 else label)
        return "[" + " ".join(parts) + "]" if parts else "[1]"

    def dims_equal(self, d1: tuple[int, int, int],
                   d2: tuple[int, int, int]) -> bool:
        """Check if two dimension tuples are equal.

        Args:
            d1: First dimension tuple.
            d2: Second dimension tuple.

        Returns:
            True if dimensions match.
        """
        return d1 == d2

    def get_available_quantities(self) -> list[str]:
        """Return all available quantity names.

        Returns:
            List of quantity name strings.
        """
        return list(self._DIMENSION_TABLE.keys())


@register
class ProofStrategyGenerator(StepGenerator):
    """Select the best proof strategy for a mathematical statement.

    Given a mathematical statement type, identifies the most appropriate
    proof strategy (direct, contradiction, induction, cases, construction),
    provides rationale, and lists alternatives.

    Input format:
        ``select proof strategy for this statement``

    Target format:
        ``statement: for all n>=1, 1+2+...+n = n(n+1)/2 <step>
        type: sum formula <step> best strategy: induction <step>
        rationale: base case then inductive step on n <step>
        alternatives: direct <step> induction``

    Difficulty scaling:
        Difficulty 1-2: divisibility or sum formula (obvious choice).
        Difficulty 3-4: irrationality or existence.
        Difficulty 5-6: inequality or uniqueness.
        Difficulty 7-8: pigeonhole or equivalence.

    Prerequisites:
        verify_proof.

    Example:
        >>> gen = ProofStrategyGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'proof_strategy'
    """

    _STATEMENTS = {
        "divisibility": [
            "prove that n^2-n is divisible by 2 for all n>=1",
            "prove that n^3-n is divisible by 6 for all n>=1",
            "prove that 3 divides n^3+2n for all n>=0",
        ],
        "irrationality": [
            "prove that sqrt(2) is irrational",
            "prove that sqrt(3) is irrational",
            "prove that log_2(3) is irrational",
        ],
        "sum_formula": [
            "prove that 1+2+...+n = n(n+1)/2",
            "prove that 1^2+2^2+...+n^2 = n(n+1)(2n+1)/6",
            "prove that 1+3+5+...+(2n-1) = n^2",
        ],
        "inequality": [
            "prove that |a+b| <= |a|+|b|",
            "prove that (a+b)/2 >= sqrt(ab) for a,b >= 0",
            "prove that |ab| = |a||b|",
        ],
        "existence": [
            "prove there exists an irrational number between any two rationals",
            "prove there exists a prime greater than any given n",
            "prove there exists a solution to x^2 = 2 in the reals",
        ],
        "uniqueness": [
            "prove that the identity element of a group is unique",
            "prove that the inverse of each element in a group is unique",
            "prove that the zero vector is unique",
        ],
        "equivalence": [
            "prove that n is even iff n^2 is even",
            "prove that a|b and b|a iff a=b (for positive integers)",
            "prove that f is continuous iff preimage of every open set is open",
        ],
        "pigeonhole": [
            "prove that among 13 people, at least 2 share a birth month",
            "prove that in any set of 5 integers, two have same remainder mod 4",
            "prove that among n+1 numbers from {1,...,2n}, two are consecutive",
        ],
    }

    _DIFFICULTY_TYPES = {
        1: ["divisibility", "sum_formula"],
        2: ["divisibility", "sum_formula"],
        3: ["irrationality", "existence"],
        4: ["irrationality", "existence"],
        5: ["inequality", "uniqueness"],
        6: ["inequality", "uniqueness"],
        7: ["pigeonhole", "equivalence"],
        8: ["pigeonhole", "equivalence"],
    }

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "proof_strategy"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["verify_proof"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls statement type.

        Returns:
            Natural language description.
        """
        return "select proof strategy for this statement"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a mathematical statement and determine best proof strategy.

        Args:
            difficulty: Controls statement complexity.

        Returns:
            Tuple of (statement, solution_data).
        """
        pool = ProofStrategyPool()
        types = self._DIFFICULTY_TYPES.get(difficulty, ["divisibility"])
        stmt_type = self._rng.choice(types)
        statement = self._rng.choice(self._STATEMENTS[stmt_type])
        strategy_info = pool.get_strategy(stmt_type)

        problem = f"statement: {statement}"
        return problem, {
            "statement": statement,
            "stmt_type": stmt_type,
            "best": strategy_info["best"],
            "rationale": strategy_info["rationale"],
            "alternatives": strategy_info["alternatives"],
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate strategy selection and rationale steps.

        Args:
            data: Solution data with strategy info.

        Returns:
            Steps showing type identification, strategy, and rationale.
        """
        alt_str = ", ".join(data["alternatives"])
        return [
            f"type: {data['stmt_type']}",
            f"best strategy: {data['best']}",
            f"rationale: {data['rationale']}",
            f"alternatives: {alt_str}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the selected proof strategy.

        Args:
            data: Solution data.

        Returns:
            Strategy name string.
        """
        return data["best"]


@register
class DimensionalCheckGenerator(StepGenerator):
    """Verify dimensional consistency of a physics equation.

    Assigns fundamental dimensions [M], [L], [T] to each term in a
    physics equation and checks that LHS and RHS have matching dimensions.

    Input format:
        ``check dimensional consistency``

    Target format:
        ``equation: F = m*a <step>
        LHS: F -> [M L T^-2] <step>
        RHS: m*a -> [M]*[L T^-2] = [M L T^-2] <step>
        consistent: True <step> True``

    Difficulty scaling:
        Difficulty 1-3: 2-term equations (F=ma, p=mv).
        Difficulty 4-6: 3-term equations (E=0.5mv^2, P=F*v).
        Difficulty 7-8: equations with deliberate errors to detect.

    Prerequisites:
        dimensional_analysis.

    Example:
        >>> gen = DimensionalCheckGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'dimensional_check'
    """

    _EQUATIONS = [
        {
            "equation": "F = m * a",
            "lhs": "force", "lhs_dims": (1, 1, -2),
            "rhs_parts": [("mass", (1, 0, 0)), ("acceleration", (0, 1, -2))],
            "rhs_dims": (1, 1, -2), "consistent": True,
        },
        {
            "equation": "p = m * v",
            "lhs": "momentum", "lhs_dims": (1, 1, -1),
            "rhs_parts": [("mass", (1, 0, 0)), ("velocity", (0, 1, -1))],
            "rhs_dims": (1, 1, -1), "consistent": True,
        },
        {
            "equation": "E = 0.5 * m * v^2",
            "lhs": "energy", "lhs_dims": (1, 2, -2),
            "rhs_parts": [("mass", (1, 0, 0)), ("velocity^2", (0, 2, -2))],
            "rhs_dims": (1, 2, -2), "consistent": True,
        },
        {
            "equation": "P = F * v",
            "lhs": "power", "lhs_dims": (1, 2, -3),
            "rhs_parts": [("force", (1, 1, -2)), ("velocity", (0, 1, -1))],
            "rhs_dims": (1, 2, -3), "consistent": True,
        },
        {
            "equation": "pressure = F / A",
            "lhs": "pressure", "lhs_dims": (1, -1, -2),
            "rhs_parts": [("force", (1, 1, -2)), ("area^-1", (0, -2, 0))],
            "rhs_dims": (1, -1, -2), "consistent": True,
        },
        {
            "equation": "F = m * v (WRONG)",
            "lhs": "force", "lhs_dims": (1, 1, -2),
            "rhs_parts": [("mass", (1, 0, 0)), ("velocity", (0, 1, -1))],
            "rhs_dims": (1, 1, -1), "consistent": False,
        },
        {
            "equation": "E = m * a (WRONG)",
            "lhs": "energy", "lhs_dims": (1, 2, -2),
            "rhs_parts": [("mass", (1, 0, 0)), ("acceleration", (0, 1, -2))],
            "rhs_dims": (1, 1, -2), "consistent": False,
        },
        {
            "equation": "P = m * v^2 (WRONG)",
            "lhs": "power", "lhs_dims": (1, 2, -3),
            "rhs_parts": [("mass", (1, 0, 0)), ("velocity^2", (0, 2, -2))],
            "rhs_dims": (1, 2, -2), "consistent": False,
        },
    ]

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "dimensional_check"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["dimensional_analysis"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls equation complexity.

        Returns:
            Natural language description.
        """
        return "check dimensional consistency"

    def _get_pool(self, difficulty: int) -> list[dict]:
        """Select equation pool based on difficulty.

        Args:
            difficulty: Difficulty level.

        Returns:
            List of candidate equation dicts.
        """
        consistent = [e for e in self._EQUATIONS if e["consistent"]]
        inconsistent = [e for e in self._EQUATIONS if not e["consistent"]]
        if difficulty <= 3:
            return consistent[:2]
        if difficulty <= 6:
            return consistent[2:]
        return consistent + inconsistent

    def _format_dims(self, dims: tuple[int, int, int]) -> str:
        """Format dimension tuple as human-readable string.

        Args:
            dims: Tuple of (M, L, T) exponents.

        Returns:
            Formatted dimension string.
        """
        checker = DimensionChecker()
        return checker.format_dimensions(dims)

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an equation and check its dimensional consistency.

        Args:
            difficulty: Controls equation complexity.

        Returns:
            Tuple of (equation_string, solution_data).
        """
        pool = self._get_pool(difficulty)
        eq = self._rng.choice(pool)

        problem = f"check: {eq['equation']}"
        return problem, {
            "equation": eq["equation"],
            "lhs": eq["lhs"], "lhs_dims": eq["lhs_dims"],
            "rhs_parts": eq["rhs_parts"], "rhs_dims": eq["rhs_dims"],
            "consistent": eq["consistent"],
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate dimensional analysis steps.

        Args:
            data: Solution data with equation and dimensions.

        Returns:
            Steps showing LHS dims, RHS dims, and consistency check.
        """
        steps: list[str] = []
        lhs_str = self._format_dims(data["lhs_dims"])
        steps.append(f"LHS: {data['lhs']} -> {lhs_str}")

        rhs_parts_str = " * ".join(
            f"{name}={self._format_dims(dims)}"
            for name, dims in data["rhs_parts"]
        )
        rhs_str = self._format_dims(data["rhs_dims"])
        steps.append(f"RHS: {rhs_parts_str} = {rhs_str}")

        steps.append(f"LHS={lhs_str}, RHS={rhs_str}")
        steps.append(f"consistent: {data['consistent']}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return whether the equation is dimensionally consistent.

        Args:
            data: Solution data.

        Returns:
            'True' or 'False'.
        """
        return str(data["consistent"])


@register
class ApproximationBoundGenerator(StepGenerator):
    """Bound the error of a Taylor approximation.

    Computes |R_n(x)| <= M * |x - a|^(n+1) / (n+1)! where M bounds
    |f^(n+1)| on the interval. Uses common functions (sin, cos, exp)
    with known derivative bounds.

    Input format:
        ``bound Taylor approximation error``

    Target format:
        ``f(x)=sin(x), a=0, n=3, x=0.5 <step>
        |f^(4)(x)|<=1 for sin, so M=1 <step>
        |R_3(0.5)|<=1*|0.5|^4/4!=0.0625/24=0.0026 <step> 0.0026``

    Difficulty scaling:
        Difficulty 1-3: sin/cos at x near 0, low order.
        Difficulty 4-6: exp, moderate order.
        Difficulty 7-8: larger x or higher order.

    Prerequisites:
        taylor_series.

    Example:
        >>> gen = ApproximationBoundGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'approximation_bound'
    """

    _FUNCTIONS = {
        "sin": {"M_bound": 1.0, "desc": "|f^(k)(x)|<=1 for all k"},
        "cos": {"M_bound": 1.0, "desc": "|f^(k)(x)|<=1 for all k"},
        "exp": {"M_bound": None, "desc": "|f^(k)(x)|<=exp(|x|)"},
    }

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "approximation_bound"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["taylor_series"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls function and order.

        Returns:
            Natural language description.
        """
        return "bound Taylor approximation error"

    def _config(self, difficulty: int) -> tuple[str, int, float]:
        """Map difficulty to function, order, and evaluation point.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (function_name, order, x_value).
        """
        if difficulty <= 3:
            func = self._rng.choice(["sin", "cos"])
            n = self._rng.choice([2, 3])
            x = round(self._rng.uniform(0.1, 0.5), 2)
        elif difficulty <= 6:
            func = self._rng.choice(["sin", "cos", "exp"])
            n = self._rng.choice([3, 4])
            x = round(self._rng.uniform(0.2, 0.8), 2)
        else:
            func = self._rng.choice(["sin", "cos", "exp"])
            n = self._rng.choice([4, 5, 6])
            x = round(self._rng.uniform(0.5, 1.5), 2)
        return func, n, x

    def _factorial(self, n: int) -> int:
        """Compute n factorial.

        Args:
            n: Non-negative integer.

        Returns:
            n! value.
        """
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Taylor remainder bound problem.

        Args:
            difficulty: Controls function, order, and point.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        func, n, x = self._config(difficulty)
        a = 0

        func_info = self._FUNCTIONS[func]
        if func == "exp":
            m_bound = round(math.exp(abs(x)), 4)
            m_desc = f"M=exp(|{x}|)={m_bound}"
        else:
            m_bound = func_info["M_bound"]
            m_desc = f"M=1 ({func_info['desc']})"

        x_power = round(abs(x - a) ** (n + 1), 4)
        factorial_val = self._factorial(n + 1)
        bound = round(m_bound * x_power / factorial_val, 4)

        problem = f"|R_{n}({x})| for f(x)={func}(x), a={a}, n={n}"
        return problem, {
            "func": func, "n": n, "x": x, "a": a,
            "m_bound": m_bound, "m_desc": m_desc,
            "x_power": x_power, "factorial_val": factorial_val,
            "bound": bound,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate remainder bound computation steps.

        Args:
            data: Solution data with function and bound info.

        Returns:
            Steps showing M, |x-a|^(n+1), (n+1)!, and final bound.
        """
        n = data["n"]
        return [
            f"derivative bound: {data['m_desc']}",
            f"|{data['x']}-{data['a']}|^{{{n + 1}}}={data['x_power']}",
            f"({n + 1})!={data['factorial_val']}",
            f"|R_{n}|<={data['m_bound']}*{data['x_power']}/{data['factorial_val']}={data['bound']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the remainder bound.

        Args:
            data: Solution data.

        Returns:
            String representation of the error bound.
        """
        return str(data["bound"])


@register
class ResearchMethodologyGenerator(StepGenerator):
    """Design an experiment to test a mathematical conjecture.

    States a hypothesis, chooses appropriate test cases, defines
    success criteria, and outlines the verification plan.

    Input format:
        ``design experiment to test conjecture``

    Target format:
        ``conjecture: every even n>2 is sum of two primes <step>
        hypothesis: Goldbach's conjecture holds for n<=1000 <step>
        test cases: n=4,6,8,...,1000 (499 cases) <step>
        method: for each n, find primes p,q with p+q=n <step>
        success: all cases satisfied <step> design complete``

    Difficulty scaling:
        Difficulty 1-3: simple number theory conjectures.
        Difficulty 4-6: sequence and combinatorial conjectures.
        Difficulty 7-8: analytic or structural conjectures.

    Prerequisites:
        hypothesis_design.

    Example:
        >>> gen = ResearchMethodologyGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'research_methodology'
    """

    _CONJECTURES = [
        {
            "name": "Goldbach's conjecture",
            "statement": "every even n>2 is sum of two primes",
            "hypothesis": "holds for all even n in [4, N]",
            "method": "for each even n, search for primes p,q with p+q=n",
            "success": "all even numbers decomposed",
            "test_range": (4, 200),
            "test_count_fn": "even",
        },
        {
            "name": "twin prime density",
            "statement": "there are infinitely many twin primes",
            "hypothesis": "twin prime count grows with N",
            "method": "count pairs (p, p+2) both prime up to N",
            "success": "count increases with each doubling of N",
            "test_range": (10, 1000),
            "test_count_fn": "log",
        },
        {
            "name": "Collatz conjecture",
            "statement": "every positive integer reaches 1 under 3n+1 iteration",
            "hypothesis": "holds for all n in [1, N]",
            "method": "iterate each n; if n even: n/2, if odd: 3n+1, stop at 1",
            "success": "all starting values reach 1",
            "test_range": (1, 500),
            "test_count_fn": "all",
        },
        {
            "name": "prime gap bound",
            "statement": "gap between consecutive primes < sqrt(p)*ln(p)",
            "hypothesis": "bound holds for all primes up to N",
            "method": "compute gaps g_n = p_{n+1} - p_n, check g_n < sqrt(p_n)*ln(p_n)",
            "success": "no gap exceeds bound",
            "test_range": (2, 1000),
            "test_count_fn": "primes",
        },
        {
            "name": "Catalan sequence monotonicity",
            "statement": "C(n+1)/C(n) approaches 4 from below",
            "hypothesis": "ratio C(n+1)/C(n) is strictly increasing and < 4",
            "method": "compute C(n) = (2n)!/(n!(n+1)!), check ratio for n=1..N",
            "success": "ratio increasing and bounded by 4",
            "test_range": (1, 20),
            "test_count_fn": "all",
        },
        {
            "name": "Fibonacci divisibility",
            "statement": "gcd(F_m, F_n) = F_{gcd(m,n)}",
            "hypothesis": "holds for all m,n in [1, N]",
            "method": "for each pair (m,n), verify gcd(F_m,F_n) = F_{gcd(m,n)}",
            "success": "all pairs satisfy the identity",
            "test_range": (1, 20),
            "test_count_fn": "pairs",
        },
    ]

    _DIFFICULTY_POOLS = {
        1: [0, 2], 2: [0, 2], 3: [1, 3], 4: [1, 3],
        5: [4, 5], 6: [4, 5], 7: [0, 1, 2, 3, 4, 5], 8: [0, 1, 2, 3, 4, 5],
    }

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "research_methodology"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 9

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["hypothesis_design"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls conjecture complexity.

        Returns:
            Natural language description.
        """
        return "design experiment to test conjecture"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a conjecture and design an experimental test.

        Args:
            difficulty: Controls conjecture type.

        Returns:
            Tuple of (conjecture_statement, solution_data).
        """
        indices = self._DIFFICULTY_POOLS.get(difficulty, [0])
        idx = self._rng.choice(indices)
        conj = self._CONJECTURES[idx]

        n_max = self._rng.randint(conj["test_range"][0] * 2,
                                  conj["test_range"][1])
        test_count = self._estimate_test_count(conj["test_count_fn"], n_max)

        problem = f"conjecture: {conj['statement']}"
        return problem, {
            "name": conj["name"],
            "statement": conj["statement"],
            "hypothesis": conj["hypothesis"].replace("N", str(n_max)),
            "method": conj["method"],
            "success": conj["success"],
            "n_max": n_max,
            "test_count": test_count,
        }

    def _estimate_test_count(self, fn_type: str, n_max: int) -> int:
        """Estimate number of test cases for a given range.

        Args:
            fn_type: Type of counting function.
            n_max: Maximum value in test range.

        Returns:
            Estimated test case count.
        """
        if fn_type == "even":
            return n_max // 2 - 1
        if fn_type == "log":
            return max(1, int(math.log2(n_max)))
        if fn_type == "primes":
            return max(1, int(n_max / math.log(max(n_max, 2))))
        if fn_type == "pairs":
            return n_max * (n_max - 1) // 2
        return n_max

    def _create_steps(self, data: dict) -> list[str]:
        """Generate experiment design steps.

        Args:
            data: Solution data with conjecture and test plan.

        Returns:
            Steps showing hypothesis, test cases, method, and criteria.
        """
        return [
            f"hypothesis: {data['hypothesis']}",
            f"test cases: {data['test_count']} cases up to N={data['n_max']}",
            f"method: {data['method']}",
            f"success criteria: {data['success']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the experiment design summary.

        Args:
            data: Solution data.

        Returns:
            Design completion string.
        """
        return "design complete"


@register
class TheoremDependencyGenerator(StepGenerator):
    """Identify prerequisite theorems needed to prove a given theorem.

    Given a target theorem, maps its dependency graph by identifying
    which lemmas and prerequisite results are required.

    Input format:
        ``identify prerequisite theorems``

    Target format:
        ``theorem: fundamental theorem of calculus <step>
        requires: mean value theorem <step>
        requires: intermediate value theorem <step>
        requires: definition of Riemann integral <step>
        depth: 3, total prerequisites: 3 <step> dependency graph mapped``

    Difficulty scaling:
        Difficulty 1-3: shallow dependency (1-2 prerequisites).
        Difficulty 4-6: medium depth (2-3 prerequisites).
        Difficulty 7-8: deeper chains (3-4 prerequisites).

    Prerequisites:
        verify_proof.

    Example:
        >>> gen = TheoremDependencyGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'theorem_dependency'
    """

    _THEOREMS = [
        {
            "theorem": "Pythagorean theorem: a^2+b^2=c^2",
            "prerequisites": ["similar triangles", "area of square"],
            "depth": 1,
        },
        {
            "theorem": "quadratic formula: x=(-b+-sqrt(b^2-4ac))/2a",
            "prerequisites": ["completing the square", "square root properties"],
            "depth": 1,
        },
        {
            "theorem": "fundamental theorem of arithmetic",
            "prerequisites": ["well-ordering principle", "Euclid's lemma"],
            "depth": 2,
        },
        {
            "theorem": "Euler's formula: e^{ix}=cos(x)+i*sin(x)",
            "prerequisites": [
                "Taylor series of exp", "Taylor series of sin",
                "Taylor series of cos",
            ],
            "depth": 2,
        },
        {
            "theorem": "fundamental theorem of calculus",
            "prerequisites": [
                "mean value theorem", "definition of Riemann integral",
                "intermediate value theorem",
            ],
            "depth": 3,
        },
        {
            "theorem": "Bolzano-Weierstrass: bounded sequence has convergent subsequence",
            "prerequisites": [
                "nested intervals theorem", "completeness of reals",
                "monotone convergence theorem",
            ],
            "depth": 3,
        },
        {
            "theorem": "spectral theorem for symmetric matrices",
            "prerequisites": [
                "eigenvalue existence (char. polynomial)",
                "Gram-Schmidt orthogonalisation",
                "Schur decomposition",
                "real symmetric => real eigenvalues",
            ],
            "depth": 4,
        },
        {
            "theorem": "Cayley-Hamilton: A satisfies its char. polynomial",
            "prerequisites": [
                "definition of characteristic polynomial",
                "matrix polynomial evaluation",
                "cofactor expansion",
                "adjugate matrix properties",
            ],
            "depth": 4,
        },
    ]

    _DIFFICULTY_POOLS = {
        1: [0, 1], 2: [0, 1], 3: [2, 3], 4: [2, 3],
        5: [4, 5], 6: [4, 5], 7: [6, 7], 8: [6, 7],
    }

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "theorem_dependency"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 8

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["verify_proof"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls theorem complexity.

        Returns:
            Natural language description.
        """
        return "identify prerequisite theorems"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a theorem and identify its prerequisites.

        Args:
            difficulty: Controls theorem depth.

        Returns:
            Tuple of (theorem_statement, solution_data).
        """
        indices = self._DIFFICULTY_POOLS.get(difficulty, [0])
        idx = self._rng.choice(indices)
        thm = self._THEOREMS[idx]

        problem = f"theorem: {thm['theorem']}"
        return problem, {
            "theorem": thm["theorem"],
            "prerequisites": thm["prerequisites"],
            "depth": thm["depth"],
            "total": len(thm["prerequisites"]),
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate dependency identification steps.

        Args:
            data: Solution data with theorem and prerequisites.

        Returns:
            Steps showing each prerequisite and dependency depth.
        """
        steps: list[str] = []
        for prereq in data["prerequisites"]:
            steps.append(f"requires: {prereq}")
        steps.append(
            f"depth: {data['depth']}, total prerequisites: {data['total']}"
        )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the dependency graph summary.

        Args:
            data: Solution data.

        Returns:
            Completion string.
        """
        return "dependency graph mapped"
