"""Numerical methods generators.

4 generators across tiers 3-4.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register

@register
class BisectionMethodGenerator(StepGenerator):
    """Find a root using the bisection method."""

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "bisection_method"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 3

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["division"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description."""
        return "bisection method step"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        root = self._rng.randint(1, 10 * difficulty)
        a = root - self._rng.randint(1, 5)
        b = root + self._rng.randint(1, 5)
        n_steps = min(2 + difficulty, 6)
        steps_log = []
        for _ in range(n_steps):
            mid = (a + b) / 2
            f_mid = mid - root
            steps_log.append(f"[{a:.2f},{b:.2f}] mid={mid:.2f} f(mid)={f_mid:.2f}")
            if f_mid > 0:
                b = mid
            else:
                a = mid
        final = round((a + b) / 2, 4)
        return (
            f"f(x) = x - {root}, interval [{a:.2f},{b:.2f}], {n_steps} steps",
            {"root": root, "steps_log": steps_log, "final": final},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        return sd["steps_log"]

    def _create_answer(self, sd: dict) -> str:
        return f"{sd['final']}"


@register
class TrapezoidalRuleGenerator(StepGenerator):
    """Approximate an integral using the trapezoidal rule."""

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "trapezoidal_rule"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 3

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["area_rectangle"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description."""
        return "trapezoidal rule"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        a_val = self._rng.randint(0, 3)
        b_val = a_val + self._rng.randint(1, 3 + difficulty)
        n = min(2 + difficulty, 8)
        h = (b_val - a_val) / n
        xs = [a_val + i * h for i in range(n + 1)]
        fn_type = self._rng.choice(["x^2", "x^3", "x"])
        if fn_type == "x^2":
            fxs = [x ** 2 for x in xs]
        elif fn_type == "x^3":
            fxs = [x ** 3 for x in xs]
        else:
            fxs = [x for x in xs]
        integral = h / 2 * (fxs[0] + fxs[-1] + 2 * sum(fxs[1:-1]))
        return (
            f"integral of {fn_type} from {a_val} to {b_val}, n={n}",
            {"fn": fn_type, "a": a_val, "b": b_val, "n": n, "h": h,
             "xs": xs, "fxs": fxs, "integral": round(integral, 4)},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        return [
            f"h = ({sd['b']}-{sd['a']})/{sd['n']} = {sd['h']:.4f}",
            f"f values: {[round(f, 2) for f in sd['fxs']]}",
        ]

    def _create_answer(self, sd: dict) -> str:
        return f"{sd['integral']}"


@register
class EulerMethodODEGenerator(StepGenerator):
    """Take Euler method steps for a simple ODE."""

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "euler_method_ode"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["derivative"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description."""
        return "Euler method step"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        y0 = round(self._rng.uniform(0.5, 3.0), 1)
        h = round(self._rng.choice([0.1, 0.2, 0.5]), 2)
        n_steps = min(3 + difficulty, 8)
        ode = self._rng.choice(["y", "-y", "2*y", "x+y"])
        x, y = 0.0, y0
        trace = [(round(x, 4), round(y, 4))]
        for _ in range(n_steps):
            if ode == "y":
                dy = y
            elif ode == "-y":
                dy = -y
            elif ode == "2*y":
                dy = 2 * y
            else:
                dy = x + y
            y = y + h * dy
            x = x + h
            trace.append((round(x, 4), round(y, 4)))
        return (
            f"dy/dx = {ode}, y(0)={y0}, h={h}, {n_steps} steps",
            {"ode": ode, "y0": y0, "h": h, "trace": trace},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        return [f"x={x}, y={y}" for x, y in sd["trace"]]

    def _create_answer(self, sd: dict) -> str:
        x, y = sd["trace"][-1]
        return f"y({x}) = {y}"


@register
class NumericalDerivativeGenerator(StepGenerator):
    """Approximate a derivative using finite differences."""

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "numerical_derivative"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 3

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["derivative"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description."""
        return "numerical derivative"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        fn = self._rng.choice(["x^2", "x^3", "sin(x)"])
        x = round(self._rng.uniform(0.5, 5.0), 2)
        h = round(10 ** (-self._rng.randint(1, min(4, 1 + difficulty))), 6)

        if fn == "x^2":
            f = lambda v: v ** 2
            exact = 2 * x
        elif fn == "x^3":
            f = lambda v: v ** 3
            exact = 3 * x ** 2
        else:
            f = lambda v: math.sin(v)
            exact = math.cos(x)

        central = (f(x + h) - f(x - h)) / (2 * h)
        error = abs(central - exact)
        return (
            f"d/dx({fn}) at x={x}, h={h}",
            {"fn": fn, "x": x, "h": h, "approx": round(central, 6),
             "exact": round(exact, 6), "error": round(error, 8)},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        return [
            f"central diff: (f(x+h) - f(x-h)) / (2h)",
            f"approx = {sd['approx']}",
            f"exact = {sd['exact']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        return f"{sd['approx']} (error={sd['error']})"
