"""Extended measurement generators -- error propagation, dimensional
analysis, significant figures calculation, calibration curves,
accuracy/precision, logarithmic scales.

6 generators across tiers 3-5, deepening the measurement domain.
"""
from __future__ import annotations

import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


# ===================================================================
# 1. Error propagation  (tier 5)
# ===================================================================

@register
class ErrorPropagationGenerator(StepGenerator):
    """Compute propagated uncertainty through arithmetic operations.

    For multiplication f = a*b: df/f = sqrt((da/a)^2 + (db/b)^2).
    For addition f = a+b: df = sqrt(da^2 + db^2).

    Difficulty scaling:
        Difficulty 1-3: addition/subtraction uncertainty only.
        Difficulty 4-6: multiplication/division uncertainty only.
        Difficulty 7-8: mixed operations (add then multiply).

    Prerequisites:
        square_root.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "error_propagation"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["square_root"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "compute propagated uncertainty"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an error propagation problem.

        Creates measured values with uncertainties and asks for the
        propagated uncertainty of a derived quantity.

        Args:
            difficulty: Controls operation type.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        a = round(self._rng.uniform(5.0, 50.0), 2)
        da = round(self._rng.uniform(0.01, a * 0.1), 2)
        b = round(self._rng.uniform(5.0, 50.0), 2)
        db = round(self._rng.uniform(0.01, b * 0.1), 2)

        if difficulty <= 3:
            # f = a + b
            f_val = round(a + b, 4)
            df = round(math.sqrt(da ** 2 + db ** 2), 4)
            desc = (
                f"a = {a} +/- {da}, b = {b} +/- {db}; "
                f"f = a + b; propagated uncertainty df?"
            )
            return desc, {
                "mode": "add", "a": a, "da": da, "b": b, "db": db,
                "f": f_val, "df": df,
            }
        elif difficulty <= 6:
            # f = a * b
            f_val = round(a * b, 4)
            rel_a = round(da / a, 4)
            rel_b = round(db / b, 4)
            rel_f = round(math.sqrt(rel_a ** 2 + rel_b ** 2), 4)
            df = round(f_val * rel_f, 4)
            desc = (
                f"a = {a} +/- {da}, b = {b} +/- {db}; "
                f"f = a * b; propagated uncertainty df?"
            )
            return desc, {
                "mode": "mul", "a": a, "da": da, "b": b, "db": db,
                "f": f_val, "rel_a": rel_a, "rel_b": rel_b,
                "rel_f": rel_f, "df": df,
            }
        else:
            # f = (a + b) * c, c given
            c = round(self._rng.uniform(2.0, 10.0), 2)
            dc = round(self._rng.uniform(0.01, c * 0.05), 2)
            s = round(a + b, 4)
            ds = round(math.sqrt(da ** 2 + db ** 2), 4)
            f_val = round(s * c, 4)
            rel_s = round(ds / s, 4)
            rel_c = round(dc / c, 4)
            rel_f = round(math.sqrt(rel_s ** 2 + rel_c ** 2), 4)
            df = round(f_val * rel_f, 4)
            desc = (
                f"a = {a}+/-{da}, b = {b}+/-{db}, "
                f"c = {c}+/-{dc}; f = (a+b)*c; df?"
            )
            return desc, {
                "mode": "mixed", "a": a, "da": da, "b": b, "db": db,
                "c": c, "dc": dc, "s": s, "ds": ds,
                "f": f_val, "rel_s": rel_s, "rel_c": rel_c,
                "rel_f": rel_f, "df": df,
            }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        if sd["mode"] == "add":
            return [
                "f = a + b: df = sqrt(da^2 + db^2)",
                f"df = sqrt({sd['da']}^2 + {sd['db']}^2) = {sd['df']}",
                f"f = {sd['f']} +/- {sd['df']}",
            ]
        elif sd["mode"] == "mul":
            return [
                "f = a*b: df/f = sqrt((da/a)^2 + (db/b)^2)",
                f"da/a = {sd['rel_a']}, db/b = {sd['rel_b']}",
                f"df/f = sqrt({sd['rel_a']}^2 + {sd['rel_b']}^2) = {sd['rel_f']}",
                f"df = {sd['f']} * {sd['rel_f']} = {sd['df']}",
            ]
        else:
            return [
                f"s = a+b = {sd['s']}, ds = sqrt({sd['da']}^2+{sd['db']}^2) = {sd['ds']}",
                f"f = s*c = {sd['s']}*{sd['c']} = {sd['f']}",
                f"rel_s = {sd['rel_s']}, rel_c = {sd['rel_c']}",
                f"df/f = sqrt({sd['rel_s']}^2+{sd['rel_c']}^2) = {sd['rel_f']}",
                f"df = {sd['f']}*{sd['rel_f']} = {sd['df']}",
            ]

    def _create_answer(self, sd: dict) -> str:
        """Return the propagated uncertainty.

        Args:
            sd: Solution data.

        Returns:
            Uncertainty as a string.
        """
        return f"df = {sd['df']}"


# ===================================================================
# 2. Dimensional analysis compute  (tier 4)
# ===================================================================

@register
class DimensionalAnalysisComputeGenerator(StepGenerator):
    """Convert compound units by chaining conversion factors.

    Converts between compound unit systems (e.g. kg*m/s^2 to g*cm/s^2)
    by applying successive conversion factors.

    Difficulty scaling:
        Difficulty 1-3: single unit conversion (e.g. kg to g).
        Difficulty 4-6: two-factor conversion (e.g. kg*m to g*cm).
        Difficulty 7-8: three-factor conversion (e.g. kg*m/s^2 to g*cm/s^2).

    Prerequisites:
        multiplication.
    """

    _CONVERSIONS: list[dict] = [
        {"from": "kg", "to": "g", "factor": 1000.0},
        {"from": "m", "to": "cm", "factor": 100.0},
        {"from": "km", "to": "m", "factor": 1000.0},
        {"from": "hr", "to": "s", "factor": 3600.0},
        {"from": "min", "to": "s", "factor": 60.0},
        {"from": "L", "to": "mL", "factor": 1000.0},
        {"from": "m", "to": "mm", "factor": 1000.0},
        {"from": "kg", "to": "mg", "factor": 1e6},
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "dimensional_analysis_compute"

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
        return "convert compound units using dimensional analysis"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a dimensional analysis conversion problem.

        Chains conversion factors to convert a value from one compound
        unit system to another.

        Args:
            difficulty: Controls number of conversion factors.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            n_factors = 1
        elif difficulty <= 6:
            n_factors = 2
        else:
            n_factors = 3

        chosen = self._rng.sample(self._CONVERSIONS, n_factors)
        value = round(self._rng.uniform(0.5, 100.0), 2)
        result = value
        chain_steps: list[str] = []
        from_units: list[str] = []
        to_units: list[str] = []

        for conv in chosen:
            from_units.append(conv["from"])
            to_units.append(conv["to"])
            result = round(result * conv["factor"], 4)
            chain_steps.append(
                f"1 {conv['from']} = {conv['factor']} {conv['to']}"
            )

        from_str = "*".join(from_units)
        to_str = "*".join(to_units)
        desc = f"convert {value} {from_str} to {to_str}"
        return desc, {
            "value": value, "result": result,
            "chain_steps": chain_steps,
            "from_str": from_str, "to_str": to_str,
            "factors": chosen,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        steps = list(sd["chain_steps"])
        steps.append(f"{sd['value']} {sd['from_str']} = {sd['result']} {sd['to_str']}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the converted value.

        Args:
            sd: Solution data.

        Returns:
            Converted value with units.
        """
        return f"{sd['result']} {sd['to_str']}"


# ===================================================================
# 3. Significant figures calculation  (tier 3)
# ===================================================================

@register
class SignificantFiguresCalcGenerator(StepGenerator):
    """Compute a result and round to the correct number of sig figs.

    For multiplication/division: result takes fewest significant figures
    of any operand. For addition/subtraction: result takes fewest
    decimal places of any operand.

    Difficulty scaling:
        Difficulty 1-3: addition/subtraction, 2 operands.
        Difficulty 4-6: multiplication/division, 2 operands.
        Difficulty 7-8: mixed operations, 3 operands.

    Prerequisites:
        multiplication.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "significant_figures_calc"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 3

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
        return "compute result with correct significant figures"

    def _count_sig_figs(self, value_str: str) -> int:
        """Count significant figures in a numeric string.

        Args:
            value_str: String representation of a number.

        Returns:
            Number of significant figures.
        """
        s = value_str.strip().lstrip("-")
        if "." in s:
            s = s.lstrip("0") or "0"
            if s.startswith("."):
                return len(s.replace(".", "").lstrip("0"))
            return len(s.replace(".", ""))
        s = s.lstrip("0") or "0"
        return len(s.rstrip("0"))

    def _decimal_places(self, value_str: str) -> int:
        """Count decimal places in a numeric string.

        Args:
            value_str: String representation of a number.

        Returns:
            Number of decimal places (0 if no decimal point).
        """
        if "." in value_str:
            return len(value_str.split(".")[-1])
        return 0

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a significant figures calculation problem.

        Creates operands and an operation, then determines the correct
        number of significant figures for the result.

        Args:
            difficulty: Controls operation type.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            # Addition with varying decimal places
            dp1 = self._rng.randint(1, 3)
            dp2 = self._rng.randint(1, 3)
            a = round(self._rng.uniform(1.0, 100.0), dp1)
            b = round(self._rng.uniform(1.0, 100.0), dp2)
            a_str = f"{a:.{dp1}f}"
            b_str = f"{b:.{dp2}f}"
            raw = a + b
            min_dp = min(dp1, dp2)
            result = round(raw, min_dp)
            result_str = f"{result:.{min_dp}f}"
            desc = f"{a_str} + {b_str}; answer with correct sig figs"
            return desc, {
                "mode": "add", "a_str": a_str, "b_str": b_str,
                "raw": round(raw, 4), "min_dp": min_dp,
                "result": result_str,
            }
        elif difficulty <= 6:
            # Multiplication with varying sig figs
            sf1 = self._rng.randint(2, 4)
            sf2 = self._rng.randint(2, 4)
            a = round(self._rng.uniform(1.0, 50.0), sf1 - 1)
            b = round(self._rng.uniform(1.0, 50.0), sf2 - 1)
            a_str = f"{a:.{sf1 - 1}f}"
            b_str = f"{b:.{sf2 - 1}f}"
            raw = a * b
            min_sf = min(sf1, sf2)
            # Round to min_sf significant figures
            if raw != 0:
                magnitude = math.floor(math.log10(abs(raw)))
                result = round(raw, min_sf - 1 - magnitude)
            else:
                result = 0.0
            desc = f"{a_str} * {b_str}; answer with correct sig figs"
            return desc, {
                "mode": "mul", "a_str": a_str, "b_str": b_str,
                "sf_a": sf1, "sf_b": sf2, "min_sf": min_sf,
                "raw": round(raw, 4), "result": str(round(result, 4)),
            }
        else:
            # Division
            sf1 = self._rng.randint(2, 4)
            sf2 = self._rng.randint(2, 4)
            a = round(self._rng.uniform(10.0, 200.0), sf1 - 1)
            b = round(self._rng.uniform(1.0, 20.0), sf2 - 1)
            a_str = f"{a:.{sf1 - 1}f}"
            b_str = f"{b:.{sf2 - 1}f}"
            raw = a / b
            min_sf = min(sf1, sf2)
            if raw != 0:
                magnitude = math.floor(math.log10(abs(raw)))
                result = round(raw, min_sf - 1 - magnitude)
            else:
                result = 0.0
            desc = f"{a_str} / {b_str}; answer with correct sig figs"
            return desc, {
                "mode": "div", "a_str": a_str, "b_str": b_str,
                "sf_a": sf1, "sf_b": sf2, "min_sf": min_sf,
                "raw": round(raw, 4), "result": str(round(result, 4)),
            }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        if sd["mode"] == "add":
            return [
                f"addition: fewest decimal places rule",
                f"{sd['a_str']} has {self._decimal_places(sd['a_str'])} dp, "
                f"{sd['b_str']} has {self._decimal_places(sd['b_str'])} dp",
                f"raw = {sd['raw']}, round to {sd['min_dp']} dp",
            ]
        else:
            op = "multiply" if sd["mode"] == "mul" else "divide"
            return [
                f"{op}: fewest sig figs rule",
                f"{sd['a_str']} has {sd['sf_a']} sf, "
                f"{sd['b_str']} has {sd['sf_b']} sf",
                f"raw = {sd['raw']}, round to {sd['min_sf']} sf",
            ]

    def _create_answer(self, sd: dict) -> str:
        """Return the correctly rounded result.

        Args:
            sd: Solution data.

        Returns:
            Result string.
        """
        return sd["result"]


# ===================================================================
# 4. Calibration curve  (tier 5)
# ===================================================================

@register
class CalibrationCurveGenerator(StepGenerator):
    """Compute linear calibration parameters by least squares.

    Given calibration standards (x_i, y_i), compute slope m and
    intercept b by ordinary least squares. Then predict x from a
    measured y using x = (y - b) / m.

    Difficulty scaling:
        Difficulty 1-3: 3 data points, compute m and b.
        Difficulty 4-6: 4 data points, compute m, b, and predict x.
        Difficulty 7-8: 5 data points with prediction.

    Prerequisites:
        division.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "calibration_curve"

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
            Short task description string.
        """
        return "compute linear calibration curve and predict"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a calibration curve problem.

        Creates standard data points along a noisy linear relationship,
        computes OLS slope and intercept, and optionally predicts x.

        Args:
            difficulty: Controls number of points and prediction.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            n = 3
            predict = False
        elif difficulty <= 6:
            n = 4
            predict = True
        else:
            n = 5
            predict = True

        true_m = round(self._rng.uniform(0.5, 5.0), 2)
        true_b = round(self._rng.uniform(0.0, 10.0), 2)

        xs = [round(self._rng.uniform(1.0, 20.0), 1) for _ in range(n)]
        ys = [round(true_m * x + true_b + self._rng.uniform(-0.5, 0.5), 2)
              for x in xs]

        # OLS: m = (n*sum(xy) - sum(x)*sum(y)) / (n*sum(x^2) - sum(x)^2)
        sum_x = sum(xs)
        sum_y = sum(ys)
        sum_xy = sum(x * y for x, y in zip(xs, ys))
        sum_x2 = sum(x ** 2 for x in xs)

        denom = n * sum_x2 - sum_x ** 2
        m = round((n * sum_xy - sum_x * sum_y) / denom, 4)
        b = round((sum_y - m * sum_x) / n, 4)

        data_str = ", ".join(f"({x}, {y})" for x, y in zip(xs, ys))
        desc = f"standards: {data_str}; find y = mx + b"

        sd: dict = {
            "xs": xs, "ys": ys, "n": n,
            "sum_x": round(sum_x, 4), "sum_y": round(sum_y, 4),
            "sum_xy": round(sum_xy, 4), "sum_x2": round(sum_x2, 4),
            "m": m, "b": b, "predict": predict,
        }

        if predict:
            y_meas = round(self._rng.uniform(min(ys), max(ys)), 2)
            x_pred = round((y_meas - b) / m, 4)
            desc += f"; predict x for y = {y_meas}"
            sd["y_meas"] = y_meas
            sd["x_pred"] = x_pred

        return desc, sd

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        steps = [
            f"n = {sd['n']}, sum_x = {sd['sum_x']}, sum_y = {sd['sum_y']}",
            f"sum_xy = {sd['sum_xy']}, sum_x2 = {sd['sum_x2']}",
            f"m = (n*sum_xy - sum_x*sum_y)/(n*sum_x2 - sum_x^2) = {sd['m']}",
            f"b = (sum_y - m*sum_x)/n = {sd['b']}",
        ]
        if sd["predict"]:
            steps.append(
                f"x = (y - b)/m = ({sd['y_meas']} - {sd['b']})/{sd['m']} = {sd['x_pred']}"
            )
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the calibration parameters and prediction.

        Args:
            sd: Solution data.

        Returns:
            Result string.
        """
        ans = f"m = {sd['m']}, b = {sd['b']}"
        if sd["predict"]:
            ans += f", x_pred = {sd['x_pred']}"
        return ans


# ===================================================================
# 5. Accuracy and precision  (tier 4)
# ===================================================================

@register
class AccuracyPrecisionGenerator(StepGenerator):
    """Compute accuracy and precision from measurements.

    Accuracy = |mean - true| / true * 100 (percent error).
    Precision = standard deviation of measurements.
    Classify as: high accuracy + high precision, high accuracy + low
    precision, low accuracy + high precision, low accuracy + low
    precision.

    Difficulty scaling:
        Difficulty 1-3: 3 measurements, compute accuracy only.
        Difficulty 4-6: 5 measurements, compute accuracy and precision.
        Difficulty 7-8: 7 measurements, compute both and classify.

    Prerequisites:
        division.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "accuracy_precision"

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
        return "compute accuracy and precision of measurements"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an accuracy/precision problem.

        Creates a set of measurements with a known true value, then
        computes percent error (accuracy) and standard deviation
        (precision).

        Args:
            difficulty: Controls number of measurements and outputs.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            n = 3
            classify = False
        elif difficulty <= 6:
            n = 5
            classify = False
        else:
            n = 7
            classify = True

        true_val = round(self._rng.uniform(10.0, 100.0), 2)
        bias = round(self._rng.uniform(-5.0, 5.0), 2)
        spread = round(self._rng.uniform(0.1, 3.0), 2)
        measurements = [
            round(true_val + bias + self._rng.gauss(0, spread), 2)
            for _ in range(n)
        ]

        mean_val = round(sum(measurements) / n, 4)
        accuracy = round(abs(mean_val - true_val) / true_val * 100, 4)
        variance = sum((x - mean_val) ** 2 for x in measurements) / (n - 1)
        std_dev = round(math.sqrt(variance), 4)

        classification = ""
        if classify:
            high_acc = accuracy < 5.0
            high_prec = std_dev < 1.0
            if high_acc and high_prec:
                classification = "high accuracy, high precision"
            elif high_acc:
                classification = "high accuracy, low precision"
            elif high_prec:
                classification = "low accuracy, high precision"
            else:
                classification = "low accuracy, low precision"

        meas_str = ", ".join(str(m) for m in measurements)
        desc = f"measurements: [{meas_str}], true value = {true_val}"
        return desc, {
            "measurements": measurements, "true_val": true_val,
            "n": n, "mean": mean_val, "accuracy": accuracy,
            "std_dev": std_dev, "classify": classify,
            "classification": classification,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        steps = [
            f"mean = sum/n = {sd['mean']}",
            f"accuracy = |{sd['mean']} - {sd['true_val']}|/{sd['true_val']}*100 = {sd['accuracy']}%",
            f"std_dev = {sd['std_dev']}",
        ]
        if sd["classify"]:
            steps.append(f"classification: {sd['classification']}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return accuracy, precision, and optional classification.

        Args:
            sd: Solution data.

        Returns:
            Result string.
        """
        ans = f"accuracy = {sd['accuracy']}%, precision(std) = {sd['std_dev']}"
        if sd["classify"]:
            ans += f", {sd['classification']}"
        return ans


# ===================================================================
# 6. Logarithmic scales  (tier 4)
# ===================================================================

@register
class LogarithmicScalesGenerator(StepGenerator):
    """Convert between linear and logarithmic scales.

    Supports decibels (dB = 10*log10(P2/P1) for power, or
    dB = 20*log10(V2/V1) for voltage/amplitude) and pH
    (pH = -log10([H+])).

    Difficulty scaling:
        Difficulty 1-3: power dB conversion.
        Difficulty 4-6: pH computation.
        Difficulty 7-8: voltage dB or inverse (linear from log).

    Prerequisites:
        logarithm.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "logarithmic_scales"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["logarithm"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "convert between linear and logarithmic scales"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a logarithmic scale conversion problem.

        Creates problems involving decibel or pH conversions in
        both forward and inverse directions.

        Args:
            difficulty: Controls scale type and direction.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            # Power dB
            p1 = round(self._rng.uniform(0.001, 10.0), 3)
            p2 = round(self._rng.uniform(0.001, 10.0), 3)
            ratio = round(p2 / p1, 4)
            db = round(10 * math.log10(ratio), 4)
            desc = f"P1 = {p1} W, P2 = {p2} W; compute dB"
            return desc, {
                "mode": "power_db", "p1": p1, "p2": p2,
                "ratio": ratio, "db": db,
            }
        elif difficulty <= 6:
            # pH
            exponent = self._rng.randint(-14, -1)
            h_conc = round(10.0 ** exponent, 4)
            ph = round(-math.log10(h_conc), 4)
            desc = f"[H+] = {h_conc} M; compute pH"
            return desc, {
                "mode": "ph", "h_conc": h_conc, "ph": ph,
            }
        else:
            # Voltage dB or inverse
            if self._rng.random() < 0.5:
                v1 = round(self._rng.uniform(0.01, 5.0), 3)
                v2 = round(self._rng.uniform(0.01, 5.0), 3)
                ratio = round(v2 / v1, 4)
                db = round(20 * math.log10(ratio), 4)
                desc = f"V1 = {v1} V, V2 = {v2} V; voltage dB?"
                return desc, {
                    "mode": "voltage_db", "v1": v1, "v2": v2,
                    "ratio": ratio, "db": db,
                }
            else:
                db_val = round(self._rng.uniform(-20.0, 40.0), 1)
                ratio = round(10.0 ** (db_val / 10.0), 4)
                desc = f"gain = {db_val} dB (power); find P2/P1"
                return desc, {
                    "mode": "inverse_db", "db": db_val, "ratio": ratio,
                }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        if sd["mode"] == "power_db":
            return [
                "dB = 10 * log10(P2/P1)",
                f"P2/P1 = {sd['p2']}/{sd['p1']} = {sd['ratio']}",
                f"dB = 10 * log10({sd['ratio']}) = {sd['db']}",
            ]
        elif sd["mode"] == "ph":
            return [
                "pH = -log10([H+])",
                f"[H+] = {sd['h_conc']}",
                f"pH = -log10({sd['h_conc']}) = {sd['ph']}",
            ]
        elif sd["mode"] == "voltage_db":
            return [
                "dB = 20 * log10(V2/V1)",
                f"V2/V1 = {sd['v2']}/{sd['v1']} = {sd['ratio']}",
                f"dB = 20 * log10({sd['ratio']}) = {sd['db']}",
            ]
        else:
            return [
                "P2/P1 = 10^(dB/10)",
                f"P2/P1 = 10^({sd['db']}/10) = {sd['ratio']}",
            ]

    def _create_answer(self, sd: dict) -> str:
        """Return the conversion result.

        Args:
            sd: Solution data.

        Returns:
            Result string.
        """
        if sd["mode"] == "power_db":
            return f"{sd['db']} dB"
        elif sd["mode"] == "ph":
            return f"pH = {sd['ph']}"
        elif sd["mode"] == "voltage_db":
            return f"{sd['db']} dB"
        else:
            return f"P2/P1 = {sd['ratio']}"
