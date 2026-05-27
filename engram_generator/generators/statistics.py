"""Statistics and probability generators — descriptive statistics and stochastic reasoning.

Spans tiers 2-5. Statistics generators cover mean, median, mode, variance,
standard deviation, linear regression, correlation, and z-score. Probability
generators cover basic probability, conditional probability, binomial
distribution, expected value, and Markov chains.
"""
import math
from fractions import Fraction

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


class FractionFormatter:
    """Formats fractions as LaTeX strings with simplification.

    Converts a Fraction or numerator/denominator pair into a
    human-readable representation: integers when the denominator is 1,
    LaTeX \\frac notation otherwise.

    Example:
        >>> f = FractionFormatter()
        >>> f.format(Fraction(3, 4))
        '\\\\frac{3}{4}'
        >>> f.format(Fraction(6, 1))
        '6'
    """

    def format(self, frac: Fraction) -> str:
        """Format a Fraction as LaTeX.

        Args:
            frac: Fraction instance.

        Returns:
            LaTeX string, integer if denominator is 1.
        """
        if frac.denominator == 1:
            return str(frac.numerator)
        num = frac.numerator
        den = frac.denominator
        return f"\\frac{{{num}}}{{{den}}}"

    def format_decimal(self, value: float, places: int = 4) -> str:
        """Format a float rounded to given decimal places.

        Args:
            value: Floating point number.
            places: Number of decimal places.

        Returns:
            Rounded string representation.
        """
        return str(round(value, places))


class DatasetBuilder:
    """Builds random integer datasets with difficulty-scaled size and range.

    Provides dataset generation for statistics generators with
    controllable list length and value range based on difficulty.

    Example:
        >>> import random
        >>> rng = random.Random(42)
        >>> b = DatasetBuilder(rng)
        >>> data = b.build(3, 1, 20)
        >>> len(data)
        3
    """

    def __init__(self, rng: "random.Random") -> None:
        """Initialise with a random number generator.

        Args:
            rng: Seeded random instance.
        """
        self._rng = rng

    def build(self, length: int, lower: int, upper: int) -> list[int]:
        """Generate a random integer dataset.

        Args:
            length: Number of data points.
            lower: Minimum value (inclusive).
            upper: Maximum value (inclusive).

        Returns:
            List of random integers.
        """
        return [self._rng.randint(lower, upper) for _ in range(length)]

    def length_for_difficulty(self, difficulty: int) -> int:
        """Map difficulty to dataset length.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Dataset length from 3 to 10.
        """
        return min(3 + difficulty, 10)

    def range_for_difficulty(self, difficulty: int) -> tuple[int, int]:
        """Map difficulty to value range.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (lower, upper) bounds.
        """
        if difficulty <= 2:
            return 1, 10
        if difficulty <= 4:
            return 1, 50
        if difficulty <= 6:
            return 1, 100
        return 1, 200


class TransitionMatrixBuilder:
    """Builds stochastic transition matrices for Markov chain problems.

    Constructs square matrices where each row sums to 1 using
    integer-friendly fractions to keep arithmetic tractable.

    Example:
        >>> import random
        >>> rng = random.Random(42)
        >>> b = TransitionMatrixBuilder(rng)
        >>> m = b.build(2)
        >>> all(sum(row) == Fraction(1) for row in m)
        True
    """

    def __init__(self, rng: "random.Random") -> None:
        """Initialise with a random number generator.

        Args:
            rng: Seeded random instance.
        """
        self._rng = rng

    def build(self, size: int) -> list[list[Fraction]]:
        """Build a stochastic transition matrix.

        Args:
            size: Number of states (matrix dimension).

        Returns:
            Square matrix of Fractions where each row sums to 1.
        """
        return [self._build_row(size) for _ in range(size)]

    def _build_row(self, size: int) -> list[Fraction]:
        """Build one row of transition probabilities summing to 1.

        Uses random integer weights normalised to fractions.

        Args:
            size: Number of entries in the row.

        Returns:
            List of Fractions summing to 1.
        """
        weights = [self._rng.randint(1, 5) for _ in range(size)]
        total = sum(weights)
        return [Fraction(w, total) for w in weights]


@register
class MeanGenerator(StepGenerator):
    """Compute the arithmetic mean of a dataset.

    Generates a list of integers and shows the summation step
    followed by division by the count to produce the mean.

    Input format:
        ``compute mean of 5 numbers``

    Target format:
        ``\\bar{x}(4,7,2,9,3) <step> 4+7+2+9+3=25 <step> 25/5=5 <step> 5``

    Difficulty scaling:
        Dataset length is difficulty + 2 (3 to 10 elements).
        Value range scales from [1,10] at d1 to [1,200] at d8.

    Prerequisites:
        addition, division.

    Example:
        >>> gen = MeanGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'mean'
    """

    def __init__(self, **kwargs) -> None:
        """Initialise with dataset builder and fraction formatter.

        Args:
            **kwargs: Passed to parent constructor.
        """
        super().__init__(**kwargs)
        self._builder = DatasetBuilder(self._rng)
        self._fmt = FractionFormatter()

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "mean"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 2

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["addition", "division"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls dataset size.

        Returns:
            Natural language description.
        """
        n = self._builder.length_for_difficulty(difficulty)
        return f"compute mean of {n} numbers"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a dataset and compute its mean.

        Args:
            difficulty: Controls dataset size and value range.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        n = self._builder.length_for_difficulty(difficulty)
        lo, hi = self._builder.range_for_difficulty(difficulty)
        data = self._builder.build(n, lo, hi)
        total = sum(data)
        mean = Fraction(total, n)
        label = ",".join(str(x) for x in data)
        return (
            f"\\bar{{x}}({label})",
            {"data": data, "total": total, "n": n, "mean": mean},
        )

    def _create_steps(self, data: dict) -> list[str]:
        """Generate summation and division steps.

        Args:
            data: Solution data with dataset and computed values.

        Returns:
            Steps showing the sum and the division.
        """
        nums = data["data"]
        total = data["total"]
        n = data["n"]
        mean = data["mean"]
        sum_str = "+".join(str(x) for x in nums)
        return [
            f"{sum_str}={total}",
            f"{total}/{n}={self._fmt.format(mean)}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the mean as a string.

        Args:
            data: Solution data.

        Returns:
            Formatted mean value.
        """
        return self._fmt.format(data["mean"])


@register
class MedianGenerator(StepGenerator):
    """Find the median of a dataset.

    Generates a list of integers, shows the sorted list, and
    extracts the middle value (or average of two middle values).

    Input format:
        ``find median of 5 numbers``

    Target format:
        ``\\text{median}(4,7,2,9,3) <step> sorted: 2,3,4,7,9 <step>
        middle=4 <step> 4``

    Difficulty scaling:
        Dataset length is difficulty + 2 (3 to 10 elements).
        Value range scales with difficulty.

    Prerequisites:
        sorting.

    Example:
        >>> gen = MedianGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'median'
    """

    def __init__(self, **kwargs) -> None:
        """Initialise with dataset builder and fraction formatter.

        Args:
            **kwargs: Passed to parent constructor.
        """
        super().__init__(**kwargs)
        self._builder = DatasetBuilder(self._rng)
        self._fmt = FractionFormatter()

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "median"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 2

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["sorting"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls dataset size.

        Returns:
            Natural language description.
        """
        n = self._builder.length_for_difficulty(difficulty)
        return f"find median of {n} numbers"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a dataset and compute its median.

        Args:
            difficulty: Controls dataset size and value range.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        n = self._builder.length_for_difficulty(difficulty)
        lo, hi = self._builder.range_for_difficulty(difficulty)
        data = self._builder.build(n, lo, hi)
        sorted_data = sorted(data)
        median = self._compute_median(sorted_data)
        label = ",".join(str(x) for x in data)
        return (
            f"\\text{{median}}({label})",
            {"data": data, "sorted": sorted_data, "n": n, "median": median},
        )

    def _compute_median(self, sorted_data: list[int]) -> Fraction:
        """Compute the median of a sorted list.

        Args:
            sorted_data: Sorted integer list.

        Returns:
            Median as a Fraction.
        """
        n = len(sorted_data)
        mid = n // 2
        if n % 2 == 1:
            return Fraction(sorted_data[mid])
        return Fraction(sorted_data[mid - 1] + sorted_data[mid], 2)

    def _create_steps(self, data: dict) -> list[str]:
        """Generate sorting and extraction steps.

        Args:
            data: Solution data with sorted list and median.

        Returns:
            Steps showing the sorted list and middle extraction.
        """
        sorted_str = ",".join(str(x) for x in data["sorted"])
        n = data["n"]
        steps = [f"sorted: {sorted_str}"]
        steps.append(self._middle_step(data))
        return steps

    def _middle_step(self, data: dict) -> str:
        """Format the middle-value extraction step.

        Args:
            data: Solution data with sorted list and count.

        Returns:
            Step string showing the median extraction.
        """
        n = data["n"]
        sorted_data = data["sorted"]
        mid = n // 2
        if n % 2 == 1:
            return f"middle={sorted_data[mid]}"
        a = sorted_data[mid - 1]
        b = sorted_data[mid]
        median = self._fmt.format(data["median"])
        return f"middle=({a}+{b})/2={median}"

    def _create_answer(self, data: dict) -> str:
        """Return the median as a string.

        Args:
            data: Solution data.

        Returns:
            Formatted median value.
        """
        return self._fmt.format(data["median"])


@register
class ModeGenerator(StepGenerator):
    """Find the most frequent value in a dataset.

    Generates a list of integers with at least one repeated value,
    shows the frequency count for each value, and identifies the mode.

    Input format:
        ``find mode of 6 numbers``

    Target format:
        ``\\text{mode}(3,7,3,5,7,3) <step> 3:3, 5:1, 7:2 <step> 3``

    Difficulty scaling:
        Dataset length is difficulty + 2 (3 to 10 elements).
        Value range is deliberately narrower than dataset length
        to encourage repeats.

    Prerequisites:
        sorting.

    Example:
        >>> gen = ModeGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'mode'
    """

    def __init__(self, **kwargs) -> None:
        """Initialise with dataset builder.

        Args:
            **kwargs: Passed to parent constructor.
        """
        super().__init__(**kwargs)
        self._builder = DatasetBuilder(self._rng)

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "mode"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 2

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["sorting"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls dataset size.

        Returns:
            Natural language description.
        """
        n = self._builder.length_for_difficulty(difficulty)
        return f"find mode of {n} numbers"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a dataset with guaranteed repeats.

        Uses a narrower value range than the dataset length to
        force repeated values, then computes the frequency table.

        Args:
            difficulty: Controls dataset size.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        n = self._builder.length_for_difficulty(difficulty)
        upper = max(3, n - 1)
        data = self._builder.build(n, 1, upper)
        freq = self._frequency_table(data)
        mode_val = max(freq, key=lambda k: freq[k])
        label = ",".join(str(x) for x in data)
        return (
            f"\\text{{mode}}({label})",
            {"data": data, "freq": freq, "mode": mode_val},
        )

    def _frequency_table(self, data: list[int]) -> dict[int, int]:
        """Build a frequency table from a dataset.

        Args:
            data: List of integers.

        Returns:
            Dict mapping each value to its frequency.
        """
        freq: dict[int, int] = {}
        for x in data:
            freq[x] = freq.get(x, 0) + 1
        return dict(sorted(freq.items()))

    def _create_steps(self, data: dict) -> list[str]:
        """Generate frequency counting steps.

        Args:
            data: Solution data with frequency table.

        Returns:
            Steps showing each value's count.
        """
        freq = data["freq"]
        counts = ", ".join(
            f"{k}:{v}" for k, v in freq.items()
        )
        return [counts]

    def _create_answer(self, data: dict) -> str:
        """Return the mode as a string.

        Args:
            data: Solution data.

        Returns:
            String representation of the mode.
        """
        return str(data["mode"])


@register
class VarianceGenerator(StepGenerator):
    """Compute the population variance of a dataset.

    Generates a dataset, computes the mean, shows each squared
    deviation, sums them, and divides by n to get the variance.

    Input format:
        ``compute variance of 5 numbers``

    Target format:
        ``\\sigma^2(4,7,2,9,3) <step> \\bar{x}=25/5=5 <step>
        (4-5)^2=1 <step> (7-5)^2=4 <step> (2-5)^2=9 <step>
        (9-5)^2=16 <step> (3-5)^2=4 <step> (1+4+9+16+4)/5=34/5 <step>
        \\frac{34}{5}``

    Difficulty scaling:
        Dataset length is difficulty + 2 (3 to 10 elements).
        Value range scales with difficulty.

    Prerequisites:
        mean, exponentiation.

    Example:
        >>> gen = VarianceGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'variance'
    """

    def __init__(self, **kwargs) -> None:
        """Initialise with dataset builder and fraction formatter.

        Args:
            **kwargs: Passed to parent constructor.
        """
        super().__init__(**kwargs)
        self._builder = DatasetBuilder(self._rng)
        self._fmt = FractionFormatter()

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "variance"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 3

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["mean", "exponentiation"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls dataset size.

        Returns:
            Natural language description.
        """
        n = self._builder.length_for_difficulty(difficulty)
        return f"compute variance of {n} numbers"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a dataset and compute its variance.

        Args:
            difficulty: Controls dataset size and value range.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        n = self._builder.length_for_difficulty(difficulty)
        lo, hi = self._builder.range_for_difficulty(difficulty)
        data = self._builder.build(n, lo, hi)
        total = sum(data)
        mean = Fraction(total, n)
        sq_devs = [self._squared_deviation(x, mean) for x in data]
        variance = Fraction(sum(sq_devs), n)
        label = ",".join(str(x) for x in data)
        return (
            f"\\sigma^2({label})",
            {"data": data, "n": n, "total": total,
             "mean": mean, "sq_devs": sq_devs, "variance": variance},
        )

    def _squared_deviation(self, x: int, mean: Fraction) -> Fraction:
        """Compute (x - mean)^2 as a Fraction.

        Args:
            x: Data point.
            mean: Dataset mean.

        Returns:
            Squared deviation as a Fraction.
        """
        dev = Fraction(x) - mean
        return dev * dev

    def _create_steps(self, data: dict) -> list[str]:
        """Generate mean, deviation, and summation steps.

        Args:
            data: Solution data with all computed values.

        Returns:
            Steps showing mean, each squared deviation, and final division.
        """
        steps: list[str] = []
        mean_str = self._fmt.format(data["mean"])
        steps.append(
            f"\\bar{{x}}={data['total']}/{data['n']}={mean_str}"
        )
        steps.extend(self._deviation_steps(data))
        steps.append(self._summation_step(data))
        return steps

    def _deviation_steps(self, data: dict) -> list[str]:
        """Generate one step per squared deviation.

        Args:
            data: Solution data with data points and mean.

        Returns:
            List of step strings.
        """
        mean = data["mean"]
        mean_str = self._fmt.format(mean)
        results: list[str] = []
        for x, sq in zip(data["data"], data["sq_devs"]):
            sq_str = self._fmt.format(sq)
            results.append(f"({x}-{mean_str})^2={sq_str}")
        return results

    def _summation_step(self, data: dict) -> str:
        """Format the final summation and division step.

        Args:
            data: Solution data.

        Returns:
            Step string showing sum of squared deviations divided by n.
        """
        sq_sum = sum(data["sq_devs"])
        sq_sum_str = self._fmt.format(sq_sum)
        n = data["n"]
        var_str = self._fmt.format(data["variance"])
        parts = "+".join(self._fmt.format(sq) for sq in data["sq_devs"])
        return f"({parts})/{n}={var_str}"

    def _create_answer(self, data: dict) -> str:
        """Return the variance as a string.

        Args:
            data: Solution data.

        Returns:
            Formatted variance value.
        """
        return self._fmt.format(data["variance"])


@register
class StdDevGenerator(StepGenerator):
    """Compute the population standard deviation of a dataset.

    Generates a dataset, computes variance first, then takes
    the square root to produce the standard deviation.

    Input format:
        ``compute standard deviation of 5 numbers``

    Target format:
        ``\\sigma(4,7,2,9,3) <step> \\bar{x}=5 <step> \\sigma^2=34/5
        <step> \\sigma=\\sqrt{34/5}=2.6077 <step> 2.6077``

    Difficulty scaling:
        Dataset length is difficulty + 2 (3 to 10 elements).
        Value range scales with difficulty.

    Prerequisites:
        variance.

    Example:
        >>> gen = StdDevGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'std_dev'
    """

    def __init__(self, **kwargs) -> None:
        """Initialise with dataset builder and fraction formatter.

        Args:
            **kwargs: Passed to parent constructor.
        """
        super().__init__(**kwargs)
        self._builder = DatasetBuilder(self._rng)
        self._fmt = FractionFormatter()

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "std_dev"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 3

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["variance"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls dataset size.

        Returns:
            Natural language description.
        """
        n = self._builder.length_for_difficulty(difficulty)
        return f"compute standard deviation of {n} numbers"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a dataset and compute its standard deviation.

        Args:
            difficulty: Controls dataset size and value range.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        n = self._builder.length_for_difficulty(difficulty)
        lo, hi = self._builder.range_for_difficulty(difficulty)
        data = self._builder.build(n, lo, hi)
        total = sum(data)
        mean = Fraction(total, n)
        sq_devs = [(Fraction(x) - mean) ** 2 for x in data]
        variance = Fraction(sum(sq_devs), n)
        std_dev = math.sqrt(float(variance))
        label = ",".join(str(x) for x in data)
        return (
            f"\\sigma({label})",
            {"data": data, "n": n, "total": total, "mean": mean,
             "variance": variance, "std_dev": std_dev},
        )

    def _create_steps(self, data: dict) -> list[str]:
        """Generate mean, variance, and square root steps.

        Args:
            data: Solution data with all computed values.

        Returns:
            Steps showing mean, variance, and final square root.
        """
        mean_str = self._fmt.format(data["mean"])
        var_str = self._fmt.format(data["variance"])
        std_str = self._fmt.format_decimal(data["std_dev"])
        return [
            f"\\bar{{x}}={data['total']}/{data['n']}={mean_str}",
            f"\\sigma^2={var_str}",
            f"\\sigma=\\sqrt{{{var_str}}}={std_str}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the standard deviation as a decimal string.

        Args:
            data: Solution data.

        Returns:
            Rounded decimal representation.
        """
        return self._fmt.format_decimal(data["std_dev"])


@register
class LinearRegressionGenerator(StepGenerator):
    """Fit a line y = mx + b to a set of (x, y) points.

    Computes slope m and intercept b using least-squares formulae:
    m = (n*sum(xy) - sum(x)*sum(y)) / (n*sum(x^2) - (sum(x))^2)
    b = (sum(y) - m*sum(x)) / n

    Input format:
        ``fit line to 4 points``

    Target format:
        ``\\text{linreg}((1,2),(2,4),(3,5),(4,7)) <step>
        \\sum x=10, \\sum y=18 <step> \\sum xy=49, \\sum x^2=30 <step>
        m=(4*49-10*18)/(4*30-100)=16/20=4/5 <step>
        b=(18-4/5*10)/4=\\frac{1}{2} <step> y=\\frac{4}{5}x+\\frac{1}{2}``

    Difficulty scaling:
        Number of points is difficulty + 2 (3 to 10 points).
        x-values are sequential integers; y-values are linear with noise.

    Prerequisites:
        mean, multiplication.

    Example:
        >>> gen = LinearRegressionGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'linear_regression'
    """

    def __init__(self, **kwargs) -> None:
        """Initialise with fraction formatter.

        Args:
            **kwargs: Passed to parent constructor.
        """
        super().__init__(**kwargs)
        self._fmt = FractionFormatter()

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "linear_regression"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["mean", "multiplication"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls number of points.

        Returns:
            Natural language description.
        """
        n = min(3 + difficulty, 10)
        return f"fit line to {n} points"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate data points and compute regression coefficients.

        Args:
            difficulty: Controls number of data points.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        n = min(3 + difficulty, 10)
        xs, ys = self._generate_points(n, difficulty)
        sums = self._compute_sums(xs, ys, n)
        label = ",".join(
            f"({xs[i]},{ys[i]})" for i in range(n)
        )
        return (
            f"\\text{{linreg}}({label})",
            {"xs": xs, "ys": ys, "n": n, **sums},
        )

    def _generate_points(self, n: int,
                         difficulty: int) -> tuple[list[int], list[int]]:
        """Generate x and y data with linear trend plus noise.

        Args:
            n: Number of data points.
            difficulty: Controls noise magnitude.

        Returns:
            Tuple of (x_values, y_values).
        """
        slope = self._rng.randint(1, 3 + difficulty)
        intercept = self._rng.randint(0, 5)
        xs = list(range(1, n + 1))
        noise_bound = max(1, difficulty)
        ys = [
            slope * x + intercept + self._rng.randint(-noise_bound, noise_bound)
            for x in xs
        ]
        return xs, ys

    def _compute_sums(self, xs: list[int], ys: list[int],
                      n: int) -> dict:
        """Compute all regression intermediate sums.

        Args:
            xs: x-values.
            ys: y-values.
            n: Number of points.

        Returns:
            Dict with sum_x, sum_y, sum_xy, sum_x2, slope, intercept.
        """
        sum_x = sum(xs)
        sum_y = sum(ys)
        sum_xy = sum(x * y for x, y in zip(xs, ys))
        sum_x2 = sum(x * x for x in xs)
        numer = Fraction(n * sum_xy - sum_x * sum_y)
        denom = Fraction(n * sum_x2 - sum_x * sum_x)
        slope = numer / denom
        intercept = (Fraction(sum_y) - slope * sum_x) / n
        return {
            "sum_x": sum_x, "sum_y": sum_y,
            "sum_xy": sum_xy, "sum_x2": sum_x2,
            "slope": slope, "intercept": intercept,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate summation, slope, and intercept steps.

        Args:
            data: Solution data with sums and coefficients.

        Returns:
            Steps showing each stage of the computation.
        """
        n = data["n"]
        slope_str = self._fmt.format(data["slope"])
        int_str = self._fmt.format(data["intercept"])
        numer = n * data["sum_xy"] - data["sum_x"] * data["sum_y"]
        denom = n * data["sum_x2"] - data["sum_x"] ** 2
        return [
            f"\\sum x={data['sum_x']}, \\sum y={data['sum_y']}",
            f"\\sum xy={data['sum_xy']}, \\sum x^2={data['sum_x2']}",
            f"m=({n}*{data['sum_xy']}-{data['sum_x']}*{data['sum_y']})"
            f"/({n}*{data['sum_x2']}-{data['sum_x']}^2)"
            f"={numer}/{denom}={slope_str}",
            f"b=({data['sum_y']}-{slope_str}*{data['sum_x']})/{n}={int_str}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the regression equation.

        Args:
            data: Solution data.

        Returns:
            String like 'y=\\frac{4}{5}x+\\frac{1}{2}'.
        """
        slope_str = self._fmt.format(data["slope"])
        int_str = self._fmt.format(data["intercept"])
        if data["intercept"] >= 0:
            return f"y={slope_str}x+{int_str}"
        return f"y={slope_str}x{int_str}"


@register
class CorrelationGenerator(StepGenerator):
    """Compute Pearson correlation coefficient r between two datasets.

    Generates paired (x, y) data and computes r using:
    r = (n*sum(xy) - sum(x)*sum(y)) /
        sqrt((n*sum(x^2) - sum(x)^2) * (n*sum(y^2) - sum(y)^2))

    Input format:
        ``compute correlation of 4 pairs``

    Target format:
        ``r((1,2),(2,5),(3,7),(4,8)) <step> \\sum x=10, \\sum y=22 <step>
        \\sum xy=67, \\sum x^2=30, \\sum y^2=142 <step>
        num=4*67-10*22=48 <step> den=\\sqrt{(120-100)*(568-484)}=\\sqrt{1680}
        <step> r=48/40.988=1.1706... <step> 0.9839``

    Difficulty scaling:
        Number of pairs is difficulty + 2 (3 to 10).
        Data is generated with a linear trend to produce non-trivial r.

    Prerequisites:
        std_dev, mean.

    Example:
        >>> gen = CorrelationGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'correlation'
    """

    def __init__(self, **kwargs) -> None:
        """Initialise with fraction formatter.

        Args:
            **kwargs: Passed to parent constructor.
        """
        super().__init__(**kwargs)
        self._fmt = FractionFormatter()

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "correlation"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["std_dev", "mean"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls number of data pairs.

        Returns:
            Natural language description.
        """
        n = min(3 + difficulty, 10)
        return f"compute correlation of {n} pairs"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate paired data and compute Pearson r.

        Args:
            difficulty: Controls number of pairs.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        n = min(3 + difficulty, 10)
        xs, ys = self._generate_pairs(n, difficulty)
        sums = self._compute_sums(xs, ys, n)
        label = ",".join(
            f"({xs[i]},{ys[i]})" for i in range(n)
        )
        return f"r({label})", {"xs": xs, "ys": ys, "n": n, **sums}

    def _generate_pairs(self, n: int,
                        difficulty: int) -> tuple[list[int], list[int]]:
        """Generate correlated x and y data.

        Args:
            n: Number of data pairs.
            difficulty: Controls noise level.

        Returns:
            Tuple of (x_values, y_values).
        """
        slope = self._rng.randint(1, 3)
        intercept = self._rng.randint(0, 5)
        xs = list(range(1, n + 1))
        noise = max(1, difficulty // 2)
        ys = [
            slope * x + intercept + self._rng.randint(-noise, noise)
            for x in xs
        ]
        return xs, ys

    def _compute_sums(self, xs: list[int], ys: list[int],
                      n: int) -> dict:
        """Compute all Pearson r intermediate values.

        Args:
            xs: x-values.
            ys: y-values.
            n: Number of pairs.

        Returns:
            Dict with sums, numerator, denominator, and r.
        """
        sum_x = sum(xs)
        sum_y = sum(ys)
        sum_xy = sum(x * y for x, y in zip(xs, ys))
        sum_x2 = sum(x * x for x in xs)
        sum_y2 = sum(y * y for y in ys)
        numer = n * sum_xy - sum_x * sum_y
        denom_sq = (n * sum_x2 - sum_x ** 2) * (n * sum_y2 - sum_y ** 2)
        denom = math.sqrt(max(1, denom_sq))
        r = numer / denom if denom > 0 else 0.0
        return {
            "sum_x": sum_x, "sum_y": sum_y,
            "sum_xy": sum_xy, "sum_x2": sum_x2, "sum_y2": sum_y2,
            "numer": numer, "denom_sq": denom_sq,
            "denom": denom, "r": r,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate summation and computation steps.

        Args:
            data: Solution data with all intermediate values.

        Returns:
            Steps showing sums, numerator, denominator, and r.
        """
        n = data["n"]
        r_str = self._fmt.format_decimal(data["r"])
        denom_str = self._fmt.format_decimal(data["denom"])
        return [
            f"\\sum x={data['sum_x']}, \\sum y={data['sum_y']}",
            f"\\sum xy={data['sum_xy']}, "
            f"\\sum x^2={data['sum_x2']}, "
            f"\\sum y^2={data['sum_y2']}",
            f"num={n}*{data['sum_xy']}-{data['sum_x']}*{data['sum_y']}"
            f"={data['numer']}",
            f"den=\\sqrt{{{data['denom_sq']}}}={denom_str}",
            f"r={data['numer']}/{denom_str}={r_str}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the correlation coefficient.

        Args:
            data: Solution data.

        Returns:
            Rounded decimal representation of r.
        """
        return self._fmt.format_decimal(data["r"])


@register
class ZScoreGenerator(StepGenerator):
    """Compute the z-score of a value given a dataset.

    Generates a dataset, computes its mean and standard deviation,
    then calculates z = (x - mean) / std_dev for a target value.

    Input format:
        ``compute z-score``

    Target format:
        ``z(7, \\bar{x}=5, \\sigma=2) <step> z=(7-5)/2 <step> z=1.0 <step> 1.0``

    Difficulty scaling:
        Dataset length is difficulty + 2. At low difficulty the
        target value is drawn from the dataset itself; at high
        difficulty it can be any value in the range.

    Prerequisites:
        mean, std_dev.

    Example:
        >>> gen = ZScoreGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'z_score'
    """

    def __init__(self, **kwargs) -> None:
        """Initialise with dataset builder and fraction formatter.

        Args:
            **kwargs: Passed to parent constructor.
        """
        super().__init__(**kwargs)
        self._builder = DatasetBuilder(self._rng)
        self._fmt = FractionFormatter()

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "z_score"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 3

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["mean", "std_dev"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls dataset size.

        Returns:
            Natural language description.
        """
        return "compute z-score"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a dataset, pick a target, and compute z-score.

        Args:
            difficulty: Controls dataset size and value range.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        n = self._builder.length_for_difficulty(difficulty)
        lo, hi = self._builder.range_for_difficulty(difficulty)
        data = self._builder.build(n, lo, hi)
        mean = sum(data) / n
        variance = sum((x - mean) ** 2 for x in data) / n
        std_dev = math.sqrt(variance) if variance > 0 else 1.0
        target = self._pick_target(data, lo, hi, difficulty)
        z = (target - mean) / std_dev if std_dev > 0 else 0.0
        mean_str = self._fmt.format_decimal(mean)
        std_str = self._fmt.format_decimal(std_dev)
        return (
            f"z({target}, \\bar{{x}}={mean_str}, \\sigma={std_str})",
            {"target": target, "mean": mean,
             "std_dev": std_dev, "z": z},
        )

    def _pick_target(self, data: list[int], lo: int,
                     hi: int, difficulty: int) -> int:
        """Choose a target value for z-score computation.

        At low difficulty picks from the dataset; at high difficulty
        picks any value in the range.

        Args:
            data: The dataset.
            lo: Lower bound of value range.
            hi: Upper bound of value range.
            difficulty: Difficulty level.

        Returns:
            Target integer value.
        """
        if difficulty <= 3:
            return self._rng.choice(data)
        return self._rng.randint(lo, hi)

    def _create_steps(self, data: dict) -> list[str]:
        """Generate z-score computation steps.

        Args:
            data: Solution data with target, mean, std_dev, and z.

        Returns:
            Steps showing the subtraction, division, and result.
        """
        target = data["target"]
        mean_str = self._fmt.format_decimal(data["mean"])
        std_str = self._fmt.format_decimal(data["std_dev"])
        z_str = self._fmt.format_decimal(data["z"])
        diff = self._fmt.format_decimal(data["target"] - data["mean"])
        return [
            f"z=({target}-{mean_str})/{std_str}",
            f"z={diff}/{std_str}={z_str}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the z-score as a decimal string.

        Args:
            data: Solution data.

        Returns:
            Rounded decimal representation.
        """
        return self._fmt.format_decimal(data["z"])


@register
class BasicProbGenerator(StepGenerator):
    """Compute basic probability P(A) = favorable / total.

    Generates a scenario with a known number of favorable and total
    outcomes, then computes the probability as a simplified fraction.

    Input format:
        ``compute probability``

    Target format:
        ``P(A)=\\frac{favorable}{total} <step>
        \\frac{3}{12}=\\frac{1}{4} <step> \\frac{1}{4}``

    Difficulty scaling:
        d1-2: total outcomes 4-12, favorable 1-total.
        d3-4: total 10-30.
        d5-6: total 20-60.
        d7-8: total 50-100.

    Prerequisites:
        division.

    Example:
        >>> gen = BasicProbGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'basic_prob'
    """

    _TOTAL_RANGES: dict[int, tuple[int, int]] = {
        1: (4, 12), 2: (4, 12),
        3: (10, 30), 4: (10, 30),
        5: (20, 60), 6: (20, 60),
        7: (50, 100), 8: (50, 100),
    }

    def __init__(self, **kwargs) -> None:
        """Initialise with fraction formatter.

        Args:
            **kwargs: Passed to parent constructor.
        """
        super().__init__(**kwargs)
        self._fmt = FractionFormatter()

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "basic_prob"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 2

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["division"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls outcome counts.

        Returns:
            Natural language description.
        """
        return "compute probability"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a probability problem.

        Args:
            difficulty: Controls the total outcome count.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        lo, hi = self._TOTAL_RANGES.get(difficulty, (4, 12))
        total = self._rng.randint(lo, hi)
        favorable = self._rng.randint(1, total - 1)
        prob = Fraction(favorable, total)
        return (
            f"P(A)=\\frac{{{favorable}}}{{{total}}}",
            {"favorable": favorable, "total": total, "prob": prob},
        )

    def _create_steps(self, data: dict) -> list[str]:
        """Generate simplification steps.

        Args:
            data: Solution data with favorable, total, and prob.

        Returns:
            Steps showing the fraction simplification.
        """
        fav = data["favorable"]
        tot = data["total"]
        prob = data["prob"]
        prob_str = self._fmt.format(prob)
        if prob.numerator == fav and prob.denominator == tot:
            return [f"\\frac{{{fav}}}{{{tot}}}={prob_str}"]
        return [f"\\frac{{{fav}}}{{{tot}}}={prob_str}"]

    def _create_answer(self, data: dict) -> str:
        """Return the probability as a simplified fraction.

        Args:
            data: Solution data.

        Returns:
            Formatted fraction string.
        """
        return self._fmt.format(data["prob"])


@register
class ConditionalProbGenerator(StepGenerator):
    """Compute conditional probability P(A|B) = P(A and B) / P(B).

    Generates joint and marginal probabilities using integer counts,
    then computes P(A|B) as a simplified fraction.

    Input format:
        ``compute conditional probability``

    Target format:
        ``P(A|B)=P(A \\cap B)/P(B) <step> P(A \\cap B)=\\frac{3}{20}
        <step> P(B)=\\frac{8}{20} <step> P(A|B)=\\frac{3}{8} <step>
        \\frac{3}{8}``

    Difficulty scaling:
        d1-2: total outcomes 10-20.
        d3-4: total 20-50.
        d5-6: total 50-100.
        d7-8: total 100-200.

    Prerequisites:
        basic_prob, division.

    Example:
        >>> gen = ConditionalProbGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'conditional_prob'
    """

    _TOTAL_RANGES: dict[int, tuple[int, int]] = {
        1: (10, 20), 2: (10, 20),
        3: (20, 50), 4: (20, 50),
        5: (50, 100), 6: (50, 100),
        7: (100, 200), 8: (100, 200),
    }

    def __init__(self, **kwargs) -> None:
        """Initialise with fraction formatter.

        Args:
            **kwargs: Passed to parent constructor.
        """
        super().__init__(**kwargs)
        self._fmt = FractionFormatter()

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "conditional_prob"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 3

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["basic_prob", "division"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls outcome counts.

        Returns:
            Natural language description.
        """
        return "compute conditional probability"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a conditional probability problem from counts.

        Constructs integer counts for B and A-intersect-B to
        guarantee clean fractions.

        Args:
            difficulty: Controls the total outcome count.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        lo, hi = self._TOTAL_RANGES.get(difficulty, (10, 20))
        total = self._rng.randint(lo, hi)
        count_b = self._rng.randint(2, total - 1)
        count_ab = self._rng.randint(1, count_b)
        p_b = Fraction(count_b, total)
        p_ab = Fraction(count_ab, total)
        p_a_given_b = Fraction(count_ab, count_b)
        return (
            f"P(A|B)=P(A \\cap B)/P(B)",
            {"total": total, "count_b": count_b, "count_ab": count_ab,
             "p_b": p_b, "p_ab": p_ab, "p_a_given_b": p_a_given_b},
        )

    def _create_steps(self, data: dict) -> list[str]:
        """Generate joint, marginal, and conditional steps.

        Args:
            data: Solution data with counts and probabilities.

        Returns:
            Steps showing each probability computation.
        """
        p_ab_str = self._fmt.format(data["p_ab"])
        p_b_str = self._fmt.format(data["p_b"])
        result_str = self._fmt.format(data["p_a_given_b"])
        return [
            f"P(A \\cap B)={data['count_ab']}/{data['total']}={p_ab_str}",
            f"P(B)={data['count_b']}/{data['total']}={p_b_str}",
            f"P(A|B)={p_ab_str}/{p_b_str}={result_str}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the conditional probability.

        Args:
            data: Solution data.

        Returns:
            Formatted fraction string.
        """
        return self._fmt.format(data["p_a_given_b"])


@register
class BinomialDistGenerator(StepGenerator):
    """Compute binomial probability P(X=k) = C(n,k) * p^k * (1-p)^(n-k).

    Generates problems with small n and simple p values (fractions
    with small denominators) so each step is tractable.

    Input format:
        ``compute binomial probability``

    Target format:
        ``P(X=2), n=5, p=\\frac{1}{3} <step> C(5,2)=10 <step>
        (\\frac{1}{3})^2=\\frac{1}{9} <step>
        (\\frac{2}{3})^3=\\frac{8}{27} <step>
        10*\\frac{1}{9}*\\frac{8}{27}=\\frac{80}{243} <step>
        \\frac{80}{243}``

    Difficulty scaling:
        d1-2: n=3-5, simple fractions p=1/2, 1/3, 1/4.
        d3-4: n=5-8.
        d5-6: n=7-10.
        d7-8: n=9-12, decimal probabilities 0.1-0.5.

    Prerequisites:
        binomial, exponentiation.

    Example:
        >>> gen = BinomialDistGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'binomial_dist'
    """

    _N_RANGES: dict[int, tuple[int, int]] = {
        1: (3, 5), 2: (3, 5),
        3: (5, 8), 4: (5, 8),
        5: (7, 10), 6: (7, 10),
        7: (9, 12), 8: (9, 12),
    }

    _SIMPLE_PROBS = [
        Fraction(1, 2), Fraction(1, 3), Fraction(1, 4),
        Fraction(1, 5), Fraction(1, 6), Fraction(2, 5),
        Fraction(3, 10), Fraction(2, 3),
    ]

    def __init__(self, **kwargs) -> None:
        """Initialise with fraction formatter.

        Args:
            **kwargs: Passed to parent constructor.
        """
        super().__init__(**kwargs)
        self._fmt = FractionFormatter()

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "binomial_dist"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["binomial", "exponentiation"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls n and p ranges.

        Returns:
            Natural language description.
        """
        return "compute binomial probability"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a binomial probability problem.

        Args:
            difficulty: Controls n range and p complexity.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        n_lo, n_hi = self._N_RANGES.get(difficulty, (3, 5))
        n = self._rng.randint(n_lo, n_hi)
        k = self._rng.randint(1, n - 1)
        p = self._choose_p(difficulty)
        q = Fraction(1) - p
        binom_coeff = self._binom(n, k)
        p_k = p ** k
        q_nk = q ** (n - k)
        result = binom_coeff * p_k * q_nk
        p_str = self._fmt.format(p)
        return (
            f"P(X={k}), n={n}, p={p_str}",
            {"n": n, "k": k, "p": p, "q": q,
             "binom": binom_coeff, "p_k": p_k,
             "q_nk": q_nk, "result": result},
        )

    def _choose_p(self, difficulty: int) -> Fraction:
        """Choose a probability value appropriate for difficulty.

        Args:
            difficulty: Difficulty level.

        Returns:
            Fraction representing p.
        """
        return self._rng.choice(self._SIMPLE_PROBS)

    def _binom(self, n: int, k: int) -> int:
        """Compute binomial coefficient C(n, k).

        Args:
            n: Total.
            k: Choose count.

        Returns:
            Binomial coefficient.
        """
        return math.comb(n, k)

    def _create_steps(self, data: dict) -> list[str]:
        """Generate coefficient, power, and multiplication steps.

        Args:
            data: Solution data with all components.

        Returns:
            Steps showing C(n,k), p^k, q^(n-k), and final product.
        """
        n = data["n"]
        k = data["k"]
        p_str = self._fmt.format(data["p"])
        q_str = self._fmt.format(data["q"])
        pk_str = self._fmt.format(data["p_k"])
        qnk_str = self._fmt.format(data["q_nk"])
        result_str = self._fmt.format(data["result"])
        binom_val = data["binom"]
        return [
            f"C({n},{k})={binom_val}",
            f"({p_str})^{k}={pk_str}",
            f"({q_str})^{n - k}={qnk_str}",
            f"{binom_val}*{pk_str}*{qnk_str}={result_str}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the binomial probability.

        Args:
            data: Solution data.

        Returns:
            Formatted fraction string.
        """
        return self._fmt.format(data["result"])


@register
class ExpectedValueGenerator(StepGenerator):
    """Compute expected value E[X] = sum(x_i * p_i).

    Generates a discrete probability distribution as (value, probability)
    pairs and computes the weighted sum.

    Input format:
        ``compute expected value``

    Target format:
        ``E[X]: (1,\\frac{1}{4}),(2,\\frac{1}{2}),(5,\\frac{1}{4}) <step>
        1*\\frac{1}{4}=\\frac{1}{4} <step> 2*\\frac{1}{2}=1 <step>
        5*\\frac{1}{4}=\\frac{5}{4} <step>
        \\frac{1}{4}+1+\\frac{5}{4}=\\frac{5}{2} <step> \\frac{5}{2}``

    Difficulty scaling:
        d1-2: 2-3 outcomes, values 1-6.
        d3-4: 3-4 outcomes, values 1-10.
        d5-6: 4-5 outcomes, values 1-20.
        d7-8: 5-6 outcomes, values 1-50.

    Prerequisites:
        multiplication, addition.

    Example:
        >>> gen = ExpectedValueGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'expected_value'
    """

    _OUTCOME_RANGES: dict[int, tuple[int, int]] = {
        1: (2, 3), 2: (2, 3),
        3: (3, 4), 4: (3, 4),
        5: (4, 5), 6: (4, 5),
        7: (5, 6), 8: (5, 6),
    }

    _VALUE_RANGES: dict[int, tuple[int, int]] = {
        1: (1, 6), 2: (1, 6),
        3: (1, 10), 4: (1, 10),
        5: (1, 20), 6: (1, 20),
        7: (1, 50), 8: (1, 50),
    }

    def __init__(self, **kwargs) -> None:
        """Initialise with fraction formatter.

        Args:
            **kwargs: Passed to parent constructor.
        """
        super().__init__(**kwargs)
        self._fmt = FractionFormatter()

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "expected_value"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 3

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["multiplication", "addition"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls outcome count.

        Returns:
            Natural language description.
        """
        return "compute expected value"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a probability distribution and compute E[X].

        Args:
            difficulty: Controls outcome count and value range.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        out_lo, out_hi = self._OUTCOME_RANGES.get(difficulty, (2, 3))
        val_lo, val_hi = self._VALUE_RANGES.get(difficulty, (1, 6))
        n = self._rng.randint(out_lo, out_hi)
        values = self._distinct_values(n, val_lo, val_hi)
        probs = self._make_distribution(n)
        products = [Fraction(v) * p for v, p in zip(values, probs)]
        expected = sum(products)
        pairs = ",".join(
            f"({v},{self._fmt.format(p)})"
            for v, p in zip(values, probs)
        )
        return (
            f"E[X]: {pairs}",
            {"values": values, "probs": probs,
             "products": products, "expected": expected},
        )

    def _distinct_values(self, n: int, lo: int,
                         hi: int) -> list[int]:
        """Generate n distinct sorted values in [lo, hi].

        Args:
            n: Number of distinct values.
            lo: Lower bound.
            hi: Upper bound.

        Returns:
            Sorted list of distinct integers.
        """
        pool = list(range(lo, hi + 1))
        self._rng.shuffle(pool)
        return sorted(pool[:n])

    def _make_distribution(self, n: int) -> list[Fraction]:
        """Generate a probability distribution summing to 1.

        Args:
            n: Number of outcomes.

        Returns:
            List of Fractions summing to 1.
        """
        weights = [self._rng.randint(1, 5) for _ in range(n)]
        total = sum(weights)
        return [Fraction(w, total) for w in weights]

    def _create_steps(self, data: dict) -> list[str]:
        """Generate per-outcome multiplication and summation steps.

        Args:
            data: Solution data with values, probs, and products.

        Returns:
            Steps showing each product and the final sum.
        """
        steps: list[str] = []
        for v, p, prod in zip(
            data["values"], data["probs"], data["products"]
        ):
            p_str = self._fmt.format(p)
            prod_str = self._fmt.format(prod)
            steps.append(f"{v}*{p_str}={prod_str}")
        parts = "+".join(self._fmt.format(p) for p in data["products"])
        exp_str = self._fmt.format(data["expected"])
        steps.append(f"{parts}={exp_str}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the expected value.

        Args:
            data: Solution data.

        Returns:
            Formatted fraction string.
        """
        return self._fmt.format(data["expected"])


@register
class MarkovChainGenerator(StepGenerator):
    """Compute state distribution after n transitions in a Markov chain.

    Generates a stochastic transition matrix and an initial state
    vector, then applies matrix-vector multiplication n times to
    produce the final distribution.

    Input format:
        ``compute markov chain state after 2 transitions``

    Target format:
        ``\\pi_0=(1,0), T=[[1/2,1/2],[1/3,2/3]] <step>
        \\pi_1=(1*1/2+0*1/3, 1*1/2+0*2/3)=(1/2,1/2) <step>
        \\pi_2=(1/2*1/2+1/2*1/3, 1/2*1/2+1/2*2/3)=(5/12,7/12) <step>
        (5/12,7/12)``

    Difficulty scaling:
        d1-2: 2 states, 1-2 transitions.
        d3-4: 2 states, 2-3 transitions.
        d5-6: 3 states, 2-3 transitions.
        d7-8: 3 states, 3-4 transitions.

    Prerequisites:
        matrix_multiply, expected_value.

    Example:
        >>> gen = MarkovChainGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'markov_chain'
    """

    _PARAM_RANGES: dict[int, dict[str, tuple[int, int]]] = {
        1: {"states": (2, 2), "steps": (1, 2)},
        2: {"states": (2, 2), "steps": (1, 2)},
        3: {"states": (2, 2), "steps": (2, 3)},
        4: {"states": (2, 2), "steps": (2, 3)},
        5: {"states": (3, 3), "steps": (2, 3)},
        6: {"states": (3, 3), "steps": (2, 3)},
        7: {"states": (3, 3), "steps": (3, 4)},
        8: {"states": (3, 3), "steps": (3, 4)},
    }

    def __init__(self, **kwargs) -> None:
        """Initialise with transition matrix builder and formatter.

        Args:
            **kwargs: Passed to parent constructor.
        """
        super().__init__(**kwargs)
        self._matrix_builder = TransitionMatrixBuilder(self._rng)
        self._fmt = FractionFormatter()

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "markov_chain"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["matrix_multiply", "expected_value"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls state count and transitions.

        Returns:
            Natural language description.
        """
        params = self._PARAM_RANGES.get(difficulty, self._PARAM_RANGES[1])
        n_steps = self._rng.randint(*params["steps"])
        return f"compute markov chain state after {n_steps} transitions"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Markov chain problem.

        Args:
            difficulty: Controls state count and number of transitions.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        params = self._PARAM_RANGES.get(difficulty, self._PARAM_RANGES[1])
        n_states = self._rng.randint(*params["states"])
        n_steps = self._rng.randint(*params["steps"])
        matrix = self._matrix_builder.build(n_states)
        init = self._initial_state(n_states)
        history = self._simulate(init, matrix, n_steps)
        matrix_str = self._format_matrix(matrix)
        init_str = self._format_vector(init)
        return (
            f"\\pi_0={init_str}, T={matrix_str}",
            {"matrix": matrix, "init": init, "n_steps": n_steps,
             "history": history, "n_states": n_states},
        )

    def _initial_state(self, n_states: int) -> list[Fraction]:
        """Generate an initial state vector with one hot state.

        Args:
            n_states: Number of states.

        Returns:
            One-hot vector as list of Fractions.
        """
        start = self._rng.randint(0, n_states - 1)
        vec = [Fraction(0)] * n_states
        vec[start] = Fraction(1)
        return vec

    def _simulate(self, init: list[Fraction],
                  matrix: list[list[Fraction]],
                  n_steps: int) -> list[list[Fraction]]:
        """Simulate the Markov chain for n steps.

        Args:
            init: Initial state vector.
            matrix: Transition matrix.
            n_steps: Number of transitions.

        Returns:
            List of state vectors at each step (including initial).
        """
        history = [init]
        current = init
        for _ in range(n_steps):
            current = self._multiply_vector(current, matrix)
            history.append(current)
        return history

    def _multiply_vector(self, vec: list[Fraction],
                         matrix: list[list[Fraction]]) -> list[Fraction]:
        """Multiply a row vector by a transition matrix.

        Args:
            vec: Row vector.
            matrix: Transition matrix.

        Returns:
            Resulting row vector.
        """
        n = len(vec)
        result: list[Fraction] = []
        for j in range(n):
            total = sum(vec[i] * matrix[i][j] for i in range(n))
            result.append(total)
        return result

    def _format_matrix(self, matrix: list[list[Fraction]]) -> str:
        """Format transition matrix as a nested list string.

        Args:
            matrix: Transition matrix.

        Returns:
            String like '[[1/2,1/2],[1/3,2/3]]'.
        """
        rows = []
        for row in matrix:
            entries = ",".join(self._fmt.format(f) for f in row)
            rows.append(f"[{entries}]")
        return "[" + ",".join(rows) + "]"

    def _format_vector(self, vec: list[Fraction]) -> str:
        """Format a state vector as a parenthesised tuple.

        Args:
            vec: State vector.

        Returns:
            String like '(1/2,1/2)'.
        """
        entries = ",".join(self._fmt.format(f) for f in vec)
        return f"({entries})"

    def _create_steps(self, data: dict) -> list[str]:
        """Generate one step per transition showing the matrix multiply.

        Args:
            data: Solution data with transition history.

        Returns:
            Steps showing each state transition.
        """
        history = data["history"]
        matrix = data["matrix"]
        steps: list[str] = []
        for t in range(1, len(history)):
            step = self._transition_step(
                t, history[t - 1], history[t], matrix,
            )
            steps.append(step)
        return steps

    def _transition_step(self, t: int, prev: list[Fraction],
                         curr: list[Fraction],
                         matrix: list[list[Fraction]]) -> str:
        """Format one transition step.

        Args:
            t: Time step index.
            prev: Previous state vector.
            curr: Current state vector.
            matrix: Transition matrix.

        Returns:
            Step string showing the matrix multiplication result.
        """
        vec_str = self._format_vector(curr)
        return f"\\pi_{t}={vec_str}"

    def _create_answer(self, data: dict) -> str:
        """Return the final state distribution.

        Args:
            data: Solution data.

        Returns:
            Formatted vector of the final state.
        """
        final = data["history"][-1]
        return self._format_vector(final)
