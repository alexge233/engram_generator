"""Signal processing task generators.

6 generators across tiers 5-6 covering DFT computation, sampling theorem,
FIR filtering, Z-transform, transfer functions, and frequency response.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

def _cexp(re: float, im: float) -> tuple[float, float]:
    """Compute e^(re + j*im) = e^re * (cos(im) + j*sin(im)).

    Args:
        re: Real part of the exponent.
        im: Imaginary part of the exponent.

    Returns:
        Tuple of (real_part, imaginary_part).
    """
    mag = math.exp(re)
    return (round(mag * math.cos(im), 4), round(mag * math.sin(im), 4))


def _cmul(a: tuple[float, float], b: tuple[float, float]) -> tuple[float, float]:
    """Multiply two complex numbers (a_re, a_im) * (b_re, b_im).

    Args:
        a: First complex number as (real, imag).
        b: Second complex number as (real, imag).

    Returns:
        Product as (real, imag) rounded to 4 dp.
    """
    re = round(a[0] * b[0] - a[1] * b[1], 4)
    im = round(a[0] * b[1] + a[1] * b[0], 4)
    return (re, im)


def _cadd(a: tuple[float, float], b: tuple[float, float]) -> tuple[float, float]:
    """Add two complex numbers.

    Args:
        a: First complex number as (real, imag).
        b: Second complex number as (real, imag).

    Returns:
        Sum as (real, imag) rounded to 4 dp.
    """
    return (round(a[0] + b[0], 4), round(a[1] + b[1], 4))


def _cabs(c: tuple[float, float]) -> float:
    """Compute magnitude of a complex number.

    Args:
        c: Complex number as (real, imag).

    Returns:
        Magnitude rounded to 4 dp.
    """
    return round(math.sqrt(c[0] ** 2 + c[1] ** 2), 4)


def _cfmt(c: tuple[float, float]) -> str:
    """Format a complex number as a string.

    Args:
        c: Complex number as (real, imag).

    Returns:
        Formatted string like '1.5 + 2.3j' or '1.5 - 2.3j'.
    """
    re, im = c
    if im >= 0:
        return f"{re} + {im}j"
    return f"{re} - {abs(im)}j"


# ---------------------------------------------------------------------------
# 1. DFT Compute (tier 6)
# ---------------------------------------------------------------------------

@register
class DftComputeGenerator(StepGenerator):
    """Compute the Discrete Fourier Transform of a small signal.

    For a signal x[0..N-1] with N=4, compute X[k] = sum_{n=0}^{N-1}
    x[n] * e^{-j*2*pi*k*n/N}. Shows each twiddle factor term.

    Difficulty scaling:
        Difficulty 1-3: integer signal values in [0, 5], compute X[0].
        Difficulty 4-6: signal values in [-5, 9], compute X[0..1].
        Difficulty 7-8: signal values in [-9, 9], compute X[k] for random k.

    Prerequisites:
        complex_arithmetic, summation.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "dft_compute"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["complex_arithmetic", "summation"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute DFT of a small signal"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a DFT computation problem with N=4.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        n_pts = 4
        lo = 0 if difficulty <= 3 else -5
        hi = 5 if difficulty <= 3 else 9
        signal = [self._rng.randint(lo, hi) for _ in range(n_pts)]

        if difficulty <= 3:
            k = 0
        elif difficulty <= 6:
            k = self._rng.randint(0, 1)
        else:
            k = self._rng.randint(0, n_pts - 1)

        # Compute X[k] = sum x[n] * e^{-j*2*pi*k*n/N}
        terms = []
        result = (0.0, 0.0)
        for n in range(n_pts):
            angle = -2.0 * math.pi * k * n / n_pts
            twiddle = (round(math.cos(angle), 4), round(math.sin(angle), 4))
            xn = (float(signal[n]), 0.0)
            term = _cmul(xn, twiddle)
            terms.append({"n": n, "twiddle": twiddle, "term": term})
            result = _cadd(result, term)

        sig_str = ", ".join(str(v) for v in signal)
        return (
            f"X[k] = \\sum_{{n=0}}^{{{n_pts - 1}}} x[n] e^{{-j2\\pi kn/{n_pts}}}. "
            f"x = [{sig_str}], compute X[{k}].",
            {
                "signal": signal,
                "N": n_pts,
                "k": k,
                "terms": terms,
                "result": result,
            },
        )

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps for DFT computation.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing each twiddle factor product and the sum.
        """
        steps = []
        k = data["k"]
        for t in data["terms"]:
            n = t["n"]
            tw = t["twiddle"]
            term = t["term"]
            steps.append(
                f"n={n}: x[{n}]*W^({k}*{n}) = "
                f"{data['signal'][n]}*({_cfmt(tw)}) = {_cfmt(term)}"
            )
        steps.append(f"X[{k}] = {_cfmt(data['result'])}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the DFT coefficient.

        Args:
            data: Solution data dict.

        Returns:
            X[k] as a formatted complex string.
        """
        return f"X[{data['k']}] = {_cfmt(data['result'])}"


# ---------------------------------------------------------------------------
# 2. Sampling Theorem (tier 5)
# ---------------------------------------------------------------------------

@register
class SamplingTheoremGenerator(StepGenerator):
    """Determine Nyquist rate and check sampling sufficiency.

    Given a signal with maximum frequency f_max, compute the Nyquist
    rate f_N = 2 * f_max and determine whether a given sampling rate
    fs is sufficient (fs >= f_N).

    Difficulty scaling:
        Difficulty 1-3: f_max in [100, 1000] Hz, fs is clearly sufficient.
        Difficulty 4-6: f_max in [500, 10000] Hz, fs may or may not suffice.
        Difficulty 7-8: f_max in [1000, 50000] Hz, borderline cases.

    Prerequisites:
        multiplication.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "sampling_theorem"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

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
        return "determine Nyquist rate and check sampling sufficiency"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a sampling theorem problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            f_max = self._rng.randint(1, 10) * 100
            fs = f_max * self._rng.randint(2, 4)
        elif difficulty <= 6:
            f_max = self._rng.randint(5, 100) * 100
            multiplier = self._rng.choice([1.5, 1.8, 2.0, 2.5, 3.0])
            fs = int(f_max * multiplier)
        else:
            f_max = self._rng.randint(10, 500) * 100
            multiplier = self._rng.choice([1.2, 1.5, 1.8, 2.0, 2.2, 3.0])
            fs = int(f_max * multiplier)

        nyquist = 2 * f_max
        sufficient = fs >= nyquist

        return (
            f"Signal with f_{{max}} = {f_max} Hz, sampled at f_s = {fs} Hz. "
            f"Is f_s sufficient?",
            {
                "f_max": f_max,
                "fs": fs,
                "nyquist": nyquist,
                "sufficient": sufficient,
            },
        )

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps for sampling theorem.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing Nyquist rate and comparison.
        """
        return [
            f"Nyquist rate: f_N = 2 * f_max = 2 * {data['f_max']} = {data['nyquist']} Hz",
            f"f_s = {data['fs']} Hz, f_N = {data['nyquist']} Hz",
            f"f_s >= f_N? {data['fs']} >= {data['nyquist']} -> {data['sufficient']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return Nyquist rate and sufficiency.

        Args:
            data: Solution data dict.

        Returns:
            Nyquist rate and whether sampling is sufficient.
        """
        status = "sufficient" if data["sufficient"] else "insufficient"
        return f"f_N = {data['nyquist']} Hz, {status}"


# ---------------------------------------------------------------------------
# 3. FIR Filter (tier 5)
# ---------------------------------------------------------------------------

@register
class FirFilterGenerator(StepGenerator):
    """Apply an FIR filter to a short signal.

    Compute y[n] = sum_{k=0}^{M} h[k]*x[n-k] for a 3-5 tap filter
    on a short input signal. Uses zero-padding for out-of-bounds indices.

    Difficulty scaling:
        Difficulty 1-3: 3 taps, signal length 4, integer coefficients.
        Difficulty 4-6: 4 taps, signal length 5, small decimal coefficients.
        Difficulty 7-8: 5 taps, signal length 6, wider coefficient range.

    Prerequisites:
        convolution.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "fir_filter"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["convolution"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "apply FIR filter to a signal"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an FIR filtering problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            n_taps = 3
            sig_len = 4
            h = [self._rng.randint(1, 3) for _ in range(n_taps)]
            x = [self._rng.randint(0, 5) for _ in range(sig_len)]
        elif difficulty <= 6:
            n_taps = 4
            sig_len = 5
            h = [round(self._rng.uniform(-2.0, 2.0), 1) for _ in range(n_taps)]
            x = [self._rng.randint(-3, 5) for _ in range(sig_len)]
        else:
            n_taps = 5
            sig_len = 6
            h = [round(self._rng.uniform(-3.0, 3.0), 1) for _ in range(n_taps)]
            x = [self._rng.randint(-5, 9) for _ in range(sig_len)]

        # Pick an output index to compute
        n_out = self._rng.randint(0, sig_len - 1)

        # Compute y[n_out] = sum h[k]*x[n_out - k]
        terms = []
        y_val = 0.0
        for k in range(n_taps):
            idx = n_out - k
            x_val = x[idx] if 0 <= idx < sig_len else 0
            prod = round(h[k] * x_val, 4)
            terms.append({"k": k, "idx": idx, "x_val": x_val,
                          "h_val": h[k], "prod": prod})
            y_val += prod
        y_val = round(y_val, 4)

        h_str = ", ".join(str(v) for v in h)
        x_str = ", ".join(str(v) for v in x)
        return (
            f"y[n] = \\sum_{{k=0}}^{{{n_taps - 1}}} h[k] x[n-k]. "
            f"h = [{h_str}], x = [{x_str}]. Compute y[{n_out}].",
            {
                "h": h,
                "x": x,
                "n_out": n_out,
                "terms": terms,
                "y_val": y_val,
            },
        )

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps for FIR filtering.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing each tap product and the sum.
        """
        steps = []
        n_out = data["n_out"]
        for t in data["terms"]:
            k = t["k"]
            idx = t["idx"]
            x_label = f"x[{idx}]={t['x_val']}" if 0 <= idx else f"x[{idx}]=0"
            steps.append(
                f"k={k}: h[{k}]*x[{n_out}-{k}] = "
                f"{t['h_val']}*{t['x_val']} = {t['prod']}"
            )
        parts = " + ".join(str(t["prod"]) for t in data["terms"])
        steps.append(f"y[{n_out}] = {parts} = {data['y_val']}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the filter output value.

        Args:
            data: Solution data dict.

        Returns:
            y[n] value as a string.
        """
        return f"y[{data['n_out']}] = {data['y_val']}"


# ---------------------------------------------------------------------------
# 4. Z-Transform (tier 6)
# ---------------------------------------------------------------------------

@register
class ZTransformGenerator(StepGenerator):
    """Compute the Z-transform of a finite sequence.

    For a finite sequence x[0..N-1], compute X(z) = sum_{n=0}^{N-1}
    x[n]*z^{-n}. Produces a polynomial in z^{-1}.

    Difficulty scaling:
        Difficulty 1-3: sequence length 3, integer values in [1, 5].
        Difficulty 4-6: sequence length 4, values in [-5, 9].
        Difficulty 7-8: sequence length 5, values in [-9, 9].

    Prerequisites:
        exponentiation, summation.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "z_transform"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["exponentiation", "summation"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute Z-transform of a finite sequence"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Z-transform problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            length = 3
            seq = [self._rng.randint(1, 5) for _ in range(length)]
        elif difficulty <= 6:
            length = 4
            seq = [self._rng.randint(-5, 9) for _ in range(length)]
        else:
            length = 5
            seq = [self._rng.randint(-9, 9) for _ in range(length)]
            # Avoid all-zero sequence
            if all(v == 0 for v in seq):
                seq[0] = 1

        # Build polynomial terms
        terms = []
        for n, val in enumerate(seq):
            if val != 0:
                if n == 0:
                    terms.append(f"{val}")
                else:
                    terms.append(f"{val}*z^(-{n})")

        poly_str = " + ".join(terms).replace("+ -", "- ")

        seq_str = ", ".join(str(v) for v in seq)
        return (
            f"X(z) = \\sum_{{n=0}}^{{{length - 1}}} x[n] z^{{-n}}. "
            f"x = [{seq_str}].",
            {
                "seq": seq,
                "length": length,
                "poly_str": poly_str,
            },
        )

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps for Z-transform.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing each term and the final polynomial.
        """
        steps = []
        for n, val in enumerate(data["seq"]):
            steps.append(f"n={n}: x[{n}]*z^(-{n}) = {val}*z^(-{n})")
        steps.append(f"X(z) = {data['poly_str']}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the Z-transform polynomial.

        Args:
            data: Solution data dict.

        Returns:
            Polynomial in z^{-1} as a string.
        """
        return f"X(z) = {data['poly_str']}"


# ---------------------------------------------------------------------------
# 5. Transfer Function (Signal) (tier 6)
# ---------------------------------------------------------------------------

@register
class TransferFunctionSignalGenerator(StepGenerator):
    """Compute H(z) for a simple difference equation.

    Given y[n] = a*y[n-1] + b*x[n], derive H(z) = Y(z)/X(z) = b/(1 - a*z^{-1}).

    Difficulty scaling:
        Difficulty 1-3: a in {0.25, 0.5}, b in {1, 2}.
        Difficulty 4-6: a in [-0.9, 0.9], b in [0.5, 3.0].
        Difficulty 7-8: second-order: y[n] = a1*y[n-1] + a2*y[n-2] + b*x[n].

    Prerequisites:
        z_transform.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "transfer_function_signal"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["z_transform"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute H(z) from a difference equation"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a transfer function problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            a1 = self._rng.choice([0.25, 0.5, 0.75])
            a2 = 0.0
            b = self._rng.choice([1, 2])
            order = 1
        elif difficulty <= 6:
            a1 = round(self._rng.uniform(-0.9, 0.9), 2)
            a2 = 0.0
            b = round(self._rng.uniform(0.5, 3.0), 2)
            order = 1
        else:
            a1 = round(self._rng.uniform(-0.8, 0.8), 2)
            a2 = round(self._rng.uniform(-0.5, 0.5), 2)
            b = round(self._rng.uniform(0.5, 3.0), 2)
            order = 2

        if order == 1:
            eq_str = f"y[n] = {a1}*y[n-1] + {b}*x[n]"
            num = f"{b}"
            den = f"1 - {a1}*z^(-1)"
            h_str = f"{b}/(1 - {a1}*z^(-1))"
        else:
            eq_str = (f"y[n] = {a1}*y[n-1] + {a2}*y[n-2] + {b}*x[n]")
            num = f"{b}"
            den = f"1 - {a1}*z^(-1) - {a2}*z^(-2)"
            h_str = f"{b}/(1 - {a1}*z^(-1) - {a2}*z^(-2))"

        return (
            f"{eq_str}. Compute H(z) = Y(z)/X(z).",
            {
                "a1": a1,
                "a2": a2,
                "b": b,
                "order": order,
                "num": num,
                "den": den,
                "h_str": h_str,
            },
        )

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps for transfer function derivation.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing Z-transform application and rearrangement.
        """
        steps = []
        if data["order"] == 1:
            steps.append(
                f"Z-transform: Y(z) = {data['a1']}*z^(-1)*Y(z) + {data['b']}*X(z)"
            )
            steps.append(
                f"Y(z)*(1 - {data['a1']}*z^(-1)) = {data['b']}*X(z)"
            )
        else:
            steps.append(
                f"Z-transform: Y(z) = {data['a1']}*z^(-1)*Y(z) + "
                f"{data['a2']}*z^(-2)*Y(z) + {data['b']}*X(z)"
            )
            steps.append(
                f"Y(z)*(1 - {data['a1']}*z^(-1) - {data['a2']}*z^(-2)) "
                f"= {data['b']}*X(z)"
            )
        steps.append(f"H(z) = {data['h_str']}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the transfer function.

        Args:
            data: Solution data dict.

        Returns:
            H(z) as a string.
        """
        return f"H(z) = {data['h_str']}"


# ---------------------------------------------------------------------------
# 6. Frequency Response (tier 6)
# ---------------------------------------------------------------------------

@register
class FrequencyResponseGenerator(StepGenerator):
    """Evaluate |H(e^{jw})| at w = 0, pi/2, pi for a first-order system.

    Given H(z) = b/(1 - a*z^{-1}), substitute z = e^{jw} and compute
    the magnitude at the three test frequencies.

    Difficulty scaling:
        Difficulty 1-3: a in {0.25, 0.5}, b = 1.
        Difficulty 4-6: a in [-0.9, 0.9], b in [0.5, 3.0].
        Difficulty 7-8: second-order H(z), wider coefficient range.

    Prerequisites:
        transfer_function_signal.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "frequency_response"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["transfer_function_signal"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "evaluate frequency response magnitude at w = 0, pi/2, pi"

    def _eval_first_order(self, a: float, b: float,
                          w: float) -> tuple[tuple[float, float], float]:
        """Evaluate H(e^{jw}) = b/(1 - a*e^{-jw}) for first order.

        Args:
            a: Feedback coefficient.
            b: Numerator gain.
            w: Angular frequency in radians.

        Returns:
            Tuple of (denominator_complex, magnitude).
        """
        # denominator = 1 - a*e^{-jw} = 1 - a*(cos(w) - j*sin(w))
        den_re = round(1.0 - a * math.cos(w), 4)
        den_im = round(a * math.sin(w), 4)
        den_mag = math.sqrt(den_re ** 2 + den_im ** 2)
        mag = round(abs(b) / den_mag, 4) if den_mag > 1e-10 else 0.0
        return ((den_re, den_im), mag)

    def _eval_second_order(self, a1: float, a2: float, b: float,
                           w: float) -> tuple[tuple[float, float], float]:
        """Evaluate H(e^{jw}) for second-order system.

        H(z) = b / (1 - a1*z^{-1} - a2*z^{-2}).

        Args:
            a1: First feedback coefficient.
            a2: Second feedback coefficient.
            b: Numerator gain.
            w: Angular frequency in radians.

        Returns:
            Tuple of (denominator_complex, magnitude).
        """
        # den = 1 - a1*e^{-jw} - a2*e^{-j2w}
        den_re = round(1.0 - a1 * math.cos(w) - a2 * math.cos(2 * w), 4)
        den_im = round(a1 * math.sin(w) + a2 * math.sin(2 * w), 4)
        den_mag = math.sqrt(den_re ** 2 + den_im ** 2)
        mag = round(abs(b) / den_mag, 4) if den_mag > 1e-10 else 0.0
        return ((den_re, den_im), mag)

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a frequency response evaluation problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        freqs = [("0", 0.0), ("pi/2", math.pi / 2), ("pi", math.pi)]

        if difficulty <= 3:
            a1 = self._rng.choice([0.25, 0.5])
            a2 = 0.0
            b = 1.0
            order = 1
        elif difficulty <= 6:
            a1 = round(self._rng.uniform(-0.9, 0.9), 2)
            a2 = 0.0
            b = round(self._rng.uniform(0.5, 3.0), 2)
            order = 1
        else:
            a1 = round(self._rng.uniform(-0.8, 0.8), 2)
            a2 = round(self._rng.uniform(-0.5, 0.5), 2)
            b = round(self._rng.uniform(0.5, 3.0), 2)
            order = 2

        results = []
        for label, w in freqs:
            if order == 1:
                den, mag = self._eval_first_order(a1, b, w)
            else:
                den, mag = self._eval_second_order(a1, a2, b, w)
            results.append({"label": label, "w": w, "den": den, "mag": mag})

        if order == 1:
            h_str = f"H(z) = {b}/(1 - {a1}*z^(-1))"
        else:
            h_str = f"H(z) = {b}/(1 - {a1}*z^(-1) - {a2}*z^(-2))"

        return (
            f"{h_str}. Evaluate |H(e^{{jw}})| at w = 0, pi/2, pi.",
            {
                "a1": a1,
                "a2": a2,
                "b": b,
                "order": order,
                "h_str": h_str,
                "results": results,
            },
        )

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps for frequency response evaluation.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing denominator and magnitude at each frequency.
        """
        steps = []
        for r in data["results"]:
            den = r["den"]
            steps.append(
                f"w={r['label']}: den = {_cfmt(den)}, "
                f"|H| = {r['mag']}"
            )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the frequency response magnitudes.

        Args:
            data: Solution data dict.

        Returns:
            Magnitudes at the three test frequencies.
        """
        parts = ", ".join(
            f"|H(e^j{r['label']})| = {r['mag']}"
            for r in data["results"]
        )
        return parts
