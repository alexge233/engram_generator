"""Deep distributed systems generators.

8 generators across tiers 4-6 covering Byzantine generals, quorum
systems, eventual consistency, sharding strategy, replication factor,
LSM tree computation, gossip protocol, and snapshot algorithm.
"""
from __future__ import annotations

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


# ---------------------------------------------------------------------------
# 1. Byzantine Generals (tier 6)
# ---------------------------------------------------------------------------

@register
class ByzantineGeneralsGenerator(StepGenerator):
    """Determine if Byzantine consensus is achievable.

    With f faulty generals, need 3f+1 total for consensus. Given
    n generals and f faults, determine if consensus is possible,
    and compute the number of message rounds required.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "byzantine_generals"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["comparison"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task instruction string.
        """
        return "determine if Byzantine consensus is achievable"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Byzantine generals problem.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        f = self._rng.randint(1, min(2 + difficulty // 2, 5))
        threshold = 3 * f + 1
        if self._rng.random() < 0.6:
            n = self._rng.randint(threshold, threshold + 3)
        else:
            n = self._rng.randint(max(2, threshold - 2), threshold - 1)

        possible = n >= threshold
        rounds = f + 1 if possible else 0
        loyal = n - f

        steps = [
            f"n={n} generals, f={f} faulty",
            f"need 3f+1 = {threshold} for consensus",
            f"n={n} >= {threshold}? => {'YES' if possible else 'NO'}",
        ]
        if possible:
            steps.append(f"loyal={loyal}, rounds needed=f+1={rounds}")
        else:
            steps.append(f"insufficient generals, consensus impossible")

        problem = f"Byzantine: n={n}, f={f}"
        return problem, {
            "steps": steps,
            "possible": possible,
            "threshold": threshold,
            "rounds": rounds,
        }

    def _create_steps(self, solution_data: dict) -> list[str]:
        """Return the analysis steps.

        Args:
            solution_data: All computed solution information.

        Returns:
            Step strings in execution order.
        """
        return solution_data["steps"]

    def _create_answer(self, solution_data: dict) -> str:
        """Return the consensus verdict.

        Args:
            solution_data: All computed solution information.

        Returns:
            Consensus possible/impossible string.
        """
        d = solution_data
        if d["possible"]:
            return f"POSSIBLE, rounds={d['rounds']}"
        return f"IMPOSSIBLE (need {d['threshold']})"


# ---------------------------------------------------------------------------
# 2. Quorum Systems (tier 5)
# ---------------------------------------------------------------------------

@register
class QuorumSystemsGenerator(StepGenerator):
    """Compute valid read/write quorum pairs.

    For N replicas, read quorum R + write quorum W must be > N.
    Also W > N/2 for write-write conflict resolution. Find all
    valid (R, W) pairs.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "quorum_systems"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["addition"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task instruction string.
        """
        return "find valid read/write quorum pairs for N replicas"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a quorum systems problem.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        n = self._rng.randint(3, min(3 + difficulty, 9))
        half_n = n / 2

        valid_pairs = []
        for w in range(1, n + 1):
            if w <= half_n:
                continue
            r_min = n - w + 1
            for r in range(max(1, r_min), n + 1):
                valid_pairs.append((r, w))

        sample_count = min(len(valid_pairs), 3 + difficulty // 2)
        shown_pairs = self._rng.sample(valid_pairs, sample_count)
        shown_pairs.sort()

        steps = [
            f"N={n}",
            f"require R+W > {n} and W > {_f(half_n)}",
        ]
        for r, w in shown_pairs:
            steps.append(f"R={r}, W={w}: R+W={r + w}>{n}, W={w}>{_f(half_n)} => VALID")

        problem = f"quorum: N={n}"
        return problem, {
            "steps": steps,
            "n": n,
            "valid_pairs": shown_pairs,
            "total_valid": len(valid_pairs),
        }

    def _create_steps(self, solution_data: dict) -> list[str]:
        """Return the quorum analysis steps.

        Args:
            solution_data: All computed solution information.

        Returns:
            Step strings in execution order.
        """
        return solution_data["steps"]

    def _create_answer(self, solution_data: dict) -> str:
        """Return the valid quorum pairs.

        Args:
            solution_data: All computed solution information.

        Returns:
            Quorum pairs string.
        """
        d = solution_data
        pairs_str = ", ".join(f"({r},{w})" for r, w in d["valid_pairs"])
        return f"valid pairs: {pairs_str} ({d['total_valid']} total)"


# ---------------------------------------------------------------------------
# 3. Eventual Consistency (tier 5)
# ---------------------------------------------------------------------------

@register
class EventualConsistencyGenerator(StepGenerator):
    """Compute gossip convergence with anti-entropy.

    After t rounds of gossip, expected fraction informed =
    1 - (1 - 1/N)^t. Compute the number of rounds needed to
    reach a target convergence threshold.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "eventual_consistency"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["basic_prob"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task instruction string.
        """
        return "compute gossip convergence rounds for target fraction"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an eventual consistency problem.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        n = self._rng.choice([5, 10, 20, 50, 100])
        target = round(self._rng.uniform(0.8, 0.99), 2)
        p_miss = 1.0 - 1.0 / n

        rounds_needed = 0
        fraction = 0.0
        steps = [f"N={n}, target={target}"]
        steps.append(f"fraction(t) = 1 - (1 - 1/{n})^t = 1 - {_f(p_miss)}^t")

        max_rounds = n * 10
        trace = []
        for t in range(1, max_rounds + 1):
            fraction = round(1.0 - p_miss ** t, 4)
            if len(trace) < 5 or fraction >= target:
                trace.append((t, fraction))
            if fraction >= target:
                rounds_needed = t
                break

        for t, frac in trace:
            steps.append(f"t={t}: fraction={_f(frac)}")

        if rounds_needed > 0:
            steps.append(f"reach {target} at t={rounds_needed}")
        else:
            rounds_needed = max_rounds
            steps.append(f"did not reach {target} in {max_rounds} rounds")

        problem = f"anti-entropy: N={n}, target={target}"
        return problem, {
            "steps": steps,
            "rounds": rounds_needed,
            "final_fraction": fraction,
        }

    def _create_steps(self, solution_data: dict) -> list[str]:
        """Return the convergence computation steps.

        Args:
            solution_data: All computed solution information.

        Returns:
            Step strings in execution order.
        """
        return solution_data["steps"]

    def _create_answer(self, solution_data: dict) -> str:
        """Return the convergence result.

        Args:
            solution_data: All computed solution information.

        Returns:
            Rounds needed string.
        """
        return f"rounds={solution_data['rounds']}"


# ---------------------------------------------------------------------------
# 4. Sharding Strategy (tier 5)
# ---------------------------------------------------------------------------

@register
class ShardingStrategyGenerator(StepGenerator):
    """Compare range sharding vs hash sharding.

    Given a key distribution, compute shard sizes under both
    strategies and identify hotspot risk.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "sharding_strategy"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["hash_table_ops"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task instruction string.
        """
        return "compare range vs hash sharding for key distribution"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a sharding strategy problem.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        n_shards = self._rng.choice([3, 4, 5])
        n_keys = self._rng.randint(20, min(30 + difficulty * 10, 80))
        max_key = n_shards * 100

        skew = self._rng.choice(["uniform", "skewed", "hotspot"])
        if skew == "uniform":
            keys = [self._rng.randint(0, max_key - 1) for _ in range(n_keys)]
        elif skew == "skewed":
            hot_range = max_key // n_shards
            keys = []
            for _ in range(n_keys):
                if self._rng.random() < 0.6:
                    keys.append(self._rng.randint(0, hot_range - 1))
                else:
                    keys.append(self._rng.randint(0, max_key - 1))
        else:
            keys = []
            for _ in range(n_keys):
                if self._rng.random() < 0.8:
                    keys.append(self._rng.randint(0, max_key // n_shards - 1))
                else:
                    keys.append(self._rng.randint(0, max_key - 1))

        range_size = max_key // n_shards
        range_counts = [0] * n_shards
        hash_counts = [0] * n_shards
        for k in keys:
            r_shard = min(k // range_size, n_shards - 1)
            h_shard = k % n_shards
            range_counts[r_shard] += 1
            hash_counts[h_shard] += 1

        range_max = max(range_counts)
        range_min = min(range_counts)
        hash_max = max(hash_counts)
        hash_min = min(hash_counts)
        range_imbalance = round(range_max / max(range_min, 1), 4)
        hash_imbalance = round(hash_max / max(hash_min, 1), 4)

        steps = [
            f"{n_keys} keys, {n_shards} shards, dist={skew}",
            f"range sharding: {range_counts}, max/min={_f(range_imbalance)}",
            f"hash sharding: {hash_counts}, max/min={_f(hash_imbalance)}",
        ]

        if range_imbalance > hash_imbalance:
            better = "hash"
            steps.append("hash sharding more balanced")
        elif hash_imbalance > range_imbalance:
            better = "range"
            steps.append("range sharding more balanced")
        else:
            better = "equal"
            steps.append("both equally balanced")

        problem = f"{n_shards} shards, {n_keys} keys, dist={skew}"
        return problem, {
            "steps": steps,
            "better": better,
            "range_imbalance": range_imbalance,
            "hash_imbalance": hash_imbalance,
        }

    def _create_steps(self, solution_data: dict) -> list[str]:
        """Return the sharding analysis steps.

        Args:
            solution_data: All computed solution information.

        Returns:
            Step strings in execution order.
        """
        return solution_data["steps"]

    def _create_answer(self, solution_data: dict) -> str:
        """Return the sharding verdict.

        Args:
            solution_data: All computed solution information.

        Returns:
            Better strategy string.
        """
        d = solution_data
        return (
            f"better={d['better']}, "
            f"range_imbal={_f(d['range_imbalance'])}, "
            f"hash_imbal={_f(d['hash_imbalance'])}"
        )


# ---------------------------------------------------------------------------
# 5. Replication Factor (tier 4)
# ---------------------------------------------------------------------------

@register
class ReplicationFactorGenerator(StepGenerator):
    """Compute quorum constraints and availability for replication.

    Given N replicas and f failures tolerated, verify R + W > N
    and W > N/2. Compute system availability assuming independent
    node failures.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "replication_factor"

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
            Task instruction string.
        """
        return "compute replication quorum constraints and availability"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a replication factor problem.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        n = self._rng.randint(3, min(3 + difficulty, 7))
        f = self._rng.randint(1, n // 2)
        node_reliability = round(self._rng.uniform(0.9, 0.999), 4)

        w = f + 1
        r = n - f

        rw_valid = r + w > n
        ww_valid = w > n / 2

        avail = 0.0
        for k in range(f + 1):
            comb = math.comb(n, k)
            avail += comb * ((1 - node_reliability) ** k) * (node_reliability ** (n - k))
        avail = round(1.0 - (1.0 - avail), 4)

        steps = [
            f"N={n}, f={f}, node_rel={node_reliability}",
            f"W = f+1 = {w}, R = N-f = {r}",
            f"R+W = {r + w} > {n} => {rw_valid}",
            f"W = {w} > N/2 = {_f(n / 2)} => {ww_valid}",
            f"availability = P(at most {f} failures) = {_f(avail)}",
        ]

        problem = f"replication: N={n}, f={f}, rel={node_reliability}"
        return problem, {
            "steps": steps,
            "r": r,
            "w": w,
            "availability": avail,
        }

    def _create_steps(self, solution_data: dict) -> list[str]:
        """Return the replication analysis steps.

        Args:
            solution_data: All computed solution information.

        Returns:
            Step strings in execution order.
        """
        return solution_data["steps"]

    def _create_answer(self, solution_data: dict) -> str:
        """Return the replication parameters.

        Args:
            solution_data: All computed solution information.

        Returns:
            Quorum and availability string.
        """
        d = solution_data
        return f"R={d['r']}, W={d['w']}, avail={_f(d['availability'])}"


# ---------------------------------------------------------------------------
# 6. Log-Structured Merge Tree (tier 5)
# ---------------------------------------------------------------------------

@register
class LogStructuredMergeGenerator(StepGenerator):
    """Compute LSM tree level sizes and total levels.

    L0 size is S, each level grows by ratio T. Level i size = S*T^i.
    Total levels = ceil(log_T(N/S)). Compute for given total data N.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "log_structured_merge"

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
            Task instruction string.
        """
        return "compute LSM tree level sizes and total levels"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an LSM tree computation problem.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        s = self._rng.choice([1, 2, 4, 8])
        t = self._rng.choice([4, 8, 10])
        n = self._rng.choice([64, 256, 1024, 4096, 10000])

        if n <= s:
            n = s * t * t

        total_levels = math.ceil(math.log(n / s) / math.log(t))
        total_levels = max(1, total_levels)

        level_sizes = []
        steps = [f"S={s} MB, T={t}, N={n} MB"]
        steps.append(f"levels = ceil(log_{t}({n}/{s})) = ceil({_f(math.log(n / s) / math.log(t))}) = {total_levels}")

        for i in range(total_levels):
            size = round(s * (t ** i), 4)
            level_sizes.append(size)
            steps.append(f"L{i}: {s}*{t}^{i} = {_f(size)} MB")

        write_amp = round(t * total_levels / 2, 4)
        steps.append(f"write amplification ~ T*L/2 = {_f(write_amp)}")

        problem = f"LSM: S={s}MB, T={t}, N={n}MB"
        return problem, {
            "steps": steps,
            "total_levels": total_levels,
            "level_sizes": level_sizes,
            "write_amp": write_amp,
        }

    def _create_steps(self, solution_data: dict) -> list[str]:
        """Return the LSM computation steps.

        Args:
            solution_data: All computed solution information.

        Returns:
            Step strings in execution order.
        """
        return solution_data["steps"]

    def _create_answer(self, solution_data: dict) -> str:
        """Return the LSM tree parameters.

        Args:
            solution_data: All computed solution information.

        Returns:
            Levels and write amplification string.
        """
        d = solution_data
        return f"levels={d['total_levels']}, write_amp={_f(d['write_amp'])}"


# ---------------------------------------------------------------------------
# 7. Gossip Protocol (tier 5)
# ---------------------------------------------------------------------------

@register
class GossipProtocolGenerator(StepGenerator):
    """Simulate push gossip protocol convergence.

    Each round, each informed node tells one random node. After k
    rounds, approximately N*(1 - e^(-2^k / N)) nodes are informed.
    Compute the expected informed count over several rounds.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "gossip_protocol"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["basic_prob"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task instruction string.
        """
        return "compute gossip protocol convergence over rounds"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a gossip protocol problem.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        n = self._rng.choice([10, 20, 50, 100])
        n_rounds = min(3 + difficulty, 8)

        steps = [f"N={n}, push gossip"]
        steps.append(f"informed(k) ~ N*(1 - e^(-2^k/N))")
        round_data = []

        for k in range(1, n_rounds + 1):
            exponent = -(2 ** k) / n
            informed = round(n * (1.0 - math.exp(exponent)), 4)
            informed = min(informed, n)
            fraction = round(informed / n, 4)
            round_data.append({"round": k, "informed": informed, "fraction": fraction})
            steps.append(f"k={k}: ~{_f(informed)} informed ({_f(fraction)})")

        full_round = 0
        for rd in round_data:
            if rd["fraction"] >= 0.99:
                full_round = rd["round"]
                break

        if full_round > 0:
            steps.append(f"99% coverage at round {full_round}")
        else:
            steps.append(f"99% not reached in {n_rounds} rounds")

        problem = f"gossip: N={n}, rounds={n_rounds}"
        return problem, {
            "steps": steps,
            "round_data": round_data,
            "full_round": full_round,
        }

    def _create_steps(self, solution_data: dict) -> list[str]:
        """Return the gossip convergence steps.

        Args:
            solution_data: All computed solution information.

        Returns:
            Step strings in execution order.
        """
        return solution_data["steps"]

    def _create_answer(self, solution_data: dict) -> str:
        """Return the convergence result.

        Args:
            solution_data: All computed solution information.

        Returns:
            Final informed count and 99% round.
        """
        d = solution_data
        last = d["round_data"][-1]
        if d["full_round"] > 0:
            return f"99% at round {d['full_round']}, final={_f(last['informed'])}/{d['round_data'][0]['informed']}"
        return f"final informed={_f(last['informed'])}, fraction={_f(last['fraction'])}"


# ---------------------------------------------------------------------------
# 8. Snapshot Algorithm (tier 5)
# ---------------------------------------------------------------------------

@register
class SnapshotAlgorithmGenerator(StepGenerator):
    """Trace the Chandy-Lamport snapshot algorithm.

    The initiator records its local state and sends markers on all
    outgoing channels. Followers record channel state between marker
    receipt. Template-based tracing of the protocol.
    """

    _TEMPLATES = [
        {
            "n_procs": 2,
            "initiator": "P0",
            "states": {"P0": 100, "P1": 50},
            "channels": {"P0->P1": [10, 20], "P1->P0": [5]},
        },
        {
            "n_procs": 3,
            "initiator": "P0",
            "states": {"P0": 200, "P1": 100, "P2": 75},
            "channels": {"P0->P1": [15], "P0->P2": [10], "P1->P0": [], "P1->P2": [25], "P2->P0": [5], "P2->P1": []},
        },
        {
            "n_procs": 2,
            "initiator": "P1",
            "states": {"P0": 80, "P1": 120},
            "channels": {"P0->P1": [30], "P1->P0": [15, 10]},
        },
        {
            "n_procs": 3,
            "initiator": "P1",
            "states": {"P0": 150, "P1": 90, "P2": 60},
            "channels": {"P0->P1": [20], "P0->P2": [], "P1->P0": [10], "P1->P2": [5], "P2->P0": [], "P2->P1": [15]},
        },
        {
            "n_procs": 2,
            "initiator": "P0",
            "states": {"P0": 50, "P1": 200},
            "channels": {"P0->P1": [], "P1->P0": [40, 20]},
        },
        {
            "n_procs": 3,
            "initiator": "P2",
            "states": {"P0": 100, "P1": 100, "P2": 100},
            "channels": {"P0->P1": [10], "P0->P2": [20], "P1->P0": [5], "P1->P2": [15], "P2->P0": [10], "P2->P1": [10]},
        },
        {
            "n_procs": 2,
            "initiator": "P0",
            "states": {"P0": 300, "P1": 0},
            "channels": {"P0->P1": [50, 25, 25], "P1->P0": []},
        },
        {
            "n_procs": 3,
            "initiator": "P0",
            "states": {"P0": 50, "P1": 50, "P2": 50},
            "channels": {"P0->P1": [10], "P0->P2": [10], "P1->P0": [10], "P1->P2": [10], "P2->P0": [10], "P2->P1": [10]},
        },
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "snapshot_algorithm"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["comparison"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task instruction string.
        """
        return "trace Chandy-Lamport snapshot algorithm"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a snapshot algorithm trace problem.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        idx = difficulty % len(self._TEMPLATES)
        tmpl = self._TEMPLATES[idx]

        initiator = tmpl["initiator"]
        states = tmpl["states"]
        channels = tmpl["channels"]
        procs = sorted(states.keys())

        steps = [f"initiator={initiator} records state={states[initiator]}"]

        for p in procs:
            if p != initiator:
                steps.append(f"{initiator} sends MARKER to {p}")

        recorded_channels: dict[str, list[int]] = {}
        for p in procs:
            if p != initiator:
                steps.append(f"{p} receives MARKER, records state={states[p]}")
                for q in procs:
                    if q != p:
                        ch_key = f"{q}->{p}"
                        ch_msgs = channels.get(ch_key, [])
                        recorded_channels[ch_key] = ch_msgs
                        if ch_msgs:
                            steps.append(f"channel {ch_key}: {ch_msgs}")
                        else:
                            steps.append(f"channel {ch_key}: empty")

        total_state = sum(states.values())
        total_in_transit = sum(sum(v) for v in recorded_channels.values())
        steps.append(f"global snapshot: states={total_state}, in_transit={total_in_transit}")

        state_str = ", ".join(f"{k}={v}" for k, v in states.items())
        problem = f"Chandy-Lamport: init={initiator}, states=[{state_str}]"
        return problem, {
            "steps": steps,
            "total_state": total_state,
            "total_in_transit": total_in_transit,
            "snapshot_total": total_state + total_in_transit,
        }

    def _create_steps(self, solution_data: dict) -> list[str]:
        """Return the snapshot algorithm steps.

        Args:
            solution_data: All computed solution information.

        Returns:
            Step strings in execution order.
        """
        return solution_data["steps"]

    def _create_answer(self, solution_data: dict) -> str:
        """Return the global snapshot summary.

        Args:
            solution_data: All computed solution information.

        Returns:
            Snapshot total string.
        """
        d = solution_data
        return (
            f"states={d['total_state']}, "
            f"in_transit={d['total_in_transit']}, "
            f"total={d['snapshot_total']}"
        )
