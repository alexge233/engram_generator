"""Deep operating systems generators.

8 generators across tiers 4-5 covering preemptive SJF scheduling,
memory allocation strategies, page table lookup, disk scheduling,
deadlock detection, semaphore tracing, virtual memory replacement,
and file allocation methods.
"""
from __future__ import annotations

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
# 1. Preemptive SJF Scheduling (tier 4)
# ---------------------------------------------------------------------------

@register
class ProcessSchedulingSjfGenerator(StepGenerator):
    """Simulate preemptive Shortest Job First (SRTF) scheduling.

    When a new process arrives with a shorter remaining burst than
    the running process, preempt. Show Gantt chart segments and
    compute average waiting time.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "process_scheduling_sjf"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["sorting"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task instruction string.
        """
        return "simulate preemptive SJF scheduling and compute avg wait"

    def _make_processes(self, difficulty: int) -> list[dict]:
        """Generate process list with arrival and burst times.

        Args:
            difficulty: Controls number and burst range.

        Returns:
            List of process dicts with pid, arrival, burst.
        """
        n = min(3 + difficulty // 2, 5)
        procs = []
        for i in range(n):
            arrival = self._rng.randint(0, min(difficulty, 5))
            burst = self._rng.randint(1, min(3 + difficulty, 8))
            procs.append({"pid": f"P{i}", "arrival": arrival, "burst": burst})
        return procs

    def _simulate(self, procs: list[dict]) -> tuple[list[str], float]:
        """Run preemptive SJF (SRTF) simulation.

        Args:
            procs: Process list with arrival and burst.

        Returns:
            Tuple of (gantt_steps, avg_wait_time).
        """
        remaining = {p["pid"]: p["burst"] for p in procs}
        arrival_map = {p["pid"]: p["arrival"] for p in procs}
        burst_map = {p["pid"]: p["burst"] for p in procs}
        finish_time: dict[str, int] = {}
        steps = []
        time = 0
        max_time = sum(p["burst"] for p in procs) + max(p["arrival"] for p in procs) + 1

        while any(r > 0 for r in remaining.values()) and time < max_time:
            available = [
                pid for pid, rem in remaining.items()
                if rem > 0 and arrival_map[pid] <= time
            ]
            if not available:
                time += 1
                continue
            available.sort(key=lambda pid: (remaining[pid], pid))
            running = available[0]
            start = time
            while time < max_time and remaining[running] > 0:
                time += 1
                remaining[running] -= 1
                new_arrivals = [
                    pid for pid, rem in remaining.items()
                    if rem > 0 and arrival_map[pid] <= time
                    and pid != running and rem < remaining[running]
                ]
                if new_arrivals and remaining[running] > 0:
                    break
            steps.append(f"[{start}-{time}] {running}")
            if remaining[running] == 0:
                finish_time[running] = time

        total_wait = 0
        for p in procs:
            ft = finish_time.get(p["pid"], time)
            turnaround = ft - p["arrival"]
            wait = turnaround - p["burst"]
            total_wait += max(0, wait)
        avg_wait = round(total_wait / len(procs), 4)
        return steps, avg_wait

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a preemptive SJF scheduling problem.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        procs = self._make_processes(difficulty)
        steps, avg_wait = self._simulate(procs)
        proc_str = ", ".join(
            f"{p['pid']}(arr={p['arrival']},burst={p['burst']})" for p in procs
        )
        problem = f"SRTF: {proc_str}"
        return problem, {"steps": steps, "avg_wait": avg_wait}

    def _create_steps(self, solution_data: dict) -> list[str]:
        """Return the Gantt chart steps.

        Args:
            solution_data: All computed solution information.

        Returns:
            Step strings in execution order.
        """
        return solution_data["steps"]

    def _create_answer(self, solution_data: dict) -> str:
        """Return the average waiting time.

        Args:
            solution_data: All computed solution information.

        Returns:
            Average wait time string.
        """
        return f"avg_wait={_f(solution_data['avg_wait'])}"


# ---------------------------------------------------------------------------
# 2. Memory Allocation (tier 4)
# ---------------------------------------------------------------------------

@register
class MemoryAllocationGenerator(StepGenerator):
    """Simulate first-fit, best-fit, and worst-fit memory allocation.

    Given a list of free memory blocks and process sizes, allocate
    each process using the chosen strategy and show the result.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "memory_allocation"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["sorting"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task instruction string.
        """
        return "allocate processes to memory blocks using fit strategy"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a memory allocation problem.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        n_blocks = min(3 + difficulty // 2, 6)
        n_procs = min(2 + difficulty // 2, 4)
        blocks = [self._rng.randint(50, 300) for _ in range(n_blocks)]
        proc_sizes = [self._rng.randint(30, 200) for _ in range(n_procs)]
        strategy = self._rng.choice(["first-fit", "best-fit", "worst-fit"])

        avail = list(blocks)
        allocations = []
        steps = [f"blocks={blocks}", f"strategy={strategy}"]

        for i, size in enumerate(proc_sizes):
            candidates = [(j, avail[j]) for j in range(len(avail)) if avail[j] >= size]
            if not candidates:
                allocations.append({"proc": f"P{i}", "size": size, "block": -1})
                steps.append(f"P{i}(size={size}): no fit")
                continue

            if strategy == "first-fit":
                chosen_j, chosen_sz = candidates[0]
            elif strategy == "best-fit":
                candidates.sort(key=lambda x: x[1])
                chosen_j, chosen_sz = candidates[0]
            else:
                candidates.sort(key=lambda x: -x[1])
                chosen_j, chosen_sz = candidates[0]

            avail[chosen_j] -= size
            allocations.append({"proc": f"P{i}", "size": size, "block": chosen_j})
            steps.append(
                f"P{i}(size={size}): block {chosen_j}({chosen_sz}), "
                f"remain={avail[chosen_j]}"
            )

        problem = f"{strategy}: blocks={blocks}, procs={proc_sizes}"
        return problem, {
            "steps": steps,
            "allocations": allocations,
            "remaining": avail,
        }

    def _create_steps(self, solution_data: dict) -> list[str]:
        """Return the allocation steps.

        Args:
            solution_data: All computed solution information.

        Returns:
            Step strings in execution order.
        """
        return solution_data["steps"]

    def _create_answer(self, solution_data: dict) -> str:
        """Return the allocation result.

        Args:
            solution_data: All computed solution information.

        Returns:
            Allocation summary string.
        """
        parts = []
        for a in solution_data["allocations"]:
            if a["block"] >= 0:
                parts.append(f"{a['proc']}->blk{a['block']}")
            else:
                parts.append(f"{a['proc']}->FAIL")
        return ", ".join(parts)


# ---------------------------------------------------------------------------
# 3. Page Table Lookup (tier 4)
# ---------------------------------------------------------------------------

@register
class PageTableLookupGenerator(StepGenerator):
    """Translate a virtual address to physical using a page table.

    Given a virtual address, page size, and page table mapping,
    extract the page number and offset, look up the frame number,
    and compute the physical address.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "page_table_lookup"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["binary_arithmetic"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task instruction string.
        """
        return "translate virtual address to physical via page table"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a page table lookup problem.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        page_bits = self._rng.choice([8, 10, 12]) if difficulty >= 4 else 8
        page_size = 1 << page_bits
        n_pages = min(4 + difficulty, 8)
        page_table = {i: self._rng.randint(0, 15) for i in range(n_pages)}
        page_num = self._rng.randint(0, n_pages - 1)
        offset = self._rng.randint(0, page_size - 1)
        virtual_addr = page_num * page_size + offset
        frame = page_table[page_num]
        physical_addr = frame * page_size + offset

        steps = [
            f"virtual addr={virtual_addr}, page_size={page_size}",
            f"page_num = {virtual_addr} / {page_size} = {page_num}",
            f"offset = {virtual_addr} % {page_size} = {offset}",
            f"page_table[{page_num}] = frame {frame}",
            f"physical = {frame} * {page_size} + {offset} = {physical_addr}",
        ]

        pt_str = ", ".join(f"{k}:{v}" for k, v in page_table.items())
        problem = (
            f"VA={virtual_addr}, page_size={page_size}, "
            f"PT=[{pt_str}]"
        )
        return problem, {
            "steps": steps,
            "physical_addr": physical_addr,
            "page_num": page_num,
            "frame": frame,
            "offset": offset,
        }

    def _create_steps(self, solution_data: dict) -> list[str]:
        """Return the translation steps.

        Args:
            solution_data: All computed solution information.

        Returns:
            Step strings in execution order.
        """
        return solution_data["steps"]

    def _create_answer(self, solution_data: dict) -> str:
        """Return the physical address.

        Args:
            solution_data: All computed solution information.

        Returns:
            Physical address string.
        """
        return f"physical_addr={solution_data['physical_addr']}"


# ---------------------------------------------------------------------------
# 4. Disk Scheduling (tier 4)
# ---------------------------------------------------------------------------

@register
class DiskSchedulingGenerator(StepGenerator):
    """Simulate FCFS, SSTF, or SCAN disk scheduling.

    Given the current head position and a request queue of cylinder
    numbers, compute the seek sequence and total seek distance.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "disk_scheduling"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["sorting"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task instruction string.
        """
        return "compute disk seek sequence and total distance"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a disk scheduling problem.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        max_cyl = 200
        n_requests = min(4 + difficulty, 8)
        head = self._rng.randint(20, 180)
        requests = [self._rng.randint(0, max_cyl) for _ in range(n_requests)]
        algo = self._rng.choice(["FCFS", "SSTF", "SCAN"])

        if algo == "FCFS":
            order = list(requests)
        elif algo == "SSTF":
            order = []
            remaining = list(requests)
            cur = head
            while remaining:
                closest = min(remaining, key=lambda r: abs(r - cur))
                order.append(closest)
                remaining.remove(closest)
                cur = closest
        else:
            direction = self._rng.choice(["up", "down"])
            above = sorted([r for r in requests if r >= head])
            below = sorted([r for r in requests if r < head], reverse=True)
            if direction == "up":
                order = above + below
            else:
                order = below + above

        steps = [f"head={head}, algo={algo}"]
        total_seek = 0
        cur = head
        for cyl in order:
            dist = abs(cyl - cur)
            total_seek += dist
            steps.append(f"seek {cur}->{cyl}, dist={dist}")
            cur = cyl
        steps.append(f"total_seek={total_seek}")

        req_str = ",".join(str(r) for r in requests)
        problem = f"{algo}: head={head}, requests=[{req_str}]"
        return problem, {
            "steps": steps,
            "total_seek": total_seek,
            "order": order,
        }

    def _create_steps(self, solution_data: dict) -> list[str]:
        """Return the seek sequence steps.

        Args:
            solution_data: All computed solution information.

        Returns:
            Step strings in execution order.
        """
        return solution_data["steps"]

    def _create_answer(self, solution_data: dict) -> str:
        """Return the total seek distance.

        Args:
            solution_data: All computed solution information.

        Returns:
            Total seek distance string.
        """
        return f"total_seek={solution_data['total_seek']}"


# ---------------------------------------------------------------------------
# 5. Deadlock Detection (tier 5)
# ---------------------------------------------------------------------------

@register
class DeadlockDetectionGenerator(StepGenerator):
    """Detect deadlock using the banker's algorithm safety check.

    Given allocation, maximum, and available resource matrices,
    determine whether the system is in a safe state and find a
    safe sequence if one exists.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "deadlock_detection"

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
        return "run banker's algorithm to detect deadlock"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a deadlock detection problem.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        n_proc = min(3 + difficulty // 2, 5)
        n_res = 2 if difficulty <= 4 else 3
        total = [self._rng.randint(5, 10) for _ in range(n_res)]
        alloc = []
        max_need = []
        for _ in range(n_proc):
            a = [self._rng.randint(0, total[j] // n_proc) for j in range(n_res)]
            m = [a[j] + self._rng.randint(0, total[j] // 2) for j in range(n_res)]
            alloc.append(a)
            max_need.append(m)

        avail = [
            total[j] - sum(alloc[i][j] for i in range(n_proc))
            for j in range(n_res)
        ]
        avail = [max(0, v) for v in avail]

        need = [
            [max_need[i][j] - alloc[i][j] for j in range(n_res)]
            for i in range(n_proc)
        ]

        work = list(avail)
        finish = [False] * n_proc
        safe_seq = []
        steps = [f"avail={avail}"]

        changed = True
        while changed:
            changed = False
            for i in range(n_proc):
                if not finish[i] and all(need[i][j] <= work[j] for j in range(n_res)):
                    for j in range(n_res):
                        work[j] += alloc[i][j]
                    finish[i] = True
                    safe_seq.append(f"P{i}")
                    steps.append(f"P{i} can finish, work={list(work)}")
                    changed = True

        is_safe = all(finish)
        if is_safe:
            steps.append(f"safe sequence: {safe_seq}")
        else:
            deadlocked = [f"P{i}" for i in range(n_proc) if not finish[i]]
            steps.append(f"DEADLOCK: {deadlocked} cannot finish")

        alloc_str = "; ".join(f"P{i}={alloc[i]}" for i in range(n_proc))
        need_str = "; ".join(f"P{i}={need[i]}" for i in range(n_proc))
        problem = f"alloc=[{alloc_str}], need=[{need_str}], avail={avail}"
        return problem, {
            "steps": steps,
            "is_safe": is_safe,
            "safe_seq": safe_seq,
        }

    def _create_steps(self, solution_data: dict) -> list[str]:
        """Return the banker's algorithm steps.

        Args:
            solution_data: All computed solution information.

        Returns:
            Step strings in execution order.
        """
        return solution_data["steps"]

    def _create_answer(self, solution_data: dict) -> str:
        """Return the safety verdict.

        Args:
            solution_data: All computed solution information.

        Returns:
            SAFE or DEADLOCK string.
        """
        if solution_data["is_safe"]:
            return f"SAFE: {solution_data['safe_seq']}"
        return "DEADLOCK"


# ---------------------------------------------------------------------------
# 6. Semaphore Trace (tier 5)
# ---------------------------------------------------------------------------

@register
class SemaphoreTraceGenerator(StepGenerator):
    """Trace P (wait) and V (signal) operations on a semaphore.

    Given a sequence of P and V operations from multiple processes,
    track the semaphore value and process states (running, waiting,
    ready).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "semaphore_trace"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["queue_operations"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task instruction string.
        """
        return "trace semaphore P/V operations and process states"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a semaphore trace problem.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        n_procs = min(2 + difficulty // 2, 4)
        init_val = self._rng.randint(1, 2)
        n_ops = min(4 + difficulty, 8)

        ops = []
        for _ in range(n_ops):
            proc = f"P{self._rng.randint(0, n_procs - 1)}"
            op_type = self._rng.choice(["P", "V"])
            ops.append({"proc": proc, "op": op_type})

        sem = init_val
        wait_queue: list[str] = []
        steps = [f"sem init={init_val}"]

        for entry in ops:
            proc = entry["proc"]
            op = entry["op"]
            if op == "P":
                sem -= 1
                if sem < 0:
                    wait_queue.append(proc)
                    steps.append(
                        f"{proc} P(sem): sem={sem}, {proc} BLOCKED, "
                        f"queue={wait_queue}"
                    )
                else:
                    steps.append(f"{proc} P(sem): sem={sem}, {proc} runs")
            else:
                sem += 1
                if wait_queue:
                    woken = wait_queue.pop(0)
                    steps.append(
                        f"{proc} V(sem): sem={sem}, wake {woken}, "
                        f"queue={wait_queue}"
                    )
                else:
                    steps.append(f"{proc} V(sem): sem={sem}")

        ops_str = ", ".join(f"{o['proc']}.{o['op']}" for o in ops)
        problem = f"sem(init={init_val}): ops=[{ops_str}]"
        return problem, {
            "steps": steps,
            "final_sem": sem,
            "blocked": list(wait_queue),
        }

    def _create_steps(self, solution_data: dict) -> list[str]:
        """Return the semaphore trace steps.

        Args:
            solution_data: All computed solution information.

        Returns:
            Step strings in execution order.
        """
        return solution_data["steps"]

    def _create_answer(self, solution_data: dict) -> str:
        """Return the final semaphore state.

        Args:
            solution_data: All computed solution information.

        Returns:
            Final semaphore value and blocked processes.
        """
        d = solution_data
        if d["blocked"]:
            return f"sem={d['final_sem']}, blocked={d['blocked']}"
        return f"sem={d['final_sem']}, none blocked"


# ---------------------------------------------------------------------------
# 7. Virtual Memory Replacement - Optimal / LRU (tier 4)
# ---------------------------------------------------------------------------

@register
class VirtualMemoryReplacementGenerator(StepGenerator):
    """Compare Optimal (Belady) and LRU page replacement.

    Given a page reference string and frame count, simulate both
    Optimal (evict page used farthest in future) and LRU, then
    compare fault counts.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "virtual_memory_replacement"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

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
        return "compare Optimal and LRU page replacement"

    def _optimal(self, refs: list[int], frames: int) -> tuple[list[str], int]:
        """Simulate Optimal (Belady) replacement.

        Args:
            refs: Page reference string.
            frames: Number of frames.

        Returns:
            Tuple of (steps, fault_count).
        """
        buf: list[int] = []
        faults = 0
        steps = []
        for idx, page in enumerate(refs):
            if page in buf:
                steps.append(f"ref {page}: hit {list(buf)}")
            else:
                faults += 1
                if len(buf) >= frames:
                    farthest = -1
                    victim = buf[0]
                    for b in buf:
                        try:
                            next_use = refs[idx + 1:].index(b)
                        except ValueError:
                            next_use = len(refs)
                        if next_use > farthest:
                            farthest = next_use
                            victim = b
                    buf.remove(victim)
                    buf.append(page)
                    steps.append(
                        f"ref {page}: FAULT evict {victim} {list(buf)}"
                    )
                else:
                    buf.append(page)
                    steps.append(f"ref {page}: FAULT load {list(buf)}")
        return steps, faults

    def _lru(self, refs: list[int], frames: int) -> tuple[list[str], int]:
        """Simulate LRU replacement.

        Args:
            refs: Page reference string.
            frames: Number of frames.

        Returns:
            Tuple of (steps, fault_count).
        """
        buf: list[int] = []
        faults = 0
        steps = []
        for page in refs:
            if page in buf:
                buf.remove(page)
                buf.append(page)
                steps.append(f"ref {page}: hit {list(buf)}")
            else:
                faults += 1
                if len(buf) >= frames:
                    evicted = buf.pop(0)
                    buf.append(page)
                    steps.append(
                        f"ref {page}: FAULT evict {evicted} {list(buf)}"
                    )
                else:
                    buf.append(page)
                    steps.append(f"ref {page}: FAULT load {list(buf)}")
        return steps, faults

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a page replacement comparison problem.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        length = min(6 + difficulty * 2, 14)
        max_page = min(3 + difficulty, 7)
        refs = [self._rng.randint(0, max_page) for _ in range(length)]
        frames = self._rng.randint(2, 4)

        opt_steps, opt_faults = self._optimal(refs, frames)
        lru_steps, lru_faults = self._lru(refs, frames)

        steps = ["=== Optimal ==="] + opt_steps
        steps += ["=== LRU ==="] + lru_steps
        steps.append(f"OPT faults={opt_faults}, LRU faults={lru_faults}")

        ref_str = ",".join(str(r) for r in refs)
        problem = f"frames={frames}, refs=[{ref_str}]"
        return problem, {
            "steps": steps,
            "opt_faults": opt_faults,
            "lru_faults": lru_faults,
        }

    def _create_steps(self, solution_data: dict) -> list[str]:
        """Return the replacement simulation steps.

        Args:
            solution_data: All computed solution information.

        Returns:
            Step strings in execution order.
        """
        steps = solution_data["steps"]
        return steps[:6] if len(steps) > 6 else steps

    def _create_answer(self, solution_data: dict) -> str:
        """Return the fault counts.

        Args:
            solution_data: All computed solution information.

        Returns:
            Fault count comparison string.
        """
        d = solution_data
        return f"OPT={d['opt_faults']} faults, LRU={d['lru_faults']} faults"


# ---------------------------------------------------------------------------
# 8. File Allocation (tier 4)
# ---------------------------------------------------------------------------

@register
class FileAllocationGenerator(StepGenerator):
    """Compare contiguous, linked, and indexed file allocation.

    Given file size in blocks, compute access time for sequential
    and random access under each allocation strategy.
    """

    _STRATEGIES = [
        {
            "name": "contiguous",
            "seq_cost": "1 seek + n reads",
            "rand_cost": "1 seek + 1 read",
        },
        {
            "name": "linked",
            "seq_cost": "n seeks + n reads",
            "rand_cost": "i seeks + i reads (for block i)",
        },
        {
            "name": "indexed",
            "seq_cost": "1 index read + n reads",
            "rand_cost": "1 index read + 1 read",
        },
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "file_allocation"

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
            Task instruction string.
        """
        return "compare file allocation strategies for access cost"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a file allocation comparison problem.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        n_blocks = self._rng.randint(4, min(8 + difficulty * 2, 20))
        seek_time = self._rng.choice([5, 8, 10])
        read_time = self._rng.choice([1, 2])
        target_block = self._rng.randint(0, n_blocks - 1)

        results = {}
        steps = [f"file={n_blocks} blocks, seek={seek_time}ms, read={read_time}ms"]

        for strat in self._STRATEGIES:
            name = strat["name"]
            if name == "contiguous":
                seq = 1 * seek_time + n_blocks * read_time
                rand = 1 * seek_time + 1 * read_time
            elif name == "linked":
                seq = n_blocks * seek_time + n_blocks * read_time
                rand_seeks = target_block + 1
                rand = rand_seeks * seek_time + rand_seeks * read_time
            else:
                seq = 1 * read_time + n_blocks * read_time
                rand = 1 * read_time + 1 * read_time

            results[name] = {"seq": seq, "rand": rand}
            steps.append(f"{name}: seq={seq}ms, rand(blk {target_block})={rand}ms")

        problem = (
            f"blocks={n_blocks}, seek={seek_time}ms, read={read_time}ms, "
            f"target_block={target_block}"
        )
        return problem, {"steps": steps, "results": results}

    def _create_steps(self, solution_data: dict) -> list[str]:
        """Return the allocation comparison steps.

        Args:
            solution_data: All computed solution information.

        Returns:
            Step strings in execution order.
        """
        return solution_data["steps"]

    def _create_answer(self, solution_data: dict) -> str:
        """Return the cost comparison.

        Args:
            solution_data: All computed solution information.

        Returns:
            Best strategy for each access pattern.
        """
        r = solution_data["results"]
        best_seq = min(r, key=lambda k: r[k]["seq"])
        best_rand = min(r, key=lambda k: r[k]["rand"])
        return f"best_seq={best_seq}({r[best_seq]['seq']}ms), best_rand={best_rand}({r[best_rand]['rand']}ms)"
