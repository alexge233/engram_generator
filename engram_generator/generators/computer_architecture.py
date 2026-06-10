"""Computer architecture task generators.

6 generators covering pipeline throughput, cache hit ratio, branch
prediction, instruction scheduling, memory hierarchy access time,
and Amdahl's law speedup computation.
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
# 1. Pipeline Throughput (tier 4)
# ===================================================================

@register
class PipelineThroughputGenerator(StepGenerator):
    """Compute pipeline throughput and total execution time.

    Given k pipeline stages each taking t ns and n instructions,
    throughput after fill = 1/t instructions per ns, latency = k*t ns,
    and total execution time = (k + n - 1) * t ns.

    Difficulty scaling:
        Difficulty 1-3: small k (3-5), small n (5-10), integer t.
        Difficulty 4-6: larger k (5-8), larger n (10-50), decimal t.
        Difficulty 7-8: compute optimal k given total time constraint.

    Prerequisites:
        multiplication.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "pipeline_throughput"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

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
        if difficulty >= 7:
            return "compute pipeline execution time and optimal throughput"
        return "compute pipeline throughput and total execution time"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate pipeline parameters and compute timing.

        Args:
            difficulty: Controls parameter ranges.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            k = self._rng.randint(3, 5)
            n = self._rng.randint(5, 10)
            t = float(self._rng.randint(1, 5))
        elif difficulty <= 6:
            k = self._rng.randint(5, 8)
            n = self._rng.randint(10, 50)
            t = round(self._rng.uniform(0.5, 5.0), 1)
        else:
            k = self._rng.randint(6, 10)
            n = self._rng.randint(20, 100)
            t = round(self._rng.uniform(0.5, 3.0), 1)

        latency = round(k * t, 4)
        throughput = round(1.0 / t, 4)
        total_time = round((k + n - 1) * t, 4)

        problem = (
            f"\\text{{Pipeline}}: k={k} \\text{{ stages}}, "
            f"t={_f(t)} \\text{{ ns}}, n={n} \\text{{ instr}}"
        )
        return problem, {
            "k": k, "n": n, "t": t,
            "latency": latency,
            "throughput": throughput,
            "total_time": total_time,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate pipeline computation steps.

        Args:
            data: Solution data with pipeline parameters.

        Returns:
            List of step strings.
        """
        return [
            f"k={data['k']}, t={_f(data['t'])} ns, n={data['n']}",
            f"latency = k*t = {data['k']}*{_f(data['t'])} = {_f(data['latency'])} ns",
            f"throughput = 1/t = 1/{_f(data['t'])} = {_f(data['throughput'])} instr/ns",
            (
                f"total = (k+n-1)*t = ({data['k']}+{data['n']}-1)*{_f(data['t'])} "
                f"= {_f(data['total_time'])} ns"
            ),
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the pipeline timing results.

        Args:
            data: Solution data.

        Returns:
            Total execution time and throughput.
        """
        return (
            f"total = {_f(data['total_time'])} ns, "
            f"throughput = {_f(data['throughput'])} instr/ns"
        )


# ===================================================================
# 2. Cache Hit Ratio (tier 4)
# ===================================================================

@register
class CacheHitRatioGenerator(StepGenerator):
    """Compute cache hit ratio and average memory access time.

    Given hits and misses, hit_ratio = hits / (hits + misses).
    AMAT = hit_time + miss_rate * miss_penalty.

    Difficulty scaling:
        Difficulty 1-3: simple integer hits/misses, compute ratio only.
        Difficulty 4-6: compute AMAT with given hit_time and miss_penalty.
        Difficulty 7-8: multi-level cache with L1 and L2 AMAT.

    Prerequisites:
        division.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "cache_hit_ratio"

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
        if difficulty >= 7:
            return "compute multi-level cache AMAT"
        if difficulty >= 4:
            return "compute cache hit ratio and AMAT"
        return "compute cache hit ratio"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate cache access parameters and compute metrics.

        Args:
            difficulty: Controls problem variant.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        hits = self._rng.randint(50, 500)
        misses = self._rng.randint(5, 100)
        total = hits + misses
        hit_ratio = round(hits / total, 4)
        miss_rate = round(1.0 - hit_ratio, 4)

        if difficulty <= 3:
            hit_time = 0.0
            miss_penalty = 0.0
            amat = 0.0
            mode = "ratio_only"
        elif difficulty <= 6:
            hit_time = float(self._rng.randint(1, 5))
            miss_penalty = float(self._rng.randint(20, 100))
            amat = round(hit_time + miss_rate * miss_penalty, 4)
            mode = "amat"
        else:
            hit_time = float(self._rng.randint(1, 3))
            miss_penalty = float(self._rng.randint(10, 30))
            l2_miss_rate = round(self._rng.uniform(0.05, 0.3), 2)
            l2_miss_penalty = float(self._rng.randint(50, 200))
            l2_amat = round(miss_penalty + l2_miss_rate * l2_miss_penalty, 4)
            amat = round(hit_time + miss_rate * l2_amat, 4)
            mode = "multi_level"

        problem = f"\\text{{Cache}}: hits={hits}, misses={misses}"
        if mode == "amat":
            problem += f", t_{{hit}}={_f(hit_time)} ns, t_{{miss}}={_f(miss_penalty)} ns"
        elif mode == "multi_level":
            problem += (
                f", t_{{L1}}={_f(hit_time)} ns, "
                f"t_{{L2}}={_f(miss_penalty)} ns, "
                f"L2\\_miss={l2_miss_rate}, "
                f"t_{{DRAM}}={_f(l2_miss_penalty)} ns"
            )

        data = {
            "hits": hits, "misses": misses, "total": total,
            "hit_ratio": hit_ratio, "miss_rate": miss_rate,
            "hit_time": hit_time, "miss_penalty": miss_penalty,
            "amat": amat, "mode": mode,
        }
        if mode == "multi_level":
            data["l2_miss_rate"] = l2_miss_rate
            data["l2_miss_penalty"] = l2_miss_penalty
            data["l2_amat"] = l2_amat

        return problem, data

    def _create_steps(self, data: dict) -> list[str]:
        """Generate cache metric computation steps.

        Args:
            data: Solution data with cache parameters.

        Returns:
            List of step strings.
        """
        steps = [
            f"total = {data['hits']}+{data['misses']} = {data['total']}",
            f"hit_ratio = {data['hits']}/{data['total']} = {_f(data['hit_ratio'])}",
            f"miss_rate = 1-{_f(data['hit_ratio'])} = {_f(data['miss_rate'])}",
        ]
        if data["mode"] == "amat":
            steps.append(
                f"AMAT = {_f(data['hit_time'])}+{_f(data['miss_rate'])}*"
                f"{_f(data['miss_penalty'])} = {_f(data['amat'])} ns"
            )
        elif data["mode"] == "multi_level":
            steps.append(
                f"L2_AMAT = {_f(data['miss_penalty'])}+"
                f"{data['l2_miss_rate']}*{_f(data['l2_miss_penalty'])} "
                f"= {_f(data['l2_amat'])} ns"
            )
            steps.append(
                f"AMAT = {_f(data['hit_time'])}+{_f(data['miss_rate'])}*"
                f"{_f(data['l2_amat'])} = {_f(data['amat'])} ns"
            )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the cache metrics.

        Args:
            data: Solution data.

        Returns:
            Hit ratio and optionally AMAT.
        """
        if data["mode"] == "ratio_only":
            return f"hit_ratio = {_f(data['hit_ratio'])}"
        return (
            f"hit_ratio = {_f(data['hit_ratio'])}, "
            f"AMAT = {_f(data['amat'])} ns"
        )


# ===================================================================
# 3. Branch Prediction (tier 5)
# ===================================================================

@register
class BranchPredictionGenerator(StepGenerator):
    """Simulate a 2-bit saturating branch predictor.

    States: strongly taken (ST=3), weakly taken (WT=2), weakly not
    taken (WN=1), strongly not taken (SN=0). Given a branch history
    (sequence of T/N), simulate state transitions and count
    mispredictions.

    Difficulty scaling:
        Difficulty 1-3: 4-6 branches, start at ST.
        Difficulty 4-6: 6-8 branches, random start state.
        Difficulty 7-8: 8-10 branches, compute accuracy percentage.

    Prerequisites:
        comparison.
    """

    _STATE_NAMES = {0: "SN", 1: "WN", 2: "WT", 3: "ST"}

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "branch_prediction"

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
        return "simulate 2-bit branch predictor and count mispredictions"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate branch history and simulate predictor.

        Args:
            difficulty: Controls history length and start state.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            length = self._rng.randint(4, 6)
            state = 3
        elif difficulty <= 6:
            length = self._rng.randint(6, 8)
            state = self._rng.randint(0, 3)
        else:
            length = self._rng.randint(8, 10)
            state = self._rng.randint(0, 3)

        history = [self._rng.choice(["T", "N"]) for _ in range(length)]
        transitions = []
        mispredictions = 0

        current = state
        for outcome in history:
            predicted_taken = current >= 2
            actual_taken = outcome == "T"
            correct = predicted_taken == actual_taken
            if not correct:
                mispredictions += 1

            if actual_taken:
                new_state = min(current + 1, 3)
            else:
                new_state = max(current - 1, 0)

            transitions.append({
                "outcome": outcome,
                "state_before": current,
                "predicted": "T" if predicted_taken else "N",
                "correct": correct,
                "state_after": new_state,
            })
            current = new_state

        accuracy = round((length - mispredictions) / length, 4)
        hist_str = ",".join(history)
        problem = (
            f"\\text{{2-bit predictor}}: "
            f"start={self._STATE_NAMES[state]}, "
            f"history=[{hist_str}]"
        )
        return problem, {
            "history": history,
            "start_state": state,
            "transitions": transitions,
            "mispredictions": mispredictions,
            "accuracy": accuracy,
            "length": length,
            "show_accuracy": difficulty >= 7,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate branch prediction simulation steps.

        Args:
            data: Solution data with transition history.

        Returns:
            List of step strings.
        """
        steps = [f"initial state = {self._STATE_NAMES[data['start_state']]}"]
        for t in data["transitions"]:
            mark = "ok" if t["correct"] else "MISS"
            steps.append(
                f"{self._STATE_NAMES[t['state_before']]}->pred={t['predicted']}, "
                f"actual={t['outcome']}, [{mark}]->"
                f"{self._STATE_NAMES[t['state_after']]}"
            )
        steps.append(f"mispredictions = {data['mispredictions']}/{data['length']}")
        if data["show_accuracy"]:
            steps.append(f"accuracy = {_f(data['accuracy'])}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the misprediction count.

        Args:
            data: Solution data.

        Returns:
            Misprediction count and optionally accuracy.
        """
        ans = f"mispredictions = {data['mispredictions']}"
        if data["show_accuracy"]:
            ans += f", accuracy = {_f(data['accuracy'])}"
        return ans


# ===================================================================
# 4. Instruction Scheduling (tier 5)
# ===================================================================

@register
class InstructionSchedulingGenerator(StepGenerator):
    """Compute instruction start times considering RAW data hazards.

    Given instructions with latencies and dependencies, compute the
    earliest start time for each instruction. Find total cycles with
    and without reordering.

    Difficulty scaling:
        Difficulty 1-3: 3 instructions, simple chain dependency.
        Difficulty 4-6: 4 instructions, branching dependencies.
        Difficulty 7-8: 5 instructions, multiple dependency paths.

    Prerequisites:
        addition.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "instruction_scheduling"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["addition"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute instruction earliest start times with RAW hazards"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate instructions with latencies and dependencies.

        Args:
            difficulty: Controls number of instructions.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            n = 3
        elif difficulty <= 6:
            n = 4
        else:
            n = 5

        latencies = [self._rng.randint(1, 4) for _ in range(n)]
        deps = self._build_dependencies(n, difficulty)
        start_times = self._compute_start_times(n, latencies, deps)
        total_cycles = max(
            start_times[i] + latencies[i] for i in range(n)
        )
        serial_cycles = sum(latencies)

        instr_strs = []
        for i in range(n):
            dep_str = ",".join(f"I{d}" for d in deps[i]) if deps[i] else "none"
            instr_strs.append(f"I{i}(lat={latencies[i]},deps=[{dep_str}])")
        problem = f"\\text{{Schedule}}: {'; '.join(instr_strs)}"

        return problem, {
            "n": n, "latencies": latencies, "deps": deps,
            "start_times": start_times, "total_cycles": total_cycles,
            "serial_cycles": serial_cycles,
        }

    def _build_dependencies(self, n: int, difficulty: int) -> list[list[int]]:
        """Build dependency lists for instructions.

        Args:
            n: Number of instructions.
            difficulty: Controls dependency complexity.

        Returns:
            List of dependency lists per instruction.
        """
        deps: list[list[int]] = [[] for _ in range(n)]
        if difficulty <= 3:
            for i in range(1, n):
                deps[i] = [i - 1]
        elif difficulty <= 6:
            for i in range(1, n):
                dep_count = min(i, self._rng.randint(1, 2))
                possible = list(range(i))
                self._rng.shuffle(possible)
                deps[i] = sorted(possible[:dep_count])
        else:
            for i in range(1, n):
                dep_count = min(i, self._rng.randint(1, 3))
                possible = list(range(i))
                self._rng.shuffle(possible)
                deps[i] = sorted(possible[:dep_count])
        return deps

    def _compute_start_times(self, n: int, latencies: list[int],
                             deps: list[list[int]]) -> list[int]:
        """Compute earliest start time for each instruction.

        Args:
            n: Number of instructions.
            latencies: Cycle count for each instruction.
            deps: Dependencies per instruction.

        Returns:
            List of earliest start times.
        """
        start_times = [0] * n
        for i in range(n):
            if deps[i]:
                start_times[i] = max(
                    start_times[d] + latencies[d] for d in deps[i]
                )
        return start_times

    def _create_steps(self, data: dict) -> list[str]:
        """Generate instruction scheduling steps.

        Args:
            data: Solution data with instructions and timings.

        Returns:
            List of step strings.
        """
        steps = []
        for i in range(data["n"]):
            if not data["deps"][i]:
                steps.append(f"I{i}: start=0, end={data['latencies'][i]}")
            else:
                dep_str = ", ".join(
                    f"I{d} ends@{data['start_times'][d]+data['latencies'][d]}"
                    for d in data["deps"][i]
                )
                steps.append(
                    f"I{i}: wait({dep_str}), "
                    f"start={data['start_times'][i]}, "
                    f"end={data['start_times'][i]+data['latencies'][i]}"
                )
        steps.append(f"total(parallel) = {data['total_cycles']} cycles")
        steps.append(f"total(serial) = {data['serial_cycles']} cycles")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the total execution cycles.

        Args:
            data: Solution data.

        Returns:
            Parallel and serial cycle counts.
        """
        return (
            f"parallel = {data['total_cycles']} cycles, "
            f"serial = {data['serial_cycles']} cycles"
        )


# ===================================================================
# 5. Memory Hierarchy (tier 4)
# ===================================================================

@register
class MemoryHierarchyGenerator(StepGenerator):
    """Compute effective memory access time from a hierarchy.

    Given L1 (1ns, 32KB), L2 (10ns, 256KB), L3 (30ns, 8MB),
    DRAM (100ns). Working set size determines which level is accessed.
    Effective time is computed from hit rates at each level.

    Difficulty scaling:
        Difficulty 1-3: single working set, direct level lookup.
        Difficulty 4-6: compute with given hit rates per level.
        Difficulty 7-8: mixed workload with two access patterns.

    Prerequisites:
        multiplication.
    """

    _LEVELS = [
        {"name": "L1", "time": 1, "size": 32 * 1024},
        {"name": "L2", "time": 10, "size": 256 * 1024},
        {"name": "L3", "time": 30, "size": 8 * 1024 * 1024},
        {"name": "DRAM", "time": 100, "size": float("inf")},
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "memory_hierarchy"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

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
        if difficulty >= 7:
            return "compute effective access time for mixed workload"
        return "compute effective memory access time"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate memory access pattern and compute effective time.

        Args:
            difficulty: Controls problem variant.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            ws_kb = self._rng.choice([16, 64, 128, 512, 4096, 16384])
            ws_bytes = ws_kb * 1024
            level_idx = 0
            for i, lvl in enumerate(self._LEVELS):
                if ws_bytes <= lvl["size"]:
                    level_idx = i
                    break
            access_time = self._LEVELS[level_idx]["time"]
            problem = (
                f"\\text{{Memory hierarchy}}: "
                f"working\\_set={ws_kb}KB"
            )
            return problem, {
                "mode": "simple",
                "ws_kb": ws_kb,
                "level": self._LEVELS[level_idx]["name"],
                "access_time": access_time,
            }

        l1_rate = round(self._rng.uniform(0.85, 0.98), 2)
        l2_rate = round(self._rng.uniform(0.7, 0.95), 2)
        l3_rate = round(self._rng.uniform(0.6, 0.9), 2)

        l1_miss = round(1.0 - l1_rate, 4)
        l2_miss = round(1.0 - l2_rate, 4)
        l3_miss = round(1.0 - l3_rate, 4)

        effective = round(
            1.0 * l1_rate
            + 10.0 * l1_miss * l2_rate
            + 30.0 * l1_miss * l2_miss * l3_rate
            + 100.0 * l1_miss * l2_miss * l3_miss,
            4,
        )

        problem = (
            f"\\text{{Mem hierarchy}}: "
            f"L1(1ns,h={l1_rate}), "
            f"L2(10ns,h={l2_rate}), "
            f"L3(30ns,h={l3_rate}), "
            f"DRAM(100ns)"
        )

        data = {
            "mode": "hit_rates",
            "l1_rate": l1_rate, "l2_rate": l2_rate, "l3_rate": l3_rate,
            "l1_miss": l1_miss, "l2_miss": l2_miss, "l3_miss": l3_miss,
            "effective": effective,
        }

        if difficulty >= 7:
            frac_a = round(self._rng.uniform(0.3, 0.7), 2)
            frac_b = round(1.0 - frac_a, 2)
            time_b = float(self._rng.randint(1, 10))
            mixed = round(frac_a * effective + frac_b * time_b, 4)
            data["frac_a"] = frac_a
            data["frac_b"] = frac_b
            data["time_b"] = time_b
            data["mixed"] = mixed
            data["mode"] = "mixed"

        return problem, data

    def _create_steps(self, data: dict) -> list[str]:
        """Generate memory hierarchy computation steps.

        Args:
            data: Solution data with hierarchy parameters.

        Returns:
            List of step strings.
        """
        if data["mode"] == "simple":
            return [
                f"working set = {data['ws_kb']}KB",
                f"fits in {data['level']}",
                f"access time = {data['access_time']} ns",
            ]

        t_l1 = round(1.0 * data["l1_rate"], 4)
        t_l2 = round(10.0 * data["l1_miss"] * data["l2_rate"], 4)
        t_l3 = round(30.0 * data["l1_miss"] * data["l2_miss"] * data["l3_rate"], 4)
        t_dram = round(100.0 * data["l1_miss"] * data["l2_miss"] * data["l3_miss"], 4)

        steps = [
            f"L1 contrib = 1*{data['l1_rate']} = {_f(t_l1)} ns",
            f"L2 contrib = 10*{_f(data['l1_miss'])}*{data['l2_rate']} = {_f(t_l2)} ns",
            f"L3 contrib = 30*{_f(data['l1_miss'])}*{_f(data['l2_miss'])}*{data['l3_rate']} = {_f(t_l3)} ns",
            f"DRAM contrib = 100*{_f(data['l1_miss'])}*{_f(data['l2_miss'])}*{_f(data['l3_miss'])} = {_f(t_dram)} ns",
            f"effective = {_f(t_l1)}+{_f(t_l2)}+{_f(t_l3)}+{_f(t_dram)} = {_f(data['effective'])} ns",
        ]

        if data["mode"] == "mixed":
            steps.append(
                f"mixed = {data['frac_a']}*{_f(data['effective'])}+"
                f"{data['frac_b']}*{_f(data['time_b'])} = {_f(data['mixed'])} ns"
            )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the effective access time.

        Args:
            data: Solution data.

        Returns:
            Effective access time in ns.
        """
        if data["mode"] == "simple":
            return f"{data['level']}: {data['access_time']} ns"
        if data["mode"] == "mixed":
            return f"effective = {_f(data['mixed'])} ns"
        return f"effective = {_f(data['effective'])} ns"


# ===================================================================
# 6. Amdahl's Speedup (tier 4)
# ===================================================================

@register
class AmdahlSpeedupGenerator(StepGenerator):
    """Compute Amdahl's law speedup: S = 1 / ((1-f) + f/p).

    Given the fraction parallelisable f and number of processors p,
    compute the speedup. Also compute max speedup = 1/(1-f).

    Difficulty scaling:
        Difficulty 1-3: simple f (0.5, 0.75), small p (2, 4).
        Difficulty 4-6: varied f and p, compute max speedup.
        Difficulty 7-8: given target speedup, find required p.

    Prerequisites:
        division.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "amdahl_speedup"

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
        if difficulty >= 7:
            return "compute Amdahl's speedup and required processors"
        return "compute Amdahl's law speedup"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate parallelisation parameters and compute speedup.

        Args:
            difficulty: Controls parameter ranges.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            f = self._rng.choice([0.5, 0.75, 0.9])
            p = self._rng.choice([2, 4, 8])
        elif difficulty <= 6:
            f = round(self._rng.uniform(0.5, 0.99), 2)
            p = self._rng.choice([2, 4, 8, 16, 32])
        else:
            f = round(self._rng.uniform(0.7, 0.99), 2)
            p = self._rng.choice([4, 8, 16, 32, 64])

        serial_frac = round(1.0 - f, 4)
        speedup = round(1.0 / (serial_frac + f / p), 4)
        max_speedup = round(1.0 / serial_frac, 4) if serial_frac > 0 else float("inf")

        problem = f"S = 1/((1-f)+f/p), f={f}, p={p}"
        return problem, {
            "f": f, "p": p,
            "serial_frac": serial_frac,
            "speedup": speedup,
            "max_speedup": max_speedup,
            "show_max": difficulty >= 4,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Amdahl's law computation steps.

        Args:
            data: Solution data with parallelisation parameters.

        Returns:
            List of step strings.
        """
        f_over_p = round(data["f"] / data["p"], 4)
        denom = round(data["serial_frac"] + f_over_p, 4)
        steps = [
            f"f = {data['f']}, p = {data['p']}",
            f"1-f = {_f(data['serial_frac'])}",
            f"f/p = {data['f']}/{data['p']} = {_f(f_over_p)}",
            f"denom = {_f(data['serial_frac'])}+{_f(f_over_p)} = {_f(denom)}",
            f"S = 1/{_f(denom)} = {_f(data['speedup'])}",
        ]
        if data["show_max"]:
            steps.append(
                f"max S = 1/(1-{data['f']}) = {_f(data['max_speedup'])}"
            )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the speedup value.

        Args:
            data: Solution data.

        Returns:
            Speedup and optionally max speedup.
        """
        ans = f"S = {_f(data['speedup'])}"
        if data["show_max"]:
            ans += f", max S = {_f(data['max_speedup'])}"
        return ans
