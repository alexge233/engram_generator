"""Deep information theory task generators.

6 generators across tiers 5-6 covering Slepian-Wolf distributed source
coding, multiple access channel capacity, binary rate-distortion,
asymptotic equipartition property, polar code reliability, and
entropy rate of Markov chains.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _binary_entropy(p: float) -> float:
    """Compute the binary entropy function H(p).

    Args:
        p: Probability in (0, 1).

    Returns:
        H(p) = -p*log2(p) - (1-p)*log2(1-p), or 0.0 at boundaries.
    """
    if p <= 0.0 or p >= 1.0:
        return 0.0
    return -p * math.log2(p) - (1.0 - p) * math.log2(1.0 - p)


def _entropy_from_dist(dist: list[float]) -> float:
    """Compute Shannon entropy of a probability distribution.

    Args:
        dist: List of probabilities summing to 1.

    Returns:
        H(X) = -sum p_i * log2(p_i).
    """
    h = 0.0
    for p in dist:
        if p > 0.0:
            h -= p * math.log2(p)
    return h


# ===================================================================
# 1. Slepian-Wolf (tier 6)
# ===================================================================

@register
class SlepianWolfGenerator(StepGenerator):
    """Compute Slepian-Wolf rate region for distributed source coding.

    R1 >= H(X|Y), R2 >= H(Y|X), R1 + R2 >= H(X,Y).
    Given a joint distribution P(X,Y), compute the rate region bounds.

    Difficulty scaling:
        Difficulty 1-3: 2x2 joint distribution.
        Difficulty 4-6: 2x3 distribution.
        Difficulty 7-8: 3x3 distribution.

    Prerequisites:
        info_entropy.
    """

    _SIZES = {
        1: (2, 2), 2: (2, 2), 3: (2, 2),
        4: (2, 3), 5: (2, 3), 6: (2, 3),
        7: (3, 3), 8: (3, 3),
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "slepian_wolf"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["info_entropy"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute Slepian-Wolf rate region for distributed sources"

    def _generate_joint(self, rows: int, cols: int) -> list[list[float]]:
        """Generate a valid joint probability distribution.

        Args:
            rows: Number of X values.
            cols: Number of Y values.

        Returns:
            2D list of probabilities summing to 1.
        """
        raw = [[self._rng.randint(1, 10) for _ in range(cols)]
               for _ in range(rows)]
        total = sum(sum(row) for row in raw)
        joint = [[round(v / total, 4) for v in row] for row in raw]
        current_sum = sum(sum(row) for row in joint) - joint[-1][-1]
        joint[-1][-1] = round(1.0 - current_sum, 4)
        return joint

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Slepian-Wolf rate region problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        rows, cols = self._SIZES.get(difficulty, (3, 3))
        joint = self._generate_joint(rows, cols)

        # Marginals
        p_x = [round(sum(joint[i][j] for j in range(cols)), 4)
               for i in range(rows)]
        p_y = [round(sum(joint[i][j] for i in range(rows)), 4)
               for j in range(cols)]

        # Entropies
        h_x = round(_entropy_from_dist(p_x), 4)
        h_y = round(_entropy_from_dist(p_y), 4)

        h_xy = 0.0
        for row in joint:
            for p in row:
                if p > 0:
                    h_xy -= p * math.log2(p)
        h_xy = round(h_xy, 4)

        # Conditional entropies
        h_x_given_y = round(h_xy - h_y, 4)
        h_y_given_x = round(h_xy - h_x, 4)

        table_str = "; ".join(
            "[" + ",".join(str(v) for v in row) + "]"
            for row in joint
        )

        problem = f"SW: P(X,Y)=[{table_str}]"
        return problem, {
            "joint": joint, "rows": rows, "cols": cols,
            "p_x": p_x, "p_y": p_y,
            "h_x": h_x, "h_y": h_y, "h_xy": h_xy,
            "h_x_given_y": h_x_given_y, "h_y_given_x": h_y_given_x,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Slepian-Wolf rate region steps.

        Args:
            data: Solution data with entropies.

        Returns:
            Steps showing H(X|Y), H(Y|X), H(X,Y).
        """
        return [
            f"H(X)={data['h_x']}, H(Y)={data['h_y']}",
            f"H(X,Y)={data['h_xy']}",
            f"R1 >= H(X|Y)={data['h_x_given_y']}",
            f"R2 >= H(Y|X)={data['h_y_given_x']}",
            f"R1+R2 >= H(X,Y)={data['h_xy']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the rate region bounds.

        Args:
            data: Solution data.

        Returns:
            Rate bounds as a string.
        """
        return (
            f"R1>={data['h_x_given_y']}, R2>={data['h_y_given_x']}, "
            f"R1+R2>={data['h_xy']}"
        )


# ===================================================================
# 2. Multiple Access Channel (tier 6)
# ===================================================================

@register
class MultipleAccessChannelGenerator(StepGenerator):
    """Compute MAC capacity region bounds.

    R1 <= I(X1;Y|X2), R2 <= I(X2;Y|X1), R1+R2 <= I(X1,X2;Y).
    For a binary MAC with Y = f(X1,X2) + noise.

    Difficulty scaling:
        Difficulty 1-3: Binary XOR MAC, noise prob 0.1.
        Difficulty 4-6: Binary OR MAC, noise prob varies.
        Difficulty 7-8: Binary AND MAC, noise prob varies.

    Prerequisites:
        mutual_information.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "multiple_access_channel"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["mutual_information"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute MAC capacity region bounds"

    def _config(self, difficulty: int) -> tuple[str, float]:
        """Map difficulty to MAC type and noise probability.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (gate_type, noise_prob).
        """
        if difficulty <= 3:
            return "XOR", 0.1
        if difficulty <= 6:
            return "OR", round(self._rng.uniform(0.05, 0.2), 2)
        return "AND", round(self._rng.uniform(0.05, 0.2), 2)

    def _mac_output(self, gate: str, x1: int, x2: int) -> int:
        """Compute noiseless MAC output.

        Args:
            gate: Gate type ("XOR", "OR", or "AND").
            x1: First input bit.
            x2: Second input bit.

        Returns:
            Output bit.
        """
        if gate == "XOR":
            return x1 ^ x2
        if gate == "OR":
            return x1 | x2
        return x1 & x2

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a MAC capacity region problem.

        Args:
            difficulty: Controls MAC type and noise.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        gate, noise = self._config(difficulty)

        # Assume uniform inputs: P(X1=0)=P(X1=1)=0.5, same for X2
        # Compute joint P(X1,X2,Y)
        p_joint = {}  # (x1, x2, y) -> prob
        for x1 in [0, 1]:
            for x2 in [0, 1]:
                y_clean = self._mac_output(gate, x1, x2)
                p_input = 0.25  # uniform
                p_joint[(x1, x2, y_clean)] = round(
                    p_input * (1 - noise), 4)
                p_joint[(x1, x2, 1 - y_clean)] = round(
                    p_input * noise, 4)

        # P(Y)
        p_y = {0: 0.0, 1: 0.0}
        for (x1, x2, y), p in p_joint.items():
            p_y[y] += p
        p_y = {k: round(v, 4) for k, v in p_y.items()}

        # H(Y)
        h_y = round(_entropy_from_dist([p_y[0], p_y[1]]), 4)

        # H(Y|X1): for each x1, compute H(Y|X1=x1) weighted
        h_y_given_x1 = 0.0
        for x1_val in [0, 1]:
            py_given_x1 = {0: 0.0, 1: 0.0}
            px1 = 0.0
            for (x1, x2, y), p in p_joint.items():
                if x1 == x1_val:
                    py_given_x1[y] += p
                    px1 += p
            if px1 > 0:
                dist = [py_given_x1[0] / px1, py_given_x1[1] / px1]
                h_y_given_x1 += px1 * _entropy_from_dist(dist)
        h_y_given_x1 = round(h_y_given_x1, 4)

        # H(Y|X2): symmetric for X2
        h_y_given_x2 = 0.0
        for x2_val in [0, 1]:
            py_given_x2 = {0: 0.0, 1: 0.0}
            px2 = 0.0
            for (x1, x2, y), p in p_joint.items():
                if x2 == x2_val:
                    py_given_x2[y] += p
                    px2 += p
            if px2 > 0:
                dist = [py_given_x2[0] / px2, py_given_x2[1] / px2]
                h_y_given_x2 += px2 * _entropy_from_dist(dist)
        h_y_given_x2 = round(h_y_given_x2, 4)

        # H(Y|X1,X2) = H(noise) for BSC
        h_y_given_x1x2 = round(_binary_entropy(noise), 4)

        # Capacity bounds
        i_x1_y_given_x2 = round(h_y_given_x2 - h_y_given_x1x2, 4)
        i_x2_y_given_x1 = round(h_y_given_x1 - h_y_given_x1x2, 4)
        i_x1x2_y = round(h_y - h_y_given_x1x2, 4)

        problem = f"MAC({gate}): noise={noise}, uniform inputs"
        return problem, {
            "gate": gate, "noise": noise,
            "h_y": h_y, "h_y_given_x1": h_y_given_x1,
            "h_y_given_x2": h_y_given_x2,
            "h_y_given_x1x2": h_y_given_x1x2,
            "r1_max": i_x1_y_given_x2,
            "r2_max": i_x2_y_given_x1,
            "r_sum_max": i_x1x2_y,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate MAC capacity computation steps.

        Args:
            data: Solution data with entropies and bounds.

        Returns:
            Steps showing entropy values and capacity bounds.
        """
        return [
            f"H(Y)={data['h_y']}, H(noise)={data['h_y_given_x1x2']}",
            f"H(Y|X1)={data['h_y_given_x1']}, H(Y|X2)={data['h_y_given_x2']}",
            f"R1 <= I(X1;Y|X2)={data['r1_max']}",
            f"R2 <= I(X2;Y|X1)={data['r2_max']}",
            f"R1+R2 <= I(X1,X2;Y)={data['r_sum_max']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the capacity region bounds.

        Args:
            data: Solution data.

        Returns:
            Rate bounds as a string.
        """
        return (
            f"R1<={data['r1_max']}, R2<={data['r2_max']}, "
            f"R1+R2<={data['r_sum_max']}"
        )


# ===================================================================
# 3. Rate-Distortion Binary (tier 6)
# ===================================================================

@register
class RateDistortionBinaryGenerator(StepGenerator):
    """Compute rate-distortion R(D) for BSC with Hamming distortion.

    R(D) = H(p) - H(D) for 0 <= D <= min(p, 1-p).
    Also compute Shannon lower bound R_SLB = H(p) - H(D).

    Difficulty scaling:
        Difficulty 1-3: p = 0.5, D in simple fractions.
        Difficulty 4-6: p varies, D = 0.01-0.2.
        Difficulty 7-8: Fine-grained p and D, compute multiple D points.

    Prerequisites:
        info_entropy.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "rate_distortion_binary"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["info_entropy"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute binary rate-distortion R(D) with Shannon bound"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a binary rate-distortion problem.

        Args:
            difficulty: Controls source probability and distortion.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            p = 0.5
            d_vals = [self._rng.choice([0.05, 0.1, 0.15])]
        elif difficulty <= 6:
            p = round(self._rng.uniform(0.2, 0.8), 2)
            d_vals = [round(self._rng.uniform(0.01, 0.2), 2)]
        else:
            p = round(self._rng.uniform(0.15, 0.85), 3)
            d_vals = sorted([
                round(self._rng.uniform(0.01, 0.15), 3)
                for _ in range(2)
            ])

        d_max = round(min(p, 1.0 - p), 4)
        h_p = round(_binary_entropy(p), 4)

        results = []
        for d in d_vals:
            h_d = round(_binary_entropy(d), 4)
            if d <= d_max:
                r_d = round(max(0.0, h_p - h_d), 4)
            else:
                r_d = 0.0
            results.append({
                "d": d, "h_d": h_d, "r_d": r_d,
                "in_range": d <= d_max,
            })

        d_str = ", ".join(str(r["d"]) for r in results)
        problem = f"R(D): P(1)={p}, D=[{d_str}]"
        return problem, {
            "p": p, "h_p": h_p, "d_max": d_max, "results": results,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate rate-distortion computation steps.

        Args:
            data: Solution data with R(D) for each distortion.

        Returns:
            Steps showing H(p), D_max, and R(D) for each point.
        """
        steps: list[str] = [
            f"H(p)=H({data['p']})={data['h_p']}",
            f"D_max=min({data['p']},{round(1.0-data['p'],4)})={data['d_max']}",
        ]
        for r in data["results"]:
            if r["in_range"]:
                steps.append(
                    f"D={r['d']}: H(D)={r['h_d']}, "
                    f"R(D)={data['h_p']}-{r['h_d']}={r['r_d']}"
                )
            else:
                steps.append(f"D={r['d']} > D_max={data['d_max']}: R(D)=0")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the rate-distortion values.

        Args:
            data: Solution data.

        Returns:
            R(D) values as a string.
        """
        parts = [f"R({r['d']})={r['r_d']}" for r in data["results"]]
        return ", ".join(parts)


# ===================================================================
# 4. AEP Property (tier 5)
# ===================================================================

@register
class AEPPropertyGenerator(StepGenerator):
    """Compute asymptotic equipartition property quantities.

    For a discrete memoryless source X with distribution p:
    - P(x^n) ~ 2^{-n*H(X)} for typical x^n.
    - |A_eps^n| ~ 2^{n*H(X)}.
    - Probability of typical set -> 1 as n -> inf.

    Difficulty scaling:
        Difficulty 1-3: Binary source, n = 5-10.
        Difficulty 4-6: 3-symbol source, n = 10-20.
        Difficulty 7-8: 4-symbol source, n = 20-50.

    Prerequisites:
        info_entropy.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "aep_property"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["info_entropy"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute AEP typical set properties for a source"

    def _config(self, difficulty: int) -> tuple[int, int]:
        """Map difficulty to alphabet size and block length.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (alphabet_size, block_length).
        """
        if difficulty <= 3:
            return 2, self._rng.randint(5, 10)
        if difficulty <= 6:
            return 3, self._rng.randint(10, 20)
        return 4, self._rng.randint(20, 50)

    def _generate_dist(self, k: int) -> list[float]:
        """Generate a valid probability distribution over k symbols.

        Args:
            k: Alphabet size.

        Returns:
            Probability distribution summing to 1.
        """
        raw = [self._rng.randint(1, 10) for _ in range(k)]
        total = sum(raw)
        dist = [round(v / total, 4) for v in raw]
        dist[-1] = round(1.0 - sum(dist[:-1]), 4)
        return dist

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an AEP problem for a discrete source.

        Args:
            difficulty: Controls alphabet size and block length.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        k, n = self._config(difficulty)
        dist = self._generate_dist(k)

        h_x = round(_entropy_from_dist(dist), 4)
        n_h = round(n * h_x, 4)
        typical_size = round(2.0 ** n_h, 4)
        total_seqs = k ** n
        # Probability per typical sequence
        p_typical = round(2.0 ** (-n_h), 4) if n_h > 0 else 0.0
        fraction = round(typical_size / total_seqs, 4) if total_seqs > 0 else 0.0

        dist_str = "[" + ",".join(str(p) for p in dist) + "]"
        problem = f"AEP: P={dist_str}, n={n}"
        return problem, {
            "dist": dist, "k": k, "n": n,
            "h_x": h_x, "n_h": n_h,
            "typical_size": typical_size,
            "total_seqs": total_seqs,
            "p_typical": p_typical,
            "fraction": fraction,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate AEP computation steps.

        Args:
            data: Solution data with entropy and typical set.

        Returns:
            Steps showing H(X), typical set size, and probability.
        """
        return [
            f"H(X)={data['h_x']} bits",
            f"n*H(X)={data['n']}*{data['h_x']}={data['n_h']}",
            f"|A_eps|~2^{{{data['n_h']}}}~{data['typical_size']}",
            f"total seqs={data['k']}^{data['n']}={data['total_seqs']}",
            f"P(typical seq)~2^(-{data['n_h']})~{data['p_typical']}",
            f"fraction={data['fraction']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the AEP quantities.

        Args:
            data: Solution data.

        Returns:
            Typical set size and fraction as a string.
        """
        return (
            f"|A_eps|~{data['typical_size']}, "
            f"fraction={data['fraction']}"
        )


# ===================================================================
# 5. Polar Code (tier 6)
# ===================================================================

@register
class PolarCodeGenerator(StepGenerator):
    """Compute polar code channel reliability parameters.

    For BSC with crossover probability p, compute Bhattacharyya
    parameter Z(W) = 2*sqrt(p*(1-p)) for each sub-channel after
    polarization. Frozen bits assigned to unreliable sub-channels.

    Difficulty scaling:
        Difficulty 1-3: N=2, 1 polarization step.
        Difficulty 4-6: N=4, 2 polarization steps.
        Difficulty 7-8: N=8, 3 polarization steps.

    Prerequisites:
        basic_prob.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "polar_code"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["basic_prob"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute polar code reliability and frozen bit assignment"

    def _config(self, difficulty: int) -> int:
        """Map difficulty to code length N.

        Args:
            difficulty: Difficulty level.

        Returns:
            Code length (power of 2).
        """
        if difficulty <= 3:
            return 2
        if difficulty <= 6:
            return 4
        return 8

    def _polarize(self, z_vals: list[float]) -> list[float]:
        """Perform one level of channel polarization.

        Args:
            z_vals: Current Bhattacharyya parameters.

        Returns:
            Polarized parameters (doubled in count).
        """
        result = []
        for z in z_vals:
            # W- (bad channel): Z- = 2*z - z^2
            z_minus = round(min(1.0, 2 * z - z ** 2), 4)
            # W+ (good channel): Z+ = z^2
            z_plus = round(z ** 2, 4)
            result.append(z_minus)
            result.append(z_plus)
        return result

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a polar code reliability problem.

        Args:
            difficulty: Controls code length.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        n_val = self._config(difficulty)
        p = round(self._rng.uniform(0.05, 0.3), 2)

        # Initial Bhattacharyya parameter for BSC
        z0 = round(2 * math.sqrt(p * (1 - p)), 4)

        # Polarize
        z_current = [z0]
        levels = [[z0]]
        n_steps = int(math.log2(n_val))
        for _ in range(n_steps):
            z_current = self._polarize(z_current)
            levels.append(list(z_current))

        # Classify: Z < 0.5 = good (info), Z >= 0.5 = bad (frozen)
        threshold = 0.5
        frozen = [i for i, z in enumerate(z_current) if z >= threshold]
        info = [i for i, z in enumerate(z_current) if z < threshold]
        rate = round(len(info) / n_val, 4)

        problem = f"polar: BSC(p={p}), N={n_val}"
        return problem, {
            "p": p, "z0": z0, "n": n_val,
            "levels": levels, "final_z": z_current,
            "frozen": frozen, "info": info, "rate": rate,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate polar code computation steps.

        Args:
            data: Solution data with polarization levels.

        Returns:
            Steps showing Z parameters at each level.
        """
        steps: list[str] = [
            f"BSC(p={data['p']}): Z0={data['z0']}"
        ]
        for lvl, z_vals in enumerate(data["levels"][1:], 1):
            z_str = ",".join(str(z) for z in z_vals)
            steps.append(f"level {lvl}: Z=[{z_str}]")
        steps.append(f"frozen={data['frozen']}, info={data['info']}")
        steps.append(f"rate={data['rate']}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the frozen bit assignment and rate.

        Args:
            data: Solution data.

        Returns:
            Frozen channels and rate as a string.
        """
        return f"frozen={data['frozen']}, rate={data['rate']}"


# ===================================================================
# 6. Entropy Rate (tier 5)
# ===================================================================

@register
class EntropyRateGenerator(StepGenerator):
    """Compute entropy rate of a stationary Markov chain.

    H_rate = -sum_i pi_i * sum_j P_{ij} * log2(P_{ij})
    where pi is the stationary distribution.

    Difficulty scaling:
        Difficulty 1-3: 2-state Markov chain.
        Difficulty 4-6: 3-state Markov chain.
        Difficulty 7-8: 4-state Markov chain.

    Prerequisites:
        info_entropy.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "entropy_rate"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["info_entropy"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute entropy rate of a stationary Markov chain"

    def _n_states(self, difficulty: int) -> int:
        """Map difficulty to number of states.

        Args:
            difficulty: Difficulty level.

        Returns:
            Number of Markov chain states (2-4).
        """
        if difficulty <= 3:
            return 2
        if difficulty <= 6:
            return 3
        return 4

    def _generate_transition(self, n: int) -> list[list[float]]:
        """Generate a valid row-stochastic transition matrix.

        Args:
            n: Number of states.

        Returns:
            n x n transition matrix with rows summing to 1.
        """
        matrix = []
        for _ in range(n):
            raw = [self._rng.randint(1, 10) for _ in range(n)]
            total = sum(raw)
            row = [round(v / total, 4) for v in raw]
            row[-1] = round(1.0 - sum(row[:-1]), 4)
            matrix.append(row)
        return matrix

    def _stationary_dist(self, trans: list[list[float]],
                         n: int) -> list[float]:
        """Compute stationary distribution by power iteration.

        Args:
            trans: Transition matrix.
            n: Number of states.

        Returns:
            Stationary distribution rounded to 4 dp.
        """
        pi = [1.0 / n] * n
        for _ in range(200):
            pi_new = [0.0] * n
            for j in range(n):
                for i in range(n):
                    pi_new[j] += pi[i] * trans[i][j]
            pi = pi_new
        return [round(p, 4) for p in pi]

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Markov chain entropy rate problem.

        Args:
            difficulty: Controls number of states.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        n = self._n_states(difficulty)
        trans = self._generate_transition(n)
        pi = self._stationary_dist(trans, n)

        # Fix pi to sum to 1
        pi_sum = sum(pi)
        if abs(pi_sum - 1.0) > 0.001:
            pi = [round(p / pi_sum, 4) for p in pi]
            pi[-1] = round(1.0 - sum(pi[:-1]), 4)

        # H_rate = -sum_i pi_i * sum_j P_ij * log2(P_ij)
        per_state = []
        h_rate = 0.0
        for i in range(n):
            hi = 0.0
            for j in range(n):
                if trans[i][j] > 0:
                    hi -= trans[i][j] * math.log2(trans[i][j])
            hi = round(hi, 4)
            per_state.append(hi)
            h_rate += pi[i] * hi
        h_rate = round(h_rate, 4)

        trans_str = "; ".join(
            "[" + ",".join(str(v) for v in row) + "]"
            for row in trans
        )
        problem = f"Markov: P=[{trans_str}]"
        return problem, {
            "n": n, "trans": trans, "pi": pi,
            "per_state": per_state, "h_rate": h_rate,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate entropy rate computation steps.

        Args:
            data: Solution data with stationary dist and per-state entropy.

        Returns:
            Steps showing pi, per-state H, and entropy rate.
        """
        pi_str = "[" + ",".join(str(p) for p in data["pi"]) + "]"
        steps: list[str] = [f"pi={pi_str}"]
        for i, hi in enumerate(data["per_state"]):
            steps.append(f"H(X|state={i})={hi}")
        steps.append(
            f"H_rate=sum pi_i*H_i={data['h_rate']}"
        )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the entropy rate.

        Args:
            data: Solution data.

        Returns:
            Entropy rate as a string.
        """
        return f"H_rate={data['h_rate']}"
