"""Harmonic analysis generators.

10 generators across tiers 5-7 covering Fourier series, Parseval's
theorem, convolution theorem, windowed Fourier, Haar wavelets, spectral
density, Laplace inversion, Hilbert transform, sampling reconstruction,
and spectral leakage.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


# ═══════════════════════════════════════════════════════════════════
# HELPER UTILITIES
# ═══════════════════════════════════════════════════════════════════

def _cmul(a: tuple[float, float], b: tuple[float, float]) -> tuple[float, float]:
    """Multiply two complex numbers.

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


def _cabs_sq(c: tuple[float, float]) -> float:
    """Compute squared magnitude of a complex number.

    Args:
        c: Complex number as (real, imag).

    Returns:
        |c|^2 rounded to 4 dp.
    """
    return round(c[0] ** 2 + c[1] ** 2, 4)


def _cfmt(c: tuple[float, float]) -> str:
    """Format a complex number as a string.

    Args:
        c: Complex number as (real, imag).

    Returns:
        Formatted string like ``1.5 + 2.3j``.
    """
    re, im = c
    if im >= 0:
        return f"{re} + {im}j"
    return f"{re} - {abs(im)}j"


def _sinc(x: float) -> float:
    """Compute normalised sinc: sin(pi*x)/(pi*x).

    Args:
        x: Input value.

    Returns:
        sinc(x) rounded to 4 dp.
    """
    if abs(x) < 1e-10:
        return 1.0
    return round(math.sin(math.pi * x) / (math.pi * x), 4)


# ═══════════════════════════════════════════════════════════════════
# 1. FOURIER SERIES COMPUTE (tier 6)
# ═══════════════════════════════════════════════════════════════════

@register
class FourierSeriesComputeGenerator(StepGenerator):
    """Compute Fourier coefficients for simple periodic functions.

    Given a periodic function (square wave, sawtooth, triangle),
    compute a_0, a_n, b_n for specific harmonics using standard
    formulas.

    Difficulty scaling:
        Difficulty 1-3: square wave, first harmonic only.
        Difficulty 4-6: sawtooth, first two harmonics.
        Difficulty 7-8: triangle wave, first three harmonics.

    Prerequisites:
        fourier_coefficient (tier 6).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "fourier_series_compute"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["fourier_coefficient"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls waveform type.

        Returns:
            Task description string.
        """
        return "compute Fourier series coefficients of periodic function"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Fourier series problem.

        Args:
            difficulty: Controls waveform and number of harmonics.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        amp = self._rng.randint(1, 4)

        if difficulty <= 3:
            wave = "square"
            n_harmonics = 1
            # Square wave: b_n = 4A/(n*pi) for odd n, 0 for even
            a0 = 0.0
            coeffs = []
            for n in range(1, n_harmonics + 1):
                a_n = 0.0
                b_n = round(4 * amp / (n * math.pi), 4) if n % 2 == 1 else 0.0
                coeffs.append({"n": n, "a_n": a_n, "b_n": b_n})
        elif difficulty <= 6:
            wave = "sawtooth"
            n_harmonics = 2
            # Sawtooth: b_n = -2A/(n*pi) * (-1)^n
            a0 = 0.0
            coeffs = []
            for n in range(1, n_harmonics + 1):
                a_n = 0.0
                b_n = round(-2 * amp / (n * math.pi) * ((-1) ** n), 4)
                coeffs.append({"n": n, "a_n": a_n, "b_n": b_n})
        else:
            wave = "triangle"
            n_harmonics = 3
            # Triangle: b_n = 8A/(n^2*pi^2) * (-1)^((n-1)/2) for odd n
            a0 = 0.0
            coeffs = []
            for n in range(1, n_harmonics + 1):
                a_n = 0.0
                if n % 2 == 1:
                    b_n = round(8 * amp / ((n ** 2) * (math.pi ** 2))
                               * ((-1) ** ((n - 1) // 2)), 4)
                else:
                    b_n = 0.0
                coeffs.append({"n": n, "a_n": a_n, "b_n": b_n})

        problem = (
            f"Compute Fourier coefficients of {wave} wave, "
            f"amplitude {amp}, first {n_harmonics} harmonic(s)."
        )
        return problem, {
            "wave": wave, "amp": amp, "a0": a0,
            "coeffs": coeffs, "n_harmonics": n_harmonics,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Fourier coefficient computation steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing each coefficient.
        """
        steps = [f"waveform: {data['wave']}, amplitude A = {data['amp']}"]
        steps.append(f"a_0 = {data['a0']}")
        for c in data["coeffs"]:
            steps.append(f"n={c['n']}: a_{c['n']} = {c['a_n']}, b_{c['n']} = {c['b_n']}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the Fourier coefficients.

        Args:
            data: Solution data.

        Returns:
            Summary of coefficients.
        """
        parts = [f"a_0={data['a0']}"]
        for c in data["coeffs"]:
            parts.append(f"b_{c['n']}={c['b_n']}")
        return ", ".join(parts)


# ═══════════════════════════════════════════════════════════════════
# 2. PARSEVAL'S THEOREM (tier 6)
# ═══════════════════════════════════════════════════════════════════

@register
class ParsevalTheoremGenerator(StepGenerator):
    """Verify Parseval's theorem for Fourier coefficients.

    Checks (1/T)*integral|f|^2 dt = sum|c_n|^2 for a signal with
    known Fourier coefficients. Uses discrete approximation.

    Difficulty scaling:
        Difficulty 1-3: 2 coefficients.
        Difficulty 4-6: 3 coefficients.
        Difficulty 7-8: 4 coefficients.

    Prerequisites:
        fourier_series_compute (tier 6).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "parseval_theorem"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["fourier_series_compute"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls number of coefficients.

        Returns:
            Task description string.
        """
        return "verify Parseval's theorem for Fourier coefficients"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Parseval verification problem.

        Args:
            difficulty: Controls number of terms.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            n_terms = 2
        elif difficulty <= 6:
            n_terms = 3
        else:
            n_terms = 4

        # Generate coefficients c_n as (real, imag)
        coeffs = []
        for _ in range(n_terms):
            re = round(self._rng.uniform(-3, 3), 4)
            im = round(self._rng.uniform(-3, 3), 4)
            coeffs.append((re, im))

        # |c_n|^2
        energies = [_cabs_sq(c) for c in coeffs]
        total = round(sum(energies), 4)

        coeff_str = ", ".join(_cfmt(c) for c in coeffs)
        problem = (
            f"Fourier coefficients: c = [{coeff_str}]. "
            f"Verify Parseval: sum|c_n|^2 = signal energy."
        )
        return problem, {
            "coeffs": coeffs, "energies": energies, "total": total,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Parseval verification steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing each |c_n|^2 and the sum.
        """
        steps = []
        for i, (c, e) in enumerate(zip(data["coeffs"], data["energies"])):
            steps.append(f"|c_{i}|^2 = {c[0]}^2 + {c[1]}^2 = {e}")
        steps.append(f"sum|c_n|^2 = {data['total']}")
        steps.append(f"Parseval: signal energy = {data['total']}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the total energy.

        Args:
            data: Solution data.

        Returns:
            Signal energy.
        """
        return f"energy = {data['total']}"


# ═══════════════════════════════════════════════════════════════════
# 3. CONVOLUTION THEOREM (tier 6)
# ═══════════════════════════════════════════════════════════════════

@register
class ConvolutionTheoremGenerator(StepGenerator):
    """Apply the convolution theorem: F{f*g} = F{f} . F{g}.

    Given DFT coefficients of two signals, compute the DFT of their
    convolution by pointwise multiplication.

    Difficulty scaling:
        Difficulty 1-3: 2-point DFT, real coefficients.
        Difficulty 4-6: 3-point DFT, real coefficients.
        Difficulty 7-8: 4-point DFT, complex coefficients.

    Prerequisites:
        fourier_series_compute (tier 6).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "convolution_theorem"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["fourier_series_compute"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls DFT size.

        Returns:
            Task description string.
        """
        return "compute DFT of convolution using convolution theorem"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a convolution theorem problem.

        Args:
            difficulty: Controls DFT length and complexity.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            n_pts = 2
            f_dft = [(float(self._rng.randint(-3, 3)), 0.0) for _ in range(n_pts)]
            g_dft = [(float(self._rng.randint(-3, 3)), 0.0) for _ in range(n_pts)]
        elif difficulty <= 6:
            n_pts = 3
            f_dft = [(float(self._rng.randint(-3, 3)), 0.0) for _ in range(n_pts)]
            g_dft = [(float(self._rng.randint(-3, 3)), 0.0) for _ in range(n_pts)]
        else:
            n_pts = 4
            f_dft = [(round(self._rng.uniform(-3, 3), 4),
                       round(self._rng.uniform(-3, 3), 4)) for _ in range(n_pts)]
            g_dft = [(round(self._rng.uniform(-3, 3), 4),
                       round(self._rng.uniform(-3, 3), 4)) for _ in range(n_pts)]

        # F{f*g}[k] = F{f}[k] * F{g}[k]
        conv_dft = [_cmul(f_dft[k], g_dft[k]) for k in range(n_pts)]

        f_str = ", ".join(_cfmt(c) for c in f_dft)
        g_str = ", ".join(_cfmt(c) for c in g_dft)
        problem = (
            f"F{{f}} = [{f_str}], F{{g}} = [{g_str}]. "
            f"Compute F{{f*g}}."
        )
        return problem, {
            "f_dft": f_dft, "g_dft": g_dft, "conv_dft": conv_dft,
            "n_pts": n_pts,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate convolution theorem steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing pointwise multiplication.
        """
        steps = ["convolution theorem: F{f*g}[k] = F{f}[k] * F{g}[k]"]
        for k in range(data["n_pts"]):
            f_k = _cfmt(data["f_dft"][k])
            g_k = _cfmt(data["g_dft"][k])
            r_k = _cfmt(data["conv_dft"][k])
            steps.append(f"k={k}: ({f_k}) * ({g_k}) = {r_k}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the convolution DFT.

        Args:
            data: Solution data.

        Returns:
            DFT of the convolution.
        """
        return "F{f*g} = [" + ", ".join(_cfmt(c) for c in data["conv_dft"]) + "]"


# ═══════════════════════════════════════════════════════════════════
# 4. WINDOWED FOURIER (tier 6)
# ═══════════════════════════════════════════════════════════════════

@register
class WindowedFourierGenerator(StepGenerator):
    """Apply a window function and compute DFT of the windowed signal.

    Applies rectangular or Hann window to a short signal segment,
    then computes the DFT of the windowed result.

    Difficulty scaling:
        Difficulty 1-3: rectangular window, 4-point signal.
        Difficulty 4-6: Hann window, 4-point signal.
        Difficulty 7-8: Hann window, 8-point signal.

    Prerequisites:
        complex_arithmetic (tier 4).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "windowed_fourier"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["complex_arithmetic"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls window type and signal length.

        Returns:
            Task description string.
        """
        return "apply window function and compute DFT"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a windowed Fourier problem.

        Args:
            difficulty: Controls window and signal length.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            n_pts = 4
            win_type = "rectangular"
        elif difficulty <= 6:
            n_pts = 4
            win_type = "hann"
        else:
            n_pts = 8
            win_type = "hann"

        signal = [self._rng.randint(-5, 5) for _ in range(n_pts)]

        # Window coefficients
        if win_type == "rectangular":
            window = [1.0] * n_pts
        else:
            window = [round(0.5 * (1 - math.cos(2 * math.pi * n / (n_pts - 1))), 4)
                      for n in range(n_pts)]

        windowed = [round(signal[i] * window[i], 4) for i in range(n_pts)]

        # DFT of windowed signal at k=0
        dft_k0 = (round(sum(windowed), 4), 0.0)

        sig_str = ", ".join(str(v) for v in signal)
        win_str = ", ".join(str(w) for w in window)
        problem = (
            f"Signal x = [{sig_str}]. "
            f"Window ({win_type}): w = [{win_str}]. "
            f"Compute DFT of windowed signal at k=0."
        )
        return problem, {
            "signal": signal, "window": window, "win_type": win_type,
            "windowed": windowed, "dft_k0": dft_k0,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate windowed Fourier steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing windowing and DFT.
        """
        steps = [f"window type: {data['win_type']}"]
        for i, (s, w, ws) in enumerate(zip(data["signal"], data["window"], data["windowed"])):
            steps.append(f"x[{i}]*w[{i}] = {s}*{w} = {ws}")
        steps.append(f"X[0] = sum(windowed) = {_cfmt(data['dft_k0'])}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the windowed DFT coefficient.

        Args:
            data: Solution data.

        Returns:
            DFT at k=0 of windowed signal.
        """
        return f"X[0] = {_cfmt(data['dft_k0'])}"


# ═══════════════════════════════════════════════════════════════════
# 5. HAAR WAVELET (tier 6)
# ═══════════════════════════════════════════════════════════════════

@register
class WaveletHaarGenerator(StepGenerator):
    """Compute Haar wavelet decomposition of a short signal.

    Decomposes a signal into approximation (average) and detail
    (difference) coefficients at one level.

    Difficulty scaling:
        Difficulty 1-3: length-4 signal, one level.
        Difficulty 4-6: length-4 signal, two levels.
        Difficulty 7-8: length-8 signal, one level.

    Prerequisites:
        summation (tier 3).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "wavelet_haar"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["summation"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls signal length and decomposition depth.

        Returns:
            Task description string.
        """
        return "compute Haar wavelet decomposition"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Haar wavelet problem.

        Args:
            difficulty: Controls signal length and levels.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            n_pts = 4
            levels = 1
        elif difficulty <= 6:
            n_pts = 4
            levels = 2
        else:
            n_pts = 8
            levels = 1

        signal = [float(self._rng.randint(-5, 5)) for _ in range(n_pts)]

        all_approx = []
        all_detail = []
        current = signal[:]
        for _ in range(levels):
            approx = []
            detail = []
            for i in range(0, len(current), 2):
                a = round((current[i] + current[i + 1]) / 2, 4)
                d = round((current[i] - current[i + 1]) / 2, 4)
                approx.append(a)
                detail.append(d)
            all_approx.append(approx)
            all_detail.append(detail)
            current = approx

        sig_str = ", ".join(str(v) for v in signal)
        problem = (
            f"Signal x = [{sig_str}]. "
            f"Compute Haar wavelet decomposition ({levels} level(s))."
        )
        return problem, {
            "signal": signal, "levels": levels,
            "all_approx": all_approx, "all_detail": all_detail,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Haar decomposition steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing approximation and detail at each level.
        """
        steps = [f"signal: {data['signal']}"]
        for lv in range(data["levels"]):
            a_str = ", ".join(str(v) for v in data["all_approx"][lv])
            d_str = ", ".join(str(v) for v in data["all_detail"][lv])
            steps.append(f"level {lv + 1} approx: [{a_str}]")
            steps.append(f"level {lv + 1} detail: [{d_str}]")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the wavelet coefficients.

        Args:
            data: Solution data.

        Returns:
            Final approximation and all detail coefficients.
        """
        final_a = data["all_approx"][-1]
        all_d = []
        for d in data["all_detail"]:
            all_d.extend(d)
        a_str = ", ".join(str(v) for v in final_a)
        d_str = ", ".join(str(v) for v in all_d)
        return f"approx=[{a_str}], detail=[{d_str}]"


# ═══════════════════════════════════════════════════════════════════
# 6. SPECTRAL DENSITY (tier 6)
# ═══════════════════════════════════════════════════════════════════

@register
class SpectralDensityGenerator(StepGenerator):
    """Compute power spectral density S(f) = |X(f)|^2.

    Given DFT coefficients, compute the power spectral density
    at each frequency bin.

    Difficulty scaling:
        Difficulty 1-3: 4-point DFT, real coefficients.
        Difficulty 4-6: 4-point DFT, complex coefficients.
        Difficulty 7-8: 8-point DFT, complex coefficients.

    Prerequisites:
        complex_arithmetic (tier 4).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "spectral_density"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["complex_arithmetic"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls DFT size and complexity.

        Returns:
            Task description string.
        """
        return "compute power spectral density from DFT coefficients"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a spectral density problem.

        Args:
            difficulty: Controls DFT length.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            n_pts = 4
            dft = [(float(self._rng.randint(-5, 5)), 0.0) for _ in range(n_pts)]
        elif difficulty <= 6:
            n_pts = 4
            dft = [(round(self._rng.uniform(-5, 5), 4),
                    round(self._rng.uniform(-5, 5), 4)) for _ in range(n_pts)]
        else:
            n_pts = 8
            dft = [(round(self._rng.uniform(-5, 5), 4),
                    round(self._rng.uniform(-5, 5), 4)) for _ in range(n_pts)]

        psd = [_cabs_sq(c) for c in dft]

        dft_str = ", ".join(_cfmt(c) for c in dft)
        problem = f"DFT coefficients X = [{dft_str}]. Compute PSD S[k] = |X[k]|^2."
        return problem, {"dft": dft, "psd": psd, "n_pts": n_pts}

    def _create_steps(self, data: dict) -> list[str]:
        """Generate PSD computation steps.

        Args:
            data: Solution data.

        Returns:
            Steps computing |X[k]|^2 for each k.
        """
        steps = []
        for k in range(data["n_pts"]):
            c = data["dft"][k]
            steps.append(f"S[{k}] = |{_cfmt(c)}|^2 = {c[0]}^2 + {c[1]}^2 = {data['psd'][k]}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the PSD values.

        Args:
            data: Solution data.

        Returns:
            PSD array.
        """
        psd_str = ", ".join(str(v) for v in data["psd"])
        return f"S = [{psd_str}]"


# ═══════════════════════════════════════════════════════════════════
# 7. LAPLACE INVERSION (tier 7)
# ═══════════════════════════════════════════════════════════════════

@register
class LaplaceInversionGenerator(StepGenerator):
    """Compute inverse Laplace transform by partial fractions.

    Uses standard transform pairs: L^{-1}{1/(s-a)} = e^{at},
    L^{-1}{1/(s^2+w^2)} = sin(wt)/w, L^{-1}{s/(s^2+w^2)} = cos(wt).

    Difficulty scaling:
        Difficulty 1-3: single pole 1/(s-a).
        Difficulty 4-6: conjugate poles 1/(s^2+w^2).
        Difficulty 7-8: partial fraction decomposition of sum.

    Prerequisites:
        fourier_coefficient (tier 6).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "laplace_inversion"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["fourier_coefficient"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls transform complexity.

        Returns:
            Task description string.
        """
        return "compute inverse Laplace transform"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an inverse Laplace problem.

        Args:
            difficulty: Controls transform type.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            a = self._rng.randint(-3, 3)
            problem = f"L^{{-1}}{{1/(s - {a})}} = ?"
            return problem, {
                "type": "exponential", "a": a,
                "result": f"e^({a}t)" if a != 0 else "1",
            }
        elif difficulty <= 6:
            w = self._rng.randint(1, 5)
            kind = self._rng.choice(["sin", "cos"])
            if kind == "sin":
                problem = f"L^{{-1}}{{1/(s^2 + {w**2})}} = ?"
                result = f"sin({w}t)/{w}" if w != 1 else "sin(t)"
            else:
                problem = f"L^{{-1}}{{s/(s^2 + {w**2})}} = ?"
                result = f"cos({w}t)" if w != 1 else "cos(t)"
            return problem, {
                "type": kind, "w": w, "result": result,
            }
        else:
            a = self._rng.randint(-3, -1)
            w = self._rng.randint(1, 4)
            problem = (
                f"L^{{-1}}{{1/(s - {a}) + 1/(s^2 + {w**2})}} = ?"
            )
            sin_part = f"sin({w}t)/{w}" if w != 1 else "sin(t)"
            result = f"e^({a}t) + {sin_part}"
            return problem, {
                "type": "sum", "a": a, "w": w, "result": result,
            }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate inverse Laplace steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing transform pair identification.
        """
        if data["type"] == "exponential":
            return [
                f"standard pair: L^{{-1}}{{1/(s-a)}} = e^(at)",
                f"a = {data['a']}",
                f"result: {data['result']}",
            ]
        elif data["type"] in ("sin", "cos"):
            w = data["w"]
            if data["type"] == "sin":
                return [
                    f"standard pair: L^{{-1}}{{1/(s^2+w^2)}} = sin(wt)/w",
                    f"w = {w}",
                    f"result: {data['result']}",
                ]
            else:
                return [
                    f"standard pair: L^{{-1}}{{s/(s^2+w^2)}} = cos(wt)",
                    f"w = {w}",
                    f"result: {data['result']}",
                ]
        else:
            return [
                "linearity of inverse Laplace transform",
                f"L^{{-1}}{{1/(s-{data['a']})}} = e^({data['a']}t)",
                f"L^{{-1}}{{1/(s^2+{data['w']**2})}} = sin({data['w']}t)/{data['w']}",
                f"result: {data['result']}",
            ]

    def _create_answer(self, data: dict) -> str:
        """Return the inverse Laplace transform.

        Args:
            data: Solution data.

        Returns:
            Time-domain function.
        """
        return data["result"]


# ═══════════════════════════════════════════════════════════════════
# 8. HILBERT TRANSFORM (tier 7)
# ═══════════════════════════════════════════════════════════════════

@register
class HilbertTransformGenerator(StepGenerator):
    """Apply the Hilbert transform to simple sinusoidal signals.

    Uses known pairs: H{cos(wt)} = sin(wt), H{sin(wt)} = -cos(wt).
    Applies linearity for sums of sinusoids.

    Difficulty scaling:
        Difficulty 1-3: single cosine or sine.
        Difficulty 4-6: scaled sinusoid A*cos(wt) or A*sin(wt).
        Difficulty 7-8: sum of two sinusoids.

    Prerequisites:
        sin_cos_eval (tier 1).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "hilbert_transform"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["sin_cos_eval"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls signal complexity.

        Returns:
            Task description string.
        """
        return "apply Hilbert transform to sinusoidal signal"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Hilbert transform problem.

        Args:
            difficulty: Controls signal complexity.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            w = self._rng.randint(1, 5)
            func = self._rng.choice(["cos", "sin"])
            if func == "cos":
                signal = f"cos({w}t)"
                result = f"sin({w}t)"
            else:
                signal = f"sin({w}t)"
                result = f"-cos({w}t)"
            return f"H{{{signal}}} = ?", {
                "type": "single", "signal": signal, "result": result,
            }
        elif difficulty <= 6:
            w = self._rng.randint(1, 5)
            a = self._rng.randint(2, 5)
            func = self._rng.choice(["cos", "sin"])
            if func == "cos":
                signal = f"{a}*cos({w}t)"
                result = f"{a}*sin({w}t)"
            else:
                signal = f"{a}*sin({w}t)"
                result = f"-{a}*cos({w}t)"
            return f"H{{{signal}}} = ?", {
                "type": "scaled", "signal": signal, "result": result, "a": a,
            }
        else:
            w1 = self._rng.randint(1, 4)
            w2 = self._rng.randint(1, 4)
            while w2 == w1:
                w2 = self._rng.randint(1, 4)
            a1 = self._rng.randint(1, 3)
            a2 = self._rng.randint(1, 3)
            signal = f"{a1}*cos({w1}t) + {a2}*sin({w2}t)"
            result = f"{a1}*sin({w1}t) - {a2}*cos({w2}t)"
            return f"H{{{signal}}} = ?", {
                "type": "sum", "signal": signal, "result": result,
                "a1": a1, "a2": a2, "w1": w1, "w2": w2,
            }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Hilbert transform steps.

        Args:
            data: Solution data.

        Returns:
            Steps applying transform pairs.
        """
        steps = ["Hilbert transform pairs: H{cos(wt)} = sin(wt), H{sin(wt)} = -cos(wt)"]
        if data["type"] == "sum":
            steps.append(f"H{{{data['a1']}*cos({data['w1']}t)}} = {data['a1']}*sin({data['w1']}t)")
            steps.append(f"H{{{data['a2']}*sin({data['w2']}t)}} = -{data['a2']}*cos({data['w2']}t)")
            steps.append(f"by linearity: {data['result']}")
        else:
            steps.append(f"apply to {data['signal']}: {data['result']}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the Hilbert transform.

        Args:
            data: Solution data.

        Returns:
            Transformed signal.
        """
        return data["result"]


# ═══════════════════════════════════════════════════════════════════
# 9. SAMPLING RECONSTRUCTION (tier 5)
# ═══════════════════════════════════════════════════════════════════

@register
class SamplingReconstructionGenerator(StepGenerator):
    """Reconstruct a signal from samples using sinc interpolation.

    Computes x(t) = sum x[n]*sinc((t - nT)/T) at a given point t
    from a small set of samples.

    Difficulty scaling:
        Difficulty 1-3: 3 samples, reconstruct at t = sample point.
        Difficulty 4-6: 4 samples, reconstruct at t = midpoint.
        Difficulty 7-8: 5 samples, reconstruct at arbitrary t.

    Prerequisites:
        sin_cos_eval (tier 1).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "sampling_reconstruction"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["sin_cos_eval"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls sample count and target point.

        Returns:
            Task description string.
        """
        return "reconstruct signal from samples using sinc interpolation"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a sampling reconstruction problem.

        Args:
            difficulty: Controls complexity.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        t_period = 1.0  # Sampling period T = 1

        if difficulty <= 3:
            n_samples = 3
            samples = [float(self._rng.randint(-5, 5)) for _ in range(n_samples)]
            t_eval = float(self._rng.randint(0, n_samples - 1))
        elif difficulty <= 6:
            n_samples = 4
            samples = [float(self._rng.randint(-5, 5)) for _ in range(n_samples)]
            t_eval = round(self._rng.randint(0, n_samples - 2) + 0.5, 4)
        else:
            n_samples = 5
            samples = [float(self._rng.randint(-5, 5)) for _ in range(n_samples)]
            t_eval = round(self._rng.uniform(0.0, n_samples - 1), 4)

        # x(t) = sum x[n] * sinc((t - n*T)/T)
        terms = []
        result = 0.0
        for n in range(n_samples):
            s = _sinc((t_eval - n * t_period) / t_period)
            contribution = round(samples[n] * s, 4)
            terms.append({"n": n, "sinc": s, "contrib": contribution})
            result += contribution
        result = round(result, 4)

        samp_str = ", ".join(str(v) for v in samples)
        problem = (
            f"Samples x[n] = [{samp_str}], T = {t_period}. "
            f"Reconstruct x({t_eval}) using sinc interpolation."
        )
        return problem, {
            "samples": samples, "t_period": t_period, "t_eval": t_eval,
            "terms": terms, "result": result,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate reconstruction steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing each sinc term.
        """
        steps = [f"x(t) = sum x[n]*sinc((t - n*T)/T), t = {data['t_eval']}"]
        for t in data["terms"]:
            steps.append(
                f"n={t['n']}: x[{t['n']}]*sinc({round(data['t_eval'] - t['n'], 4)}) "
                f"= {data['samples'][t['n']]}*{t['sinc']} = {t['contrib']}"
            )
        steps.append(f"x({data['t_eval']}) = {data['result']}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the reconstructed value.

        Args:
            data: Solution data.

        Returns:
            Reconstructed signal value.
        """
        return f"x({data['t_eval']}) = {data['result']}"


# ═══════════════════════════════════════════════════════════════════
# 10. SPECTRAL LEAKAGE (tier 6)
# ═══════════════════════════════════════════════════════════════════

@register
class SpectralLeakageGenerator(StepGenerator):
    """Compute spectral leakage when signal frequency mismatches DFT bin.

    Generates a sinusoidal signal at a non-integer frequency relative
    to the DFT bins, computes the DFT, and shows energy spreading.

    Difficulty scaling:
        Difficulty 1-3: N=4, frequency offset 0.25 bins.
        Difficulty 4-6: N=4, frequency offset 0.5 bins.
        Difficulty 7-8: N=8, arbitrary offset.

    Prerequisites:
        complex_arithmetic (tier 4).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "spectral_leakage"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["complex_arithmetic"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls frequency offset and DFT size.

        Returns:
            Task description string.
        """
        return "compute spectral leakage from frequency mismatch"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a spectral leakage problem.

        Args:
            difficulty: Controls DFT size and offset.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            n_pts = 4
            offset = 0.25
        elif difficulty <= 6:
            n_pts = 4
            offset = 0.5
        else:
            n_pts = 8
            offset = round(self._rng.uniform(0.1, 0.9), 4)

        freq = 1.0 + offset  # Non-integer bin frequency

        # Generate signal x[n] = cos(2*pi*freq*n/N)
        signal = [round(math.cos(2 * math.pi * freq * n / n_pts), 4)
                  for n in range(n_pts)]

        # Compute DFT
        dft = []
        for k in range(n_pts):
            re = 0.0
            im = 0.0
            for n in range(n_pts):
                angle = -2 * math.pi * k * n / n_pts
                re += signal[n] * math.cos(angle)
                im += signal[n] * math.sin(angle)
            dft.append((round(re, 4), round(im, 4)))

        psd = [_cabs_sq(c) for c in dft]
        max_bin = psd.index(max(psd))
        total_energy = round(sum(psd), 4)
        main_lobe = round(psd[max_bin], 4)
        leakage = round(total_energy - main_lobe, 4)

        sig_str = ", ".join(str(v) for v in signal)
        problem = (
            f"Signal x[n] = cos(2*pi*{freq}*n/{n_pts}), N={n_pts}. "
            f"Compute DFT and identify spectral leakage."
        )
        return problem, {
            "signal": signal, "freq": freq, "n_pts": n_pts,
            "dft": dft, "psd": psd, "max_bin": max_bin,
            "total_energy": total_energy, "main_lobe": main_lobe,
            "leakage": leakage,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate spectral leakage steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing DFT, PSD, and leakage.
        """
        steps = [f"signal freq = {data['freq']} (non-integer bin)"]
        for k in range(data["n_pts"]):
            steps.append(f"X[{k}] = {_cfmt(data['dft'][k])}, |X[{k}]|^2 = {data['psd'][k]}")
        steps.append(f"max energy at bin {data['max_bin']}: {data['main_lobe']}")
        steps.append(f"total energy = {data['total_energy']}, leaked = {data['leakage']}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the leakage analysis.

        Args:
            data: Solution data.

        Returns:
            Main lobe bin and leakage amount.
        """
        return f"main bin={data['max_bin']}, leakage={data['leakage']}"
