"""Extended signal processing task generators.

8 generators across tiers 4-6 covering continuous convolution,
signal correlation, Nyquist diagrams, Bode plot computation,
signal energy and power, modulation/demodulation, matched filter,
and sigma-delta modulation.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


def _f(value: float, decimals: int = 4) -> str:
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


def _fv(vec: list[float]) -> str:
    """Format a vector as a compact string.

    Args:
        vec: List of floats.

    Returns:
        Bracket-enclosed comma-separated string.
    """
    return "[" + ",".join(_f(v) for v in vec) + "]"


def _cfmt(c: tuple[float, float]) -> str:
    """Format a complex number as a string.

    Args:
        c: Complex number as (real, imag).

    Returns:
        Formatted string like '1.5+2.3j' or '1.5-2.3j'.
    """
    re, im = c
    if im >= 0:
        return f"{_f(re)}+{_f(im)}j"
    return f"{_f(re)}{_f(im)}j"


# ===================================================================
# 1. Continuous Convolution (tier 5)
# ===================================================================

@register
class ConvolutionContinuousGenerator(StepGenerator):
    """Compute continuous convolution for simple signal pairs.

    (f*g)(t) = integral f(tau)*g(t-tau) dtau. Uses rectangular
    and exponential signals with analytically tractable results.

    Difficulty scaling:
        Difficulty 1-3: rect*rect, width 1, evaluate at 1-2 points.
        Difficulty 4-6: rect*rect, different widths, 3 points.
        Difficulty 7-8: rect*exp(decaying), 3 points.

    Prerequisites:
        definite_integral.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "convolution_continuous"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["definite_integral"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls signal types.

        Returns:
            Short task description.
        """
        return "compute continuous convolution of two signals"

    def _rect_rect_conv(self, a: float, b: float,
                        t: float) -> float:
        """Compute rect(t/a)*rect(t/b) convolution at time t.

        Both rectangles are symmetric about origin with widths a and b.
        Result is a trapezoid with support [-(a+b)/2, (a+b)/2].

        Args:
            a: Width of first rectangle.
            b: Width of second rectangle.
            t: Time at which to evaluate.

        Returns:
            Convolution value rounded to 4 dp.
        """
        half_sum = (a + b) / 2.0
        half_diff = abs(a - b) / 2.0
        min_ab = min(a, b)
        abs_t = abs(t)

        if abs_t > half_sum:
            return 0.0
        if abs_t <= half_diff:
            return round(min_ab, 4)
        return round(half_sum - abs_t, 4)

    def _rect_exp_conv(self, w: float, alpha: float,
                       t: float) -> float:
        """Compute rect(t/w)*exp(-alpha*t)*u(t) convolution at time t.

        rect has width w centred at origin, exp is causal.

        Args:
            w: Width of rectangle.
            alpha: Decay rate of exponential.
            t: Time at which to evaluate.

        Returns:
            Convolution value rounded to 4 dp.
        """
        lower = max(0.0, t - w / 2.0)
        upper = max(0.0, t + w / 2.0)
        if upper <= 0 or lower >= upper:
            return 0.0
        if alpha == 0:
            return round(upper - lower, 4)
        val = (math.exp(-alpha * lower) - math.exp(-alpha * upper)) / alpha
        return round(val, 4)

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate signals and evaluate convolution at sample points.

        Args:
            difficulty: Controls signal types and number of points.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            a = 1.0
            b = 1.0
            n_pts = 2
            mode = "rect_rect"
        elif difficulty <= 6:
            a = self._rng.choice([1.0, 2.0])
            b = self._rng.choice([1.0, 2.0, 3.0])
            n_pts = 3
            mode = "rect_rect"
        else:
            a = self._rng.choice([1.0, 2.0])
            alpha = round(self._rng.uniform(0.5, 2.0), 2)
            n_pts = 3
            mode = "rect_exp"

        half_range = 3.0
        t_pts = sorted([
            round(self._rng.uniform(-half_range, half_range), 2)
            for _ in range(n_pts)
        ])

        results = []
        if mode == "rect_rect":
            for t in t_pts:
                val = self._rect_rect_conv(a, b, t)
                results.append((t, val))
            problem = (
                f"(rect_{{w={_f(a)}}} * rect_{{w={_f(b)}}})(t), "
                f"t={[_f(t) for t in t_pts]}"
            )
            data = {
                "mode": mode, "a": a, "b": b,
                "results": results, "alpha": None,
            }
        else:
            for t in t_pts:
                val = self._rect_exp_conv(a, alpha, t)
                results.append((t, val))
            problem = (
                f"(rect_{{w={_f(a)}}} * e^{{-{_f(alpha)}t}}u(t))(t), "
                f"t={[_f(t) for t in t_pts]}"
            )
            data = {
                "mode": mode, "a": a, "b": None,
                "results": results, "alpha": alpha,
            }

        return problem, data

    def _create_steps(self, data: dict) -> list[str]:
        """Generate per-point convolution evaluation steps.

        Args:
            data: Solution data with signal parameters and results.

        Returns:
            Steps showing each evaluation point.
        """
        steps: list[str] = []
        if data["mode"] == "rect_rect":
            steps.append(f"rect*rect: a={_f(data['a'])}, b={_f(data['b'])}")
        else:
            steps.append(
                f"rect*exp: w={_f(data['a'])}, alpha={_f(data['alpha'])}"
            )
        for t, val in data["results"]:
            steps.append(f"(f*g)({_f(t)})={_f(val)}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the convolution values at sample points.

        Args:
            data: Solution data.

        Returns:
            String with t:value pairs.
        """
        parts = [f"t={_f(t)}:{_f(val)}" for t, val in data["results"]]
        return ", ".join(parts)


# ===================================================================
# 2. Signal Correlation (tier 5)
# ===================================================================

@register
class CorrelationSignalGenerator(StepGenerator):
    """Compute discrete cross-correlation of two finite sequences.

    R_xy[k] = sum_n x[n] * y[n+k]. For finite-length signals,
    evaluate at specified lags.

    Difficulty scaling:
        Difficulty 1-3: length 3, evaluate at lag 0.
        Difficulty 4-6: length 4, evaluate at lags -1, 0, 1.
        Difficulty 7-8: length 5, evaluate at lags -2..2, find peak.

    Prerequisites:
        definite_integral.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "correlation_signal"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["definite_integral"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls signal length and lags.

        Returns:
            Short task description.
        """
        return "compute discrete cross-correlation"

    def _config(self, difficulty: int) -> tuple[int, list[int]]:
        """Map difficulty to signal length and lag values.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (signal_length, lags).
        """
        if difficulty <= 3:
            return 3, [0]
        if difficulty <= 6:
            return 4, [-1, 0, 1]
        return 5, [-2, -1, 0, 1, 2]

    def _correlate(self, x: list[float], y: list[float],
                   lag: int) -> float:
        """Compute cross-correlation at a given lag.

        Args:
            x: First signal.
            y: Second signal.
            lag: Lag value (y is shifted by lag).

        Returns:
            Correlation value rounded to 4 dp.
        """
        n = len(x)
        total = 0.0
        for i in range(n):
            j = i + lag
            if 0 <= j < len(y):
                total += x[i] * y[j]
        return round(total, 4)

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate two signals and compute cross-correlation.

        Args:
            difficulty: Controls signal length and lags.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        length, lags = self._config(difficulty)
        x = [round(self._rng.uniform(-2.0, 2.0), 2) for _ in range(length)]
        y = [round(self._rng.uniform(-2.0, 2.0), 2) for _ in range(length)]

        results = [(k, self._correlate(x, y, k)) for k in lags]
        peak_lag = max(results, key=lambda r: abs(r[1]))

        problem = f"R_xy[k], x={_fv(x)}, y={_fv(y)}, k={lags}"
        return problem, {
            "x": x, "y": y, "lags": lags, "results": results,
            "peak_lag": peak_lag,
            "show_peak": difficulty >= 7,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate per-lag correlation computation steps.

        Args:
            data: Solution data with signals and correlations.

        Returns:
            Steps showing each lag's correlation value.
        """
        steps: list[str] = [f"x={_fv(data['x'])}, y={_fv(data['y'])}"]
        for k, val in data["results"]:
            steps.append(f"R_xy[{k}]={_f(val)}")
        if data["show_peak"]:
            steps.append(
                f"peak at k={data['peak_lag'][0]}: {_f(data['peak_lag'][1])}"
            )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the correlation values.

        Args:
            data: Solution data.

        Returns:
            String with lag:value pairs.
        """
        parts = [f"k={k}:{_f(val)}" for k, val in data["results"]]
        return ", ".join(parts)


# ===================================================================
# 3. Nyquist Diagram (tier 6)
# ===================================================================

@register
class NyquistDiagramGenerator(StepGenerator):
    """Compute H(jw) at key frequencies for Nyquist diagram analysis.

    For a transfer function H(s) = K / (s + a) or
    H(s) = K / ((s + a)(s + b)), evaluate at w = 0, key frequencies,
    and w -> inf. Count encirclements of -1+0j.

    Difficulty scaling:
        Difficulty 1-3: first-order H(s) = K/(s+a), 3 frequencies.
        Difficulty 4-6: first-order, 4 frequencies.
        Difficulty 7-8: second-order H(s) = K/((s+a)(s+b)), 4 freqs.

    Prerequisites:
        complex_arithmetic.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "nyquist_diagram"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["complex_arithmetic"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls system order.

        Returns:
            Short task description.
        """
        return "compute H(jw) for Nyquist diagram"

    def _h_first_order(self, k: float, a: float,
                       w: float) -> tuple[float, float]:
        """Evaluate first-order transfer function at jw.

        H(jw) = K / (jw + a) = K * (a - jw) / (a^2 + w^2).

        Args:
            k: Gain.
            a: Pole location.
            w: Frequency.

        Returns:
            Complex value as (real, imag).
        """
        denom = a ** 2 + w ** 2
        if denom < 1e-10:
            return (0.0, 0.0)
        re = round(k * a / denom, 4)
        im = round(-k * w / denom, 4)
        return (re, im)

    def _h_second_order(self, k: float, a: float, b: float,
                        w: float) -> tuple[float, float]:
        """Evaluate second-order transfer function at jw.

        H(jw) = K / ((jw + a)(jw + b)).

        Args:
            k: Gain.
            a: First pole location.
            b: Second pole location.
            w: Frequency.

        Returns:
            Complex value as (real, imag).
        """
        # (jw + a)(jw + b) = (a*b - w^2) + j*w*(a+b)
        real_d = a * b - w ** 2
        imag_d = w * (a + b)
        denom = real_d ** 2 + imag_d ** 2
        if denom < 1e-10:
            return (0.0, 0.0)
        re = round(k * real_d / denom, 4)
        im = round(-k * imag_d / denom, 4)
        return (re, im)

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate transfer function and evaluate at key frequencies.

        Args:
            difficulty: Controls system order and frequency count.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        k = round(self._rng.uniform(1.0, 10.0), 2)
        a = round(self._rng.uniform(0.5, 5.0), 2)

        if difficulty <= 6:
            order = 1
            b = None
            n_freqs = 3 if difficulty <= 3 else 4
        else:
            order = 2
            b = round(self._rng.uniform(0.5, 5.0), 2)
            n_freqs = 4

        freqs = [0.0]
        for _ in range(n_freqs - 1):
            freqs.append(round(self._rng.uniform(0.1, 10.0), 2))
        freqs.sort()

        points = []
        for w in freqs:
            if order == 1:
                h = self._h_first_order(k, a, w)
            else:
                h = self._h_second_order(k, a, b, w)
            mag = round(math.sqrt(h[0] ** 2 + h[1] ** 2), 4)
            points.append({"w": w, "H": h, "mag": mag})

        # Simple encirclement check: does the curve pass left of -1?
        h_at_0 = points[0]["H"]
        encirclements = 0
        if h_at_0[0] < -1.0:
            encirclements = 1

        if order == 1:
            problem = f"Nyquist: H(s)={_f(k)}/(s+{_f(a)})"
        else:
            problem = f"Nyquist: H(s)={_f(k)}/((s+{_f(a)})(s+{_f(b)}))"

        return problem, {
            "k": k, "a": a, "b": b, "order": order,
            "points": points, "encirclements": encirclements,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate per-frequency H(jw) evaluation steps.

        Args:
            data: Solution data with frequency evaluations.

        Returns:
            Steps showing H at each frequency and encirclements.
        """
        steps: list[str] = []
        for p in data["points"]:
            steps.append(
                f"w={_f(p['w'])}: H={_cfmt(p['H'])}, |H|={_f(p['mag'])}"
            )
        steps.append(f"encirclements of -1: {data['encirclements']}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return key Nyquist diagram data.

        Args:
            data: Solution data.

        Returns:
            String with H(j0) and encirclement count.
        """
        h0 = data["points"][0]["H"]
        return (
            f"H(j0)={_cfmt(h0)}, "
            f"encirclements={data['encirclements']}"
        )


# ===================================================================
# 4. Bode Plot Compute (tier 5)
# ===================================================================

@register
class BodePlotComputeGenerator(StepGenerator):
    """Compute Bode plot magnitude and phase at key frequencies.

    For H(s) = K/(s/w0 + 1), compute |H(jw)| in dB = 20*log10(|H|)
    and phase = atan2(imag, real) at break and nearby frequencies.

    Difficulty scaling:
        Difficulty 1-3: first-order, 3 frequencies.
        Difficulty 4-6: first-order, 4 frequencies including w0.
        Difficulty 7-8: second-order (two real poles), 5 frequencies.

    Prerequisites:
        logarithm.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "bode_plot_compute"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["logarithm"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls system order.

        Returns:
            Short task description.
        """
        return "compute Bode plot magnitude and phase"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate transfer function and compute Bode data.

        Args:
            difficulty: Controls system order and frequency count.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        k = round(self._rng.uniform(1.0, 10.0), 2)
        w0 = round(self._rng.uniform(1.0, 100.0), 2)

        if difficulty <= 6:
            order = 1
            w1 = None
            if difficulty <= 3:
                freqs = [w0 / 10, w0, w0 * 10]
            else:
                freqs = [w0 / 10, w0 / 2, w0, w0 * 10]
        else:
            order = 2
            w1 = round(self._rng.uniform(1.0, 100.0), 2)
            freqs = [
                min(w0, w1) / 10,
                min(w0, w1),
                (w0 + w1) / 2,
                max(w0, w1),
                max(w0, w1) * 10,
            ]

        freqs = [round(f, 4) for f in freqs]
        bode_pts = []
        for w in freqs:
            if order == 1:
                # H(jw) = K / (1 + jw/w0)
                re = k / (1 + (w / w0) ** 2)
                im = -k * (w / w0) / (1 + (w / w0) ** 2)
            else:
                # H(jw) = K / ((1+jw/w0)(1+jw/w1))
                d1_re = 1.0
                d1_im = w / w0
                d2_re = 1.0
                d2_im = w / w1
                # product of denominators
                dr = d1_re * d2_re - d1_im * d2_im
                di = d1_re * d2_im + d1_im * d2_re
                denom = dr ** 2 + di ** 2
                re = k * dr / denom if denom > 1e-10 else 0.0
                im = -k * di / denom if denom > 1e-10 else 0.0

            mag = math.sqrt(re ** 2 + im ** 2)
            mag_db = round(20 * math.log10(mag) if mag > 1e-10 else -200, 4)
            phase_deg = round(math.degrees(math.atan2(im, re)), 4)
            bode_pts.append({
                "w": w, "mag_db": mag_db, "phase_deg": phase_deg,
            })

        if order == 1:
            problem = f"Bode: H(s)={_f(k)}/(s/{_f(w0)}+1)"
        else:
            problem = (
                f"Bode: H(s)={_f(k)}/((s/{_f(w0)}+1)(s/{_f(w1)}+1))"
            )

        return problem, {
            "k": k, "w0": w0, "w1": w1, "order": order,
            "bode_pts": bode_pts,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate per-frequency Bode computation steps.

        Args:
            data: Solution data with Bode points.

        Returns:
            Steps showing magnitude and phase at each frequency.
        """
        steps: list[str] = [f"K={_f(data['k'])}, w0={_f(data['w0'])}"]
        if data["w1"] is not None:
            steps[0] += f", w1={_f(data['w1'])}"
        for pt in data["bode_pts"]:
            steps.append(
                f"w={_f(pt['w'])}: |H|={_f(pt['mag_db'])}dB, "
                f"phase={_f(pt['phase_deg'])}deg"
            )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return Bode data at the break frequency.

        Args:
            data: Solution data.

        Returns:
            String with magnitude and phase at w0.
        """
        # Find the point closest to w0
        w0 = data["w0"]
        closest = min(data["bode_pts"], key=lambda p: abs(p["w"] - w0))
        return (
            f"|H(w0)|={_f(closest['mag_db'])}dB, "
            f"phase={_f(closest['phase_deg'])}deg"
        )


# ===================================================================
# 5. Signal Energy and Power (tier 4)
# ===================================================================

@register
class SignalEnergyPowerGenerator(StepGenerator):
    """Compute energy and power of discrete signals.

    Energy: E = sum |x[n]|^2. Power: P = E / N.
    Classify as energy signal (finite E) or power signal.

    Difficulty scaling:
        Difficulty 1-3: 4-element real signal.
        Difficulty 4-6: 6-element real signal.
        Difficulty 7-8: 8-element signal, compare two signals.

    Prerequisites:
        multiplication.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "signal_energy_power"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["multiplication"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls signal length.

        Returns:
            Short task description.
        """
        return "compute signal energy and average power"

    def _length(self, difficulty: int) -> int:
        """Map difficulty to signal length.

        Args:
            difficulty: Difficulty level.

        Returns:
            Signal length (4-8).
        """
        if difficulty <= 3:
            return 4
        if difficulty <= 6:
            return 6
        return 8

    def _compute_ep(self, x: list[float]) -> tuple[float, float]:
        """Compute energy and average power of a signal.

        Args:
            x: Signal samples.

        Returns:
            Tuple of (energy, average_power).
        """
        energy = round(sum(xi ** 2 for xi in x), 4)
        power = round(energy / len(x), 4)
        return energy, power

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate signal(s) and compute energy/power.

        Args:
            difficulty: Controls signal length and comparison.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        n = self._length(difficulty)
        x = [round(self._rng.uniform(-3.0, 3.0), 2) for _ in range(n)]
        e1, p1 = self._compute_ep(x)

        if difficulty >= 7:
            y = [round(self._rng.uniform(-3.0, 3.0), 2) for _ in range(n)]
            e2, p2 = self._compute_ep(y)
        else:
            y = None
            e2 = None
            p2 = None

        problem = f"E,P: x={_fv(x)}"
        if y is not None:
            problem += f", y={_fv(y)}"

        return problem, {
            "x": x, "e1": e1, "p1": p1,
            "y": y, "e2": e2, "p2": p2,
            "compare": difficulty >= 7,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate energy and power computation steps.

        Args:
            data: Solution data with energy and power values.

        Returns:
            Steps showing squared sum and division.
        """
        sq = "+".join(f"{_f(xi)}^2" for xi in data["x"])
        steps: list[str] = [
            f"E_x={sq}={_f(data['e1'])}",
            f"P_x={_f(data['e1'])}/{len(data['x'])}={_f(data['p1'])}",
        ]
        if data["compare"] and data["y"] is not None:
            sq_y = "+".join(f"{_f(yi)}^2" for yi in data["y"])
            steps.append(f"E_y={sq_y}={_f(data['e2'])}")
            steps.append(
                f"P_y={_f(data['e2'])}/{len(data['y'])}={_f(data['p2'])}"
            )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the energy and power values.

        Args:
            data: Solution data.

        Returns:
            String with energy and power.
        """
        ans = f"E={_f(data['e1'])}, P={_f(data['p1'])}"
        if data["compare"]:
            ans += f"; E_y={_f(data['e2'])}, P_y={_f(data['p2'])}"
        return ans


# ===================================================================
# 6. Modulation / Demodulation (tier 5)
# ===================================================================

@register
class ModulationDemodGenerator(StepGenerator):
    """Compute AM and FM modulation parameters.

    AM: modulation index m = A_m / A_c, bandwidth = 2*f_m.
    FM: frequency deviation delta_f = k_f * max|m(t)|,
    bandwidth (Carson's rule) BW = 2*(delta_f + f_m).

    Difficulty scaling:
        Difficulty 1-3: AM only, integer parameters.
        Difficulty 4-6: FM only, decimal parameters.
        Difficulty 7-8: Both AM and FM, compare bandwidths.

    Prerequisites:
        multiplication.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "modulation_demod"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["multiplication"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls modulation type.

        Returns:
            Short task description.
        """
        if difficulty >= 7:
            return "compute AM and FM modulation parameters"
        if difficulty <= 3:
            return "compute AM modulation parameters"
        return "compute FM modulation parameters"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate modulation parameters and compute bandwidth.

        Args:
            difficulty: Controls modulation type.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            a_c = float(self._rng.randint(1, 10))
            a_m = float(self._rng.randint(1, 10))
            f_m = float(self._rng.randint(1, 20)) * 1000
            mod_idx = round(a_m / a_c, 4)
            bw_am = round(2 * f_m, 4)
            problem = (
                f"AM: A_c={_f(a_c)}, A_m={_f(a_m)}, f_m={_f(f_m)}Hz"
            )
            return problem, {
                "mode": "am", "a_c": a_c, "a_m": a_m, "f_m": f_m,
                "mod_idx": mod_idx, "bw_am": bw_am,
                "k_f": None, "max_m": None, "delta_f": None, "bw_fm": None,
            }
        elif difficulty <= 6:
            f_m = round(self._rng.uniform(1, 20), 2) * 1000
            k_f = round(self._rng.uniform(1, 50), 2)
            max_m = round(self._rng.uniform(0.5, 5.0), 2)
            delta_f = round(k_f * max_m, 4)
            bw_fm = round(2 * (delta_f + f_m), 4)
            problem = (
                f"FM: k_f={_f(k_f)}, max|m|={_f(max_m)}, f_m={_f(f_m)}Hz"
            )
            return problem, {
                "mode": "fm", "f_m": f_m,
                "k_f": k_f, "max_m": max_m, "delta_f": delta_f,
                "bw_fm": bw_fm,
                "a_c": None, "a_m": None, "mod_idx": None, "bw_am": None,
            }
        else:
            a_c = round(self._rng.uniform(1, 10), 2)
            a_m = round(self._rng.uniform(1, 10), 2)
            f_m = round(self._rng.uniform(1, 20), 2) * 1000
            k_f = round(self._rng.uniform(1, 50), 2)
            max_m = a_m
            mod_idx = round(a_m / a_c, 4)
            bw_am = round(2 * f_m, 4)
            delta_f = round(k_f * max_m, 4)
            bw_fm = round(2 * (delta_f + f_m), 4)
            problem = (
                f"AM+FM: A_c={_f(a_c)}, A_m={_f(a_m)}, "
                f"f_m={_f(f_m)}Hz, k_f={_f(k_f)}"
            )
            return problem, {
                "mode": "both", "a_c": a_c, "a_m": a_m, "f_m": f_m,
                "mod_idx": mod_idx, "bw_am": bw_am,
                "k_f": k_f, "max_m": max_m, "delta_f": delta_f,
                "bw_fm": bw_fm,
            }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate modulation computation steps.

        Args:
            data: Solution data with modulation parameters.

        Returns:
            Steps showing index, deviation, and bandwidth.
        """
        steps: list[str] = []
        if data["mode"] in ("am", "both"):
            steps.append(
                f"AM: m={_f(data['a_m'])}/{_f(data['a_c'])}"
                f"={_f(data['mod_idx'])}"
            )
            steps.append(f"BW_AM=2*{_f(data['f_m'])}={_f(data['bw_am'])}Hz")
        if data["mode"] in ("fm", "both"):
            steps.append(
                f"FM: delta_f={_f(data['k_f'])}*{_f(data['max_m'])}"
                f"={_f(data['delta_f'])}"
            )
            steps.append(
                f"BW_FM=2*({_f(data['delta_f'])}+{_f(data['f_m'])})"
                f"={_f(data['bw_fm'])}Hz"
            )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the computed bandwidth(s).

        Args:
            data: Solution data.

        Returns:
            String with bandwidth values.
        """
        if data["mode"] == "am":
            return f"m={_f(data['mod_idx'])}, BW={_f(data['bw_am'])}Hz"
        if data["mode"] == "fm":
            return (
                f"delta_f={_f(data['delta_f'])}, BW={_f(data['bw_fm'])}Hz"
            )
        return (
            f"BW_AM={_f(data['bw_am'])}Hz, BW_FM={_f(data['bw_fm'])}Hz"
        )


# ===================================================================
# 7. Matched Filter (tier 6)
# ===================================================================

@register
class MatchedFilterGenerator(StepGenerator):
    """Compute matched filter output for a known signal.

    h[n] = s*[N-1-n] (time-reversed conjugate of signal).
    Output y = conv(x, h). SNR is maximised at n = N-1.

    Difficulty scaling:
        Difficulty 1-3: length 3 real signal, compute h and peak.
        Difficulty 4-6: length 4 real signal, compute full output.
        Difficulty 7-8: length 4 complex signal, compute h and peak.

    Prerequisites:
        complex_arithmetic.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "matched_filter"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["complex_arithmetic"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls signal type.

        Returns:
            Short task description.
        """
        return "compute matched filter impulse response and peak output"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate signal and compute matched filter.

        Args:
            difficulty: Controls signal length and type.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            n = 3
            s = [round(self._rng.uniform(-2.0, 2.0), 2) for _ in range(n)]
            is_complex = False
        elif difficulty <= 6:
            n = 4
            s = [round(self._rng.uniform(-2.0, 2.0), 2) for _ in range(n)]
            is_complex = False
        else:
            n = 4
            s = [(round(self._rng.uniform(-2.0, 2.0), 2),
                  round(self._rng.uniform(-2.0, 2.0), 2))
                 for _ in range(n)]
            is_complex = True

        # Matched filter: h[k] = s*[N-1-k]
        if is_complex:
            h = [(s[n - 1 - k][0], -s[n - 1 - k][1]) for k in range(n)]
            # Peak output: sum |s[k]|^2
            peak = round(sum(
                s[k][0] ** 2 + s[k][1] ** 2 for k in range(n)
            ), 4)
            s_str = "[" + ",".join(_cfmt(c) for c in s) + "]"
            h_str = "[" + ",".join(_cfmt(c) for c in h) + "]"
        else:
            h = [s[n - 1 - k] for k in range(n)]
            peak = round(sum(sk ** 2 for sk in s), 4)
            s_str = _fv(s)
            h_str = _fv(h)

        problem = f"matched filter, s={s_str}"
        return problem, {
            "s": s, "h": h, "peak": peak, "n": n,
            "is_complex": is_complex,
            "s_str": s_str, "h_str": h_str,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate matched filter computation steps.

        Args:
            data: Solution data with signal and filter.

        Returns:
            Steps showing filter construction and peak output.
        """
        steps: list[str] = [
            f"s={data['s_str']}, N={data['n']}",
            f"h[k]=s*[N-1-k]={data['h_str']}",
        ]
        if data["is_complex"]:
            terms = "+".join(
                f"|{_cfmt(c)}|^2" for c in data["s"]
            )
        else:
            terms = "+".join(f"{_f(v)}^2" for v in data["s"])
        steps.append(f"peak=sum|s|^2={terms}={_f(data['peak'])}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the matched filter and peak SNR output.

        Args:
            data: Solution data.

        Returns:
            String with filter and peak value.
        """
        return f"h={data['h_str']}, peak={_f(data['peak'])}"


# ===================================================================
# 8. Sigma-Delta Modulation (tier 5)
# ===================================================================

@register
class SigmaDeltaGenerator(StepGenerator):
    """Trace 1-bit sigma-delta modulator operation.

    Loop: integrator += (input - feedback), quantise to +1/-1,
    feedback = quantised output. Trace 5-8 clock cycles.

    Difficulty scaling:
        Difficulty 1-3: constant input, 5 cycles.
        Difficulty 4-6: step input (changes midway), 6 cycles.
        Difficulty 7-8: sinusoidal input samples, 8 cycles.

    Prerequisites:
        summation.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "sigma_delta"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["summation"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls input type and cycle count.

        Returns:
            Short task description.
        """
        return "trace 1-bit sigma-delta modulator output"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate input signal and trace sigma-delta operation.

        Args:
            difficulty: Controls input type and cycle count.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            n_cycles = 5
            inp_val = round(self._rng.uniform(-0.8, 0.8), 2)
            inputs = [inp_val] * n_cycles
        elif difficulty <= 6:
            n_cycles = 6
            val1 = round(self._rng.uniform(-0.8, 0.8), 2)
            val2 = round(self._rng.uniform(-0.8, 0.8), 2)
            inputs = [val1] * 3 + [val2] * 3
        else:
            n_cycles = 8
            inputs = [
                round(0.5 * math.sin(2 * math.pi * i / n_cycles), 4)
                for i in range(n_cycles)
            ]

        integrator = 0.0
        feedback = 0.0
        trace = []
        bitstream = []
        for i in range(n_cycles):
            error = round(inputs[i] - feedback, 4)
            integrator = round(integrator + error, 4)
            output = 1.0 if integrator >= 0 else -1.0
            feedback = output
            trace.append({
                "cycle": i, "input": inputs[i], "error": error,
                "integrator": integrator, "output": output,
            })
            bitstream.append(int(output))

        inp_str = _fv(inputs[:min(5, len(inputs))])
        if len(inputs) > 5:
            inp_str = inp_str[:-1] + ",...]"
        problem = f"sigma-delta 1-bit, input={_fv(inputs)}"
        return problem, {
            "inputs": inputs, "trace": trace, "bitstream": bitstream,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate per-cycle sigma-delta trace steps.

        Args:
            data: Solution data with cycle trace.

        Returns:
            Steps showing each cycle's integrator state and output.
        """
        steps: list[str] = []
        for t in data["trace"]:
            steps.append(
                f"c{t['cycle']}: in={_f(t['input'])}, "
                f"err={_f(t['error'])}, "
                f"int={_f(t['integrator'])}, "
                f"out={int(t['output'])}"
            )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the output bitstream.

        Args:
            data: Solution data.

        Returns:
            String representation of the bitstream.
        """
        return "[" + ",".join(str(b) for b in data["bitstream"]) + "]"
