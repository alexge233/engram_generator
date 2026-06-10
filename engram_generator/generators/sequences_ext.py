"""Extended sequences and series generators.

6 generators across tiers 4-5 covering harmonic series, telescoping
series, second-order recurrences, power series evaluation, sequence
limits, and Fibonacci properties.
"""
from __future__ import annotations

import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


# ---------------------------------------------------------------------------
# 1. Harmonic series (tier 4)
# ---------------------------------------------------------------------------


@register
class HarmonicSeriesGenerator(StepGenerator):
    """Compute partial sums of the harmonic series H_n = sum 1/k for k=1..n.

    Compares H_n with the approximation ln(n) + gamma.

    Difficulty scaling:
        d1-3: n in 3..8.
        d4-6: n in 8..15.
        d7-8: n in 15..25.

    Prerequisites:
        addition.
    """

    _EULER_GAMMA = 0.5772

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "harmonic_series"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["addition"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task description string.
        """
        return "compute harmonic partial sum"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a harmonic series partial sum problem.

        Args:
            difficulty: Controls the value of n.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            n = self._rng.randint(3, 8)
        elif difficulty <= 6:
            n = self._rng.randint(8, 15)
        else:
            n = self._rng.randint(15, 25)

        partial = 0.0
        terms = []
        for k in range(1, n + 1):
            partial += 1.0 / k
            terms.append(f"1/{k}")
        partial = round(partial, 4)
        approx = round(math.log(n) + self._EULER_GAMMA, 4)

        return (
            f"H_{n} = sum 1/k for k=1..{n}",
            {"n": n, "partial": partial, "approx": approx, "terms": terms},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Return summation steps.

        Args:
            sd: Solution data.

        Returns:
            Step strings.
        """
        shown = sd["terms"][:6]
        summary = " + ".join(shown)
        if len(sd["terms"]) > 6:
            summary += " + ..."
        return [
            f"H_{sd['n']} = {summary}",
            f"partial sum = {sd['partial']}",
            f"ln({sd['n']}) + gamma ~ {sd['approx']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the partial sum.

        Args:
            sd: Solution data.

        Returns:
            Answer string.
        """
        return f"H_{sd['n']} = {sd['partial']}"


# ---------------------------------------------------------------------------
# 2. Telescoping series (tier 4)
# ---------------------------------------------------------------------------


@register
class TelescopingSeriesGenerator(StepGenerator):
    """Compute telescoping sum: sum (1/k - 1/(k+1)) = 1 - 1/(n+1).

    Shows term cancellation.

    Difficulty scaling:
        d1-3: n in 3..6.
        d4-6: n in 6..10.
        d7-8: n in 10..15.

    Prerequisites:
        addition.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "telescoping_series"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["addition"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task description string.
        """
        return "evaluate telescoping series"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a telescoping series problem.

        Args:
            difficulty: Controls number of terms.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            n = self._rng.randint(3, 6)
        elif difficulty <= 6:
            n = self._rng.randint(6, 10)
        else:
            n = self._rng.randint(10, 15)

        terms = []
        for k in range(1, n + 1):
            terms.append(f"(1/{k} - 1/{k + 1})")

        result = round(1.0 - 1.0 / (n + 1), 4)

        return (
            f"sum (1/k - 1/(k+1)) for k=1..{n}",
            {"n": n, "terms": terms, "result": result},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Return cancellation steps.

        Args:
            sd: Solution data.

        Returns:
            Step strings.
        """
        shown = sd["terms"][:4]
        return [
            " + ".join(shown) + (" + ..." if len(sd["terms"]) > 4 else ""),
            "most terms cancel",
            f"= 1 - 1/{sd['n'] + 1} = {sd['result']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the series sum.

        Args:
            sd: Solution data.

        Returns:
            Answer string.
        """
        return str(sd["result"])


# ---------------------------------------------------------------------------
# 3. Second-order recurrence (tier 5)
# ---------------------------------------------------------------------------


@register
class RecurrenceSecondOrderGenerator(StepGenerator):
    """Compute terms of a_n = p*a_{n-1} + q*a_{n-2}.

    Given a_0, a_1, compute a_2..a_6. Also gives the characteristic
    equation r^2 = p*r + q.

    Difficulty scaling:
        d1-4: small coefficients (p,q in 1..3).
        d5-8: larger coefficients (p,q in 1..5).

    Prerequisites:
        arithmetic_sequence.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "recurrence_second_order"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["arithmetic_sequence"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task description string.
        """
        return "solve second-order recurrence"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a second-order recurrence and compute terms.

        Args:
            difficulty: Controls coefficient ranges.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        hi = 3 if difficulty <= 4 else 5
        p = self._rng.randint(1, hi)
        q = self._rng.randint(1, hi)
        a0 = self._rng.randint(0, 5)
        a1 = self._rng.randint(1, 5)

        vals = [a0, a1]
        for _ in range(5):
            nxt = p * vals[-1] + q * vals[-2]
            vals.append(nxt)

        # Characteristic equation: r^2 - p*r - q = 0
        disc = p * p + 4 * q
        char_eq = f"r^2 - {p}*r - {q} = 0"

        return (
            f"a_0={a0}, a_1={a1}, a_n = {p}*a_{{n-1}} + {q}*a_{{n-2}}. Find a_2..a_6.",
            {"p": p, "q": q, "vals": vals, "char_eq": char_eq, "disc": disc},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Return computation steps.

        Args:
            sd: Solution data.

        Returns:
            Step strings.
        """
        steps = [f"a_{i} = {sd['vals'][i]}" for i in range(len(sd["vals"]))]
        steps.append(f"char. eq.: {sd['char_eq']}, disc={sd['disc']}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the computed sequence.

        Args:
            sd: Solution data.

        Returns:
            Answer string.
        """
        return ", ".join(f"a_{i}={sd['vals'][i]}" for i in range(len(sd["vals"])))


# ---------------------------------------------------------------------------
# 4. Power series evaluation (tier 5)
# ---------------------------------------------------------------------------


@register
class PowerSeriesEvalGenerator(StepGenerator):
    """Evaluate power series for e^x or sin(x) for the first N terms.

    e^x = sum x^n/n!, sin(x) = sum (-1)^n * x^(2n+1) / (2n+1)!.

    Difficulty scaling:
        d1-4: 4 terms, x in {0.5, 1.0}.
        d5-8: 5-6 terms, x in {0.5, 1.0, 2.0}.

    Prerequisites:
        exponentiation.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "power_series_eval"

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
        return "evaluate power series"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a power series evaluation problem.

        Args:
            difficulty: Controls number of terms and x values.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 4:
            n_terms = 4
            x = self._rng.choice([0.5, 1.0])
        else:
            n_terms = self._rng.randint(5, 6)
            x = self._rng.choice([0.5, 1.0, 2.0])

        func = self._rng.choice(["exp", "sin"])
        terms = []
        total = 0.0

        if func == "exp":
            for n in range(n_terms):
                term = (x ** n) / math.factorial(n)
                terms.append(f"x^{n}/{n}! = {round(term, 4)}")
                total += term
            exact = math.exp(x)
            label = f"e^{x}"
        else:
            for n in range(n_terms):
                sign = (-1) ** n
                power = 2 * n + 1
                term = sign * (x ** power) / math.factorial(power)
                terms.append(f"(-1)^{n}*x^{power}/{power}! = {round(term, 4)}")
                total += term
            exact = math.sin(x)
            label = f"sin({x})"

        total = round(total, 4)
        exact = round(exact, 4)
        error = round(abs(total - exact), 4)

        return (
            f"Evaluate {label} using first {n_terms} terms of power series",
            {
                "func": func, "x": x, "n_terms": n_terms,
                "terms": terms, "total": total,
                "exact": exact, "error": error, "label": label,
            },
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Return term-by-term evaluation steps.

        Args:
            sd: Solution data.

        Returns:
            Step strings.
        """
        steps = sd["terms"]
        steps.append(f"sum = {sd['total']}")
        steps.append(f"exact {sd['label']} = {sd['exact']}, error = {sd['error']}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the partial sum.

        Args:
            sd: Solution data.

        Returns:
            Answer string.
        """
        return f"{sd['label']} ~ {sd['total']}"


# ---------------------------------------------------------------------------
# 5. Sequence limit (tier 4)
# ---------------------------------------------------------------------------


@register
class SequenceLimitGenerator(StepGenerator):
    """Compute the limit of a sequence as n -> infinity.

    Templates: (3n+1)/(2n-5) -> 3/2, n/(n^2+1) -> 0,
    (1+1/n)^n -> e.

    Difficulty scaling:
        d1-4: rational limit (linear/linear).
        d5-8: includes (1+1/n)^n -> e and n/poly.

    Prerequisites:
        division.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "sequence_limit"

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
            Task description string.
        """
        return "find sequence limit"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a sequence limit problem from templates.

        Args:
            difficulty: Controls which templates are available.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        templates = []

        # Template 1: (an+b)/(cn+d) -> a/c
        a = self._rng.randint(1, 6)
        b = self._rng.randint(-5, 5)
        c = self._rng.randint(1, 6)
        d = self._rng.randint(-5, 5)
        limit_val = round(a / c, 4)
        templates.append({
            "expr": f"({a}n+{b})/({c}n+{d})",
            "method": f"divide by n: ({a}+{b}/n)/({c}+{d}/n) -> {a}/{c}",
            "limit": limit_val,
            "limit_str": f"{a}/{c} = {limit_val}",
        })

        # Template 2: n/(n^2+1) -> 0
        templates.append({
            "expr": "n/(n^2+1)",
            "method": "divide by n^2: (1/n)/(1+1/n^2) -> 0",
            "limit": 0.0,
            "limit_str": "0",
        })

        if difficulty >= 5:
            # Template 3: (1+1/n)^n -> e
            templates.append({
                "expr": "(1+1/n)^n",
                "method": "classic limit: (1+1/n)^n -> e",
                "limit": round(math.e, 4),
                "limit_str": f"e = {round(math.e, 4)}",
            })

        chosen = self._rng.choice(templates)

        # Compute numeric check at large n
        n_check = 1000
        try:
            if "^n" in chosen["expr"]:
                check_val = round((1 + 1 / n_check) ** n_check, 4)
            elif "n^2" in chosen["expr"]:
                check_val = round(n_check / (n_check ** 2 + 1), 4)
            else:
                check_val = round((a * n_check + b) / (c * n_check + d), 4)
        except ZeroDivisionError:
            check_val = chosen["limit"]

        return (
            f"lim n->inf a_n = {chosen['expr']}",
            {
                "expr": chosen["expr"], "method": chosen["method"],
                "limit": chosen["limit"], "limit_str": chosen["limit_str"],
                "check_val": check_val,
            },
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Return limit computation steps.

        Args:
            sd: Solution data.

        Returns:
            Step strings.
        """
        return [
            f"a_n = {sd['expr']}",
            sd["method"],
            f"numeric check at n=1000: {sd['check_val']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the limit value.

        Args:
            sd: Solution data.

        Returns:
            Answer string.
        """
        return f"limit = {sd['limit_str']}"


# ---------------------------------------------------------------------------
# 6. Fibonacci properties (tier 4)
# ---------------------------------------------------------------------------


@register
class FibonacciPropertiesGenerator(StepGenerator):
    """Verify Fibonacci identities: partial sum and Cassini's identity.

    sum F_1..F_n = F_{n+2} - 1.
    F_n * F_{n+2} - F_{n+1}^2 = (-1)^{n+1} (Cassini).

    Difficulty scaling:
        d1-4: n in 3..8.
        d5-8: n in 8..14.

    Prerequisites:
        fibonacci.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "fibonacci_properties"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["fibonacci"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task description string.
        """
        return "verify Fibonacci identity"

    def _fib(self, n: int) -> int:
        """Compute the nth Fibonacci number (F_1=1, F_2=1).

        Args:
            n: Index (1-based).

        Returns:
            F_n.
        """
        if n <= 0:
            return 0
        a, b = 0, 1
        for _ in range(n):
            a, b = b, a + b
        return a

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Fibonacci identity verification problem.

        Args:
            difficulty: Controls the value of n.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 4:
            n = self._rng.randint(3, 8)
        else:
            n = self._rng.randint(8, 14)

        prop = self._rng.choice(["partial_sum", "cassini"])

        fibs = [self._fib(i) for i in range(n + 3)]

        if prop == "partial_sum":
            # sum F_1..F_n = F_{n+2} - 1
            partial = sum(fibs[1:n + 1])
            f_np2 = fibs[n + 2]
            expected = f_np2 - 1
            steps = [
                f"F_1..F_{n}: {fibs[1:n+1]}",
                f"sum = {partial}",
                f"F_{n+2} - 1 = {f_np2} - 1 = {expected}",
                f"match: {partial == expected}",
            ]
            answer = f"sum={partial}, F_{n+2}-1={expected}, verified"
        else:
            # Cassini: F_n * F_{n+2} - F_{n+1}^2 = (-1)^{n+1}
            fn = fibs[n]
            fn1 = fibs[n + 1]
            fn2 = fibs[n + 2]
            lhs = fn * fn2 - fn1 * fn1
            rhs = (-1) ** (n + 1)
            steps = [
                f"F_{n}={fn}, F_{n+1}={fn1}, F_{n+2}={fn2}",
                f"F_{n}*F_{n+2} - F_{n+1}^2 = {fn}*{fn2} - {fn1}^2 = {lhs}",
                f"(-1)^{n+1} = {rhs}",
                f"match: {lhs == rhs}",
            ]
            answer = f"Cassini: {lhs} = {rhs}, verified"

        return (
            f"Verify Fibonacci {prop} for n={n}",
            {"prop": prop, "n": n, "steps": steps, "answer": answer},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Return verification steps.

        Args:
            sd: Solution data.

        Returns:
            Step strings.
        """
        return sd["steps"]

    def _create_answer(self, sd: dict) -> str:
        """Return the verification result.

        Args:
            sd: Solution data.

        Returns:
            Answer string.
        """
        return sd["answer"]
