"""Telecommunications task generators.

6 generators across tier 5 covering Shannon channel capacity, BPSK
modulation BER, link budget analysis, antenna gain, OFDM subcarrier
frequency computation, and spread spectrum processing gain.
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


# ===================================================================
# 1. Shannon Limit (tier 5)
# ===================================================================

@register
class ShannonLimitGenerator(StepGenerator):
    """Compute Shannon channel capacity: C = B * log2(1 + SNR).

    Given bandwidth B (Hz) and signal-to-noise ratio SNR (linear),
    compute the maximum channel capacity in bits per second.

    Difficulty scaling:
        Difficulty 1-3: integer B in kHz, SNR as simple ratio.
        Difficulty 4-6: B in MHz, SNR given in dB (convert first).
        Difficulty 7-8: compute required SNR for a target capacity.

    Prerequisites:
        logarithm.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "shannon_limit"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["logarithm"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        if difficulty >= 7:
            return "compute required SNR for target channel capacity"
        return "compute Shannon channel capacity"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate bandwidth and SNR parameters.

        Args:
            difficulty: Controls unit and problem variant.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            b_khz = self._rng.randint(1, 50)
            b_hz = b_khz * 1000
            snr_linear = self._rng.randint(2, 20)
            snr_db = round(10.0 * math.log10(snr_linear), 4)
            mode = "direct"
        elif difficulty <= 6:
            b_mhz = round(self._rng.uniform(0.1, 20), 2)
            b_hz = b_mhz * 1e6
            snr_db = round(self._rng.uniform(3, 30), 2)
            snr_linear = round(10.0 ** (snr_db / 10.0), 4)
            mode = "from_db"
        else:
            b_mhz = round(self._rng.uniform(0.5, 10), 2)
            b_hz = b_mhz * 1e6
            snr_db = round(self._rng.uniform(5, 25), 2)
            snr_linear = round(10.0 ** (snr_db / 10.0), 4)
            mode = "find_snr"

        capacity = round(b_hz * math.log2(1 + snr_linear), 4)

        return "C = B \\log_2(1 + \\text{SNR})", {
            "B_hz": b_hz,
            "snr_linear": snr_linear,
            "snr_db": snr_db,
            "capacity": capacity,
            "mode": mode,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Shannon capacity computation steps.

        Args:
            data: Solution data with B, SNR, and capacity.

        Returns:
            List of step strings.
        """
        steps = [f"B = {_f(data['B_hz'])} Hz"]
        if data["mode"] == "from_db":
            steps.append(f"SNR(dB) = {_f(data['snr_db'])}")
            steps.append(f"SNR(linear) = 10^({_f(data['snr_db'])}/10) = {_f(data['snr_linear'])}")
        elif data["mode"] == "find_snr":
            steps.append(f"target C = {_f(data['capacity'])} bps")
            steps.append(f"SNR = 2^(C/B) - 1")
        else:
            steps.append(f"SNR = {_f(data['snr_linear'])}")
        log_val = round(math.log2(1 + data["snr_linear"]), 4)
        steps.append(f"log2(1 + SNR) = {_f(log_val)}")
        steps.append(f"C = B * log2(1+SNR)")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the channel capacity.

        Args:
            data: Solution data.

        Returns:
            Capacity in bps.
        """
        return f"C = {_f(data['capacity'])} bps"


# ===================================================================
# 2. BPSK Modulation BER (tier 5)
# ===================================================================

@register
class ModulationBpskGenerator(StepGenerator):
    """Compute BPSK bit error rate from Eb/N0.

    Uses the Q-function approximation: BER = Q(sqrt(2*Eb/N0)).
    Q(x) is approximated by 0.5*erfc(x/sqrt(2)) using a lookup table
    for small integer arguments to keep output compact.

    Difficulty scaling:
        Difficulty 1-3: Eb/N0 in {1..5} dB, direct lookup.
        Difficulty 4-6: Eb/N0 in {3..10} dB, interpolation.
        Difficulty 7-8: compare BPSK vs QPSK (same BER, double throughput).

    Prerequisites:
        basic_prob.
    """

    # Pre-computed Q-function table for sqrt(2*Eb/N0) arguments
    _Q_TABLE = {
        0.0: 0.5,
        0.5: 0.3085,
        1.0: 0.1587,
        1.5: 0.0668,
        2.0: 0.0228,
        2.5: 0.0062,
        3.0: 0.0013,
        3.5: 0.0002,
        4.0: 0.00003,
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "modulation_bpsk"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["basic_prob"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute BPSK bit error rate"

    def _q_lookup(self, x: float) -> float:
        """Look up Q-function value from pre-computed table.

        Args:
            x: Non-negative argument.

        Returns:
            Q(x) from nearest table entry.
        """
        best_key = min(self._Q_TABLE.keys(), key=lambda k: abs(k - x))
        return self._Q_TABLE[best_key]

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate Eb/N0 and compute BER.

        Args:
            difficulty: Controls Eb/N0 range and variant.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            eb_n0_db = float(self._rng.randint(1, 5))
        elif difficulty <= 6:
            eb_n0_db = float(self._rng.randint(3, 10))
        else:
            eb_n0_db = float(self._rng.randint(5, 12))

        eb_n0_linear = round(10.0 ** (eb_n0_db / 10.0), 4)
        arg = round(math.sqrt(2.0 * eb_n0_linear), 4)
        ber = self._q_lookup(arg)

        return "\\text{BER} = Q\\left(\\sqrt{2 E_b/N_0}\\right)", {
            "eb_n0_db": eb_n0_db,
            "eb_n0_linear": eb_n0_linear,
            "arg": arg,
            "ber": ber,
            "compare_qpsk": difficulty >= 7,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate BPSK BER computation steps.

        Args:
            data: Solution data with Eb/N0 and BER.

        Returns:
            List of step strings.
        """
        steps = [
            f"Eb/N0 = {_f(data['eb_n0_db'])} dB",
            f"Eb/N0(linear) = 10^({_f(data['eb_n0_db'])}/10) = {_f(data['eb_n0_linear'])}",
            f"sqrt(2*Eb/N0) = {_f(data['arg'])}",
            f"BER = Q({_f(data['arg'])}) = {data['ber']}",
        ]
        if data["compare_qpsk"]:
            steps.append(f"QPSK: same BER, 2x throughput")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the bit error rate.

        Args:
            data: Solution data.

        Returns:
            BER value.
        """
        return f"BER = {data['ber']}"


# ===================================================================
# 3. Link Budget (tier 5)
# ===================================================================

@register
class LinkBudgetGenerator(StepGenerator):
    """Compute received power: Pr = Pt + Gt + Gr - FSPL.

    Free-space path loss: FSPL(dB) = 20*log10(d) + 20*log10(f) + 32.44
    where d is in km and f is in MHz.

    Difficulty scaling:
        Difficulty 1-3: simple integer values, short range.
        Difficulty 4-6: realistic values, longer range.
        Difficulty 7-8: solve for maximum distance given minimum Pr.

    Prerequisites:
        logarithm.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "link_budget"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["logarithm"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        if difficulty >= 7:
            return "compute maximum link distance"
        return "compute received power using link budget"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate transmit parameters and compute received power.

        Args:
            difficulty: Controls parameter ranges and variant.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            pt = float(self._rng.randint(10, 40))
            gt = float(self._rng.randint(0, 10))
            gr = float(self._rng.randint(0, 10))
            d_km = float(self._rng.randint(1, 10))
            f_mhz = float(self._rng.choice([900, 1800, 2400]))
        elif difficulty <= 6:
            pt = round(self._rng.uniform(10, 50), 1)
            gt = round(self._rng.uniform(0, 20), 1)
            gr = round(self._rng.uniform(0, 15), 1)
            d_km = round(self._rng.uniform(0.5, 50), 2)
            f_mhz = round(self._rng.uniform(400, 6000), 1)
        else:
            pt = round(self._rng.uniform(20, 50), 1)
            gt = round(self._rng.uniform(5, 25), 1)
            gr = round(self._rng.uniform(0, 20), 1)
            d_km = round(self._rng.uniform(1, 100), 2)
            f_mhz = round(self._rng.uniform(800, 28000), 1)

        fspl = round(20.0 * math.log10(d_km) + 20.0 * math.log10(f_mhz) + 32.44, 4)
        pr = round(pt + gt + gr - fspl, 4)

        return "P_r = P_t + G_t + G_r - \\text{FSPL}", {
            "Pt": pt, "Gt": gt, "Gr": gr,
            "d_km": d_km, "f_mhz": f_mhz,
            "fspl": fspl, "Pr": pr,
            "mode": "find_d" if difficulty >= 7 else "find_pr",
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate link budget computation steps.

        Args:
            data: Solution data with transmit params and path loss.

        Returns:
            List of step strings.
        """
        steps = [
            f"Pt = {_f(data['Pt'])} dBm, Gt = {_f(data['Gt'])} dBi, Gr = {_f(data['Gr'])} dBi",
            f"d = {_f(data['d_km'])} km, f = {_f(data['f_mhz'])} MHz",
            f"FSPL = 20*log10({_f(data['d_km'])}) + 20*log10({_f(data['f_mhz'])}) + 32.44",
            f"FSPL = {_f(data['fspl'])} dB",
            f"Pr = {_f(data['Pt'])} + {_f(data['Gt'])} + {_f(data['Gr'])} - {_f(data['fspl'])}",
        ]
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the received power.

        Args:
            data: Solution data.

        Returns:
            Received power in dBm.
        """
        return f"Pr = {_f(data['Pr'])} dBm"


# ===================================================================
# 4. Antenna Gain (tier 5)
# ===================================================================

@register
class AntennaGainGenerator(StepGenerator):
    """Compute antenna gain: G = 4*pi*A_eff / lambda^2.

    Given effective aperture A_eff (m^2) and wavelength lambda (m),
    compute the antenna gain as a linear ratio and convert to dBi.

    Difficulty scaling:
        Difficulty 1-3: lambda from common frequencies, integer aperture.
        Difficulty 4-6: decimal aperture, varied frequencies.
        Difficulty 7-8: compute A_eff from gain and frequency.

    Prerequisites:
        division.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "antenna_gain"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["division"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        if difficulty >= 7:
            return "compute effective aperture from antenna gain"
        return "compute antenna gain from aperture and wavelength"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate aperture and wavelength parameters.

        Args:
            difficulty: Controls parameter ranges and variant.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            f_mhz = self._rng.choice([900, 1800, 2400, 5000])
            lam = round(300.0 / f_mhz, 4)
            a_eff = float(self._rng.randint(1, 5))
        elif difficulty <= 6:
            f_mhz = round(self._rng.uniform(100, 10000), 1)
            lam = round(300.0 / f_mhz, 4)
            a_eff = round(self._rng.uniform(0.01, 5.0), 3)
        else:
            f_mhz = round(self._rng.uniform(500, 30000), 1)
            lam = round(300.0 / f_mhz, 4)
            a_eff = round(self._rng.uniform(0.005, 3.0), 4)

        g_linear = round(4.0 * math.pi * a_eff / (lam ** 2), 4)
        g_dbi = round(10.0 * math.log10(g_linear), 4) if g_linear > 0 else 0.0

        return "G = \\frac{4 \\pi A_{\\text{eff}}}{\\lambda^2}", {
            "f_mhz": f_mhz,
            "lambda": lam,
            "A_eff": a_eff,
            "G_linear": g_linear,
            "G_dBi": g_dbi,
            "mode": "find_A" if difficulty >= 7 else "find_G",
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate antenna gain computation steps.

        Args:
            data: Solution data with aperture, wavelength, and gain.

        Returns:
            List of step strings.
        """
        lam = data["lambda"]
        steps = [
            f"f = {_f(data['f_mhz'])} MHz, lambda = {_f(lam)} m",
            f"A_eff = {_f(data['A_eff'])} m^2",
            f"lambda^2 = {_f(round(lam ** 2, 4))}",
            f"G(linear) = 4*pi*{_f(data['A_eff'])}/{_f(round(lam ** 2, 4))}",
            f"G(linear) = {_f(data['G_linear'])}",
            f"G(dBi) = 10*log10({_f(data['G_linear'])}) = {_f(data['G_dBi'])}",
        ]
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the antenna gain.

        Args:
            data: Solution data.

        Returns:
            Gain in dBi.
        """
        return f"G = {_f(data['G_dBi'])} dBi"


# ===================================================================
# 5. OFDM Subcarrier (tier 5)
# ===================================================================

@register
class OfdmSubcarrierGenerator(StepGenerator):
    """Compute OFDM subcarrier frequencies: f_k = f_0 + k * delta_f.

    Given center frequency f_0, symbol duration T_symbol (delta_f = 1/T_symbol),
    and number of subcarriers N, compute the N subcarrier frequencies.

    Difficulty scaling:
        Difficulty 1-3: N = 4, integer f_0 in kHz.
        Difficulty 4-6: N = 8, f_0 in MHz.
        Difficulty 7-8: N = 8, also compute total bandwidth.

    Prerequisites:
        multiplication.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "ofdm_subcarrier"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["multiplication"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute OFDM subcarrier frequencies"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate OFDM parameters and compute subcarrier frequencies.

        Args:
            difficulty: Controls number of subcarriers and frequency range.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            n_sub = 4
            f0 = float(self._rng.randint(1, 10)) * 1000  # Hz
            t_sym = round(self._rng.choice([0.001, 0.002, 0.005]), 4)  # seconds
        elif difficulty <= 6:
            n_sub = 8
            f0 = round(self._rng.uniform(1, 5) * 1e6, 2)  # Hz
            t_sym = round(self._rng.uniform(0.0001, 0.001), 6)
        else:
            n_sub = 8
            f0 = round(self._rng.uniform(2, 6) * 1e9, 2)  # Hz
            t_sym = round(self._rng.uniform(0.00001, 0.0001), 6)

        delta_f = round(1.0 / t_sym, 4)
        freqs = [round(f0 + k * delta_f, 4) for k in range(n_sub)]
        bw = round(n_sub * delta_f, 4)

        return "f_k = f_0 + k \\cdot \\Delta f, \\quad \\Delta f = 1/T_{\\text{sym}}", {
            "f0": f0,
            "T_sym": t_sym,
            "delta_f": delta_f,
            "N": n_sub,
            "freqs": freqs,
            "bw": bw,
            "show_bw": difficulty >= 7,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate OFDM subcarrier computation steps.

        Args:
            data: Solution data with frequencies and spacing.

        Returns:
            List of step strings.
        """
        steps = [
            f"f0 = {_f(data['f0'])} Hz, T_sym = {data['T_sym']} s",
            f"delta_f = 1/{data['T_sym']} = {_f(data['delta_f'])} Hz",
        ]
        for k in range(min(data["N"], 4)):
            steps.append(f"f_{k} = {_f(data['freqs'][k])} Hz")
        if data["N"] > 4:
            steps.append(f"... f_{data['N'] - 1} = {_f(data['freqs'][-1])} Hz")
        if data["show_bw"]:
            steps.append(f"BW = {data['N']}*{_f(data['delta_f'])} = {_f(data['bw'])} Hz")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the subcarrier frequencies summary.

        Args:
            data: Solution data.

        Returns:
            First and last frequency with spacing.
        """
        ans = f"f_0 = {_f(data['freqs'][0])}, f_{data['N'] - 1} = {_f(data['freqs'][-1])}, delta_f = {_f(data['delta_f'])} Hz"
        if data["show_bw"]:
            ans += f", BW = {_f(data['bw'])} Hz"
        return ans


# ===================================================================
# 6. Spread Spectrum Processing Gain (tier 5)
# ===================================================================

@register
class SpreadSpectrumGenerator(StepGenerator):
    """Compute spread spectrum processing gain: PG = 10*log10(chip_rate/data_rate).

    Given the chip rate and data rate, compute the processing gain
    in decibels.

    Difficulty scaling:
        Difficulty 1-3: power-of-2 ratios, integer rates.
        Difficulty 4-6: realistic CDMA rates, decimal values.
        Difficulty 7-8: compute required chip rate for target PG.

    Prerequisites:
        logarithm.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "spread_spectrum"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["logarithm"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        if difficulty >= 7:
            return "compute required chip rate for target processing gain"
        return "compute spread spectrum processing gain"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate chip rate and data rate.

        Args:
            difficulty: Controls rate ranges and variant.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            ratio = 2 ** self._rng.randint(2, 6)
            data_rate = float(self._rng.choice([1000, 2000, 4000, 8000]))
            chip_rate = data_rate * ratio
        elif difficulty <= 6:
            data_rate = round(self._rng.uniform(9.6e3, 64e3), 1)
            chip_rate = round(self._rng.uniform(1.0e6, 5.0e6), 1)
        else:
            data_rate = round(self._rng.uniform(9.6e3, 128e3), 1)
            chip_rate = round(self._rng.uniform(1.0e6, 10.0e6), 1)

        ratio_val = round(chip_rate / data_rate, 4)
        pg_db = round(10.0 * math.log10(ratio_val), 4)

        return "\\text{PG} = 10 \\log_{10}\\left(\\frac{R_c}{R_d}\\right)", {
            "chip_rate": chip_rate,
            "data_rate": data_rate,
            "ratio": ratio_val,
            "pg_db": pg_db,
            "mode": "find_chip" if difficulty >= 7 else "find_pg",
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate processing gain computation steps.

        Args:
            data: Solution data with rates and gain.

        Returns:
            List of step strings.
        """
        steps = [
            f"Rc = {_f(data['chip_rate'])} chips/s",
            f"Rd = {_f(data['data_rate'])} bps",
            f"Rc/Rd = {_f(data['ratio'])}",
            f"PG = 10*log10({_f(data['ratio'])})",
        ]
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the processing gain.

        Args:
            data: Solution data.

        Returns:
            Processing gain in dB.
        """
        return f"PG = {_f(data['pg_db'])} dB"
