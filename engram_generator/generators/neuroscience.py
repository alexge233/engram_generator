"""Neuroscience generators -- membrane potentials, neural coding, brain imaging.

10 generators across tiers 4-6 covering electrophysiology, neural coding,
synaptic integration, cable theory, and neuroimaging fundamentals.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


def _fmt(value: float, decimals: int = 4) -> str:
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


# Physical constants
_R = 8.314       # gas constant (J/(mol*K))
_F = 96485.0     # Faraday constant (C/mol)


# ===================================================================
# 1. Membrane potential (Nernst equation)  (tier 5)
# ===================================================================

@register
class MembranePotentialGenerator(StepGenerator):
    """Nernst equation: E = (RT/zF) * ln(C_out/C_in).

    Computes the equilibrium potential for Na+, K+, or Cl- ions
    at a given temperature using the Nernst equation.

    Difficulty scaling:
        Difficulty 1-3: single ion, standard 37C.
        Difficulty 4-6: single ion, variable temperature.
        Difficulty 7-8: two ions, compare potentials.

    Prerequisites:
        logarithm.
    """

    _IONS = {
        "Na+": {"z": 1, "c_out_range": (135, 150), "c_in_range": (5, 15)},
        "K+":  {"z": 1, "c_out_range": (3, 6), "c_in_range": (130, 155)},
        "Cl-": {"z": -1, "c_out_range": (95, 115), "c_in_range": (4, 12)},
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "membrane_potential"

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
        return "compute equilibrium potential using Nernst equation"

    def _pick_ion(self, difficulty: int) -> tuple[str, int, float, float, float]:
        """Select an ion and generate concentrations.

        Args:
            difficulty: Controls temperature variation.

        Returns:
            Tuple of (ion_name, z, C_out, C_in, T_kelvin).
        """
        ion_name = self._rng.choice(list(self._IONS.keys()))
        ion = self._IONS[ion_name]
        c_out = round(self._rng.uniform(*ion["c_out_range"]), 1)
        c_in = round(self._rng.uniform(*ion["c_in_range"]), 1)
        if difficulty <= 3:
            t_k = 310.15  # 37 C
        else:
            t_k = round(self._rng.uniform(295.0, 315.0), 2)
        return ion_name, ion["z"], c_out, c_in, t_k

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Nernst equation problem.

        Args:
            difficulty: Controls complexity.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        ion_name, z, c_out, c_in, t_k = self._pick_ion(difficulty)
        ratio = round(c_out / c_in, 4)
        ln_ratio = round(math.log(ratio), 4)
        prefactor = round((_R * t_k) / (z * _F), 4)
        e_mv = round(prefactor * ln_ratio * 1000, 4)  # convert V to mV

        return "E = \\frac{RT}{zF} \\ln\\frac{C_{out}}{C_{in}}", {
            "ion": ion_name, "z": z, "c_out": c_out, "c_in": c_in,
            "T": t_k, "ratio": ratio, "ln_ratio": ln_ratio,
            "prefactor": prefactor, "E_mV": e_mv,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Nernst computation steps.

        Args:
            data: Solution data.

        Returns:
            List of step strings.
        """
        return [
            f"ion={data['ion']}, z={data['z']}, "
            f"C_out={data['c_out']} mM, C_in={data['c_in']} mM",
            f"RT/(zF) = {_R}*{_fmt(data['T'])}/({data['z']}*{_F})"
            f" = {_fmt(data['prefactor'])} V",
            f"ln(C_out/C_in) = ln({_fmt(data['ratio'])}) = {_fmt(data['ln_ratio'])}",
            f"E = {_fmt(data['prefactor'])}*{_fmt(data['ln_ratio'])}*1000 mV",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the equilibrium potential.

        Args:
            data: Solution data.

        Returns:
            Equilibrium potential in mV.
        """
        return f"E({data['ion']}) = {_fmt(data['E_mV'])} mV"


# ===================================================================
# 2. Goldman equation  (tier 5)
# ===================================================================

@register
class GoldmanEquationGenerator(StepGenerator):
    """Goldman equation for resting membrane potential.

    V_m = (RT/F) * ln((P_K[K]o + P_Na[Na]o + P_Cl[Cl]i) /
                       (P_K[K]i + P_Na[Na]i + P_Cl[Cl]o)).

    Difficulty scaling:
        Difficulty 1-3: standard permeability ratios (1:0.04:0.45).
        Difficulty 4-6: varied permeability ratios.
        Difficulty 7-8: compare two states (rest vs depolarised).

    Prerequisites:
        membrane_potential.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "goldman_equation"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["membrane_potential"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute resting membrane potential using Goldman equation"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Goldman equation problem.

        Args:
            difficulty: Controls permeability variation.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        t_k = 310.15  # 37 C
        # Concentrations (mM) -- physiological ranges
        k_o = round(self._rng.uniform(3.0, 6.0), 1)
        k_i = round(self._rng.uniform(130.0, 155.0), 1)
        na_o = round(self._rng.uniform(135.0, 150.0), 1)
        na_i = round(self._rng.uniform(5.0, 15.0), 1)
        cl_o = round(self._rng.uniform(95.0, 115.0), 1)
        cl_i = round(self._rng.uniform(4.0, 12.0), 1)

        if difficulty <= 3:
            p_k, p_na, p_cl = 1.0, 0.04, 0.45
        else:
            p_k = 1.0
            p_na = round(self._rng.uniform(0.01, 0.1), 4)
            p_cl = round(self._rng.uniform(0.1, 0.6), 4)

        numerator = round(p_k * k_o + p_na * na_o + p_cl * cl_i, 4)
        denominator = round(p_k * k_i + p_na * na_i + p_cl * cl_o, 4)
        ratio = round(numerator / denominator, 4)
        ln_ratio = round(math.log(ratio), 4)
        rt_f = round((_R * t_k) / _F, 4)
        v_m = round(rt_f * ln_ratio * 1000, 4)  # mV

        return ("V_m = \\frac{RT}{F} \\ln\\frac{P_K[K]_o + P_{Na}[Na]_o"
                " + P_{Cl}[Cl]_i}{P_K[K]_i + P_{Na}[Na]_i + P_{Cl}[Cl]_o}"), {
            "T": t_k, "k_o": k_o, "k_i": k_i,
            "na_o": na_o, "na_i": na_i, "cl_o": cl_o, "cl_i": cl_i,
            "p_k": p_k, "p_na": p_na, "p_cl": p_cl,
            "numerator": numerator, "denominator": denominator,
            "ratio": ratio, "ln_ratio": ln_ratio,
            "rt_f": rt_f, "V_m": v_m,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Goldman equation computation steps.

        Args:
            data: Solution data.

        Returns:
            List of step strings.
        """
        return [
            f"P_K={data['p_k']}, P_Na={data['p_na']}, P_Cl={data['p_cl']}",
            f"num = {data['p_k']}*{data['k_o']} + {data['p_na']}*{data['na_o']}"
            f" + {data['p_cl']}*{data['cl_i']} = {_fmt(data['numerator'])}",
            f"den = {data['p_k']}*{data['k_i']} + {data['p_na']}*{data['na_i']}"
            f" + {data['p_cl']}*{data['cl_o']} = {_fmt(data['denominator'])}",
            f"ln({_fmt(data['ratio'])}) = {_fmt(data['ln_ratio'])}",
            f"V_m = {_fmt(data['rt_f'])}*{_fmt(data['ln_ratio'])}*1000",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the resting membrane potential.

        Args:
            data: Solution data.

        Returns:
            V_m in mV.
        """
        return f"V_m = {_fmt(data['V_m'])} mV"


# ===================================================================
# 3. Hodgkin-Huxley gate  (tier 6)
# ===================================================================

@register
class HodgkinHuxleyGateGenerator(StepGenerator):
    """Hodgkin-Huxley gating variable: dn/dt = alpha_n(1-n) - beta_n*n.

    Computes one Euler step of the gating variable n given
    alpha_n, beta_n, current n, and timestep dt.

    Difficulty scaling:
        Difficulty 1-3: given alpha, beta, n, dt directly.
        Difficulty 4-6: compute alpha, beta from voltage.
        Difficulty 7-8: two gating variables (n and m).

    Prerequisites:
        derivative.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "hodgkin_huxley_gate"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["derivative"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute Hodgkin-Huxley gating variable Euler step"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an HH gating variable problem.

        Args:
            difficulty: Controls complexity.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        n = round(self._rng.uniform(0.1, 0.9), 4)
        alpha = round(self._rng.uniform(0.01, 0.5), 4)
        beta = round(self._rng.uniform(0.01, 0.5), 4)
        dt = round(self._rng.uniform(0.01, 0.1), 4)

        dn_dt = round(alpha * (1 - n) - beta * n, 4)
        n_new = round(n + dn_dt * dt, 4)
        n_new = round(max(0.0, min(1.0, n_new)), 4)

        return "\\frac{dn}{dt} = \\alpha_n(1-n) - \\beta_n n", {
            "n": n, "alpha": alpha, "beta": beta, "dt": dt,
            "dn_dt": dn_dt, "n_new": n_new,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate HH gating computation steps.

        Args:
            data: Solution data.

        Returns:
            List of step strings.
        """
        alpha_term = round(data["alpha"] * (1 - data["n"]), 4)
        beta_term = round(data["beta"] * data["n"], 4)
        return [
            f"n={_fmt(data['n'])}, alpha={_fmt(data['alpha'])}, "
            f"beta={_fmt(data['beta'])}, dt={_fmt(data['dt'])}",
            f"alpha*(1-n) = {_fmt(data['alpha'])}*(1-{_fmt(data['n'])})"
            f" = {_fmt(alpha_term)}",
            f"beta*n = {_fmt(data['beta'])}*{_fmt(data['n'])}"
            f" = {_fmt(beta_term)}",
            f"dn/dt = {_fmt(alpha_term)} - {_fmt(beta_term)}"
            f" = {_fmt(data['dn_dt'])}",
            f"n_new = {_fmt(data['n'])} + {_fmt(data['dn_dt'])}*{_fmt(data['dt'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the updated gating variable.

        Args:
            data: Solution data.

        Returns:
            n_new value.
        """
        return f"n_new = {_fmt(data['n_new'])}"


# ===================================================================
# 4. Spike rate  (tier 4)
# ===================================================================

@register
class SpikeRateGenerator(StepGenerator):
    """Compute firing rate from a spike train.

    Given a binary spike train and a time window, counts spikes
    and computes firing rate = num_spikes / time_window.

    Difficulty scaling:
        Difficulty 1-3: short trains (5-10 bins).
        Difficulty 4-6: medium trains (10-20 bins).
        Difficulty 7-8: long trains (20-30 bins).

    Prerequisites:
        division.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "spike_rate"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

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
        return "compute firing rate from spike train"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a spike rate computation problem.

        Args:
            difficulty: Controls spike train length.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            n_bins = self._rng.randint(5, 10)
        elif difficulty <= 6:
            n_bins = self._rng.randint(10, 20)
        else:
            n_bins = self._rng.randint(20, 30)

        bin_width_ms = round(self._rng.uniform(1.0, 5.0), 1)
        spike_prob = round(self._rng.uniform(0.1, 0.5), 2)
        train = [1 if self._rng.random() < spike_prob else 0
                 for _ in range(n_bins)]
        num_spikes = sum(train)
        time_window = round(n_bins * bin_width_ms / 1000, 4)  # seconds
        rate = round(num_spikes / time_window, 4) if time_window > 0 else 0

        train_str = "".join(str(s) for s in train)
        desc = (f"spike train: {train_str}, bin_width={bin_width_ms}ms; "
                f"compute firing rate")

        return desc, {
            "train": train_str, "n_bins": n_bins,
            "bin_width_ms": bin_width_ms,
            "num_spikes": num_spikes, "time_window": time_window,
            "rate": rate,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate spike rate computation steps.

        Args:
            data: Solution data.

        Returns:
            List of step strings.
        """
        return [
            f"train = {data['train']}, {data['n_bins']} bins",
            f"num_spikes = {data['num_spikes']}",
            f"time_window = {data['n_bins']}*{data['bin_width_ms']}ms"
            f" = {_fmt(data['time_window'])} s",
            f"rate = {data['num_spikes']}/{_fmt(data['time_window'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the firing rate.

        Args:
            data: Solution data.

        Returns:
            Firing rate in Hz.
        """
        return f"rate = {_fmt(data['rate'])} Hz"


# ===================================================================
# 5. Receptive field  (tier 5)
# ===================================================================

@register
class ReceptiveFieldGenerator(StepGenerator):
    """1D center-surround receptive field response.

    Computes response = sum(stimulus * kernel) where the kernel has
    +1 in the center and -1 in the surround.

    Difficulty scaling:
        Difficulty 1-3: kernel size 3 (1 center, 2 surround).
        Difficulty 4-6: kernel size 5 (1 center, 4 surround).
        Difficulty 7-8: kernel size 7 (3 center, 4 surround).

    Prerequisites:
        multiplication.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "receptive_field"

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
        return "compute center-surround receptive field response"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a receptive field problem.

        Args:
            difficulty: Controls kernel size.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            kernel = [-1, 1, -1]
        elif difficulty <= 6:
            kernel = [-1, -1, 1, -1, -1]
        else:
            kernel = [-1, -1, 1, 1, 1, -1, -1]

        k_size = len(kernel)
        stimulus = [self._rng.randint(0, 10 + difficulty * 2)
                    for _ in range(k_size)]

        products = [round(s * k, 4) for s, k in zip(stimulus, kernel)]
        response = round(sum(products), 4)

        desc = f"stimulus={stimulus}, kernel={kernel}"
        return desc, {
            "stimulus": stimulus, "kernel": kernel,
            "products": products, "response": response,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate receptive field computation steps.

        Args:
            data: Solution data.

        Returns:
            List of step strings.
        """
        pairs = [f"{s}*{k}={_fmt(p)}" for s, k, p
                 in zip(data["stimulus"], data["kernel"], data["products"])]
        return [
            f"stimulus={data['stimulus']}",
            f"kernel={data['kernel']}",
            f"products: {', '.join(pairs)}",
            f"response = sum = {_fmt(data['response'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the receptive field response.

        Args:
            data: Solution data.

        Returns:
            Response value.
        """
        return f"response = {_fmt(data['response'])}"


# ===================================================================
# 6. Neural coding (mutual information)  (tier 5)
# ===================================================================

@register
class NeuralCodingGenerator(StepGenerator):
    """Compute mutual information between stimulus and response.

    Given a joint probability distribution P(s, r), computes
    I(S;R) = sum P(s,r) * log2(P(s,r) / (P(s)*P(r))).

    Difficulty scaling:
        Difficulty 1-3: 2x2 joint distribution.
        Difficulty 4-6: 2x3 joint distribution.
        Difficulty 7-8: 3x3 joint distribution.

    Prerequisites:
        logarithm.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "neural_coding"

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
        return "compute mutual information between stimulus and response"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a mutual information problem.

        Args:
            difficulty: Controls distribution size.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            n_s, n_r = 2, 2
        elif difficulty <= 6:
            n_s, n_r = 2, 3
        else:
            n_s, n_r = 3, 3

        # Generate random joint distribution and normalise
        raw = [[self._rng.randint(1, 10) for _ in range(n_r)]
               for _ in range(n_s)]
        total = sum(sum(row) for row in raw)
        joint = [[round(v / total, 4) for v in row] for row in raw]

        # Marginals
        p_s = [round(sum(row), 4) for row in joint]
        p_r = [round(sum(joint[i][j] for i in range(n_s)), 4)
               for j in range(n_r)]

        # Mutual information
        mi = 0.0
        for i in range(n_s):
            for j in range(n_r):
                p_ij = joint[i][j]
                if p_ij > 0 and p_s[i] > 0 and p_r[j] > 0:
                    mi += p_ij * math.log2(p_ij / (p_s[i] * p_r[j]))
        mi = round(mi, 4)

        joint_str = "; ".join(
            ",".join(_fmt(v) for v in row) for row in joint
        )
        desc = f"joint P(s,r): [{joint_str}]; compute I(S;R)"

        return desc, {
            "joint": joint, "p_s": p_s, "p_r": p_r,
            "n_s": n_s, "n_r": n_r, "mi": mi,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate mutual information computation steps.

        Args:
            data: Solution data.

        Returns:
            List of step strings.
        """
        p_s_str = ", ".join(_fmt(p) for p in data["p_s"])
        p_r_str = ", ".join(_fmt(p) for p in data["p_r"])
        return [
            f"P(s) = [{p_s_str}]",
            f"P(r) = [{p_r_str}]",
            "I(S;R) = sum P(s,r)*log2(P(s,r)/(P(s)*P(r)))",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the mutual information.

        Args:
            data: Solution data.

        Returns:
            MI in bits.
        """
        return f"I(S;R) = {_fmt(data['mi'])} bits"


# ===================================================================
# 7. Synaptic integration  (tier 5)
# ===================================================================

@register
class SynapticIntegrationGenerator(StepGenerator):
    """EPSP/IPSP summation with temporal decay.

    Computes V_total = sum(w_i * V_i * exp(-dt_i / tau)) where
    w_i are synaptic weights, V_i are post-synaptic potentials,
    and dt_i are time delays from the current moment.

    Difficulty scaling:
        Difficulty 1-3: 2-3 synapses, no temporal decay.
        Difficulty 4-6: 3-4 synapses with temporal decay.
        Difficulty 7-8: 4-5 synapses with temporal decay.

    Prerequisites:
        multiplication.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "synaptic_integration"

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
        return "compute synaptic integration with temporal decay"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a synaptic integration problem.

        Args:
            difficulty: Controls number of synapses and decay.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            n_syn = self._rng.randint(2, 3)
            use_decay = False
        elif difficulty <= 6:
            n_syn = self._rng.randint(3, 4)
            use_decay = True
        else:
            n_syn = self._rng.randint(4, 5)
            use_decay = True

        tau = round(self._rng.uniform(5.0, 20.0), 2) if use_decay else 0.0
        weights = [round(self._rng.uniform(-1.0, 1.0), 4)
                   for _ in range(n_syn)]
        voltages = [round(self._rng.uniform(1.0, 10.0), 2)
                    for _ in range(n_syn)]

        if use_decay:
            delays = [round(self._rng.uniform(0.0, 10.0), 2)
                      for _ in range(n_syn)]
            decay_factors = [round(math.exp(-dt / tau), 4) for dt in delays]
        else:
            delays = [0.0] * n_syn
            decay_factors = [1.0] * n_syn

        contributions = [round(w * v * d, 4)
                         for w, v, d in zip(weights, voltages, decay_factors)]
        v_total = round(sum(contributions), 4)

        desc = (f"weights={[_fmt(w) for w in weights]}, "
                f"V={[_fmt(v) for v in voltages]}")
        if use_decay:
            desc += f", delays={[_fmt(d) for d in delays]}, tau={_fmt(tau)}"

        return desc, {
            "weights": weights, "voltages": voltages,
            "delays": delays, "tau": tau, "use_decay": use_decay,
            "decay_factors": decay_factors,
            "contributions": contributions, "v_total": v_total,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate synaptic integration steps.

        Args:
            data: Solution data.

        Returns:
            List of step strings.
        """
        steps = []
        for i, (w, v, d, c) in enumerate(zip(
            data["weights"], data["voltages"],
            data["decay_factors"], data["contributions"],
        )):
            steps.append(
                f"syn{i}: {_fmt(w)}*{_fmt(v)}*{_fmt(d)} = {_fmt(c)} mV"
            )
        steps.append(
            f"V_total = sum = {_fmt(data['v_total'])} mV"
        )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the total membrane potential.

        Args:
            data: Solution data.

        Returns:
            V_total in mV.
        """
        return f"V_total = {_fmt(data['v_total'])} mV"


# ===================================================================
# 8. Cable equation  (tier 6)
# ===================================================================

@register
class CableEquationGenerator(StepGenerator):
    """Cable equation: length constant and voltage attenuation.

    Computes lambda = sqrt(r_m / (r_i + r_o)) and
    V(x) = V_0 * exp(-x / lambda).

    Difficulty scaling:
        Difficulty 1-3: compute lambda only.
        Difficulty 4-6: compute lambda and V(x) at one point.
        Difficulty 7-8: compute V(x) at multiple points.

    Prerequisites:
        exponentiation.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "cable_equation"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["exponentiation"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute cable equation length constant and voltage decay"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a cable equation problem.

        Args:
            difficulty: Controls problem scope.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        r_m = round(self._rng.uniform(1e4, 1e6), 2)  # Ohm*cm
        r_i = round(self._rng.uniform(50.0, 300.0), 2)  # Ohm/cm
        r_o = round(self._rng.uniform(1.0, 50.0), 2)  # Ohm/cm
        v_0 = round(self._rng.uniform(5.0, 50.0), 2)  # mV

        lam = round(math.sqrt(r_m / (r_i + r_o)), 4)  # cm

        if difficulty <= 3:
            x_vals = []
            v_vals = []
        elif difficulty <= 6:
            x = round(self._rng.uniform(0.1, 2.0) * lam, 4)
            v_x = round(v_0 * math.exp(-x / lam), 4)
            x_vals = [x]
            v_vals = [v_x]
        else:
            x_vals = [round(self._rng.uniform(0.1, 0.5) * i * lam, 4)
                      for i in range(1, 4)]
            v_vals = [round(v_0 * math.exp(-x / lam), 4) for x in x_vals]

        return "\\lambda = \\sqrt{r_m/(r_i+r_o)}, V(x) = V_0 e^{-x/\\lambda}", {
            "r_m": r_m, "r_i": r_i, "r_o": r_o, "v_0": v_0,
            "lambda": lam, "x_vals": x_vals, "v_vals": v_vals,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate cable equation computation steps.

        Args:
            data: Solution data.

        Returns:
            List of step strings.
        """
        ri_ro = round(data["r_i"] + data["r_o"], 4)
        ratio = round(data["r_m"] / ri_ro, 4)
        steps = [
            f"r_m={_fmt(data['r_m'])}, r_i={_fmt(data['r_i'])}, "
            f"r_o={_fmt(data['r_o'])}",
            f"r_i+r_o = {_fmt(ri_ro)}",
            f"r_m/(r_i+r_o) = {_fmt(ratio)}",
            f"lambda = sqrt({_fmt(ratio)}) = {_fmt(data['lambda'])} cm",
        ]
        for x, v in zip(data["x_vals"], data["v_vals"]):
            steps.append(
                f"V({_fmt(x)}) = {_fmt(data['v_0'])}*exp(-{_fmt(x)}"
                f"/{_fmt(data['lambda'])}) = {_fmt(v)} mV"
            )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the length constant and voltage values.

        Args:
            data: Solution data.

        Returns:
            Lambda and V(x) values.
        """
        ans = f"lambda = {_fmt(data['lambda'])} cm"
        if data["v_vals"]:
            v_strs = [f"V({_fmt(x)})={_fmt(v)}"
                      for x, v in zip(data["x_vals"], data["v_vals"])]
            ans += f", {', '.join(v_strs)} mV"
        return ans


# ===================================================================
# 9. fMRI BOLD signal  (tier 5)
# ===================================================================

@register
class FmriBoldGenerator(StepGenerator):
    """BOLD signal: percent change = (S_active - S_baseline) / S_baseline * 100.

    Computes percent signal change from activation data across
    multiple brain regions or conditions.

    Difficulty scaling:
        Difficulty 1-3: single region, single condition.
        Difficulty 4-6: 2-3 regions, find max activation.
        Difficulty 7-8: 3-4 regions, rank by activation.

    Prerequisites:
        division.
    """

    _REGIONS = [
        "V1", "V2", "MT", "PFC", "ACC", "amygdala",
        "hippocampus", "SMA", "M1", "S1",
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "fmri_bold"

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
        return "compute BOLD percent signal change"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate fMRI BOLD signal problem.

        Args:
            difficulty: Controls number of regions.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            n_regions = 1
        elif difficulty <= 6:
            n_regions = self._rng.randint(2, 3)
        else:
            n_regions = self._rng.randint(3, 4)

        regions = self._rng.sample(self._REGIONS, n_regions)
        baselines = [round(self._rng.uniform(500.0, 2000.0), 2)
                     for _ in range(n_regions)]
        actives = [round(b + self._rng.uniform(5.0, 60.0), 2)
                   for b in baselines]
        pct_changes = [round((a - b) / b * 100, 4)
                       for a, b in zip(actives, baselines)]

        max_idx = pct_changes.index(max(pct_changes))
        max_region = regions[max_idx]

        pairs = [f"{r}: base={b}, active={a}" for r, b, a
                 in zip(regions, baselines, actives)]
        desc = "; ".join(pairs) + "; compute % BOLD change"

        return desc, {
            "regions": regions, "baselines": baselines,
            "actives": actives, "pct_changes": pct_changes,
            "max_region": max_region, "n_regions": n_regions,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate BOLD computation steps.

        Args:
            data: Solution data.

        Returns:
            List of step strings.
        """
        steps = ["% change = (S_active - S_baseline) / S_baseline * 100"]
        for r, b, a, p in zip(data["regions"], data["baselines"],
                              data["actives"], data["pct_changes"]):
            steps.append(
                f"{r}: ({_fmt(a)}-{_fmt(b)})/{_fmt(b)}*100 = {_fmt(p)}%"
            )
        if data["n_regions"] > 1:
            steps.append(f"max activation: {data['max_region']}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the BOLD percent changes.

        Args:
            data: Solution data.

        Returns:
            Percent changes per region.
        """
        parts = [f"{r}={_fmt(p)}%"
                 for r, p in zip(data["regions"], data["pct_changes"])]
        return ", ".join(parts)


# ===================================================================
# 10. EEG frequency band classification  (tier 5)
# ===================================================================

@register
class EegFrequencyGenerator(StepGenerator):
    """Classify EEG frequency into standard bands.

    Bands: delta (0.5-4 Hz), theta (4-8 Hz), alpha (8-13 Hz),
    beta (13-30 Hz), gamma (30+ Hz). Given a frequency, classify it
    and compute the period.

    Difficulty scaling:
        Difficulty 1-3: single frequency, classify.
        Difficulty 4-6: two frequencies, classify and compare.
        Difficulty 7-8: three frequencies, rank by band.

    Prerequisites:
        comparison.
    """

    _BANDS = [
        ("delta", 0.5, 4.0),
        ("theta", 4.0, 8.0),
        ("alpha", 8.0, 13.0),
        ("beta", 13.0, 30.0),
        ("gamma", 30.0, 100.0),
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "eeg_frequency"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["comparison"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "classify EEG frequency into standard brain wave bands"

    def _classify(self, freq: float) -> str:
        """Classify a frequency into an EEG band.

        Args:
            freq: Frequency in Hz.

        Returns:
            Band name string.
        """
        for name, lo, hi in self._BANDS:
            if lo <= freq < hi:
                return name
        return "gamma"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an EEG frequency classification problem.

        Args:
            difficulty: Controls number of frequencies.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            n_freq = 1
        elif difficulty <= 6:
            n_freq = 2
        else:
            n_freq = 3

        freqs = [round(self._rng.uniform(0.5, 80.0), 2)
                 for _ in range(n_freq)]
        bands = [self._classify(f) for f in freqs]
        periods = [round(1.0 / f, 4) for f in freqs]

        freq_str = ", ".join(f"{_fmt(f)} Hz" for f in freqs)
        desc = f"frequencies: {freq_str}; classify EEG bands"

        return desc, {
            "freqs": freqs, "bands": bands, "periods": periods,
            "n_freq": n_freq,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate EEG classification steps.

        Args:
            data: Solution data.

        Returns:
            List of step strings.
        """
        steps = ["bands: delta(0.5-4), theta(4-8), alpha(8-13), "
                 "beta(13-30), gamma(30+)"]
        for f, b, t in zip(data["freqs"], data["bands"], data["periods"]):
            steps.append(f"{_fmt(f)} Hz -> {b}, T={_fmt(t)} s")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the frequency classifications.

        Args:
            data: Solution data.

        Returns:
            Band assignments.
        """
        parts = [f"{_fmt(f)} Hz = {b}"
                 for f, b in zip(data["freqs"], data["bands"])]
        return ", ".join(parts)
