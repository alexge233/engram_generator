"""Cognitive science generators.

6 generators across tiers 4-6 covering signal detection theory,
memory decay, reaction time, Weber fraction, information processing,
and Rescorla-Wagner conditioning.
"""
from __future__ import annotations

import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

# Standard normal z-score lookup table for common hit/FA rates.
_Z_TABLE: dict[float, float] = {
    0.01: -2.3263, 0.02: -2.0537, 0.05: -1.6449, 0.10: -1.2816,
    0.15: -1.0364, 0.20: -0.8416, 0.25: -0.6745, 0.30: -0.5244,
    0.35: -0.3853, 0.40: -0.2533, 0.45: -0.1257, 0.50: 0.0,
    0.55: 0.1257, 0.60: 0.2533, 0.65: 0.3853, 0.70: 0.5244,
    0.75: 0.6745, 0.80: 0.8416, 0.85: 1.0364, 0.90: 1.2816,
    0.95: 1.6449, 0.98: 2.0537, 0.99: 2.3263,
}


def _z_lookup(p: float) -> float:
    """Look up z-score for a probability using the table.

    Falls back to Abramowitz & Stegun approximation when exact
    value is not in the table.

    Args:
        p: Probability in (0, 1).

    Returns:
        Approximate z-score rounded to 4 decimal places.
    """
    if p in _Z_TABLE:
        return _Z_TABLE[p]
    # Abramowitz & Stegun rational approximation
    if p <= 0.0 or p >= 1.0:
        return 0.0
    sign = 1.0
    q = p
    if p < 0.5:
        q = 1.0 - p
        sign = -1.0
    t = math.sqrt(-2.0 * math.log(1.0 - q))
    c0, c1, c2 = 2.515517, 0.802853, 0.010328
    d1, d2, d3 = 1.432788, 0.189269, 0.001308
    z = t - (c0 + c1 * t + c2 * t * t) / (
        1.0 + d1 * t + d2 * t * t + d3 * t * t * t
    )
    return round(sign * z, 4)


# ---------------------------------------------------------------------------
# 1. Signal Detection Theory (tier 5)
# ---------------------------------------------------------------------------

@register
class SignalDetectionGenerator(StepGenerator):
    """Compute d-prime from hit rate and false alarm rate.

    d' = z(hit_rate) - z(false_alarm_rate). Given hit rate and FA
    rate, look up z-scores and compute the sensitivity index.

    Difficulty scaling:
        Difficulty 1-3: rates from common table values.
        Difficulty 4-6: rates with finer granularity.
        Difficulty 7-8: extreme hit/FA rates near boundaries.

    Prerequisites:
        z_score.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "signal_detection"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["z_score"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute d' (d-prime) from hit rate and false alarm rate"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a signal detection problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (problem_text, solution_data).
        """
        table_keys = sorted(_Z_TABLE.keys())
        if difficulty <= 3:
            # Use nice table values
            hit_rate = self._rng.choice(
                [k for k in table_keys if 0.5 <= k <= 0.95]
            )
            fa_rate = self._rng.choice(
                [k for k in table_keys if 0.05 <= k < hit_rate]
            )
        elif difficulty <= 6:
            hit_rate = round(self._rng.uniform(0.55, 0.95), 2)
            fa_rate = round(self._rng.uniform(0.05, min(0.45, hit_rate - 0.1)), 2)
        else:
            hit_rate = round(self._rng.uniform(0.80, 0.99), 2)
            fa_rate = round(self._rng.uniform(0.01, 0.15), 2)

        z_hit = _z_lookup(hit_rate)
        z_fa = _z_lookup(fa_rate)
        d_prime = round(z_hit - z_fa, 4)

        problem = f"hit rate = {hit_rate}, FA rate = {fa_rate}. d'?"
        return problem, {
            "hit_rate": hit_rate, "fa_rate": fa_rate,
            "z_hit": z_hit, "z_fa": z_fa, "d_prime": d_prime,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate signal detection computation steps.

        Args:
            sd: Solution data dict.

        Returns:
            Steps showing z-score lookups and d' computation.
        """
        return [
            f"z(hit={sd['hit_rate']}) = {sd['z_hit']}",
            f"z(FA={sd['fa_rate']}) = {sd['z_fa']}",
            f"d' = {sd['z_hit']} - {sd['z_fa']} = {sd['d_prime']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return d-prime.

        Args:
            sd: Solution data dict.

        Returns:
            d' value as string.
        """
        return f"d' = {sd['d_prime']}"


# ---------------------------------------------------------------------------
# 2. Memory Decay / Ebbinghaus (tier 5)
# ---------------------------------------------------------------------------

@register
class MemoryDecayGenerator(StepGenerator):
    """Compute retention using the Ebbinghaus forgetting curve.

    R = e^(-t/S) where S is memory strength and t is time elapsed.

    Difficulty scaling:
        Difficulty 1-3: integer time and strength values.
        Difficulty 4-6: fractional strength values.
        Difficulty 7-8: multiple time points to compare.

    Prerequisites:
        exponentiation.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "memory_decay"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["exponentiation"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute retention using Ebbinghaus forgetting curve R=e^(-t/S)"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a memory decay problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            s = float(self._rng.randint(1, 5))
            n_times = 1
        elif difficulty <= 6:
            s = round(self._rng.uniform(0.5, 8.0), 2)
            n_times = 1
        else:
            s = round(self._rng.uniform(0.5, 10.0), 2)
            n_times = self._rng.randint(2, 3)

        times = sorted(
            [self._rng.randint(1, 20 * max(1, difficulty))
             for _ in range(n_times)]
        )
        retentions = [round(math.exp(-t / s), 4) for t in times]

        if n_times == 1:
            problem = f"S={s}, t={times[0]}. R = e^(-t/S)?"
        else:
            t_str = ", ".join(str(t) for t in times)
            problem = f"S={s}, times=[{t_str}]. R = e^(-t/S) for each?"

        return problem, {
            "s": s, "times": times, "retentions": retentions,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate memory decay computation steps.

        Args:
            sd: Solution data dict.

        Returns:
            Steps showing exponent computation for each time point.
        """
        steps = []
        for t, r in zip(sd["times"], sd["retentions"]):
            exponent = round(-t / sd["s"], 4)
            steps.append(f"R({t}) = e^({exponent}) = {r}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return retention values.

        Args:
            sd: Solution data dict.

        Returns:
            Retention value(s) as string.
        """
        if len(sd["times"]) == 1:
            return f"R = {sd['retentions'][0]}"
        parts = ", ".join(
            f"R({t})={r}" for t, r in zip(sd["times"], sd["retentions"])
        )
        return parts


# ---------------------------------------------------------------------------
# 3. Reaction Time / Hick's Law (tier 5)
# ---------------------------------------------------------------------------

@register
class ReactionTimeGenerator(StepGenerator):
    """Compute reaction time using Hick's law.

    RT = a + b * log2(n) where a is base RT, b is slope, and n is
    the number of stimulus-response alternatives.

    Difficulty scaling:
        Difficulty 1-3: small n (2-4), round a and b.
        Difficulty 4-6: moderate n (4-8), decimal a and b.
        Difficulty 7-8: large n (8-16), fine-grained parameters.

    Prerequisites:
        logarithm.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "reaction_time"

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
        return "compute reaction time using Hick's law RT = a + b*log2(n)"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Hick's law problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            a = float(self._rng.randint(150, 300))
            b = float(self._rng.randint(50, 150))
            n = self._rng.randint(2, 4)
        elif difficulty <= 6:
            a = round(self._rng.uniform(100.0, 350.0), 1)
            b = round(self._rng.uniform(30.0, 180.0), 1)
            n = self._rng.randint(4, 8)
        else:
            a = round(self._rng.uniform(80.0, 400.0), 2)
            b = round(self._rng.uniform(20.0, 200.0), 2)
            n = self._rng.randint(8, 16)

        log2_n = round(math.log2(n), 4)
        rt = round(a + b * log2_n, 4)

        problem = f"a={a} ms, b={b} ms/bit, n={n} choices. RT?"
        return problem, {
            "a": a, "b": b, "n": n, "log2_n": log2_n, "rt": rt,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate Hick's law computation steps.

        Args:
            sd: Solution data dict.

        Returns:
            Steps showing log computation and RT calculation.
        """
        return [
            f"log2({sd['n']}) = {sd['log2_n']}",
            f"RT = {sd['a']} + {sd['b']} * {sd['log2_n']}",
            f"RT = {sd['rt']} ms",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the reaction time.

        Args:
            sd: Solution data dict.

        Returns:
            RT in milliseconds.
        """
        return f"RT = {sd['rt']} ms"


# ---------------------------------------------------------------------------
# 4. Weber Fraction (tier 4)
# ---------------------------------------------------------------------------

@register
class WeberFractionGenerator(StepGenerator):
    """Compute just noticeable difference using Weber's law.

    dI/I = k (Weber's constant). Given stimulus intensity I and
    Weber fraction k, compute JND = k * I.

    Difficulty scaling:
        Difficulty 1-3: integer I, simple k.
        Difficulty 4-6: larger I, finer k.
        Difficulty 7-8: multiple stimuli to compare.

    Prerequisites:
        division.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "weber_fraction"

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
        return "compute JND using Weber's law dI/I = k"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Weber fraction problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            intensities = [self._rng.randint(10, 100)]
            k = round(self._rng.choice([0.01, 0.02, 0.05, 0.1, 0.2]), 2)
        elif difficulty <= 6:
            intensities = [self._rng.randint(50, 500)]
            k = round(self._rng.uniform(0.01, 0.3), 3)
        else:
            n = self._rng.randint(2, 3)
            intensities = sorted(
                [self._rng.randint(100, 1000) for _ in range(n)]
            )
            k = round(self._rng.uniform(0.005, 0.2), 4)

        jnds = [round(k * i, 4) for i in intensities]

        if len(intensities) == 1:
            problem = f"I={intensities[0]}, k={k}. JND?"
        else:
            i_str = ", ".join(str(i) for i in intensities)
            problem = f"intensities=[{i_str}], k={k}. JND for each?"

        return problem, {
            "intensities": intensities, "k": k, "jnds": jnds,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate Weber fraction computation steps.

        Args:
            sd: Solution data dict.

        Returns:
            Steps showing JND = k * I for each intensity.
        """
        steps = []
        for i, jnd in zip(sd["intensities"], sd["jnds"]):
            steps.append(f"JND({i}) = {sd['k']} * {i} = {jnd}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the JND value(s).

        Args:
            sd: Solution data dict.

        Returns:
            JND as string.
        """
        if len(sd["intensities"]) == 1:
            return f"JND = {sd['jnds'][0]}"
        parts = ", ".join(
            f"JND({i})={jnd}"
            for i, jnd in zip(sd["intensities"], sd["jnds"])
        )
        return parts


# ---------------------------------------------------------------------------
# 5. Information Processing / Channel Capacity (tier 6)
# ---------------------------------------------------------------------------

@register
class InformationProcessingGenerator(StepGenerator):
    """Compute bits transmitted in absolute identification task.

    Human channel capacity for absolute identification is approximately
    2.5 bits. Given a stimulus set of size n, compute information
    transmitted H_t = min(log2(n), C) where C ~ 2.5 bits.

    Difficulty scaling:
        Difficulty 1-3: 2-4 stimuli.
        Difficulty 4-6: 4-8 stimuli, compute H_t and accuracy.
        Difficulty 7-8: 8-32 stimuli, compare to capacity.

    Prerequisites:
        channel_capacity.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "information_processing"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["channel_capacity"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute bits transmitted in absolute identification task"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an information processing problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (problem_text, solution_data).
        """
        capacity = 2.5  # Miller's magic number channel capacity

        if difficulty <= 3:
            n_stimuli = self._rng.randint(2, 4)
        elif difficulty <= 6:
            n_stimuli = self._rng.randint(4, 8)
        else:
            n_stimuli = self._rng.choice([8, 10, 12, 16, 20, 32])

        h_input = round(math.log2(n_stimuli), 4)
        h_transmitted = round(min(h_input, capacity), 4)
        # Effective categories distinguishable
        eff_categories = round(2.0 ** h_transmitted, 4)
        # Approximate accuracy when limited by capacity
        accuracy = round(min(1.0, eff_categories / n_stimuli), 4)

        problem = (
            f"absolute identification: {n_stimuli} stimuli, "
            f"C=2.5 bits. bits transmitted?"
        )
        return problem, {
            "n_stimuli": n_stimuli, "capacity": capacity,
            "h_input": h_input, "h_transmitted": h_transmitted,
            "eff_categories": eff_categories, "accuracy": accuracy,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate information processing steps.

        Args:
            sd: Solution data dict.

        Returns:
            Steps showing input entropy, capacity limit, and accuracy.
        """
        return [
            f"H(input) = log2({sd['n_stimuli']}) = {sd['h_input']} bits",
            f"C = {sd['capacity']} bits",
            f"H_t = min({sd['h_input']}, {sd['capacity']}) = {sd['h_transmitted']} bits",
            f"effective categories = 2^{sd['h_transmitted']} = {sd['eff_categories']}",
            f"approx accuracy = {sd['accuracy']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return bits transmitted and accuracy.

        Args:
            sd: Solution data dict.

        Returns:
            H_t and accuracy as string.
        """
        return f"H_t = {sd['h_transmitted']} bits, accuracy = {sd['accuracy']}"


# ---------------------------------------------------------------------------
# 6. Rescorla-Wagner (tier 5)
# ---------------------------------------------------------------------------

@register
class RescorlaWagnerGenerator(StepGenerator):
    """Update associative strength using the Rescorla-Wagner rule.

    dV = alpha * beta * (lambda - V). Update V over one or more
    conditioning trials.

    Difficulty scaling:
        Difficulty 1-3: 1 trial, simple parameters.
        Difficulty 4-6: 2-3 trials, track V across trials.
        Difficulty 7-8: 3-5 trials, multiple CSs with summed V.

    Prerequisites:
        multiplication.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "rescorla_wagner"

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
        return "update associative strength using Rescorla-Wagner rule"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Rescorla-Wagner conditioning problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (problem_text, solution_data).
        """
        alpha = round(self._rng.uniform(0.1, 0.5), 2)
        beta = round(self._rng.uniform(0.1, 0.5), 2)
        lam = round(self._rng.uniform(0.5, 1.0), 2)

        if difficulty <= 3:
            n_trials = 1
        elif difficulty <= 6:
            n_trials = self._rng.randint(2, 3)
        else:
            n_trials = self._rng.randint(3, 5)

        v = 0.0
        trial_data = []
        for _ in range(n_trials):
            dv = round(alpha * beta * (lam - v), 4)
            v_new = round(v + dv, 4)
            trial_data.append({
                "v_before": round(v, 4), "dv": dv, "v_after": v_new,
            })
            v = v_new

        problem = (
            f"alpha={alpha}, beta={beta}, lambda={lam}, V0=0; "
            f"{n_trials} trial(s). final V?"
        )
        return problem, {
            "alpha": alpha, "beta": beta, "lam": lam,
            "trials": trial_data, "final_v": trial_data[-1]["v_after"],
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate Rescorla-Wagner update steps.

        Args:
            sd: Solution data dict.

        Returns:
            Steps showing dV and updated V for each trial.
        """
        steps = []
        for i, t in enumerate(sd["trials"]):
            steps.append(
                f"trial {i+1}: dV = {sd['alpha']}*{sd['beta']}*"
                f"({sd['lam']} - {t['v_before']}) = {t['dv']}"
            )
            steps.append(
                f"V = {t['v_before']} + {t['dv']} = {t['v_after']}"
            )
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the final associative strength.

        Args:
            sd: Solution data dict.

        Returns:
            Final V value.
        """
        return f"V = {sd['final_v']}"
