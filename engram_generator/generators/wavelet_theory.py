"""Wavelet theory generators.

6 generators across tiers 5-6 covering Haar wavelet decomposition
and reconstruction, multiresolution analysis, wavelet energy,
filter banks, and wavelet thresholding for denoising.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


# ═══════════════════════════════════════════════════════════════════
# HELPER UTILITIES
# ═══════════════════════════════════════════════════════════════════

def _fmt(x: float) -> str:
    """Format a float to 4 decimal places, stripping trailing zeros.

    Args:
        x: Value to format.

    Returns:
        Formatted string with up to 4 decimal places.
    """
    return f"{round(x, 4):.4f}".rstrip("0").rstrip(".")


def _signal_str(signal: list[float]) -> str:
    """Format a signal as a compact string.

    Args:
        signal: List of signal values.

    Returns:
        String like '[1.5, -0.25, 3.0, 0.5]'.
    """
    return "[" + ", ".join(_fmt(x) for x in signal) + "]"


# ═══════════════════════════════════════════════════════════════════
# 1. HAAR WAVELET DECOMPOSE (tier 5)
# ═══════════════════════════════════════════════════════════════════

@register
class HaarWaveletDecomposeGenerator(StepGenerator):
    """Decompose a signal using the Haar wavelet transform.

    Computes approximation coefficients a_k = (x[2k] + x[2k+1]) / 2
    and detail coefficients d_k = (x[2k] - x[2k+1]) / 2 for each
    level. Supports multi-level decomposition.

    Difficulty scaling:
        Difficulty 1-3: 4-sample signal, 1 level.
        Difficulty 4-6: 8-sample signal, 2 levels.
        Difficulty 7-8: 8-sample signal, 3 levels.

    Prerequisites:
        division (tier 1).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "haar_wavelet_decompose"

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
            difficulty: Controls signal length and decomposition depth.

        Returns:
            Task description string.
        """
        return "decompose signal using Haar wavelet transform"

    def _haar_one_level(self, signal: list[float]) -> tuple[list[float], list[float]]:
        """Perform one level of Haar decomposition.

        Args:
            signal: Input signal (even length).

        Returns:
            Tuple of (approximation_coeffs, detail_coeffs).
        """
        n = len(signal) // 2
        approx = [round((signal[2 * k] + signal[2 * k + 1]) / 2, 4) for k in range(n)]
        detail = [round((signal[2 * k] - signal[2 * k + 1]) / 2, 4) for k in range(n)]
        return approx, detail

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Haar decomposition problem.

        Args:
            difficulty: Controls signal length and levels.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            n = 4
            levels = 1
        elif difficulty <= 6:
            n = 8
            levels = 2
        else:
            n = 8
            levels = 3

        signal = [round(self._rng.randint(-10, 10) + self._rng.random(), 4)
                  for _ in range(n)]
        # Simplify to integers for cleaner arithmetic
        signal = [float(self._rng.randint(-10, 10)) for _ in range(n)]

        all_details: list[list[float]] = []
        current = list(signal)
        for _ in range(levels):
            if len(current) < 2:
                break
            approx, detail = self._haar_one_level(current)
            all_details.append(detail)
            current = approx

        problem = (
            f"Signal x = {_signal_str(signal)}. "
            f"Haar decomposition, {levels} level(s)."
        )
        return problem, {
            "signal": signal, "levels": levels,
            "all_details": all_details, "final_approx": current,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Haar decomposition steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing each decomposition level.
        """
        steps = [f"input signal: {_signal_str(data['signal'])}"]
        current = data["signal"]
        for level, detail in enumerate(data["all_details"]):
            n = len(current) // 2
            approx = [round((current[2 * k] + current[2 * k + 1]) / 2, 4)
                      for k in range(n)]
            steps.append(
                f"level {level + 1}: a = {_signal_str(approx)}, "
                f"d = {_signal_str(detail)}"
            )
            current = approx
        steps.append(f"final approximation: {_signal_str(data['final_approx'])}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the decomposition result.

        Args:
            data: Solution data.

        Returns:
            Final approximation and all detail coefficients.
        """
        parts = [f"approx={_signal_str(data['final_approx'])}"]
        for i, d in enumerate(data["all_details"]):
            parts.append(f"d{i + 1}={_signal_str(d)}")
        return ", ".join(parts)


# ═══════════════════════════════════════════════════════════════════
# 2. HAAR RECONSTRUCT (tier 5)
# ═══════════════════════════════════════════════════════════════════

@register
class HaarReconstructGenerator(StepGenerator):
    """Reconstruct a signal from Haar wavelet coefficients.

    Given approximation a_k and detail d_k coefficients, reconstructs
    x[2k] = a_k + d_k, x[2k+1] = a_k - d_k. Supports multi-level
    reconstruction.

    Difficulty scaling:
        Difficulty 1-3: 2 approx + 2 detail -> 4-sample signal.
        Difficulty 4-6: 2 levels (final 2 approx + 2 detail levels).
        Difficulty 7-8: 3 levels reconstruction.

    Prerequisites:
        haar_wavelet_decompose (tier 5).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "haar_reconstruct"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["haar_wavelet_decompose"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls reconstruction depth.

        Returns:
            Task description string.
        """
        return "reconstruct signal from Haar wavelet coefficients"

    def _reconstruct_one_level(self, approx: list[float],
                                detail: list[float]) -> list[float]:
        """Reconstruct one level of Haar transform.

        Args:
            approx: Approximation coefficients.
            detail: Detail coefficients.

        Returns:
            Reconstructed signal (double length).
        """
        result: list[float] = []
        for a, d in zip(approx, detail):
            result.append(round(a + d, 4))
            result.append(round(a - d, 4))
        return result

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Haar reconstruction problem.

        Args:
            difficulty: Controls number of levels.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            levels = 1
            final_approx = [float(self._rng.randint(-5, 5)) for _ in range(2)]
            all_details = [
                [float(self._rng.randint(-5, 5)) for _ in range(2)]
            ]
        elif difficulty <= 6:
            levels = 2
            final_approx = [float(self._rng.randint(-5, 5)) for _ in range(2)]
            all_details = [
                [float(self._rng.randint(-5, 5)) for _ in range(2)],
                [float(self._rng.randint(-5, 5)) for _ in range(4)],
            ]
        else:
            levels = 3
            final_approx = [float(self._rng.randint(-3, 3))]
            all_details = [
                [float(self._rng.randint(-3, 3))],
                [float(self._rng.randint(-3, 3)) for _ in range(2)],
                [float(self._rng.randint(-3, 3)) for _ in range(4)],
            ]

        # Reconstruct level by level
        current = list(final_approx)
        intermediates: list[list[float]] = [list(current)]
        for detail in all_details:
            current = self._reconstruct_one_level(current, detail)
            intermediates.append(list(current))

        det_strs = ", ".join(
            f"d{i + 1}={_signal_str(d)}" for i, d in enumerate(all_details)
        )
        problem = (
            f"Haar coefficients: approx={_signal_str(final_approx)}, "
            f"{det_strs}. Reconstruct signal ({levels} level(s))."
        )
        return problem, {
            "final_approx": final_approx,
            "all_details": all_details,
            "intermediates": intermediates,
            "reconstructed": current,
            "levels": levels,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate reconstruction steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing each reconstruction level.
        """
        steps = [f"start: approx = {_signal_str(data['final_approx'])}"]
        current = data["final_approx"]
        for i, detail in enumerate(data["all_details"]):
            recon = self._reconstruct_one_level(current, detail)
            steps.append(
                f"level {i + 1}: x[2k] = a_k + d_k, x[2k+1] = a_k - d_k"
            )
            steps.append(f"  result: {_signal_str(recon)}")
            current = recon
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the reconstructed signal.

        Args:
            data: Solution data.

        Returns:
            Reconstructed signal.
        """
        return f"signal = {_signal_str(data['reconstructed'])}"


# ═══════════════════════════════════════════════════════════════════
# 3. MULTIRESOLUTION ANALYSIS (tier 6)
# ═══════════════════════════════════════════════════════════════════

@register
class MultiresolutionGenerator(StepGenerator):
    """Evaluate scaling function coefficients at different resolutions.

    Computes phi_{j,k}(x) = 2^{j/2} * phi(2^j * x - k) for the Haar
    scaling function phi(x) = 1 for x in [0,1), 0 otherwise. Evaluates
    at a specified point x.

    Difficulty scaling:
        Difficulty 1-3: j=0 or j=1, single evaluation.
        Difficulty 4-6: j=2, evaluate at fractional x.
        Difficulty 7-8: j=3, multiple evaluations.

    Prerequisites:
        exponentiation (tier 2).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "multiresolution"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["exponentiation"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls scale level.

        Returns:
            Task description string.
        """
        return "evaluate Haar scaling function at given resolution"

    def _haar_phi(self, x: float) -> float:
        """Evaluate the Haar scaling function.

        Args:
            x: Input value.

        Returns:
            1.0 if 0 <= x < 1, else 0.0.
        """
        if 0.0 <= x < 1.0:
            return 1.0
        return 0.0

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a multiresolution evaluation problem.

        Args:
            difficulty: Controls scale level j.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            j = self._rng.randint(0, 1)
        elif difficulty <= 6:
            j = 2
        else:
            j = 3

        # k must be valid: phi_{j,k} is supported on [k/2^j, (k+1)/2^j)
        max_k = 2 ** j - 1
        k = self._rng.randint(0, max_k)

        # Choose x: either inside or outside the support
        two_j = 2 ** j
        support_lo = k / two_j
        support_hi = (k + 1) / two_j

        if self._rng.random() < 0.7:
            # Inside support
            # Pick x in [support_lo, support_hi)
            frac = self._rng.randint(0, two_j - 1)
            x_val = round(support_lo + frac / (two_j * 4), 4)
            if x_val >= support_hi:
                x_val = round(support_lo + 0.001, 4)
        else:
            # Outside support
            x_val = round(support_hi + 0.1, 4)

        arg = round(two_j * x_val - k, 4)
        phi_val = self._haar_phi(arg)
        scale = round(math.pow(2, j / 2), 4)
        result = round(scale * phi_val, 4)

        problem = (
            f"Haar scaling: phi_{{j={j},k={k}}}(x) = 2^({j}/2) * phi(2^{j}*x - {k}). "
            f"Evaluate at x = {_fmt(x_val)}."
        )
        return problem, {
            "j": j, "k": k, "x": x_val,
            "two_j": two_j, "arg": arg,
            "scale": scale, "phi_val": phi_val,
            "result": result,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate multiresolution evaluation steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing the computation.
        """
        j = data["j"]
        return [
            f"j = {j}, k = {data['k']}, x = {_fmt(data['x'])}",
            f"2^{j} = {data['two_j']}",
            f"argument = 2^{j} * {_fmt(data['x'])} - {data['k']} = {_fmt(data['arg'])}",
            f"phi({_fmt(data['arg'])}) = {_fmt(data['phi_val'])} ({'in' if data['phi_val'] > 0 else 'outside'} [0,1))",
            f"scale = 2^({j}/2) = {_fmt(data['scale'])}",
            f"phi_{{{j},{data['k']}}}({_fmt(data['x'])}) = {_fmt(data['scale'])} * {_fmt(data['phi_val'])} = {_fmt(data['result'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the scaling function value.

        Args:
            data: Solution data.

        Returns:
            The evaluation result.
        """
        return f"phi_{{{data['j']},{data['k']}}}({_fmt(data['x'])}) = {_fmt(data['result'])}"


# ═══════════════════════════════════════════════════════════════════
# 4. WAVELET ENERGY (tier 5)
# ═══════════════════════════════════════════════════════════════════

@register
class WaveletEnergyGenerator(StepGenerator):
    """Compute energy distribution across wavelet scales.

    For each scale j, computes E_j = sum |d_{j,k}|^2. Verifies
    Parseval's relation: total energy = sum E_j + E_approx where
    E_approx = sum |a_k|^2.

    Difficulty scaling:
        Difficulty 1-3: 4-sample signal, 1 level.
        Difficulty 4-6: 8-sample signal, 2 levels.
        Difficulty 7-8: 8-sample signal, 3 levels.

    Prerequisites:
        summation (tier 3).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "wavelet_energy"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["summation"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls signal size and decomposition depth.

        Returns:
            Task description string.
        """
        return "compute wavelet energy at each scale"

    def _haar_one_level(self, signal: list[float]) -> tuple[list[float], list[float]]:
        """Perform one level of Haar decomposition.

        Args:
            signal: Input signal (even length).

        Returns:
            Tuple of (approximation_coeffs, detail_coeffs).
        """
        n = len(signal) // 2
        approx = [round((signal[2 * k] + signal[2 * k + 1]) / 2, 4) for k in range(n)]
        detail = [round((signal[2 * k] - signal[2 * k + 1]) / 2, 4) for k in range(n)]
        return approx, detail

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a wavelet energy problem.

        Args:
            difficulty: Controls signal length and levels.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            n = 4
            levels = 1
        elif difficulty <= 6:
            n = 8
            levels = 2
        else:
            n = 8
            levels = 3

        signal = [float(self._rng.randint(-8, 8)) for _ in range(n)]

        current = list(signal)
        detail_energies: list[float] = []
        all_details: list[list[float]] = []
        for _ in range(levels):
            if len(current) < 2:
                break
            approx, detail = self._haar_one_level(current)
            energy = round(sum(d * d for d in detail), 4)
            detail_energies.append(energy)
            all_details.append(detail)
            current = approx

        approx_energy = round(sum(a * a for a in current), 4)
        total_wavelet = round(sum(detail_energies) + approx_energy, 4)
        total_signal = round(sum(x * x for x in signal) / (2 ** levels), 4)

        problem = (
            f"Signal x = {_signal_str(signal)}. "
            f"Haar decomposition {levels} level(s). "
            f"Compute energy at each scale."
        )
        return problem, {
            "signal": signal, "levels": levels,
            "all_details": all_details,
            "final_approx": current,
            "detail_energies": detail_energies,
            "approx_energy": approx_energy,
            "total_wavelet": total_wavelet,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate energy computation steps.

        Args:
            data: Solution data.

        Returns:
            Steps computing energy at each scale.
        """
        steps = [f"signal: {_signal_str(data['signal'])}"]
        for i, (detail, energy) in enumerate(
            zip(data["all_details"], data["detail_energies"])
        ):
            steps.append(
                f"level {i + 1}: d = {_signal_str(detail)}, "
                f"E_{i + 1} = sum|d|^2 = {_fmt(energy)}"
            )
        steps.append(
            f"approx energy: E_a = sum|a|^2 = {_fmt(data['approx_energy'])}"
        )
        steps.append(
            f"total = {' + '.join(_fmt(e) for e in data['detail_energies'])} + "
            f"{_fmt(data['approx_energy'])} = {_fmt(data['total_wavelet'])}"
        )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the energy distribution.

        Args:
            data: Solution data.

        Returns:
            Energy at each scale and total.
        """
        parts = [f"E_{i + 1}={_fmt(e)}" for i, e in enumerate(data["detail_energies"])]
        parts.append(f"E_approx={_fmt(data['approx_energy'])}")
        parts.append(f"total={_fmt(data['total_wavelet'])}")
        return ", ".join(parts)


# ═══════════════════════════════════════════════════════════════════
# 5. FILTER BANK (tier 6)
# ═══════════════════════════════════════════════════════════════════

@register
class FilterBankGenerator(StepGenerator):
    """Compute conjugate mirror filter and apply to a signal.

    Given low-pass filter h[n], computes the high-pass conjugate
    mirror filter g[n] = (-1)^n * h[N-1-n], then applies both
    filters to a signal via convolution and downsampling.

    Difficulty scaling:
        Difficulty 1-3: Haar filter h = [1/sqrt(2), 1/sqrt(2)], 4-sample signal.
        Difficulty 4-6: Daubechies D4 filter (4 taps), 6-sample signal.
        Difficulty 7-8: D4 filter, 8-sample signal.

    Prerequisites:
        multiplication (tier 1).
    """

    _HAAR_H = [round(1.0 / math.sqrt(2), 4), round(1.0 / math.sqrt(2), 4)]

    _DB4_H = [
        round((1 + math.sqrt(3)) / (4 * math.sqrt(2)), 4),
        round((3 + math.sqrt(3)) / (4 * math.sqrt(2)), 4),
        round((3 - math.sqrt(3)) / (4 * math.sqrt(2)), 4),
        round((1 - math.sqrt(3)) / (4 * math.sqrt(2)), 4),
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "filter_bank"

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
            difficulty: Controls filter and signal complexity.

        Returns:
            Task description string.
        """
        return "compute conjugate mirror filter and apply filter bank"

    def _compute_highpass(self, h: list[float]) -> list[float]:
        """Compute high-pass conjugate mirror filter.

        g[n] = (-1)^n * h[N-1-n] where N = len(h).

        Args:
            h: Low-pass filter coefficients.

        Returns:
            High-pass filter coefficients.
        """
        n_len = len(h)
        g = [round((-1) ** n * h[n_len - 1 - n], 4) for n in range(n_len)]
        return g

    def _apply_filter(self, signal: list[float], filt: list[float]) -> list[float]:
        """Apply filter to signal and downsample by 2.

        Computes y[k] = sum_n h[n] * x[2k - n] with periodic extension.

        Args:
            signal: Input signal.
            filt: Filter coefficients.

        Returns:
            Filtered and downsampled signal.
        """
        sig_len = len(signal)
        filt_len = len(filt)
        out_len = sig_len // 2
        result: list[float] = []
        for k in range(out_len):
            val = 0.0
            for n in range(filt_len):
                idx = (2 * k - n) % sig_len
                val += filt[n] * signal[idx]
            result.append(round(val, 4))
        return result

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a filter bank problem.

        Args:
            difficulty: Controls filter type and signal length.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            h = list(self._HAAR_H)
            sig_len = 4
            filt_name = "Haar"
        elif difficulty <= 6:
            h = list(self._DB4_H)
            sig_len = 6
            filt_name = "Daubechies D4"
        else:
            h = list(self._DB4_H)
            sig_len = 8
            filt_name = "Daubechies D4"

        g = self._compute_highpass(h)
        signal = [float(self._rng.randint(-5, 5)) for _ in range(sig_len)]

        low = self._apply_filter(signal, h)
        high = self._apply_filter(signal, g)

        problem = (
            f"Low-pass h = {_signal_str(h)} ({filt_name}). "
            f"Signal x = {_signal_str(signal)}. "
            f"Compute g[n] and apply filter bank."
        )
        return problem, {
            "h": h, "g": g, "filt_name": filt_name,
            "signal": signal, "low": low, "high": high,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate filter bank computation steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing filter derivation and application.
        """
        return [
            f"low-pass h = {_signal_str(data['h'])}",
            f"g[n] = (-1)^n * h[N-1-n]",
            f"high-pass g = {_signal_str(data['g'])}",
            f"apply h to signal, downsample: low = {_signal_str(data['low'])}",
            f"apply g to signal, downsample: high = {_signal_str(data['high'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the filter bank output.

        Args:
            data: Solution data.

        Returns:
            Low-pass and high-pass subbands.
        """
        return f"low={_signal_str(data['low'])}, high={_signal_str(data['high'])}"


# ═══════════════════════════════════════════════════════════════════
# 6. THRESHOLDING (tier 5)
# ═══════════════════════════════════════════════════════════════════

@register
class ThresholdingGenerator(StepGenerator):
    """Apply wavelet thresholding for signal denoising.

    Given detail coefficients and a threshold T, applies either
    hard thresholding (d'_k = d_k if |d_k| > T, else 0) or soft
    thresholding (d'_k = sign(d_k)*(|d_k|-T) if |d_k| > T, else 0).

    Difficulty scaling:
        Difficulty 1-3: 4 coefficients, hard threshold only.
        Difficulty 4-6: 6 coefficients, hard or soft threshold.
        Difficulty 7-8: 8 coefficients, compare hard vs soft.

    Prerequisites:
        multiplication (tier 1).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "thresholding"

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
            difficulty: Controls coefficient count and threshold type.

        Returns:
            Task description string.
        """
        return "apply wavelet thresholding for denoising"

    def _hard_threshold(self, coeffs: list[float], t: float) -> list[float]:
        """Apply hard thresholding.

        Args:
            coeffs: Detail coefficients.
            t: Threshold value.

        Returns:
            Thresholded coefficients.
        """
        return [round(c if abs(c) > t else 0.0, 4) for c in coeffs]

    def _soft_threshold(self, coeffs: list[float], t: float) -> list[float]:
        """Apply soft thresholding.

        Args:
            coeffs: Detail coefficients.
            t: Threshold value.

        Returns:
            Thresholded coefficients.
        """
        result: list[float] = []
        for c in coeffs:
            if abs(c) > t:
                sign = 1.0 if c > 0 else -1.0
                result.append(round(sign * (abs(c) - t), 4))
            else:
                result.append(0.0)
        return result

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a thresholding problem.

        Args:
            difficulty: Controls number of coefficients and threshold type.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            n = 4
            mode = "hard"
        elif difficulty <= 6:
            n = 6
            mode = self._rng.choice(["hard", "soft"])
        else:
            n = 8
            mode = "both"

        coeffs = [round(self._rng.uniform(-5.0, 5.0), 4) for _ in range(n)]
        threshold = round(self._rng.uniform(0.5, 3.0), 4)

        hard_result = self._hard_threshold(coeffs, threshold)
        soft_result = self._soft_threshold(coeffs, threshold)

        n_zeroed_hard = sum(1 for c in hard_result if c == 0.0)
        n_zeroed_soft = sum(1 for c in soft_result if c == 0.0)

        if mode == "both":
            mode_desc = "hard and soft"
        else:
            mode_desc = mode

        problem = (
            f"Detail coefficients d = {_signal_str(coeffs)}. "
            f"Threshold T = {_fmt(threshold)}. "
            f"Apply {mode_desc} thresholding."
        )
        return problem, {
            "coeffs": coeffs, "threshold": threshold, "mode": mode,
            "hard_result": hard_result, "soft_result": soft_result,
            "n_zeroed_hard": n_zeroed_hard, "n_zeroed_soft": n_zeroed_soft,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate thresholding steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing coefficient-by-coefficient thresholding.
        """
        steps = [
            f"coefficients: {_signal_str(data['coeffs'])}",
            f"threshold T = {_fmt(data['threshold'])}",
        ]
        mode = data["mode"]
        if mode in ("hard", "both"):
            steps.append("hard: keep d_k if |d_k| > T, else 0")
            steps.append(f"hard result: {_signal_str(data['hard_result'])}")
            steps.append(f"hard: {data['n_zeroed_hard']} coefficients zeroed")
        if mode in ("soft", "both"):
            steps.append("soft: sign(d_k)*(|d_k|-T) if |d_k| > T, else 0")
            steps.append(f"soft result: {_signal_str(data['soft_result'])}")
            steps.append(f"soft: {data['n_zeroed_soft']} coefficients zeroed")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the thresholded coefficients.

        Args:
            data: Solution data.

        Returns:
            Thresholded coefficient string.
        """
        mode = data["mode"]
        if mode == "hard":
            return f"hard: {_signal_str(data['hard_result'])}"
        elif mode == "soft":
            return f"soft: {_signal_str(data['soft_result'])}"
        return (
            f"hard: {_signal_str(data['hard_result'])}, "
            f"soft: {_signal_str(data['soft_result'])}"
        )
