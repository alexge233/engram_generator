"""Time series analysis task generators.

6 generators across tiers 4-6 covering autocorrelation, exponential smoothing,
moving average, ARIMA forecasting, seasonal decomposition, and stationarity
checking.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


# ---------------------------------------------------------------------------
# 1. Autocorrelation (tier 5)
# ---------------------------------------------------------------------------

@register
class AutocorrelationGenerator(StepGenerator):
    """Compute autocorrelation r_k of a short time series.

    Uses r_k = sum((x_t - x_bar)(x_{t+k} - x_bar)) / sum((x_t - x_bar)^2)
    for lag k=1 or k=2 on a short integer series.

    Difficulty scaling:
        Difficulty 1-3: series length 5, values in [1, 10], lag k=1.
        Difficulty 4-6: series length 6, values in [-5, 15], lag k=1 or k=2.
        Difficulty 7-8: series length 7, values in [-10, 20], lag k=2.

    Prerequisites:
        std_dev.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "autocorrelation"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["std_dev"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute autocorrelation of a time series"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an autocorrelation problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            n = 5
            lo, hi = 1, 10
            lag = 1
        elif difficulty <= 6:
            n = 6
            lo, hi = -5, 15
            lag = self._rng.choice([1, 2])
        else:
            n = 7
            lo, hi = -10, 20
            lag = 2

        series = [self._rng.randint(lo, hi) for _ in range(n)]
        x_bar = round(sum(series) / n, 4)
        devs = [round(x - x_bar, 4) for x in series]

        denom = round(sum(d ** 2 for d in devs), 4)
        numer = round(
            sum(devs[t] * devs[t + lag] for t in range(n - lag)), 4
        )
        r_k = round(numer / denom, 4) if denom != 0 else 0.0

        s_str = ", ".join(str(v) for v in series)
        return (
            f"r_k = \\frac{{\\sum (x_t - \\bar{{x}})(x_{{t+k}} - \\bar{{x}})}}"
            f"{{\\sum (x_t - \\bar{{x}})^2}}. "
            f"x = [{s_str}], k = {lag}.",
            {
                "series": series, "n": n, "lag": lag,
                "x_bar": x_bar, "devs": devs,
                "numer": numer, "denom": denom, "r_k": r_k,
            },
        )

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps for autocorrelation.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing mean, denominator, numerator, and r_k.
        """
        return [
            f"x_bar = {data['x_bar']}",
            f"sum((x_t - x_bar)^2) = {data['denom']}",
            f"sum((x_t - x_bar)(x_{{t+{data['lag']}}} - x_bar)) = {data['numer']}",
            f"r_{data['lag']} = {data['numer']}/{data['denom']} = {data['r_k']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the autocorrelation coefficient.

        Args:
            data: Solution data dict.

        Returns:
            r_k value as a string.
        """
        return f"r_{data['lag']} = {data['r_k']}"


# ---------------------------------------------------------------------------
# 2. Exponential Smoothing (tier 4)
# ---------------------------------------------------------------------------

@register
class ExponentialSmoothingGenerator(StepGenerator):
    """Apply simple exponential smoothing to a short series.

    S_t = alpha * x_t + (1 - alpha) * S_{t-1}, with S_0 = x_0.

    Difficulty scaling:
        Difficulty 1-3: series length 4, alpha in {0.2, 0.3, 0.5}.
        Difficulty 4-6: series length 5, alpha in {0.1, 0.2, 0.3, 0.4, 0.5}.
        Difficulty 7-8: series length 6, alpha in [0.1, 0.9].

    Prerequisites:
        multiplication.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "exponential_smoothing"

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
            Short task description.
        """
        return "apply exponential smoothing to a time series"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an exponential smoothing problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            n = 4
            alpha = self._rng.choice([0.2, 0.3, 0.5])
            series = [self._rng.randint(1, 20) for _ in range(n)]
        elif difficulty <= 6:
            n = 5
            alpha = self._rng.choice([0.1, 0.2, 0.3, 0.4, 0.5])
            series = [self._rng.randint(-5, 30) for _ in range(n)]
        else:
            n = 6
            alpha = round(self._rng.uniform(0.1, 0.9), 1)
            series = [self._rng.randint(-10, 40) for _ in range(n)]

        smoothed = [float(series[0])]
        for t in range(1, n):
            s_t = round(alpha * series[t] + (1 - alpha) * smoothed[-1], 4)
            smoothed.append(s_t)

        s_str = ", ".join(str(v) for v in series)
        return (
            f"S_t = \\alpha x_t + (1-\\alpha) S_{{t-1}}. "
            f"x = [{s_str}], \\alpha = {alpha}.",
            {
                "series": series, "alpha": alpha,
                "smoothed": smoothed, "n": n,
            },
        )

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps for exponential smoothing.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing S_0 and each subsequent smoothed value.
        """
        steps = [f"S_0 = x_0 = {data['smoothed'][0]}"]
        alpha = data["alpha"]
        for t in range(1, data["n"]):
            steps.append(
                f"S_{t} = {alpha}*{data['series'][t]} + "
                f"{round(1 - alpha, 4)}*{data['smoothed'][t - 1]} = "
                f"{data['smoothed'][t]}"
            )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the final smoothed value.

        Args:
            data: Solution data dict.

        Returns:
            S_n as a string.
        """
        sm = data["smoothed"]
        vals = ", ".join(str(v) for v in sm)
        return f"S = [{vals}]"


# ---------------------------------------------------------------------------
# 3. Moving Average (tier 4)
# ---------------------------------------------------------------------------

@register
class MovingAverageGenerator(StepGenerator):
    """Compute a simple moving average of window size k on a short series.

    MA(k): y_t = (x_t + x_{t-1} + ... + x_{t-k+1}) / k.

    Difficulty scaling:
        Difficulty 1-3: series length 5, window k=2.
        Difficulty 4-6: series length 6, window k=3.
        Difficulty 7-8: series length 7, window k in {3, 4}.

    Prerequisites:
        arithmetic_mean.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "moving_average"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["arithmetic_mean"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute moving average of a time series"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a moving average problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            n = 5
            k = 2
            series = [self._rng.randint(1, 20) for _ in range(n)]
        elif difficulty <= 6:
            n = 6
            k = 3
            series = [self._rng.randint(-5, 30) for _ in range(n)]
        else:
            n = 7
            k = self._rng.choice([3, 4])
            series = [self._rng.randint(-10, 40) for _ in range(n)]

        ma_values = []
        for t in range(k - 1, n):
            window = series[t - k + 1: t + 1]
            avg = round(sum(window) / k, 4)
            ma_values.append({"t": t, "window": window, "avg": avg})

        s_str = ", ".join(str(v) for v in series)
        return (
            f"MA(k) = \\frac{{1}}{{k}} \\sum_{{i=0}}^{{k-1}} x_{{t-i}}. "
            f"x = [{s_str}], k = {k}.",
            {"series": series, "k": k, "ma_values": ma_values},
        )

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps for moving average.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing each window average.
        """
        k = data["k"]
        steps = []
        for mv in data["ma_values"]:
            w_str = "+".join(str(v) for v in mv["window"])
            steps.append(
                f"y_{mv['t']} = ({w_str})/{k} = {mv['avg']}"
            )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return all moving average values.

        Args:
            data: Solution data dict.

        Returns:
            Moving average values as a string.
        """
        vals = ", ".join(str(mv["avg"]) for mv in data["ma_values"])
        return f"MA = [{vals}]"


# ---------------------------------------------------------------------------
# 4. ARIMA Forecast (tier 6)
# ---------------------------------------------------------------------------

@register
class ArimaForecastGenerator(StepGenerator):
    """Forecast using a simple AR(1) model: x_t = phi * x_{t-1} + e_t.

    Given phi and recent observed values, forecast x_{t+1} and x_{t+2}
    assuming zero future errors (deterministic forecast).

    Difficulty scaling:
        Difficulty 1-3: phi in {0.3, 0.5, 0.7}, 3 recent values.
        Difficulty 4-6: phi in [-0.8, 0.9], 4 recent values.
        Difficulty 7-8: phi in [-0.9, 0.95], 5 recent values.

    Prerequisites:
        multiplication.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "arima_forecast"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["multiplication"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "forecast next values using AR(1) model"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an AR(1) forecasting problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            phi = self._rng.choice([0.3, 0.5, 0.7])
            n_obs = 3
            values = [round(self._rng.uniform(1, 20), 1) for _ in range(n_obs)]
        elif difficulty <= 6:
            phi = round(self._rng.uniform(-0.8, 0.9), 2)
            n_obs = 4
            values = [round(self._rng.uniform(-10, 30), 1) for _ in range(n_obs)]
        else:
            phi = round(self._rng.uniform(-0.9, 0.95), 2)
            n_obs = 5
            values = [round(self._rng.uniform(-20, 40), 1) for _ in range(n_obs)]

        last = values[-1]
        f1 = round(phi * last, 4)
        f2 = round(phi * f1, 4)

        v_str = ", ".join(str(v) for v in values)
        return (
            f"AR(1): x_t = \\phi x_{{t-1}} + e_t. "
            f"\\phi = {phi}, x = [{v_str}]. "
            f"Forecast x_{{t+1}}, x_{{t+2}} (e=0).",
            {
                "phi": phi, "values": values,
                "last": last, "f1": f1, "f2": f2,
            },
        )

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps for AR(1) forecast.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing each forecast computation.
        """
        return [
            f"x_last = {data['last']}",
            f"x_{{t+1}} = {data['phi']} * {data['last']} = {data['f1']}",
            f"x_{{t+2}} = {data['phi']} * {data['f1']} = {data['f2']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the forecasted values.

        Args:
            data: Solution data dict.

        Returns:
            Two-step forecast as a string.
        """
        return f"x_{{t+1}} = {data['f1']}, x_{{t+2}} = {data['f2']}"


# ---------------------------------------------------------------------------
# 5. Seasonal Decompose (tier 5)
# ---------------------------------------------------------------------------

@register
class SeasonalDecomposeGenerator(StepGenerator):
    """Additive seasonal decomposition: x_t = T_t + S_t + R_t.

    Given original data, trend (moving average), and seasonal component
    (average per period position), compute the residual R_t = x_t - T_t - S_t.

    Difficulty scaling:
        Difficulty 1-3: period=2, 4 data points.
        Difficulty 4-6: period=3, 6 data points.
        Difficulty 7-8: period=4, 8 data points.

    Prerequisites:
        subtraction.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "seasonal_decompose"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["subtraction"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute seasonal decomposition residuals"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a seasonal decomposition problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            period = 2
            n = 4
        elif difficulty <= 6:
            period = 3
            n = 6
        else:
            period = 4
            n = 8

        series = [self._rng.randint(5, 50) for _ in range(n)]
        trend = [round(self._rng.uniform(10, 40), 1) for _ in range(n)]
        seasonal = [round(self._rng.uniform(-5, 5), 1) for _ in range(period)]

        residuals = []
        for t in range(n):
            s_t = seasonal[t % period]
            r_t = round(series[t] - trend[t] - s_t, 4)
            residuals.append(r_t)

        x_str = ", ".join(str(v) for v in series)
        t_str = ", ".join(str(v) for v in trend)
        s_str = ", ".join(str(v) for v in seasonal)
        return (
            f"x_t = T_t + S_t + R_t. "
            f"x = [{x_str}], T = [{t_str}], S = [{s_str}] (period={period}).",
            {
                "series": series, "trend": trend,
                "seasonal": seasonal, "period": period,
                "residuals": residuals, "n": n,
            },
        )

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps for seasonal decomposition.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing R_t = x_t - T_t - S_t for each point.
        """
        steps = []
        for t in range(data["n"]):
            s_idx = t % data["period"]
            steps.append(
                f"R_{t} = {data['series'][t]} - {data['trend'][t]} - "
                f"{data['seasonal'][s_idx]} = {data['residuals'][t]}"
            )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the residual series.

        Args:
            data: Solution data dict.

        Returns:
            Residuals as a formatted list.
        """
        vals = ", ".join(str(v) for v in data["residuals"])
        return f"R = [{vals}]"


# ---------------------------------------------------------------------------
# 6. Stationarity Check (tier 5)
# ---------------------------------------------------------------------------

@register
class StationarityCheckGenerator(StepGenerator):
    """Check weak stationarity by comparing mean and variance of two windows.

    Given two consecutive windows of a time series, compare their mean
    and variance. If both are approximately equal, the series may be
    weakly stationary.

    Difficulty scaling:
        Difficulty 1-3: window size 3, values in [1, 20].
        Difficulty 4-6: window size 4, values in [-10, 30].
        Difficulty 7-8: window size 5, values in [-20, 50].

    Prerequisites:
        std_dev.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "stationarity_check"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["std_dev"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "check stationarity of a time series via two windows"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a stationarity check problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            w = 3
            lo, hi = 1, 20
        elif difficulty <= 6:
            w = 4
            lo, hi = -10, 30
        else:
            w = 5
            lo, hi = -20, 50

        w1 = [self._rng.randint(lo, hi) for _ in range(w)]
        w2 = [self._rng.randint(lo, hi) for _ in range(w)]

        m1 = round(sum(w1) / w, 4)
        m2 = round(sum(w2) / w, 4)
        v1 = round(sum((x - m1) ** 2 for x in w1) / w, 4)
        v2 = round(sum((x - m2) ** 2 for x in w2) / w, 4)

        mean_diff = round(abs(m1 - m2), 4)
        var_diff = round(abs(v1 - v2), 4)
        threshold = max(round(0.2 * max(abs(m1), abs(m2), 1), 4), 1.0)
        stationary = mean_diff <= threshold and var_diff <= threshold * 5

        w1_str = ", ".join(str(v) for v in w1)
        w2_str = ", ".join(str(v) for v in w2)
        return (
            f"Window 1: [{w1_str}], Window 2: [{w2_str}]. "
            f"Compare mean and variance.",
            {
                "w1": w1, "w2": w2, "w": w,
                "m1": m1, "m2": m2, "v1": v1, "v2": v2,
                "mean_diff": mean_diff, "var_diff": var_diff,
                "stationary": stationary,
            },
        )

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps for stationarity check.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing mean, variance, and comparison for each window.
        """
        return [
            f"W1: mean = {data['m1']}, var = {data['v1']}",
            f"W2: mean = {data['m2']}, var = {data['v2']}",
            f"|mean_diff| = {data['mean_diff']}, |var_diff| = {data['var_diff']}",
            f"stationary = {data['stationary']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the stationarity verdict.

        Args:
            data: Solution data dict.

        Returns:
            Mean/variance comparison and verdict.
        """
        verdict = "likely stationary" if data["stationary"] else "non-stationary"
        return f"mean_diff={data['mean_diff']}, var_diff={data['var_diff']}, {verdict}"
