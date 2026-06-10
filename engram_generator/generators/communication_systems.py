"""Communication systems task generators.

4 generators across tiers 4-5 covering AM modulation, uniform quantization,
mu-law companding, and QPSK constellation diagram detection.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


# ---------------------------------------------------------------------------
# 1. AM Modulation (tier 4)
# ---------------------------------------------------------------------------

@register
class AmModulationGenerator(StepGenerator):
    """Compute AM modulation parameters.

    s(t) = [1 + m*cos(2*pi*fm*t)] * cos(2*pi*fc*t). Given modulation
    index m, carrier frequency fc, and message frequency fm, compute
    peak amplitude, minimum amplitude, and bandwidth = 2*fm.

    Difficulty scaling:
        Difficulty 1-3: m in {0.25, 0.5, 0.75}, integer fm and fc.
        Difficulty 4-6: m in (0, 1.0], larger frequencies.
        Difficulty 7-8: m > 1 (overmodulation), wider range.

    Prerequisites:
        multiplication.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "am_modulation"

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
        return "compute AM modulation peak/min amplitude and bandwidth"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an AM modulation problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            m = self._rng.choice([0.25, 0.5, 0.75])
            fm = self._rng.randint(1, 5) * 100
            fc = self._rng.randint(5, 20) * 1000
        elif difficulty <= 6:
            m = round(self._rng.uniform(0.1, 1.0), 2)
            fm = self._rng.randint(1, 10) * 100
            fc = self._rng.randint(10, 50) * 1000
        else:
            m = round(self._rng.uniform(0.5, 1.5), 2)
            fm = self._rng.randint(5, 20) * 100
            fc = self._rng.randint(20, 100) * 1000

        peak = round(1 + m, 4)
        minimum = round(1 - m, 4)
        bandwidth = 2 * fm

        return (
            f"s(t) = [1 + m \\cos(2\\pi f_m t)] \\cos(2\\pi f_c t). "
            f"m = {m}, f_m = {fm} Hz, f_c = {fc} Hz.",
            {
                "m": m, "fm": fm, "fc": fc,
                "peak": peak, "minimum": minimum,
                "bandwidth": bandwidth,
            },
        )

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps for AM modulation.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing peak, min, and bandwidth.
        """
        return [
            f"peak amplitude = 1 + m = 1 + {data['m']} = {data['peak']}",
            f"min amplitude = 1 - m = 1 - {data['m']} = {data['minimum']}",
            f"bandwidth = 2*f_m = 2*{data['fm']} = {data['bandwidth']} Hz",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the AM modulation parameters.

        Args:
            data: Solution data dict.

        Returns:
            Peak, min, and bandwidth as a string.
        """
        return (
            f"peak={data['peak']}, min={data['minimum']}, "
            f"BW={data['bandwidth']} Hz"
        )


# ---------------------------------------------------------------------------
# 2. Quantization (tier 4)
# ---------------------------------------------------------------------------

@register
class QuantizationGenerator(StepGenerator):
    """Compute uniform quantizer parameters.

    step_size = (V_max - V_min) / 2^n. Quantization error bounds are
    +/- step/2. SNR_q = 6.02*n + 1.76 dB.

    Difficulty scaling:
        Difficulty 1-3: n in {2, 3}, V_max - V_min in {2, 4, 8}.
        Difficulty 4-6: n in {4, 5, 6}, wider voltage range.
        Difficulty 7-8: n in {7, 8}, asymmetric ranges.

    Prerequisites:
        division.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "quantization"

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
            Short task description.
        """
        return "compute uniform quantizer step size, error, and SNR"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a quantization problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            n_bits = self._rng.choice([2, 3])
            v_min = 0
            v_max = self._rng.choice([2, 4, 8])
        elif difficulty <= 6:
            n_bits = self._rng.choice([4, 5, 6])
            v_min = self._rng.choice([-2, -1, 0])
            v_max = self._rng.choice([2, 4, 5, 8])
        else:
            n_bits = self._rng.choice([7, 8])
            v_min = self._rng.randint(-5, -1)
            v_max = self._rng.randint(3, 10)

        levels = 2 ** n_bits
        v_range = v_max - v_min
        step_size = round(v_range / levels, 4)
        error_bound = round(step_size / 2, 4)
        snr_q = round(6.02 * n_bits + 1.76, 4)

        return (
            f"Uniform quantizer: V_{{min}} = {v_min}, V_{{max}} = {v_max}, "
            f"n = {n_bits} bits.",
            {
                "n_bits": n_bits, "v_min": v_min, "v_max": v_max,
                "levels": levels, "v_range": v_range,
                "step_size": step_size, "error_bound": error_bound,
                "snr_q": snr_q,
            },
        )

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps for quantization.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing levels, step size, error, and SNR.
        """
        return [
            f"levels = 2^{data['n_bits']} = {data['levels']}",
            f"step = ({data['v_max']} - {data['v_min']})/{data['levels']} "
            f"= {data['v_range']}/{data['levels']} = {data['step_size']}",
            f"error = +/- step/2 = +/- {data['error_bound']}",
            f"SNR_q = 6.02*{data['n_bits']} + 1.76 = {data['snr_q']} dB",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the quantization parameters.

        Args:
            data: Solution data dict.

        Returns:
            Step size, error bound, and SNR as a string.
        """
        return (
            f"step={data['step_size']}, error=+/-{data['error_bound']}, "
            f"SNR_q={data['snr_q']} dB"
        )


# ---------------------------------------------------------------------------
# 3. Companding (tier 5)
# ---------------------------------------------------------------------------

@register
class CompandingGenerator(StepGenerator):
    """Compute mu-law companding compression.

    F(x) = sign(x) * ln(1 + mu*|x|) / ln(1 + mu). Standard mu = 255.

    Difficulty scaling:
        Difficulty 1-3: mu = 255, |x| in {0.1, 0.2, ..., 0.9}.
        Difficulty 4-6: mu = 255, |x| includes negatives and small values.
        Difficulty 7-8: mu in {15, 100, 255}, wider input range.

    Prerequisites:
        logarithm.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "companding"

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
            Short task description.
        """
        return "compute mu-law compressed value"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a mu-law companding problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            mu = 255
            x = round(self._rng.choice([0.1, 0.2, 0.3, 0.4, 0.5,
                                         0.6, 0.7, 0.8, 0.9]), 1)
        elif difficulty <= 6:
            mu = 255
            x = round(self._rng.uniform(-0.9, 0.9), 2)
            if abs(x) < 0.01:
                x = 0.1
        else:
            mu = self._rng.choice([15, 100, 255])
            x = round(self._rng.uniform(-0.95, 0.95), 2)
            if abs(x) < 0.01:
                x = 0.1

        sign_x = 1 if x >= 0 else -1
        abs_x = abs(x)
        numerator = round(math.log(1 + mu * abs_x), 4)
        denominator = round(math.log(1 + mu), 4)
        compressed = round(sign_x * numerator / denominator, 4)

        return (
            f"F(x) = \\text{{sign}}(x) \\frac{{\\ln(1 + \\mu|x|)}}"
            f"{{\\ln(1 + \\mu)}}. \\mu = {mu}, x = {x}.",
            {
                "mu": mu, "x": x, "sign_x": sign_x,
                "abs_x": abs_x, "numerator": numerator,
                "denominator": denominator, "compressed": compressed,
            },
        )

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps for mu-law companding.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing numerator, denominator, and result.
        """
        sign_str = "+" if data["sign_x"] >= 0 else "-"
        return [
            f"|x| = {data['abs_x']}",
            f"ln(1 + {data['mu']}*{data['abs_x']}) = {data['numerator']}",
            f"ln(1 + {data['mu']}) = {data['denominator']}",
            f"F(x) = {sign_str}{data['numerator']}/{data['denominator']} "
            f"= {data['compressed']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the compressed value.

        Args:
            data: Solution data dict.

        Returns:
            F(x) value as a string.
        """
        return f"F({data['x']}) = {data['compressed']}"


# ---------------------------------------------------------------------------
# 4. Constellation Diagram (tier 5)
# ---------------------------------------------------------------------------

@register
class ConstellationDiagramGenerator(StepGenerator):
    """Determine the closest QPSK constellation point to a noisy received point.

    QPSK: 4 points at (1,1), (-1,1), (-1,-1), (1,-1) scaled by 1/sqrt(2).
    Given a received point with noise, find the minimum-distance
    constellation point (ML detection).

    Difficulty scaling:
        Difficulty 1-3: noise magnitude 0.1-0.3, clear detection.
        Difficulty 4-6: noise magnitude 0.2-0.5, closer margins.
        Difficulty 7-8: noise magnitude 0.3-0.7, ambiguous cases.

    Prerequisites:
        multiplication.
    """

    _CONSTELLATION = [
        (1, 1), (-1, 1), (-1, -1), (1, -1),
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "constellation_diagram"

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
        return "detect closest QPSK constellation point"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a QPSK detection problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            noise_mag = self._rng.uniform(0.1, 0.3)
        elif difficulty <= 6:
            noise_mag = self._rng.uniform(0.2, 0.5)
        else:
            noise_mag = self._rng.uniform(0.3, 0.7)

        scale = round(1 / math.sqrt(2), 4)
        ideal_idx = self._rng.randint(0, 3)
        ideal = self._CONSTELLATION[ideal_idx]
        scaled_ideal = (round(ideal[0] * scale, 4), round(ideal[1] * scale, 4))

        noise_x = round(self._rng.uniform(-noise_mag, noise_mag), 4)
        noise_y = round(self._rng.uniform(-noise_mag, noise_mag), 4)
        received = (
            round(scaled_ideal[0] + noise_x, 4),
            round(scaled_ideal[1] + noise_y, 4),
        )

        distances = []
        for i, pt in enumerate(self._CONSTELLATION):
            sp = (round(pt[0] * scale, 4), round(pt[1] * scale, 4))
            d = round(
                math.sqrt(
                    (received[0] - sp[0]) ** 2 + (received[1] - sp[1]) ** 2
                ), 4
            )
            distances.append({"idx": i, "point": sp, "dist": d})

        closest_idx = min(range(4), key=lambda i: distances[i]["dist"])
        closest = distances[closest_idx]

        return (
            f"QPSK: points at (\\pm 1, \\pm 1)/\\sqrt{{2}}. "
            f"Received: ({received[0]}, {received[1]}). "
            f"Find closest constellation point.",
            {
                "received": received, "scale": scale,
                "distances": distances, "closest": closest,
            },
        )

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps for constellation detection.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing distance to each point and detection result.
        """
        steps = []
        for d in data["distances"]:
            pt = d["point"]
            steps.append(
                f"d to ({pt[0]},{pt[1]}) = {d['dist']}"
            )
        cp = data["closest"]["point"]
        steps.append(f"closest = ({cp[0]}, {cp[1]})")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the detected constellation point.

        Args:
            data: Solution data dict.

        Returns:
            Closest point coordinates as a string.
        """
        cp = data["closest"]["point"]
        return f"detected = ({cp[0]}, {cp[1]})"
